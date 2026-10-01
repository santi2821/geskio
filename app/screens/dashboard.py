import calendar as pycal
from datetime import date, timedelta

import flet as ft
from datos import cli_por_id, cuentas, productos, stats, ventas
from screen_base import Pantalla
from theme import (
    ANCHO_BORDE,
    FS_12,
    FS_13,
    FS_14,
    ICON_MD,
    SP_4,
    SP_8,
    SP_12,
    colores,
    color_rol,
)
from widgets import (
    tarjeta_stat,
    Calendario,
    tarjeta_focal,
    encabezado,
    barras_ventas,
    seccion,
    grilla_stats,
    moneda,
)


def ventas_del_dia(lista_ventas, fecha_iso: str) -> list:
    return [v for v in (lista_ventas or []) if v.get("fecha") == fecha_iso]


def ventas_por_medio_del_dia(lista_ventas, fecha_iso: str) -> dict:
    totales = {medio: 0 for medio in ("efectivo", "transferencia", "fiado")}
    for venta in ventas_del_dia(lista_ventas, fecha_iso):
        medio = venta.get("pago")
        if medio in totales:
            totales[medio] += venta.get("total", 0) or 0
    return totales


def abonos_por_medio_del_dia(lista_cuentas, fecha_iso: str) -> dict:
    totales = {medio: 0 for medio in ("efectivo", "transferencia")}
    for cuenta in lista_cuentas or []:
        for abono in cuenta.get("abonos", []):
            medio = abono.get("medio_pago")
            if abono.get("fecha") == fecha_iso and medio in totales:
                totales[medio] += abono.get("monto", 0) or 0
    return totales


def totales_ultimos_7_dias(lista_ventas, hoy: date) -> list:
    totales: dict[str, float] = {}
    for v in lista_ventas or []:
        totales[v.get("fecha", "")] = totales.get(v.get("fecha", ""), 0) + (v.get("total", 0) or 0)
    serie = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        iso = dia.isoformat()
        serie.append((iso, totales.get(iso, 0)))
    return serie


def totales_mes(lista_ventas, anio: int, mes: int) -> dict:
    prefijo = f"{anio:04d}-{mes:02d}-"
    totales: dict[int, float] = {}
    for v in lista_ventas or []:
        fecha = v.get("fecha", "")
        if fecha.startswith(prefijo):
            try:
                dia = int(fecha[8:10])
            except (ValueError, IndexError):
                continue
            totales[dia] = totales.get(dia, 0) + (v.get("total", 0) or 0)
    return totales


class PantallaDashboard(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Dashboard")
        self.vista = "week"
        self.al_navegar = None

    def _ir_a(self, destino: str) -> None:
        if callable(self.al_navegar):
            self.al_navegar(destino)

    def _serie_calendario(self, vista: str) -> ft.Control:
        if vista == "day":
            return self._contenido_dia()
        if vista == "month":
            return self._contenido_mes()
        return self._contenido_semana()

    def _contenido_dia(self) -> ft.Control:
        paleta = colores.get()
        hoy_iso = date.today().isoformat()
        entradas = ventas_del_dia(ventas, hoy_iso)
        if not entradas:
            resumen_vacio = ventas_por_medio_del_dia(ventas, hoy_iso)
            pagos_vacios = abonos_por_medio_del_dia(cuentas, hoy_iso)
            return self._bloque_cobros_hoy(resumen_vacio, pagos_vacios, "Sin ventas hoy")
        filas: list[ft.Control] = []
        for v in entradas:
            cli = cli_por_id(v.get("cliente_id", ""))
            nombre = cli["nombre"] if cli else "Mostrador"
            detalle = f"{moneda(v.get('total', 0))} - {nombre} - {v.get('pago', '')}"
            filas.append(
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.RECEIPT_LONG,
                            color=paleta.text_soft,
                            size=ICON_MD,
                        ),
                        ft.Text(detalle, size=FS_14, color=paleta.text),
                    ],
                    spacing=SP_8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        resumen = ventas_por_medio_del_dia(ventas, hoy_iso)
        pagos = abonos_por_medio_del_dia(cuentas, hoy_iso)
        return ft.Column(
            [self._bloque_cobros_hoy(resumen, pagos), ft.Divider(), *filas],
            spacing=SP_8,
        )

    @staticmethod
    def _bloque_cobros_hoy(ventas_medio, abonos, encabezado_vacio=None):
        paleta = colores.get()
        lineas = []
        if encabezado_vacio:
            lineas.append(ft.Text(encabezado_vacio, size=FS_14, color=paleta.text_soft))
        lineas.append(ft.Text("Ventas de hoy por medio de pago", size=FS_14, weight=ft.FontWeight.BOLD))
        for medio, rotulo in (("efectivo", "Efectivo"), ("transferencia", "Transferencia"), ("fiado", "Fiado")):
            lineas.append(
                ft.Row(
                    [ft.Text(rotulo, size=FS_14), ft.Text(moneda(ventas_medio[medio]), size=FS_14)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        lineas.append(ft.Divider())
        lineas.append(ft.Text("Abonos de fiado recibidos hoy", size=FS_14, weight=ft.FontWeight.BOLD))
        for medio, rotulo in (("efectivo", "Efectivo"), ("transferencia", "Transferencia")):
            lineas.append(
                ft.Row(
                    [ft.Text(rotulo, size=FS_14), ft.Text(moneda(abonos[medio]), size=FS_14)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        return ft.Column(lineas, spacing=SP_4)

    def _contenido_semana(self) -> ft.Control:
        serie = totales_ultimos_7_dias(ventas, date.today())
        return barras_ventas(serie, hoy_iso=date.today().isoformat())

    def _contenido_mes(self) -> ft.Control:
        paleta = colores.get()
        hoy = date.today()
        totales = totales_mes(ventas, hoy.year, hoy.month)
        try:
            num_dias = pycal.monthrange(hoy.year, hoy.month)[1]
        except Exception:
            num_dias = 30
        hoy_iso = hoy.isoformat()
        celdas: list[ft.Control] = []
        for dia in range(1, num_dias + 1):
            iso = f"{hoy.year:04d}-{hoy.month:02d}-{dia:02d}"
            total = totales.get(dia, 0)
            es_hoy = iso == hoy_iso
            color_dia = paleta.on_accent_soft if es_hoy else paleta.text_muted
            color_total = paleta.on_accent_soft if es_hoy else paleta.text
            texto_total = moneda(total) if total else "-"
            celdas.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(str(dia), size=FS_12, color=color_dia),
                            ft.Text(texto_total, size=FS_12, color=color_total),
                        ],
                        spacing=SP_4,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=SP_8,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=paleta.accent_soft if es_hoy else paleta.surface,
                    border=ft.Border.all(
                        ANCHO_BORDE,
                        paleta.primary if es_hoy else paleta.border,
                    ),
                    border_radius=ft.BorderRadius.all(SP_4),
                    col={"xs": 4, "sm": 3, "md": 2},
                )
            )
        return ft.ResponsiveRow(celdas, spacing=SP_8, run_spacing=SP_8)

    def _armar_alertas(self) -> ft.Column:
        paleta = colores.get()
        peligro = color_rol(paleta, "deben")
        ok = color_rol(paleta, "paid")
        alertas = []
        for p in productos:
            if p["stock"] <= p["minimo"]:
                alertas.append(
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.INVENTORY_2,
                                color=peligro,
                                size=ICON_MD,
                            ),
                            ft.Text(
                                f"{p['nombre']}: stock {p['stock']} (mínimo {p['minimo']})",
                                size=FS_14,
                                color=paleta.text,
                            ),
                        ],
                        spacing=SP_8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
        for c in cuentas:
            pendiente = c["total"] - c["pagado"]
            if pendiente > 0:
                cli = cli_por_id(c["cliente_id"])
                alertas.append(
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.ACCOUNT_BALANCE_WALLET,
                                color=peligro,
                                size=ICON_MD,
                            ),
                            ft.Text(
                                f"{cli['nombre'] if cli else '?'} debe {moneda(pendiente)}",
                                size=FS_14,
                                color=paleta.text,
                            ),
                        ],
                        spacing=SP_8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
        if not alertas:
            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ok, size=ICON_MD),
                            ft.Text("Todo en orden", size=FS_14, color=paleta.text),
                        ],
                        spacing=SP_8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                spacing=SP_8,
            )

        total_alertas = len(alertas)
        visibles = alertas[:4]
        resumen = ft.Text(
            f"{total_alertas} alertas"
            + (f" · mostrando {len(visibles)}" if total_alertas > len(visibles) else ""),
            size=FS_13,
            color=paleta.text_muted,
        )
        accesos = ft.Row(
            [
                ft.TextButton(
                    "Ver stock",
                    icon=ft.Icons.INVENTORY_2,
                    on_click=lambda _: self._ir_a("stock"),
                ),
                ft.TextButton(
                    "Ver fiado",
                    icon=ft.Icons.ACCOUNT_BALANCE_WALLET,
                    on_click=lambda _: self._ir_a("fiado"),
                ),
            ],
            spacing=SP_4,
            wrap=True,
        )
        return ft.Column([resumen, *visibles, accesos], spacing=SP_8)

    def build(self):
        resumen = stats()
        focal_hoy = tarjeta_focal("Hoy", moneda(resumen["hoy"]), rol="text", icono=ft.Icons.TODAY)
        tarjeta_mes = tarjeta_stat(
            "Ventas del mes",
            moneda(resumen["mes"]),
            rol="accent_text",
            icono=ft.Icons.CALENDAR_MONTH,
        )
        tarjeta_ganancia = tarjeta_stat(
            "Margen registrado del mes",
            moneda(resumen["ganancia"]),
            rol="success" if resumen["ganancia"] >= 0 else "danger_text",
            icono=ft.Icons.TRENDING_UP,
        )
        tarjeta_deben = tarjeta_stat(
            "Por cobrar",
            moneda(resumen["deben"]),
            rol="danger_text",
            icono=ft.Icons.RECEIPT_LONG,
        )

        seccion_alertas = seccion("Alertas", self._armar_alertas())
        try:
            seccion_alertas.col = {"xs": 12, "xl": 4}
        except Exception:
            pass
        self.calendario = Calendario(
            obtener_serie=self._serie_calendario,
            hoy=date.today().isoformat(),
            vista=self.vista,
            al_cambiar=self._fijar_vista,
        )
        try:
            self.calendario.col = {"xs": 12, "xl": 8}
        except Exception:
            pass
        fila_stats = grilla_stats(
            focal=focal_hoy, tarjetas=[tarjeta_mes, tarjeta_ganancia, tarjeta_deben]
        )
        fila_contenido = ft.ResponsiveRow(
            [self.calendario, seccion_alertas],
            spacing=SP_12,
            run_spacing=SP_12,
            breakpoints={
                "xs": 0,
                "sm": 576,
                "md": 768,
                "lg": 992,
                "xl": 1200,
                "xxl": 1400,
            },
        )

        return ft.Container(
            content=ft.Column(
                [
                    encabezado(
                        "Resumen de ventas",
                        al_refrescar=lambda _: self.actualizar(),
                        descripcion="Un vistazo a ventas, margen y pendientes del negocio.",
                    ),
                    fila_stats,
                    ft.Text(
                        (
                            f"Excluye {resumen.get('ventas_sin_costo', 0)} ventas antiguas "
                            "sin costo registrado."
                            if resumen.get("ventas_sin_costo", 0)
                            else "Usa el costo guardado al momento de cada venta."
                        ),
                        size=FS_12,
                        color=colores.get().text_muted,
                    ),
                    fila_contenido,
                ],
                spacing=SP_12,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
        )

    def _fijar_vista(self, vista: str) -> None:
        self.vista = vista
