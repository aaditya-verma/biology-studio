# Design plan — tokens, devices, shell, screens

*(Purpose: the app's design system and screen layouts — tokens, type, spacing, device classes (moved here from master plan §8a), shell, screens, storage, debug and checks. Updated: 20 Nov 2026 · Bio · Fix · Visual style 2 port (§2 Player 16:9 = Lesson preview, D-046). Before: 19 Nov 2026 · Bio · Build · W1 progress map (§2 progress + step rows, §4.7, `?debug=tracker`). Before: S1 studio (Studio row, `?debug=studio`). Before: 19 Nov 2026 · Bio · Build · V1 viewer (v2: 3D viewer §4.6, motion setting, viewer checks); before: A0 shell (v1).)*

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
| Player 16:9 (Lesson) | video on top as a preview (tap → full-screen landscape); transcript + card rail below; labels' terms in the transcript (visual-style §10) | full-bleed video, overlay controls | video on top; transcript + rail below | video │ transcript + rail | video │ transcript + rail |
| Player 9:16 (Short) | full screen | centred; extras behind a button | centred; transcript below | centred; transcript + cards beside | same; never stretched or cropped |
| 3D viewer | full-width canvas; controls in a bottom sheet | full-screen canvas; controls in a side strip | canvas + bottom panel | canvas │ side panel (layers, labels, day) | canvas │ side panel; hover labels, wheel zoom, shortcuts |
| Studio (app, testing mode `#studio`; S1 ✅) | review only: approve / fix line by line | as phone portrait | draft over review | draft │ review | draft │ review │ sources (3 panes) |
| Progress map `#progress` (W1) | map flows top → bottom (lanes = columns); board 1 column; inputs 1 column | map left → right (lanes = rows, scrolls in its frame); board 2 columns | map top → bottom; board 2 columns | map left → right; board 4 columns; inputs 2 columns; ideas │ key | same as tablet landscape, max width ~1280 px |
| Step page `#step=<id>` (W1) | head → facts → prompt, inputs, to-dos | head + prompt │ facts | head → facts → rest | step rail │ page | step rail │ page │ facts (3 panes) |

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
Top bar: Back · brand · breadcrumbs · (testing flag) · Up. Addresses (master plan §8): `#today` · `#map` · `#map=E05` · `#concept=E05.02.01` · `#x=layer&y=day[&cell=a|b]` · `#settings` · `#colours` · `#scene` (3D list) · `#scene=sc-E00.01.04&day=16` · `#day=16` (opens the scene covering that day; V1); later `#card=` · `#ep=…&t=`. Scrubbing the day **replaces** the address (no history flood). Up: scene → 3D list → today. Back/Forward = browser history (one entry per address); **Up** = parent address (concept → chapter → map → today). **Android Back stays in-app:** the first entry is a base `#today`; Back at home shows "Press Back again to leave" and only a second press within 2 s leaves. Keys (desktop): `/` search, `Esc` back or close; focus always visible. Code: `src/js/05-router.js`, `06-shell.js`.

## 4. Screens (A0)
4.1 **Today** — continue (recent concepts), start here (Part 0, Ch 5), book stats, what's coming. 1 / 2 / 2 / 2–3 / 3 columns by class. Full Today (On the go / Study) = L1.
4.2 **Card, player, 3D viewer** — layouts per §2 table; built in C1 / R1 / V1.
4.3 **Book map** (K1 explorer ported) — three panes in the DOM (tree │ chapter or crosstab │ concept); phone shows the one the address names, tablet portrait + landscape show tree + detail, desktop all three. Search + filters (tier, importance, layer, system, thread, confidence) live in the tree pane. Concept page shows the X1 fields: confidence mark, cited stage (else ≈ stage), NMC AN codes. Crosstabs: any two of chapter, recurs, day, stage, layer, system, tier, importance, thread, confidence; cells list their concepts.
4.4 **Settings** — theme (device/light/dark), **motion** (device/reduce/full — reduce: no camera tweens, Play jumps key day to key day; V1, H5), storage + save log, backup export/import, testing mode, version line.
4.5 **Colour key** — every D-031 token with pattern + label and its contrast **measured on the device** against the worst of page, card and panel (fill or edge ≥ 3.5:1, label ≥ 4.5:1, accent ring ≥ 3:1, accent text ≥ 4.5:1, control borders ≥ 3:1, heat text ≥ 4.5:1); layout-check enforces the same numbers in both themes.

4.7 **Progress map** (W1, D-040; data `build/steps.json`, format `tools/tracker/README.md`) — `#progress` Map · `#progress=board` · `#progress=inputs` · `#step=<id>`; reads steps.json, STATUS § Lock, master plan §13 and the backlog live from Pages (sw: network-first for `studio-docs/`), saves nothing. **Map:** HTML boxes on an SVG edge layer, lanes = chat types, depth = longest needs chain; edges routed only through gutters (solid = need met, dashed = waiting); Done hidden by default (toggle), parked ideas as a grey grid below; a scroll hint shows when it is wider than its frame. **Status looks:** colour (good/warn/accent/grey mixes, never a germ-layer token) + pattern + border style + word (`--st-*` tokens); accent ring ◎ = can start now. **Board:** Now · Ready · Blocked · Done. **Your inputs:** open inputs + open owner checks + proposals, oldest first, Copy reply. **Step page:** needs/unblocks chips, gates, owner check, D-ids (GitHub links), last log line, carried to-dos, inputs, ready prompt + chat name with Copy, red "Can't start — needs …" (unmet needs, blocking answers, a lock held by another chat). Not in the learner nav (testing-mode nav only; C1).

4.6 **3D viewer** (V1; format `docs/scene-spec.md`) — one engine + one canvas per session (`src/js/14-scene3d.mjs`, three.js r170 loaded only when a scene opens); a re-render moves the canvas, so rotate/theme keep day, camera, cut and tab. **Stage** = dark island in both themes (`.stage-dark` reuses the dark tokens): canvas, on-structure labels with leader dots (placed to never overlap each other or the overlays; hidden if no room), stamp `Day · CS · ≈size` (status, polite; silent during Play), disclaimers line (first two + `+n more`, opens the list; D-036 (9)), axis gizmo (Cr/Cd, D/V, L/R; cranial in accent), scale bar (round mm length ≤ 130 px; orthographic camera so it holds everywhere). **Panel** = title + id/version + ✎, day row (−1 day · slider with key-day ticks · +1 day · Play), tabs Layers · Cut · View · About (+ Debug); tablet landscape + desktop show every section, no tabs. Layers = toggles with colour + pattern swatch + label (aria-pressed); a "look here" layer (streak + node) is `ctx` + pattern with an accent outline, never an accent fill (D-036 (4)). Cut = labels toggle, cut toggle, cross-section/lengthwise, position. View = 3/4, from the back, from the side, face the cut, reset, zoom. About = summary, cited + marked facts, cards, marks key, three.js + GPU line. Input: drag turn, pinch/wheel zoom, double-tap reset, hover names a structure (mouse); keys `[` `]` day · Space play · arrows turn · `+` `−` zoom · `0` reset · `L` labels · `C` cut. Layouts per §2 table: phone = canvas (≈52 dvh) + bottom sheet; phone landscape = canvas │ strip (36 %); tablet portrait = canvas (≈56 dvh) + panel; tablet landscape + desktop = canvas │ side panel (32 % / 320–380 px), full height. 3D list `#scene` = cards per scene; concept pages link "Open in 3D"; Today › Start here links the colour-key scene. No WebGL → message + facts still readable.

## 5. Words
All UI words in `content/strings.js` (`STR`). Code never holds UI text.

## 6. Storage, PWA, config
IndexedDB `biostudio` (stores `state`, `answers`, `files`). State record `{schema, rev, app, created, savedAt, settings, last, visited, answers}` — fields only added, back-filled on load (A1, A4). Writes are rev-guarded in one transaction; a stale tab merges first (visited/answers union, newer settings); an unchecked write is stashed and merged next start; save log = last 20 events (Settings). Backup = JSON export/import (merge). Testing mode keeps everything in memory. PWA: `manifest.webmanifest` + `sw.js` (shell cache-first, map network-first; bump `CACHE` with `APP.v`). Settings in `src/js/02-config.js`.

## 7. Debug, testing, checks (RULES I5–I6, C8, C13)
- `?test=1` testing mode: ✎ on every chapter, concept, screen and token → shows id + file and copies a ready "edit this" prompt (`Bio · Fix · <id>`); nothing saved; overlay on (add `&debug=0` to hide it).
- `?debug=tracker` (W1): overlay adds steps · fetch ms · issues · lock age; a Debug section on `#progress`/`#step` shows depths, can-start list and the in-page rule check; `tools/tracker/check.py` runs in CI (with `TR_RULES` parity).
- `?debug=studio` (S1): overlay adds card id · status · gate · error/warning counts · edited; console logs loads, card-check counts, gate decisions, exports. Studio itself is testing mode only (`#studio`, `#calib`), saves nothing and exports cards as JSON (D-038); `tools/card-check` (+ `--parity` with the app's rules) and layout-check's Studio flows run in CI.
- `?debug=viewer`: overlay adds scene id, triangles, draw calls, canvas px @ dpr, three.js revision; the viewer gets a **Debug** tab with **Measure fps (~30 s)** (every scene with a slow orbit, then +50k/150k/300k test triangles; avg + 5th-percentile fps per phase; Copy → paste into a chat → pipeline reference §2) and **Bounding boxes** (I5).
- `?debug=1` or `?debug=map,viewer,layout,store,router,device,test`: overlay (version, route, ids, fps, state size + rev, device class, viewport, dpr, pointer) and `[area]` console logs; `layout` adds a **Check layout** button. `&boxes` outlines every box.
- `appTests()` (in `src/js/91-tests.js`): device classes, routes ↔ addresses (incl. scene/day), Up, storage fill/merge (incl. motion), tokens, strings, viewer config.
- **`tools/scene-check/check.py`** (C3): every scene vs `docs/scene-spec.md` (ids, keys, tokens only, labels ≤ 3 words, cites + marks, stamp size vs geometry ±15 %, debug off, cards in map.json). **`tools/stills/stills.py`** (C11): renders each scene's `stills` days in still mode (`?still=1`, 960×540, dpr 1, SwiftShader) and compares the WebGL pixels with `tools/stills/baseline/` (mean < 0.5, < 0.05 % pixels off); triangle budget; look sheet `out/stills/contact-look.png`; `--update` after review. Both run in CI (Playwright pinned 1.63.0 = the baselines' Chromium).
- **`tools/layout-check/check.py`** (Playwright, free): §2 matrix × 11 screens (V1 adds `scenes`, `viewer`, `viewer-axes`) × 100/125 % × light/dark → audit (overlap, spill, page wider, clipped controls, tap < `--tap`, text < `--fs-min`, fixed bars over controls), device class + theme per size, rotate keeps place and scroll (+ viewer: day, camera, tab), in-app tests, real-mode flows (save survives reload, Back at home asks first, malformed address), D-031/D-034 colour re-check; 125 % and dark contact sheets too; report + contact sheets per class in `out/layout-check/`. Flags `--preview` (5 sizes) `--only <screen>` `--debug` `--dry-run`. CI: `.github/workflows/checks.yml` (plus the map dry run); report and sheets are the run's artifact.

## 8. File map (edit points)
`index.html` (shell markup, `?v=`) · `src/css/app.css` (all tokens + layouts) · `src/js/00-version.js` (APP.v) · `01-debug.js` (flags, overlay) · `02-config.js` (settings) · `03-device.js` (classes) · `04-storage.js` (state shape: `stNew`/`stFill`) · `05-router.js` (addresses) · `06-shell.js` (nav, icons, ✎, keys) · `10-today.js` · `11-bookmap.js` (crosstab dims `BM_DIMS`) · `12-settings.js` (+ colour key, motion) · `13-viewer.js` (3D screen, panel, overlay, input, Measure) · `17-tracker.js` (progress map: `TR_RULES` = check.py's, `TR_SIZE`, views) · `14-scene3d.mjs` (engine: geometry, tokens → patterns, lights `// EDIT:`) · `lib/three-r170/` (vendored, MIT) · `content/E/scenes/` (scene files + `index.json`) · `90-layout-audit.js` · `91-tests.js` · `99-boot.js` · `content/strings.js` · `manifest.webmanifest` · `sw.js` (`CACHE`) · `assets/` icons.
