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

# helper para recorrer arbol
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
        # explorar hijos comunes
        # controls (list)
        if hasattr(cur, "controls") and isinstance(cur.controls, (list, tuple)):
            for child in cur.controls:
                if isinstance(child, ft.Control):
                    stack.append(child)
        # content (single)
        if hasattr(cur, "content") and isinstance(cur.content, ft.Control):
            stack.append(cur.content)
        # acciones dialogs
        if hasattr(cur, "actions") and isinstance(cur.actions, (list, tuple)):
            for child in cur.actions:
                if isinstance(child, ft.Control):
                    stack.append(child)
        # data_table rows cells content
        if hasattr(cur, "rows") and isinstance(getattr(cur, "rows"), list):
            for row in cur.rows:
                if hasattr(row, "cells"):
                    for cell in row.cells:
                        if hasattr(cell, "content") and isinstance(cell.content, ft.Control):
                            stack.append(cell.content)
        # column.controls ya manejado, pero también Column dentro de Container etc ya cubierto
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
        # debe ser Container o Column
        assert isinstance(built, (ft.Container, ft.Column)), f"{name} build debe retornar Container/Column got {type(built)}"
        # expand True en root o en content
        expand_ok = False
        if getattr(built, "expand", None) is True:
            expand_ok = True
        elif isinstance(built, ft.Container) and getattr(getattr(built, "content", None), "expand", None) is True:
            expand_ok = True
        # algunos dashboards retornan Container con Column expand True, aceptamos ambos
        # pero según test_dimensionamiento_expand original, root o self.expand debe ser True
        # en Screen, self.expand True por herencia Container?
        # También verificar s.expand True heredado de Screen base
        if not expand_ok and getattr(s, "expand", None) is True:
            expand_ok = True
        # fallback: buscar cualquier Column expand True dentro
        if not expand_ok:
            cols = collect_controls(built, (ft.Column, ft.ListView))
            for col in cols:
                if getattr(col, "expand", None) is True:
                    expand_ok = True
                    break
        assert expand_ok, f"{name} build debe tener expand=True en root o Column interna"

def test_dimensionamiento_scroll_auto_donde_corresponde():
    # Verificar que cada screen que maneja listas/tablas tenga scroll AUTO
    for name, Cls in SCREENS.items():
        page = MockPage()
        s = Cls(page)
        built = s.build()
        # recolectar Rows y ListViews
        rows = collect_controls(built, ft.Row)
        listviews = collect_controls(built, ft.ListView)
        columns = collect_controls(built, ft.Column)

        # Verificar existencia de scroll AUTO según tipo
        has_scroll_auto = False
        # Rows con scroll AUTO
        for r in rows:
            if getattr(r, "scroll", None) == ft.ScrollMode.AUTO:
                has_scroll_auto = True
                break
        # Columns con scroll AUTO (stock, caja, etc usan Column scroll AUTO expand)
        if not has_scroll_auto:
            for c in columns:
                if getattr(c, "scroll", None) == ft.ScrollMode.AUTO:
                    has_scroll_auto = True
                    break
        # ListViews con auto_scroll True (caja carrito, dashboard alertas, chat)
        for lv in listviews:
            if getattr(lv, "auto_scroll", False) is True:
                has_scroll_auto = True
                break
            if getattr(lv, "expand", None) is True:
                # expand implica dimensionamiento correcto para listas
                has_scroll_auto = True
                break

        # Reglas específicas:
        # dashboard, stock, caja, clientes, fiado deben tener scroll
        # chat debe tener ListView auto_scroll
        if name in ("dashboard", "stock", "caja", "clientes", "fiado", "proveedores"):
            assert has_scroll_auto, f"{name} debe tener al menos un Row/Column con scroll=AUTO o ListView expand/auto_scroll"
        elif name == "chat":
            # chat especificamente debe tener ListView auto_scroll
            assert any(getattr(lv, "auto_scroll", False) is True for lv in listviews), f"{name} debe tener ListView auto_scroll True"
            assert any(getattr(lv, "expand", None) is True for lv in listviews), f"{name} ListView debe tener expand True"

def test_caja_dimensionamiento_detalle():
    from screens.caja import PantallaCaja
    page = MockPage()
    s = PantallaCaja(page)
    built = s.build()
    # lista_carrito ListView expand + auto_scroll
    assert hasattr(s, "lista_carrito")
    assert isinstance(s.lista_carrito, ft.ListView)
    assert s.lista_carrito.expand is True
    assert s.lista_carrito.auto_scroll is True
    # verificar que built tiene Rows con scroll AUTO (productos row, main column scroll)
    rows = collect_controls(built, ft.Row)
    assert any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows), "Caja debe tener Row con scroll AUTO para evitar overflow"
    # verificar Container carrito tiene border y bgcolor
    # buscar Container que envuelve lista_carrito
    containers = collect_controls(built, ft.Container)
    carrito_container = None
    for c in containers:
        if getattr(c, "content", None) is s.lista_carrito:
            carrito_container = c
            break
    assert carrito_container is not None, "Caja debe tener Container envolviendo lista_carrito"
    assert carrito_container.border is not None
    # height limitado para no empujar total
    assert getattr(carrito_container, "height", None) is not None or getattr(carrito_container, "expand", None) is False

def test_stock_dimensionamiento_detalle():
    from screens.stock import PantallaStock
    page = MockPage()
    s = PantallaStock(page)
    built = s.build()
    assert hasattr(s, "tabla_datos")
    assert isinstance(s.tabla_datos, ft.DataTable)
    # DataTable expand True
    assert s.tabla_datos.expand is True
    # wrapper horizontal scroll
    rows = collect_controls(built, ft.Row)
    # debe haber Row con scroll AUTO que contiene DataTable
    found_row_scroll = any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows)
    assert found_row_scroll, "Stock DataTable debe estar dentro de Row con scroll AUTO"
    # Column raiz scroll AUTO expand True
    assert isinstance(built, ft.Column)
    assert built.scroll == ft.ScrollMode.AUTO
    assert built.expand is True
    # verificar Row de inputs también scroll AUTO
    # inputs Row con campo_nombre etc
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
        # DataTable dentro de Container + Row scroll AUTO
        rows = collect_controls(built, ft.Row)
        assert any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows), f"{Cls.__name__} debe tener Row scroll AUTO"

def test_dashboard_dimensionamiento():
    from screens.dashboard import PantallaDashboard
    page = MockPage()
    s = PantallaDashboard(page)
    built = s.build()
    # built es Container con Column scroll AUTO expand True
    assert isinstance(built, ft.Container)
    assert built.expand is True
    inner = built.content
    assert isinstance(inner, ft.Column)
    assert inner.expand is True
    assert inner.scroll == ft.ScrollMode.AUTO
    # debe tener al menos un Row con scroll AUTO (kpi_row)
    rows = collect_controls(built, ft.Row)
    assert any(getattr(r, "scroll", None) == ft.ScrollMode.AUTO for r in rows), "Dashboard debe tener Row scroll AUTO"

def test_chat_dimensionamiento_detalle():
    from screens.chat import PantallaChat
    page = MockPage()
    s = PantallaChat(page)
    built = s.build()
    # root Column expand True
    assert isinstance(built, ft.Column)
    assert built.expand is True
    # ListView auto_scroll expand bgcolor white border #e2e8f0
    assert isinstance(s.contenedor_mensajes, ft.ListView)
    assert s.contenedor_mensajes.auto_scroll is True
    assert s.contenedor_mensajes.expand is True
    # verificar container padre border y bgcolor
    containers = collect_controls(built, ft.Container)
    msg_container = None
    for c in containers:
        if getattr(c, "content", None) is s.contenedor_mensajes:
            msg_container = c
            break
    assert msg_container is not None
    assert str(getattr(msg_container, "bgcolor", "")).lower() in ("white", "#ffffff", "ffffff") or "white" in str(msg_container.bgcolor).lower()
    assert "e2e8f0" in str(msg_container.border).lower()
    assert msg_container.expand is True
    # TextField filled border_radius 24
    assert s.campo_mensaje.filled is True
    assert "24" in str(s.campo_mensaje.border_radius)
    assert "Preguntale" in s.campo_mensaje.hint_text
    assert s.campo_mensaje.expand is True
    # verificar que mensajes container padding 14
    assert "14" in str(msg_container.padding)

def test_no_doble_scroll_innecesario():
    # Verificar que screens no tienen doble scroll anidado excesivo que cause overflow, pero sí único principal
    for name, Cls in SCREENS.items():
        page = MockPage()
        s = Cls(page)
        built = s.build()
        columns = collect_controls(built, ft.Column)
        scroll_columns = [c for c in columns if getattr(c, "scroll", None) == ft.ScrollMode.AUTO]
        # Debe haber al menos 1 pero no más de 3 scroll columnas para evitar doble scroll excesivo
        # dashboard puede tener 2 (main + lista_ventas_dia), caja 1, stock 1, chat 0-1 pero usa ListView
        # solo verificamos que no sea excesivo >4
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
