"""GesKio shared widget kit.

Every style value resolves to a ``theme.py`` token; this module defines
no color, spacing, radius, or type literal. Screens consume these fixed
defaults instead of hand-building cards, tables, dialogs, or SnackBars.
"""

from __future__ import annotations

from datetime import date as _date

import flet as ft

from theme import (
    BORDER_WIDTH,
    CALENDAR_CELL_SPACING,
    CALENDAR_GAP,
    DIVIDER_HEIGHT,
    FEEDBACK_DURATION_MS,
    FOCAL_BORDER_WIDTH,
    FOCAL_VALUE_FS,
    FS_12,
    FS_14,
    FS_18,
    FS_20,
    FS_28,
    FS_30,
    ICON_MD,
    ICON_SM,
    ICON_LG,
    R_LG,
    R_MD,
    R_PILL,
    R_SM,
    SHELL_BREAKPOINT_H,
    SHELL_BREAKPOINT_W,
    SHELL_CONTENT_PADDING,
    SHELL_RAIL_W,
    SHELL_SIDEBAR_W,
    SHELL_TOPBAR_H,
    SP_4,
    SP_8,
    SP_12,
    SP_20,
    SP_24,
    STAT_VALUE_FS,
    app_colors,
    role_color,
)


def sync_text(field: ft.TextField) -> ft.TextField:
    """Mirror what the user typed back into ``field.value`` on change+blur.

    Flet 0.84 only streams TextField content to the server for fields with a
    subscribed change event. Dialog/form fields without one keep their
    construction value, so save buttons read stale text while showing a
    success message. Subscribing here keeps existing ``field.value`` readers
    working unchanged under both sync models. Blur mirrors the same value
    so the "change loses events, blur brings data" model still saves.
    """

    def _sync(e):
        try:
            if e is None:
                return
            data = getattr(e, "data", None)
            if data is not None:
                field.value = data
                return
            try:
                ctrl_val = getattr(getattr(e, "control", None), "value", None)
                if ctrl_val is not None:
                    field.value = ctrl_val
            except Exception:
                pass
        except Exception:
            pass

    try:
        prev_change = getattr(field, "on_change", None)
    except Exception:
        prev_change = None
    try:
        prev_blur = getattr(field, "on_blur", None)
    except Exception:
        prev_blur = None

    def _chained_change(e):
        _sync(e)
        try:
            if callable(prev_change):
                try:
                    prev_change(e)
                except TypeError:
                    prev_change()
        except Exception:
            pass

    def _chained_blur(e):
        _sync(e)
        try:
            if callable(prev_blur):
                try:
                    prev_blur(e)
                except TypeError:
                    prev_blur()
        except Exception:
            pass

    try:
        field.on_change = _chained_change if callable(prev_change) else _sync
    except Exception:
        pass
    try:
        field.on_blur = _chained_blur if callable(prev_blur) else _sync
    except Exception:
        pass
    return field


def AppCard(
    content: ft.Control, padding: int = SP_20, radius: int = R_MD
) -> ft.Container:
    palette = app_colors.get()
    return ft.Container(
        content=content,
        padding=padding,
        expand=True,
        bgcolor=palette.surface,
        border=ft.Border.all(BORDER_WIDTH, palette.border),
        border_radius=ft.BorderRadius.all(radius),
    )


def AppStatCard(
    label: str,
    value: str,
    role: str = "info",
    icon=None,
) -> ft.Container:
    """Equal stat card: tinted icon-chip + muted label + text value.

    Value uses text on surface (>=15:1) so all four cards pass 4.5:1;
    the role color lives only on the chip icon (UI >=3:1).
    """
    palette = app_colors.get()
    color = role_color(palette, role)
    chip = ft.Container(
        content=ft.Icon(icon or ft.Icons.INSIGHTS, color=color, size=ICON_SM),
        bgcolor=palette.accent_soft,
        border=ft.Border.all(BORDER_WIDTH, palette.border),
        border_radius=ft.BorderRadius.all(R_SM),
        padding=SP_8,
    )
    return AppCard(
        ft.Row(
            [
                chip,
                ft.Column(
                    [
                        ft.Text(
                            label,
                            size=FS_12,
                            weight=ft.FontWeight.W_500,
                            color=palette.text_muted,
                        ),
                        ft.Text(
                            value,
                            size=FS_28,
                            weight=ft.FontWeight.BOLD,
                            color=palette.text,
                        ),
                    ],
                    spacing=SP_4,
                    expand=True,
                ),
            ],
            spacing=SP_12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


def fecha_actual_es(hoy=None) -> str:
    """Spanish topbar date like 'jueves, 10 de septiembre' (no locale)."""
    dias = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo",
    ]
    meses = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    d = hoy or _date.today()
    return f"{dias[d.weekday()]}, {d.day} de {meses[d.month - 1]}"


_BAR_MAX_H = 120
_BAR_MIN_H = 8
_BAR_W = 28


def SalesBars(series, today_iso=None) -> ft.Control:
    """Custom 7-day bars: proportional heights, rounded tips, today primary.

    ``ft.BarChart`` does not exist in Flet 0.84.0 (verified headless via
    ``dir(ft)``), so bars are Containers. Letters L M X J V S D come from
    the ISO date weekday; all captions use text/muted on surface (>=4.5).
    """
    palette = app_colors.get()
    try:
        peak = max((t or 0) for _, t in (series or []))
    except Exception:
        peak = 0
    cols: list[ft.Control] = []
    for iso, total in series or []:
        try:
            wd = _date.fromisoformat(str(iso)).weekday()
        except Exception:
            wd = 0
        letra = "LMXJVSD"[wd]
        is_today = str(iso) == str(today_iso)
        h = (
            _BAR_MIN_H
            if not peak
            else max(_BAR_MIN_H, round((total or 0) / peak * _BAR_MAX_H))
        )
        bar = ft.Container(
            width=_BAR_W,
            height=h,
            bgcolor=palette.primary if is_today else palette.border_strong,
            border_radius=ft.BorderRadius.all(R_SM),
            tooltip=f"${(total or 0):,.0f}",
        )
        cols.append(
            ft.Column(
                [
                    ft.Container(
                        content=bar,
                        height=_BAR_MAX_H,
                        alignment=ft.Alignment.BOTTOM_CENTER,
                    ),
                    ft.Text(
                        letra,
                        size=FS_12,
                        weight=ft.FontWeight.BOLD if is_today else None,
                        color=palette.text if is_today else palette.text_muted,
                    ),
                ],
                spacing=SP_4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    if not cols:
        return ft.Text("Sin datos", size=FS_14, color=palette.text_soft)
    return ft.Row(
        cols,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=SP_8,
    )


def FocalStatCard(
    label: str,
    value: str,
    role: str = "accent_text",
    icon=None,
) -> ft.Container:
    """Von Restorff focal stat: FS_36 role color plus 2px primary border.

    Spans the full row width. Only the focal card uses the 2px primary
    edge; secondary cards stay on AppStatCard (FS_28, 1px border).
    """
    palette = app_colors.get()
    color = role_color(palette, role)
    header: list[ft.Control] = [
        ft.Text(label, size=FS_12, weight=ft.FontWeight.W_500, color=palette.text_muted)
    ]
    if icon is not None:
        header.append(ft.Icon(icon, color=color, size=ICON_MD))
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(header, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(
                    value, size=FOCAL_VALUE_FS, weight=ft.FontWeight.BOLD, color=color
                ),
            ],
            spacing=SP_4,
        ),
        padding=SP_20,
        bgcolor=palette.surface,
        border=ft.Border.all(FOCAL_BORDER_WIDTH, palette.primary),
        border_radius=ft.BorderRadius.all(R_MD),
        width=float("inf"),
    )


def Section(title: str, content: ft.Control) -> ft.Container:
    """Card with heading; heading uses text on surface."""
    palette = app_colors.get()
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    title, size=FS_18, weight=ft.FontWeight.BOLD, color=palette.text
                ),
                content,
            ],
            spacing=SP_12,
        ),
        padding=SP_20,
        bgcolor=palette.surface,
        border=ft.Border.all(BORDER_WIDTH, palette.border),
        border_radius=ft.BorderRadius.all(R_MD),
    )


def StatGrid(focal: ft.Control, stats: list[ft.Control]) -> ft.Column:
    """Focal hierarchy: focal spans width, trio renders in a ResponsiveRow.

    Only the focal card carries the 2px primary border; secondary cards
    are FS_28 role-colored with no screen-level overrides.
    """
    items = list(stats)
    for item in items:
        try:
            item.col = {"xs": 12, "sm": 6, "md": 4}
        except Exception:
            pass
    grid = ft.ResponsiveRow(items, spacing=SP_12, run_spacing=SP_12)
    return ft.Column([focal, grid], spacing=SP_12)


class Calendar(ft.Container):
    """View-only calendar over a ventas series with a SegmentedButton.

    Toggle (day/week/month) is the only interaction; there is no
    creation, edit, or click-through. Content comes from
    ``get_series(view)`` grouped view-side by the screen. The today cell
    uses the accent_soft pair and totals use text on surface (AD-6).
    """

    VIEWS = ("day", "week", "month")

    def __init__(self, get_series, today=None, view="week"):
        super().__init__()
        self.get_series = get_series
        self.today = today
        self.view = view if view in self.VIEWS else "week"
        palette = app_colors.get()
        self.seg = ft.SegmentedButton(
            segments=[
                ft.Segment(value="day", label=ft.Text("D\u00eda")),
                ft.Segment(value="week", label=ft.Text("Semana")),
                ft.Segment(value="month", label=ft.Text("Mes")),
            ],
            selected=[self.view],
            on_change=self._on_change,
        )
        self.body = ft.Container(content=self._safe_series(self.view))
        self.padding = SP_20
        self.bgcolor = palette.surface
        self.border = ft.Border.all(BORDER_WIDTH, palette.border)
        self.border_radius = ft.BorderRadius.all(R_MD)
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Ventas",
                            size=FS_18,
                            weight=ft.FontWeight.BOLD,
                            color=palette.text,
                        ),
                        self.seg,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.body,
            ],
            spacing=SP_12,
        )

    def _safe_series(self, view: str) -> ft.Control:
        try:
            return self.get_series(view)
        except Exception:
            palette = app_colors.get()
            return ft.Text("Sin datos", size=FS_14, color=palette.text_soft)

    def _on_change(self, e) -> None:
        try:
            selected = (
                e.control.selected
                if e is not None and hasattr(e, "control")
                else self.seg.selected
            )
            new_view = selected[0] if selected else self.view
        except Exception:
            new_view = self.view
        if new_view not in self.VIEWS:
            return
        self.view = new_view
        try:
            self.seg.selected = [new_view]
        except Exception:
            pass
        self.body.content = self._safe_series(new_view)
        self._safe_update()

    def refresh(self) -> None:
        self.body.content = self._safe_series(self.view)
        self._safe_update()

    def _safe_update(self) -> None:
        try:
            self.update()
        except Exception:
            pass


def PageHeader(
    title: str,
    actions=(),
    on_refresh=None,
) -> ft.Row:
    """Canonical screen header."""
    palette = app_colors.get()
    controls: list[ft.Control] = [
        ft.Text(title, size=FS_30, weight=ft.FontWeight.BOLD, color=palette.text)
    ]
    if on_refresh is not None:
        controls.append(
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                icon_color=palette.text_soft,
                tooltip="Actualizar",
                on_click=on_refresh,
            )
        )
    controls.extend(actions)
    return ft.Row(
        controls,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=SP_12,
    )


TABLE_PAGE_SIZE = 10
_TABLE_HEADING_H = SP_24 + SP_12
_TABLE_ROW_MIN_H = SP_24 + SP_8
_TABLE_ROW_MAX_H = SP_24 + SP_12


def paginate_rows(rows, page, page_size=TABLE_PAGE_SIZE):
    """View-side pagination tail (filter -> sort -> paginate).

    Returns ``(slice, current, total)`` with ``current`` clamped to
    ``1..total`` so prev on page 1 stays at 1 with no error.
    """
    try:
        per = max(1, int(page_size or TABLE_PAGE_SIZE))
    except (TypeError, ValueError):
        per = TABLE_PAGE_SIZE
    total = max(1, -(-len(rows or []) // per))
    try:
        current = int(page or 1)
    except (TypeError, ValueError):
        current = 1
    current = max(1, min(current, total))
    start = (current - 1) * per
    return (list((rows or [])[start : start + per]), current, total)


def TableToolbar(
    on_query=None, chips=(), actions=(), search_hint="Buscar..."
) -> ft.Row:
    """SnowUI toolbar: search field + filter chips + actions (AD-3).

    The search field keeps ``sync_text`` semantics and forwards the
    query string to ``on_query``; filtering stays view-side.
    """
    palette = app_colors.get()
    search = ft.TextField(
        hint_text=search_hint,
        expand=True,
        prefix_icon=ft.Icons.SEARCH,
        hint_style=ft.TextStyle(size=FS_14, color=palette.text_muted),
        text_style=ft.TextStyle(size=FS_14, color=palette.text),
    )
    sync_text(search)
    prev = search.on_change

    def _notify(e):
        try:
            if callable(prev):
                try:
                    prev(e)  # type: ignore[call-arg]
                except TypeError:
                    prev()  # type: ignore[call-arg]
        except Exception:
            pass
        query = ""
        try:
            if e is not None and getattr(e, "data", None) is not None:
                query = e.data
            else:
                query = search.value
        except Exception:
            try:
                query = search.value
            except Exception:
                query = ""
        if callable(on_query):
            try:
                on_query(query or "")
            except Exception:
                pass

    try:
        search.on_change = _notify
    except Exception:
        pass
    controls: list[ft.Control] = [search]
    controls.extend(list(chips or ()))
    controls.extend(list(actions or ()))
    return ft.Row(
        controls,
        spacing=SP_8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def TablePager(page, pages, on_page=None) -> ft.Row:
    """Composed pager: prev/next plus an "n de m" indicator (AD-3).

    There is no Flet-native pager in 0.84.0, so paging goes through
    this composed row. Bounds: prev on page 1 stays at 1.
    """
    palette = app_colors.get()
    try:
        total = max(1, int(pages or 1))
    except (TypeError, ValueError):
        total = 1
    try:
        current = int(page or 1)
    except (TypeError, ValueError):
        current = 1
    current = max(1, min(current, total))

    def _go(new_page):
        try:
            bounded = max(1, min(int(new_page), total))
        except (TypeError, ValueError):
            bounded = current
        if callable(on_page):
            try:
                on_page(bounded)
            except Exception:
                pass

    prev_btn = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        tooltip="Anterior",
        icon_color=palette.text_soft,
        on_click=lambda _: _go(current - 1),
        disabled=(current <= 1),
    )
    next_btn = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        tooltip="Siguiente",
        icon_color=palette.text_soft,
        on_click=lambda _: _go(current + 1),
        disabled=(current >= total),
    )
    label = ft.Text(f"{current} de {total}", size=FS_14, color=palette.text)
    return ft.Row(
        [prev_btn, label, next_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=SP_8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def AppTable(
    columns: list[ft.DataColumn],
    rows: list[ft.DataRow],
    column_spacing: int = SP_12,
    empty_message: str = "Sin datos",
    empty_icon=ft.Icons.INBOX,
    page_size: int = TABLE_PAGE_SIZE,
) -> ft.Control:
    """Denser SnowUI table with a fixed contractual page size of 10 (AD-3).

    Density knobs resolve to spacing/border tokens; heading uses
    text_soft on surface and rows use text on surface (AD-6).
    ``page_size`` documents the view-side pipeline width: screens slice
    rows view-side and MUST NOT override it. Empty-state row preserved.
    """
    palette = app_colors.get()
    if not rows:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(empty_icon, size=ICON_LG, color=palette.text_muted),
                    ft.Text(empty_message, size=FS_14, color=palette.text_soft),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=SP_8,
            ),
            padding=SP_20,
            alignment=ft.Alignment.CENTER,
        )
    return ft.DataTable(
        columns=columns,
        rows=rows,
        column_spacing=column_spacing,
        bgcolor=palette.surface,
        border=ft.Border.all(BORDER_WIDTH, palette.border),
        border_radius=ft.BorderRadius.all(R_MD),
        divider_thickness=BORDER_WIDTH,
        horizontal_margin=SP_12,
        heading_row_height=_TABLE_HEADING_H,
        data_row_min_height=_TABLE_ROW_MIN_H,
        data_row_max_height=_TABLE_ROW_MAX_H,
        heading_row_color=palette.surface,
        data_row_color=palette.surface,
        horizontal_lines=ft.BorderSide(width=BORDER_WIDTH, color=palette.border),
        heading_text_style=ft.TextStyle(
            size=FS_12, weight=ft.FontWeight.BOLD, color=palette.text_soft
        ),
        data_text_style=ft.TextStyle(size=FS_14, color=palette.text),
    )


def AppDialog(
    title: str,
    content: ft.Control,
    actions: list[ft.Control],
) -> ft.AlertDialog:
    palette = app_colors.get()
    return ft.AlertDialog(
        modal=True,
        bgcolor=palette.surface,
        shape=ft.RoundedRectangleBorder(radius=R_MD),
        title=ft.Text(title, size=FS_20, weight=ft.FontWeight.BOLD, color=palette.text),
        content=content,
        actions=actions,
        actions_alignment=ft.MainAxisAlignment.END,
    )


def confirm_delete(
    page,
    on_confirm,
    item_name="",
    title="Eliminar",
    message=None,
) -> None:
    palette = app_colors.get()
    text = message
    if text is None:
        text = (
            f'¿Eliminar "{item_name}"? Esta acción no se puede deshacer.'
            if item_name
            else "¿Eliminar este elemento? Esta acción no se puede deshacer."
        )

    state: dict = {}

    def close(_):
        state["dialog"].open = False
        page.update()

    def confirm(event):
        close(event)
        on_confirm(event)

    actions: list[ft.Control] = [
        ft.TextButton("Cancelar", on_click=close),
        ft.FilledButton(
            "Eliminar",
            on_click=confirm,
            style=ft.ButtonStyle(
                bgcolor=palette.danger,
                color=palette.on_primary,
                shape=ft.RoundedRectangleBorder(radius=R_SM),
                padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
            ),
        ),
    ]
    dialog = AppDialog(
        title,
        ft.Text(text, size=FS_14, color=palette.text_soft),
        actions=actions,
    )
    state["dialog"] = dialog
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def feedback(page: ft.Page, text: str) -> None:
    palette = app_colors.get()
    bar = ft.SnackBar(
        content=ft.Text(text, size=FS_14, color=palette.bg),
        bgcolor=palette.text,
        duration=FEEDBACK_DURATION_MS,
        open=True,
    )
    page.overlay.append(bar)
    page.update()


def Badge(text: str, role: str = "info") -> ft.Container:
    palette = app_colors.get()
    color = role_color(palette, role)
    return ft.Container(
        content=ft.Text(text, size=FS_12, weight=ft.FontWeight.W_600, color=color),
        bgcolor=palette.surface,
        border=ft.Border.all(BORDER_WIDTH, color),
        border_radius=ft.BorderRadius.all(R_PILL),
        padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_4),
    )


def ChatBubble(text: str, is_user: bool) -> ft.Row:
    palette = app_colors.get()
    if is_user:
        bubble = ft.Container(
            content=ft.Text(text, size=FS_14, color=palette.on_accent_soft),
            bgcolor=palette.accent_soft,
            border_radius=ft.BorderRadius.all(R_LG),
            padding=SP_12,
        )
        alignment = ft.MainAxisAlignment.END
    else:
        bubble = ft.Container(
            content=ft.Text(text, size=FS_14, color=palette.text),
            bgcolor=palette.surface,
            border=ft.Border.all(BORDER_WIDTH, palette.border),
            border_radius=ft.BorderRadius.all(R_LG),
            padding=SP_12,
        )
        alignment = ft.MainAxisAlignment.START
    return ft.Row([bubble], alignment=alignment)


def is_rail_for_size(width, height) -> bool:
    """Collapse rule: rail when width<=1024 OR height<=600 (1100x700 expanded)."""
    try:
        w = float(width)
        h = float(height)
    except (TypeError, ValueError):
        return True
    return w <= SHELL_BREAKPOINT_W or h <= SHELL_BREAKPOINT_H


class Sidebar(ft.Container):
    """Shell sidebar: 240px expanded, 64px icon rail collapsed.

    Expanded: brand (accent square + GesKio + muted subtitle), MENÚ label,
    40px items (icon 20 + label 14, gaps 4px, radius 8px). Active is a
    single signal: accent_soft pill + on_accent_soft icon/label semibold
    (no extra edge); hover is bg_soft. Divider separates sections;
    user-card pinned bottom (avatar + Mi negocio, tap goes Ajustes).
    Rail: centered icons 22, active pill, tooltips.
    """

    def __init__(
        self, nav_items, active_key: str, on_navigate=None, collapsed: bool = False
    ):
        super().__init__()
        self.nav_items = list(nav_items)
        self.active_key = active_key
        self.on_navigate = on_navigate
        self.collapsed = collapsed
        self.buttons: dict[str, ft.TextButton] = {}
        self._rebuild()

    def _nav_style(self, key: str) -> ft.ButtonStyle:
        palette = app_colors.get()
        active = key == self.active_key
        icon_sz = 22 if self.collapsed else 20
        if active:
            return ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: palette.accent_soft,
                    ft.ControlState.DEFAULT: palette.accent_soft,
                },
                color=palette.on_accent_soft,
                icon_color=palette.on_accent_soft,
                icon_size=icon_sz,
                shape=ft.RoundedRectangleBorder(radius=SP_8),
                padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
                text_style=ft.TextStyle(size=FS_14, weight=ft.FontWeight.W_600),
            )
        return ft.ButtonStyle(
            bgcolor={
                ft.ControlState.HOVERED: palette.bg_soft,
                ft.ControlState.DEFAULT: "transparent",
            },
            color=palette.text_muted,
            icon_color=palette.text_muted,
            icon_size=icon_sz,
            shape=ft.RoundedRectangleBorder(radius=SP_8),
            padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
            text_style=ft.TextStyle(size=FS_14),
        )

    def _brand(self) -> ft.Control:
        palette = app_colors.get()
        mark = ft.Container(
            content=ft.Text(
                "G", size=FS_18, weight=ft.FontWeight.BOLD, color=palette.on_primary
            ),
            bgcolor=palette.primary,
            border_radius=ft.BorderRadius.all(SP_8),
            padding=SP_8,
            alignment=ft.Alignment.CENTER,
        )
        if self.collapsed:
            return ft.Row([mark], alignment=ft.MainAxisAlignment.CENTER)
        return ft.Row(
            [
                mark,
                ft.Column(
                    [
                        ft.Text(
                            "GesKio",
                            size=FS_18,
                            weight=ft.FontWeight.BOLD,
                            color=palette.text,
                        ),
                        ft.Text(
                            "Gestión",
                            size=FS_12,
                            color=palette.text_muted,
                        ),
                    ],
                    spacing=SP_4,
                    expand=True,
                ),
            ],
            spacing=SP_8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _avatar(self, size: int = 32) -> ft.Container:
        palette = app_colors.get()
        return ft.Container(
            content=ft.Text(
                "M",
                size=FS_14,
                weight=ft.FontWeight.BOLD,
                color=palette.on_primary,
            ),
            bgcolor=palette.primary,
            border_radius=ft.BorderRadius.all(SP_8),
            width=size,
            height=size,
            alignment=ft.Alignment.CENTER,
        )

    def _user_row(self) -> ft.Control:
        palette = app_colors.get()
        if self.collapsed:
            row = ft.Row(
                [self._avatar()],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            try:
                row.tooltip = "Mi negocio"
            except Exception:
                pass
            return row
        card = ft.Container(
            content=ft.Row(
                [
                    self._avatar(),
                    ft.Column(
                        [
                            ft.Text(
                                "Mi negocio",
                                size=FS_14,
                                weight=ft.FontWeight.BOLD,
                                color=palette.text,
                            ),
                            ft.Text(
                                "admin@geskio",
                                size=FS_12,
                                color=palette.text_muted,
                            ),
                        ],
                        spacing=SP_4,
                        expand=True,
                    ),
                ],
                spacing=SP_8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border=ft.Border.all(BORDER_WIDTH, palette.border),
            border_radius=ft.BorderRadius.all(R_MD),
            padding=SP_8,
            tooltip="Ajustes",
        )
        try:
            card.on_click = lambda _: self._handle_nav("ajustes")
        except Exception:
            pass
        return card

    def _rebuild(self) -> None:
        palette = app_colors.get()
        self.width = SHELL_RAIL_W if self.collapsed else SHELL_SIDEBAR_W
        self.bgcolor = palette.bg_soft
        self.padding = SP_8
        self.border = ft.Border.all(BORDER_WIDTH, palette.border)
        controls: list[ft.Control] = [self._brand()]
        controls.append(
            ft.Divider(height=SP_8, thickness=BORDER_WIDTH, color=palette.border)
        )
        if not self.collapsed:
            controls.append(
                ft.Text(
                    "MENÚ",
                    size=FS_12,
                    weight=ft.FontWeight.W_600,
                    color=palette.text_muted,
                )
            )
        self.buttons = {}
        for key, icon, label in self.nav_items:
            btn = ft.TextButton(
                "" if self.collapsed else label,
                icon=icon,
                tooltip=label,
                style=self._nav_style(key),
                on_click=lambda _, k=key: self._handle_nav(k),
                height=40,
            )
            self.buttons[key] = btn
            controls.append(btn)
        controls.append(
            ft.Divider(height=SP_8, thickness=BORDER_WIDTH, color=palette.border)
        )
        controls.append(ft.Container(expand=True))
        controls.append(self._user_row())
        self.content = ft.Column(
            controls, spacing=SP_4, scroll=ft.ScrollMode.AUTO, expand=True
        )

    def refresh_chrome(self) -> None:
        """Re-resolve every chrome color from the live palette + update."""
        self._rebuild()
        self._safe_update()

    def _handle_nav(self, key: str) -> None:
        if callable(self.on_navigate):
            self.on_navigate(key)

    def set_active(self, key: str) -> None:
        self.active_key = key
        for k, btn in self.buttons.items():
            try:
                btn.style = self._nav_style(k)
            except Exception:
                pass
        self._safe_update()

    def set_collapsed(self, collapsed: bool) -> None:
        if collapsed == self.collapsed:
            return
        self.collapsed = collapsed
        self._rebuild()
        self._safe_update()

    def _safe_update(self) -> None:
        try:
            self.update()
        except Exception:
            pass


class Topbar(ft.Container):
    """Shell topbar: 56px; hamburger + title + Spanish date + theme controls.

    No search box and no user menu (out of scope by design).
    The brand Dropdown keeps v1 on_select semantics (V2-D5).
    """

    def __init__(
        self,
        title: str,
        brand_value: str,
        brand_options=(),
        on_toggle_rail=None,
        on_toggle_mode=None,
        on_brand_change=None,
        mode_is_dark: bool = False,
    ):
        super().__init__()
        self.title_text = ft.Text(title, size=FS_20, weight=ft.FontWeight.BOLD)
        self.date_text = ft.Text(fecha_actual_es(), size=FS_14)
        self.menu_btn = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="Contraer/expandir barra lateral",
            on_click=on_toggle_rail,
        )
        self.mode_btn = ft.IconButton(
            icon=ft.Icons.LIGHT_MODE if mode_is_dark else ft.Icons.DARK_MODE,
            tooltip="Cambiar tema",
            on_click=on_toggle_mode,
        )
        self.brand = ft.Dropdown(
            options=[
                ft.dropdown.Option(value, label) for value, label in brand_options
            ],
            value=brand_value,
            on_select=on_brand_change,
        )
        self.height = SHELL_TOPBAR_H
        self.padding = ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8)
        self.content = ft.Row(
            [
                self.menu_btn,
                self.title_text,
                self.date_text,
                ft.Container(expand=True),
                self.mode_btn,
                self.brand,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SP_12,
        )
        self.refresh(mode_is_dark, brand_value)

    def set_title(self, title: str) -> None:
        try:
            self.title_text.value = title
            self.title_text.update()
        except Exception:
            self.title_text.value = title

    def refresh(self, mode_is_dark: bool, brand_value: str) -> None:
        palette = app_colors.get()
        try:
            self.bgcolor = palette.surface
            self.border = ft.Border(bottom=ft.BorderSide(BORDER_WIDTH, palette.border))
            self.title_text.color = palette.text
            self.date_text.color = palette.text_muted
            try:
                self.date_text.value = fecha_actual_es()
            except Exception:
                pass
            self.menu_btn.icon_color = palette.text_soft
            self.mode_btn.icon = (
                ft.Icons.LIGHT_MODE if mode_is_dark else ft.Icons.DARK_MODE
            )
            self.mode_btn.icon_color = palette.text_soft
            self.brand.value = brand_value
        except Exception:
            pass


class Shell(ft.Row):
    """Paperpillar shell: sidebar | topbar + content slot with adapter.

    Collapse rule: rail when ``page.window.width <= 1024`` OR
    ``page.window.height <= 600``; expand only when both thresholds are
    exceeded (1100x700 boots expanded). The resize driver is
    ``WindowEventType.RESIZED`` (also honoring ``RESIZE`` while dragging)
    reading ``page.window.width/height``.

    Resize-event availability is OS-dependent (Flet docs); the topbar
    manual toggle is mandatory and works even when the OS never delivers
    resize events. The adapter renders any ``Screen`` control unchanged
    in the content slot (``navigate(key)`` keeps ``Screen``/``invalidate``
    contract, zero screen edits).
    """

    def __init__(
        self,
        page,
        nav_items,
        screens,
        active_key: str = "dash",
        brand_options=(),
    ):
        super().__init__(spacing=SP_4, expand=True)
        self.pagina = page
        self.nav_items = list(nav_items)
        self.screens = dict(screens)
        self.active_key = active_key
        self.brand_options = tuple(brand_options)
        self.labels = {key: label for key, _, label in self.nav_items}
        self.collapsed = self._initial_collapsed()
        palette = app_colors.get()
        self.sidebar = Sidebar(
            self.nav_items,
            self.active_key,
            on_navigate=self.navigate,
            collapsed=self.collapsed,
        )
        self.topbar = Topbar(
            self.labels.get(self.active_key, self.active_key),
            app_colors.theme_name,
            self.brand_options,
            on_toggle_rail=self.toggle_rail,
            on_toggle_mode=self.toggle_mode,
            on_brand_change=self.change_brand,
            mode_is_dark=(app_colors.mode == "dark"),
        )
        self.divider = ft.Divider(
            height=DIVIDER_HEIGHT,
            thickness=BORDER_WIDTH,
            color=palette.border,
        )
        self.host = ft.Container(expand=True, padding=SP_4)
        right = ft.Column(
            [self.topbar, self.divider, self.host],
            spacing=SP_4,
            expand=True,
        )
        self.controls = [self.sidebar, right]
        self._wire_resize()

    def _read_window_size(self):
        try:
            return self.pagina.window.width, self.pagina.window.height
        except Exception:
            return None, None

    def _initial_collapsed(self) -> bool:
        width, height = self._read_window_size()
        if width is None or height is None:
            return True
        return is_rail_for_size(width, height)

    def _wire_resize(self) -> None:
        try:
            self.pagina.window.on_event = self._on_window_event
        except Exception:
            pass

    def _on_window_event(self, event) -> None:
        event_type = getattr(event, "type", None)
        if event_type in (ft.WindowEventType.RESIZED, ft.WindowEventType.RESIZE):
            self._apply_breakpoint()
            return
        try:
            name = str(getattr(event_type, "value", event_type) or "").lower()
        except Exception:
            name = ""
        if name in ("resized", "resize", "none", ""):
            self._apply_breakpoint()

    def _apply_breakpoint(self) -> None:
        width, height = self._read_window_size()
        if width is None or height is None:
            return
        collapsed = is_rail_for_size(width, height)
        if collapsed != self.collapsed:
            self.collapsed = collapsed
            try:
                self.sidebar.set_collapsed(collapsed)
            except Exception:
                pass
            self._safe_update()

    def toggle_rail(self, _=None) -> None:
        self.collapsed = not self.collapsed
        try:
            self.sidebar.set_collapsed(self.collapsed)
        except Exception:
            pass
        self._safe_update()

    def navigate(self, key: str) -> None:
        if key not in self.screens:
            return
        self.active_key = key
        screen = self.screens[key]
        try:
            screen.visible = True
        except Exception:
            pass
        self.host.content = screen
        try:
            screen.al_entrar()
        except Exception:
            pass
        try:
            self.sidebar.set_active(key)
        except Exception:
            pass
        try:
            self.topbar.set_title(self.labels.get(key, key))
        except Exception:
            pass
        self._safe_update()

    def refresh_chrome(self) -> None:
        """Re-resolve every chrome color from the live palette + update."""
        palette = app_colors.get()
        try:
            self.divider.color = palette.border
        except Exception:
            pass
        try:
            self.topbar.refresh(app_colors.mode == "dark", app_colors.theme_name)
        except Exception:
            pass
        try:
            self.sidebar.refresh_chrome()
        except Exception:
            pass
        self._safe_update()

    def toggle_mode(self, _=None) -> None:
        app_colors.set_mode(
            "light" if app_colors.mode == "dark" else "dark", self.pagina
        )
        self.apply_and_rebuild()

    def change_brand(self, event) -> None:
        try:
            value = getattr(event, "data", None) or getattr(
                getattr(event, "control", None), "value", ""
            )
            if value:
                self._ultimo_brand = value
            else:
                value = getattr(self, "_ultimo_brand", "") or ""
            app_colors.set_theme(value or app_colors.theme_name, self.pagina)
        except Exception:
            return
        self.apply_and_rebuild()

    def apply_and_rebuild(self) -> None:
        app_colors.apply_to_page(self.pagina)
        for screen in self.screens.values():
            try:
                screen.invalidate()
            except Exception:
                pass
        self.refresh_chrome()
        self.navigate(self.active_key)

    def _safe_update(self) -> None:
        try:
            self.pagina.update()
        except Exception:
            pass


__all__ = [
    "AppCard",
    "AppStatCard",
    "FocalStatCard",
    "Section",
    "StatGrid",
    "Calendar",
    "PageHeader",
    "AppTable",
    "TableToolbar",
    "TablePager",
    "paginate_rows",
    "TABLE_PAGE_SIZE",
    "AppDialog",
    "confirm_delete",
    "feedback",
    "sync_text",
    "Badge",
    "ChatBubble",
    "Sidebar",
    "Topbar",
    "Shell",
    "is_rail_for_size",
    "fecha_actual_es",
    "SalesBars",
    "DIVIDER_HEIGHT",
]
