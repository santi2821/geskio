"""Regression checks for GesKio's demo data model, screens, and product claims."""

from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
sys.path.insert(0, str(APP))
_IMPORT_DATA_DIR = tempfile.TemporaryDirectory(prefix="geskio-test-import-")
_OLD_DATA_FILE = os.environ.get("GESKIO_DATA_FILE")
os.environ["GESKIO_DATA_FILE"] = str(Path(_IMPORT_DATA_DIR.name) / "initial.json")

import datos  # noqa: E402 - isolate the import-time demo seed above
import flet as ft  # noqa: E402
from screens.ajustes import PantallaAjustes  # noqa: E402
from screens.caja import PantallaCaja  # noqa: E402
from screens.chat import PantallaChat, respuesta_local  # noqa: E402
from screens.clientes import PantallaClientes  # noqa: E402
from screens.dashboard import (  # noqa: E402
    PantallaDashboard,
    totales_mes,
    totales_ultimos_7_dias,
    ventas_del_dia,
)
from screens.fiado import PantallaFiado  # noqa: E402
from screens.stock import PantallaStock  # noqa: E402
from theme import colores  # noqa: E402
from widgets import campo_texto, en_rail_para_tamano  # noqa: E402

if _OLD_DATA_FILE is None:
    os.environ.pop("GESKIO_DATA_FILE", None)
else:
    os.environ["GESKIO_DATA_FILE"] = _OLD_DATA_FILE


class DatosTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="geskio-test-")
        datos.RUTA_ARCHIVO_DATOS = Path(self.temp.name) / "estado.json"
        datos.productos[:] = []
        datos.clientes[:] = []
        datos.ventas[:] = []
        datos.cuentas[:] = []
        datos._PERSISTENCIA_ACTIVA = True
        self.producto = datos.crear_producto("Yerba", 100, 150, 8, 2)
        self.cliente = datos.crear_cliente(" Ana ", " 123 ")

    def tearDown(self):
        datos._PERSISTENCIA_ACTIVA = False
        self.temp.cleanup()

    def item(self, cantidad=2, precio=None):
        return {
            "prod_id": self.producto["id"],
            "nombre": self.producto["nombre"],
            "cantidad": cantidad,
            "precio": self.producto["precio"] if precio is None else precio,
        }

    def test_cliente_se_normaliza_y_rechaza_entrada_invalida(self):
        self.assertEqual(self.cliente["nombre"], "Ana")
        self.assertEqual(self.cliente["telefono"], "123")
        for nombre, telefono in [("   ", "123"), ("Ana", 123)]:
            with self.subTest(nombre=nombre, telefono=telefono):
                with self.assertRaises(ValueError):
                    datos.crear_cliente(nombre, telefono)
        with self.assertRaises(ValueError):
            datos.actualizar_cliente(self.cliente["id"], " ", "123")
        self.assertEqual(self.cliente["nombre"], "Ana")
        self.assertEqual(datos._cargar_estado(), True)

    def test_producto_edicion_y_movimientos_de_stock_validan_y_persisten(self):
        actualizado = datos.actualizar_producto(
            self.producto["id"], "Yerba suave", 110, 170, 9, 3
        )
        self.assertEqual(actualizado["nombre"], "Yerba suave")
        antes = dict(actualizado)
        with self.assertRaises(ValueError):
            datos.actualizar_producto(self.producto["id"], " ", 100, 150, 8, 2)
        self.assertEqual(actualizado, antes)
        for valores in [("A", True, 2, 1, 0), ("B", 1, 2, True, 0)]:
            with self.subTest(valores=valores), self.assertRaises(ValueError):
                datos.crear_producto(*valores)
        datos.ajustar_stock(self.producto["id"], 4)
        datos.ajustar_stock(self.producto["id"], -2)
        self.assertEqual(self.producto["stock"], 11)
        for cantidad in [0, True, 1.5, -12]:
            with self.subTest(cantidad=cantidad), self.assertRaises(ValueError):
                datos.ajustar_stock(self.producto["id"], cantidad)
        self.assertEqual(self.producto["stock"], 11)
        self.assertEqual(datos.prod_por_id("no-existe"), None)

    def test_stock_y_edicion_sobreviven_recarga_y_json_entero_decimal_se_normaliza(self):
        datos.actualizar_producto(self.producto["id"], "Yerba", 100, 150, 8, 2)
        datos.ajustar_stock(self.producto["id"], 3)
        estado = json.loads(datos.RUTA_ARCHIVO_DATOS.read_text(encoding="utf-8"))
        estado["productos"][0]["stock"] = 11.0
        estado["productos"][0]["minimo"] = 2.0
        datos.RUTA_ARCHIVO_DATOS.write_text(json.dumps(estado), encoding="utf-8")
        self.assertTrue(datos._cargar_estado())
        producto_recargado = datos.prod_por_id(self.producto["id"])
        self.assertEqual(producto_recargado["stock"], 11)
        self.assertIs(type(producto_recargado["stock"]), int)
        self.assertIs(type(producto_recargado["minimo"]), int)

    def test_venta_agrupa_requerimiento_repetido_y_acepta_stock_exactamente_disponible(self):
        venta = datos.crear_venta(
            [self.item(cantidad=3), self.item(cantidad=5)], self.cliente["id"], "efectivo"
        )
        self.assertEqual(venta["total"], 1200)
        self.assertEqual(self.producto["stock"], 0)
        with self.assertRaises(ValueError):
            datos.crear_venta([self.item(cantidad=1)], self.cliente["id"], "efectivo")
        self.assertEqual(len(datos.ventas), 1)

    def test_no_permite_borrar_cliente_ni_producto_con_historial(self):
        venta = datos.crear_venta([self.item()], self.cliente["id"], "efectivo")
        self.assertFalse(datos.eliminar_cliente(self.cliente["id"]))
        self.assertFalse(datos.eliminar_producto(self.producto["id"]))
        self.assertEqual(datos.ventas[0]["id"], venta["id"])

    def test_stats_resume_ventas_deudas_ganancia_y_stock_bajo(self):
        datos.crear_venta([self.item()], self.cliente["id"], "fiado")
        resumen = datos.stats()
        self.assertEqual(resumen["hoy"], 300)
        self.assertEqual(resumen["mes"], 300)
        self.assertEqual(resumen["ganancia"], 100)
        self.assertEqual(resumen["deben"], 300)
        self.assertNotIn(self.producto, resumen["stock_bajo"])
        datos.ajustar_stock(self.producto["id"], -6)
        self.assertIn(self.producto, datos.stats()["stock_bajo"])

    def test_venta_fiado_pago_parcial_anulacion_y_stock(self):
        entrada = self.item()
        entrada["nombre"] = "nombre falsificado"
        venta = datos.crear_venta([entrada], self.cliente["id"], "fiado")
        cuenta = datos.cuentas[0]
        self.assertEqual(venta["total"], 300)
        self.assertEqual(venta["items"][0]["nombre"], self.producto["nombre"])
        entrada["precio"] = -10
        self.assertEqual(venta["items"][0]["precio"], self.producto["precio"])
        self.assertEqual(self.producto["stock"], 6)
        self.assertEqual(datos.pagar_fiado(cuenta["id"], 100)["pagado"], 100)
        self.assertTrue(datos.deshacer_venta(venta["id"]))
        self.assertEqual(self.producto["stock"], 8)
        self.assertEqual(datos.cuentas, [])
        self.assertTrue(datos.eliminar_cliente(self.cliente["id"]))
        self.assertTrue(datos.eliminar_producto(self.producto["id"]))

    def test_venta_rechaza_pago_cliente_precio_y_stock_invalidos(self):
        casos = [
            ([], "", "efectivo"),
            ([self.item()], "", "fiado"),
            ([self.item()], "cliente-inexistente", "efectivo"),
            ([self.item()], "", "banana"),
            ([self.item()], "", []),
            ([self.item()], [], "efectivo"),
            ([self.item(precio=999)], "", "efectivo"),
            ([self.item(cantidad=9)], "", "efectivo"),
            ([self.item(cantidad=True)], "", "efectivo"),
        ]
        for items, cliente_id, pago in casos:
            with self.subTest(items=items, cliente_id=cliente_id, pago=pago):
                with self.assertRaises(ValueError):
                    datos.crear_venta(items, cliente_id, pago)
                self.assertEqual(self.producto["stock"], 8)
                self.assertEqual(datos.ventas, [])

    def test_pago_fiado_rechaza_cero_negativo_no_finito_y_exceso(self):
        venta = datos.crear_venta([self.item()], self.cliente["id"], "fiado")
        cuenta = datos.cuentas[0]
        for monto in [0, -1, float("nan"), float("inf"), 301]:
            with self.subTest(monto=monto):
                with self.assertRaises(ValueError):
                    datos.pagar_fiado(cuenta["id"], monto)
        self.assertEqual(cuenta["pagado"], 0)
        self.assertEqual(datos.ventas[0]["id"], venta["id"])

    def test_fallo_al_persistir_revierte_mutacion_y_conserva_archivo(self):
        datos._guardar_estado()
        antes = datos.RUTA_ARCHIVO_DATOS.read_bytes()
        with patch.object(datos, "_guardar_estado", side_effect=RuntimeError("disco")):
            with self.assertRaisesRegex(RuntimeError, "disco"):
                datos.crear_venta([self.item()], self.cliente["id"], "fiado")
        self.assertEqual(self.producto["stock"], 8)
        self.assertEqual(datos.ventas, [])
        self.assertEqual(datos.cuentas, [])
        self.assertEqual(datos.RUTA_ARCHIVO_DATOS.read_bytes(), antes)

    def test_archivo_corrupto_o_version_desconocida_falla_sin_reemplazo(self):
        datos._guardar_estado()
        original = datos.RUTA_ARCHIVO_DATOS.read_bytes()
        datos.RUTA_ARCHIVO_DATOS.write_text("{ roto", encoding="utf-8")
        corrupto = datos.RUTA_ARCHIVO_DATOS.read_bytes()
        with self.assertRaises(RuntimeError):
            datos._cargar_estado()
        self.assertEqual(datos.RUTA_ARCHIVO_DATOS.read_bytes(), corrupto)
        estado = {"version": 999, "productos": [], "clientes": [], "ventas": [], "cuentas": []}
        datos.RUTA_ARCHIVO_DATOS.write_text(json.dumps(estado), encoding="utf-8")
        desconocido = datos.RUTA_ARCHIVO_DATOS.read_bytes()
        with self.assertRaises(RuntimeError):
            datos._cargar_estado()
        self.assertEqual(datos.RUTA_ARCHIVO_DATOS.read_bytes(), desconocido)
        self.assertNotEqual(original, desconocido)

    def test_estado_se_recupera_en_un_proceso_nuevo(self):
        venta = datos.crear_venta([self.item()], self.cliente["id"], "efectivo")
        env = os.environ.copy()
        env["GESKIO_DATA_FILE"] = str(datos.RUTA_ARCHIVO_DATOS)
        env["PYTHONPATH"] = str(APP)
        proceso = subprocess.run(
            [
                sys.executable,
                "-c",
                "import datos; print(len(datos.productos), len(datos.clientes), len(datos.ventas), len(datos.cuentas))",
            ],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(proceso.stdout.strip(), "1 1 1 0")
        self.assertEqual(datos.ventas[0]["id"], venta["id"])

    def test_json_rechaza_venta_con_pago_o_relacion_invalida(self):
        venta = datos.crear_venta([self.item()], self.cliente["id"], "efectivo")
        base = {
            "version": datos._VERSION_ESTADO,
            "productos": datos.productos,
            "clientes": datos.clientes,
            "ventas": datos.ventas,
            "cuentas": datos.cuentas,
        }
        estado = json.loads(json.dumps(base))
        estado["ventas"][0]["pago"] = "banana"
        with self.assertRaisesRegex(ValueError, "pago"):
            datos._validar_estado(estado)
        estado = json.loads(json.dumps(base))
        estado["ventas"][0]["cliente_id"] = "fantasma"
        with self.assertRaisesRegex(ValueError, "cliente"):
            datos._validar_estado(estado)
        self.assertEqual(venta["total"], 300)

    def test_chat_local_distingue_periodos_y_aclara_ambiguedad(self):
        datos.crear_venta([self.item(cantidad=2)], self.cliente["id"], "efectivo")
        self.assertIn("Ventas de hoy:", respuesta_local("¿Cuánto vendí hoy?"))
        self.assertIn("Ventas del mes:", respuesta_local("Ventas de este mes"))
        self.assertIn("últimos 7 días", respuesta_local("¿Cuánto vendí esta semana?"))
        self.assertIn("Qué periodo", respuesta_local("ventas"))
        self.assertIn("ganancia histórica todavía no es confiable", respuesta_local("ganancia del mes"))

    def test_chat_agrega_deuda_por_cliente_y_ordena_el_mayor_saldo(self):
        otro = datos.crear_cliente("Beto")
        datos.crear_venta([self.item(cantidad=2)], self.cliente["id"], "fiado")
        datos.crear_venta([self.item(cantidad=1)], self.cliente["id"], "fiado")
        datos.crear_venta([self.item(cantidad=1)], otro["id"], "fiado")
        respuesta = respuesta_local("¿Quién me debe más?")
        self.assertIn("Ana", respuesta)
        self.assertNotIn("Beto", respuesta)


class PantallasYProductoTests(unittest.TestCase):
    def test_las_siete_pantallas_construyen_su_arbol(self):
        pantallas = [
            PantallaDashboard,
            PantallaCaja,
            PantallaStock,
            PantallaClientes,
            PantallaFiado,
            PantallaChat,
            PantallaAjustes,
        ]
        for clase in pantallas:
            with self.subTest(pantalla=clase.__name__):
                control = clase(Mock()).build()
                self.assertIsInstance(control, ft.Control)

    def test_helpers_de_formulario_y_breakpoint_de_navegacion(self):
        campo = campo_texto(label="Producto")
        self.assertEqual(campo.border_radius, 10)
        self.assertEqual(campo.focused_border_width, 2)
        self.assertTrue(en_rail_para_tamano(760, 700))
        self.assertFalse(en_rail_para_tamano(1100, 700))
        self.assertTrue(en_rail_para_tamano(1100, 560))

    def test_dropdowns_de_caja_tienen_opciones_en_el_primer_render(self):
        caja = PantallaCaja(Mock())
        caja.build()
        self.assertEqual(
            [o.key for o in caja.combo_cliente.options],
            [""] + [cliente["id"] for cliente in datos.clientes],
        )
        self.assertEqual(
            [o.key for o in caja.combo_producto.options],
            [p["id"] for p in datos.productos if p["stock"] > 0],
        )
        self.assertEqual([o.key for o in caja.combo_pago.options], ["efectivo", "transferencia", "fiado"])

    def test_periodos_dashboard_con_fechas_controladas(self):
        ventas = [
            {"fecha": "2026-09-24", "total": 120},
            {"fecha": "2026-09-24", "total": 30},
            {"fecha": "2026-09-23", "total": 50},
            {"fecha": "2026-08-24", "total": 90},
        ]
        self.assertEqual(len(ventas_del_dia(ventas, "2026-09-24")), 2)
        self.assertEqual(totales_mes(ventas, 2026, 9), {24: 150, 23: 50})
        serie = totales_ultimos_7_dias(ventas, __import__("datetime").date(2026, 9, 24))
        self.assertEqual(len(serie), 7)
        self.assertEqual(serie[-1], ("2026-09-24", 150))

    def test_dashboard_etiqueta_la_ganancia_como_estimacion(self):
        def controles(control):
            yield control
            for hijo in getattr(control, "controls", []):
                yield from controles(hijo)
            contenido = getattr(control, "content", None)
            if contenido is not None:
                yield from controles(contenido)

        for valor, rol in [(-25, colores.get().danger_text), (25, colores.get().success)]:
            with self.subTest(ganancia=valor), patch(
                "screens.dashboard.stats",
                return_value={"hoy": 0, "mes": 0, "ganancia": valor, "deben": 0, "stock_bajo": []},
            ):
                arbol = PantallaDashboard(Mock()).build()
                textos = [c for c in controles(arbol) if isinstance(c, ft.Text)]
                valores = [c for c in textos if c.value == "-$25" or c.value == "$25"]
                titulo = [c for c in textos if c.value == "Ganancia estimada del mes"]
                nota = [c for c in textos if "costos vigentes" in str(c.value)]
                self.assertEqual(len(valores), 1)
                self.assertEqual(valores[0].color, rol)
                self.assertEqual(len(titulo), 1)
                self.assertTrue(nota)


class LandingConsistencyTests(unittest.TestCase):
    def test_landing_no_afirma_perdida_de_datos_ni_pago_con_tarjeta(self):
        home = (ROOT / "landing" / "index.html").read_text(encoding="utf-8")
        funciones = (ROOT / "landing" / "pages" / "funciones.html").read_text(encoding="utf-8")
        contacto = (ROOT / "landing" / "pages" / "contacto.html").read_text(encoding="utf-8")
        texto = home + funciones + contacto
        self.assertNotIn("se borran al cerrar", texto.lower())
        self.assertNotIn("los cambios no se conservan al cerrar", texto.lower())
        self.assertNotIn("Tarjeta</span>", texto)
        self.assertNotIn("lo ves antes de guardar", texto.lower())
        self.assertIn("proveedor de IA todavía está por decidir", home)
        self.assertIn("no comprende todos los periodos", funciones)

    def test_radios_de_landing_coinciden_con_tokens_de_app(self):
        css = (ROOT / "landing" / "assets" / "css" / "tokens.css").read_text(encoding="utf-8")
        theme = (APP / "theme.py").read_text(encoding="utf-8")
        for nombre, valor in [("sm", 8), ("md", 10), ("lg", 16)]:
            with self.subTest(radio=nombre):
                self.assertIn(f"--radius-{nombre}: {valor}px", css)
                self.assertIn(f"R_{nombre.upper()} = {valor}", theme)

    def test_landing_tiene_archivos_locales_y_anclas_validas(self):
        class Parser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids = set()
                self.refs = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if "id" in attrs:
                    self.ids.add(attrs["id"])
                if tag == "a" and "href" in attrs:
                    self.refs.append(attrs["href"])
                attr = "src" if tag in {"script", "img"} else "href"
                if tag in {"script", "link", "img"} and attr in attrs:
                    self.refs.append(attrs[attr])

        root = ROOT / "landing"
        pages = [root / "index.html", *sorted((root / "pages").glob("*.html"))]
        parsed = {}
        for page in pages:
            parser = Parser()
            parser.feed(page.read_text(encoding="utf-8"))
            parsed[page.resolve()] = parser
        broken = []
        for page, parser in parsed.items():
            for ref in parser.refs:
                if ref.startswith(("http:", "https:", "mailto:", "tel:", "data:", "javascript:")):
                    continue
                path, _, fragment = ref.partition("#")
                destination = (page.parent / path).resolve() if path else page
                if path and not destination.is_file():
                    broken.append((page.name, ref))
                elif fragment and destination in parsed and fragment not in parsed[destination].ids:
                    broken.append((page.name, ref))
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
