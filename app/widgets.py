"""Kit de widgets compartidos de GesKio. Todo lo visual sale de theme.py."""

from __future__ import annotations

from datetime import date as _date

import flet as ft

from theme import (
    ALTO_DIVISOR,
    ANCHO_BORDE,
    CALENDARIO_CELDA_GAP,
    CALENDARIO_GAP,
    CONTENIDO_PADDING,
    DURACION_AVISO_MS,
    FOCO_BORDE,
    FS_12,
    FS_13,
    FS_14,
    FS_16,
    FS_18,
    FS_20,
    FS_24,
    FS_28,
    FS_30,
    ICON_MD,
    ICON_SM,
    ICON_LG,
    R_LG,
    R_MD,
    R_PILL,
    R_SM,
    RUPTURA_ALTO,
    RUPTURA_ANCHO,
    RAIL_ANCHO,
    LATERAL_ANCHO,
    SUPERIOR_ALTO,
    SP_4,
    SP_8,
    SP_12,
    SP_16,
    SP_20,
    SP_24,
    VALOR_FOCAL_FS,
    VALOR_STAT_FS,
    colores,
    color_rol,
)


def sincronizar_texto(campo: ft.TextField) -> ft.TextField:
    # Flet 0.84 solo manda el texto al server si el campo tiene on_change
    def _sync(e):
        data = getattr(e, "data", None)
        if data is not None:
            campo.value = data

    def _blur(e):
        v = getattr(getattr(e, "control", None), "value", None)
        if v is not None:
            campo.value = v

    campo.on_change = _sync
    campo.on_blur = _blur
    return campo


def moneda(valor) -> str:
    # es-AR: puntos de miles, sin decimales, negativos "-$1.800"
    try:
        numero = int(round(float(valor)))
    except (TypeError, ValueError, OverflowError):
        return "$0"
    agrupado = f"{abs(numero):,}".replace(",", ".")
    return f"-${agrupado}" if numero < 0 else f"${agrupado}"


def sincronizar_combo(combo: ft.Dropdown) -> ft.Dropdown:
    # Flet 0.84: igual que el texto, el combo no refresca .value sin listener
    anterior = combo.on_select

    def _sync(e):
        data = getattr(e, "data", None)
        if data is not None and data != "":
            combo.value = data
        if callable(anterior):
            anterior(e)

    combo.on_select = _sync
    return combo


def leer_texto(campo, evento=None) -> str:
    # lee lo mas fresco: el dato del evento si trae, si no el del campo
    dato = getattr(evento, "data", None)
    if isinstance(dato, str) and dato:
        return dato
    try:
        return campo.value or ""
    except Exception:
        return ""


def tarjeta(
    contenido: ft.Control, padding: int = SP_20, radio: int = R_MD
) -> ft.Container:
    paleta = colores.get()
    return ft.Container(
        content=contenido,
        padding=padding,
        expand=True,
        bgcolor=paleta.surface,
        border=ft.Border.all(ANCHO_BORDE, paleta.border),
        border_radius=ft.BorderRadius.all(radio),
    )


def campo_texto(*args, **kwargs) -> ft.TextField:
    """Campo de texto GesKio con radios coherentes en todas las pantallas."""
    paleta = colores.get()
    kwargs.setdefault("border", ft.InputBorder.OUTLINE)
    kwargs.setdefault("border_radius", R_MD)
    kwargs.setdefault("border_color", paleta.border_strong)
    kwargs.setdefault("focused_border_color", paleta.primary)
    kwargs.setdefault("border_width", ANCHO_BORDE)
    kwargs.setdefault("focused_border_width", FOCO_BORDE)
    return ft.TextField(*args, **kwargs)


def selector(*args, **kwargs) -> ft.Dropdown:
    """Selector GesKio con los mismos radios que los campos de formulario."""
    paleta = colores.get()
    kwargs.setdefault("border", ft.InputBorder.OUTLINE)
    kwargs.setdefault("border_radius", R_MD)
    kwargs.setdefault("border_color", paleta.border_strong)
    kwargs.setdefault("focused_border_color", paleta.primary)
    kwargs.setdefault("border_width", ANCHO_BORDE)
    kwargs.setdefault("focused_border_width", FOCO_BORDE)
    return ft.Dropdown(*args, **kwargs)


def tarjeta_stat(
    etiqueta: str,
    valor: str,
    rol: str = "info",
    icono=None,
) -> ft.Container:
    # metrica compacta: etiqueta y valor primero, icono secundario
    paleta = colores.get()
    # valores neutros por defecto; solo estados financieros destacan por color
    return tarjeta(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(etiqueta, size=FS_13, color=paleta.text_muted),
                        ft.Icon(icono, color=paleta.text_muted, size=ICON_SM)
                        if icono
                        else ft.Container(width=0),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
        ft.Text(
            valor,
            size=VALOR_STAT_FS,
            weight=ft.FontWeight.W_600,
            color=(
                paleta.danger_text
                if rol in {"danger", "danger_text"}
                else paleta.success if rol == "success" else paleta.text
            ),
        ),
            ],
            spacing=SP_8,
        ),
        padding=SP_16,
        radio=R_SM,
    )


def fecha_actual_es(hoy=None) -> str:
    # fecha de la barra superior: 'jueves, 10 de septiembre'
    dias = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo",
    ]
    meses = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    d = hoy or _date.today()
    return f"{dias[d.weekday()]}, {d.day} de {meses[d.month - 1]}"


_BARRA_MAX_ALTO = 120
_BARRA_MIN_ALTO = 8
_BARRA_ANCHO = 28


def barras_ventas(serie, hoy_iso=None) -> ft.Control:
    # barras a mano porque ft.BarChart no existe en Flet 0.84
    paleta = colores.get()
    try:
        pico = max((t or 0) for _, t in (serie or []))
    except Exception:
        pico = 0
    columnas: list[ft.Control] = []
    for iso, total in serie or []:
        try:
            wd = _date.fromisoformat(str(iso)).weekday()
        except Exception:
            wd = 0
        letra = "LMXJVSD"[wd]
        es_hoy = str(iso) == str(hoy_iso)
        h = (
            _BARRA_MIN_ALTO
            if not pico
            else max(_BARRA_MIN_ALTO, round((total or 0) / pico * _BARRA_MAX_ALTO))
        )
        barra = ft.Container(
            width=_BARRA_ANCHO,
            height=h,
            bgcolor=paleta.primary if es_hoy else paleta.border_strong,
            border_radius=ft.BorderRadius.all(R_SM),
            tooltip=moneda(total or 0),
        )
        columnas.append(
            ft.Column(
                [
                    ft.Container(
                        content=barra,
                        height=_BARRA_MAX_ALTO,
                        alignment=ft.Alignment.BOTTOM_CENTER,
                    ),
                    ft.Text(
                        letra,
                        size=FS_12,
                        weight=ft.FontWeight.BOLD if es_hoy else None,
                        color=paleta.text if es_hoy else paleta.text_muted,
                    ),
                ],
                spacing=SP_4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    if not columnas:
        return ft.Text("Sin datos", size=FS_14, color=paleta.text_soft)
    return ft.Row(
        columnas,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=SP_8,
    )


def tarjeta_focal(
    etiqueta: str,
    valor: str,
    rol: str = "accent_text",
    icono=None,
) -> ft.Container:
    # metrica protagonista: valor grande con borde del acento
    paleta = colores.get()
    color = color_rol(paleta, rol)
    fila: list[ft.Control] = [
        ft.Text(etiqueta, size=FS_13, weight=ft.FontWeight.W_500, color=paleta.text_muted)
    ]
    if icono is not None:
        fila.append(ft.Icon(icono, color=paleta.text_muted, size=ICON_SM))
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(fila, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(
                    valor, size=VALOR_FOCAL_FS, weight=ft.FontWeight.BOLD, color=color
                ),
            ],
            spacing=SP_4,
        ),
        padding=SP_16,
        bgcolor=paleta.surface,
        border=ft.Border(
            left=ft.BorderSide(FOCO_BORDE, paleta.primary),
            top=ft.BorderSide(ANCHO_BORDE, paleta.border),
            right=ft.BorderSide(ANCHO_BORDE, paleta.border),
            bottom=ft.BorderSide(ANCHO_BORDE, paleta.border),
        ),
        border_radius=ft.BorderRadius.all(R_MD),
        width=float("inf"),
    )


def seccion(titulo: str, contenido: ft.Control) -> ft.Container:
    # tarjeta con titulo
    paleta = colores.get()
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    titulo, size=FS_16, weight=ft.FontWeight.W_600, color=paleta.text
                ),
                contenido,
            ],
            spacing=SP_12,
        ),
        padding=SP_16,
        bgcolor=paleta.surface,
        border=ft.Border.all(ANCHO_BORDE, paleta.border),
        border_radius=ft.BorderRadius.all(R_MD),
    )


def grilla_stats(focal: ft.Control, tarjetas: list[ft.Control]) -> ft.Column:
    # la focal arriba, el resto en fila responsive
    items = list(tarjetas)
    for item in items:
        try:
            item.col = {"xs": 12, "sm": 6, "md": 4}
        except Exception:
            pass
    grilla = ft.ResponsiveRow(items, spacing=SP_12, run_spacing=SP_12)
    return ft.Column([focal, grilla], spacing=SP_12)


class Calendario(ft.Container):
    # solo lectura sobre la serie de ventas (dia/semana/mes)

    VIEWS = ("day", "week", "month")

    def __init__(self, obtener_serie, hoy=None, vista="week", al_cambiar=None):
        super().__init__()
        self.obtener_serie = obtener_serie
        self.al_cambiar = al_cambiar
        self.hoy = hoy
        self.vista = vista if vista in self.VIEWS else "week"
        paleta = colores.get()
        self.selector = ft.SegmentedButton(
            segments=[
                ft.Segment(value="day", label=ft.Text("D\u00eda")),
                ft.Segment(value="week", label=ft.Text("Semana")),
                ft.Segment(value="month", label=ft.Text("Mes")),
            ],
            selected=[self.vista],
            on_change=self._al_cambiar,
        )
        self.cuerpo = ft.Container(content=self._serie_segura(self.vista))
        self.padding = SP_20
        self.bgcolor = paleta.surface
        self.border = ft.Border.all(ANCHO_BORDE, paleta.border)
        self.border_radius = ft.BorderRadius.all(R_MD)
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Ventas",
                            size=FS_18,
                            weight=ft.FontWeight.BOLD,
                            color=paleta.text,
                        ),
                        self.selector,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.cuerpo,
            ],
            spacing=SP_12,
        )

    def _serie_segura(self, vista: str) -> ft.Control:
        try:
            return self.obtener_serie(vista)
        except Exception:
            paleta = colores.get()
            return ft.Text("Sin datos", size=FS_14, color=paleta.text_soft)

    def _al_cambiar(self, e) -> None:
        try:
            elegido = (
                e.control.selected
                if e is not None and hasattr(e, "control")
                else self.selector.selected
            )
            nueva_vista = elegido[0] if elegido else self.vista
        except Exception:
            nueva_vista = self.vista
        if nueva_vista not in self.VIEWS:
            return
        self.vista = nueva_vista
        if callable(self.al_cambiar):
            self.al_cambiar(nueva_vista)
        try:
            self.selector.selected = [nueva_vista]
        except Exception:
            pass
        self.refrescar()

    def refrescar(self) -> None:
        self.cuerpo.content = self._serie_segura(self.vista)
        self.cuerpo.update()

    def _update_seguro(self) -> None:
        try:
            self.update()
        except Exception:
            pass


def encabezado(
    titulo: str,
    acciones=(),
    al_refrescar=None,
    descripcion: str | None = None,
) -> ft.Row:
    # encabezado de cada pantalla
    paleta = colores.get()
    bloque_titulo = ft.Column(
        [
            ft.Text(titulo, size=FS_24, weight=ft.FontWeight.W_600, color=paleta.text),
            *(
                [ft.Text(descripcion, size=FS_14, color=paleta.text_muted)]
                if descripcion
                else []
            ),
        ],
        spacing=SP_4,
        tight=True,
    )
    controles: list[ft.Control] = [bloque_titulo]
    if al_refrescar is not None:
        controles.append(
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                icon_color=paleta.text_soft,
                tooltip="Actualizar",
                on_click=al_refrescar,
            )
        )
    controles.extend(acciones)
    return ft.Row(
        controles,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=SP_12,
        wrap=True,
    )


FILAS_POR_PAGINA = 10
_TABLA_TITULO_ALTO = SP_24 + SP_12
_TABLA_FILA_MIN = SP_24 + SP_8
_TABLA_FILA_MAX = SP_24 + SP_12


def paginar(filas, pagina, por_pagina=FILAS_POR_PAGINA):
    # corta la lista ya filtrada; devuelve (recorte, actual, total)
    try:
        por_pag = max(1, int(por_pagina or FILAS_POR_PAGINA))
    except (TypeError, ValueError):
        por_pag = FILAS_POR_PAGINA
    total = max(1, -(-len(filas or []) // por_pag))
    try:
        actual = int(pagina or 1)
    except (TypeError, ValueError):
        actual = 1
    actual = max(1, min(actual, total))
    inicio = (actual - 1) * por_pag
    return (list((filas or [])[inicio : inicio + por_pag]), actual, total)


def barra_busqueda(al_buscar=None, chips=(), acciones=(), pista="Buscar...") -> ft.Row:
    # buscador + filtros + acciones; el filtro lo resuelve la pantalla
    paleta = colores.get()
    buscador = campo_texto(
        hint_text=pista,
        expand=True,
        prefix_icon=ft.Icons.SEARCH,
        hint_style=ft.TextStyle(size=FS_14, color=paleta.text_muted),
        text_style=ft.TextStyle(size=FS_14, color=paleta.text),
    )

    def _avisar(e):
        texto = ""
        try:
            if e is not None and getattr(e, "data", None) is not None:
                texto = e.data
            else:
                texto = buscador.value
        except Exception:
            texto = buscador.value or ""
        if callable(al_buscar):
            try:
                al_buscar(texto or "")
            except Exception:
                pass

    buscador.on_change = _avisar
    controles: list[ft.Control] = [buscador]
    controles.extend(list(chips or ()))
    controles.extend(list(acciones or ()))
    return ft.Row(
        controles,
        spacing=SP_8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def paginador(pagina, paginas, al_paginar=None) -> ft.Control:
    # prev/next con 'n de m'; si hay una sola pagina, no se dibuja
    paleta = colores.get()
    try:
        total = max(1, int(paginas or 1))
    except (TypeError, ValueError):
        total = 1
    try:
        actual = int(pagina or 1)
    except (TypeError, ValueError):
        actual = 1
    actual = max(1, min(actual, total))
    if total <= 1:
        return ft.Container(height=0, width=0)

    def _ir(nueva):
        try:
            acotada = max(1, min(int(nueva), total))
        except (TypeError, ValueError):
            acotada = actual
        if callable(al_paginar):
            try:
                al_paginar(acotada)
            except Exception:
                pass

    boton_ant = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        tooltip="Anterior",
        icon_color=paleta.text_soft,
        on_click=lambda _: _ir(actual - 1),
        disabled=(actual <= 1),
    )
    boton_sig = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        tooltip="Siguiente",
        icon_color=paleta.text_soft,
        on_click=lambda _: _ir(actual + 1),
        disabled=(actual >= total),
    )
    etiqueta = ft.Text(f"{actual} de {total}", size=FS_14, color=paleta.text)
    return ft.Row(
        [boton_ant, etiqueta, boton_sig],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=SP_8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def tabla(
    columnas: list[ft.DataColumn],
    filas: list[ft.DataRow],
    espaciado: int = SP_12,
    mensaje_vacio: str = "Sin datos",
    icono_vacio=ft.Icons.INBOX,
    por_pagina: int = FILAS_POR_PAGINA,
) -> ft.Control:
    # tabla densa con estado vacio; la paginacion la hace la pantalla
    paleta = colores.get()
    if not filas:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono_vacio, size=ICON_LG, color=paleta.text_muted),
                    ft.Text(mensaje_vacio, size=FS_14, color=paleta.text_soft),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=SP_8,
            ),
            padding=SP_20,
            alignment=ft.Alignment.CENTER,
        )
    return ft.DataTable(
        columns=columnas,
        rows=filas,
        column_spacing=espaciado,
        bgcolor=paleta.surface,
        border=ft.Border.all(ANCHO_BORDE, paleta.border),
        border_radius=ft.BorderRadius.all(R_MD),
        divider_thickness=ANCHO_BORDE,
        horizontal_margin=SP_12,
        heading_row_height=_TABLA_TITULO_ALTO,
        data_row_min_height=_TABLA_FILA_MIN,
        data_row_max_height=_TABLA_FILA_MAX,
        heading_row_color=paleta.surface,
        data_row_color=paleta.surface,
        horizontal_lines=ft.BorderSide(width=ANCHO_BORDE, color=paleta.border),
        heading_text_style=ft.TextStyle(
            size=FS_12, weight=ft.FontWeight.BOLD, color=paleta.text_soft
        ),
        data_text_style=ft.TextStyle(size=FS_14, color=paleta.text),
    )


def dialogo(
    titulo: str,
    contenido: ft.Control,
    acciones: list[ft.Control],
) -> ft.AlertDialog:
    paleta = colores.get()
    return ft.AlertDialog(
        modal=True,
        bgcolor=paleta.surface,
        shape=ft.RoundedRectangleBorder(radius=R_MD),
        title=ft.Text(titulo, size=FS_20, weight=ft.FontWeight.BOLD, color=paleta.text),
        content=contenido,
        actions=acciones,
        actions_alignment=ft.MainAxisAlignment.END,
    )


def confirmar_eliminar(
    pagina,
    al_confirmar,
    nombre="",
    titulo="Eliminar",
    mensaje=None,
) -> None:
    paleta = colores.get()
    texto = mensaje
    if texto is None:
        texto = (
            f'¿Eliminar "{nombre}"? Esta acción no se puede deshacer.'
            if nombre
            else "¿Eliminar este elemento? Esta acción no se puede deshacer."
        )

    estado: dict = {}

    def cerrar(_):
        estado["ventana"].open = False
        pagina.update()

    def confirmar(evento):
        cerrar(evento)
        al_confirmar(evento)

    acciones: list[ft.Control] = [
        ft.TextButton("Cancelar", on_click=cerrar),
        ft.FilledButton(
            "Eliminar",
            on_click=confirmar,
            style=ft.ButtonStyle(
                bgcolor=paleta.danger,
                color=paleta.on_primary,
                shape=ft.RoundedRectangleBorder(radius=R_SM),
                padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
            ),
        ),
    ]
    ventana = dialogo(
        titulo,
        ft.Text(texto, size=FS_14, color=paleta.text_soft),
        acciones=acciones,
    )
    estado["ventana"] = ventana
    pagina.overlay.append(ventana)
    ventana.open = True
    pagina.update()


def aviso(
    pagina: ft.Page, texto: str, rol: str = "info", texto_accion=None, al_accion=None
) -> None:
    # SnackBar con rol (success/danger/warning/info) y accion opcional
    paleta = colores.get()
    fondos = {
        "success": paleta.success,
        "danger": paleta.danger,
        "warning": paleta.warning,
    }
    if rol in fondos:
        fondo = fondos[rol]
        color_texto = paleta.on_primary if rol == "danger" else paleta.bg
    else:
        fondo = paleta.text
        color_texto = paleta.bg
    accion = None
    if texto_accion:
        accion = ft.SnackBarAction(str(texto_accion), text_color=color_texto)
    barra = ft.SnackBar(
        content=ft.Text(texto, size=FS_14, color=color_texto),
        bgcolor=fondo,
        duration=DURACION_AVISO_MS,
        open=True,
        action=accion,
        on_action=al_accion,
    )
    pagina.overlay.append(barra)
    pagina.update()


def burbuja_chat(texto: str, es_usuario: bool) -> ft.Row:
    paleta = colores.get()
    if es_usuario:
        burbuja = ft.Container(
            content=ft.Text(texto, size=FS_14, color=paleta.on_accent_soft),
            bgcolor=paleta.accent_soft,
            border_radius=ft.BorderRadius.all(R_LG),
            padding=SP_12,
        )
        alineacion = ft.MainAxisAlignment.END
    else:
        burbuja = ft.Container(
            content=ft.Text(texto, size=FS_14, color=paleta.text),
            bgcolor=paleta.surface,
            border=ft.Border.all(ANCHO_BORDE, paleta.border),
            border_radius=ft.BorderRadius.all(R_LG),
            padding=SP_12,
        )
        alineacion = ft.MainAxisAlignment.START
    return ft.Row([burbuja], alignment=alineacion)


def en_rail_para_tamano(ancho, alto) -> bool:
    # rail si ancho<=1024 o alto<=600 (a 1100x700 arranca expandido)
    try:
        a = float(ancho)
        l = float(alto)
    except (TypeError, ValueError):
        return True
    return a <= RUPTURA_ANCHO or l <= RUPTURA_ALTO


class MenuLateral(ft.Container):
    # barra lateral: 240px expandida, 64px rail de iconos colapsada

    def __init__(
        self, items_nav, clave_activa: str, al_navegar=None, colapsado: bool = False
    ):
        super().__init__()
        self.items_nav = list(items_nav)
        self.clave_activa = clave_activa
        self.al_navegar = al_navegar
        self.colapsado = colapsado
        self.botones: dict[str, ft.TextButton] = {}
        self._reconstruir()

    def _estilo_nav(self, clave: str) -> ft.ButtonStyle:
        paleta = colores.get()
        activa = clave == self.clave_activa
        tam_icono = 22 if self.colapsado else 20
        if activa:
            return ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: paleta.accent_soft,
                    ft.ControlState.DEFAULT: paleta.accent_soft,
                },
                color=paleta.on_accent_soft,
                icon_color=paleta.on_accent_soft,
                icon_size=tam_icono,
                shape=ft.RoundedRectangleBorder(radius=R_SM),
                padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
                text_style=ft.TextStyle(size=FS_14, weight=ft.FontWeight.W_600),
            )
        return ft.ButtonStyle(
            bgcolor={
                ft.ControlState.HOVERED: paleta.bg_soft,
                ft.ControlState.DEFAULT: "transparent",
            },
            color=paleta.text_muted,
            icon_color=paleta.text_muted,
            icon_size=tam_icono,
            shape=ft.RoundedRectangleBorder(radius=R_SM),
            padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
            text_style=ft.TextStyle(size=FS_14),
        )

    def _reconstruir(self) -> None:
        paleta = colores.get()
        self.width = RAIL_ANCHO if self.colapsado else LATERAL_ANCHO
        self.bgcolor = paleta.surface
        self.padding = ft.Padding.symmetric(horizontal=SP_8, vertical=SP_12)
        self.border = ft.Border(right=ft.BorderSide(ANCHO_BORDE, paleta.border))
        marca: ft.Control
        if self.colapsado:
            marca = ft.Container(
                content=ft.Text("G", size=FS_20, weight=ft.FontWeight.W_600, color=paleta.text),
                width=40,
                height=40,
                alignment=ft.Alignment.CENTER,
                tooltip="GesKio",
            )
        else:
            marca = ft.Container(
                content=ft.Text("GesKio", size=FS_20, weight=ft.FontWeight.W_600, color=paleta.text),
                padding=ft.Padding.only(left=SP_8, top=SP_8, bottom=SP_8),
            )
        self.botones = {}
        botones_nav: list[ft.Control] = []
        boton_ajustes = None
        for clave, icono, etiqueta in self.items_nav:
            boton = ft.TextButton(
                "" if self.colapsado else etiqueta,
                icon=icono,
                tooltip=etiqueta,
                style=self._estilo_nav(clave),
                on_click=lambda _, c=clave: self._al_navegar(c),
                height=44,
            )
            self.botones[clave] = boton
            if clave == "ajustes":
                boton_ajustes = boton
            else:
                botones_nav.append(boton)
        pie: list[ft.Control] = []
        if boton_ajustes is not None:
            if not self.colapsado:
                pie.append(ft.Divider(height=SP_12, color=paleta.border))
            pie.append(boton_ajustes)
        self.content = ft.Column(
            [
                marca,
                ft.Container(height=SP_12),
                ft.Column(
                    botones_nav,
                    spacing=SP_4,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                *pie,
            ],
            spacing=SP_4,
            expand=True,
        )

    def refrescar_marco(self) -> None:
        # reaplica la paleta viva a la barra
        self._reconstruir()
        self._update_seguro()

    def _al_navegar(self, clave: str) -> None:
        if callable(self.al_navegar):
            self.al_navegar(clave)

    def fijar_activa(self, clave: str) -> None:
        self.clave_activa = clave
        for c, boton in self.botones.items():
            try:
                boton.style = self._estilo_nav(c)
            except Exception:
                pass
        self._update_seguro()

    def fijar_colapso(self, colapsado: bool) -> None:
        if colapsado == self.colapsado:
            return
        self.colapsado = colapsado
        self._reconstruir()
        self._update_seguro()

    def _update_seguro(self) -> None:
        try:
            self.update()
        except Exception:
            pass


class BarraSuperior(ft.Container):
    # barra de contexto con navegación y fecha, sin acciones duplicadas

    def __init__(self, al_colapsar=None):
        super().__init__()
        self.titulo_activo = ft.Text("GesKio", size=FS_16, weight=ft.FontWeight.W_600)
        self.texto_fecha = ft.Text(fecha_actual_es(), size=FS_14)
        self.boton_menu = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="Contraer/expandir barra lateral",
            on_click=al_colapsar,
        )
        self.height = SUPERIOR_ALTO
        self.padding = ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8)
        self.content = ft.Row(
            [
                self.boton_menu,
                self.titulo_activo,
                ft.Container(expand=True),
                ft.Icon(ft.Icons.CALENDAR_TODAY, size=ICON_SM),
                self.texto_fecha,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SP_12,
        )
        self.refrescar()

    def fijar_titulo(self, titulo: str) -> None:
        self.titulo_activo.value = titulo
        try:
            self.titulo_activo.update()
        except Exception:
            pass

    def refrescar(self) -> None:
        paleta = colores.get()
        try:
            self.bgcolor = paleta.surface
            self.border = ft.Border(bottom=ft.BorderSide(ANCHO_BORDE, paleta.border))
            self.texto_fecha.color = paleta.text_muted
            self.titulo_activo.color = paleta.text
            try:
                self.texto_fecha.value = fecha_actual_es()
            except Exception:
                pass
            self.boton_menu.icon_color = paleta.text_soft
        except Exception:
            pass


class Marco(ft.Row):
    # casco: lateral | superior + pantallas. La hamburguesa siempre funciona

    def __init__(
        self,
        pagina,
        items_nav,
        pantallas,
        clave_activa: str = "dash",
    ):
        super().__init__(
            spacing=SP_4, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )
        self.pagina = pagina
        self.items_nav = list(items_nav)
        self.pantallas = dict(pantallas)
        self.clave_activa = clave_activa
        self.etiquetas = {clave: etiqueta for clave, _, etiqueta in self.items_nav}
        self.colapsado = self._colapso_inicial()
        self.lateral = MenuLateral(
            self.items_nav,
            self.clave_activa,
            al_navegar=self.navegar,
            colapsado=self.colapsado,
        )
        self.superior = BarraSuperior(al_colapsar=self.colapsar)
        self.area = ft.Container(
            expand=True,
            padding=CONTENIDO_PADDING,
            bgcolor=colores.get().bg_soft,
            border_radius=ft.BorderRadius.all(R_LG),
        )
        derecha = ft.Column(
            [self.superior, self.area],
            spacing=SP_4,
            expand=True,
        )
        self.controls = [self.lateral, derecha]
        self._conectar_resize()

    def _leer_tamano(self):
        try:
            return self.pagina.window.width, self.pagina.window.height
        except Exception:
            return None, None

    def _colapso_inicial(self) -> bool:
        ancho, alto = self._leer_tamano()
        if ancho is None or alto is None:
            return True
        return en_rail_para_tamano(ancho, alto)

    def _conectar_resize(self) -> None:
        try:
            self.pagina.window.on_event = self._al_evento_ventana
        except Exception:
            pass

    def _al_evento_ventana(self, evento) -> None:
        tipo = getattr(evento, "type", None)
        if tipo in (ft.WindowEventType.RESIZED, ft.WindowEventType.RESIZE):
            self._aplicar_ruptura()
            return
        try:
            nombre = str(getattr(tipo, "value", tipo) or "").lower()
        except Exception:
            nombre = ""
        if nombre in ("resized", "resize", "none", ""):
            self._aplicar_ruptura()

    def _aplicar_ruptura(self) -> None:
        ancho, alto = self._leer_tamano()
        if ancho is None or alto is None:
            return
        colapsado = en_rail_para_tamano(ancho, alto)
        if colapsado != self.colapsado:
            self.colapsado = colapsado
            try:
                self.lateral.fijar_colapso(colapsado)
            except Exception:
                pass
            self._update_seguro()

    def colapsar(self, _=None) -> None:
        self.colapsado = not self.colapsado
        try:
            self.lateral.fijar_colapso(self.colapsado)
        except Exception:
            pass
        self._update_seguro()

    def navegar(self, clave: str) -> None:
        if clave not in self.pantallas:
            return
        self.clave_activa = clave
        pantalla = self.pantallas[clave]
        try:
            pantalla.visible = True
        except Exception:
            pass
        self.area.content = pantalla
        try:
            pantalla.al_entrar()
        except Exception:
            pass
        try:
            self.lateral.fijar_activa(clave)
        except Exception:
            pass
        try:
            self.superior.fijar_titulo(self.etiquetas.get(clave, clave))
        except Exception:
            pass
        self._update_seguro()

    def refrescar_marco(self) -> None:
        # reaplica la paleta viva al casco
        try:
            self.superior.refrescar()
            self.area.bgcolor = colores.get().bg_soft
        except Exception:
            pass
        try:
            self.lateral.refrescar_marco()
        except Exception:
            pass
        self._update_seguro()

    def aplicar_y_rearmar(self) -> None:
        colores.apply_to_page(self.pagina)
        for pantalla in self.pantallas.values():
            try:
                pantalla.invalidate()
            except Exception:
                pass
        self.refrescar_marco()
        self.navegar(self.clave_activa)

    def _update_seguro(self) -> None:
        try:
            self.pagina.update()
        except Exception:
            pass


__all__ = [
    "tarjeta",
    "campo_texto",
    "selector",
    "tarjeta_stat",
    "tarjeta_focal",
    "seccion",
    "grilla_stats",
    "Calendario",
    "encabezado",
    "tabla",
    "barra_busqueda",
    "paginador",
    "paginar",
    "FILAS_POR_PAGINA",
    "dialogo",
    "confirmar_eliminar",
    "aviso",
    "sincronizar_texto",
    "sincronizar_combo",
    "leer_texto",
    "moneda",
    "burbuja_chat",
    "MenuLateral",
    "BarraSuperior",
    "Marco",
    "en_rail_para_tamano",
    "fecha_actual_es",
    "barras_ventas",
]
