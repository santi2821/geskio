from datetime import date
import flet as ft
from screen_base import Screen
from datos import cuentas, cli_por_id, pagar_fiado
from theme import (
    ICON_SM,
    SP_4,
    SP_8,
    SP_10,
    SP_12,
    app_colors,
    role_color,
)
from widgets import (
    AppDialog,
    AppTable,
    PageHeader,
    TablePager,
    TableToolbar,
    feedback,
    paginate_rows,
    sync_text,
)


class PantallaFiado(Screen):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Fiado")
        self._query = ""
        self._solo_pendientes = True
        self._page = 1

    def actualizar(self):
        self.cargar_cuentas()

    def build(self):
        self.filtro_pendientes = ft.Switch(
            label="Solo pendientes",
            value=self._solo_pendientes,
            on_change=lambda _: self._on_filtro(),
        )
        toolbar = TableToolbar(
            on_query=self._on_query,
            chips=(self.filtro_pendientes,),
            search_hint="Buscar cliente...",
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
        self._pager_holder = ft.Column([], spacing=SP_8)

        return ft.Column(
            [
                PageHeader("Fiado", on_refresh=lambda _: self.cargar_cuentas()),
                toolbar,
                self._tabla_holder,
                self._pager_holder,
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    # ─── toolbar + pager ────────────────────────────────────────────

    def _on_query(self, query):
        self._query = query or ""
        self._page = 1
        self.cargar_cuentas()

    def _on_filtro(self):
        try:
            self._solo_pendientes = bool(self.filtro_pendientes.value)
        except Exception:
            self._solo_pendientes = True
        self._page = 1
        self.cargar_cuentas()

    def _on_page(self, new_page):
        try:
            self._page = max(1, int(new_page or 1))
        except (TypeError, ValueError):
            self._page = 1
        self.cargar_cuentas()

    def cargar_cuentas(self):
        try:
            palette = app_colors.get()
            pagado_color = role_color(palette, "paid")
            pendiente_color = role_color(palette, "due")
            vencido_color = role_color(palette, "danger_text")
            solo_pendientes = bool(getattr(self, "_solo_pendientes", True))
            q = (getattr(self, "_query", "") or "").lower()
            entries = []
            for c in cuentas:
                p = c["total"] - c["pagado"]
                if solo_pendientes and p <= 0:
                    continue
                cli = cli_por_id(c["cliente_id"])
                nombre = cli["nombre"] if cli else "?"
                if q and q not in nombre.lower():
                    continue
                dias = (
                    (date.today() - date.fromisoformat(c["created_at"])).days
                    if c.get("created_at")
                    else 0
                )
                entries.append((dias, c, nombre, p))
            entries.sort(key=lambda item: item[0], reverse=True)
            filas = []
            for dias, c, nombre, p in entries:
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
            page = int(getattr(self, "_page", 1) or 1)
            visibles, current, total = paginate_rows(filas, page)
            self._page = current
            self._tabla_holder.controls = [
                AppTable(
                    self._columnas, visibles, empty_message="Sin deudas pendientes"
                )
            ]
            self._pager_holder.controls = [
                TablePager(current, total, on_page=self._on_page)
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
