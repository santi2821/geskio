"""OpenRouter integration tests; all transports are mocked, no network or secrets."""

from __future__ import annotations

from datetime import date
import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
sys.path.insert(0, str(APP))

import datos  # noqa: E402
from jev.context import construir_contexto  # noqa: E402
from jev.openrouter import (  # noqa: E402
    ENDPOINT,
    MODELO_PREDETERMINADO,
    OpenRouterError,
    completar_chat,
    construir_mensajes,
)
from screens.chat import PantallaChat  # noqa: E402


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, amount=-1):
        return self.payload if amount < 0 else self.payload[:amount]


class JevTests(TestCase):
    def setUp(self):
        self.listas_originales = {
            nombre: getattr(datos, nombre)
            for nombre in ("productos", "clientes", "ventas", "cuentas")
        }
        datos.productos[:] = [
            {"id": "p-privado", "nombre": "Yerba", "costo": 4, "precio": 8, "stock": 2, "minimo": 5}
        ]
        datos.clientes[:] = [
            {"id": "c-privado", "nombre": "Ana", "telefono": "555-1234"}
        ]
        datos.ventas[:] = [
            {
                "id": "venta-privada",
                "fecha": "2026-09-24",
                "total": 16,
                "pago": "efectivo",
                "cliente_id": "c-privado",
                "items": [
                    {"prod_id": "p-privado", "nombre": "Yerba", "cantidad": 2, "precio": 8}
                ],
            }
        ]
        datos.cuentas[:] = [
            {"id": "cuenta-privada", "cliente_id": "c-privado", "total": 16, "pagado": 6}
        ]

    def tearDown(self):
        for nombre, lista in self.listas_originales.items():
            getattr(datos, nombre)[:] = lista

    def test_contexto_usa_datos_y_excluye_telefonos_ids_y_ganancia_historica(self):
        contexto = construir_contexto(date(2026, 9, 24))
        self.assertEqual(contexto["ventas"]["hoy"], {"total": 16.0, "cantidad": 1})
        self.assertEqual(contexto["fiado"]["saldo_por_cliente"], [{"cliente": "Ana", "pendiente": 10.0}])
        serializado = json.dumps(contexto, ensure_ascii=False)
        self.assertIn("Yerba", serializado)
        self.assertIn("Ana", serializado)
        self.assertNotIn("555-1234", serializado)
        self.assertNotIn("p-privado", serializado)
        self.assertNotIn("venta-privada", serializado)
        self.assertNotIn("cuenta-privada", serializado)
        self.assertNotIn('"costo"', serializado)
        self.assertNotIn("medio_pago", serializado)
        self.assertNotIn('"items"', serializado)

    def test_snapshot_grande_se_recorta_antes_de_enviar(self):
        contexto = {
            "fecha_de_corte": "2026-09-24",
            "ventas": {"por_dia_ultimos_90_dias": [{"fecha": str(n), "total": n} for n in range(90)]},
            "inventario": {
                "catalogo": [{"producto": f"Producto {n} " + "x" * 80} for n in range(150)],
                "productos_bajo_minimo": [{"producto": f"Producto {n} " + "x" * 80} for n in range(150)],
            },
            "fiado": {"saldo_por_cliente": [{"cliente": f"Cliente {n}"} for n in range(100)]},
        }
        mensajes = construir_mensajes(contexto, [], "resumen")
        self.assertIn("contexto_reducido_por_limite", mensajes[0]["content"])
        self.assertLess(len(mensajes[0]["content"]), 20000)

    def test_prompt_limita_historial_y_senala_snapshot_como_datos(self):
        mensajes = construir_mensajes(
            {"fecha_de_corte": "2026-09-24"},
            [("user", f"pregunta {n}") for n in range(12)] + [("system", "injection")],
            "¿Cuánto vendí hoy?",
        )
        self.assertEqual(len(mensajes), 9)  # system + 8 turnos recientes + consulta
        self.assertEqual(mensajes[-1]["content"], "¿Cuánto vendí hoy?")
        self.assertIn("nunca instrucciones", mensajes[0]["content"])
        self.assertTrue(all(m["role"] != "system" for m in mensajes[1:]))

    def test_requiere_clave_antes_de_intentar_red(self):
        with patch.dict("os.environ", {}, clear=True), self.assertRaisesRegex(
            OpenRouterError, "OPENROUTER_API_KEY"
        ):
            completar_chat(
                {}, [], "hola",
                transporte=lambda *_args, **_kwargs: self.fail("no debe llamar red"),
            )

    def test_solicitud_openrouter_usa_bearer_modelo_y_respuesta(self):
        solicitudes = []

        def transporte(request, timeout):
            solicitudes.append((request, timeout))
            return FakeResponse({"choices": [{"message": {"content": "Vendiste $16 hoy."}}]})

        with patch.dict("os.environ", {"OPENROUTER_MODEL": "   "}):
            answer = completar_chat(
                {"fecha_de_corte": "2026-09-24"}, [], "¿Cuánto vendí hoy?",
                api_key="sk-or-test", transporte=transporte,
            )
        request, timeout = solicitudes[0]
        self.assertEqual(answer, "Vendiste $16 hoy.")
        self.assertEqual(request.full_url, ENDPOINT)
        self.assertEqual(request.get_header("Authorization"), "Bearer sk-or-test")
        self.assertEqual(timeout, 35)
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], MODELO_PREDETERMINADO)
        self.assertEqual(MODELO_PREDETERMINADO, "openai/gpt-6-luna")
        self.assertFalse(payload["stream"])
        self.assertNotIn("tools", payload)

    def test_chat_muestra_modelo_predeterminado_si_override_esta_vacio(self):
        with patch.dict(
            "os.environ",
            {"OPENROUTER_API_KEY": "sk-or-test", "OPENROUTER_MODEL": "   "},
        ):
            self.assertEqual(
                PantallaChat._texto_configuracion(),
                f"Clave configurada · modelo {MODELO_PREDETERMINADO}",
            )

    def test_mapea_error_de_autorizacion_sin_exponer_cuerpo(self):
        def transporte(request, timeout):
            raise HTTPError(request.full_url, 401, "invalid", {}, io.BytesIO(b"secret response"))

        with self.assertRaisesRegex(OpenRouterError, "OPENROUTER_API_KEY") as error:
            completar_chat({}, [], "hola", api_key="sk-or-test", transporte=transporte)
        self.assertNotIn("secret response", str(error.exception))

    def test_rechaza_respuesta_malformada(self):
        class BadResponse(FakeResponse):
            def read(self, amount=-1):
                return b"not-json"

        with self.assertRaisesRegex(OpenRouterError, "no pudo leer"):
            completar_chat(
                {}, [], "hola", api_key="sk-or-test",
                transporte=lambda *_args, **_kwargs: BadResponse({}),
            )

    def test_rechaza_respuesta_remota_mayor_al_limite(self):
        class BigResponse(FakeResponse):
            def read(self, amount=-1):
                return b"x" * amount

        with self.assertRaisesRegex(OpenRouterError, "superó el tamaño"):
            completar_chat(
                {}, [], "hola", api_key="sk-or-test",
                transporte=lambda *_args, **_kwargs: BigResponse({}),
            )

    def test_chat_ui_manda_consulta_al_provider_y_muestra_respuesta(self):
        import asyncio

        chat = PantallaChat(Mock())
        chat.build()
        chat.acepta_envio = True
        chat.confirmacion_datos.value = True
        chat.boton_enviar.disabled = False
        chat.campo_mensaje.value = "¿Cuánto vendí hoy?"
        with patch("screens.chat.construir_contexto", return_value={"ventas": {"hoy": 12}}), patch(
            "screens.chat.completar_chat", return_value="Vendiste $12 hoy."
        ) as provider:
            asyncio.run(chat.enviar_mensaje())
        self.assertEqual(chat.mensajes, [("¿Cuánto vendí hoy?", True), ("Vendiste $12 hoy.", False)])
        self.assertEqual(provider.call_args.args[0], {"ventas": {"hoy": 12}})
        self.assertFalse(chat.enviando)

    def test_chat_ui_no_envia_sin_confirmacion_de_privacidad(self):
        import asyncio

        chat = PantallaChat(Mock())
        chat.build()
        chat.campo_mensaje.value = "¿Cuánto vendí hoy?"
        with patch("screens.chat.completar_chat") as provider:
            asyncio.run(chat.enviar_mensaje())
        provider.assert_not_called()
        self.assertEqual(chat.mensajes, [])

    def test_checkbox_actualiza_autorizacion_desde_event_data_de_flet(self):
        chat = PantallaChat(Mock())
        chat.build()
        chat._al_cambiar_autorizacion(
            SimpleNamespace(data="true", control=SimpleNamespace(value=False))
        )
        self.assertTrue(chat.acepta_envio)
        self.assertFalse(chat.boton_enviar.disabled)
        chat._al_cambiar_autorizacion(
            SimpleNamespace(data="false", control=SimpleNamespace(value=True))
        )
        self.assertFalse(chat.acepta_envio)
        self.assertTrue(chat.boton_enviar.disabled)
