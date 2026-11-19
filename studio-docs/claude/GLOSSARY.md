# Glossary

*(Purpose: one name per thing — terms by thread, production, app and project terms. Updated: 19 Nov 2026 · Bio · Build · W1 progress map — §8 progress map, steps.json, owner input, can start now, proposed status (D-040). Before: 19 Nov 2026 · Bio · Research · X1 Ch 06 — §7 CS11–CS23 events + R02 age note (D-039). Before: 19 Nov 2026 · Bio · Build · V1 viewer — day key, stamp, cut plane, axis gizmo, still; embryo axes + planes. Before: 18 Nov 2026 · Bio · Fix · doc reconcile — ported from the uploaded copy: §5 rendition, §6 device class, input class, test matrix, layout check, contact sheet (D-033); added host, Short, kinetic captions (D-032). Our own words. Each embryology term gets its book citation once I1 numbers the sections. New term → add it here.)*

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
- **Shot:** one continuous piece of an episode, made from one scene. **Storyboard:** one frame per beat. **Shot list:** shots with duration and day range.
- **Render:** turning a scene into video frames. **Master:** the final full-quality episode file. **Clip:** a 10–20 s cut used on a card.
- **Rendition:** one encode of a master at a set resolution (720p for phones; 1080p for tablet/desktop if M1 allows — D-033).
- **TTS:** text-to-speech voice-over. **VTT / SRT:** subtitle files. **Drift:** subtitle lag behind speech.
- **Host:** the episode's on-screen character (cell/embryo by default · animal · stylised human · none); asks, reacts, jokes, never shows anatomy (audience profile `host`, playbook §5b, D-032).
- **Short:** the 9:16, ≤ 60 s audience cut (`-short` suffix) — hook ≤ 1 s, cuts every 1–3 s (playbook §5b). **Kinetic captions:** styled, toggleable subtitles for Shorts — one phrase at a time, key term highlighted, Latin + Devanagari.
- **Bake-off:** making the same shot several ways and comparing (M1).
- **Animatic:** a rough three.js version of an episode with scratch voice, reviewed before any final render (RULES H3).
- **Render manifest:** the record written with every render — scene hash, tools, GPU, settings, seed, voice (RULES H7).
- **Preview render:** a fast low-res render (`--preview`) for checking motion and framing.

## 6. App & engine terms
- **Part 0:** orientation cards (`E00.01.nn`) — axes, staging, scale, colour key, reading a section, how to use the app.
- **Card statuses:** Read → Understood (Check passed) → Can explain.
- **Remember deck:** spaced review of read cards at 1, 3, 7, 21, 60 days.
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
