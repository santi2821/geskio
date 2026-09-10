# Design: Unified Design System (geskio)

## Technical Approach

One namespace: `app/theme.py` (D1) → `app/widgets.py` (kit) → 6 screens in slices (D5). Values only from exploration; kits supply patterns re-expressed, never measurements (C0.3). CRM-04: zero patterns (C4.7).

**Flet 0.84.0 verified in the installed env**: `ft.Theme(color_scheme=…)`, `ft.ColorScheme` (primary/surface/outline/outline_variant/error…), `page.theme`, `page.theme_mode`, `page.fonts`, `SnackBar(open=True, duration=…)` exist. `page.show_snack_bar`/`page.open` do NOT exist → feedback keeps `page.overlay` + `open=True` via the kit.

## Architecture Decisions

| ADR | Decision | Choice | Alternatives | Rationale |
|-----|----------|--------|--------------|-----------|
| 1 | Primary (D2) | Red accent: `#ef4444` light / `#f43f5e` dark, hover `#dc2626`/`#fb7185` | Keep app green | Brand convergence (D2); green stays semantic (Hoy, paid, money). Deben shares red — accepted collision |
| 2 | Inter deferred | `Theme.font_family` = Inter-if-available, platform fallback; **no bundling v1** | Bundle fonts now | `page.fonts` exists but bundling on unpinned Flet is the riskiest surface; defer until pinned |
| 3 | Icons unified | App: Material only; emoji → `TRENDING_DOWN/PAID/CHECK_CIRCLE/WARNING`. Landing keeps stroke SVGs; mapping documented, not cross-ported | Port SVGs to Flet | Kills drift per medium, zero asset work |
| 4 | Theme switch | `page.theme` + `theme_mode` swap, then rebuild (`Screen.armado=False` → `al_entrar()`) | Re-tint in place | Screens bake colors at build; rebuild is simpler and total |

### Theme switch sequence

```
User → AppColors.set_theme(name)
  → resolve PaletteTheme (light|dark + accent override)
  → page.theme = ft.Theme(color_scheme=…); page.theme_mode
  → for s in screens: s.armado = False
  → next mostrar(): al_entrar() → build() reads fresh tokens
  → page.update()
```

## Unified Matrix

| Source | Pattern role | Re-expression (tokens only) |
|--------|-------------|------------------------------|
| 01 Paperpillar | **Shell anchor (D1)** | Nav-shell + card dashboard structure; layout unchanged, restyled |
| 02 WellNest | Stats | `AppStatCard` (label 12 / value 28, role colors) |
| 03 DashStack | Widget mechanics | 4px-grid discipline; light/dark pair |
| 05 SnowUI | Table/form | `AppTable` + `AppDialog` fixed defaults |
| 04 CRM | **Deferred pointer — zero patterns v1 (C4.7)** | None |

**Token provenance (exploration only)**: colors/radii/typography ← landing `:root`/`[data-theme="dark"]`; spacing steps {4,8,10,12,20,24} ← app patterns; semantic roles ← dashboard. No token cites a Figma measurement.

**Landing (D4, CSS-var-only)**: shared roles 1:1 (bg/surface/text/border/accent/radii). `.card`↔`AppCard`, `.btn-primary`↔CTA, `.chip`↔`Badge`, `.mc-row`↔`ChatBubble`. No layout rewrite; behaviors preserved; single-commit revert.

## Data Flow

```
theme.py (tokens + app_colors registry)
     │──→ widgets.py (kit, zero literals) ──→ 6 screens (zero literals)
     └──1:1 mirror──→ landing/styles.css  :root / [data-theme="dark"]
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `app/theme.py` | Create | `PaletteTheme` (light/dark), roles Hoy=success/Mes=info/Ganancia=warning/Deben=danger/estado paid·due·late, type scale 12–36, `SP_4..SP_24`, `R_SM=10/R_MD=12/R_LG=18/R_PILL`, `AppColors` registry (≥2 themes, accent override, `set_theme`) |
| `app/widgets.py` | Create | `AppCard`, `AppStatCard`, `AppHeader`, `AppTable(SP_12, empty-state)`, `AppDialog`/`confirm_delete`, `feedback`, `Badge`, `ChatBubble` |
| `app/main.py` | Modify | Nav on tokens; theme-switch wiring |
| `app/screen_base.py` | Modify | `padding=SP_24` from token; rebuild hook (ADR-4) |
| `app/screens/*.py` | Modify | Adopt tokens/kit; fix drift: clientes `column_spacing` 16→12, fiado `Divider` 4→standard, cart radius 8→12, title `Cuenta Corriente`→`Fiado` |
| `landing/styles.css` | Modify | Variable alignment only, one commit |

## Interfaces / Contracts

```python
# theme.py
@dataclass
class PaletteTheme:  # bg, bg_soft, surface, text, text_soft, text_muted, border,
    ...              # border_strong, primary, on_primary, accent_hover, accent_soft,
                     # success, warning, danger, info

class AppColors:
    THEMES: dict[str, tuple[PaletteTheme, PaletteTheme]]  # brand + alternate
    accent_override: str | None
    def set_theme(self, name: str) -> None
    def get(self, mode: ThemeMode) -> PaletteTheme

# widgets.py — fixed defaults, never passed per screen
AppCard(content, padding=SP_20, radius=R_MD, expand=True)
AppHeader(title, on_refresh=None, actions=())          # Text 30 bold
AppTable(columns, rows, column_spacing=SP_12)          # empty state
AppDialog / confirm_delete(...)                        # destructive = danger
feedback(page, text)                                    # SnackBar duration=4000
ChatBubble(text, is_user)   # user: accent_soft END; bot: surface START
```

## Slices (D5)

0 foundation (`theme.py`+`widgets.py`+`main.py`) → 1 dashboard → 2 caja+stock → 3 clientes+fiado → 4 chat + landing vars. One commit/slice, revertible.

## Testing Strategy

| Gate | What | How |
|------|------|-----|
| Static | Zero style literals in screens/widgets | Grep `ft.Colors`/hex/padding numbers |
| Static | No reference-04 pattern | Grep tokens/specs |
| Parity | Landing vars == `PaletteTheme` values | Diff `:root`/dark vs token module |
| Smoke | Slice renders; theme switch rebuilds screens | Run `ft.app` + checklist |
| Budget | Slice ≤800 lines | Changed-line count |

No pytest in env (`strict_tdd: false` per config) — verify phase proves spec scenarios by evidence.

## Threat Matrix

N/A — no routing, shell, subprocess, VCS/PR automation, executable-file classification, or process-integration boundary.

## Migration / Rollout

No data migration. Rollback = revert per slice commit; landing is one CSS-var commit.

## Open Questions

- [ ] Alternate `THEMES` entry (name + accent): user chooses at Slice 0
- [ ] Desktop persistence of chosen theme: none v1 (no localStorage) vs file-backed — Slice 0
