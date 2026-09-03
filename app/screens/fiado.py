from datetime import date
import flet as ft
from screen_base import Screen
from datos import cuentas, cli_por_id, pagar_fiado


class PantallaFiado(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Cuenta Corriente")

    def actualizar(self):
        self.cargar_cuentas()

    def build(self):
        self.filtro_pendientes = ft.Switch(label="Solo pendientes", value=True, on_change=lambda e: self.cargar_cuentas())

        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Total")),
                ft.DataColumn(ft.Text("Pagado")),
                ft.DataColumn(ft.Text("Pendiente")),
                ft.DataColumn(ft.Text("Dias")),
                ft.DataColumn(ft.Text("")),
            ],
            column_spacing=12,
            expand=True,
        )

        tabla_scroll = ft.Container(
            content=ft.Row([self.tabla_datos], scroll=ft.ScrollMode.AUTO, expand=True),
            expand=True,
        )

        return ft.Column([
            ft.Text("Cuenta Corriente", size=30, weight=ft.FontWeight.BOLD),
            self.filtro_pendientes,
            ft.Divider(height=4),
            tabla_scroll,
            ft.ElevatedButton("Refrescar", on_click=lambda _: self.cargar_cuentas()),
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def cargar_cuentas(self):
        try:
            solo_pendientes = self.filtro_pendientes.value
            filas = []
            for c in cuentas:
                p = c["total"] - c["pagado"]
                if solo_pendientes and p <= 0:
                    continue
                cli = cli_por_id(c["cliente_id"])
                nombre = cli["nombre"] if cli else "?"
                dias = (date.today() - date.fromisoformat(c["created_at"])).days if c.get("created_at") else 0
                ccid = c["id"]

                estado_color = ft.Colors.GREEN if p <= 0 else (ft.Colors.RED if dias > 30 else ft.Colors.AMBER)

                filas.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nombre, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(f"${c['total']:,}")),
                    ft.DataCell(ft.Text(f"${c['pagado']:,}")),
                    ft.DataCell(ft.Text(f"${p:,}", color=estado_color, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(f"{dias}d")),
                    ft.DataCell(
                        ft.ElevatedButton("Pagar", on_click=lambda _, x=ccid: self.abrir_pago(x))
                        if p > 0 else ft.Text("✔", color=ft.Colors.GREEN)
                    ),
                ]))
            if not filas:
                filas.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Sin deudas 🎉", color=ft.Colors.GREEN, italic=True)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]))
            self.tabla_datos.rows = filas
        except Exception as ex:
            print(f"Error cargar_cuentas: {ex}")
        self.pagina.update()

    def abrir_pago(self, ccid):
        try:
            c = next((x for x in cuentas if x["id"] == ccid), None)
            if not c:
                return
            d = c["total"] - c["pagado"]
            campo_monto = ft.TextField(label="Monto $", value=str(d), keyboard_type=ft.KeyboardType.NUMBER)

            def confirmar(e):
                try:
                    m = float(campo_monto.value or 0)
                    if m > 0:
                        pagar_fiado(ccid, m)
                    self.cerrar_dialogo(dialogo)
                    self.cargar_cuentas()
                except Exception as ex:
                    print(f"Error confirmar pago: {ex}")

            def cancelar(e):
                try:
                    self.cerrar_dialogo(dialogo)
                except Exception as ex:
                    print(f"Error cancelar: {ex}")

            dialogo = ft.AlertDialog(
                modal=True,
                open=False,
                shape=ft.RoundedRectangleBorder(radius=16),
                title=ft.Text("Registrar pago"),
                content=ft.Column([
                    ft.Text(f"Debe ${d:,} de ${c['total']:,}"),
                    campo_monto,
                ], spacing=12, tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.ElevatedButton("Pagar", on_click=confirmar),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.abrir_dialogo(dialogo)
        except Exception as ex:
            print(f"Error abrir_pago: {ex}")
