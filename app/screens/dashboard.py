import flet as ft
import calendar
from datetime import date, datetime
from screen_base import Screen
from datos import stats, productos, cuentas, cli_por_id, ventas, ventas_por_dia, stock_stats, ventas_por_mes, ganancia_por_mes

# ─── Tokens Figma ───────────────────────────────────────────────────────
COLORS = {
    "primary": "#16a34a",
    "primary_bg": "#dcfce7",
    "primary_text": "#166534",
    "bg": "#f8fafc",
    "surface": "white",
    "text": "#0f172a",
    "muted": "#64748b",
    "border": "#e2e8f0",
    "blue": "#2563eb",
    "blue_bg": "#dbeafe",
    "amber": "#d97706",
    "amber_bg": "#fef3c7",
    "red": "#dc2626",
    "red_bg": "#fee2e2",
    "green": "#16a34a",
    "green_bg": "#dcfce7",
}

RADIUS = 16
PADDING = 20

MESES_ES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
DIAS_SEM = ["L", "M", "X", "J", "V", "S", "D"]


class PantallaDashboard(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Dashboard")
        self.fecha_seleccionada: date = date.today()
        self._cal_year = date.today().year
        self._cal_month = date.today().month

        # refs que se crean en build
        self.texto_hoy: ft.Text | None = None
        self.texto_mes: ft.Text | None = None
        self.texto_ganancia: ft.Text | None = None
        self.texto_deben: ft.Text | None = None
        self.sub_hoy: ft.Text | None = None
        self.sub_mes: ft.Text | None = None
        self.sub_ganancia: ft.Text | None = None
        self.sub_deben: ft.Text | None = None

        self.bar_chart: ft.BarChart | None = None
        self.pie_chart: ft.PieChart | None = None
        self.line_chart: ft.LineChart | None = None
        self.bar_chart_container: ft.Container | None = None
        self.pie_chart_container: ft.Container | None = None
        self.line_chart_container: ft.Container | None = None

        self.lista_alertas: ft.ListView | None = None

        # calendario
        self.text_fecha_sel: ft.Text | None = None
        self.text_total_dia: ft.Text | None = None
        self.lista_ventas_dia: ft.Column | None = None
        self.calendario_titulo: ft.Text | None = None
        self.calendario_grid: ft.Column | None = None
        self.date_picker: ft.DatePicker | None = None
        self._chart_header_total_dia: ft.Text | None = None

    # ─── helpers KPI ───────────────────────────────────────────────
    def _kpi_card(self, icon, icon_color: str, icon_bg: str, label: str, texto_valor: ft.Text, subtitulo: str) -> ft.Container:
        icon_box = ft.Container(
            content=ft.Icon(icon, color=icon_color, size=20),
            width=36,
            height=36,
            bgcolor=icon_bg,
            border_radius=10,
            alignment=ft.alignment.center,
        )
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([icon_box, ft.Text(label, size=12, weight=ft.FontWeight.W_600, color=COLORS["muted"])], spacing=8, alignment=ft.MainAxisAlignment.START),
                    texto_valor,
                    ft.Text(subtitulo, size=11, color=COLORS["muted"]),
                ],
                spacing=6,
            ),
            padding=PADDING,
            border_radius=RADIUS,
            bgcolor=COLORS["surface"],
            border=ft.border.all(1, COLORS["border"]),
            expand=True,
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=0, color="#0f172a0a", offset=ft.Offset(0, 2)),
        )

    # ─── helpers charts ────────────────────────────────────────────
    def _build_bar_chart(self) -> ft.BarChart:
        try:
            data = ventas_por_dia(7)
        except Exception:
            data = []
        max_val = max((d.get("total", 0) for d in data), default=0)
        if max_val == 0:
            max_val = 100
        ceiling = max_val * 1.25
        groups = []
        for idx, d in enumerate(data):
            val = float(d.get("total", 0))
            groups.append(
                ft.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=val,
                            width=16,
                            color=COLORS["primary"],
                            border_radius=ft.border_radius.all(6),
                            tooltip=f"{d.get('fecha','')} ${val:,.0f}",
                        )
                    ],
                )
            )
        # evitar chart vacío
        if not groups:
            groups = [ft.BarChartGroup(x=0, bar_rods=[ft.BarChartRod(from_y=0, to_y=0, width=16, color=COLORS["primary"])])]

        labels = []
        for i, d in enumerate(data):
            fecha = d.get("fecha", "")
            short = fecha[5:] if len(fecha) >= 10 else str(i)
            labels.append(ft.ChartAxisLabel(value=i, label=ft.Text(short, size=10, color=COLORS["muted"])))
        # si no hay data, label dummy
        if not labels:
            labels = [ft.ChartAxisLabel(value=0, label=ft.Text("-", size=10, color=COLORS["muted"]))]

        return ft.BarChart(
            bar_groups=groups,
            groups_space=12,
            max_y=ceiling,
            min_y=0,
            interactive=True,
            expand=True,
            left_axis=ft.ChartAxis(
                show_labels=True,
                labels_size=42,
                title=ft.Text("ARS", size=11, color=COLORS["muted"]),
            ),
            bottom_axis=ft.ChartAxis(labels=labels, labels_size=28),
            horizontal_grid_lines=ft.ChartGridLines(interval=ceiling / 4, color=COLORS["border"], width=1, dash_pattern=[3, 3]),
            border=ft.border.all(1, COLORS["border"]),
            tooltip_bgcolor=COLORS["surface"],
        )

    def _build_pie_chart(self) -> ft.PieChart:
        try:
            s = stock_stats()
        except Exception:
            s = {"ok": 0, "bajo": 0, "agotado": 0}
        vals = [
            ("Ok", s.get("ok", 0), "#16a34a"),
            ("Bajo", s.get("bajo", 0), "#f59e0b"),
            ("Agotado", s.get("agotado", 0), "#ef4444"),
        ]
        sections = []
        total = sum(v for _, v, _ in vals)
        # Si todo cero, mostrar placeholder
        if total == 0:
            sections.append(
                ft.PieChartSection(value=1, color=COLORS["border"], title="Sin datos", radius=65, title_style=ft.TextStyle(size=11, color=COLORS["muted"]))
            )
        else:
            for label, val, col in vals:
                if val <= 0:
                    continue
                sections.append(
                    ft.PieChartSection(
                        value=float(val),
                        color=col,
                        radius=68,
                        title=f"{label}\n{val}",
                        title_style=ft.TextStyle(size=11, color="white", weight=ft.FontWeight.BOLD),
                        border_side=ft.BorderSide(2, "white"),
                    )
                )
        return ft.PieChart(
            sections=sections,
            sections_space=2,
            center_space_radius=38,
            expand=True,
        )

    def _build_line_chart(self) -> ft.LineChart:
        try:
            data = ganancia_por_mes(6)
        except Exception:
            data = []
        puntos = []
        max_y = 0
        for i, e in enumerate(data):
            y = float(e.get("ganancia", 0))
            max_y = max(max_y, y)
            puntos.append(ft.LineChartDataPoint(x=float(i), y=y, tooltip=f"{e.get('mes','')} ${y:,.0f}"))
        if not puntos:
            puntos = [ft.LineChartDataPoint(x=0, y=0)]
            max_y = 100
        if max_y == 0:
            max_y = 100
        labels = []
        for i, e in enumerate(data):
            mes = e.get("mes", "")  # YYYY-MM
            short = mes[2:] if mes else str(i)
            labels.append(ft.ChartAxisLabel(value=i, label=ft.Text(short, size=10, color=COLORS["muted"])))
        if not labels:
            labels = [ft.ChartAxisLabel(value=0, label=ft.Text("-", size=10, color=COLORS["muted"]))]

        serie = ft.LineChartData(
            data_points=puntos,
            color=COLORS["primary"],
            stroke_width=3,
            curved=True,
            point=True,
            below_line_bgcolor="#16a34a22",
            below_line_cutoff_y=0,
        )
        return ft.LineChart(
            data_series=[serie],
            expand=True,
            min_y=0,
            max_y=max_y * 1.25,
            left_axis=ft.ChartAxis(show_labels=True, labels_size=44, title=ft.Text("ARS", size=11, color=COLORS["muted"])),
            bottom_axis=ft.ChartAxis(labels=labels, labels_size=28),
            horizontal_grid_lines=ft.ChartGridLines(interval=max_y / 4 if max_y else 25, color=COLORS["border"], width=1, dash_pattern=[3, 3]),
            border=ft.border.all(1, COLORS["border"]),
            tooltip_bgcolor=COLORS["surface"],
        )

    def _wrap_chart(self, titulo: str, chart: ft.Control, subtitulo: str, icon=ft.Icons.BAR_CHART) -> ft.Container:
        header = ft.Row(
            [
                ft.Column([ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=COLORS["text"]), ft.Text(subtitulo, size=11, color=COLORS["muted"])], spacing=2, expand=True),
                ft.Container(
                    content=ft.Icon(icon, size=16, color=COLORS["muted"]),
                    width=30,
                    height=30,
                    bgcolor=COLORS["bg"],
                    border_radius=8,
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        chart_box = ft.Container(content=chart, height=220, expand=True, alignment=ft.alignment.center)
        return ft.Container(
            content=ft.Column([header, ft.Divider(height=1, color=COLORS["border"]), chart_box], spacing=12),
            padding=PADDING,
            border_radius=RADIUS,
            bgcolor=COLORS["surface"],
            border=ft.border.all(1, COLORS["border"]),
            expand=True,
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=0, color="#0f172a0a", offset=ft.Offset(0, 2)),
        )

    # ─── calendario helpers ────────────────────────────────────────
    def _month_name(self, m: int) -> str:
        return MESES_ES[m] if 1 <= m <= 12 else str(m)

    def _on_fecha_picker(self, e):
        try:
            val = None
            if e and hasattr(e, "control") and e.control and getattr(e.control, "value", None) is not None:
                val = e.control.value
            elif self.date_picker and getattr(self.date_picker, "value", None) is not None:
                val = self.date_picker.value

            if val is None:
                return

            if isinstance(val, str):
                try:
                    val = date.fromisoformat(val[:10])
                except Exception:
                    return
            elif isinstance(val, datetime):
                val = val.date()
            elif isinstance(val, date):
                pass
            else:
                try:
                    val = date.fromisoformat(str(val)[:10])
                except Exception:
                    return

            self.fecha_seleccionada = val
            self._cal_year = val.year
            self._cal_month = val.month
            if self.text_fecha_sel:
                self.text_fecha_sel.value = val.isoformat()
            self._reconstruir_calendario()
            self._actualizar_ventas_dia()
            try:
                self.pagina.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error on_fecha_picker: {ex}")

    def _cambiar_mes(self, delta: int):
        try:
            m = self._cal_month + delta
            y = self._cal_year
            while m > 12:
                m -= 12
                y += 1
            while m < 1:
                m += 12
                y -= 1
            self._cal_year = y
            self._cal_month = m
            self._reconstruir_calendario()
            try:
                self.pagina.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error cambiar_mes: {ex}")

    def _seleccionar_dia(self, dia: int):
        try:
            self.fecha_seleccionada = date(self._cal_year, self._cal_month, dia)
            if self.text_fecha_sel:
                self.text_fecha_sel.value = self.fecha_seleccionada.isoformat()
            self._reconstruir_calendario()
            self._actualizar_ventas_dia()
            try:
                self.pagina.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error seleccionar_dia: {ex}")

    def _reconstruir_calendario(self):
        try:
            if not self.calendario_titulo or not self.calendario_grid:
                return
            self.calendario_titulo.value = f"{self._month_name(self._cal_month)} {self._cal_year}"

            # header días semana
            header = ft.Row(
                [ft.Container(content=ft.Text(d, size=11, weight=ft.FontWeight.W_600, color=COLORS["muted"], text_align=ft.TextAlign.CENTER), expand=True, alignment=ft.alignment.center) for d in DIAS_SEM],
                spacing=2,
            )
            filas = [header]

            dias_en_mes = calendar.monthrange(self._cal_year, self._cal_month)[1]
            primer_dia_sem = calendar.monthrange(self._cal_year, self._cal_month)[0]  # 0=lunes
            # celdas
            dia = 1
            for semana in range(6):  # max 6 semanas
                celdas = []
                for col in range(7):
                    idx = semana * 7 + col
                    if idx < primer_dia_sem or dia > dias_en_mes:
                        celdas.append(ft.Container(expand=True, height=34))
                    else:
                        es_hoy = (date.today() == date(self._cal_year, self._cal_month, dia))
                        es_sel = (self.fecha_seleccionada == date(self._cal_year, self._cal_month, dia))
                        # verificar si hay ventas ese día para puntito
                        fecha_iso = date(self._cal_year, self._cal_month, dia).isoformat()
                        hay_ventas = any(v.get("fecha") == fecha_iso for v in ventas)

                        bg = None
                        border = None
                        text_color = COLORS["text"]
                        if es_sel:
                            bg = COLORS["primary"]
                            text_color = "white"
                        elif es_hoy:
                            bg = COLORS["primary_bg"]
                            border = ft.border.all(1, COLORS["primary"])
                            text_color = COLORS["primary_text"]

                        # puntito indicador
                        indicator = ft.Container(width=4, height=4, border_radius=2, bgcolor=COLORS["primary"] if hay_ventas and not es_sel else None)

                        cell_content = ft.Column(
                            [ft.Text(str(dia), size=12, weight=ft.FontWeight.W_600 if es_sel or es_hoy else ft.FontWeight.W_400, color=text_color, text_align=ft.TextAlign.CENTER), indicator],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                        # Need to capture dia correctly in lambda
                        cel = ft.Container(
                            content=cell_content,
                            expand=True,
                            height=36,
                            bgcolor=bg,
                            border=border,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            ink=True,
                            on_click=lambda _, d=dia: self._seleccionar_dia(d),
                        )
                        celdas.append(cel)
                        dia += 1
                filas.append(ft.Row(celdas, spacing=2))
                if dia > dias_en_mes:
                    break

            self.calendario_grid.controls = filas
            # actualizar también texto fecha seleccionado si no estaba seteado
            if self.text_fecha_sel:
                self.text_fecha_sel.value = self.fecha_seleccionada.isoformat()
        except Exception as ex:
            print(f"Error reconstruir_calendario: {ex}")

    def _actualizar_ventas_dia(self):
        try:
            if not self.text_total_dia or not self.lista_ventas_dia:
                return
            fecha_iso = self.fecha_seleccionada.isoformat()
            ventas_dia = [v for v in ventas if v.get("fecha") == fecha_iso]
            total = sum(v.get("total", 0) for v in ventas_dia)
            self.text_total_dia.value = f"${total:,.0f}"
            if self._chart_header_total_dia:
                self._chart_header_total_dia.value = f"Total ventas del día: ${total:,.0f} • {len(ventas_dia)} ventas"

            if not ventas_dia:
                self.lista_ventas_dia.controls = [
                    ft.Container(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.INBOX, size=18, color=COLORS["muted"]), ft.Text("Sin ventas en esta fecha", size=12, color=COLORS["muted"])],
                            spacing=8,
                        ),
                        padding=12,
                        bgcolor=COLORS["bg"],
                        border_radius=10,
                        border=ft.border.all(1, COLORS["border"]),
                    )
                ]
                return

            items = []
            for v in ventas_dia:
                pago = v.get("pago", "efectivo")
                color_pago = {"efectivo": COLORS["primary"], "fiado": COLORS["red"], "tarjeta": COLORS["blue"]}.get(pago, COLORS["muted"])
                # resumen items
                resumen = ", ".join(f"{it.get('nombre','?')} x{it.get('cantidad',1)}" for it in v.get("items", [])[:2])
                if len(v.get("items", [])) > 2:
                    resumen += f" +{len(v['items'])-2} más"

                chip = ft.Container(
                    content=ft.Text(pago.upper(), size=10, weight=ft.FontWeight.BOLD, color=color_pago),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    bgcolor=color_pago + "14" if len(color_pago) == 7 else color_pago,
                    border=ft.border.all(1, color_pago + "33" if len(color_pago) == 7 else color_pago),
                    border_radius=20,
                )
                # For hex colors with alpha: use with_opacity fallback; simpler use ft.Colors.with_opacity? Keep string approach but ensure valid
                # Actually need proper: use ft.Colors.with_opacity; but we keep simple bgcolor with opacity via with_opacity helper would be better.
                # Use helper: ft.Colors.with_opacity(0.08, color_pago) if we can; but our string may be invalid for ft. Use try.
                # Fallback: keep bg as light
                try:
                    # try to use helper to validate color string
                    ft.Colors.with_opacity(0.1, color_pago)
                    chip.bgcolor = ft.Colors.with_opacity(0.08, color_pago)
                except Exception:
                    pass

                card = ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.RECEIPT_LONG, size=16, color=COLORS["muted"]),
                                width=30,
                                height=30,
                                bgcolor=COLORS["bg"],
                                border_radius=8,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [
                                    ft.Text(f"Venta #{v.get('id','')[:6]}  •  ${v.get('total',0):,}", size=12, weight=ft.FontWeight.W_600, color=COLORS["text"]),
                                    ft.Text(resumen if resumen else "—", size=11, color=COLORS["muted"], max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            chip,
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=10,
                    bgcolor="white",
                    border=ft.border.all(1, COLORS["border"]),
                    border_radius=10,
                )
                items.append(card)

            self.lista_ventas_dia.controls = items
        except Exception as ex:
            print(f"Error actualizar_ventas_dia: {ex}")

    # ─── actualizar ──────────────────────────────────────────────────
    def actualizar(self):
        try:
            s = stats()

            if self.texto_hoy is not None:
                self.texto_hoy.value = f"${s.get('hoy', 0):,.0f}"
            if self.texto_mes is not None:
                self.texto_mes.value = f"${s.get('mes', 0):,.0f}"
            if self.texto_ganancia is not None:
                self.texto_ganancia.value = f"${s.get('ganancia', 0):,.0f}"
            if self.texto_deben is not None:
                self.texto_deben.value = f"${s.get('deben', 0):,.0f}"

            # subtítulos dinâmicos (opcional)
            if self.sub_ganancia is not None:
                try:
                    margen_val = round((s.get('ganancia',0) / s.get('mes',1) *100)) if s.get('mes',0) else 0
                    self.sub_ganancia.value = f"Margen ~{margen_val}% mes actual"
                except Exception:
                    pass
            if self.sub_deben is not None:
                pendientes = sum(1 for c in cuentas if c.get("total",0) - c.get("pagado",0) > 0)
                self.sub_deben.value = f"{pendientes} cuentas pendientes"

            # ── alertas mejoradas ──
            if self.lista_alertas is not None:
                alertas_controls = []

                # stock alertas
                for p in productos:
                    if p.get("stock", 0) == 0:
                        chip = ft.Container(
                            content=ft.Text("AGOTADO", size=10, weight=ft.FontWeight.BOLD, color=COLORS["red"]),
                            bgcolor=ft.Colors.with_opacity(0.08, COLORS["red"]) if hasattr(ft.Colors, "with_opacity") else COLORS["red_bg"],
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=20,
                            border=ft.border.all(1, COLORS["red"]),
                        )
                        row = ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=18, color=COLORS["red"]),
                                    ft.Column(
                                        [ft.Text(p.get("nombre","?"), size=12, weight=ft.FontWeight.W_600, color=COLORS["text"]), ft.Text(f"Stock {p.get('stock',0)} / mínimo {p.get('minimo',0)}", size=11, color=COLORS["muted"])],
                                        spacing=2,
                                        expand=True,
                                    ),
                                    chip,
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=10,
                            bgcolor="white",
                            border=ft.border.all(1, COLORS["border"]),
                            border_radius=10,
                        )
                        alertas_controls.append(row)
                    elif p.get("stock", 0) <= p.get("minimo", 0):
                        chip = ft.Container(
                            content=ft.Text("BAJO", size=10, weight=ft.FontWeight.BOLD, color=COLORS["amber"]),
                            bgcolor=ft.Colors.with_opacity(0.08, COLORS["amber"]) if hasattr(ft.Colors, "with_opacity") else COLORS["amber_bg"],
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=20,
                            border=ft.border.all(1, COLORS["amber"]),
                        )
                        row = ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, size=18, color=COLORS["amber"]),
                                    ft.Column(
                                        [ft.Text(p.get("nombre","?"), size=12, weight=ft.FontWeight.W_600, color=COLORS["text"]), ft.Text(f"Stock {p.get('stock',0)} / mínimo {p.get('minimo',0)}", size=11, color=COLORS["muted"])],
                                        spacing=2,
                                        expand=True,
                                    ),
                                    chip,
                                ],
                                spacing=10,
                            ),
                            padding=10,
                            bgcolor="white",
                            border=ft.border.all(1, COLORS["border"]),
                            border_radius=10,
                        )
                        alertas_controls.append(row)

                # cuentas por cobrar
                for c in cuentas:
                    pendiente = c.get("total",0) - c.get("pagado",0)
                    if pendiente > 0:
                        cli = cli_por_id(c.get("cliente_id"))
                        nombre = cli.get("nombre") if cli else "Cliente ?"
                        # calcular días atraso si hay created_at
                        dias_txt = ""
                        try:
                            creado = c.get("created_at") or c.get("fecha") or ""
                            if creado:
                                d = date.fromisoformat(str(creado)[:10])
                                dias = (date.today() - d).days
                                dias_txt = f" • hace {dias}d"
                                if dias > 30:
                                    col_dias = COLORS["red"]
                                elif dias > 7:
                                    col_dias = COLORS["amber"]
                                else:
                                    col_dias = COLORS["muted"]
                            else:
                                col_dias = COLORS["muted"]
                        except Exception:
                            dias_txt = ""
                            col_dias = COLORS["muted"]

                        chip = ft.Container(
                            content=ft.Text(f"${pendiente:,} pendiente", size=10, weight=ft.FontWeight.BOLD, color=COLORS["red"]),
                            bgcolor=ft.Colors.with_opacity(0.08, COLORS["red"]) if hasattr(ft.Colors, "with_opacity") else COLORS["red_bg"],
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=20,
                            border=ft.border.all(1, COLORS["red"]),
                        )
                        row = ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, size=18, color=COLORS["blue"]),
                                    ft.Column(
                                        [ft.Text(nombre, size=12, weight=ft.FontWeight.W_600, color=COLORS["text"]), ft.Text(f"Debe ${pendiente:,}{dias_txt}", size=11, color=col_dias)],
                                        spacing=2,
                                        expand=True,
                                    ),
                                    chip,
                                ],
                                spacing=10,
                            ),
                            padding=10,
                            bgcolor="white",
                            border=ft.border.all(1, COLORS["border"]),
                            border_radius=10,
                        )
                        alertas_controls.append(row)

                if not alertas_controls:
                    alertas_controls.append(
                        ft.Container(
                            content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["primary"], size=18), ft.Text("Todo en orden ✅", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"])], spacing=8),
                            padding=14,
                            bgcolor=COLORS["primary_bg"],
                            border=ft.border.all(1, "#bbf7d0"),
                            border_radius=10,
                        )
                    )
                # ListView usa controls
                self.lista_alertas.controls = alertas_controls

            # ── gráficos: reconstruir ──
            try:
                if self.bar_chart is not None:
                    nuevo = self._build_bar_chart()
                    self.bar_chart.bar_groups = nuevo.bar_groups
                    self.bar_chart.max_y = nuevo.max_y
                    self.bar_chart.bottom_axis = nuevo.bottom_axis
                    self.bar_chart.left_axis = nuevo.left_axis
            except Exception as ex:
                print(f"Error update bar_chart: {ex}")

            try:
                if self.pie_chart is not None:
                    nuevo = self._build_pie_chart()
                    self.pie_chart.sections = nuevo.sections
                    self.pie_chart.center_space_radius = nuevo.center_space_radius
            except Exception as ex:
                print(f"Error update pie_chart: {ex}")

            try:
                if self.line_chart is not None:
                    nuevo = self._build_line_chart()
                    self.line_chart.data_series = nuevo.data_series
                    self.line_chart.max_y = nuevo.max_y
                    self.line_chart.min_y = nuevo.min_y
                    self.line_chart.bottom_axis = nuevo.bottom_axis
                    self.line_chart.left_axis = nuevo.left_axis
            except Exception as ex:
                print(f"Error update line_chart: {ex}")

            # calendario ventas día
            self._actualizar_ventas_dia()
            # reconstruir grid para reflejar puntitos nuevos
            self._reconstruir_calendario()

        except Exception as ex:
            print(f"Error actualizar dashboard: {ex}")
        try:
            self.pagina.update()
        except Exception:
            pass

    # ─── build ───────────────────────────────────────────────────────
    def build(self):
        # ── KPI texts ──
        self.texto_hoy = ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=COLORS["text"])
        self.texto_mes = ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=COLORS["text"])
        self.texto_ganancia = ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=COLORS["text"])
        self.texto_deben = ft.Text("$0", size=28, weight=ft.FontWeight.BOLD, color=COLORS["text"])
        self.sub_hoy = ft.Text("Ventas del día", size=11, color=COLORS["muted"])
        self.sub_mes = ft.Text("Ventas mensuales", size=11, color=COLORS["muted"])
        self.sub_ganancia = ft.Text("Ganancia del mes", size=11, color=COLORS["muted"])
        self.sub_deben = ft.Text("Cuentas pendientes", size=11, color=COLORS["muted"])

        card_hoy = self._kpi_card(ft.Icons.TODAY, COLORS["primary"], COLORS["primary_bg"], "Hoy", self.texto_hoy, "Ventas del día")
        # reassign subtítulo interno para actualizar dinámico: el _kpi_card crea Text nuevo, así que reemplazamos referencia interna?
        # Creamos cards con nuestro texto + sub personalizado: reconstruimos con nuestros objetos ya creados pero mantenemos layout
        # Para mantener referencia actualizable, usamos método ad-hoc: parchear el subtítulo dentro del container
        # card_hoy.content.controls[2] es el subtítulo Text → reemplazamos por self.sub_hoy
        try:
            card_hoy.content.controls[2] = self.sub_hoy
        except Exception:
            pass

        card_mes = self._kpi_card(ft.Icons.CALENDAR_MONTH, COLORS["blue"], COLORS["blue_bg"], "Este mes", self.texto_mes, "Ventas mensuales")
        try:
            card_mes.content.controls[2] = self.sub_mes
        except Exception:
            pass

        card_ganancia = self._kpi_card(ft.Icons.TRENDING_UP, COLORS["amber"], COLORS["amber_bg"], "Ganancia", self.texto_ganancia, "Ganancia del mes")
        try:
            card_ganancia.content.controls[2] = self.sub_ganancia
        except Exception:
            pass

        card_deben = self._kpi_card(ft.Icons.ACCOUNT_BALANCE_WALLET, COLORS["red"], COLORS["red_bg"], "Por cobrar", self.texto_deben, "Cuentas pendientes")
        try:
            card_deben.content.controls[2] = self.sub_deben
        except Exception:
            pass

        # ── charts ──
        self.bar_chart = self._build_bar_chart()
        self.pie_chart = self._build_pie_chart()
        self.line_chart = self._build_line_chart()

        card_bar = self._wrap_chart("Ventas últimos 7 días", self.bar_chart, "Total diario (ARS)", icon=ft.Icons.BAR_CHART)
        card_pie = self._wrap_chart("Stock por estado", self.pie_chart, "Ok / Bajo / Agotado", icon=ft.Icons.PIE_CHART)
        card_line = self._wrap_chart("Ganancia mensual", self.line_chart, "Últimos 6 meses", icon=ft.Icons.SHOW_CHART)

        # ── alertas ──
        self.lista_alertas = ft.ListView(expand=True, spacing=6, auto_scroll=False, height=200)
        card_alertas = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, size=18, color=COLORS["amber"]),
                            ft.Text("Alertas", size=14, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Text("En vivo", size=10, weight=ft.FontWeight.BOLD, color=COLORS["primary"]),
                                bgcolor=COLORS["primary_bg"],
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=20,
                                border=ft.border.all(1, "#bbf7d0"),
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(height=1, color=COLORS["border"]),
                    ft.Container(content=self.lista_alertas, height=200, expand=False),
                ],
                spacing=10,
            ),
            padding=PADDING,
            border_radius=RADIUS,
            bgcolor=COLORS["surface"],
            border=ft.border.all(1, COLORS["border"]),
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=0, color="#0f172a0a", offset=ft.Offset(0, 2)),
        )

        # ── calendario ──
        self.text_fecha_sel = ft.Text(self.fecha_seleccionada.isoformat(), size=13, weight=ft.FontWeight.BOLD, color=COLORS["text"])
        self.text_total_dia = ft.Text("$0", size=18, weight=ft.FontWeight.BOLD, color=COLORS["primary"])
        self._chart_header_total_dia = ft.Text("Seleccioná un día", size=11, color=COLORS["muted"])
        self.lista_ventas_dia = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)
        self.calendario_titulo = ft.Text(f"{self._month_name(self._cal_month)} {self._cal_year}", size=14, weight=ft.FontWeight.BOLD, color=COLORS["text"])
        self.calendario_grid = ft.Column(spacing=4)

        self.date_picker = ft.DatePicker(
            value=self.fecha_seleccionada,
            first_date=date(2020, 1, 1),
            last_date=date(2035, 12, 31),
            confirm_text="Confirmar",
            cancel_text="Cancelar",
            help_text="Seleccionar fecha",
            on_change=self._on_fecha_picker,
            on_dismiss=lambda e: None,
        )

        # header calendario con navegación
        cal_header = ft.Row(
            [
                ft.IconButton(ft.Icons.CHEVRON_LEFT, icon_size=18, tooltip="Mes anterior", on_click=lambda _: self._cambiar_mes(-1)),
                ft.Container(content=self.calendario_titulo, expand=True, alignment=ft.alignment.center),
                ft.IconButton(ft.Icons.CHEVRON_RIGHT, icon_size=18, tooltip="Mes siguiente", on_click=lambda _: self._cambiar_mes(1)),
                ft.IconButton(ft.Icons.CALENDAR_TODAY, icon_size=18, tooltip="Elegir fecha", on_click=lambda _: self.pagina.open(self.date_picker)),
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # lista ventas del día container con altura limitada scrolleable
        ventas_dia_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [ft.Icon(ft.Icons.RECEIPT_LONG, size=16, color=COLORS["muted"]), self.text_fecha_sel, ft.Container(expand=True), self.text_total_dia],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self._chart_header_total_dia,
                    ft.Divider(height=1, color=COLORS["border"]),
                    ft.Container(content=self.lista_ventas_dia, height=180),
                ],
                spacing=8,
            ),
            padding=12,
            bgcolor=COLORS["bg"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"]),
        )

        card_calendario = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=COLORS["primary"]),
                            ft.Text("Calendario de ventas", size=14, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                            ft.Container(expand=True),
                            ft.TextButton("Hoy", icon=ft.Icons.TODAY, style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=10, vertical=6)), on_click=lambda _: (setattr(self, "fecha_seleccionada", date.today()), setattr(self, "_cal_year", date.today().year), setattr(self, "_cal_month", date.today().month), self._reconstruir_calendario(), self._actualizar_ventas_dia(), self.pagina.update())),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(height=1, color=COLORS["border"]),
                    cal_header,
                    self.calendario_grid,
                    ventas_dia_container,
                ],
                spacing=12,
            ),
            padding=PADDING,
            border_radius=RADIUS,
            bgcolor=COLORS["surface"],
            border=ft.border.all(1, COLORS["border"]),
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=0, color="#0f172a0a", offset=ft.Offset(0, 2)),
        )

        # construir grid inicial y lista ventas
        self._reconstruir_calendario()
        self._actualizar_ventas_dia()

        # ── layout final: único Column scroll ──
        # KPI row con scroll horizontal
        kpi_row = ft.Row([card_hoy, card_mes, card_ganancia, card_deben], spacing=12, scroll=ft.ScrollMode.AUTO)

        # Gráficos rows: 2 columnas responsive
        # Usamos Row con 2 cards expand; si hace falta scroll, añadimos scroll AUTO envolviendo
        charts_row1 = ft.Row([card_bar, card_pie], spacing=16)
        # Para line + alertas: fila 2
        charts_row2 = ft.Row([card_line, card_alertas], spacing=16)

        # En pantallas angostas, habilitar scroll horizontal envolviendo cada row en Row(scroll=AUTO)
        # Flet Row con scroll maneja overflow, mantenemos expand pero permitimos scroll si no cabe.
        # Creamos contenedores con scroll para evitar overflow de width 1100
        charts_row1_scroll = ft.Row([charts_row1], scroll=ft.ScrollMode.AUTO, expand=True)
        charts_row2_scroll = ft.Row([charts_row2], scroll=ft.ScrollMode.AUTO, expand=True)

        # Header dashboard
        header = ft.Row(
            [
                ft.Column(
                    [ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD, color=COLORS["text"]), ft.Text("Resumen general del negocio", size=12, color=COLORS["muted"])],
                    spacing=2,
                ),
                ft.Container(expand=True),
                ft.FilledButton("Refrescar", icon=ft.Icons.REFRESH, style=ft.ButtonStyle(bgcolor=COLORS["primary"], color="white", shape=ft.RoundedRectangleBorder(radius=12)), on_click=lambda _: self.actualizar()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        root = ft.Column(
            [
                header,
                kpi_row,
                charts_row1,
                charts_row2,
                card_calendario,
                ft.Container(height=8),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # Wrapper con fondo bg
        return ft.Container(content=root, expand=True, bgcolor=COLORS["bg"])
