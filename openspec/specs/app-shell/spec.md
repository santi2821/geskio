# App Shell Specification

## Purpose

Desktop shell (`app/main.py`): branded sidebar + contextual topbar + content slot. The sidebar groups work areas and keeps Ajustes at the bottom. Appearance controls stay in Ajustes so theme configuration remains together. The shell adapts to the available window size. Its visual identity is formal and task-oriented: compact GesKio wordmark, neutral work surfaces, no marketing claim or decorative logo tile.

## Requirements

### Requirement: Shell Geometry

The system MUST render a `Marco` as an `ft.Row`: sidebar + content column. The sidebar MUST be 240px expanded and 64px as an icon rail when collapsed; the topbar MUST be 56px high. Dimensions MUST resolve to shell constants in `theme.py`.

#### Scenario: Default boot at 1100x700

- GIVEN the app boots at the 1100x700 default window size
- WHEN the Shell renders
- THEN the sidebar is expanded with labels and the content adapts to the remaining width

#### Scenario: Expanded shell above breakpoint

- GIVEN the window is 1400x900
- WHEN the Shell renders
- THEN the sidebar is 240px wide with nav labels visible and the topbar is 56px

### Requirement: Responsive Collapse Rule

The shell MUST collapse to the rail when the live page width is `<= RUPTURA_ANCHO (1024)` OR the page height is `<= RUPTURA_ALTO (600)`, and MUST expand when both thresholds are exceeded. Web and native page resizing MUST use `page.on_resize` event dimensions; `page.window.on_event` remains the native-window fallback. Initial sizing MUST prefer `page.width/page.height` and fall back to window dimensions when page dimensions are unavailable. The compact topbar MUST hide the long date at widths `<=600`.

#### Scenario: Shrink below breakpoint collapses

- GIVEN the shell is expanded at 1400x900
- WHEN the window resizes to 1000x800
- THEN the sidebar collapses to the 64px rail

#### Scenario: Grow past both thresholds expands

- GIVEN the shell is collapsed at 1000x800
- WHEN the window resizes to 1100x700
- THEN the sidebar expands to 240px

#### Scenario: Browser width is read at startup and resize

- GIVEN a web page starts narrow or receives a resize event
- WHEN its current width crosses 1024 logical pixels and its height exceeds 600
- THEN the sidebar changes between rail and expanded states, and the date returns above 600px

### Requirement: Manual Collapse Fallback

The topbar MUST provide a manual toggle that switches the sidebar between rail and expanded states. It SHALL work regardless of whether OS resize events fire; the code MUST document that resize-event availability is OS-dependent.

#### Scenario: Toggle works without resize events

- GIVEN the OS never delivers RESIZED events
- WHEN the user clicks the manual topbar toggle
- THEN the sidebar switches between rail and expanded without relying on resize handling

### Requirement: Adapter Renders Screens Unchanged

The shell MUST render every existing `Pantalla` in its content slot and preserve screen state where the screen owns it (for example, Chat messages and Dashboard's selected period).

#### Scenario: Unmigrated screen loads in shell

- GIVEN a slice has migrated only some screens to shell-native composition
- WHEN a still-unmigrated screen is opened
- THEN it renders unchanged inside the shell content slot

### Requirement: Navigation Contract

`Marco.navegar(key)` MUST update the active sidebar item, the topbar's current section, and the screen content together. The sidebar MUST show the GesKio brand in expanded and compact states; Ajustes stays visually separated at the bottom. Appearance controls remain in Ajustes. Screens MUST keep the `Pantalla`/`invalidate()` contract.

#### Scenario: Navigate updates rail and content

- GIVEN the shell is booted with nav items
- WHEN `Marco.navegar('stock')` is invoked
- THEN the rail highlights `stock` and the content slot renders the stock screen

#### Scenario: Topbar stays focused

- GIVEN the topbar implementation
- WHEN reviewed
- THEN it shows the current section and manual collapse toggle; the date appears when space allows and is hidden at compact widths

### Requirement: Formal Product Hierarchy

The shell MUST use a compact typographic wordmark without a colored monogram tile or marketing subtitle. The topbar identifies the current navigation section; each screen content header MAY show a distinct task title and descriptor, but MUST NOT repeat the same screen label as its prominent title. Selection and primary action use the brand role sparingly; neutral surfaces MUST be used for workspace structure.

#### Scenario: Screen context is not duplicated

- GIVEN a screen is active
- WHEN its shell and content header are reviewed together
- THEN the topbar names the section and the content header names the task without repeating the same prominent label
