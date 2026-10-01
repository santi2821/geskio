# Dashboard Composition Specification

## Purpose

Compose `app/screens/dashboard.py` with a focal sales hierarchy and a view-only calendar. Summary metrics use the domain's `stats()` result; the calendar groups sales by their ISO date. Margin is calculated from the cost saved on each sale. Migrated legacy sales without a recorded cost are excluded and counted; their costs are never guessed from the current catalog.

## Requirements

### Requirement: Focal Stat Hierarchy (Von Restorff)

The dashboard MUST present one visually dominant focal stat **"Hoy"** on a neutral surface with a stronger primary leading edge, spanning the full content width. It MUST be visually distinct from all other stats through hierarchy and placement, not a decorative colored fill.

#### Scenario: Focal stat is dominant

- GIVEN the dashboard renders
- WHEN the "Hoy" card is inspected
- THEN it uses a neutral text color, neutral surface and stronger primary leading edge, spans the row width, and no other stat card shares this treatment

### Requirement: Secondary Stat Grid

The dashboard MUST render the secondary trio (Ventas del mes, Margen registrado del mes, Por cobrar) through `grilla_stats()` and its `ft.ResponsiveRow` with consistent typography. Neutral values are default; success and danger use semantic color according to the registered margin sign. Secondary cards MUST NOT use the focal treatment (2px border). The explanatory text MUST state that the margin uses sale-time costs or report how many legacy sales without costs were excluded.

#### Scenario: Trio renders without focal treatment

- GIVEN the secondary stats render through `grilla_stats()`
- WHEN each card is inspected
- THEN the labels are "Ventas del mes", "Margen registrado del mes" and "Por cobrar"; it uses consistent stat typography, semantic success/danger color only where relevant, and no focal leading edge

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

### Requirement: Calendar Series Derivation

Calendar series MUST be derived in view-side helpers grouping `ventas` by `fecha` and `total`; the overdue badge list MAY use `cuentas.created_at`. Summary card aggregates are read from the domain's `stats()` function.

#### Scenario: Calendar series resolves from sales dates

- GIVEN the calendar needs a series
- WHEN data is fetched
- THEN it comes from `ventas` reads grouped by ISO date in view-side helpers

### Requirement: Bounded Alert Preview

The Dashboard MUST show the total number of active stock/debt alerts, preview no more than four rows, and provide clear navigation to Stock and Fiado. Alert counts and labels MUST remain understandable without color alone.

#### Scenario: Many alerts exist

- GIVEN more than four low-stock or unpaid-account alerts
- WHEN the Dashboard renders
- THEN it shows the total count, at most four previews, and direct links to Stock and Fiado

#### Scenario: No active alerts

- GIVEN no product at or below minimum and no unpaid account
- WHEN the Dashboard renders
- THEN it shows an explicit all-clear state
