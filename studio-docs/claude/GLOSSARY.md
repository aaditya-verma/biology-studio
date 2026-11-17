# Glossary

*(Purpose: one name per thing — terms by thread, production, app and project terms. Updated: 17 Nov 2026 · Bio · Ideation · Setup guide (D-025). Our own words. Each embryology term gets its book citation once I1 numbers the sections. New term → add it here.)*

## 1. Timeline & staging (thread T)
- **Fertilization age vs gestational age:** embryology counts from fertilization; clinicians count from the last menstrual period (about 2 weeks earlier). Always say which.
- **Embryonic period:** weeks 3–8, when the organ systems are laid down. **Fetal period:** month 3 to birth, mostly growth and maturation.
- **Carnegie stage (CS01–CS23):** the standard staging of human embryos by form, not age, covering roughly the first 8 weeks. Table in §7 (filled in I1 with sources).
- **Day / week notation:** "day 17", "week 3"; episodes show both on screen (RULES B2).

## 2. Germ layers (thread G) — colour tokens fixed (RULES B3)
- **Epiblast / hypoblast:** the two layers of the bilaminar disc in week 2. The epiblast gives rise to all three germ layers.
- **Gastrulation:** week 3 process that turns the two-layer disc into three germ layers.
- **Ectoderm** (`--g-ecto`): outer layer → skin epidermis, nervous system.
- **Mesoderm** (`--g-meso`): middle layer → muscle, bone, blood, heart, kidneys.
- **Endoderm** (`--g-endo`): inner layer → gut lining and its glands, lungs.
- **Neural crest** (`--g-crest`): cells that leave the edges of the neural folds and migrate widely; sometimes called the fourth germ layer.

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
- **Shot:** one continuous piece of an episode, made from one scene. **Storyboard:** one frame per beat. **Shot list:** shots with duration and day range.
- **Render:** turning a scene into video frames. **Master:** the final full-quality episode file. **Clip:** a 10–20 s cut used on a card.
- **TTS:** text-to-speech voice-over. **VTT / SRT:** subtitle files. **Drift:** subtitle lag behind speech.
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
- **Debug flag:** a switch, off by default, that shows extra detail for one area — `?debug=map,viewer` in the app, `--debug` / `--dry-run` / `--only` / `--preview` on tool scripts, `debug: true` in a scene (RULES I5).
- **Edit hook:** a marked place to change something — one home per value (tokens, `02-config.js`, `content/`, `strings.js`), `// EDIT:` markers in code, and the ✎ button in testing mode that shows an item's id + file and copies an "edit this" prompt (RULES I6).
- **Edit prompt:** the text the ✎ copies; paste it into a `Bio · Fix · <id>` chat.

## 7. Carnegie stages (to fill in I1, with sources)
| Stage | Approx. day | Key events | Taught in |
|---|---|---|---|
| CS01 | | | |
| … | | | |
| CS23 | | | |

## 8. Project terms
- **Owner doc:** the one doc that owns a fact (INSTRUCTIONS §2); it wins on conflict.
- **Pendencies:** open questions, blocks and owner to-dos — kept only in STATUS § Blocked + Owner reminders.
- **Changelog:** `logs/build-log.md`, newest first.
- **Review gate:** a check an artefact must pass (G-Sci, G-Learn, G-Story, G-Art, G-Eng, G-A11y, G-Owner; playbook §2).
- **Usage check:** the 1–3 suggestions at the end of a chat to keep the project lean.
- **Ready prompt:** the paste-in text that starts the next chat, with its chat name.
- **Owner / collaborator:** the owner (Aaditya) has the final say; a collaborator (first: the Professor) shares the project and proposes (D-025).
- **Studio home:** each person's laptop folder for the project — `tools\`, `apps\`, `models\`, `repo\` (owner: `D:\Projects\biology_studio`).
- **Build lock:** the line in STATUS § Lock that a Build chat takes first and frees at the end, so only one build runs across both people (RULES I8).
- **Handoff note:** what a collaborator chat sends the owner while only the owner edits docs (templates §10).
- **Laptop 1 / Laptop 2:** owner's / collaborator's render machine in `build/pipeline-reference.md`.
