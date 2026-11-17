# Status — updated 17 Nov 2026

*(Purpose: current state + all pendencies — nothing else. Updated: 17 Nov 2026 · Bio · Build · H1 shared repo. Finished work lives in `logs/build-log.md`.)*

## Lock
- Build lock: Aaditya · Bio · Build · K1 concept map · 17 Nov 2026, 09:50 IST *(RULES I8)*
- H1: released 17 Nov 2026 (free). K1's build is finished; its end-of-chat doc updates are still to be committed (route A, setup guide §6a), and that commit releases the K1 line above.

## Now
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
3. **K1 wrap-up** — in the K1 chat: commit its doc updates (STATUS, build log, DECISIONS, README map, master plan, concept map, roadmap) to the repo by route A, then release its lock. `concept-map.md` + `roadmap.md` were copied in by H1 at 10:12 IST; K1's commit overwrites them with its final versions.
4. **T1** (owner, phone) once clips are in Drive → pick from D-024.
5. **X1 Research · Ch 5** → **A0** (incl. debug + edit hooks) → **V1** (seed: kit's `shot.json` + `scene_math.py`) → **S1** → **C1** → **P1 S1E01** (with animatic) → **R1** → **L1** → **use gate**.

## Blocked / open questions (pendencies)
- **M1 numbers** — blocked on the laptop run (this chat's bridge can't run commands; cloud workspace has no GPU).
- **I1 known gaps (fix in K1/X1, small):** the PDF has no Index pages (terms placed by text search, D-026) · Day 27 missing from the timeline (OCR) · Table 8.1 has 5/8 rows (OCR) — finish by hand · 3 glossary terms unplaced (annulus fibrosis, fossa ovalis, peritoneal ligaments) · Carnegie stage column empty → X1 fills from registry sources (GLOSSARY §7) · some page ranges are OCR-based (≈), e.g. Ch 12 has only 2 ■ sections.
- Germ-layer token colours: kit uses Okabe–Ito placeholders (epiblast/hypoblast have no token yet) — settle in V1/A0.
- Accent colour — open (needed by A0).
- ⚑ watch: notochord formation order (dossier ch05 §2) — resolved in X1. The M1 shot leaves the notochordal process out on purpose.
- M1 shot values (sizes, streak length) are ≈ until X1 cites the book.
- **D-025 (c)** still proposed: Professor as human G-Sci reviewer? (a) decided, (b) rejected → D-027.
- Professor's name, Google address and **GitHub username** — needed for invites (repo: Settings → Collaborators → Add people).
- `THIRD_PARTY.md` licences are ≈ — check each against its licence file before A0.
- Laptop: after cloning the repo into `repo\biology-studio\`, the old `tools\` + `content\` in Studio home are retired (keep `out\`).
- Google Cloud project "Biology Studio" not created yet; add the Professor as an OAuth test user when it is (D1).

## Owner reminders
- [ ] **Skim the I1 section tables** on your phone (`curriculum/book-index-part1.md`, `-part2.md`) — anything that looks wrong, say so before K1 uses the ids (I1 owner check: summary skim).
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
