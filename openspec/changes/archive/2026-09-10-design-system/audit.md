# Auditoría de diseño frontend — cambio `design-system` (geskio)

**Veredicto: NO shipeable como design system.** El dark mode es de verdad (no un invertido barato) y la tokenización es seria, pero el light mode falla WCAG AA en 5 pares de color que están en el camino crítico (CTA de cobro, burbuja de chat, estados de deuda, texto secundario), el foco de teclado es inexistente en la landing, y el kit solo se adoptó a medias: 5 de 6 pantallas ignoran `AppHeader` y no existe `AppButton`, así que conviven 3 tratamientos de botón. Detalle abajo; punch list al final.

## Alcance y método

- **Leído completo:** `app/theme.py`, `app/widgets.py`, `app/main.py`, `app/screen_base.py`, las 6 pantallas (`dashboard`, `caja`, `stock`, `clientes`, `fiado`, `chat`), `landing/index.html` + `styles.css` (616 líneas) + `script.js`, `openspec/changes/design-system/design.md`.
- **Visto en browser (landing real, no código):** desktop 1440 y mobile 390, en light y dark vía toggle `geskio-theme`, con scroll completo para disparar los reveals; drawer mobile abierto; medidas de caja de botones/links; inspección de estados.
- **App Flet:** auditada desde el código declarado (cada control, tamaño, color, spacing). No corre headless: lo no verificable en runtime se marca **NO-VERIFICADO**, nunca se inventa.
- **Skill aplicada:** `cognitive-doc-design` — veredicto primero, tablas sobre prosa, una idea por sección.

## Contraste WCAG 2.2 AA (calculado, no estimado)

Metodología: ratio relativo sRGB sobre los hex literales de `theme.py` y `styles.css`. Criterio: **4.5:1** texto normal, **3:1** texto grande (≥24px o ≥19px bold) y gráficos/UI.

### App Flet — LIGHT (`ROJO_LIGHT`, superficies `#ffffff` / `#f6f7f9`)

| Par (fg / bg) | Dónde se usa | Ratio | 4.5:1 | 3:1 | Dictamen |
|---|---|---|---|---|---|
| `text` / `bg` `#161b22`/`#ffffff` | cuerpo general | **17.30** | pass | pass | ✅ |
| `text-soft` / `bg` `#52606d`/`#ffffff` | tabla headers, diálogos | **6.46** | pass | pass | ✅ |
| `text-muted` / `bg-soft` `#8993a3`/`#f6f7f9` | labels stat 12px (`widgets.py:59`), meta carrito 13px (`caja.py:81`), subtítulo chat (`chat.py:46`) | **2.90** | **FAIL** | **FAIL** | 🔴 BLOCKER |
| `text-muted` / `surface` `#8993a3`/`#ffffff` | detalle ítem 12px (`caja.py:187`) | **3.10** | **FAIL** | pass | 🔴 BLOCKER (texto normal) |
| `on-primary` / `primary` `#ffffff`/`#ef4444` | **"Cobrar"** (`caja.py:139`), CTA primario | **3.76** | **FAIL** | pass | 🔴 BLOCKER |
| `on-primary` / verde `#ffffff`/`#16a34a` | "Cobrar" en tema verde | **3.30** | **FAIL** | pass | 🔴 BLOCKER |
| `success` / `surface` `#16a34a`/`#fff` | valor stat 28 bold (grande → 3:1 aplica) | **3.30** | FAIL | pass | ⚠️ MAYOR (margen 0.30) |
| `warning` / `surface` `#d97706`/`#fff` | valor "Ganancia" 28 bold; **monto Pendiente 14px bold en fiado** (`fiado.py:100`) | **3.19** | **FAIL** | pass justo | 🔴 BLOCKER (uso en 14px) |
| `danger` / `surface` `#dc2626`/`#fff` | "Eliminar" en light (`widgets.py:183`) | **4.83** | pass | pass | ✅ |
| `info` / `surface` `#2563eb`/`#fff` | stat "Mes" | **5.17** | pass | pass | ✅ |
| `primary` / `accent_soft` `#ef4444`/`#fdecec` | **nav activa** (`main.py:54`), **burbuja chat usuario 14px** (`widgets.py:231`) | **3.29** | **FAIL** | pass | 🔴 BLOCKER (ambos son texto normal) |
| verde: `#16a34a` / `#e7f5ec` | nav activa tema verde | **2.93** | **FAIL** | **FAIL** | 🔴 BLOCKER |

### App Flet — DARK (`ROJO_DARK`, superficies `#0e1014` / `#15181e` / `#181c23`)

| Par (fg / bg) | Dónde se usa | Ratio | 4.5:1 | 3:1 | Dictamen |
|---|---|---|---|---|---|
| `text` / `bg` | general | **17.43** | pass | pass | ✅ |
| `text-soft` / `bg` `#aab2bf`/`#0e1014` | general | **8.91** | pass | pass | ✅ |
| `text-muted` / `bg-soft` `#6e7783`/`#15181e` | meta 12–13px | **3.92** | **FAIL** | pass | 🔴 BLOCKER (texto normal) |
| `on-primary` / `primary` `#ffffff`/`#f43f5e` | "Cobrar" dark | **3.67** | **FAIL** | pass | 🔴 BLOCKER |
| **blanco / `danger` `#ffffff`/`#fb7185`** | **"Eliminar" en dark** (`widgets.py:183`) | **2.69** | **FAIL** | **FAIL** | 🔴 BLOCKER (ni a 3:1) |
| `success` `#4ade80`, `warning` `#fbbf24`, `danger` `#fb7185`, `info` `#60a5fa` / surface | stats y estados | **9.80 / 10.23 / 6.35 / 6.72** | pass | pass | ✅ (dark semántico, impecable) |
| `primary` / `accent_soft` `#f43f5e`/`#2e161e` | nav activa, burbuja usuario | **4.58** | pass | pass | ✅ |
| SnackBar `#0e1014`/`#f3f5f8` (`widgets.py:207`) | feedback | **17.4** | pass | pass | ✅ |

### Landing (pares propios, medidos en browser)

| Par | Ratio | Dictamen |
|---|---|---|
| `.eyebrow`, `.hero-foot`, `.device-tab`, `.author-role` (`text-muted` sobre bg) light | **~3.1** | 🔴 BLOCKER (12–13px, Mayúsculas incluidas) |
| `pill-warn` `#dc2626`/`#fdecec` light | **4.23** | ⚠️ MAYOR (badge 11px → texto normal, FAIL 4.5) |
| `pill-warn` dark | **6.24** | ✅ |
| Números display serif en accent (`#ef4444`/blanco, ~70px) | **3.76** | ✅ solo por texto grande (3:1) |
| Números dark (`#f43f5e`/`#0e1014`) | **5.19** | ✅ |
| Avatares iniciales blancos sobre accent (15px bold) | **3.76** | 🔴 BLOCKER (texto normal) |
| `form-note` error `var(--accent)` sobre blanco | **3.76** | 🔴 BLOCKER |
| `form-note` éxito hardcodeado `#059669` sobre blanco (`script.js:140`) | **3.77** | 🔴 BLOCKER + anti-token (ver M-12) |
| Botón primario (casi-negro/blanco, ambos modos) | **~17.3** | ✅ (el CTA más visto es el único rojo que no falla, ironía incluida) |
| Footer `color-mix` sobre fondo oscuro | **~6–9** | ✅ en navegadores modernos; ⚠️ ver M-13 |

## BLOCKERS (rompen usabilidad o AA)

- **B-1 — Texto secundario ilegible según AA, en ambos productos y ambos modos.** `text-muted` no llega a 4.5:1 en ningún fondo (2.90–3.92) y se usa en texto de 12–13px: labels de stats (`widgets.py:59`), "0 items" (`caja.py:81`), subtítulo del chat (`chat.py:46`), eyebrows, `hero-foot`, tabs del mockup, roles de autor. Ley: **WCAG 1.4.3**. No es "texto decorativo": son labels funcionales.
- **B-2 — El botón que cobra no pasa AA en light.** "Cobrar" (`caja.py:139`) es blanco sobre `#ef4444` (3.76) y sobre `#16a34a` (3.30) en tema verde. Es 14px normal → exige 4.5. Ley: **WCAG 1.4.3 + efecto estética-usabilidad** (lo más lindo de la pantalla es lo menos legible).
- **B-3 — "Eliminar" en dark falla hasta el 3:1.** Blanco sobre `#fb7185` = **2.69** (`widgets.py:183`). El botón más peligroso del sistema es el menos legible, justo en el modo donde todo lo demás sí pasa. Ley: **WCAG 1.4.3**.
- **B-4 — Burbuja de chat del usuario en light.** `#ef4444` sobre `#fdecec` = 3.29 a 14px (`widgets.py:231`). El usuario lee su propio mensaje con contraste insuficiente. Ley: **WCAG 1.4.3**. (En dark da 4.58 y pasa: asimetría entre modos.)
- **B-5 — Deuda pendiente solo en ámbar que no pasa.** `fiado.py:100` pinta el monto pendiente con `role_color("due")` → warning `#d97706` (3.19) a 14px bold = texto normal → FAIL. Y es doble falta: el estado **se comunica solo por color** (pagado = "✔", pendiente = color). Ley: **WCAG 1.4.3 + 1.4.1 (uso del color)**.
- **B-6 — Nav activa en light.** `main.py:54`: texto `primary` sobre `accent_soft` = 3.29 (rojo) y 2.93 (verde). La señal de "dónde estoy" es la de menor contraste del chrome. Ley: **WCAG 1.4.3 + Gestalt figura-fondo**.
- **B-7 — Foco de teclado invisible en la landing.** Verificado por lectura total de `styles.css`: no existe ningún `:focus-visible` en el archivo; el único `:focus` es el de inputs (`styles.css:516`), cuyo halo `box-shadow 0 0 0 4px accent-soft` es rosa pálido sobre blanco (~1.1:1, decorativo). Links, botones, toggle, drawer, sociales: sin indicador propio, solo el default del UA donde sobreviva al reset. Ley: **WCAG 2.4.11 (apariencia del foco, AA en 2.2)**. En la app Flet no hay estilos de foco propios: **NO-VERIFICADO** en runtime (defaults de Material), no se dictamina.

## MAYORES (degradan notablemente)

- **M-1 — Von Restorff diluido en la landing: todo grita, nada destaca.** El rojo aparece en accent-word + scribble + dots del device + pill + montos deudor + números gigantes + avatares + separadores del marquee + hovers. Visto en screenshots 1440: el ojo no tiene un único punto de énfasis por vista. Un acento que está en 15 lugares no es un acento.
- **M-2 — Von Restorff roto en el dashboard + colisión admitida.** 4 stat values, cada uno en un saturado distinto (verde/azul/ámbar/rojo, `dashboard.py:103`), y `design.md` ADR-1 admite que "Deben shares red" con el brand. Deuda y marca gritan en el mismo hueso. Un dashboard necesita UNA jerarquía: el dato que exige acción.
- **M-3 — Kit adoptado a medias (anti-frankenstein interno).** `AppHeader` se usa en 1 de 6 pantallas (`dashboard.py:117`); caja/stock/clientes/fiado/chat construyen el título a mano (`ft.Text(..., FS_30, BOLD)`). No existe `AppButton`: conviven Elevated default ("Guardar" `stock.py:98`, "Agregar" `clientes.py:75`, "Pagar" `fiado.py:109`), Filled custom primario ("Cobrar" `caja.py:139`) y Filled danger (`widgets.py:183`). `Badge` está definido (`widgets.py:217`) y **no se usa en ninguna pantalla** (grep: 0 usos) mientras la landing sí tiene `.chip`. Ley: **Gestalt similitud + Tesler** (la complejidad que el kit debía absorber sigue en las pantallas).
- **M-4 — Errores silenciosos en las 6 pantallas.** Todos los `except` terminan en `print()` (consola invisible para el kiosquero); `guardar_nuevo` retorna sin feedback si el nombre está vacío (`stock.py:187`, `clientes.py:161`); el usuario nunca sabe si falló. Ley: **Doherty + visibilidad del estado**. Además `feedback()` (`widgets.py:205`) agrega un SnackBar nuevo al overlay en cada llamada sin retirar anteriores: apilamiento sin cota.
- **M-5 — Mobile entierra el H1.** A ≤980px, `.hero-visual { order: -1 }` (`styles.css:575`) pone el mockup ANTES del titular (verificado en screenshot 390: dashboard ficticio primero, "Menos vueltas…" después). El H1 + CTAs quedan bajo el fold en la pantalla que más los necesita. Ley: **jerarquía + Fitts/distancia al CTA**.
- **M-6 — Drawer mobile sin scrim, sin CTA y sin semántica.** Verificado abierto en 390 dark: sin overlay/scrim (la página sigue visible e interactuable detrás), sin botón de acción (el CTA del nav está en `display:none` a ≤760px, `styles.css:601`), sin `aria-expanded` (medido: `null`), sin cierre con Escape (no hay `keydown` en `script.js`). Ley: **Jakob (convenciones de drawer) + Gestalt figura-fondo**.
- **M-7 — La landing promete un producto que no existe.** "Sin instalaciones · Funciona en el navegador" (`index.html:77`) vs app Flet desktop fija de 1100×700 (`main.py:24`). El mockup muestra un "Dashboard" de navegador. Ley: **confianza/estética-usabilidad** (la promesa falsa rompe más que un defecto visual).
- **M-8 — Contacto no accionable + enlaces muertos.** Email/teléfono son `<span>` sin `mailto:`/`tel:` (`index.html:306`); en mobile eso es fricción directa. Los 3 sociales apuntan a `href="#"` (`index.html:360`). Ley: **Jakob + Fitts** (tap-to-call es la convención).
- **M-9 — Marquee sin control de pausa.** Animación infinita sin mecanismo propio; `prefers-reduced-motion` la desactiva (`styles.css:563`, bien), pero no hay control en página. Ley: **WCAG 2.2.2** (mitigado, no cumplido).
- **M-10 — Búsquedas etiquetadas solo con hint.** `hint_text` como única etiqueta en stock/clientes/chat (`stock.py:38`, `clientes.py:36`, `chat.py:28`); el hint desaparece al escribir. Brand dropdown sin `label` (`main.py:121`). Ley: **WCAG 3.3.2**. El dropdown de marca junto al toggle de modo son dos controles de tema compitiendo (Hick).
- **M-11 — Densidad táctil en tablas.** Acciones de fila: 3 IconButtons de 18px con gaps de 4px (`stock.py:143`, `clientes.py:126`); hit-area real **NO-VERIFICADA** headless, pero lo declarado (18px, 4px) está lejos de 44px con distancia segura. Ley: **Fitts**. El "✔" de pagado como `ft.Text` (`fiado.py:114`) viola el propio ADR-3 (emoji→Material).
- **M-12 — Verde = marca = éxito.** En `VERDE_LIGHT`, `primary` y `success` son el mismo `#16a34a`: "Cobrar" y "todo en orden" hablan en idéntico verde (Tesler/Von Restorff). El mensaje de éxito del form usa `#059669` hardcodeado (`script.js:140`), fuera de tokens: rompe la paridad 1:1 que `design.md` proclama.
- **M-13 — Footer frágil sin `color-mix`.** Todo el footer depende de `color-mix` (`styles.css:526`); donde no se soporte, la declaración se descarta y el texto hereda el color del body sobre fondo oscuro → footer ilegible. Sin fallback. (Moderno: bien; viejo: catástrofe silenciosa.)

## MENORES (pulido)

- Radios fuera de escala: `.nav-link` 8px (`styles.css:190`), `.mc-row` 13px (`styles.css:415`); la escala es 10/12/18/999 y por lo demás se respeta bien.
- Dos voces para dinero: total de caja FS_36 (`caja.py:78`) vs stats FS_28 (`widgets.py:67). Una sola idea por nivel: elijan una.
- Padding horizontal de 4px en ítems del carrito (`caja.py:210`): respiración insuficiente (proximidad al límite).
- Dividers de 12px de alto (`theme.py:45`) + spacing de columna SP_10 en 4 pantallas vs SP_12 en dashboard: el ritmo vertical cambia según la pantalla.
- Dos voces tipográficas entre productos: landing titular en Instrument Serif (83px medidos), app 100% Inter. Defendible como "voz editorial", pero `design.md` vende paridad 1:1 y la paridad real es solo de color.
- Mockup monocromo vs stats a color en la app; tile "Ganancia" invertida en negro sin motivo jerárquico (énfasis arbitrario dentro del device).
- `.btn-primary:hover` cambia de negro a rojo: el hover muta el hueso en vez de la luminosidad (continuidad).
- "Detalles" enlaza a `#numeros` cuya sección se titula "Por qué GesKio": etiqueta ≠ destino (Jakob leve).
- Opciones de dropdown verbosas (`"nombre ($precio — stock: N)"`, `caja.py:41`): carga Hick en el control más usado del flujo de cobro.
- "Cant" + campo de 80px (`caja.py:73`): abreviatura y ancho mínimo en el flujo crítico.
- Autenticidad de testimonios sin forma de verificación (avatares de iniciales): **NO-VERIFICADO**, se señala como riesgo de confianza, no como hecho.

## Lo que sí funciona (justicia ante todo)

- **Dark mode real.** Fondos `#0e1014` con superficies elevadas, texto reequilibrado, acentos aclarados direccionalmente (`#ef4444`→`#f43f5e`), sombras y grano re-sintonizados (`multiply`→`screen`), footer/marquee/mockup re-mapeados. Visto en screenshot: se siente nocturno, no invertido. El semántico en dark (9.80/10.23/6.35/6.72) es ejemplar.
- **Tokens 1:1 verificados** entre `:root`/`dark` y `ROJO_LIGHT`/`ROJO_DARK` (incluidos radios y el `accent_soft` pre-mezclado documentado). La disciplina existe.
- **Estados vacíos bien resueltos:** `AppTable` con icono 36 + mensaje (`widgets.py:101`), "Sin deudas pendientes", "Todo en orden" con icono de éxito. La mayoría de los sistemas falla acá; este no.
- **Chat con buena Gestalt:** usuario/bot distinguidos por alineación + color + radio asimétrico (`border-bottom-right/left-radius: 4px`, `styles.css:419`), espejado en `ChatBubble`. `role="status"` en el form, `aria-hidden` en marquee y scribble, `lang="es"`, un solo H1: la base a11y está pensada.
- **Consistencia de spacing/radios** en el 90% de los casos: la escala 4/8/10/12/20/24 se respeta y R_MD=12 unifica cards, tablas y diálogos.

## Punch list priorizada

1. [ ] Recalibrar `text-muted` (light y dark) hasta 4.5:1 sobre `bg-soft`/`surface`, o reservar el muted actual solo para texto ≥18px/decorativo. (B-1)
2. [ ] Endurecer primarios light (rojo y verde) u oscurecer `on-primary` hasta 4.5:1; afecta "Cobrar", hovers y `accent-soft`. (B-2)
3. [ ] Rehacer "Eliminar" en dark (fondo danger profundo, no texto blanco sobre rosa: 2.69). (B-3)
4. [ ] Burbuja de usuario en light: texto `text` sobre `accent_soft` (conservar alineación como diferenciador). (B-4)
5. [ ] Deuda pendiente: no solo color — icono + peso + ratio 4.5 en light; idem nav activa. (B-5, B-6)
6. [ ] `:focus-visible` global en landing (anillo 2–3px con contraste 3:1) + halo de input que pase 3:1. (B-7)
7. [ ] Completar el kit: `AppButton` + título de pantalla; migrar las 5 pantallas; usar o eliminar `Badge`. (M-3)
8. [ ] Errores visibles para el usuario (cero `print` como único destino) + SnackBar reutilizable. (M-4)
9. [ ] Mobile: H1 antes que mockup; CTA dentro del drawer; scrim; `aria-expanded` + Escape. (M-5, M-6)
10. [ ] `mailto:`/`tel:`, sociales reales o fuera; corregir copy "navegador" vs desktop. (M-7, M-8)

## Checklist de verificación (para la próxima pasada)

- [ ] Ratios recalculados ≥4.5 en los 7 pares clave, light + dark, documentados como acá
- [ ] Tab por teclado visible en todos los interactivos de la landing (screenshot con foco)
- [ ] Las 6 pantallas usan kit (grep de `ft.Text` con `FS_30` fuera de `widgets.py` = 0)
- [ ] Drawer mobile con scrim, CTA, Escape y `aria-expanded` (verificado en browser 390)
- [ ] App Flet corrida y capturada a 1100×700: toolbar sin overflow, tabla stock legible, hit-areas
- [ ] Cero `print(` como manejo de error visible en `app/screens/`

## NO-VERIFICADO (dicho explícito, no asumido)

Render real de la app Flet (hit-areas efectivas, foco Material, anuncios de lector de pantalla, overflow del toolbar con 6 botones + dropdown a 1100px, las 7 columnas de stock); performance; `prefers-contrast`; autenticidad de los testimonios.

> Nota de entorno (fuera del alcance de diseño, se deja constancia): el LSP del workspace reporta errores preexistentes en `app/` con el Flet instalado (ej. `DataColumn` sin parámetro `label`, `Dropdown(on_change=…)` desconocido). Si el Flet del entorno difiere del 0.84.0 que `design.md` declara verificado, el smoke test del Slice 0 debe re-validarse antes de cualquier ship. No se tocó código.
