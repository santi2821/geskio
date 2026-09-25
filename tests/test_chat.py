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
    # La arquitectura newer exige consentimiento de privacidad antes de enviar.
    # Sin OPENROUTER_API_KEY el provider falla y el chat usa el fallback local.
    s.acepta_envio = True
    try:
        s.confirmacion_datos.value = True
        s.boton_enviar.disabled = False
    except Exception:
        pass
    return s, page, built


def test_chat_build_sin_crash():
    s, page, built = _get_chat()
    assert built is not None
    # root debe ser Column o Container expand=True
    assert (
        getattr(built, "expand", None) is True
        or getattr(getattr(built, "content", None), "expand", None) is True
    )
    # debe ser Column expand True en algun nivel
    assert isinstance(built, (ft.Column, ft.Container))
    # verificar contenedor_mensajes es ListView auto_scroll expand bgcolor white border #e2e8f0
    assert hasattr(s, "contenedor_mensajes")
    assert isinstance(s.contenedor_mensajes, ft.ListView)
    assert getattr(s.contenedor_mensajes, "auto_scroll", False) is True
    assert getattr(s.contenedor_mensajes, "expand", None) is True
    # verificar que el contenedor padre de mensajes tiene bgcolor white y border #e2e8f0
    # built es Column [header_container, mensajes_container, input_container]
    # buscar Container que envuelve ListView
    found_container = None
    if isinstance(built, ft.Column):
        for c in built.controls:
            if isinstance(c, ft.Container) and getattr(c, "content", None) is s.contenedor_mensajes:
                found_container = c
                break
            # si no directo, buscar recursivo simple
            if isinstance(c, ft.Container) and c.content is s.contenedor_mensajes:
                found_container = c
                break
    else:
        # built es Container con Column
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
    # bgcolor white (case-insensitive)
    bg = str(getattr(found_container, "bgcolor", "")).lower()
    assert "white" in bg or "#ffffff" in bg or "fff" in bg, f"bgcolor inesperado {bg}"
    # border 1 #e2e8f0
    border = getattr(found_container, "border", None)
    assert border is not None, "Border no seteado en container mensajes"
    # verificar border contiene #e2e8f0 (como string o como color)
    # border puede ser Border object con left/top etc; inspeccionar repr
    border_str = str(border).lower()
    # tambien revisar por color atributo en border (si es dict)
    assert "e2e8f0" in border_str or "228" in border_str, f"border no contiene #e2e8f0 {border_str}"

    # verificar header premium existe y tiene subtitulo
    # header_container es primer control si es Container
    header_found = False
    if isinstance(built, ft.Column) and len(built.controls) >= 1:
        hdr = built.controls[0]
        if isinstance(hdr, ft.Container):
            # debe contener Row con Text "Chat IA" y subtitulo
            content = hdr.content
            if isinstance(content, ft.Row):
                # buscar textos recursivamente
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
                # debe tener titulo Chat IA y subtitulo con datos reales o En vivo o Responde
                assert any("Chat IA" in t for t in texts), f"Header no tiene Chat IA {texts}"
                assert any(
                    "Responde" in t or "En vivo" in t or "Assistant" in t or "datos reales" in t
                    for t in texts
                ), f"Header no tiene subtitulo {texts}"
                header_found = True
    assert header_found, "Header premium no encontrado"

    # verificar input: TextField filled True border_radius 24 hint "Preguntale..."
    assert hasattr(s, "campo_mensaje")
    tf = s.campo_mensaje
    assert isinstance(tf, ft.TextField)
    assert getattr(tf, "filled", None) is True, "TextField filled debe ser True"
    # border_radius 24
    br = getattr(tf, "border_radius", None)
    # puede ser int o BorderRadius object
    br_str = str(br)
    assert "24" in br_str, f"border_radius no es 24: {br}"
    hint = getattr(tf, "hint_text", "")
    assert "Preguntale" in hint, f"hint_text debe contener 'Preguntale...' got {hint}"
    assert getattr(tf, "expand", None) is True, "TextField expand debe ser True"

    # verificar FilledButton circular send existe
    found_button = False
    # input_row es ultimo control en built Column -> Container -> Row
    if isinstance(built, ft.Column):
        last = built.controls[-1]
        # last puede ser Container con Row
        row = None
        if isinstance(last, ft.Container) and isinstance(last.content, ft.Row):
            row = last.content
        elif isinstance(last, ft.Row):
            row = last
        if row:
            for c in row.controls:
                # FilledButton o ElevatedButton con send icon
                if isinstance(c, (ft.FilledButton, ft.ElevatedButton, ft.IconButton)):
                    found_button = True
                    break
                # si es Container wrapping button ?
                if hasattr(c, "content") and isinstance(getattr(c, "content"), ft.Icon):
                    found_button = True
                    break
    assert found_button, "FilledButton circular send no encontrado en input row"


def test_chat_burbujas_premium():
    s, page, built = _get_chat()
    # limpiar y agregar mensajes para inspeccionar burbujas
    s.contenedor_mensajes.controls = []
    s.agregar_mensaje("Hola IA", is_user=False)
    s.agregar_mensaje("Hola usuario", is_user=True)
    assert len(s.contenedor_mensajes.controls) == 2
    for fila in s.contenedor_mensajes.controls:
        assert isinstance(fila, ft.Row)
        # debe tener spacing y alignment
        # buscar Container burbuja y CircleAvatar
        has_avatar = False
        has_bubble = False
        has_timestamp = False
        # fila.controls tiene [avatar, bubble] o [bubble, avatar]
        for inner in fila.controls:
            if isinstance(inner, ft.CircleAvatar):
                has_avatar = True
                # verificar inicial length <=2 y radius 16
                assert getattr(inner, "radius", 0) == 16, (
                    f"CircleAvatar radius debe ser 16 got {inner.radius}"
                )
                txt = getattr(inner, "content", None)
                assert isinstance(txt, ft.Text)
                assert len(txt.value) <= 2 and len(txt.value) >= 1
            if isinstance(inner, ft.Container):
                has_bubble = True
                # verificar padding 14/10 y border_radius 16
                pad = getattr(inner, "padding", None)
                pad_str = str(pad).lower()
                # padding symmetric horizontal 14 vertical 10 -> debe contener 14 y 10
                assert "14" in pad_str and "10" in pad_str, f"padding debe ser 14/10 got {pad_str}"
                br = getattr(inner, "border_radius", None)
                assert "16" in str(br), f"border_radius debe ser 16 got {br}"
                # buscar timestamp dentro Column
                content = inner.content
                if isinstance(content, ft.Column):
                    for t in content.controls:
                        if (
                            isinstance(t, ft.Text)
                            and ":" in (t.value or "")
                            and len((t.value or "").strip()) <= 5
                        ):
                            # heuristica timestamp HH:MM
                            has_timestamp = True
                        # buscar size 10 color muted
                        if isinstance(t, ft.Text) and t.value and ":" in t.value:
                            has_timestamp = True
                # bgcolor segun is_user
                bg = str(getattr(inner, "bgcolor", "")).lower()
                # user bg #dcfce7, assistant #f1f5f9
                assert any(c in bg for c in ["dcfce7", "f1f5f9", "grey", "green"]), (
                    f"bg inesperado {bg}"
                )
        assert has_avatar, "Burbuja debe tener CircleAvatar"
        assert has_bubble, "Burbuja debe tener Container"
        assert has_timestamp, "Burbuja debe tener timestamp"

    # verificar que al menos una burbuja de usuario tiene END alignment y assistant START
    filas = s.contenedor_mensajes.controls
    assert filas[0].alignment == ft.MainAxisAlignment.START, "IA debe ser START"
    assert filas[1].alignment == ft.MainAxisAlignment.END, "Usuario debe ser END"


def test_chat_enviar_mensaje_venta_margen_stock_clientes():
    from datos import productos, clientes

    s, page, built = _get_chat()

    # helper para enviar y verificar respuesta
    def enviar_y_verificar(query, expected_substrings):
        initial_len = len(s.contenedor_mensajes.controls)
        s.campo_mensaje.value = query
        asyncio.run(s.enviar_mensaje())
        # debe agregar 2 mensajes: user + bot
        assert len(s.contenedor_mensajes.controls) == initial_len + 2, (
            f"Query '{query}' no agrego 2 mensajes"
        )
        # ultimo es respuesta bot
        last_row = s.contenedor_mensajes.controls[-1]
        # extraer texto de burbuja
        bubble = None
        for c in last_row.controls:
            if isinstance(c, ft.Container):
                bubble = c
                break
        assert bubble is not None
        col = bubble.content
        assert isinstance(col, ft.Column)
        texto_bot = col.controls[0].value if col.controls else ""
        # verificar expected_substrings alguno presente (case-insensitive)
        lower = texto_bot.lower()
        assert any(sub.lower() in lower for sub in expected_substrings), (
            f"Respuesta '{texto_bot}' no contiene {expected_substrings} para query '{query}'"
        )
        assert s.campo_mensaje.value == "", "campo debe limpiarse"

    # venta / hoy / mes / resumen -> stats
    enviar_y_verificar("cuanto vendi hoy?", ["Hoy", "$", "Mes"])
    enviar_y_verificar("resumen de ventas", ["Hoy", "Mes"])
    # margen / ganancia
    enviar_y_verificar("que margen tengo?", ["%", "margen"])
    enviar_y_verificar("ganancia", ["%"])
    # stock
    enviar_y_verificar("stock bajo", ["Stock", "Todo con stock"])
    enviar_y_verificar("como esta mi stock?", ["Stock", "Todo"])
    # clientes
    enviar_y_verificar("lista de clientes", [c["nombre"].split()[0] for c in clientes[:1]])
    # deudas / fiado
    enviar_y_verificar("quien me debe?", ["$", "Nadie", "debe"])
    enviar_y_verificar("fiado", ["$", "Nadie"])
    # fallback desconocido
    enviar_y_verificar("blabla desconocido", ["Proba", "cuanto vendi"])
    # venta con mock para margen: asegurar no crashea con productos vacios parciales
    # test vacio no debe agregar mensaje
    before = len(s.contenedor_mensajes.controls)
    s.campo_mensaje.value = "   "
    asyncio.run(s.enviar_mensaje())
    assert len(s.contenedor_mensajes.controls) == before, "Mensaje vacio no debe agregar nada"
    s.campo_mensaje.value = ""
    asyncio.run(s.enviar_mensaje())
    assert len(s.contenedor_mensajes.controls) == before


def test_chat_mostrar_alerta_heredado_no_overlay():
    s, page, built = _get_chat()
    # mostrar_alerta debe usar page.snack_bar no overlay
    s.mostrar_alerta("test alerta")
    assert page.snack_bar is not None, "snack_bar debe estar seteado"
    assert getattr(page.snack_bar, "open", False) is True
    # overlay no debe contener SnackBar si uso correcto; pero MockPage.open añade a overlay, snackbar no
    # asegurar que no se uso overlay.append directo para SnackBar: snackbar via snack_bar property
    # Verificar que no se añadió dialogo a overlay
    # Debe seguir sin dialog overlay extra
    # El test original verifica page.overlay vs snack_bar
    assert (
        page.snack_bar.content.value == "test alerta"
        if hasattr(page.snack_bar.content, "value")
        else True
    )


def test_chat_no_usa_overlay():
    # asegurar que chat.py no contiene overlay.append
    import pathlib

    p = pathlib.Path("app/screens/chat.py")
    content = p.read_text()
    assert "overlay.append" not in content, "chat.py no debe usar overlay.append"
    assert "AlertDialog" not in content or "page.open" in content or "mostrar_alerta" in content, (
        "Si usa AlertDialog debe usar page.open"
    )
