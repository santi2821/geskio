import flet as ft
from screen_base import Screen
from datos import clientes, ventas, cuentas, crear_cliente, actualizar_cliente, eliminar_cliente


class PantallaClientes(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Clientes")

    def actualizar(self):
        self.filtrar_datos()

    def build(self):
        self.campo_buscar = ft.TextField(hint_text="Buscar cliente...", expand=True, on_change=lambda _: self.filtrar_datos())

        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Telefono")),
                ft.DataColumn(ft.Text("Compras")),
                ft.DataColumn(ft.Text("Debe")),
                ft.DataColumn(ft.Text("")),
            ],
            column_spacing=16,
            expand=True,
        )

        self.campo_nombre = ft.TextField(label="Nombre", expand=True)
        self.campo_telefono = ft.TextField(label="Telefono", expand=True)

        # Wrapper horizontal scroll para DataTable
        tabla_scroll = ft.Container(
            content=ft.Row([self.tabla_datos], scroll=ft.ScrollMode.AUTO, expand=True),
            expand=True,
        )

        return ft.Column([
            ft.Text("Clientes", size=30, weight=ft.FontWeight.BOLD),
            self.campo_buscar,
            tabla_scroll,
            ft.Divider(),
            ft.Row([self.campo_nombre, self.campo_telefono,
                    ft.ElevatedButton("Agregar", on_click=self.guardar_nuevo)], spacing=8, scroll=ft.ScrollMode.AUTO),
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── filtro ───────────────────────────────────────────────────────

    def filtrar_datos(self):
        try:
            q = (self.campo_buscar.value or "").lower()
            filas = []
            for c in clientes:
                if q and q not in c["nombre"].lower() and q not in c.get("telefono", ""):
                    continue
                compras = len([v for v in ventas if v.get("cliente_id") == c["id"]])
                debe = sum(x["total"] - x["pagado"] for x in cuentas if x["cliente_id"] == c["id"])
                cid = c["id"]

                filas.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(c["nombre"], weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(c.get("telefono", "—"))),
                    ft.DataCell(ft.Text(str(compras))),
                    ft.DataCell(ft.Text(f"${debe:,}", color=ft.Colors.RED if debe else None,
                                        weight=ft.FontWeight.BOLD if debe else None)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_size=16, tooltip="Editar",
                                      on_click=lambda _, x=cid: self.editar_cliente(x)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_size=16, tooltip="Eliminar",
                                      icon_color=ft.Colors.ERROR,
                                      on_click=lambda _, x=cid: self.eliminar_cliente(x)),
                    ], spacing=2)),
                ]))
            if not filas:
                filas.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Sin resultados", italic=True)) for _ in range(5)
                ]))
            self.tabla_datos.rows = filas
        except Exception as ex:
            print(f"Error en filtrar_datos clientes: {ex}")
        self.pagina.update()

    # ─── nuevo ─────────────────────────────────────────────────────

    def guardar_nuevo(self, e=None):
        try:
            nombre = self.campo_nombre.value.strip()
            if not nombre:
                return
            crear_cliente(nombre, self.campo_telefono.value.strip())
            self.campo_nombre.value = ""
            self.campo_telefono.value = ""
            self.filtrar_datos()
            self.mostrar_alerta("Cliente agregado")
        except Exception as ex:
            print(f"Error guardar_nuevo: {ex}")

    # ─── editar ────────────────────────────────────────────────────

    def editar_cliente(self, cid):
        try:
            c = next((x for x in clientes if x["id"] == cid), None)
            if not c:
                return

            campo_nombre = ft.TextField(label="Nombre", value=c["nombre"])
            campo_telefono = ft.TextField(label="Telefono", value=c.get("telefono", ""))

            def guardar(e):
                try:
                    actualizar_cliente(cid, campo_nombre.value.strip() or c["nombre"], campo_telefono.value.strip())
                    self.cerrar_dialogo(dialogo)
                    self.filtrar_datos()
                    self.mostrar_alerta("Cliente actualizado")
                except Exception as ex:
                    print(f"Error guardar editar cliente: {ex}")

            dialogo = ft.AlertDialog(
                modal=True,
                open=False,
                shape=ft.RoundedRectangleBorder(radius=16),
                title=ft.Text("Editar cliente"),
                content=ft.Column([campo_nombre, campo_telefono], spacing=12, tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                    ft.ElevatedButton("Guardar", on_click=guardar),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.abrir_dialogo(dialogo)
        except Exception as ex:
            print(f"Error editar_cliente: {ex}")

    # ─── eliminar ──────────────────────────────────────────────────

    def eliminar_cliente(self, cid):
        try:
            c = next((x for x in clientes if x["id"] == cid), None)
            if not c:
                return

            tiene_deuda = sum(x["total"] - x["pagado"] for x in cuentas if x["cliente_id"] == cid) > 0

            def confirmar(e):
                try:
                    eliminar_cliente(cid)
                    self.cerrar_dialogo(dialogo)
                    self.filtrar_datos()
                    self.mostrar_alerta(f"'{c['nombre']}' eliminado")
                except Exception as ex:
                    print(f"Error confirmar eliminar cliente: {ex}")

            msg = f"¿Eliminar a '{c['nombre']}'?"
            if tiene_deuda:
                msg += "\n⚠️ Tiene deudas pendientes"
            msg += "\nNo se puede deshacer."

            dialogo = ft.AlertDialog(
                modal=True,
                open=False,
                shape=ft.RoundedRectangleBorder(radius=16),
                title=ft.Text("Eliminar cliente"),
                content=ft.Text(msg),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                    ft.ElevatedButton("Eliminar", on_click=confirmar,
                                      style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.abrir_dialogo(dialogo)
        except Exception as ex:
            print(f"Error eliminar_cliente: {ex}")

    # ─── helpers (heredados de Screen) ──────────────────────────────

    def cerrar_dialogo(self, dialogo):
        return super().cerrar_dialogo(dialogo)

    def mostrar_alerta(self, texto):
        return super().mostrar_alerta(texto)
