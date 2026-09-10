# Archive Report: Unified Design System (geskio)

```yaml
schema: gentle-ai.archive-report/v1
change: design-system
project: geskio
branch: base-primer-commit
archived_to: openspec/changes/archive/2026-09-10-design-system/
archive_date: 2026-09-10
artifact_store: openspec (authoritative)
verdict_at_close: PASS (verify rev4, supersedes rev1-rev3 in same file)
requirements: 16/16
scenarios: 25/25
critical: 0
warnings: 0
tasks: 15/15 + 5.4 + 5.5 + 5.6 all [x]
specs_synced: 3 created / 0 updated / 0 removed
```

## Final State (authoritative at close)

Per orchestrator FINAL-STATE FACTS (outrank intermediate `apply-progress.md` and `verify-report.md` rev1-rev3):

- Vigent verdict: verify rev4 PASS — 16/16 requirements, 25/25 scenarios, 0 CRITICAL, 0 WARNING. C-1 and B-1..B-7 closed with recomputed ratios over current code.
- 12 local commits, no push yet: 5 slices (`0e79fc5` 764L, `873f071` 135L, `7fd4751` 574L, `c9c684d` 390L, `ec02d7b` 158L) + closeout `c0da8b2` + fix `c252c88` + hardening `5a80d38`, `6b3baf2`, `8692a4b`, `2f80001` + remediation `b6ec7be`, `f3c754a`.
- `tasks.md`: 15/15 + 5.4 + 5.5 + 5.6 all `[x]`. Task Completion Gate passes with no stale checkboxes; no exceptional reconciliation was needed.
- `audit.md`: its 7 BLOCKERs (B-1..B-7) are closed with evidence in verify rev4. Its 13 MAYORs + MENORES move to follow-up backlog (listed below) — they are NOT close debt.
- Post-archive pending (orchestrator-owned, NOT this phase): push + 6 stacked PRs to main (`stacked-to-main`).
- This phase commits in ONE docs-only commit what remained uncommitted (verify-report rev4, audit.md, this archive-report, tasks.md if changed): `docs(design-system): close change with verify rev4, audit and archive report`. No code touched, no push, no PR.

## Effective Tokens (recalibrated post-design, authoritative)

Values in force are those in `app/theme.py` at close, NOT the `design.md` snapshot:

- muted `#606b7a` / `#7f8894`, primary light `#c81e1e` / `#166534`, primary dark `#e11d48`, danger bg `#dc2626` + danger_text `#dc2626` / `#fb7185`, accent_text `#c81e1e` / `#f43f5e`, footer_hover `#f43f5e`, success light `#166534`.
- 19/19 pairs >= 4.5 both themes/modes; landing parity 1:1 over 20 roles + 4 radii.
- Documented collisions kept: VERDE `primary == success` (`#166534`) mirrors ADR-1/M-12; Deben shares red (accepted per ADR-1).

## Specs Synced (Step 2, before move)

`openspec/specs/` was empty, so each delta spec was a full spec. Mechanically copied with shell only (`cp` to temp + `diff -r` + `mv`), never Read/Write. All readbacks empty (verbatim output in phase result).

| Domain | Action | Details |
|--------|--------|---------|
| design-tokens | Created | 6 requirements, 9 scenarios added; 0 modified; 0 removed |
| widget-kit | Created | 5 requirements, 7 scenarios added; 0 modified; 0 removed |
| brand-alignment | Created | 5 requirements, 9 scenarios added; 0 modified; 0 removed |

`rules.archive` from `openspec/config.yaml` ("Warn before merging destructive deltas") was checked: merge is purely additive (no main spec existed, nothing deleted), so no destructive warning applies.

Targets now source of truth:

- `openspec/specs/design-tokens/spec.md`
- `openspec/specs/widget-kit/spec.md`
- `openspec/specs/brand-alignment/spec.md`

## Archive Move (Step 3, mechanical)

Moved with shell only (`git mv`, fallback `mv` refused unless source unchanged), verified by recursive snapshot + `diff -r`. Readback empty (verbatim output in phase result). Archive-report in destination is additive-only and excluded from the source/destination comparison (it did not exist in the pre-move snapshot).

Archived to: `openspec/changes/archive/2026-09-10-design-system/`

### Archive Contents

- proposal.md present
- specs/ present (3 domains)
- design.md present
- tasks.md present (15/15 + 5.4/5.5/5.6 complete, no unchecked implementation tasks)
- apply-progress.md present (intermediate snapshot, superseded by final-state facts where they differ)
- verify-report.md present (rev4 PASS vigent; rev1-rev3 history in same file, superseded)
- research.md present (rev3, outcome done)
- exploration.md present
- audit.md present (7 BLOCKERs closed per rev4; MAYORs/MENORES to backlog)
- references/ present (5 fichas + README + 5 canvas notes + 5 audit PNGs)
- archive-report.md present (this file, additive)

Active directory `openspec/changes/design-system/` no longer exists.

## Decision Traceability

- D1 One token namespace (Paperpillar 01 anchors shell; 02-05 re-expressed, never verbatim; anti-frankenstein). Implemented as `app/theme.py` + `app/widgets.py`.
- D2 Brand: primary = landing accent red family for convergence; green stays semantic (success/money). Multi-theme `app_colors` + accent override per explicit user requirement.
- D3 Spacing + radii frozen upfront in system per explicit requirement.
- D4 Landing NOT frozen: in scope for token alignment (user asked to improve app AND page). CSS-var-only + 3 `script.js` token assignments, single-unit revert.
- D5 Delivery via per-screen slices under auto-chain, 800-line review budget, order theme -> widgets -> dashboard -> caja/stock -> clientes/fiado -> chat+landing.
- Research rescope (orchestrator-binding, rev3): research answers PATTERNS + observable metadata only; final numerics out of scope (decided in design from exploration + D1-D5). Q4 `figma-crm-pointer-deferred` contributes zero patterns to v1 until logged-in canvas verification (C4.7). Corpus-wide absence of hex/radius/font values logged as validated finding C0.3, not a gap.
- Ledger accounting resets by delegation: user delegated ALL product decisions; D1-D5 registered as CONFIRMED (product choices, non-evidence). Rev2 partial (Q4 title-only, decisions pending) upgraded by canvas evidence + rescope; rev2 upgrade path superseded by rescope, not silently dropped (research.md records lineage).
- Verify chain fail->pass: rev3 FAIL blocked solely by C-1 (accent-as-text regressions) -> remediation `b6ec7be` (accent_text role + success token) + `f3c754a` (footer_hover split, justified by 3.02 recomputation) -> rev4 PASS with all 5 regressed pairs recomputed >= 4.5, B-1..B-7 re-confirmed, bounded regression 7/7 clean, parity enlarged to 20 roles, W-1 resolved. No fixes made by verify phase itself. S-1..S-7 persist as non-blocking suggestions.

## Verify Summary (rev4, vigent)

- Build gate: `python -m py_compile` 10 app modules, exit 0.
- Test gate: `geskio_verify_c1_remediation.py`, exit 0 (49 threshold rows + 1 justification row, all in-threshold; methodology cross-check reproduces rev3 numbers on unchanged pairs).
- C-1 closure: form-note 5.74/4.65, debtor-amt 4.65, mc-bot strong 5.35/4.84, footer hover 4.71/5.42, success note 7.13/9.80; accent-as-text sweep leaves only large-text/decorative `var(--accent)` set.
- B-1..B-7 closed with structural greps + recomputed ratios (see verify-report for full matrix).
- Pre-existing conditions re-confirmed NOT introduced: Dropdown `on_change` quirk (base `5d3a3c7`), LSP stub noise, ElevatedButton DeprecationWarning, audit M-1..M-13 punch list (M-12 script.js half token-fixed, M-13 color-mix fallback still open), keyword chat without LLM.
- CRITICAL: none. WARNING: none. Strict archive policy satisfied (no CRITICAL override, no partial archive, no stale checkboxes).

## Follow-up Backlog (NOT close debt)

From `audit.md` MAYORs + MENORES, per orchestrator instruction listed as follow-ups:

1. Kit completion: `AppButton` + screen titles; migrate 5/6 screens off hand-built `FS_30` titles; use or remove `Badge` (M-3; S-1 persists).
2. Silent errors: zero `print()` as sole handler; empty-name guards without feedback (`stock.py:187`, `clientes.py:161`); unbounded SnackBar stacking in `feedback()` (M-4).
3. Mobile drawer: scrim, in-drawer CTA, `aria-expanded`, Escape close (M-6); H1 before mockup at <=980px (M-5).
4. Copy trust: "Sin instalaciones / Funciona en el navegador" vs fixed 1100x700 desktop; browser Dashboard mockup (M-7); `mailto:`/`tel:`, real socials or removal (M-8).
5. Footer `color-mix` fallback for non-supporting browsers (M-13).
6. Von Restorff dilution: landing accent in ~15 places (M-1); dashboard 4 saturated stats + Deben/brand red collision (M-2, accepted per ADR-1).
7. Marquee pause control (WCAG 2.2.2 mitigated by `prefers-reduced-motion` only) (M-9).
8. Search inputs hint-only labeling; brand dropdown vs mode toggle competing theme controls (M-10, Hick).
9. Touch density: 18px row IconButtons at 4px gaps; paid `✔` as `ft.Text` violating ADR-3 (M-11).
10. Verde = marca = exito conceptual collision (M-12, code half fixed; conceptual part remains).
11. Minor polish batch: off-scale radii (nav-link 8px, mc-row 13px), dual money voices (FS_36 vs FS_28), 4px cart padding, 12px dividers + SP_10 vs SP_12 rhythm, Instrument Serif vs Inter voice split, monochrome mockup vs color stats, black->red primary hover hue mutation, "Detalles"->#numeros label mismatch, verbose dropdown options, "Cant" 80px field, testimonial verifiability (MENORES).
12. Code-doc nits: `design.md` open questions unchecked though resolved in code (S-5); `theme.py:49` "nav also bold" vs `main.py` nav_style + superseded B-4 line coexisting (S-7); light `accent_soft` pre-blend <=4/255 inexactness (S-3); file-scoped styles.css-only revert would desync JS tokens — chain revert stays atomic (S-4).

## SDD Cycle Complete

Change fully planned, implemented, verified, and archived. Next owner: orchestrator for push + 6 stacked PRs to main.
