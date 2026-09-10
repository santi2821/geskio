import flet as ft
from screen_base import Screen
from datos import stats, productos, cuentas, clientes, cli_por_id, margen
from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    FS_13,
    FS_14,
    ICON_MD,
    SP_8,
    SP_10,
    app_colors,
)
from widgets import ChatBubble, PageHeader, Section, sync_text


class PantallaChat(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Chat IA")

    def build(self):
        palette = app_colors.get()
        self.contenedor_mensajes = ft.Column(
            spacing=SP_8, scroll=ft.ScrollMode.AUTO, expand=True
        )
        self.campo_mensaje = ft.TextField(
            hint_text="Preguntale a tu negocio...",
            expand=True,
            on_submit=self.enviar_mensaje,
        )
        sync_text(self.campo_mensaje)

        self.estado_vacio = ft.Text(
            "Todavía no hay mensajes. Preguntame algo para empezar.",
            size=FS_14,
            color=palette.text_muted,
        )
        self._sincronizar_vacio()

        self.agregar_mensaje(
            "Preguntame sobre tu negocio. Ej: cuanto vendi hoy?, que margen tengo?"
        )

        conversacion = Section("Conversación", self.contenedor_mensajes)

        return ft.Column(
            [
                PageHeader("Chat IA"),
                ft.Text(
                    "Responde con tus datos reales",
                    size=FS_13,
                    color=palette.text_muted,
                ),
                ft.Divider(
                    height=DIVIDER_HEIGHT,
                    thickness=BORDER_WIDTH,
                    color=palette.border,
                ),
                conversacion,
                ft.Row(
                    [
                        self.campo_mensaje,
                        ft.IconButton(
                            ft.Icons.SEND,
                            icon_color=palette.primary,
                            icon_size=ICON_MD,
                            tooltip="Enviar",
                            on_click=self.enviar_mensaje,
                        ),
                    ],
                    spacing=SP_8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=SP_10,
            expand=True,
        )

    def _sincronizar_vacio(self):
        try:
            vacio = len(self.contenedor_mensajes.controls) == 0
            if vacio and self.estado_vacio not in self.contenedor_mensajes.controls:
                self.contenedor_mensajes.controls = [self.estado_vacio]
            elif not vacio and len(self.contenedor_mensajes.controls) > 1:
                self.contenedor_mensajes.controls = [
                    c
                    for c in self.contenedor_mensajes.controls
                    if c is not self.estado_vacio
                ]
        except Exception:
            pass

    def agregar_mensaje(self, text, is_user=False):
        try:
            nuevo = ChatBubble(text, is_user)
            controles = [
                c
                for c in list(self.contenedor_mensajes.controls)
                if c is not getattr(self, "estado_vacio", None)
            ] + [nuevo]
            self.contenedor_mensajes.controls = controles
            self._sincronizar_vacio()
        except Exception as ex:
            print(f"Error agregar_mensaje: {ex}")

    def enviar_mensaje(self, e=None):
        try:
            q = self.campo_mensaje.value.strip()
            if not q:
                return
            self.agregar_mensaje(q, is_user=True)
            self.campo_mensaje.value = ""
            ql = q.lower()

            if "debe" in ql or "fiado" in ql:
                deudas = []
                for c in cuentas:
                    p = c["total"] - c["pagado"]
                    if p > 0:
                        cli = cli_por_id(c["cliente_id"])
                        deudas.append(f"{cli['nombre'] if cli else '?'}: ${p:,}")
                self.agregar_mensaje(
                    "\n".join(deudas) if deudas else "Nadie te debe plata."
                )

            elif "margen" in ql or "ganancia" in ql:
                ps = sorted(
                    productos,
                    key=lambda p: margen(p["costo"], p["precio"]),
                    reverse=True,
                )
                lines = [
                    f"{p['nombre']}: {margen(p['costo'],p['precio'])}% (stock {p['stock']})"
                    for p in ps[:5]
                ]
                self.agregar_mensaje("Top 5 por margen:\n" + "\n".join(lines))

            elif "stock" in ql:
                lines = [
                    f"{p['nombre']}: {p['stock']}u"
                    for p in productos
                    if p["stock"] <= p["minimo"]
                ]
                self.agregar_mensaje(
                    "Stock bajo:\n" + "\n".join(lines)
                    if lines
                    else "Todo con stock suficiente."
                )

            elif "venta" in ql or "hoy" in ql or "mes" in ql or "resumen" in ql:
                s = stats()
                self.agregar_mensaje(
                    f"Hoy: ${s['hoy']:,} | Mes: ${s['mes']:,} | Ganancia: ${s['ganancia']:,} | Deben: ${s['deben']:,}"
                )

            elif "cliente" in ql:
                self.agregar_mensaje("" + ", ".join(c["nombre"] for c in clientes))

            else:
                self.agregar_mensaje(
                    "Proba: cuanto vendi hoy? que margen tengo? quien me debe?"
                )
        except Exception as ex:
            print(f"Error enviar_mensaje: {ex}")
        self.pagina.update()
