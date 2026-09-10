import calendar as pycal
from datetime import date, timedelta

import flet as ft
from datos import cli_por_id, cuentas, productos, stats, ventas
from screen_base import Screen
from theme import (
    BORDER_WIDTH,
    FS_12,
    FS_14,
    ICON_MD,
    SP_4,
    SP_8,
    SP_12,
    app_colors,
    role_color,
)
from widgets import (
    AppStatCard,
    Calendar,
    FocalStatCard,
    PageHeader,
    Section,
    StatGrid,
)


def ventas_del_dia(ventas_list, fecha_iso: str) -> list:
    """View-side filter: ventas entries for one ISO day."""
    return [v for v in (ventas_list or []) if v.get("fecha") == fecha_iso]


def totales_ultimos_7_dias(ventas_list, today: date) -> list:
    """View-side aggregate: totals for the last 7 days ending today."""
    totals: dict[str, float] = {}
    for v in ventas_list or []:
        totals[v.get("fecha", "")] = totals.get(v.get("fecha", ""), 0) + (
            v.get("total", 0) or 0
        )
    series = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        iso = day.isoformat()
        series.append((iso, totals.get(iso, 0)))
    return series


def totales_mes(ventas_list, year: int, month: int) -> dict:
    """View-side aggregate: per-day totals for one calendar month."""
    prefix = f"{year:04d}-{month:02d}-"
    totals: dict[int, float] = {}
    for v in ventas_list or []:
        fecha = v.get("fecha", "")
        if fecha.startswith(prefix):
            try:
                day = int(fecha[8:10])
            except (ValueError, IndexError):
                continue
            totals[day] = totals.get(day, 0) + (v.get("total", 0) or 0)
    return totals


class PantallaDashboard(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Dashboard")
        self.cal_view = "week"

    def _serie_calendario(self, view: str) -> ft.Control:
        if view == "day":
            return self._contenido_dia()
        if view == "month":
            return self._contenido_mes()
        return self._contenido_semana()

    def _contenido_dia(self) -> ft.Control:
        palette = app_colors.get()
        today_iso = date.today().isoformat()
        entries = ventas_del_dia(ventas, today_iso)
        if not entries:
            return ft.Text(
                "Sin ventas hoy", size=FS_14, color=palette.text_soft
            )
        rows: list[ft.Control] = []
        for v in entries:
            cli = cli_por_id(v.get("cliente_id", ""))
            nombre = cli["nombre"] if cli else "Mostrador"
            detalle = f"${v.get('total', 0):,.0f} - {nombre} - {v.get('pago', '')}"
            rows.append(
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.RECEIPT_LONG,
                            color=palette.text_soft,
                            size=ICON_MD,
                        ),
                        ft.Text(detalle, size=FS_14, color=palette.text),
                    ],
                    spacing=SP_8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        return ft.Column(rows, spacing=SP_8)

    def _contenido_semana(self) -> ft.Control:
        palette = app_colors.get()
        series = totales_ultimos_7_dias(ventas, date.today())
        rows: list[ft.Control] = []
        for iso, total in series:
            rows.append(
                ft.Row(
                    [
                        ft.Text(iso, size=FS_12, color=palette.text_muted),
                        ft.Text(
                            f"${total:,.0f}", size=FS_14, color=palette.text
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        return ft.Column(rows, spacing=SP_4)

    def _contenido_mes(self) -> ft.Control:
        palette = app_colors.get()
        today = date.today()
        totals = totales_mes(ventas, today.year, today.month)
        try:
            num_days = pycal.monthrange(today.year, today.month)[1]
        except Exception:
            num_days = 30
        today_iso = today.isoformat()
        cells: list[ft.Control] = []
        for day in range(1, num_days + 1):
            iso = f"{today.year:04d}-{today.month:02d}-{day:02d}"
            total = totals.get(day, 0)
            is_today = iso == today_iso
            day_color = (
                palette.on_accent_soft if is_today else palette.text_muted
            )
            total_color = (
                palette.on_accent_soft if is_today else palette.text
            )
            total_text = f"${total:,.0f}" if total else "-"
            cells.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(str(day), size=FS_12, color=day_color),
                            ft.Text(total_text, size=FS_12, color=total_color),
                        ],
                        spacing=SP_4,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=SP_8,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=palette.accent_soft if is_today else palette.surface,
                    border=ft.Border.all(
                        BORDER_WIDTH,
                        palette.primary if is_today else palette.border,
                    ),
                    border_radius=ft.BorderRadius.all(SP_4),
                    col={"xs": 4, "sm": 3, "md": 2},
                )
            )
        return ft.ResponsiveRow(cells, spacing=SP_8, run_spacing=SP_8)

    def actualizar(self):
        try:
            s = stats()

            self.texto_hoy.value = f"${s['hoy']:,.0f}"
            self.texto_mes.value = f"${s['mes']:,.0f}"
            self.texto_ganancia.value = f"${s['ganancia']:,.0f}"
            self.texto_deben.value = f"${s['deben']:,.0f}"

            palette = app_colors.get()
            danger = role_color(palette, "deben")
            success = role_color(palette, "paid")

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
            try:
                self.calendar.refresh()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error actualizar dashboard: {ex}")
        self.pagina.update()

    def build(self):
        focal = FocalStatCard("Hoy", "$0", role="accent_text")
        card_mes = AppStatCard("Mes", "$0", role="info")
        card_ganancia = AppStatCard("Ganancia", "$0", role="warning")
        card_deben = AppStatCard("Deben", "$0", role="danger")

        self.texto_hoy = focal.content.controls[1]
        self.texto_mes = card_mes.content.controls[1]
        self.texto_ganancia = card_ganancia.content.controls[1]
        self.texto_deben = card_deben.content.controls[1]

        self.lista_alertas = ft.Column(spacing=SP_8)
        alert_section = Section("Alertas", self.lista_alertas)
        self.calendar = Calendar(
            get_series=self._serie_calendario,
            today=date.today().isoformat(),
            view=self.cal_view,
        )
        stats_block = StatGrid(focal, [card_mes, card_ganancia, card_deben])

        return ft.Column(
            [
                PageHeader(
                    "Dashboard",
                    on_refresh=lambda _: self.actualizar(),
                ),
                stats_block,
                self.calendar,
                alert_section,
            ],
            spacing=SP_12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
