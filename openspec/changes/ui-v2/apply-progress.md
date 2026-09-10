# Apply Progress: ui-v2 — Visual Rebuild Faithful to Figma

Branch: `feat/ui-figma-v2` (exclusive). Base: `origin/feat/ui-figma-v2`.
Tasks: `openspec/changes/ui-v2/tasks.md` 14/14 `[x]`.
Commits: 4 work-unit slice commits. This closeout adds only this file. Zero code.

## Slice-a — Shell + Tokens + Adapter (tasks 1.1-1.5)

Tasks: 1.1 SHELL_* constants + focal/calendar steps; 1.2 Shell/Topbar/Sidebar/PageHeader;
1.3 main.py Shell + adapter slot + navigate; 1.4 screen_base padding + RESIZED + rail toggle;
1.5 V2-D5 gate + datos.py read-only diff zero.
Files: `app/main.py`, `app/screen_base.py`, `app/theme.py`, `app/widgets.py`.
Commit: `4c1c4a6` (`4c1c4a6d02b0a106478175ff305fac56c8df83b8`)
  `feat(ui-v2): slice-a shell Paperpillar mas tokens y adapter (1.1-1.5)`.
Lines (code only): 430 insertions / 116 deletions / 546 changed.
  Detail: main.py 29+/110-, screen_base.py 9+/3-, theme.py 16+/0-, widgets.py 376+/3-.
  Plus `tasks.md` 52+/0- checkbox/plan bookkeeping in the same work unit.
Verification: boot 1100x700 rail 64px collapsed; resize 1300x800 expands past
  1280x760 breakpoint; manual rail toggle fallback; V2-D5 preserved
  (sync_text, on_select, dialog, feedback, focus); datos.py diff zero.

## Slice-b — Dashboard Focal + Calendar (tasks 2.1-2.3)

Tasks: 2.1 Section/StatGrid/Calendar view-only; 2.2 dashboard Hoy FS36 border +
  trio FS28 + view-side series; 2.3 V2-D5 + contrast re-proof + datos diff zero.
Files: `app/screens/dashboard.py`, `app/widgets.py`.
Commit: `3672c17` (`3672c17b1c3b7da9af228592e3f23f40d5b706f8`)
  `feat(ui-v2): slice-b dashboard focal mas calendario view-only (2.1-2.3)`.
Lines (code only): 332 insertions / 27 deletions / 359 changed.
  Detail: dashboard.py 170+/27-, widgets.py 162+/0-. Plus `tasks.md` 3+/3-.
Verification: Hoy focal FS36 with 2px primary border; day/week/month toggle over
  view-side ventas grouping; contrast re-proof against frozen pairs; datos diff zero.

## Slice-c — Tables Toolbar + Density + Pager (tasks 3.1-3.3)

Tasks: 3.1 TableToolbar/TablePager + denser AppTable page_size=10; 3.2 migrate
  stock/clientes/fiado to toolbar+pager view-side; 3.3 V2-D5 + pager bounds + datos zero.
Files: `app/screens/stock.py`, `app/screens/clientes.py`, `app/screens/fiado.py`,
  `app/widgets.py`.
Commit: `1c29bf0` (`1c29bf0a203776dd607e37f4d573238e95634316`)
  `feat(ui-v2): slice-c tablas densas toolbar pager 10 por pagina (3.1-3.3)`.
Lines (code only): 390 insertions / 100 deletions / 490 changed.
  Detail: clientes.py 83+/34-, fiado.py 65+/21-, stock.py 81+/43-,
  widgets.py 161+/2-. Plus `tasks.md` 3+/3-.
Verification: search filters view-side; pager "1 de 3" bounds with 23-row check;
  uniform density; V2-D5 preserved; datos.py diff zero.

## Slice-d — Caja + Chat Closure (tasks 4.1-4.3)

Tasks: 4.1 caja Section hierarchy keeping Cobrar flow + AppDialog; 4.2 chat dividers +
  empty-state + bubbles keeping responder; 4.3 final gate (literals clean + landing
  zero + contrast table + datos zero).
Files: `app/screens/caja.py`, `app/screens/chat.py`, `app/widgets.py` (cleanup).
Commit: `6fbbdc1` (`6fbbdc162dd1fbf4d317fa0d1f86428969230de8`)
  `feat(ui-v2): slice-d caja chat cierre en shell con Sections y PageHeader (4.1-4.3)`.
Lines (code only): 96 insertions / 86 deletions / 182 changed.
  Detail: caja.py 60+/54-, chat.py 35+/21-, widgets.py 1+/11-. Plus `tasks.md` 3+/3-.
Verification: Caja Cobrar flow intact; chat dividers + empty-state; literal grep clean;
  landing/ zero diff; contrast table; datos.py zero diff.

## Totals vs origin/feat/ui-figma-v2 (code, excl. tasks.md)

`git diff origin/feat/ui-figma-v2...HEAD --numstat`: 1236 insertions /
317 deletions / 1553 changed lines across 10 code files.
Including `tasks.md` plan bookkeeping (52+/0- net): 1288 insertions / 317 deletions.
Per-slice code changed: a 546 + b 359 + c 490 + d 182 = 1577 (summed per commit;
HEAD net is 1553 because widgets.py cleanup in slice-d supersedes earlier adds).

## Global Gates (closeout re-check, read-only)

- Datos diff zero: `git diff origin/feat/ui-figma-v2...HEAD -- app/datos.py` empty. PASS.
- Landing zero: `git diff origin/feat/ui-figma-v2...HEAD -- landing/` empty. PASS.
- Zero new hex: `git grep -E "#[0-9a-fA-F]{3,8}"` outside `app/theme.py`
  (widgets, main, all screens, screen_base) returns no matches. Hex stays confined
  to frozen `PaletteTheme` tokens plus contrast docstring. PASS.
- AA: no new color roles; additive SHELL_* layout constants only; reuse of proven
  pairs documented in `app/theme.py` (>=4.5 normal text, >=3.0 large/UI). PASS.
- V2-D5: sync_text via on_change, Dropdown on_select (Flet 0.84), AppDialog kit,
  feedback, focus preserved per slice gate. PASS.
- Syntax (read-only, zero writes): `ast.parse` OK on all 10 touched files. PASS.

## Closeout Scope

This file only. No code, no `tasks.md` edits, no push, no PR.
Next: verify phase, then archive.
