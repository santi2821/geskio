import flet as ft
from screen_base import Screen
from datos import stats, productos, cuentas, clientes, cli_por_id, margen

class PantallaChat(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Chat IA")

    def build(self):
        self.contenedor_mensajes = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)
        self.campo_mensaje = ft.TextField(hint_text="Preguntale a tu negocio...", expand=True, on_submit=self.enviar_mensaje)

        self.agregar_mensaje("Preguntame sobre tu negocio. Ej: cuanto vendi hoy?, que margen tengo?")

        return ft.Column([
            ft.Text("Chat IA", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Responde con tus datos reales", size=13, color=ft.Colors.GREY_500),
            ft.Divider(),
            ft.Container(content=self.contenedor_mensajes, expand=True, border_radius=12, bgcolor=ft.Colors.SURFACE,
                         border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), padding=14),
            ft.Row([self.campo_mensaje, ft.IconButton(ft.Icons.SEND, icon_color=ft.Colors.GREEN, on_click=self.enviar_mensaje)]),
        ], spacing=10, expand=True)

    def agregar_mensaje(self, text, is_user=False):
        try:
            nuevo = ft.Row([ft.Container(
                content=ft.Text(text, size=14),
                padding=ft.padding.symmetric(horizontal=14, vertical=10),
                border_radius=12,
                bgcolor=ft.Colors.GREEN_50 if is_user else ft.Colors.GREY_100,
            )], alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START)
            self.contenedor_mensajes.controls = list(self.contenedor_mensajes.controls) + [nuevo]
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
        self.pagina.update()
