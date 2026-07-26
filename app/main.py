import flet as ft
from screens.dashboard import PantallaDashboard
from screens.caja import PantallaCaja
from screens.stock import PantallaStock
from screens.clientes import PantallaClientes
from screens.fiado import PantallaFiado
from screens.chat import PantallaChat


def main(page: ft.Page):
    page.title = "GesKio"
    page.window.width = 1100
    page.window.height = 700
    page.padding = 0

    body = ft.Column(expand=True)

    screens = {
        "dash": PantallaDashboard(page),
        "caja": PantallaCaja(page),
        "stock": PantallaStock(page),
        "clientes": PantallaClientes(page),
        "fiado": PantallaFiado(page),
        "chat": PantallaChat(page),
    }

    # navegacion
    nav_items = [
        ("dash",     ft.Icons.DASHBOARD,       "Dashboard"),
        ("caja",     ft.Icons.POINT_OF_SALE,    "Caja"),
        ("stock",    ft.Icons.INVENTORY_2,      "Stock"),
        ("clientes", ft.Icons.PEOPLE,           "Clientes"),
        ("fiado",    ft.Icons.RECEIPT_LONG,     "Fiado"),
        ("chat",     ft.Icons.SMART_TOY,        "Chat IA"),
    ]

    active_key = ft.Text("dash")

    def mostrar(nombre):
        s = screens[nombre]
        s.visible = True
        body.controls = [s]  # asigna nueva lista → llama al property setter!
        s.al_entrar()
        active_key.value = nombre
        actualizar_nav()
        page.update()

    def actualizar_nav():
        for key, btn in zip([k for k, _, _ in nav_items], botones):
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_100 if key == active_key.value else None,
                color=ft.Colors.GREEN_800 if key == active_key.value else None,
                side=ft.BorderSide(2, ft.Colors.GREEN) if key == active_key.value else None,
            )
        page.update()

    botones = []
    for key, icon, label in nav_items:
        btn = ft.TextButton(label, icon=icon,
                            style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=12, vertical=8)),
                            on_click=lambda _, k=key: mostrar(k))
        botones.append(btn)

    nav = ft.Row(botones, alignment=ft.MainAxisAlignment.CENTER, spacing=4)

    page.add(ft.Container(padding=ft.padding.only(top=5)))
    page.add(ft.Column([nav, ft.Divider(height=1), body], expand=True))
    mostrar("dash")

ft.app(target=main)
