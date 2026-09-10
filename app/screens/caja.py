import flet as ft
from screen_base import Screen
from datos import productos, clientes, crear_venta, prod_por_id
from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    FS_12,
    FS_13,
    FS_14,
    FS_16,
    FS_20,
    FS_30,
    FS_36,
    ICON_SM,
    R_SM,
    SP_4,
    SP_8,
    SP_10,
    SP_12,
    app_colors,
)
from widgets import AppCard, feedback


class PantallaCaja(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Caja")
        self.items_carrito = []

    def actualizar(self):
        self.items_carrito.clear()
        self.cargar_opciones()
        self.actualizar_carrito()

    def cargar_opciones(self):
        try:
            self.combo_cliente.options = [ft.dropdown.Option("", "— Mostrador —")] + [
                ft.dropdown.Option(c["id"], c["nombre"]) for c in clientes
            ]
            self.combo_producto.options = [
                ft.dropdown.Option(
                    p["id"], f"{p['nombre']} (${p['precio']:,} — stock: {p['stock']})"
                )
                for p in productos
                if p["stock"] > 0
            ]
            self.pagina.update()
        except Exception as ex:
            print(f"Error cargar_opciones: {ex}")

    def build(self):
        palette = app_colors.get()
        self.combo_cliente = ft.Dropdown(
            label="Cliente", hint_text="Mostrador", expand=True
        )
        self.combo_pago = ft.Dropdown(
            label="Pago",
            value="efectivo",
            expand=True,
            options=[
                ft.dropdown.Option("efectivo"),
                ft.dropdown.Option("transferencia"),
                ft.dropdown.Option("debito"),
                ft.dropdown.Option("credito"),
                ft.dropdown.Option("fiado", "Fiado"),
            ],
        )
        self.combo_producto = ft.Dropdown(
            label="Producto",
            expand=True,
            on_change=self.on_producto_change,
        )
        self.campo_cantidad = ft.TextField(
            label="Cant", value="1", width=80, keyboard_type=ft.KeyboardType.NUMBER
        )

        self.lista_carrito = ft.Column(spacing=SP_4)
        self.texto_total = ft.Text(
            "$0", size=FS_36, weight=ft.FontWeight.BOLD, color=palette.success
        )
        self.texto_items = ft.Text("0 items", size=FS_13, color=palette.text_muted)

        return ft.Column(
            [
                ft.Text(
                    "Caja", size=FS_30, weight=ft.FontWeight.BOLD, color=palette.text
                ),
                ft.Row([self.combo_cliente, self.combo_pago], spacing=SP_12),
                ft.Row(
                    [
                        self.combo_producto,
                        self.campo_cantidad,
                        ft.ElevatedButton(
                            "Agregar", icon=ft.Icons.ADD, on_click=self.agregar_item
                        ),
                    ],
                    spacing=SP_12,
                ),
                ft.Divider(
                    height=DIVIDER_HEIGHT,
                    thickness=BORDER_WIDTH,
                    color=palette.border,
                ),
                ft.Row(
                    [
                        ft.Text(
                            "Carrito",
                            size=FS_16,
                            weight=ft.FontWeight.BOLD,
                            color=palette.text,
                        ),
                        self.texto_items,
                        ft.Container(expand=True),
                        ft.TextButton(
                            "Vaciar",
                            icon=ft.Icons.DELETE_SWEEP,
                            on_click=self.vaciar_carrito,
                        ),
                    ]
                ),
                AppCard(self.lista_carrito, padding=SP_8),
                ft.Divider(
                    height=DIVIDER_HEIGHT,
                    thickness=BORDER_WIDTH,
                    color=palette.border,
                ),
                ft.Row(
                    [
                        ft.Text(
                            "TOTAL",
                            size=FS_20,
                            weight=ft.FontWeight.BOLD,
                            color=palette.text,
                        ),
                        self.texto_total,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.FilledButton(
                    "Cobrar",
                    on_click=self.cobrar_carrito,
                    style=ft.ButtonStyle(
                        bgcolor=palette.primary,
                        color=palette.on_primary,
                        shape=ft.RoundedRectangleBorder(radius=R_SM),
                        padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_8),
                    ),
                ),
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def on_producto_change(self, e):
        """Track selected product ID when user selects from dropdown."""
        try:
            pid = e.data if e.data else e.control.value
            if pid:
                self._ultimo_pid = pid
        except Exception as ex:
            print(f"Error on_producto_change: {ex}")

    # ─── carrito ────────────────────────────────────────────────────

    def actualizar_carrito(self):
        try:
            palette = app_colors.get()
            t = 0
            controles = []
            for i, item in enumerate(self.items_carrito):
                st = item["precio"] * item["cantidad"]
                t += st
                idx = i
                controles.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            item["nombre"],
                                            weight=ft.FontWeight.BOLD,
                                            size=FS_14,
                                            color=palette.text,
                                        ),
                                        ft.Text(
                                            f"${item['precio']:,} x {item['cantidad']}",
                                            size=FS_12,
                                            color=palette.text_muted,
                                        ),
                                    ],
                                    spacing=SP_4,
                                    expand=True,
                                ),
                                ft.Text(
                                    f"${st:,}",
                                    size=FS_16,
                                    weight=ft.FontWeight.BOLD,
                                    color=palette.text,
                                ),
                                ft.IconButton(
                                    ft.Icons.CLOSE,
                                    icon_size=ICON_SM,
                                    icon_color=palette.danger,
                                    on_click=lambda _, n=idx: self.quitar_item(n),
                                ),
                            ]
                        ),
                        padding=ft.padding.symmetric(vertical=SP_4, horizontal=SP_4),
                        border=ft.Border(
                            bottom=ft.BorderSide(BORDER_WIDTH, palette.border)
                        ),
                    )
                )
            self.lista_carrito.controls = controles
            self.texto_total.value = f"${t:,}"
            self.texto_items.value = f"{len(self.items_carrito)} items"
        except Exception as ex:
            print(f"Error actualizar_carrito: {ex}")
        self.pagina.update()

    def quitar_item(self, i):
        try:
            self.items_carrito.pop(i)
            self.actualizar_carrito()
        except Exception as ex:
            print(f"Error quitar_item: {ex}")

    def vaciar_carrito(self, e=None):
        try:
            self.items_carrito.clear()
            self.actualizar_carrito()
        except Exception as ex:
            print(f"Error vaciar_carrito: {ex}")

    def agregar_item(self, e=None):
        try:
            pid = self.combo_producto.value
            # Fallback: use tracked value if direct dropdown value is empty
            if not pid and hasattr(self, "_ultimo_pid"):
                pid = self._ultimo_pid

            if not pid:
                self.mostrar_alerta("Selecciona un producto")
                return

            prod = prod_por_id(pid)
            if not prod:
                self.mostrar_alerta(f"Producto no encontrado (ID: {pid})")
                return

            try:
                qty = int(self.campo_cantidad.value or 1)
            except ValueError:
                qty = 1

            if qty <= 0:
                self.mostrar_alerta("Cantidad invalida")
                return

            if prod["stock"] < qty:
                self.mostrar_alerta(f"Solo hay {prod['stock']} en stock")
                return

            ex = next((x for x in self.items_carrito if x["prod_id"] == pid), None)
            if ex:
                ex["cantidad"] += qty
            else:
                self.items_carrito.append(
                    {
                        "prod_id": pid,
                        "nombre": prod["nombre"],
                        "cantidad": qty,
                        "precio": prod["precio"],
                    }
                )

            self.campo_cantidad.value = "1"
            self.actualizar_carrito()
        except Exception as ex:
            print(f"Error agregar_item: {ex}")
            self.mostrar_alerta(f"Error: {ex}")

    def cobrar_carrito(self, e=None):
        try:
            if not self.items_carrito:
                self.mostrar_alerta("Carrito vacio")
                return
            pago = self.combo_pago.value or "efectivo"
            cid = self.combo_cliente.value or ""

            # verificar stock de nuevo
            for item in self.items_carrito:
                p = prod_por_id(item["prod_id"])
                if p and p["stock"] < item["cantidad"]:
                    self.mostrar_alerta(
                        f"Stock insuficiente de {item['nombre']}: quedan {p['stock']}"
                    )
                    return

            total = sum(i["precio"] * i["cantidad"] for i in self.items_carrito)
            crear_venta(list(self.items_carrito), cid, pago)
            self.items_carrito.clear()
            self.actualizar_carrito()
            self.cargar_opciones()
            self.mostrar_alerta(f"Cobrado ${total:,} — {pago}")
        except Exception as ex:
            print(f"Error cobrar_carrito: {ex}")
            self.mostrar_alerta(f"Error al cobrar: {ex}")

    # ─── helpers ────────────────────────────────────────────────────

    def mostrar_alerta(self, texto):
        try:
            feedback(self.pagina, texto)
        except Exception as ex:
            print(f"Error mostrar_alerta: {ex}")
