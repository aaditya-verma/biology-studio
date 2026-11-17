# Owner test checklist

*(Purpose: owner checks on real devices, T1…; no next build until the last is done. Updated: 18 Nov 2026 · Bio · Review · T3a results — T3a passed.)*

Run on real devices. Write each result on its **Result** line, then tick it in `claude/STATUS.md` › Owner reminders. Newest open items first. No next build starts until the last check is done (D-010).

**Devices (D-033, RULES C13):** every check with a screen runs on the **phone (portrait + landscape)**, a **tablet (portrait + landscape)** and the **laptop**. No tablet to hand → use the laptop browser's device mode (Chrome: F12 › device toolbar › iPad / Android tablet) and note "emulated". Report layout problems as *device + orientation + screen + what's wrong*.

**Apps:** A0 shell live at https://aaditya-verma.github.io/biology-studio/ (GitHub Pages, D-035).

**Status, 17 Nov 2026:** T1 written; opens when the laptop run puts clips in Drive. T2 open (K1 published the explorer). (Renumbered 17 Nov: old T2 → T3, old T3 → T4, after K1 was added, D-017.)

---

## T1. Bake-off: pick the renderer + voice *(~10 min on the phone + ~3 min tablet/laptop)* — WAITING FOR CLIPS (M1)
Before: on the laptop, `python bakeoff.py all` (+ `C_ai\README.md` for the AI clip), then upload `out\for_drive\` to Drive › Embryo Studio › renders › bakeoff. Keep `out\blind_key.json` closed.
1. Open Drive › renders › bakeoff on the phone. Up to 4 clips of the same 20 s shot: `clip-A … clip-D` (Blender Cycles, Blender Eevee, three.js, AI video — in random order).
2. Watch each full screen, once with sound off.
2b. Watch your favourite clip once on a tablet (both orientations) and once on the laptop: labels legible, nothing looks oversized or blurry.
3. For each, judge:
   - **Biology:** streak in the caudal midline, node at its cranial tip, mesoderm spreading between the layers, endoderm replacing hypoblast, disc broader cranially, day 15 → 17.
   - **Readable:** day stamp, scale bar, axis gizmo (Cr/Ca/D/V) and the labels, on a phone.
   - **Steady:** the same embryo throughout; no flicker or jumps.
   - **Look:** clear and attractive enough for a medical student to keep watching.
4. Listen to `voice1_kokoro.wav` and `voice2_piper.wav` (20 terms in the order of `D_tts\terms.txt`, then one sentence). Note any term said wrong.
5. Then open `blind_key.json` and reply in the M1 chat with your picks (options in DECISIONS D-024).
- **Result:** ☐ pass ☐ problems — A: ☐ clear ☐ confusing · B: ☐ clear ☐ confusing · C: ☐ clear ☐ confusing · D: ☐ clear ☐ confusing · pick: ___ ☐ mix · voice: ☐ 1 ☐ 2 ☐ neither · mispronounced terms: ___ · tablet/laptop: ☐ fine ☐ labels too small/large ☐ blurry · notes:

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
6b. Rotate the phone mid-task, then open the explorer on a tablet (both orientations, or emulated). Note layout problems only — the explorer was built before the device rule (D-033); A0 brings it up to master plan §8a when it ports it as the Book map.
7. Open `curriculum/roadmap.md`: read Wave 1 (Season 1). Order sensible?
8. Skim one chapter you know well in `curriculum/concept-map.md` — anything missing or wrong?
- **Result:** ☐ pass ☐ problems · coverage: ☐ complete ☐ missing (which?) · crosstabs: ☐ useful ☐ confusing (which?) · navigation: ☐ easy ☐ lost (where?) · roadmap order: ☐ makes sense ☐ change (what?) · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · layout problems (device + screen):

## T3. App shell + Part 0 cards *(~15 min: phone, tablet, laptop)* — **T3a ✅ 18 Nov 2026** (shell + Book map); 3D (V1) and cards (C1) parts follow
**T3a — A0 shell (~10 min).** Open the app preview (link in STATUS › Owner reminders) on the phone, then a tablet (or the laptop browser's device mode, marked emulated), then the laptop.
1. **Today:** read it once. Tap **Book map** in the bar (phone) or rail (tablet landscape / laptop).
2. **Book map:** phone — tap Ch 5 → Notochord; tablet/laptop — the chapter list stays on the left, the concept opens beside it (laptop: three panes). Check the concept shows **Confidence ⚑**, **Stage CS07–12 · cited**, **NMC AN** codes.
3. **Back / Up:** use the top-bar ← and ↑, and the phone's Back gesture. At Today, Back once shows "Press Back again to leave"; the app should never close by surprise.
4. **Rotate** the phone and tablet on the Notochord page: same page, same place, layout changes (two columns in landscape).
5. **Crosstab:** Book map → Germ layer × Day/week → tap a cell → its concepts list. Each layer row shows its pattern swatch.
6. **Settings → Colour key:** every layer shows colour + pattern + label with ✓ marks; switch Theme to Dark and look again.
7. **Install** (phone): browser menu → Add to Home screen (works fully once the app is on GitHub Pages; the preview may not offer it).
8. **Testing mode:** Settings → Turn on testing mode → tap a ✎ → the edit prompt opens; Copy works. Turn it off again.
- **Result T3a (18 Nov 2026, on GitHub Pages):** ☑ pass · navigation: ☑ easy · Back/Up: ☑ right · Notochord ⚑ / CS07–12 cited / NMC AN: ☑ yes · crosstab + cell list: ☑ works · colours/patterns readable (light + dark): ☑ yes · install: ☑ worked · testing mode ✎ + Copy: ☑ worked · devices: phone P ☑ L ☑ · tablet P ☑ L ☑ (real/emulated + model not stated) · laptop ☑ · rotate keeps place: ☑ yes · layout problems: none · owner: "All are checked"; more feedback will come during later builds.

**T3b — 3D + Part 0 cards:** steps written by the C1 build chat.
- **Result:** ☐ pass ☐ problems · 3D smooth: ☐ yes ☐ stutters (where?) · cards: ☐ clear ☐ too dense · navigation: ☐ easy ☐ lost (where?) · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · rotate keeps place: ☐ yes ☐ no · layout problems (device + screen):

## T4. S1E01 Gastrulation *(~5 min on the phone + ~2 min next day + ~2 min at 7 days; one watch on tablet or laptop)* — PLANNED (R1, L1)
Steps written by the L1 build chat. Watch the MBBS cut; a non-medical friend watches the General cut if possible.
- **Result:** ☐ pass ☐ problems · ☐ biologically right ☐ off at (time) · ☐ watched to the end ☐ drifted at (time) · story ☐ gripping ☐ flat · voice pace ☐ right ☐ fast · 3D ☐ clear ☐ lost track at (time) · General cut understood by a non-medical viewer: ☐ yes ☐ no · Check: __ / __ · 24 h: __ / __ · 7 d: __ / __ · player on tablet/laptop: ☐ good ☐ problems (what?)
