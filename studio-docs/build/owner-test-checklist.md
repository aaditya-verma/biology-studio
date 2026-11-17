# Owner test checklist

*(Purpose: owner checks on real devices, T1…; no next build until the last is done. Updated: 17 Nov 2026 · Bio · Build · K1 concept map (T2 written).)*

Run on real devices. Write each result on its **Result** line, then tick it in `claude/STATUS.md` › Owner reminders. Newest open items first. No next build starts until the last check is done (D-010).

**Apps:** none live yet.

**Status, 17 Nov 2026:** T1 written; opens when the laptop run puts clips in Drive. T2 open (K1 published the explorer). (Renumbered 17 Nov: old T2 → T3, old T3 → T4, after K1 was added, D-017.)

---

## T1. Bake-off: pick the renderer + voice *(~10 min on the phone)* — WAITING FOR CLIPS (M1)
Before: on the laptop, `python bakeoff.py all` (+ `C_ai\README.md` for the AI clip), then upload `out\for_drive\` to Drive › Embryo Studio › renders › bakeoff. Keep `out\blind_key.json` closed.
1. Open Drive › renders › bakeoff on the phone. Up to 4 clips of the same 20 s shot: `clip-A … clip-D` (Blender Cycles, Blender Eevee, three.js, AI video — in random order).
2. Watch each full screen, once with sound off.
3. For each, judge:
   - **Biology:** streak in the caudal midline, node at its cranial tip, mesoderm spreading between the layers, endoderm replacing hypoblast, disc broader cranially, day 15 → 17.
   - **Readable:** day stamp, scale bar, axis gizmo (Cr/Ca/D/V) and the labels, on a phone.
   - **Steady:** the same embryo throughout; no flicker or jumps.
   - **Look:** clear and attractive enough for a medical student to keep watching.
4. Listen to `voice1_kokoro.wav` and `voice2_piper.wav` (20 terms in the order of `D_tts\terms.txt`, then one sentence). Note any term said wrong.
5. Then open `blind_key.json` and reply in the M1 chat with your picks (options in DECISIONS D-024).
- **Result:** ☐ pass ☐ problems — A: ☐ clear ☐ confusing · B: ☐ clear ☐ confusing · C: ☐ clear ☐ confusing · D: ☐ clear ☐ confusing · pick: ___ ☐ mix · voice: ☐ 1 ☐ 2 ☐ neither · mispronounced terms: ___ · notes:

## T5. Laptop 2 setup — the Professor *(~1 h 30 min on the laptop, once)* — OPEN: repo ready (H1 ✅ 17 Nov 2026); waits for the Professor's GitHub invite
Follow `build/setup-guide.md` §1–§5.
1. `nvidia-smi` shows the GPU; Studio Driver current.
2. `ffmpeg -hide_banner -encoders | findstr nvenc` lists `h264_nvenc`.
3. `python bakeoff.py hw` → no MISSING in `out\hw.json`.
4. `python bakeoff.py quick` finishes; Blender lists OptiX.
5. Claude Project shows today's STATUS (after Sync now).
6. First chat `Bio · Review · Laptop 2 setup` records Laptop 2 in `build/pipeline-reference.md` §1b.
- **Result:** ☐ pass ☐ problems · GPU/VRAM: ___ · missing tools: ___ · quick run minutes: ___ · stuck at step: ___ · notes:

## T2. Concept map explorer *(~10 min, phone + laptop)* — OPEN (K1)
1. On the phone open https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin. Book tab: E05 › E05.01 › tap "Primitive streak". Read the page; tap a "Needs first" link, then go back.
2. Crosstabs: Rows = Germ layer, Columns = Day / week; tap Mesoderm × Wk 3; open one concept. Tap ⇄ Swap; try System × Tier.
3. Search "pouch" — the list narrows; clear it. Filters: Importance = exam-high, System = Heart & vessels.
4. Prerequisites tab: are the top 10 sensible "learn first" ideas?
5. Tap ✎ Test, then ✎ on any concept: an edit prompt appears; Copy works (or select by hand).
6. On the laptop: repeat step 2; the concept page opens beside the list.
7. Open `curriculum/roadmap.md`: read Wave 1 (Season 1). Order sensible?
8. Skim one chapter you know well in `curriculum/concept-map.md` — anything missing or wrong?
- **Result:** ☐ pass ☐ problems · coverage: ☐ complete ☐ missing (which?) · crosstabs: ☐ useful ☐ confusing (which?) · navigation: ☐ easy ☐ lost (where?) · roadmap order: ☐ makes sense ☐ change (what?)

## T3. App shell + Part 0 cards *(~10 min, phone + tablet)* — PLANNED (A0, V1, C1)
Steps written by the C1 build chat.
- **Result:** ☐ pass ☐ problems · 3D smooth: ☐ yes ☐ stutters (where?) · cards: ☐ clear ☐ too dense · navigation: ☐ easy ☐ lost (where?)

## T4. S1E01 Gastrulation *(~5 min on the phone + ~2 min next day + ~2 min at 7 days)* — PLANNED (R1, L1)
Steps written by the L1 build chat. Watch the MBBS cut; a non-medical friend watches the General cut if possible.
- **Result:** ☐ pass ☐ problems · ☐ biologically right ☐ off at (time) · ☐ watched to the end ☐ drifted at (time) · story ☐ gripping ☐ flat · voice pace ☐ right ☐ fast · 3D ☐ clear ☐ lost track at (time) · General cut understood by a non-medical viewer: ☐ yes ☐ no · Check: __ / __ · 24 h: __ / __ · 7 d: __ / __
