"""Trazabilidad de ajustes, ventas y anulaciones que cambian el inventario."""

import flet as ft

from datos import movimientos_stock
from screen_base import Pantalla
from theme import SP_8, SP_10, colores
from widgets import encabezado, paginador, paginar, tabla, barra_busqueda


_TIPOS = {"ajuste": "Ajuste", "venta": "Venta", "anulacion": "Anulación"}


class PantallaMovimientosStock(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Movimientos")
        self._busqueda = ""
        self._pagina = 1

    def build(self):
        self._zona_tabla = ft.Container(expand=True)
        self._zona_paginador = ft.Container()
        self._columnas = [
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Cambio")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Motivo")),
        ]
        self._cargar()
        return ft.Column(
            [
                encabezado(
                    "Movimientos de stock",
                    al_refrescar=lambda _: self.actualizar(),
                    descripcion="Revisá ajustes manuales, ventas y anulaciones que cambiaron el inventario.",
                ),
                barra_busqueda(al_buscar=self._buscar, pista="Buscar producto o motivo..."),
                self._zona_tabla,
                self._zona_paginador,
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _buscar(self, texto):
        self._busqueda = (texto or "").strip().casefold()
        self._pagina = 1
        self._refrescar()

    def _cargar(self):
        resultados = [
            fila
            for fila in reversed(movimientos_stock)
            if self._busqueda in fila.get("producto_nombre", "").casefold()
            or self._busqueda in fila.get("motivo", "").casefold()
        ]
        filas = []
        for movimiento in resultados:
            cantidad = movimiento.get("cantidad", 0)
            paleta = colores.get()
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(movimiento.get("fecha", "—"))),
                        ft.DataCell(ft.Text(movimiento.get("producto_nombre", "Producto"))),
                        ft.DataCell(ft.Text(_TIPOS.get(movimiento.get("tipo"), "Movimiento"))),
                        ft.DataCell(
                            ft.Text(
                                f"{cantidad:+d}",
                                color=paleta.success if cantidad > 0 else paleta.danger,
                            )
                        ),
                        ft.DataCell(ft.Text(f"{movimiento.get('anterior', '—')} → {movimiento.get('nuevo', '—')}")),
                        ft.DataCell(ft.Text(movimiento.get("motivo", "—"))),
                    ]
                )
            )
        visibles, actual, total = paginar(filas, self._pagina)
        self._pagina = actual
        mensaje = "Todavía no hay movimientos de stock" if not movimientos_stock else "No hay movimientos para esa búsqueda"
        self._zona_tabla.content = tabla(self._columnas, visibles, mensaje_vacio=mensaje)
        self._zona_paginador.content = paginador(actual, total, self._ir_pagina)

    def _refrescar(self):
        self._cargar()
        try:
            self._zona_tabla.update()
            self._zona_paginador.update()
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
