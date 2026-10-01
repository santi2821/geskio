# Design Tokens Specification (geskio)

## Purpose

Single token namespace (`app/theme.py`) for application palettes, semantic roles, typography, spacing, radii, and shell dimensions. GesKio currently supports red and green brands in light and dark modes, plus user-selected accent colors. The landing has its own CSS tokens; any cross-surface differences are documented instead of assumed to match.

## Requirements

### Requirement: Single Token Namespace

The system MUST define shared color palettes, semantic roles, typography, spacing, radius, and shell-size constants in one module (`app/theme.py`). Screen modules MUST NOT define duplicate style constants. Reusable UI patterns are implemented through named helpers in `app/widgets.py`.

#### Scenario: Screens import tokens only

- GIVEN the GesKio app screens
- WHEN a grep runs for color/padding/radius literals (e.g. `ft.Colors`, raw hex, inline padding numbers) in `app/screens/*.py`
- THEN shared colors and dimensions come from `theme.py`; examples in labels or validation messages are not style literals

#### Scenario: Reference pattern is re-expressed, not copied

- GIVEN a pattern adopted from references 02–05 (e.g. WellNest stats card, SnowUI table)
- WHEN its implementation is reviewed
- THEN its styling uses `theme.py` tokens only, and `design.md` records the re-expression mapping

### Requirement: Primary and Semantic Color Roles (D2)

Each brand/mode palette MUST define its own primary and on-primary pair. The green palette MAY use green as its primary; the red palette uses red. Success, warning, danger, and information roles MUST retain their semantic meaning. Dashboard stat colors MUST resolve through semantic roles, not per-screen hex literals.

#### Scenario: CTA uses primary

- GIVEN any primary action button (e.g. `Cobrar` in caja)
- WHEN it is rendered
- THEN its background is the active palette's primary role and its text is the on-primary role

#### Scenario: Brand and semantic greens are distinct

- GIVEN the paid/success states in fiado and the money-related stat
- WHEN colors are resolved
- THEN the green brand may use a green primary pair, while success/money status uses the semantic success role

### Requirement: Multi-Theme `Tema` with Personalization (D2)

The system MUST provide `Tema` supporting the red and green brand families in light and dark modes plus a validated accent override for the user.

#### Scenario: Theme switch

- GIVEN `Tema` with ≥2 registered brand families
- WHEN the active theme changes
- THEN every token resolves consistently in the new theme with no screen-level edits

#### Scenario: Personalized accent

- GIVEN the personalization mechanism
- WHEN a user overrides the accent role
- THEN all primary usages reflect the override without touching `theme.py` internals

### Requirement: Frozen Spacing and Radii Scale (D3)

The shared spacing scale is 4/8/10/12/16/20/24 and the radius scale is 8/10/16/pill. Small controls use 8px, fields/cards/dialogs use 10px, and larger panels use 16px. Calendar cells may remain tighter where density requires it.

#### Scenario: Off-scale value rejected in review

- GIVEN a proposed screen change using an off-scale padding or radius
- WHEN reviewed against the frozen scale
- THEN the change is rejected unless `theme.py` first adds the value as a named token

### Requirement: Typography Scale

The system MUST define text-size tokens in `theme.py` for the sizes used by current screens. Font family SHOULD resolve to Inter when available without bundling; it MAY fall back to the platform default.

#### Scenario: Text styles resolve from tokens

- GIVEN a migrated screen rendering headings, labels, values, and body text
- WHEN inspected
- THEN sizes come from named tokens such as `FS_14`, `FS_24`, or `FS_36`

### Requirement: Token-Source Provenance

The system SHOULD document, per token group, its source: landing CSS vars (colors/radii/typography) or app patterns (spacing). Research numeric values MUST NOT be sourced from references (corpus has none — C0.3).

#### Scenario: Value has a source

- GIVEN any token value in `theme.py`
- WHEN traced in `design.md`
- THEN it maps to a documented app or landing value; equality across those surfaces is claimed only when verified

### Requirement: Shell and Compact Layout Tokens

Shell dimensions and breakpoints MUST be named non-color module constants in `theme.py`: `LATERAL_ANCHO=240`, `RAIL_ANCHO=64`, `SUPERIOR_ALTO=56`, `RUPTURA_ANCHO=1024`, `RUPTURA_ALTO=600`, and `ANCHO_TOPBAR_COMPACTO=600`. Bounded cart geometry MUST use named `CARRITO_ALTO_MIN`, `CARRITO_ALTO_POR_ITEM`, and `CARRITO_ALTO_MAX` tokens. Theme palettes MAY define colors only in `theme.py`; screen-specific colors are not allowed.

#### Scenario: Zero new hex constants

- GIVEN slice a extends `theme.py`
- WHEN the file is diffed
- THEN added shell geometry uses named constants and any new palette color is defined in `theme.py`

#### Scenario: Shell constants are named tokens

- GIVEN `main.py` renders sidebar, rail, and topbar
- WHEN dimensions are resolved
- THEN they come from `LATERAL_ANCHO`, `RAIL_ANCHO`, and `SUPERIOR_ALTO`

### Requirement: New Usage Pairs Reuse Verified AA Roles (AD-6)

The 19/19 proven AA pairs MUST be reused unchanged: `danger`/`danger_text`, `accent`/`accent_text`, `footer_hover` (landing parity), and `_ROLE_ALIASES`. New usage mapping MUST be: sidebar idle = `text_muted` on `bg_soft`; sidebar active = `accent_soft`/`on_accent_soft`; chips = surface+border or `accent_soft` pair; calendar today = `accent_soft` pair; calendar totals = `text` on `surface`. Every NEW usage pair MUST be re-proved in a contrast table (≥4.5:1 normal text, ≥3:1 large text + UI components).

#### Scenario: Contrast re-proof table complete

- GIVEN the set of NEW usage pairs introduced by ui-v2
- WHEN the contrast table is checked against `theme.py` docstring values
- THEN every pair meets ≥4.5:1 (normal) or ≥3:1 (large/UI) and none introduces an unverified pair
