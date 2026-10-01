"""Listado de ventas del negocio y vista de cada comprobante."""

from datetime import date, timedelta

import flet as ft

from datos import cli_por_id, ventas
from screen_base import Pantalla
from theme import FS_12, FS_14, FS_16, SP_8, SP_10, SP_12, colores
from widgets import (
    aviso,
    barra_busqueda,
    campo_texto,
    dialogo,
    encabezado,
    moneda,
    paginador,
    paginar,
    selector,
    sincronizar_combo,
    tabla,
)


_MEDIOS = {
    "": "Todos los medios",
    "efectivo": "Efectivo",
    "transferencia": "Transferencia",
    "fiado": "Fiado",
}


def filtrar_ventas(lista, periodo="todas", medio="", busqueda="", hoy=None):
    hoy = hoy or date.today()
    desde = hoy if periodo == "hoy" else hoy - timedelta(days=6) if periodo == "7dias" else None
    texto = (busqueda or "").strip().casefold()
    resultado = []
    for venta in lista or []:
        fecha = venta.get("fecha", "")
        if desde and not (desde.isoformat() <= fecha <= hoy.isoformat()):
            continue
        if medio and venta.get("pago") != medio:
            continue
        cliente = cli_por_id(venta.get("cliente_id", ""))
        nombre = cliente.get("nombre", "Mostrador") if cliente else "Mostrador"
        if texto and texto not in nombre.casefold():
            continue
        resultado.append(venta)
    return sorted(resultado, key=lambda venta: (venta.get("fecha", ""), venta.get("id", "")), reverse=True)


class PantallaHistorialVentas(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Ventas")
        self._periodo = "todas"
        self._medio = ""
        self._busqueda = ""
        self._pagina = 1

    def build(self):
        paleta = colores.get()
        self._filtro_periodo = selector(
            label="Fecha",
            value=self._periodo,
            options=[
                ft.dropdown.Option("hoy", "Hoy"),
                ft.dropdown.Option("7dias", "Últimos 7 días"),
                ft.dropdown.Option("todas", "Todas"),
            ],
            width=190,
            on_select=self._cambio_periodo,
        )
        self._filtro_medio = selector(
            label="Medio de pago",
            value=self._medio,
            options=[ft.dropdown.Option(k, v) for k, v in _MEDIOS.items()],
            width=200,
            on_select=self._cambio_medio,
        )
        sincronizar_combo(self._filtro_periodo)
        sincronizar_combo(self._filtro_medio)
        filtros = barra_busqueda(
            al_buscar=self._cambio_busqueda,
            chips=(self._filtro_periodo, self._filtro_medio),
            pista="Buscar cliente...",
        )
        self._resumen = ft.Text(size=FS_14, color=paleta.text_muted)
        self._zona_tabla = ft.Container(expand=True)
        self._zona_paginador = ft.Container()
        self._columnas = [
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Pago")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Detalle")),
        ]
        self._cargar()
        return ft.Column(
            [
                encabezado(
                    "Historial de ventas",
                    al_refrescar=lambda _: self.actualizar(),
                    descripcion="Revisá operaciones registradas y el detalle de sus productos.",
                ),
                filtros,
                self._resumen,
                self._zona_tabla,
                self._zona_paginador,
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _cambio_periodo(self, e):
        self._periodo = getattr(e, "data", None) or self._filtro_periodo.value or "todas"
        self._pagina = 1
        self._refrescar()

    def _cambio_medio(self, e):
        self._medio = getattr(e, "data", None) or self._filtro_medio.value or ""
        self._pagina = 1
        self._refrescar()

    def _cambio_busqueda(self, texto):
        self._busqueda = texto or ""
        self._pagina = 1
        self._refrescar()

    def _cargar(self):
        resultados = filtrar_ventas(ventas, self._periodo, self._medio, self._busqueda)
        total = sum(float(v.get("total", 0)) for v in resultados)
        self._resumen.value = f"{len(resultados)} ventas · {moneda(total)} en el filtro"
        filas = []
        for venta in resultados:
            cliente = cli_por_id(venta.get("cliente_id", ""))
            nombre = cliente.get("nombre", "Mostrador") if cliente else "Mostrador"
            try:
                fecha = date.fromisoformat(venta["fecha"]).strftime("%d/%m/%Y")
            except (KeyError, TypeError, ValueError):
                fecha = venta.get("fecha", "—")
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(fecha)),
                        ft.DataCell(ft.Text(nombre)),
                        ft.DataCell(ft.Text(_MEDIOS.get(venta.get("pago"), venta.get("pago", "—")))),
                        ft.DataCell(ft.Text(moneda(venta.get("total", 0)))),
                        ft.DataCell(
                            ft.IconButton(
                                ft.Icons.RECEIPT_LONG,
                                tooltip="Ver detalle de la venta",
                                on_click=lambda _, registro=venta: self._ver_detalle(registro),
                            )
                        ),
                    ]
                )
            )
        pagina_filas, actual, paginas = paginar(filas, self._pagina)
        self._pagina = actual
        vacio = (
            "Todavía no hay ventas registradas"
            if not ventas
            else "No hay ventas para los filtros elegidos"
        )
        self._zona_tabla.content = tabla(self._columnas, pagina_filas, mensaje_vacio=vacio)
        self._zona_paginador.content = paginador(actual, paginas, self._ir_pagina)

    def _refrescar(self):
        self._cargar()
        try:
            self._zona_tabla.update()
            self._zona_paginador.update()
            self._resumen.update()
        except Exception:
            self.rearmar()

    def _ir_pagina(self, pagina):
        self._pagina = pagina
        self._refrescar()

    def actualizar(self):
        if hasattr(self, "_zona_tabla"):
            self._refrescar()
        else:
            self.rearmar()

    def _ver_detalle(self, venta):
        cliente = cli_por_id(venta.get("cliente_id", ""))
        nombre = cliente.get("nombre", "Mostrador") if cliente else "Mostrador"
        renglones = []
        for item in venta.get("items", []):
            cantidad = item.get("cantidad", 0)
            precio = item.get("precio", 0)
            renglones.append(
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(item.get("nombre", "Producto"), weight=ft.FontWeight.W_600),
                                ft.Text(f"{cantidad} × {moneda(precio)}", size=FS_12, color=colores.get().text_muted),
                            ],
                            spacing=SP_8,
                            expand=True,
                        ),
                        ft.Text(moneda(cantidad * precio), weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        if not renglones:
            renglones.append(ft.Text("Esta venta no tiene detalle de productos."))
        cuerpo = ft.Column(
            [
                ft.Text(f"{nombre} · {_MEDIOS.get(venta.get('pago'), '—')}", size=FS_14),
                ft.Divider(),
                *renglones,
                ft.Divider(),
                ft.Row(
                    [ft.Text("Total", weight=ft.FontWeight.BOLD), ft.Text(moneda(venta.get("total", 0)), weight=ft.FontWeight.BOLD)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=SP_8,
            scroll=ft.ScrollMode.AUTO,
            height=360,
        )
        ventana = dialogo(
            "Detalle de venta",
            ft.Container(content=cuerpo, width=500),
            acciones=[ft.TextButton("Cerrar", on_click=lambda _: self.cerrar_dialogo(ventana))],
        )
        self.abrir_dialogo(ventana)
