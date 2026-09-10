# Tasks: ui-v2 — Visual Rebuild Faithful to Figma

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~1420 total; a ~480, b ~330, c ~390, d ~220 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR1 slice-a → PR2 slice-b → PR3 slice-c → PR4 slice-d |
| Delivery strategy | auto-chain |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Slice-a shell+tokens+adapter | PR1 on feat/ui-figma-v2 | `python -m py_compile app/main.py app/widgets.py app/theme.py` + `git diff --exit-code -- app/datos.py` | Boot 1100x700 rail 64px; resize 1300x800 expands; manual toggle | `git revert` PR1; adapter keeps v1 screens |
| 2 | Slice-b dashboard focal+calendar | PR2 on PR1 | `python -m py_compile app/screens/dashboard.py app/widgets.py` + datos diff cero | Hoy FS36 border; day/week/month toggle | `git revert` PR2; shell intact |
| 3 | Slice-c 3 tablas toolbar+pager | PR3 on PR2 | `python -m py_compile` stock+clientes+fiado; pager 23-row check | Search filters; pager 1→3 de 3; density uniform | `git revert` PR3; dashboard intact |
| 4 | Slice-d caja+chat cierre | PR4 on PR3 | `python -m py_compile app/screens/caja.py app/screens/chat.py`; grep literals clean | Caja Cobrar flow; chat dividers+empty-state | `git revert` PR4; resto intacto |

## Phase 1: Slice-a Shell + Tokens + Adapter

- [x] 1.1 Extend `app/theme.py` with SHELL_* constants + focal/calendar steps, cero hex nuevo
- [x] 1.2 Add `Shell`, `Topbar`, `Sidebar`, `PageHeader` to `app/widgets.py`, keep `AppDialog`/`feedback`
- [x] 1.3 Rebuild `app/main.py` with `Shell` + adapter slot + `shell.navigate(key)`
- [x] 1.4 Wire `app/screen_base.py` padding + RESIZED spike + mandatory manual rail toggle
- [x] 1.5 Gate slice-a V2-D5 (sync_text, on_select, dialog, feedback, focus) + `app/datos.py` (read-only) diff cero

## Phase 2: Slice-b Dashboard Focal + Calendar

- [x] 2.1 Add `Section`, `StatGrid`, `Calendar` view-only to `app/widgets.py`
- [x] 2.2 Recompose `app/screens/dashboard.py` Hoy FS36 border + trio FS28 + view-side series
- [x] 2.3 Gate slice-b V2-D5 + contrast re-proof + `app/datos.py` (read-only) diff cero

## Phase 3: Slice-c Tables Toolbar + Density + Pager

- [x] 3.1 Add `TableToolbar`, `TablePager`, denser `AppTable` page_size=10 to `app/widgets.py`
- [x] 3.2 Migrate `app/screens/stock.py`, `app/screens/clientes.py`, `app/screens/fiado.py` to toolbar+pager view-side
- [x] 3.3 Gate slice-c V2-D5 + pager bounds + `app/datos.py` (read-only) diff cero

## Phase 4: Slice-d Caja + Chat + Closure

- [ ] 4.1 Rework `app/screens/caja.py` into `Section` hierarchy, keep Cobrar flow + `AppDialog`
- [ ] 4.2 Polish `app/screens/chat.py` dividers + empty-state + bubbles, keep responder
- [ ] 4.3 Final gate: grep literals clean + `landing/` (read-only) diff cero + contrast table + `app/datos.py` (read-only) diff cero
