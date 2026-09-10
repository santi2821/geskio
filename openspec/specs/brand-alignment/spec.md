# Brand Alignment Specification (geskio)

## Purpose

Convergence between the Flet app and the landing site, plus normalization of copy-paste drift found in exploration. Decisions: D2 (red primary, green semantic), D4 (landing in scope for token alignment), D5 (per-screen slices, auto-chain, 800-line review budget). Research 04 (CRM) contributes zero patterns in v1.

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

The change MUST normalize the exploration drifts: `column_spacing` 16→12 (clientes), `Divider` heights (dashboard 20 vs fiado 4 → one standard via tokens), cart radius 8→12, and the `fiado.py` title `Cuenta Corriente` → nav name `Fiado`.

#### Scenario: Spacing inconsistency eliminated

- GIVEN the six migrated screens
- WHEN their `column_spacing`, `Divider` usage, and card radii are compared
- THEN all resolve to the same token values (12, standard divider height, radius 12)

#### Scenario: Fiado naming consistent

- GIVEN the fiado screen header
- WHEN rendered
- THEN its title matches the nav label `Fiado` (no `Cuenta Corriente` remains)

### Requirement: Landing No Regression

Landing changes MUST NOT alter existing behavior: navbar blur/scrolled state, mobile drawer, theme toggle with `localStorage geskio-theme` persistence, reveal observer, marquee, contact form flow, footer year. The landing revert MUST remain a single-commit change (CSS-var-only diff).

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

Implementation MUST be delivered as per-screen slices under auto-chain, each ≤800 review lines, one screen per slice, in the order: `theme.py` → `widgets.py` → dashboard → caja/stock → clientes/fiado → chat + landing. Tokens are isolated in `theme.py`; each slice is independently revertible.

#### Scenario: Slice budget enforced

- GIVEN any implementation slice
- WHEN its changed-lines are counted
- THEN the total is ≤800; if one screen exceeds the budget, it is split or rejected, never merged over budget

#### Scenario: Token isolation enables rollback

- GIVEN a defective screen slice
- WHEN it is reverted
- THEN `theme.py` and other migrated screens are unaffected
