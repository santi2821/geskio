import flet as ft
from screen_base import Pantalla
from datos import (
    clientes,
    ventas,
    cuentas,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente,
)
from theme import (
    ICON_SM,
    SP_4,
    SP_8,
    SP_10,
    SP_12,
    colores,
    color_rol,
)
from widgets import (
    campo_texto,
    dialogo,
    tabla,
    encabezado,
    seccion,
    paginador,
    barra_busqueda,
    confirmar_eliminar,
    aviso,
    moneda,
    paginar,
    sincronizar_texto,
)


class PantallaClientes(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Clientes")
        self._busqueda = ""
        self._solo_deuda = False
        self._pagina = 1

    def actualizar(self):
        self.filtrar_datos()

    def build(self):
        paleta = colores.get()
        self._columnas = [
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Compras")),
            ft.DataColumn(ft.Text("Debe")),
            ft.DataColumn(ft.Text("")),
        ]
        self._zona_tabla = ft.Container(expand=True)
        self._zona_paginador = ft.Container()
        self._chip_deuda = ft.Switch(
            label="Con deuda",
            value=self._solo_deuda,
            on_change=self._al_filtro_deuda,
        )
        barra = barra_busqueda(
            al_buscar=self._al_buscar,
            chips=(self._chip_deuda,),
            pista="Buscar cliente...",
        )

        self.campo_nombre = campo_texto(label="Nombre", expand=True)
        self.campo_telefono = campo_texto(label="Teléfono")
        for _campo in (self.campo_nombre, self.campo_telefono):
            sincronizar_texto(_campo)

        form = ft.Row(
            [
                self.campo_nombre,
                self.campo_telefono,
                ft.FilledButton(
                    "Agregar",
                    on_click=self.guardar_nuevo,
                    style=ft.ButtonStyle(bgcolor=paleta.primary, color=paleta.on_primary),
                ),
            ],
            spacing=SP_8,
        )

        self._cargar_tabla()

        return ft.Column(
            [
                encabezado(
                    "Directorio de clientes",
                    al_refrescar=lambda _: self.filtrar_datos(),
                    descripcion="Personas y datos de contacto de tu comercio.",
                ),
                barra,
                self._zona_tabla,
                self._zona_paginador,
                seccion("Nuevo cliente", form),
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )


    def _al_buscar(self, texto):
        self._busqueda = texto or ""
        self._pagina = 1
        self.filtrar_datos()

    def _al_filtro_deuda(self, e=None):
        valor = self._solo_deuda
        try:
            if e is not None:
                dato = getattr(e, "data", None)
                if isinstance(dato, bool):
                    valor = dato
                elif dato in ("true", "false"):
                    valor = dato == "true"
                else:
                    control = getattr(e, "control", None)
                    if control is not None and control.value is not None:
                        valor = bool(control.value)
        except Exception:
            pass
        self._solo_deuda = bool(valor)
        self._pagina = 1
        self.filtrar_datos()

    def _al_paginar(self, nueva):
        try:
            self._pagina = max(1, int(nueva or 1))
        except (TypeError, ValueError):
            self._pagina = 1
        self.filtrar_datos()


    def _cargar_tabla(self):
        paleta = colores.get()
        color_deuda = color_rol(paleta, "danger_text")
        q = (getattr(self, "_busqueda", "") or "").lower()
        solo_deuda = bool(getattr(self, "_solo_deuda", False))
        items = []
        for c in clientes:
            if q and q not in c["nombre"].lower() and q not in c.get("telefono", ""):
                continue
            debe = sum(x["total"] - x["pagado"] for x in cuentas if x["cliente_id"] == c["id"])
            if solo_deuda and debe <= 0:
                continue
            items.append(c)
        items.sort(key=lambda c: c["nombre"].lower())
        filas = []
        for c in items:
            compras = len([v for v in ventas if v.get("cliente_id") == c["id"]])
            debe = sum(x["total"] - x["pagado"] for x in cuentas if x["cliente_id"] == c["id"])
            cid = c["id"]

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(c["nombre"], weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(c.get("telefono", "—"))),
                        ft.DataCell(ft.Text(str(compras))),
                        ft.DataCell(
                            ft.Text(
                                moneda(debe),
                                color=color_deuda if debe > 0 else paleta.text_muted,
                                weight=ft.FontWeight.BOLD if debe > 0 else None,
                            )
                            if debe > 0
                            else ft.Text("—", color=paleta.text_muted)
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        icon_size=ICON_SM,
                                        tooltip="Editar",
                                        on_click=lambda _, x=cid: self.editar_cliente(x),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        icon_size=ICON_SM,
                                        tooltip="Eliminar",
                                        icon_color=paleta.danger,
                                        on_click=lambda _, x=cid: self.eliminar_cliente(x),
                                    ),
                                ],
                                spacing=SP_4,
                            )
                        ),
                    ]
                )
            )
        pagina = int(getattr(self, "_pagina", 1) or 1)
        visibles, actual, total = paginar(filas, pagina)
        self._pagina = actual
        filtro_activo = bool(q or solo_deuda)
        texto_vacio = "Sin resultados" if filtro_activo else "Sin clientes"
        self._zona_tabla.content = tabla(self._columnas, visibles, mensaje_vacio=texto_vacio)
        self._zona_paginador.content = (
            paginador(actual, total, al_paginar=self._al_paginar) if total > 1 else None
        )

    def filtrar_datos(self):
        self._cargar_tabla()
        try:
            self._zona_tabla.update()
            self._zona_paginador.update()
        except Exception:
            self.rearmar()


    def guardar_nuevo(self, e=None):
        try:
            nombre = self.campo_nombre.value.strip()
            if not nombre:
                aviso(self.pagina, "Poné un nombre", rol="warning")
                return
            crear_cliente(nombre, self.campo_telefono.value.strip())
            self.campo_nombre.value = ""
            self.campo_telefono.value = ""
            self.filtrar_datos()
            self.mostrar_alerta("Cliente agregado")
        except Exception as ex:
            print(f"Error guardar_nuevo: {ex}")


    def editar_cliente(self, cid):
        try:
            c = next((x for x in clientes if x["id"] == cid), None)
            if not c:
                return

            campo_nombre = campo_texto(label="Nombre", value=c["nombre"])
            campo_telefono = campo_texto(label="Teléfono", value=c.get("telefono", ""))
            for _campo in (campo_nombre, campo_telefono):
                sincronizar_texto(_campo)

            def guardar(e):
                try:
                    actualizar_cliente(
                        cid,
                        campo_nombre.value.strip() or c["nombre"],
                        campo_telefono.value.strip(),
                    )
                    self.cerrar_dialogo(ventana)
                    self.filtrar_datos()
                    self.mostrar_alerta("Cliente actualizado")
                except Exception as ex:
                    print(f"Error guardar editar cliente: {ex}")

            ventana = dialogo(
                "Editar cliente",
                ft.Column([campo_nombre, campo_telefono], spacing=SP_12, tight=True),
                acciones=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(ventana)),
                    ft.FilledButton("Guardar", on_click=guardar),
                ],
            )
            self.abrir_dialogo(ventana)
        except Exception as ex:
            print(f"Error editar_cliente: {ex}")


    def eliminar_cliente(self, cid):
        try:
            c = next((x for x in clientes if x["id"] == cid), None)
            if not c:
                return

            debe = sum(x["total"] - x["pagado"] for x in cuentas if x["cliente_id"] == cid)
            if debe > 0:
                aviso(
                    self.pagina,
                    f"No se puede eliminar: {c['nombre']} debe {moneda(debe)} — cobrá el fiado primero",
                    rol="warning",
                )
                return
            if any(v.get("cliente_id") == cid for v in ventas) or any(
                x.get("cliente_id") == cid for x in cuentas
            ):
                aviso(
                    self.pagina,
                    f"No se puede eliminar a {c['nombre']}: conserva historial de compras o pagos.",
                    rol="warning",
                )
                return

            def confirmar(e):
                try:
                    if not eliminar_cliente(cid):
                        self.mostrar_alerta("No se pudo eliminar el cliente con historial asociado")
                        return
                    self.filtrar_datos()
                    self.mostrar_alerta(f"'{c['nombre']}' eliminado")
                except Exception as ex:
                    print(f"Error confirmar eliminar cliente: {ex}")

            mensaje = f"¿Eliminar a '{c['nombre']}'?"
            mensaje += "\nNo se puede deshacer."

            confirmar_eliminar(
                self.pagina,
                confirmar,
                nombre=c["nombre"],
                titulo="Eliminar cliente",
                mensaje=mensaje,
            )
        except Exception as ex:
            print(f"Error eliminar_cliente: {ex}")


    @property
    def tabla_datos(self):
        contenido = getattr(getattr(self, "_zona_tabla", None), "content", None)
        if isinstance(contenido, ft.DataTable):
            return contenido
        return ft.DataTable(
            columns=list(getattr(self, "_columnas", []) or []),
            rows=[],
            expand=True,
        )

    @property
    def campo_buscar(self):
        campo = campo_texto(hint_text="Buscar cliente...", expand=True)
        try:
            campo.value = getattr(self, "_busqueda", "") or ""
        except Exception:
            pass
        return campo
