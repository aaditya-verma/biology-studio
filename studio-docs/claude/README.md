# Biology Studio — Start here

*(Purpose: what this project is, the doc map and id formats. Updated: 22 Nov 2026 · Bio · Build · L2 lessons (doc map: `docs/lesson-spec.md`). Before: 21 Nov 2026 · Bio · Build · W2 scheduler (steps.json schedule data). Before: 21 Nov 2026 · Bio · Build · L1 learning core (ⓘ mark). Before: 20 Nov 2026 · Bio · Fix · Visual style 2 port — visual-style line extended; `content/E/segments.json` (D-046). Before: 20 Nov 2026 · Bio · Build · Visual style commit — build/visual-style.md in the doc map (D-041). Before: 19 Nov 2026 · Bio · Build · W1 progress map — steps.json in the doc map, W + progress-map ids, `tracker` debug area. Before: S1 studio — docs/card-spec.md in the doc map. Before: 19 Nov 2026 · Bio · Build · V1 viewer — docs/scene-spec.md in the doc map. Before: 18 Nov 2026 · Bio · Build · A0 shell — design-plan added to the doc map.); `layout` debug area (D-033). Renamed from "Embryo Studio", D-015.)*

An engine that takes a book or a biology topic, indexes it, maps its concepts, checks them against trusted outside sources, turns them into concept cards and story-led 3D explainer videos (voice-over + subtitles), and helps the learner remember them. **First book: Langman's Medical Embryology, 14th edition** (429 pp, 21 chapters in 3 parts). Other books and topics follow the same pipeline (D-015). We work like a small science-animation studio: a lead biology researcher who is also designer, teacher and storyteller, with a team of engineers (`build/studio-playbook.md`, D-020). Lean on usage, docs always current, debug flags and edit hooks everywhere (RULES §I, D-022).

| | |
|---|---|
| **Owner** | Aaditya (personal project, executive producer; final say, logs decisions, passes G-Owner). Way of working copied from the Drums project (DrumPath). |
| **Collaborator** | The Professor — same project, own Windows + NVIDIA laptop; collaborator chats propose, the owner decides (D-025). Setup: `build/setup-guide.md`. |
| **Audience** | Mainly medical students; every episode also works for non-medical viewers. Level, depth, type, format, length, language (English default) and host (cell/embryo character default) set per request (audience profile, D-016, D-032). |
| **Quality bar** | The owner's reference reels QR01/QR02 — cinematic look, character + humour, local language, short-form pacing; science shots stay exact (D-032, `research/quality-references.md`). |
| **Devices** | Every screen and output designed for phone, tablet and desktop, portrait + landscape (D-033, RULES C13, `build/design-plan.md` §2). |
| **Machines** | Laptop 1 = owner's NVIDIA gaming laptop (Studio home `D:\Projects\biology_studio`); Laptop 2 = the Professor's (Windows + NVIDIA, any Studio home). Local-first rendering, voice and AI (D-014). Phone/tablet to watch and study. |
| **Books** | Langman 14e PDF — per person: each uses their own licensed copy in a private Drive `book/` folder (owner's uploaded 17 Nov 2026), never shared, never in the repo, app or videos (D-005, D-025). Only derived data is shared. The owner's PDF has no Index pages (D-026). |
| **Sources** | Book is the spine; human-embryo atlases, peer-reviewed papers and the NMC curriculum confirm, correct and add depth (D-011). |
| **Cost** | Free first; paid only suggested, owner approves (D-013). |
| **App** | Not built yet. One app, two homes — GitHub Pages viewer (PWA, three.js) + claude.ai Studio (D-003, D-006); media on Drive (D-008). Repo `biology-studio`. |
| **Status** | Live progress map: https://aaditya-verma.github.io/biology-studio/#progress (data `build/steps.json`); now · next · lock in `claude/STATUS.md`. |

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
- `research/quality-references.md` — the owner's reference reels (QR01, QR02): measured, what makes them work, what we adopt (D-032). Files in Drive › research/quality-refs/ (reference only).
- `research/dossiers/` — one per chapter, written in X1 before its cards. First: `ch05-gastrulation.md`.

### Curriculum (what to learn)
- `curriculum/concept-map.md` — every chapter → section → concept (314), with crosstabs; built by `tools/map/` with `content/E/map.json`. Explorer: https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin.
- `curriculum/roadmap.md` — waves → seasons → episodes covering every core and exam-high concept (built by `tools/map/roadmap.py`).
- `curriculum/book-index-part1.md` — I1 section index, Part 0 orientation + Chapters 1–9; Ch 5 draft cards.
- `curriculum/book-index-part2.md` — I1 section index, Chapters 10–21, with dependencies on Part 1.
- `curriculum/episodes-catalog.md` — episodes, card tags, audience profiles, unlock counts, gaps.

### Build (how it is made)
- `build/master-plan.md` — the master build plan (scope, steps, ready prompts). Rich version with flowcharts: https://claude.ai/artifact/92iZDWeXzzA9GcNcru2ZwK (not yet showing X1/K1, the playbook, the host, the device layouts or the new name).
- `build/studio-playbook.md` — crew roles, 7 review gates, craft standards (research, teaching, story, host + Short profile §5b, visual, sound, accessibility, engineering), production pipeline, Definition of Done, metrics.
- `build/visual-style.md` — how our videos look: Short + Lesson formats, segment colours, labels, media, licences (D-041, D-046). Segment colours data: `content/E/segments.json` (format: `docs/scene-spec.md` §10).
- `build/design-plan.md` — the app's design system: tokens (D-031/D-034), device classes + layout per screen (moved from master plan §8a), shell, addresses, screens, storage, testing mode, ✎ hooks, `tools/layout-check`.
- `build/pipeline-reference.md` — Expected vs **Measured** numbers (laptop, phone, tablet, desktop, renders, voice). Build only on Measured.
- `build/steps.json` — **progress map data**: every step's status, needs/unblocks, gates, owner check, D-ids, last log line, to-dos and owner inputs (D-040) and the **schedule data** — calendar, plan order (`queue`), estimates, resource rows, runs (D-063); dates are computed by `src/js/17-plan.js` = `tools/tracker/check.py plan()`, shown at `#progress=plan` and by `check.py --next`. Drawn at https://aaditya-verma.github.io/biology-studio/#progress; checked by `tools/tracker/check.py` (format: `tools/tracker/README.md`).
- `build/owner-test-checklist.md` — owner checks T1… (steps per check; open/pass state lives in steps.json)
- `build/setup-guide.md` — set up a second laptop + person: accounts, invites, own book, Claude Project, tools, daily working, troubleshooting (D-025).
- `build/ideas-backlog.md` — parked ideas, the only place for them (no pick before the use gate).
- `docs/scene-spec.md` (repo root `docs/`) — the 3D scene format (V1, RULES C2).
- `docs/card-spec.md` — the concept card format: one JSON per concept id in `content/E/cards/`, cites, marks, gates, card-check (S1, RULES C2).
- `docs/lesson-spec.md` — the lesson format: one lesson per chapter in `content/E/lessons/<ch>.json`, sittings, steps, time model, lesson-check `tools/lesson-check/` (L2, RULES C2, D-070). Later: `build/studio-brief.md`.
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
- **Concept:** `<book><ch>.<sec>.<nn>` — `E05.02.01` (a concept in the map becomes a card with the same id). Part 0 orientation: `E00.01.01`. Rows live in `tools/map/concepts.txt`; add new concepts at the end of their section.
- **Term:** `<book>.t.<slug>` — `E.t.primitive-streak` (glossary term, I1 `terms.json`).
- **Episode:** `S<season>E<nn>` — `S1E01`; cuts for other audience profiles add a suffix: `S1E01-gen`, `S1E01-short`; other languages add the language: `S1E01-short-hi`.
- **Scene:** `sc-<card id>` or `sc-<episode>-<shot>` — `sc-E05.02.01`, `sc-S1E01-03`.
- **Carnegie stage:** `CS01`–`CS23`.
- **Page locator:** printed page number (`p. 61`); I1 JSON also keeps the PDF page (Langman: printed = PDF − 19).
- **Source:** `R00`–`R39` (registry); tools `T01`…; teaching evidence `M01`…; quality references `QR01`…; citation `[E05.02 · R01 CS8]`.
- **Confidence marks:** ✔✔ book + Tier 1 agree · ✔ book only · ⚑ disagree (logged) · ✚ beyond the book · ≈ blocks final · ⓘ how the app works (guide cards only, `APP <screen>` cite, D-050).
- **Review gates:** G-Sci · G-Learn · G-Story · G-Art · G-Eng · G-A11y · G-Owner (playbook §2).
- **Decision:** `D-001`… · **Owner check:** `T1`, `T1b`… · **Build step:** `M0, R0, M1, M1b, H1, I1, K1, X1, A0, V1, S1, W1, C1, P1, R1, L1` (W = progress map, D-040).
- **Progress-map step ids** (`build/steps.json`): the build steps above · `X1.<ch>` research per chapter (`X1.07`) · `GATE` use gate · `D1` `G1` after the gate · `IB<nn>` parked backlog idea = backlog item number (`IB01`) · Ideation rows `PB` playbook · `UR` usage rule · `QB` quality bar · `DR` device rule. **Owner input:** `<step>.q<n>` (`C1.q1`).
- **Chat name:** `Bio · <Type> · <Step or id>` — types: Ideation · Research · Build · Content · Episode · Review · Fix.
- **Debug areas:** `map · viewer · sync · audio · player · deck · studio · tracker · layout` (`?debug=map,viewer`); add new areas here. The explorer artifact uses `#debug` (artifact links are plain `#name`: `#c-E05-01-02`, `#x-layer-day`). Tool log tags: `[map]` `[pdf] [tree] [terms] [xrefs] [timeline]`.

Ids are permanent once shipped: never renumber or reuse (RULES A2).

**Depth tiers:** A Foundation · B MBBS exam · C NEET-PG / clinical · D molecular.
**Audience levels:** General · School · NEET · MBBS · PG.
**Languages:** English (`en`, default) · Hinglish (`hien`) · Hindi (`hi`).
**Hosts:** cell/embryo character (default) · animal · stylised human · none.
**Threads:** T timeline · G germ layer · F folding/shape (the spiral strand) · S system · M molecular · C clinical · A adult anatomy.
