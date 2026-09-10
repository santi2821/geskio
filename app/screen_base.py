import flet as ft

from theme import SHELL_CONTENT_PADDING


class Screen(ft.Container):
    """Base screen rendered unchanged inside the Shell adapter slot.

    Content padding resolves to the shell content token (SP_24 grid step);
    the Shell host adds no extra padding so v1 screens keep their rhythm.
    """

    def __init__(self, page: ft.Page, title: str):
        super().__init__(expand=True, visible=False, padding=SHELL_CONTENT_PADDING)
        self.pagina = page
        self.titulo = title
        self.armado = False

    def invalidate(self):
        """Mark for rebuild on next al_entrar (theme switch hook)."""
        self.armado = False

    def al_entrar(self):
        if not self.armado:
            self.content = self.build()
            self.armado = True
        self.actualizar()
        self.pagina.update()

    def actualizar(self):
        pass

    def build(self):  # type: ignore[override]
        return ft.Text(self.titulo)
