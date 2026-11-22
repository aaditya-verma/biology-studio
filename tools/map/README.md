# tools/map — K1 concept map builder

Purpose: turns `concepts.txt` (our concept rows) + `research.txt` (X1 layer: AN codes, marks, cited stages per concept) + `links.txt` (K2: cited becomes / defect links) + I1 index (`content/E/index/`) into `content/E/map.json`, `curriculum/concept-map.md` and `curriculum/roadmap.md`. Owner doc: `build/master-plan.md` §5; **map.json fields: § Map data below (owner of the format, RULES C2)**. Updated: 22 Nov 2026 · Bio · Build · K2 map data (§ Map data: links, ring, wedge, side, layout; `layout.py`, `links.txt`, `--selftest`, `--preview`). Before: 22 Nov 2026 · Bio · Research · X1 Ch 11 (E11 rows in research.txt: muscle AN codes AN3/4.1/7.4–7.5/24.4/28.1/31.1/45.3/67.2/74.4/79.4, cs from human specimens — 9–23 muscle origin, 14–22 fibres + limb muscle, 15–18 frontier, 15–20 epaxial/hypaxial, 16–21 head). Before: 21 Nov 2026 · Bio · Research · X1 Ch 10 (E10 rows in research.txt: axial AN codes AN2/21/26/35.9/50/53.4/74.4/79.4–79.5, cs 10–23 on the vertebra and 14–23 on the disc from human specimens). Before: X1 Ch 09 (E09 rows in research.txt: AN79.5/79.6 + AN81 codes, cs 7–23 on the teratogenic window only). Before: X1 Ch 08 (E08 rows: AN80 codes + marks, cs blank for the fetal period). Before: X1 Ch 07 (E07 rows; septtr/diaphragm definitions fixed, D-043 c).

Run from this folder (Python 3, no packages):
```
python build_map.py --dry-run --debug     # checks only (ids, prereqs, cycles, coverage, links, layout, overlaps)
python build_map.py --selftest            # K2: determinism (2 runs, byte-identical), no overlaps, every becomes/defect cite, every concept placed
python build_map.py --dry-run --preview --out out   # K2: out/map-preview.svg — contact sheet (rings + side, light + dark) for G-Art
python build_map.py --out out             # writes out/map.json, out/concept-map.md, out/map-report.json
python roadmap.py                         # reads out/map.json, writes out/roadmap.md
```
Then copy `out/map.json` to `content/E/map.json` and the two .md files to `studio-docs/curriculum/`, commit (setup guide §6a), and republish the explorer (needs `map.json` beside `explorer/index.html`).
Flags: `--dry-run --debug --only E05 --preview --selftest` (RULES I5; `--only` limits the md, `--preview` writes the K2 contact sheet). Edit points: rows in `concepts.txt` (add at the END of a section — ids are permanent, A2); per-chapter X1 rows in `research.txt` (`id|AN codes|mark|cs` → additive fields `an`, `mark`, `cs`, `x1` in map.json; the dossier owns the facts); vocab and manual term links marked `# EDIT:` in `build_map.py`; cited links in `links.txt`; layout numbers in `layout.py` `LAYOUT` (bump `version`); seasons in `roadmap.py`.
`roadmap.py` runs from the folder that holds `out/map.json`.
Explorer page: explorer/index.html (published at https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin with map.json beside it).

## Map data — K2 fields in `content/E/map.json` (D-071, spec; RULES C2: change this first, then the code)

**Rules.** Fields are only **added**, never renamed; old fields keep their meaning (A1, A4). Ids are permanent (A2). Same input = same output, byte for byte (fixed seed; `--selftest` builds twice and compares sha256). The phone does no layout work (H8): K3/K4 only draw these numbers. `schema` stays `biostudio.map/1`.

**Per concept (all 314 get every field):**
| Field | Meaning |
|---|---|
| `links.needs` | = `prereq` (learn first). Same list, kept beside the other links for the panel. |
| `links.unlocks` | = `unlocks` (direct dependants — comes next). |
| `links.back_in` | **Comes back in:** the same thread in a **later chapter** — concepts in later chapters that share a thread letter (T G F S M C A) **and** are linked (any dependant — direct or further down the prerequisite chain — or a shared glossary term); best one per chapter (score = shared terms + 2 if a dependant; ties → lower id), nearest chapter first, at most 6. Derived, not cited. |
| `links.becomes` | **Becomes… (adult structure, D4):** `[{to, cite}]` — `to` = the adult structure in our words; `cite` = `{doc, line, anchor}`: the dossier line that states it. **Only where a dossier states it, never guessed** (D-071 f). |
| `links.defect` | **Goes wrong as… (birth defect):** `[{to, cite}]` — `to` = the defect concept id (system `defects`); `cite` as above. |
| `ring` | `{r, r_day, band, day, src}` — `r` = drawn radius (0 centre … 1 edge); `r_day` = the exact radius of `day` on the day scale; `band` = the stage band (`cs1`…`cs23`, `fetal0`–`fetal2`, `rim`, `toolkit`); `day` = placement day after fertilization; `src` = where `day` came from: `day` (own day), `cs` (cited Carnegie stage → its first day), `from:<id>` (a defect: the start of its sensitive period = earliest start day among the concepts that cite it; if none of them has a day, the defect's own day/stage, else `none`), `none` (no day yet → the rim band, `day` null — never guessed from a section or chapter median, G-Art), `toolkit`. |
| `wedge` | `{sys, a}` — `sys` = wedge (the System column; a defect concept takes the system of the first citing concept — lowest id — whose system is an organ, i.e. not ori · mol · defects · early · gam · plac; else of its first such prerequisite; else `defects`; E00 + E01 = `toolkit`); `a` = the dot's angle in degrees (0 = right, clockwise, SVG y down), given **inside its wedge's range [a0, a1]** (so it may exceed 180). |
| `pos` | `{x, y}` — the dot's centre, normalised (−1…1; `x` right, `y` down). |
| `side` | `{h}` — Side view: cone height = `r_day` (0 = apex = Toolkit … top = term); **null** for no-day dots (K4 draws them on a shelf above Birth, never as late fetal). The cone's ground position is `pos` (`x` → x, `y` → z). |
| `shape` | `defect` (◆, a cited defect concept) or `dot`. |

`cite.line` is found by `build_map.py` from `links.txt` (the **one** line in the dossier that contains `anchor`); 0 or 2+ matches stop the build, so an edited dossier can't leave a stale cite.

**Top-level `layout` block:** `hash` (16 hex: fingerprint of every position and band — changes whenever an X1 moves dots; K3/K4 key caches on it), `version` (bump when the layout *rule* changes) (1), `seed` (71), `phone` (`px` 360, `dot_zoom` 1.5, `edge_px` 12, `dot_px` 8, `gap_px` 2, `min_center` 0.0388 — normalised centre-to-centre minimum), `scale` (`toolkit_r`, `band_r`, `base_t`, `pack`, `rim_gap`, `term_day`, the rule, `bands` = `[{key, lo, hi, r0, r1, n}]`, `breakpoints` = `[[first day, r0]]` + `[term, end of fetal2]`), `wedges` (`order`, `deg` = `{sys: [a0, a1]}`, `edge_px`, rule), `rings` (guide circles at each week's **first day** on the exact day radius: Wk 1 (day 1) · Wk 2 (8) · Wk 3 (15) · Wk 4 (22) · Wk 5 (29) · Wk 6 (36) · Wk 7 (43) · Wk 8 (50) · Birth (266), + *No day yet* at the rim band), `toolkit` (E00, E01).

**Day scale (rings).** One monotonic scale for the whole map. Toolkit (E00 + E01, no day) sits inside `toolkit_r` 0.16 at the centre. Then a band per Carnegie stage **CS1–CS23** (days 1–60), three fetal bands (days 61–90, 91–180, 181–266) and a rim band for "no day". A band is as wide as its **most crowded wedge** needs (dots × `min_center`² × `pack` ÷ (wedge angle × band radius), at least `base_t`); spare width goes to the CS bands only — so the embryonic weeks are **stretched** and the fetal weeks **squeezed**. Inside a band: `r_day = r0 + (r1 − r0) × (day − lo + 0.5) ÷ (hi − lo + 1)` — use this, not straight lines between breakpoints, so a K3/K4 day slider lands on the dots. The ≈ stage table overlaps (CS3 days 4–5, CS4 days 5–6): a shared day belongs to the earlier stage, so a band's `lo` is the first day it really holds (CS4 = day 6). An empty `rim_gap` (0.04) separates Birth from the No-day rim. A dot sits at its exact day inside its band (`r_day`) and may move only **within its own band** to clear a neighbour (`r`).

**Wedges.** Order = `LAYOUT.wedge_order` (mol · gam · early · plac · cav · cv · resp · gi · uro · gen · limb · msk · head · cns · ear · eye · skin · defects — related systems side by side; the day-less ones meet at the top seam), clockwise from the top; angle ∝ dots^0.9, at least 9°, 1.5° gaps; a whole dot plus 2 px keeps inside its wedge.

**No overlaps (min dot gap).** Dot **8 px**, clear gap **≥ 2 px**, checked on the **360 px** phone (design-plan §2's smallest) at **1.5× zoom** = a 540 px map: radius 540/2 − 12 = 258 px, so `min_center` = 10/258. **Owner pick (22 Nov 2026, K2 chat):** on a phone the map opens on Parts / Chapters (D-071 d levels) and concept dots appear from 1.5× zoom; 768 px and wider show every dot at 1×. (At 1× on 360 px the 314 dots need ~2.8× the room — rejected options: ~4 px dots, or loosening ring = day.)

**Placement.** Golden-angle spread inside each wedge from a `random.Random(seed)` jitter, then up to 3,000 passes of pairwise push-apart (grid neighbours, 4 % safety margin), each pass clamped to the wedge (whole dot inside) and the band; values rounded to 4 decimals.

**◆ defects.** A concept is ◆ only when a `links.txt` defect row cites it; its day = the start of the sensitive period (above). Defect concepts in chapters with no X1 dossier yet (E02–E04 conditions, E15–E21) stay dots until their X1 adds rows; E08 pregnancy conditions, E09 general concepts (types, teratology, screening, therapy) and capillary haemangiomas (a benign infant tumour, no sensitive period — G-Sci) are not structural birth defects and get no ◆.

**Undated concepts** (no own day, no cited stage) sit on the rim band (`src` `none`) until their chapter's X1 cites a day or stage in `research.txt` — 105 on 22 Nov 2026. K3 should draw `src` = `none` / `from:` visibly different (≈ in the panel) so a guessed or inferred day never looks exact (B2).

**`--selftest`** (CI): determinism · no overlaps at the phone check size · every becomes/defect link has a cite whose anchor is on that exact line · every concept placed · Toolkit inside the centre disc and nothing else · every whole dot (+ edge space) inside its wedge, `wedge.a` inside [a0, a1] · every dot inside its own band (±2e-4 rounding) · every guide ring at its day radius · day scale monotonic · ◆ exactly on cited defects · `links.needs/unlocks` = `prereq/unlocks`. Determinism = 2 fresh builds compared by sha256; overlaps use the exact minimum, not the rounded field. CI also rebuilds and `cmp`s against the committed `content/E/map.json` (CI is the reference build). A missing `links.txt` is an error.

**`--preview`** writes `out/map-preview.svg` (rings + side, light + dark, at the checked size; token colours copied from `src/css/app.css`, D-031 — review image only, the app never hard-codes them, B3).
