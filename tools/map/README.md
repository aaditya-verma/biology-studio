# tools/map — K1 concept map builder

Purpose: turns `concepts.txt` (our concept rows) + `research.txt` (X1 layer: AN codes, marks, cited stages per concept) + I1 index (`content/E/index/`) into `content/E/map.json`, `curriculum/concept-map.md` and `curriculum/roadmap.md`. Owner doc: `build/master-plan.md` §5. Updated: 22 Nov 2026 · Bio · Research · X1 Ch 11 (E11 rows in research.txt: muscle AN codes AN3/4.1/7.4–7.5/24.4/28.1/31.1/45.3/67.2/74.4/79.4, cs from human specimens — 9–23 muscle origin, 14–22 fibres + limb muscle, 15–18 frontier, 15–20 epaxial/hypaxial, 16–21 head). Before: 21 Nov 2026 · Bio · Research · X1 Ch 10 (E10 rows in research.txt: axial AN codes AN2/21/26/35.9/50/53.4/74.4/79.4–79.5, cs 10–23 on the vertebra and 14–23 on the disc from human specimens). Before: X1 Ch 09 (E09 rows in research.txt: AN79.5/79.6 + AN81 codes, cs 7–23 on the teratogenic window only). Before: X1 Ch 08 (E08 rows: AN80 codes + marks, cs blank for the fetal period). Before: X1 Ch 07 (E07 rows; septtr/diaphragm definitions fixed, D-043 c).

Run from this folder (Python 3, no packages):
```
python build_map.py --dry-run --debug     # checks only (ids, prereqs, cycles, coverage)
python build_map.py --out out             # writes out/map.json, out/concept-map.md, out/map-report.json
python roadmap.py                         # reads out/map.json, writes out/roadmap.md
```
Then copy `out/map.json` to `content/E/map.json` and the two .md files to `studio-docs/curriculum/`, commit (setup guide §6a), and republish the explorer (needs `map.json` beside `explorer/index.html`).
Flags: `--dry-run --debug --only E05 --preview` (RULES I5). Edit points: rows in `concepts.txt` (add at the END of a section — ids are permanent, A2); per-chapter X1 rows in `research.txt` (`id|AN codes|mark|cs` → additive fields `an`, `mark`, `cs`, `x1` in map.json; the dossier owns the facts); vocab and manual term links marked `# EDIT:` in `build_map.py`; seasons in `roadmap.py`.
`roadmap.py` runs from the folder that holds `out/map.json`.
Explorer page: explorer/index.html (published at https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin with map.json beside it).
