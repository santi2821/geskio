# Proposal: ui-v2 — Visual Rebuild Faithful to Figma

## Intent
Replace flat top-nav Flet UI with Paperpillar-anchored shell and recomposed screens. Patterns-only fidelity (layout/composition/density/hierarchy, never pixels). Zero logic change; `app/datos.py` FROZEN (V2-D2).

## Scope

### In Scope
- Shell sidebar+topbar with adapter to current screens (V2-D1)
- Dashboard recomposed: Von Restorff focal + view-only calendar over `ventas`/`created_at`
- Tables SnowUI: toolbar (search/chips/actions), density, pagination affordance (stock/clientes/fiado)
- Forms normalized: caja sheet/section hierarchy, chat polish (dividers, empty-state)
- Tokens re-expressed if needed with AA gate + landing 1:1 parity (V2-D4)
- Preserve v1 fixes: sync_text, on_select, AA roles, :focus-visible, AppDialog, feedback (V2-D5)

### Out of Scope
- `app/datos.py` logic, schema, or API changes
- New features, backend, persistence
- CRM-04 (zero contribution)
- Landing layout/interaction rewrite (parity trace only)
- Pixel-perfect copy; login-gated canvas measurements

## Capabilities

### New Capabilities
- `app-shell`: sidebar + topbar + content area + adapter + collapse rule at 1100x700
- `dashboard-composition`: focal stat hierarchy + view-only calendar aggregation
- `table-density`: toolbar/density/pagination pattern applied to 3 table screens

### Modified Capabilities
- `design-tokens`: restructure allowed (shell/stat/elevation roles) with AA gate
- `widget-kit`: add Shell, Topbar, Sidebar, PageHeader, Section, StatGrid, Calendar, TableToolbar; denser AppTable
- `brand-alignment`: extend parity trace to new roles; no landing rewrite

## Approach
Shell-new-first (V2-D1, V2-D3): (a) shell slice + token extensions + adapter; (b) dashboard stats+calendar; (c) tables; (d) caja+chat. Slices ≤800 lines, auto-chain on `feat/ui-figma-v2`. `base-primer-commit` frozen. Collapse at 1100x700 defined in design (V2-D6).

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app/main.py` | New | Sidebar+topbar shell, adapter |
| `app/screens/dashboard.py` | Modified | Focal stats + calendar view-only |
| `app/screens/stock.py`, `clientes.py`, `fiado.py` | Modified | Toolbar + denser AppTable |
| `app/screens/caja.py`, `chat.py` | Modified | Form/sheet hierarchy, polish |
| `app/theme.py`, `app/widgets.py` | Modified | Shell/stat tokens, kit extension |
| `app/datos.py` | Untouched | Frozen contract, view-side derive only |
| `landing/` | Untouched | Out of visual scope |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| AA regression (new roles) | Med | Gate: ≥4.5 normal / ≥3:1 large+UI; re-prove 19/19 |
| DataTable ceiling | Med | Design spike; fallback composed Column/Row |
| A11y loss (sync_text, on_select, focus, dialog) | Med | Per-slice gate on V2-D5 |
| datos.py temptation | Low | View-side helpers only; diff must be zero |
| Collapse undefined | Med | Must be decided in design (V2-D6) |

## Rollback Plan
Per-slice `git revert` on `feat/ui-figma-v2` (never touch `base-primer-commit`). Adapter keeps unmigrated screens renderable, so reverting any slice restores prior shell/screen. Tokens isolated: screen revert leaves `theme.py` intact. Zero `datos.py` diff means no data migration to undo.

## Dependencies
- Branch `feat/ui-figma-v2` exclusive; `base-primer-commit` frozen
- Pinned `flet==0.84.0`; patterns-only Figma (research rev3 background, non-authoritative)

## Success Criteria
- [ ] Shell renders with adapter; old screens load inside new shell
- [ ] Dashboard focal + calendar view-only from existing reads
- [ ] 3 table screens share toolbar/density pattern
- [ ] New roles pass AA gate; landing parity 1:1 holds
- [ ] V2-D5 fixes preserved; each slice ≤800; `datos.py` diff zero
