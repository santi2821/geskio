import flet as ft
from screen_base import Screen
from theme import FS_14, SP_8, SP_10, SP_12, app_colors
from widgets import PageHeader, Section, feedback, sync_text

ACCENT_PRESETS = ("#c81e1e", "#166534", "#2563eb", "#7c3aed", "#ea580c", "#0d9488")
_SWATCH_SIZE = 40


class PantallaAjustes(Screen):
    def __init__(self, page: ft.Page, on_appearance=None):
        super().__init__(page, "Ajustes")
        self.on_appearance = on_appearance
        self._hex_value = ""

    def actualizar(self):
        if self.armado:
            self.content = self.build()
            self._safe_update()

    def build(self):
        palette = app_colors.get()
        self._seg_modo = ft.SegmentedButton(
            segments=[
                ft.Segment(value="light", label=ft.Text("Claro")),
                ft.Segment(value="dark", label=ft.Text("Oscuro")),
            ],
            selected=[app_colors.mode],
            on_change=self._on_modo,
        )
        marca_cards = ft.Row(
            [self._marca_card("rojo", "Rojo"), self._marca_card("verde", "Verde")],
            spacing=SP_12,
        )
        swatches = ft.Row(
            [self._swatch(h) for h in ACCENT_PRESETS],
            spacing=SP_8,
            wrap=True,
        )
        self.campo_hex = ft.TextField(
            label="Hex personalizado",
            hint_text="#c81e1e",
            value=self._hex_value or app_colors.accent_override or "",
            on_submit=lambda _: self.aplicar_hex(),
        )
        sync_text(self.campo_hex)
        acento_form = ft.Column(
            [
                swatches,
                ft.Row(
                    [
                        self.campo_hex,
                        ft.ElevatedButton(
                            "Aplicar", on_click=lambda _: self.aplicar_hex()
                        ),
                        ft.TextButton(
                            "Restablecer", on_click=lambda _: self.restablecer_acento()
                        ),
                    ],
                    spacing=SP_8,
                ),
                ft.Text(
                    "El acento tiñe botones y enlaces activos.",
                    size=FS_14,
                    color=palette.text_muted,
                ),
            ],
            spacing=SP_8,
        )
        return ft.Column(
            [
                PageHeader("Ajustes", on_refresh=lambda _: self.actualizar()),
                Section("Modo", self._seg_modo),
                Section("Marca", marca_cards),
                Section("Acento", acento_form),
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _marca_card(self, name: str, label: str) -> ft.Container:
        palette = app_colors.get()
        active = app_colors.theme_name == name
        light, dark = app_colors.THEMES[name]
        dot_hex = (dark if app_colors.mode == "dark" else light).primary
        dot = ft.Container(
            width=_SWATCH_SIZE,
            height=_SWATCH_SIZE,
            bgcolor=dot_hex,
            border_radius=ft.BorderRadius.all(_SWATCH_SIZE // 2),
        )
        marca = ft.Text(
            label, size=FS_14, weight=ft.FontWeight.BOLD, color=palette.text
        )
        tick = (
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=palette.success)
            if active
            else ft.Container()
        )
        card = ft.Container(
            content=ft.Row([dot, marca, tick], spacing=SP_8),
            padding=SP_12,
            bgcolor=palette.surface,
            border=ft.Border.all(
                2 if active else 1, palette.primary if active else palette.border
            ),
            border_radius=ft.BorderRadius.all(SP_8),
        )
        card.on_click = lambda _, n=name: self.set_marca(n)
        card.tooltip = label
        return card

    def _swatch(self, hex_value: str) -> ft.Container:
        palette = app_colors.get()
        active = (app_colors.accent_override or "").lower() == hex_value.lower()
        sw = ft.Container(
            width=_SWATCH_SIZE,
            height=_SWATCH_SIZE,
            bgcolor=hex_value,
            border=ft.Border.all(
                2 if active else 1, palette.primary if active else palette.border
            ),
            border_radius=ft.BorderRadius.all(SP_8),
            tooltip=hex_value,
        )
        sw.on_click = lambda _, h=hex_value: self.set_acento(h)
        return sw

    def _on_modo(self, e) -> None:
        try:
            selected = (
                e.control.selected
                if e is not None and hasattr(e, "control")
                else [app_colors.mode]
            )
            modo = selected[0] if selected else app_colors.mode
        except Exception:
            modo = app_colors.mode
        self.set_modo(modo)

    def set_modo(self, modo: str) -> None:
        try:
            app_colors.set_mode(modo, self.pagina)
        except ValueError:
            return
        self._aplicar("Modo " + ("oscuro" if modo == "dark" else "claro"))

    def set_marca(self, name: str) -> None:
        try:
            app_colors.set_theme(name, self.pagina)
        except ValueError:
            return
        self._aplicar("Marca " + name)

    def set_acento(self, hex_value: str) -> None:
        try:
            app_colors.set_accent(hex_value, self.pagina)
        except ValueError:
            feedback(self.pagina, "Hex inválido (ej: #c81e1e)")
            return
        self._hex_value = hex_value
        self._aplicar("Acento " + hex_value)

    def aplicar_hex(self, e=None) -> None:
        try:
            typed = (self.campo_hex.value or "").strip()
        except Exception:
            typed = ""
        if not typed:
            return
        self.set_acento(typed)

    def restablecer_acento(self, e=None) -> None:
        app_colors.set_accent(None, self.pagina)
        self._hex_value = ""
        self._aplicar("Acento restablecido")

    def _aplicar(self, texto: str) -> None:
        self.invalidate()
        try:
            if callable(self.on_appearance):
                self.on_appearance()
            else:
                self.al_entrar()
        except Exception:
            pass
        try:
            feedback(self.pagina, texto)
        except Exception:
            pass

    def _safe_update(self) -> None:
        try:
            self.pagina.update()
        except Exception:
            pass
