"""GesKio design tokens (single namespace).

Provenance: colors/radii/typography come from ``landing/styles.css``
``:root`` / ``[data-theme="dark"]``; spacing steps {4, 8, 10, 12, 20, 24}
come from established app patterns. Reference kits contribute patterns
only, never values.

Flet 0.84.0 verified in this env: ``ft.Theme(color_scheme=...)``,
``ft.ColorScheme``, ``page.theme`` / ``page.dark_theme`` /
``page.theme_mode``, ``page.fonts``, ``page.overlay`` and
``SnackBar(open=True, duration=...)`` exist. ``page.client_storage``,
``page.show_snack_bar`` and ``page.open`` do NOT exist, so persistence
resolves ``client_storage`` (forward-compat) then ``page.session.store``
with an in-memory fallback, and feedback goes through ``page.overlay``.

Hover derivation: the light hover darkens the primary (#ef4444 ->
#dc2626) for contrast on light surfaces; the dark hover lightens it
(#f43f5e -> #fb7185) for contrast on dark surfaces. The verde alternate
mirrors this: light darkens (#16a34a -> #15803d), dark lightens
(#15803d -> #16a34a).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace

import flet as ft

FONT_FAMILY = "Inter"

SP_4 = 4
SP_8 = 8
SP_10 = 10
SP_12 = 12
SP_20 = 20
SP_24 = 24

R_SM = 10
R_MD = 12
R_LG = 18
R_PILL = 999

BORDER_WIDTH = 1
DIVIDER_HEIGHT = 12
FEEDBACK_DURATION_MS = 4000

ICON_SM = 18
ICON_MD = 24
ICON_LG = 36

FS_12 = 12
FS_13 = 13
FS_14 = 14
FS_16 = 16
FS_18 = 18
FS_20 = 20
FS_28 = 28
FS_30 = 30
FS_36 = 36

_HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")


@dataclass(frozen=True)
class PaletteTheme:
    bg: str
    bg_soft: str
    surface: str
    text: str
    text_soft: str
    text_muted: str
    border: str
    border_strong: str
    primary: str
    on_primary: str
    accent_hover: str
    accent_soft: str
    success: str
    warning: str
    danger: str
    info: str


ROJO_LIGHT = PaletteTheme(
    bg="#ffffff",
    bg_soft="#f6f7f9",
    surface="#ffffff",
    text="#161b22",
    text_soft="#52606d",
    text_muted="#8993a3",
    border="#e7e9ed",
    border_strong="#d5d9e0",
    primary="#ef4444",
    on_primary="#ffffff",
    accent_hover="#dc2626",
    # Pre-blended approx of landing rgba(239,68,68,.10) over bg.
    accent_soft="#fdecec",
    success="#16a34a",
    warning="#d97706",
    danger="#dc2626",
    info="#2563eb",
)

ROJO_DARK = PaletteTheme(
    bg="#0e1014",
    bg_soft="#15181e",
    surface="#181c23",
    text="#f3f5f8",
    text_soft="#aab2bf",
    text_muted="#6e7783",
    border="#232831",
    border_strong="#2f3540",
    primary="#f43f5e",
    on_primary="#ffffff",
    accent_hover="#fb7185",
    # Pre-blended approx of landing rgba(244,63,94,.14) over bg.
    accent_soft="#2e161e",
    success="#4ade80",
    warning="#fbbf24",
    danger="#fb7185",
    info="#60a5fa",
)

VERDE_LIGHT = PaletteTheme(
    bg="#ffffff",
    bg_soft="#f6f7f9",
    surface="#ffffff",
    text="#161b22",
    text_soft="#52606d",
    text_muted="#8993a3",
    border="#e7e9ed",
    border_strong="#d5d9e0",
    primary="#16a34a",
    on_primary="#ffffff",
    accent_hover="#15803d",
    accent_soft="#e7f5ec",
    success="#16a34a",
    warning="#d97706",
    danger="#dc2626",
    info="#2563eb",
)

VERDE_DARK = PaletteTheme(
    bg="#0e1014",
    bg_soft="#15181e",
    surface="#181c23",
    text="#f3f5f8",
    text_soft="#aab2bf",
    text_muted="#6e7783",
    border="#232831",
    border_strong="#2f3540",
    primary="#15803d",
    on_primary="#ffffff",
    accent_hover="#16a34a",
    accent_soft="#0e1f19",
    success="#4ade80",
    warning="#fbbf24",
    danger="#fb7185",
    info="#60a5fa",
)

_ROLE_ALIASES = {
    "hoy": "success",
    "paid": "success",
    "mes": "info",
    "ganancia": "warning",
    "due": "warning",
    "deben": "danger",
    "late": "danger",
}


def role_color(palette: PaletteTheme, role: str) -> str:
    """Resolve a semantic role (or dashboard/state alias) to a hex color."""
    key = _ROLE_ALIASES.get(role, role)
    return getattr(palette, key)


def to_flet_theme(palette: PaletteTheme) -> ft.Theme:
    """Build an ft.Theme from a palette (font via ADR-2, no bundling)."""
    return ft.Theme(
        font_family=FONT_FAMILY,
        color_scheme=ft.ColorScheme(
            primary=palette.primary,
            on_primary=palette.on_primary,
            primary_container=palette.accent_soft,
            on_primary_container=palette.primary,
            secondary=palette.info,
            on_secondary=palette.on_primary,
            error=palette.danger,
            on_error=palette.on_primary,
            surface=palette.surface,
            on_surface=palette.text,
            on_surface_variant=palette.text_soft,
            outline=palette.border,
            outline_variant=palette.border_strong,
        ),
    )


_MEMORY_FALLBACK: dict[str, str] = {}


def _read_key(page: ft.Page, key: str) -> str | None:
    store = getattr(page, "client_storage", None)
    if store is not None:
        try:
            value = store.get(key)
            if value is not None:
                return str(value)
        except Exception:
            pass
    try:
        value = page.session.store.get(key)
        if value is not None:
            return str(value)
    except Exception:
        pass
    return _MEMORY_FALLBACK.get(key)


def _write_key(page: ft.Page, key: str, value: str) -> None:
    store = getattr(page, "client_storage", None)
    if store is not None:
        try:
            store.set(key, value)
        except Exception:
            pass
    try:
        page.session.store.set(key, value)
    except Exception:
        pass
    _MEMORY_FALLBACK[key] = value


class AppColors:
    """Theme registry: brand x mode palettes plus accent personalization."""

    THEMES: dict[str, tuple[PaletteTheme, PaletteTheme]] = {
        "rojo": (ROJO_LIGHT, ROJO_DARK),
        "verde": (VERDE_LIGHT, VERDE_DARK),
    }
    DEFAULT_THEME = "rojo"
    DEFAULT_MODE = "light"
    VALID_MODES = ("light", "dark")
    # MODE_KEY shares landing `localStorage geskio-theme` semantics.
    MODE_KEY = "geskio-theme"
    BRAND_KEY = "geskio-brand"
    ACCENT_KEY = "geskio-accent"

    def __init__(
        self,
        theme_name: str = DEFAULT_THEME,
        mode: str = DEFAULT_MODE,
        accent_override: str | None = None,
    ) -> None:
        self.theme_name = theme_name
        self.mode = mode
        self.accent_override = accent_override

    @classmethod
    def available_themes(cls) -> list[str]:
        return list(cls.THEMES)

    def get(self, mode: str | None = None) -> PaletteTheme:
        resolved = mode or self.mode
        light, dark = self.THEMES[self.theme_name]
        palette = dark if resolved == "dark" else light
        if self.accent_override:
            palette = replace(palette, primary=self.accent_override)
        return palette

    @property
    def current(self) -> PaletteTheme:
        return self.get()

    def set_theme(self, name: str, page: ft.Page | None = None) -> None:
        if name not in self.THEMES:
            raise ValueError(f"Unknown theme: {name}")
        self.theme_name = name
        if page is not None:
            _write_key(page, self.BRAND_KEY, name)

    def set_mode(self, mode: str, page: ft.Page | None = None) -> None:
        if mode not in self.VALID_MODES:
            raise ValueError(f"Unknown mode: {mode}")
        self.mode = mode
        if page is not None:
            _write_key(page, self.MODE_KEY, mode)

    def set_accent(self, value: str | None, page: ft.Page | None = None) -> None:
        if value is not None and not (
            isinstance(value, str) and _HEX_RE.fullmatch(value)
        ):
            raise ValueError(f"Invalid accent hex: {value}")
        self.accent_override = value
        if page is not None:
            _write_key(page, self.ACCENT_KEY, value or "")

    def load_from_store(self, page: ft.Page) -> None:
        brand = _read_key(page, self.BRAND_KEY)
        if brand in self.THEMES:
            self.theme_name = brand
        stored_mode = _read_key(page, self.MODE_KEY)
        if stored_mode in self.VALID_MODES:
            self.mode = stored_mode
        accent = _read_key(page, self.ACCENT_KEY)
        if accent and _HEX_RE.fullmatch(accent):
            self.accent_override = accent

    def save_to_store(self, page: ft.Page) -> None:
        _write_key(page, self.BRAND_KEY, self.theme_name)
        _write_key(page, self.MODE_KEY, self.mode)
        _write_key(page, self.ACCENT_KEY, self.accent_override or "")

    def apply_to_page(self, page: ft.Page) -> PaletteTheme:
        """Push light/dark ft.Themes plus theme_mode; caller runs update."""
        light, dark = self.THEMES[self.theme_name]
        if self.accent_override:
            light = replace(light, primary=self.accent_override)
            dark = replace(dark, primary=self.accent_override)
        page.theme = to_flet_theme(light)
        page.dark_theme = to_flet_theme(dark)
        page.theme_mode = (
            ft.ThemeMode.DARK if self.mode == "dark" else ft.ThemeMode.LIGHT
        )
        active = dark if self.mode == "dark" else light
        page.bgcolor = active.bg
        return active


app_colors = AppColors()
