# S1E01 Gastrulation — storyboard + shot list

*(Purpose: what each shot shows, its scene + day key, cameras, labels, honesty tag and caption band; V-step needs. Source of truth: `content/E/episodes/S1E01/shots.json`. Updated: 22 Nov 2026 · Bio · Episode · S1E01 script (P1 ①).)*

## Frame rules used (all shots)

- **Lesson + General (16:9):** captions 85–95 % from the top; bottom-left stack above the 84 % line: scale bar + honesty tag, axes, day/stage (visual-style §10). Labels ≤ 6, outside the subject's outline, leader lines (§12).
- **Short (9:16):** M1b.q10 = **B** (D-059): captions **68–72 %, bottom-anchored at 72 %**, on host *and* anatomy shots; axes + scale bar move **top-left** (patch note `patches/visual-style-s1.md`). Labels ≤ 3. Cuts every 1–3 s; reveals hold ≥ 1 s.
- **Host shots:** Nani (D-048, H-a in Blender, D-059). Any host shot with colour tokens on screen → neutral/cool key on her, or tokens on their own panel (D-059 (5)). Every host shot plans `cam_short` + `cam_lesson` on one scene (N1). Host never shows anatomy (playbook §5b).
- **Always on 3D shots:** day/stage/size stamp, scale bar, axis gizmo (B2, H4). Stamps from the scene's day keys: day 15 · CS06 · ≈0.2 mm; day 17 · CS07 · ≈0.4 mm; day 18 · CS08 · ≈1.25 mm (dossier §1). Between keys the viewer eases (e.g. 'Day 16 · CS06–07 · ≈0.3 mm').
- **Colour mode:** layer mode on every shot (no segment mode, no legend chip). Accent ring = 'look here' only; on tracer shots the ring is the marked cell's alone (scene spec §6).
- **Reduced motion:** push-ins/orbits → cuts; no dust; label fades stay (§8).

## Storyboard (Lesson order; General + Short reuse the same scene states)

- **S01** (host) `host (tools/m1b-host)` day — — Nani asks the question to camera; book closed on her lap. Labels: none · tag: none · cams: cam_short + cam_lesson · key: warm key (no tokens on screen) · needs: N1 · lines: L01, G01
- **S02** (host+panel) `host + terms strip` day — — Terms strip, 5 s: 3 chips per profile — MBBS 'germ layers · primitive node · notochord' (L02), General 'epiblast · primitive streak · gastrulation' (G02); host in a corner cut-in. Labels: none · tag: none · cams: cam_lesson (Lesson/General only) · key: token panel: chips on their own neutral panel, host keeps warm key (D-059 (5)) · needs: N1, N2 · lines: L02, G02
- **S03** (3D) `sc-E00.01.04` day 15 · view: top (From the back) — Establish: two-layer disc, slow push-in. Labels: Epiblast, Hypoblast · General labels: none · tag: Colours illustrative · cams: cam_lesson + cam_short · lines: L03, L04, G03
- **S04** (3D) `sc-E00.01.04` day 15 · view: top — Push in to the caudal midline; streak ring (accent); stamp Day 15 · CS06. Labels: Primitive streak · tag: Colours illustrative · cams: cam_lesson + cam_short · lines: L05, L06, G04
- **S05** (3D) `sc-E00.01.04` day 15→16 · view: top, close — Ring moves to the cranial end; the mound is shown, not named yet (named at L18/S14). Labels: none · tag: Time compressed · cams: cam_lesson + cam_short · lines: L07
- **S06** (3D) `sc-E00.01.04` day 16 · view: top, pull back — Pull back to whole disc; axis gizmo arrows Cranial/Caudal highlighted. Labels: Primitive streak · tag: Colours illustrative · cams: cam_lesson + cam_short · needs: N12 · lines: L08, G05
- **S07** (3D) `sc-E00.01.04` day 15 · view: side (From the right), lengthwise cut — Rewind to day 15; marked cell appears in the epiblast (accent ring is the cell's alone). Labels: Marked cell, Epiblast · General labels: Marked cell · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3, N4 · lines: L09, G06
- **S08** (3D) `sc-E00.01.04` day 15→15.5 · view: side, lengthwise cut — Cell moves to the streak, briefly changes shape and slips under (invagination; no sheet stretch). General G07: camera stays on the marked cell through the whole analogy (no cut ahead to S10, keeps time order). Labels: Marked cell, Primitive streak · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3, N4 · lines: L10, G07
- **S09** (3D) `sc-E00.01.04` day 15.5→16 · view: side, lengthwise cut — Earlier cells (ghost tracer t-endo) replace the hypoblast; endoderm label as the sheet forms. Labels: Endoderm, Hypoblast · General labels: none · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3 · lines: L11, L12, G08
- **S10** (3D) `sc-E00.01.04` day 16 · view: side, lengthwise cut — Our cell settles between the layers; mesoderm label. Labels: Marked cell, Mesoderm · General labels: Marked cell · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3, N4, N12 · lines: L13, G09
- **S11** (3D) `sc-E00.01.04` day 16→17 · view: top, semi-transparent epiblast — Mesoderm sheet spreads sideways + cranially; marked cell ringed, riding the sheet. Labels: Mesoderm, Marked cell · General labels: none · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3 · lines: L14, G10
- **S12** (3D) `sc-E00.01.04` day 17 · view: side, lengthwise cut — Cells left on top lit; marked cell ringed below them; label Epiblast → Ectoderm swap. Labels: Ectoderm · General labels: none · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3, N6 · lines: L15, G11
- **S13** (3D) `sc-E00.01.04` day 17 · view: front (From the head), transverse cut through the streak + slab — D9 section: ectoderm / mesoderm / endoderm, yolk-sac side ventral; marked cell ringed in the mesoderm; hold. Labels: Ectoderm, Mesoderm, Endoderm · tag: Not to scale · cams: cam_lesson + cam_short · needs: N3, N7 · lines: L16, L17, G12
- **S14** (3D) `sc-E05.02.01` day 16 · view: top — Opens on the day-17 frame, our marked cell dimmed out in the lateral mesoderm (end of its t-meso path); stamp counts back to day 16 (N11); pan to the node; prenotochordal cells run forward toward the head end. Labels: Primitive node · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3, N4, N11, N12 · lines: L18, L18b
- **S15** (3D) `sc-E05.02.01` day 16→17 · view: end (transverse cut, cranial of node) — Notochordal plate in the endoderm, then folds into a rod; 'Notochord' label appears only on L20 (no label on the plate stage — the voice does not name it). Labels: Endoderm, Notochord · tag: Time compressed · cams: cam_lesson + cam_short · lines: L19, L20
- **S16** (3D) `sc-E05.02.01` day 17→18 · view: side — Book order: head end of the rod first, tail parts added as the streak moves back (D-029: book version only). Labels: Notochord · tag: Time compressed · cams: cam_lesson + cam_short · lines: L21, L22
- **S17** (3D) `sc-E05.02.01` day 18 · view: end — Rod in the midline under the ectoderm; no neural tube drawn or named. Labels: Notochord · tag: Simplified · cams: cam_lesson + cam_short · lines: L23
- **S18** (3D-adult) `new: sc-S1E01-18 (adult disc, Z-Anatomy, D-021)` day adult · view: spine segment, one disc cut; cm scale bar + 'Adult' stamp replace the day stamp; Z-Anatomy credit + licence row (D-021) — This becomes: nucleus pulposus at the core of an intervertebral disc; vertebrae dim (ctx). Labels: Nucleus pulposus · tag: Not to scale · cams: cam_lesson + cam_short · needs: N8 · lines: L24
- **S19** (3D) `sc-E00.01.04` day 17 · view: top, mesoderm only — This becomes: mesoderm sheet lit, rest ctx; marked cell ringed in it; no icons on anatomy — the voice carries the list. Labels: Mesoderm · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · needs: N3 · lines: L25, G13
- **S20** (3D) `sc-E00.01.04` day 17 · view: top — Clinical link slot: replay starts on the marked cell's entry point in the streak (2 s), then ring the caudal streak; 'Clinical link' tag top-left. Labels: Primitive streak · tag: Exaggerated for clarity · cams: cam_lesson + cam_short · **Clinical link slot** · needs: N9 · lines: L26
- **S21** (diagram) `new: sc-S1E01-21 (caudal remnant diagram)` day — · view: sagittal sketch — Diagram of a remnant at the sacrococcygeal region (no patient imaging, D6). Labels: Sacrococcygeal teratoma · tag: Simplified · cams: cam_lesson + cam_short · **Clinical link slot** · needs: N9 · lines: L27, L28
- **S22** (3D) `sc-E00.01.04` day 17 · view: front, transverse cut + slab — Payoff: back to the S13 section; marked cell shown in mesoderm. Labels: Ectoderm, Mesoderm, Endoderm · tag: Not to scale · cams: cam_lesson + cam_short · needs: N3, N7 · lines: L29, L30, G14
- **S23** (check) `sc-E00.01.04` day 17 · view: front, transverse cut — 2 Checks: tap-the-layer (spatial) + spoken-choice MCQ with ≤ 3-word chips; labels off for the tap; on the reveal (L31a/G15a) the Mesoderm label and the marked cell's ring come back. Labels: none · tag: Not to scale · cams: cam_lesson + cam_short · needs: N10 · lines: L31, L31a, L32, L32a, G15, G15a, G16, G16a
- **S24** (host) `host` day — — Teaser ≤ 5 s; Nani opens the book — pages blank/abstract, no diagram (host props carry no diagrams, §5b). Labels: none · tag: none · cams: cam_short + cam_lesson · key: warm key · needs: N1 · lines: L33, G17
- **SS1** (host+3D) `host / sc-E00.01.04 d15` day 15 — Frame 1: day-15 disc, epiblast lit, hypoblast dimmed ('this one sheet'), question starts at 0 s; Nani cut-in at ~1.5 s; marked cell visible from ch2. Labels: none · tag: Colours illustrative · cams: cam_short · key: neutral/cool key on Nani (tokens on screen) · needs: N1 · lines: R01
- **SS2** (3D) `sc-E00.01.04` day 15 — S04 push-in → S05 close → S06 pull-back (3 cuts); the streak gets label + glow, no ring — the accent ring is the marked cell's alone. Labels: Primitive streak, Marked cell · tag: Exaggerated for clarity · cams: cam_short · lines: R02
- **SS3** (3D) `sc-E00.01.04` day 15→15.5 — S07 → S08 shape change → S08 slip-under (3 shots, ~2.6 s each). Labels: Marked cell · tag: Exaggerated for clarity · cams: cam_short · needs: N3, N4 · lines: R03
- **SS4** (3D) `sc-E00.01.04` day 15.5→16 — S09 → S09 endoderm close → S10 → close on the marked cell's ring (4 shots ~2.4 s + 1.5 s hold). Labels: Mesoderm · tag: Exaggerated for clarity · cams: cam_short · needs: N3 · lines: R04
- **SS5** (3D) `sc-E00.01.04` day 17 — S12 ring → S11 top → S12 cells-on-top close → 1.5 s close on the marked cell's ring (4 shots ~2.1 s + 1.5 s hold). Labels: none · tag: Exaggerated for clarity · cams: cam_short · needs: N3, N6 · lines: R05
- **SS6** (3D) `sc-E00.01.04` day 17 — Section cut-in → ring on the marked cell in mesoderm → 2 s hold (3 beats). Labels: Mesoderm, Marked cell · tag: Not to scale · cams: cam_short · needs: N3, N7 · lines: R06
- **SS7** (endcard) `end card` day — — 'Full episode in the app' + chip 'Gastrulation · Part 1'; key structure + title inside the centre 4:5 crop (§15). Labels: none · tag: none · cams: cam_short · lines: R07

## Shot list (table)

| Shot | Scene | Day | Labels | Tag | Lines | Needs |
|---|---|---|---|---|---|---|
| S01 | `host (tools/m1b-host)` | — | — | — | L01, G01 | N1 |
| S02 | `host + terms strip` | — | — | — | L02, G02 | N1, N2 |
| S03 | `sc-E00.01.04` | 15 | Epiblast, Hypoblast | Colours illustrative | L03, L04, G03 | — |
| S04 | `sc-E00.01.04` | 15 | Primitive streak | Colours illustrative | L05, L06, G04 | — |
| S05 | `sc-E00.01.04` | 15→16 | — | Time compressed | L07 | — |
| S06 | `sc-E00.01.04` | 16 | Primitive streak | Colours illustrative | L08, G05 | N12 |
| S07 | `sc-E00.01.04` | 15 | Marked cell, Epiblast | Exaggerated for clarity | L09, G06 | N3, N4 |
| S08 | `sc-E00.01.04` | 15→15.5 | Marked cell, Primitive streak | Exaggerated for clarity | L10, G07 | N3, N4 |
| S09 | `sc-E00.01.04` | 15.5→16 | Endoderm, Hypoblast | Exaggerated for clarity | L11, L12, G08 | N3 |
| S10 | `sc-E00.01.04` | 16 | Marked cell, Mesoderm | Exaggerated for clarity | L13, G09 | N3, N4, N12 |
| S11 | `sc-E00.01.04` | 16→17 | Mesoderm, Marked cell | Exaggerated for clarity | L14, G10 | N3 |
| S12 | `sc-E00.01.04` | 17 | Ectoderm | Exaggerated for clarity | L15, G11 | N3, N6 |
| S13 | `sc-E00.01.04` | 17 | Ectoderm, Mesoderm, Endoderm | Not to scale | L16, L17, G12 | N3, N7 |
| S14 | `sc-E05.02.01` | 16 | Primitive node | Exaggerated for clarity | L18, L18b | N3, N4, N11, N12 |
| S15 | `sc-E05.02.01` | 16→17 | Endoderm, Notochord | Time compressed | L19, L20 | — |
| S16 | `sc-E05.02.01` | 17→18 | Notochord | Time compressed | L21, L22 | — |
| S17 | `sc-E05.02.01` | 18 | Notochord | Simplified | L23 | — |
| S18 | `new: sc-S1E01-18 (adult disc, Z-Anatomy, D-021)` | adult | Nucleus pulposus | Not to scale | L24 | N8 |
| S19 | `sc-E00.01.04` | 17 | Mesoderm | Exaggerated for clarity | L25, G13 | N3 |
| S20 | `sc-E00.01.04` | 17 | Primitive streak | Exaggerated for clarity | L26 | N9 |
| S21 | `new: sc-S1E01-21 (caudal remnant diagram)` | — | Sacrococcygeal teratoma | Simplified | L27, L28 | N9 |
| S22 | `sc-E00.01.04` | 17 | Ectoderm, Mesoderm, Endoderm | Not to scale | L29, L30, G14 | N3, N7 |
| S23 | `sc-E00.01.04` | 17 | — | Not to scale | L31, L31a, L32, L32a, G15, G15a, G16, G16a | N10 |
| S24 | `host` | — | — | — | L33, G17 | N1 |
| SS1 | `host / sc-E00.01.04 d15` | 15 | — | Colours illustrative | R01 | N1 |
| SS2 | `sc-E00.01.04` | 15 | Primitive streak, Marked cell | Exaggerated for clarity | R02 | — |
| SS3 | `sc-E00.01.04` | 15→15.5 | Marked cell | Exaggerated for clarity | R03 | N3, N4 |
| SS4 | `sc-E00.01.04` | 15.5→16 | Mesoderm | Exaggerated for clarity | R04 | N3 |
| SS5 | `sc-E00.01.04` | 17 | — | Exaggerated for clarity | R05 | N3, N6 |
| SS6 | `sc-E00.01.04` | 17 | Mesoderm, Marked cell | Not to scale | R06 | N3, N7 |
| SS7 | `end card` | — | — | — | R07 | — |

## Simplifications and omissions (G-Sci item 9 — shown or in the description)

- Amnion and yolk sac not drawn (scene disclaimers); the voice names the yolk sac only as the side the endoderm faces (L16).
- Layer thickness not to scale; marked cell drawn larger (tracer disclaimer); time compressed on every moving shot (day 15 → 17 in ~2 min).
- Oropharyngeal and cloacal membranes not shown (scene disclaimers) — not mentioned in the script.
- 'Marked cell' label: used by sc-E00.01.04 (V3 trace drill) but not yet in GLOSSARY → commit task adds a GLOSSARY line (tracer convention, no book section).
- Notochord: the book order only (head end first); the middle-first human data are not animated (D-029 (3)); one spoken pointer to the card (L22, MBBS only).
- Neural tube not drawn or named (L23 says only 'help build the spine').
- Fate map (E05.04.01) left out — not a core card for S1E01; the marked cell's mesoderm subtype is not named.

## V-step needs (scenes or spec work that ② or R1 needs)

- **N1** — Host scene: add `cam_lesson` (16:9) beside the 9:16 camera — one scene, two cameras (M1b to-do; visual-style §10). Lines S01/S24/SS1. Step: M1V8 or R1.
- **N2** — Terms-strip graphic: 3 term chips on a neutral token panel next to the host (D-059 (5)); chips use layer tokens only for layer names (none here → neutral chips). Step: R1.
- **N3** — Video use of a tracer: scene spec §5/§6 make `tracer` drill-only ('never in Try it, stills or video'). S1E01 needs the marked cell on screen. Spec change + engine flag, e.g. shot `show.trace` (scene-spec §10). Step: V-step (V4?) before ② can show it; ② may fake it as an animatic placeholder.
- **N4** — New tracer `t-meso` (with the scene disclaimer 'marked cell drawn larger' kept on every shot it appears in) in sc-E00.01.04 (and the same cell in sc-E05.02.01 at its day-16 lateral mesoderm position, for S14): an epiblast cell that ingresses after the endoderm cell and ends in mesoderm, then spreads laterally (path keyed days 15 → 17). The existing `t-endo` stays as the 'first cells' ghost. Step: V-step (scene edit + scene-check path rules).
- **N6** — Label swap 'Epiblast → ectoderm' becomes a spoken text item (C1 G-A11y to-do: '→' needs spoken text) and a clean 'Ectoderm' label at day 17. Step: V-step / scene owner.
- **N7** — Shot-sheet `show` state: §10 has no `view/cut/slab_mm/layers/trace` per shot — add `show` (same shape as card drills §8a) so S13/S22 can ask for the transverse cut + slab at day 17. Step: R1 shot-sheet code (spec first).
- **N8** — Adult anchor scene `sc-S1E01-18`: adult lumbar segment, one intervertebral disc cut to show the nucleus pulposus (Z-Anatomy adult mesh, rendered video only, D-021); vertebrae ctx. Step: V-step or R1.
- **N9** — Clinical slot: caudal streak remnant + sacrococcygeal teratoma diagram `sc-S1E01-21` (our own diagram, no imaging, D6/§14); streak shrink after day 18 is not in any scene (keys end at day 17/18) → either a day-28 key or a diagram only. Step: V-step.
- **N11** — Day stamp rewinds on screen (counts back) on the S06→S07 and S13→S14 time jumps, so a jump back in day reads as intended (G-Story r1). Step: ② animatic overlay, then R1.
- **N12** — Day-16 stamp agrees across scenes: sc-E00.01.04 eases day 16 to 'CS06–07 · ≈0.3 mm' while sc-E05.02.01 keys day 16 as 'CS07 · 0.4 mm'. Add a day-16 key to sc-E00.01.04 = CS07 · 0.4 mm (dossier §1 book 16–18 d, R06/R08), or re-key sc-E05.02.01. Step: V-step (scene edit + scene-check).
- **N10** — Spatial Check in video: tap-the-layer on a section is an app drill (V2 label drill); the video shows the question + a 4 s pause and the answer reveal; the app version links to the E05.01.03 drill. Step: R1 (player Checks).

## Per device (C13) — what ② must lay out

- **Phone portrait:** the Lesson plays inline as a 16:9 preview with the transcript + Checks below; tap → full-screen landscape. The Short plays full-frame 9:16.
- **Phone landscape / tablet:** Lesson full-width; tablet portrait shows the transcript beside or below (two panes).
- **Desktop:** Lesson with transcript + shot list side panel (animatic review mode); labels must not look oversized at 1080 (playbook §6.10).
- G-Art checks one 16:9 frame at 210 px high and at 1080, and the 9:16 frame at phone size, in ② (visual-style §10).
