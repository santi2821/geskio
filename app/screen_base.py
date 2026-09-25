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

    # ─── helpers (Flet 0.84 runtime + compat 0.28.3/Mock) ───────────────
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
                self.pagina.snack_bar = sb  # type: ignore[attr-defined]
                sb.open = True
                self.pagina.update()
                return
            except Exception:
                pass
            try:
                if hasattr(self.pagina, "open"):
                    self.pagina.open(sb)  # type: ignore[attr-defined]
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
                    self.pagina.close(dialogo)  # type: ignore[attr-defined]
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
                    self.pagina.open(dialogo)  # type: ignore[attr-defined]
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


# Alias de compatibilidad: el merge integro pantallas main-only que importan
# `Screen`, mientras la arquitectura newer (Flet 0.84 + Marco) usa `Pantalla`.
# Ambas son la misma clase para mantener coherentes ambas suites de tests.
Screen = Pantalla
