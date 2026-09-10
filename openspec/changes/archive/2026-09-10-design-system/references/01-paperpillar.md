# 01 — Paperpillar Property Management Dashboard (BASE)

> BASE MAYORITARIA for `design-system`: dashboard + nav + sidebar. Start here; use the other four only for their listed slice.

## Identity

| Field | Value |
|-------|-------|
| Title | Property Management Dashboard UI Kit - Paperpillar |
| Publisher | Paperpillar — support `hello@paperpillar.com` |
| URL (task) | https://www.figma.com/es-la/comunidad/file/1423862565654844475/property-management-dashboard-ui-kit-paperpillar |
| URL (canonical) | https://www.figma.com/community/file/1423862565654844475/property-management-dashboard-ui-kit-paperpillar |
| Accessed | 2026-09-10 |
| License | CC BY 4.0 |
| Popularity | ~247 likes · ~9.2k users (search index, may drift) |
| Last updated | ~2 years ago (search index) |
| Tags | Dashboards, Real estate, CRM |

## Extract (observed)

> Source: websearch excerpts of thecanonical Community page + mirrors (Freebie Supply, Sketchfav, Dribbble). Verbatim substance, not paraphrase-invention:
>
> "Want to create and easily manage properties in a dashboard? Then our Property Management Dashboard UI Kit is for you! Use this for free for your personal or commercial projects."
> "Here's what you get inside the UI Kit: 1 Dashboard Screen; Components (Cards, Charts, Search Bar, Sidebar Menu); Design style guide (Typography and Color)."
> "Features: Auto layout components; Fully customizable components; The UI Kit is using 3 free fonts (Inter, General Sans, and Plus Jakarta Sans)."

## Tokens observed

| Token | Status | Value / evidence |
|-------|--------|------------------|
| Fonts | OBSERVED | Inter, General Sans, Plus Jakarta Sans (named in description; download links for General Sans / Plus Jakarta Sans mentioned) |
| Colors (hex) | NOT OBSERVED | Description promises a color style guide, but no hex values are exposed outside Figma canvas |
| Spacing | NOT OBSERVED | "Auto layout" mentioned, no scale values (no 4/8px statement for this file) |
| Radii | NOT OBSERVED | No corner values exposed |
| Shadows / effects | NOT OBSERVED | None exposed |

## Component patterns (observed)

| Pattern | Evidence |
|---------|----------|
| Dashboard screen (1) | Listed in contents; customizable widgets + interactive charts per mirrors |
| Sidebar menu | Listed component; role = app nav shell |
| Search bar | Listed component; top-bar search pattern |
| Cards | Listed component; KPI/property summary cards (mirrors: "customizable widgets", "visualizing KPIs and trends") |
| Charts | Listed component; trend/KPI visualization (mirrors) |
| Style guide frame | Typography + Color guide exists inside file (not extractable as values) |

## Extraction limits (evidence, no invention)

| Attempt | Result |
|---------|--------|
| `webfetch markdown` on `es-la` URL | Title only: `Property Management Dashboard UI Kit - Paperpillar \| Figma`. No body, no palette, no previews — Figma canvas requires JS/auth |
| `webfetch markdown` on canonical URL | Same title-only result |
| `websearch` file ID | Returned canonical page excerpt (used above) + Dribbble shot 24985609 + Freebie Supply / Sketchfav mirrors. No hex, no spacing, no radii found anywhere indexed |

## Observed vs inferred

| Claim | Verdict |
|-------|---------|
| Title, publisher, license, tags, font names, component list, auto-layout/customizable | OBSERVED (description text) |
| Any hex, spacing scale, radius, shadow, exact sidebar width/topbar height | NOT OBSERVED — do not cite; resolve inside Figma before `design.md` |
| "Fits GesKio nav-shell + dashboard cards" | INFERRED from role + component list, not from pixels. Usable as research direction, not as token claim |

## Checklist

- [ ] Open in Figma (logged in) and read the Typography + Color style-guide frame before freezing tokens
- [ ] Confirm sidebar anatomy (width, item height, active state) against `app/main.py` nav-shell
- [ ] Confirm card anatomy (padding, radius, label/value scale) against `app/screens/dashboard.py`

## Next step

Use `02-wellnest.md` only for stats-widget + calendar slice; keep this file as the structural base.
