from types import SimpleNamespace

from theme import RAIL_ANCHO, LATERAL_ANCHO
from widgets import Marco


class _Page:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = SimpleNamespace(width=1100, height=700)
        self.on_resize = None
        self.update_count = 0

    def update(self):
        self.update_count += 1


def test_marco_usa_ancho_real_y_reacciona_al_resize_del_navegador():
    page = _Page(width=390, height=844)
    marco = Marco(page, [], {})

    assert marco.colapsado is True
    assert marco.lateral.width == RAIL_ANCHO
    assert marco.superior.icono_fecha.visible is False
    assert marco.superior.texto_fecha.visible is False

    page.width = 1280
    page.height = 800
    page.on_resize(SimpleNamespace(width=1280, height=800))

    assert marco.colapsado is False
    assert marco.lateral.width == LATERAL_ANCHO
    assert marco.superior.icono_fecha.visible is True
    assert marco.superior.texto_fecha.visible is True

    page.width = 390
    page.height = 844
    page.on_resize(SimpleNamespace(width=390, height=844))

    assert marco.colapsado is True
    assert marco.lateral.width == RAIL_ANCHO
    assert marco.superior.icono_fecha.visible is False
    assert page.update_count >= 2


def test_marco_preserva_callback_de_resize_existente():
    eventos = []
    page = _Page(width=1280, height=800)
    page.on_resize = eventos.append
    marco = Marco(page, [], {})
    evento = SimpleNamespace(width=390, height=844)

    page.on_resize(evento)

    assert eventos == [evento]
    assert marco.colapsado is True
    assert marco.superior.icono_fecha.visible is False
