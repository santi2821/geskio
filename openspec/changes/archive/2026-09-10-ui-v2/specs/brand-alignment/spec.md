# Delta for brand-alignment

## MODIFIED Requirements

### Requirement: Sliced Delivery Budget (D5)

Implementation MUST be delivered as shell-first slices a–d under auto-chain on `feat/ui-figma-v2` (`base-primer-commit` frozen), each ≤800 review lines, in the order: (a) shell + token extension + adapter; (b) dashboard stats + calendar; (c) tables (stock/clientes/fiado); (d) caja + chat. Tokens MUST stay isolated in `theme.py`; each slice MUST be independently revertible; every slice MUST gate on `git diff --exit-code -- app/datos.py` and preserve V2-D5 fixes (sync_text, on_select, AA roles, `:focus-visible`, AppDialog, feedback).
(Previously: per-screen slices ordered theme.py → widgets.py → dashboard → caja/stock → clientes/fiado → chat + landing.)

#### Scenario: Slice budget enforced

- GIVEN any implementation slice
- WHEN its changed-lines are counted
- THEN the total is ≤800; if one slice exceeds the budget, it is split or rejected, never merged over budget

#### Scenario: Token isolation enables rollback

- GIVEN a defective screen slice
- WHEN it is reverted
- THEN `theme.py` and other migrated screens are unaffected

#### Scenario: datos.py frozen per slice

- GIVEN slice a, b, c, or d lands
- WHEN `git diff --exit-code -- app/datos.py` runs
- THEN it exits clean with zero diff

## ADDED Requirements

### Requirement: Parity Trace Extended to New Roles

The landing 1:1 token parity MUST continue to hold. Every NEW usage pair introduced by ui-v2 (shell idle/active, chips, calendar today/totals, focal accent) MUST be added to the unified trace in `design.md` mapping each to its verified source pair. Landing MUST remain untouched (no layout/interaction changes) — parity is a trace + re-proof obligation only.

#### Scenario: New roles traced to proven pairs

- GIVEN the extended parity trace
- WHEN each NEW usage pair is reviewed
- THEN it names the verified pair it reuses (e.g. `accent_soft`/`on_accent_soft`) and no new hex appears in the trace

#### Scenario: Landing stays 1:1

- GIVEN ui-v2 slices land
- WHEN shared landing roles (bg, surface, text, border, accent red, radius, spacing) are compared
- THEN they match value-for-value in light and dark and `landing/` shows zero diff
