"""Aísla persistencia y credenciales para que pytest nunca use datos del usuario."""

from __future__ import annotations

import atexit
from copy import deepcopy
import os
from pathlib import Path
import tempfile

import pytest


_VARIABLES = (
    "GESKIO_DATA_FILE",
    "OPENROUTER_API_KEY",
    "OPENROUTER_MODEL",
    "GESKIO_MODO_INICIAL",
)
_VALORES_PREVIOS = {nombre: os.environ.get(nombre) for nombre in _VARIABLES}
_RAIZ_TEMPORAL = tempfile.TemporaryDirectory(prefix="geskio-pytest-suite-")
os.environ["GESKIO_DATA_FILE"] = str(Path(_RAIZ_TEMPORAL.name) / "suite.json")
os.environ.pop("OPENROUTER_API_KEY", None)
os.environ["OPENROUTER_MODEL"] = "openai/gpt-6-luna"
os.environ["GESKIO_MODO_INICIAL"] = "demo"


def _restaurar_entorno():
    for nombre, valor in _VALORES_PREVIOS.items():
        if valor is None:
            os.environ.pop(nombre, None)
        else:
            os.environ[nombre] = valor


atexit.register(_restaurar_entorno)
atexit.register(_RAIZ_TEMPORAL.cleanup)


@pytest.fixture(autouse=True)
def aislar_estado_de_datos():
    """Da a cada prueba listas de ejemplo independientes y un JSON temporal."""
    import datos

    nombres = (
        "productos", "clientes", "proveedores", "ventas", "cuentas", "movimientos_stock"
    )
    if not hasattr(aislar_estado_de_datos, "base"):
        aislar_estado_de_datos.base = {
            nombre: deepcopy(getattr(datos, nombre)) for nombre in nombres
        }

    ruta_previa = datos.RUTA_ARCHIVO_DATOS
    persistencia_previa = datos._PERSISTENCIA_ACTIVA
    comercio_previo = datos.COMERCIO_INICIALIZADO
    modo_previo = datos.MODO_COMERCIO
    temporal = tempfile.TemporaryDirectory(prefix="geskio-pytest-case-")
    datos.RUTA_ARCHIVO_DATOS = Path(temporal.name) / "estado.json"
    datos._PERSISTENCIA_ACTIVA = True
    for nombre in nombres:
        getattr(datos, nombre)[:] = deepcopy(aislar_estado_de_datos.base[nombre])
    try:
        yield
    finally:
        for nombre in nombres:
            getattr(datos, nombre)[:] = deepcopy(aislar_estado_de_datos.base[nombre])
        datos.RUTA_ARCHIVO_DATOS = ruta_previa
        datos._PERSISTENCIA_ACTIVA = persistencia_previa
        datos.COMERCIO_INICIALIZADO = comercio_previo
        datos.MODO_COMERCIO = modo_previo
        temporal.cleanup()
