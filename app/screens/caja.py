import math

import flet as ft
from screen_base import Pantalla
from datos import productos, clientes, crear_venta, deshacer_venta, prod_por_id
from theme import (
    ANCHO_BORDE,
    CARRITO_ALTO_MAX,
    CARRITO_ALTO_MIN,
    CARRITO_ALTO_POR_ITEM,
    FS_12,
    FS_13,
    FS_14,
    FS_16,
    FS_20,
    FS_36,
    ICON_SM,
    R_SM,
    SP_4,
    SP_8,
    SP_10,
    SP_12,
    colores,
)
from widgets import (
    campo_texto,
    selector,
    encabezado,
    seccion,
    confirmar_eliminar,
    aviso,
    moneda,
    leer_texto,
    sincronizar_combo,
    sincronizar_texto,
)


class PantallaCaja(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Caja")
        self.items_carrito = []
        self._ultimo_cid = ""
        self._ultimo_pago = "efectivo"

    def actualizar(self):
        self.cargar_opciones()
        self.actualizar_carrito()

    def cargar_opciones(self):
        ids_clientes = {c["id"] for c in clientes}
        cliente_actual = self._ultimo_cid or self.combo_cliente.value or ""
        if cliente_actual and cliente_actual not in ids_clientes:
            self._ultimo_cid = ""
            self.combo_cliente.value = None
        self.combo_cliente.options = self._opciones_clientes()
        self.combo_producto.options = self._opciones_productos()
        for combo in (self.combo_cliente, self.combo_producto):
            try:
                combo.update()
            except Exception:
                pass

    @staticmethod
    def _opciones_clientes():
        return [ft.dropdown.Option("", "— Mostrador —")] + [
            ft.dropdown.Option(c["id"], c["nombre"]) for c in clientes
        ]

    @staticmethod
    def _opciones_productos():
        return [
            ft.dropdown.Option(
                p["id"],
                f"{p['nombre']} ({moneda(p['precio'])} — stock: {p['stock']})",
            )
            for p in productos
            if p["stock"] > 0
        ]

    def build(self):
        paleta = colores.get()
        ids_clientes = {c["id"] for c in clientes}
        if self._ultimo_cid and self._ultimo_cid not in ids_clientes:
            self._ultimo_cid = ""
        self.combo_cliente = selector(
            label="Cliente",
            hint_text="Mostrador",
            expand=True,
            value=self._ultimo_cid or None,
            options=self._opciones_clientes(),
            on_select=self.al_cambio_cliente,
        )
        sincronizar_combo(self.combo_cliente)
        self.combo_pago = selector(
            label="Pago",
            value=self._ultimo_pago or "efectivo",
            expand=True,
            on_select=self.al_cambio_pago,
            options=[
                ft.dropdown.Option("efectivo", "Efectivo"),
                ft.dropdown.Option("transferencia", "Transferencia"),
                ft.dropdown.Option("fiado", "Fiado"),
            ],
        )
        sincronizar_combo(self.combo_pago)
        self.combo_producto = selector(
            label="Producto",
            expand=True,
            options=self._opciones_productos(),
            on_select=self.al_cambio_producto,
        )
        sincronizar_combo(self.combo_producto)
        self.campo_cantidad = campo_texto(
            label="Cantidad",
            value="1",
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        sincronizar_texto(self.campo_cantidad)
        self.campo_recibido = campo_texto(
            label="Recibido ($)",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        sincronizar_texto(self.campo_recibido)
        self.campo_recibido.on_change = self._al_cambio_recibido
        self.campo_recibido.visible = self._ultimo_pago == "efectivo"

        self._zona_carrito = ft.ListView(
            height=CARRITO_ALTO_MIN,
            spacing=SP_4,
            auto_scroll=True,
        )
        self._pintar_carrito()
        t = sum(i["precio"] * i["cantidad"] for i in self.items_carrito)
        self.texto_total = ft.Text(
            moneda(t), size=FS_36, weight=ft.FontWeight.BOLD, color=paleta.success
        )
        self.texto_items = ft.Text(
            f"{len(self.items_carrito)} items", size=FS_13, color=paleta.text_muted
        )
        self.texto_vuelto = ft.Text(
            "Si lo dejás vacío, se registra pago exacto.",
            size=FS_13,
            color=paleta.text_muted,
        )

        self.combo_cliente.col = {"xs": 12, "sm": 6}
        self.combo_pago.col = {"xs": 12, "sm": 6}
        self.combo_producto.col = {"xs": 12, "sm": 7}
        self.campo_cantidad.col = {"xs": 12, "sm": 2}
        boton_agregar = ft.FilledButton(
            "Agregar",
            icon=ft.Icons.ADD,
            on_click=self.agregar_item,
            style=ft.ButtonStyle(
                bgcolor=paleta.primary,
                color=paleta.on_primary,
                shape=ft.RoundedRectangleBorder(radius=R_SM),
            ),
        )
        boton_agregar.col = {"xs": 12, "sm": 3}
        form_venta = ft.Column(
            [
                ft.ResponsiveRow(
                    [self.combo_cliente, self.combo_pago],
                    columns=12,
                    spacing=SP_12,
                    run_spacing=SP_8,
                ),
                ft.ResponsiveRow(
                    [self.combo_producto, self.campo_cantidad, boton_agregar],
                    columns=12,
                    spacing=SP_12,
                    run_spacing=SP_8,
                ),
            ],
            spacing=SP_8,
        )
        seccion_venta = seccion("Venta", form_venta)

        encabezado_carrito = ft.Row(
            [
                self.texto_items,
                ft.Container(expand=True),
                ft.TextButton(
                    "Vaciar",
                    icon=ft.Icons.DELETE_SWEEP,
                    on_click=self.vaciar_carrito,
                ),
            ]
        )
        cuerpo_carrito = ft.Column(
            [encabezado_carrito, self._zona_carrito],
            spacing=SP_8,
        )
        seccion_carrito = seccion("Carrito", cuerpo_carrito)

        fila_total = ft.Row(
            [
                ft.Text(
                    "TOTAL",
                    size=FS_20,
                    weight=ft.FontWeight.BOLD,
                    color=paleta.text,
                ),
                self.texto_total,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        boton_cobrar = ft.FilledButton(
            "Cobrar",
            on_click=self.cobrar_carrito,
            expand=True,
            style=ft.ButtonStyle(
                bgcolor=paleta.primary,
                color=paleta.on_primary,
                shape=ft.RoundedRectangleBorder(radius=R_SM),
                padding=ft.Padding.symmetric(horizontal=SP_12, vertical=SP_12),
            ),
        )
        cierre = ft.Column(
            [
                fila_total,
                self.campo_recibido,
                self.texto_vuelto,
                ft.Row([boton_cobrar], expand=True),
            ],
            spacing=SP_8,
        )

        return ft.Column(
            [
                encabezado(
                    "Nueva venta",
                    al_refrescar=lambda _: self.actualizar(),
                    descripcion="Registrá productos, revisá el total y cobrá la venta.",
                ),
                seccion_venta,
                seccion_carrito,
                cierre,
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def al_cambio_producto(self, e):
        """Guarda el id del producto elegido en el combo."""
        try:
            pid = e.data if e.data else e.control.value
            if pid:
                self._ultimo_pid = pid
        except Exception as ex:
            print(f"Error al_cambio_producto: {ex}")

    def al_cambio_cliente(self, e):
        try:
            cid = getattr(e, "data", None) or getattr(getattr(e, "control", None), "value", "")
            self._ultimo_cid = cid or ""
        except Exception as ex:
            print(f"Error al_cambio_cliente: {ex}")

    def al_cambio_pago(self, e):
        try:
            pago = getattr(e, "data", None) or getattr(getattr(e, "control", None), "value", "")
            if pago:
                self._ultimo_pago = pago
            if hasattr(self, "campo_recibido"):
                self.campo_recibido.visible = self._ultimo_pago == "efectivo"
                self.campo_recibido.update()
                self._actualizar_vuelto()
        except Exception as ex:
            print(f"Error al_cambio_pago: {ex}")


    def _total_carrito(self):
        return sum(i["precio"] * i["cantidad"] for i in self.items_carrito)

    def _actualizar_vuelto(self, e=None):
        if not hasattr(self, "texto_vuelto"):
            return
        if self._ultimo_pago != "efectivo":
            self.texto_vuelto.value = "El vuelto solo aplica a pagos en efectivo."
        else:
            recibido = leer_texto(getattr(self, "campo_recibido", None), e).strip()
            if not recibido:
                self.texto_vuelto.value = "Si lo dejás vacío, se registra pago exacto."
            else:
                try:
                    monto = float(recibido.replace("$", "").replace(" ", "").replace(",", "."))
                    total = self._total_carrito()
                    if not math.isfinite(monto):
                        self.texto_vuelto.value = "Importe inválido. Escribí un número."
                    elif monto < total:
                        self.texto_vuelto.value = (
                            f"Faltan {moneda(total - monto)} para completar el pago."
                        )
                    else:
                        self.texto_vuelto.value = f"Vuelto: {moneda(monto - total)}"
                except (TypeError, ValueError):
                    self.texto_vuelto.value = "Importe inválido. Escribí un número."
        try:
            self.texto_vuelto.update()
        except Exception:
            pass

    def _al_cambio_recibido(self, e):
        dato = getattr(e, "data", None)
        if dato is not None:
            self.campo_recibido.value = dato
        self._actualizar_vuelto(e)

    def _pintar_carrito(self):
        try:
            paleta = colores.get()
            controles = []
            for i, item in enumerate(self.items_carrito):
                st = item["precio"] * item["cantidad"]
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
                                            color=paleta.text,
                                        ),
                                        ft.Text(
                                            f"{moneda(item['precio'])} x {item['cantidad']}",
                                            size=FS_12,
                                            color=paleta.text_muted,
                                        ),
                                    ],
                                    spacing=SP_4,
                                    expand=True,
                                ),
                                ft.Text(
                                    moneda(st),
                                    size=FS_16,
                                    weight=ft.FontWeight.BOLD,
                                    color=paleta.text,
                                ),
                                ft.IconButton(
                                    ft.Icons.REMOVE,
                                    tooltip=f"Quitar una unidad de {item['nombre']}",
                                    on_click=lambda _, n=idx: self.cambiar_cantidad(n, -1),
                                ),
                                ft.IconButton(
                                    ft.Icons.ADD,
                                    tooltip=f"Agregar una unidad de {item['nombre']}",
                                    on_click=lambda _, n=idx: self.cambiar_cantidad(n, 1),
                                ),
                                ft.IconButton(
                                    ft.Icons.CLOSE,
                                    icon_size=ICON_SM,
                                    icon_color=paleta.danger,
                                    tooltip=f"Quitar {item['nombre']} del carrito",
                                    on_click=lambda _, n=idx: self.quitar_item(n),
                                ),
                            ]
                        ),
                        padding=ft.Padding.symmetric(vertical=SP_4, horizontal=SP_4),
                        border=ft.Border(bottom=ft.BorderSide(ANCHO_BORDE, paleta.border)),
                    )
                )
            if not controles:
                controles.append(
                    ft.Text(
                        "Agregá productos desde arriba",
                        size=FS_14,
                        color=paleta.text_muted,
                    )
                )
            self._zona_carrito.controls = controles
            self._zona_carrito.height = max(
                CARRITO_ALTO_MIN,
                min(CARRITO_ALTO_MAX, len(self.items_carrito) * CARRITO_ALTO_POR_ITEM),
            )
        except Exception as ex:
            print(f"Error pintar_carrito: {ex}")

    def actualizar_carrito(self):
        self._pintar_carrito()
        try:
            self._zona_carrito.update()
            t = self._total_carrito()
            self.texto_total.value = moneda(t)
            self.texto_total.update()
            self.texto_items.value = f"{len(self.items_carrito)} items"
            self.texto_items.update()
            self._actualizar_vuelto()
        except Exception as ex:
            print(f"Error actualizar_carrito: {ex}")

    def quitar_item(self, i):
        try:
            idx = int(i)
            if 0 <= idx < len(self.items_carrito):
                self.items_carrito.pop(idx)
                self.actualizar_carrito()
        except (TypeError, ValueError) as ex:
            print(f"Error quitar_item: {ex}")

    def cambiar_cantidad(self, i, delta):
        try:
            idx = int(i)
            item = self.items_carrito[idx]
            nueva = item["cantidad"] + int(delta)
            if nueva <= 0:
                self.quitar_item(idx)
                return
            if delta > 0:
                otro = sum(
                    fila["cantidad"]
                    for posicion, fila in enumerate(self.items_carrito)
                    if posicion != idx and fila["prod_id"] == item["prod_id"]
                )
                producto = prod_por_id(item["prod_id"])
                disponible = producto["stock"] - otro if producto else 0
                if nueva > disponible:
                    self.mostrar_alerta(
                        f"Solo quedan {max(0, disponible - item['cantidad'])} unidades disponibles"
                    )
                    return
            item["cantidad"] = nueva
            self.actualizar_carrito()
        except (IndexError, TypeError, ValueError):
            return

    def vaciar_carrito(self, e=None):
        try:

            def _confirmar(e=None):
                try:
                    self.items_carrito.clear()
                    self.actualizar_carrito()
                except Exception as ex:
                    print(f"Error vaciar_carrito: {ex}")

            confirmar_eliminar(
                self.pagina,
                _confirmar,
                titulo="Vaciar carrito",
                mensaje="¿Vaciar el carrito? Se quitarán todos los items.",
                nombre="",
            )
        except Exception as ex:
            print(f"Error vaciar_carrito: {ex}")

    def agregar_item(self, e=None):
        try:
            pid = self.combo_producto.value
            if not pid and hasattr(self, "_ultimo_pid"):
                pid = self._ultimo_pid

            if not pid:
                self.mostrar_alerta("Seleccioná un producto")
                return

            prod = prod_por_id(pid)
            if not prod:
                self.mostrar_alerta(f"Producto no encontrado (ID: {pid})")
                return

            try:
                cantidad = int((leer_texto(self.campo_cantidad, e) or "1").strip())
            except (TypeError, ValueError, AttributeError):
                self.mostrar_alerta("Cantidad inválida")
                return

            if cantidad <= 0:
                self.mostrar_alerta("Cantidad inválida")
                return

            existente = next((x for x in self.items_carrito if x["prod_id"] == pid), None)
            cantidad_nueva = (existente["cantidad"] if existente else 0) + cantidad
            if cantidad_nueva > prod["stock"]:
                disponible = max(0, prod["stock"] - (existente["cantidad"] if existente else 0))
                mensaje = (
                    f"Solo quedan {disponible} unidades disponibles de {prod['nombre']}"
                    if existente
                    else f"Solo hay {prod['stock']} en stock"
                )
                self.mostrar_alerta(mensaje)
                return
            if existente:
                existente["cantidad"] += cantidad
            else:
                self.items_carrito.append(
                    {
                        "prod_id": pid,
                        "nombre": prod["nombre"],
                        "cantidad": cantidad,
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
                self.mostrar_alerta("Carrito vacío")
                return
            pago = self._ultimo_pago or self.combo_pago.value or "efectivo"
            cid = self._ultimo_cid or self.combo_cliente.value or ""
            if pago == "fiado" and not cid:
                self.mostrar_alerta("Elegí un cliente para fiado")
                return

            for item in self.items_carrito:
                p = prod_por_id(item["prod_id"])
                if not p:
                    self.mostrar_alerta(
                        f"{item['nombre']} ya no existe en Stock. Quitalo del carrito."
                    )
                    return
                if not math.isclose(
                    float(item["precio"]), float(p["precio"]), rel_tol=1e-9, abs_tol=1e-9
                ):
                    self.mostrar_alerta(
                        f"Cambió el precio de {p['nombre']}. Quitalo y agregalo nuevamente para revisar el precio actual."
                    )
                    return
                if p["stock"] < item["cantidad"]:
                    self.mostrar_alerta(
                        f"Stock insuficiente de {item['nombre']}: quedan {p['stock']}"
                    )
                    return

            total = self._total_carrito()
            recibido = total
            if pago == "efectivo":
                texto_recibido = leer_texto(self.campo_recibido).strip()
                if texto_recibido:
                    try:
                        recibido = float(
                            texto_recibido.replace("$", "").replace(" ", "").replace(",", ".")
                        )
                    except (TypeError, ValueError):
                        self.mostrar_alerta("Importe recibido inválido")
                        return
                    if not math.isfinite(recibido) or recibido < total:
                        self.mostrar_alerta(
                            f"El importe recibido debe cubrir el total ({moneda(total)})"
                        )
                        return
            try:
                v = crear_venta(list(self.items_carrito), cid, pago)
            except ValueError as ex:
                self.mostrar_alerta(str(ex))
                return
            self.items_carrito.clear()
            if hasattr(self, "campo_recibido"):
                self.campo_recibido.value = ""
            self.actualizar_carrito()
            self.cargar_opciones()
            etiquetas_pago = {
                "efectivo": "Efectivo",
                "transferencia": "Transferencia",
                "fiado": "Fiado",
            }

            def _deshacer(e=None):
                try:
                    deshacer_venta(v["id"])
                    self.cargar_opciones()
                    self.actualizar_carrito()
                    self.mostrar_alerta("Venta deshecha")
                except Exception as ex:
                    print(f"Error deshacer_venta: {ex}")

            aviso(
                self.pagina,
                (
                    f"Cobrado {moneda(total)} — Efectivo · Vuelto {moneda(recibido - total)}"
                    if pago == "efectivo" and recibido > total
                    else f"Cobrado {moneda(total)} — {etiquetas_pago.get(pago, pago)}"
                ),
                texto_accion="Deshacer",
                al_accion=_deshacer,
            )
        except Exception as ex:
            print(f"Error cobrar_carrito: {ex}")
            self.mostrar_alerta(f"Error al cobrar: {ex}")
