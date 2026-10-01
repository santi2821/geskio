# Brand Alignment Specification (geskio)

## Purpose

Convergence between the Flet app and the landing site, plus normalization of copy-paste drift found in exploration. Decisions: D2 (red primary, green semantic), D4 (landing in scope for token alignment), D5 (per-screen slices, auto-chain, 800-line review budget). Research 04 (CRM) contributes zero patterns in v1.

## Current Implementation Reconciliation

The requirements below record the original UI exploration. For the current application, the implemented red/green light/dark palettes in `app/theme.py` are authoritative; exact 1:1 hex parity with landing CSS is not assumed for alternate brands or custom accents. The landing keeps its existing layout and interactions, while truthful copy may be updated when product capabilities change. Shared Flet component names are documented in `widget-kit/spec.md`. The old fixed branch/base-commit, 800-line budget, and `app/datos.py`-must-never-change instructions are historical delivery constraints, not current product requirements; scoped data-integrity work may change that module.

## Requirements

### Requirement: App–Landing Token Convergence (D2, D4)

`theme.py` tokens and landing CSS vars MUST be 1:1 mapped (names + values). Landing changes MUST be limited to CSS variable alignment (no layout/interaction rewrites). `design.md` MUST trace the unified matrix: Paperpillar shell anchor; 02–05 re-expressed; every token has a source.

#### Scenario: Token parity check

- GIVEN the token namespace and `landing/styles.css` `:root` / `[data-theme="dark"]`
- WHEN parity is verified
- THEN shared roles (bg, surface, text, border, accent red, radius, spacing steps) match value-for-value in light and dark

#### Scenario: `design.md` traces the matrix

- GIVEN the unified matrix in `design.md`
- WHEN reviewed
- THEN each pattern entry names its reference, its re-expression, and no entry cites reference 04 (see Requirement: CRM-04 Zero Contribution)

### Requirement: Drift Normalization

The shared implementation MUST normalize visual drift through named tokens and helpers. The current app uses a compact 10px card/field radius, 12px table spacing, shared divider tokens, and `Fiado` as the account screen name.

#### Scenario: Spacing inconsistency eliminated

- GIVEN the six migrated screens
- WHEN their `column_spacing`, `Divider` usage, and card radii are compared
- THEN all resolve to the same token values (12, standard divider height, radius 12)

#### Scenario: Fiado naming consistent

- GIVEN the fiado screen header
- WHEN rendered
- THEN its title matches the nav label `Fiado` (no `Cuenta Corriente` remains)

### Requirement: Landing No Regression

Landing changes MUST preserve existing behavior: navbar blur/scrolled state, mobile drawer, theme toggle with `localStorage geskio-theme` persistence, reveal observer, marquee, contact form flow, and footer year. Factual copy may be corrected without changing those flows or the page layout.

#### Scenario: Landing behaviors survive

- GIVEN the landing after token alignment
- WHEN nav scroll, drawer, theme toggle, reveal, marquee, and form are exercised
- THEN each behaves as before with no console errors and no markup-structure changes beyond class/var usage

#### Scenario: Revert isolation

- GIVEN the landing commit
- WHEN reverting it
- THEN app slices are unaffected (separate commits per slice)

### Requirement: CRM-04 Zero Contribution

`design.md` v1 and all tokens/kit MUST NOT include any pattern from reference 04 (CRM) until logged-in canvas verification. The pointer stays explicit with its deferral status.

#### Scenario: Trace check excludes 04

- GIVEN `design.md` v1 and the spec files
- WHEN searched for reference-04-derived patterns
- THEN none exist; reference 04 appears only as a deferred pointer with zero contribution

### Requirement: Sliced Delivery Budget (D5)

Implementation changes MUST be scoped, reviewable, and covered by tests appropriate to the change. Data-model changes MUST preserve migration, rollback, and persistence guarantees; they are allowed when required by data-integrity work. Branch names, commit boundaries, and delivery order are selected per task.

#### Scenario: Scoped change is reviewed

- GIVEN any implementation change
- WHEN its changed-lines are counted
- THEN its touched routes and rationale are documented, and large changes are separated into reviewable parts

#### Scenario: Token source stays centralized

- GIVEN a screen uses shared palette or geometry styles
- WHEN those styles are changed
- THEN shared roles and dimensions remain defined in `theme.py`

#### Scenario: Data change is covered

- GIVEN a scoped change modifies `app/datos.py`
- WHEN the change is reviewed
- THEN migration, persistence, validation, and rollback behavior are tested as applicable

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
