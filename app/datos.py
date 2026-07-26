from datetime import date
import uuid

productos = [
    {"id": "p1", "nombre": "Yerba Mate 1kg", "costo": 1200, "precio": 1800, "stock": 25, "minimo": 10},
    {"id": "p2", "nombre": "Azucar 1kg", "costo": 800, "precio": 1200, "stock": 8, "minimo": 10},
    {"id": "p3", "nombre": "Harina 000 1kg", "costo": 500, "precio": 900, "stock": 40, "minimo": 15},
    {"id": "p4", "nombre": "Aceite Girasol 1.5L", "costo": 1500, "precio": 2200, "stock": 3, "minimo": 5},
    {"id": "p5", "nombre": "Fideos 500g", "costo": 600, "precio": 950, "stock": 18, "minimo": 10},
    {"id": "p6", "nombre": "Arroz 1kg", "costo": 700, "precio": 1100, "stock": 12, "minimo": 8},
    {"id": "p7", "nombre": "Leche 1L", "costo": 900, "precio": 1300, "stock": 0, "minimo": 6},
    {"id": "p8", "nombre": "Pan Lactal", "costo": 400, "precio": 700, "stock": 15, "minimo": 8},
    {"id": "p9", "nombre": "Queso Cremoso 1kg", "costo": 2500, "precio": 3500, "stock": 5, "minimo": 3},
    {"id": "p10", "nombre": "Jabon Liquido 750ml", "costo": 600, "precio": 1000, "stock": 20, "minimo": 10},
]

clientes = [
    {"id": "c1", "nombre": "Juan Perez", "telefono": "3511234567"},
    {"id": "c2", "nombre": "Maria Garcia", "telefono": "3519876543"},
    {"id": "c3", "nombre": "Carlos Lopez", "telefono": "3515551234"},
]

ventas = []
cuentas = []


def id_unico():
    return str(uuid.uuid4())[:8]

def prod_por_id(pid):
    for p in productos:
        if p["id"] == pid:
            return p

def cli_por_id(cid):
    for c in clientes:
        if c["id"] == cid:
            return c

def cta_por_id(ccid):
    for c in cuentas:
        if c["id"] == ccid:
            return c

def margen(costo, precio):
    if precio is None or precio == 0:
        return 0
    return round(((precio - costo) / precio) * 100)

# ─── Productos CRUD ─────────────────────────────────────────────────

def crear_producto(nombre, costo, precio, stock=0, minimo=5):
    p = {"id": id_unico(), "nombre": nombre, "costo": costo, "precio": precio, "stock": stock, "minimo": minimo}
    productos.append(p)
    return p

def actualizar_producto(pid, nombre, costo, precio, stock, minimo):
    p = prod_por_id(pid)
    if p:
        p.update({"nombre": nombre, "costo": costo, "precio": precio, "stock": stock, "minimo": minimo})
    return p

def eliminar_producto(pid):
    # no se borra si tiene ventas asociadas
    if any(pid in (i.get("prod_id") for i in v.get("items", [])) for v in ventas):
        return False
    idx = next((i for i, p in enumerate(productos) if p["id"] == pid), None)
    if idx is not None:
        productos.pop(idx)
        return True
    return False

def ajustar_stock(pid, cantidad):
    """cantidad positiva = entra, negativa = sale"""
    p = prod_por_id(pid)
    if p:
        p["stock"] = max(0, p["stock"] + cantidad)
    return p

# ─── Clientes CRUD ──────────────────────────────────────────────────

def crear_cliente(nombre, telefono=""):
    c = {"id": id_unico(), "nombre": nombre, "telefono": telefono}
    clientes.append(c)
    return c

def actualizar_cliente(cid, nombre, telefono):
    c = cli_por_id(cid)
    if c:
        c.update({"nombre": nombre, "telefono": telefono})
    return c

def eliminar_cliente(cid):
    idx = next((i for i, c in enumerate(clientes) if c["id"] == cid), None)
    if idx is not None:
        clientes.pop(idx)
        return True
    return False

# ─── Ventas ─────────────────────────────────────────────────────────

def crear_venta(items, cliente_id="", pago="efectivo"):
    total = sum(i["precio"] * i["cantidad"] for i in items)
    hoy = date.today().isoformat()
    v = {"id": id_unico(), "cliente_id": cliente_id, "items": items, "total": total, "pago": pago, "fecha": hoy}
    ventas.append(v)
    for item in items:
        p = prod_por_id(item["prod_id"])
        if p:
            p["stock"] = max(0, p["stock"] - item["cantidad"])
    if pago == "fiado" and cliente_id:
        cuentas.append({"id": id_unico(), "cliente_id": cliente_id, "venta_id": v["id"], "total": total, "pagado": 0, "created_at": hoy})
    return v

def pagar_fiado(ccid, monto):
    c = cta_por_id(ccid)
    if c:
        c["pagado"] += monto
    return c

def stats():
    hoy = date.today().isoformat()
    mes = date.today().strftime("%Y-%m")
    vh = sum(v["total"] for v in ventas if v["fecha"] == hoy)
    vm = sum(v["total"] for v in ventas if v["fecha"].startswith(mes))
    gan = sum(
        (i["precio"] - (prod_por_id(i["prod_id"]) or {}).get("costo", 0)) * i["cantidad"]
        for v in ventas if v["fecha"].startswith(mes) for i in v.get("items", [])
    )
    deb = sum(c["total"] - c["pagado"] for c in cuentas)
    bajo = [p for p in productos if p["stock"] <= p["minimo"]]
    return {"hoy": vh, "mes": vm, "ganancia": gan, "deben": deb, "stock_bajo": bajo}


# ventas de ejemplo
if not ventas:
    crear_venta(
        items=[{"prod_id": "p1", "nombre": "Yerba Mate 1kg", "cantidad": 2, "precio": 1800}],
        cliente_id="c1", pago="fiado",
    )
    crear_venta(
        items=[
            {"prod_id": "p2", "nombre": "Azucar 1kg", "cantidad": 1, "precio": 1200},
            {"prod_id": "p6", "nombre": "Arroz 1kg", "cantidad": 1, "precio": 1100},
        ],
    )
