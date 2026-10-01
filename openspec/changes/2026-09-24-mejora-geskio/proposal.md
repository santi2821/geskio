# Propuesta: mejora integral de GesKio

## Objetivo

Convertir GesKio en una app de escritorio clara y confiable para atender un comercio de barrio. Mantener la secuencia de confiabilidad del core y avanzar primero con un Chat generativo; Jev de TypeSafe se reserva para decisiones estructuradas. El usuario eligió OpenRouter como provider el 2026-09-24; voz, autocompletado y Playground continúan postergados.

## Estado observado

- La app Flet ya tiene Dashboard, Caja, Stock, Clientes, Fiado, Chat y Ajustes, pero el árbol de trabajo contiene una reescritura amplia sin commit que requiere reconciliarse con las especificaciones activas.
- Los datos de la demo persisten como JSON versionado bajo la carpeta local del usuario. Ajustes ofrece exportación y restauración manuales de copias de hasta 16 MB; no hay sincronización ni backup automático, por lo que no se presenta como almacenamiento comercial.
- La capa de dominio valida ventas contra productos/precios/stock actuales, relaciones de cliente, tipos de pago y pagos de fiado. Las ventas nuevas guardan el costo por línea al cobrar; la migración v1 conserva como desconocido el costo histórico que no se puede reconstruir.
- El shell, jerarquía del Dashboard, encabezados y Ajustes recibieron una primera revisión visual. Caja/Stock/Clientes/Fiado aún requieren revisar sus flujos interactivos y tamaños estrechos.
- El Chat generativo integra OpenRouter con `OPENROUTER_API_KEY` y `OPENROUTER_MODEL` opcional; usa `openai/gpt-6-luna` como modelo normal predeterminado. Tras autorización por sesión, envía una consulta, hasta ocho mensajes previos y un snapshot minimizado: periodos, totales diarios, inventario y hasta 50 saldos pendientes por nombre. No incluye ventas individuales, teléfonos, identificadores ni el JSON completo. No guarda las conversaciones al cerrar ni tiene herramientas de escritura.
- Jev de TypeSafe es un modelo distinto, de decisiones tipadas (Choice/Score/Noul) que no genera prosa de chat. OpenRouter ofrece para Jev una API de decisiones Alpha separada de Chat Completions; queda en el roadmap de clasificación/enrutamiento, no como el modelo de conversación.
- La suite `python -m unittest discover -s tests -v` prueba persistencia entre procesos, reglas de comercio, carga dañada, rollback de escritura, construcción de siete pantallas y consistencia de la landing. No equivale a una auditoría visual/interactiva integral de accesibilidad, teclado, tema oscuro ni ventanas compactas.

## Prioridad

1. Proteger el estado actual en Git y reconciliar implementación, especificaciones y cambios locales.
2. Seguir cerrando invariantes financieros y evaluar requisitos de respaldo/recuperación para un futuro uso comercial; la demo ya permite exportar/restaurar copias manualmente.
3. Completar la revisión interactiva de Caja, Stock, Clientes, Fiado y Dashboard a tamaños amplio y compacto.
4. Completar Ajustes sin inventar opciones comerciales aún no modeladas; validar foco, teclado y temas.
5. Validar Chat generativo con una clave/modelo reales; después estabilizar datos para análisis histórico.
6. Mantener voz, sugerencias para alta de producto y Playground en el roadmap, sin implementarlos todavía.

## Alcance

- Validación en la capa de dominio para productos, ventas y pagos de fiado.
- Preservación del historial de ventas, saldos y costos/precios al momento de la operación.
- Persistencia local JSON elegida para la demo: un archivo versionado en la carpeta de datos del usuario, guardado de forma atómica. Ajustes ofrece exportación/restauración manual, validadas y con confirmación; no es la estrategia para uso comercial prolongado ni incluye sincronización entre equipos.
- Revisión visual de escritorio a 1100×700 y otros tamaños; jerarquía, densidad, foco de teclado, errores junto al campo y estados vacíos claros.
- Ajustes divididos en secciones reconocibles: apariencia, comercio, datos y accesibilidad. Cada preferencia debe indicar si se guarda localmente.
- Hoja de ruta de IA: modelo generativo normal para Chat ahora; Jev separado para decisiones; voz, sugerencias y Playground después.

## Fuera de alcance por ahora

- Implementar proveedores distintos de OpenRouter.
- Enviar al provider otros datos que no estén en el snapshot mínimo descrito para Chat.
- Permitir que la IA cobre, borre, modifique stock o guarde productos sin confirmación explícita.
- Ejecutar código arbitrario o conceder a Playground acceso ilimitado al equipo.
- Prometer disponibilidad comercial, instalador, backup automático o retención que todavía no existan.

## Criterios de éxito

- Reiniciar la app no borra ventas, productos, clientes, cuentas ni preferencias guardadas.
- Caja, Stock y Fiado rechazan operaciones inválidas incluso si se llama a la capa de datos sin pasar por la UI.
- Editar costos no reescribe el margen de ventas históricas.
- El historial no pierde la identidad de clientes con ventas previas.
- Los flujos principales se pueden completar con teclado y mouse; errores, confirmaciones y acciones para recuperarse son visibles.
- Las opciones de Ajustes se guardan, se explican y no duplican controles dispersos.
- El Chat generativo se puede usar solo cuando existe una clave configurada; el resto de GesKio permanece operativo sin ella.
- El Chat no puede modificar datos y presenta los fallos del provider de forma recuperable.

## Ciclo de trabajo y Git

- Estado base versionado preservado en `refs/codex/checkpoints/geskio-before-improvement` (objeto `dd5a569fc275a933751596ade6e92501cac022d0`). La rama actual no se movió. El checkpoint registra los archivos versionados del árbol sucio; los archivos sin seguimiento preexistentes quedaron intactos.
- Antes de cada ciclo: guardar un checkpoint de los archivos versionados y anotar su ref; confirmar alcance y rutas.
- Hacer un cambio pequeño y revisar `git diff` contra el estado previo; no incluir artefactos de `.atl/`, `.playwright-mcp/`, logs o capturas por accidente.
- Validar el comportamiento afectado, revisar cambios y documentar evidencia. Si falla, restaurar únicamente las rutas del ciclo al ref de su checkpoint con `git restore --source=<ref> --worktree -- <rutas>`.
- No borrar, resetear ni reescribir cambios que ya existían antes de esta propuesta. No crear commits de ellos sin autorización específica.

## Hoja de ruta de IA aprobada por fases

OpenRouter fue elegido por el usuario como provider el 2026-09-24. El asistente de Chat usa un modelo generativo normal (`openai/gpt-6-luna` por defecto) y hace una petición al endpoint Chat Completions; el modelo se puede cambiar por entorno. Cada envío comparte la consulta, hasta ocho mensajes anteriores y un snapshot limitado de datos de negocio; la UI lo advierte. No se guarda la clave en el JSON local. Jev es el modelo System One de TypeSafe: sus salidas tipadas sirven a código para tomar decisiones acotadas, no para redactar respuestas conversacionales.

| Fase | Alcance y salida | Criterios de aceptación | Bloqueo/decisión |
|---|---|---|---|
| A. Datos aptos para análisis | Capturar costo/precio en cada línea de venta; definir migración versionada/reversible del JSON; fijar moneda, zona horaria y semántica de periodos. | Ventas pasadas conservan su margen tras editar/borrar catálogo; migración con fixture anterior/nuevo, backup temporal y fallo seguro. | No se permiten respuestas históricas de margen hasta completar esta fase. |
| B. Contrato JEV sin modelo | Módulo independiente de Flet: `JEVRequest`, `Intent`, `Period`, `Source`, `MetricResult`, `Confidence`, `Clarification` y errores tipados. Parser fake determinista; catálogo cerrado de queries. | Tests para cada intent, parámetros fuera de rango, ambigüedad, sin datos y error de lectura; solo funciones de dominio allowlisted producen cifras; estado idéntico antes/después. | No provider real ni claves. Review de dominio y seguridad. |
| C. Chat generativo OpenRouter (primero) | Asistente de solo lectura con un modelo de texto normal para responder sobre ventas, inventario y deudas mediante snapshot mínimo y limitado. Predeterminado fijo `openai/gpt-6-luna`; slug configurable. | Requests asíncronos; consentimiento explícito; no teléfono/IDs/JSON completo; historial efímero; sin tools ni mutaciones. Validar respuesta real cuando se configure una clave. | OpenRouter está aprobado. La selección del modelo concreto puede cambiar por entorno. |
| D. Jev System One para decisiones | Integrar `typesafe/jev-1.13` mediante el endpoint OpenRouter `/api/alpha/decisions` (no Chat Completions) tras confirmar estabilidad/acceso. Clasificar intención del Chat en ventas/inventario/fiado/otro y seleccionar consulta allowlisted; medir confianza/probabilidades. | Contrato tipado, fake offline, evaluación con mensajes reales anonimizados, umbrales conservadores; baja confianza pregunta/aclara o deriva al modelo generativo. Nada de escrituras automáticas. | API Alpha y producto Jev en early access al investigar (2026-09-24); encapsular y poder desactivar. Jev devuelve Choice/Score/Noul, no prosa. |
| E. Captura asistida de productos | Un modelo de texto crea un borrador editable desde texto transcrito; Jev puede clasificar categorías/unidades predefinidas, pero no inventar nombre ni extraer audio por sí solo. Voz requiere un paso separado de Speech-to-Text y permiso de micrófono. | Campo por campo con fuente; precio/stock dudosos vacíos; Jev decide solo dentro de opciones predefinidas; revisión humana antes de validar/guardar por dominio. | Definir STT, privacidad, costos/permisos y calidad de castellano rioplatense antes de implementar audio. |
| F. Playground | Modelo generativo interpreta el pedido y propone JSON de gráfico conforme a DSL: tipo, serie, periodo y filtros permitidos. Jev opcionalmente clasifica intención/elige entre esquemas o rangos permitidos. | No `eval`/shell/archivos/código generado; validar DSL, consultas y presupuesto; no mutaciones; gráficos reconciliados con Dashboard. | Jev no crea gráficos ni prosa; la renderización la controla GesKio. Definir persistencia/compartir después del prototipo. |

Orden recomendado: mantener Chat C con el modelo generativo normal; completar A; prototipar y evaluar D con fake antes de conectar la API Alpha; solo sumar Jev a producción si su precisión/estabilidad supera el fallback determinista en GesKio; después E y F. Cada fase tiene su propio checkpoint, contrato, pruebas y recorrido UI. El provider elegido es OpenRouter; voz y Playground siguen fuera del alcance actual.
