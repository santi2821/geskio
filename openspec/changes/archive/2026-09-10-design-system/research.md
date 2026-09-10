# SDD Research — change: design-system

```yaml
schema: gentle-ai.sdd-research/v1
revision: 3
outcome: done
generated_at: 2026-09-09
project: geskio
store_mode: hybrid
recovery_of: revision 2 (partial — Q4 title-only + decisions pending; upgraded by canvas evidence + orchestrator rescope)
grants: {documentation: 11, open-web: 0}
```

## Admission

- Final recovery run of partial revision 2. Inputs applied since rev 2: (a) the reference-gathering pass added a browser canvas layer — 5 per-file canvas notes + an updated README canvas section (all documentation-class, audited); (b) the orchestrator issued a binding rescope and 5 confirmed product decisions. No state invented: everything below is derived from the 11 admitted documentation files, read in full during this run, plus orchestrator-declared scope.
- Capability declaration supplied by orchestrator: `gentle-ai.sdd-research-capability/v1`.
- Observed exact grants (all 11 files verified present on disk and read in full before any claim was written):
  - `documentation`:
    1. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\01-paperpillar.md`
    2. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\02-wellnest.md`
    3. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\03-dashstack.md`
    4. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\04-crm.md`
    5. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\05-order-list.md`
    6. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\README.md`
    7. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\canvas\c1-paperpillar.md`
    8. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\canvas\c2-wellnest.md`
    9. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\canvas\c3-dashstack.md`
    10. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\canvas\c4-crm.md`
    11. `E:\Nueva carpeta (2)\openspec\changes\design-system\references\canvas\c5-order-list.md`
  - `open-web`: `[]` — declared and stayed empty; this revision contains zero open-web claims. Browser MCP tools remain inherited generic tools and are **not** evidence grants of this run; the canvas notes under `references/canvas/` are cited as documentation-class sources (recorded by the reference-gathering pass, ledger date 2026-09-10), never as open-web observations of this run.
- Audit screenshots `canvas/01.png`–`05.png` are referenced by the admitted canvas notes but are **not** in the declared grant set and were not read by this run.
- Requested source classes: `documentation` only.
- Admission decision: **GRANTED** for all 11 documentation sources. Question-to-source mapping: each rescoped question maps to its ficha (SRC-01..05) + canvas note (SRC-06..10) pair, with the README as the cross-cutting ledger (SRC-00).
- Scope rule: every claim below cites documentation-class sources only.

## Rescope (orchestrator-owned, binding for this revision)

- Research answers **PATTERNS + observable metadata only**. Final numeric values (hex colors, radius px, spacing px except the 4px grid cited as text, final font family) are **explicitly out of scope** for research; they are decided in `design` from explore evidence (landing CSS vars + app patterns) plus the confirmed decisions below.
- No NOT OBSERVED item is cited as observed; the absence of values is itself a validated finding (C0.3), not a gap to fill.
- Q4 rescoped and renamed: `figma-crm-pointer-deferred` — verified pointer only (identity, tags, counters, confirmed description absence); contributes **zero patterns** to `design.md` v1 until logged-in canvas verification. Explicit deferral, no substitution.

## Retained intent — execution status (recovery lineage)

- Objective carried losslessly from rev 1: 5 Figma references → harmonious `design.md`, one design system, anti-frankenstein. Rev 2 outcome (`partial`: Q4 title-only, decisions pending) was carried honestly into this run's inputs.
- Rev 2's upgrade path ("Canvas-pass requirements") is **superseded by rescope, not silently dropped**: items 1/2/5 (sample hex/font/px in canvas; re-enter research with measured values) → moved to design-side value decisions; item 3 (resolve 04) → identity now resolved via canvas page (SRC-09), contents deferred by explicit decision; item 4 (single-base discipline) → remains in force.
- The confirmed decisions (see preproposal) replace rev 2's "decision points pending" table. Nothing was re-derived from either surviving store; canonical desired content was fixed before any write, per the hybrid recovery contract.

## Questions

| # | Question id | Mapped sources | Support level (within rescoped scope) |
|---|-------------|----------------|----------------------------------------|
| 1 | figma-paperpillar-base | SRC-01, SRC-06 | Strong — shell structure, component existence, font shortlist as text OBSERVED (canvas-corroborated); numeric values out of scope |
| 2 | figma-wellnest-stats-calendar | SRC-02, SRC-07 | Strong — screen inventory as text, calm direction, stats/calendar existence OBSERVED; interaction/anatomy NOT OBSERVED (design-side) |
| 3 | figma-dashstack-widgets | SRC-03, SRC-08 | Strong — widget mechanism set (4px grid as text, variables, auto-layout, light/dark, responsive intent) OBSERVED; widget pixels NOT OBSERVED |
| 4 | figma-crm-pointer-deferred | SRC-04, SRC-09 | Strong for pointer scope — Maietry identity, tags, counters, confirmed description absence OBSERVED; zero pattern contribution by design |
| 5 | figma-order-list | SRC-05, SRC-10 | Strong — table/form/sheets existence + SnowUI mechanics as text OBSERVED; page pixels NOT OBSERVED |

Outcome driver: all 5 rescoped questions are supported with claims mapped to admitted sources; numeric tokens are out of scope by orchestrator decision and their corpus-wide absence is logged as a finding → outcome **`done`**.

## Sources

All sources are local documentation-class files. `accessed_at` = this run's readback of the local docs. The Figma Community URLs recorded inside each source are carried metadata from the reference-gathering pass (ledger access date 2026-09-10, per SRC-00) — they identify the underlying file; they are not open-web admissions of this run.

| id | class | title | publisher | URL (local grant) | accessed_at | excerpt |
|----|-------|-------|-----------|-------------------|-------------|---------|
| SRC-00 | documentation | Design-system references — index (sdd-research input, not SDD output) | local reference-gathering pass | openspec/changes/design-system/references/README.md | 2026-09-09 | "OBSERVED (cite freely): titles, publishers (except 04 UNKNOWN), URLs, access date 2026-09-10, descriptions/excerpts quoted in each file, Paperpillar font names, DashStack 4px grid + variables/themes, SnowUI foundation categories + layout/theme mechanics, popularity/license/tags as index data." / canvas section: "Evidence preparation only. No token claims changed." |
| SRC-01 | documentation | 01 — Paperpillar Property Management Dashboard (BASE) | local reference note; underlying publisher: Paperpillar (hello@paperpillar.com) | openspec/changes/design-system/references/01-paperpillar.md | 2026-09-09 | "Features: Auto layout components; Fully customizable components; The UI Kit is using 3 free fonts (Inter, General Sans, and Plus Jakarta Sans)." |
| SRC-02 | documentation | 02 — WellNest Hospital Management Dashboard (stats + calendar slice) | local reference note; underlying publisher: peterdraw | openspec/changes/design-system/references/02-wellnest.md | 2026-09-09 | "12 screens dashboard template. Support for Figma. Easy to edit and customize." / "The combination of blue ocean on every page brings a calm vibe." |
| SRC-03 | documentation | 03 — DashStack Free Admin Dashboard UI Kit (widgets slice) | local reference note; underlying publisher: Seju (@sejal_ui_ux) per comment thread | openspec/changes/design-system/references/03-dashstack.md | 2026-09-09 | "Key Features: 1. Figma Config Compatible (Variables, Updated Auto layout, more!) 2. Editable Components 3. Auto Layout 4. 4px Grid System 5. Light & Dark Themes 6. Fully Responsive (Mobile & Tablet) 7. Regular Update." |
| SRC-04 | documentation | 04 — CRM Dashboard (widgets + lists + icons + details slice) — LOW EVIDENCE | local reference note; underlying publisher: Maietry (observed via SRC-09; the SRC-04 ficha predates the canvas pass) | openspec/changes/design-system/references/04-crm.md | 2026-09-09 | "Assigned slice: CRM widgets + lists + icons + details. Evidence for THIS file ID is title-only — everything beyond the table below is explicitly marked INFERRED or RELATED, never observed." |
| SRC-05 | documentation | 05 — Order List Page by ByeWind / SnowUI (lists slice) | local reference note; underlying publisher: ByeWind (byewind@live.com) | openspec/changes/design-system/references/05-order-list.md | 2026-09-09 | "SnowUI design system is used to define design foundations such as variables, spacing, icon size, corner size, color, font style, effect style, etc." |
| SRC-06 | documentation | C1 — Paperpillar Property Management (canvas pass 2026-09-10) | canvas note over SRC-01's underlying page | openspec/changes/design-system/references/canvas/c1-paperpillar.md | 2026-09-09 | "Browser + JS, no login (this pass): full page above rendered. No login prompt blocked reading." / "Numeric design tokens: Zero observed. No hex, no px, no radius appears as page text. Nothing invented here." |
| SRC-07 | documentation | C2 — WellNest Hospital Dashboard (canvas pass 2026-09-10) | canvas note over SRC-02's underlying page | openspec/changes/design-system/references/canvas/c2-wellnest.md | 2026-09-09 | "`Comprar USD 22` button + `Vista previa` button (literal page text, not a design token)" / "`12 screens dashboard template` … `Using FREE fonts from Google Fonts` (no family names given)" / "Numeric design tokens: Zero observed." |
| SRC-08 | documentation | C3 — DashStack Admin UI Kit (canvas pass 2026-09-10) | canvas note over SRC-03's underlying page | openspec/changes/design-system/references/canvas/c3-dashstack.md | 2026-09-09 | "`4px` appears only inside the quoted feature string `4px Grid System` — cited as text, not as verified spacing scale. No hex, no radius, no font names on page." / comments: "Confirms icons + responsive intent, no values." |
| SRC-09 | documentation | C4 — CRM Dashboard by Maietry (canvas pass 2026-09-10) | canvas note over SRC-04's underlying page | openspec/changes/design-system/references/canvas/c4-crm.md | 2026-09-09 | "Publisher: `Maietry` (`/@maietry`) — previously UNKNOWN, now observed" / "Description: NONE — no `Acerca de` body text on page (only `Vista previa`, tags, share, footer). Any prior feature assignment to 04 is unconfirmed." / "absence of description confirmed in DOM (`bodyText` has no feature sentences). Not a load failure." |
| SRC-10 | documentation | C5 — Order List Page by ByeWind / SnowUI (canvas pass 2026-09-10) | canvas note over SRC-05's underlying page | openspec/changes/design-system/references/canvas/c5-order-list.md | 2026-09-09 | "Description (full, quoted): `Hello` / `This page from SnowUI.` / `SnowUI is a design system and UI Kit.` / `Preview in Figma` (link `https://www.figma.com/file/PAA0JKidFMVK44KRRWB1zL`)" / "Requires login; table columns, form fields, sheets behavior, and any hex/font/px NOT observable." |

Underlying Figma URLs (carried metadata from the sources, not open-web admissions of this run):

| ref | Figma Community file (canonical URL recorded in source) | ledger access date |
|-----|---|---|
| 01 | https://www.figma.com/community/file/1423862565654844475/property-management-dashboard-ui-kit-paperpillar | 2026-09-10 |
| 02 | https://www.figma.com/community/file/1410399675335737504/wellnest-hospital-management-admin-dashboard | 2026-09-10 |
| 03 | https://www.figma.com/community/file/1324762163080748317/dashstack-free-admin-dashboard-ui-kit-admin-dashboard-ui-kit-admin-dashboard | 2026-09-10 |
| 04 | https://www.figma.com/community/file/1234052751192815621/crm-dashboard | 2026-09-10 |
| 05 | https://www.figma.com/community/file/1486633496506469857/order-list-page | 2026-09-10 |

## Claims

Every claim carries a verdict — OBSERVED / INFERRED / OBSERVED ABSENCE / BOUNDARY / DEFERRED — and source IDs. No claim states a NOT OBSERVED value as observed. Per rescope, no claim proposes a final numeric token value.

### Q1 — figma-paperpillar-base (SRC-01 + SRC-06, cross-checked SRC-00)

- C1.1 (OBSERVED) Identity: "Property Management Dashboard UI Kit - Paperpillar" (Figma ID 1423862565654844475), publisher Paperpillar, license CC BY 4.0, tags Dashboards/Real estate/CRM (+ #dashboard #property #saas #statistics on page). Counter drift documented: search index ~247 likes/~9.2k users (SRC-01) vs page text 252 likes/9.3k users/0 comments (SRC-06) — both recorded, neither authoritative.
- C1.2 (OBSERVED) Kit contents: "1 Dashboard Screen; Components (Cards, Charts, Search Bar, Sidebar Menu); Design style guide (Typography and Color)" — stated in the ficha extract and corroborated as page text in the canvas pass (SRC-06 Contents row).
- C1.3 (OBSERVED) Font shortlist as text: "3 free fonts (Inter, General Sans, and Plus Jakarta Sans)" — the only font families observed anywhere in the corpus.
- C1.4 (OBSERVED) "Auto layout components; Fully customizable components."
- C1.5 (OBSERVED ABSENCE) No hex, px, or radius appears as page text anywhere (SRC-06: "Numeric design tokens: Zero observed"). The Typography + Color style-guide frame exists (SRC-01) but its values stay login-gated (SRC-06) — logged as finding; value decisions are design-side per rescope.
- C1.6 (OBSERVED, canvas method) The community page renders without login; only `Abrir en Figma` / iframe embeds require login (SRC-06).
- C1.7 (INFERRED, direction only) "Fits GesKio nav-shell + dashboard cards" — from role + component list, not from pixels.
- Contribution (pattern-level): app-shell existence pattern — sidebar menu + top-bar search + card/chart dashboard + 1 dashboard screen + style-guide frame; font shortlist {Inter, General Sans, Plus Jakarta Sans} as text. Paperpillar anchors the shell per confirmed decision D1.

### Q2 — figma-wellnest-stats-calendar (SRC-02 + SRC-07)

- C2.1 (OBSERVED) Identity: "WellNest - Hospital Management Admin Dashboard" (ID 1410399675335737504), publisher Peterdraw, community paid license, "Última actualización hace 2 años"; price button `Comprar USD 22` as literal page text (commerce datum, not a design token).
- C2.2 (OBSERVED) Screen inventory as text (Dribbble shot 25526604 via SRC-02): "Dashboard, Patients & Patient Details, Doctors & Doctor Details, Department Details, Doctor Schedules, …" — 12 screens total; the canvas carousel renders 7 thumbnail buttons + 9 preview imgs (existence only, not transcribed, SRC-07).
- C2.3 (OBSERVED, qualitative) Calm direction: "The combination of blue ocean on every page brings a calm vibe"; "The varied graphics and chart displays make the data presentation more diverse and attractive."
- C2.4 (OBSERVED, qualitative) Dense-data readability intent: "The simplicity of this template is very suitable for loading a bunch of data in a way that is easy to find and understand."
- C2.5 (OBSERVED) Page contents as text: "Modern and clean design"; "Using FREE fonts from Google Fonts" (no family names given); "Well documented"; "Easy to edit and customize"; "All graphics re-sizeable and editable."
- C2.6 (OBSERVED ABSENCE) No hex, font family, spacing, or radius anywhere in the corpus for this file; the canvas itself is paid+login-gated (SRC-07).
- C2.7 (INFERRED) Calendar interaction (day/week/month) — from "Doctor Schedules" + hospital norms; design verifies against GesKio needs.
- C2.8 (BOUNDARY) Medlink (13-page sibling kit by same author) is RELATED, NOT THIS FILE — its details must not be attributed to WellNest.
- Contribution (pattern-level): stats-widget existence + dense-data readability intent + schedules/calendar screen existence + screen inventory as text, for the GesKio dashboard slice only.

### Q3 — figma-dashstack-widgets (SRC-03 + SRC-08)

- C3.1 (OBSERVED) Identity: "DashStack - Free Admin Dashboard UI Kit - Admin & Dashboard Ui Kit - Admin Dashboard" (ID 1324762163080748317), publisher Seju (@sejal_ui_ux), free kit; counters as page text 4.7k likes / 206k users / 43 comments (ficha search index said 42 comments — drift documented, may drift).
- C3.2 (OBSERVED) 7-point Key Features, quoted on the page and in the ficha: Figma Config Compatible (Variables, Updated Auto layout, more!); Editable Components; Auto Layout; 4px Grid System; Light & Dark Themes; Fully Responsive (Mobile & Tablet); Regular Update.
- C3.3 (OBSERVED, mechanism-as-text) The only spacing datum in the corpus: "4px Grid System" — cited strictly as feature text, never as a measured scale (SRC-08 enforces this).
- C3.4 (OBSERVED, mechanism) Theming mechanism: Figma Variables + Light & Dark Themes + Auto Layout; responsive intent qualitative (Mobile & Tablet, no px breakpoints exposed).
- C3.5 (OBSERVED, signal) Comment thread asks about LineAwesome icon font, mobile version, typographies; creator replies with contact email — confirms icon + responsive intent, no values (SRC-08).
- C3.6 (OBSERVED ABSENCE) Zero measured tokens; widget inventory, hex, fonts, radii all login-gated.
- Contribution (pattern-level): generic admin-widget existence + mechanism set {4px grid as text, Variables, Auto Layout, light/dark theming, responsive intent}.

### Q4 — figma-crm-pointer-deferred (SRC-04 + SRC-09)

- C4.1 (OBSERVED) ID 1234052751192815621 verified: page exists, titled "CRM Dashboard".
- C4.2 (OBSERVED) Publisher now observed: Maietry (/@maietry), support maietryprajapat@gmail.com — resolves the rev 2 UNKNOWN.
- C4.3 (OBSERVED) Counters 199 likes / 13.6k users / 0 comments (page text); license CC BY 4.0; "Última actualización hace 3 años".
- C4.4 (OBSERVED ABSENCE, confirmed in DOM) Description: NONE — no `Acerca de` body text on the page; `bodyText` contains no feature sentences; "Not a load failure." Any prior feature assignment to 04 is unconfirmed.
- C4.5 (OBSERVED) Tags: CRM + #components #crm #dashboard #saas #style guide.
- C4.6 (NOT OBSERVED / DEFERRED) Widgets/lists/icons/details contents and all token classes — canvas login-gated; visual preview content not transcribed (SRC-09).
- C4.7 (DEFERRED, by confirmed rescope) 04 contributes ZERO patterns to `design.md` v1 until logged-in canvas verification; pointer status explicit; if later unreachable, formal replacement with an accessible file — no silent substitution.
- C4.8 (BOUNDARY) Avi Yansah "CRM Dashboard Customers List" facts are OBSERVED ABOUT ANOTHER FILE — usable only as questions to ask of 04 in canvas, never as facts about it.
- Contribution: verified research pointer only.

### Q5 — figma-order-list (SRC-05 + SRC-10)

- C5.1 (OBSERVED) Identity: "Order list page" (ID 1486633496506469857), publisher ByeWind, CC BY 4.0, 11 likes / 1k users / 0 comments, "Última actualización hace 3 días".
- C5.2 (OBSERVED) Description quoted verbatim in canvas (SRC-10): "Hello / This page from SnowUI. / SnowUI / SnowUI is a design system and UI Kit. / Preview in Figma" with preview link `https://www.figma.com/file/PAA0JKidFMVK44KRRWB1zL`.
- C5.3 (OBSERVED) Tags: Dashboards/SaaS/CRM · #form #sheets #table.
- C5.4 (OBSERVED, system level) SnowUI foundations (system file 1388431032861751537, 406 likes / 13.3k users): "SnowUI design system is used to define design foundations such as variables, spacing, icon size, corner size, color, font style, effect style, etc." + "SnowUI and 260+ pages use this design system. This design system has been optimized for 3 years."
- C5.5 (OBSERVED, mechanism; `snowui.byewind.com` fetched OK in the reference pass — the only system-level source that rendered) Free Layout (1/2/3-column + free block arrangement); Free Operation (sortable sidebar, freely-defined block sizes); Free Style (light/dark via variables + definable brand colors); Auto Layout 4.0 + component properties + individual strokes; core vs business components split; Lego-block page composition guidance ("copy the page case, delete unneeded functions, add required ones").
- C5.6 (OBSERVED, existence) Order-list table + form + sheets on THIS page (title + tags); filters/search/responsive tables OBSERVED at system level (paid-kit areas list "Dashboard Data Tables, Table Design, Responsive Tables, Filters, Search Bar") — confirm on THIS page in canvas before any anatomy claim.
- C5.7 (OBSERVED ABSENCE) No page-level hex, font family, spacing px, or radius px; row actions / pagination / statuses not exposed off-canvas; canvas login-gated (SRC-10).
- C5.8 (INFERRED) "GesKio stock/clientes/fiado tables map to this pattern" — direction from tags + system fit; GesKio `DataTable(column_spacing=12/16)` drift is exploration context, non-evidence.
- C5.9 (BOUNDARY) Paid kit listing ($99, Desktop + Mobile separately, not mere breakpoints) is system context, not THIS page's anatomy.
- Contribution (pattern-level): table/form/sheet existence pattern + SnowUI foundation categories + variable-theming + free-layout composition model, as text.

### Cross-cutting (SRC-00, SRC-06..SRC-10)

- C0.1 (OBSERVED, ledger) Honesty ledger for the set — OBSERVED: titles, publishers (04's now observed via SRC-09), URLs, access date 2026-09-10, descriptions/excerpts quoted in each file, Paperpillar font names, DashStack 4px grid + variables/themes, SnowUI foundation categories + layout/theme mechanics, popularity/license/tags as index data. NOT OBSERVED: any hex color, any spacing px beyond "4px grid" (03), any radius px, any font for 02/03/04/05, any widget/table pixel anatomy. INFERRED: "fits GesKio nav/cards/tables" mappings; calendar interaction; 04's slice assignment.
- C0.2 (OBSERVED, discipline) Single-base rule: 01 is structure/base shell; 02–05 are slices, not competing shells; 04 feeds nothing until canvas-verified.
- C0.3 (OBSERVED ABSENCE, global) Zero hex values, zero radius values, and zero font families for 02–05 exist anywhere in the corpus — including the full canvas pass ("no hex/radio/px appears as text on any page"; the real canvas remains login-gated in all 5 cases). This absence is the validated boundary finding of the evidence class and, per rescope, is terminal for research — not a gap.
- C0.4 (OBSERVED, canvas method) All 5 community pages render without login via browser+JS; `webfetch markdown` remained title-only for all five (JS wall for fetch, not for browser); screenshots + per-file notes recorded under `canvas/` for audit.

## Contradictions

- None substantive among admitted sources: ficha and canvas notes for each file agree on identity, contents, and absence claims; slices do not overlap (SRC-00 contribution matrix).
- Bookkeeping note 1 (freshness artifact, not substance): SRC-00's honesty ledger still reads "(except 04 UNKNOWN)" — written before the canvas section in the same file that observes Maietry (SRC-09). The README's later canvas section supersedes it ("Weakest link now bounded"). No claim depends on the stale parenthetical.
- Bookkeeping note 2 (index drift, expected): counter values differ between search-index (SRC-01: ~247/~9.2k; SRC-03: 42 comments) and page text (SRC-06: 252/9.3k/0; SRC-08: 43 comments). Both documented; neither authoritative; all marked "may drift".
- Freshness ordering note: the ledger records the off-canvas + canvas passes as 2026-09-10, while this run's readback is 2026-09-09; quoted excerpts are verbatim from the granted docs regardless of that ordering.

## Uncertainty and freshness

- Final numeric values (hex, radius px, spacing steps beyond 4px-as-text, font family for 02–05) are NOT OBSERVED corpus-wide and are OUT OF RESEARCH SCOPE by orchestrator decision — design decides them from explore evidence + confirmed decisions. No research claim blocks on them.
- Q4 slice contents remain unobserved; pointer status is locked by confirmed decision until logged-in canvas verification.
- Popularity/likes/users/price/updated figures are index/page text that may drift — volatile, non-authoritative.
- Calendar interaction (day/week/month) and all GesKio-fit mappings are INFERRED directions; design verifies against app needs.
- Figma community pages and index metadata may have changed since the recorded 2026-09-10 passes.

## Product choices — confirmed decisions (separate from claims; non-authoritative for evidence)

Registered by orchestrator instruction: the user delegated ALL product decisions; the following are CONFIRMED. They are product choices, not evidence claims.

- D1. One token namespace (color/type/space/radius). Paperpillar (01) anchors the shell; 02–05 contribute patterns re-expressed in that namespace, never verbatim styles (anti-frankenstein).
- D2. Brand: primary = the landing accent family (red) for convergence; green remains a semantic role (success/money), not the primary. The `app_colors` module offers several themes + customization (explicit user requirement).
- D3. Spacing + radii frozen upfront in the system (explicit requirement) during design.
- D4. Landing NOT frozen: in scope for token alignment (user asked to improve both app AND page).
- D5. Delivery via per-screen slices under auto-chain, review budget 800 lines.

## Out-of-scope register (explicit)

- Research does NOT decide: final hex palette, radius px values, spacing px values (beyond the 4px grid cited as text), final font family. Design sources these from exploration evidence (landing CSS vars + app patterns) + D1–D5.
- 04 CRM contents: deferred until logged-in canvas verification; zero pattern contribution to `design.md` v1 (C4.7).

## Preproposal state (gentle-ai.sdd-preproposal/v1, revision 3)

```yaml
schema: gentle-ai.sdd-preproposal/v1
revision: 3
exploration_outcome: ready-for-proposal (per openspec/changes/design-system/exploration.md; non-authoritative context)
research_request:
  change: design-system
  questions: [figma-paperpillar-base, figma-wellnest-stats-calendar, figma-dashstack-widgets, figma-crm-pointer-deferred, figma-order-list]
  requested_classes: [documentation]
admission: granted (documentation: 11 sources — 5 fichas + README ledger + 5 canvas notes; open-web declared empty and stayed empty)
research_outcome: done
product_decisions: confirmed (D1–D5 listed above)
proposal_ready: true
engram_reference: sdd/design-system/research + sdd/design-system/preproposal
openspec_reference: openspec/changes/design-system/research.md
```

### Readiness (closed matrix, hybrid)

- Evidence: valid — every rescoped question supported with claims mapped to admitted documentation sources; absences logged as findings.
- Store: OpenSpec write + Engram upserts issued with identical bytes; readiness declared only after readback comparison of both stores (result recorded in the phase envelope returned to the orchestrator).
- Decisions: `confirmed` (D1–D5, orchestrator-registered).
- `proposal_ready`: **true** — outcome `done`, decisions confirmed, references valid, store ready (pending the readback comparison executed below).

### Persistence log (rev 3)

- Canonical desired content fixed before any write (11 granted docs + orchestrator rescope + confirmed decisions D1–D5).
- Writes: `openspec/changes/design-system/research.md` (rev 3) + `mem_save` upserts to `sdd/design-system/research` and `sdd/design-system/preproposal`, all with identical bytes.
- Readback + byte comparison of all three stores executed before the readiness declaration in the envelope; any divergence would have triggered a new positive revision from retained intent per the hybrid recovery contract.
