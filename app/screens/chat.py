"""Chat del negocio: UI premium (main-only) + OpenRouter (newer) + local fallback."""

import asyncio
import os
from datetime import date, datetime, timedelta

import flet as ft
from screen_base import Pantalla
from datos import stats, productos, cuentas, clientes, ventas, cli_por_id, margen
from jev.context import construir_contexto
from jev.openrouter import MODELO_PREDETERMINADO, OpenRouterError, completar_chat
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

# Paleta local para las burbujas premium (coherente con Figma + tests main-only).
COLORS = {
    "primary": "#16a34a",
    "primary_bg": "#dcfce7",
    "bg": "#f8fafc",
    "surface": "#ffffff",
    "text": "#0f172a",
    "muted": "#64748b",
    "border": "#e2e8f0",
    "assistant_bg": "#f1f5f9",
    "user_bg": "#dcfce7",
}

RADIUS_BUBBLE = 16
RADIUS_CONTAINER = 16
RADIUS_INPUT = 24


def respuesta_local(texto: str) -> str:
    """Responde solo a intents simples; no es IA ni reemplaza un informe."""
    minus = (texto or "").strip().lower()
    if "ganancia" in minus and ("mes" in minus or "histor" in minus or "confiable" in minus):
        return (
            "La ganancia histórica todavía no es confiable: las ventas no guardan "
            "el costo vigente al momento de cobrarlas."
        )

    if "debe" in minus or "fiado" in minus:
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

    if "margen" in minus or "ganancia" in minus:
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

    if "stock" in minus:
        lineas = [f"{p['nombre']}: {p['stock']}u" for p in productos if p["stock"] <= p["minimo"]]
        return "Stock bajo:\n" + "\n".join(lineas) if lineas else "Todo con stock suficiente."

    if "resumen" in minus:
        resumen = stats()
        return (
            f"Resumen — ventas de hoy: {moneda(resumen['hoy'])}; "
            f"ventas del mes: {moneda(resumen['mes'])}; "
            f"por cobrar: {moneda(resumen['deben'])}."
        )

    if any(palabra in minus for palabra in ("venta", "vend", "hoy", "mes", "semana")):
        if "hoy" in minus:
            return f"Ventas de hoy: {moneda(stats()['hoy'])}."
        if "mes" in minus:
            return f"Ventas del mes: {moneda(stats()['mes'])}."
        if "semana" in minus:
            desde = date.today() - timedelta(days=6)
            total = sum(
                venta["total"]
                for venta in ventas
                if desde.isoformat() <= venta.get("fecha", "") <= date.today().isoformat()
            )
            return f"Ventas de los últimos 7 días (incluido hoy): {moneda(total)}."
        return "¿Qué periodo querés consultar: hoy, últimos 7 días o este mes?"

    if "cliente" in minus:
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
        # ── Input premium (main-only) con sync 0.84 ──
        self.campo_mensaje = ft.TextField(
            hint_text="Preguntale a tu negocio...",
            expand=True,
            filled=True,
            border_radius=RADIUS_INPUT,
            on_submit=self.enviar_mensaje,
        )
        sincronizar_texto(self.campo_mensaje)

        # ── ListView mensajes premium (main-only) ──
        self.contenedor_mensajes = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            padding=ft.padding.all(8),
        )
        # Compat: la arquitectura newer usaba _zona_chat; es el mismo ListView.
        self._zona_chat = self.contenedor_mensajes
        # Mensaje inicial solo visual (no entra a self.mensajes para no romper
        # el historial que usa OpenRouter ni los tests de privacidad).
        self._agregar_fila("Preguntame sobre tu negocio. Ej: cuanto vendi hoy?, que margen tengo?")

        self.confirmacion_datos = ft.Checkbox(
            label=(
                "Autorizo enviar a OpenRouter mi pregunta, el resumen del negocio y hasta los últimos 8 mensajes "
                "del chat durante esta sesión."
            ),
            value=self.acepta_envio,
            on_change=self._al_cambiar_autorizacion,
        )

        # ── Botón circular (main-only) con gate de privacidad (newer) ──
        try:
            self.boton_enviar = ft.FilledButton(
                content=ft.Icon(ft.Icons.SEND_ROUNDED, color="white", size=18),
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    bgcolor=COLORS["primary"],
                    padding=12,
                ),
                on_click=self.enviar_mensaje,
                disabled=True,
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
                style=ft.ButtonStyle(bgcolor=COLORS["primary"], color="white"),
                on_click=self.enviar_mensaje,
                disabled=True,
            )

        # ── Header premium (main-only): primera fila del Column ──
        avatar_ia_header = ft.Container(
            content=ft.Icon(ft.Icons.SMART_TOY, color="white", size=18),
            width=36,
            height=36,
            bgcolor=COLORS["primary"],
            border_radius=10,
            alignment=ft.Alignment.CENTER,
        )
        header = ft.Row(
            [
                avatar_ia_header,
                ft.Column(
                    [
                        ft.Text(
                            "Chat IA", size=18, weight=ft.FontWeight.BOLD, color=COLORS["text"]
                        ),
                        ft.Text(
                            "Responde con tus datos reales • GesKio Assistant",
                            size=12,
                            color=COLORS["muted"],
                        ),
                    ],
                    spacing=2,
                    expand=True,
                    tight=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "En vivo", size=10, weight=ft.FontWeight.BOLD, color=COLORS["primary"]
                    ),
                    bgcolor=COLORS["primary_bg"],
                    padding=ft.padding.symmetric(horizontal=10, vertical=6),
                    border_radius=20,
                    border=ft.border.all(1, "#bbf7d0"),
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        header_container = ft.Container(
            content=header,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["surface"],
            border=ft.border.all(1, COLORS["border"]),
            border_radius=RADIUS_CONTAINER,
        )

        mensajes_container = ft.Container(
            content=self.contenedor_mensajes,
            expand=True,
            bgcolor="white",
            border=ft.border.all(1, COLORS["border"]),
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
            padding=ft.padding.symmetric(horizontal=4, vertical=4),
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
                    "Cada consulta y hasta 8 mensajes previos pueden acompañar un resumen con nombres y saldos de "
                    "clientes, productos/precios/stock y ventas agregadas. Se excluyen teléfonos, IDs y el JSON "
                    "completo. Podés retirar el permiso desmarcando la casilla; OpenRouter puede aplicar cargos. "
                    "El Chat no modifica datos y el historial se borra al cerrar.",
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
        if os.environ.get("OPENROUTER_API_KEY", "").strip():
            modelo = os.environ.get("OPENROUTER_MODEL", "").strip() or MODELO_PREDETERMINADO
            return f"Clave configurada · modelo {modelo}"
        return (
            "Falta configurar OPENROUTER_API_KEY en el entorno antes de usar el chat. "
            "La clave no se guarda en el JSON de GesKio."
        )

    def _agregar_fila(self, texto, es_usuario=False):
        """Solo pinta la burbuja premium en el ListView (sin tocar el historial)."""
        try:
            hora = datetime.now().strftime("%H:%M")
            inicial = "T" if es_usuario else "IA"
            avatar_bg = COLORS["primary"] if es_usuario else "#0f172a"
            bubble_bg = COLORS["user_bg"] if es_usuario else COLORS["assistant_bg"]
            bubble_border = None
            if not es_usuario:
                bubble_border = ft.border.all(1, COLORS["border"])

            avatar = ft.CircleAvatar(
                content=ft.Text(inicial, color="white", weight=ft.FontWeight.BOLD, size=11),
                bgcolor=avatar_bg,
                radius=16,
            )
            bubble = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(texto, size=14, color=COLORS["text"], selectable=True),
                        ft.Text(hora, size=10, color=COLORS["muted"]),
                    ],
                    spacing=4,
                    tight=True,
                ),
                padding=ft.padding.symmetric(horizontal=14, vertical=10),
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

    def _pintar_chat(self):
        # Reconcilia el ListView con el historial (patrón 0.84: re-montar + update).
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
        # Firma dual: newer (texto, es_usuario) y main-only (text, is_user).
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
        if not self.acepta_envio:
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
        try:
            self.campo_mensaje.update()
            self.boton_enviar.update()
        except Exception:
            pass
        self._pintar_chat()

        try:
            contexto = construir_contexto()
            respuesta = await asyncio.to_thread(completar_chat, contexto, historial, texto)
            self.agregar_mensaje(respuesta, False)
            self.mensajes = self.mensajes[-80:]
        except OpenRouterError:
            # Sin clave o con error del provider: fallback local con datos
            # reales en vez de dejar el chat mudo. No se registra el cuerpo
            # del error: algunas librerías incluyen datos del request.
            try:
                self.agregar_mensaje(respuesta_local(texto), False)
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
            self._pintar_chat()
            try:
                self.campo_mensaje.update()
                self.boton_enviar.update()
            except Exception:
                pass
