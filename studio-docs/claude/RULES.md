# Rules

*(Purpose: the non-negotiables. Updated: 22 Nov 2026 · Bio · Build · V3 trace a cell — B2 masked stamp also for a trace drill that asks when (D-075). Before: 22 Nov 2026 · Bio · Fix · open-run first — I8 (8) open run first. Before: 21 Nov 2026 · Bio · Build · H2 reviewer mode — I2 build-log lines end with a plain line (D-061). Before: 21 Nov 2026 · Bio · Build · V2 3D drills — B2 masked-day exception for the day drill (D-054). Before: 20 Nov 2026 · Bio · Fix · Visual style 2 port — D8 media tags/credits, Part chip, legend, honesty tags; G4 real media CC0/PD/CC BY; A2 segment + media ids; D6 real imaging per visual-style §16 (D-046). Before: 20 Nov 2026 · Bio · Build · Visual style commit — D8 chapter titles (D-041). Before: 19 Nov 2026 · Bio · Build · W1 progress map — I2 + I3 point to `build/steps.json`, I5 `tracker` area (D-040). Before: 18 Nov 2026 · doc reconcile — C13, H8, I5 `layout` (D-033).)*

Non-negotiables. To change one, log a decision in `claude/DECISIONS.md` first. How-to and craft standards behind §H: `build/studio-playbook.md`.

## A. Data & progress
- **A1.** Never break saved progress. State lives in IndexedDB `biostudio` (D-015). Only **add** fields and back-fill them on load.
- **A2.** Card, episode, scene, segment and media-ledger ids are permanent once shipped. Fix wording freely; never renumber or reuse. A retired item keeps its id and is hidden.
- **A3.** Before any deploy that touches state or content data, tell the owner to tap **Export backup**.
- **A4.** Views must cope with old data (missing new fields).

## B. Accuracy & curriculum
- **B1.** Every fact in a card or script cites a book section (`E05.02`). Uncited or low-confidence lines are marked **≈**; nothing with a ≈ line is marked final.
- **B2.** Scale and time are on screen whenever a 3D view or shot shows an embryo ("day 17 · ~1.5 mm"). Deliberate distortions are labelled ("not to scale", "colours illustrative"). One exception: while a *Which day is this?* drill — or a *Trace a cell* drill that asks *when* (`mask_day`, D-075) — is open, the day/stage/size stamp is masked until it is answered (the scale bar stays) — D-054.
- **B3.** Germ layers use fixed tokens only — `--g-epi`, `--g-hypo`, `--g-ecto`, `--g-meso`, `--g-endo`, `--g-crest`, plus `--g-ctx` for non-layer tissue — each with a pattern and a label (colour-blind safe; values D-031). Never hard-code their colours. The one accent `--accent` means "look here": a ring/outline + label, never a fill alone and never a layer colour.
- **B4.** Card statuses: Read → Understood (Check passed) → Can explain. Card Checks set status; episode quizzes count for streak and recall stats only.
- **B5.** Episodes tag cards **core** (×2) or **support** (×1). Tags to unwritten cards show "Coming in Tier X". Ready to watch = weighted share Understood; it never blocks.
- **B6.** Langman 14e is the primary source; every fact cites its book section. Outside sources come only from `research/source-registry.md` and are cited after the section: `[E05.02 · R01 CS8]` (D-011).
- **B7.** Every fact line carries a confidence mark: **✔✔** book + Tier 1 agree · **✔** book only · **⚑** book vs Tier 1 disagree · **✚** beyond the book (Tier 1 only) · **≈** blocks final. Tier A cards aim for ✔✔. A ⚑ gets a DECISIONS entry — never silently resolved; the card gives the book answer and a "Newer evidence" line in More. ✚ lives only in More or Tier D, labelled "beyond Langman". Tier 2–3 sources can't create ⚑ or ✚.
- **B8.** A chapter's research dossier (`research/dossiers/`) exists before its cards are drafted; teaching choices follow `research/teaching-methods.md`.
- **B9.** No chapter's cards are drafted before its rows exist in `curriculum/concept-map.md` (K1, D-017). New books or topics follow the same order: ingest/intake → index → research → map → cards (D-015).
- **B10.** Every episode is made for a stated **audience profile** (level, depth, type, format, length, language — D-016) and must still make sense to a non-medical viewer at its General cut: plain-language hook, terms explained on first use.

## C. Engine & code
- **C1.** New features are opt-in; existing content behaves exactly as before.
- **C2.** `docs/card-spec.md` and `docs/scene-spec.md` are the only definitions of their formats. Change the spec first, then the code.
- **C3.** Validators must pass before content ships: card-check (citations, confidence marks, length, terms, one right answer) and scene-check (scale label, tokens, day keys).
- **C4.** Build only on **Measured** numbers in `build/pipeline-reference.md` (devices, renders, voice, streaming).
- **C5.** Light code: no bundler, plain scripts, hand-written SVG charts. **three.js is the one heavy library**, pinned and vendored (D-006, decided D-019); glTF (.glb) is the 3D exchange format.
- **C6.** After a deploy, tell the owner to hard-refresh (or re-add the home-screen app). Bump `?v=` on changed files.
- **C7.** Commit to `main` with a clear message; add a line to `logs/build-log.md`.
- **C8.** **Layout check before every UI deploy:** no overlap or overflow; taps ≥ `--tap`; text ≥ `--fs-min`; nothing fixed over controls; Android Back stays in the app. 13 sizes (matrix: `build/design-plan.md` §2), portrait + landscape, + 125 % text — run by `tools/layout-check`.
- **C9.** When the claude.ai Studio copy is affected, rebuild and republish it in the same step (or leave an owner reminder if this chat can't).
- **C10.** **Keep the Guide true** (once G1 exists): a behaviour change updates its How page, tour steps and What's new in the same step.
- **C11.** **Still regression:** a viewer or scene change re-renders every shipped card's still and compares; differences must be intended.
- **C12.** **Local-first** (D-014): render, encode, voice and AI-model steps are written to run on the owner's NVIDIA laptop (GPU paths: OptiX/CUDA, NVENC). A step that needs an online service says why and names the free option first.
- **C13.** **Optimal on every device (D-033 — owner standing rule).** Every UI (app, explorer, Studio, any artifact) and every viewer-facing output gets a designed layout — not just a working one — on phone, tablet and desktop, portrait and landscape: five classes `dev-p / pl / tp / tl / d`, the layout per screen and the test matrix in `build/design-plan.md` §2 (→ `build/design-plan.md` after A0). Layouts change by class (panes, rails, drawers, side panels), never by stretching; touch and mouse/keyboard are both first-class; rotating never loses place. A UI step is not done until `tools/layout-check` is green for all classes and G-Art has passed its contact sheet; owner checks run on phone, tablet and laptop.

## D. Teaching & story
- **D1.** Shape before names: show the fold, then label it.
- **D2.** One idea per beat; at most 3 new terms per minute of video and per card.
- **D3.** Every episode opens with a question or a clinical mystery and answers it by the end.
- **D4.** Anchor to the adult: "this becomes…" in the same episode or card.
- **D5.** Accuracy beats drama: a metaphor never changes what happens biologically.
- **D6.** Clinical content is factual and humane: diagrams by default; real imaging only per build/visual-style.md §16; never shock images.
- **D7.** Every season has a recap / "connect the dots" episode across chapters.
- **D8.** On-screen text is labels, day, scale, B2 disclaimers and honesty tags, **chapter titles of 4 words or fewer** (Shorts, D-041), **media tags + credits, the Part chip and the colour legend** (D-046; build/visual-style.md §10–§15); the voice carries the sentences; a label sits on its structure as it is named (teaching methods 4–5). Captions/subtitles are accessibility text, not on-screen text (H5).
- **D9.** Folding and layer shots end on the cross-section view learners meet in exams (teaching method 10).

## E. Docs
- **E1.** One owner doc per fact (`claude/INSTRUCTIONS.md` §2).
- **E2.** Dates are absolute (17 Nov 2026), never "yesterday".
- **E3.** End-of-chat duties apply (`claude/INSTRUCTIONS.md` §4).

## F. Free first (D-013)
- **F1.** Every step uses free tools by default: GitHub Pages/Actions, Google Drive + free Cloud APIs, Blender, three.js, free/local TTS, ffmpeg, open models run locally, the owner's Claude plan through Studio.
- **F2.** A paid option may be **suggested** only when it is clearly better: name it, its cost, what it adds, and the free alternative. Nothing paid is used until the owner approves and a D-entry logs it.
- **F3.** If the free route needs something built, build it or guide the owner step by step.
- **F4.** Licences still apply to free tools and models: check before use; non-commercial models stay on the owner's devices, credited, never copied into the repo.

## G. Copyright
- **G1.** No book sentences, figures, tables or page images in the repo, app or videos.
- **G2.** Facts are restated in our own words with a section citation; every visual is our own 3D or diagram (except G4's licensed assets).
- **G3.** Page photos may be used in Studio for analysis only; the output is never a reproduction.
- **G4.** Third-party assets only with an approved licence (MIT/Apache/CC-BY; for real images and footage CC0, CC BY or public domain only — never CC BY-SA, build/visual-style.md §16, D-046), credited and logged. **One exception (D-021):** Z-Anatomy adult meshes (CC BY-SA, registry T07) may appear in rendered video only; such a video is released CC BY-SA 4.0 with the credit line from D-021; the meshes never enter the repo or app.
- **G5.** Sources marked NC, ND or "no reuse" (registry Licence column) are **reference only**: look, then draw our own. Never trace, import, screenshot or quote at length.

## H. Production craft & review (D-020; details in `build/studio-playbook.md`)
- **H1.** Every card and every episode beat has one testable **learning objective**; its Checks test that objective.
- **H2.** **Review gates:** an artefact ships only after its gates pass — G-Sci, G-Learn, G-Story, G-Art, G-Eng, G-A11y (playbook §2) — and the next build waits for G-Owner. A **different role** reviews than the one that made it; cards, scripts and public outputs get a fresh-eyes reviewer.
- **H3.** **Animatic before render:** no final render until a three.js animatic with scratch voice has passed G-Sci, G-Story and G-Art.
- **H4.** **Orientation always:** every 3D shot shows axes (cranial/caudal, dorsal/ventral), scale and day/stage (with B2).
- **H5.** **Accessibility:** captions + transcript on every video; WCAG AA contrast; colour never the only cue; no flashing above 3/s; reduced-motion option.
- **H6.** **Sound:** narration 130–150 wpm; pronunciation dictionary; music never under key sentences; about −14 LUFS integrated, true peak ≤ −1 dBTP.
- **H7.** **Reproducible outputs:** every render writes a manifest (scene hash, tool + version, GPU, settings, seed, voice version); published files are never overwritten — bump the version.
- **H8.** **Performance budgets** (until Measured replaces them): phone scene ≤ 150k triangles and ≤ 2 MB at ≥ 30 fps; app first load ≤ 3 s on 4G; 720p episode ≤ 12 MB/min. Tablet/desktop extras (richer 3D detail, 1080p rung) only once Measured (C13).
- **H9.** **AI disclosure:** AI-generated material is credited as such and never carries anatomy without passing G-Sci.
- **H10.** **Licence ledger:** every library, model and asset used is listed with its licence in the repo's `THIRD_PARTY.md` (and the registry Tools section).

## I. Usage, upkeep & editability (D-022 — owner standing rule)
- **I1. Optimise for usage.** One step per chat; read only the docs the step needs (INSTRUCTIONS §2); point to docs by path, never paste them. Claude proactively says **"start a new chat"** — with a ready prompt + chat name — when the step is done, the topic changes, or the chat gets long (~25 turns or many large reads).
- **I2. Docs always current, in the same chat.** Every change updates, before the chat ends: **update `build/steps.json`** (step status, gates, check, last log line, to-dos, owner inputs; then `tools/tracker/check.py --write`, D-040), STATUS (now · next · lock), `logs/build-log.md` (**changelog**; each line ends with `<!--plain: one sentence a non-builder understands-->` — Reviewer mode › Updates shows it, D-061), DECISIONS, the owner doc (plan, glossary, registry, backlog, checklist, catalog, pipeline reference…) and the README doc map if a doc is added or renamed. A stale doc is a bug: fix it when found.
- **I3. One place for each list.** Step status, dependencies, pendencies, owner inputs and the schedule data — calendar, plan order, estimates, runs → `build/steps.json` only (D-040, D-063; dates are computed, never stored; STATUS keeps now · next · lock). Ideas → `build/ideas-backlog.md` only. History → build log only. Terms → GLOSSARY only. Superseded text is removed (history lives in the log and DECISIONS), not left beside the new.
- **I4. Every doc says what it is.** First lines: one-line purpose + `Updated: <date> · <step/chat>`. Added the next time a doc is touched.
- **I5. Debug flags everywhere, off by default.** App: `?debug=1` or per area `?debug=map,viewer,sync,audio,layout,studio,tracker` (one module `src/js/01-debug.js`; overlay shows version, ids, fps, triangles, state size, device class; logs tagged `[area]`); `?test=1` testing mode. Tools: every script takes `--dry-run`, `--debug`, `--only <id>`, `--preview` (low-res, fast). Scenes: `debug: true` shows axes and bounding boxes. Debug never shows in published videos or the default app.
- **I6. Edit hooks.** Every changeable value has one home: look in `:root` tokens (`app.css`), settings in `src/js/02-config.js`, content in `content/<book>/…` data (never in code), UI words in `content/strings.js`. Code marks edit points with `// EDIT:` and each file starts with purpose + owner doc. In testing mode, a ✎ on any card, scene, episode or map node shows its id and file path and copies a ready "edit this" prompt.
- **I7. No confusion.** One name per thing (GLOSSARY), fixed file/id patterns (README), owner doc wins on conflict and the other doc is fixed in the same chat. If a request is ambiguous or conflicts with a rule or decision, Claude says so and asks before acting.

- **I8. Shared working (D-025).** Two people (owner + collaborator) share one project. (1) **Build lock:** a Build chat first checks STATUS § Lock; if free it writes `Build lock: <name> · <chat name> · <date, time IST>`, and releases it (`free`) at the end; held by the other person → no build, offer Ideation/Research/Review instead; a lock older than 24 h → ask the holder. (2) Code: `git pull` before, commit + push after; never commit `out/`, `apps/`, `models/` or book material. (3) Log lines and review entries name who (`· by <name>`). (4) The owner decides: collaborator chats may log D-entries only as *proposed*; G-Owner is the owner's. (5) The book PDF is per person and never shared (RULES §G); only derived data is shared. (6) **Docs live only in the repo** `aaditya-verma/biology-studio` › `studio-docs/` (D-027). A chat changes a doc **only by a git commit** to `main` — route A (chat pushes from its own workspace) or B (chat writes into the laptop clone, the person runs `sync.bat`), exactly as `build/setup-guide.md` §6a says; never by uploading to Project knowledge or a Projects-tool write (that makes an unsynced duplicate). No route → handoff note (templates §10). Press **Sync now** before every chat and after every push. Never force-push; merge both people's lines. (7) Paths: say "Studio home" (any folder), not one person's drive letter. (8) **Open run first:** every chat that works on a step (any type, lock or not) adds its open run to that step in steps.json right after the start checks and pushes it (route A), or tells the owner to run sync.bat now (route B), before any other work. A 'next steps' answer checks open runs and asks the owner what is running before suggesting a step.
