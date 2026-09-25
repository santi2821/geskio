import flet as ft
from screen_base import Pantalla
from datos import (
    productos,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
    ajustar_stock,
    margen,
)
from theme import (
    ICON_SM,
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
    paginador,
    barra_busqueda,
    confirmar_eliminar,
    aviso,
    moneda,
    paginar,
    sincronizar_texto,
)


class PantallaStock(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Stock")
        self._busqueda = ""
        self._solo_bajo = False
        self._pagina = 1

    def actualizar(self):
        self.filtrar_datos()

    def build(self):
        self._columnas = [
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Costo")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Margen")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Mínimo")),
            ft.DataColumn(ft.Text("Acciones")),
        ]
        # zonas tipo Container: refrescar = cambiar .content + update()
        self._zona_tabla = ft.Container(expand=True)
        self._zona_paginador = ft.Container()
        self._chip_bajo = ft.Switch(
            label="Solo bajo stock",
            value=self._solo_bajo,
            on_change=self._al_filtro_bajo,
        )
        barra = barra_busqueda(
            al_buscar=self._al_buscar,
            chips=(self._chip_bajo,),
            pista="Buscar producto...",
        )

        self.campo_nombre = campo_texto(label="Nombre")
        self.campo_costo = campo_texto(label="Costo $", keyboard_type=ft.KeyboardType.NUMBER)
        self.campo_precio = campo_texto(label="Precio $", keyboard_type=ft.KeyboardType.NUMBER)
        self.campo_stock = campo_texto(
            label="Stock", value="0", keyboard_type=ft.KeyboardType.NUMBER
        )
        self.campo_minimo = campo_texto(
            label="Mínimo", value="5", keyboard_type=ft.KeyboardType.NUMBER
        )
        for _campo in (
            self.campo_nombre,
            self.campo_costo,
            self.campo_precio,
            self.campo_stock,
            self.campo_minimo,
        ):
            sincronizar_texto(_campo)
        self.campo_nombre.expand = False
        for _campo in (
            self.campo_costo,
            self.campo_precio,
            self.campo_stock,
            self.campo_minimo,
        ):
            _campo.expand = True

        self._mensaje_nuevo = ft.Text(color=color_rol(colores.get(), "danger_text"))
        formulario_nuevo = ft.Column(
            [
                self.campo_nombre,
                ft.Row([self.campo_costo, self.campo_precio], spacing=SP_8),
                ft.Row([self.campo_stock, self.campo_minimo], spacing=SP_8),
                self._mensaje_nuevo,
            ],
            tight=True,
            spacing=SP_12,
        )
        self._dialogo_nuevo = dialogo(
            "Nuevo producto",
            ft.Container(content=formulario_nuevo, width=420),
            acciones=[
                ft.TextButton("Cancelar", on_click=self._cancelar_nuevo),
                ft.FilledButton("Guardar producto", on_click=self.guardar_nuevo),
            ],
        )
        boton_nuevo = ft.FilledButton(
            "Nuevo producto",
            on_click=lambda _: self.abrir_dialogo(self._dialogo_nuevo),
        )

        # el build renderiza los datos actuales: entran montados con la pantalla
        self._cargar_tabla()

        return ft.Column(
            [
                encabezado(
                    "Inventario",
                    acciones=(boton_nuevo,),
                    al_refrescar=lambda _: self.filtrar_datos(),
                    descripcion="Productos, precios y disponibilidad de inventario.",
                ),
                barra,
                self._zona_tabla,
                self._zona_paginador,
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _cancelar_nuevo(self, e=None):
        for campo in (self.campo_nombre, self.campo_costo, self.campo_precio):
            campo.value = ""
        self.campo_stock.value = "0"
        self.campo_minimo.value = "5"
        self._limpiar_errores(
            {
                "nombre": self.campo_nombre,
                "costo": self.campo_costo,
                "precio": self.campo_precio,
                "stock": self.campo_stock,
                "minimo": self.campo_minimo,
            },
            self._mensaje_nuevo,
        )
        self.cerrar_dialogo(self._dialogo_nuevo)

    # ─── busqueda + paginador ───────────────────────────────────────

    def _al_buscar(self, texto):
        self._busqueda = texto or ""
        self._pagina = 1
        self.filtrar_datos()

    def _al_filtro_bajo(self, e=None):
        # el .value del widget llega viejo; el estado nuevo viene en el evento
        valor = self._solo_bajo
        try:
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
        self._solo_bajo = bool(valor)
        self._pagina = 1
        self.filtrar_datos()

    def _al_paginar(self, nueva):
        try:
            self._pagina = max(1, int(nueva or 1))
        except (TypeError, ValueError):
            self._pagina = 1
        self.filtrar_datos()

    # ─── filtro view-side: filtrar → ordenar → paginar ──────────────

    def _cargar_tabla(self):
        # arma la tabla filtrada en las zonas, sin update
        paleta = colores.get()
        color_bajo = color_rol(paleta, "danger_text")
        q = (getattr(self, "_busqueda", "") or "").lower()
        solo_bajo = bool(getattr(self, "_solo_bajo", False))
        items = []
        for p in productos:
            if q and q not in p["nombre"].lower():
                continue
            if solo_bajo and not p["stock"] <= p["minimo"]:
                continue
            items.append(p)
        items.sort(key=lambda p: p["nombre"].lower())
        filas = []
        for p in items:
            m = margen(p["costo"], p["precio"])
            bajo = p["stock"] <= p["minimo"]
            pid = p["id"]

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p["nombre"], weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(moneda(p["costo"]))),
                        ft.DataCell(ft.Text(moneda(p["precio"]))),
                        ft.DataCell(ft.Text(f"{m}%")),
                        ft.DataCell(
                            ft.Text(
                                str(p["stock"]),
                                color=color_bajo if bajo else None,
                                weight=ft.FontWeight.BOLD if bajo else None,
                            )
                        ),
                        ft.DataCell(ft.Text(str(p["minimo"]))),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        icon_size=ICON_SM,
                                        tooltip="Editar",
                                        on_click=lambda _, x=pid: self.editar_producto(x),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.UNFOLD_MORE,
                                        icon_size=ICON_SM,
                                        tooltip="Ajustar stock",
                                        on_click=lambda _, x=pid: self.ajustar_stock_dialog(x),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        icon_size=ICON_SM,
                                        tooltip="Eliminar",
                                        icon_color=paleta.danger,
                                        on_click=lambda _, x=pid: self.eliminar_producto(x),
                                    ),
                                ],
                                spacing=SP_8,
                            )
                        ),
                    ]
                )
            )
        pagina = int(getattr(self, "_pagina", 1) or 1)
        visibles, actual, total = paginar(filas, pagina)
        self._pagina = actual
        self._zona_tabla.content = tabla(self._columnas, visibles, mensaje_vacio="Sin resultados")
        self._zona_paginador.content = (
            paginador(actual, total, al_paginar=self._al_paginar) if total > 1 else None
        )

    def filtrar_datos(self):
        # refresco post-accion: mismo render + update de las zonas montadas
        self._cargar_tabla()
        try:
            self._zona_tabla.update()
            self._zona_paginador.update()
        except Exception:
            self.rearmar()

    # ─── nuevo producto ─────────────────────────────────────────────

    def guardar_nuevo(self, e=None):
        campos = {
            "nombre": self.campo_nombre,
            "costo": self.campo_costo,
            "precio": self.campo_precio,
            "stock": self.campo_stock,
            "minimo": self.campo_minimo,
        }
        self._limpiar_errores(campos, self._mensaje_nuevo)
        try:
            nombre = (self.campo_nombre.value or "").strip()
            if not nombre:
                self._marcar_error(campos, "Poné un nombre", "nombre", self._mensaje_nuevo)
                return
            for clave, campo in (
                ("costo", self.campo_costo),
                ("precio", self.campo_precio),
            ):
                if not (campo.value or "").strip():
                    etiqueta = "costo" if clave == "costo" else "precio"
                    self._marcar_error(campos, f"Ingresá el {etiqueta}", clave, self._mensaje_nuevo)
                    return
            numericos = {}
            for clave, campo, defecto in (
                ("costo", self.campo_costo, 0),
                ("precio", self.campo_precio, 0),
                ("stock", self.campo_stock, 0),
                ("minimo", self.campo_minimo, 5),
            ):
                try:
                    numericos[clave] = float(campo.value or defecto)
                except (TypeError, ValueError):
                    self._marcar_error(
                        campos,
                        "Revisá el valor numérico",
                        clave,
                        self._mensaje_nuevo,
                    )
                    return
            costo, precio = numericos["costo"], numericos["precio"]
            stock, minimo = numericos["stock"], numericos["minimo"]
            aviso_barato = precio < costo
            try:
                crear_producto(nombre, costo, precio, stock, minimo)
            except ValueError as ex:
                self._marcar_error(campos, str(ex), feedback=self._mensaje_nuevo)
                return
            for _campo in (
                self.campo_nombre,
                self.campo_costo,
                self.campo_precio,
            ):
                _campo.value = ""
                _campo.update()
            self.campo_stock.value = "0"
            self.campo_stock.update()
            self.campo_minimo.value = "5"
            self.campo_minimo.update()
            self.cerrar_dialogo(self._dialogo_nuevo)
            self.filtrar_datos()
            if aviso_barato:
                self.mostrar_alerta("Ojo: el precio es menor al costo")
            else:
                self.mostrar_alerta("Producto creado")
        except Exception as ex:
            print(f"Error guardar_nuevo: {ex}")

    # ─── editar producto ────────────────────────────────────────────

    def editar_producto(self, pid):
        try:
            p = next((x for x in productos if x["id"] == pid), None)
            if not p:
                return

            campo_nombre = campo_texto(label="Nombre", value=p["nombre"])
            campo_costo = campo_texto(
                label="Costo $",
                value=str(p["costo"]),
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            campo_precio = campo_texto(
                label="Precio $",
                value=str(p["precio"]),
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            campo_stock = campo_texto(
                label="Stock",
                value=str(p["stock"]),
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            campo_minimo = campo_texto(
                label="Mínimo",
                value=str(p["minimo"]),
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            for _campo in (
                campo_nombre,
                campo_costo,
                campo_precio,
                campo_stock,
                campo_minimo,
            ):
                sincronizar_texto(_campo)
            mensaje_error = ft.Text(color=color_rol(colores.get(), "danger_text"))

            def guardar(e):
                campos = {
                    "nombre": campo_nombre,
                    "costo": campo_costo,
                    "precio": campo_precio,
                    "stock": campo_stock,
                    "minimo": campo_minimo,
                }
                self._limpiar_errores(campos, mensaje_error)
                try:
                    actualizar_producto(
                        pid,
                        (campo_nombre.value or "").strip() or p["nombre"],
                        float(campo_costo.value or 0),
                        float(campo_precio.value or 0),
                        float(campo_stock.value or 0),
                        float(campo_minimo.value or 5),
                    )
                    self.cerrar_dialogo(ventana)
                    self.filtrar_datos()
                    self.mostrar_alerta("Producto actualizado")
                except ValueError as ex:
                    self._marcar_error(
                        campos,
                        str(ex) or "Revisá los valores numéricos",
                        feedback=mensaje_error,
                    )
                except Exception as ex:
                    print(f"Error al guardar: {ex}")

            ventana = dialogo(
                "Editar producto",
                ft.Column(
                    [
                        campo_nombre,
                        ft.Row([campo_costo, campo_precio], spacing=SP_8),
                        ft.Row([campo_stock, campo_minimo], spacing=SP_8),
                        mensaje_error,
                    ],
                    spacing=SP_12,
                    tight=True,
                ),
                acciones=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(ventana)),
                    ft.ElevatedButton("Guardar", on_click=guardar),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.abrir_dialogo(ventana)
        except Exception as ex:
            print(f"Error editar_producto: {ex}")

    # ─── ajustar stock (port main-only a arquitectura 0.84) ──────────

    def ajustar_stock_dialog(self, pid):
        try:
            p = next((x for x in productos if x["id"] == pid), None)
            if not p:
                return

            texto_actual = ft.Text(
                f"Stock actual: {p['stock']}", size=16, weight=ft.FontWeight.BOLD
            )
            campo = campo_texto(label="Cantidad", value="1", keyboard_type=ft.KeyboardType.NUMBER)
            sincronizar_texto(campo)

            def aplicar(cantidad):
                try:
                    ajustar_stock(pid, cantidad)
                    texto_actual.value = f"Stock actual: {p['stock']}"
                    campo.value = "1"
                    self.filtrar_datos()
                    self.pagina.update()
                except ValueError as ex:
                    self.mostrar_alerta(str(ex) or f"Solo hay {p['stock']} en stock")
                except Exception as ex:
                    print(f"Error aplicar: {ex}")

            def confirmar(e):
                try:
                    try:
                        cantidad = int((campo.value or "0").strip())
                    except (TypeError, ValueError, AttributeError):
                        self.mostrar_alerta("Cantidad inválida")
                        return
                    if cantidad == 0:
                        return
                    ajustar_stock(pid, cantidad)
                    self.cerrar_dialogo(ventana)
                    self.filtrar_datos()
                    self.mostrar_alerta(f"Stock de {p['nombre']} actualizado")
                except ValueError as ex:
                    self.mostrar_alerta(str(ex) or "Cantidad inválida")
                except Exception as ex:
                    print(f"Error confirmar: {ex}")

            ventana = dialogo(
                f"Ajustar stock — {p['nombre']}",
                ft.Column(
                    [
                        texto_actual,
                        ft.Row(
                            [
                                ft.ElevatedButton("-10", on_click=lambda e: aplicar(-10)),
                                ft.ElevatedButton("-1", on_click=lambda e: aplicar(-1)),
                                campo,
                                ft.ElevatedButton("+1", on_click=lambda e: aplicar(1)),
                                ft.ElevatedButton("+10", on_click=lambda e: aplicar(10)),
                            ],
                            spacing=SP_8,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                    ],
                    spacing=SP_12,
                    tight=True,
                ),
                acciones=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.cerrar_dialogo(ventana)),
                    ft.ElevatedButton("Aplicar y cerrar", on_click=confirmar),
                ],
            )
            self.abrir_dialogo(ventana)
        except Exception as ex:
            print(f"Error ajustar_stock_dialog: {ex}")

    # ─── eliminar ───────────────────────────────────────────────────

    def eliminar_producto(self, pid):
        try:
            p = next((x for x in productos if x["id"] == pid), None)
            if not p:
                return

            def confirmar(e):
                try:
                    ok = eliminar_producto(pid)
                    self.filtrar_datos()
                    if ok:
                        self.mostrar_alerta(f"'{p['nombre']}' eliminado")
                    else:
                        self.mostrar_alerta("No se puede eliminar: tiene ventas asociadas")
                except Exception as ex:
                    print(f"Error confirmar eliminar: {ex}")

            confirmar_eliminar(
                self.pagina,
                confirmar,
                nombre=p["nombre"],
                titulo="Eliminar producto",
            )
        except Exception as ex:
            print(f"Error eliminar_producto: {ex}")

    # ─── helpers (heredados de Screen, mantienen compatibilidad) ───

    def _limpiar_errores(self, campos, feedback=None):
        for campo in campos.values():
            campo.error_text = None
            try:
                campo.update()
            except Exception:
                pass
        if feedback is not None:
            feedback.value = ""
            try:
                feedback.update()
            except Exception:
                pass

    def _marcar_error(self, campos, mensaje, preferido=None, feedback=None):
        texto = mensaje.lower()
        if "nombre" in texto or "poné" in texto:
            afectados = ("nombre",)
        elif "costo" in texto:
            afectados = ("costo",)
        elif "precio" in texto:
            afectados = ("precio",)
        elif "stock" in texto and "mínimo" in texto:
            afectados = ("stock", "minimo")
        elif "stock" in texto:
            afectados = ("stock",)
        elif "mínimo" in texto:
            afectados = ("minimo",)
        else:
            afectados = (preferido,) if preferido else tuple(campos)
        for clave in afectados:
            campo = campos.get(clave)
            if campo is not None:
                campo.error_text = mensaje
                try:
                    campo.update()
                except Exception:
                    pass
        campo = campos.get(afectados[0])
        if feedback is not None:
            feedback.value = mensaje
            try:
                feedback.update()
            except Exception:
                pass
        if campo is not None:
            try:
                campo.focus()
            except Exception:
                pass

    # ─── helpers: heredados de Pantalla (dual 0.84 runtime + Mock/0.28.3).
    # mostrar_alerta/abrir_dialogo/cerrar_dialogo viven en screen_base.
    # Se conservan _limpiar_errores/_marcar_error propios del formulario newer.

    # ─── compat dimensionamiento main-only (tests antiguos) ──────────
    # La UI newer pagina la tabla en _zona_tabla; se expone tabla_datos como
    # espejo DataTable y campo_buscar para que la suite 0.28.3 siga pasando.
    @property
    def tabla_datos(self):  # type: ignore[override]
        contenido = getattr(getattr(self, "_zona_tabla", None), "content", None)
        if isinstance(contenido, ft.DataTable):
            return contenido
        espejo = ft.DataTable(
            columns=list(getattr(self, "_columnas", []) or []),
            rows=(contenido.rows if isinstance(contenido, ft.DataTable) else []),
            expand=True,
        )
        return espejo

    @property
    def campo_buscar(self):  # type: ignore[override]
        campo = campo_texto(hint_text="Buscar producto...", expand=True)
        try:
            campo.value = getattr(self, "_busqueda", "") or ""
        except Exception:
            pass
        return campo
