# Teaching methods — evidence → our design rules

*(Owner doc for how we teach. Created 17 Nov 2026, D-011. Each method: what the research says (own words) → what we do. New method → add a row and, if it's a must, a RULES §D line. Updated: 26 Nov 2026 · Bio · Fix · video craft — methods 1–5 + checklist: ideas, primer, label numbers (D-107; closes D-102 (1)).)*

## Evidence sources
| Id | Source | Strength |
|---|---|---|
| M01 | Mayer, *Cognitive Theory of Multimedia Learning* — principles kept only where median effect ≥ d 0.40 (Mayer 2008/2009; Chartered College summary) | Strong (many RCTs) |
| M02 | Guo, Kim & Rubin 2014 — 6.9 M edX video sessions; median engagement peaks around 6 min, falls to ~50 % at 9–12 min | Strong (observational, huge) |
| M03 | Deng, Gluckstein & Larsen 2015, *Perspect Med Educ* — self-testing with spaced repetition (Anki, Q-banks) independently predicted licensing-exam scores | Moderate |
| M04 | 3D visualisation meta-analyses: Yammine & Violato 2015 (*Anat Sci Educ*); Bogomolova et al. 2021 (*Med Educ*, 13 RCTs); Wang et al. 2024 (*BMC Med Educ*, 39 RCTs, 2,959 learners) | Strong |
| M05 | Embryology-specific: gastrulation, neurulation and folding are hard because they are 3D movements that 2D slides show badly (Playdoh model study, *J Microbiol Biol Educ* 2021; flexagon gastrulation model, Kirkness et al.); animated folding module with long + cross sections (MedEdPORTAL 2007) | Moderate (small studies) |
| M06 | Narrative / cinematic clinical stories (Bland 2025, *JMIR Med Educ*, n = 40; Patel & Snyder 2023 patient narratives) | Weak — engagement shown; learning gain not proven |
| M07 | de Bakker et al. 2016 (*Science*) and de Bree et al. 2018 — textbook embryo pictures partly come from old or non-human specimens; real human data differ in places | Strong (primary data) |
| M08 | NMC CBME 2024 — competency codes, knows / knows-how levels, integration | Curriculum mandate |

## Methods we adopt
| # | Method | Evidence | What we do (rule) |
|---|---|---|---|
| 1 | **Segmenting** — short pieces, learner controls pace | M01, M02 | Lessons 6–10 min, in segments of 60–120 s and **ideas** of 20–60 s (one chapter per idea); the learner sets the pace — Study pace pauses after each idea (playbook §6b.1, RULES D10). Shorts ≤ 60 s never pause. Cards = one screen. |
| 2 | **Pre-training** — learn the names before the process | M01 | Core cards before the episode (Ready to watch); Part 0 first; a ~20 s "Meet the parts" primer after the cold open in Lessons (≤ 3 parts; 15 s in the General cut; playbook §6b.3) — replaces the old 5-s terms strip. |
| 3 | **Signalling** — cue what matters | M01 | The structure being named glows/outlines at that moment; germ-layer tokens (RULES B3); idea titles on the scrubber + transcript (app, not the frame); ≤ 1 accent ring and ≤ 1 moving focus at a time (MM6). |
| 4 | **Temporal & spatial contiguity** — word and picture together | M01 | A label appears *on* the structure *as* the voice says it: fade-in −0.3 … +0.5 s from the word, text ≤ 12 % of the short side from its dot (MM2, MM3); never a legend far away. |
| 5 | **Redundancy & modality** — narrate, don't print paragraphs | M01 | On-screen text = 1–3-word labels + scale/day stamp only. Subtitles are a toggle (on by default when muted) — not sentences baked into the frame; Lesson captions are never burned in (Shorts' kinetic captions are the a11y exception) (MM5). |
| 6 | **Coherence** — cut interesting-but-irrelevant extras | M01 | No trivia, no music under key narration, no decorative motion. Extras go to More. (Pairs with D5 "accuracy beats drama".) |
| 7 | **Personalisation** — conversational voice | M01 | Scripts speak to "you"; plain words; one guide character per season. |
| 8 | **Interactive 3D beats static 2D for spatial knowledge** (gain larger for spatial than factual; takes more time) | M04 | Every Tier A card has a rotatable scene + day scrubber; Checks test spatial skill (rotate-to-match, which day, order frames). |
| 9 | **Depth matters** — stereo views beat flat ones; phones are flat | M04 | Fake depth: soft shadows, slow orbit, motion parallax, cut-plane slices; optional stereo/VR later (backlog). |
| 10 | **Show long and cross sections together** for folding | M05 | Split-screen: 3D body + live cut plane at the same day. Every folding shot ends on the transverse section the learner will meet in exams. |
| 11 | **Hands-on modelling helps 3D movement** | M05 | "Make it" on hard cards: a 1-min paper/clay fold the learner does with a sheet of paper (backlog #21). |
| 12 | **Retrieval + spacing** | M03 | Checks set card status (B4); Remember deck 1/3/7/21/60 d; each episode opens with its question (pre-question) and ends with 2 Checks. |
| 13 | **Story frames attention; measure, don't assume** | M06 | Keep the five story formats, but the recall quotient (24 h / 7 d) decides which formats stay. Log per-format recall in the review log. |
| 14 | **Science is alive** | M07 | Where human data corrected the textbook (⚑), the card adds a "Newer evidence" line; good material for Mystery episodes. |
| 15 | **Curriculum-mapped** | M08 | Each card carries its NMC AN code(s); coverage report shows uncovered competencies. |

## Episode checklist (from the above)
- [ ] Opens with a question or clinical mystery (D3)
- [ ] ≤ 3 new terms, shown first (2) and named on the structure (4)
- [ ] One objective per idea (20–60 s); one chapter per idea; `ideas[]` breaks signed (1)
- [ ] Lessons: primer of ≤ 3 parts after the cold open (2)
- [ ] Final render passes MM1–MM8 (playbook §2)
- [ ] No sentence on screen; labels + day/scale only (5, B2)
- [ ] 3D shot ends on the section view students meet in exams (10)
- [ ] "This becomes…" adult anchor (D4)
- [ ] 2 Checks, at least one spatial (8, 12)
- [ ] Every line ✔ or ✔✔; ⚑ handled; no ≈ (B1, B7)
