"""GesKio shared widget kit.

Every style value resolves to a ``theme.py`` token; this module defines
no color, spacing, radius, or type literal. Screens consume these fixed
defaults instead of hand-building cards, tables, dialogs, or SnackBars.
"""

from __future__ import annotations

import flet as ft

from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    FEEDBACK_DURATION_MS,
    FS_12,
    FS_14,
    FS_20,
    FS_28,
    FS_30,
    ICON_LG,
    ICON_MD,
    R_LG,
    R_MD,
    R_PILL,
    R_SM,
    SP_4,
    SP_8,
    SP_12,
    SP_20,
    app_colors,
    role_color,
)


def sync_text(field: ft.TextField) -> ft.TextField:
    """Mirror what the user typed back into ``field.value`` on every change.

    Flet 0.84 only streams TextField content to the server for fields with a
    subscribed change event. Dialog/form fields without one keep their
    construction value, so save buttons read stale text while showing a
    success message. Subscribing here keeps existing ``field.value`` readers
    working unchanged under both sync models.
    """

    def _sync(e):
        try:
            if e is not None and getattr(e, "data", None) is not None:
                field.value = e.data
        except Exception:
            pass

    try:
        field.on_change = _sync
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
    palette = app_colors.get()
    color = role_color(palette, role)
    header: list[ft.Control] = [
        ft.Text(label, size=FS_12, weight=ft.FontWeight.W_500, color=palette.text_muted)
    ]
    if icon is not None:
        header.append(ft.Icon(icon, color=color, size=ICON_MD))
    return AppCard(
        ft.Column(
            [
                ft.Row(header, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(value, size=FS_28, weight=ft.FontWeight.BOLD, color=color),
            ],
            spacing=SP_4,
        )
    )


def AppHeader(
    title: str,
    on_refresh=None,
    actions=(),
) -> ft.Row:
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


def AppTable(
    columns: list[ft.DataColumn],
    rows: list[ft.DataRow],
    column_spacing: int = SP_12,
    empty_message: str = "Sin datos",
    empty_icon=ft.Icons.INBOX,
) -> ft.Control:
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


__all__ = [
    "AppCard",
    "AppStatCard",
    "AppHeader",
    "AppTable",
    "AppDialog",
    "confirm_delete",
    "feedback",
    "sync_text",
    "Badge",
    "ChatBubble",
    "DIVIDER_HEIGHT",
]
