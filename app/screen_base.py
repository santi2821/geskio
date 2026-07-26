import flet as ft


class Screen(ft.Container):

    def __init__(self, page: ft.Page, title: str):
        super().__init__(expand=True, visible=False, padding=24)
        self.pagina = page
        self.titulo = title
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
