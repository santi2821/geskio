import sys
sys.path.insert(0, "app")
sys.path.insert(0, "app/screens")

import flet as ft

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

def collect_controls(root, types):
    found = []
    stack = [root]
    visited = set()
    while stack:
        cur = stack.pop()
        if id(cur) in visited:
            continue
        visited.add(id(cur))
        if isinstance(cur, types):
            found.append(cur)
        if hasattr(cur, "controls") and isinstance(cur.controls, (list, tuple)):
            for child in cur.controls:
                if isinstance(child, ft.Control):
                    stack.append(child)
        if hasattr(cur, "content") and isinstance(cur.content, ft.Control):
            stack.append(cur.content)
        if hasattr(cur, "actions") and isinstance(cur.actions, (list, tuple)):
            for child in cur.actions:
                if isinstance(child, ft.Control):
                    stack.append(child)
        if hasattr(cur, "rows") and isinstance(getattr(cur, "rows"), list):
            for row in cur.rows:
                if hasattr(row, "cells"):
                    for cell in row.cells:
                        if hasattr(cell, "content") and isinstance(cell.content, ft.Control):
                            stack.append(cell.content)
    return found

def _load_screens():
    screens = {}
    from screens.dashboard import PantallaDashboard
    from screens.stock import PantallaStock
    from screens.caja import PantallaCaja
    from screens.clientes import PantallaClientes
    from screens.fiado import PantallaFiado
    from screens.chat import PantallaChat
    screens["dashboard"] = PantallaDashboard
    screens["stock"] = PantallaStock
    screens["caja"] = PantallaCaja
    screens["clientes"] = PantallaClientes
    screens["fiado"] = PantallaFiado
    screens["chat"] = PantallaChat
    try:
        from screens.proveedores import PantallaProveedores
        screens["proveedores"] = PantallaProveedores
    except Exception:
        pass
    return screens

SCREENS = _load_screens()

def test_each_screen_build_expand_true():
    for name, Cls in SCREENS.items():
        page = MockPage()
        s = Cls(page)
        built = s.build()
        assert built is not None, f"{name} build retorno None"
        assert isinstance(built, (ft.Container, ft.Column)), f"{name} build debe retornar Container/Column got {type(built)}"
        expand_ok = False
        if getattr(built, "expand", None) is True:
            expand_ok = True
        elif isinstance(built, ft.Container) and getattr(getattr(built, "content", None), "expand", None) is True:
            expand_ok = True
        if not expand_ok and getattr(s, "expand", None) is True:
            expand_ok = True
        if not expand_ok:
            cols = collect_controls(built, (ft.Column, ft.ListView))
            for col in cols:
                if getattr(col, "expand", None) is True:
                    expand_ok = True
                    break
        assert expand_ok, f"{name} build debe tener expand=True en root o Column interna"

def test_dimensionamiento_scroll_auto_donde_corresponde():
    for name, Cls in SCREENS.items():
        page = MockPage()
        s = Cls(page)
        built = s.build()
        rows = collect_controls(built, ft.Row)
        listviews = collect_controls(built, ft.ListView)
        columns = collect_controls(built, ft.Column)

        has_scroll_auto = False
        for r in rows:
            if getattr(r, "scroll", None) == ft.ScrollMode.AUTO:
                has_scroll_auto = True
                break
        if not has_scroll_auto:
            for c in columns:
                if getattr(c, "scroll", None) == ft.ScrollMode.AUTO:
                    has_scroll_auto = True
                    break
        for lv in listviews:
            if getattr(lv, "auto_scroll", False) is True:
                has_scroll_auto = True
                break
            if getattr(lv, "expand", None) is True:
                has_scroll_auto = True
                break

        if name in ("dashboard", "stock", "caja", "clientes", "fiado", "proveedores"):
            assert has_scroll_auto, f"{name} debe tener al menos un Row/Column con scroll=AUTO o ListView expand/auto_scroll"
        elif name == "chat":
            assert any(getattr(lv, "auto_scroll", False) is True for lv in listviews), f"{name} debe tener ListView auto_scroll True"
            assert any(getattr(lv, "expand", None) is True for lv in listviews), f"{name} ListView debe tener expand True"

def test_caja_dimensionamiento_detalle():
    from screens.caja import PantallaCaja
    from theme import CARRITO_ALTO_MAX, CARRITO_ALTO_MIN
    page = MockPage()
    s = PantallaCaja(page)
    built = s.build()
    assert built.scroll == ft.ScrollMode.AUTO
    assert isinstance(s._zona_carrito, ft.ListView)
    assert s._zona_carrito in collect_controls(built, ft.ListView)
    assert s._zona_carrito.auto_scroll is True
    assert s._zona_carrito.height == CARRITO_ALTO_MIN
    assert len(s._zona_carrito.controls) == 1

    responsive_rows = collect_controls(built, ft.ResponsiveRow)
    assert len(responsive_rows) == 2
    assert s.combo_cliente.col == {"xs": 12, "sm": 6}
    assert s.combo_pago.col == {"xs": 12, "sm": 6}
    assert s.combo_producto.col == {"xs": 12, "sm": 7}
    assert s.campo_cantidad.col == {"xs": 12, "sm": 2}
    assert s.campo_cantidad.expand is True
    fila_producto = next(r for r in responsive_rows if s.combo_producto in r.controls)
    assert fila_producto.controls[-1].col == {"xs": 12, "sm": 3}
    assert s.campo_cantidad.label == "Cantidad"

    s.items_carrito = [
        {"prod_id": str(i), "nombre": f"Producto {i}", "cantidad": 1, "precio": 100}
        for i in range(5)
    ]
    s._pintar_carrito()
    assert s._zona_carrito.height == CARRITO_ALTO_MAX
    assert len(s._zona_carrito.controls) == 5
    assert all(
        any(
            button.tooltip.startswith("Quitar Producto ")
            for button in collect_controls(row, ft.IconButton)
        )
        for row in s._zona_carrito.controls
    )

def test_stock_dimensionamiento_detalle():
    from screens.stock import PantallaStock
    page = MockPage()
    s = PantallaStock(page)
    built = s.build()
    assert hasattr(s, "tabla_datos")
    assert isinstance(s.tabla_datos, ft.DataTable)
    assert s.tabla_datos.expand is True
    rows = collect_controls(built, ft.Row)
    found_row_scroll = any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows)
    assert found_row_scroll, "Stock DataTable debe estar dentro de Row con scroll AUTO"
    assert isinstance(built, ft.Column)
    assert built.scroll == ft.ScrollMode.AUTO
    assert built.expand is True
    input_rows = [r for r in rows if any(isinstance(child, ft.TextField) for child in getattr(r, "controls", []))]
    if input_rows:
        assert any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in input_rows) or found_row_scroll

def test_clientes_fiado_dimensionamiento():
    from screens.clientes import PantallaClientes
    from screens.fiado import PantallaFiado
    for Cls in (PantallaClientes, PantallaFiado):
        page = MockPage()
        s = Cls(page)
        built = s.build()
        assert hasattr(s, "tabla_datos")
        assert built.scroll == ft.ScrollMode.AUTO or any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in collect_controls(built, ft.Row))
        rows = collect_controls(built, ft.Row)
        assert any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows), f"{Cls.__name__} debe tener Row scroll AUTO"

def test_dashboard_dimensionamiento():
    from screens.dashboard import PantallaDashboard
    page = MockPage()
    s = PantallaDashboard(page)
    built = s.build()
    assert isinstance(built, ft.Container)
    assert built.expand is True
    inner = built.content
    assert isinstance(inner, ft.Column)
    assert inner.expand is True
    assert inner.scroll == ft.ScrollMode.AUTO
    rows = collect_controls(built, ft.Row)
    assert any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows), "Dashboard debe tener Row scroll AUTO"

def test_chat_dimensionamiento_detalle():
    from screens.chat import PantallaChat
    page = MockPage()
    s = PantallaChat(page)
    built = s.build()
    assert isinstance(built, ft.Column)
    assert built.expand is True
    assert isinstance(s.contenedor_mensajes, ft.ListView)
    assert s.contenedor_mensajes.auto_scroll is True
    assert s.contenedor_mensajes.expand is True
    containers = collect_controls(built, ft.Container)
    msg_container = None
    for c in containers:
        if getattr(c, "content", None) is s.contenedor_mensajes:
            msg_container = c
            break
    assert msg_container is not None
    from theme import colores

    paleta = colores.get()
    assert str(getattr(msg_container, "bgcolor", "")).lower() == paleta.surface.lower()
    assert paleta.border.lstrip("#").lower() in str(msg_container.border).lower()
    assert msg_container.expand is True
    assert s.campo_mensaje.filled is True
    assert "24" in str(s.campo_mensaje.border_radius)
    assert "Preguntale" in s.campo_mensaje.hint_text
    assert s.campo_mensaje.expand is True
    assert "14" in str(msg_container.padding)

def test_no_doble_scroll_innecesario():
    for name, Cls in SCREENS.items():
        page = MockPage()
        s = Cls(page)
        built = s.build()
        columns = collect_controls(built, ft.Column)
        scroll_columns = [c for c in columns if getattr(c, "scroll", None) == ft.ScrollMode.AUTO]
        assert len(scroll_columns) <= 4, f"{name} tiene demasiados Column scroll AUTO ({len(scroll_columns)}), posible doble scroll overflow"

def test_proveedores_dimensionamiento_si_existe():
    try:
        from screens.proveedores import PantallaProveedores
    except ImportError:
        return
    page = MockPage()
    s = PantallaProveedores(page)
    built = s.build()
    assert hasattr(s, "tabla_datos")
    rows = collect_controls(built, ft.Row)
    assert any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows)
    assert isinstance(built, ft.Column)
    assert built.expand is True
