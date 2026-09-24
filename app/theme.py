"""Tokens de disenio de GesKio (paletas rojo/verde x claro/oscuro)."""

from __future__ import annotations

import re
from dataclasses import dataclass, replace

import flet as ft

FUENTE = "Inter"

SP_4 = 4
SP_8 = 8
SP_10 = 10
SP_12 = 12
SP_16 = 16
SP_20 = 20
SP_24 = 24

R_SM = 8   # botones y elementos compactos
R_MD = 10  # campos, tablas, diálogos y tarjetas de trabajo
R_LG = 16  # paneles mayores y marco de contenido
R_PILL = 999

ANCHO_BORDE = 1
ALTO_DIVISOR = 12
DURACION_AVISO_MS = 4000

# breakpoints bajos para que 1100x700 arranque expandido
LATERAL_ANCHO = 240
RAIL_ANCHO = 64
SUPERIOR_ALTO = 56
RUPTURA_ANCHO = 1024
RUPTURA_ALTO = 600
FOCO_BORDE = 2
CONTENIDO_PADDING = SP_20
CALENDARIO_GAP = SP_8
CALENDARIO_CELDA_GAP = SP_4

ICON_SM = 18
ICON_MD = 24
ICON_LG = 36

FS_12 = 12
FS_13 = 13
FS_14 = 14
FS_16 = 16
FS_18 = 18
FS_20 = 20
FS_24 = 24
FS_28 = 28
FS_30 = 30
FS_36 = 36

# reusan la escala probada, sin tamanios nuevos
VALOR_FOCAL_FS = FS_30
VALOR_STAT_FS = FS_24

_HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")


def _hex_to_rgb(hex_value: str) -> tuple[int, int, int]:
    h = hex_value.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    clamped = tuple(max(0, min(255, c)) for c in rgb)
    return "#{:02x}{:02x}{:02x}".format(*clamped)


def _srgb_channel(value: int) -> float:
    c = value / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _luminance(hex_value: str) -> float:
    r, g, b = _hex_to_rgb(hex_value)
    return (
        0.2126 * _srgb_channel(r)
        + 0.7152 * _srgb_channel(g)
        + 0.0722 * _srgb_channel(b)
    )


def _contrast(a: str, b: str) -> float:
    la = _luminance(a)
    lb = _luminance(b)
    lighter = max(la, lb)
    darker = min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def _blend(fg_hex: str, bg_hex: str, alpha: float) -> str:
    fr, fgc, fb = _hex_to_rgb(fg_hex)
    br, bgc, bb = _hex_to_rgb(bg_hex)
    return _rgb_to_hex(
        (
            round(fr * alpha + br * (1 - alpha)),
            round(fgc * alpha + bgc * (1 - alpha)),
            round(fb * alpha + bb * (1 - alpha)),
        )
    )


def _adjust_until(accent: str, against: str, target: float, step: float) -> str:
    current = accent
    for _ in range(40):
        if _contrast(current, against) >= target:
            return current
        current = _blend("#000000" if step < 0 else "#ffffff", current, 0.08)
    return current


def resolver_acento(paleta: TemaPaleta, acento: str) -> TemaPaleta:
    # deriva toda la familia del primario desde un acento a medida
    is_light = _luminance(paleta.bg) > 0.5
    if is_light:
        ground = _adjust_until(acento, "#ffffff", 4.5, -1)
    else:
        ground = acento
        if _contrast("#ffffff", ground) < 4.5:
            ground = _adjust_until(ground, "#ffffff", 4.5, -1)
        if _contrast(ground, paleta.bg) < 3.0:
            probe = ground
            for _ in range(40):
                nxt = _blend("#ffffff", probe, 0.08)
                if _contrast("#ffffff", nxt) < 4.5:
                    break
                probe = nxt
                if _contrast(probe, paleta.bg) >= 3.0:
                    ground = probe
                    break
    soft_alpha = 0.10 if is_light else 0.14
    soft = _blend(ground, paleta.bg, soft_alpha)
    on_soft = _adjust_until(ground, soft, 4.5, -1 if is_light else 1)
    hover = _blend("#000000" if is_light else "#ffffff", ground, 0.12)
    return replace(
        paleta,
        primary=ground,
        accent_hover=hover,
        accent_soft=soft,
        on_accent_soft=on_soft,
        accent_text=ground,
    )


@dataclass(frozen=True)
class TemaPaleta:
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
    on_accent_soft: str
    success: str
    warning: str
    danger: str
    danger_text: str
    accent_text: str
    footer_hover: str
    info: str


ROJO_CLARO = TemaPaleta(
    bg="#f3f5f7",
    bg_soft="#f3f5f7",
    surface="#ffffff",
    text="#202833",
    text_soft="#4f5b67",
    text_muted="#65717e",
    border="#dde2e7",
    border_strong="#c8d0d8",
    primary="#9e3035",
    on_primary="#ffffff",
    accent_hover="#82262c",
    accent_soft="#f6eaeb",
    on_accent_soft="#84252b",
    success="#28704f",
    warning="#8a5a18",
    danger="#b33d42",
    danger_text="#a22e35",
    accent_text="#84252b",
    footer_hover="#8e3438",
    info="#425c75",
)

ROJO_OSCURO = TemaPaleta(
    bg="#121920",
    bg_soft="#171f27",
    surface="#1e2831",
    text="#ebeff3",
    text_soft="#bdc6ce",
    text_muted="#a0acb7",
    border="#2c3944",
    border_strong="#394a56",
    primary="#e49496",
    on_primary="#2b1416",
    accent_hover="#e49496",
    accent_soft="#34272a",
    on_accent_soft="#f0bfc1",
    success="#75ba91",
    warning="#e9b86f",
    danger="#e16e73",
    danger_text="#f0a0a3",
    accent_text="#e49496",
    footer_hover="#e49496",
    info="#91afc4",
)

VERDE_CLARO = TemaPaleta(
    bg="#f3f5f7",
    bg_soft="#f3f5f7",
    surface="#ffffff",
    text="#202833",
    text_soft="#4f5b67",
    text_muted="#65717e",
    border="#dde2e7",
    border_strong="#c8d0d8",
    primary="#286b50",
    on_primary="#ffffff",
    accent_hover="#1e563e",
    accent_soft="#eaf2ee",
    on_accent_soft="#225b45",
    success="#28704f",
    warning="#8a5a18",
    danger="#b33d42",
    danger_text="#a22e35",
    accent_text="#225b45",
    footer_hover="#1e563e",
    info="#425c75",
)

VERDE_OSCURO = TemaPaleta(
    bg="#121920",
    bg_soft="#171f27",
    surface="#1e2831",
    text="#ebeff3",
    text_soft="#bdc6ce",
    text_muted="#a0acb7",
    border="#2c3944",
    border_strong="#394a56",
    primary="#6bac8b",
    on_primary="#10251b",
    accent_hover="#8ac4a4",
    accent_soft="#1e3028",
    on_accent_soft="#a1d2b5",
    success="#75ba91",
    warning="#e9b86f",
    danger="#e16e73",
    danger_text="#f0a0a3",
    accent_text="#a1d2b5",
    footer_hover="#8ac4a4",
    info="#91afc4",
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


def color_rol(paleta: TemaPaleta, rol: str) -> str:
    # resuelve un rol semantico (o alias del dashboard) a un hex
    key = _ROLE_ALIASES.get(rol, rol)
    return getattr(paleta, key)


def a_tema_flet(paleta: TemaPaleta) -> ft.Theme:
    # arma el ft.Theme de Flet desde una paleta
    estilo_boton = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=R_SM),
    )
    return ft.Theme(
        font_family=FUENTE,
        button_theme=ft.ButtonTheme(style=estilo_boton),
        filled_button_theme=ft.FilledButtonTheme(style=estilo_boton),
        outlined_button_theme=ft.OutlinedButtonTheme(style=estilo_boton),
        text_button_theme=ft.TextButtonTheme(style=estilo_boton),
        color_scheme=ft.ColorScheme(
            primary=paleta.primary,
            on_primary=paleta.on_primary,
            primary_container=paleta.accent_soft,
            on_primary_container=paleta.on_accent_soft,
            secondary=paleta.info,
            on_secondary=paleta.on_primary,
            error=paleta.danger,
            on_error=paleta.on_primary,
            surface=paleta.surface,
            on_surface=paleta.text,
            on_surface_variant=paleta.text_soft,
            outline=paleta.border,
            outline_variant=paleta.border_strong,
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


class Tema:
    # paleta por marca x modo, mas acento personalizado

    THEMES: dict[str, tuple[TemaPaleta, TemaPaleta]] = {
        "rojo": (ROJO_CLARO, ROJO_OSCURO),
        "verde": (VERDE_CLARO, VERDE_OSCURO),
    }
    DEFAULT_THEME = "rojo"
    DEFAULT_MODE = "light"
    VALID_MODES = ("light", "dark")
    # misma clave que usa el landing en localStorage
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

    def get(self, mode: str | None = None) -> TemaPaleta:
        resolved = mode or self.mode
        light, dark = self.THEMES[self.theme_name]
        paleta = dark if resolved == "dark" else light
        if self.accent_override:
            paleta = resolver_acento(paleta, self.accent_override)
        return paleta

    @property
    def current(self) -> TemaPaleta:
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

    def apply_to_page(self, page: ft.Page) -> TemaPaleta:
        # aplica tema claro/oscuro y modo a la page; quien llama hace update
        light, dark = self.THEMES[self.theme_name]
        if self.accent_override:
            light = resolver_acento(light, self.accent_override)
            dark = resolver_acento(dark, self.accent_override)
        page.theme = a_tema_flet(light)
        page.dark_theme = a_tema_flet(dark)
        page.theme_mode = (
            ft.ThemeMode.DARK if self.mode == "dark" else ft.ThemeMode.LIGHT
        )
        active = dark if self.mode == "dark" else light
        page.bgcolor = active.bg
        return active


colores = Tema()
