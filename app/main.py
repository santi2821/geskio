"""Punto de entrada del marco + pantallas de GesKio."""

import flet as ft
import datos
from screens.ajustes import PantallaAjustes
from screens.caja import PantallaCaja
from screens.chat import PantallaChat
from screens.clientes import PantallaClientes
from screens.dashboard import PantallaDashboard
from screens.fiado import PantallaFiado
from screens.historial_ventas import PantallaHistorialVentas
from screens.proveedores import PantallaProveedores
from screens.stock import PantallaStock
from screens.movimientos_stock import PantallaMovimientosStock
from theme import colores
from widgets import Marco, aviso


def _bienvenida(page: ft.Page):
    paleta = colores.get()

    def elegir(modo):
        try:
            datos.iniciar_comercio(modo)
            page.clean()
            main(page)
        except Exception as ex:
            aviso(page, f"No se pudieron iniciar los datos: {ex}", rol="danger")

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            padding=32,
            content=ft.Container(
                width=560,
                padding=32,
                bgcolor=paleta.surface,
                border=ft.Border.all(1, paleta.border),
                border_radius=ft.BorderRadius.all(16),
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.STORE, size=40, color=paleta.primary),
                        ft.Text("Empezá a usar GesKio", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Elegí cómo querés preparar este equipo. La opción se guarda "
                            "junto con tus datos locales.",
                            size=16,
                            color=paleta.text_muted,
                        ),
                        ft.FilledButton(
                            "Probar con datos de ejemplo",
                            icon=ft.Icons.PLAY_ARROW,
                            on_click=lambda _: elegir("demo"),
                        ),
                        ft.OutlinedButton(
                            "Empezar con el comercio vacío",
                            icon=ft.Icons.STORE_MALL_DIRECTORY,
                            on_click=lambda _: elegir("vacio"),
                        ),
                        ft.Text(
                            "El inicio vacío no incluye productos ni clientes; podés cargarlos "
                            "desde Inventario y Clientes.",
                            size=13,
                            color=paleta.text_muted,
                        ),
                    ],
                    spacing=16,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    tight=True,
                ),
            ),
        )
    )


def main(page: ft.Page):
    colores.load_from_store(page)
    colores.apply_to_page(page)
    page.title = "GesKio"
    page.window.width = 1100
    page.window.height = 700
    page.padding = 0
    if not datos.COMERCIO_INICIALIZADO:
        _bienvenida(page)
        return

    items_nav = [
        ("dash", ft.Icons.DASHBOARD, "Dashboard"),
        ("caja", ft.Icons.POINT_OF_SALE, "Caja"),
        ("ventas", ft.Icons.RECEIPT_LONG, "Ventas"),
        ("stock", ft.Icons.INVENTORY_2, "Stock"),
        ("movimientos", ft.Icons.SWAP_VERT, "Movimientos"),
        ("clientes", ft.Icons.PEOPLE, "Clientes"),
        ("proveedores", ft.Icons.LOCAL_SHIPPING, "Proveedores"),
        ("fiado", ft.Icons.RECEIPT_LONG, "Fiado"),
        ("chat", ft.Icons.SMART_TOY, "Chat"),
        ("ajustes", ft.Icons.SETTINGS, "Ajustes"),
    ]
    pantallas = {
        "dash": PantallaDashboard(page),
        "caja": PantallaCaja(page),
        "ventas": PantallaHistorialVentas(page),
        "stock": PantallaStock(page),
        "movimientos": PantallaMovimientosStock(page),
        "clientes": PantallaClientes(page),
        "proveedores": PantallaProveedores(page),
        "fiado": PantallaFiado(page),
        "chat": PantallaChat(page),
        "ajustes": PantallaAjustes(page),
    }

    marco = Marco(
        page,
        items_nav,
        pantallas,
        clave_activa="dash",
    )
    page.add(marco)
    pantallas["dash"].al_navegar = marco.navegar
    pantallas["ajustes"].al_apariencia = marco.aplicar_y_rearmar
    pantallas["ajustes"].al_restaurar = marco.aplicar_y_rearmar
    marco.navegar("dash")


if __name__ == "__main__":
    ft.run(main)
