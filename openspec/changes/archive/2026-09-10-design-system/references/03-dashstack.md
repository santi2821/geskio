# 03 — DashStack Free Admin Dashboard UI Kit (widgets slice)

> Use ONLY for: generic admin widgets. Structure stays with `01-paperpillar.md`.

## Identity

| Field | Value |
|-------|-------|
| Title | DashStack - Free Admin Dashboard UI Kit - Admin & Dashboard Ui Kit - Admin Dashboard |
| Publisher | Creator handle `Seju (@sejal_ui_ux)` per comment thread on canonical page |
| URL (task) | https://www.figma.com/es-la/comunidad/file/1324762163080748317/dashstack-free-admin-dashboard-ui-kit-admin-dashboard-ui-kit-admin-dashboard |
| URL (canonical) | https://www.figma.com/community/file/1324762163080748317/dashstack-free-admin-dashboard-ui-kit-admin-dashboard-ui-kit-admin-dashboard |
| Accessed | 2026-09-10 |
| Popularity | ~4.7k likes · ~206k users · 42 comments (search index, may drift) |
| License | Free UI kit (see canonical page for current terms before reuse) |

## Extract (observed)

> Source: websearch excerpts of canonical page.
>
> "Explore DashStack, a cutting-edge and free Admin Dashboard UI Kit designed to elevate your web administration and dashboard experience."
> "This meticulously crafted UI kit offers a seamless blend of functionality and aesthetics … responsive design, rich set of features, and user-friendly components."
> "Key Features: 1. Figma Config Compatible (Variables, Updated Auto layout, more!) 2. Editable Components 3. Auto Layout 4. 4px Grid System 5. Light & Dark Themes 6. Fully Responsive (Mobile & Tablet) 7. Regular Update."
> Community signal (3-mo-old comment): "This is one of the best dashboard templates in the Figma Community."

## Tokens observed

| Token | Status | Value / evidence |
|-------|--------|------------------|
| Spacing grid | OBSERVED | 4px Grid System (named in features) |
| Themes | OBSERVED | Light & Dark Themes; Figma Variables + Updated Auto Layout |
| Breakpoints | OBSERVED (qualitative) | Fully Responsive (Mobile & Tablet); no px values exposed |
| Colors (hex) | NOT OBSERVED | No hex indexed |
| Fonts | NOT OBSERVED | No family named for this file |
| Radii | NOT OBSERVED | No corner values exposed |

## Component patterns

| Pattern | Verdict | Evidence |
|---------|---------|----------|
| Admin widgets (generic) | OBSERVED (existence) / INFERRED (pixels) | "Rich set of features / user-friendly components" + dashboards category; exact widget set lives in canvas only |
| Responsive admin shell | OBSERVED (intent) | Mobile & tablet responsiveness claimed |
| Themable components | OBSERVED (mechanism) | Variables + editable components + auto layout |

## Extraction limits (evidence, no invention)

| Attempt | Result |
|---------|--------|
| `webfetch markdown` on `es-la` URL | Title only: `DashStack - Free Admin Dashboard UI Kit … \| Figma` — JS/auth wall |
| `websearch` file ID | Returned description + 7-point feature list + popularity. No hex, fonts, radii, widget inventory |

## Observed vs inferred

| Claim | Verdict |
|-------|---------|
| Variables, auto layout, editable components, 4px grid, light & dark, responsive, regular updates | OBSERVED (feature list) |
| Any specific widget anatomy, hex, font, radius | NOT OBSERVED — resolve in canvas |
| "Best template" praise | OBSERVED as community opinion, not a spec claim |

## Checklist

- [ ] In canvas, inventory 3–5 reusable widgets that map to GesKio stats/alerts without duplicating 01/02
- [ ] Record grid adherence (4px) + theme-variable naming before proposing GesKio tokens
- [ ] Discard anything that conflicts with the 01 base shell — widgets only

## Next step

CRM lists/icons/details → `04-crm.md`; order-list tables → `05-order-list.md`.
