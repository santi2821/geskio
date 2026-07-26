import flet as ft
from screen_base import Screen
from datos import productos, crear_producto, actualizar_producto, eliminar_producto, ajustar_stock, margen


class PantallaStock(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Stock")

    def actualizar(self):
        self.filtrar_datos()

    def build(self):
        self.campo_buscar = ft.TextField(hint_text="Buscar producto...", expand=True, on_change=lambda _: self.filtrar_datos())

        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Costo")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("%")),
                ft.DataColumn(ft.Text("Stock")),
                ft.DataColumn(ft.Text("Min")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            column_spacing=12,
        )

        self.campo_nombre = ft.TextField(label="Nombre")
        self.campo_costo = ft.TextField(label="Costo $", keyboard_type=ft.KeyboardType.NUMBER)
        self.campo_precio = ft.TextField(label="Precio $", keyboard_type=ft.KeyboardType.NUMBER)
        self.campo_stock = ft.TextField(label="Stock", value="0", keyboard_type=ft.KeyboardType.NUMBER)
        self.campo_minimo = ft.TextField(label="Minimo", value="5", keyboard_type=ft.KeyboardType.NUMBER)

        return ft.Column([
            ft.Text("Stock", size=30, weight=ft.FontWeight.BOLD),
            self.campo_buscar,
            ft.Column([self.tabla_datos], scroll=ft.ScrollMode.AUTO, expand=True),
            ft.Divider(),
            ft.Text("Nuevo producto", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.campo_nombre, self.campo_costo, self.campo_precio,
                self.campo_stock, self.campo_minimo,
                ft.ElevatedButton("Guardar", on_click=self.guardar_nuevo),
            ], spacing=8),
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── filtro ───────────────────────────────────────────────────────

    def filtrar_datos(self):
        try:
            q = (self.campo_buscar.value or "").lower()
            filas = []
            for p in productos:
                if q and q not in p["nombre"].lower():
                    continue
                m = margen(p["costo"], p["precio"])
                bajo = p["stock"] <= p["minimo"]
                pid = p["id"]

                filas.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p["nombre"], weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(f"${p['costo']:,}")),
                    ft.DataCell(ft.Text(f"${p['precio']:,}")),
                    ft.DataCell(ft.Text(f"{m}%")),
                    ft.DataCell(ft.Text(str(p["stock"]), color=ft.Colors.RED if bajo else None,
                                        weight=ft.FontWeight.BOLD if bajo else None)),
                    ft.DataCell(ft.Text(str(p["minimo"]))),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_size=16, tooltip="Editar",
                                      on_click=lambda _, x=pid: self.editar_producto(x)),
                        ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_size=16, tooltip="Ajustar stock",
                                      on_click=lambda _, x=pid: self.ajustar_stock_dialog(x)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_size=16, tooltip="Eliminar",
                                      icon_color=ft.Colors.ERROR,
                                      on_click=lambda _, x=pid: self.eliminar_producto(x)),
                    ], spacing=2)),
                ]))
            if not filas:
                filas.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Sin resultados", italic=True)) for _ in range(7)
                ]))
            self.tabla_datos.rows = filas
        except Exception as ex:
            print(f"Error en filtrar_datos: {ex}")
        self.pagina.update()

    # ─── nuevo producto ─────────────────────────────────────────────

    def guardar_nuevo(self, e=None):
        try:
            nombre = self.campo_nombre.value.strip()
            if not nombre:
                return
            try:
                crear_producto(
                    nombre,
                    float(self.campo_costo.value or 0),
                    float(self.campo_precio.value or 0),
                    int(self.campo_stock.value or 0),
                    int(self.campo_minimo.value or 5),
                )
            except ValueError:
                self.mostrar_alerta("Revisa los valores numericos")
                return
            self.campo_nombre.value = ""
            self.campo_costo.value = ""
            self.campo_precio.value = ""
            self.campo_stock.value = "0"
            self.campo_minimo.value = "5"
            self.filtrar_datos()
            self.mostrar_alerta("Producto creado")
        except Exception as ex:
            print(f"Error guardar_nuevo: {ex}")

    # ─── editar producto ────────────────────────────────────────────

    def editar_producto(self, pid):
        try:
            p = next((x for x in productos if x["id"] == pid), None)
            if not p:
                return

            campo_nombre = ft.TextField(label="Nombre", value=p["nombre"])
            campo_costo = ft.TextField(label="Costo $", value=str(p["costo"]), keyboard_type=ft.KeyboardType.NUMBER)
            campo_precio = ft.TextField(label="Precio $", value=str(p["precio"]), keyboard_type=ft.KeyboardType.NUMBER)
            campo_stock = ft.TextField(label="Stock", value=str(p["stock"]), keyboard_type=ft.KeyboardType.NUMBER)
            campo_minimo = ft.TextField(label="Minimo", value=str(p["minimo"]), keyboard_type=ft.KeyboardType.NUMBER)

            def guardar(e):
                try:
                    actualizar_producto(
                        pid,
                        campo_nombre.value.strip() or p["nombre"],
                        float(campo_costo.value or 0),
                        float(campo_precio.value or 0),
                        int(campo_stock.value or 0),
                        int(campo_minimo.value or 5),
                    )
                    dialogo.open = False
                    self.pagina.update()
                    self.filtrar_datos()
                    self.mostrar_alerta("Producto actualizado")
                except ValueError:
                    self.mostrar_alerta("Revisa los valores numericos")
                except Exception as ex:
                    print(f"Error al guardar: {ex}")

            dialogo = ft.AlertDialog(
                title=ft.Text("Editar producto"),
                content=ft.Column([
                    campo_nombre,
                    ft.Row([campo_costo, campo_precio], spacing=8),
                    ft.Row([campo_stock, campo_minimo], spacing=8),
                ], spacing=12, tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                    ft.ElevatedButton("Guardar", on_click=guardar),
                ],
            )
            dialogo.open = True
            if dialogo not in self.pagina.overlay:
                self.pagina.overlay.append(dialogo)
            self.pagina.update()
        except Exception as ex:
            print(f"Error editar_producto: {ex}")

    # ─── ajustar stock ──────────────────────────────────────────────

    def ajustar_stock_dialog(self, pid):
        try:
            p = next((x for x in productos if x["id"] == pid), None)
            if not p:
                return

            texto_actual = ft.Text(f"Stock actual: {p['stock']}", size=16, weight=ft.FontWeight.BOLD)
            campo = ft.TextField(label="Cantidad", value="1", keyboard_type=ft.KeyboardType.NUMBER)

            def aplicar(cantidad):
                try:
                    if p["stock"] + cantidad < 0:
                        self.mostrar_alerta(f"Solo hay {p['stock']} en stock")
                        return
                    ajustar_stock(pid, cantidad)
                    texto_actual.value = f"Stock actual: {p['stock']}"
                    campo.value = "1"
                    self.filtrar_datos()
                except Exception as ex:
                    print(f"Error aplicar: {ex}")

            def confirmar(e):
                try:
                    c = int(campo.value or 0)
                    if c == 0:
                        return
                    ajustar_stock(pid, c)
                    dialogo.open = False
                    self.pagina.update()
                    self.filtrar_datos()
                    self.mostrar_alerta(f"Stock de {p['nombre']} actualizado")
                except ValueError:
                    pass
                except Exception as ex:
                    print(f"Error confirmar: {ex}")

            dialogo = ft.AlertDialog(
                title=ft.Text(f"Ajustar stock — {p['nombre']}"),
                content=ft.Column([
                    texto_actual,
                    ft.Row([
                        ft.ElevatedButton("−10", on_click=lambda e: aplicar(-10)),
                        ft.ElevatedButton("−1", on_click=lambda e: aplicar(-1)),
                        campo,
                        ft.ElevatedButton("+1", on_click=lambda e: aplicar(1)),
                        ft.ElevatedButton("+10", on_click=lambda e: aplicar(10)),
                    ], spacing=6),
                ], spacing=12, tight=True),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                    ft.ElevatedButton("Aplicar y cerrar", on_click=confirmar),
                ],
            )
            dialogo.open = True
            if dialogo not in self.pagina.overlay:
                self.pagina.overlay.append(dialogo)
            self.pagina.update()
        except Exception as ex:
            print(f"Error ajustar_stock_dialog: {ex}")

    # ─── eliminar ───────────────────────────────────────────────────

    def eliminar_producto(self, pid):
        try:
            p = next((x for x in productos if x["id"] == pid), None)
            if not p:
                return

            def confirmar(e):
                try:
                    ok = eliminar_producto(pid)
                    dialogo.open = False
                    self.pagina.update()
                    self.filtrar_datos()
                    if ok:
                        self.mostrar_alerta(f"'{p['nombre']}' eliminado")
                    else:
                        self.mostrar_alerta("No se puede eliminar: tiene ventas asociadas")
                except Exception as ex:
                    print(f"Error confirmar eliminar: {ex}")

            dialogo = ft.AlertDialog(
                title=ft.Text("Eliminar producto"),
                content=ft.Text(f"¿Eliminar '{p['nombre']}'?\nNo se puede deshacer."),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                    ft.ElevatedButton("Eliminar", on_click=confirmar,
                                      style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)),
                ],
            )
            dialogo.open = True
            if dialogo not in self.pagina.overlay:
                self.pagina.overlay.append(dialogo)
            self.pagina.update()
        except Exception as ex:
            print(f"Error eliminar_producto: {ex}")

    # ─── helpers ────────────────────────────────────────────────────

    def cerrar_dialogo(self, dialogo):
        try:
            dialogo.open = False
            self.pagina.update()
        except Exception as ex:
            print(f"Error cerrar dialogo: {ex}")

    def mostrar_alerta(self, texto):
        try:
            sb = ft.SnackBar(ft.Text(texto), open=True, duration=4000)
            if sb not in self.pagina.overlay:
                self.pagina.overlay.append(sb)
            self.pagina.update()
        except Exception as ex:
            print(f"Error mostrar_alerta: {ex}")
