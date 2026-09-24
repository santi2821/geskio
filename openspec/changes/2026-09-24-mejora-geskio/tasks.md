# Tareas propuestas

## Fase 0 — Base y control

- [x] 0.1 Crear objetivo explícito para mejorar GesKio con alcance por ciclos.
- [x] 0.2 Guardar ref Git del estado versionado sucio sin mover la rama ni limpiar archivos.
- [x] 0.3 Hacer revisiones independientes de UI, reglas de negocio y roadmap IA.
- [ ] 0.4 Comparar código actual con las especificaciones activas; registrar deltas intencionales y corregir docs obsoletas (landing reconciliada; especificaciones de módulos pendientes).
- [x] 0.5 Añadir una rutina repetible `python -m unittest discover -s tests -v`, con datos aislados y sin tocar el JSON del usuario.

## Fase 1 — Datos fiables antes de uso real

- [x] 1.1 Añadir validadores de productos compartidos por alta, edición y dominio.
- [x] 1.2 Rechazar cantidades no positivas, stock insuficiente, producto inexistente y fiado sin cliente al crear una venta.
- [x] 1.3 Validar pagos de fiado para impedir importes negativos, no finitos o superiores al saldo.
- [x] 1.4 Bloquear borrado de cliente con historial; una opción de archivo queda pendiente de decisión de producto.
- [ ] 1.5 Guardar costo/precio unitarios en ventas para mantener el historial; migrar datos demo con cuidado.
- [x] 1.6 Implementar persistencia local JSON versionada para la demo: carga al iniciar, guardado atómico al mutar datos y semilla de ejemplo solo cuando no existe archivo.
- [x] 1.7 Verificar reinicio entre procesos, archivo malformado/versión desconocida y recuperación con ruta temporal; definir backups antes de aceptar datos reales.
- [x] 1.8 Impedir ventas con productos eliminados, precios o stock desactualizados; conservar clientes con historial y rechazar pagos de fiado no finitos o fuera de saldo.

## Fase 2 — UI y funciones principales, sin IA

- [ ] 2.1 Auditar Caja en ventana 1100×700 y tamaño estrecho: producto, carrito, total, medio de pago, cobrar, deshacer y errores.
- [ ] 2.2 Reordenar Stock alrededor de buscar/estado/acciones; ofrecer movimiento de stock comprensible y edición validada.
- [ ] 2.3 Hacer Clientes y Fiado más legibles con historial y estado de deuda/pago claros.
- [ ] 2.4 Corregir periodos, contexto de cifras, jerarquía y acciones del Dashboard.
- [ ] 2.5 Organizar Ajustes por Apariencia, Comercio, Datos y Accesibilidad; definir persistencia para cada preferencia.
- [ ] 2.6 Revisar controles con teclado/mouse, etiquetas accesibles, estados vacíos/errores y claro/oscuro.
- [x] 2.7 Reconciliar CSS/JS del sitio y las afirmaciones de landing con comportamiento y distribución existentes.

## Fase 3 — Asistente generativo y Jev para decisiones

- [x] 3.1 Documentar propuesta de contratos JEV (intención, periodo, resultado, origen, confianza y aclaración) y consultas locales allowlisted; aún no implementar.
- [x] 3.2 Usar OpenRouter para el Chat (decisión del usuario del 2026-09-24); configurar la clave solo por entorno y mantener modelo configurable.
- [x] 3.3 Integrar el Chat read-only con snapshot allowlisted, UI asíncrona, límites y errores recuperables; sin margen histórico, tools ni operaciones de escritura.
- [ ] 3.4 Captura por voz opcional: transcripción → borrador de producto editable → validación de dominio → confirmación humana; errores de audio recuperables.
- [ ] 3.5 Sugerencias por campo con procedencia/confianza/aceptar/editar/descartar; costo, precio y stock vacíos si no existe una fuente confiable.
- [ ] 3.6 Playground declarativo para series/gráficas sobre consultas permitidas; sin código arbitrario, mutaciones ni acceso a archivos.
- [ ] 3.7 Ajustes: separar Apariencia, Comercio, Datos, Accesibilidad e IA; cada opción con consumidor, valor inicial y persistencia definida.
- [ ] 3.8 Aprobar historial del chat, permisos/retención, controles de privacidad y comportamiento sin red antes de persistir prompts o enviar datos.
- [x] 3.9 Usar un modelo conversacional concreto (`openai/gpt-6-luna`) por defecto en Chat; conservar `OPENROUTER_MODEL` como override y separar la identidad del asistente del modelo Jev de TypeSafe.
- [ ] 3.10 Prototipar Jev (TypeSafe System One) con contrato typed y fake offline; evaluar la API Alpha `/api/alpha/decisions` para clasificación/enrutamiento solo tras una evaluación local útil.

## Cierre de cada ciclo

- [ ] Guardar checkpoint antes de editar y registrar su ref.
- [ ] Limitar cambios a las rutas declaradas; revisar diff frente a checkpoint.
- [ ] Validar las rutas felices, errores y recuperación de ese cambio.
- [ ] Pedir review a un agente en solo lectura y resolver hallazgos antes del siguiente ciclo.
- [ ] Registrar qué quedó implementado, qué se verificó y qué sigue siendo una limitación.

## Bitácora de ciclos

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
