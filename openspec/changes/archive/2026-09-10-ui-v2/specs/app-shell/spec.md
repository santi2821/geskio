# App Shell Specification

## Purpose

Paperpillar-anchored shell (`app/main.py`): sidebar + topbar + content slot with an adapter that renders any existing `Screen` control unchanged. Closes V2-D6 (collapse rule) and V2-D1 (shell-first migration). Zero logic change; `app/datos.py` FROZEN.

## Requirements

### Requirement: Shell Geometry

The system MUST render a `Shell` as an `ft.Row`: sidebar + content column. The sidebar MUST be 240px expanded and 64px as an icon rail when collapsed; the topbar MUST be 56px high. Dimensions MUST resolve to `theme.py` shell constants (`SHELL_SIDEBAR_W`, `SHELL_RAIL_W`, `SHELL_TOPBAR_H`) — no literals in `main.py`.

#### Scenario: Default boot at 1100x700

- GIVEN the app boots at the 1100x700 default window size
- WHEN the Shell renders
- THEN the sidebar is the 64px icon rail (labels hidden, icons kept) and content width is ~990px

#### Scenario: Expanded shell above breakpoint

- GIVEN the window is 1400x900
- WHEN the Shell renders
- THEN the sidebar is 240px wide with nav labels visible and the topbar is 56px

### Requirement: Responsive Collapse Rule

The Shell MUST collapse to the rail when `page.window.width <= SHELL_BREAKPOINT_W (1280)` OR `page.window.height <= SHELL_BREAKPOINT_H (760)`, and MUST expand when both thresholds are exceeded. The resize driver MUST be `page.window.on_event` (`WindowEventType.RESIZED`) reading `page.window.width/height`.

#### Scenario: Shrink below breakpoint collapses

- GIVEN the shell is expanded at 1400x900
- WHEN the window resizes to 1200x800
- THEN the sidebar collapses to the 64px rail

#### Scenario: Grow past both thresholds expands

- GIVEN the shell is collapsed at 1100x700
- WHEN the window resizes to 1300x800
- THEN the sidebar expands to 240px

### Requirement: Manual Collapse Fallback

The topbar MUST provide a manual toggle that switches the sidebar between rail and expanded states. It SHALL work regardless of whether OS resize events fire; the code MUST document that resize-event availability is OS-dependent.

#### Scenario: Toggle works without resize events

- GIVEN the OS never delivers RESIZED events
- WHEN the user clicks the manual topbar toggle
- THEN the sidebar switches between rail and expanded without relying on resize handling

### Requirement: Adapter Renders Screens Unchanged

The Shell MUST provide a thin adapter that renders any `Screen` control unchanged in the content slot. Unmigrated v1 screens MUST remain renderable inside the new shell so per-slice revert restores the prior state.

#### Scenario: Unmigrated screen loads in shell

- GIVEN a slice has migrated only some screens to shell-native composition
- WHEN a still-unmigrated screen is opened
- THEN it renders unchanged inside the shell content slot

### Requirement: Navigation Contract

`mostrar(key)` MUST be replaced by `shell.navigate(key)`. The topbar MUST show the active screen title, the mode (theme) toggle, and the brand `Dropdown` moved from the v1 toolbar. Navigation MUST NOT add search or user-menu features. Screens MUST keep the `Screen`/`invalidate()` contract.

#### Scenario: Navigate updates rail and content

- GIVEN the shell is booted with nav items
- WHEN `shell.navigate('stock')` is invoked
- THEN the rail highlights `stock` and the content slot renders the stock screen

#### Scenario: No new topbar features

- GIVEN the topbar implementation
- WHEN reviewed
- THEN it contains only title, mode toggle, brand Dropdown, and manual collapse toggle (no search box, no user menu)
