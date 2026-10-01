"""Behavior checks for the sales, cashier, onboarding, debt, and stock improvements."""

from copy import deepcopy
from datetime import date, timedelta
from unittest.mock import Mock

import datos
from screens.caja import PantallaCaja
from screens.dashboard import abonos_por_medio_del_dia, ventas_por_medio_del_dia
from screens.historial_ventas import PantallaHistorialVentas, filtrar_ventas
from screens.movimientos_stock import PantallaMovimientosStock


def test_migration_v2_preserves_paid_balance_without_inventing_abonos():
    legacy = deepcopy(datos._estado_actual())
    cuenta = legacy["cuentas"][0]
    cuenta["pagado"] = 250
    cuenta.pop("abonos", None)
    cuenta.pop("pagado_sin_detalle", None)
    legacy.pop("inicio")
    legacy.pop("movimientos_stock")
    legacy["version"] = 2

    migrado, cambio = datos._migrar_estado(legacy)

    assert cambio is True
    assert migrado["version"] == 3
    assert migrado["cuentas"][0]["pagado"] == 250
    assert migrado["cuentas"][0]["pagado_sin_detalle"] == 250
    assert migrado["cuentas"][0]["abonos"] == []
    datos._validar_estado(migrado)


def test_payment_adds_a_dated_method_and_preserves_account_totals():
    cuenta = datos.cuentas[0]
    pagado = cuenta["pagado"]
    pendiente = cuenta["total"] - pagado
    datos.pagar_fiado(cuenta["id"], 100, "transferencia")

    assert cuenta["pagado"] == pagado + 100
    assert cuenta["total"] - cuenta["pagado"] == pendiente - 100
    assert cuenta["abonos"][-1] == {
        "id": cuenta["abonos"][-1]["id"],
        "fecha": date.today().isoformat(),
        "monto": 100,
        "medio_pago": "transferencia",
    }
    datos._validar_estado({"version": datos._VERSION_ESTADO, **deepcopy(datos._estado_actual())})


def test_stock_ledger_records_manual_sale_and_reversal():
    producto = datos.productos[0]
    antes = producto["stock"]
    datos.ajustar_stock(producto["id"], 2, "Reposición semanal")
    movimiento = datos.movimientos_stock[-1]
    assert (movimiento["tipo"], movimiento["anterior"], movimiento["nuevo"]) == (
        "ajuste", antes, antes + 2
    )
    assert movimiento["motivo"] == "Reposición semanal"

    venta = datos.crear_venta(
        [{"prod_id": producto["id"], "nombre": producto["nombre"], "cantidad": 1, "precio": producto["precio"]}]
    )
    assert datos.movimientos_stock[-1]["tipo"] == "venta"
    assert datos.deshacer_venta(venta["id"]) is True
    assert datos.movimientos_stock[-1]["tipo"] == "anulacion"
    assert producto["stock"] == antes + 2
    datos._validar_estado({"version": datos._VERSION_ESTADO, **deepcopy(datos._estado_actual())})


def test_new_empty_commerce_choice_is_saved_once():
    datos.COMERCIO_INICIALIZADO = False
    datos.iniciar_comercio("vacio")

    assert datos.COMERCIO_INICIALIZADO is True
    assert datos.MODO_COMERCIO == "vacio"
    assert datos.productos == []
    assert datos.clientes == []
    assert datos.ventas == []
    assert datos.RUTA_ARCHIVO_DATOS.exists()
    estado = datos.leer_respaldo(datos.RUTA_ARCHIVO_DATOS.read_bytes())
    assert estado["inicio"] == {"seleccionado": True, "modo": "vacio"}


def test_cashier_rejects_accumulated_oversell_and_computes_change(monkeypatch):
    pantalla = PantallaCaja(Mock())
    pantalla.build()
    pantalla._zona_carrito.update = Mock()
    pantalla.texto_total.update = Mock()
    pantalla.texto_items.update = Mock()
    pantalla.texto_vuelto.update = Mock()
    producto = datos.productos[0]
    producto["stock"] = 5
    avisos = []
    monkeypatch.setattr(pantalla, "mostrar_alerta", avisos.append)
    pantalla.combo_producto.value = producto["id"]
    pantalla.campo_cantidad.value = "3"
    pantalla.agregar_item()
    pantalla.campo_cantidad.value = "3"
    pantalla.agregar_item()
    assert pantalla.items_carrito[0]["cantidad"] == 3
    assert "Solo quedan 2" in avisos[-1]
    pantalla.cambiar_cantidad(0, -1)

    avisos_ui = {}
    monkeypatch.setattr(
        "screens.caja.aviso",
        lambda _pagina, mensaje, texto_accion, al_accion: avisos_ui.update(
            mensaje=mensaje, accion=texto_accion, al_accion=al_accion
        ),
    )
    pantalla.campo_recibido.value = "5000"
    pantalla.cobrar_carrito()
    assert "Vuelto $1.400" in avisos_ui["mensaje"]


def test_sales_history_filters_and_daily_payment_summaries():
    hoy = date.today()
    lista = [
        {"id": "hoy-a", "fecha": hoy.isoformat(), "cliente_id": "", "pago": "efectivo", "total": 100},
        {"id": "hoy-b", "fecha": hoy.isoformat(), "cliente_id": "", "pago": "fiado", "total": 300},
        {"id": "ayer", "fecha": (hoy - timedelta(days=1)).isoformat(), "cliente_id": "", "pago": "transferencia", "total": 200},
    ]
    filtradas = filtrar_ventas(lista, "7dias", "efectivo", "Mostrador", hoy=hoy)
    assert [venta["id"] for venta in filtradas] == ["hoy-a"]
    assert ventas_por_medio_del_dia(lista, hoy.isoformat()) == {
        "efectivo": 100, "transferencia": 0, "fiado": 300
    }
    assert abonos_por_medio_del_dia(
        [{"abonos": [
            {"fecha": hoy.isoformat(), "medio_pago": "efectivo", "monto": 50},
            {"fecha": hoy.isoformat(), "medio_pago": "transferencia", "monto": 75},
        ]}],
        hoy.isoformat(),
    ) == {"efectivo": 50, "transferencia": 75}


def test_new_sales_and_movement_screens_render():
    for pantalla in (PantallaHistorialVentas(Mock()), PantallaMovimientosStock(Mock())):
        assert pantalla.build() is not None
