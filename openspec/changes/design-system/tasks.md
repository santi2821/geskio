# Tasks: Unified Design System (geskio)

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 1100-1500 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR1 foundation → PR2 dashboard → PR3 caja+stock → PR4 clientes+fiado → PR5 chat+landing |
| Delivery strategy | auto-chain |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Foundation: tokens+kit+shell | PR1 | `python -m py_compile app/theme.py app/widgets.py` | `python app/main.py` smoke nav+theme swap | Revert PR1 only; slices 2-5 unstarted |
| 2 | Dashboard slice | PR2 | `grep -rn "ft.Colors\|#" app/screens/dashboard.py` expect zero | `python app/main.py` dashboard light/dark rojo/verde | Revert PR2; foundation intact |
| 3 | Caja+Stock slice | PR3 | `grep -rn "ft.Colors\|column_spacing\|border_radius" app/screens/caja.py app/screens/stock.py` | `python app/main.py` cobrar flow + stock table/delete | Revert PR3; other screens intact |
| 4 | Clientes+Fiado slice | PR4 | `grep -rn "Cuenta Corriente\|16\|Divider" app/screens/clientes.py app/screens/fiado.py` | `python app/main.py` filter + pending empty-state | Revert PR4; other slices intact |
| 5 | Chat+Landing+verify | PR5 | `diff landing vars vs PaletteTheme; grep CRM-04` | `python app/main.py` chat bubbles; landing checklist nav/drawer/toggle/reveal | Revert PR5 CSS-var commit only |

## Phase 1: Foundation (Slice 0)

- [x] 1.1 Create `app/theme.py` with PaletteTheme light/dark x rojo (#ef4444/#f43f5e) + verde, AppColors THEMES/accent_override/set_theme, SP/R/type tokens, #fb7185 pairing comment
- [x] 1.2 Verify client_storage API on Flet 0.84.0 in `app/theme.py`, add persistence with in-memory fallback
- [x] 1.3 Create `app/widgets.py` with AppCard/AppStatCard/AppHeader/AppTable/confirm_delete/feedback via page.overlay/Badge/ChatBubble, tokens only
- [x] 1.4 Modify `app/main.py` nav to tokens + rebuild on switch; modify `app/screen_base.py` padding SP_24 + armado rebuild hook

## Phase 2: Dashboard (Slice 1)

- [x] 2.1 Migrate `app/screens/dashboard.py` to AppStatCard/AppHeader, Hoy=success/Mes=info/Ganancia=warning/Deben=danger, standard Divider, Material icons
- [x] 2.2 Grep zero literals in `app/screens/dashboard.py`; smoke rojo/verde light/dark + accent override

## Phase 3: Caja + Stock (Slice 2)

- [x] 3.1 Migrate `app/screens/caja.py` CTA to primary red, cart radius 8→12, feedback() for totals
- [x] 3.2 Migrate `app/screens/stock.py` to AppTable SP_12 + empty-state and confirm_delete(danger)
- [x] 3.3 Grep zero literals in `app/screens/caja.py` `app/screens/stock.py`; smoke both themes

## Phase 4: Clientes + Fiado (Slice 3)

- [x] 4.1 Migrate `app/screens/clientes.py` to AppTable (16→12) + confirm_delete, kill ad-hoc dialog
- [x] 4.2 Migrate `app/screens/fiado.py` title to Fiado, Divider 4→standard, paid/due/late roles, empty-state for Solo pendientes
- [x] 4.3 Grep zero literals in `app/screens/clientes.py` `app/screens/fiado.py`; smoke filters + rebuild

## Phase 5: Chat + Landing + Verify (Slice 4)

- [x] 5.1 Migrate `app/screens/chat.py` to ChatBubble user-END accent_soft / bot-START surface, Inter-if-available no bundle
- [x] 5.2 Align `landing/styles.css` vars 1:1 to PaletteTheme light/dark, CSS-var-only, preserve nav/drawer/toggle/reveal/marquee/form
- [x] 5.3 Verify parity diff, zero literals repo-wide, CRM-04 absent, each slice ≤800 lines
- [x] 5.4 Fix WARNING-1: route 4 ad-hoc ft.AlertDialog (stock editar/ajustar, clientes editar, fiado pago) through AppDialog kit (surface + R_MD), texts/behavior preserved
- [x] 5.5 Harden a11y BLOCKERs B-1..B-7 (tokens: muted/primary/warning light+dark, danger dark deep; ChatBubble text-on-soft; fiado icon+bold+CHECK; nav 2px border; landing :focus-visible + input halo) + 3 dead assigns; ratios recalculated in theme.py parity table; verify: py_compile + ratio asserts + grep zero literals + landing parity; micro-fix danger_text split (danger bg #dc2626 both modes, danger_text light #dc2626/dark #fb7185 for stock/clientes/fiado 14px >=4.5); micro-fix contrast-2: primary dark #f43f5e->#e11d48 (Cobrar-dark 4.70) + success light #16a34a->#166534 (paid-light 7.13, collision verde-primary aceptada espejo ADR-1/M-12), landing 1:1; micro-fix contrast-3: on_accent_soft (light=primary, dark rojo #fb7185/verde #4ade80) for nav-active + ChatBubble-user + landing pill-warn/card-icon, ratios >=4.5 both modes, landing 1:1 incl. --on-accent-soft
