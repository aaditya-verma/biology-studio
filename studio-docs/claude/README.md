# Biology Studio — Start here

*(Purpose: what this project is, the doc map and id formats. Updated: 17 Nov 2026 · Bio · Build · H1 shared repo (repo layout). Renamed from "Embryo Studio", D-015.)*

An engine that takes a book or a biology topic, indexes it, maps its concepts, checks them against trusted outside sources, turns them into concept cards and story-led 3D explainer videos (voice-over + subtitles), and helps the learner remember them. **First book: Langman's Medical Embryology, 14th edition** (429 pp, 21 chapters in 3 parts). Other books and topics follow the same pipeline (D-015). We work like a small science-animation studio: a lead biology researcher who is also designer, teacher and storyteller, with a team of engineers (`build/studio-playbook.md`, D-020). Lean on usage, docs always current, debug flags and edit hooks everywhere (RULES §I, D-022).

| | |
|---|---|
| **Owner** | Aaditya (personal project, executive producer; final say, logs decisions, passes G-Owner). Way of working copied from the Drums project (DrumPath). |
| **Collaborator** | The Professor — same project, own Windows + NVIDIA laptop; collaborator chats propose, the owner decides (D-025). Setup: `build/setup-guide.md`. |
| **Audience** | Mainly medical students; every episode also works for non-medical viewers. Level, depth, type, format, length and language set per request (audience profile, D-016). |
| **Machines** | Laptop 1 = owner's NVIDIA gaming laptop (Studio home `D:\Projects\biology_studio`); Laptop 2 = the Professor's (Windows + NVIDIA, any Studio home). Local-first rendering, voice and AI (D-014). Phone/tablet to watch and study. |
| **Books** | Langman 14e PDF — per person: each uses their own licensed copy in a private Drive `book/` folder (owner's uploaded 17 Nov 2026), never shared, never in the repo, app or videos (D-005, D-025). Only derived data is shared. The owner's PDF has no Index pages (D-026). |
| **Sources** | Book is the spine; human-embryo atlases, peer-reviewed papers and the NMC curriculum confirm, correct and add depth (D-011). |
| **Cost** | Free first; paid only suggested, owner approves (D-013). |
| **App** | Not built yet. One app, two homes — GitHub Pages viewer (PWA, three.js) + claude.ai Studio (D-003, D-006); media on Drive (D-008). Repo `biology-studio`. |
| **Status** | I1 index done; H1 repo live (17 Nov 2026); M1 bake-off run pending; K1 concept map in progress. See `claude/STATUS.md`. |

---

## Doc map
*(Every doc is listed here. Adding or renaming one updates this map in the same chat — RULES I2.)*

### Read first (routers — keep short)
- `claude/README.md` — this page.
- `claude/INSTRUCTIONS.md` — how every chat works: crew roles, owner per fact, chat types, when to start a new chat, end-of-chat duties. §6 = custom-instructions paste.
- `claude/RULES.md` — non-negotiables (§H craft and review gates; §I usage, upkeep, debug flags, edit hooks).
- `claude/STATUS.md` — now · next · **pendencies** · owner reminders (current only).

### Reference
- `claude/DECISIONS.md` — dated decision log. Check before reopening a question.
- `claude/GLOSSARY.md` — terms by thread, "Don't confuse" pairs, production, app and project terms, Carnegie table.

### Research (what we trust and how we teach)
- `research/source-registry.md` — trusted sources and tools by tier, licences, citation + confidence marks.
- `research/teaching-methods.md` — learning-science evidence → design rules; episode checklist.
- `research/dossiers/` — one per chapter, written in X1 before its cards. First: `ch05-gastrulation.md`.

### Curriculum (what to learn)
- `curriculum/concept-map.md` — *(K1)* every chapter → subheader → concept, with crosstabs; source for the clickable explorer.
- `curriculum/roadmap.md` — *(K1)* step-by-step order to cover all important concepts.
- `curriculum/book-index-part1.md` — I1 section index, Part 0 orientation + Chapters 1–9; Ch 5 draft cards.
- `curriculum/book-index-part2.md` — I1 section index, Chapters 10–21, with dependencies on Part 1.
- `curriculum/episodes-catalog.md` — episodes, card tags, audience profiles, unlock counts, gaps.

### Build (how it is made)
- `build/master-plan.md` — the master build plan (scope, steps, ready prompts). Rich version with flowcharts: https://claude.ai/artifact/92iZDWeXzzA9GcNcru2ZwK (not yet showing X1/K1, the playbook or the new name).
- `build/studio-playbook.md` — crew roles, 7 review gates, craft standards (research, teaching, story, visual, sound, accessibility, engineering), production pipeline, Definition of Done, metrics.
- `build/pipeline-reference.md` — Expected vs **Measured** numbers (laptop, phone, renders, voice). Build only on Measured.
- `build/owner-test-checklist.md` — owner checks T1…
- `build/setup-guide.md` — set up a second laptop + person: accounts, invites, own book, Claude Project, tools, daily working, troubleshooting (D-025).
- `build/ideas-backlog.md` — parked ideas, the only place for them (no pick before the use gate).
- Later: `build/studio-brief.md`, `build/design-plan.md`, `docs/card-spec.md`, `docs/scene-spec.md`.
- **Repo** `aaditya-verma/biology-studio` (private until A0, D-027): `studio-docs/` (these docs — the only copy) · `tools/indexer/` (I1 script + `books/<code>.json` + README) · `content/E/index/` (I1 JSON: tree, terms, xrefs, timeline, report) · `tools/m1-bakeoff/` · `sync.bat` (one-click git pull/commit/push) · `THIRD_PARTY.md` (H10). Laptop clone: `<Studio home>\repo\biology-studio\`; the old `tools\` and `content\` folders in Studio home are retired after the clone (outputs in `out\` stay).

### Logs and templates
- `logs/build-log.md` — the **changelog**: what changed, newest first.
- `logs/review-log.md` — what the owner noticed while watching/using.
- `templates/templates.md` — handoff, card, episode, review, bug, decision, research dossier.

---

## Id formats (used everywhere — this doc owns them)
- **Book code:** one letter per book. `E` = Langman's Medical Embryology 14e. New books get the next free code here before indexing (then a `tools/indexer/books/<code>.json`).
- **Chapter:** `<book><ch>` — `E05` (chapters numbered 01–21 in book order).
- **Section:** `<book><ch>.<sec>` — `E05.02`, numbered by I1: `.00` = chapter opener (text before the first ■ heading); `.01…` = each ■ heading in book order; Summary and Problems to Solve are the last two. Boxes (Clinical Correlates, Molecular Regulation) and smaller subheads are not numbered — they belong to their section. Full list: `curriculum/book-index-part1.md` / `-part2.md`. The indexer warns if a re-run would change any section id.
- **Concept:** `<book><ch>.<sec>.<nn>` — `E05.02.01` (a concept in the map becomes a card with the same id). Part 0 orientation: `E00.01.01`.
- **Term:** `<book>.t.<slug>` — `E.t.primitive-streak` (glossary term, I1 `terms.json`).
- **Episode:** `S<season>E<nn>` — `S1E01`; cuts for other audience profiles add a suffix: `S1E01-gen`, `S1E01-short`.
- **Scene:** `sc-<card id>` or `sc-<episode>-<shot>` — `sc-E05.02.01`, `sc-S1E01-03`.
- **Carnegie stage:** `CS01`–`CS23`.
- **Page locator:** printed page number (`p. 61`); I1 JSON also keeps the PDF page (Langman: printed = PDF − 19).
- **Source:** `R00`–`R39` (registry); tools `T01`…; teaching evidence `M01`…; citation `[E05.02 · R01 CS8]`.
- **Confidence marks:** ✔✔ book + Tier 1 agree · ✔ book only · ⚑ disagree (logged) · ✚ beyond the book · ≈ blocks final.
- **Review gates:** G-Sci · G-Learn · G-Story · G-Art · G-Eng · G-A11y · G-Owner (playbook §2).
- **Decision:** `D-001`… · **Owner check:** `T1`… · **Build step:** `M0, R0, M1, H1, I1, K1, X1, A0, V1, S1, C1, P1, R1, L1`.
- **Chat name:** `Bio · <Type> · <Step or id>` — types: Ideation · Research · Build · Content · Episode · Review · Fix.
- **Debug areas:** `map · viewer · sync · audio · player · deck · studio` (`?debug=map,viewer`); add new areas here. Tool log tags: `[pdf] [tree] [terms] [xrefs] [timeline]`.

Ids are permanent once shipped: never renumber or reuse (RULES A2).

**Depth tiers:** A Foundation · B MBBS exam · C NEET-PG / clinical · D molecular.
**Audience levels:** General · School · NEET · MBBS · PG.
**Threads:** T timeline · G germ layer · F folding/shape (the spiral strand) · S system · M molecular · C clinical · A adult anatomy.
