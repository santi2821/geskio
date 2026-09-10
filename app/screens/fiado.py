from datetime import date
import flet as ft
from screen_base import Screen
from datos import cuentas, cli_por_id, pagar_fiado
from theme import (
    BORDER_WIDTH,
    DIVIDER_HEIGHT,
    FS_20,
    FS_30,
    ICON_SM,
    SP_4,
    SP_10,
    SP_12,
    app_colors,
    role_color,
)
from widgets import AppDialog, AppTable, feedback, sync_text


class PantallaFiado(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Fiado")

    def actualizar(self):
        self.cargar_cuentas()

    def build(self):
        palette = app_colors.get()
        self.filtro_pendientes = ft.Switch(
            label="Solo pendientes",
            value=True,
            on_change=lambda e: self.cargar_cuentas(),
        )

        self._columnas = [
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Pagado")),
            ft.DataColumn(ft.Text("Pendiente")),
            ft.DataColumn(ft.Text("Dias")),
            ft.DataColumn(ft.Text("")),
        ]
        self._tabla_holder = ft.Column(
            [AppTable(self._columnas, [], empty_message="Sin deudas pendientes")],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        return ft.Column(
            [
                ft.Text(
                    "Fiado", size=FS_30, weight=ft.FontWeight.BOLD, color=palette.text
                ),
                self.filtro_pendientes,
                ft.Divider(
                    height=DIVIDER_HEIGHT, thickness=BORDER_WIDTH, color=palette.border
                ),
                self._tabla_holder,
                ft.ElevatedButton(
                    "Refrescar", on_click=lambda _: self.cargar_cuentas()
                ),
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def cargar_cuentas(self):
        try:
            palette = app_colors.get()
            pagado_color = role_color(palette, "paid")
            pendiente_color = role_color(palette, "due")
            vencido_color = role_color(palette, "danger_text")
            solo_pendientes = self.filtro_pendientes.value
            filas = []
            for c in cuentas:
                p = c["total"] - c["pagado"]
                if solo_pendientes and p <= 0:
                    continue
                cli = cli_por_id(c["cliente_id"])
                nombre = cli["nombre"] if cli else "?"
                dias = (
                    (date.today() - date.fromisoformat(c["created_at"])).days
                    if c.get("created_at")
                    else 0
                )
                ccid = c["id"]

                if p <= 0:
                    estado_color = pagado_color
                    estado_icon = ft.Icons.CHECK
                elif dias > 30:
                    estado_color = vencido_color
                    estado_icon = ft.Icons.WARNING
                else:
                    estado_color = pendiente_color
                    estado_icon = ft.Icons.SCHEDULE

                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(nombre, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(f"${c['total']:,}")),
                            ft.DataCell(ft.Text(f"${c['pagado']:,}")),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(
                                            estado_icon,
                                            color=estado_color,
                                            size=ICON_SM,
                                        ),
                                        ft.Text(
                                            f"${p:,}",
                                            color=estado_color,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    spacing=SP_4,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                )
                            ),
                            ft.DataCell(ft.Text(f"{dias}d")),
                            ft.DataCell(
                                ft.ElevatedButton(
                                    "Pagar",
                                    on_click=lambda _, x=ccid: self.abrir_pago(x),
                                )
                                if p > 0
                                else ft.Icon(
                                    ft.Icons.CHECK,
                                    color=pagado_color,
                                    size=ICON_SM,
                                )
                            ),
                        ]
                    )
                )
            self._tabla_holder.controls = [
                AppTable(self._columnas, filas, empty_message="Sin deudas pendientes")
            ]
        except Exception as ex:
            print(f"Error cargar_cuentas: {ex}")
        self.pagina.update()

    def abrir_pago(self, ccid):
        try:
            c = next((x for x in cuentas if x["id"] == ccid), None)
            if not c:
                return
            d = c["total"] - c["pagado"]
            campo_monto = ft.TextField(
                label="Monto $", value=str(d), keyboard_type=ft.KeyboardType.NUMBER
            )
            sync_text(campo_monto)

            def confirmar(e):
                try:
                    m = float(campo_monto.value or 0)
                    if m > 0:
                        pagar_fiado(ccid, m)
                    dialogo.open = False
                    self.pagina.update()
                    self.cargar_cuentas()
                    self.mostrar_alerta("Pago registrado")
                except Exception as ex:
                    print(f"Error confirmar pago: {ex}")

            def cancelar(e):
                try:
                    dialogo.open = False
                    self.pagina.update()
                except Exception as ex:
                    print(f"Error cancelar: {ex}")

            dialogo = AppDialog(
                "Registrar pago",
                ft.Column(
                    [
                        ft.Text(f"Debe ${d:,} de ${c['total']:,}"),
                        campo_monto,
                    ],
                    spacing=SP_12,
                    tight=True,
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.ElevatedButton("Pagar", on_click=confirmar),
                ],
            )
            dialogo.open = True
            if dialogo not in self.pagina.overlay:
                self.pagina.overlay.append(dialogo)
            self.pagina.update()
        except Exception as ex:
            print(f"Error abrir_pago: {ex}")

    # ─── helpers ───────────────────────────────────────────────────

    def mostrar_alerta(self, texto):
        try:
            feedback(self.pagina, texto)
        except Exception as ex:
            print(f"Error mostrar_alerta: {ex}")
