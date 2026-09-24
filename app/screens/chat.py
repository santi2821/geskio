import asyncio
import os

import flet as ft
from datetime import date, timedelta
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
    campo_texto,
    burbuja_chat,
    encabezado,
    seccion,
    moneda,
    leer_texto,
    sincronizar_texto,
)


def respuesta_local(texto: str) -> str:
    """Responde solo a intents simples; no es IA ni reemplaza un informe."""
    minus = (texto or "").strip().lower()
    if "ganancia" in minus:
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

    if "margen" in minus:
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
        lineas = [
            f"{p['nombre']}: {p['stock']}u"
            for p in productos
            if p["stock"] <= p["minimo"]
        ]
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
        self._zona_chat = ft.Container(expand=True)
        self.campo_mensaje = campo_texto(
            hint_text="Preguntale a tu negocio...",
            expand=True,
            on_submit=self.enviar_mensaje,
        )
        sincronizar_texto(self.campo_mensaje)
        self.boton_enviar = ft.IconButton(
            ft.Icons.SEND,
            icon_size=ICON_MD,
            tooltip="Enviar",
            on_click=self.enviar_mensaje,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: paleta.primary},
                color={ft.ControlState.DEFAULT: paleta.on_primary},
            ),
            disabled=True,
        )
        self.confirmacion_datos = ft.Checkbox(
            label=(
                "Autorizo enviar a OpenRouter mi pregunta, el resumen del negocio y hasta los últimos 8 mensajes "
                "del chat durante esta sesión."
            ),
            value=self.acepta_envio,
            on_change=self._al_cambiar_autorizacion,
        )

        # el build pinta el estado actual sin update: entra montado con la pantalla
        self._pintar_chat()

        conversacion = seccion("Conversación", self._zona_chat)
        try:
            conversacion.expand = True
            conversacion.width = float("inf")
            conversacion.content.expand = True
        except Exception:
            pass

        return ft.Column(
            [
                encabezado(
                    "Consultas",
                    descripcion="Preguntale al asistente sobre las ventas, el inventario y el fiado.",
                ),
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
                ft.Divider(
                    height=ALTO_DIVISOR,
                    thickness=ANCHO_BORDE,
                    color=paleta.border,
                ),
                conversacion,
                ft.Row(
                    [
                        self.campo_mensaje,
                        self.boton_enviar,
                    ],
                    spacing=SP_8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=SP_10,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
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

    def _pintar_chat(self):
        # arma las burbujas en la zona, sin update
        if not self.mensajes and not self.enviando:
            self._zona_chat.content = ft.Column(
                [
                    ft.Text(
                        "Todavía no hay mensajes. Preguntame algo para empezar.",
                        size=FS_14,
                        color=colores.get().text_muted,
                    )
                ],
                spacing=SP_8,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
            return
        burbujas = [burbuja_chat(t, u) for t, u in self.mensajes]
        if self.enviando:
            burbujas.append(
                ft.Text("El asistente está consultando tus datos…", size=FS_13, color=colores.get().text_muted)
            )
        self._zona_chat.content = ft.Column(
            burbujas, spacing=SP_8, scroll=ft.ScrollMode.AUTO, expand=True
        )

    def agregar_mensaje(self, texto, es_usuario=False):
        try:
            self.mensajes.append((texto, es_usuario))
            # refresco por re-montaje del contenido (patron que funciona en 0.84)
            self._pintar_chat()
            self._zona_chat.update()
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
            self.campo_mensaje.error_text = "Confirmá el envío de datos a OpenRouter antes de enviar."
            try:
                self.campo_mensaje.update()
            except Exception:
                pass
            return

        historial = [
            ("user" if usuario else "assistant", mensaje)
            for mensaje, usuario in self.mensajes[-8:]
        ]
        self.mensajes.append((texto, True))
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
            self._zona_chat.update()
        except Exception:
            pass

        try:
            contexto = construir_contexto()
            respuesta = await asyncio.to_thread(
                completar_chat, contexto, historial, texto
            )
            self.mensajes.append((respuesta, False))
            self.mensajes = self.mensajes[-80:]
        except OpenRouterError as error:
            self.mensajes.append((str(error), False))
        except Exception:
            # No registrar la excepción: algunas librerías incluyen datos del request.
            self.mensajes.append(("Ocurrió un error inesperado al consultar el asistente.", False))
        finally:
            self.enviando = False
            self.campo_mensaje.disabled = False
            self.boton_enviar.disabled = not self.acepta_envio
            self._pintar_chat()
            try:
                self.campo_mensaje.update()
                self.boton_enviar.update()
                self._zona_chat.update()
            except Exception:
                pass
