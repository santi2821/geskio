# GesKio

Gestor de ventas, inventario y cuentas para pequeños comercios, hecho con Python y Flet. Incluye una aplicación de escritorio multiplataforma y una landing estática.

> Prototipo en evolución. En el primer inicio se puede elegir entre usar datos de ejemplo o empezar con el comercio vacío. Los datos se guardan como JSON en el perfil local; todavía no hay una base de datos multiusuario ni sincronización entre dispositivos.

## Funciones

- Panel con ventas, calendario y gráficos.
- Caja, productos, clientes, proveedores y cuentas corrientes.
- Historial de ventas con filtros y detalle de productos, y registro de pagos de fiado.
- Trazabilidad de ventas, anulaciones y ajustes de inventario.
- Apariencia clara y oscura, con ajustes de marca.
- Chat local de solo lectura, con conexión opcional a OpenRouter y permiso explícito antes de compartir el resumen comercial.
- Copias JSON manuales desde Ajustes, con validación previa y confirmación antes de reemplazar los datos.

El historial presenta las ventas por fecha y medio; los pagos de deudas se muestran como cobros aparte en el Dashboard. Los saldos pagados en archivos anteriores se conservan, pero aparecen identificados como importes sin fecha ni medio porque esos datos no estaban guardados.

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

Sin `OPENROUTER_API_KEY`, el chat usa reglas locales sencillas y no envía consultas por internet. Con una clave configurada, muestra un permiso explícito antes de cada sesión remota; la consulta puede incluir el texto, hasta ocho mensajes previos y un resumen de nombres y saldos de clientes, productos, precios, stock y ventas agregadas. No se envían teléfonos, identificadores ni el archivo JSON completo. OpenRouter puede aplicar cargos; revisa sus condiciones. Los pasos están en [`docs/openrouter-local.md`](docs/openrouter-local.md).

En Ajustes podés exportar y restaurar copias JSON de hasta 16 MB. Restaurar reemplaza los datos locales, no los combina. No hay sincronización ni respaldo automático; usa datos de prueba y conserva las copias en un lugar seguro.

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
