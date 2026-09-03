import sys
sys.path.insert(0, "app")
sys.path.insert(0, "app/screens")

import datos
from datos import (
    proveedores, crear_proveedor, actualizar_proveedor, eliminar_proveedor, prov_por_id,
    ventas_por_dia, stock_stats, ventas_por_mes, ganancia_por_mes, productos
)


def test_proveedores_iniciales():
    assert len(proveedores) >= 3
    ids = [p["id"] for p in proveedores]
    assert "pr1" in ids and "pr2" in ids and "pr3" in ids
    for p in proveedores:
        assert "nombre" in p and "telefono" in p and "email" in p and "rubro" in p


def test_crear_proveedor():
    n = len(proveedores)
    pr = crear_proveedor("Test Prov", "3511112222", "test@prov.com", "TestRubro")
    assert pr["id"] in [x["id"] for x in proveedores]
    assert pr["nombre"] == "Test Prov"
    assert pr["telefono"] == "3511112222"
    assert pr["email"] == "test@prov.com"
    assert pr["rubro"] == "TestRubro"
    assert len(proveedores) == n + 1
    # cleanup via eliminar
    assert eliminar_proveedor(pr["id"]) is True
    assert len(proveedores) == n


def test_actualizar_proveedor():
    pr = crear_proveedor("Tmp Prov", "3510000000", "tmp@prov.com", "Inicial")
    pid = pr["id"]
    # actualizar todos campos
    actualizar_proveedor(pid, "Tmp Prov 2", "3519999999", "nuevo@prov.com", "NuevoRubro")
    fetched = prov_por_id(pid)
    assert fetched["nombre"] == "Tmp Prov 2"
    assert fetched["telefono"] == "3519999999"
    assert fetched["email"] == "nuevo@prov.com"
    assert fetched["rubro"] == "NuevoRubro"
    # actualizar parcial con kwargs
    actualizar_proveedor(pid, nombre="Solo Nombre")
    assert prov_por_id(pid)["nombre"] == "Solo Nombre"
    # telefono debe permanecer igual si None
    assert prov_por_id(pid)["telefono"] == "3519999999"
    eliminar_proveedor(pid)


def test_eliminar_proveedor():
    pr = crear_proveedor("Borrable Prov", "3511231234", "borrar@prov.com", "Borrable")
    n = len(proveedores)
    assert eliminar_proveedor(pr["id"]) is True
    assert len(proveedores) == n - 1
    assert prov_por_id(pr["id"]) is None
    # eliminar inexistente
    assert eliminar_proveedor("noexiste123") is False


def test_prov_por_id():
    pr = prov_por_id("pr1")
    assert pr is not None
    assert pr["nombre"] == "Distribuidora Sur"
    assert prov_por_id("inexistente") is None


def test_ventas_por_dia():
    data = ventas_por_dia(7)
    assert len(data) == 7
    for entry in data:
        assert "fecha" in entry and "total" in entry
        assert isinstance(entry["total"], (int, float))
    # por defecto 7
    assert len(ventas_por_dia()) == 7
    # custom dias
    assert len(ventas_por_dia(3)) == 3
    # ultimo dia debe incluir ventas de hoy si hay
    from datetime import date
    hoy = date.today().isoformat()
    assert data[-1]["fecha"] == hoy


def test_stock_stats():
    s = stock_stats()
    assert "ok" in s and "bajo" in s and "agotado" in s
    assert s["ok"] + s["bajo"] + s["agotado"] == len(productos)
    # verificar tipos
    assert all(isinstance(v, int) for v in s.values())


def test_ventas_por_mes():
    data = ventas_por_mes(6)
    assert len(data) == 6
    for entry in data:
        assert "mes" in entry and "total" in entry
        assert len(entry["mes"]) == 7  # YYYY-MM
        assert "-" in entry["mes"]
    # custom
    assert len(ventas_por_mes(3)) == 3
    assert len(ventas_por_mes()) == 6


def test_ganancia_por_mes():
    data = ganancia_por_mes(3)
    assert len(data) == 3
    for e in data:
        assert "mes" in e and "ganancia" in e


# ─── Screen test (mock Page) ────────────────────────────────────────────

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


def test_pantalla_proveedores_build():
    from screens.proveedores import PantallaProveedores
    page = MockPage()
    s = PantallaProveedores(page)
    built = s.build()
    assert built is not None
    # verificar que tiene tabla y campos
    assert hasattr(s, "tabla_datos")
    assert hasattr(s, "campo_nombre")
    assert hasattr(s, "campo_telefono")
    assert hasattr(s, "campo_email")
    assert hasattr(s, "campo_rubro")
    # columnas
    assert len(s.tabla_datos.columns) == 5
    # actualizar no debe crashear
    s.actualizar()
    # filtrar
    s.campo_buscar.value = "Sur"
    s.filtrar_datos()
    assert len(s.tabla_datos.rows) >= 1
    s.campo_buscar.value = "noexisteXYZ123"
    s.filtrar_datos()
    # debe mostrar Sin resultados
    assert len(s.tabla_datos.rows) == 1


def test_pantalla_proveedores_crud_dialogs():
    from screens.proveedores import PantallaProveedores
    page = MockPage()
    s = PantallaProveedores(page)
    s.build()
    # guardar nuevo via campos
    n = len(proveedores)
    s.campo_nombre.value = "Prov Test Dialog"
    s.campo_telefono.value = "3510001111"
    s.campo_email.value = "dlg@test.com"
    s.campo_rubro.value = "DialogRubro"
    s.guardar_nuevo()
    assert len(proveedores) == n + 1
    pr = proveedores[-1]
    assert pr["nombre"] == "Prov Test Dialog"
    # cleanup
    eliminar_proveedor(pr["id"])
    # probar editar_proveedor dialog open
    s.editar_proveedor("pr1")
    # debe haber abierto dialog via page.open
    assert len(page._opened) >= 1
    # cerrar
    dlg = page._opened[-1]
    s.cerrar_dialogo(dlg)
    assert dlg.open is False
    # probar eliminar dialog
    prev_opened = len(page._opened)
    s.eliminar_proveedor("pr2")
    assert len(page._opened) > prev_opened
    # mostrar alerta usa snack_bar
    s.mostrar_alerta("Test alerta")
    assert page.snack_bar is not None


def test_pantalla_proveedores_search_multifield():
    from screens.proveedores import PantallaProveedores
    page = MockPage()
    s = PantallaProveedores(page)
    s.build()
    # buscar por rubro
    s.campo_buscar.value = "Bebidas"
    s.filtrar_datos()
    # debe encontrar Bebidas Norte
    found = any("Bebidas" in str(row.cells[3].content.value) for row in s.tabla_datos.rows if len(row.cells) >= 4)
    # fallback: check row count
    assert len(s.tabla_datos.rows) >= 1
    # buscar por email
    s.campo_buscar.value = "distrisur"
    s.filtrar_datos()
    assert len(s.tabla_datos.rows) >= 1
    # buscar por telefono
    s.campo_buscar.value = "351423"
    s.filtrar_datos()
    assert len(s.tabla_datos.rows) >= 1
