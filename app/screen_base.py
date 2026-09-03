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

    # ─── helpers Flet 0.28.3 ───────────────────────────────────────────
    def mostrar_alerta(self, texto: str):
        """Centralized SnackBar using page.snack_bar (0.28.3). No overlay."""
        try:
            sb = ft.SnackBar(
                content=ft.Text(texto),
                duration=4000,
                show_close_icon=True,
            )
            # 0.28.3 correct: asignar a page.snack_bar y abrir
            self.pagina.snack_bar = sb
            sb.open = True
            self.pagina.update()
        except Exception as ex:
            print(f"Error mostrar_alerta: {ex}")

    def cerrar_dialogo(self, dialogo: ft.AlertDialog):
        """Cierra dialogo con page.close (0.28.3). Fallback a open=False."""
        try:
            try:
                self.pagina.close(dialogo)
            except Exception:
                dialogo.open = False
                self.pagina.update()
        except Exception as ex:
            print(f"Error cerrar dialogo: {ex}")

    def abrir_dialogo(self, dialogo: ft.AlertDialog):
        """Abre dialogo con page.open (0.28.3). Fallback a open=True."""
        try:
            # Asegurar props requeridas 0.28.3
            if not hasattr(dialogo, "open") or dialogo.open is None:
                dialogo.open = False
            try:
                self.pagina.open(dialogo)
            except Exception:
                dialogo.open = True
                self.pagina.update()
        except Exception as ex:
            print(f"Error abrir dialogo: {ex}")
