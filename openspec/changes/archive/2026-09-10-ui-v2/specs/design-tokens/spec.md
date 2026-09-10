# Delta for design-tokens

## ADDED Requirements

### Requirement: Additive Shell/Layout Token Extension (AD-5)

`PaletteTheme` dataclass fields MUST remain frozen. Shell and layout dimensions MUST be added as non-color module constants in `theme.py`: `SHELL_SIDEBAR_W=240`, `SHELL_RAIL_W=64`, `SHELL_TOPBAR_H=56`, `SHELL_BREAKPOINT_W=1280`, `SHELL_BREAKPOINT_H=760`, plus focal/calendar layout steps. NO new hex color MAY be introduced anywhere in `theme.py`.

#### Scenario: Zero new hex constants

- GIVEN slice a extends `theme.py`
- WHEN the file is diffed
- THEN no new color hex literals appear and the `PaletteTheme` dataclass fields are unchanged

#### Scenario: Shell constants are named tokens

- GIVEN `main.py` renders sidebar, rail, and topbar
- WHEN dimensions are resolved
- THEN they come from the named shell constants (no raw 240/64/56 literals)

### Requirement: New Usage Pairs Reuse Verified AA Roles (AD-6)

The 19/19 proven AA pairs MUST be reused unchanged: `danger`/`danger_text`, `accent`/`accent_text`, `footer_hover` (landing parity), and `_ROLE_ALIASES`. New usage mapping MUST be: sidebar idle = `text_muted` on `bg_soft`; sidebar active = `accent_soft`/`on_accent_soft`; chips = surface+border or `accent_soft` pair; calendar today = `accent_soft` pair; calendar totals = `text` on `surface`. Every NEW usage pair MUST be re-proved in a contrast table (≥4.5:1 normal text, ≥3:1 large text + UI components).

#### Scenario: Contrast re-proof table complete

- GIVEN the set of NEW usage pairs introduced by ui-v2
- WHEN the contrast table is checked against `theme.py` docstring values
- THEN every pair meets ≥4.5:1 (normal) or ≥3:1 (large/UI) and none introduces an unverified pair
