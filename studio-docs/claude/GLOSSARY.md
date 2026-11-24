# Glossary

*(Purpose: one name per thing — terms by thread, production, app and project terms. Updated: 24 Nov 2026 · Bio · Episode · S1E01 commit (Marked cell). Before: 24 Nov 2026 · Bio · Build · W5 dispatcher (desk.json home, Dispatcher tick, Desk answers). Before: 24 Nov 2026 · Bio · Fix · tentative rows (Desk, desk.json, Tentative step; §9 Step ids). Before: 22 Nov 2026 · Bio · Build · L2 lessons (lesson, sitting, lesson step, On the go, Study, Mixed review, recall stats). Before: 21 Nov 2026 · Bio · Build · W2 scheduler (plan, resource row, critical path, run, professor suggestion). Before: 21 Nov 2026 · Bio · Build · H2 reviewer mode (Reviewer mode, human science pass, plain line). Before: 21 Nov 2026 · Bio · Build · V2 3D drills (drill, pin, masked stamp, scene view, demo card; notochord looks). Before: 21 Nov 2026 · Bio · Build · L1 learning core (statuses, deck, guide card). Before: 20 Nov 2026 · Bio · Fix · Visual style 2 port — §5 Lesson, Part, segment mode, leader line, media tag, clinical link slot, honesty tag, end-state handoff (D-046). Before: 20 Nov 2026 · Bio · Content · C1 Part 0 + Ch 5 — §6 Remember prompt, Clinical link, Where it shows up (D-042). Before: 20 Nov 2026 · Bio · Build · Visual style commit — §8 five look terms (D-041). Before: 19 Nov 2026 · Bio · Build · W1 progress map — §8 progress map, steps.json, owner input, can start now, proposed status (D-040). Before: 19 Nov 2026 · Bio · Research · X1 Ch 06 — §7 CS11–CS23 events + R02 age note (D-039). Before: 19 Nov 2026 · Bio · Build · V1 viewer — day key, stamp, cut plane, axis gizmo, still; embryo axes + planes. Before: 18 Nov 2026 · Bio · Fix · doc reconcile — ported from the uploaded copy: §5 rendition, §6 device class, input class, test matrix, layout check, contact sheet (D-033); added host, Short, kinetic captions (D-032). Our own words. Each embryology term gets its book citation once I1 numbers the sections. New term → add it here.)*

## 1. Timeline & staging (thread T)
- **Fertilization age vs gestational age:** embryology counts from fertilization; clinicians count from the last menstrual period (about 2 weeks earlier). Always say which.
- **Embryonic period:** weeks 3–8, when the organ systems are laid down. **Fetal period:** month 3 to birth, mostly growth and maturation.
- **Carnegie stage (CS01–CS23):** the standard staging of human embryos by form, not age, covering roughly the first 8 weeks. Table in §7 (day column for all stages; events filled per chapter in X1).
- **Day / week notation:** "day 17", "week 3"; episodes show both on screen (RULES B2).

## 2. Germ layers (thread G) — colour tokens fixed (RULES B3)
- **Epiblast / hypoblast** (`--g-epi` / `--g-hypo`): the two layers of the bilaminar disc in week 2. The epiblast gives rise to all three germ layers.
- **Gastrulation:** week 3 process that turns the two-layer disc into three germ layers.
- **Ectoderm** (`--g-ecto`): outer layer → skin epidermis, nervous system.
- **Mesoderm** (`--g-meso`): middle layer → muscle, bone, blood, heart, kidneys.
- **Endoderm** (`--g-endo`): inner layer → gut lining and its glands, lungs.
- **Neural crest** (`--g-crest`): cells that leave the edges of the neural folds and migrate widely; sometimes called the fourth germ layer.
- **Context** (`--g-ctx`): non-layer tissue in a shot (amnion, yolk-sac wall, trophoblast), drawn neutral grey.
- **Accent** (`--accent`): the one "look here" colour — a ring/outline + label, never a layer colour (D-031).

## 3. Folding & shape (thread F — the spiral strand)
- **Primitive streak:** a groove on the epiblast that marks the body axis; cells move through it during gastrulation.
- **Notochord:** a midline rod of mesoderm that signals the overlying ectoderm to form the neural plate.
- **Neural plate → neural tube:** ectoderm thickens, folds and closes into the tube that becomes the brain and spinal cord.
- **Somites:** paired blocks of paraxial mesoderm along the axis.
- **Embryo folding:** the flat disc folds head-to-tail and side-to-side into a body shape (week 4).

## 4. Don't confuse (feeds Check distractors)
| These | The difference |
|---|---|
| Embryoblast vs trophoblast | Embryoblast (inner cell mass) → the embryo; trophoblast → part of the placenta |
| Epiblast vs ectoderm | Epiblast is the week-2 layer; ectoderm is one of its week-3 products |
| Primitive streak vs notochord | Streak = where cells move in; notochord = a rod that forms from cells moving in |
| Somite vs somitomere | Somitomeres are the earlier, less-defined whorls; somites are the segmented blocks |
| Neural tube vs neural crest | Tube = CNS; crest = migrating cells for much of the PNS and more |
| Gestational vs fertilization age | ~2 weeks apart (see §1) |

## 5. Production terms
- **Scene:** a file describing shapes, keyframes by day, labels and camera for one card or shot (`docs/scene-spec.md`).
- **Axes (embryo):** cranial = head end · caudal = tail end · dorsal = back (epiblast side) · ventral = belly · left/right = the embryo's own, not the viewer's. **Planes:** sagittal divides left from right · transverse (cross-section) divides head end from tail end · frontal (coronal) divides back from belly. Conventions, not book facts (shown as Terms in 3D scenes, D-036).
- **Day key:** a day in a scene with its stage, size, cite and mark; between keys the scene eases. **Stamp:** the always-on `Day · CS · ≈size` line on the 3D stage. **Cut plane:** a slice through the scene (cross-section = transverse, lengthwise = sagittal) that shows the layers' cut faces. **Axis gizmo:** the corner key Cr/Cd, D/V, L/R. **Still:** one fixed render of a scene at a day, compared on every change (`tools/stills`, C11).
- **Marked cell:** the one tracked cell drawn by a `tracer` (V3 trace drill; S1E01 Journey); drawn larger than life; no book section (app convention).
- **Shot:** one continuous piece of an episode, made from one scene. **Storyboard:** one frame per beat. **Shot list:** shots with duration and day range.
- **Render:** turning a scene into video frames. **Master:** the final full-quality episode file. **Clip:** a 10–20 s cut used on a card.
- **Rendition:** one encode of a master at a set resolution (720p for phones; 1080p for tablet/desktop if M1 allows — D-033).
- **TTS:** text-to-speech voice-over. **VTT / SRT:** subtitle files. **Drift:** subtitle lag behind speech.
- **Host:** the episode's on-screen character (cell/embryo by default · animal · stylised human · none); asks, reacts, jokes, never shows anatomy (audience profile `host`, playbook §5b, D-032).
- **Short:** the 9:16, ≤ 60 s audience cut (`-short` suffix) — hook ≤ 1 s, cuts every 1–3 s (playbook §5b). **Kinetic captions:** styled, toggleable subtitles for Shorts — one phrase at a time, key term highlighted, Latin + Devanagari.
- **Lesson:** the 16:9 teaching format, 6–10 min per **Part** (one numbered video of a multi-part topic series, e.g. "Heart · Part 3"; shown on the **Part chip**); was "Explainer/MBBS" (visual-style §10, D-046). Short and Lesson come from one scene with two cameras.
- **Segment mode:** a shot coloured by regions inside one germ layer (e.g. heart-tube segments) instead of by layer; tokens `--s-<organ>-<seg>` from `content/E/segments.json`; a **legend chip** names the mode; colour = origin, kept across Parts (visual-style §11). **Layer mode:** the default, D-031 germ-layer tokens.
- **Leader line:** the thin line from a label to a dot on its structure, anchored in 3D (visual-style §12).
- **Media tag:** the small on-screen tag on any non-3D shot ("Real image · <credit>", "Diagram") (visual-style §13); its ledger row lives in the registry § Media.
- **Clinical link (video slot):** a 15–30 s Lesson segment showing which normal step fails and the result, ≤ 2 per Part (visual-style §14). Same name as the card part in §6 — same job, different place.
- **Honesty tag:** one of five fixed on-screen tags — Exaggerated for clarity · Not to scale · Time compressed · Colours illustrative · Simplified (visual-style §15, RULES B2).
- **End-state handoff:** Part N+1 opens on Part N's last frame, recorded in that Part's `endstate.json` (visual-style §15, scene spec §10).
- **Bake-off:** making the same shot several ways and comparing (M1).
- **Animatic:** a rough three.js version of an episode with scratch voice, reviewed before any final render (RULES H3).
- **Render manifest:** the record written with every render — scene hash, tools, GPU, settings, seed, voice (RULES H7).
- **Preview render:** a fast low-res render (`--preview`) for checking motion and framing.

## 6. App & engine terms
- **Part 0:** orientation cards (`E00.01.nn`) — axes, staging, scale, colour key, reading a section, how to use the app.
- **Card statuses:** Read (card open 1.5 s) → Understood (every Check question right in one run) → Can explain (explained aloud after Understood) — D-050.
- **Reviewer mode (H2, D-061):** the app's guided home for the human science reviewer — `#review` (To review · What's new · My feedback), card review `#rcard`, tour `#rtour`, `#updates`; feedback goes as a pre-filled GitHub Issue Form she submits with **Create**. **Human science pass (D-060):** the Professor's ✓ on a card version, on top of the chat G-Sci. **Plain line:** `<!--plain: …-->` at the end of a build-log line — what Updates shows her.
- **Lesson (L2, `docs/lesson-spec.md`):** one chapter's cards in roadmap order, split into **sittings** of 10–15 min; each card adds **lesson steps** read → Check → Try the 3D *or* 3D drill (when the card has one) → Remember. Progress is saved per step; a lesson never blocks (D-070).
- **On the go / Study (Today, L2):** Today's two plans — On the go = up to 5 min (due Remember prompts + one Check); Study = 15–30 min (the next lesson sitting + due prompts, optional Mixed review).
- **Mixed review (L2):** Check questions from Understood cards across chapters, card text hidden; counts toward **recall stats** only (share right in the last 30 days) — it never sets a card status (B4).
- **Remember deck:** spaced review of the Remember prompts of read cards — 1, 3, 7 days, then every 7 (L1, D-050; 21/60 after the use gate).
- **Drill (3D drill):** a Check question run in the card's own 3D scene — **Rotate to match** (`rotate`), **Which day is this?** (`day`), **Order the frames** (`frames`), **Label it** (`label`), **Folded or not?** (`folded`); one right answer, a text alternative, scored like any Check (card-spec §2a, D-054). **Pin:** a numbered marker on a structure in a *Label it* drill. **Masked stamp:** *Day ? · stage ? · size ?* while a *Which day is this?* drill is open (RULES B2 exception). **Scene view:** a named camera view in a scene file (`views`), the target of a rotate drill. **Demo card:** a testing-only card copy with every drill type (`?test=1&fixture=drills`).
- **Prenotochordal cells → notochordal plate → notochord:** the three looks of the midline axial cells in `sc-E05.02.01` — a thin strand between epiblast and endoderm, a flat band within the endoderm, then a solid rod lifted off it, cranial end first (book order, D-029).
- **Guide card:** a Part 0 card about the app itself (`kind: guide`); its facts cite `APP <screen>` and carry the mark **ⓘ** (D-050).
- **Card parts (C1, `docs/card-spec.md`):** **Remember prompt** — a short recall question + answer on a card (2–5 per card) that feeds the Remember deck · **Clinical link** — the card's clinical sentences (book Clinical Correlates), cited · **Where it shows up** — other concepts where the idea returns.
- **Core / support tags:** an episode's cards weighted ×2 / ×1. **Ready to watch:** weighted share Understood.
- **Unlock count:** how many episodes use a card as core; the top ones are written first.
- **≈ line:** a fact without a valid citation or with low confidence; blocks "final".
- **Draft & review:** Studio's flow for drafting cards and scripts with Claude and approving them line by line.
- **Recall quotient:** % right on a cold Check 24 h and 7 days after first watching.
- **Testing mode:** the app runs but saves nothing (`?test=1`). **Version line:** "vNN · commit · date" in Settings.
- **Debug flag:** a switch, off by default, that shows extra detail for one area — `?debug=map,viewer,layout` in the app, `--debug` / `--dry-run` / `--only` / `--preview` on tool scripts, `debug: true` in a scene (RULES I5).
- **Edit hook:** a marked place to change something — one home per value (tokens, `02-config.js`, `content/`, `strings.js`), `// EDIT:` markers in code, and the ✎ button in testing mode that shows an item's id + file and copies an "edit this" prompt (RULES I6).
- **Edit prompt:** the text the ✎ copies; paste it into a `Bio · Fix · <id>` chat.
- **Device class:** which layout a screen uses — `dev-p` phone portrait · `dev-pl` phone landscape · `dev-tp` tablet portrait · `dev-tl` tablet landscape · `dev-d` desktop/laptop; set from short side, orientation and pointer (`build/design-plan.md` §2, RULES C13).
- **Input class:** `.in-touch` (finger) or `.in-mouse` (mouse/trackpad + hover); separate from device class.
- **Test matrix:** the 13 fixed screen sizes every UI is checked at — phones and tablets in both orientations, 100 % and 125 % text, light and dark (`build/design-plan.md` §2).
- **Layout check:** `tools/layout-check` — the headless sweep over the test matrix with automatic checks (RULES C8, C13). **Contact sheet:** its grid of screenshots per device class, reviewed at G-Art.

## 7. Carnegie stages
A stage is set by **form**, not by age or length (R05f). Day = classic estimate, days after fertilization ≈ postovulatory (R08 from R06; the book's days agree). R02's revised ages run ~3–7 days older at CS6–CS13 and converge or run younger later — see D-030, D-039 (c); on screen we show the book day. Same day ranges fill `content/E/index/timeline.json` `cs` (via `tools/indexer/carnegie.json`). Key events: CS06–CS10 done in X1 Ch 05 (dossier ch05 §1), CS11–CS23 in X1 Ch 06 (dossier ch06 §1; sizes = R08 greatest length, show "≈ size"; ✚ = R08 feature with no book event, More only); CS01–CS05 filled by X1 Ch 03–04.

| Stage | Approx. day | Size (≈) | Key events (our words) | Taught in |
|---|---|---|---|---|
| CS01 | 1 | | | E03 |
| CS02 | 2–3 | | | E03 |
| CS03 | 4–5 | | | E03 |
| CS04 | 5–6 | | | E03 |
| CS05 | 7–12 | | | E04 |
| **CS06** | 13–15 | 0.2 mm | Chorionic villi appear; primitive streak appears (6b) — gastrulation starts `[E05.01, E06.06 · R06, R08]` ✔✔ | E05.01.02 · S1E01 |
| **CS07** | 15–17 | 0.4 mm | Notochordal process grows forward from the node; secondary villi `[E05.02, E06.06 · R06, R05a]` ✔✔ | E05.01.03, E05.02.01 |
| **CS08** | 17–19 | 1–1.5 mm | Primitive pit, notochordal and neurenteric canals; neural groove; pear-shaped disc `[E05.02, E05.05 · R06, R05a, R02]` ✔✔ | E05.02.01–02, E05.05.01 |
| **CS09** | 19–21 | 1.2–2.5 mm | First 1–3 somite pairs; neural folds; heart area and pericardial cavity `[E06.02, E06.06 · R08, R02]` ✔✔ | Ch 6 bridge (S1) |
| **CS10** | 22–23 | 2–3.5 mm | 4–12 somite pairs (book: 5–12); neural folds begin to fuse (neck region first) `[E06.06 · R06, R08]` ✔✔ | Ch 6 (S1) |
| **CS11** | 23–26 | 2.5–4.5 mm | 13–20 somite pairs; rostral (cranial) neuropore closes (~day 25); optic vesicles; folding under way; oropharyngeal membrane ruptures `[E06.01, E06.06 · R06, R08, R05l]` ✔✔ | E06.01.03, E06.03.01 |
| **CS12** | 26–30 | 3–5 mm | 21–29 pairs; caudal neuropore closes (~day 28); 3 pharyngeal arches; upper limb buds `[E06.01, E06.06 · R06, R08, R05l]` ✔✔ | E06.01.03, E06.05.01 |
| **CS13** | 28–32 | 4–6 mm | 30+ pairs; four limb buds; lens disc (placode); otic vesicle; 4th arch `[E06.06 · R08]` ✔✔ | E06.01.06, E06.05.01 |
| **CS14** | 31–35 | 5–7 mm | Lens pit and optic cup `[R08]` ✚ · body tightly C-shaped `[E06.06]` ✔ | E06.05.01 |
| **CS15** | 35–38 | 7–9 mm | Lens vesicle; nasal pits; hand plate (arms paddle-shaped) `[E06.05, E06.06 · R08]` ✔✔ | E06.05.01 |
| **CS16** | 37–42 | 8–11 mm | Auricular hillocks; foot plate `[E06.06 · R08]` ✔✔ · retinal pigment visible (R08; book 43–49 d) ⚑ D-039 b | E06.05.01 |
| **CS17** | 42–44 | 11–14 mm | Finger rays `[R08]` (book: hand and foot rays from day 36) ⚑ D-039 b | E06.05.01 |
| **CS18** | 44–48 | 13–17 mm | Eyelids begin; nipples appear `[E06.06 · R08]` ✔✔ · toe rays ⚑ D-039 b · elbow region, ossification may begin `[R08]` ✚ | E06.05.01 |
| **CS19** | 48–51 | 16–18 mm | Trunk lengthens and straightens `[R08]` ✚ (no book event) | E06.05.01 |
| **CS20** | 51–53 | 18–22 mm | Arms longer, bent at the elbows `[E06.06 · R08]` ✔✔ | E06.05.01 |
| **CS21** | 53–54 | 22–24 mm | Fingers and toes free `[E06.06]` ✔ · hands and feet approach each other `[R08]` ✚ | E06.05.01 |
| **CS22** | 54–56 | 23–28 mm | Eyelids and external ear more developed `[R08]` ✚ (no book event) | E06.05.01 |
| **CS23** | 56–60 | 27–31 mm | End of the embryonic period (~CRL 30 mm) `[E06.05, E06.06 · R08, R02]` ✔✔ · head more rounded `[R08]` ✚ | E06.00.01, E06.05.02 |

## 8. Project terms
- **Owner doc:** the one doc that owns a fact (INSTRUCTIONS §2); it wins on conflict.
- **Pendencies:** open questions, blocks and owner to-dos — kept only in `build/steps.json` (a step's `todo` and `inputs`; D-040).
- **Progress map:** the app page `#progress` (Map · Board · Your inputs) and `#step=<id>` that draws `build/steps.json` live from the repo: every step in lanes by chat type, coloured and patterned by status, with what blocks it (W1, D-040).
- **`steps.json`:** `studio-docs/build/steps.json`, the owner doc for step status, needs (`unblocks` derived), gates, owner checks, D-ids, last log line, to-dos and owner inputs; checked by `tools/tracker/check.py`.
- **Plan (schedule):** the `#progress=plan` page and `check.py --next` — estimated dates per step from today, status, `est`, `runs` and the `calendar`; the order is fixed (`queue`, D-047), only dates move (D-063).
- **Resource row:** lock · GPU · research · you · professor — what a step holds while it runs; two steps never share the lock or GPU row at once.
- **Critical path:** the chain of needs that sets the estimated finish (◆ on Plan); a slip on it moves every date after it.
- **Run:** one chat's work on a step, kept in that step's `runs` (chat, by, start, end, outcome); no `end` = running now; more runs than estimated = **slipped**.
- **Professor suggestion:** an optional item for the professor (`uses: ["prof"]` or an input `for: "prof"`); never blocks anything (D-063).
- **Owner input:** something the owner owes a step — decide, answer or do — id `<step>.q<n>`; listed oldest first under Your inputs. **Blocking input:** one marked `blocks`, so the step can't start until it is answered.
- **Can start now (◎):** a planned or ready step whose needs are done (or only wait on an owner check), with no blocking input open and the build lock free (or its own).
- **Proposed status:** a collaborator chat's suggested status change (`proposed_by`); the owner confirms it.
- **Changelog:** `logs/build-log.md`, newest first.
- **Review gate:** a check an artefact must pass (G-Sci, G-Learn, G-Story, G-Art, G-Eng, G-A11y, G-Owner; playbook §2).
- **Usage check:** the 1–3 suggestions at the end of a chat to keep the project lean.
- **Ready prompt:** the paste-in text that starts the next chat, with its chat name.
- **Owner / collaborator:** the owner (Aaditya) has the final say; a collaborator (first: the Professor) shares the project and proposes (D-025).
- **Studio home:** each person's laptop folder for the project — `tools\`, `apps\`, `models\`, `repo\` (owner: `D:\Projects\biology_studio`).
- **Build lock:** the line in STATUS § Lock that a Build chat takes first and frees at the end, so only one build runs across both people (RULES I8).
- **Handoff note:** what a collaborator chat sends the owner while only the owner edits docs (templates §10).
- **Laptop 1 / Laptop 2:** owner's / collaborator's render machine in `build/pipeline-reference.md`.
- **Glassy tissue / SSS:** subsurface scattering — light enters a surface and spreads inside before leaving, so tissue looks soft and translucent. Rendered in Blender; faked in the app.
- **Grade (colour grade):** the overall colour tint added to a shot. Ours touches background, light and `ctx` only; germ layers keep their D-031 colours.
- **Chapter title:** ≤ 4-word thin-caps title at the top of each 8-s chapter of a Short (D8, D-041).
- **Chapter grammar:** the 6 × 8 s Short structure: hook, four ideas, payoff on the section view.
- **Swatch-chip frame:** a debug frame rendered per shot that shows each layer's graded colour beside its token, with ΔE00.
- **Desk:** the central coordination chat, a Cowork chat rolled weekly (`Bio · Desk · <date>`); it reads `desk.json` + STATUS, suggests steps and queues owner answers to W5. Its dashboard is the Desk tab on `#progress` (W6, D-099).
- **`desk.json`:** `build/desk.json` on branch `desk-data` (never `main`), the snapshot the dispatcher tick writes (now, lock, next 5 with dates, ranked inputs, running, slips, CI, checks, pipeline tasks, pending answers, generated-at); also untracked at `out/desk.json` in the laptop clone, which Desk reads first; over 6 h old = stale (W5, D-099, D-101).
- **Dispatcher tick:** one hourly run of `tools/dispatch/desk.py --tick` by the scheduled task `Bio · Dispatcher`; reports and commits Desk answers, starts no jobs (W5, D-101).
- **Desk answers:** owner answers Desk queues in Studio home `handoff\desk-answers.json`; the tick commits them, the owner pushes (D-101).
- **Tentative step:** a planned step agreed before it is scoped — `todo` line 1 reads *Tentative — firm up when its prompt is written*; the Plan dates it (D-099).

## 9. Step ids

*(From the owner's doc Biology Studio — Task ID glossary, sections 1, 2 and 5, as read 24 Nov 2026. Step status stays in `build/steps.json`.)*

### 9.1 How to read a step id
A step id is **letter(s) = track** + **number = order inside that track**. A higher number usually needs the lower one. Ids never change or get reused (RULES A2), so gaps and odd names are history, not mistakes.

| Pattern | Means | Example |
| --- | --- | --- |
| `L1`, `L2`, `L3` | Track L, steps in order | L2 needs L1 |
| `…b` | Second pass of the same step | `M1b` = M1 host shot, after M1 numbers |
| `…F` | Fix chat on that step | `L1F`, `U2F`, `W3F`, `MAPF` |
| `…a` / `…b` | One step split in parts | `X3a` → `X3b`, `X2a` → `X2c` |
| `X1.NN` | One step per book chapter | `X1.04` = research, Ch 4 |
| `…V8` | A version of a step's kit | `M1V8` = M1b v8 install |
| `<step>.q<n>` | Owner input on that step | `X1.04.q1` |
| Word ids | One-off steps | `GATE`, `CIG`, `WCON`, `FD`, `FA` |

Chat name always follows: `Bio · <Type> · <Step>`, e.g. `Bio · Build · U3 look screens`. Source: `build/steps.json` (100 steps on 24 Nov 2026, incl. 21 X1 chapters and 25 IB ideas).

### 9.2 Letter families
Each letter is one track. Lane = where it sits on the Plan (lock lane runs one at a time).

| Letter | Track | Steps | Lane |
| --- | --- | --- | --- |
| **M** | Media: render/voice bake-off, host | M0 setup, M1, M1b, M1V8 | GPU |
| **H** | Hub: shared repo, reviewer home | H1, H2 | Lock |
| **I** | Index the book | I1 | Lock |
| **K** | Knowledge (concept) map | K1, K2, K3, K4 | Lock |
| **X** | eXtra research (dossiers) | X1.01–X1.21, X2a–c, X3a–b | Research |
| **A** | App shell | A0 | Lock |
| **V** | 3D Viewer + drills | V1, V2, V3 | Lock |
| **S** | Studio (draft + review cards) | S1 | Lock |
| **W** | Workflow tracker | W1, W2, W3, W3F | Lock |
| **C** | Cards (content) | C1, C2 | Lock |
| **L** | Learning app | L1, L1F, L2, L3 | Lock |
| **U** | UI look | U1, U2, U2F, U3 | Lock |
| **SR** | Sources & Resources | SR1 | Lock |
| **P** | Plan an episode | P1 (S1E01) | GPU |
| **R** | Render a video | R1 | GPU |
| **F…** | Flags (⚑ decisions) | FD digest, FA answers | You / Lock |
| **GATE** | Use gate: 7 days of real use | GATE | You |
| **D / G** | After-gate: Drive sync, Guide | D1, G1 | Ideas |
| **IB** | Ideas backlog items | IB01–IB25 | Ideas |
| **Fixes** | One-off repairs | CIG (CI guard), MAPF (map compare), WCON (Windows UTF-8) | Lock |
| **Early docs** | Ideation setup, all done | R0, PB, UR, QB, DR, VS, VS2, VS2P | — |

Watch: **R0** (research layer, done) and **R1** (render) share a letter but are different tracks. **M0** is setup, not media.

### 9.3 Other id families
These are not steps; they hang off steps.

| Id | What it is | Example | Lives in |
| --- | --- | --- | --- |
| `T<n>` (+ b/c) | Owner check on real devices | T14 = SR1; T13 → T13b → T13c = U1 → U2 → U3 | owner-test-checklist.md |
| `<step>.q<n>` | Owner input: decide, answer or do | X1.03.q1, W2.q1 | steps.json `inputs` |
| `D-###` | Decision (why) | D-098 = SR1 sources | DECISIONS.md |
| `G-xxx` | Review gate | G-Sci, G-Learn, G-Story, G-Art, G-Eng, G-A11y, G-Owner | playbook §2 |
| `E` | Book code (Langman) | E = Embryology | README |
| `E<ch>.<sec>` | Book section | E05.02 | content/E/index |
| `E<ch>.<sec>.<nn>` | Concept card | E05.01.03 | content/E |
| `R<nn>`, `R05xx` | Trusted source | R06, R05pn | source-registry.md |
| `S<n>E<nn>` | Video episode | S1E01 Gastrulation | episodes-catalog.md |
| `IB<nn>` | Idea in the backlog | IB07 Trace a cell | ideas-backlog.md |
| `QR<nn>` | Quality reference reel | QR04, QR05 | quality-references.md |
| `CS<n>` | Carnegie stage (biology) | CS11 | GLOSSARY §7 |
| `AN<n>.<n>` | NMC curriculum code | AN43.4 | curriculum |
| v<n> | App version | v21 = SR1 | Settings › Version |
| Route A / B | How a chat commits | A = pushes from chat; B = you run sync.bat | setup-guide |
| Marks | Fact confidence | ✔✔ ✔ ≈ ⚑ ✚ | RULES B6–B7 |

Owner-check map: T1 M1 · T1b M1b · T2 K1 · T3a A0 · T3b V1 · T3c C1 · T3d C2 · T4 L3 · T5 H1 · T7 L1 · T7b L1F · T8 V2 · T8b V3 · T9 L2 · T10 H2 · T11 W1+W2 (T6 folded in) · T12 K3 · T13 U1 · T13b U2 · T13c U3 · T14 SR1.
