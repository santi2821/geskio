## Exploration: ui-v2 (geskio) — rebuild from scratch, faithful to Figma references

### Current State
v1 after `design-system` (archived `2026-09-10-design-system`) is a coherent but flat Flet app on pinned `flet==0.84.0` (`requirements.txt`). `app/datos.py` is an in-memory store (productos/clientes/ventas/cuentas, CRUD, `stats()`, 2 seed ventas) and is the frozen contract for v2. `app/theme.py` is a single token namespace (`PaletteTheme` ROJO/VERDE x light/dark, `AppColors` registry with accent override + `geskio-theme`/`geskio-brand`/`geskio-accent` persistence, spacing 4/8/10/12/20/24 on a 4px grid, radii 10/12/18/pill, type 12–36, Inter-if-available with no bundling). `app/widgets.py` is a partial kit on tokens only: `AppCard`, `AppStatCard` (label 12 muted + value 28 bold, role color), `AppHeader` (title 30 bold + refresh), `AppTable` (`column_spacing=12`, empty-state), `AppDialog`/`confirm_delete` (modal, destructive = danger), `feedback` (SnackBar via `page.overlay`, 4000ms), `Badge`, `ChatBubble` (user accent_soft END / bot surface START), `sync_text`. `app/screen_base.py` (`Screen(ft.Container, padding=24, expand=True)`, lazy `build()` + `actualizar()`, `invalidate()` rebuild hook) and `app/main.py` (eager 6 screens, top centered `Row(spacing=4)` of `TextButton`s + `Divider`, toolbar mixing nav + mode + brand, window 1100x700, `page.padding=0`) complete the shell. Six screens keep current features/flows: dashboard (4 stat cards + alert list), caja (client/pago/producto dropdowns + cart + TOTAL + Cobrar), stock/clientes/fiado (DataTable + inline create row + dialogs), chat (keyword responder over real datos). Hardened v1 behaviors that v2 MUST preserve: `sync_text` on fields, `on_select` on dropdowns, AA roles 19/19 >=4.5 (`danger`/`danger_text` split, `accent`/`accent_text` split, `footer_hover`), `:focus-visible`, `AppDialog` with no bypass. Figma evidence boundary (research rev 3, binding): canvases stay login-gated; admissible evidence is documented patterns only, never pixel measurements. Hierarchy is fixed: Paperpillar = shell/base (sidebar + topbar + dashboard), WellNest = stats + calendar, DashStack = widget mechanics, SnowUI = tables/forms, CRM-04 = deferred (zero contribution until logged-in verification).

### Affected Areas
- `app/main.py` — biggest fidelity blocker. Top `Row` nav vs Paperpillar sidebar + topbar shell; toolbar conflates nav/mode/brand; no search, no user slot, no responsive collapse; window fixed 1100x700. Rebuild as shell.
- `app/screens/dashboard.py` — flat density. Four `AppStatCard`s in one `Row` with equal weight (no Von Restorff focal), no trend/sparkline slot, alert list as bare `Row`s (icon + text) not cards, section header weak (`Alertas` 18 bold + divider). Rebuild composition; add calendar surface (does not exist anywhere today).
- `app/screens/stock.py`, `app/screens/clientes.py`, `app/screens/fiado.py` — SnowUI gap. `AppTable` is a thin `DataTable` wrapper: no table toolbar (search + filter chips + actions), no sticky header / density control / pagination affordance, no sheet-based forms; create rows are inline `Row(spacing=8)` of 5 fields. Rebuild table pattern; keep `DataTable` if Flet allows, else compose equivalent.
- `app/screens/caja.py` — form density. Dropdowns + `TextField(width=80)` + cart `AppCard(padding=8)` + item rows with bottom border; TOTAL 36 bold + `Cobrar` filled CTA. Closest to SnowUI form pattern but needs sheet/section structure and hierarchy pass. Rebuild layout, keep flow.
- `app/screens/chat.py` — structure OK (container + bubbles + input + send), but bubble radius/padding uniform, no date dividers, no empty-state illustration slot. Light rebuild.
- `app/theme.py` — reusable starting point, not obligation. Roles, AA pairs, spacing/radii/type scales, `AppColors` wiring (`page.theme`/`dark_theme`/`theme_mode`, `to_flet_theme`) are keepers; if the visual language needs a different token structure (e.g. shell tokens: sidebar width, topbar height, elevation levels, stat hierarchy roles), propose it in design.
- `app/widgets.py` — partially reusable. Keep `sync_text`, `AppDialog`/`confirm_delete`, `feedback`, `Badge`, `ChatBubble` logic, `AppTable` empty-state; extend with `Shell`, `Topbar`, `Sidebar`, `PageHeader`, `Section`, `StatGrid`, `Calendar`, `TableToolbar`, denser `AppTable` variants.
- `app/screen_base.py` — keep `invalidate()`/rebuild contract; extend padding/section conventions for sidebar content area.
- `app/datos.py` — DO NOT TOUCH. Stable contract: CRUD, `stats()` keys (`hoy/mes/ganancia/deben/stock_bajo`), ventas `fecha`, cuentas `created_at`. Calendar and stats density MUST derive from existing reads (`ventas`, `cuentas`, `stats()`) without schema or API changes.
- `landing/` — out of scope for ui-v2 (visual scope is app only per orchestrator).
- `openspec/specs/` (`brand-alignment`, `design-tokens`, `widget-kit`) — read-only context; v2 deltas go under `openspec/changes/ui-v2/`.

### Approaches
1. **Shell-new-first (Paperpillar anchor first)** — Rebuild `main.py` into sidebar + topbar shell + new token extensions first (one slice), then migrate dashboard (stats + calendar), then tables (stock/clientes/fiado), then caja/chat into the live shell with adapters for unmigrated screens.
   - Pros: biggest fidelity gap (nav shell) validated early; gives every screen its real layout constraints; enforces one namespace before screen work; matches D1 single-base discipline.
   - Cons: temporary v2-shell + v1-screen mismatch needs a thin adapter; shell API must be stable upfront.
   - Effort: Medium (shell slice) + Medium per screen group.

2. **Screen-by-screen migration (keep top nav until last)** — Rebuild each screen's density/hierarchy inside the current top-nav shell; replace shell with sidebar + topbar only at the end.
   - Pros: smallest blast radius per slice; no adapter; each screen independently reviewable under 800-line budget.
   - Cons: screens designed against the wrong shell get reworked when the sidebar lands; delays the highest-value fidelity proof; risks two density passes.
   - Effort: Medium overall, higher rework risk.

3. **Parallel `ui_v2/` package + cutover** — Build the new UI as a sibling package importing `datos` read-only, switchable via flag, then cut over and delete v1 screens.
   - Pros: zero regression on v1 during build; cleanest structural freedom (new token layout, new kit without back-compat); easy side-by-side demo.
   - Cons: duplicates shell/kit/screens during build; cutover is a big-bang delete; drift between v1 fixes and v2 copy; largest total diff.
   - Effort: High.

### Recommendation
Approach 1 (shell-new-first). The fidelity gaps are hierarchical, not per-screen: without the Paperpillar sidebar + topbar, no screen can prove layout, density, or Von Restorff hierarchy. Sequence: (a) shell slice (sidebar + topbar + content area + token extensions, with adapter rendering old screens), (b) dashboard slice (stat density + WellNest calendar as a view-only aggregation over `ventas`/`cuentas`), (c) tables slice (SnowUI toolbar + denser `AppTable` applied to stock/clientes/fiado), (d) caja + chat slice (forms/sheets + bubble polish). Keep `theme.py`/`widgets.py` as the starting point; authorize design to restructure tokens only if the visual language requires it, with AA re-verification. Enforce per-slice <=800 lines under auto-chain on `feat/ui-figma-v2`; `base-primer-commit` stays frozen.

### Risks
- Contrast regression: any new stat hierarchy, sidebar active state, or calendar cell MUST re-prove the 19/19 AA pairs; new roles need large/UI vs normal-text classification before merge.
- `datos.py` temptation: calendar/month aggregation and table filters MUST NOT add schema or mutate APIs; derive only (e.g. group `ventas.fecha`, age `cuentas.created_at`); any needed helper is view-side.
- Flet `DataTable` ceiling: SnowUI density (sticky header, toolbar, pagination, row actions) may exceed `DataTable`; fallback is composed `Column`/`Row` tables on tokens — decide in design with a spike, not mid-slice.
- A11y/behavior loss: `sync_text`, dropdown `on_select`, `:focus-visible`, modal `AppDialog` discipline, `feedback` duration are easy to drop in a rewrite; gate each slice on them.
- Pixel-copy trap: canvases are login-gated; enforce patterns-only fidelity (layout/composition/density/hierarchy) and keep CRM-04 at zero contribution.
- Shell responsiveness: sidebar collapse at 1100x700 and smaller must be defined in design; otherwise the shell slice blocks all screens.

### Ready for Proposal
Yes — scope is bounded (visual only, 6 screens keep flows, `datos.py` frozen, references ranked, base tech pinned). Orchestrator can open proposal with: shell-first slice order above, token-restructure allowance with AA gate, calendar as view-only, and per-slice <=800-line auto-chain on `feat/ui-figma-v2`.
