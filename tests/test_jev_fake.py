"""Evaluación de referencia del clasificador offline; sin datos ni red."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
import sys
from unittest import TestCase


APP = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP))

from jev.contract import (
    FuenteDecision,
    JevDecision,
    JevIntent,
    JevRequest,
    Periodo,
)
from jev.fake import clasificar
from screens.chat import respuesta_local


class FakeJevTests(TestCase):
    def test_eval_de_intenciones_y_periodos_con_casos_fijos(self):
        casos = (
            ("¿Cuánto vendí hoy?", JevIntent.VENTAS, Periodo.HOY),
            ("Ventas de esta semana", JevIntent.VENTAS, Periodo.ULTIMOS_7_DIAS),
            ("Ventas de este mes", JevIntent.VENTAS, Periodo.MES),
            ("Margen registrado histórico", JevIntent.GANANCIA_REGISTRADA, Periodo.HISTORIAL),
            ("Ganancia del mes", JevIntent.GANANCIA_REGISTRADA, Periodo.MES),
            ("¿Quién me debe más?", JevIntent.FIADO, None),
            ("Stock bajo", JevIntent.STOCK, None),
            ("Resumen del negocio", JevIntent.RESUMEN, None),
            ("Lista de clientes", JevIntent.CLIENTES, None),
        )

        acertados = sum(
            (decision := clasificar(consulta)).intent == intent
            and decision.periodo == periodo
            for consulta, intent, periodo in casos
        )

        self.assertEqual(acertados / len(casos), 1.0)

    def test_consulta_ambigua_se_devuelve_como_aclaracion_tipada(self):
        decision = clasificar(JevRequest("ventas"))

        self.assertEqual(decision.intent, JevIntent.VENTAS)
        self.assertIsNone(decision.periodo)
        self.assertLess(decision.confianza, 0.7)
        self.assertIn("qué periodo", decision.aclaracion.lower())
        self.assertEqual(decision.fuente, FuenteDecision.REGLAS_LOCALES)

    def test_intencion_desconocida_no_se_convierte_en_consulta_de_datos(self):
        decision = clasificar("blabla desconocido")

        self.assertEqual(decision.intent, JevIntent.DESCONOCIDO)
        self.assertIsNone(decision.periodo)
        self.assertEqual(decision.confianza, 0.0)
        self.assertTrue(decision.aclaracion)

    def test_chat_local_usa_decision_y_pide_periodo_para_margen_registrado(self):
        self.assertIn(
            "este mes o de todo el historial",
            respuesta_local("margen registrado").lower(),
        )
        self.assertIn(
            "Margen registrado de todo el historial",
            respuesta_local("margen registrado histórico"),
        )

    def test_decision_es_inmutable_y_confianza_se_valida(self):
        decision = clasificar("stock bajo")

        with self.assertRaises(FrozenInstanceError):
            decision.confianza = 2.0
        with self.assertRaisesRegex(ValueError, "entre 0 y 1"):
            JevDecision(
                JevIntent.STOCK,
                None,
                FuenteDecision.REGLAS_LOCALES,
                1.1,
            )
