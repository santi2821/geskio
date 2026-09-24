# Diseño formal de producto: GesKio confiable y fácil de usar

## Reemplazo de la dirección visual anterior

Este ciclo reemplaza la propuesta visual del ciclo 4 (tile de marca, claim, fondo cálido y tratamiento de tarjeta genérico). GesKio debe leerse como un sistema de operación de mostrador: prioriza exactitud, velocidad y recuperación ante errores. La apariencia profesional sale de jerarquía, densidad y consistencia, no de paneles decorativos. “Demo” describe la madurez y los datos; no es un estilo visual.

- Usar workspace gris frío neutro y una sola superficie de trabajo; máximo dos niveles de superficies. Reservar tarjetas para métricas o grupos realmente independientes.
- Rojo solo para acción primaria y selección actual; verde para éxito o saldo positivo; advertencias y errores siempre llevan texto e icono además del color.
- Escala preferida de espaciado 4/8/12/16/24 px; conservar 10/20 px solo donde el componente existente lo requiera hasta su revisión específica. Padding habitual de 12–16 px, radios graduales de 8 px en controles, 10 px en campos/tarjetas y 16 px en paneles mayores. Mantener celdas de calendario compactas y más filas visibles en 1100×700.
- Campos de texto y selectores comparten contorno fino neutral y foco primario de 2 px en todas las pantallas; el foco debe ser visible también al navegar con teclado.
- Mostrar un título de pantalla prominente una vez: barra superior como contexto y contenido con título de tarea, descripción y acciones, sin duplicar el nombre de navegación.
- Marca como wordmark GesKio compacto, sin tile ni claim comercial. La marca nunca compite con Caja, el total o Cobrar.
- No usar sombras, degradados, ilustraciones ni colores decorativos. Claro/oscuro comparten los mismos roles semánticos.
- Identificar los datos locales de demo con discreción en el lugar pertinente; no insinuar sincronización, respaldo ni aptitud para datos reales.

Aceptación visual: revisar Caja sin perder total ni Cobrar; Dashboard con cifras contextualizadas y sin grandes huecos inútiles; ventanas 1100×700, amplia y compacta; contraste claro/oscuro; recorrido por teclado y significado de color no dependiente únicamente del tono. Los anchos compactos, tema oscuro y teclado requieren validación manual posterior antes de declarar cobertura completa.

## Dirección de producto

GesKio es una herramienta de mostrador para kioscos, almacenes y despensas. Su trabajo principal es registrar una venta rápido y mantener Caja, Stock y Fiado de acuerdo entre sí. El detalle propio de la experiencia será ver el total, el medio de pago y el resultado de la operación sin perder el contexto del mostrador; no sumar más paneles de administración por decoración.

La app es Flet de escritorio, no una app de macOS. Se mantienen convenciones de escritorio: navegación lateral con sección actual visible, formularios con orden de tabulación lógico, acciones identificables, soporte de mouse y teclado, y ventana adaptable. El objetivo inicial es que 1100×700 funcione bien y que reducir o ampliar la ventana no oculte acciones importantes.

## Secuencia visual

1. **Caja:** producto/búsqueda y carrito como área principal; total y Cobrar siempre fáciles de encontrar; forma de pago y cliente fiado agrupados; errores en el lugar de corrección; estado vacío que invite a añadir el primer artículo.
2. **Stock:** búsqueda y estado de inventario primero; acciones por producto visibles; alta y edición coherentes, con campos relacionados agrupados; ajustar stock como movimiento explícito para entradas y correcciones.
3. **Clientes y Fiado:** deuda pendiente, pagos y último movimiento legibles; no perder historial al cambiar/eliminar un cliente.
4. **Dashboard:** periodo seleccionado y moneda visibles; cifras, tendencia, faltantes y cuentas por cobrar con definiciones consistentes.
5. **Ajustes:** agrupados en Apariencia, Comercio, Datos y Accesibilidad. Opciones avanzadas van detrás de una revelación; no habrá campos de proveedor IA hasta que esa elección exista.

## Sistema visual

- Reusar roles semánticos de `app/theme.py` para texto, superficies, bordes, éxito, atención y error; evitar hex nuevos dentro de las pantallas.
- La shell muestra el wordmark GesKio, áreas de trabajo agrupadas y Ajustes separado al pie. El contexto superior identifica sección y fecha; el área principal usa gris frío neutral.
- Los encabezados de tarea usan título y explicación breve distintos de la etiqueta superior. Dashboard prioriza la cifra del día, mantiene cifras neutrales salvo estados semánticos y limita alertas a cuatro filas con accesos a Stock y Fiado.
- Los botones de tema/acento tienen etiqueta, foco y selección explícitos. Ajustes expone la ubicación local real del JSON de demo sin prometer backup o sincronización.
- Preservar temas claro/oscuro, paletas existentes, sidebar y controles compartidos que ya estén funcionando.
- Hacer que el texto y los iconos no dependan solo del color; mantener foco visible y etiquetas en controles solo-icono.
- Objetivos WCAG AA: 4.5:1 para texto normal y 3:1 para texto grande/controles en claro y oscuro; medir con los hex reales antes de declarar cumplimiento.
- Validar escalado, orden de teclado, hit areas de acciones frecuentes, feedback para operaciones y estados vacíos/error. Los mensajes que se descartan solos no serán el único lugar para dejar un error importante.
- Quitar adornos que resten espacio al cobro o al inventario. Animación solo si aclara un cambio; respetar reducción de movimiento si se introduce.

## Decisiones de datos propuestas

- **Persistencia de la demo:** JSON local, seleccionado por el usuario. Un archivo versionado conserva productos, clientes, ventas y cuentas de fiado. La ruta predeterminada es la carpeta de datos del usuario; `GESKIO_DATA_FILE` permite elegir otra ubicación. Se escribe a un temporal en la misma carpeta y después se reemplaza el archivo para evitar dejar un JSON parcial. Si la carga detecta un archivo dañado o una versión desconocida, la app falla de forma explícita y no inicia con datos de ejemplo ni sobrescribe el archivo. Las semillas se crean solo cuando el archivo todavía no existe. No asumir sincronización simultánea entre equipos ni usar esto como protección suficiente para información comercial real.
- **Historial:** almacenar nombre, costo unitario y precio unitario en la línea de venta al cobrar; una modificación futura de producto no cambia ventas cerradas.
- **Relaciones:** no eliminar clientes con ventas o saldos históricos; ofrecer archivar o conservar una referencia histórica.
- **Reglas:** validar límites y consistencia en funciones de dominio, y dar mensajes editables/accionables en UI.

## Arquitectura de Chat y Jev (dos modelos distintos)

```text
Chat Flet -> OpenRouter /api/v1/chat/completions -> GPT-6 Luna -> respuesta en prosa
   |             consulta + contexto permitido
   +-- GesKio: consultas de solo lectura y métricas deterministas

Futuro clasificador -> OpenRouter /api/alpha/decisions -> TypeSafe Jev -> Choice/Score/Noul tipado
                          intención/datos acotados
```

- OpenRouter es el provider aprobado por el usuario el 2026-09-24. OPENROUTER_API_KEY y OPENROUTER_MODEL solo se leen del entorno del proceso; la clave no se guarda en el JSON del comercio, el chat ni los logs. Modelo de texto por defecto: `openai/gpt-6-luna` (slug concreto, no Auto Router), configurable por entorno.
- La petición usa el endpoint oficial /api/v1/chat/completions, timeout de 35 segundos, stream=false, máximo de 600 tokens, sin SDK adicional y sin tools/function calling.
- Antes del primer request de cada sesión, el usuario autoriza explícitamente compartir la consulta y un contexto allowlisted con agregados de ventas, totales diarios de 90 días, catálogo acotado y hasta 50 saldos por nombre de cliente. No se incluyen filas de ventas individuales, teléfonos, IDs ni el JSON completo. La interfaz avisa que puede haber cargos según provider/modelo.
- Los datos del snapshot son datos, nunca instrucciones del sistema. No se ejecutan texto, código, comandos ni acciones. OpenRouter solo devuelve texto; Caja, Stock, Clientes y Fiado no exponen herramientas de escritura al modelo.
- Jev de TypeSafe es un modelo System One de decisiones tipadas, no el modelo del Chat. Recibe `state` más preguntas `choice`, `score` o `noul` y no genera prosa. OpenRouter lo expone por `/api/alpha/decisions`, una superficie Alpha separada de Chat Completions; no conectar al flujo crítico sin comprobar acceso, estabilidad y evals locales.
- Para respuestas con datos, el dominio es autoridad en números: futuras queries allowlisted calculan cifras localmente; el modelo conversacional las explica/pide aclaración. Jev podría clasificar intención y seleccionar una ruta cerrada si la evaluación de GesKio justifica el servicio; debe caer a aclaración/determinismo ante baja confianza.
- El snapshot se limita a 18.000 caracteres y se reduce de forma determinista si es más grande; cada consulta acepta hasta 4.000 caracteres y el historial remoto usa hasta 8 mensajes anteriores acotados a 1.200 caracteres cada uno. El cuerpo de respuesta se limita a 512 KB. El historial UI vive en memoria durante la sesión y desaparece al cerrar la app.
- Cada respuesta numérica debería indicar métrica, unidad, periodo y corte. Si el contexto no cubre el periodo pedido, el modelo debe declarar el límite. No se ofrece ganancia histórica: las ventas no guardan costo unitario al momento de la operación.
- El flujo de borrador separa Speech-to-Text y estructuración desde texto del guardado. Jev no acepta audio ni genera texto arbitrario; un modelo de texto propone el borrador y Jev solo decide entre opciones/campos delimitados si aporta valor. El usuario revisa; `crear_producto()` es la única ruta que persiste y vuelve a validar.
- Playground usa un modelo generativo para convertir una solicitud a una especificación declarativa de gráfico, validada contra DSL/queries permitidas. Jev es opcional para clasificar o escoger valores enumerados; ninguno puede ejecutar código arbitrario ni mutar productos, ventas, clientes o pagos.

### Configuración y límites de OpenRouter

La selección de OpenRouter y el Chat fueron aprobados por el usuario. La clave real todavía debe ser configurada por el usuario en el entorno local; nunca pedirla ni imprimirla en el chat. La aplicación sigue operativa si la variable no existe, mostrando ayuda. Errores de clave, saldo, cuota, red y respuesta tienen mensajes separados. GPT-6 Luna es el modelo normal predeterminado verificado en el catálogo de OpenRouter al 2026-09-24; precios y slugs cambian y se deben revalidar. Jev es una integración futura separada, con endpoint Alpha y acceso/estabilidad por confirmar. Antes de distribuir GesKio en web o escritorio a terceros se requiere una revisión específica del almacenamiento/proxy de la clave; una variable de entorno no convierte una clave empaquetada en secreto.

### Dependencias de producto para IA

- El chat de margen depende de guardar costo/precio unitarios históricos y migrar JSON de manera segura; hoy el cálculo usa costo actual.
- Las consultas por fecha requieren fijar qué significa “hoy/semana/mes”, zona horaria y moneda. El primer alcance usa fechas y moneda de la demo de forma explícita.
- La voz depende de permiso de micrófono y un servicio/modelo Speech-to-Text: Jev actualmente evalúa texto/estado y no procesa audio. Debe poder probarse/editarse como borrador incluso cuando la transcripción falle o no esté disponible.
- La sugerencia solo puede reutilizar datos existentes con procedencia; el costo, precio y stock quedan vacíos si no hay fuente confiable.
- Playground se entrega al final porque amplía la superficie de interacción. Almacenar diseños guardados requiere decidir su formato/migración por separado.

## Ciclos y reversión

| Ciclo | Cambio acotado | Salida verificable | Reversa |
|---|---|---|---|
| 0 | Reconciliar estado dirty, API actual y OpenSpec | Inventario fuente de verdad y alcance firmado | Mantener checkpoint inicial sin cambiar archivos del usuario |
| 1 | Reglas de dominio e invariantes financieras | Casos válidos e inválidos documentados y ejecutables | Restaurar las rutas de dominio/UI a checkpoint previo |
| 2 | Persistencia local JSON para demo | Reinicio carga el archivo versionado y no duplica semillas | Restaurar el ciclo desde su checkpoint |
| 3 | Jerarquía/estados de Caja y Stock | Flujos revisados en ventana compacta y amplia | Revertir solo archivos del ciclo |
| 4 | Clientes, Fiado, Dashboard y Ajustes | Historial y preferencias consistentes y revisados | Revertir solo archivos del ciclo |
| A | Costos históricos, periodos y migración JSON | Margen histórico y periodos comparables; migración probada/recuperable | Restaurar backup temporal y dejar migración sin aplicar |
| B | Contrato de decisiones Jev + Fake local | Intents allowlisted, respuestas tipadas y no-mutación verificadas sin red | Quitar el fake; el Chat y el dominio siguen operativos sin Jev |
| C | Chat generativo de solo lectura vía OpenRouter | Contexto mínimo, fechas explícitas, timeout y errores visibles; integración aislada del dominio | Sin clave configurada, el resto de GesKio sigue operativo |
| D | Revisión del Chat y privacidad | Reconciliar cifras, contextos grandes, fallos del provider y recorrido de UI | No añadir más datos al contexto sin revisar exposición/costo |
| E | Borrador de producto, después voz/sugerencias | Campo por campo: fuente, edición, descarte y confirmación humana | Desactivar asistencia; seguir usando alta manual |
| F | Playground de gráficos declarativos | Queries allowlisted, gráficos reconciliables, cero ejecución/mutaciones | Desactivar Playground sin afectar Dashboard |

## Principios de validación

- Primero comprobar límites de negocio y datos; después la presentación visual del flujo.
- En cada ciclo hacer review independiente y reproducir el flujo tocado en la app. Incluir tipo de verificación y límites de evidencia en el reporte.
- No inferir build, persistencia, accesibilidad o funcionamiento en dispositivo a partir de una lectura de código.
- Mantener un checkpoint Git por ciclo, inspeccionar el diff completo y aceptar únicamente archivos del alcance.
