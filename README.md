<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/GesKio-gesti%C3%B3n%20de%20negocio-22c55e?style=for-the-badge&logo=store&logoColor=white">
    <img alt="GesKio" src="https://img.shields.io/badge/GesKio-gesti%C3%B3n%20de%20negocio-22c55e?style=for-the-badge&logo=store&logoColor=white">
  </picture>
</p>

# GesKio

**App de gestión de negocio para emprendedores + Landing promocional.** CRUD de productos, ventas, clientes, caja, fiado, stock y chat integrado. App Flet multiplataforma con landing page web.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-0.28.3-00B4AB?logo=flutter&logoColor=white)

## Modules

| Module | Descripcion |
|---|---|
| Dashboard | KPIs + Gráficos (Bar/Line/Pie) + Calendario |
| Stock | Gestión de productos, DataTable scrolleable, chips estado |
| Caja | Registro de ventas, carrito ListView auto_scroll |
| Clientes | CRUD con búsqueda, historial de compras |
| Proveedores | CRUD completo (nombre, teléfono, email, rubro), DataTable + dialogs 0.28.3 |
| Fiado | Cuenta corriente, filtros, badges días, pagos |
| Chat IA | Burbujas premium con avatar, timestamp, ListView auto_scroll, input filled 24 |
| Calendario | DatePicker + mini calendario mensual + ventas por día |
| Gráficos | BarChart (7 días), PieChart (stock), LineChart (ganancia 6 meses) |
| Personalización | Theme claro/oscuro (page.theme_mode) + client_storage + toggle premium |

## Novedades Flet 0.28.3 (Premium)

### Proveedores
- Nueva screen `app/screens/proveedores.py` + helpers en `datos.py` (`proveedores`, `crear_proveedor`, `actualizar_proveedor`, `eliminar_proveedor`, `prov_por_id`)
- CRUD completo con DataTable, filtros multi-campo, dialogs con `page.open/close` (sin `overlay.append`) y SnackBar vía `page.snack_bar`
- Integrada al nav premium (sidebar 240px, activo border-left 3px green)

### Calendario
- `PantallaDashboard` integra `ft.DatePicker` + calendario mensual custom (navegación mes, indicador ventas, selección día)
- Lista ventas del día seleccionado con total y chips de pago, altura limitada scrolleable

### Gráficos (Flet 0.28.3)
- `ft.BarChart` ventas últimos 7 días, `ft.PieChart` stock por estado (ok/bajo/agotado), `ft.LineChart` ganancia 6 meses
- Helpers `ventas_por_dia`, `stock_stats`, `ventas_por_mes`, `ganancia_por_mes` en `datos.py`, datos reales

### Personalización
- Sidebar premium + AppBar con toggle tema claro/oscuro (`page.theme_mode` + `page.client_storage`)
- Tokens Figma `#f8fafc`, `#16a34a`, `#0f172a`, `#e2e8f0`, border_radius 16, cards con shadow

### Chat Premium (QA Final)
- Burbujas con `CircleAvatar` inicial, timestamp `HH:MM`, `padding 14/10`, `border_radius 16`, `bgcolor white/#dcfce7/#f1f5f9`
- `ListView auto_scroll expand bgcolor white border 1 #e2e8f0`, `TextField filled True border_radius 24 hint "Preguntale..."`, `FilledButton` circular send
- Header premium con subtítulo y badge "En vivo", `mostrar_alerta` heredado (SnackBar, no overlay)

## Tech Stack

| Capa | Tecnologia |
|---|---|
| App | Python 3.11 + Flet 0.28.3 (`flet[all]==0.28.3`) |
| Landing | HTML5, CSS3, JavaScript |
| Persistencia | Memoria + helpers (SQLite opcional) |
| Tests | pytest 8.3.4, 37 tests verdes |

## Quick Start (Flet 0.28.3)

```bash
# venv ya incluido en .venv
source .venv/bin/activate
.venv/bin/python -c "import flet.version; print(flet.version.version)" # -> 0.28.3
.venv/bin/python -m pytest -q -v   # 37 passed
.venv/bin/python -m py_compile app/main.py app/datos.py app/screen_base.py app/screens/*.py
.venv/bin/flet run app/main.py     # requiere display
# alternativa sin display (CI)
.venv/bin/python -m pytest -q
```

```bash
cd app
pip install "flet[all]==0.28.3"
flet run main.py
```

La landing se abre con `landing/index.html` en cualquier navegador.

## Verificación QA (Flet 0.28.3)

```bash
python -m py_compile app/main.py app/datos.py app/screen_base.py app/screens/*.py
.venv/bin/python -m pytest -q -v  # esperado 23+ tests verdes (actual 37)
grep -rn "overlay.append" app/  # debe ser 0
grep -rn "AlertDialog" app/ | grep "page.open"  # uso correcto vía abrir_dialogo/page.open
```

## Project Structure

```
geskio/
├── app/
│   ├── main.py         # Entry point + sidebar premium + theme toggle
│   ├── datos.py        # Datos + proveedores + helpers gráficos
│   ├── screen_base.py  # Screen base (mostrar_alerta SnackBar, abrir/cerrar Dialog 0.28.3)
│   └── screens/
│       ├── dashboard.py   # KPIs + Bar/Pie/LineChart + calendario + alertas
│       ├── caja.py        # Caja con ListView auto_scroll
│       ├── stock.py       # Stock DataTable scroll AUTO
│       ├── clientes.py
│       ├── proveedores.py
│       ├── fiado.py
│       └── chat.py        # Chat premium (ListView, burbujas 16, input 24, avatar)
├── tests/
│   ├── test_datos.py
│   ├── test_screens.py
│   ├── test_proveedores.py
│   ├── test_chat.py            # build, burbujas 16, input 24, enviar_mensaje mocks
│   └── test_dimensionamiento.py # expand True + scroll AUTO
├── landing/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md
```

## License

[MIT](LICENSE) © 2026 Santino Avila
