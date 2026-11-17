# Design plan — tokens, devices, shell, screens

*(Purpose: the app's design system and screen layouts — tokens, type, spacing, device classes (moved here from master plan §8a), shell, screens, storage, debug and checks. Updated: 18 Nov 2026 · Bio · Build · A0 shell (v1).)*

Owner doc for: colour/type/spacing tokens, the five device classes and the layout of every screen on each, navigation and addresses, testing mode, ✎ edit hooks, `tools/layout-check`. Rules: RULES B3, C8, C13, H5, I5–I6. Decisions: D-031 (colours), D-033 (devices), D-019 (storage). Code: `index.html`, `src/css/app.css`, `src/js/`, `content/strings.js`.

## 1. Tokens (all in `src/css/app.css` `:root` — edit there only)
**Surfaces.** Light: bg `#FAFAF7` · surface `#FFFFFF` · surface-2 `#F1F0EB` · ink `#1B1D21` · muted `#55585F` · line `#DCDAD3` · control border `--line-strong` `#858279`. Dark: bg `#14161A` · surface `#1C1F24` · surface-2 `#252930` · ink `#ECEDEF` · muted `#A9AEB7` · line `#343840` · control border `#737985` (≥ 3:1, D-034). D-031 was measured on these two backgrounds.

**Germ layers (D-031 fills, D-034 edges; RULES B3)** — fill · edge (2 px, ≥ 3.5:1 on page, card **and** panel) · label text · pattern:
| Token | Fill | Edge light | Edge dark | Label | Pattern |
|---|---|---|---|---|---|
| `--g-epi` | `#56B4E9` | `#1986C4` | fill | `#111111` | open rings |
| `--g-hypo` | `#BDD9B8` | `#558C4B` | fill | `#111111` | vertical lines |
| `--g-ecto` | `#0072B2` | fill | `#0082CA` | `#FFFFFF` | dots |
| `--g-meso` | `#D55E00` | `#D05C00` | fill | `#111111` | diagonal lines |
| `--g-endo` | `#E6CF3A` | `#907F12` | fill | `#111111` | horizontal lines |
| `--g-crest` | `#009E73` | `#009069` | fill | `#111111` | cross-hatch |
| `--g-ctx` | `#828A99` | `#767F8F` | fill | `#111111` | speckle (map vocab `extra`) |
Classes `.L-<token>` draw fill + pattern + edge; `.L-multi` (several layers) is a three-way split, `.L-none` a plain chip. A layer is never shown by colour alone: pattern + label always (H5).

**Accent** `--accent #994774` (light) / `--accent-on-dark` + `--accent-text` `#C77BA2` on dark (D-034; ≥ 4.5:1 on dark page and cards) = "look here": focus rings, the current nav item, primary buttons (always with a label), the `.look` ring. Never a layer colour, never a fill alone.
**Heatmaps** use a neutral grey scale (tokens `--heat0`–`--heat4`, `.h0`–`.h4`) so colour only ever means a germ layer; the number is always printed.
**Type.** System font stack (offline, no web fonts; Devanagari via Noto when present). `--fs` 1rem (tablet portrait 1.0625rem) · `--fs-sm` .875 · `--fs-xs` .8125 · `--fs-min` 12 px floor (C8) · headings per class. Text scales with the browser/OS setting (rem); 125 % is in the test matrix.
**Spacing + shape.** `--pad` 14/12/20/20/24 px and `--gap` 10/10/14/16/16 px for p/pl/tp/tl/d · `--r` 12 px · `--tap` 44 px on touch, 36 px with a mouse (C8) · reading width `--measure` 68ch.

## 2. Devices — an optimal layout on every screen (moved from master plan §8a; D-033, RULES C13)
**Classes** — set on `<html>` by `src/js/03-device.js` from `matchMedia`, on load, rotate and resize; CSS reads `.dev-*`; components also use container queries.
| Class | Screens | Typical use |
|---|---|---|
| `dev-p` phone portrait | short side < 600 px, portrait | On the go: cards, deck, Shorts |
| `dev-pl` phone landscape | short side < 600 px, landscape | Full-screen video and 3D |
| `dev-tp` tablet portrait | short side 600–1023 px, portrait (incl. open foldables) | Study: card + 3D, reading |
| `dev-tl` tablet landscape | short side 600–1023 px landscape, or ≥ 1024 px wide with a touch pointer | Study mode: two panes |
| `dev-d` desktop / laptop | ≥ 1024 px wide with a fine pointer (mouse, trackpad) | Explorer, Studio, long sessions |

Input is separate from class: `.in-touch` (coarse pointer) / `.in-mouse` (fine + hover); keyboard works everywhere.

**Test matrix (C8 — 13 sizes, CSS px):** phones 360×640 · 390×844 · 412×915 · 430×932 · tablets 768×1024 · 800×1280 · 820×1180 · 1024×1366 · desktop 1280×720 · 1366×768 · 1440×900 · 1920×1080 · 2560×1440. Phones and tablets in portrait **and** landscape; all at 100 % and 125 % text, light and dark.

**Layout per screen:**
| Screen | Phone portrait | Phone landscape | Tablet portrait | Tablet landscape | Desktop |
|---|---|---|---|---|---|
| Today | 1 column | 2 columns, slim header | 2-column grid | nav rail + 2–3 columns | nav rail + 3 columns, max width ~1280 px |
| Explorer / Book map | drill-down, one level per screen, breadcrumb; heatmap scrolls with sticky headers | heatmap full width; tree in a drawer | tree rail + detail | tree │ heatmap or concept (2 panes) | tree │ heatmap │ concept page (3 panes) |
| Card | 3D on top (~40 % height), text below | 3D left ~55 % │ text right | 3D on top (~45 %), text below at reading width | 3D left │ text right | 3D left │ text right (≤ 70 ch) + card rail |
| Player 16:9 | video on top; transcript + card rail below | full-bleed video, overlay controls | video on top; transcript + rail below | video │ transcript + rail | video │ transcript + rail |
| Player 9:16 (Short) | full screen | centred; extras behind a button | centred; transcript below | centred; transcript + cards beside | same; never stretched or cropped |
| 3D viewer | full-width canvas; controls in a bottom sheet | full-screen canvas; controls in a side strip | canvas + bottom panel | canvas │ side panel (layers, labels, day) | canvas │ side panel; hover labels, wheel zoom, shortcuts |
| Studio (claude.ai) | review only: approve / fix line by line | as phone portrait | draft over review | draft │ review | draft │ review │ sources (3 panes) |

**Common rules:**
1. Layouts change by class (panes, rails, drawers, side panels) — never just stretched or shrunk.
2. Rotating never reloads or loses place: video time, 3D camera, scroll and open panel are kept.
3. `dvh` units and `env(safe-area-inset-*)` (notches in landscape); nothing fixed over controls (C8).
4. Reading width 45–75 characters; type, spacing and tap tokens per class in `:root` (`--fs-*`, `--tap` ≥ 44 px on touch).
5. Touch and mouse are both first-class: hover only adds (never hides a needed action); desktop keys — Space play/pause, ←/→ seek 5 s, `[` `]` day scrub, `/` search, Esc back; focus always visible.
6. Phone: main actions within thumb reach (lower half). No sideways scrolling except heatmaps and timelines (sticky headers).
7. **3D by class:** device pixel ratio capped at 2; phone budget per H8; tablet/desktop may load a richer detail level only after it is Measured (pipeline reference §2).
8. **Video outputs:** the profile's format sets the master (16:9 or 9:16); the player frames it per the table. Encodes: 720p for phones (H8); a **1080p rung for tablet/desktop — *proposed*, kept if M1 render times allow** (pipeline reference §3). Captions scale by class; burned-in Short captions stay inside the 9:16 safe area so they read on every device.
9. Artifacts (explorer, Studio, plan pages) follow the same classes and table.

**Tool:** `tools/layout-check/` (Playwright, headless Chromium, free): every screen × the matrix → automatic checks (overflow, overlap, tap size, text size, fixed-over-controls, horizontal scroll) + a **contact sheet** of screenshots per class for G-Art. Flags: `--only <screen>`, `--preview` (5 key sizes), `--debug` (outlines boxes), `--dry-run`. Runs in CI and before every UI deploy; artifacts are checked from their saved HTML. App `?debug=layout` shows class, viewport, pixel ratio and pointer in the overlay.

**Owner checks:** every UI owner check (Tn) runs on the phone (both orientations), a tablet (both) and the laptop; if a device is missing, note it and use the laptop browser's device mode instead.

**As built in A0 (v1):** nav = bottom bar on `dev-p` + `dev-tp` (thumb reach), rail on `dev-tl` + `dev-d` (labels on desktop) and a compact icon rail on `dev-pl` (keeps the short landscape height for content). Phone portrait shows only the page name in the top bar (Back + Up carry the path); phone landscape shows the last crumb. Class changes are CSS-only, so rotating keeps route, scroll and open pane (checked by layout-check).

## 3. Shell, addresses, navigation
Top bar: Back · brand · breadcrumbs · (testing flag) · Up. Addresses (master plan §8): `#today` · `#map` · `#map=E05` · `#concept=E05.02.01` · `#x=layer&y=day[&cell=a|b]` · `#settings` · `#colours`; later `#card=` · `#ep=…&t=` · `#day=`. Back/Forward = browser history (one entry per address); **Up** = parent address (concept → chapter → map → today). **Android Back stays in-app:** the first entry is a base `#today`; Back at home shows "Press Back again to leave" and only a second press within 2 s leaves. Keys (desktop): `/` search, `Esc` back or close; focus always visible. Code: `src/js/05-router.js`, `06-shell.js`.

## 4. Screens (A0)
4.1 **Today** — continue (recent concepts), start here (Part 0, Ch 5), book stats, what's coming. 1 / 2 / 2 / 2–3 / 3 columns by class. Full Today (On the go / Study) = L1.
4.2 **Card, player, 3D viewer** — layouts per §2 table; built in C1 / R1 / V1.
4.3 **Book map** (K1 explorer ported) — three panes in the DOM (tree │ chapter or crosstab │ concept); phone shows the one the address names, tablet portrait + landscape show tree + detail, desktop all three. Search + filters (tier, importance, layer, system, thread, confidence) live in the tree pane. Concept page shows the X1 fields: confidence mark, cited stage (else ≈ stage), NMC AN codes. Crosstabs: any two of chapter, recurs, day, stage, layer, system, tier, importance, thread, confidence; cells list their concepts.
4.4 **Settings** — theme (device/light/dark), storage + save log, backup export/import, testing mode, version line.
4.5 **Colour key** — every D-031 token with pattern + label and its contrast **measured on the device** against the worst of page, card and panel (fill or edge ≥ 3.5:1, label ≥ 4.5:1, accent ring ≥ 3:1, accent text ≥ 4.5:1, control borders ≥ 3:1, heat text ≥ 4.5:1); layout-check enforces the same numbers in both themes.

## 5. Words
All UI words in `content/strings.js` (`STR`). Code never holds UI text.

## 6. Storage, PWA, config
IndexedDB `biostudio` (stores `state`, `answers`, `files`). State record `{schema, rev, app, created, savedAt, settings, last, visited, answers}` — fields only added, back-filled on load (A1, A4). Writes are rev-guarded in one transaction; a stale tab merges first (visited/answers union, newer settings); an unchecked write is stashed and merged next start; save log = last 20 events (Settings). Backup = JSON export/import (merge). Testing mode keeps everything in memory. PWA: `manifest.webmanifest` + `sw.js` (shell cache-first, map network-first; bump `CACHE` with `APP.v`). Settings in `src/js/02-config.js`.

## 7. Debug, testing, checks (RULES I5–I6, C8, C13)
- `?test=1` testing mode: ✎ on every chapter, concept, screen and token → shows id + file and copies a ready "edit this" prompt (`Bio · Fix · <id>`); nothing saved; overlay on (add `&debug=0` to hide it).
- `?debug=1` or `?debug=map,layout,store,router,device,test`: overlay (version, route, ids, fps, state size + rev, device class, viewport, dpr, pointer) and `[area]` console logs; `layout` adds a **Check layout** button. `&boxes` outlines every box.
- `appTests()` (in `src/js/91-tests.js`): device classes, routes ↔ addresses, Up, storage fill/merge, tokens, strings.
- **`tools/layout-check/check.py`** (Playwright, free): §2 matrix × 8 screens × 100/125 % × light/dark → audit (overlap, spill, page wider, clipped controls, tap < `--tap`, text < `--fs-min`, fixed bars over controls), device class + theme per size, rotate keeps place and scroll, in-app tests, real-mode flows (save survives reload, Back at home asks first, malformed address), D-031/D-034 colour re-check; 125 % and dark contact sheets too; report + contact sheets per class in `out/layout-check/`. Flags `--preview` (5 sizes) `--only <screen>` `--debug` `--dry-run`. CI: `.github/workflows/checks.yml` (plus the map dry run); report and sheets are the run's artifact.

## 8. File map (edit points)
`index.html` (shell markup, `?v=`) · `src/css/app.css` (all tokens + layouts) · `src/js/00-version.js` (APP.v) · `01-debug.js` (flags, overlay) · `02-config.js` (settings) · `03-device.js` (classes) · `04-storage.js` (state shape: `stNew`/`stFill`) · `05-router.js` (addresses) · `06-shell.js` (nav, icons, ✎, keys) · `10-today.js` · `11-bookmap.js` (crosstab dims `BM_DIMS`) · `12-settings.js` (+ colour key) · `90-layout-audit.js` · `91-tests.js` · `99-boot.js` · `content/strings.js` · `manifest.webmanifest` · `sw.js` (`CACHE`) · `assets/` icons.
