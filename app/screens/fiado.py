from datetime import date
import math
import flet as ft
from screen_base import Pantalla
from datos import cuentas, cli_por_id, pagar_fiado
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
    paginador,
    barra_busqueda,
    aviso,
    moneda,
    paginar,
    leer_texto,
    sincronizar_texto,
    selector,
    sincronizar_combo,
)


class PantallaFiado(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Fiado")
        self._busqueda = ""
        self._solo_pendientes = True
        self._pagina = 1

    def actualizar(self):
        self.cargar_cuentas()

    def build(self):
        self.filtro_pendientes = ft.Switch(
            label="Solo pendientes",
            value=self._solo_pendientes,
            on_change=self._al_filtro,
        )
        barra = barra_busqueda(
            al_buscar=self._al_buscar,
            chips=(self.filtro_pendientes,),
            pista="Buscar cliente...",
        )

        self._columnas = [
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Pagado")),
            ft.DataColumn(ft.Text("Pendiente")),
            ft.DataColumn(ft.Text("Días")),
            ft.DataColumn(ft.Text("")),
        ]
        self._zona_tabla = ft.Container(expand=True)
        self._zona_paginador = ft.Container()

        self._cargar_cuentas()

        return ft.Column(
            [
                encabezado(
                    "Cuentas por cobrar",
                    al_refrescar=lambda _: self.cargar_cuentas(),
                    descripcion="Saldos pendientes, pagos recibidos y clientes.",
                ),
                barra,
                self._zona_tabla,
                self._zona_paginador,
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )


    def _al_buscar(self, texto):
        self._busqueda = texto or ""
        self._pagina = 1
        self.cargar_cuentas()

    def _al_filtro(self, e=None):
        valor = self._solo_pendientes
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
        self._solo_pendientes = bool(valor)
        self._pagina = 1
        self.cargar_cuentas()

    def _al_paginar(self, nueva):
        try:
            self._pagina = max(1, int(nueva or 1))
        except (TypeError, ValueError):
            self._pagina = 1
        self.cargar_cuentas()

    def _cargar_cuentas(self):
        paleta = colores.get()
        color_pagado = color_rol(paleta, "paid")
        color_pendiente = color_rol(paleta, "due")
        color_vencido = color_rol(paleta, "danger_text")
        solo_pendientes = bool(getattr(self, "_solo_pendientes", True))
        q = (getattr(self, "_busqueda", "") or "").lower()
        entradas = []
        for c in cuentas:
            pendiente = c["total"] - c["pagado"]
            if solo_pendientes and pendiente <= 0:
                continue
            cli = cli_por_id(c["cliente_id"])
            nombre = cli["nombre"] if cli else "?"
            if q and q not in nombre.lower():
                continue
            dias = (
                (date.today() - date.fromisoformat(c["created_at"])).days
                if c.get("created_at")
                else 0
            )
            entradas.append((dias, c, nombre, pendiente))
        entradas.sort(key=lambda item: (item[3] <= 0, -item[0]))
        filas = []
        for dias, c, nombre, pendiente in entradas:
            ccid = c["id"]

            if pendiente <= 0:
                color_estado = color_pagado
                icono_estado = ft.Icons.CHECK
            elif dias > 30:
                color_estado = color_vencido
                icono_estado = ft.Icons.WARNING
            else:
                color_estado = color_pendiente
                icono_estado = ft.Icons.SCHEDULE

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(nombre, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(moneda(c["total"]))),
                        ft.DataCell(ft.Text(moneda(c["pagado"]))),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(
                                        icono_estado,
                                        color=color_estado,
                                        size=ICON_SM,
                                    ),
                                    ft.Text(
                                        moneda(pendiente),
                                        color=color_estado,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=SP_4,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                        ),
                        ft.DataCell(ft.Text(f"{dias}d")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.Icons.HISTORY,
                                        tooltip="Ver historial de abonos",
                                        on_click=lambda _, x=ccid: self.ver_abonos(x),
                                    ),
                                    ft.FilledButton(
                                        "Pagar",
                                        on_click=lambda _, x=ccid: self.abrir_pago(x),
                                        style=ft.ButtonStyle(
                                            bgcolor=paleta.primary,
                                            color=paleta.on_primary,
                                        ),
                                    )
                                    if pendiente > 0
                                    else ft.Icon(ft.Icons.CHECK, color=color_pagado, size=ICON_SM),
                                ],
                                spacing=SP_4,
                                scroll=ft.ScrollMode.AUTO,
                            )
                        ),
                    ]
                )
            )
        pagina = int(getattr(self, "_pagina", 1) or 1)
        visibles, actual, total = paginar(filas, pagina)
        self._pagina = actual
        texto_vacio = "Sin deudas pendientes" if solo_pendientes else "Sin cuentas registradas"
        self._zona_tabla.content = tabla(self._columnas, visibles, mensaje_vacio=texto_vacio)
        self._zona_paginador.content = (
            paginador(actual, total, al_paginar=self._al_paginar) if total > 1 else None
        )

    def cargar_cuentas(self):
        self._cargar_cuentas()
        try:
            self._zona_tabla.update()
            self._zona_paginador.update()
        except Exception:
            self.rearmar()

    def abrir_pago(self, ccid):
        try:
            paleta = colores.get()
            c = next((x for x in cuentas if x["id"] == ccid), None)
            if not c:
                return
            deuda = c["total"] - c["pagado"]
            cli = cli_por_id(c["cliente_id"])
            nombre = cli["nombre"] if cli else "?"
            campo_monto = campo_texto(
                label="Monto $", value=str(deuda), keyboard_type=ft.KeyboardType.NUMBER
            )
            sincronizar_texto(campo_monto)
            combo_medio = selector(
                label="Medio de pago",
                value="efectivo",
                options=[
                    ft.dropdown.Option("efectivo", "Efectivo"),
                    ft.dropdown.Option("transferencia", "Transferencia"),
                ],
                expand=True,
            )
            sincronizar_combo(combo_medio)

            def confirmar(e):
                try:
                    try:
                        monto = float((leer_texto(campo_monto, e) or "").replace(",", ".") or 0)
                    except (TypeError, ValueError):
                        aviso(self.pagina, "Monto inválido", rol="warning")
                        return
                    if not math.isfinite(monto) or monto <= 0:
                        aviso(self.pagina, "Monto inválido", rol="warning")
                        return
                    if monto > deuda:
                        aviso(
                            self.pagina,
                            f"El monto supera la deuda ({moneda(deuda)})",
                            rol="warning",
                        )
                        return
                    monto = min(monto, deuda)
                    pagar_fiado(ccid, monto, combo_medio.value or "efectivo")
                    self.cerrar_dialogo(ventana)
                    self.cargar_cuentas()
                    self.mostrar_alerta(f"Pago de {moneda(monto)} registrado a {nombre}")
                except Exception as ex:
                    print(f"Error confirmar pago: {ex}")
                    aviso(
                        self.pagina,
                        "No se pudo registrar el pago. Revisá el monto y volvé a intentar.",
                        rol="danger",
                    )

            ventana = dialogo(
                "Registrar pago",
                ft.Column(
                    [
                        ft.Text(f"Debe {moneda(deuda)} de {moneda(c['total'])}"),
                        campo_monto,
                        combo_medio,
                    ],
                    spacing=SP_12,
                    tight=True,
                ),
                acciones=[
                    ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo(ventana)),
                    ft.FilledButton(
                        "Pagar",
                        on_click=confirmar,
                        style=ft.ButtonStyle(
                            bgcolor=paleta.primary,
                            color=paleta.on_primary,
                        ),
                    ),
                ],
            )
            self.abrir_dialogo(ventana)
        except Exception as ex:
            print(f"Error abrir_pago: {ex}")

    def ver_abonos(self, ccid):
        cuenta = next((fila for fila in cuentas if fila["id"] == ccid), None)
        if not cuenta:
            return
        cli = cli_por_id(cuenta["cliente_id"])
        nombre = cli["nombre"] if cli else "Cliente"
        paleta = colores.get()
        lineas = []
        heredado = cuenta.get("pagado_sin_detalle", 0)
        if heredado:
            lineas.append(
                ft.Text(
                    f"{moneda(heredado)} ya figuraban pagados; la copia anterior no guardaba fecha ni medio.",
                    color=paleta.text_muted,
                )
            )
        for abono in sorted(cuenta.get("abonos", []), key=lambda fila: (fila["fecha"], fila["id"]), reverse=True):
            medio = "Efectivo" if abono["medio_pago"] == "efectivo" else "Transferencia"
            lineas.append(
                ft.Row(
                    [
                        ft.Text(f"{abono['fecha']} · {medio}", expand=True),
                        ft.Text(moneda(abono["monto"]), weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        if not lineas:
            lineas.append(ft.Text("Todavía no hay abonos registrados."))
        ventana = dialogo(
            f"Abonos de {nombre}",
            ft.Container(
                content=ft.Column(lineas, spacing=SP_8, scroll=ft.ScrollMode.AUTO),
                width=440,
                height=320,
            ),
            acciones=[ft.TextButton("Cerrar", on_click=lambda _: self.cerrar_dialogo(ventana))],
        )
        self.abrir_dialogo(ventana)


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
