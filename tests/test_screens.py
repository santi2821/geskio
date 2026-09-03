import sys
sys.path.insert(0, "app")
sys.path.insert(0, "app/screens")

class MockPage:
    def __init__(self):
        self.overlay = []
        self.controls = []
        self.snack_bar = None
        self.dialog = None
        self.title = ""
        self.window = type("obj", (object,), {"width": 1100, "height": 700})()
        self._opened = []
        self._closed = []
    def update(self): pass
    def add(self, c): self.controls.append(c)
    def open(self, control):
        control.open = True
        if control not in self.overlay:
            self.overlay.append(control)
        self._opened.append(control)
    def close(self, control):
        control.open = False
        self._closed.append(control)

def test_import_screens():
    from screen_base import Screen
    from screens.dashboard import PantallaDashboard
    from screens.stock import PantallaStock
    from screens.caja import PantallaCaja
    from screens.clientes import PantallaClientes
    from screens.fiado import PantallaFiado
    from screens.chat import PantallaChat
    assert Screen and PantallaDashboard

def test_build_screens():
    from screens.dashboard import PantallaDashboard
    from screens.stock import PantallaStock
    from screens.caja import PantallaCaja
    from screens.clientes import PantallaClientes
    from screens.fiado import PantallaFiado
    from screens.chat import PantallaChat
    page = MockPage()
    for Cls in [PantallaDashboard, PantallaStock, PantallaCaja, PantallaClientes, PantallaFiado, PantallaChat]:
        s = Cls(page)
        built = s.build()
        assert built is not None
        # actualizar no debe crashear
        try:
            s.actualizar()
        except Exception as e:
            assert False, f"{Cls.__name__}.actualizar() raised {e}"

def test_dimensionamiento_expand():
    from screens.dashboard import PantallaDashboard
    from screens.stock import PantallaStock
    page = MockPage()
    for Cls in [PantallaDashboard, PantallaStock]:
        s = Cls(page)
        b = s.build()
        # root debe ser Column expand=True
        assert getattr(b, "expand", None) is True or getattr(s, "expand", None) is True

def test_dialog_api_028():
    import flet as ft
    page = MockPage()
    from screens.stock import PantallaStock
    s = PantallaStock(page)
    s.build()
    # verificar que mostrar_alerta usa page.snack_bar o page.open, no overlay directo para SnackBar
    # Simular mostrar_alerta
    s.mostrar_alerta("test")
    # debe haber snack_bar seteado
    assert page.snack_bar is not None or len(page.overlay) > 0
