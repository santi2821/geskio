# C1 — Paperpillar Property Management (canvas pass 2026-09-10)

Canvas evidence for `01-paperpillar.md`. Page rendered without login; Figma canvas values remain gated.

## Quick path

1. Open `01.png` — community page header + preview render.
2. Trust the Details table below; everything else stays NOT OBSERVED.
3. Open in Figma logged-in before citing any hex/spacing/radius.

## Details

| Topic | Observed (verbatim or literal) |
|-------|-------------------------------|
| Title / H1 | `Property Management Dashboard UI Kit - Paperpillar` |
| Publisher | `Paperpillar` (`/@paperpillar`), support `hello@paperpillar.com` |
| Counters | `252` likes · `9.3k usuarios` · `0 comentarios` (page text, may drift) |
| License / updated | `CC BY 4.0` · `Última actualización hace 2 años` |
| Description | `Want to create and easily manage properties in a dashboard? ... Use this for free for your personal or commercial projects.` |
| Contents | `1 Dashboard Screen`; `Components (Cards, Charts, Search Bar, Sidebar Menu)`; `Design style guide (Typography and Color)` |
| Features | `Auto layout components`; `Fully customizable components`; `3 free fonts (Inter, General Sans, and Plus Jakarta Sans)` |
| Tags | `Paneles`, `Inmobiliaria`, `CRM` + `#dashboard #property #saas #statistics` (among others) |
| Preview | `Vista previa` section: cover image + carousel image + embedded iframe; 2 `<img>` with preview alt observed |

## Behind auth / JS wall

| Attempt | Result |
|---------|--------|
| `webfetch markdown` (this pass) | Title only: `Property Management Dashboard UI Kit - Paperpillar \| Figma`. No body. |
| Browser + JS, no login (this pass) | Full page above rendered. No login prompt blocked reading. |
| `Abrir en Figma` button / iframe embed | Requires login; actual canvas nodes, style-guide frame values, and any hex/spacing/radius NOT observable. |
| Numeric design tokens | Zero observed. No hex, no px, no radius appears as page text. Nothing invented here. |

## Checklist

- [ ] `01.png` shows the community header + preview for audit
- [ ] No hex/radius/px cited above (only quoted feature text)
- [ ] Style-guide frame still needs logged-in canvas read before `design.md`

## Next step

Feed this + `01-paperpillar.md` to `sdd-research`; sample the Typography + Color frame in-canvas.
