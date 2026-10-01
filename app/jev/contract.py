"""Contrato mínimo de decisiones locales para enrutar consultas del Chat."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class JevIntent(str, Enum):
    VENTAS = "ventas"
    GANANCIA_REGISTRADA = "ganancia_registrada"
    MARGEN_CATALOGO = "margen_catalogo"
    FIADO = "fiado"
    STOCK = "stock"
    RESUMEN = "resumen"
    CLIENTES = "clientes"
    DESCONOCIDO = "desconocido"


class Periodo(str, Enum):
    HOY = "hoy"
    ULTIMOS_7_DIAS = "ultimos_7_dias"
    MES = "mes"
    HISTORIAL = "historial"


class FuenteDecision(str, Enum):
    REGLAS_LOCALES = "reglas_locales"


@dataclass(frozen=True)
class JevRequest:
    consulta: str


@dataclass(frozen=True)
class JevDecision:
    intent: JevIntent
    periodo: Periodo | None
    fuente: FuenteDecision
    confianza: float
    aclaracion: str | None = None

    def __post_init__(self) -> None:
        if (
            isinstance(self.confianza, bool)
            or not isinstance(self.confianza, (int, float))
            or not 0.0 <= self.confianza <= 1.0
        ):
            raise ValueError("La confianza debe estar entre 0 y 1")
        if not isinstance(self.intent, JevIntent):
            raise ValueError("La intención debe pertenecer al catálogo permitido")
        if self.periodo is not None and not isinstance(self.periodo, Periodo):
            raise ValueError("El periodo debe pertenecer al catálogo permitido")
        if not isinstance(self.fuente, FuenteDecision):
            raise ValueError("La fuente de la decisión no es válida")
        if self.intent == JevIntent.DESCONOCIDO and not self.aclaracion:
            raise ValueError("Una intención desconocida debe pedir aclaración")
