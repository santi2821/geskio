# 05 — Order List Page by ByeWind / SnowUI (lists slice)

> Use ONLY for: lists/tables (order-list). Tokens come from the SnowUI system description, not from page pixels.

## Identity

| Field | Value |
|-------|-------|
| Title | Order list page |
| Publisher | ByeWind — `byewind@live.com` |
| URL (task) | https://www.figma.com/es-la/comunidad/file/1486633496506469857/order-list-page |
| URL (canonical) | https://www.figma.com/community/file/1486633496506469857/order-list-page |
| Accessed | 2026-09-10 |
| License | CC BY 4.0 (canonical page, search index) |
| Popularity | ~11 likes · ~975 users (search index, may drift) |
| Tags | Dashboards, SaaS, CRM · #form #sheets #table |
| System | "This page from SnowUI. SnowUI is a design system and UI Kit." (observed) |

## Extract (observed)

> Sources: websearch excerpts of canonical page + `webfetch markdown` of `snowui.byewind.com` (succeeded) + canonical SnowUI system listings.
>
> File: "Hello. This page from SnowUI. SnowUI is a design system and UI Kit. Preview in Figma."
> System (`1388431032861751537 SnowUI Design System`, 406 likes · 13.3k users): "SnowUI design system is used to define design foundations such as variables, spacing, icon size, corner size, color, font style, effect style, etc. And it provides commonly used design components based on these design foundations. SnowUI and 260+ pages use this design system. This design system has been optimized for 3 years."
> Site (`snowui.byewind.com`, fetched 2026-09-10): Free Layout (1/2/3-column + free block arrangement); Free Operation (sortable sidebar, freely-defined block sizes); Free Style (light/dark via variables + definable brand colors); Auto Layout 4.0 + component properties + individual strokes; core vs business components split; 60+ pages (project dev, e-commerce, ops); guidance "copy the page case, delete unneeded functions, add required ones — like Lego blocks."
> Paid kit listing (`1301134685302006646`, $99): Desktop + Mobile separately (not mere breakpoints); Light & Dark via variables; "Dashboard Data Tables, Table Design, Responsive Tables, Filters, Search Bar" among named areas.

## Tokens observed

| Token | Status | Value / evidence |
|-------|--------|------------------|
| Foundation categories | OBSERVED | variables, spacing, icon size, corner size, color, font style, effect style (named as what SnowUI defines) |
| Theme mechanism | OBSERVED | Light & Dark toggled via Figma Variables; definable brand colors |
| Layout mechanism | OBSERVED | 1/2/3-column free layout; resizable blocks; sortable sidebar |
| Build primitives | OBSERVED | Auto Layout 4.0, component properties, individual strokes |
| Colors (hex) | NOT OBSERVED | No hex for this page or system off-canvas |
| Fonts (families) | NOT OBSERVED | "Font style" named as category only; no family indexed |
| Spacing / radii (numbers) | NOT OBSERVED | "Spacing / corner size" named as categories only; no px values |

## Component patterns

| Pattern | Verdict | Evidence |
|---------|---------|----------|
| Order-list table + form + sheets | OBSERVED (existence) | Tags #form #sheets #table + "order list page" title + SnowUI data-table areas |
| Filters + search bar over tables | OBSERVED at system level | Named in SnowUI kit areas; confirm on THIS page in canvas |
| Responsive tables | OBSERVED at system level | "Responsive Tables" named; confirm on THIS page in canvas |
| Row actions / pagination / statuses | NOT OBSERVED | Not exposed off-canvas; record in-canvas before use |

## Extraction limits (evidence, no invention)

| Attempt | Result |
|---------|--------|
| `webfetch markdown` on `es-la` URL | Title only: `Order list page \| Figma` — JS/auth wall |
| `websearch` file ID | Returned description + tags + SnowUI lineage (used above). No page-level hex/fonts/px |
| `webfetch markdown` on `snowui.byewind.com` | SUCCEEDED — system-level features/pricing/FAQ retrieved (only system-level source that rendered) |

## Observed vs inferred

| Claim | Verdict |
|-------|---------|
| Publisher, tags, SnowUI lineage, foundation categories, variable-theming, free-layout mechanics, table/form/sheets existence | OBSERVED |
| Any hex, font family, spacing px, radius px for the order-list page | NOT OBSERVED |
| "GesKio stock/clientes/fiado tables map to this pattern" | INFERRED direction (tags + system fit), pending canvas check of row anatomy vs `DataTable(column_spacing=12/16)` inconsistency in GesKio |

## Checklist

- [ ] In canvas, record THIS page's table anatomy: header style, row height, cell padding, status chips, pagination, filters/search placement
- [ ] Map to GesKio `stock.py / clientes.py / fiado.py` tables + `caja.py` cart rows; note where SnowUI row-detail covers the "debt warning / low-stock" cases
- [ ] Adopt variable-naming + light/dark mechanism, not guessed hex

## Next step

Set status in `README.md`; canvas pass over 01+05 first (shell + tables unblock GesKio fastest).
