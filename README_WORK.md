# GesKio — Carpeta de Trabajo (Flet 0.28.3)

> Preparada el 2026-09-03 — lista para 1-2h de mejora intensiva.

## Estado actual
- ✅ `flet==0.28.3` instalado en `.venv` (Python 3.11.16)
- ✅ `flet[all]==0.28.3` para gráficos y extras
- ✅ Estructura verificada, auditoría de bugs completa
- ✅ Tests base creados (`tests/test_datos.py`, `tests/test_screens.py`)
- ✅ Prompt maestro para agentes: `PROMPT_AGENTES.md`

## Cómo activar
```bash
source .venv/bin/activate
# o
export PATH="$HOME/.local/bin:$PATH"
uv run python -c "import flet.version; print(flet.version.version)"  # debe dar 0.28.3
```

## Cómo correr la app
```bash
source .venv/bin/activate
flet run app/main.py
# o
uv run flet run app/main.py
# o directo
python app/main.py  # ft.app(target=main)
```

## Cómo correr tests
```bash
source .venv/bin/activate
uv run pytest -q
# o
.venv/bin/python -m pytest -q
python -m py_compile app/main.py app/datos.py app/screen_base.py app/screens/*.py
```

## Archivos clave para agentes
- `PROMPT_AGENTES.md` — instrucciones completas (referencias Figma, bugs, features)
- `AUDITORIA_BUGS.md` — detalle de popups/dimensionamiento
- `tests/` — suite que debe quedar verde
- `app/main.py` — nav a reescribir con sidebar premium
- `app/screen_base.py` — centralizar `mostrar_alerta` y `cerrar_dialogo` con API 0.28.3
- `app/datos.py` — añadir proveedores + helpers gráficos

## Próximos pasos (automáticos, con agentes)
1. Agente A corrige popups/dimensionamiento
2. Agente B hace dashboard + gráficos + calendario
3. Agente C crea proveedores
4. Agente D rehace UI global + tema
5. Agente E verifica tests y hace push a GitHub

Todo está listo para `opencode` lanzar los 5 agentes en paralelo sin preguntar.
