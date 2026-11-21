# Owner test checklist

*(Purpose: owner checks on real devices, T1…; no next build until the last is done. Updated: 21 Nov 2026 · Bio · Build · M1b host results — T1b rewritten for the kit that actually runs (`m1b.py t1b`, v6, D-051). Before: 21 Nov 2026 · Bio · Build · L1 learning core — T7 written. Before: 21 Nov 2026 · Bio · Fix · M1b merge — T3c result logged (pass, from the L1 chat 03:43 IST). Before: 20 Nov 2026 · Bio · Build · M1b host shot (Step 2) — T1b written. Before: 21 Nov 2026 · Bio · Plan · App-first — T7, T8, T8b, T9, T3d stubs; T4 now the L3 player check (D-047). Before: 20 Nov 2026 · Bio · Build · M1 bake-off — T1 opened (3 clips, Method C pending). Before: 20 Nov 2026 · Bio · Content · C1 Part 0 + Ch 5 — T3c written. Before: 19 Nov 2026 · Bio · Build · W1 progress map — T6 written, T1b stub; open/pass state of each check now lives in `build/steps.json` (D-040). Before: V1 viewer — T3b written.)*

Run on real devices. Write each result on its **Result** line, then tick it in `claude/STATUS.md` › Owner reminders. Newest open items first. No next build starts until the last check is done (D-010).

**Devices (D-033, RULES C13):** every check with a screen runs on the **phone (portrait + landscape)**, a **tablet (portrait + landscape)** and the **laptop**. No tablet to hand → use the laptop browser's device mode (Chrome: F12 › device toolbar › iPad / Android tablet) and note "emulated". Report layout problems as *device + orientation + screen + what's wrong*.

**Apps:** A0 shell live at https://aaditya-verma.github.io/biology-studio/ (GitHub Pages, D-035).

**Status, 17 Nov 2026:** T1 written (opened 20 Nov, M1 run done). T2 open (K1 published the explorer). (Renumbered 17 Nov: old T2 → T3, old T3 → T4, after K1 was added, D-017.)

---

## T6. Progress map *(~6 min: phone, then tablet or laptop)* — OPEN (W1)
Open https://aaditya-verma.github.io/biology-studio/#progress on the phone (pull to refresh once so v5 loads), then a tablet (or the laptop's device mode, marked emulated), then the laptop.
1. **Map:** lanes by chat type (Ideation · Build · Research · Content · Episode · Review · Ideas). Each box shows its id and status as colour **and** pattern **and** a word; the key under the map lists them. Phone portrait: the map runs top → bottom; landscape and larger: left → right.
2. Tap **C1**: the step page shows needs (S1, X1.05, X1.06 ✓), unblocks (P1, L1), gates, D-ids, last log line and your open D-037 question (C1.q1); a grey note says it waits only for the build lock if a build chat holds it. **Copy prompt** copies the ready prompt; the chat name shows above it.
3. Tap **P1**: a red "Can't start — needs C1 (ready), M1b (planned)" line shows.
4. **Board:** Now · Ready · Blocked · Done. Phone: one section under another; phone landscape and tablets: two columns (tablet landscape four if ≥ 1200 px wide); laptop: four.
5. **Your inputs:** oldest first; tap one → its step; **Copy reply** copies a line to paste into that step's chat.
6. **Rotate** phone and tablet on a step page: same step, same place.
7. Turn on testing mode (Settings): ✎ on a step opens an edit prompt pointing at `build/steps.json`.
- **Result:** ☐ pass ☐ problems · map readable on the phone: ☐ yes ☐ no (where?) · can't-start line right: ☐ yes · board columns right: ☐ yes · inputs list complete: ☐ yes ☐ missing (which?) · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · rotate keeps place: ☐ yes · layout problems (device + screen):

## T7. Learning core *(~20 min: phone, then tablet, then laptop; + 1 min tomorrow)* — OPEN (L1, 21 Nov 2026)
Open the app **without** `?test=1`: https://aaditya-verma.github.io/biology-studio/ — pull to refresh once so **v7** loads (Settings shows the version). This time your taps are saved on the device. Tap **Export backup** in Settings first (A3).
1. **Cards tab (phone, portrait):** 13 cards in two groups, each with a ring + word: ○ New, ◔ Read, ◑ Understood, ● Can explain.
2. **Open E05.01.01 Gastrulation in one picture.** Title, General/MBBS switch and "You will be able to" sit above the 3D. Wait 2 s: the chip turns **Read**. Turn the 3D and scrub the days; **Open full 3D** keeps the day. Tap a small number after a sentence: its facts open with source + mark.
3. **Check:** answer one question wrong on purpose. You should see ✗, the right answer and why. Finish → "Read the card again, then retry". Try again (options reshuffle) and get all right → **Understood**.
4. **Can explain:** say the objective out loud, tap **Show a model answer**, then **I explained it** → **Can explain**.
5. **Rotate** to landscape mid-Check: same question, same day in 3D, same place on the page.
6. **E00.01.06 How to use the app** (the new guide card, marks ⓘ): does it describe the app as you just used it? Anything wrong or unclear → note the line.
7. **Tablet** (or laptop device mode, "emulated"): portrait = 3D on top, text below; landscape = 3D │ text. **Laptop:** 3D │ text │ card rail; the 3D stays in view while the text scrolls. Try the Check with the keyboard only (Tab, Enter/Space).
8. **Remember deck:** Today shows "Nothing due today" (prompts first come back tomorrow). **Tomorrow:** Today shows the due count → **Review now** → answer from memory, Show answer, Got it / Not yet. Note: anything confusing?
9. **G-Owner** on D-050 (guide cards + ⓘ, statuses, 1-3-7 deck, Reviewed cards shown to learners): say "D-050 confirmed" or what to change.
- **Result T7:** ☐ pass ☐ problems · statuses move as described: ☐ · Check feedback clear: ☐ · Can explain makes sense: ☐ · rotate keeps place: ☐ · E00.01.06 matches the app: ☐ · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · deck next day: ☐ · D-050: ☐ confirmed ☐ change: ___ · notes (screen + device + what): ___

## T8. 3D drills + new scenes *(phone, tablet, laptop)* — PLANNED (V2 writes the steps)
- **Result:** ☐ pass ☐ problems · notes: ___

## T8b. Trace a cell *(phone, tablet, laptop)* — PLANNED (V3 writes the steps)
- **Result:** ☐ pass ☐ problems · notes: ___

## T9. Lessons, Today, Mixed review *(phone, tablet, laptop)* — PLANNED (L2 writes the steps)
- **Result:** ☐ pass ☐ problems · notes: ___

## T3d. Ch 6–8 cards *(phone, tablet, laptop)* — PLANNED (C2 writes the steps, like T3c)
- **Result:** ☐ pass ☐ problems · notes: ___

## T1b. Host shot: Nani Koshika test *(~15–20 min laptop run + ~10 min phone, tablet/laptop)* — OPEN (M1b, rewritten 21 Nov 2026 for v6, D-051)
Host: **Nani Koshika** (D-048), voice Kokoro `af_heart`, route H-a = our 3D model in Blender (D-049). The v5 preview (360p) is not enough: T1b runs on the v6 720p render.
**Before:** Anaconda Prompt → `conda activate bio` → `cd D:\Projects\biology_studio\tools\m1b-host` → **`python m1b.py t1b`** (one run, ~10–20 min, plugged in). If a step fails, paste the last 30 lines into the chat.
1. Upload **the files inside** `tools\m1b-host\out\for_drive\` — not the folder — to Drive › renders › bakeoff › host. It holds v6 only: `M1b-hs01_v6_720p_cap-en.mp4`, `_cap-hi.mp4`, `_clean.mp4`, one `.manifest.json` per clip, `sheet_portrait.png`, `sheet_landscape.png`, the VTTs, `RESULTS.md`. (Optional tidy: move the old v1–v5 files on Drive into a folder `old`.)
2. **Sheet** (`sheet_portrait.png`) on the phone: clearly Nani from the reference (pearl egg body, wine shawl + fringe + pale vines, oval glasses on a chain, book)? Front and side the same character? All 6 faces readable at phone size — warm, curious, delighted, surprised (wide eyes from the lids), thinking, tsk?
3. **Shot** (`…_cap-en.mp4`), full screen, sound on, then sound off:
   - Same Nani in both angles (cut at 2.6 s)? Lips match the words? Blinks natural?
   - Light warm and cinematic; nothing flickers. In the second angle her head stands clear of the lamp (thin dark edge on the body is new — does it look natural or like a cartoon line?).
   - Captions: one phrase at a time, key word "whole body" highlighted, all clear of the app buttons (bottom + right).
   - Voice: pace OK (about 143 wpm), warm, no odd sounds; level about the same as other videos on your phone.
4. **Hindi** (`…_cap-hi.mp4`): "अगर एक चपटी डिस्क को / पूरा शरीर बनाना पड़े तो?" — letters joined right (no boxes, no broken matras), key "पूरा शरीर" highlighted. (Audio is still English — a Hindi voice is a later step.)
5. Against **QR01/QR02** (quality-references §1): would a student stop scrolling? Score 1–5 for look, face, lip-sync, captions.
6. Once on a tablet (both orientations) and once on the laptop: nothing blurry or oversized.
7. Reply in one message: pass / problems + the 4 scores + host OK y/n + notes, and paste `RESULTS.md`. If look or face ≤ 2 after one tune round, the chat brings the paid options (H-c, D-049/D-051 costs).
- **Result:** ☐ pass ☐ problems · scores look _ / face _ / lip-sync _ / captions _ · host OK ☐ y ☐ n · notes:

## T1. Bake-off: pick the renderer + voice *(~10 min on the phone + ~3 min tablet/laptop)* — OPEN (M1, 20 Nov 2026)
Before: the laptop run is done (20 Nov). Upload `D:\Projects\biology_studio\tools\m1-bakeoff\out\for_drive\` (3 clips, 3 manifests, 2 voices) to Drive › renders › bakeoff. Keep `out\blind_key.json` closed.
1. Open Drive › renders › bakeoff on the phone. **3 clips** of the same 20 s shot: `clip-A … clip-C` (Blender Cycles, Blender Eevee, three.js — in random order). The AI clip (Method C) was not run (6 GB VRAM; D-045) — skip D.
   Known (reviewer, stills): the day-15 stamp says CS07 (should be CS06, fixed in the scene spec later); the colour key and disclaimer are too small to read on a phone — judge the shot, not the key size.
2. Watch each full screen, once with sound off.
2b. Watch your favourite clip once on a tablet (both orientations) and once on the laptop: labels legible, nothing looks oversized or blurry.
3. For each, judge:
   - **Biology:** streak in the caudal midline, node at its cranial tip, mesoderm spreading between the layers, endoderm replacing hypoblast, disc broader cranially, day 15 → 17.
   - **Readable:** day stamp, scale bar, axis gizmo (Cr/Ca/D/V) and the labels, on a phone.
   - **Steady:** the same embryo throughout; no flicker or jumps.
   - **Look:** clear and attractive enough for a medical student to keep watching.
4. Listen to `voice1_kokoro.wav` and `voice2_piper.wav` (20 terms in the order of `D_tts\terms.txt`, then one sentence). Note any term said wrong.
5. Then open `blind_key.json` and reply in the M1 chat with your picks (options in DECISIONS D-024).
- **Result:** ☐ pass ☐ problems — A: ☐ clear ☐ confusing · B: ☐ clear ☐ confusing · C: ☐ clear ☐ confusing · pick (D-024/D-045 O1–O3): ___ · encode E1/E2: ___ · favourite clip: ___ ☐ mix · voice: ☐ 1 ☐ 2 ☐ neither · mispronounced terms: ___ · tablet/laptop: ☐ fine ☐ labels too small/large ☐ blurry · notes:

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

## T3. App shell + 3D + Part 0 cards *(~15 min each: phone, tablet, laptop)* — **T3a ✅ 18 Nov 2026** (shell + Book map) · **T3b ✅ 19 Nov 2026** (3D viewer) · **T3c ✅ 21 Nov 2026** (C1, opened 20 Nov 2026): read the cards in the Studio review pane on each device and give your **G-Owner** on E05.01.01
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

**T3b — 3D viewer (V1, ~10 min; cards part follows in C1).** Open https://aaditya-verma.github.io/biology-studio/ on the phone (pull to refresh once so v2 loads), then a tablet (or the laptop's device mode, marked emulated), then the laptop.
1. **Today → Start here → 3D · Two layers become three.** The stage shows `Day 15 · CS06 · ≈0.20 mm`, a scale bar, the Cr/Cd·D/V·L/R key and the disclaimer line.
2. **Day:** drag the slider 15 → 17, then tap ▶ Play. Mesoderm (orange, diagonal lines) spreads between the layers; endoderm (yellow, lines) appears under it; the stamp shows `CS06–07` between key days. On the laptop: `[` `]` step a day, Space plays.
3. **Turn + zoom:** drag to turn, pinch (phone) or scroll (laptop) to zoom, double-tap to reset. The scale bar changes length and label as you zoom.
4. **Layers:** turn Epiblast off, then on. Each toggle shows colour + pattern + name.
5. **Cut:** Cut tab → Cross-section → View → Face the cut: the layers show as stacked bands with labels on them.
6. **Rotate** phone and tablet mid-scene: same day, same view, same tab.
7. **3D list** (3D in the bar/rail) → Axes & planes → Layers → turn on the three planes; then **Days, stages & scale**: play 15 → 18 against the 1 mm ruler.
8. **Settings → Motion → Reduce**, then Play again: it jumps day to day, views snap. Set it back.
9. **fps (phone, once):** open https://aaditya-verma.github.io/biology-studio/?debug=viewer#scene=sc-E00.01.04 → Debug tab → **Measure fps** (~30 s, keep the screen on) → **Copy** → paste into a chat (fills pipeline reference §2).
- **Result T3b (19 Nov 2026, app v3 on GitHub Pages):** ☑ pass · 3D smooth: ☑ yes · labels readable / on the right structure: ☑ yes · cut face clear: ☑ yes · day/stage/size makes sense: ☑ yes · Reduce motion: ☑ works · devices: phone P ☑ L ☑ · tablet P ☑ L ☑ (real/emulated not stated) · laptop ☑ · rotate keeps place: ☑ yes · layout problems: none · fps (step 9): done earlier (phone 60, tablet P 60) · D-036 confirmed · owner: "All pass".

**T3c — cards in the Studio (C1, ~15 min: phone, tablet, laptop).** Open https://aaditya-verma.github.io/biology-studio/?test=1#studio (pull to refresh once so **v6** loads; Settings shows the version). The Studio saves nothing; you only read and judge.
1. **Card list:** 12 cards — 5 Part 0 (E00.01.01–05; E00.01.06 waits for L1, D-042) + 7 Ch 5 Tier A. Each shows its status (Reviewed once both gates pass) and ✓ when card-check is clean.
2. **Phone (portrait, then landscape):** open **E05.01.01 Gastrulation in one picture**. You get the review pane only. Read every line: General and MBBS sentences, facts with their [cites] and marks, misconceptions, Checks (✓ marks the right option), the new **Remember** prompts (r1–r3) and **Where it shows up**. Switch gates with the G-Sci / G-Learn / G-A11y / G-Owner buttons: G-Sci and G-Learn show the reviewers' passes.
3. **Tablet** (portrait: draft above review; landscape: draft │ review): open **E00.01.04 Colour key** and **E05.02.01 Notochord**. Check the colour key now names the three layers in plain words (your D-037 answer) and the notochord gives the book answer with the ⚑ "Newer evidence" line in More.
4. **Laptop** (draft │ review │ sources): skim the other cards. Rotate/resize once mid-card: same card, same pane.
5. **Read for sense, not rules:** would a non-medical reader follow the General text? Is anything wrong, unclear or dull? Note card id + line id (e.g. `E05.01.03 body.general.2`).
6. **G-Owner on E05.01.01:** if you're happy, open its G-Owner gate, put your name, role **Owner**, agent `T3c`, tick the box and tap **Pass** — then tell the next chat "G-Owner pass E05.01.01" (or tap Copy JSON and paste it). Shipping also needs G-A11y, which C1 passed on the text.
- **Result T3c:** ☑ pass (21 Nov 2026, 03:43 IST · by Aaditya, reported in the L1 chat) · G-Owner E05.01.01: ☑ pass · notes: tablet P · Studio · debug overlay covers text top-right; make it tap-to-hide (→ steps.json L1 to-do). ___
- **Result:** ☐ pass ☐ problems · 3D smooth: ☐ yes ☐ stutters (where?) · cards: ☐ clear ☐ too dense · navigation: ☐ easy ☐ lost (where?) · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · rotate keeps place: ☐ yes ☐ no · layout problems (device + screen):

## T4. S1E01 Gastrulation *(~5 min on the phone + ~2 min next day + ~2 min at 7 days; one watch on tablet or laptop)* — PLANNED (R1, L3 player; D-047)
Steps written by the L1 build chat. Watch the MBBS cut; a non-medical friend watches the General cut if possible.
- **Result:** ☐ pass ☐ problems · ☐ biologically right ☐ off at (time) · ☐ watched to the end ☐ drifted at (time) · story ☐ gripping ☐ flat · voice pace ☐ right ☐ fast · 3D ☐ clear ☐ lost track at (time) · General cut understood by a non-medical viewer: ☐ yes ☐ no · Check: __ / __ · 24 h: __ / __ · 7 d: __ / __ · player on tablet/laptop: ☐ good ☐ problems (what?)
