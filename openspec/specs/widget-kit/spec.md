# Widget Kit Specification (geskio)

## Purpose

Shared Flet component kit (`app/widgets.py`) built exclusively on `design-tokens`, replacing the dialog/SnackBar/table/card code duplicated across the 6 screens. Fixed defaults (per proposal) so the kit enforces consistency by construction.

## Requirements

### Requirement: Shared Components with Fixed Defaults

The kit MUST provide: `AppCard`, `PageHeader(title, actions=(), on_refresh=None)` (replaces `AppHeader`), `AppTable` (fixed `column_spacing=12`, `page_size=10`, empty-state row), `AppDialog` incl. `confirm_delete` (destructive = error/red role), `feedback(text)` (SnackBar with fixed duration), status badges/chips, and chat bubbles (user vs bot, no tail). All defaults MUST be fixed in the kit, not passed per screen.
(Previously: header was `AppHeader(title, on_refresh)` and `AppTable` had no page-size default.)

### Requirement: Rounded Form Controls and Visible Focus

The widget kit MUST expose shared GesKio text-field and dropdown constructors. They MUST use the 10px field radius, neutral outline, and a 2px primary focus border. Screens MUST use these constructors so form styling stays consistent. Primary, outlined, and text buttons MUST use the shared 8px control radius unless a control has a named, documented exception.

#### Scenario: Form control consistency

- GIVEN text fields and dropdowns across Caja, Stock, Clientes, Fiado, Chat and Ajustes
- WHEN their shared constructors are inspected
- THEN all use the same field radius, neutral outline and visible primary focus border

#### Scenario: Table normalization via kit

- GIVEN `stock` uses `column_spacing=12` and `clientes` uses `16` (exploration drift)
- WHEN both migrate to `AppTable`
- THEN both render with the kit's fixed `column_spacing=12` and no screen overrides it

#### Scenario: Delete dialog reuse

- GIVEN `stock` and `clientes` both implement delete confirmation with red/white button (exploration)
- WHEN either screen needs a delete dialog
- THEN it calls `confirm_delete` and gets identical destructive styling and behavior

#### Scenario: Feedback consistency

- GIVEN any success/error action in any screen
- WHEN user feedback is needed
- THEN the screen calls `feedback(text)` and receives a SnackBar with the kit's fixed duration and token styling (no per-screen `page.overlay` setups)

### Requirement: Kit Depends Only on Tokens

Kit widgets MUST use `theme.py` tokens exclusively. The kit MUST NOT contain color/padding/radius literals.

#### Scenario: Kit grep stays clean

- GIVEN a grep for style literals in `app/widgets.py`
- WHEN run
- THEN zero literals are found; every value resolves to a token import

### Requirement: Screen Adoption

The 6 screens MUST consume the kit for card, header, table, dialog, feedback, and bubble patterns. Screens MUST NOT build ad-hoc equivalents of kit components.

#### Scenario: Migration replaces duplication

- GIVEN a screen that previously hand-built its card/dialog/SnackBar
- WHEN the migration slice lands
- THEN the ad-hoc code is deleted and the kit call is the only usage path (no dead copies kept)

### Requirement: Table Empty State

`AppTable` MUST render an empty-state row (message + icon) when the data source is empty.

#### Scenario: Empty table renders message

- GIVEN a screen whose dataset is empty (e.g. fiado with `Solo pendientes` and no pending rows)
- WHEN `AppTable` builds
- THEN it shows the empty-state row instead of a bare header table

### Requirement: Chat Bubble Contract

The kit MUST provide two bubble variants: user (accent/soft role, `Row` aligned END) and bot (neutral surface role, aligned START), with fixed padding and radius from tokens.

#### Scenario: Bubble sides and roles

- GIVEN a message list in `chat`
- WHEN user and bot messages render
- THEN user bubbles align END with the user role and bot bubbles align START with the bot role, both with identical token-driven padding/radius

### Requirement: Shell Kit Components

The kit MUST provide `Shell(page, nav_items, active_key, on_navigate) -> ft.Row` and `PageHeader`. All shell geometry MUST resolve to `theme.py` shell constants. Screens MUST NOT hand-build sidebar/topbar equivalents. `PageHeader` MUST be the only header entry point (no dead `AppHeader` copies kept).

#### Scenario: Shell is the single nav builder

- GIVEN the app boots
- WHEN the shell renders
- THEN sidebar, rail, and topbar come from kit `Shell`/`Topbar`/`Sidebar` components with zero literals in `main.py`

### Requirement: Dashboard Kit Components

The kit MUST provide `Section(title, content) -> ft.Container` (card with heading), `StatGrid(focal: AppStatCard, stats: list[AppStatCard]) -> ft.ResponsiveRow`, and `Calendar(get_series, today, view) -> ft.Control` (view-only). The focal treatment (2px primary border, FS_36) MUST be fixed inside the kit.

#### Scenario: StatGrid owns the hierarchy

- GIVEN the dashboard composes its stats
- WHEN `StatGrid` renders
- THEN only the focal card carries the 2px primary border and secondary cards are FS_28 role-colored, with no screen-level styling overrides

### Requirement: Table Chrome Kit Components

The kit MUST provide `TableToolbar(on_query, chips=(), actions=()) -> ft.Row` and `TablePager(page, pages, on_page) -> ft.Row` (composed prev/next + "n de m"). `AppTable` MUST default `page_size=10` and keep its empty-state row. There is no Flet-native pager in 0.84.0, so paging MUST go through the composed `TablePager`.

#### Scenario: Pager is composed, not native

- GIVEN a table screen paginates
- WHEN the pager renders
- THEN it is the kit's composed `TablePager` row and all 3 table screens reuse it identically
