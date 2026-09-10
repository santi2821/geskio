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

Hover derivation: the light hover darkens the primary (#c81e1e ->
#b91c1c) for contrast on light surfaces; the dark hover lightens it
(#e11d48 -> #f43f5e) for contrast on dark surfaces. The verde alternate
mirrors this: light darkens (#166534 -> #14532d), dark keeps a deep
base (#15803d) whose hover lightens (#16a34a) for icons on dark.

Hardening slice (B-1..B-7, geskio): recalibrated to WCAG 2.2 AA.
Decision B-2: deepen the LIGHT primaries inside the brand family
(rojo #ef4444 -> #c81e1e, verde #16a34a -> #166534) and keep white
on-primary, instead of darkening on-primary to near-black. Rationale:
white-on-red CTA preserves brand; a dark on-primary would break the
shared on_primary used by the danger button. Dark rojo primary is
deepened (#f43f5e -> #e11d48) so white-on-primary passes; nav and
chat bubbles use text-on-accent_soft (15+:1) so primary vibrancy loss
does not affect chrome legibility. Danger dark is a deep ground
(#fb7185 -> #dc2626) so white-on-danger passes 4.83 (B-3).
Danger-as-text is split: `danger` stays the button/background ground
(#dc2626 both modes) while `danger_text` carries normal-text usage
(light #dc2626 = 4.83 on #fff; dark #fb7185 = 6.35 on #181c23).

Recalculated key pairs (sRGB relative luminance, WCAG 1.4.3 normal
text >= 4.5, large/UI >= 3.0; next verify must assert these):
- light muted #606b7a on bg-soft #f6f7f9: 5.05 / on surface #fff: 5.41
- dark muted #7f8894 on bg-soft #15181e: 4.95 / on surface #181c23: 4.76
- light rojo white on #c81e1e: 5.74 (was 3.76); verde white on #166534: 7.13 (was 3.30)
- dark rojo white on #e11d48: 4.70 (was 3.67); verde dark white on #15803d: 5.02 (kept)
- dark white on danger #dc2626: 4.83 (was 2.69)
- danger_text light #dc2626 on #fff: 4.83; dark #fb7185 on #181c23: 6.35
- light nav rojo #c81e1e on accent_soft #fdecec: 5.02 (was 3.29);
  verde #166534 on #e7f5ec: 6.34 (was 2.93); nav also bold + 2px border (B-6)
- light due warning #b45309 on #fff: 5.02 (was 3.19), plus icon + bold (B-5)
- light bubble text #161b22 on #fdecec: 15.15; dark text #f3f5f8 on #2e161e: 15.39 (B-4)
- landing focus ring/input halo solid accent: light #c81e1e on #fff 5.74,
  dark #e11d48 on #0e1014 4.05 (both >= 3.0, B-7).
Resolved split (micro-fix): `danger` #dc2626 on dark surface #181c23 =
3.54 (passes 3:1 UI/large, fails 4.5 normal) is kept for button
backgrounds only; `danger_text` (#dc2626 light / #fb7185 dark) is
used for 14px normal text (stock bajo, debe, late) and passes >= 4.5
in both modes. Landing 1:1 holds incl. --danger-text (see styles.css).
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
    danger_text: str
    info: str


ROJO_LIGHT = PaletteTheme(
    bg="#ffffff",
    bg_soft="#f6f7f9",
    surface="#ffffff",
    text="#161b22",
    text_soft="#52606d",
    text_muted="#606b7a",
    border="#e7e9ed",
    border_strong="#d5d9e0",
    primary="#c81e1e",
    on_primary="#ffffff",
    accent_hover="#b91c1c",
    # Pre-blended approx of landing rgba(200,30,30,.10) over bg.
    accent_soft="#fdecec",
    success="#16a34a",
    warning="#b45309",
    danger="#dc2626",
    danger_text="#dc2626",
    info="#2563eb",
)

ROJO_DARK = PaletteTheme(
    bg="#0e1014",
    bg_soft="#15181e",
    surface="#181c23",
    text="#f3f5f8",
    text_soft="#aab2bf",
    text_muted="#7f8894",
    border="#232831",
    border_strong="#2f3540",
    primary="#f43f5e",
    on_primary="#ffffff",
    accent_hover="#fb7185",
    # Pre-blended approx of landing rgba(244,63,94,.14) over bg.
    accent_soft="#2e161e",
    success="#4ade80",
    warning="#fbbf24",
    danger="#dc2626",
    danger_text="#fb7185",
    info="#60a5fa",
)

VERDE_LIGHT = PaletteTheme(
    bg="#ffffff",
    bg_soft="#f6f7f9",
    surface="#ffffff",
    text="#161b22",
    text_soft="#52606d",
    text_muted="#606b7a",
    border="#e7e9ed",
    border_strong="#d5d9e0",
    primary="#166534",
    on_primary="#ffffff",
    accent_hover="#14532d",
    accent_soft="#e7f5ec",
    success="#16a34a",
    warning="#b45309",
    danger="#dc2626",
    danger_text="#dc2626",
    info="#2563eb",
)

VERDE_DARK = PaletteTheme(
    bg="#0e1014",
    bg_soft="#15181e",
    surface="#181c23",
    text="#f3f5f8",
    text_soft="#aab2bf",
    text_muted="#7f8894",
    border="#232831",
    border_strong="#2f3540",
    primary="#15803d",
    on_primary="#ffffff",
    accent_hover="#16a34a",
    accent_soft="#0e1f19",
    success="#4ade80",
    warning="#fbbf24",
    danger="#dc2626",
    danger_text="#fb7185",
    info="#60a5fa",
)

_ROLE_ALIASES = {
    "hoy": "success",
    "paid": "success",
    "mes": "info",
    "ganancia": "warning",
    "due": "warning",
    "deben": "danger",
    "late": "danger_text",
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
