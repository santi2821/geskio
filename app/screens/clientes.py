import flet as ft
from screen_base import Screen
from datos import (
    clientes,
    ventas,
    cuentas,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente,
)
from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    FS_20,
    FS_30,
    ICON_SM,
    SP_4,
    SP_8,
    SP_10,
    SP_12,
    app_colors,
    role_color,
)
from widgets import AppDialog, AppTable, confirm_delete, feedback


class PantallaClientes(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Clientes")

    def actualizar(self):
        self.filtrar_datos()

    def build(self):
        palette = app_colors.get()
        self.campo_buscar = ft.TextField(
            hint_text="Buscar cliente...",
            expand=True,
            on_change=lambda _: self.filtrar_datos(),
        )

        self._columnas = [
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Telefono")),
            ft.DataColumn(ft.Text("Compras")),
            ft.DataColumn(ft.Text("Debe")),
            ft.DataColumn(ft.Text("")),
        ]
        self._tabla_holder = ft.Column(
            [AppTable(self._columnas, [], empty_message="Sin resultados")],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        self.campo_nombre = ft.TextField(label="Nombre", expand=True)
        self.campo_telefono = ft.TextField(label="Telefono")

        return ft.Column(
            [
                ft.Text(
                    "Clientes",
                    size=FS_30,
                    weight=ft.FontWeight.BOLD,
                    color=palette.text,
                ),
                self.campo_buscar,
                self._tabla_holder,
                ft.Divider(
                    height=DIVIDER_HEIGHT, thickness=BORDER_WIDTH, color=palette.border
                ),
                ft.Row(
                    [
                        self.campo_nombre,
                        self.campo_telefono,
                        ft.ElevatedButton("Agregar", on_click=self.guardar_nuevo),
                    ],
                    spacing=SP_8,
                ),
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    # ─── filtro ───────────────────────────────────────────────────────

    def filtrar_datos(self):
        try:
            palette = app_colors.get()
            deuda_color = role_color(palette, "danger")
            q = (self.campo_buscar.value or "").lower()
            filas = []
            for c in clientes:
                if (
                    q
                    and q not in c["nombre"].lower()
                    and q not in c.get("telefono", "")
                ):
                    continue
                compras = len([v for v in ventas if v.get("cliente_id") == c["id"]])
                debe = sum(
                    x["total"] - x["pagado"]
                    for x in cuentas
                    if x["cliente_id"] == c["id"]
                )
                cid = c["id"]

                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(c["nombre"], weight=ft.FontWeight.BOLD)
                            ),
                            ft.DataCell(ft.Text(c.get("telefono", "—"))),
                            ft.DataCell(ft.Text(str(compras))),
                            ft.DataCell(
                                ft.Text(
                                    f"${debe:,}",
                                    color=deuda_color if debe else None,
                                    weight=ft.FontWeight.BOLD if debe else None,
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            ft.Icons.EDIT,
                                            icon_size=ICON_SM,
                                            tooltip="Editar",
                                            on_click=lambda _, x=cid: (
                                                self.editar_cliente(x)
                                            ),
                                        ),
                                        ft.IconButton(
                                            ft.Icons.DELETE_OUTLINE,
                                            icon_size=ICON_SM,
                                            tooltip="Eliminar",
                                            icon_color=palette.danger,
                                            on_click=lambda _, x=cid: (
                                                self.eliminar_cliente(x)
                                            ),
                                        ),
                                    ],
                                    spacing=SP_4,
                                )
                            ),
                        ]
                    )
                )
            self._tabla_holder.controls = [
                AppTable(self._columnas, filas, empty_message="Sin resultados")
            ]
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
                    actualizar_cliente(
                        cid,
                        campo_nombre.value.strip() or c["nombre"],
                        campo_telefono.value.strip(),
                    )
                    dialogo.open = False
                    self.pagina.update()
                    self.filtrar_datos()
                    self.mostrar_alerta("Cliente actualizado")
                except Exception as ex:
                    print(f"Error guardar editar cliente: {ex}")

            dialogo = AppDialog(
                "Editar cliente",
                ft.Column([campo_nombre, campo_telefono], spacing=SP_12, tight=True),
                actions=[
                    ft.TextButton(
                        "Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)
                    ),
                    ft.ElevatedButton("Guardar", on_click=guardar),
                ],
            )
            dialogo.open = True
            if dialogo not in self.pagina.overlay:
                self.pagina.overlay.append(dialogo)
            self.pagina.update()
        except Exception as ex:
            print(f"Error editar_cliente: {ex}")

    # ─── eliminar ──────────────────────────────────────────────────

    def eliminar_cliente(self, cid):
        try:
            c = next((x for x in clientes if x["id"] == cid), None)
            if not c:
                return

            tiene_deuda = (
                sum(x["total"] - x["pagado"] for x in cuentas if x["cliente_id"] == cid)
                > 0
            )

            def confirmar(e):
                try:
                    eliminar_cliente(cid)
                    self.filtrar_datos()
                    self.mostrar_alerta(f"'{c['nombre']}' eliminado")
                except Exception as ex:
                    print(f"Error confirmar eliminar cliente: {ex}")

            msg = f"¿Eliminar a '{c['nombre']}'?"
            if tiene_deuda:
                msg += "\nTiene deudas pendientes"
            msg += "\nNo se puede deshacer."

            confirm_delete(
                self.pagina,
                confirmar,
                item_name=c["nombre"],
                title="Eliminar cliente",
                message=msg,
            )
        except Exception as ex:
            print(f"Error eliminar_cliente: {ex}")

    # ─── helpers ───────────────────────────────────────────────────

    def cerrar_dialogo(self, dialogo):
        try:
            dialogo.open = False
            self.pagina.update()
        except Exception as ex:
            print(f"Error cerrar dialogo: {ex}")

    def mostrar_alerta(self, texto):
        try:
            feedback(self.pagina, texto)
        except Exception as ex:
            print(f"Error mostrar_alerta: {ex}")
