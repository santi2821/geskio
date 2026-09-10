# 02 — WellNest Hospital Management Dashboard (stats + calendar slice)

> Use ONLY for: stats widgets + calendar/schedule patterns. Structure stays with `01-paperpillar.md`.

## Identity

| Field | Value |
|-------|-------|
| Title | WellNest - Hospital Management Admin Dashboard |
| Publisher | peterdraw (ThemeForest + peterdraw.studio) |
| URL (task) | https://www.figma.com/es-la/comunidad/file/1410399675335737504/wellnest-hospital-management-admin-dashboard |
| URL (canonical) | https://www.figma.com/community/file/1410399675335737504/wellnest-hospital-management-admin-dashboard |
| Accessed | 2026-09-10 |
| Screens | 12 dashboard screens (observed) |
| Price mirror | $28 on ThemeForest, 14 sales, last updated 11 Nov 24 (search index) |
| Editability | "Easy to edit and customize" (observed) |

## Extract (observed)

> Sources: websearch excerpts of canonical page + `es-es` mirror + ThemeForest listing + templatelelo mirror + Dribbble shot 25526604.
>
> "Get a better management dashboard based on its look and flow using WellNest, a simple modern hospital management dashboard Figma template."
> "The simplicity of this template is very suitable for loading a bunch of data in a way that is easy to find and understand."
> "The combination of blue ocean on every page brings a calm vibe."
> "12 screens dashboard template. Support for Figma. Easy to edit and customize."
> Dribbble (31 Jan 2025): "This powerful template includes everything you need: Dashboard, Patients & Patient Details, Doctors & Doctor Details, Department Details, Doctor Schedules, …"

## Tokens observed

| Token | Status | Value / evidence |
|-------|--------|------------------|
| Colors (hex) | NOT OBSERVED | Only the phrase "blue ocean" (calm vibe). No hex anywhere indexed |
| Fonts | NOT OBSERVED | No family named for this file |
| Spacing | NOT OBSERVED | No scale exposed |
| Radii | NOT OBSERVED | No corner values exposed |
| Density cue | OBSERVED (qualitative) | "Simplicity … loading a bunch of data … easy to find and understand" — dense-data readability intent, not a number |

## Component patterns

| Pattern | Verdict | Evidence |
|---------|---------|----------|
| Stats widgets | OBSERVED (existence) / INFERRED (pixels) | Hospital dashboard with visitors/patients/appointments monitoring is the stated purpose; exact widget anatomy not extractable |
| Calendar / schedules | OBSERVED (existence) | "Doctor Schedules" screen listed on Dribbble; appointment tracking is core purpose |
| Patients list + patient detail | OBSERVED (existence) | Listed screens |
| Doctors list + doctor detail | OBSERVED (existence) | Listed screens |
| Department detail | OBSERVED (existence) | Listed screen |

## Extraction limits (evidence, no invention)

| Attempt | Result |
|---------|--------|
| `webfetch markdown` on `es-la` URL | Title only: `WellNest - Hospital Management Admin Dashboard \| Figma` — JS/auth wall, no body |
| `webfetch markdown` on `peterdraw.studio` product page | Transport error (fetch failed, no content) |
| `websearch` file ID | Returned description + screen list + "blue ocean" phrase. No hex, fonts, spacing, radii |

## Observed vs inferred — do not conflate

| Claim | Verdict |
|-------|---------|
| 12 screens; patients/doctors/departments/schedules screens; "blue ocean" calm vibe; easy to customize | OBSERVED |
| Any blue hex (e.g. sky/teal guesses) | NOT OBSERVED — never cite a hex for WellNest |
| Calendar interaction (day/week/month) | INFERRED from "schedules" + hospital norms; verify in canvas |
| Medlink (13-page sibling by same author) details | RELATED, NOT THIS FILE — do not attribute Medlink inputs/tables/dropdowns/tags to WellNest |

## Checklist

- [ ] In canvas, sample the actual "blue ocean" primaries + stat-widget deltas (up/down) before touching GesKio `hoy/mes/ganancia/deben` cards
- [ ] Capture schedule/calendar anatomy (header, day cell, status chips) for GesKio dashboard "next/pending" slice
- [ ] Keep nav/sidebar authority in 01, not here

## Next step

Widgets generically → `03-dashstack.md`; CRM lists/icons/details → `04-crm.md`.
