# GesKio

Gestor de ventas, inventario y cuentas para pequeños comercios, hecho con Python y Flet. Incluye una aplicación de escritorio multiplataforma y una landing estática.

> Prototipo en evolución. Los datos de ejemplo se guardan como JSON en el perfil local del usuario; todavía no hay una base de datos multiusuario ni sincronización entre dispositivos.

## Funciones

- Panel con ventas, calendario y gráficos.
- Caja, productos, clientes, proveedores y cuentas corrientes.
- Apariencia clara y oscura, con ajustes de marca.
- Chat opcional con OpenRouter. Antes de enviar una consulta, la app muestra qué resumen comercial compartirá.

## Requisitos

- Python 3.11 o posterior.
- Windows, macOS o Linux para la aplicación Flet.

## Ejecutar la aplicación

Desde la raíz del repositorio:

```bash
python -m venv .venv
```

Activa el entorno y luego instala las dependencias:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python app/main.py
```

La landing estática se encuentra en `landing/`. Ábrela con un servidor local para que funcionen sus recursos:

```bash
python -m http.server 8080 --directory landing
```

## Chat con OpenRouter

El chat necesita `OPENROUTER_API_KEY` y pide autorización antes de enviar datos. La configuración opcional del modelo y las instrucciones para iniciar la app están en [`docs/openrouter-local.md`](docs/openrouter-local.md). La consulta puede incluir el texto escrito, hasta ocho mensajes previos y un resumen de nombres y saldos de clientes, productos, precios, stock y ventas agregadas. No se envían teléfonos, identificadores ni el archivo JSON completo. Revisa los cargos y límites de tu cuenta de OpenRouter.

## Desarrollo

Las dependencias de la aplicación y las herramientas de desarrollo están en `requirements.txt`. La suite se puede ejecutar con:

```bash
python -m pytest -q
```

## Estructura

```text
app/                 Aplicación Flet y funciones de negocio
app/jev/             Adaptador experimental para decisiones tipadas
docs/                Configuración y notas del proyecto
landing/             Sitio estático de presentación
openspec/            Especificaciones y cambios del producto
tests/               Pruebas unitarias y de interfaz
```

## Licencia

[MIT](LICENSE)
