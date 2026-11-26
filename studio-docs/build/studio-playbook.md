# Studio playbook — how the crew works, and the craft standards

*(Purpose: best practices, crew roles, review gates and Definition of Done. Created 17 Nov 2026, D-020. Updated: 26 Nov 2026 · Bio · Fix · video craft — §6b multimedia craft (ideas, signalling, primer), §2 MM checklist under G-Learn, G-Sci 10/14 point to MM2/MM3, §4.1 beat → idea (D-107). Before: 21 Nov 2026 · Bio · Build · M1b host results — §5b(3) figure/ground + loudness checks on every host render (D-051). Before: 20 Nov 2026 · Bio · Build · M1b host shot (Step 2) — §5b(2) host colour + D5 host rules (D-048). Before: 20 Nov 2026 · Bio · Fix · Visual style 2 port — §2 G-Sci items 13–18, §5/§5b Explainer/MBBS → Lesson, §6.1 summary + §8.5 → visual-style §10–§16 (D-046). Before: 20 Nov 2026 · Bio · Build · Visual style commit — §2 G-Sci video checklist, §6.1 look summary → build/visual-style.md (D-041). Before: 18 Nov 2026 · Bio · Fix · doc reconcile — ported from the uploaded copy: host + Short profile §5b, cinematic look (D-032); designed per device §6.10, gates, DoD (D-033); §6.2 accent per D-031. RULES §H holds the musts; this doc holds the how. Evidence for teaching choices stays in `research/teaching-methods.md`; the quality bar's reference reels in `research/quality-references.md`; device classes and layouts in `build/design-plan.md` §2.)*

**Stance:** we work like a small science-animation studio. A lead biologist-researcher who is also designer, teacher and storyteller, with a team of engineers behind him. Facts first, clarity over realism, story for attention, measurement for truth.

---

## 1. The crew (who does what)
The owner is **executive producer**: sets direction, approves at gates, watches on real devices. Claude plays the crew roles below, one primary role per chat (INSTRUCTIONS §1), and a **different role reviews** before a gate passes.

| Crew role | Owns | Reviews |
|---|---|---|
| **Lead scientist** (subject expert) | Concept map, card facts, ⚑ calls, tiers | Scripts, scenes (anatomy) |
| **Research librarian** | Sources, dossiers, confidence marks, licences | Cards (citations) |
| **Learning designer** | Objectives, Checks, sequencing, Remember lines | Scripts, cards (pedagogy) |
| **Story director / writer** | Episode structure, hooks, voice, audience cuts, host character | Cards (clarity for General level) |
| **Art director** | Look, colour, camera grammar, typography, thumbnails, host design, layouts per device class | Scenes, storyboards, UI screens, layout contact sheets |
| **3D / technical artist** | Scenes, meshes, rigs, lighting, render settings | Viewer performance |
| **Pipeline TD** | Tools, render queue, manifests, encoding + renditions, Drive publish | Build steps touching media |
| **Front-end engineer** | App, explorer, viewer, PWA, storage, device classes | UI builds |
| **QA & accessibility** | Validators, layout sweep (all device classes, `tools/layout-check`), still regression, captions, contrast | Every gate |
| **Sound** | Voice, pronunciation dictionary, mix, loudness | Episodes |

**Fresh-eyes rule:** cards, scripts and anything going public get a review by a separate reviewer (a separate agent or a fresh chat) that did not write them, so the work never grades itself.

## 2. Review gates (every artefact passes the ones that apply)
| Gate | Question | Checked by | Blocks |
|---|---|---|---|
| **G-Sci** Science | Every fact cited + marked; no ≈; anatomy, timing, scale right vs book + R01/R02 | Lead scientist + librarian | Cards, scripts, scenes |
| **G-Learn** Learning | Objective stated; Checks match it; ≤ 3 new terms; teaching-methods checklist | Learning designer | Cards, episodes |
| **G-Story** Story | Hook in ≤ 10 s (≤ 1 s for Shorts); one question carried to payoff; General cut understandable | Story director | Episodes |
| **G-Art** Design | Hierarchy, colour semantics, orientation; readable and **designed for each device class** (phone, tablet, desktop; portrait + landscape — contact sheet, design plan §2); meets the QR01/QR02 look bar | Art director | Scenes, storyboards, host shots, UI |
| **G-Eng** Engineering | Tests green, `tools/layout-check` green on the design-plan §2 matrix, budgets met, reproducible build/render, nothing secret or copyrighted committed | Engineers + QA | Builds, renders |
| **G-A11y** Accessibility | Captions, contrast, colour-blind safe, no flashing, reduced motion, 125 % text, keyboard + touch reachable | QA | Everything shipped |
| **G-Owner** | Watches/uses on real devices — phone, tablet, laptop (owner checks Tn) | Owner | Next build (use gate) |

**G-Sci video checklist** (animatic and final; each item pass/fail + timestamp; the reviewer is not the maker and not the G-Art reviewer):
1. **Stage** — day/CS on screen match the dossier staging table (D-030/D-039 conventions); features fit that day (somite count, neuropores, folds).
2. **Scale** — scale bar matches the dossier value for that stage, cited with its CS; consistent across cuts; zooms are announced.
3. **Orientation** — cranial/caudal, dorsal/ventral, left/right correct; no mirror flips. Layer order dorsal → ventral: amnion · epiblast/ectoderm · mesoderm · hypoblast/endoderm · yolk sac. After folding, ectoderm outside, endoderm inside. Left-right cues: node at the cranial end of the streak; heart tube loops to the right.
4. **Topology** — layers stay continuous; cavity vs solid right; oropharyngeal and cloacal membranes shown as two layers only (ectoderm + endoderm, no mesoderm).
5. **Layer identity** — D-031 token colours. Definitive endoderm = ingressed epiblast cells displacing the hypoblast (never a hypoblast recolour); ectoderm = epiblast left after gastrulation; all three layers come from epiblast.
6. **Motion** — right direction (ingression through the streak, then lateral + cranial); plausible speed; no "stretch" where the process is proliferation or ingression. Folding: cephalocaudal + lateral (week 4); heart and septum transversum swing ventral-caudal; disc edges meet ventrally at the umbilical ring. Time compression shown on screen ("day 15 → 17"). Notochord middle-first (D-029) carries ⚑ and the book version (item 11).
7. **Counts** — somite pairs fit the day (dossier staging table); neuropore state fits the day; pharyngeal arches five, numbered 1, 2, 3, 4, 6 (5th absent or rudimentary — never shown), appearing cranial → caudal; arch arteries appear and regress in sequence, never all at once.
8. **Look-induced errors** (build/visual-style.md) — SSS doesn't imply a lumen; dust doesn't read as cells; depth of field doesn't blur the named structure; glow doesn't imply signalling unless labelled; graded layers within ΔE00 ≤ 8.
9. **Simplifications** — omissions listed in the shot sheet; "simplified / not to scale / colours illustrative" on screen where true (B2).
10. **Labels** — appear as the structure is shown (D8), point at the right thing, use GLOSSARY terms; timing + distance are measured by MM2/MM3 (below), not restated here.
11. **Citations** — every spoken fact has a section + mark; no ≈; a ⚑ gives the book answer.
12. **AI shots** — host only, no anatomy, credited (H9).
13. **Segment colours** — segment mode stated by the legend chip; each segment matches `content/E/segments.json` and the previous Part; splits/merges follow visual-style §11 at the right day; each segment and derivative has a cite + mark; colours change only by a morph.
14. **Labels + leaders** — every dot sits on the named structure (visual-style §12); placement and crossing are measured by MM2.
15. **Real media** — the image shows what the voice says (stage, view, structure); orientation + scale correct or "scale not given"; unaltered except logged edits; ledger row exists (visual-style §13, §16).
16. **Clinical link** — cites the book section + mark; the fault shown matches the mechanism the book gives; humane (D6; visual-style §14).
17. **Honesty tags** — the right tag (visual-style §15 order) on every exaggerated, unscaled or time-compressed shot; `exam_fact` exaggerations are said in the voice; no exaggeration changes number, order, side, topology or sequence (visual-style §15).
18. **Series continuity** — the Part opens on the last Part's end state (`endstate.json`); recap facts match its `recap_facts`.
*(G-Art checks the look of visual-style §10–§15; G-A11y checks label/tag contrast, colour chips + patterns, caption band clear.)*

**G-Learn multimedia checklist (MM, D-107)** — runs on the **final render + final mix** (R1), never the scratch. Two parts: `tools/episode/render_check.py` (`--dry-run --debug --only --preview`, I5) runs the auto items, then the **learning designer** (not the maker, H2) signs the human items. Each item records pass/fail + timestamp in the render manifest (H7).
| # | Check | How |
|---|---|---|
| MM1 | Labels ≤ 3 words · each Check chip ≤ 3 words · titles ≤ 4 · no other on-screen string > 4 words (captions, credits, honesty/media tags excepted) | auto (shots.json + overlay track) |
| MM2 | Dot on the structure; label text's near edge ≤ 12 % of the frame's short side from the dot; outside the subject's outline (Lesson); no crossings | auto (anchors) + human spot check at 210 px high and at 1080 |
| MM3 | Label fade-in starts −0.3 … +0.5 s from the spoken word's onset; report the max \|Δ\| | auto (word timings) |
| MM4 | Dwell (time at full opacity) ≥ 1.5 s (Lesson) / ≥ 1.0 s (Short) | auto |
| MM5 | No on-screen sentence repeats the voice; no burned-in captions in Lessons (Shorts' kinetic captions excepted, §6b.2) | auto + human |
| MM6 | ≤ 1 accent ring and ≤ 1 moving focus at a time; clutter dimmed (ctx) | human |
| MM7 | Every label's term is spoken within the MM3 window of the label's fade-in, and is in the transcript there | auto |
| MM8 | Idea breaks: hold ≥ 1.5 s, no speech within ±0.3 s, music ducked or sustained (never a cadence; only segment ends resolve), break placement per §6b.1, `chapters.vtt` = one cue per idea; each primer part labelled + named inside the MM3 window | auto + listen |
Templates refer here; don't copy the list (RULES I3).

## 3. Research craft
1. **Claim → cite → mark.** Break a section into atomic claims; each gets its book section, registry sources and a mark (✔✔ ✔ ⚑ ✚ ≈).
2. **Triangulate.** Tier A claims aim for book + one Tier 1 source; prefer recent reviews and human-specimen data over drawings.
3. **Record uncertainty, don't hide it.** Ranges ("days 16–18"), "about", and which age convention (fertilization vs gestational).
4. **Mine misconceptions.** Each dossier lists the 3–5 errors students make (exam Q-banks, papers); cards and Checks target them (refutation: state the wrong idea, then correct it).
5. **Units and staging always.** Size in mm, age in days + Carnegie stage.
6. **Licence before look-alike.** Check the licence before any source shapes a visual (RULES G5).

## 4. Teaching craft (with `research/teaching-methods.md`)
1. **One objective per card, one per idea** (an episode's 20–60 s unit, §6b.1), written as a verb you can test ("explain why…", "identify on a section…", "order…").
2. **Sequence:** what it looks like → how it happens → why it matters (clinical) → what it becomes (adult).
3. **Multiple representations:** 3D view + cross-section + simple schematic for each key concept; switch between them explicitly.
4. **Analogies with an expiry date:** every analogy says where it breaks ("like folding a sheet — except cells are moving, not bending").
5. **Worked example before practice;** Checks after, spaced via the Remember deck; interleave chapters only after mastery.
6. **Assessment matches the objective:** spatial objectives get spatial Checks (rotate, order frames, label a section).
7. **Desirable difficulty, not confusion:** the pre-question at the start may be hard; the explanation must not be.

## 5. Story craft
1. **ABT spine:** *And* (here's the situation) → *But* (a problem or mystery) → *Therefore* (what the embryo does about it). One question per episode, answered at the end.
2. **Cold open ≤ 10 s:** a clinical mystery, a surprising fact or a visual puzzle; the General cut uses an everyday hook.
3. **A protagonist with a goal:** a cell, a layer, a structure on a journey; anthropomorphism is labelled as metaphor (cells don't "want"; RULES D5).
4. **Stakes:** what goes wrong if this step fails (the clinical correlate), told humanely (D6).
5. **Season arc + motifs:** one season question, a recurring guide voice, visual motifs (the colour key, the day ruler) that pay off later; each episode teases the next.
6. **Payoff and recap:** the answer lands as a visual, then 2 Checks.
7. **Audience cuts from one scene set:** MBBS cut (terms, clinical depth), General cut (everyday words, one analogy more, no exam detail). Two formats (visual-style §10): **Lesson** (16:9, 6–10 min per Part; was "Explainer/MBBS", D-046) and **Short** (9:16, ≤ 60 s, one idea).

## 5b. Host character and the Short profile (D-032)
**Host (profile field `host`):** cell/embryo character (**default**) · animal · stylised human · none.
1. **Job:** asks the episode's question, reacts, jokes, recaps — a face for attention. It **never shows anatomy**; the science shot carries every fact (H9, D5).
2. **Design:** our own original character (no copying references — G1); a character sheet (front, side, 6 expressions, palette, silhouette readable at phone size), a name, a voice, a personality line. **Colour (D-048, loosened 20 Nov 2026):** costume colours are fine; no germ-layer token hue or the accent as a main colour; the host stands on its own plate. Body = glassy pearl near-white (#F5EBFF, floor #EBE1F5) with a warm inner glow; ink #1F1A24/#2A1C40 for eyes and line; measure ΔE00 of costume colours vs the tokens and accent on rendered pixels (manifest); the host skips the warm grade (own pass). (Round 1's strict pearl+ink-only rule is superseded.)
   **D5 — never mislead about anatomy:** no organelles, layers or cell clusters; never divides or turns into anatomy; own plate or corner cut-in; never cut host → same-scale zygote/morula; never in groups of 2/4/8; never says cells plan or intend; host props carry no diagrams.
3. **Consistency:** same sheet + same seed/reference image for every shot; checked across 2 angles before use.
   **Measured on every host render (D-051):** body edge vs the real plate ≥ 3:1 on ≥ 90 % of edge samples, every camera at start/mid/end (fix order: move the practical/plate, then rim, an ink outline only as a fallback — a ring can read as a cell membrane); colour vs germ-layer tokens gated only for tokens on screen in that shot (swatches always ≥ 15); loudness −14 LUFS ±0.5, true peak ≤ −1.5 dBTP after AAC, linear; one manifest per clip.
4. **Humour:** light, character-driven, never at a patient's or condition's expense (D6); a joke never bends a fact.
5. **Credits:** AI-made host shots are labelled in credits and the description.

**Language (profile field `language`):** English (**default**) · Hinglish · Hindi. One cited script per episode; translations keep the citations; pronunciation dictionary per language.

**Short profile (9:16, ≤ 60 s):**
1. Hook ≤ 1 s (host question or visual puzzle); one idea; payoff by the end; "full episode in the app" end card.
2. Cuts every 1–3 s; science shots still hold ≥ 1 s on a reveal.
3. **Kinetic captions** = styled subtitles (toggleable): one phrase at a time, key term highlighted, outline for contrast, Latin + Devanagari, inside the 9:16 safe area (clear of app buttons at the bottom and right).
4. Same loudness target (H6).

**Lessons** (16:9; was Explainer/MBBS, D-046) keep learning pace: hold 1–2 s after each reveal, chapter markers, captions as a toggle; frame, recap and clinical slots in visual-style §10, §14–§15.

## 6. Visual & motion craft (science animation)
1. **Clarity over realism — but cinematic.** **Look (owner doc: `build/visual-style.md`, D-041).** 9:16 Short frame with safe zones; 6 × 8 s chapter grammar for Shorts only; thin-caps chapter titles ≤ 4 words (D8); glassy SSS tissue (cheap fake in the app); warm grade on background + ctx only, layers within ΔE00 ≤ 8 of D-031; plum accent = ring + label, never fill; macro depth of field with the named structure sharp; background-only dust, off in reduced motion; cuts every 1–3 s, one move per shot; safe zones include the right action rail. **D-046 (§10–§16):** two formats from one scene (Short 9:16 + Lesson 16:9); segment colour mode, colour = origin across Parts; labels with leader lines; real media tagged and unaltered; clinical slots in Lessons; Part recaps + honesty tags; CC0/CC BY/PD real media only.
2. **Colour has meaning:** germ-layer tokens (RULES B3, D-031) with patterns; `--g-ctx` neutral for non-layer tissue; the accent `--accent` only as a "look here" ring/outline + label (+ motion in video), never a fill or a layer colour.
3. **Visual hierarchy:** the subject is lit, sharp and saturated; context is dimmer and desaturated; at most one moving focus at a time.
4. **Always oriented:** axis gizmo (cranial/caudal, dorsal/ventral), scale bar and day/stage stamp on every 3D shot (B2).
5. **Camera grammar:** establish → move in → detail → pull back to context; slow, motivated moves with ease in/out; no fast spins; hold 1–2 s after each reveal.
6. **Continuity:** show change as a morph, not a cut, when the shape is the lesson; end folding shots on the exam cross-section (D9).
7. **Typography:** one family, 2 weights; labels 1–3 words on their structure (D8); safe areas for 16:9 and 9:16.
8. **Animatic first:** a rough three.js preview with scratch voice is reviewed (G-Story, G-Sci, G-Art) before any final render.
9. **Thumbnails and titles:** a single clear image + a question; never misleading.
10. **Designed per device (D-033, RULES C13):** each screen has its own layout per class (`build/design-plan.md` §2): phones stack or drill down with actions in thumb reach; tablets split into two panes (study mode); desktops use up to three panes with hover and keyboard. Never just stretch. Labels and overlays in shots stay legible on a phone *and* don't look oversized on a desktop — check frames at both sizes.


## 6b. Multimedia craft (M01; D-107)
Teaching methods 1–5 say *what*; this says *how much* and *how it is checked* (MM, §2). Episode data: `docs/episode-spec.md` spec 2.

**6b.1 Segmenting — learner-paced ideas.**
- Three levels: **episode → segment** (60–120 s, the `seg` field; a coarse group on the scrubber and transcript) **→ idea** (one objective, H1 + D2; 20–60 s; ends on a reveal hold).
- **Pace:** *Study pace* pauses at each idea's end on the held frame and waits for **Next idea ▸**; *Watch* plays straight through (apart from the video's own Check pauses), ideas show only as chapter ticks. **Chapters = ideas:** `chapters.vtt` has one cue per idea (YouTube + the app's ticks). Default: Study pace for both Lesson cuts, Watch for Shorts; **Shorts never pause**.
- **Where a break goes:** after a reveal hold ≥ 1.5 s with no speech within 0.3 s either side; music is ducked or sustained across it, never a cadence (only a segment end may resolve). Never mid-sentence or mid-morph (the shape is the lesson, §6.6); never between a Check and its reveal (the video's own Check pause plays in both modes); never within 10 s after a Check's reveal; never inside or at the end of the cold open (≤ 10 s, D3); never inside or at the end of the primer — the first idea runs from the cold open through the primer to the first reveal in segment 1 (still ≤ 60 s).
- **A break is a cliffhanger, not a full stop.** The episode question and ABT spine stay pinned on the idea pause panel, with the protagonist's progress (§5, e.g. Journey: "Our cell: in the streak → ?"), or the question's progress when there is no protagonist (Mystery, Factory). An idea ends on a *Therefore* or an open loop the voice already set up. The video never says "tap": YouTube and Watch viewers hear one unbroken story.
- Panel words live in the app, not the frame (D8 untouched).
- **Data, not code:** `ideas[]` per Lesson profile in `script.json` — id, from/to line, objective, `check_by` (what tests it), title ≤ 4 words, optional `next_q` ≤ 6 words. Ids are permanent (A2): `S1E01.L.i03`. The builder proposes breaks snapped to the nearest hold; the story director signs them (G-Story).

**6b.2 Signalling, redundancy, temporal contiguity.**
- **Words:** label ≤ 3 words · each Check chip ≤ 3 words · titles ≤ 4 · no other on-screen string over 4 words, except captions, credits and honesty/media tags (D8).
- **Beside, not away:** the anchor dot is on the structure (visual-style §12); the text's near edge is ≤ 12 % of the frame's short side from the dot; in Lessons the label stays outside the subject's outline. If both can't hold (a structure deep inside the subject), distance wins and the label may sit on a ctx-dimmed region. The only distant key is the legend chip (visual-style §11).
- **Timed to the voice:** fade-in starts −0.3 … +0.5 s from the spoken word's onset; dwell ≥ 1.5 s (Lesson) / ≥ 1.0 s (Short). Word onsets come from the final mix (TTS word timings or a free local forced aligner — the R1 pipeline picks one and Measures it, C4).
- **Redundancy:** the voice carries the sentences; no on-screen sentence repeats the narration. Lesson captions are VTT toggles only, never burned in. Shorts keep burned-in kinetic captions (watched muted) — an a11y exception, not on-screen text; the app never lays VTT over a burned-in Short.
- **Signalling:** ≤ 1 accent ring at a time (the marked cell's alone on tracer shots); ≤ 1 moving focus; context dimmed (ctx) when the named structure sits in clutter. Every label's term is in the transcript at the same timestamp (visual-style §10).

**6b.3 Pre-training — the "Meet the parts" primer.**
- **Where:** Lessons (both cuts), after the cold open (hook first, D3) and before segment 1. It replaces the 5-s terms strip. Shorts have none.
- **Shape:** ~20 s in the MBBS Lesson, 15 s in the General cut, each including the 2 s end hold; ≤ 3 parts, each isolated (rest ctx-dimmed), on a still view or a ≤ 15° turntable, with stamp + scale (B2). The label lands as the voice names the part and says what it is in one line; its token colour + pattern becomes the episode's colour key. No process motion — names and looks only. Ends with all parts in place, then a 2 s hold. The voice opens the primer on the cold-open question ("To answer that, meet three parts…") and adds no new question.
- **Term budget:** primer terms go in their line's `new[]` and count toward D2's ≤ 3 new terms in any rolling 60 s (`max_terms_per_60s`; the builder checks). A term introduced in Part 0, an earlier Part, or on a Ready-to-watch core card counts as review, not new — decided at build time, never from a learner's status.
- **Which terms:** the profile's primer terms (`primer.<profile>.parts[].term`; S1E01 MBBS: germ layers · primitive node · notochord; General, in everyday words: epiblast · hypoblast · primitive streak — the top sheet, the bottom sheet, the groove).
- **App:** primer parts show as chips linking to their cards; the player offers **Know these? Skip ▸** only when every linked card is Understood (B4) — an offer, never automatic.

## 7. Sound craft
1. **Voice:** 130–150 words per minute; pronunciation dictionary for every term; consistent voice per season (and per host).
2. **Mix:** music ducked well under narration (none under key sentences, D6 coherence); light sound design for state changes only.
3. **Loudness:** about −14 LUFS integrated for web/YouTube, true peak ≤ −1 dBTP; check on phone speakers and laptop speakers.

## 8. Accessibility & ethics
1. **Captions on every video** (accurate, synced, speaker-neutral) + a transcript; subtitles toggle (on by default when muted).
2. **Contrast** at least WCAG AA (4.5:1 text); colour never the only cue (patterns + labels).
3. **No flashing** above 3 per second; a reduced-motion option for the viewer and player.
4. **Transcript describes key visuals** for screen-reader users.
5. **Humane clinical content;** diverse bodies in adult anchors; no real patient images without consent and licence — rules for footage, X-rays and other real imagery: `build/visual-style.md` §16.
6. **Disclose AI-generated material** in credits; AI-made visuals never carry anatomy without passing G-Sci.

## 9. Engineering practice (the team behind the studio)
1. **One build chat per repo; small steps; tests before merge** (DrumPath practice).
2. **Schemas first:** card, scene, map and episode formats as versioned JSON Schemas (`docs/*-spec.md`); validators run them.
3. **CI on GitHub Actions (free):** validators, citation/mark check, id check, **layout sweep (`tools/layout-check`, design-plan §2 matrix)**, still regression on every push.
4. **Reproducible renders:** each render writes a **manifest** (scene file hash, tool + version, GPU, settings, seed, voice version) next to the output.
5. **Asset naming:** `<book>/<id>/<type>-<version>.<ext>` (e.g. `E/S1E01/master-v03.mp4`; renditions `-720p` / `-1080p`); never overwrite a published file — bump the version.
6. **Performance budgets:** phone scene ≤ 150k triangles and ≤ 2 MB, ≥ 30 fps; app first load ≤ 3 s on 4G; episode 720p ≤ 12 MB/min (until Measured replaces them). Tablet/desktop extras only once Measured.
7. **Local-first models:** find candidates on Hugging Face (connector available), record each model's licence and size in the pipeline reference; non-commercial models stay on the laptop (RULES F4).
8. **Licence ledger:** `THIRD_PARTY.md` in the repo lists every library, model and asset with its licence and credit.
9. **Privacy:** no analytics or tracking; stats stay on the device and the owner's Drive.
10. **Backups before data changes;** testing mode for experiments (RULES A3).

## 10. Production pipeline (stages and artefacts)
Brief + audience profile (level, depth, type, format, length, **language, host**) → research dossier (X1) → objectives → cited script → table read (scratch TTS) → **animatic** (three.js, scratch voice; host as a placeholder) → gates G-Sci/G-Learn/G-Story/G-Art → scene build + host shots → final render (laptop GPU) → final voice + mix → captions (kinetic for Shorts) → renditions (§8a) → QC (G-Eng, G-A11y; plays well on phone, tablet, laptop) → publish (Drive + catalog + clips) → owner check → measure (recall 24 h / 7 d, completion, drop-off) → retro line in the review log.

## 11. Definition of Done
- **Concept (K1):** id, name, tier, threads, day/stage, layer, system, importance, prerequisites, locator; no orphan links.
- **Card:** objective; idea + 3D view; Remember; Check aligned; every fact cited + marked; G-Sci, G-Learn, G-A11y passed.
- **Scene:** spec-valid; scale, day, orientation shown; budgets met; checked against R01/R02 (look only); still stored for regression.
- **Host shot:** original design from its sheet; identity consistent across angles; synced to its line; no anatomy shown; credited; G-Art passed.
- **Episode:** audience profile; ABT script, cited; animatic approved; captions + transcript; loudness; renditions; QC + all gates; manifest; catalog row.
- **UI screen / artifact:** a design-plan §2 layout for all five device classes; layout-check green (13 sizes, both orientations, 125 % text, light + dark); contact sheet passed G-Art; rotation keeps place; touch, mouse and keyboard all work.
- **Build step:** tests green; budgets met; STATUS, log, DECISIONS updated; owner check written (phone, tablet, laptop); next prompt given.

## 12. What we measure
Recall at 24 h and 7 d (per episode, story format, audience cut, host on/off) · completion rate and drop-off timestamps · Check accuracy per objective · Understood rate per card · General-cut comprehension (a non-medical viewer explains it back in one sentence) · production time per minute of video · which device class each session uses (on-device only, no analytics).
