import flet as ft
from screen_base import Screen
from datos import stats, productos, cuentas, cli_por_id


class PantallaDashboard(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Dashboard")

    def actualizar(self):
        try:
            s = stats()

            self.texto_hoy.value = f"${s['hoy']:,.0f}"
            self.texto_mes.value = f"${s['mes']:,.0f}"
            self.texto_ganancia.value = f"${s['ganancia']:,.0f}"
            self.texto_deben.value = f"${s['deben']:,.0f}"

            alertas = []
            for p in productos:
                if p["stock"] <= p["minimo"]:
                    alertas.append(
                        ft.Text(f"⬇ {p['nombre']}: stock {p['stock']} (min {p['minimo']})", color=ft.Colors.RED))
            for c in cuentas:
                pendiente = c["total"] - c["pagado"]
                if pendiente > 0:
                    cli = cli_por_id(c["cliente_id"])
                    alertas.append(
                        ft.Text(f"💰 {cli['nombre'] if cli else '?'} debe ${pendiente:,}"))
            if not alertas:
                alertas.append(ft.Text("Todo en orden ✅", color=ft.Colors.GREEN))
            self.lista_alertas.controls = alertas
        except Exception as ex:
            print(f"Error actualizar dashboard: {ex}")
        self.pagina.update()

    def build(self):
        card_hoy      = ft.Container(content=ft.Column([ft.Text("Hoy",      size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500), ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)],  spacing=4), padding=20, border_radius=12, bgcolor=ft.Colors.SURFACE, border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), expand=True)
        card_mes      = ft.Container(content=ft.Column([ft.Text("Mes",      size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500), ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)],   spacing=4), padding=20, border_radius=12, bgcolor=ft.Colors.SURFACE, border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), expand=True)
        card_ganancia = ft.Container(content=ft.Column([ft.Text("Ganancia", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500), ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER)], spacing=4), padding=20, border_radius=12, bgcolor=ft.Colors.SURFACE, border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), expand=True)
        card_deben    = ft.Container(content=ft.Column([ft.Text("Deben",   size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500), ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED)],    spacing=4), padding=20, border_radius=12, bgcolor=ft.Colors.SURFACE, border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), expand=True)

        self.texto_hoy      = card_hoy.content.controls[1]
        self.texto_mes      = card_mes.content.controls[1]
        self.texto_ganancia = card_ganancia.content.controls[1]
        self.texto_deben    = card_deben.content.controls[1]

        self.lista_alertas = ft.Column(spacing=5)

        return ft.Column([
            ft.Row([
                ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.REFRESH, icon_size=20, tooltip="Refrescar", on_click=lambda _: self.actualizar()),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([card_hoy, card_mes, card_ganancia, card_deben], spacing=12),
            ft.Divider(height=20),
            ft.Text("Alertas", size=18, weight=ft.FontWeight.BOLD),
            self.lista_alertas,
        ], spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
