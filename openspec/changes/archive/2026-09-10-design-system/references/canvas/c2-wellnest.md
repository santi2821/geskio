# C2 — WellNest Hospital Dashboard (canvas pass 2026-09-10)

Canvas evidence for `02-wellnest.md`. Paid file: description + thumbnails visible without login; canvas itself gated.

## Quick path

1. Open `02.png` — header with price + preview carousel.
2. Trust the Details table below; no color/font/px values exist as page text.
3. Open in Figma logged-in + purchased before citing any token.

## Details

| Topic | Observed (verbatim or literal) |
|-------|-------------------------------|
| Title / H1 | `WellNest - Hospital Management Admin Dashboard` |
| Publisher | `Peterdraw` (`/@peterdraw`), support `afandihore@gmail.com` |
| Counters | `63` likes · `1.4k usuarios` (page text, may drift) |
| Price | `Comprar USD 22` button + `Vista previa` button (literal page text, not a design token) |
| License / updated | `Licencia de recursos de pago de la comunidad` · `Última actualización hace 2 años` |
| Description | `Get a better management dashboard ... The combination of blue ocean on every page brings a calm vibe. The varied graphics and chart displays make the data presentation more diverse and attractive ...` |
| Contents | `12 screens dashboard template`; `Support for Figma`; `Modern and clean design`; `Using FREE fonts from Google Fonts` (no family names given); `Well documented`; `Easy to edit and customize`; `All graphics re-sizeable and editable` |
| Tags | `Paneles`, `SaaS`, `Simple`, `CRM` + `#admin #doctor #health #hospital #hospital admin` (among others) |
| Preview | Carousel with 7 thumbnail buttons + main preview + `Vista previa` section; 9 `<img>` with preview alt observed |

## Behind auth / JS wall

| Attempt | Result |
|---------|--------|
| `webfetch markdown` (this pass) | Title only: `WellNest - Hospital Management Admin Dashboard \| Figma`. No body. |
| Browser + JS, no login (this pass) | Full page above rendered, including thumbnails. No login wall for reading. |
| `Abrir` / buy / iframe embed | Paid + login required; screen contents, calendar interaction, and any hex/spacing/radius NOT observable. |
| Numeric design tokens | Zero observed. `12 screens` and `USD 22` are counts/price as page text, not design values. Nothing invented here. |

## Checklist

- [ ] `02.png` shows price + carousel for audit
- [ ] No hex/font-name/px cited (Google Fonts unnamed on page)
- [ ] Calendar + dense-data claims still need in-canvas verification

## Next step

Feed this + `02-wellnest.md` to `sdd-research` for the stats-widget + calendar slice only.
