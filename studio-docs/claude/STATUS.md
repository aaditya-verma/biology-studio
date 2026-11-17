# Status — updated 17 Nov 2026

*(Purpose: current state + all pendencies — nothing else. Updated: 17 Nov 2026 · Bio · Research · X1 Ch 05 (D-029, D-030). Finished work lives in `logs/build-log.md`.)*

## Lock
- Build lock: free *(RULES I8; K1 released 17 Nov 2026, 10:25 IST; H1 released earlier)*

## Now
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
3. **Owner: T2** — explorer + roadmap check on phone and laptop (`build/owner-test-checklist.md` T2, ~10 min).
4. **A0 shell** — `Bio · Build · A0 shell` (prompt: master plan §13; settles accent + germ-layer colours first). In parallel, no lock: **X1 Ch 6** — `Bio · Research · X1 Ch 06`.
5. **T1** (owner, phone) once clips are in Drive → pick from D-024.
6. **V1** (seed: kit's `shot.json` + `scene_math.py`) → **S1** → **C1** → **P1 S1E01** (with animatic) → **R1** → **L1** → **use gate**.

## Blocked / open questions (pendencies)
- **M1 numbers** — blocked on the laptop run (this chat's bridge can't run commands; cloud workspace has no GPU).
- **K1 leftovers (X1 per chapter, E05 done):** AN codes, marks and cited `cs` missing outside E05 · map.json `cs_approx` stays derived elsewhere · ⚑ candidate: adult spinal-cord end level (E18.01.05) · deferred Tier D detail concepts (crest induction, somite signals, PDX1, limb D-V / TBX4-5).
- **I1 locator gaps (≈, X1 per chapter):** no Index pages in the PDF (D-026) · E05.01/E05.02 are pp 59–60, not p 59 (checked in X1; fix in the next I1 run) · E08.08/E08.09 twin vs parturition terms look swapped · E10.03 holds spina bifida/Chiari terms · E12.02 spans most of Ch 12 · Day 27 missing · Table 8.1 5/8 rows.
- Roadmap episode numbers after S1E01 are provisional until added to the episode catalog.
- Germ-layer token colours: kit uses Okabe–Ito placeholders (epiblast/hypoblast have no token yet) — settle in V1/A0.
- Accent colour — open (needed by A0).
- M1 shot: days 15–17 and disc ≈ 0.2 → 0.4 mm now cited (dossier §1, CS06–07 ✔✔); streak length has no book value — stays ≈. The shot leaves the notochordal process out (D-029: scenes follow the book).
- Explorer artifact doesn't show the new X1 fields (AN, mark, cited CS) yet — A0's Book map shows them.
- NMC AN codes were read from a university reprint of the 2024 table — confirm against NMC Vol I when available ≈.
- **D-025 (c)** still proposed: Professor as human G-Sci reviewer? (a) decided, (b) rejected → D-027.
- Professor's name, Google address and **GitHub username** — needed for invites (repo: Settings → Collaborators → Add people).
- `THIRD_PARTY.md` licences are ≈ — check each against its licence file before A0.
- Laptop: after cloning the repo into `repo\biology-studio\`, the old `tools\` + `content\` in Studio home are retired (keep `out\`); `tools\map\K1-handoff.md` there is superseded — delete it.
- Google Cloud project "Biology Studio" not created yet; add the Professor as an OAuth test user when it is (D1).

## Owner reminders
- [ ] **Press Sync now** (Project knowledge) — this chat changed docs.
- [ ] **Skim the ⚑ list** (2 min, X1 owner check): D-029 notochord, D-030 stage ages / SCT frequency / SSRI line — say if you want a different handling.
- [ ] **T2 explorer check** (Next 3) — https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin; tap ✎ Test once to see edit prompts.
- [ ] **Skim the I1 section tables** (`curriculum/book-index-part1.md`, `-part2.md`) — K1 used these ids; say if any look wrong.
- [ ] Optional: if your print copy has the Index (it's missing from the PDF), photograph those pages to Drive › book/ — a later I1 re-run can calibrate term placement against it.
- [ ] **Send the Professor the setup Doc** (https://claude.ai/artifact/VF2tLYkuJs1PjWLatCbEAd — share it from the Doc) and share Drive subfolders renders/ audio/ research/ assets/ index/ backup/ as Editor — **not** book/ (D-025).
- [ ] Confirm D-025 (c) (Professor as G-Sci reviewer) in any Bio chat.
- [ ] **Invite the Professor** when you have his username: github.com/aaditya-verma/biology-studio → Settings → Collaborators → Add people (Write). Then send him the T5 message.
- [ ] **Connect Project knowledge to GitHub** (`studio-docs/` only) → a chat checks it shows this STATUS → then remove the 23 uploaded duplicates (only after you confirm).
- [ ] Clone the repo on your laptop: Anaconda Prompt → `cd /d D:\Projects\biology_studio\repo` → `git clone https://github.com/aaditya-verma/biology-studio.git`. Run M1 from `repo\biology-studio\tools\m1-bakeoff` from then on.
- [ ] **Run the M1 kit** (see Next 1). Keep the laptop plugged in; Cycles is the long part.
- [ ] **T1** after clips are in Drive.
- [x] Re-paste `claude/INSTRUCTIONS.md` §6 into Project → Custom instructions — done 17 Nov (D-022 version, checked: matches §6).
- [ ] Optional: rename the Drive folder Embryo Studio → Biology Studio (then tell a chat so the docs follow).
- [ ] Optional: download the free 3D Atlas of Human Embryology PDFs (3dembryoatlas.com) to Drive › research/ — reference only (also needed for the M1 G-Sci look check vs R01 CS7).
- [ ] Rich plan artifact still shows the old name and lacks X1/K1/playbook — next ideation chat that can edit it updates it.
- [ ] "GitHub projects added" (owner, 17 Nov): still not found — share the links so they join the registry § Tools.
