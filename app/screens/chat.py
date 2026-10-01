"""Chat del negocio: UI premium (main-only) + OpenRouter (newer) + local fallback."""

import asyncio
import os
import unicodedata
from datetime import date, datetime, timedelta

import flet as ft
from screen_base import Pantalla
from datos import (
    stats,
    productos,
    cuentas,
    clientes,
    ventas,
    cli_por_id,
    margen,
    ganancia_registrada,
)
from jev.context import construir_contexto
from jev.contract import JevIntent, Periodo
from jev.fake import clasificar as clasificar_consulta_local
from jev.openrouter import OpenRouterError, completar_chat, configuracion_actual
from theme import (
    ANCHO_BORDE,
    ALTO_DIVISOR,
    FS_13,
    FS_14,
    ICON_MD,
    SP_8,
    SP_10,
    colores,
)
from widgets import (
    leer_texto,
    moneda,
    sincronizar_texto,
)

RADIUS_BUBBLE = 16
RADIUS_CONTAINER = 16
RADIUS_INPUT = 24


def respuesta_local(texto: str) -> str:
    """Responde solo a intents simples; no es IA ni reemplaza un informe."""
    consulta = (texto or "").strip().lower()
    minus = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", consulta)
        if not unicodedata.combining(caracter)
    )
    decision = clasificar_consulta_local(texto)
    if decision.aclaracion:
        return decision.aclaracion

    if decision.intent == JevIntent.GANANCIA_REGISTRADA:
        es_historico = decision.periodo == Periodo.HISTORIAL
        if es_historico:
            periodo = ventas
            etiqueta = "todo el historial"
        else:
            mes = date.today().strftime("%Y-%m")
            periodo = [venta for venta in ventas if venta.get("fecha", "").startswith(mes)]
            etiqueta = "este mes"
        ganancia, sin_costo = ganancia_registrada(periodo)
        respuesta = f"Margen registrado de {etiqueta}: {moneda(ganancia)}."
        if sin_costo:
            respuesta += (
                f" Se excluyen {sin_costo} venta(s) sin costo histórico registrado."
            )
        return respuesta

    if decision.intent == JevIntent.FIADO:
        acumulado = {}
        for cuenta in cuentas:
            pendiente = cuenta["total"] - cuenta["pagado"]
            if pendiente > 0:
                cid = cuenta.get("cliente_id", "")
                acumulado[cid] = acumulado.get(cid, 0) + pendiente
        ordenadas = sorted(acumulado.items(), key=lambda fila: fila[1], reverse=True)
        if not ordenadas:
            return "Nadie te debe plata."
        if any(palabra in minus for palabra in ("quien", "quién", "mas", "más", "mayor")):
            cid, pendiente = ordenadas[0]
            cliente = cli_por_id(cid)
            nombre = cliente["nombre"] if cliente else "Cliente sin ficha"
            return f"Mayor saldo pendiente: {nombre}, {moneda(pendiente)}."
        return "\n".join(
            f"{(cli_por_id(cid) or {}).get('nombre', 'Cliente sin ficha')}: {moneda(pendiente)}"
            for cid, pendiente in ordenadas
        )

    if decision.intent == JevIntent.MARGEN_CATALOGO:
        invertido = any(palabra in minus for palabra in ("bajo", "peor", "menor", "mal"))
        ordenados = sorted(
            productos,
            key=lambda producto: margen(producto["costo"], producto["precio"]),
            reverse=not invertido,
        )
        lineas = [
            f"{p['nombre']}: {margen(p['costo'], p['precio'])}% (stock {p['stock']})"
            for p in ordenados[:5]
        ]
        intro = "Peores 5 por margen actual:" if invertido else "Top 5 por margen actual:"
        return intro + ("\n" + "\n".join(lineas) if lineas else "\nNo hay productos cargados.")

    if decision.intent == JevIntent.STOCK:
        lineas = [f"{p['nombre']}: {p['stock']}u" for p in productos if p["stock"] <= p["minimo"]]
        return "Stock bajo:\n" + "\n".join(lineas) if lineas else "Todo con stock suficiente."

    if decision.intent == JevIntent.RESUMEN:
        resumen = stats()
        return (
            f"Resumen — ventas de hoy: {moneda(resumen['hoy'])}; "
            f"ventas del mes: {moneda(resumen['mes'])}; "
            f"por cobrar: {moneda(resumen['deben'])}."
        )

    if decision.intent == JevIntent.VENTAS:
        if decision.periodo == Periodo.HOY:
            return f"Ventas de hoy: {moneda(stats()['hoy'])}."
        if decision.periodo == Periodo.MES:
            return f"Ventas del mes: {moneda(stats()['mes'])}."
        if decision.periodo == Periodo.ULTIMOS_7_DIAS:
            desde = date.today() - timedelta(days=6)
            total = sum(
                venta["total"]
                for venta in ventas
                if desde.isoformat() <= venta.get("fecha", "") <= date.today().isoformat()
            )
            return f"Ventas de los últimos 7 días (incluido hoy): {moneda(total)}."
        return "¿Qué periodo querés consultar: hoy, últimos 7 días o este mes?"

    if decision.intent == JevIntent.CLIENTES:
        nombres = [cliente["nombre"] for cliente in clientes]
        return (
            f"Tus clientes ({len(nombres)}): " + ", ".join(nombres)
            if nombres
            else "Todavía no cargaste clientes."
        )

    return "Proba: ¿cuánto vendí hoy? ¿qué margen actual tengo? ¿quién me debe?"


class PantallaChat(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Chat")
        self.mensajes = []
        self.enviando = False
        self.acepta_envio = False

    def build(self):
        paleta = colores.get()
        self._paleta = paleta
        self._usa_openrouter = bool(os.environ.get("OPENROUTER_API_KEY", "").strip())
        self.campo_mensaje = ft.TextField(
            hint_text="Preguntale a tu negocio...",
            expand=True,
            filled=True,
            border_radius=RADIUS_INPUT,
            on_submit=self.enviar_mensaje,
        )
        sincronizar_texto(self.campo_mensaje)

        self.contenedor_mensajes = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            padding=ft.Padding.all(8),
        )
        self._zona_chat = self.contenedor_mensajes
        self._agregar_fila("Preguntame sobre tu negocio. Ej: cuanto vendi hoy?, que margen tengo?")

        self.confirmacion_datos = ft.Checkbox(
            label=(
                "Autorizo enviar a OpenRouter mi pregunta, el resumen del negocio y hasta los últimos 8 mensajes "
                "del chat durante esta sesión."
            ),
            value=self.acepta_envio,
            visible=self._usa_openrouter,
            on_change=self._al_cambiar_autorizacion,
        )
        self.boton_borrar = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            tooltip="Borrar conversación",
            disabled=self.enviando,
            on_click=self.borrar_conversacion,
        )

        try:
            self.boton_enviar = ft.FilledButton(
                content=ft.Icon(ft.Icons.SEND_ROUNDED, color=paleta.on_primary, size=18),
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    bgcolor=paleta.primary,
                    color=paleta.on_primary,
                    padding=12,
                ),
                tooltip="Enviar consulta",
                on_click=self.enviar_mensaje,
                disabled=self._usa_openrouter and not self.acepta_envio,
            )
        except Exception:
            self.boton_enviar = ft.FilledButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SEND, color="white", size=18),
                        ft.Text("Enviar", color="white"),
                    ],
                    spacing=8,
                ),
                style=ft.ButtonStyle(bgcolor=paleta.primary, color=paleta.on_primary),
                on_click=self.enviar_mensaje,
                disabled=self._usa_openrouter and not self.acepta_envio,
            )

        avatar_ia_header = ft.Container(
            content=ft.Icon(ft.Icons.SMART_TOY, color=paleta.on_primary, size=18),
            width=36,
            height=36,
            bgcolor=paleta.primary,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
        )
        header = ft.Row(
            [
                avatar_ia_header,
                ft.Column(
                    [
                        ft.Text(
                            "Asistente", size=18, weight=ft.FontWeight.BOLD, color=paleta.text
                        ),
                        ft.Text(
                            "Consultas de solo lectura sobre esta demo",
                            size=12,
                            color=paleta.text_muted,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                    tight=True,
                ),
                self.boton_borrar,
                ft.Container(
                    content=ft.Text(
                        "OpenRouter" if self._usa_openrouter else "Local",
                        size=10,
                        weight=ft.FontWeight.BOLD,
                        color=paleta.on_accent_soft,
                    ),
                    bgcolor=paleta.accent_soft,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    border_radius=20,
                    border=ft.Border.all(1, paleta.border),
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        header_container = ft.Container(
            content=header,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            bgcolor=paleta.surface,
            border=ft.Border.all(1, paleta.border),
            border_radius=RADIUS_CONTAINER,
        )

        mensajes_container = ft.Container(
            content=self.contenedor_mensajes,
            expand=True,
            bgcolor=paleta.surface,
            border=ft.Border.all(1, paleta.border),
            border_radius=RADIUS_CONTAINER,
            padding=14,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        input_row = ft.Row(
            [self.campo_mensaje, self.boton_enviar],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        input_container = ft.Container(
            content=input_row,
            padding=ft.Padding.symmetric(horizontal=4, vertical=4),
            bgcolor="transparent",
        )

        return ft.Column(
            [
                header_container,
                ft.Text(
                    self._texto_configuracion(),
                    size=FS_13,
                    color=paleta.text_muted,
                ),
                ft.Text(
                    (
                        "Al aceptar, cada consulta y hasta 8 mensajes previos pueden acompañar un resumen con nombres "
                        "y saldos de clientes, productos/precios/stock y ventas agregadas. Se excluyen teléfonos, IDs "
                        "y el JSON completo. Podés retirar el permiso desmarcando la casilla; OpenRouter puede aplicar "
                        "cargos. El chat no modifica datos y podés borrar la conversación cuando quieras."
                        if self._usa_openrouter
                        else "Modo local: la consulta se procesa dentro de GesKio y no se envía por internet. "
                        "Usa respuestas sencillas, no una IA generativa; no modifica datos y podés borrar la conversación "
                        "cuando quieras."
                    ),
                    size=FS_13,
                    color=paleta.text_muted,
                ),
                self.confirmacion_datos,
                mensajes_container,
                input_container,
            ],
            spacing=SP_10,
            expand=True,
        )

    @staticmethod
    def _texto_configuracion() -> str:
        return configuracion_actual().etiqueta

    def _agregar_fila(self, texto, es_usuario=False):
        """Solo pinta la burbuja premium en el ListView (sin tocar el historial)."""
        try:
            paleta = getattr(self, "_paleta", colores.get())
            hora = datetime.now().strftime("%H:%M")
            inicial = "T" if es_usuario else "IA"
            avatar_bg = paleta.primary if es_usuario else paleta.text
            avatar_fg = paleta.on_primary if es_usuario else paleta.surface
            bubble_bg = paleta.accent_soft if es_usuario else paleta.surface
            bubble_text = paleta.on_accent_soft if es_usuario else paleta.text
            bubble_border = None
            if not es_usuario:
                bubble_border = ft.Border.all(1, paleta.border)

            avatar = ft.CircleAvatar(
                content=ft.Text(inicial, color=avatar_fg, weight=ft.FontWeight.BOLD, size=11),
                bgcolor=avatar_bg,
                radius=16,
            )
            bubble = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(texto, size=14, color=bubble_text, selectable=True),
                        ft.Text(hora, size=10, color=bubble_text),
                    ],
                    spacing=4,
                    tight=True,
                ),
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                border_radius=RADIUS_BUBBLE,
                bgcolor=bubble_bg,
                border=bubble_border,
            )
            if es_usuario:
                fila = ft.Row(
                    [bubble, avatar],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    spacing=8,
                )
            else:
                fila = ft.Row(
                    [avatar, bubble],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    spacing=8,
                )
            self.contenedor_mensajes.controls = list(self.contenedor_mensajes.controls) + [fila]
            try:
                self.contenedor_mensajes.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error agregar fila chat: {ex}")

    def borrar_conversacion(self, e=None):
        """Borra el historial efímero sin tocar los datos del negocio."""
        if self.enviando:
            return
        self.mensajes.clear()
        self.contenedor_mensajes.controls = []
        if hasattr(self, "campo_mensaje"):
            self.campo_mensaje.value = ""
            self.campo_mensaje.error_text = None
        self._agregar_fila(
            "Conversación borrada. Preguntame sobre ventas, stock o cuentas."
        )
        try:
            self.pagina.update()
            if hasattr(self, "campo_mensaje"):
                self.campo_mensaje.update()
        except Exception:
            pass

    def _pintar_chat(self):
        try:
            self.contenedor_mensajes.controls = []
            for texto, es_usuario in self.mensajes:
                self._agregar_fila(texto, es_usuario)
            if self.enviando:
                self._agregar_fila("El asistente está consultando tus datos…")
            try:
                self.contenedor_mensajes.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error pintar chat: {ex}")

    def agregar_mensaje(self, texto=None, es_usuario=False, text=None, is_user=None):
        try:
            if texto is None:
                texto = text if text is not None else ""
            if is_user is not None:
                es_usuario = bool(is_user)
            self.mensajes.append((texto, bool(es_usuario)))
            self._agregar_fila(texto, bool(es_usuario))
            try:
                self.pagina.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error agregar_mensaje: {ex}")

    def _al_cambiar_autorizacion(self, evento):
        valor = getattr(evento, "data", None)
        if isinstance(valor, str):
            valor = valor.strip().lower() in {"true", "1", "yes"}
        elif valor is None:
            valor = getattr(getattr(evento, "control", None), "value", False)
        self.acepta_envio = bool(valor)
        self.confirmacion_datos.value = self.acepta_envio
        self.boton_enviar.disabled = not self.acepta_envio or self.enviando
        try:
            self.confirmacion_datos.update()
            self.boton_enviar.update()
        except Exception:
            pass

    async def enviar_mensaje(self, e=None):
        if self.enviando:
            return
        texto = (leer_texto(self.campo_mensaje, e) or "").strip()
        if not texto:
            return
        if self._usa_openrouter and not self.acepta_envio:
            self.campo_mensaje.error_text = (
                "Confirmá el envío de datos a OpenRouter antes de enviar."
            )
            try:
                self.campo_mensaje.update()
            except Exception:
                pass
            return

        historial = [
            ("user" if usuario else "assistant", mensaje) for mensaje, usuario in self.mensajes[-8:]
        ]
        self.agregar_mensaje(texto, True)
        self.enviando = True
        self.campo_mensaje.error_text = None
        self.campo_mensaje.value = ""
        self.campo_mensaje.disabled = True
        self.boton_enviar.disabled = True
        self.boton_borrar.disabled = True
        try:
            self.campo_mensaje.update()
            self.boton_enviar.update()
            self.boton_borrar.update()
        except Exception:
            pass
        self._pintar_chat()

        try:
            if self._usa_openrouter:
                contexto = construir_contexto()
                respuesta = await asyncio.to_thread(completar_chat, contexto, historial, texto)
            else:
                respuesta = await asyncio.to_thread(respuesta_local, texto)
            self.agregar_mensaje(respuesta, False)
            self.mensajes = self.mensajes[-80:]
        except OpenRouterError:
            try:
                respuesta = respuesta_local(texto)
                self.agregar_mensaje(
                    "No se pudo contactar con OpenRouter; esta respuesta usa el modo local.\n\n"
                    + respuesta,
                    False,
                )
                self.mensajes = self.mensajes[-80:]
            except Exception:
                self.agregar_mensaje(
                    "Ocurrió un error inesperado al consultar el asistente.", False
                )
        except Exception:
            self.agregar_mensaje("Ocurrió un error inesperado al consultar el asistente.", False)
        finally:
            self.enviando = False
            self.campo_mensaje.disabled = False
            self.boton_enviar.disabled = not self.acepta_envio
            self.boton_borrar.disabled = False
            self._pintar_chat()
            try:
                self.campo_mensaje.update()
                self.boton_enviar.update()
                self.boton_borrar.update()
            except Exception:
                pass
