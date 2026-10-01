# Table Density Specification

## Purpose

Shared table behavior for Stock, Clientes, and Fiado on top of Flet `DataTable`. The current helpers in `app/widgets.py` are `barra_busqueda`, `tabla`, `paginar`, and `paginador`. Filtering, sorting, and page selection stay in the screens; domain data may change when a separately scoped integrity or persistence feature requires it.

## Requirements

### Requirement: Shared Search and Filter Toolbar

All three table screens MUST use `barra_busqueda(al_buscar, chips=(), acciones=(), pista=...)` for search and optional filters. Primary actions MAY live in the shared page header.

#### Scenario: Search query feeds the table

- GIVEN the search field receives text
- WHEN the query changes
- THEN the visible rows are filtered in the screen without changing the domain data

### Requirement: Dense Table and Empty State

`tabla()` MUST apply shared DataTable density values (`heading_row_height`, `data_row_min/max_height`, `heading_row_color`, `horizontal_lines`) and MUST render an explicit empty state when there are no rows. `FILAS_POR_PAGINA` MUST remain 10 unless a later product change updates the shared default.

#### Scenario: Page size stays shared

- GIVEN any of the three table screens renders data
- WHEN rows are counted per page
- THEN at most 10 rows render by default and screens do not override the page size

#### Scenario: Empty data is clear

- GIVEN a search/filter leaves no rows
- WHEN the table renders
- THEN it shows a screen-appropriate empty message and icon instead of a blank table

### Requirement: Shared Pager

Screens MUST use `paginar(filas, pagina, por_pagina=...)` for bounded page slicing and `paginador(pagina, paginas, al_paginar)` for previous/next controls and the "n de m" indicator.

#### Scenario: Pager navigates pages

- GIVEN 23 rows and the shared 10-row page size
- WHEN the user advances twice
- THEN the indicator reaches "3 de 3" and the last page contains rows 21–23

#### Scenario: Previous is bounded

- GIVEN the pager is on page 1
- WHEN previous is invoked
- THEN it stays on page 1 without error
