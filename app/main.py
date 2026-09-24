"""Punto de entrada del marco + pantallas de GesKio."""

import flet as ft
from screens.ajustes import PantallaAjustes
from screens.caja import PantallaCaja
from screens.chat import PantallaChat
from screens.clientes import PantallaClientes
from screens.dashboard import PantallaDashboard
from screens.fiado import PantallaFiado
from screens.stock import PantallaStock
from theme import colores
from widgets import Marco


def main(page: ft.Page):
    colores.load_from_store(page)
    colores.apply_to_page(page)
    page.title = "GesKio"
    page.window.width = 1100
    page.window.height = 700
    page.padding = 0

    items_nav = [
        ("dash", ft.Icons.DASHBOARD, "Dashboard"),
        ("caja", ft.Icons.POINT_OF_SALE, "Caja"),
        ("stock", ft.Icons.INVENTORY_2, "Stock"),
        ("clientes", ft.Icons.PEOPLE, "Clientes"),
        ("fiado", ft.Icons.RECEIPT_LONG, "Fiado"),
        ("chat", ft.Icons.SMART_TOY, "Chat"),
        ("ajustes", ft.Icons.SETTINGS, "Ajustes"),
    ]
    pantallas = {
        "dash": PantallaDashboard(page),
        "caja": PantallaCaja(page),
        "stock": PantallaStock(page),
        "clientes": PantallaClientes(page),
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
    marco.navegar("dash")


if __name__ == "__main__":
    ft.run(main)
