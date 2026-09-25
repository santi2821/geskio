import sys

sys.path.insert(0, "app")
import datos
from datos import (
    productos,
    clientes,
    ventas,
    cuentas,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
    ajustar_stock,
    crear_cliente,
    crear_venta,
    pagar_fiado,
    stats,
    margen,
    cli_por_id,
    prod_por_id,
)


def test_margen():
    assert margen(100, 200) == 50
    assert margen(0, 0) == 0
    assert margen(100, None) == 0


def test_crear_producto():
    n = len(productos)
    p = crear_producto("Test Prod", 100, 200, stock=5, minimo=2)
    assert p["id"] in [x["id"] for x in productos]
    assert p["nombre"] == "Test Prod"
    # cleanup
    productos.remove(p)
    assert len(productos) == n


def test_ajustar_stock():
    p = productos[0]
    orig = p["stock"]
    ajustar_stock(p["id"], 5)
    assert p["stock"] == orig + 5
    ajustar_stock(p["id"], -5)
    assert p["stock"] == orig
    # la arquitectura newer valida: rechaza ajustes que dejen stock negativo
    # (antes se clampaba a 0; ahora es ValueError y el stock no cambia)
    try:
        ajustar_stock(p["id"], -(orig + 9999))
        assert False, "debió rechazar el ajuste que deja stock negativo"
    except ValueError:
        pass
    assert p["stock"] == orig
    p["stock"] = orig  # restore


def test_crear_venta_descuenta_stock():
    p = productos[2]
    orig = p["stock"]
    v = crear_venta(
        [{"prod_id": p["id"], "nombre": p["nombre"], "cantidad": 1, "precio": p["precio"]}]
    )
    assert p["stock"] == max(0, orig - 1)
    # cleanup
    ventas.remove(v)
    p["stock"] = orig


def test_eliminar_producto_con_venta():
    # p1 tiene venta asociada (creada en datos.py)
    assert eliminar_producto("p1") is False
    # crear producto sin ventas y borrar
    p = crear_producto("Borrable", 10, 20, stock=1)
    assert eliminar_producto(p["id"]) is True
    # ya borrado
    assert eliminar_producto(p["id"]) is False


def test_stats():
    s = stats()
    assert "hoy" in s
    assert "mes" in s
    assert "ganancia" in s
    assert "deben" in s
    assert "stock_bajo" in s


def test_fiado():
    # crear venta fiada
    p = productos[5]
    orig_stock = p["stock"]
    v = crear_venta(
        [{"prod_id": p["id"], "nombre": p["nombre"], "cantidad": 1, "precio": p["precio"]}],
        cliente_id="c1",
        pago="fiado",
    )
    assert len(cuentas) > 0
    c = cuentas[-1]
    assert c["cliente_id"] == "c1"
    pendiente = c["total"] - c["pagado"]
    pagar_fiado(c["id"], pendiente)
    assert c["pagado"] == c["total"]
    # cleanup
    ventas.remove(v)
    cuentas.remove(c)
    p["stock"] = orig_stock
