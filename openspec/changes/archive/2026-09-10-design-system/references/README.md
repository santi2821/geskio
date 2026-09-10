# Design-system references — index (sdd-research input, not SDD output)

> What these 5 files are: local, admissible evidence notes for a future `sdd-research` run. No `research.md`, no proposal, no design decisions are made here.

## Quick path

1. Read `01-paperpillar.md` first (base shell), then `05-order-list.md` (tables), then 02/03/04 for their slice only.
2. Open each URL logged-in in Figma before citing any hex/font/px in `design.md` — off-canvas values below are intentionally sparse.
3. Check the honesty ledger (§4) before quoting any file.

## Contribution matrix — what each file may feed (and nothing else)

| File | Role | May feed | Must NOT feed |
|------|------|----------|---------------|
| `01-paperpillar.md` — Paperpillar Property Mgmt (BASE) | Dashboard + nav + sidebar | App shell anatomy; card/chart/search/sidebar existence; font shortlist (Inter, General Sans, Plus Jakarta Sans) | Hex, spacing, radii (unobserved) |
| `02-wellnest.md` — WellNest Hospital (peterdraw) | Stats widgets + calendar | Dense-data readability intent; "blue ocean" calm direction; patients/doctors/schedules screen inventory | Any hex; calendar interaction specifics |
| `03-dashstack.md` — DashStack (Seju) | Widgets | 4px grid; Variables + auto-layout + light/dark mechanism; responsive intent | Widget pixels; hex; fonts; radii |
| `04-crm.md` — CRM Dashboard (ID …2815621) | Widgets + lists + icons + details | Research pointer only — canvas visit mandatory | Everything until canvas-verified (title-only evidence) |
| `05-order-list.md` — Order list (ByeWind/SnowUI) | Lists | Table/form/sheets existence; SnowUI foundation categories + variable-theming + free-layout mechanics | Page-level hex/fonts/px |

## Evidence status per file

| File | webfetch (markdown) | websearch | Best off-canvas substance |
|------|---------------------|-----------|---------------------------|
| 01 Paperpillar | Title only — JS/auth wall | Excerpt: contents, fonts, features, license, tags | Strong description, zero numeric tokens |
| 02 WellNest | Title only — JS/auth wall; peterdraw.studio fetch = transport error | Excerpt: 12 screens, "blue ocean", screen list, price/sales | Strong description, zero numeric tokens |
| 03 DashStack | Title only — JS/auth wall | Excerpt: 7-point feature list + popularity | Feature list incl. 4px grid + variables + themes |
| 04 CRM …2815621 | Title only — JS/auth wall | Zero hits for this ID (only unrelated CRM files) | Title only — weakest link, flagged |
| 05 Order list | Title only — JS/auth wall | Excerpt: tags + SnowUI lineage; `snowui.byewind.com` fetched OK | System-level mechanics, zero page-level tokens |

## Honesty ledger (observed vs inferred)

- OBSERVED (cite freely): titles, publishers (except 04 UNKNOWN), URLs, access date 2026-09-10, descriptions/excerpts quoted in each file, Paperpillar font names, DashStack 4px grid + variables/themes, SnowUI foundation categories + layout/theme mechanics, popularity/license/tags as index data.
- NOT OBSERVED (never cite): any hex color, any spacing px beyond "4px grid" (03), any radius px, any font for 02/03/04/05, any widget/table pixel anatomy.
- INFERRED (direction only, marked in files): "fits GesKio nav/cards/tables" mappings; calendar interaction; 04's entire slice assignment.
- RELATED ≠ SAME: Avi Yansah CRM Customers List and Medlink are context, not substitutes for 04 and 02.

## Checklist for the sdd-research runner

- [ ] Canvas pass 01+05 first (shell + tables unblock GesKio `app/` fastest)
- [ ] Sample real hex/font/px in-canvas; replace each NOT OBSERVED with a measured value + Figma node ref
- [ ] Resolve 04 (verify ID …2815621 or formally replace it — no silent substitution)
- [ ] Keep single-base discipline: 01 is structure; 02/03/04/05 are slices, not competing shells

## Next step

Run `sdd-research` with these five notes as admitted inputs; it (not this index) produces `research.md` claims.

## Canvas pass (2026-09-10, browser + JS without login)

> Evidence preparation only. No token claims changed. Screenshots + per-file notes live under `canvas/`; `research.md` untouched.

| # | Screenshot | Note | What was captured |
|---|------------|------|-------------------|
| 01 Paperpillar | `canvas/01.png` | `canvas/c1-paperpillar.md` | H1, publisher, 252 likes / 9.3k users, CC BY 4.0, full description + contents/features/fonts as text, Vista previa images. No hex/px/radius observed. |
| 02 WellNest | `canvas/02.png` | `canvas/c2-wellnest.md` | H1, Peterdraw, 63 likes / 1.4k users, USD 22 price button, 12-screens + blue-ocean description, 7-thumb carousel (9 preview imgs). Paid + login gates canvas. |
| 03 DashStack | `canvas/03.png` | `canvas/c3-dashstack.md` | H1, Seju, 4.7k likes / 206k users / 43 comments, 7-bullet Key Features quoted as text (incl. `4px Grid System` as text only), icon/responsive comment signals. No measured values. |
| 04 CRM (Maietry) | `canvas/04.png` | `canvas/c4-crm.md` | ID verified, author `Maietry` now observed, 199 likes / 13.6k users, CC BY 4.0, NO description body (confirmed absent in DOM), tags only. Weakest link now bounded. |
| 05 Order list | `canvas/05.png` | `canvas/c5-order-list.md` | H1, ByeWind, 11 likes / 1k users, CC BY 4.0, 4-line SnowUI description quoted verbatim + Preview link, #form #sheets #table tags. Table anatomy still gated. |

Method: `playwright_browser_navigate` + snapshot + viewport screenshot + DOM evaluate per URL; `webfetch markdown` returned title-only for all five (JS wall for fetch, not for browser). `Abrir en Figma` / iframe embeds require login, so no canvas node values are claimed anywhere in `canvas/`.
