# Widget Kit Specification (GesKio)

## Purpose

Shared Flet components live in `app/widgets.py`. The current API uses Spanish names: `tarjeta`, `encabezado`, `seccion`, `tabla`, `barra_busqueda`, `paginar`, `paginador`, `dialogo`, `confirmar_eliminar`, `aviso`, `burbuja_chat`, and `Calendario`. The shell is composed from `Marco`, `MenuLateral`, and `BarraSuperior`. These names replace earlier English component proposals such as `AppCard`, `PageHeader`, and `AppTable`.

## Requirements

### Requirement: Shared Theme-Aware Components

Components that draw application UI MUST source colors, spacing, typography, borders, radii, and focus styling from `app/theme.py`. Components MUST support the active light/dark palette. Screen code MAY pass content and behavior but MUST avoid duplicating shared visual primitives.

#### Scenario: Theme changes reach shared components

- GIVEN a light or dark palette is active
- WHEN a shared widget is built
- THEN its surface, text, border, and semantic roles come from that palette

### Requirement: Form Controls and Focus

Screens MUST use `campo_texto()` and `selector()` for text fields and dropdowns. Both MUST use the shared field radius, neutral outline, and visible 2px primary focus border unless a documented exception is needed.

#### Scenario: Form styling is consistent

- GIVEN fields across Stock, Caja, Clientes, Chat, Fiado, and Ajustes
- WHEN they are built through the shared constructors
- THEN they use the same outline, radius, and focus treatment

### Requirement: Shared Screen Structure

`encabezado()` MUST provide the task title, optional description/actions, and refresh action. `seccion()` MUST provide a themed section container. `tarjeta()`, `tarjeta_stat()`, `tarjeta_focal()`, and `grilla_stats()` MUST provide the shared card and dashboard-stat hierarchy.

#### Scenario: Dashboard stat hierarchy

- GIVEN the dashboard renders its focal and secondary metrics
- WHEN `grilla_stats()` is built
- THEN only the focal stat uses the focal treatment and secondary stats use the shared responsive grid

### Requirement: Shared Table Structure

Table screens MUST use `barra_busqueda()` for search/filter chrome, `tabla()` for density and empty-state presentation, and `paginar()` plus `paginador()` for page slicing and controls. Shared page-header actions MAY remain outside the toolbar.

#### Scenario: Empty table is actionable

- GIVEN a table has no rows
- WHEN `tabla()` builds
- THEN it shows an explicit empty-state icon and message

### Requirement: Dialogs and Feedback

Dialogs MUST use `dialogo()`; destructive confirmations MUST use `confirmar_eliminar()`; transient success/error feedback MUST use `aviso()`. These helpers MUST use shared theme roles and duration defaults.

#### Scenario: Destructive action can be cancelled

- GIVEN a destructive action is requested
- WHEN the confirmation dialog opens
- THEN the user can cancel without changing data or confirm the named action

### Requirement: Shell Composition

`Marco` MUST compose the sidebar, topbar, and active `Pantalla`. Geometry MUST resolve to shared theme constants. Screens MUST keep the `Pantalla`/`invalidate()` contract and MUST NOT hand-build a second shell.

#### Scenario: Navigation updates the shell

- GIVEN the application is open
- WHEN `Marco.navegar(key)` is called
- THEN the active navigation item, topbar title, and content slot update together

### Requirement: Chat Bubble Contract

`burbuja_chat(texto, es_usuario)` MUST align user messages to the end with the user role and assistant messages to the start with a neutral surface; the Chat screen MUST apply the active palette.
