"""Clasificador de referencia, determinista, tipado y completamente offline."""

from __future__ import annotations

import unicodedata

from jev.contract import (
    FuenteDecision,
    JevDecision,
    JevIntent,
    JevRequest,
    Periodo,
)


def _normalizar(texto: str) -> str:
    return "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", (texto or "").lower())
        if not unicodedata.combining(caracter)
    )


def _contiene(texto: str, *alternativas: str) -> bool:
    return any(alternativa in texto for alternativa in alternativas)


def _periodo(texto: str) -> Periodo | None:
    if _contiene(texto, "histor", "todo el tiempo", "desde que empece"):
        return Periodo.HISTORIAL
    if _contiene(texto, "hoy", "este dia"):
        return Periodo.HOY
    if _contiene(texto, "semana", "ultimos 7 dias", "ultimos siete dias", "7 dias"):
        return Periodo.ULTIMOS_7_DIAS
    if _contiene(texto, "mes", "mensual"):
        return Periodo.MES
    return None


def clasificar(request: JevRequest | str) -> JevDecision:
    """Resuelve solo intenciones conocidas; no lee datos ni ejecuta acciones."""
    consulta = request.consulta if isinstance(request, JevRequest) else request
    texto = _normalizar(consulta)
    periodo = _periodo(texto)

    if (
        _contiene(texto, "ganancia")
        and _contiene(texto, "mes", "histor", "confiable")
    ) or _contiene(texto, "margen registrado"):
        intent = JevIntent.GANANCIA_REGISTRADA
    elif _contiene(texto, "margen", "rentabilidad", "ganancia"):
        intent = JevIntent.MARGEN_CATALOGO
    elif _contiene(texto, "debe", "deben", "deuda", "fiado", "por cobrar"):
        intent = JevIntent.FIADO
    elif _contiene(texto, "stock", "inventario", "existencia", "reponer"):
        intent = JevIntent.STOCK
    elif _contiene(texto, "resumen", "panorama"):
        intent = JevIntent.RESUMEN
    elif _contiene(texto, "venta", "vendi", "factur", "ingreso") or periodo is not None:
        intent = JevIntent.VENTAS
    elif _contiene(texto, "cliente", "clientes"):
        intent = JevIntent.CLIENTES
    else:
        return JevDecision(
            JevIntent.DESCONOCIDO,
            None,
            FuenteDecision.REGLAS_LOCALES,
            0.0,
            "Proba: ¿cuánto vendí hoy? ¿qué margen actual tengo? ¿quién me debe?",
        )

    aclaracion = None
    confianza = 0.92
    if intent == JevIntent.VENTAS and periodo is None:
        confianza = 0.62
        aclaracion = "¿Qué periodo querés consultar: hoy, últimos 7 días o este mes?"
    elif intent == JevIntent.GANANCIA_REGISTRADA and periodo is None:
        confianza = 0.62
        aclaracion = "¿Querés el margen registrado de este mes o de todo el historial?"

    return JevDecision(
        intent=intent,
        periodo=periodo,
        fuente=FuenteDecision.REGLAS_LOCALES,
        confianza=confianza,
        aclaracion=aclaracion,
    )
