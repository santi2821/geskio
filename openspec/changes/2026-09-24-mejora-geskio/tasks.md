# Tareas propuestas

## Fase 0 — Base y control

- [x] 0.1 Crear objetivo explícito para mejorar GesKio con alcance por ciclos.
- [x] 0.2 Guardar ref Git del estado versionado sucio sin mover la rama ni limpiar archivos.
- [x] 0.3 Hacer revisiones independientes de UI, reglas de negocio y roadmap IA.
- [x] 0.4 Comparar código actual con las especificaciones activas; registrar deltas intencionales y corregir docs obsoletas.
- [x] 0.5 Añadir una rutina repetible `python -m unittest discover -s tests -v`, con datos aislados y sin tocar el JSON del usuario.

## Fase 1 — Datos fiables antes de uso real

- [x] 1.1 Añadir validadores de productos compartidos por alta, edición y dominio.
- [x] 1.2 Rechazar cantidades no positivas, stock insuficiente, producto inexistente y fiado sin cliente al crear una venta.
- [x] 1.3 Validar pagos de fiado para impedir importes negativos, no finitos o superiores al saldo.
- [x] 1.4 Bloquear borrado de cliente con historial; una opción de archivo queda pendiente de decisión de producto.
- [x] 1.5 Guardar el costo unitario registrado en cada venta y migrar datos demo v1 sin inventar costos históricos.
- [x] 1.6 Implementar persistencia local JSON versionada para la demo: carga al iniciar, guardado atómico al mutar datos y semilla de ejemplo solo cuando no existe archivo.
- [x] 1.7 Verificar reinicio entre procesos, archivo malformado/versión desconocida y recuperación con ruta temporal; definir backups antes de aceptar datos reales.
- [x] 1.8 Impedir ventas con productos eliminados, precios o stock desactualizados; conservar clientes con historial y rechazar pagos de fiado no finitos o fuera de saldo.

## Fase 2 — UI y funciones principales, sin IA

- [x] 2.1 Auditar Caja en ventana 1100×700 y tamaño estrecho: producto, carrito, total, medio de pago, cobrar, deshacer y errores.
- [x] 2.2 Reordenar Stock alrededor de buscar/estado/acciones; ofrecer movimiento de stock comprensible y edición validada.
- [x] 2.3 Hacer Clientes y Fiado más legibles con historial y estado de deuda/pago claros.
- [x] 2.4 Corregir periodos, contexto de cifras, jerarquía y acciones del Dashboard.
- [ ] 2.5 Organizar Ajustes por Apariencia, Comercio, Datos y Accesibilidad; definir persistencia para cada preferencia.
- [ ] 2.6 Revisar controles con teclado/mouse, etiquetas accesibles, estados vacíos/errores y claro/oscuro.
- [x] 2.7 Reconciliar CSS/JS del sitio y las afirmaciones de landing con comportamiento y distribución existentes.
- [x] 2.8 Historial de ventas con filtros, detalle histórico y total del conjunto filtrado.
- [x] 2.9 Mejorar Caja con vuelto, edición de cantidades y validación de stock acumulado.
- [x] 2.10 Presentar ventas del día por medio y abonos de fiado como cobros separados.
- [x] 2.11 Elegir datos de ejemplo o inicio vacío cuando todavía no hay un archivo local.
- [x] 2.12 Guardar y mostrar el historial de abonos de fiado con fecha e instrumento de cobro.
- [x] 2.13 Registrar ajustes, ventas y anulaciones en el historial de movimientos de stock.
- [x] 2.14 Migrar el estado y los respaldos v1/v2 a v3 sin inventar detalles de abonos ni movimientos históricos.

## Fase 3 — Asistente generativo y Jev para decisiones

- [x] 3.1 Documentar propuesta de contratos JEV (intención, periodo, resultado, origen, confianza y aclaración) y consultas locales allowlisted; aún no implementar.
- [x] 3.2 Usar OpenRouter para el Chat (decisión del usuario del 2026-09-24); configurar la clave solo por entorno y mantener modelo configurable.
- [x] 3.3 Integrar el Chat read-only con snapshot allowlisted, UI asíncrona, límites y errores recuperables; sin margen histórico, tools ni operaciones de escritura.
- [ ] 3.4 Captura por voz opcional: transcripción → borrador de producto editable → validación de dominio → confirmación humana; errores de audio recuperables.
- [ ] 3.5 Sugerencias por campo con procedencia/confianza/aceptar/editar/descartar; costo, precio y stock vacíos si no existe una fuente confiable.
- [ ] 3.6 Playground declarativo para series/gráficas sobre consultas permitidas; sin código arbitrario, mutaciones ni acceso a archivos.
- [ ] 3.7 Ajustes: separar Apariencia, Comercio, Datos, Accesibilidad e IA; cada opción con consumidor, valor inicial y persistencia definida.
- [x] 3.8 Mantener historial efímero, pedir permiso antes de cada sesión remota y permitir borrar el chat; sin clave, no enviar consultas ni exigir permiso externo.
- [x] 3.9 Usar un modelo conversacional concreto (`openai/gpt-6-luna`) por defecto en Chat; conservar `OPENROUTER_MODEL` como override y separar la identidad del asistente del modelo Jev de TypeSafe.
- [x] 3.10a Crear contrato de decisión tipado y clasificador fake/offline para intents allowlisted; enrutar el fallback local y evaluar casos curados sin red.
- [ ] 3.10b Evaluar la API Alpha `/api/alpha/decisions` para clasificación/enrutamiento solo después de medir preguntas anonimizadas, confirmar acceso y decidir habilitar ese provider.

## Cierre de cada ciclo

- [ ] Guardar checkpoint antes de editar y registrar su ref.
- [ ] Limitar cambios a las rutas declaradas; revisar diff frente a checkpoint.
- [ ] Validar las rutas felices, errores y recuperación de ese cambio.
- [ ] Pedir review a un agente en solo lectura y resolver hallazgos antes del siguiente ciclo.
- [x] Registrar qué quedó implementado, qué se verificó y qué sigue siendo una limitación (bitácora del ciclo 15 y `docs/oportunidades-mejora-2026-10-01.md`).

## Bitácora de ciclos

### Ciclo 15 — Mejoras funcionales de ventas, inventario y deuda

- Se implementaron los seis frentes del informe del 1 de octubre y se actualizaron README y documentación de oportunidades.
- El JSON pasó a v3: conserva saldos previos de fiado como `pagado_sin_detalle`; añade el historial de abonos, configuración de primer inicio y libro de movimientos. Restauración y exportación incluyen esos datos.
- Se actualizaron las expectativas de versión en las pruebas existentes y el entorno pytest sigue aislando el JSON y el provider. Se agregaron siete pruebas de regresión para migración v2, abonos, movimientos, inicio vacío, control de Caja y resumen diario.
- Verificación: `python -m pytest -q -W error::DeprecationWarning` — 105 pasaron; `python -m compileall -q app tests`, disponibilidad de las APIs/iconos Flet utilizados y `git diff --check` también pasan.
- Smoke Flet de escritorio, con JSON temporal: se recorrieron bienvenida, Dashboard diario, historial y detalle de ventas, pantalla de abonos y Caja. Se confirmó que «Cobrar» ocupa el ancho disponible; no se registraron ventas ni pagos. El selector real de archivos se cubre fuera del alcance de este ciclo.
- Queda pendiente revisar visualmente los filtros en uso, el vuelto, un pago nuevo, Movimientos y ancho compacto; también una auditoría integral de teclado/lector de pantalla. El checkpoint conserva el estado anterior a las ediciones en `%TEMP%\geskio-before-20261001-025239`.

### Ciclo 1 — Validación de productos

- Alcance: impedir valores vacíos, negativos, no enteros en stock/mínimo y no finitos en costo/precio desde la capa de datos; exponer el motivo en alta/edición de Stock.
- Rutas: `app/datos.py`, `app/screens/stock.py`, `specs/product-data-integrity/spec.md`.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-improvement` (`dd5a569fc275a933751596ade6e92501cac022d0`).
- Verificación: `python -m py_compile app/datos.py app/screens/stock.py` pasó; smoke aislado pasó para creación válida, valores vacíos/negativos/NaN, stock fraccional y rechazo atómico de actualización inválida. Review independiente detectó que `int()` ocultaba el mensaje específico de fracciones; se cambió a parsear como decimal y se repitió la verificación.
- Límites: aún no se recorrió la ruta de error dentro de la UI; el resto de invariantes financieras y persistencia siguen pendientes.

### Checkpoint al cierre del ciclo 1

- `refs/codex/checkpoints/geskio-cycle-1-product-validation` → `11eef7362c94c2931424fbf84a5aeb06d80524b0`.
- La rama visible continúa en el mismo HEAD; el ref retiene el estado versionado al cierre del ciclo.

### Ciclo 3 — Persistencia JSON para demo

- Decisión: JSON local versionado; no usar una base externa ni SQLite en esta demo.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-json-demo` (`b7e5ce84ceac4fe483725f7c37bbc6067368e35e`).
- Alcance: estado de productos, clientes, ventas y cuentas; ruta local estable, carga fail-closed, siembra inicial única, escritura temporal + reemplazo y reversión en memoria si falla el guardado.
- La revisión de agentes confirmó que venta/anulación deben persistirse como una sola mutación y que el cargador debe conservar las referencias a listas que importan las pantallas.
- Verificación aislada: compilación Python; dos procesos con la misma ruta temporal recuperaron producto, cliente, venta, stock y pago sin duplicar semillas; se guardó y volvió a cargar una lista de ventas vacía sin resembrarla; JSON corrupto falló sin sobrescribirse; un fallo de escritura revirtió la mutación en memoria. Tras la revisión final se añadieron y comprobaron las relaciones venta-cuenta: medios de pago, unicidad, suma de artículos y total de deuda.
- Límite de verificación: no se recorrió Caja/Clientes/Fiado en la ventana real con el backend JSON; el smoke cubrió el dominio, no la UI completa. La prueba de versión desconocida y los flujos de CRUD/anulación quedan pendientes.
- Límite: esta persistencia sirve para la demo; antes de datos reales hacen falta respaldo/recuperación probados y revisar la decisión de almacenamiento.

### Ciclo 2 — Alta de producto en diálogo

- Checkpoint previo: `refs/codex/checkpoints/geskio-cycle-1-product-validation`.
- Cambio: la pantalla Stock mantiene búsqueda/tabla como contenido principal y ofrece alta en un diálogo desde el encabezado.
- Criterio: cancelar no cambia el catálogo y descarta borrador; guardar válido cierra y refresca; error deja el diálogo abierto y conserva la entrada, con el mensaje visible en el formulario.
- Cambio adicional: costo y precio vacíos muestran su error específico (el cero explícito sigue siendo permitido); errores antiguos se limpian al corregir o cancelar.
- Revisión independiente: pidió confirmar conservación del movimiento de stock, limpieza visual de errores, costo/precio vacíos y ventana estrecha. Se verificó que el movimiento de stock no forma parte del checkpoint previo (el informe de esa capacidad era incorrecto); el ancho estrecho queda como revisión pendiente. Se resolvieron los errores y los valores vacíos.
- Verificación: `python -m py_compile app/datos.py app/screens/stock.py`, smoke aislado del dominio y `git diff --check` pasaron. En Flet a 1100×700, la lista quedó como contenido principal; Guardar vacío mostró `Poné un nombre`; al completar el nombre, el mensaje pasó a `Ingresá el costo`; un alta con costo/precio válidos cerró y agregó el producto a la tabla. Cancelar cerró y, tras reabrir, el formulario apareció limpio. El proceso local se detuvo después de usar datos de prueba en memoria.
- Riesgo abierto: faltan validar el ancho estrecho y los flujos de edición y movimiento de stock; no se afirma cobertura general del inventario.
- Estado: verificado en el alcance descrito; la ventana estrecha y otros flujos de Stock siguen en 2.2.
- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-2-stock-entry` (captura los archivos versionados y solo los documentos nuevos de esta propuesta; no movió la rama).

- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-3-json-persistence` (captura solo app/datos.py y los cinco documentos de esta propuesta; no mueve la rama ni el índice real).

### Ciclo 4 — Rediseño de interfaz y flujos críticos

- Objetivo: hacer que la demo se sienta como una herramienta coherente de mostrador: identidad GesKio presente, sección actual reconocible, tareas legibles y recuperables; corregir invariantes que podían romper el cierre de caja o el historial.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-ui-redesign` (`981e1538ead1d2f835e60b7c70ddeaeddd89868d`).
- Rutas del ciclo: `app/theme.py`, `app/widgets.py`, `app/main.py`, `app/screens/{dashboard,ajustes,caja,clientes,fiado,stock,chat}.py`, `app/datos.py` y esta bitácora.
- Cambios visuales: shell con marca, navegación agrupada y Ajustes al pie; barra superior con sección y fecha; fondo de trabajo neutro, panel destacado de Hoy, valores con roles semánticos, alertas limitadas con accesos a Stock/Fiado, encabezados explicativos y controles accesibles de marca/acento. Ajustes muestra la ubicación real del JSON local.
- Retención de estado: el selector día/semana/mes se conserva al reconstruir Dashboard y Chat conserva mensajes al volver a la pestaña.
- Bugs críticos cerrados: el dominio vuelve a validar existencia, precio y stock del carrito; Caja conserva el carrito y explica cómo corregir un precio/producto obsoleto. No se puede borrar un cliente con ventas/cuentas relacionadas. Fiado rechaza NaN/infinito y montos fuera de saldo con feedback visible.
- IA: no se agregó provider ni capacidades nuevas; el chat conserva su estado actual. JEV, voz, sugerencias y Playground permanecen en la hoja de ruta.
- Verificación: compilación y construcción aislada de las siete pantallas; smoke local aislado de validación de venta y pago. Contraste de tokens principal/acento/estados mayor o igual a 4.5:1 en cuatro paletas. Revisión visual web de Dashboard en navegador a 1480×1270. Queda revisar flujos con interacción real, tamaño estrecho, tema oscuro, teclado/accesibilidad y regresión Caja/Clientes/Fiado.
- Revisión independiente: UI detectó el título superior vacío, pérdida de estado al rearmar y alertas sin límite; se atendieron en este ciclo. La segunda revisión no encontró fallos críticos de shell, headers, tokens, Ajustes ni contratos.
- Límites: el rediseño mejora la capa compartida y jerarquía; no implica auditoría completa pixel a pixel de cada diálogo, ni validación de todos los flujos de comercio.
- Segundo review de dominio: confirmó las guardas de venta, la retención de historial de clientes y el rechazo de pagos no finitos o fuera de saldo. Se limpió también una selección de cliente que ya no existe al refrescar Caja.
- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-4-ui-refresh` (captura cambios versionados y documentos declarados para este ciclo; no mueve la rama ni el índice real).

### Ciclo 5 — Dirección formal de producto

- Objetivo: reemplazar la estética de demo anterior por una interfaz formal, sobria y orientada a la operación diaria.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-formal-ui` (`bc89e9c5113f01e1784d63ee873c72a63e5532eb`).
- Alcance: `app/theme.py`, `app/widgets.py`, encabezados de las siete pantallas, specs `app-shell` y `dashboard-composition`, y esta propuesta.
- Cambios: fondos neutrales fríos, superficies/bordes/radios compactos, cifras mayormente neutrales y estados semánticos, wordmark sin tile/claim, títulos de tarea que no repiten el nombre superior. En Dashboard, gráfico y alertas se apilan bajo 1200 px de ventana para que no se recorte la columna de alertas.
- IA: provider continúa pendiente; no agregar nuevas capacidades de IA en este ciclo.
- Revisión independiente: aceptó la dirección formal y confirmó que marca, superficies, títulos y escala coinciden con la tesis. Recomendó dejar abierta la aceptación visual completa por el espacio vertical libre en ventanas muy altas; no editó archivos.
- Verificación: compilación de módulos Python y construcción aislada de las siete pantallas; screenshot web de Dashboard y Caja a 1480×1270; revisión de Dashboard a 1100×700 detectó y corrigió el recorte de alertas mediante apilado de columnas; contraste de texto/superficie mutado ≥4.98:1 y primario/on-primary ≥6.06:1 en las cuatro paletas; `git diff --check` pasó. La construcción detectó un import faltante de `FS_13` y quedó corregido antes de repetir las siete pantallas.
- Límites: el Dashboard conserva contenido compacto y deja superficie neutra libre en ventanas muy altas (1480×1270); no se añadieron paneles de relleno. Interacción real de compra, ancho compacto, contraste de elementos individuales, teclado, lector de pantalla y tema oscuro requieren validación posterior. A 1100×700 Alertas pasa debajo del gráfico para evitar recortes y queda accesible con scroll vertical.
- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-5-formal-ui`; rama e índice Git real preservados.
- Límites: contraste completo, navegación por teclado, tema oscuro y anchos compactos requieren validación manual posterior.

### Ciclo 6 — Pulido redondeado y controles coherentes

- Objetivo: conservar el estilo formal aceptado y dar más calidez con radios graduales, campos consistentes y foco visible.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-rounding-polish`.
- Alcance: tokens de radio, widgets compartidos, controles TextField/Dropdown de pantallas, specs de tokens/widget kit y este registro.
- Reglas: 8 px para botones/controles compactos, 10 px para campos y tarjetas, 16 px para paneles mayores; no redondear celdas por decoración. Campos con borde neutral y foco primario de 2 px.
- Cambios: se reutilizan `campo_texto()` y `selector()` con radios/foco homogéneos; se redondearon tarjetas, secciones, diálogos y marco por nivel. Ajustes presenta claro/oscuro y color base sin ocupar la pantalla con seis botones saturados; los tonos personalizados quedan tras «Color de acento» y se muestran como muestras circulares con etiqueta accesible.
- Verificación: compilación de 10 módulos de pantalla/tema/widgets; comprobación del constructor de muestra como `IconButton` circular con tooltip; radios/foco de `campo_texto()` y `selector()` comprobados previamente; `git diff --check` pasó (solo avisos de conversión LF/CRLF). Las capturas web de Dashboard, Caja y Ajustes y el foco visible del campo se revisaron previamente en este ciclo.
- Revisión independiente: conservó la dirección formal, recomendó hacer las muestras de acento controles de teclado nativos; se cambió `Container` por `IconButton` circular y se verificó su forma, clase de control y etiqueta. La activación con teclado en navegador aún requiere recorrido manual.
- Limitaciones pendientes del frontend completo: estados hover/pressed/disabled/error siguen por auditar; gráfica de Dashboard necesita mejores referencias de escala; oscuro, teclado completo y ancho compacto siguen pendientes.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-rounding-polish` (`05b56de477ddbb2a56e5c2d01cf1c8f4605ff528`).
- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-6-rounding-polish` (captura cambios versionados y los cinco documentos de esta propuesta; no mueve la rama ni el índice real).

### Ciclo 7 — Pruebas de regresión y plan IA aprobable

- Objetivo: cubrir los flujos disponibles con pruebas aisladas, reparar defectos que puedan corromper/invalidar el JSON y dejar una hoja de ruta IA que se pueda aprobar por fases, sin provider.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-full-test-review` (`7f1eab41767d0672f4c11f75eb94b274de5611ac`).
- Hallazgos reproducidos: alta de cliente aceptaba nombre vacío/teléfono no textual y podía hacer que el siguiente inicio rechazara el archivo; venta aceptaba `pago="banana"`; chat respondía los mismos agregados para “hoy” y “mes”, no aclaraba “ventas” y usaba costo actual como ganancia histórica; Dashboard presentaba esa cifra como ganancia exacta; landing afirmaba pérdida de datos, pago con tarjeta y previsualización de margen no presentes; radios CSS distintos de los tokens de app.
- Correcciones: validar/normalizar cliente en creación y edición, limitar pago a medios existentes, validar medio y referencias cliente/cuenta al cargar JSON; construir cada línea de venta desde el catálogo y aislarla de los objetos que Caja entrega; rechazar booleanos en campos numéricos de producto, movimientos fraccionarios/cero y ajustes que dejarían stock negativo; validar producto y precio frente al catálogo; Chat local ahora distingue hoy/mes/últimos 7 días, pregunta ante periodo ambiguo, agrega deuda por cliente y advierte que la ganancia histórica no es confiable; Dashboard etiqueta la cifra como estimación mensual, la colorea según signo y explica su límite; reconciliar landing, radios y spec de Dashboard con la app.
- Pruebas persistentes: `tests/test_geskio.py`, con directorio temporal por caso y sin dejar `GESKIO_DATA_FILE` alterado al importar. Cobertura de CRUD de cliente/producto, movimientos de stock y recarga/canonicalización del JSON, carrito repetido y stock exacto, agregados, cobro/pago/anulación, rechazos financieros, rollback al fallar escritura, archivo corrupto/versión desconocida, reabrir desde otro proceso, consultas y aclaración de periodo del Chat, build aislado de siete pantallas, breakpoints puros, periodos del Dashboard y enlaces/claims/radios de la landing.
- Verificación: 22 tests de unittest, compilación de módulos Python, sintaxis Node de 6 scripts JS, enlaces locales/anclas HTML y `git diff --check` (los comandos completaron sin errores; Git emitió solo avisos LF→CRLF).
- Review independiente: agentes reprodujeron defectos de dominio y discrepancias de UI; la revisión IA propuso dependencias, criterios y una puerta de provider. Se retiró la promesa falsa de previsualización de margen, se corrigió el color verde de la estimación negativa y se cerraron gaps de tipos persistidos y carrito repetido. El review final confirmó que el test consulta el producto reconstruido y que el aislamiento temporal sirve para esta suite; el estado global mutable del módulo es un riesgo bajo si más adelante se agregan suites que importen `datos` en el mismo proceso.
- Plan IA: fases A–F en `proposal.md`, arquitectura/gate de provider en `design.md` y tareas detalladas aquí. El provider no fue elegido, configurado ni conectado.
- Límites: Flet se probó mediante construcción aislada de todos los árboles y arranque HTTP 200 con JSON temporal, no con automatización interactiva completa del navegador. Caja en ancho compacto, teclado/lector de pantalla, tema oscuro y backup/restore siguen pendientes. El chat de keywords continúa siendo un prototipo limitado, no IA. El costo histórico por venta sigue sin guardarse, por eso Chat rehúsa reportar ganancia histórica confiable.
- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-7-full-validation` (cambios de ciclo aislados mediante índice alterno; no mueve la rama ni modifica el índice real).

### Ciclo 8 — JEV Chat con OpenRouter y menús de Caja

- Objetivo: responder consultas de solo lectura sobre datos de GesKio con OpenRouter y garantizar opciones iniciales en los selectores de Caja.
- Checkpoint previo: `refs/codex/checkpoints/geskio-before-openrouter-chat-dropdown` (`062edc38b81ffe26369d14309d102518f178fda6`).
- Hallazgo UI: Cliente y Producto se construían sin opciones y solo se rellenaban al refrescar/tras cobrar; Pago sí tenía opciones. Débito/Crédito aparecían como opciones aunque el dominio las rechaza.
- Cambios: cliente HTTP estándar al endpoint OpenRouter, clave/modelo por entorno, contexto minimizado con máximo de 18.000 caracteres, aviso explícito y checkbox de consentimiento por sesión, historial efímero y manejo asíncrono de espera/errores. El consentimiento ahora especifica que se envían la consulta, el resumen y hasta ocho mensajes previos; puede retirarse desmarcando. Contexto excluye teléfonos, IDs, filas individuales de venta y JSON completo; incluye nombres/saldos por cliente tras consentimiento. Sin tools ni mutaciones. Selectores de Caja reciben options antes del primer render; medios de pago limitados a los admitidos por dominio.
- Pruebas: `tests/test_jev.py` (contexto y privacidad, presupuesto de contexto, prompt/historial, transporte simulado, clave ausente, error 401, respuesta malformada/límite de tamaño, autorización y recorrido async de UI); regresión de options en primera construcción dentro de `test_geskio.py`. Suite completa: 34 tests pasan. Navegador local confirmó clic real de consentimiento y desplegables con opciones visibles para Cliente, Producto y Pago. Sin clave disponible no se hace request real.
- Revisión independiente: detectó y ayudó a cerrar el desfase entre el texto de consentimiento y el historial que se transmite. Revisión del cliente OpenRouter no halló defectos bloqueantes tras los límites, minimización y mensajes de error agregados.
- Verificación final: `python -m unittest discover -s tests -v` (34 OK), `python -m compileall -q app tests` y `git diff --check` (OK; solo avisos de conversión LF→CRLF).
- Guía de clave y modelo: `docs/openrouter-local.md`.
- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-8-openrouter-chat-dropdown` (índice alterno; rama e índice real preservados).

### Ciclo 9 — Modelo de Chat explícito y separación de Jev

- Hallazgo: se usó `openrouter/auto` como predeterminado y se identificó al asistente conversacional como JEV. La investigación confirmó que Jev de TypeSafe es otra clase de modelo: salida `choice`, `score` o `noul`, sin texto libre, y OpenRouter lo ofrece por su API Alpha `/api/alpha/decisions`, no por Chat Completions.
- Cambio: Chat usa `openai/gpt-6-luna` (modelo de texto normal) por defecto y mantiene el override `OPENROUTER_MODEL`. La UI habla del asistente de GesKio sin confundirlo con el modelo Jev.
- Recomendación: reservar Jev para clasificar/intencionar el chat y elegir rutas/querys allowlisted si evals locales validan precisión/umbral/fallback. Para voz hace falta Speech-to-Text separado; para crear texto arbitrario/producto o generar prosa/gráficos se mantiene un LLM de texto con salidas validadas por esquema. No usar Jev para audio ni redacción.
- Verificación: suite completa, 35 tests OK; `python -m compileall -q app tests` y `git diff --check` OK (avisos Git de normalización LF/CRLF en archivos existentes). Los tests HTTP y UI verifican el modelo predeterminado y el fallback cuando el override está vacío. Sin clave no se hizo llamada externa.
- Revisión de plan/modelo: confirmó la separación entre chat generativo, clasificación estructurada, transcripción de audio y DSL de Playground; validó el encaje de consultas allowlisted y fallback local.
- Checkpoint de cierre: `refs/codex/checkpoints/geskio-cycle-9-chat-model-jev-roadmap` (índice alterno; rama e índice real preservados).

### Ciclo 10 — Sincronización y mejoras integrales en `codex/geskio-complete`

- Base: `origin/main` sincronizado en `36780104fffec9cd8bf146f8d2e8ba08faa9e1aa`; rama creada para este ciclo. Checkpoint previo: `refs/codex/checkpoints/geskio-complete-before-core`.
- Datos: versión 2 del JSON guarda el costo de cada línea nueva; la migración v1 conserva margen histórico como desconocido. Dashboard, Chat y snapshot remoto excluyen las ventas heredadas sin costo verificable.
- Recuperación: copias JSON manuales, límite de 16 MB tanto al exportar como al leer, lectura validada, reemplazo atómico, previsualización y confirmación antes de restaurar. Se conserva la ubicación local y se avisa que las copias incluyen teléfonos y saldos.
- Chat: modo local sin red ni consentimiento de OpenRouter; modo externo con clave requiere autorización. Si el provider falla, la respuesta identifica el fallback local sin mostrar detalles privados. La interfaz identifica la demo, usa tokens para claro/oscuro y permite borrar borradores/historial; se evita la etiqueta engañosa «En vivo».
- Calidad adicional: se corrigió la búsqueda de proveedores para usar el valor más reciente del evento Flet y se reemplazaron APIs deprecadas de Flet en componentes editados; landing, README y guía de OpenRouter describen las funciones reales.
- Pruebas: `python -m pytest -q -W error::DeprecationWarning` — 84 pasaron, incluidas migración, margen histórico, backups, límite de tamaño, rollback, privacidad del Chat, modo local, consentimiento remoto y controles de Ajustes. `tests/conftest.py` usa JSON temporal y elimina cualquier clave de provider para la suite.
- Recorrido Flet: las ocho pantallas renderizan; tema claro/oscuro cambia y se puede restaurar; Ajustes hace scroll a 900×600 y mantiene visibles los controles. El selector/descarga de archivo real del navegador no quedó comprobado en el navegador integrado; los métodos de escritorio/web están cubiertos con el FilePicker simulado.
- Sigue pendiente el ancho compacto en Caja y la auditoría completa de teclado/lector de pantalla. Voz requiere decidir una solución de transcripción y consentimiento de micrófono; sugerencias necesitan una fuente de datos confiable; Jev Alpha y un Playground mayor requieren evaluación de producto y límites. No se conectó ningún provider ni se enviaron datos reales.

### Ciclo 11 — Caja adaptable, carrito visible y auditoría de cierre

- Alcance: `app/screens/caja.py`, `app/widgets.py`, `app/theme.py`, `openspec/specs/design-tokens/spec.md`, `tests/test_caja.py`, `tests/test_dimensionamiento.py`, `tests/test_responsive_frame.py` y esta bitácora.
- Caja usa filas responsivas para apilar controles en móvil; el carrito visible es un `ListView` acotado que crece con sus artículos; se retiró la lista invisible de compatibilidad. Cantidad conserva su etiqueta completa, el botón Agregar mantiene ancho legible y quitar un artículo anuncia su nombre.
- El marco usa ancho/alto reales de `Page`, se suscribe a `on_resize` y conserva cualquier callback previo; el encabezado oculta la fecha larga en ventanas estrechas.
- Verificación visual Flet al iniciar a 1100×700 y 390×844: barra lateral expandida/compacta, campos y botón sin recortes, y total/Cobrar accesibles al desplazar. `test_responsive_frame.py` simula los eventos de resize. La sesión local persistió solo en un JSON temporal.
- Los tests de pantalla ejecutan agregar/acumular/quitar, errores de cantidad/stock/precio, fiado sin cliente, cobro y deshacer con datos temporales. La interfaz integrada mostró las pantallas y abrió el selector, pero el control remoto de navegador no envió el evento del botón Agregar; ese límite se cubrió con el test aislado de flujo de Caja.
- Verificación completa: `python -m pytest -q -W error::DeprecationWarning` — 90 pasaron; `python -m compileall -q app tests` y `git diff --check` pasan. No se registra una venta real.

### Ciclo 12 — Reconciliación del alcance visual ya implementado

- Revisión de `stock.py`, `clientes.py`, `fiado.py`, `dashboard.py`, `widgets.py` y la suite confirma que los trabajos 2.2–2.4 ya estaban implementados por ciclos anteriores: búsqueda/filtro/paginación y edición/movimiento validado; deudas con importes pagados/pendientes, antigüedad y estado; periodos del Dashboard con margen de costos registrados y alertas limitadas.
- Se actualizaron las casillas pendientes para que el roadmap no presente como faltantes funciones existentes. El Dashboard excluye las ventas antiguas sin costo de su margen, según el ciclo 10.
- Se reconciliaron las especificaciones de shell, tokens, dashboard, tablas y widgets con las APIs, paletas y margen registrados que usa el código. `brand-alignment` distingue las decisiones históricas del contrato actual: copy factual puede cambiar, landing conserva layout/flows, y las mejoras de integridad pueden modificar `datos.py`.
- Se centralizaron los límites de altura mínima, crecimiento por artículo y altura máxima del carrito en `theme.py`; Caja y sus pruebas usan los mismos tokens.
- Verificación final tras el pulido: 90 pruebas con `-W error::DeprecationWarning`, compilación de `app` y `tests`, y `git diff --check` sin errores. La base continúa igualada con `origin/main` (`3678010`).
- No se marcan como terminadas las preferencias sin consumidor definido, la revisión manual integral de accesibilidad/teclado, voz sin proveedor Speech-to-Text elegido, sugerencias sin fuente confiable, Playground ni la evaluación remota de Jev Alpha; requieren decisiones de producto, proveedor o validación que la suite no puede demostrar.

### Ciclo 13 — Contrato local tipado para Jev

- Se implementaron `JevRequest`, `JevDecision`, enums cerrados de intención/periodo/fuente y confianza validada en `app/jev/contract.py`; `app/jev/fake.py` es determinista, no importa la capa de datos y no realiza red ni acciones.
- El Chat local enruta por las decisiones a sus consultas de solo lectura existentes. Ventas y margen registrado sin periodo solicitan aclaración; las intenciones fuera del catálogo devuelven ejemplos admitidos.
- Evaluación fija de nueve consultas curadas: 9/9 intenciones y periodos esperados. Es una prueba de implementación, no una medida de precisión con usuarios reales; Jev TypeSafe/OpenRouter Alpha no se conectó.
- Pruebas añadidas de contrato inmutable, rango de confianza, unknown/clarification y enrutamiento del Chat; la suite completa se repitió tras integrar el cambio.

### Ciclo 14 — Ajustes transparentes para el asistente

- Rama: `codex/geskio-complete`. Checkpoint de respaldo creado fuera del repositorio porque la política rechazó escribir un ref Git: `%TEMP%\geskio-cycle-14-before-settings-20260927-003524` (diff completo del árbol rastreado y copias de los tres archivos Jev nuevos; el índice y los artefactos ajenos quedaron intactos).
- Alcance: `app/jev/openrouter.py`, `app/screens/ajustes.py`, `app/screens/chat.py`, `tests/test_ajustes.py`, `tests/test_jev.py`, `proposal.md`, `design.md` y esta bitácora.
- Ajustes ahora explica el modo local/remoto, el modelo activo, que una clave detectada todavía debe validarse, el permiso por sesión, los posibles cargos y las clases de datos que se envían/excluyen. El resumen de configuración no contiene el valor de `OPENROUTER_API_KEY` y sanitiza etiquetas de modelo inválidas; el indicador del Chat usa la misma fuente.
- Pruebas nuevas comprueban ambos modos de Ajustes, que la clave no aparezca en la UI/objeto de configuración y el uso de modelo predeterminado/override. Smoke visual del Flet en 390×844 confirmó que Asistente y Datos siguen accesibles con scroll.
- La revisión documental del ciclo corrigió descripciones que seguían diciendo que no había copias manuales y que el margen histórico usaba siempre el costo actual.
- Verificación completa: 98 pruebas con `-W error::DeprecationWarning`, compilación Python, seis scripts JavaScript y `git diff --check`.
- Alcance parcial de 2.5/3.7: se agregó la categoría Asistente, pero no se inventaron preferencias de Comercio o Accesibilidad sin consumidores definidos; la revisión manual integral de teclado/lector de pantalla sigue abierta.
