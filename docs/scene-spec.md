# Scene spec — the one definition of a 3D scene (RULES C2)

*(Purpose: the scene file format that drives the 3D viewer, stills, the card drills and (later) video shots — one scene, four outputs (D-006). Updated: 25 Nov 2026 · Bio · Episode · S1E01 animatic (§8 video overlays follow visual-style §1/§10 bands; §10 `overlay` derived row (M1b.q10 = B, D-103, D-104)). Before: 21 Nov 2026 · Bio · Fix · L1 polish (`camera.phone` start framing, §7 placement: axis arrows + pins are obstacles, pinned labels first; §8a drill framing keeps the subject + ruler clear of the overlays; D-056). Before: 21 Nov 2026 · Bio · Build · V2 3D drills (`views`, per-key `fit_mm`, `notochord` part, disc `meso_midline_gap` + `streak_scale`, anchor list §7, what drills need §11; D-054). Before: 20 Nov 2026 · Bio · Fix · Visual style 2 port — §10 video shot-sheet fields, segments.json, endstate.json (D-046; spec only, no code yet). Before: 18 Nov 2026 · Bio · Build · V1 viewer. Seeded from the M1 kit's `tools/m1-bakeoff/shot.json` v2 + `common/scene_math.py`. Change this spec first, then the code (`src/js/14-scene3d.mjs`, `tools/scene-check`). Updated: 22 Nov 2026 · Bio · Build · V3 trace a cell (`tracer` part — a marked cell's path keyed by day; drill-only layers `drill: true`; anchor `tracer-<id>`; §8a trace; §9 path checks; D-075).)*

## 1. Where scenes live
- One JSON file per scene: `content/<book>/scenes/<id>.json`; the list is `content/<book>/scenes/index.json` (`{"spec":1,"scenes":[{"id","title","summary","cards","days":[first,last]}]}`).
- Id: `sc-<card id>` or `sc-<episode>-<shot>` (README). **Permanent once shipped (A2)** — fix the file, bump `version`, never renumber.
- Addresses: `#scene` (list) · `#scene=<id>` · `#scene=<id>&day=<d>` · `#day=<d>` (opens the first scene whose days include `d`).
- Checked by `tools/scene-check` (C3) and `tools/stills` (C11) before anything ships.

## 2. Space, units, time (fixed for every embryo scene)
- **Units:** `units.mm_per_unit` (0.1 → 1 unit = 0.1 mm, as the M1 shot). The scale bar is computed from this; the stamp size comes from the cited day key — scene-check makes them agree (±15 %).
- **Axes:** `+x` cranial · `−x` caudal · `+y` the embryo's left · `−y` its right · `+z` dorsal · `−z` ventral (right-handed; same as `shot.json`). Every scene shows the axis gizmo (H4).
- **Days:** book days after fertilization (B6; dossier §1). `days[]` = keyframes, strictly ascending, ≥ 1. Between keys every parameter is eased (smoothstep) from one key to the next. The scrubber runs from the first to the last key.

## 3. Fields
| Field | Type | Rule |
|---|---|---|
| `spec` | 1 | this spec's version |
| `id` | string | = file name; pattern `sc-…` |
| `version` | int ≥ 1 | bump on every change (H7) |
| `book` | `"E"` | book code |
| `cards` | [concept id] | the cards this scene serves (≥ 1; must exist in `map.json`) |
| `title`, `summary` | string | our words, short (G2) |
| `units` | `{mm_per_unit}` | see §2 |
| `days` | [key] | see §4 |
| `start_day` | number | first day shown (default: first key) |
| `layers` | [layer] | see §5 — everything that can be toggled |
| `parts` | [part] | geometry, see §6 |
| `labels` | [label] | on-structure labels (D8), see §7 |
| `facts` | [{text, cite, mark}] | what the scene shows, in our words, cited to a book section (+ registry sources) and marked (B1, B6–B7); shown under **About** |
| `terms` | [{term, text}] | optional: definitions/conventions with no book section (e.g. anatomical planes) — shown under About as *Terms* (from GLOSSARY), never as facts, no mark |
| `camera` | `{azimuth_deg, elevation_deg, fit_mm, phone?:{zoom, shift, pan}}` | start view; orthographic so the scale bar is exact everywhere. Optional `phone` (L1F): the framing on phone portrait, where the stage is short and the stamp + notes plate cover its top — `zoom` 1–4 (× the fit; the start zoom, until the learner zooms), `shift` 0–0.3 (moves the subject down by that share of the stage height) and `pan` −0.3…0.3 (+ moves it left, by that share of the width) — shift and pan apply whenever the scene shows on phone portrait. *Reset view* / double-tap go back to the phone zoom. Other classes ignore it |
| `views` | [{id, label, azimuth_deg, elevation_deg}] | optional named views (≤ 3-word `label`) — targets for `rotate` drills and `show.view` (card-spec §2a); ids unique, `elevation_deg` −89…89. Azimuth: 0 = camera on the cranial side, 90 = on the left, 180 = caudal, −90 = right (§2 axes) |
| `cut` | `{axis:"x"\|"y", at, on}` | cut plane: `y` = lengthwise (keeps `y ≥ at·half-width`), `x` = cross-section (keeps `x ≥ at·half-length`); `at` −0.9…0.9 |
| `disclaimers` | [string] | deliberate distortions, always on screen (B2): e.g. "colours illustrative", "layer thickness not to scale" |
| `stills` | [day] | days `tools/stills` renders and compares (C11); default = every key |
| `debug` | bool | `true` draws world axes + bounding boxes (I5); **must be false in shipped scenes** (scene-check) |

## 4. Day keys
`{"day":15, "stage":"CS06", "size_mm":0.2, "cite":"E06.06 Tbl 6.4 · R06 CS6", "mark":"✔✔", "params":{…}}`
- `stage` = Carnegie stage at that day (`CS01`–`CS23`). **On a key day** the stamp shows that key's stage and cited size. **Between keys** it shows the day span (`Day 17–18`, or the whole day), both stages (`CS06–07` — stages are defined by form and their day ranges overlap, dossier §1) and the eased size, never a key's mark (G-Sci, V1).
- `size_mm` + `cite` + `mark` are required (B2, B7). The on-screen size always shows **≈** (sizes differ by source — dossier §1); a key with `mark` `≈` is shown as uncited.
- `params` = the numbers the parts read at that day (§6). Missing params carry over from the previous key.
- Optional **`fit_mm`** on a key: the camera's fit (mm across the short side of the stage) at that day, eased between keys like a param — for a scene whose embryo grows a lot, so the subject stays framed; the scale bar follows it (orthographic, exact). Missing = `camera.fit_mm`. Drills and stills use it too.

## 5. Layers (toggles)
`{"id":"epiblast", "token":"epi", "label":"Epiblast", "opacity":0.5, "on":true, "ring":false}`
- `token` ∈ `epi hypo ecto meso endo crest ctx` (germ layers, B3 — fill, edge, pattern and label text all come from the CSS tokens in `src/css/app.css`; the pattern is fixed per token, design plan §1) · `guide` (axes, planes, ruler: neutral ink, never a layer colour). **No `accent` token:** the accent is never a fill (B3); a "look here" structure gets `"ring": true` — its edges draw in the accent, its fill stays a layer/`ctx` token with pattern (D-036; e.g. streak + node = `ctx` + ring).
- **No colour values in scene files** (B3; scene-check rejects any `#rgb`).
- `opacity` 0.2–1 (translucent layers keep their pattern); `on` = shown at start (default true).
- `drill: true` (V3, D-075) = a **drill-only** layer: what it draws shows only while a card drill names it (today: a `tracer`'s marked cell) — no toggle in Layers, never in Try it, stills or video; its token is `ctx` with `ring: true` (the accent ring, B3).

## 6. Parts (geometry kinds the viewer knows)
| `kind` | Draws | Options | Reads `params` |
|---|---|---|---|
| `disc` | the embryonic disc as stacked layer slabs (M1 geometry: outline → clipped prisms); the streak is a groove sunk into the epiblast, the node a small raised knob at its cranial end [E05.01] | `layers` map (`epiblast`, `hypoblast`, `mesoderm`, `endoderm`, `streak`, `node` → layer ids), `epiblast_thick`, `gap`, `hypoblast_thick` (units), `segments`, `streak{start_frac,width,height}`, `node{radius,height}`, `meso_delay`, `endo_delay` (0–1 of each key-to-key step), `meso_midline_gap` (units, optional: the mesoderm sheet stops this far each side of the midline — where the notochord runs; default 0) | `length_units`, `width_ratio`, `pear` (0 round → 0.35 pear, broad end cranial), `tip_frac` (streak tip as fraction of length from the caudal end; 0 = no streak), `meso`, `endo` (spread 0–1), `streak_scale` (0.5–4, default 1: widens the groove, edges and node so the streak still reads when the disc is large — V1 note, day 18) |
| `notochord` | the midline axial cells from the node forward: **prenotochordal cells** (a thin strand between epiblast and endoderm) → **notochordal plate** (flat, within the endoderm) → **notochord** (a solid rod, lifted off the endoderm, under the epiblast) [E05.02]; a lofted tube whose cross-section changes along its length, cranial end first (the book's order, D-029); plus the **prechordal plate**, a small flat body in the endoderm layer at the cranial end. Needs a `disc` part (reads its node + outline) | `layers` map (`notochord`, `prechordal` → layer ids), `radius` (rod, units), `plate_half_width` (units), `prechordal{at_frac, radius_frac}` (from the caudal end, of the disc length), `zone` (0.02–0.4: length of each change, as a fraction of node → prechordal), `rings` (sections along the length) | `noto` (0–1: how far the cells have reached from the node toward the prechordal plate), `noto_plate` (0–1: share of node → prechordal, from the cranial end, that is plate or rod), `noto_rod` (0–1, ≤ `noto_plate`: share that is a rod) |
| `tracer` | **one marked cell moving along a path** — for a `trace` drill (card-spec §2a): a small sphere, fill = its layer's `ctx` token + pattern, an accent ring (B3), drawn over the tissue so it never hides inside a layer; while it is drawn, other `ring` layers lose their accent ring (the accent is the cell's alone, B3); its depth on screen comes from where it sits in the stack (best on a lengthwise cut). Drawn **only while a trace drill names it** (its layer must be `drill: true`) — the path is the answer. Needs a `disc` part before it (reads its outline, layer depths, streak) | `id` (unique, `t-…`), `layer`, `radius_mm` (0.002–0.02, the cell's true-ish size), `min_px` (4–12: drawn at least this radius on screen so it reads on a phone — then the drill adds `disclaimer`), `disclaimer` (e.g. "marked cell drawn larger"; shown first in the notes while the cell is drawn, B2), `path` [{`day`, `x`, `y`, `in`}] ≥ 2 keys: `day` strictly ascending inside the scene's days; `x` −1…1 = share of the disc's half-length (+ cranial), `y` −1…1 = share of its half-width (+ left) — so the cell keeps its place as the disc grows; `in` ∈ `epiblast` · `streak` (going in: just below the epiblast, under the groove) · `mesoderm` · `endoderm` = the layer it is in at that day (depth = the middle of that slab). Between keys x, y and depth ease (smoothstep); before the first key / after the last it stays put | — (its own `path`; reads the disc's params for depths and extents) |
| `axes` | arrows from the disc centre, tips labelled Cranial/Caudal, Dorsal/Ventral, Left/Right | `layer`, `length_mm` | — |
| `planes` | translucent sagittal / transverse / frontal planes with labels | `planes:[{id, normal:"x"\|"y"\|"z", layer}]`, `size_mm` | — |
| `ruler` | a flat ruler beside the disc with ticks | `layer`, `length_mm`, `tick_mm`, `at:[x,y]` (units) | — |
| *(runtime only)* | the Measure benchmark adds a test mesh through the engine (`setStress`); never in a scene file | — | — |

New kinds are added here first (C2), then in `src/js/14-scene3d.mjs`.

## 7. Labels (D8: labels sit on their structure; ≤ 3 words)
**Anchors** (what `labels[].at` and drill `pins[].at` may name): `disc` → its mapped pieces `epiblast` `hypoblast` `mesoderm` `endoderm` `streak` `node`; `notochord` → `noto-cord` `noto-plate` `notochord` `prechordal`; `axes` → `axis-cranial` … `axis-ventral`; `planes` → `plane-<id>`; `ruler` → `ruler`; `tracer` → `tracer-<id>` (the cell; only while drawn — its label *Marked cell* is the one label a trace drill keeps, with the ruler's). An anchor exists only while its piece is drawn at that day (e.g. no `notochord` before `noto_rod` > 0). The viewer hides a label whose structure is behind an opaque piece of another layer (translucent layers — opacity < 0.6 — never hide), whose structure is off the stage, or whose leader would cross another leader or label; with a cross-section on, only the notochord stage on the cut face is labelled (V2). In a drill, labels are off except the ruler's length; pins sit beside their structure with a leader + dot. **Placement order (L1F):** the stamp, notes plate, gizmo, scale bar and the **axis arrows** are obstacles — no label or pin sits on them; drill pins are placed first, each in the first free spot around its structure (never under an overlay or another pin); once a `label` drill is answered, the labels of the pinned structures are placed next, each **beside its pin** (no second leader), then the rest by `priority`.
`{"layer":"mesoderm", "text":"Mesoderm", "days":[15.5,17], "priority":1, "at":"node"}` — `at` = the anchor (a disc piece, `axis-<dir>`, `plane-<id>`, `ruler`; default = the layer id); `priority` 1 = the lesson's subject, placed first so small screens drop context labels, not the subject. Anchored on the structure (the cut face when the cut reaches it, else the rim facing the camera); shown only while its layer is on and the day is in `days`. Labels never cover each other (the viewer stacks them) and keep their leader dot. Desktop: hovering a structure shows its label even with labels off.

## 8. Always on screen (B2, H4)
Day/stage/size stamp (`Day 16 · CS06–07 · ≈0.3 mm`; announced politely, but silent while Play runs) · scale bar (nice length, from `mm_per_unit` and the zoom) · axis gizmo (Cr/Cd, D/V, L/R) · disclaimers: one always-visible line with the first two (put the visual distortions first: colours, thickness) + `+n more` — on a stage under 300 px tall (small phones, phone landscape) the first one + `+n more` (L1F) — which opens the full list (closed by default on every class so it never covers the embryo; the full list is also under About) — D-036 (9). These are drawn by the viewer, never by the scene, and cannot be turned off.

**In video** (shot sheets, §10) the same overlays are drawn by the render/animatic overlay, placed by the frame bands in `build/visual-style.md` — Short (9:16, §1): axes + scale bar + honesty/media tag in the top-left block (28–37.5 %), captions 68–72 % bottom-anchored at 72 %, on host and anatomy shots alike (M1b.q10 = B, D-103); Lesson (16:9, §10): bottom-left stack above 84 %, captions 85–95 %, and the stack never overlaps the named structure or its accent ring, also at 375×211. A shot never places them itself.

## 8a. What a scene exposes for card drills (card-spec §2a, V2)
- **State from a `show`:** `{day, view, zoom, cut, layers}` → the engine's `setScene(S, state)` (day eased as §2; `view` from `views` or angles). Labels are off; the stamp, scale bar, gizmo and disclaimers stay — except during a `day` drill, where the stamp reads **Day ? · stage ? · size ?** until it is answered (D-054).
- **Named views** (`views`, §3) for `rotate` targets; the viewer reports the angle between the live view and a target (camera rotation, so screen roll counts).
- **Framing (L1F):** a drill on a scene with a `ruler` part opens framed so the embryo and the whole ruler sit inside the stage, clear of the stamp, notes plate, gizmo and scale bar; a `label` drill opens framed so its pinned structures (with room for their pins) sit in that free band. The viewer zooms (in at most ×2.5, `CONFIG.viewer.frame.maxIn`) and moves the subject down or up; a pinned label with no room beside its pin goes to the nearest free spot carrying the pin's number, and if the stage has no room at all (smallest landscape phones, 125 % text) the Check feedback names it (*Pin 3: …*); *Start view* and double-tap return to that framing.
- **Anchors** (§7) for `label` pins — projected to the screen every frame; a pin whose piece is not drawn at its `show` fails the in-app drill test (layout-check).
- **Stills** (`frames`, `folded`, the `rotate` target): the one engine renders a `show` to an image (no labels) with its scale bar; the live view is put back after. A cross-section `cut` may add `slab_mm`: only a slice that thick beyond the cut is drawn, so the still shows the section face alone (G-Sci V2: the tissue behind a cut must not read as part of it). With a cross-section on, only the notochord stage on the cut face is labelled.
- **Trace (V3, D-075):** a `trace` drill's state adds `trace: <tracer id>` → the engine draws that cell at the current day (`traceAt(scene, id, day)` → position + the layer it is in, shared by the viewer, tests and scene-check). The drill panel adds the day row; Play / ◀ ▶ run and step over the path's key days (reduced motion: key to key). The stamp stays (B2); labels are off but the cell's own label.
- Every scene used by a drill keeps `cards` listing that card (W-scene-cards).

## 9. Budgets + checks
- Phone budget (H8): ≤ 150k triangles, ≥ 30 fps — `tools/stills` reports triangles and draw calls per still; `?debug=viewer` shows them live and has **Measure fps**.
- `tools/scene-check` (C3): `tracer` parts (V3: id unique `t-…`, layer is `drill: true` with token `ctx` + `ring`, a `disc` before it, `radius_mm` / `min_px` in range, a `disclaimer` when `min_px` is set, ≥ 2 path keys ascending inside the scene's days, `in` known, the first key `in` = `epiblast`, every key inside the disc outline at its day, a `streak` key on the streak drawn at that day, and — sampled every 0.05 day — the cell inside the `mesoderm` / `endoderm` sheet whenever both keys around it say so: the path never runs ahead of the tissue), `views` (ids unique, angles in range, labels ≤ 3 words), per-key `fit_mm` > 0, the `notochord` part (needs a `disc`, params 0–1, `noto_rod` ≤ `noto_plate`), required fields, param ranges (0–1; `length_units`, `fit_mm` > 0), no `accent` fill, id = file name, ascending day keys with stage + size + cite + mark, tokens only (no colours), labels/parts point at real layers, cards exist in the map, stamp size vs geometry (±15 %), `debug` false, `stills` days inside the range.
- `tools/stills` (C11): renders every scene at its `stills` days (fixed 960×540 canvas, labels off) and compares with `tools/stills/baseline/`; a difference must be intended (`--update` after review).

## 10. Video shot sheet + series files (D-046 — spec only; code and checks come with P1/R1)
Look rules: `build/visual-style.md` §10–§16. Each shot in an episode's shot sheet points at one scene (`scene`, `day`) and adds:
| Field | Type | Rule |
|---|---|---|
| `mode` | `"layer"` \| `"segment"` | colour mode for the whole shot, never mixed (§11), except the `--g-crest` overlay ring and the fertilisation chromosome tints; `segment` needs `organ` (an id in `content/E/segments.json`) and shows the legend chip |
| `cam_short`, `cam_lesson` | camera (as §3 `camera`) | same scene state, two framings (9:16 Short, 16:9 Lesson, §10); never re-model for a format |
| `labels[]` | as §7 + `chip` (token) | leader-line labels (§12): ≤ 3 on screen (Short), ≤ 6 (Lesson); GLOSSARY terms |
| `media[]` | `{id, kind, from_s, to_s, overlay}` | non-3D items (§13); `id` = a registry § Media row (`M01`…); `kind` ∈ `diagram microscopy ultrasound xray ct mri footage host`; a missing ledger row fails the check |
| `exaggerations[]` | `{what, how_much, why, exam_fact}` | §15; the honesty tag shown comes from this list; `exam_fact: true` → the voice says so |
| `tag` | one of the §15 fixed honesty tags \| null | shown for the whole shot |
| `clinical` | bool | shot is part of a "Clinical link" slot (§14; Lessons only) |
| `overlay` | `"short"` \| `"lesson"` — **derived, read-only** (from the camera used; never written in a sheet) | which band layout the overlay uses. scene-check (P1/R1) tests the **anchor + label box** of each named structure at its first label: inside 38–64 % on `cam_short` and not overlapping the axes/scale or tag boxes. A close-up may bleed left/right when the anchor is ≥ 6 % inside the frame and left of the 14 % rail, flagged `deliberate_crop` (D-104) |

**Segments file** `content/E/segments.json`: `{spec, book, organs:[{id, name, cite, mark, segments:[{id, name, token, pattern, cite, mark, derivatives:[{id, name, cite, mark, split:"light"|"dark"|null, merge_into:<segment id>|null, day}]}]}]}` — ≤ 6 segments per organ; `token` names a CSS var `--s-<organ>-<seg>` (no colour values in the file, B3); `day` = when the split or merge happens (checked against the scene's day keys); segment and derivative ids permanent (A2).

**End state** `endstate.json` per Part (next to its shot sheet): `{part, scene, day, camera, mode, organ, visible:[layer, segment or derivative ids], recap_facts:[fact ids]}` = the last frame + the facts the next Part's recap may use. Part N+1's first shot must match it (G-Sci item 18; the render check diffs it).
