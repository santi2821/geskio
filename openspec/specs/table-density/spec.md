# Table Density Specification

## Purpose

SnowUI table pattern (AD-3) applied to the 3 table screens: `stock`, `clientes`, `fiado` (slice c). Composed chrome — `TableToolbar` + denser `AppTable` + `TablePager` — on top of Flet `DataTable`; `app/datos.py` stays FROZEN; filter/sort/page is view-side.

## Requirements

### Requirement: Table Toolbar

The kit MUST provide `TableToolbar(on_query, chips=(), actions=())` composed of a search field, filter chips, and action buttons. All 3 table screens MUST render it above the table and MUST NOT hand-build ad-hoc toolbar equivalents.

#### Scenario: All table screens share the toolbar

- GIVEN `stock`, `clientes`, and `fiado` render their tables
- WHEN each table area is inspected
- THEN each uses the same `TableToolbar` instance pattern (search + chips + actions) with no screen-local toolbar copies

#### Scenario: Search query feeds the table

- GIVEN the toolbar search field receives text
- WHEN the query changes
- THEN the table rows re-filter view-side without any `datos.py` modification

### Requirement: Dense Table with Fixed Page Size

`AppTable` MUST apply DataTable density knobs (`heading_row_height`, `data_row_min/max_height`, `heading_row_color`, `horizontal_lines`) with a fixed default page size of 10 rows. Screens MUST NOT override the page size. The kit's empty-state row MUST be preserved.

#### Scenario: Page size fixed at 10

- GIVEN any of the 3 table screens renders data
- WHEN rows are counted per page
- THEN at most 10 rows render and no screen overrides `page_size`

#### Scenario: Density is uniform

- GIVEN the 3 table screens
- WHEN their table row/heading heights are compared
- THEN all resolve to the same `AppTable` density defaults

### Requirement: Table Pager

The kit MUST provide `TablePager(page, pages, on_page)` as a composed `ft.Row`: prev/next controls plus an "n de m" indicator. Screens MUST paginate through it and MUST NOT rely on a Flet-native pager (none exists in 0.84.0).

#### Scenario: Pager navigates pages

- GIVEN a dataset of 23 rows at 10/page
- WHEN the user clicks next twice
- THEN the indicator shows "2 de 3" then "3 de 3" and rows 21–23 render on the last page

#### Scenario: Prev is bounded

- GIVEN the pager is on page 1
- WHEN prev is invoked
- THEN the page stays at 1 with no error

### Requirement: View-Side Pagination Pipeline

Filtering, sorting, and pagination MUST be implemented as view-side helpers (filter → sort → paginate). `app/datos.py` MUST remain untouched (gate: `git diff --exit-code -- app/datos.py`).

#### Scenario: Zero datos.py diff

- GIVEN slice c is implemented
- WHEN `git diff --exit-code -- app/datos.py` runs
- THEN it exits clean with zero diff
