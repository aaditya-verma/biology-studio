# Status — updated 19 Nov 2026

*(Purpose: current state + all pendencies — nothing else. Updated: 19 Nov 2026 · Bio · Build · V1 viewer (D-036; phone fps pending); before: T3a results (pass), A0 shell (D-034), hosting D-035. Finished work lives in `logs/build-log.md`.)*

## Lock
- Build lock: free (V1 released 19 Nov 2026)

## Now
- **V1 3D viewer built** (app v2, D-036): `#scene` list · `#scene=<id>&day=<d>` · `#day=<d>`; one engine + canvas (`src/js/14-scene3d.mjs`, three.js r170 vendored in `lib/three-r170/`, loaded only when a scene opens); day scrubber + Play, layer toggles (colour + pattern + label), on-structure labels (priority, never overlapping), cut plane (cross-section / lengthwise, opaque patterned caps), views, axis gizmo, scale bar, `Day · CS · ≈size` stamp, disclaimers line; per-class layouts (design plan §4.6); keys `[ ]` Space arrows `+ − 0 L C` (focus-scoped); Settings › **Motion**. **3 Part 0 scenes** in `content/E/scenes/`: `sc-E00.01.01` Axes & planes · `sc-E00.01.02` Days, stages & scale (1 mm ruler, days 15–18) · `sc-E00.01.04` Two layers become three (days 15–17). New `docs/scene-spec.md`, `tools/scene-check` (C3), `tools/stills` (C11, 8 baselines), layout-check + viewer (924 checks, 125 % viewer shots, viewer rotate), CI runs all three. `?debug=viewer` → triangles/draw calls + **Measure fps**. Gates (separate reviewers): G-Sci FAIL → fixed → pass · G-Eng FAIL → fixed → pass with note · G-Art FAIL → fixed → pass with notes · G-A11y pass with notes → fixed → pass.
- **T3a passed** (18 Nov): owner checked every item on phone, tablet and laptop, both orientations, light + dark — no problems, D-034 choices kept. App live: https://aaditya-verma.github.io/biology-studio/ (Pages on, install works).
- **A0 app shell done** (v1, D-034): `index.html` + `src/` + `content/strings.js` + PWA (`manifest.webmanifest`, `sw.js`). Device classes `dev-p/pl/tp/tl/d` with per-class layouts (design plan §2), history addresses + Up + Android-Back guard, IndexedDB `biostudio` + guarded saves + save log + backup, testing mode `?test=1`, `?debug=<areas>` overlay, ✎ edit hooks, all words in `strings.js`. **Book map** = K1 explorer ported (phone drill-down · tablet 2 panes · desktop 3 panes; X1 fields shown). **Colour key** measures D-031/D-034 contrast on the device. `tools/layout-check` + CI (`.github/workflows/checks.yml`): **672/672 clean** (13 sizes × orientations × 100/125 % × light/dark × 8 screens) + 27 in-app tests + rotate + real-mode flows. Kit `shot.json` v2 + overlay key patterns and the K1 explorer switched to D-031. `build/design-plan.md` new (§8a moved there). Preview: https://claude.ai/artifact/GuWVVUt5kb3uVyjSXVWf1a. Gates (separate reviewers): G-Eng ✅, G-A11y ✅, G-Art ✅ (all with notes, fixes applied).
- **Docs reconciled** (18 Nov): the four upload-only chats of 17 Nov are now in the repo — **quality bar + host + Short profile** (D-032, was upload D-028; `research/quality-references.md` added; new step **M1b**), **device rule** (D-033, was upload D-029; RULES C13, master plan §8a, `tools/layout-check`, owner checks on phone + tablet + laptop), and one merged **A0 prompt** (master plan §13). The upload's colour pick (its D-027) is not ported — D-031 replaced it. The 24 uploaded Project docs are now safe to delete (reminders).
- **Colours decided** (D-031): set A "Classic" — Okabe–Ito textbook mapping, 7 tokens with patterns (`--g-epi/-hypo/-ecto/-meso/-endo/-crest/-ctx`) + plum accent `#994774` ("look here" ring + label). RULES B3 extended. Gates G-Art + G-A11y (separate reviewer): pass with notes. Swatch page https://claude.ai/artifact/NSsdAKiM29kFj7ZwYzq79b.
- **X1 Ch 5 done** (D-029, D-030): `research/dossiers/ch05-gastrulation.md` complete — 23 Tier A fact lines cited `[E05.xx · Rxx]` and marked (✔✔ 8 · ✔ 13 · ⚑ 1 · ✚ 1, no ≈), Tier B–D marked, 10 misconceptions, 2 clinical correlates confirmed. ⚑ notochord (middle-first, D-029); ⚑ stage ages, SCT frequency, SSRI heart line (D-030). AN codes on all 20 Ch 5 concepts (`tools/map/research.txt` → map.json `an`, `mark`, `cs`; concept-map.md AN + Mark columns). GLOSSARY §7 CS06–CS10 + day column for all stages; `timeline.json` `cs` filled (`tools/indexer/carnegie.json`, R08). Registry: R05a–k, R08. Gates: G-Sci fresh eyes pass with fixes (13 applied).
- **K1 concept map done** (D-028): 314 concepts over all 21 chapters + Part 0 (every content section covered; all 265 glossary terms linked). `curriculum/concept-map.md` · `curriculum/roadmap.md` (6 waves → 10 seasons → 93 planned episodes; 222/222 core + exam-high) · `content/E/map.json` · builder `tools/map/` (rows in `concepts.txt`). **Explorer:** https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin. Gates: G-Sci (fresh eyes) pass, fixes applied · G-Eng pass · G-Art/G-A11y QA-role checks pass (fresh eyes = owner T2).
- **I1 index done** (D-026): book-agnostic indexer `tools\indexer\` + Langman JSON in `content\E\index\` on Laptop 1. 21/21 chapters · 178 sections (`E05.02` numbering in README) · 265 glossary terms, 98.9 % placed · 178 cross-ref edges · 44-day timeline. Section tables: `curriculum/book-index-part1.md` / `-part2.md`. Gates: G-Eng passed with notes.
- **H1 repo live** (D-027): private `aaditya-verma/biology-studio` = the only copy of the docs (`studio-docs/`), plus `tools/`, `content/E/index/`, `sync.bat`, `THIRD_PARTY.md`. **Docs change only by a git commit** (RULES I8 (6), setup guide §6a); press **Sync now** before every chat.
- **Shared project** (D-025): the Professor joins as collaborator on a Windows + NVIDIA laptop. Setup guide: `build/setup-guide.md` (+ shareable Doc).
- **Biology Studio** (D-015): any book or topic; Langman = book code E. Repo `biology-studio`, chats `Bio · <Type> · <Step>`.
- **All 8 owner questions settled** (D-012, D-019): free first (D-013) · local-first NVIDIA laptop (D-014) · audience profiles (D-016) · one app two homes (D-003) · K1 map before cards (D-017) · three.js + one scene, three outputs (D-006) · Drive storage + fresh Google Cloud project (D-008).
- **Studio playbook** (D-020) + **usage & upkeep rule** (D-022, RULES §I).
- **M1 in progress:** bake-off kit is on the laptop at `D:\Projects\biology_studio\tools\m1-bakeoff` (D-023); Drive › Embryo Studio › renders › bakeoff created. Laptop = MSI, Windows; GPU/VRAM not yet recorded. Options framed in D-024 (owner picks after T1).
- Tools registry (D-018); Z-Anatomy video-only (D-021); R0 research layer (D-011). Book PDF in Drive › book/.

## Next (in order)
1. **Owner: run the M1 kit** on the laptop (README in the kit; ~20 min setup, then `python bakeoff.py all`; AI clip per `C_ai\README.md`). Then in chat `Bio · Build · M1 bake-off`: "results are in" → the chat reads `out\RESULTS.md` from the laptop, fills Measured, runs G-Sci/G-Art (look) with a separate reviewer, and logs.
2. **Professor:** once invited, follows the setup guide and runs **T5** (`Bio · Review · Laptop 2 setup`).
3. **Owner: T2** — explorer + roadmap check on phone, tablet and laptop (`build/owner-test-checklist.md` T2, ~15 min).
4. **Owner: phone fps for V1** — open https://aaditya-verma.github.io/biology-studio/?debug=viewer#scene=sc-E00.01.04 → Debug → Measure fps → Copy → paste into the V1 chat (or `Bio · Review · V1 fps`) → pipeline reference §2 Measured. Then **T3b** (owner checklist, 3D). Then **S1 studio** — `Bio · Build · S1 studio` (prompt: master plan §13). In parallel, no lock: **X1 Ch 6** — `Bio · Research · X1 Ch 06`.
5. **T1** (owner, phone + one look on tablet/laptop) once clips are in Drive → pick from D-024.
6. **M1b Host shot** — `Bio · Build · M1b host shot` (after M1 numbers; prompt: master plan §13) → owner check **T1b**.
7. **S1** → **C1** → **P1 S1E01** (MBBS + General + Short; host from M1b; with animatic) → **R1** → **L1** → **use gate**.

## Blocked / open questions (pendencies)
- **M1 numbers** — blocked on the laptop run (this chat's bridge can't run commands; cloud workspace has no GPU). M1b waits on them (VRAM decides the local host-shot models); the **1080p rung** (D-033, proposed) waits on M1's 1080p timing.
- **K1 leftovers (X1 per chapter, E05 done):** AN codes, marks and cited `cs` missing outside E05 · map.json `cs_approx` stays derived elsewhere · ⚑ candidate: adult spinal-cord end level (E18.01.05) · deferred Tier D detail concepts (crest induction, somite signals, PDX1, limb D-V / TBX4-5).
- **I1 locator gaps (≈, X1 per chapter):** no Index pages in the PDF (D-026) · E05.01/E05.02 are pp 59–60, not p 59 (checked in X1; fix in the next I1 run) · E08.08/E08.09 twin vs parturition terms look swapped · E10.03 holds spina bifida/Chiari terms · E12.02 spans most of Ch 12 · Day 27 missing · Table 8.1 5/8 rows.
- Roadmap episode numbers after S1E01 are provisional until added to the episode catalog.
- **V1 phone fps not Measured yet** (needs the owner's phone; C4 — budgets stay Expected until then). Tablet + laptop fps rows too.
- **V1 notes (reviewers, not blocking):** streak faint at day 18 on the see-through epiblast · leader lines can cross in phone landscape at 125 % · cross-section through the node hides the groove's raised edges (use cut ≈ −0.3) · WebGL context-loss redraw untested on a real phone · first CI run must confirm the stills match on GitHub's machines (else re-baseline from CI after review) · scene `version` stays 1 until first ship (bump on every change after).
- **M1 kit `shot.json` still fills streak + node with the accent** (D-034 (4)); D-036 (4) moved the app to `ctx` + accent outline — align the kit in the M1 chat (or keep the kit as is: owner says).
- A0 notes for later: in-app reduced-motion switch ✅ V1 · light control borders on grey panels 3.4:1 (passes 3:1) · the published K1 explorer artifact got D-031 colours but keeps its old layouts — the app's Book map replaces it.
- **Tablet for owner checks:** model not recorded (pipeline reference §2); T3a passed on a tablet but real vs emulated wasn't stated. Which tablet do you or the Professor have? None → checks use the laptop's device mode, marked "emulated".
- Host design (name, look, voice) — picked in M1b from 2–3 concepts.
- M1 shot: days 15–17 and disc ≈ 0.2 → 0.4 mm now cited (dossier §1, CS06–07 ✔✔); streak length has no book value — stays ≈. The shot leaves the notochordal process out (D-029: scenes follow the book).
- NMC AN codes were read from a university reprint of the 2024 table — confirm against NMC Vol I when available ≈.
- **D-025 (c)** still proposed: Professor as human G-Sci reviewer? (a) decided, (b) rejected → D-027.
- Professor's name, Google address and **GitHub username** — needed for invites (repo: Settings → Collaborators → Add people).
- `THIRD_PARTY.md`: three.js r170 licence checked ✔ (V1); the other licences stay ≈ until checked against their files.
- Laptop: after cloning the repo into `repo\biology-studio\`, the old `tools\` + `content\` in Studio home are retired (keep `out\`).
- Google Cloud project "Biology Studio" not created yet; add the Professor as an OAuth test user when it is (D1).

## Owner reminders
- [ ] **Press Sync now** (Project knowledge) — V1 changed docs (D-036, design plan, scene spec, checklist T3b).
- [ ] **Measure fps on your phone** (Next 4) and paste the result into a chat; then do **T3b**.
- [ ] **Confirm D-036** (V1 choices; esp. (4) streak + node = grey + plum outline instead of a plum fill) at T3b.
- [ ] **Delete the 24 uploaded Project docs** (Project → knowledge; keep the GitHub `studio-docs/` source). All their content is in the repo now (18 Nov doc reconcile). Then a chat checks it still sees this STATUS.
- [ ] **Re-paste `claude/INSTRUCTIONS.md` §6** into Project → Custom instructions — it gained the device line (D-033). (Professor's Project too, once set up.)
- [ ] **Tell a chat which tablet you can test on** (or "none" → emulated).
- [ ] **Put the two reference reels** in Drive › research/quality-refs/ (reference only, never in the repo).
- [ ] **Skim the ⚑ list** (2 min, X1 owner check): D-029 notochord, D-030 stage ages / SCT frequency / SSRI line — say if you want a different handling.
- [ ] **T2 explorer check** (Next 3) — https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin; tap ✎ Test once to see edit prompts.
- [ ] **Skim the I1 section tables** (`curriculum/book-index-part1.md`, `-part2.md`) — K1 used these ids; say if any look wrong.
- [ ] Optional: if your print copy has the Index (it's missing from the PDF), photograph those pages to Drive › book/ — a later I1 re-run can calibrate term placement against it.
- [ ] **Send the Professor the setup Doc** (https://claude.ai/artifact/VF2tLYkuJs1PjWLatCbEAd — share it from the Doc) and share Drive subfolders renders/ audio/ research/ assets/ index/ backup/ as Editor — **not** book/ (D-025).
- [ ] Confirm D-025 (c) (Professor as G-Sci reviewer) in any Bio chat.
- [ ] **Invite the Professor** when you have his username: github.com/aaditya-verma/biology-studio → Settings → Collaborators → Add people (Write). Then send him the T5 message.
- [ ] Clone the repo on your laptop: Anaconda Prompt → `cd /d D:\Projects\biology_studio\repo` → `git clone https://github.com/aaditya-verma/biology-studio.git`. Run M1 from `repo\biology-studio\tools\m1-bakeoff` from then on.
- [ ] **Run the M1 kit** (see Next 1). Keep the laptop plugged in; Cycles is the long part.
- [ ] **T1** after clips are in Drive.
- [ ] Optional: rename the Drive folder Embryo Studio → Biology Studio (then tell a chat so the docs follow).
- [ ] Optional: download the free 3D Atlas of Human Embryology PDFs (3dembryoatlas.com) to Drive › research/ — reference only (also needed for the M1 G-Sci look check vs R01 CS7).
- [ ] Rich plan artifact still shows the old name and lacks X1/K1/playbook/host/devices — next ideation chat that can edit it updates it.
- [ ] "GitHub projects added" (owner, 17 Nov): still not found — share the links so they join the registry § Tools.
