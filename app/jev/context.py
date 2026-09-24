"""Vista de solo lectura y minimizada de datos para el asistente conversacional."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta

import datos


def construir_contexto(hoy: date | None = None) -> dict:
    """Devuelve agregados útiles; excluye teléfonos, IDs y el JSON completo."""
    corte = hoy or date.today()
    inicio_7_dias = corte - timedelta(days=6)
    inicio_90_dias = corte - timedelta(days=89)
    inicio_mes = corte.replace(day=1)

    ventas_por_dia = defaultdict(lambda: {"total": 0, "cantidad": 0})
    total_hoy = total_semana = total_mes = 0
    cantidad_hoy = cantidad_semana = cantidad_mes = 0

    for venta in datos.ventas:
        try:
            fecha = date.fromisoformat(venta.get("fecha", ""))
            total = float(venta.get("total", 0))
        except (TypeError, ValueError):
            continue
        if fecha > corte:
            continue
        iso = fecha.isoformat()
        if fecha == corte:
            total_hoy += total
            cantidad_hoy += 1
        if inicio_7_dias <= fecha <= corte:
            total_semana += total
            cantidad_semana += 1
        if inicio_mes <= fecha <= corte:
            total_mes += total
            cantidad_mes += 1
        if inicio_90_dias <= fecha <= corte:
            ventas_por_dia[iso]["total"] += total
            ventas_por_dia[iso]["cantidad"] += 1
    clientes_por_id = {cliente["id"]: cliente for cliente in datos.clientes}
    deuda_por_cliente = defaultdict(float)
    cuentas_pendientes = 0
    for cuenta in datos.cuentas:
        pendiente = max(0, float(cuenta.get("total", 0)) - float(cuenta.get("pagado", 0)))
        if pendiente:
            cid = cuenta.get("cliente_id", "")
            nombre = clientes_por_id.get(cid, {}).get("nombre", "Cliente sin ficha")
            deuda_por_cliente[nombre] += pendiente
            cuentas_pendientes += 1

    catalogo = [
        {
            "producto": str(p.get("nombre", "Producto"))[:80],
            "stock": p.get("stock", 0),
            "stock_minimo": p.get("minimo", 0),
            "precio_actual": p.get("precio", 0),
        }
        for p in datos.productos[:150]
    ]
    bajos = [p for p in catalogo if p["stock"] <= p["stock_minimo"]]
    saldos_cliente = [
        {"cliente": str(nombre)[:80], "pendiente": pendiente}
        for nombre, pendiente in sorted(
            deuda_por_cliente.items(), key=lambda fila: fila[1], reverse=True
        )[:50]
    ]

    return {
        "fecha_de_corte": corte.isoformat(),
        "ventas": {
            "hoy": {"total": total_hoy, "cantidad": cantidad_hoy},
            "ultimos_7_dias_incluido_hoy": {
                "desde": inicio_7_dias.isoformat(),
                "total": total_semana,
                "cantidad": cantidad_semana,
            },
            "mes_actual": {
                "desde": inicio_mes.isoformat(),
                "total": total_mes,
                "cantidad": cantidad_mes,
            },
            "por_dia_ultimos_90_dias": [
                {"fecha": fecha, **valores}
                for fecha, valores in sorted(ventas_por_dia.items())
            ],
            "detalle_transaccional_incluido": False,
        },
        "inventario": {
            "productos_en_catalogo": len(datos.productos),
            "catalogo_limitado_a_150": len(datos.productos) > len(catalogo),
            "productos_bajo_minimo": bajos,
            "catalogo": catalogo,
        },
        "fiado": {
            "total_pendiente": sum(deuda_por_cliente.values()),
            "cuentas_pendientes": cuentas_pendientes,
            "saldo_por_cliente": saldos_cliente,
            "clientes_omitidos": max(0, len(deuda_por_cliente) - len(saldos_cliente)),
        },
        "limites": [
            "No se incluyen teléfonos, identificadores ni el archivo JSON.",
            "Solo se incluyen agregados diarios de ventas; no se incluyen filas de venta individuales.",
            "La ganancia histórica no está disponible: no se guardó el costo de cada venta.",
            "El catálogo se limita a los primeros 150 productos y los saldos a 50 clientes.",
        ],
    }
