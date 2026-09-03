import flet as ft
from datetime import datetime
from screen_base import Screen
from datos import stats, productos, cuentas, clientes, cli_por_id, margen

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


class PantallaChat(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Chat IA")

    def build(self):
        # ── Input premium ──
        self.campo_mensaje = ft.TextField(
            hint_text="Preguntale...",
            expand=True,
            filled=True,
            border_radius=RADIUS_INPUT,
            bgcolor=ft.Colors.WHITE if hasattr(ft.Colors, "WHITE") else "#ffffff",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            on_submit=self.enviar_mensaje,
        )

        # ── ListView mensajes premium ──
        self.contenedor_mensajes = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            padding=ft.padding.all(8),
        )

        # Mensaje inicial sin timestamp extra para demo
        self.agregar_mensaje("Preguntame sobre tu negocio. Ej: cuanto vendi hoy?, que margen tengo?")

        # ── Header premium ──
        avatar_ia_header = ft.Container(
            content=ft.Icon(ft.Icons.SMART_TOY, color="white", size=18),
            width=36,
            height=36,
            bgcolor=COLORS["primary"],
            border_radius=10,
            alignment=ft.alignment.center,
        )
        header = ft.Row(
            [
                avatar_ia_header,
                ft.Column(
                    [
                        ft.Text("Chat IA", size=18, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                        ft.Text("Responde con tus datos reales • GesKio Assistant", size=12, color=COLORS["muted"]),
                    ],
                    spacing=2,
                    expand=True,
                    tight=True,
                ),
                ft.Container(
                    content=ft.Text("En vivo", size=10, weight=ft.FontWeight.BOLD, color=COLORS["primary"]),
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

        # ── Container mensajes con specs: ListView expand, bgcolor white, border 1 #e2e8f0 ──
        mensajes_container = ft.Container(
            content=self.contenedor_mensajes,
            expand=True,
            bgcolor="white",
            border=ft.border.all(1, COLORS["border"]),
            border_radius=RADIUS_CONTAINER,
            padding=14,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        # ── Boton circular FilledButton ──
        # Flet 0.28.3: FilledButton con shape CircleBorder + bgcolor primary
        try:
            btn_send = ft.FilledButton(
                content=ft.Icon(ft.Icons.SEND_ROUNDED, color="white", size=18),
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    bgcolor=COLORS["primary"],
                    padding=12,
                ),
                on_click=self.enviar_mensaje,
            )
        except Exception:
            # fallback si CircleBorder no existe en mock
            btn_send = ft.FilledButton(
                text="Enviar",
                icon=ft.Icons.SEND,
                style=ft.ButtonStyle(bgcolor=COLORS["primary"], color="white"),
                on_click=self.enviar_mensaje,
            )

        input_row = ft.Row(
            [self.campo_mensaje, btn_send],
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
                mensajes_container,
                input_container,
            ],
            spacing=12,
            expand=True,
        )

    def agregar_mensaje(self, text, is_user=False):
        try:
            hora = datetime.now().strftime("%H:%M")
            inicial = "T" if is_user else "IA"
            avatar_bg = COLORS["primary"] if is_user else "#0f172a"
            bubble_bg = COLORS["user_bg"] if is_user else COLORS["assistant_bg"]
            bubble_border = None
            if not is_user:
                bubble_border = ft.border.all(1, COLORS["border"])

            avatar = ft.CircleAvatar(
                content=ft.Text(inicial, color="white", weight=ft.FontWeight.BOLD, size=11),
                bgcolor=avatar_bg,
                radius=16,
            )

            bubble = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(text, size=14, color=COLORS["text"], selectable=True),
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

            # Fila con avatar + burbuja
            if is_user:
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

            # ListView: append control
            self.contenedor_mensajes.controls = list(self.contenedor_mensajes.controls) + [fila]
            try:
                self.pagina.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error agregar_mensaje: {ex}")

    def enviar_mensaje(self, e=None):
        try:
            q = (self.campo_mensaje.value or "").strip()
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
                self.agregar_mensaje("\n".join(deudas) if deudas else "Nadie te debe plata.")

            elif "margen" in ql or "ganancia" in ql:
                ps = sorted(productos, key=lambda p: margen(p["costo"], p["precio"]), reverse=True)
                lines = [f"{p['nombre']}: {margen(p['costo'],p['precio'])}% (stock {p['stock']})" for p in ps[:5]]
                self.agregar_mensaje("Top 5 por margen:\n" + "\n".join(lines))

            elif "stock" in ql:
                lines = [f"{p['nombre']}: {p['stock']}u" for p in productos if p["stock"] <= p["minimo"]]
                self.agregar_mensaje("Stock bajo:\n" + "\n".join(lines) if lines else "Todo con stock suficiente.")

            elif "venta" in ql or "hoy" in ql or "mes" in ql or "resumen" in ql:
                s = stats()
                self.agregar_mensaje(f"Hoy: ${s['hoy']:,} | Mes: ${s['mes']:,} | Ganancia: ${s['ganancia']:,} | Deben: ${s['deben']:,}")

            elif "cliente" in ql:
                self.agregar_mensaje("" + ", ".join(c["nombre"] for c in clientes))

            else:
                self.agregar_mensaje("Proba: cuanto vendi hoy? que margen tengo? quien me debe?")
        except Exception as ex:
            print(f"Error enviar_mensaje: {ex}")
        try:
            self.pagina.update()
        except Exception:
            pass
