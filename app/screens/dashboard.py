import flet as ft
from datos import stats, productos, cuentas, cli_por_id
from screen_base import Screen
from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    FS_14,
    FS_18,
    ICON_MD,
    SP_8,
    SP_12,
    app_colors,
    role_color,
)
from widgets import AppHeader, AppStatCard


class PantallaDashboard(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Dashboard")

    def actualizar(self):
        try:
            s = stats()
            palette = app_colors.get()
            danger = role_color(palette, "deben")
            success = role_color(palette, "paid")

            self.texto_hoy.value = f"${s['hoy']:,.0f}"
            self.texto_mes.value = f"${s['mes']:,.0f}"
            self.texto_ganancia.value = f"${s['ganancia']:,.0f}"
            self.texto_deben.value = f"${s['deben']:,.0f}"

            alertas = []
            for p in productos:
                if p["stock"] <= p["minimo"]:
                    alertas.append(
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.TRENDING_DOWN,
                                    color=danger,
                                    size=ICON_MD,
                                ),
                                ft.Text(
                                    f"{p['nombre']}: stock {p['stock']} (min {p['minimo']})",
                                    size=FS_14,
                                    color=palette.text,
                                ),
                            ],
                            spacing=SP_8,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    )
            for c in cuentas:
                pendiente = c["total"] - c["pagado"]
                if pendiente > 0:
                    cli = cli_por_id(c["cliente_id"])
                    alertas.append(
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.PAID,
                                    color=danger,
                                    size=ICON_MD,
                                ),
                                ft.Text(
                                    f"{cli['nombre'] if cli else '?'} debe ${pendiente:,}",
                                    size=FS_14,
                                    color=palette.text,
                                ),
                            ],
                            spacing=SP_8,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    )
            if not alertas:
                alertas.append(
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE,
                                color=success,
                                size=ICON_MD,
                            ),
                            ft.Text(
                                "Todo en orden",
                                size=FS_14,
                                color=palette.text,
                            ),
                        ],
                        spacing=SP_8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            self.lista_alertas.controls = alertas
        except Exception as ex:
            print(f"Error actualizar dashboard: {ex}")
        self.pagina.update()

    def build(self):
        palette = app_colors.get()
        card_hoy = AppStatCard("Hoy", "$0", role="success")
        card_mes = AppStatCard("Mes", "$0", role="info")
        card_ganancia = AppStatCard("Ganancia", "$0", role="warning")
        card_deben = AppStatCard("Deben", "$0", role="danger")

        self.texto_hoy = card_hoy.content.controls[1]
        self.texto_mes = card_mes.content.controls[1]
        self.texto_ganancia = card_ganancia.content.controls[1]
        self.texto_deben = card_deben.content.controls[1]

        self.lista_alertas = ft.Column(spacing=SP_8)

        return ft.Column(
            [
                AppHeader(
                    "Dashboard",
                    on_refresh=lambda _: self.actualizar(),
                ),
                ft.Row(
                    [card_hoy, card_mes, card_ganancia, card_deben],
                    spacing=SP_12,
                ),
                ft.Divider(
                    height=DIVIDER_HEIGHT,
                    thickness=BORDER_WIDTH,
                    color=palette.border,
                ),
                ft.Text(
                    "Alertas",
                    size=FS_18,
                    weight=ft.FontWeight.BOLD,
                    color=palette.text,
                ),
                self.lista_alertas,
            ],
            spacing=SP_12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
