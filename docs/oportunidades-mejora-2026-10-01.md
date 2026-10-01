# Mejoras de GesKio para el 2 de octubre de 2026

Revisión inicial del código local realizada el 1 de octubre. La sección «Entrega recomendada» conserva el alcance original. La ejecución del 2 de octubre aplicó también las otras oportunidades priorizadas; el informe de implementación, migración, documentación y comprobaciones aparece al final.

## Estado verificado

- La línea base de la revisión pasó 98 pruebas; después de aplicar las mejoras pasan 105 con `python -m pytest -q -W error::DeprecationWarning`.
- Ya existen búsqueda y paginación en Stock, Clientes y Fiado; alertas, margen con costo histórico, temas y copias JSON manuales. No conviene presentarlos como funciones nuevas.
- Hay cambios locales previos extensos en la rama `codex/geskio-complete`; esta revisión no los reemplaza.
- Además de revisar código y pruebas, se hizo un recorrido Flet de escritorio con un JSON temporal: bienvenida, Dashboard diario, historial y detalle de ventas, consulta de abonos y controles de Caja. No se registraron pagos ni ventas durante la revisión. No se llamó a OpenRouter.

## Oportunidades detectadas

| Prioridad | Zona | Mejora concreta | Esfuerzo orientativo | Valor |
| --- | --- | --- | --- | --- |
| 1 | Ventas | Historial con filtros por fecha y medio de pago, búsqueda de cliente y detalle de productos | 4–7 horas | Permite revisar operaciones anteriores y demostrar un flujo nuevo completo |
| 2 | Caja | Importe recibido y vuelto para efectivo, editar cantidades en el carrito y validar stock acumulado | 2–4 horas | Reduce pasos y errores durante una venta |
| 3 | Dashboard | Resumen de ventas de hoy separado en efectivo, transferencia y fiado | 1–3 horas | Da una lectura comercial inmediata con datos existentes |
| 4 | Inicio y Ajustes | Elegir entre probar la demo o empezar con un comercio vacío | 3–6 horas | Facilita usar la app con datos propios sin mezclarlos con ejemplos |
| 5 | Fiado | Historial de cada abono: fecha, importe y medio de pago; detalle por cliente | 1–2 días | Permite explicar cómo se llegó al saldo y cuándo se recibió el dinero |
| 6 | Stock | Registrar ajustes con motivo, fecha, cantidad anterior y nueva | 1–2 días | Hace trazables las entradas, pérdidas y correcciones |

## Evidencia y límites

### Historial de ventas

`app/screens/dashboard.py:81` muestra las ventas de hoy como filas de texto. El menú de `app/main.py:24` no incluye una pantalla de historial. `app/datos.py:772` ya guarda fecha, cliente, productos, cantidades, precio, costo, total y medio de pago.

Una primera entrega puede ser de solo lectura y reutilizar esos registros, sin cambiar el formato JSON. Los datos actuales tienen fecha, pero no hora: no inventar horarios para operaciones anteriores. Mantener fuera de esta entrega la anulación desde el historial; hoy `deshacer_venta` borra la venta y su cuenta de fiado, y requiere revisar el caso de cuentas con pagos previos antes de ampliar su acceso.

### Caja

`app/screens/caja.py:82` tiene cliente, medio de pago, producto, cantidad, carrito y total. No tiene importe recibido, vuelto ni controles para editar la cantidad de una fila; se puede quitar el artículo completo.

Fallo reproducido en `app/screens/caja.py:387`: la validación al agregar compara solo la cantidad nueva con el stock, sin sumar lo que ya está en el carrito. Con stock 5, agregar 3 dos veces deja cantidad 6 sin aviso. `cobrar_carrito` sí bloquea la venta: en la reproducción no se crearon ventas ni se redujo el stock. La mejora debe impedir el exceso al agregar y conservar la validación al cobrar.

### Resumen diario

Las ventas guardan su medio de pago, por lo que se pueden agrupar sin migración. Llamarlo «Ventas por medio de pago», no «Saldo de caja» ni «Dinero disponible»: faltan gastos, apertura de caja y movimientos de efectivo. Los abonos de fiado solo incrementan un total acumulado; no tienen fecha ni medio de cobro para reconstruir ingresos diarios.

### Inicio con datos propios

`app/datos.py:934` crea operaciones de ejemplo automáticamente cuando no existe un archivo previo. Proponer una elección explícita antes de inicializar un comercio nuevo. Conservar los archivos existentes y evitar cualquier limpieza automática de datos.

### Pagos y movimientos

`app/datos.py:819` aumenta `pagado` sin guardar cada abono. `app/datos.py:604` modifica el stock sin registrar el motivo. Ambas mejoras requieren extender el modelo y validar la compatibilidad de las copias antiguas; son más grandes que una mejora pequeña para mañana.

## Entrega recomendada: historial de ventas

Alcance mínimo:

1. Entrada «Ventas» en el menú y listado paginado, con las fechas más recientes primero.
2. Filtros «Hoy», «Últimos 7 días» y «Todas», medio de pago y búsqueda de cliente.
3. Columnas de fecha, cliente/Mostrador, medio de pago y total.
4. Acción «Ver detalle» con producto, cantidad, precio unitario y subtotal.
5. Cantidad de operaciones y total del conjunto filtrado, antes de paginar.
6. Mensajes distintos para historial vacío y filtros sin resultados.

Criterios de aceptación:

- Una venta nueva aparece al entrar al historial y sigue disponible después de reiniciar.
- Una venta a Mostrador se muestra sin exigir cliente.
- El detalle usa nombres, precios y costos guardados en la venta, aunque luego cambie el catálogo.
- Fechas y medios de pago filtran correctamente; los totales se calculan sobre todo el resultado filtrado.
- Consultar o filtrar no modifica ventas, stock ni deudas.
- Verificar en ventana de escritorio y ancho compacto, con datos temporales; ejecutar la suite actual y pruebas de filtros y detalle histórico.

Si el tiempo disponible es inferior a cuatro horas, priorizar Caja: validación acumulada de stock y cálculo de vuelto. No introducir pagos mixtos, descuentos, impresión ni conexiones nuevas en esa entrega.

## Implementación del 2 de octubre

Se implementaron las seis áreas priorizadas:

- **Ventas:** pantalla paginada con filtros por hoy/últimos 7 días/todas, medio de pago, búsqueda por cliente y detalle del recibo. El resumen cuenta y suma todos los resultados filtrados, no solo la página visible. Las líneas leen costo, precio y nombre guardados en la venta.
- **Caja:** muestra el importe recibido para efectivo, calcula el vuelto y rechaza importes insuficientes; vacío significa pago exacto. Se puede sumar o restar una unidad desde el carrito, quitar un producto y limpiar el carrito. Se valida la cantidad acumulada contra el stock tanto al añadir como al cobrar.
- **Dashboard:** agrupa ventas de hoy por efectivo, transferencia y fiado; presenta en separado los abonos cobrados hoy y su medio.
- **Primer inicio:** si no hay un archivo de datos, una bienvenida ofrece datos de muestra o un comercio vacío. La selección se guarda localmente y no vuelve a aparecer. Los archivos existentes continúan cargándose directamente.
- **Fiado:** cada abono nuevo persiste fecha, importe y medio de cobro, y se puede consultar desde la cuenta. Los abonos acumulados migrados se mantienen como `pagado_sin_detalle` y se explican sin inventar fechas ni medios.
- **Inventario:** los ajustes y los cambios de cantidad al editar un producto guardan motivo y cantidades anterior/nueva. Las ventas y anulaciones también registran el cambio de stock. «Movimientos» permite buscar y paginar el historial.

Los requisitos de las nuevas funciones también quedaron separados en `openspec/specs/sales-history/`, `cashier-controls/`, `first-run-choice/`, `debt-payment-history/` e `inventory-movement-history/`.

### Persistencia y alcance histórico

El formato JSON es v3. Al leer archivos v1 se migran las líneas al costo histórico desconocido; v1 y v2 también inicializan registros de movimientos vacíos, preservan los saldos y anotan los pagos antiguos sin detalle. El historial de movimientos comienza al actualizar: los cambios de stock históricos no se pueden reconstruir. Las ventas antiguas siguen visibles si el archivo las conserva. La restauración y exportación de copias v1/v2/v3 mantienen el control de validación existente.

La opción «Vacío» se puede seleccionar solo durante el primer inicio. La app no borra ni cambia un archivo ya existente para permitir cambiar de modo.

### Documentación y revisión

Se actualizó el README y los casos de prueba preexistentes que nombraban el formato v2. Se agregaron siete pruebas de regresión en `tests/test_cycle15_features.py`. Se creó un checkpoint antes de editar en `%TEMP%\geskio-before-20261001-025239`; contiene un ZIP de 87 archivos, sus hashes SHA-256, el diff previo y el estado de Git. No se incluyeron `.atl/`, `.playwright-mcp/` ni logs temporales.

La suite completa pasa: `python -m pytest -q -W error::DeprecationWarning` — 105 pruebas. También pasan `python -m compileall -q app tests`, la comprobación de los iconos y APIs Flet usados, y `git diff --check`. En el smoke visual de escritorio se comprobó la bienvenida, navegación, Dashboard del día, listado y detalle de ventas, consulta de abonos, controles de Caja y ancho completo del botón «Cobrar»; se usó un archivo JSON temporal. No se registraron operaciones. Quedan sin recorrido visual compacto los filtros en uso, el flujo de vuelto, el pago de un abono y la pantalla de movimientos; tampoco se hizo auditoría integral de teclado/lector de pantalla. El checkpoint permite recuperar íntegramente los archivos previos.
