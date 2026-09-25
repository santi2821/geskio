from datetime import date, timedelta
from copy import deepcopy
from functools import wraps
import json
import math
import os
from pathlib import Path
import platform
import tempfile
import uuid

# datos en memoria (demo); aca van productos, clientes, ventas y cuentas de fiado
productos = [
    {
        "id": "p1",
        "nombre": "Yerba Mate 1kg",
        "costo": 1200,
        "precio": 1800,
        "stock": 25,
        "minimo": 10,
    },
    {
        "id": "p2",
        "nombre": "Azucar 1kg",
        "costo": 800,
        "precio": 1200,
        "stock": 8,
        "minimo": 10,
    },
    {
        "id": "p3",
        "nombre": "Harina 000 1kg",
        "costo": 500,
        "precio": 900,
        "stock": 40,
        "minimo": 15,
    },
    {
        "id": "p4",
        "nombre": "Aceite Girasol 1.5L",
        "costo": 1500,
        "precio": 2200,
        "stock": 3,
        "minimo": 5,
    },
    {
        "id": "p5",
        "nombre": "Fideos 500g",
        "costo": 600,
        "precio": 950,
        "stock": 18,
        "minimo": 10,
    },
    {
        "id": "p6",
        "nombre": "Arroz 1kg",
        "costo": 700,
        "precio": 1100,
        "stock": 12,
        "minimo": 8,
    },
    {
        "id": "p7",
        "nombre": "Leche 1L",
        "costo": 900,
        "precio": 1300,
        "stock": 0,
        "minimo": 6,
    },
    {
        "id": "p8",
        "nombre": "Pan Lactal",
        "costo": 400,
        "precio": 700,
        "stock": 15,
        "minimo": 8,
    },
    {
        "id": "p9",
        "nombre": "Queso Cremoso 1kg",
        "costo": 2500,
        "precio": 3500,
        "stock": 5,
        "minimo": 3,
    },
    {
        "id": "p10",
        "nombre": "Jabon Liquido 750ml",
        "costo": 600,
        "precio": 1000,
        "stock": 20,
        "minimo": 10,
    },
]

clientes = [
    {"id": "c1", "nombre": "Juan Perez", "telefono": "3511234567"},
    {"id": "c2", "nombre": "Maria Garcia", "telefono": "3519876543"},
    {"id": "c3", "nombre": "Carlos Lopez", "telefono": "3515551234"},
]

proveedores = [
    {
        "id": "pr1",
        "nombre": "Distribuidora Sur",
        "telefono": "3514231122",
        "email": "contacto@distrisur.com.ar",
        "rubro": "Alimentos",
    },
    {
        "id": "pr2",
        "nombre": "Lacteos del Centro",
        "telefono": "3515559876",
        "email": "ventas@lacteoscentro.com.ar",
        "rubro": "Lacteos",
    },
    {
        "id": "pr3",
        "nombre": "Bebidas Norte",
        "telefono": "3514445566",
        "email": "info@bebidasnorte.com.ar",
        "rubro": "Bebidas",
    },
]

ventas = []
cuentas = []

_VERSION_ESTADO = 1
_PERSISTENCIA_ACTIVA = False


def _ruta_archivo_estado():
    ruta_configurada = os.environ.get("GESKIO_DATA_FILE")
    if ruta_configurada:
        return Path(ruta_configurada).expanduser()

    if os.name == "nt":
        raiz = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif platform.system() == "Darwin":
        raiz = Path.home() / "Library" / "Application Support"
    else:
        raiz = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return raiz / "GesKio" / "demo_data.json"


RUTA_ARCHIVO_DATOS = _ruta_archivo_estado()


def _estado_actual():
    return {
        "productos": productos,
        "clientes": clientes,
        "proveedores": proveedores,
        "ventas": ventas,
        "cuentas": cuentas,
    }


def _guardar_estado():
    datos = {"version": _VERSION_ESTADO, **_estado_actual()}
    temporal = None
    try:
        RUTA_ARCHIVO_DATOS.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=RUTA_ARCHIVO_DATOS.parent,
            prefix=f".{RUTA_ARCHIVO_DATOS.name}.",
            suffix=".tmp",
            delete=False,
        ) as archivo:
            temporal = Path(archivo.name)
            json.dump(datos, archivo, ensure_ascii=False, indent=2, allow_nan=False)
            archivo.write("\n")
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, RUTA_ARCHIVO_DATOS)
    except (OSError, TypeError, ValueError) as ex:
        if temporal is not None:
            try:
                temporal.unlink(missing_ok=True)
            except OSError:
                pass
        raise RuntimeError(
            f"No se pudieron guardar los datos de la demo en {RUTA_ARCHIVO_DATOS}: {ex}"
        ) from ex


def _rechazar_constante_json(valor):
    raise ValueError(f"Constante JSON inválida: {valor}")


def _validar_numero_estado(valor, campo, minimo=None):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"campo numérico inválido: {campo}")
    try:
        finito = math.isfinite(float(valor))
    except (OverflowError, ValueError):
        finito = False
    if not finito or (minimo is not None and valor < minimo):
        raise ValueError(f"valor fuera de rango: {campo}")


def _validar_estado(datos):
    claves = ("productos", "clientes", "ventas", "cuentas")
    if (
        not isinstance(datos, dict)
        or type(datos.get("version")) is not int
        or datos["version"] != _VERSION_ESTADO
    ):
        raise ValueError("versión o estructura del archivo no compatible")
    if any(not isinstance(datos.get(clave), list) for clave in claves):
        raise ValueError("faltan listas requeridas en el archivo")
    # proveedores es main-only: los archivos v1 no la traen; se acepta ausente
    # y se normaliza a lista vacia para no romper la carga de datos existentes.
    if datos.get("proveedores") is None:
        datos["proveedores"] = []
    if not isinstance(datos.get("proveedores"), list):
        raise ValueError("faltan listas requeridas en el archivo")

    for clave in (*claves, "proveedores"):
        ids = set()
        for fila in datos[clave]:
            if not isinstance(fila, dict) or not isinstance(fila.get("id"), str) or not fila["id"]:
                raise ValueError(f"registro inválido en {clave}")
            if fila["id"] in ids:
                raise ValueError(f"identificador repetido en {clave}")
            ids.add(fila["id"])

    for producto in datos["productos"]:
        nombre, costo, precio, stock, minimo = _validar_producto(
            producto.get("nombre"),
            producto.get("costo"),
            producto.get("precio"),
            producto.get("stock"),
            producto.get("minimo"),
        )
        producto.update(
            {"nombre": nombre, "costo": costo, "precio": precio, "stock": stock, "minimo": minimo}
        )
    for cliente in datos["clientes"]:
        if not isinstance(cliente.get("nombre"), str) or not cliente["nombre"].strip():
            raise ValueError("nombre de cliente inválido")
        if not isinstance(cliente.get("telefono", ""), str):
            raise ValueError("teléfono de cliente inválido")
    for proveedor in datos["proveedores"]:
        if not isinstance(proveedor.get("nombre"), str) or not proveedor["nombre"].strip():
            raise ValueError("nombre de proveedor inválido")
        for campo in ("telefono", "email", "rubro"):
            if not isinstance(proveedor.get(campo, ""), str):
                raise ValueError(f"{campo} de proveedor inválido")

    clientes_por_id = {cliente["id"] for cliente in datos["clientes"]}
    productos_por_id = {producto["id"] for producto in datos["productos"]}

    ventas_por_id = {venta["id"]: venta for venta in datos["ventas"]}
    cuentas_por_venta = {}
    for cuenta in datos["cuentas"]:
        venta_id = cuenta.get("venta_id")
        if venta_id not in ventas_por_id:
            raise ValueError("cuenta asociada a una venta inexistente")
        cuentas_por_venta[venta_id] = cuentas_por_venta.get(venta_id, 0) + 1

    for venta in datos["ventas"]:
        fecha = venta.get("fecha")
        if not isinstance(fecha, str) or date.fromisoformat(fecha).isoformat() != fecha:
            raise ValueError("fecha de venta inválida")
        if not isinstance(venta.get("items"), list) or not venta["items"]:
            raise ValueError("productos de venta inválidos")
        _validar_numero_estado(venta.get("total"), "total de venta", 0)
        pago = venta.get("pago")
        if not isinstance(pago, str) or pago not in {"efectivo", "transferencia", "fiado"}:
            raise ValueError("medio de pago inválido")
        cliente_id = venta.get("cliente_id", "")
        if not isinstance(cliente_id, str) or (cliente_id and cliente_id not in clientes_por_id):
            raise ValueError("cliente de venta inexistente")
        total_items = 0
        for item in venta["items"]:
            if not isinstance(item, dict) or not isinstance(item.get("prod_id"), str):
                raise ValueError("línea de venta inválida")
            if not isinstance(item.get("nombre"), str):
                raise ValueError("nombre de producto vendido inválido")
            _validar_numero_estado(item.get("cantidad"), "cantidad de venta", 0)
            if (
                isinstance(item["cantidad"], bool)
                or not isinstance(item["cantidad"], int)
                or item["cantidad"] == 0
            ):
                raise ValueError("cantidad de venta inválida")
            _validar_numero_estado(item.get("precio"), "precio de venta", 0)
            if item["prod_id"] not in productos_por_id:
                raise ValueError("producto vendido inexistente")
            total_items += item["precio"] * item["cantidad"]
        if not math.isclose(venta["total"], total_items, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("el total de venta no coincide con sus productos")
        numero_cuentas = cuentas_por_venta.get(venta["id"], 0)
        debe_tener_cuenta = venta["pago"] == "fiado" and bool(venta.get("cliente_id"))
        if numero_cuentas != int(debe_tener_cuenta):
            raise ValueError("cuenta de fiado incoherente con el medio de pago")
    for cuenta in datos["cuentas"]:
        fecha = cuenta.get("created_at")
        if not isinstance(fecha, str) or date.fromisoformat(fecha).isoformat() != fecha:
            raise ValueError("fecha de cuenta inválida")
        _validar_numero_estado(cuenta.get("total"), "total de cuenta", 0)
        _validar_numero_estado(cuenta.get("pagado"), "pago de cuenta", 0)
        if cuenta["pagado"] > cuenta["total"]:
            raise ValueError("pago superior al total de la cuenta")
        venta = ventas_por_id[cuenta["venta_id"]]
        cliente_id = cuenta.get("cliente_id")
        if not isinstance(cliente_id, str) or cliente_id not in clientes_por_id:
            raise ValueError("cliente de cuenta inexistente")
        if venta.get("cliente_id") != cliente_id or venta.get("pago") != "fiado":
            raise ValueError("cliente o medio de pago de cuenta incoherente")
        if cuenta["total"] != venta["total"]:
            raise ValueError("total de cuenta distinto al total de venta")


def _cargar_estado():
    if not RUTA_ARCHIVO_DATOS.exists():
        return False
    try:
        with RUTA_ARCHIVO_DATOS.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo, parse_constant=_rechazar_constante_json)
        _validar_estado(datos)
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        ValueError,
        TypeError,
        OverflowError,
    ) as ex:
        raise RuntimeError(
            f"No se pudieron cargar los datos de {RUTA_ARCHIVO_DATOS}; "
            "el archivo se conserva y no se reemplazará con datos de ejemplo. "
            f"Detalle: {ex}"
        ) from ex

    # Las pantallas importan estas listas directamente: conservar su identidad.
    productos[:] = datos["productos"]
    clientes[:] = datos["clientes"]
    proveedores[:] = datos["proveedores"]
    ventas[:] = datos["ventas"]
    cuentas[:] = datos["cuentas"]
    return True


def _persistir_mutacion(funcion):
    @wraps(funcion)
    def envuelta(*args, **kwargs):
        if not _PERSISTENCIA_ACTIVA:
            return funcion(*args, **kwargs)
        anterior = deepcopy(_estado_actual())
        referencias = {clave: list(filas) for clave, filas in _estado_actual().items()}
        try:
            resultado = funcion(*args, **kwargs)
            if _estado_actual() != anterior:
                _guardar_estado()
            return resultado
        except Exception:
            if _estado_actual() != anterior:
                for clave, destino in _estado_actual().items():
                    filas_originales = referencias[clave]
                    for fila, contenido in zip(filas_originales, anterior[clave]):
                        if isinstance(fila, dict) and isinstance(contenido, dict):
                            fila.clear()
                            fila.update(deepcopy(contenido))
                    destino[:] = filas_originales
            raise

    return envuelta


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


def _validar_producto(nombre, costo, precio, stock, minimo):
    nombre = nombre.strip() if isinstance(nombre, str) else ""
    if not nombre:
        raise ValueError("El nombre del producto es obligatorio")

    if isinstance(costo, bool) or isinstance(precio, bool):
        raise ValueError("El costo y el precio deben ser números válidos")
    try:
        costo = float(costo)
        precio = float(precio)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("El costo y el precio deben ser números válidos") from None

    if not math.isfinite(costo) or costo < 0:
        raise ValueError("El costo debe ser un número válido mayor o igual a cero")
    if not math.isfinite(precio) or precio < 0:
        raise ValueError("El precio debe ser un número válido mayor o igual a cero")

    try:
        if isinstance(stock, bool) or isinstance(minimo, bool):
            raise ValueError
        stock_entero = int(stock)
        minimo_entero = int(minimo)
        if float(stock) != stock_entero or float(minimo) != minimo_entero:
            raise ValueError
    except (TypeError, ValueError, OverflowError):
        raise ValueError("El stock y el mínimo deben ser números enteros") from None

    if stock_entero < 0 or minimo_entero < 0:
        raise ValueError("El stock y el mínimo no pueden ser negativos")
    return nombre, costo, precio, stock_entero, minimo_entero


# ─── Productos CRUD ─────────────────────────────────────────────────


@_persistir_mutacion
def crear_producto(nombre, costo, precio, stock=0, minimo=5):
    nombre, costo, precio, stock, minimo = _validar_producto(nombre, costo, precio, stock, minimo)
    p = {
        "id": id_unico(),
        "nombre": nombre,
        "costo": costo,
        "precio": precio,
        "stock": stock,
        "minimo": minimo,
    }
    productos.append(p)
    return p


@_persistir_mutacion
def actualizar_producto(pid, nombre, costo, precio, stock, minimo):
    p = prod_por_id(pid)
    if p:
        nombre, costo, precio, stock, minimo = _validar_producto(
            nombre, costo, precio, stock, minimo
        )
        p.update(
            {
                "nombre": nombre,
                "costo": costo,
                "precio": precio,
                "stock": stock,
                "minimo": minimo,
            }
        )
    return p


@_persistir_mutacion
def eliminar_producto(pid):
    # no se borra si tiene ventas asociadas
    if any(pid in (i.get("prod_id") for i in v.get("items", [])) for v in ventas):
        return False
    idx = next((i for i, p in enumerate(productos) if p["id"] == pid), None)
    if idx is not None:
        productos.pop(idx)
        return True
    return False


@_persistir_mutacion
def ajustar_stock(pid, cantidad):
    """cantidad positiva = entra, negativa = sale"""
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad == 0:
        raise ValueError("El ajuste de stock debe ser un entero distinto de cero")
    p = prod_por_id(pid)
    if p:
        if p["stock"] + cantidad < 0:
            raise ValueError(f"El ajuste dejaría stock negativo de {p['nombre']}")
        p["stock"] += cantidad
    return p


# ─── Clientes CRUD ──────────────────────────────────────────────────


@_persistir_mutacion
def crear_cliente(nombre, telefono=""):
    nombre, telefono = _validar_cliente(nombre, telefono)
    c = {"id": id_unico(), "nombre": nombre, "telefono": telefono}
    clientes.append(c)
    return c


@_persistir_mutacion
def actualizar_cliente(cid, nombre, telefono):
    c = cli_por_id(cid)
    if c:
        nombre, telefono = _validar_cliente(nombre, telefono)
        c.update({"nombre": nombre, "telefono": telefono})
    return c


@_persistir_mutacion
def eliminar_cliente(cid):
    if any(v.get("cliente_id") == cid for v in ventas) or any(
        c.get("cliente_id") == cid for c in cuentas
    ):
        return False
    idx = next((i for i, c in enumerate(clientes) if c["id"] == cid), None)
    if idx is not None:
        clientes.pop(idx)
        return True
    return False


def _validar_cliente(nombre, telefono):
    nombre = nombre.strip() if isinstance(nombre, str) else ""
    if not nombre:
        raise ValueError("El nombre del cliente es obligatorio")
    if not isinstance(telefono, str):
        raise ValueError("El teléfono del cliente debe ser texto")
    return nombre, telefono.strip()


# ─── Proveedores CRUD (port main-only a arquitectura 0.84) ────────────


def _validar_proveedor(nombre, telefono="", email="", rubro=""):
    nombre = nombre.strip() if isinstance(nombre, str) else ""
    if not nombre:
        raise ValueError("El nombre del proveedor es obligatorio")
    for campo, valor in (("telefono", telefono), ("email", email), ("rubro", rubro)):
        if not isinstance(valor, str):
            raise ValueError(f"El {campo} del proveedor debe ser texto")
    return nombre, telefono.strip(), email.strip(), rubro.strip()


def prov_por_id(pid):
    for p in proveedores:
        if p["id"] == pid:
            return p
    return None


@_persistir_mutacion
def crear_proveedor(nombre, telefono="", email="", rubro=""):
    nombre, telefono, email, rubro = _validar_proveedor(nombre, telefono, email, rubro)
    pr = {"id": id_unico(), "nombre": nombre, "telefono": telefono, "email": email, "rubro": rubro}
    proveedores.append(pr)
    return pr


@_persistir_mutacion
def actualizar_proveedor(pid, nombre=None, telefono=None, email=None, rubro=None):
    p = prov_por_id(pid)
    if p:
        if nombre is not None:
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("El nombre del proveedor es obligatorio")
            p["nombre"] = nombre.strip()
        if telefono is not None:
            if not isinstance(telefono, str):
                raise ValueError("El telefono del proveedor debe ser texto")
            p["telefono"] = telefono.strip()
        if email is not None:
            if not isinstance(email, str):
                raise ValueError("El email del proveedor debe ser texto")
            p["email"] = email.strip()
        if rubro is not None:
            if not isinstance(rubro, str):
                raise ValueError("El rubro del proveedor debe ser texto")
            p["rubro"] = rubro.strip()
    return p


@_persistir_mutacion
def eliminar_proveedor(pid):
    idx = next((i for i, p in enumerate(proveedores) if p["id"] == pid), None)
    if idx is not None:
        proveedores.pop(idx)
        return True
    return False


# ─── Ventas ─────────────────────────────────────────────────────────


@_persistir_mutacion
def crear_venta(items, cliente_id="", pago="efectivo"):
    if not isinstance(items, list) or not items:
        raise ValueError("La venta necesita al menos un producto")
    if not isinstance(cliente_id, str):
        raise ValueError("El cliente seleccionado no es válido")
    if cliente_id and not cli_por_id(cliente_id):
        raise ValueError("El cliente seleccionado ya no existe")
    if not isinstance(pago, str) or pago not in {"efectivo", "transferencia", "fiado"}:
        raise ValueError("Elegí un medio de pago válido")
    if pago == "fiado" and not cliente_id:
        raise ValueError("Elegí un cliente para registrar la venta fiada")

    items_venta = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Hay un producto inválido en la venta")
        producto = prod_por_id(item.get("prod_id"))
        if not producto:
            raise ValueError("Un producto del carrito ya no existe; revisá la venta")
        cantidad = item.get("cantidad")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad de cada producto debe ser mayor a cero")
        precio = item.get("precio")
        _validar_numero_estado(precio, "precio de venta", 0)
        if not math.isclose(float(precio), float(producto["precio"]), rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(
                f"Cambió el precio de {producto['nombre']}; quitá y agregá el producto nuevamente"
            )
        items_venta.append(
            {
                "prod_id": producto["id"],
                "nombre": producto["nombre"],
                "cantidad": cantidad,
                "precio": producto["precio"],
            }
        )
    cantidades = {}
    for item in items_venta:
        pid = item["prod_id"]
        cantidades[pid] = cantidades.get(pid, 0) + item["cantidad"]
    for pid, cantidad in cantidades.items():
        producto = prod_por_id(pid)
        if cantidad > producto["stock"]:
            raise ValueError(
                f"Stock insuficiente de {producto['nombre']}: quedan {producto['stock']}"
            )

    total = sum(i["precio"] * i["cantidad"] for i in items_venta)
    hoy = date.today().isoformat()
    v = {
        "id": id_unico(),
        "cliente_id": cliente_id,
        "items": items_venta,
        "total": total,
        "pago": pago,
        "fecha": hoy,
    }
    ventas.append(v)
    for item in items_venta:
        p = prod_por_id(item["prod_id"])
        if p:
            p["stock"] = max(0, p["stock"] - item["cantidad"])
    if pago == "fiado" and cliente_id:
        cuentas.append(
            {
                "id": id_unico(),
                "cliente_id": cliente_id,
                "venta_id": v["id"],
                "total": total,
                "pagado": 0,
                "created_at": hoy,
            }
        )
    return v


@_persistir_mutacion
def deshacer_venta(vid):
    # revierte una venta: devuelve el stock y borra venta + cuenta de fiado
    v = next((x for x in ventas if x.get("id") == vid), None)
    if not v:
        return False
    for item in v.get("items", []):
        p = prod_por_id(item.get("prod_id"))
        if p:
            p["stock"] = p["stock"] + item.get("cantidad", 0)
    idx = next((i for i, x in enumerate(ventas) if x.get("id") == vid), None)
    if idx is not None:
        ventas.pop(idx)
    for i in range(len(cuentas) - 1, -1, -1):
        if cuentas[i].get("venta_id") == vid:
            cuentas.pop(i)
    return True


@_persistir_mutacion
def pagar_fiado(ccid, monto):
    c = cta_por_id(ccid)
    if c:
        _validar_numero_estado(monto, "monto de pago", 0)
        if monto <= 0:
            raise ValueError("El pago debe ser mayor a cero")
        pendiente = c["total"] - c["pagado"]
        if monto > pendiente:
            raise ValueError(f"El pago supera el saldo pendiente ({pendiente})")
        c["pagado"] += monto
    return c


def stats():
    hoy = date.today().isoformat()
    mes = date.today().strftime("%Y-%m")
    vh = sum(v["total"] for v in ventas if v["fecha"] == hoy)
    vm = sum(v["total"] for v in ventas if v["fecha"].startswith(mes))
    gan = sum(
        (i["precio"] - (prod_por_id(i["prod_id"]) or {}).get("costo", 0)) * i["cantidad"]
        for v in ventas
        if v["fecha"].startswith(mes)
        for i in v.get("items", [])
    )
    deb = sum(c["total"] - c["pagado"] for c in cuentas)
    bajo = [p for p in productos if p["stock"] <= p["minimo"]]
    return {"hoy": vh, "mes": vm, "ganancia": gan, "deben": deb, "stock_bajo": bajo}


# ─── Helpers para gráficos / dashboard (0.28.3) ───────────────────────


def ventas_por_dia(dias=7):
    """Retorna lista dict {fecha, total} para los últimos `dias` días (incluye hoy)."""
    hoy = date.today()
    resultado = []
    for offset in range(dias):
        d = hoy - timedelta(days=dias - 1 - offset)
        fecha_str = d.isoformat()
        total = sum(v["total"] for v in ventas if v.get("fecha") == fecha_str)
        resultado.append({"fecha": fecha_str, "total": total})
    return resultado


def stock_stats():
    """Retorna dict {ok, bajo, agotado} según stock vs minimo."""
    ok = sum(1 for p in productos if p["stock"] > p["minimo"])
    bajo = sum(1 for p in productos if 0 < p["stock"] <= p["minimo"])
    agotado = sum(1 for p in productos if p["stock"] == 0)
    return {"ok": ok, "bajo": bajo, "agotado": agotado}


def ventas_por_mes(meses=6):
    """Retorna lista dict {mes, total} para los últimos `meses` meses (incluye actual). mes = 'YYYY-MM'."""
    hoy = date.today()
    meses_lista = []
    base_idx = hoy.year * 12 + (hoy.month - 1)
    for i in range(meses - 1, -1, -1):
        idx = base_idx - i
        yy = idx // 12
        mm = idx % 12 + 1
        meses_lista.append(f"{yy:04d}-{mm:02d}")
    resultado = []
    for mes_str in meses_lista:
        total = sum(v["total"] for v in ventas if v.get("fecha", "").startswith(mes_str))
        resultado.append({"mes": mes_str, "total": total})
    return resultado


def ganancia_por_mes(meses=6):
    """Retorna lista dict {mes, ganancia} para gráficos de ganancia mensual."""
    hoy = date.today()
    base_idx = hoy.year * 12 + (hoy.month - 1)
    meses_lista = []
    for i in range(meses - 1, -1, -1):
        idx = base_idx - i
        yy = idx // 12
        mm = idx % 12 + 1
        meses_lista.append(f"{yy:04d}-{mm:02d}")
    resultado = []
    for mes_str in meses_lista:
        gan = sum(
            (it["precio"] - (prod_por_id(it["prod_id"]) or {}).get("costo", 0)) * it["cantidad"]
            for v in ventas
            if v.get("fecha", "").startswith(mes_str)
            for it in v.get("items", [])
        )
        resultado.append({"mes": mes_str, "ganancia": gan})
    return resultado


# Se crean los datos iniciales solo si todavía no existe un archivo de estado.
def _inicializar_estado():
    global _PERSISTENCIA_ACTIVA
    if _cargar_estado():
        _PERSISTENCIA_ACTIVA = True
        return

    crear_venta(
        items=[{"prod_id": "p1", "nombre": "Yerba Mate 1kg", "cantidad": 2, "precio": 1800}],
        cliente_id="c1",
        pago="fiado",
    )
    crear_venta(
        items=[
            {"prod_id": "p2", "nombre": "Azucar 1kg", "cantidad": 1, "precio": 1200},
            {"prod_id": "p6", "nombre": "Arroz 1kg", "cantidad": 1, "precio": 1100},
        ],
    )
    _guardar_estado()
    _PERSISTENCIA_ACTIVA = True


_inicializar_estado()
