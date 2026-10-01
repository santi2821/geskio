import asyncio
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

    def update(self):
        pass

    def add(self, c):
        self.controls.append(c)

    def open(self, control):
        control.open = True
        if control not in self.overlay:
            self.overlay.append(control)
        self._opened.append(control)

    def close(self, control):
        control.open = False
        self._closed.append(control)


def _get_chat():
    from screens.chat import PantallaChat

    page = MockPage()
    s = PantallaChat(page)
    built = s.build()
    return s, page, built


def test_chat_build_sin_crash():
    s, page, built = _get_chat()
    assert built is not None
    assert (
        getattr(built, "expand", None) is True
        or getattr(getattr(built, "content", None), "expand", None) is True
    )
    assert isinstance(built, (ft.Column, ft.Container))
    assert hasattr(s, "contenedor_mensajes")
    assert isinstance(s.contenedor_mensajes, ft.ListView)
    assert getattr(s.contenedor_mensajes, "auto_scroll", False) is True
    assert getattr(s.contenedor_mensajes, "expand", None) is True
    found_container = None
    if isinstance(built, ft.Column):
        for c in built.controls:
            if isinstance(c, ft.Container) and getattr(c, "content", None) is s.contenedor_mensajes:
                found_container = c
                break
            if isinstance(c, ft.Container) and c.content is s.contenedor_mensajes:
                found_container = c
                break
    else:
        inner = built.content
        if isinstance(inner, ft.Column):
            for c in inner.controls:
                if (
                    isinstance(c, ft.Container)
                    and getattr(c, "content", None) is s.contenedor_mensajes
                ):
                    found_container = c
                    break

    assert found_container is not None, "Container mensajes no encontrado"
    from theme import colores

    paleta = colores.get()
    bg = str(getattr(found_container, "bgcolor", "")).lower()
    assert paleta.surface.lower() in bg, f"bgcolor inesperado {bg}"
    border = getattr(found_container, "border", None)
    assert border is not None, "Border no seteado en container mensajes"
    border_str = str(border).lower()
    assert paleta.border.lstrip("#").lower() in border_str, (
        f"border no contiene {paleta.border}: {border_str}"
    )

    header_found = False
    if isinstance(built, ft.Column) and len(built.controls) >= 1:
        hdr = built.controls[0]
        if isinstance(hdr, ft.Container):
            content = hdr.content
            if isinstance(content, ft.Row):
                texts = []
                stack = [content]
                while stack:
                    cur = stack.pop()
                    if isinstance(cur, ft.Text) and cur.value:
                        texts.append(cur.value)
                    if hasattr(cur, "controls") and cur.controls:
                        stack.extend(list(cur.controls))
                    if hasattr(cur, "content") and isinstance(cur.content, ft.Control):
                        stack.append(cur.content)
                assert any("Asistente" in t for t in texts), f"Header sin título {texts}"
                assert any("demo" in t.lower() for t in texts), f"Header sin alcance claro {texts}"
                header_found = True
    assert header_found, "Header premium no encontrado"

    assert hasattr(s, "campo_mensaje")
    tf = s.campo_mensaje
    assert isinstance(tf, ft.TextField)
    assert getattr(tf, "filled", None) is True, "TextField filled debe ser True"
    br = getattr(tf, "border_radius", None)
    br_str = str(br)
    assert "24" in br_str, f"border_radius no es 24: {br}"
    hint = getattr(tf, "hint_text", "")
    assert "Preguntale" in hint, f"hint_text debe contener 'Preguntale...' got {hint}"
    assert getattr(tf, "expand", None) is True, "TextField expand debe ser True"

    found_button = False
    if isinstance(built, ft.Column):
        last = built.controls[-1]
        row = None
        if isinstance(last, ft.Container) and isinstance(last.content, ft.Row):
            row = last.content
        elif isinstance(last, ft.Row):
            row = last
        if row:
            for c in row.controls:
                if isinstance(c, (ft.FilledButton, ft.ElevatedButton, ft.IconButton)):
                    found_button = True
                    break
                if hasattr(c, "content") and isinstance(getattr(c, "content"), ft.Icon):
                    found_button = True
                    break
    assert found_button, "FilledButton circular send no encontrado en input row"


def test_chat_burbujas_premium():
    s, page, built = _get_chat()
    s.contenedor_mensajes.controls = []
    s.agregar_mensaje("Hola IA", is_user=False)
    s.agregar_mensaje("Hola usuario", is_user=True)
    assert len(s.contenedor_mensajes.controls) == 2
    for fila in s.contenedor_mensajes.controls:
        assert isinstance(fila, ft.Row)
        has_avatar = False
        has_bubble = False
        has_timestamp = False
        for inner in fila.controls:
            if isinstance(inner, ft.CircleAvatar):
                has_avatar = True
                assert getattr(inner, "radius", 0) == 16, (
                    f"CircleAvatar radius debe ser 16 got {inner.radius}"
                )
                txt = getattr(inner, "content", None)
                assert isinstance(txt, ft.Text)
                assert len(txt.value) <= 2 and len(txt.value) >= 1
            if isinstance(inner, ft.Container):
                has_bubble = True
                pad = getattr(inner, "padding", None)
                pad_str = str(pad).lower()
                assert "14" in pad_str and "10" in pad_str, f"padding debe ser 14/10 got {pad_str}"
                br = getattr(inner, "border_radius", None)
                assert "16" in str(br), f"border_radius debe ser 16 got {br}"
                content = inner.content
                if isinstance(content, ft.Column):
                    for t in content.controls:
                        if (
                            isinstance(t, ft.Text)
                            and ":" in (t.value or "")
                            and len((t.value or "").strip()) <= 5
                        ):
                            has_timestamp = True
                        if isinstance(t, ft.Text) and t.value and ":" in t.value:
                            has_timestamp = True
                bg = str(getattr(inner, "bgcolor", "")).lower()
                from theme import colores

                paleta = colores.get()
                assert any(c.lower() in bg for c in [paleta.accent_soft, paleta.surface]), (
                    f"bg inesperado {bg}"
                )
        assert has_avatar, "Burbuja debe tener CircleAvatar"
        assert has_bubble, "Burbuja debe tener Container"
        assert has_timestamp, "Burbuja debe tener timestamp"

    filas = s.contenedor_mensajes.controls
    assert filas[0].alignment == ft.MainAxisAlignment.START, "IA debe ser START"
    assert filas[1].alignment == ft.MainAxisAlignment.END, "Usuario debe ser END"


def test_chat_enviar_mensaje_venta_margen_stock_clientes():
    from datos import productos, clientes

    s, page, built = _get_chat()
    def enviar_y_verificar(query, expected_substrings):
        initial_len = len(s.mensajes)
        s.campo_mensaje.value = query
        asyncio.run(s.enviar_mensaje())
        assert len(s.mensajes) == initial_len + 2, (
            f"Query '{query}' no agrego 2 mensajes"
        )
        assert len(s.contenedor_mensajes.controls) == len(s.mensajes)
        last_row = s.contenedor_mensajes.controls[-1]
        bubble = None
        for c in last_row.controls:
            if isinstance(c, ft.Container):
                bubble = c
                break
        assert bubble is not None
        col = bubble.content
        assert isinstance(col, ft.Column)
        texto_bot = col.controls[0].value if col.controls else ""
        lower = texto_bot.lower()
        assert any(sub.lower() in lower for sub in expected_substrings), (
            f"Respuesta '{texto_bot}' no contiene {expected_substrings} para query '{query}'"
        )
        assert s.campo_mensaje.value == "", "campo debe limpiarse"

    enviar_y_verificar("cuanto vendi hoy?", ["Ventas de hoy", "$"])
    enviar_y_verificar("resumen de ventas", ["Hoy", "Mes"])
    enviar_y_verificar("que margen tengo?", ["%", "margen"])
    enviar_y_verificar("ganancia", ["%"])
    enviar_y_verificar("stock bajo", ["Stock", "Todo con stock"])
    enviar_y_verificar("como esta mi stock?", ["Stock", "Todo"])
    enviar_y_verificar("lista de clientes", [c["nombre"].split()[0] for c in clientes[:1]])
    enviar_y_verificar("quien me debe?", ["$", "Nadie", "debe"])
    enviar_y_verificar("fiado", ["$", "Nadie"])
    enviar_y_verificar("blabla desconocido", ["Proba", "cuanto vendi"])
    before = len(s.mensajes)
    s.campo_mensaje.value = "   "
    asyncio.run(s.enviar_mensaje())
    assert len(s.mensajes) == before, "Mensaje vacio no debe agregar nada"
    s.campo_mensaje.value = ""
    asyncio.run(s.enviar_mensaje())
    assert len(s.mensajes) == before


def test_chat_local_no_exige_consentimiento_ni_contacta_provider(monkeypatch):
    from copy import deepcopy
    from datos import ventas
    from screens import chat as chat_module

    def no_debe_llamarse(*args, **kwargs):
        raise AssertionError("El modo local no debe construir ni enviar contexto remoto")

    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setattr(chat_module, "construir_contexto", no_debe_llamarse)
    monkeypatch.setattr(chat_module, "completar_chat", no_debe_llamarse)
    ventas_antes = deepcopy(ventas)
    s, _, _ = _get_chat()

    assert s.confirmacion_datos.visible is False
    assert s.boton_enviar.disabled is False
    assert s.acepta_envio is False
    s.campo_mensaje.value = "¿Cuánto vendí hoy?"
    asyncio.run(s.enviar_mensaje())

    assert len(s.mensajes) == 2
    assert "Ventas de hoy" in s.mensajes[-1][0]
    s.campo_mensaje.value = "borrador"
    s.borrar_conversacion()
    assert s.mensajes == []
    assert s.campo_mensaje.value == ""
    assert len(s.contenedor_mensajes.controls) == 1
    assert ventas == ventas_antes


def test_chat_openrouter_no_accede_a_datos_sin_permiso(monkeypatch):
    from screens import chat as chat_module

    def no_debe_llamarse(*args, **kwargs):
        raise AssertionError("No se debe preparar o enviar el contexto antes del consentimiento")

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-only-placeholder")
    monkeypatch.setattr(chat_module, "construir_contexto", no_debe_llamarse)
    monkeypatch.setattr(chat_module, "completar_chat", no_debe_llamarse)
    s, _, _ = _get_chat()

    assert s.confirmacion_datos.visible is True
    assert s.boton_enviar.disabled is True
    s.campo_mensaje.value = "¿Cuánto vendí hoy?"
    asyncio.run(s.enviar_mensaje())

    assert s.mensajes == []
    assert "Confirmá" in s.campo_mensaje.error_text


def test_chat_mostrar_alerta_heredado_no_overlay():
    s, page, built = _get_chat()
    s.mostrar_alerta("test alerta")
    assert page.snack_bar is not None, "snack_bar debe estar seteado"
    assert getattr(page.snack_bar, "open", False) is True
    assert (
        page.snack_bar.content.value == "test alerta"
        if hasattr(page.snack_bar.content, "value")
        else True
    )


def test_chat_no_usa_overlay():
    import pathlib

    p = pathlib.Path("app/screens/chat.py")
    content = p.read_text()
    assert "overlay.append" not in content, "chat.py no debe usar overlay.append"
    assert "AlertDialog" not in content or "page.open" in content or "mostrar_alerta" in content, (
        "Si usa AlertDialog debe usar page.open"
    )
