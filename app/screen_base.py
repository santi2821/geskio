import flet as ft

from theme import SP_24


class Screen(ft.Container):
    def __init__(self, page: ft.Page, title: str):
        super().__init__(expand=True, visible=False, padding=SP_24)
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

    def build(self):
        return ft.Text(self.titulo)
