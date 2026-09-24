import flet as ft
import datos
from screen_base import Pantalla
from theme import (
    ANCHO_BORDE,
    FS_14,
    R_MD,
    R_SM,
    SP_4,
    SP_8,
    SP_10,
    SP_12,
    colores,
)
from widgets import campo_texto, encabezado, seccion, aviso, sincronizar_texto

ACENTOS = ("#c81e1e", "#166534", "#2563eb", "#7c3aed", "#ea580c", "#0d9488")


class PantallaAjustes(Pantalla):
    def __init__(self, page: ft.Page, al_apariencia=None):
        super().__init__(page, "Ajustes")
        self.al_apariencia = al_apariencia
        self._hex_value = ""

    def build(self):
        paleta = colores.get()
        self._seg_modo = ft.SegmentedButton(
            segments=[
                ft.Segment(value="light", label=ft.Text("Claro")),
                ft.Segment(value="dark", label=ft.Text("Oscuro")),
            ],
            selected=[colores.mode],
            on_change=self._al_modo,
        )
        tarjetas_marca = ft.Row(
            [
                self._tarjeta_marca("rojo", "Rojo"),
                self._tarjeta_marca("verde", "Verde"),
            ],
            spacing=SP_12,
            wrap=True,
        )
        muestras = ft.Row(
            [self._muestra(h) for h in ACENTOS],
            spacing=SP_8,
            wrap=True,
        )
        self.campo_hex = campo_texto(
            label="Hex personalizado",
            hint_text="#c81e1e",
            value=self._hex_value or colores.accent_override or "",
            on_submit=lambda _: self.aplicar_hex(),
            width=280,
        )
        sincronizar_texto(self.campo_hex)
        form_acento = ft.Column(
            [
                muestras,
                ft.Row(
                    [
                        self.campo_hex,
                        ft.FilledButton(
                            "Aplicar",
                            on_click=lambda _: self.aplicar_hex(),
                            style=ft.ButtonStyle(
                                bgcolor=paleta.primary,
                                color=paleta.on_primary,
                            ),
                        ),
                        ft.TextButton(
                            "Restablecer", on_click=lambda _: self.restablecer_acento()
                        ),
                    ],
                    spacing=SP_8,
                    wrap=True,
                ),
            ],
            spacing=SP_8,
        )
        personalizar_acento = ft.ExpansionTile(
            title="Color de acento",
            subtitle="Opciones de personalización",
            controls=[form_acento],
            dense=True,
            controls_padding=SP_12,
            tile_padding=ft.Padding.symmetric(horizontal=SP_8, vertical=SP_4),
            collapsed_text_color=paleta.text,
            text_color=paleta.text,
            collapsed_icon_color=paleta.text_muted,
            icon_color=paleta.text_muted,
            collapsed_shape=ft.RoundedRectangleBorder(radius=R_MD),
            shape=ft.RoundedRectangleBorder(radius=R_MD),
            collapsed_bgcolor=paleta.surface,
            bgcolor=paleta.surface,
        )
        return ft.Column(
            [
                encabezado(
                    "Preferencias",
                    al_refrescar=lambda _: self.actualizar(),
                    descripcion="Preferencias visuales y ubicación de los datos de demo.",
                ),
                seccion(
                    "Apariencia",
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Modo", size=FS_14, weight=ft.FontWeight.W_600, color=paleta.text),
                                    self._seg_modo,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Divider(color=paleta.border),
                            ft.Row(
                                [
                                    ft.Text("Color base", size=FS_14, weight=ft.FontWeight.W_600, color=paleta.text),
                                    tarjetas_marca,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                wrap=True,
                            ),
                            ft.Divider(color=paleta.border),
                            personalizar_acento,
                        ],
                        spacing=SP_10,
                    ),
                ),
                seccion(
                    "Datos de la demo",
                    ft.Column(
                        [
                            ft.Text(
                                "Los cambios se guardan automáticamente en este equipo.",
                                size=FS_14,
                                color=paleta.text,
                            ),
                            ft.Text(
                                str(datos.RUTA_ARCHIVO_DATOS),
                                size=FS_14,
                                color=paleta.text_muted,
                                selectable=True,
                            ),
                            ft.Text(
                                "Esta ubicación corresponde al archivo JSON local de la demo.",
                                size=FS_14,
                                color=paleta.text_muted,
                            ),
                        ],
                        spacing=SP_8,
                    ),
                ),
            ],
            spacing=SP_12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _tarjeta_marca(self, nombre: str, etiqueta: str) -> ft.Container:
        paleta = colores.get()
        activa = colores.theme_name == nombre
        clara, oscura = colores.THEMES[nombre]
        hex_punto = (oscura if colores.mode == "dark" else clara).primary
        return ft.OutlinedButton(
            content=etiqueta,
            icon=ft.Icons.CHECK_CIRCLE if activa else ft.Icons.RADIO_BUTTON_UNCHECKED,
            tooltip=f"Usar marca {etiqueta}",
            on_click=lambda _, n=nombre: self.fijar_marca(n),
            width=150,
            height=48,
            style=ft.ButtonStyle(
                color=paleta.primary if activa else paleta.text,
                icon_color=paleta.primary if activa else hex_punto,
                bgcolor=paleta.accent_soft if activa else paleta.surface,
                side=ft.BorderSide(ANCHO_BORDE, paleta.primary if activa else paleta.border),
                shape=ft.RoundedRectangleBorder(radius=R_SM),
            ),
        )

    def _muestra(self, hex: str) -> ft.IconButton:
        paleta = colores.get()
        activa = (colores.accent_override or "").lower() == hex.lower()
        etiqueta = {
            "#c81e1e": "Rojo",
            "#166534": "Verde",
            "#2563eb": "Azul",
            "#7c3aed": "Violeta",
            "#ea580c": "Naranja",
            "#0d9488": "Turquesa",
        }.get(hex.lower(), hex)
        return ft.IconButton(
            icon=ft.Icons.CIRCLE,
            icon_color=hex,
            tooltip=(f"Acento actual: {etiqueta}" if activa else f"Usar acento {etiqueta}"),
            on_click=lambda _, h=hex: self.fijar_acento(h),
            width=40,
            height=40,
            style=ft.ButtonStyle(
                padding=0,
                bgcolor=paleta.accent_soft if activa else paleta.surface,
                side=ft.BorderSide(2 if activa else ANCHO_BORDE, paleta.primary if activa else paleta.border),
                shape=ft.CircleBorder(),
            ),
        )

    def _al_modo(self, e) -> None:
        try:
            elegido = (
                e.control.selected
                if e is not None and hasattr(e, "control")
                else [colores.mode]
            )
            modo = elegido[0] if elegido else colores.mode
        except Exception:
            modo = colores.mode
        self.fijar_modo(modo)

    def fijar_modo(self, modo: str) -> None:
        try:
            colores.set_mode(modo, self.pagina)
        except ValueError:
            return
        self._aplicar("Modo " + ("oscuro" if modo == "dark" else "claro"))

    def fijar_marca(self, nombre: str) -> None:
        try:
            colores.set_theme(nombre, self.pagina)
        except ValueError:
            return
        self._aplicar("Marca " + nombre.capitalize())

    def fijar_acento(self, hex: str) -> None:
        try:
            colores.set_accent(hex, self.pagina)
        except ValueError:
            aviso(self.pagina, "Hex inválido (ej: #c81e1e)")
            return
        self._hex_value = hex
        self._aplicar("Acento " + hex)

    def aplicar_hex(self, e=None) -> None:
        try:
            escrito = (self.campo_hex.value or "").strip()
        except Exception:
            escrito = ""
        if not escrito:
            return
        self.fijar_acento(escrito)

    def restablecer_acento(self, e=None) -> None:
        colores.set_accent(None, self.pagina)
        self._hex_value = ""
        self._aplicar("Acento restablecido")

    def _aplicar(self, texto: str) -> None:
        self.invalidate()
        try:
            if callable(self.al_apariencia):
                self.al_apariencia()
            else:
                self.al_entrar()
        except Exception:
            pass
        try:
            aviso(self.pagina, texto)
        except Exception:
            pass
