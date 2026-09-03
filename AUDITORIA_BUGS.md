# Auditoría GesKio — Bugs detectados (Flet 0.28.3)

Fecha: 2026-09-03 — Carpeta preparada para trabajo 1-2h

## Resumen
- Flet 0.28.3 instalado y verificado (`.venv` Python 3.11.16)
- 6 pantallas existentes + 1 nueva requerida (Proveedores)
- 3 categorías de error: Popups, Dimensionamiento, Datos/UX

## 1. Popups (CRÍTICO — rompe en 0.28.3)

| Archivo | Línea | Patrón malo | Fix 0.28.3 |
|---------|-------|-------------|------------|
| `stock.py:150-165` | `editar_producto` | `overlay.append(dialogo); dialogo.open=True` | `page.open(dialogo)` / `page.close(dialogo)` |
| `stock.py:206-226` | `ajustar_stock_dialog` | mismo | mismo |
| `stock.py:238-263` | `eliminar_producto` | mismo | mismo |
| `clientes.py:111-123` | `editar_cliente` | mismo | mismo |
| `clientes.py:145-163` | `eliminar_cliente` | mismo | mismo |
| `fiado.py:103-117` | `abrir_pago` | mismo (2 dialogs) | mismo |
| `caja.py:186-194` | `mostrar_alerta` | `overlay.append(SnackBar)` | `page.snack_bar = sb; sb.open=True; page.update()` |
| `stock.py:276-283` | `mostrar_alerta` | mismo | mismo |
| `clientes.py:176-183` | `mostrar_alerta` | mismo | mismo |
| `screen_base.py` | — | no centraliza | centralizar `mostrar_alerta` y `cerrar_dialogo` ahí |

**Impacto:** dialogs se acumulan en overlay, nunca se limpian, SnackBars no se ven o quedan detrás, memory leak, múltiples dialogs abiertos a la vez.

## 2. Dimensionamiento / Layout

| Archivo | Problema | Síntoma |
|---------|----------|---------|
| `main.py:64` | `nav = Row(botones)` sin scroll | overflow en ventana < 1100px o con muchos botones (+ proveedores) |
| `main.py:12-13` | `window.width/height` | en 0.28.3 verificar `page.window.width` vs `page.window_width` (alias); funciona pero falta `min_width` |
| `screen_base.py:7` | `Container(expand=True, padding=24)` + `Column(scroll=AUTO, expand=True)` | doble scroll, padding corta contenido |
| `dashboard.py:56` | `Row([4 cards])` sin wrap | en 900px se comprime a <200px cada card, texto se corta |
| `stock.py:38` | `Column([DataTable], scroll=AUTO, expand=True)` | DataTable ancho fijo no scrollea horizontal, se corta tabla |
| `stock.py:41-46` | `Row([5 fields + botón])` | en 1100px se desborda, sin `wrap` ni `ResponsiveRow` |
| `stock.py:210-216` | 5 botones + TextField en Row | overflow en dialog pequeño |
| `clientes.py:18` | DataTable 5 cols `column_spacing=16` | corta en mobile |
| `fiado.py:33` | `Column([DataTable])` igual | corta |
| `caja.py:57-58` | `Container(carrito, expand=True)` + `Column(spacing:4)` | carrito sin altura máxima, crece infinito, empuja total fuera de vista |
| `chat.py:20` | `Container(mensajes, expand=True, border, padding)` | sin `ListView` no hace auto-scroll al último mensaje |

## 3. Datos / Lógica

- `datos.py:65` `eliminar_producto` verifica `pid in (i.get("prod_id") ...)` OK pero mensaje genérico.
- `datos.py:73` `ajustar_stock` permite `max(0, ...)` pero no avisa si stock insuficiente.
- `datos.py:115` `pagar_fiado` no clamp a `total`, permite sobrepago.
- `datos.py:136` ventas ejemplo se crean al importar → cada reload duplica? pero `if not ventas` protege.
- `main.py:59` `TextButton(icon=...)` en 0.28.3 icon param puede ser `ft.Icons` correcto, pero `ButtonStyle` con `side` no aplica en TextButton → usar `FilledButton` para activo.

## 4. Faltantes (features nuevas)

- No existe `proveedores.py`
- No hay calendario (`DatePicker`)
- No hay gráficos (`BarChart`/`LineChart`/`PieChart`)
- No hay personalización (theme_mode, client_storage)
- No hay tests

## 5. Checklist fix inmediato (Agente A)

- [ ] Centralizar `mostrar_alerta` en `Screen` usando `page.snack_bar`
- [ ] Reemplazar todos `overlay.append(dialog)` por `page.open(dialog)` y `cerrar_dialogo` por `page.close(dialog)`
- [ ] Envolver DataTables en `ft.Row(scroll=AUTO) -> Container(expand=True) -> SingleChildScrollView` o `ft.Column(scroll=AUTO, horizontal=True)`
- [ ] Añadir `scroll=ft.ScrollMode.AUTO` al nav y `ResponsiveRow` a cards
- [ ] Limitar altura carrito: `Container(height=300, expand?)` + `ListView(expand=True, auto_scroll=True)`
- [ ] Verificar `page.window.*` no deprecated

## 6. Cómo reproducir

```bash
source .venv/bin/activate
python -m py_compile app/main.py app/datos.py app/screen_base.py app/screens/*.py  # OK hoy
# Falla visual:
# 1. Abrir Stock → Editar → Guardar → abrir de nuevo → overlay tiene 2 dialogs
# 2. Reducir ventana a 800px → nav se corta
# 3. Agregar 20 productos → tabla se corta derecha sin scroll
```

---
*Auditoría base para agentes — corregir antes de UI premium*
