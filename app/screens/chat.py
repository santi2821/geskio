import flet as ft
from screen_base import Screen
from datos import stats, productos, cuentas, clientes, cli_por_id, margen
from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    FS_13,
    FS_30,
    ICON_MD,
    R_MD,
    SP_8,
    SP_10,
    SP_12,
    app_colors,
)
from widgets import ChatBubble


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

        self.agregar_mensaje(
            "Preguntame sobre tu negocio. Ej: cuanto vendi hoy?, que margen tengo?"
        )

        return ft.Column(
            [
                ft.Text(
                    "Chat IA",
                    size=FS_30,
                    weight=ft.FontWeight.BOLD,
                    color=palette.text,
                ),
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
                ft.Container(
                    content=self.contenedor_mensajes,
                    expand=True,
                    border_radius=ft.BorderRadius.all(R_MD),
                    bgcolor=palette.surface,
                    border=ft.border.all(BORDER_WIDTH, palette.border),
                    padding=SP_12,
                ),
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

    def agregar_mensaje(self, text, is_user=False):
        try:
            nuevo = ChatBubble(text, is_user)
            self.contenedor_mensajes.controls = list(
                self.contenedor_mensajes.controls
            ) + [nuevo]
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
