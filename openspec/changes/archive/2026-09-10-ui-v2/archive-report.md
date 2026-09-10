# Archive Report: ui-v2 — Visual Rebuild Faithful to Figma (geskio)

```yaml
schema: gentle-ai.archive-report/v1
change: ui-v2
project: geskio
branch: feat/ui-figma-v2
archived_to: openspec/changes/archive/2026-09-10-ui-v2/
archive_date: 2026-09-10
artifact_store: openspec (authoritative)
verdict_at_close: PASS with warnings (37/37 scenarios, 0 critical, 2 documentary warnings)
requirements: 21/21
scenarios: 37/37
critical: 0
warnings: 2
tasks: 14/14 all [x]
specs_synced: 3 created / 3 updated / 0 removed
```

## Final State (authoritative at close)

Per Final-State Authority hierarchy (1. persisted tasks artifact > 2. orchestrator FINAL-STATE facts > 3. intermediate snapshots):

- `tasks.md`: 14/14 `[x]`, 0 unchecked. Task Completion Gate passes with no stale checkboxes; no exceptional reconciliation was needed.
- Orchestrator FINAL-STATE (launch prompt, most recent account, outranks snapshots): 5 commits (`4c1c4a6`, `3672c17`, `1c29bf0`, `6fbbdc1` + closeout `0f39848`), `app/datos.py` diff zero, AA by reuse of proven pairs, V2-D5 intact. No contradiction with higher-ranked sources or repository evidence; accepted as final.
- Per `verify-report` at verification time (intermediate snapshot, lowest rank): 21 requirements / 37 scenarios verified, verdict `pass_with_warnings`, 0 blockers, 0 critical findings, 2 documentary warnings (WARNING-1 shell signature drift, WARNING-2 trio role parenthetical). Per `apply-progress` at closeout time: 4 slice commits + closeout file, global gates PASS (datos zero, landing zero, zero new hex, AA reuse, V2-D5 preserved). Snapshot "done" claims stay true; no snapshot "pending/blocked/open" claim contradicts final state.
- No unrankable contradiction to record: launch-prompt facts are corroborated by the tasks artifact (14/14), the verify envelope (`critical_findings: 0`, `blockers: 0`), and git history (5 commits on `feat/ui-figma-v2`).
- CRITICAL gate: `verify-report` contains 0 CRITICAL findings. Strict archive policy satisfied (no CRITICAL override, no partial archive, no stale checkboxes).
- This phase touches docs only (`openspec/`), no `app/` or `landing/` code, no push, no PR (parallel actors own those trees).

## Specs Synced (Step 2, before move)

Three new domains did not exist under `openspec/specs/` and were mechanically copied with shell only (`cp` to temp + `diff -r` + `mv`), never Read/Write. All readbacks empty (verbatim output in phase result).

Three existing domains had deltas and were merged per `openspec-convention.md` (ADDED appended, MODIFIED replaced in full, other requirements preserved, no REMOVED/RENAMED). `rules.archive` from `openspec/config.yaml` ("Warn before merging destructive deltas") was checked: no deletions, no large-section removals, purely additive + in-place replacements — no destructive warning applies.

| Domain | Action | Details |
|--------|--------|---------|
| app-shell | Created | 5 requirements, 8 scenarios added; 0 modified; 0 removed |
| dashboard-composition | Created | 4 requirements, 8 scenarios added; 0 modified; 0 removed |
| table-density | Created | 4 requirements, 7 scenarios added; 0 modified; 0 removed |
| brand-alignment | Updated | 1 modified (Sliced Delivery Budget D5 shell-first a–d + datos gate + V2-D5), 1 added (Parity Trace Extended), 0 removed |
| design-tokens | Updated | 2 added (AD-5 additive shell/layout constants, AD-6 AA reuse + re-proof), 0 modified, 0 removed |
| widget-kit | Updated | 1 modified (Shared Components: PageHeader replaces AppHeader, AppTable page_size=10), 3 added (Shell kit, Dashboard kit, Table chrome kit), 0 removed |

Note on scope: the orchestrator scoped sync to the 3 NEW specs (app-shell, dashboard-composition, table-density). The 3 additional updates above follow the phase-skill mandate to sync every delta before moving, preserving all unmentioned requirements. Nothing was deleted from the source of truth.

Targets now source of truth:

- `openspec/specs/app-shell/spec.md`
- `openspec/specs/dashboard-composition/spec.md`
- `openspec/specs/table-density/spec.md`
- `openspec/specs/brand-alignment/spec.md`
- `openspec/specs/design-tokens/spec.md`
- `openspec/specs/widget-kit/spec.md`

## Archive Move (Step 3, mechanical)

Moved with shell only (`git mv` succeeded, exit 0; `mv` fallback not needed), verified by recursive pre-move snapshot + `diff -r`. Readback empty (verbatim output in phase result). This archive-report file is additive-only and was written after the readback, so it is excluded from the source/destination comparison (it did not exist in the pre-move snapshot).

Archived to: `openspec/changes/archive/2026-09-10-ui-v2/`

### Archive Contents

- proposal.md present
- specs/ present (6 domains)
- design.md present
- tasks.md present (14/14 complete, no unchecked implementation tasks)
- apply-progress.md present (intermediate snapshot, superseded by final-state facts where they differ)
- verify-report.md present (PASS with 2 documentary warnings; history in same file)
- exploration.md present
- archive-report.md present (this file, additive)

Active directory `openspec/changes/ui-v2/` no longer exists.

## Decision Traceability

- V2-D1 shell-first (AD-1/AD-2): `Shell` + adapter in `main.py`, `shell.navigate(key)`, no new topbar features. Preserved.
- V2-D2 datos frozen: view-side derive only, per-slice `git diff --exit-code -- app/datos.py` gate. Final diff zero.
- V2-D3 slice order a–d, auto-chain, ≤800 lines each (a 546, b 359, c 490, d 182). All within budget.
- V2-D4 landing parity 1:1 trace only, `landing/` zero diff. Holds.
- V2-D5 v1 fixes preserved: sync_text, on_select, AppDialog, feedback 4000ms, focus. Intact per final gates.
- V2-D6 collapse rule closed by AD-1: rail when `width <= 1280 OR height <= 760`, manual toggle fallback for OS-dependent resize events.
- AD-3 composed table chrome (TableToolbar + denser AppTable + TablePager), AD-4 focal + view-only calendar, AD-5 additive tokens (zero new hex), AD-6 AA reuse with re-proof table.

## Verify Summary (at verification time, per verify-report)

- Build gate: `python -m py_compile` 11 app modules, exit 0.
- Test gate: `python smoke_u2v.py` (paginate 23-row pager, prev bounds, collapse rule, shell tokens), exit 0.
- Global gates: datos.py zero, landing zero, zero new hex outside `theme.py`, AA re-proof all ≥4.5 normal / ≥3.0 large+UI, V2-D5 preserved, slices ≤800, CRM-04 zero, tasks 14/14.
- WARNING-1 (doc drift): implemented `Shell(page, nav_items, screens, ...)` vs documented `Shell(page, nav_items, active_key, on_navigate)`. Behavior meets contract; documented signature stale. Recommended fix is documentation alignment, no behavior defect.
- WARNING-2 (spec disagreement): trio parenthetical (accent/green/danger) vs `_ROLE_ALIASES` (info/warning/danger). Implementation follows the frozen alias table with AA proof. Recommended fix is parenthetical reconciliation, no behavior defect.
- SUGGESTION-1 (alerts as rows not cards, design-only) and SUGGESTION-2 (Calendar `today` param inert) are cosmetic/API-hygiene notes, not spec violations.

## SDD Cycle Complete

Change fully planned, implemented, verified, and archived. Next owner: orchestrator for docs-only commit (`git add openspec/` only), no push, no PR.
