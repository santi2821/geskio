from unittest.mock import Mock

import datos
from screens import caja as modulo_caja
from screens.caja import PantallaCaja
from theme import CARRITO_ALTO_MIN


def _caja_lista():
    pantalla = PantallaCaja(Mock())
    pantalla.build()
    pantalla._zona_carrito.update = Mock()
    pantalla.texto_total.update = Mock()
    pantalla.texto_items.update = Mock()
    return pantalla


def _mensaje(pantalla):
    return pantalla.pagina.snack_bar.content.value


def test_caja_agrega_acumula_y_quita_productos_del_carrito():
    pantalla = _caja_lista()
    producto = datos.productos[0]
    pantalla.combo_producto.value = producto["id"]
    pantalla.campo_cantidad.value = "2"

    pantalla.agregar_item()

    assert pantalla.items_carrito == [
        {
            "prod_id": producto["id"],
            "nombre": producto["nombre"],
            "cantidad": 2,
            "precio": producto["precio"],
        }
    ]
    assert pantalla.texto_total.value == modulo_caja.moneda(producto["precio"] * 2)
    assert pantalla.texto_items.value == "1 items"
    assert pantalla._zona_carrito.height == CARRITO_ALTO_MIN

    pantalla.campo_cantidad.value = "1"
    pantalla.agregar_item()
    assert pantalla.items_carrito[0]["cantidad"] == 3
    assert pantalla._zona_carrito.height == CARRITO_ALTO_MIN

    pantalla.quitar_item(0)
    assert pantalla.items_carrito == []
    assert pantalla.texto_total.value == "$0"
    assert pantalla.texto_items.value == "0 items"


def test_caja_informa_producto_y_cantidad_invalidos_sin_alterar_carrito():
    pantalla = _caja_lista()
    pantalla.agregar_item()
    assert _mensaje(pantalla) == "Seleccioná un producto"

    producto = datos.productos[0]
    pantalla.combo_producto.value = producto["id"]
    pantalla.campo_cantidad.value = "0"
    pantalla.agregar_item()
    assert _mensaje(pantalla) == "Cantidad inválida"

    pantalla.campo_cantidad.value = str(producto["stock"] + 1)
    pantalla.agregar_item()
    assert _mensaje(pantalla) == f"Solo hay {producto['stock']} en stock"
    assert pantalla.items_carrito == []


def test_caja_rechaza_precio_obsoleto_y_fiado_sin_cliente():
    pantalla = _caja_lista()
    producto = datos.productos[0]
    stock_inicial = producto["stock"]
    ventas_iniciales = len(datos.ventas)
    pantalla.items_carrito = [
        {
            "prod_id": producto["id"],
            "nombre": producto["nombre"],
            "cantidad": 1,
            "precio": producto["precio"] - 1,
        }
    ]
    pantalla.cobrar_carrito()
    assert "Cambió el precio" in _mensaje(pantalla)
    assert producto["stock"] == stock_inicial
    assert len(datos.ventas) == ventas_iniciales

    pantalla.items_carrito[0]["precio"] = producto["precio"]
    pantalla.combo_pago.value = "fiado"
    pantalla._ultimo_pago = "fiado"
    pantalla.cobrar_carrito()
    assert _mensaje(pantalla) == "Elegí un cliente para fiado"
    assert producto["stock"] == stock_inicial
    assert len(datos.ventas) == ventas_iniciales


def test_caja_cobra_y_permite_deshacer_la_venta(monkeypatch):
    pantalla = _caja_lista()
    producto = datos.productos[0]
    stock_inicial = producto["stock"]
    ventas_iniciales = len(datos.ventas)
    pantalla.items_carrito = [
        {
            "prod_id": producto["id"],
            "nombre": producto["nombre"],
            "cantidad": 2,
            "precio": producto["precio"],
        }
    ]
    aviso = {}
    monkeypatch.setattr(
        modulo_caja,
        "aviso",
        lambda _page, mensaje, texto_accion, al_accion: aviso.update(
            mensaje=mensaje, accion=texto_accion, al_accion=al_accion
        ),
    )

    pantalla.cobrar_carrito()

    assert producto["stock"] == stock_inicial - 2
    assert len(datos.ventas) == ventas_iniciales + 1
    assert pantalla.items_carrito == []
    assert aviso["mensaje"] == f"Cobrado {modulo_caja.moneda(producto['precio'] * 2)} — Efectivo"
    assert aviso["accion"] == "Deshacer"

    aviso["al_accion"]()
    assert producto["stock"] == stock_inicial
    assert len(datos.ventas) == ventas_iniciales
    assert _mensaje(pantalla) == "Venta deshecha"
