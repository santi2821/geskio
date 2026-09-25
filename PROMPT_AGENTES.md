# GesKio — Prompt Maestro para Agentes (Flet 0.28.3)

> **Objetivo:** en 1-2 horas dejar GesKio production-ready. UI premium inspirada en Figma, 0 errores de popups/dimensionamiento, tests verdes, todo probado "que salga a la primera".

## 0. Contexto rápido
- **Stack:** Python 3.11 + Flet 0.28.3 (`flet[all]==0.28.3`), venv en `.venv`
- **Entrada:** `app/main.py` → `ft.app(target=main)`
- **Estructura:**
```
geskio/
├── app/
│   ├── main.py
│   ├── datos.py
│   ├── screen_base.py
│   └── screens/{dashboard,caja,stock,clientes,fiado,chat}.py
│   └── screens/proveedores.py (CREAR)
├── landing/
├── tests/
└── PROMPT_AGENTES.md (este archivo)
```
- **Activar venv:** `source .venv/bin/activate`  ó  `uv run python app/main.py`  ó  `.venv/bin/flet run app/main.py`
- **Flet 0.28.3 API correcta (OBLIGATORIO):** ver sección 2.

## 1. Referencias Figma (inspiración obligatoria)
No copiar 1:1, sino extraer sistema de diseño:
- Property Management Dashboard (Paperpillar): https://www.figma.com/es-la/comunidad/file/1423862565654844475/property-management-dashboard-ui-kit-paperpillar
- CRM Dashboard: https://www.figma.com/es-la/comunidad/file/1234052751192815621/crm-dashboard
- Wellnest Hospital Admin: https://www.figma.com/es-la/comunidad/file/1410399675335737504/wellnest-hospital-management-admin-dashboard
- Crest: https://www.figma.com/es-la/comunidad/file/1544641976783743855/crest
- DashStack: https://www.figma.com/es-la/comunidad/file/1324762163080748317/dashstack-free-admin-dashboard-ui-kit-admin-dashboard-ui-kit-admin-dashboard
- BankDash: https://www.figma.com/es-la/comunidad/file/1547191110121915354/bankdash-dashboard-ui-kit-admin-template-dashboard-admin-dashboard
- ErisPro Sales: https://www.figma.com/es-la/comunidad/file/1357275675655068690/erispro-sales-dashboard
- Order List Page: https://www.figma.com/es-la/comunidad/file/1486633496506469857/order-list-page

**Tokens a extraer:**
- Paleta: fondo #f8fafc / cards blanco, primary #16a34a (green), accent amber/blue/red para estados, sidebar oscuro #0f172a opcional
- Tipografía: Inter, títulos 30 bold, subtítulos 12 grey-500, valores 28 bold
- Cards: border_radius 16, padding 20, border 1 outline_variant, shadow sutil
- Sidebar navegación premium (no solo Row centrado): colapsable, icon+label, activo con bg green-100 + border green
- DataTable → reemplazar por ListView cards en móvil, mantener tabla en desktop con horizontal scroll

## 2. Errores críticos a corregir (POPUPS + DIMENSIONAMIENTO) — PRIORIDAD 0

**Flet 0.28.3 breaking changes detectados:**

### 2.1 Diálogos (AlertDialog)
**Mal (actual en stock.py, clientes.py, fiado.py, caja.py):**
```python
dialogo.open = True
if dialogo not in self.pagina.overlay:
    self.pagina.overlay.append(dialogo)
self.pagina.update()
# cerrar:
dialogo.open = False
self.pagina.update()
```
**Bien (0.28.3):**
```python
self.pagina.open(dialogo)           # abre (hace append a offstage + open=True + update)
# o: self.pagina.dialog = dialogo; dialogo.open = True; self.pagina.update()
# cerrar:
self.pagina.close(dialogo)
# o: dialogo.open = False; self.pagina.update()
# NUNCA manipular page.overlay directamente para dialogs
```
- Cada dialog debe crearse nuevo cada vez o reutilizar uno solo cerrándolo bien. Evitar acumulación en `page.overlay`.
- Todos los diálogos deben tener `modal=True` cuando bloqueen, `shape=ft.RoundedRectangleBorder(radius=16)`, padding correcto, y `actions_alignment`.
- Verificar que `page.dialog` no interfiera con múltiples dialogs: usar `page.open(dialog)` es el pattern recomendado en docs 0.28.

### 2.2 SnackBar
**Mal:**
```python
sb = ft.SnackBar(ft.Text(texto), open=True, duration=4000)
if sb not in self.pagina.overlay:
    self.pagina.overlay.append(sb)
self.pagina.update()
```
**Bien:**
```python
sb = ft.SnackBar(content=ft.Text(texto), duration=4000, show_close_icon=True)
self.pagina.snack_bar = sb
sb.open = True
self.pagina.update()
# o:
self.pagina.show_snack_bar(ft.SnackBar(...)) # si existe helper, pero 0.28 usa snack_bar setter
# Alternativa moderna: self.pagina.open(ft.SnackBar(...))
```
- Centralizar en `screen_base.py`: método `mostrar_alerta()` corregido una sola vez y heredado.

### 2.3 Dimensionamiento / Layout
- `page.window.width = 1100` funciona pero en 0.28.3 se prefiere `page.window.width / height` + `page.window.min_width`. Verificar no rompa en web/desktop.
- `page.padding = 0` OK pero cada Screen es `ft.Container(expand=True, padding=24)` con `Column(expand=True, scroll=AUTO)` → **doble scroll** provoca overflow. Solución: un solo scroll por screen, envolver DataTable en `ft.Container(expand=True)` + `ft.Column(scroll=AUTO)` ó usar `ft.ListView` / `ResponsiveRow`.
- DataTable `column_spacing=12` muy chico en 1100px → se corta. Añadir `ft.Row(scroll=ft.ScrollMode.AUTO, expand=True)` wrapper o `DataTable(expand=True)` y `Container(expand=True, scroll)`.
- `ft.Row` con `expand=True` + `Container(expand=True)` compiten por espacio → revisar alignment.
- `screen_base.py: self.content = self.build()` reasigna Container content pero no limpia `expand`; asegurar `self.content` es siempre `Column(expand=True)`.
- Altura fija en cards: usar `expand=True` consistente.

### 2.4 Otros bugs detectados
- `main.py: nav = ft.Row(botones...)` sin scroll → en ventana chica se desborda. Solución: `ft.Row(scroll=ft.ScrollMode.AUTO)` + `ResponsiveRow` o sidebar vertical.
- `caja.py: prod_por_id` fallback con `_ultimo_pid` es fragile; dropdown on_change debe guardar correctamente.
- `datos.py: eliminar_producto` retorna False si tiene ventas pero UI no informa bien → testear.
- `fiado.py: dias calc` con `date.fromisoformat` puede fallar si formato distinto.
- `stock.py: ajustar_stock_dialog` tiene 5 botones + TextField en Row sin wrap → overflow en width 1100.

## 3. Features nuevas (obligatorias)

### 3.1 Calendario
- Nueva screen `calendario.py` o integrar en Dashboard: `ft.DatePicker` + lista de ventas por fecha + mini calendario mensual.
- Mostrar ventas del día seleccionado, total y navegación mes.

### 3.2 Gráficos
- Usar `ft.BarChart`, `ft.LineChart`, `ft.PieChart` (disponibles en 0.28.3) en Dashboard:
  - Ventas últimos 7 días (BarChart)
  - Stock por categoría / estado (PieChart)
  - Ganancia mensual (LineChart)
- Datos vienen de `datos.py` → crear helpers `ventas_por_dia()`, `stock_stats()`.

### 3.3 Más personalización
- Theme toggle claro/oscuro en AppBar (usar `page.theme_mode = ft.ThemeMode.LIGHT/DARK`)
- Selector de color primario o densidad
- Guardar preferencia en `page.client_storage`.

### 3.4 Screen Proveedores (nueva)
- `screens/proveedores.py` similar a clientes pero con campos: nombre, contacto, telefono, email, productos que provee, deuda/pagos.
- CRUD completo + DataTable + dialogs corregidos.
- Añadir a `datos.py`: lista `proveedores` + funciones `crear_proveedor`, `actualizar_proveedor`, `eliminar_proveedor`.
- Añadir al nav en `main.py`.

## 4. UI Premium — checklist por screen

### Global
- [ ] Sidebar premium vertical (120-240px) con logo GesKio, nav activo destacado, footer con usuario
- [ ] AppBar superior con título, search global, notificaciones, avatar
- [ ] Sistema de tokens: `COLORS = {primary: #16a34a, surface: white, bg: #f8fafc, text: #0f172a, muted: #64748b, border: #e2e8f0}`
- [ ] Todos los Containers con `border_radius=16`, `border=ft.border.all(1, "#e2e8f0")`, padding consistente
- [ ] Botones: `ft.FilledButton` para primary, `ft.OutlinedButton` / `ft.TextButton` para secondary, `bgcolor` con estados

### Dashboard
- [ ] 4 KPI cards con iconos (Icons.TODAY, CALENDAR_MONTH, TRENDING_UP, ACCOUNT_BALANCE_WALLET) y sparkline
- [ ] Gráficos (Bar + Pie) en Row responsive
- [ ] Alertas en card con lista scrolleable
- [ ] Calendario mini

### Stock
- [ ] Header con búsqueda + filtros (stock bajo, todos) + botón Nuevo
- [ ] DataTable con wrapping horizontal scroll + acciones icon buttons con tooltip
- [ ] Dialogs con validación y focus
- [ ] Chips de estado (En stock / Bajo / Agotado)

### Caja
- [ ] Layout 2 columnas: izquierda productos/carrito, derecha resumen/total
- [ ] Dropdowns con `filled=True`, `border_radius`
- [ ] Carrito con `ft.ListView` scrolleable, empty state
- [ ] Botón Cobrar sticky footer

### Clientes / Proveedores / Fiado
- [ ] Igual lineamiento: search + table + dialogs
- [ ] Fiado: filtros + badges de días (verde/amarillo/rojo) + gráfico de deuda

### Chat
- [ ] Burbujas mejoradas con timestamp, avatar, typing indicator
- [ ] Input con `filled`, `border_radius=24`, send button circular

## 5. Tests (que salga a la primera)

Ubicación: `tests/` con `pytest`. Já existentes 0 → crear.

**tests/test_datos.py:**
- crear_producto, actualizar, eliminar con ventas asociadas, ajustar_stock, crear_venta + stock decrement, fiado crea cuenta, pagar_fiado, stats, margen 0

**tests/test_screens.py:**
- Importar cada Pantalla sin crashear (mock Page)
- Verificar build() retorna Control
- Verificar actualizar() no lanza excepción con datos vacíos

**tests/test_dialogs.py:**
- Mock page con `open`/`close`/`snack_bar`/`dialog`, verificar `mostrar_alerta` y `cerrar_dialogo` usan API 0.28.3

**tests/test_dimensionamiento.py:**
- Verificar que cada Screen.build() usa `expand=True` y scroll único
- Verificar DataTable dentro de Container scrolleable

Ejecutar: `uv run pytest -q`  ó  `.venv/bin/pytest -q` debe dar verde antes de entregar.

## 6. Distribución del trabajo — agentes en paralelo

Lanzar 5 agentes (no preguntar, todo automático):

**Agente A — Fix Popups & Dimensionamiento (crítico)**
- Corrige `screen_base.py` (mostrar_alerta, cerrar_dialogo)
- Corrige `stock.py`, `clientes.py`, `fiado.py`, `caja.py` para usar `page.open/close`
- Arregla layout overflows (Rows con scroll, Containers expand)
- Archivo: entrega diff y test `test_dialogs.py` verde

**Agente B — Dashboard + Gráficos + Calendario**
- Mejora `dashboard.py` con BarChart/LineChart/PieChart + calendario
- Añade helpers en `datos.py` (ventas_por_dia, etc.)
- Usa tokens Figma

**Agente C — Proveedores + Datos**
- Crea `proveedores.py` + extiende `datos.py`
- Integra nav en `main.py`
- Tests para proveedores

**Agente D — UI Global + Personalización + Nav Premium**
- Reescribe `main.py` con sidebar premium + AppBar + theme toggle
- Añade `page.theme_mode` y `client_storage`
- Aplica tokens a todas screens (wrapper común)

**Agente E — QA / Tests / Integración**
- Crea suite `tests/` completa
- Corre `pytest`, `flet run --help`, `python -m py_compile`
- Verifica que `uv run flet run app/main.py` no crashee (dry run)
- Reporta coverage

Cada agente debe:
1. Leer este PROMPT
2. Leer su archivo objetivo
3. Editar con `edit` preciso
4. Ejecutar `uv run pytest` o `python -m py_compile` local
5. Marcar todo verde

## 7. Definición de Done (entrega)

- [ ] `flet==0.28.3` instalado y verificado (`flet.version.version == 0.28.3`)
- [ ] `uv run pytest -q` → 100% passed
- [ ] `python -m py_compile app/*.py app/screens/*.py` sin errores
- [ ] No queda ningún `page.overlay.append(dialog)` ni `SnackBar` en overlay
- [ ] Todas screens testeadas manual (agentes simularon Page mock)
- [ ] Nuevas features: calendario, gráficos (3 tipos), proveedores, personalización
- [ ] UI coherente con Figma tokens, sidebar premium, dimensionamiento sin overflow
- [ ] Commit en branch `feat/geskio-premium` y push a `origin` (github.com/santi2821/geskio)

## 8. Comandos útiles

```bash
source .venv/bin/activate
flet --version
python -c "import flet.version; print(flet.version.version)"
uv run pytest -q
uv run python app/main.py          # requiere display; para CI usar mock
python -m py_compile app/main.py
.venv/bin/flet run app/main.py
```

## 9. Notas finales
- No preguntar al usuario, todo automático. Si dudas, elige la opción más profesional y documenta en commit.
- Cada fix con `try/except` + `print` es ok pero añadir `mostrar_alerta` visible.
- Preferir `ft.Colors` con tokens hex si hace falta custom: `ft.Colors.with_opacity`.
- Entregar al final resumen + URL del push a GitHub.

---
*Generado automáticamente 2026-09-03 — Carpeta lista para trabajo 1-2h con Flet 0.28.3*
