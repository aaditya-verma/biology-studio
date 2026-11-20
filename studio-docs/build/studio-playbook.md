# Studio playbook — how the crew works, and the craft standards

*(Purpose: best practices, crew roles, review gates and Definition of Done. Created 17 Nov 2026, D-020. Updated: 20 Nov 2026 · Bio · Fix · Visual style 2 port — §2 G-Sci items 13–18, §5/§5b Explainer/MBBS → Lesson, §6.1 summary + §8.5 → visual-style §10–§16 (D-046). Before: 20 Nov 2026 · Bio · Build · Visual style commit — §2 G-Sci video checklist, §6.1 look summary → build/visual-style.md (D-041). Before: 18 Nov 2026 · Bio · Fix · doc reconcile — ported from the uploaded copy: host + Short profile §5b, cinematic look (D-032); designed per device §6.10, gates, DoD (D-033); §6.2 accent per D-031. RULES §H holds the musts; this doc holds the how. Evidence for teaching choices stays in `research/teaching-methods.md`; the quality bar's reference reels in `research/quality-references.md`; device classes and layouts in `build/design-plan.md` §2.)*

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
10. **Labels** — appear as the structure is shown (D8), point at the right thing, use GLOSSARY terms.
11. **Citations** — every spoken fact has a section + mark; no ≈; a ⚑ gives the book answer.
12. **AI shots** — host only, no anatomy, credited (H9).
13. **Segment colours** — segment mode stated by the legend chip; each segment matches `content/E/segments.json` and the previous Part; splits/merges follow visual-style §11 at the right day; each segment and derivative has a cite + mark; colours change only by a morph.
14. **Labels + leaders** — every dot sits on the named structure; lines don't cross; the anchor is still on the structure at the end of the move (visual-style §12).
15. **Real media** — the image shows what the voice says (stage, view, structure); orientation + scale correct or "scale not given"; unaltered except logged edits; ledger row exists (visual-style §13, §16).
16. **Clinical link** — cites the book section + mark; the fault shown matches the mechanism the book gives; humane (D6; visual-style §14).
17. **Honesty tags** — the right tag (visual-style §15 order) on every exaggerated, unscaled or time-compressed shot; `exam_fact` exaggerations are said in the voice; no exaggeration changes number, order, side, topology or sequence (visual-style §15).
18. **Series continuity** — the Part opens on the last Part's end state (`endstate.json`); recap facts match its `recap_facts`.
*(G-Art checks the look of visual-style §10–§15; G-A11y checks label/tag contrast, colour chips + patterns, caption band clear.)*
Templates refer here; don't copy the list (RULES I3).

## 3. Research craft
1. **Claim → cite → mark.** Break a section into atomic claims; each gets its book section, registry sources and a mark (✔✔ ✔ ⚑ ✚ ≈).
2. **Triangulate.** Tier A claims aim for book + one Tier 1 source; prefer recent reviews and human-specimen data over drawings.
3. **Record uncertainty, don't hide it.** Ranges ("days 16–18"), "about", and which age convention (fertilization vs gestational).
4. **Mine misconceptions.** Each dossier lists the 3–5 errors students make (exam Q-banks, papers); cards and Checks target them (refutation: state the wrong idea, then correct it).
5. **Units and staging always.** Size in mm, age in days + Carnegie stage.
6. **Licence before look-alike.** Check the licence before any source shapes a visual (RULES G5).

## 4. Teaching craft (with `research/teaching-methods.md`)
1. **One objective per card, one per beat**, written as a verb you can test ("explain why…", "identify on a section…", "order…").
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
2. **Design:** our own original character (no copying references — G1); a character sheet (front, side, 6 expressions, palette, silhouette readable at phone size), a name, a voice, a personality line. The cell/embryo host must not look like a real structure in a way that could mislead (e.g. not coloured with a germ-layer token or the accent).
3. **Consistency:** same sheet + same seed/reference image for every shot; checked across 2 angles before use.
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
