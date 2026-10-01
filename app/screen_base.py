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
        self.content = self.build()
        self.armado = True
        try:
            self.update()
        except Exception:
            self.pagina.update()

    def build(self):
        return ft.Text(self.titulo)

    def mostrar_alerta(self, texto: str):
        """SnackBar compatible: usa page.snack_bar/page.open si existen
        (tests Mock + 0.28.3); si no, overlay.append (runtime Flet 0.84)."""
        try:
            sb = ft.SnackBar(
                content=ft.Text(texto),
                duration=4000,
                show_close_icon=True,
            )
            try:
                self.pagina.snack_bar = sb
                sb.open = True
                self.pagina.update()
                return
            except Exception:
                pass
            try:
                if hasattr(self.pagina, "open"):
                    self.pagina.open(sb)
                    return
            except Exception:
                pass
            overlay = getattr(self.pagina, "overlay", None)
            if overlay is not None:
                if sb not in overlay:
                    overlay.append(sb)
                sb.open = True
            self.pagina.update()
        except Exception as ex:
            print(f"Error mostrar_alerta: {ex}")

    def cerrar_dialogo(self, dialogo: ft.AlertDialog):
        """Cierra dialogo: page.close si existe, si no open=False (0.84)."""
        try:
            try:
                if hasattr(self.pagina, "close"):
                    self.pagina.close(dialogo)
                    return
                raise AttributeError("sin page.close")
            except Exception:
                dialogo.open = False
                try:
                    dialogo.update()
                except Exception:
                    pass
                self.pagina.update()
        except Exception as ex:
            print(f"Error cerrar dialogo: {ex}")

    def abrir_dialogo(self, dialogo: ft.AlertDialog):
        """Abre dialogo: page.open si existe, si no overlay.append (0.84)."""
        try:
            if not hasattr(dialogo, "open") or dialogo.open is None:
                dialogo.open = False
            try:
                if hasattr(self.pagina, "open"):
                    self.pagina.open(dialogo)
                    return
                raise AttributeError("sin page.open")
            except Exception:
                pass
            overlay = getattr(self.pagina, "overlay", None)
            if overlay is not None and dialogo not in overlay:
                overlay.append(dialogo)
            dialogo.open = True
            try:
                dialogo.update()
            except Exception:
                pass
            self.pagina.update()
        except Exception as ex:
            print(f"Error abrir dialogo: {ex}")


Screen = Pantalla
