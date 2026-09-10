# Design: ui-v2 — Paperpillar-Anchored Visual Rebuild (geskio)

## Technical Approach

Shell-new-first (V2-D1): rebuild `app/main.py` into a `Shell` (sidebar + topbar + content slot) with a thin adapter that renders any `Screen` control unchanged. Extend `theme.py` with non-color shell/layout tokens (zero new hex → AA 19/19 pairs stay valid). Extend `widgets.py` with shell/table/dashboard kit. Then migrate dashboard → tables → caja+chat in slices a–d on `feat/ui-figma-v2` (auto-chain, ≤800 lines each). `app/datos.py` untouched; all calendar/aggregate/paging logic is view-side.

## Architecture Decisions

| # | Option | Tradeoff | Decision |
|---|--------|----------|----------|
| AD-1 Shell geometry (closes V2-D6) | (1) fixed 240px sidebar; (2) rail-only; (3) responsive expand/collapse | (1) at 1100x700 leaves ~812px content — too tight for 7-column tables; (2) loses labels (discoverability); (3) adds resize-driven complexity | **(3)**: sidebar 240px expanded, 64px icon-rail collapsed; topbar 56px; **collapse when `page.window.width <= 1280 OR height <= 760`** → at the 1100x700 default the shell boots collapsed (rail keeps nav reachable, ~990px content). Driver: `page.window.on_event` (`WindowEventType.RESIZED`) reading `page.window.width/height` — verified in 0.84.0 env. Fallback if OS drops events (docstring: availability is OS-dependent): manual rail toggle in topbar. |
| AD-2 Navigation | topbar search + user menu (Paperpillar copy) vs. minimal topbar | topbar search/user = NEW features (out of scope) | Sidebar `Column` of `TextButton`s (v1 pattern) + topbar = screen title, mode toggle, brand `Dropdown` (moved from v1 toolbar). `mostrar(key)` becomes `shell.navigate(key)`; screens keep `Screen`/`invalidate()` contract. |
| AD-3 DataTable spike (closes risk) | (1) `ft.DataTable` + composed chrome; (2) Column/Row composed table | 0.84.0 `DataTable` has density knobs (`heading_row_height`, `data_row_min/max_height`, `data_row_color`, `horizontal_lines`, `heading_row_color`) but NO `DataPager`, no sticky header, no toolbar | **(1)**: SnowUI table = `TableToolbar` (search field + filter chips + actions) + denser `AppTable` (10 rows/page) + `TablePager` (composed Row: prev/next + "n de m"). Rejected (2): reimplements cell alignment/dividers DataTable already owns, larger diff, zero density gain; paging removes the sticky-header need. |
| AD-4 Dashboard composition (WellNest) | equal-weight cards (v1) vs focal + grid | v1 has no Von Restorff hierarchy | Focal stat **"Hoy"**: FS_36 `accent_text` value + 2px primary border on surface card (spans width). Secondary trio (Mes/Ganancia/Deben) FS_28 role-colored in `StatGrid` (ResponsiveRow). Below: **`Calendar` view-only** with `SegmentedButton` (verified in 0.84.0): day = selected day's ventas list; week = last-7-day totals; month = grid of per-day totals. Source: `ventas` (`fecha`, `total`) grouped view-side; `cuentas.created_at` only for the overdue badge list (no new API). Toggle is the only interaction. |
| AD-5 Token strategy | restructure `PaletteTheme` vs additive constants | restructure touches all proven AA pairs | **Additive only**: `PaletteTheme` fields frozen; add module constants `SHELL_SIDEBAR_W=240`, `SHELL_RAIL_W=64`, `SHELL_TOPBAR_H=56`, `SHELL_BREAKPOINT_W=1280`, `SHELL_BREAKPOINT_H=760`, focal/calendar layout steps. New *roles* reuse verified pairs only. |
| AD-6 v1 roles disposition | restructure vs reuse | 19/19 pairs are proven + landing-parity-bound | **Reuse unchanged**: `danger`/`danger_text`, `accent`/`accent_text`, `footer_hover` (landing parity), `_ROLE_ALIASES`. New usage mapping: sidebar idle = `text_muted` on `bg_soft` (5.05/4.95), active = `accent_soft`/`on_accent_soft` (5.02/6.45), chips = surface+border or accent_soft pair, calendar today = accent_soft pair, calendar totals = `text` on surface. |

## Data Flow

```
datos.py (FROZEN reads: ventas, cuentas, productos, clientes, stats())
        │  read-only, zero diff
        ▼
view-side derive (screens / widgets helpers): filter → sort → paginate,
group ventas by fecha, calendar series
        ▼
kit widgets (TableToolbar/AppTable/TablePager, StatGrid/Calendar, Shell)
        ▼
Shell ──navigate(key)──► Screen.build()/actualizar() ──► Shell content slot
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `app/main.py` | Modify | Rebuild: boots `Shell` with nav_items, adapter slot, resize collapse |
| `app/theme.py` | Modify | Add shell/layout constants + focal/calendar steps (no hex, no dataclass change) |
| `app/widgets.py` | Modify | Add `Shell`, `Topbar`, `Sidebar`, `PageHeader`, `Section`, `StatGrid`, `Calendar`, `TableToolbar`, `TablePager`; denser `AppTable` |
| `app/screen_base.py` | Modify | Padding/content conventions for sidebar shell (keep `invalidate()`/`al_entrar`) |
| `app/screens/dashboard.py` | Modify | Slice b: focal + StatGrid + Calendar + alert cards |
| `app/screens/stock.py`, `clientes.py`, `fiado.py` | Modify | Slice c: TableToolbar + denser AppTable + pager; inline create rows → `Section` forms |
| `app/screens/caja.py`, `chat.py` | Modify | Slice d: caja section hierarchy (keep flow); chat dividers + empty-state + bubble polish |
| `app/datos.py` | None | FROZEN — gate: `git diff --exit-code -- app/datos.py` per slice |

## Interfaces / Contracts

```python
Shell(page, nav_items, active_key, on_navigate) -> ft.Row       # sidebar | topbar+content
PageHeader(title, actions=(), on_refresh=None) -> ft.Row        # replaces AppHeader
Section(title, content) -> ft.Container                          # card w/ heading
StatGrid(focal: AppStatCard, stats: list[AppStatCard]) -> ft.ResponsiveRow
Calendar(get_series, today, view) -> ft.Control                  # view-only
TableToolbar(on_query, chips=(), actions=()) -> ft.Row
AppTable(columns, rows, page_size=10)                            # density knobs, keeps empty-state
TablePager(page, pages, on_page) -> ft.Row
```

## Testing Strategy

No repo runner (`strict_tdd: false`, verify `test_command: ""`). Verification per slice: (1) token-literal grep clean on `screens/` + `widgets.py`; (2) `git diff --exit-code -- app/datos.py`; (3) `python -m py_compile` + import smoke of all screens; (4) contrast re-proof table for every NEW usage pair against theme.py docstring values (≥4.5 normal / ≥3:1 large+UI); (5) manual: shell boots at 1100x700 collapsed, resize past breakpoint expands; each screen loads in shell; dialogs/feedback/sync preserved; landing untouched.

## Threat Matrix

N/A — no routing, shell-command, subprocess, VCS/PR-automation, executable-file-classification, or process-integration boundary. In-app navigation is UI state only.

## Migration / Rollout

No data migration (`datos.py` zero diff). Slices a–d auto-chain on `feat/ui-figma-v2`; `base-primer-commit` frozen. The adapter keeps v1 screens renderable inside the new shell between slices, so per-slice `git revert` restores the prior state; tokens stay isolated in `theme.py`.

## Open Questions

- [ ] Slice-a spike: confirm `page.window.on_event` RESIZED fires on Windows desktop 0.84.0 (RED check); if not, ship manual rail toggle (already the designed fallback).
