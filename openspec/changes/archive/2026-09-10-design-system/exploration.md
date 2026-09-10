## Exploration: design-system

### Current State
GesKio has two UI worlds with no shared tokens. `app/` (Python 3.11 + Flet 0.84.0, unpinned) is a desktop nav-shell: `main.py` instantiates 6 screens eagerly, top `Row` of `TextButton`s + `Divider`, `Screen(ft.Container, padding=24, expand=True)` base with lazy `build()` + `actualizar()`. `landing/` is a vanilla static site (`index.html` + `styles.css` + `script.js`) with a mature token system: CSS vars for light/dark, Inter + Instrument Serif, radius 10/18/pill, shadows + grain, blur navbar, reveal/marquee/theme-toggle. All Flet styling is hardcoded per-screen; landing styling is centralized in `:root` / `[data-theme="dark"]`.

### Affected Areas
- `app/main.py` — nav-shell: window 1100x700, `page.padding=0`, top `Container(padding=top=5)` + centered `Row(spacing=4)` of `TextButton`s (`padding h12/v8`); active = `GREEN_100` bg + `GREEN_800` text + `BorderSide(2, GREEN)`, inactive = `None` (theme default). No `Theme`, no fonts, no dark mode.
- `app/screen_base.py` — `Screen`: `expand=True, visible=False, padding=24`; lazy `armado` flag. Single choke point for padding/typography — ideal token injection spot.
- `app/screens/dashboard.py` — reference card pattern: `Container(padding=20, radius=12, bgcolor=SURFACE, border=OUTLINE_VARIANT, expand=True)`, label `size=12 BOLD GREY_500`, value `size=28 BOLD` (Hoy=GREEN, Mes=BLUE, Ganancia=AMBER, Deben=RED); header `Text size=30 BOLD` + spacer + `IconButton(REFRESH, 20)`; `Row(spacing=12)`, outer `Column(spacing=12, scroll=AUTO)`; `Divider(height=20)`; alert list `Column(spacing=5)` with emoji + plain `Text` (`⬇/💰/✅`, RED/GREEN/default).
- `app/screens/caja.py` — `Column(spacing=10)`; `Dropdown`s + `TextField(width=80)`; cart `Container(radius=8, SURFACE, padding=8)` (only radius-8 in app); item rows `padding v4/h4` + bottom border `0.5 OUTLINE_VARIANT` (name 14 BOLD, detail 12 GREY_500, subtotal 16 BOLD, CLOSE 18 ERROR); `TOTAL size=20 BOLD` + total `size=36 BOLD GREEN`; `Cobrar` = only filled CTA (`GREEN` bg + `WHITE` text); `SnackBar(duration=4000)` via `page.overlay`.
- `app/screens/stock.py` — `DataTable(column_spacing=12)`, 7 cols; row actions `EDIT / ADD_CIRCLE_OUTLINE / DELETE_OUTLINE(16, ERROR, spacing=2)`; low-stock `RED+BOLD`; create-row `Row(spacing=8)` with 5 `TextField`s + default `ElevatedButton`; `AlertDialog`s (edit/stock/delete) with `TextButton Cancelar` + `ElevatedButton` (delete = `RED/WHITE`); stock quick-set `−10/−1/campo/+1/+10 (spacing=6)`.
- `app/screens/clientes.py` — same table/form/dialog/SnackBar pattern as stock but `column_spacing=16` (inconsistent); cols `Nombre/Telefono/Compras/Debe/""`; debt `RED+BOLD`; new-row `Row(spacing=8)`, `Nombre expand=True`; delete dialog appends `⚠️ Tiene deudas pendientes`.
- `app/screens/fiado.py` — title `Cuenta Corriente` vs nav label `Fiado` (naming mismatch); `Switch(Solo pendientes=True)`; `Divider(height=4)` (vs 20 dashboard); `DataTable(column_spacing=12)` 6 cols; `estado_color`: GREEN paid / RED dias>30 / AMBER else; `Pagar ElevatedButton` vs `✔ GREEN Text`; bottom `Refrescar ElevatedButton`.
- `app/screens/chat.py` — subtitle `size=13 GREY_500`; messages `Container(expand, radius=12, SURFACE, OUTLINE_VARIANT, padding=14)`; bubbles `padding h14/v10, radius=12` both sides (no tail), `GREEN_50` user vs `GREY_100` bot, `Row END/START`; input `TextField(hint, expand, on_submit)` + `IconButton(SEND, GREEN)`; rule-based keyword responder, no LLM.
- `app/datos.py` — no UI, but drives UI strings: seed products/clients/ventas shape table columns, `stats()` keys (`hoy/mes/ganancia/deben/stock_bajo`) map 1:1 to dashboard cards + chat answers.
- `landing/index.html` — sections: fixed nav + hero (copy + device mockup with Hoy/Mes/Ganancia/Deben + stock-bajo + fiado) + marquee + bento (Dashboard-lg/Caja/Stock/Clientes/Fiado/Chat-lg) + numbers + testimonials + CTA form + footer; icons = inline SVG stroke-2 (feather-style); logo = 4-square mark with accent square.
- `landing/styles.css` — tokens: light `--bg #fff, --bg-soft #f6f7f9, --bg-elevated #fff, --text #161b22, --text-soft #52606d, --text-muted #8993a3, --border #e7e9ed, --border-strong #d5d9e0, --accent #ef4444/hover #dc2626/soft rgba(239,68,68,.10)`; dark `--bg #0e1014, --bg-soft #15181e, --bg-elevated #181c23, --text #f3f5f8, --accent #f43f5e`; fonts Inter 400–900 + Instrument Serif titles (hero clamp 2.8–5.2rem, section 2.1–3.4rem); radii btn/field/icon/social/toggle=10, card/testimonial/form/device-block=18, chip=pill, ds-tile=10, mc-row=13 (4px tail); buttons `.btn-primary=var(--text)→hover accent+translateY(-2px)`, `.btn-ghost=1.5px border-strong`; shadows sm/std/lg + grain .04/.06; nav blur 16px/saturate 140%; `mc-user=var(--text)/var(--bg)`, `mc-bot=var(--bg-soft)`.
- `landing/script.js` — navbar `scrolled` (>20px), mobile drawer, theme toggle (`data-theme` + `localStorage geskio-theme` + `prefers-color-scheme` follow), IntersectionObserver reveal (`threshold .08`, `data-delay`), marquee width-fill + duration `half/42` clamped 20–90s, fake async contact form (validates nombre/email, `Enviando…` → green `#059669` success), footer year. No build step.

### Approaches
1. **Token module + landing alignment (minimal)** — New `app/theme.py` (or `tokens.py`) with colors/spacing/radii/typography constants mirroring landing CSS vars; replace hardcoded `GREEN/RED/BLUE/AMBER/GREY_500`, `padding 20/14/8`, `radius 12/8` via imports; fix `column_spacing 12 vs 16`, `Divider heights`, cart radius. Landing untouched.
   - Pros: smallest diff; single source in app; fixes internal inconsistencies fast; no dependency risk
   - Cons: two sources of truth remain (py constants vs CSS vars); no shared components, drift returns; no dark mode in Flet
   - Effort: Low

2. **Shared component kit (recommended increment)** — Option 1 + `app/widgets.py`: `AppCard`, `AppHeader(title, on_refresh)`, `AppTable` wrapper (fixed `column_spacing`, empty-state row), `AppDialog`/`confirm_delete`, `feedback(text)` (SnackBar), `StockBadge/DebtText`, chat bubbles with tail radii; migrate 6 screens + document mapping to landing classes (`.card`, `.btn`, `.chip`, `.mc-row`).
   - Pros: kills duplication (dialog/SnackBar/table code repeated in 4 screens); enforces radii/padding/type scale; reviewable in slices per screen; sets up future Flet `Theme`
   - Cons: touches every screen; needs care with Flet 0.84.0 unpinned API (`ft.Colors`, `ft.Icons`, `BorderSide`); slightly larger PR
   - Effort: Medium

3. **Full brand convergence + Flet theming** — Option 2 + Flet `Theme(color_scheme_seed, fonts Inter)` loading Inter (bundled asset or Google Fonts), accent decision (landing red `#ef4444` vs app green), dark `ThemeMode` toggle mirroring `geskio-theme`, replace Material icons + emoji (`⬇💰✅🎉⚠️✔`) with single set, responsive nav (sidebar/drawer for 1100x700).
   - Pros: one brand across app + landing; resolves biggest visual gap (red vs green, serif vs system, light-only vs dark-ready)
   - Cons: font bundling + `Theme` on unpinned Flet is the riskiest part; accent change is a product decision; largest diff, needs chained PRs
   - Effort: Medium/High

### Recommendation
Option 1 first, then Option 2 in the same change sliced per screen: centralize tokens in `app/theme.py` (colors incl. semantic Hoy/Mes/Ganancia/Deben/estado, spacing 4/8/10/12/20/24, radii, text styles 12/13/14/16/18/20/28/30/36) referencing landing `:root` values, normalize `column_spacing=12`, `Divider`, cart `radius 12`, then extract `widgets.py` (card/header/table/dialog/feedback/bubbles). Defer Option 3 (accent red-vs-green, Inter in Flet, dark mode, icon/emoji unification, responsive nav) to proposal with an explicit brand decision — it exceeds the 800-line review budget as a single PR and needs `delivery_strategy=auto-chain`.

### Risks
- Brand fork: app semantic GREEN vs landing accent RED `#ef4444` — proposal MUST pick primary/CTA color before coding, else rework.
- Unpinned Flet 0.84.0 + no `requirements.txt`/`pyproject.toml`: `Theme`/`Colors`/`Icons` API drift can break a full-theming attempt; pin or verify with `pip show flet` during design.
- Emoji-as-icons (`⬇💰✅🎉⚠️✔`) vs Material `Icons` vs landing stroke SVGs: three icon languages; unifying is scope creep if not bounded.
- `fiado.py` title (`Cuenta Corriente`) vs nav (`Fiado`) + `Divider(height=4 vs 20)` + `column_spacing (12 vs 16)` + `radius (8 vs 12)` show copy-paste drift — any token pass must grep all screens, not just dashboard.
- Review budget: 6 screens + landing mapping easily exceeds 800 lines in one PR; chain per-screen slices (dashboard → caja/stock → clientes/fiado → chat + landing doc).

### Ready for Proposal
Yes — scope to Options 1+2 (tokens + kit, landing as read-only reference), defer Option 3 brand/theming decisions. Orchestrator should confirm: (a) accent source of truth (keep app green vs adopt landing red), (b) whether landing `styles.css` may be touched or is frozen, (c) per-screen chained PRs acceptable under `auto-chain`.
