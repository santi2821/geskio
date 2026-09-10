# Dashboard Composition Specification

## Purpose

Recompose `app/screens/dashboard.py` (slice b) from equal-weight v1 cards into a Von Restorff focal hierarchy plus a view-only calendar. All aggregation is view-side over FROZEN `datos.py` reads (`ventas`, `cuentas.created_at`); no API or schema change.

## Requirements

### Requirement: Focal Stat Hierarchy (Von Restorff)

The dashboard MUST present one visually dominant focal stat **"Hoy"**: font size 36 (`accent_text` value) on a surface card with a 2px primary border, spanning the full content width. It MUST be visually distinct from all other stats.

#### Scenario: Focal stat is dominant

- GIVEN the dashboard renders
- WHEN the "Hoy" card is inspected
- THEN it uses FS_36 with `accent_text`, a 2px primary border, spans the row width, and no other stat card shares this treatment

### Requirement: Secondary Stat Grid

The dashboard MUST render the secondary trio (Mes, Ganancia, Deben) in a `StatGrid` (`ft.ResponsiveRow`) at font size 28, each colored by its semantic role (accent/green-semantic/danger). Secondary cards MUST NOT use the focal treatment (2px border).

#### Scenario: Trio renders without focal treatment

- GIVEN the secondary stats render in the StatGrid
- WHEN each card is inspected
- THEN it uses FS_28, its semantic role color, and no 2px primary border

### Requirement: View-Only Calendar

The dashboard MUST include a `Calendar` widget with a `SegmentedButton` offering day/week/month views. Toggle MUST be the only interaction (no creation, edit, or click-through). Rendering MUST be: day = selected day's `ventas` list; week = last-7-day totals; month = grid of per-day totals.

#### Scenario: Day view lists sales

- GIVEN the calendar is in day view for date D
- WHEN the series is built
- THEN it lists the day-D `ventas` entries only

#### Scenario: Week view shows 7-day totals

- GIVEN the calendar is in week view
- WHEN the series is built
- THEN it shows totals for the last 7 days derived from `ventas`

#### Scenario: Month view shows per-day grid

- GIVEN the calendar is in month view
- WHEN the series is built
- THEN it renders a grid with a per-day total for each day of the month

#### Scenario: Toggle is the only interaction

- GIVEN the calendar renders
- WHEN the user interacts with it
- THEN only the day/week/month `SegmentedButton` changes state; no other control mutates data or navigates

### Requirement: View-Side Derivation over Frozen Reads

All calendar/aggregation data MUST be derived in view-side helpers grouping `ventas` (`fecha`, `total`); the overdue badge list MAY use `cuentas.created_at`. No new function, schema, or read MAY be added to `app/datos.py` (gate: `git diff --exit-code -- app/datos.py`).

#### Scenario: Zero datos.py diff

- GIVEN slice b is implemented
- WHEN `git diff --exit-code -- app/datos.py` runs
- THEN it exits clean with zero diff

#### Scenario: Series resolves from existing reads

- GIVEN the calendar needs a series
- WHEN data is fetched
- THEN it comes from existing `ventas` reads grouped view-side (no new `datos.py` API call)
