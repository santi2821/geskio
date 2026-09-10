# Design Tokens Specification (geskio)

## Purpose

Single token namespace (`app/theme.py`) replacing per-screen hardcoded style in the 6 Flet screens. Sources values from `exploration.md` (landing CSS vars + app patterns); reference kits (research rev 3) contribute patterns only. Decisions: D1 (one namespace, Paperpillar anchor), D2 (red primary, green semantic, multi-theme `app_colors`), D3 (spacing + radii frozen upfront).

## Requirements

### Requirement: Single Token Namespace

The system MUST define all color, typography, spacing, and radius tokens in one module (`app/theme.py`) under one namespace. No other module MAY define style constants. Paperpillar (reference 01) anchors shell structure; references 02–05 contribute patterns re-expressed in this namespace, never verbatim styles (anti-frankenstein).

#### Scenario: Screens import tokens only

- GIVEN the 6 migrated screens (`dashboard`, `caja`, `stock`, `clientes`, `fiado`, `chat`)
- WHEN a grep runs for color/padding/radius literals (e.g. `ft.Colors`, raw hex, inline padding numbers) in `app/screens/*.py`
- THEN zero style literals are found — every style value resolves to a `theme.py` import

#### Scenario: Reference pattern is re-expressed, not copied

- GIVEN a pattern adopted from references 02–05 (e.g. WellNest stats card, SnowUI table)
- WHEN its implementation is reviewed
- THEN its styling uses `theme.py` tokens only, and `design.md` records the re-expression mapping

### Requirement: Primary and Semantic Color Roles (D2)

The system MUST define primary as the landing accent red family (`#ef4444` light / `#f43f5e` dark from exploration). Green SHALL remain a semantic role (success/money states) and MUST NOT be the primary CTA color. Dashboard stat colors (Hoy/Mes/Ganancia/Deben) MUST be defined as semantic roles, not per-screen literals.

#### Scenario: CTA uses primary

- GIVEN any primary action button (e.g. `Cobrar` in caja)
- WHEN it is rendered
- THEN its background is the primary red role and its text is the on-primary role

#### Scenario: Green stays semantic

- GIVEN the paid/success states in fiado and the money-related stat
- WHEN colors are resolved
- THEN green appears only in success/money semantic roles, never as primary CTA

### Requirement: Multi-Theme `app_colors` with Personalization (D2)

The system MUST provide `app_colors` supporting at least 2 complete themes (light + dark) plus a personalization mechanism (per-theme accent override) for the user.

#### Scenario: Theme switch

- GIVEN `app_colors` with ≥2 registered themes
- WHEN the active theme changes
- THEN every token resolves consistently in the new theme with no screen-level edits

#### Scenario: Personalized accent

- GIVEN the personalization mechanism
- WHEN a user overrides the accent role
- THEN all primary usages reflect the override without touching `theme.py` internals

### Requirement: Frozen Spacing and Radii Scale (D3)

The system MUST freeze the spacing scale (4px grid; steps 4/8/10/12/20/24 from exploration) and radii scale (10/12/18/pill from landing CSS vars) upfront. Screens and widgets MUST use only scale values.

#### Scenario: Off-scale value rejected in review

- GIVEN a proposed screen change using an off-scale padding or radius
- WHEN reviewed against the frozen scale
- THEN the change is rejected unless `theme.py` first adds the value as a named token

### Requirement: Typography Scale

The system MUST define text style tokens for sizes 12/13/14/16/18/20/28/30/36 with the weights observed in exploration. Font family SHOULD resolve to Inter when available without bundling; it MAY fall back to the platform default (no font bundling in v1).

#### Scenario: Text styles resolve from tokens

- GIVEN a migrated screen rendering headings, labels, values, and body text
- WHEN inspected
- THEN every `Text` style comes from a named typography token (e.g. `label`, `value_28`, `header_30`)

### Requirement: Token-Source Provenance

The system SHOULD document, per token group, its source: landing CSS vars (colors/radii/typography) or app patterns (spacing). Research numeric values MUST NOT be sourced from references (corpus has none — C0.3).

#### Scenario: Value has a source

- GIVEN any token value in `theme.py`
- WHEN traced in `design.md`
- THEN it maps to an exploration value (landing CSS var or app pattern), never to a research/Figma measurement
