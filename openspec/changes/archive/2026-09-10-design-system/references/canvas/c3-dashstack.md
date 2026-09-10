# C3 — DashStack Admin UI Kit (canvas pass 2026-09-10)

Canvas evidence for `03-dashstack.md`. Richest text of the five; still zero canvas-measured values.

## Quick path

1. Open `03.png` — header + preview render.
2. Trust the Details table below; quote `4px Grid System` only as feature text, never as measured scale.
3. Open in Figma logged-in before citing any hex/font/radius.

## Details

| Topic | Observed (verbatim or literal) |
|-------|-------------------------------|
| Title / H1 | `DashStack - Free Admin Dashboard UI Kit - Admin & Dashboard Ui Kit - Admin Dashboard` |
| Publisher | `Seju` (`/@sejal_ui_ux`) |
| Counters | `4.7k` likes · `206k usuarios` · `43 comentarios` (page text, may drift) |
| Description | `Explore DashStack, a cutting-edge and free Admin Dashboard UI Kit ... responsive design, rich set of features, and user-friendly components.` |
| Key features (quoted text) | `Figma Config Compatible (Variables, Updated Auto layout, more!)`; `Editable Components`; `Auto Layout`; `4px Grid System`; `Light & Dark Themes`; `Fully Responsive (Mobile & Tablet)`; `Regular Update` |
| Comments (sample) | Users ask about LineAwesome icons font, mobile version, typographies; creator replies `Thanks` / contact email. Confirms icons + responsive intent, no values. |
| Tags | Long SEO tag list on page (dashboard/admin/widgets/charts/tables/sidebar/header); category `Paneles`-family, exact taxonomy not copied here to avoid noise |
| Preview | Main preview + `Vista previa` section; 2 `<img>` with preview alt observed |

## Behind auth / JS wall

| Attempt | Result |
|---------|--------|
| `webfetch markdown` (this pass) | Title only. No body. |
| Browser + JS, no login (this pass) | Full page above rendered. No login wall for reading. |
| `Abrir en Figma` button / iframe embed | Requires login; Variables, auto-layout, theme mechanics, widget pixels NOT observable. |
| Numeric design tokens | Zero measured. `4px` appears only inside the quoted feature string `4px Grid System` — cited as text, not as verified spacing scale. No hex, no radius, no font names on page. Nothing invented here. |

## Checklist

- [ ] `03.png` shows header + preview for audit
- [ ] `4px` quoted only as feature text, not as token claim
- [ ] Variables + light/dark + responsive still need in-canvas sampling

## Next step

Feed this + `03-dashstack.md` to `sdd-research` for the widgets/theming-mechanism slice only.
