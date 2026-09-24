import flet as ft

from theme import CONTENIDO_PADDING


class Pantalla(ft.Container):
    """Base de las pantallas del Marco."""

    def __init__(self, pagina: ft.Page, titulo: str):
        super().__init__(expand=True, visible=False, padding=CONTENIDO_PADDING)
        self.pagina = pagina
        self.titulo = titulo
        self.armado = False

    def invalidate(self):
        self.armado = False

    def al_entrar(self):
        self.rearmar()

    def actualizar(self):
        self.rearmar()

    def rearmar(self):
        # en Flet 0.84 page.update() no baja al arbol interno de la pantalla;
        # re-asignar content (prop de la pantalla) y update() es lo que repinta.
        # build() debe renderizar con los datos actuales, sin updates internos
        # (el montaje los envia todos juntos).
        self.content = self.build()
        self.armado = True
        try:
            self.update()
        except Exception:
            self.pagina.update()

    def build(self):  # type: ignore[override]
        return ft.Text(self.titulo)
