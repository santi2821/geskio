import flet as ft
from screens.dashboard import PantallaDashboard
from screens.caja import PantallaCaja
from screens.stock import PantallaStock
from screens.clientes import PantallaClientes
from screens.fiado import PantallaFiado
from screens.chat import PantallaChat
from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    SP_4,
    SP_8,
    SP_12,
    app_colors,
)

BRAND_OPTIONS = (("rojo", "Rojo"), ("verde", "Verde"))


def main(page: ft.Page):
    app_colors.load_from_store(page)
    app_colors.apply_to_page(page)
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
        ("dash", ft.Icons.DASHBOARD, "Dashboard"),
        ("caja", ft.Icons.POINT_OF_SALE, "Caja"),
        ("stock", ft.Icons.INVENTORY_2, "Stock"),
        ("clientes", ft.Icons.PEOPLE, "Clientes"),
        ("fiado", ft.Icons.RECEIPT_LONG, "Fiado"),
        ("chat", ft.Icons.SMART_TOY, "Chat IA"),
    ]

    active_key = ft.Text("dash")

    def nav_style(key):
        palette = app_colors.get()
        active = key == active_key.value
        return ft.ButtonStyle(
            bgcolor=palette.accent_soft if active else None,
            color=palette.primary if active else palette.text_soft,
            side=ft.BorderSide(BORDER_WIDTH * 2, palette.primary) if active else None,
            padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
        )

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
            btn.style = nav_style(key)
        page.update()

    botones = []
    for key, icon, label in nav_items:
        btn = ft.TextButton(
            label, icon=icon, style=nav_style(key), on_click=lambda _, k=key: mostrar(k)
        )
        botones.append(btn)

    nav = ft.Row(botones, alignment=ft.MainAxisAlignment.CENTER, spacing=SP_4)

    def refresh_chrome():
        palette = app_colors.get()
        divider.color = palette.border
        mode_btn.icon = (
            ft.Icons.LIGHT_MODE if app_colors.mode == "dark" else ft.Icons.DARK_MODE
        )
        mode_btn.icon_color = palette.text_soft
        brand.value = app_colors.theme_name
        actualizar_nav()

    def apply_and_rebuild():
        app_colors.apply_to_page(page)
        for s in screens.values():
            s.invalidate()
        refresh_chrome()
        mostrar(active_key.value)

    def alternar_modo():
        app_colors.set_mode("light" if app_colors.mode == "dark" else "dark", page)
        apply_and_rebuild()

    def cambiar_marca(event):
        app_colors.set_theme(event.control.value, page)
        apply_and_rebuild()

    palette = app_colors.get()
    divider = ft.Divider(
        height=DIVIDER_HEIGHT,
        thickness=BORDER_WIDTH,
        color=palette.border,
    )
    mode_btn = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE if app_colors.mode == "dark" else ft.Icons.DARK_MODE,
        icon_color=palette.text_soft,
        tooltip="Cambiar tema",
        on_click=lambda _: alternar_modo(),
    )
    brand = ft.Dropdown(
        options=[ft.dropdown.Option(value, label) for value, label in BRAND_OPTIONS],
        value=app_colors.theme_name,
        on_select=cambiar_marca,
    )
    toolbar = ft.Row(
        [nav, mode_btn, brand],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=SP_12,
    )

    page.add(ft.Container(padding=ft.Padding.only(top=SP_4)))
    page.add(ft.Column([toolbar, divider, body], expand=True))
    refresh_chrome()
    mostrar("dash")


ft.app(target=main)
