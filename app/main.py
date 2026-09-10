"""GesKio shell entry (slice-a): Paperpillar Shell + adapter, zero screen edits.

Boot is 1100x700 so the shell starts on the icon rail (collapse when the
window is at or below the shell breakpoints from theme.py). Resize follows
page.window.on_event (WindowEventType.RESIZED); availability is
OS-dependent, so the topbar manual toggle is mandatory and always works.
"""

import flet as ft
from screens.caja import PantallaCaja
from screens.chat import PantallaChat
from screens.clientes import PantallaClientes
from screens.dashboard import PantallaDashboard
from screens.fiado import PantallaFiado
from screens.stock import PantallaStock
from theme import app_colors
from widgets import Shell

BRAND_OPTIONS = (("rojo", "Rojo"), ("verde", "Verde"))


def main(page: ft.Page):
    app_colors.load_from_store(page)
    app_colors.apply_to_page(page)
    page.title = "GesKio"
    page.window.width = 1100
    page.window.height = 700
    page.padding = 0

    nav_items = [
        ("dash", ft.Icons.DASHBOARD, "Dashboard"),
        ("caja", ft.Icons.POINT_OF_SALE, "Caja"),
        ("stock", ft.Icons.INVENTORY_2, "Stock"),
        ("clientes", ft.Icons.PEOPLE, "Clientes"),
        ("fiado", ft.Icons.RECEIPT_LONG, "Fiado"),
        ("chat", ft.Icons.SMART_TOY, "Chat IA"),
    ]
    screens = {
        "dash": PantallaDashboard(page),
        "caja": PantallaCaja(page),
        "stock": PantallaStock(page),
        "clientes": PantallaClientes(page),
        "fiado": PantallaFiado(page),
        "chat": PantallaChat(page),
    }

    shell = Shell(
        page,
        nav_items,
        screens,
        active_key="dash",
        brand_options=BRAND_OPTIONS,
    )
    page.add(shell)
    shell.navigate("dash")


ft.app(target=main)
