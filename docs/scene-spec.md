# Scene spec — the one definition of a 3D scene (RULES C2)

*(Purpose: the scene file format that drives the 3D viewer, stills and (later) video shots — one scene, three outputs (D-006). Updated: 18 Nov 2026 · Bio · Build · V1 viewer. Seeded from the M1 kit's `tools/m1-bakeoff/shot.json` v2 + `common/scene_math.py`. Change this spec first, then the code (`src/js/14-scene3d.mjs`, `tools/scene-check`).)*

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
| `camera` | `{azimuth_deg, elevation_deg, fit_mm}` | start view; orthographic so the scale bar is exact everywhere |
| `cut` | `{axis:"x"\|"y", at, on}` | cut plane: `y` = lengthwise (keeps `y ≥ at·half-width`), `x` = cross-section (keeps `x ≥ at·half-length`); `at` −0.9…0.9 |
| `disclaimers` | [string] | deliberate distortions, always on screen (B2): e.g. "colours illustrative", "layer thickness not to scale" |
| `stills` | [day] | days `tools/stills` renders and compares (C11); default = every key |
| `debug` | bool | `true` draws world axes + bounding boxes (I5); **must be false in shipped scenes** (scene-check) |

## 4. Day keys
`{"day":15, "stage":"CS06", "size_mm":0.2, "cite":"E06.06 Tbl 6.4 · R06 CS6", "mark":"✔✔", "params":{…}}`
- `stage` = Carnegie stage at that day (`CS01`–`CS23`). **On a key day** the stamp shows that key's stage and cited size. **Between keys** it shows the day span (`Day 17–18`, or the whole day), both stages (`CS06–07` — stages are defined by form and their day ranges overlap, dossier §1) and the eased size, never a key's mark (G-Sci, V1).
- `size_mm` + `cite` + `mark` are required (B2, B7). The on-screen size always shows **≈** (sizes differ by source — dossier §1); a key with `mark` `≈` is shown as uncited.
- `params` = the numbers the parts read at that day (§6). Missing params carry over from the previous key.

## 5. Layers (toggles)
`{"id":"epiblast", "token":"epi", "label":"Epiblast", "opacity":0.5, "on":true, "ring":false}`
- `token` ∈ `epi hypo ecto meso endo crest ctx` (germ layers, B3 — fill, edge, pattern and label text all come from the CSS tokens in `src/css/app.css`; the pattern is fixed per token, design plan §1) · `guide` (axes, planes, ruler: neutral ink, never a layer colour). **No `accent` token:** the accent is never a fill (B3); a "look here" structure gets `"ring": true` — its edges draw in the accent, its fill stays a layer/`ctx` token with pattern (D-036; e.g. streak + node = `ctx` + ring).
- **No colour values in scene files** (B3; scene-check rejects any `#rgb`).
- `opacity` 0.2–1 (translucent layers keep their pattern); `on` = shown at start (default true).

## 6. Parts (geometry kinds the viewer knows)
| `kind` | Draws | Options | Reads `params` |
|---|---|---|---|
| `disc` | the embryonic disc as stacked layer slabs (M1 geometry: outline → clipped prisms); the streak is a groove sunk into the epiblast, the node a small raised knob at its cranial end [E05.01] | `layers` map (`epiblast`, `hypoblast`, `mesoderm`, `endoderm`, `streak`, `node` → layer ids), `epiblast_thick`, `gap`, `hypoblast_thick` (units), `segments`, `streak{start_frac,width,height}`, `node{radius,height}`, `meso_delay`, `endo_delay` (0–1 of each key-to-key step) | `length_units`, `width_ratio`, `pear` (0 round → 0.35 pear, broad end cranial), `tip_frac` (streak tip as fraction of length from the caudal end; 0 = no streak), `meso`, `endo` (spread 0–1) |
| `axes` | arrows from the disc centre, tips labelled Cranial/Caudal, Dorsal/Ventral, Left/Right | `layer`, `length_mm` | — |
| `planes` | translucent sagittal / transverse / frontal planes with labels | `planes:[{id, normal:"x"\|"y"\|"z", layer}]`, `size_mm` | — |
| `ruler` | a flat ruler beside the disc with ticks | `layer`, `length_mm`, `tick_mm`, `at:[x,y]` (units) | — |
| *(runtime only)* | the Measure benchmark adds a test mesh through the engine (`setStress`); never in a scene file | — | — |

New kinds are added here first (C2), then in `src/js/14-scene3d.mjs`.

## 7. Labels (D8: labels sit on their structure; ≤ 3 words)
`{"layer":"mesoderm", "text":"Mesoderm", "days":[15.5,17], "priority":1, "at":"node"}` — `at` = the anchor (a disc piece, `axis-<dir>`, `plane-<id>`, `ruler`; default = the layer id); `priority` 1 = the lesson's subject, placed first so small screens drop context labels, not the subject. Anchored on the structure (the cut face when the cut reaches it, else the rim facing the camera); shown only while its layer is on and the day is in `days`. Labels never cover each other (the viewer stacks them) and keep their leader dot. Desktop: hovering a structure shows its label even with labels off.

## 8. Always on screen (B2, H4)
Day/stage/size stamp (`Day 16 · CS06–07 · ≈0.3 mm`; announced politely, but silent while Play runs) · scale bar (nice length, from `mm_per_unit` and the zoom) · axis gizmo (Cr/Cd, D/V, L/R) · disclaimers: one always-visible line with the first two (put the visual distortions first: colours, thickness) + `+n more`, which opens the full list (closed by default on every class so it never covers the embryo; the full list is also under About) — D-036 (9). These are drawn by the viewer, never by the scene, and cannot be turned off.

## 9. Budgets + checks
- Phone budget (H8): ≤ 150k triangles, ≥ 30 fps — `tools/stills` reports triangles and draw calls per still; `?debug=viewer` shows them live and has **Measure fps**.
- `tools/scene-check` (C3): required fields, param ranges (0–1; `length_units`, `fit_mm` > 0), no `accent` fill, id = file name, ascending day keys with stage + size + cite + mark, tokens only (no colours), labels/parts point at real layers, cards exist in the map, stamp size vs geometry (±15 %), `debug` false, `stills` days inside the range.
- `tools/stills` (C11): renders every scene at its `stills` days (fixed 960×540 canvas, labels off) and compares with `tools/stills/baseline/`; a difference must be intended (`--update` after review).
