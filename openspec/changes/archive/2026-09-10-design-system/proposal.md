# Proposal: Unified Design System (geskio)

## Intent

Two UI worlds share no tokens: six Flet screens hardcode style; landing uses CSS vars. Unify into one namespace to kill drift and enable per-screen migration.

## Scope

### In Scope
- `app/theme.py`: color/type/space/radius; multi-theme `app_colors`; spacing + radii frozen (D3).
- `app/widgets.py`: AppCard, AppHeader, AppTable, AppDialog, feedback, bubbles.
- Migrate 6 screens; normalize `column_spacing`, `Divider`, radii, Fiado naming.
- `design.md`: unified matrix (Paperpillar shell anchor; rest re-expressed).
- Landing token alignment (D4).

### Out of Scope
- SQLite persistence; real LLM in chat; landing form backend.
- CRM-04 patterns: deferred until canvas verification; zero v1 contribution.

## Capabilities

### New Capabilities
- `design-tokens`: token namespace, multi-theme `app_colors` (red primary, green semantic), frozen scale.
- `widget-kit`: shared Flet components with fixed defaults.
- `brand-alignment`: app+landing convergence and drift normalization.

### Modified Capabilities
- None (no `openspec/specs/` exist).

## Approach

Tokens → kit → per-screen slices (D5, auto-chain, 800 lines): `theme.py` from exploration values → `widgets.py` → dashboard → caja/stock → clientes/fiado → chat + landing. Research gives patterns only, never values.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app/theme.py` | New | Tokens from exploration + D1–D5 |
| `app/widgets.py` | New | Kit on tokens |
| `app/screens/*.py` + `screen_base.py` | Modified | Token + kit adoption |
| `landing/styles.css`, `index.html` | Modified | Token alignment only |
| `design.md` | New | Unified matrix |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Accent rework | Low | D2 decided; green stays semantic |
| Flet 0.84.0 unpinned drift | Med | Verify API; no font bundling in v1 |
| Slice >800 lines | Med | One screen per slice |

## Rollback Plan

Revert per slice: each screen is one commit/PR. Tokens isolated in `app/theme.py`. Landing change is CSS-var-only, one-commit revert.

## Dependencies

- `exploration.md` (values) + `research.md` rev 3 (patterns) + D1–D5 rev 3, `proposal_ready: true`.

## Success Criteria

- [ ] Tokens + kit exist; no hardcoded style in 6 screens
- [ ] Spacing, `Divider`, radii, Fiado naming consistent
- [ ] Landing on shared tokens; no regression
- [ ] Slices ≤800 lines; `design.md` traces patterns
