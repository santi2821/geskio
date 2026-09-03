import flet as ft
from screen_base import Screen
from datos import proveedores, crear_proveedor, actualizar_proveedor, eliminar_proveedor


class PantallaProveedores(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Proveedores")

    def actualizar(self):
        self.filtrar_datos()

    def build(self):
        self.campo_buscar = ft.TextField(
            hint_text="Buscar proveedor...", expand=True, on_change=lambda _: self.filtrar_datos()
        )

        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Rubro")),
                ft.DataColumn(ft.Text("")),
            ],
            column_spacing=16,
            expand=True,
        )

        self.campo_nombre = ft.TextField(label="Nombre", expand=True)
        self.campo_telefono = ft.TextField(label="Teléfono", expand=True)
        self.campo_email = ft.TextField(label="Email", expand=True)
        self.campo_rubro = ft.TextField(label="Rubro", expand=True)

        # Wrapper horizontal scroll para DataTable (Flet 0.28.3 premium)
        tabla_scroll = ft.Container(
            content=ft.Row([self.tabla_datos], scroll=ft.ScrollMode.AUTO, expand=True),
            expand=True,
        )

        return ft.Column(
            [
                ft.Text("Proveedores", size=30, weight=ft.FontWeight.BOLD),
                self.campo_buscar,
                tabla_scroll,
                ft.Divider(),
                ft.Row(
                    [
                        self.campo_nombre,
                        self.campo_telefono,
                        self.campo_email,
                        self.campo_rubro,
                        ft.ElevatedButton("Agregar", on_click=self.guardar_nuevo),
                    ],
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    # ─── filtro ───────────────────────────────────────────────────────

    def filtrar_datos(self):
        try:
            q = (self.campo_buscar.value or "").lower()
            filas = []
            for pr in proveedores:
                if q:
                    hay = (
                        q in pr["nombre"].lower()
                        or q in pr.get("telefono", "").lower()
                        or q in pr.get("email", "").lower()
                        or q in pr.get("rubro", "").lower()
                    )
                    if not hay:
                        continue
                pid = pr["id"]
                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(pr["nombre"], weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(pr.get("telefono", "—"))),
                            ft.DataCell(ft.Text(pr.get("email", "—"))),
                            ft.DataCell(ft.Text(pr.get("rubro", "—"))),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            ft.Icons.EDIT,
                                            icon_size=16,
                                            tooltip="Editar",
                                            on_click=lambda _, x=pid: self.editar_proveedor(x),
                                        ),
                                        ft.IconButton(
                                            ft.Icons.DELETE_OUTLINE,
                                            icon_size=16,
                                            tooltip="Eliminar",
                                            icon_color=ft.Colors.ERROR,
                                            on_click=lambda _, x=pid: self.eliminar_proveedor(x),
                                        ),
                                    ],
                                    spacing=2,
                                )
                            ),
                        ]
                    )
                )
            if not filas:
                filas.append(
                    ft.DataRow(
                        cells=[ft.DataCell(ft.Text("Sin resultados", italic=True)) for _ in range(5)]
                    )
                )
            self.tabla_datos.rows = filas
        except Exception as ex:
            print(f"Error en filtrar_datos proveedores: {ex}")
        self.pagina.update()

    # ─── nuevo ───────────────────────────────────────────────────────

    def guardar_nuevo(self, e=None):
        try:
            nombre = (self.campo_nombre.value or "").strip()
            if not nombre:
                return
            crear_proveedor(
                nombre,
                (self.campo_telefono.value or "").strip(),
                (self.campo_email.value or "").strip(),
                (self.campo_rubro.value or "").strip(),
            )
            self.campo_nombre.value = ""
            self.campo_telefono.value = ""
            self.campo_email.value = ""
            self.campo_rubro.value = ""
            self.filtrar_datos()
            self.mostrar_alerta("Proveedor agregado")
        except Exception as ex:
            print(f"Error guardar_nuevo proveedor: {ex}")

    # ─── editar ──────────────────────────────────────────────────────

    def editar_proveedor(self, pid):
        try:
            pr = next((x for x in proveedores if x["id"] == pid), None)
            if not pr:
                return

            campo_nombre = ft.TextField(label="Nombre", value=pr["nombre"])
            campo_telefono = ft.TextField(label="Teléfono", value=pr.get("telefono", ""))
            campo_email = ft.TextField(label="Email", value=pr.get("email", ""))
            campo_rubro = ft.TextField(label="Rubro", value=pr.get("rubro", ""))

            def guardar(e):
                try:
                    actualizar_proveedor(
                        pid,
                        campo_nombre.value.strip() or pr["nombre"],
                        campo_telefono.value.strip(),
                        campo_email.value.strip(),
                        campo_rubro.value.strip(),
                    )
                    self.cerrar_dialogo(dialogo)
                    self.filtrar_datos()
                    self.mostrar_alerta("Proveedor actualizado")
                except Exception as ex:
                    print(f"Error guardar editar proveedor: {ex}")

            dialogo = ft.AlertDialog(
                modal=True,
                open=False,
                shape=ft.RoundedRectangleBorder(radius=16),
                title=ft.Text("Editar proveedor"),
                content=ft.Column(
                    [campo_nombre, campo_telefono, campo_email, campo_rubro],
                    spacing=12,
                    tight=True,
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                    ft.ElevatedButton("Guardar", on_click=guardar),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.abrir_dialogo(dialogo)
        except Exception as ex:
            print(f"Error editar_proveedor: {ex}")

    # ─── eliminar ────────────────────────────────────────────────────

    def eliminar_proveedor(self, pid):
        try:
            pr = next((x for x in proveedores if x["id"] == pid), None)
            if not pr:
                return

            def confirmar(e):
                try:
                    eliminar_proveedor(pid)
                    self.cerrar_dialogo(dialogo)
                    self.filtrar_datos()
                    self.mostrar_alerta(f"'{pr['nombre']}' eliminado")
                except Exception as ex:
                    print(f"Error confirmar eliminar proveedor: {ex}")

            dialogo = ft.AlertDialog(
                modal=True,
                open=False,
                shape=ft.RoundedRectangleBorder(radius=16),
                title=ft.Text("Eliminar proveedor"),
                content=ft.Text(f"¿Eliminar a '{pr['nombre']}'?\nNo se puede deshacer."),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                    ft.ElevatedButton(
                        "Eliminar",
                        on_click=confirmar,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.abrir_dialogo(dialogo)
        except Exception as ex:
            print(f"Error eliminar_proveedor: {ex}")

    # ─── helpers (heredados de Screen) ──────────────────────────────

    def cerrar_dialogo(self, dialogo):
        return super().cerrar_dialogo(dialogo)

    def mostrar_alerta(self, texto):
        return super().mostrar_alerta(texto)
