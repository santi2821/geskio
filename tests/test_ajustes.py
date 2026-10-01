"""Pruebas de los flujos de respaldo visibles desde Ajustes."""

from __future__ import annotations

import asyncio
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

import flet as ft
import datos
from screens.ajustes import PantallaAjustes


class MockPage:
    def __init__(self, web=False):
        self.web = web
        self.services = []
        self.overlay = []
        self.snack_bar = None
        self.opened = []
        self.closed = []

    def update(self):
        pass

    def open(self, control):
        control.open = True
        self.overlay.append(control)
        self.opened.append(control)

    def close(self, control):
        control.open = False
        self.closed.append(control)


class FakeFilePicker:
    def __init__(self, save_path=None, files=None):
        self.save_path = save_path
        self.files = files or []
        self.save_calls = []
        self.pick_calls = []

    async def save_file(self, **kwargs):
        self.save_calls.append(kwargs)
        return self.save_path

    async def pick_files(self, **kwargs):
        self.pick_calls.append(kwargs)
        return self.files


def _textos(control):
    encontrados = []
    vistos = set()
    pendientes = [control]
    while pendientes:
        actual = pendientes.pop()
        if actual is None or id(actual) in vistos:
            continue
        vistos.add(id(actual))
        if isinstance(actual, ft.Text):
            encontrados.append(actual.value or "")
        pendientes.extend(getattr(actual, "controls", None) or [])
        pendientes.extend(getattr(actual, "actions", None) or [])
        pendientes.append(getattr(actual, "content", None))
    return encontrados


def test_ajustes_explica_modo_local_y_configuracion_futura(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_MODEL", "")
    textos = "\n".join(_textos(PantallaAjustes(MockPage()).build()))

    assert "Asistente" in textos
    assert "Modo local" in textos
    assert "no se detecta OPENROUTER_API_KEY" in textos
    assert "no se envían por internet" in textos
    assert "openai/gpt-6-luna" in textos


def test_ajustes_explica_envio_remoto_sin_mostrar_la_clave(monkeypatch):
    secreto = "sk-or-privado-de-prueba"
    monkeypatch.setenv("OPENROUTER_API_KEY", secreto)
    monkeypatch.setenv("OPENROUTER_MODEL", "proveedor/modelo")
    textos = "\n".join(_textos(PantallaAjustes(MockPage()).build()))

    assert "Clave de OpenRouter detectada" in textos
    assert "proveedor/modelo" in textos
    assert "permiso" in textos
    assert "hasta 8 mensajes" in textos
    assert "Excluye teléfonos, IDs" in textos
    assert "puede aplicar cargos" in textos
    assert secreto not in textos


def test_crear_respaldo_de_escritorio_registra_picker_y_es_valido(tmp_path):
    page = MockPage()
    pantalla = PantallaAjustes(page)
    pantalla.build()
    selector_registrado = pantalla._selector_archivos
    pantalla.build()
    assert page.services == [selector_registrado]

    ruta = tmp_path / "geskio-respaldo.json"
    selector = FakeFilePicker(save_path=str(ruta))
    pantalla._selector_archivos = selector
    asyncio.run(pantalla.crear_respaldo())

    estado = datos.leer_respaldo_archivo(ruta)
    assert estado["version"] == 3
    assert selector.save_calls[0]["allowed_extensions"] == ["json"]
    assert page.overlay[-1].content.value == "Copia guardada"


def test_crear_respaldo_web_entrega_bytes_al_selector(tmp_path):
    page = MockPage(web=True)
    pantalla = PantallaAjustes(page)
    pantalla.build()
    selector = FakeFilePicker()
    pantalla._selector_archivos = selector

    asyncio.run(pantalla.crear_respaldo())

    llamada = selector.save_calls[0]
    assert llamada["src_bytes"]
    assert datos.leer_respaldo(llamada["src_bytes"])["version"] == 3
    assert page.overlay[-1].content.value == "Se inició la descarga de la copia"


def test_restaurar_respaldo_muestra_preview_cancela_o_reemplaza(tmp_path):
    antes = datos.leer_respaldo(datos.serializar_respaldo())
    antes["productos"][0]["nombre"] = "Nombre del respaldo"
    ruta = tmp_path / "geskio-respaldo.json"
    ruta.write_text(json.dumps(antes), encoding="utf-8")
    cantidad_inicial = len(datos.productos)
    datos.crear_producto("Temporal", 10, 20, 2, 1)

    page = MockPage()
    restauraciones = []
    pantalla = PantallaAjustes(page, al_restaurar=lambda: restauraciones.append(True))
    pantalla.build()
    pantalla._selector_archivos = FakeFilePicker(
        files=[SimpleNamespace(size=ruta.stat().st_size, bytes=None, path=str(ruta))]
    )

    asyncio.run(pantalla.seleccionar_respaldo())
    dialogo = page.opened[-1]
    assert "proveedores" in dialogo.content.value
    assert len(datos.productos) == cantidad_inicial + 1
    dialogo.actions[0].on_click(None)
    assert len(datos.productos) == cantidad_inicial + 1

    asyncio.run(pantalla.seleccionar_respaldo())
    page.opened[-1].actions[1].on_click(None)
    assert len(datos.productos) == cantidad_inicial
    assert datos.productos[0]["nombre"] == "Nombre del respaldo"
    assert restauraciones == [True]
    assert page.overlay[-1].content.value.startswith("Copia restaurada")


def test_respaldo_invalido_no_abre_confirmacion_ni_cambia_datos(tmp_path):
    ruta = tmp_path / "dañado.json"
    ruta.write_text("{ roto", encoding="utf-8")
    estado_anterior = deepcopy(datos._estado_actual())
    page = MockPage()
    pantalla = PantallaAjustes(page)
    pantalla.build()
    pantalla._selector_archivos = FakeFilePicker(
        files=[SimpleNamespace(size=ruta.stat().st_size, bytes=None, path=str(ruta))]
    )

    asyncio.run(pantalla.seleccionar_respaldo())

    assert page.opened == []
    assert datos._estado_actual() == estado_anterior
    assert "dañado" in page.overlay[-1].content.value
