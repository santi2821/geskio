# C5 — Order List Page by ByeWind / SnowUI (canvas pass 2026-09-10)

Canvas evidence for `05-order-list.md`. Minimal description; system-level pointer only.

## Quick path

1. Open `05.png` — header + preview render.
2. Trust the Details table below; table/form/sheets existence still needs canvas.
3. Open in Figma logged-in before citing any table anatomy or token.

## Details

| Topic | Observed (verbatim or literal) |
|-------|-------------------------------|
| Title / H1 | `Order list page` |
| Publisher | `ByeWind` (`/@byewind`) |
| Counters | `11` likes · `1k usuarios` · `0 comentarios` (page text, may drift) |
| License / updated | `CC BY 4.0` · `Última actualización hace 3 días` |
| Description (full, quoted) | `Hello` / `This page from SnowUI.` / `SnowUI` / `SnowUI is a design system and UI Kit.` / `Preview in Figma` (link `https://www.figma.com/file/PAA0JKidFMVK44KRRWB1zL`) |
| Tags | `Paneles`, `SaaS`, `CRM` + `#form #sheets #table` |
| Preview | Main preview + `Vista previa` section with iframe; 2 `<img>` with preview alt observed |

## Behind auth / JS wall

| Attempt | Result |
|---------|--------|
| `webfetch markdown` (this pass) | Title only: `Order list page \| Figma`. No body. |
| Browser + JS, no login (this pass) | Full page above rendered. No login wall for reading. |
| `Abrir en Figma` / `Preview in Figma` link / iframe embed | Requires login; table columns, form fields, sheets behavior, and any hex/font/px NOT observable. |
| Numeric design tokens | Zero observed. No hex, no px, no radius, no font names as page text. Nothing invented here. |

## Checklist

- [ ] `05.png` shows header + preview for audit
- [ ] Description quoted verbatim, not expanded
- [ ] Table/form/sheets mechanics still need in-canvas sampling

## Next step

Feed this + `05-order-list.md` to `sdd-research` for the lists slice; sample SnowUI table in-canvas.
