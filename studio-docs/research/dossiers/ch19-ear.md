# Research dossier — Ch 19 · Ear (for C-step cards + episodes)

*(Purpose: cited, marked facts, staging, misconceptions and clinical correlates for Ch 19, the tenth chapter of Part 2. It is short — 4 sections of 1–3 pages and 1 box — and was read in one pass with sub-locators per subhead (internal ear, middle ear, external ear, hearing + its box). Cards draft from this file. Updated: 22 Nov 2026 · Bio · Research · X1 Ch 19 · by Aaditya (G-Sci fresh-eyes review: pass with fixes, 7 MUST + 9 SHOULD applied). Own words only; no book sentences, figures or tables (RULES §G). Every list is regrouped in our own order: the ear's parts by **what each part is made from** (placode · pouch · arches · surface), the clinical rows by **what goes wrong** (the sensing part · the conducting part · the outside part · the clues), never the book's page order.)*

**How to read a line:** fact in our words · `[book section · registry source]` · mark (RULES B6–B7): **✔✔** book + Tier 1 agree · **✔** book only · **⚑** book vs Tier 1 disagree (D-entry) · **✚** beyond the book (Tier 1 only; More / Tier D only, "beyond Langman") · **≈** blocks final. **Species tag:** a line from mouse or chick says so (*mouse*). Those lines can confirm a mechanism; they never give a human day or number. **Rates** are per 10,000 births unless stated. **The book gives no rate at all in Ch 19** — every rate here is ✚.

**Citation check, read before you cite:** checked 22 Nov 2026. `tools/card-check/citations.py` matches `R\d\d[a-z]{0,2}`, so the new ids **R05jk–R05kb** parse (after R05jz comes R05ka, as R05az → R05ba). Every PMID was grepped in the registry before its id was given — none was already there. Author lists are copied from the PubMed record (first three, then et al.). R05ed and R05bs stay retired. `sources.json` is rebuilt in this commit (`check.py --write-sources`, D-065 (6)). **Registry sources re-used:** R05iu (otic pit and otic crest at CS11), R05iv (otic vesicle gives crest to ganglion 7/8 at CS12), R05it (external ear movement, Kyoto), R05is (OAV spectrum, Ch 17), R05cb (CMV in developing countries, Ch 9), R06/R08 (stage tables). **Read and not used:** O'Rahilly 1963 (otic vesicle in staged human embryos — no PubMed abstract, so it cannot carry a mark; full text is the best human otic source, §10), Morton & Nance 2006 (newborn hearing screening review — no abstract), Jahrsdoerfer & Jacobson 1995 (Treacher Collins 1 in 50,000 — a quoted background figure in a case report, ≈ lead only), Torre-González 2022 ("more than 50 % genetic" — a regional review quoting a background figure, ≈ lead only), Quirk 2019 (inner-ear malformations "up to 20 %" — pictorial review, R05kb is primary data), Klockars & Rautio 2009 (microtia review — R05jy is larger and covers it), Zernotti 2019 (Argentina microtia — hospital records, R05jx is a registry).

**Ages — four clocks.** (1) The book's events are in **days or weeks after fertilization** (otic placode ~day 22, cochlear duct week 6, semicircular canals week 6, 2.5 turns by the end of week 8, cartilage shell hollows in week 10) and **months** for fetal events (meatal plug from the start of month 3, dissolves month 7; ossicles freed month 8) — read as after fertilization (D-030). (2) Specimen papers give **Carnegie stages** (R05iu, R05iv, R05jl, R05jp: Carnegie or Kyoto collections) or **CS + weeks after fertilization** (R05jk "approximately 6–10 weeks after fertilization"; R05jm "weeks of development" with CS16 = 6 weeks) — matched by stage to R08 (`tools/indexer/carnegie.json`, D-030 a). (3) **Fetal papers rarely define a clock:** R05jn ("the 16.5-week fetus") and R05jq (fetuses "15–16 weeks", "29–40 weeks") give none; R05jo ("weeks gestation") most likely means the last-period clock but does not define it; **R05jr's full text (X3a, 22 Nov 2026) names its clock** — gestational age by ultrasound in weeks + days, and it equates 12 weeks of gestation with week 10 of fetal development. Each fetal ⚑ below is checked on **both** readings (last-period clock ~2 weeks ahead of fertilization age) and holds either way. (4) Hearing-loss and rate papers count **at or after birth** — no conversion.

**Section locators (checked against the PDF, 22 Nov 2026; printed page = PDF page − 19):**
- **E19.00 p 351** — the ear's three parts and their jobs (opening lines).
- **E19.01 Internal ear pp 351–354** — otic placode → pit → vesicle, statoacoustic ganglion cells, ventral (saccule, cochlear duct) vs dorsal (utricle, canals, endolymphatic duct) p 351; *Saccule, cochlea and organ of Corti* pp 351–352 (duct outgrowth week 6, 2.5 turns by end of week 8, ductus reuniens, cartilage shell, scalae week 10, ridges and hair cells, tectorial membrane, spiral ligament and modiolus p 352); figures p 353; *Utricle and semicircular canals* **p 354** (canals week 6, crura, cristae and maculae, ganglion split).
- **E19.02 Middle ear pp 354–356** — *Tympanic cavity and auditory tube* p 354 (pouch 1, tubotympanic recess); *Ossicles* pp 354–356 (arch 1 malleus + incus, arch 2 stapes, freed month 8, endodermal mesenteries, ligaments; tensor tympani V3, stapedius VII **p 356**); antrum and mastoid pneumatization **p 356**; figures p 355.
- **E19.03 External ear p 356** — *External auditory meatus* (first-arch invagination, not cleft 1; meatal plug month 3 → month 7); *Eardrum* (three layers); *Auricle* (crest of arches 1–2 dorsal ends, mostly arch 2, HOXA2; ears start low in the neck).
- **E19.04 Hearing pp 356–357** — eardrum, muscles, ossicle lever and area ratio, cochlear fluid wave, place coding of pitch; *Clinical Correlates — Hearing loss and external ear abnormalities* **pp 358–359**.
- **E19.05 Summary p 359** · **E19.06 Problems p 359** (3 questions: placodes, middle-ear origins, bilateral microtia).

**I1 gaps** (tree.json) → I1 to-do:
- **Pages spill:** E19.01 ends **p 354** (I1 353 — the semicircular canals and the ganglion split sit on p 354 beside the start of E19.02); E19.02 ends **p 356** (I1 355 — the ossicle muscles, antrum and mastoid are on p 356); the *Clinical Correlates* box runs **pp 358–359** (I1 gives E19.04 356–358).
- **Two-column overlap:** p 356 holds the end of E19.02, all of E19.03 and the start of E19.04; p 354 holds the end of E19.01 and the start of E19.02.
- **Box title:** the one box is titled *Hearing loss and external ear abnormalities* (I1 records it only as CC×1 under E19.04). Cite its lines `E19.04 CC`.

---

## 1. Staging & scale — placode to a working ear (RULES B2)
Human anchors: **R06/R08** (stage definitions and classic ages), **R05iu** (20 *human* CS11 embryos), **R05iv** (24 *human* CS12 embryos), **R05jk** (27 *human* Kyoto samples CS17 → ~week 10, phase-contrast CT + MRI), **R05jl** (17 *human* Kyoto embryos, 33 ossicle sets CS18–23), **R05jm** (55 *human* embryos and fetuses, 6–13 weeks), **R05jp** (22 *human* Carnegie embryos CS13–23), **R05it** (171 *human* Kyoto MRIs CS17–23), **R05jn** (*human* fetal meatus), **R05jo** (167 *human* embryonic → postnatal ears), **R05jr** (*human* fetal cochleae). Days are the book's unless a source is named.

| When | Carnegie / clock | What happens `[section · source]` | Mark |
|---|---|---|---|
| ~Day 22 | CS10 | **Otic placode** — a thickening of surface ectoderm beside the hindbrain `[E19.01]` | ✔ (R08 stage features; no human abstract for the placode itself — O'Rahilly 1963, §10) |
| ~Day 24 | **CS11** | **Otic pit** deepening; its wall already gives **neural crest** cells to the faciovestibulocochlear ganglion and to a sheath round the pit `[E19.01 · R05iu]` | ✔✔ pit · ✚ crest from otic ectoderm |
| ~Day 26–30 | **CS12** | **Otic vesicle** (otocyst) closing off; it gives crest cells to **ganglion 7/8** `[E19.01 · R05iv]` | ✔✔ (book: vesicle at ~day 27, ganglion partly crest) |
| Week 4 (end) | CS13 | Vesicle has left the surface ectoderm; splits into a **dorsal** part (utricle, canals, endolymphatic duct) and a **ventral** part (saccule, cochlear duct) `[E19.01, E19.05]` | ✔ |
| Week 6 | **CS17** | **Cochlear duct** grows out of the saccule; the vesicle has lengthened and grown its **endolymphatic appendage** `[E19.01 · R05jk]` | ✔✔ |
| Week 6 → 7 | CS17 → **18** | **Semicircular canals** start as flat pouches of the utricle (book: week 6); by CS18 the anterior and posterior canals are full circles on a **common crus**; the cochlear duct **starts to coil** `[E19.01 · R05jk]` | ✔✔ canals · ✚ coiling starts CS18 |
| Week 6 | **CS16** | **Incus** primordium at the upper end of arch 1, separate from Meckel cartilage `[E19.02 · R05jm]` | ✔✔ (arch 1) · ✚ stage |
| Week 7 | **CS18 → 19** | In 3D reconstructions the **stapes** is recognisable at CS18 and the malleus and incus at CS19, lined up front → back as malleus, incus, stapes (R05jl); histology already shows all three primordia at CS16 (R05jm) `[E19.02 · R05jl, R05jm]` | ✚ stages (note d) |
| Week 6 → 8 | CS13 → 23 | **Auricle** forms round the end of cleft 1 — mostly from arch 2; the classic six hillocks are absent in most stages `[E19.03 · R05jp]` | ✔✔ arch 2 · **⚑ b** hillocks |
| Weeks 7–8 | CS17 → 23 | The ear moves mainly **sideways** with face growth, appearing to rise toward eye level `[E19.03 · R05it]` | ✔ (links D-078; note f) |
| Week 8 | **CS21 → 23** | All three ossicles are **cartilage** after CS21; they connect to each other after CS22; stapes base sits by the vestibule but has no footplate shape yet; malleus handle near the tubotympanic recess, still far from the meatus (CS23) `[E19.02 · R05jl]` | ✚ |
| End of week 8 | CS23 → fetal | Cochlear duct has **2.5 turns** (book); *human* CT: more than two turns just after the embryonic period (~weeks 9–10) `[E19.01 · R05jk]` | ✔ (note g — no clash shown) |
| Week 10 | fetal | Cartilage shell round the cochlear duct hollows → **scala vestibuli + scala tympani** (book) · a **prosensory** strip (SOX2) in the duct floor (R05jr) `[E19.01 · R05jr]` | ✔ · ✚ |
| From ~12 weeks of gestation (ultrasound clock; ≈ week 10 after fertilization — R05jr full text) | fetal | **First hair cells** (inner row first, basal turn; one cochlea at 11 wk 4 d showed early marker changes in 1 of 3 sections — possibly a start late in week 11); all three outer rows in the basal turn by 14 wk; nerve fibres reach the strip before the hair cells `[E19.01 · R05jr]` | **⚑ c** (book: organ of Corti in week 7) |
| Month 3 | fetal | **Meatal plug** — cells fill the bottom of the ear canal `[E19.03 · R05jn]` | ✔ start · ✔✔ plug present by 10 weeks (R05jn) |
| ~13 → 18 weeks (clock unclear) | fetal | Plug's inner disc splits to leave the eardrum's outer layer (15 wk); canal **open end to end by 16.5 weeks**, full shape by 18 weeks; canal skin cornifies at 18 weeks and clears outward `[E19.03 · R05jn, R05jo]` | **⚑ a** (book: plug dissolves in month 7) |
| ~20 weeks of gestation | fetal | Hair cells and spiral ganglion look **adult-like** — the time hearing is thought to begin `[E19.04 · R05jr]` | ✚ (More only, beyond Langman) |
| Month 8 → term | fetal | **Ossicles freed** from mesenchyme in month 8; cavity at least doubles; **antrum** forms late `[E19.02]` | ✔ |
| After birth | infancy → childhood | **Mastoid air cells** grow into the mastoid from the cavity lining `[E19.02]` | ✔ |

**Scale anchors (B2):** CS10 ~1.5–3 mm · CS11 ~2.5–4.5 mm · CS12 ~3–5 mm · CS13 ~4–6 mm · CS17–18 ~11–14 mm · CS23 ~23–32 mm (R08 classic). The book's figures show stage drawings at 24 days, 27 days, 4.5 weeks, 5–8 weeks and a fetus at 10 weeks, ~5 months and term — redraw our own scale bars.

---

## 2. Tier A facts — cited and marked
### E19.01.01 Otic vesicle and inner ear · AN40.3, AN43.3 (no NMC development code; note k)
- **A placode, not the brain, makes the inner ear.** Around day 22 a patch of surface ectoderm beside the hindbrain thickens (**otic placode**), sinks in as a **pit** and pinches off as the **otic vesicle** by the end of week 4. `[E19.01, E19.05 · R05iu, R05iv]` **✔✔** (pit at CS11, vesicle at CS12)
- **The hearing–balance nerve has two sources.** The **statoacoustic (VIII) ganglion** is built from placode cells (budding from the vesicle wall) plus neural crest; later it divides into a **cochlear** and a **vestibular** ganglion. `[E19.01 · R05iu, R05iv]` **✔✔** · ✚ the otic wall itself is a crest source from CS11 (R05iu) · links **D-079** (crest and placode ganglia, Ch 18)
- **One vesicle, two halves, two jobs.** **Ventral** → **saccule + cochlear duct** (hearing); **dorsal** → **utricle, three semicircular canals, endolymphatic duct** (balance). Together = the **membranous labyrinth**. `[E19.01, E19.05]` **✔**
- **The cochlear duct coils.** It grows out of the saccule in **week 6** and coils to **2.5 turns** by the end of week 8; a narrow **ductus reuniens** keeps it joined to the saccule. `[E19.01 · R05jk]` **✔✔** outgrowth at CS17 (week 6) · ✔ the 2.5 turns (note g) · ✚ coiling begins at CS18
- **Hair cells come late.** Book: the duct's cells form the **organ of Corti** in week 7 — an inner ridge (**spiral limbus**) and an outer ridge giving **one row of inner and three to four rows of outer hair cells**, capped by the gel-like **tectorial membrane**. `[E19.01]` **⚑ c** — *human*: a prosensory strip already present at 10 weeks (the youngest cochlea studied), **first hair cells from 12 weeks**, adult-like at 20 weeks (R05jr — full text: ultrasound gestational age, 12 wk ≈ week 10 after fertilization); the row pattern is ✔.
- **Balance sensors:** canals grow as flat pouches of the utricle in **week 6**; the middle of each pouch wall meets and disappears, leaving three tubes; each canal swells at one end (**ampulla**, with a **crista**), and two non-swollen ends join, so **five** crura reach the utricle. **Maculae** sit in the utricle and saccule. `[E19.01 · R05jk]` **✔✔** canals forming week 6–7 · ✔ the rest

### E19.02.01 Middle ear · AN40.2, AN43.4
- **The cavity is pharynx.** Pouch 1 (endoderm) grows outward: its far end, the **tubotympanic recess**, widens into the **tympanic cavity**; its near end stays narrow as the **auditory (Eustachian) tube** to the nasopharynx. `[E19.02, E19.05]` **✔** (links D-078, pouches — Ch 17)
- **Ossicles come from two arches.** **Malleus + incus** from arch 1 cartilage, **stapes** from arch 2. `[E19.02 · R05jm, R05jl]` **✔✔** the incus only — at the top of arch 1, independent of Meckel cartilage (R05jm) · ✚ in 3D the stapes is recognisable at CS18, malleus + incus at CS19; all three are cartilage after CS21 and joined after CS22 (R05jl); all three primordia are already seen in histology at CS16 (R05jm)
- **Nerves follow the arch (D4).** **Tensor tympani** (on the malleus) → **V3**; **stapedius** (on the stapes) → **VII**. `[E19.02]` **✔** (arch–nerve rule, links D-066)
- **The ossicles sit in mesenchyme until month 8**, when it melts away and the cavity lining spreads over them like a **mesentery** — their ligaments grow in these folds; the cavity at least doubles. `[E19.02]` **✔**
- **The stapes base has a double origin.** Its footplate is part **neural crest**, part **paraxial mesoderm**, and the crest part steers both footplate and **oval window**. `[E19.04 CC · R05js]` **✔** (*mouse* fate-mapping confirms the dual origin and that the mesoderm part fails without the crest part; the oval window still forms, but underdeveloped — mechanism only)
- **Air spaces spread late.** The cavity extends back as the **antrum** in late fetal life; after birth its lining invades the mastoid (**pneumatization**) — why middle-ear infection can reach the mastoid. `[E19.02]` **✔** (AN40.4 hook)

---

## 3. Tier B–D facts (cards later; marked now)
**Grouped by what each part is made from:** the capsule (mesenchyme round the placode) · the drum (all three layers) · the surface (arches 1 and 2) · the signals.

| Concept | Fact (our words) | Cite | Mark |
|---|---|---|---|
| **From the mesenchyme round the vesicle** | | | |
| E19.01.02 Membranous and bony labyrinth (B) · AN40.3 | Mesenchyme round the cochlear duct turns to **cartilage**; in **week 10** it hollows into two fluid spaces, **scala vestibuli** and **scala tympani**, split from the duct (scala media) by the **vestibular** and **basilar membranes**. The duct's outer wall hangs on the **spiral ligament**; its inner edge on the **modiolus**, the core the bony cochlea later winds round. Membranous labyrinth = endolymph inside; perilymph spaces outside. | `[E19.01]` | ✔ (no human stage read; §10) |
| **The drum — three layers, three sources** | | | |
| E19.03.01 Eardrum (B, inside the extear concept) · AN40.1 | **Outside:** ectoderm from the bottom of the ear canal; **middle:** connective tissue (fibrous layer); **inside:** endoderm of the tympanic cavity. Most of it is fixed to the **malleus handle**. | `[E19.03, E19.05 · R05jo, R05jn]` | ✔✔ outer layer from the canal's floor (R05jo) · ✚ plug's inner disc splits to leave it at ~15 wk (R05jn) |
| **The surface — arches 1 and 2** | | | |
| E19.03.01 External ear canal (B) · AN40.1, AN43.4 | **14e:** the canal grows in from **first-arch** surface tissue, **not** from cleft 1. From the **start of month 3** cells fill its floor (**meatal plug**); the plug later clears and its floor lines the eardrum; a plug that persists → congenital deafness (canal atresia). | `[E19.03 · R05jn, R05jo, R05jp]` | ✔ origin (note e) · ✔ start month 3 · ✔✔ plug present by 10 wk (R05jn) · **⚑ a** when it clears |
| E19.03.01 Auricle (B) · AN40.1, AN43.4 | From crest-derived tissue at the dorsal ends of **arches 1 and 2**, on either side of cleft 1: **arch 2** makes nearly all of it; **arch 1** only the **tragus** and the canal (arch 1 is **HOXA2-negative**, arch 2 **HOXA2-positive**). The ear starts **low in the neck** and reaches the side of the head as the jaw grows. Book: built from **six hillocks**. | `[E19.03 · R05jp, R05jq, R05it]` | ✔✔ arch 2 makes most, arch 1 the tragus + front of the canal (R05jp, by nerve supply: VII vs V) · **⚑ b** six hillocks · ✔ position (note f) |
| **The signals — how hearing works (Tier D, physiology)** | | | |
| E19.04 Hearing (D, no own concept row) | Sound shakes the drum (kept tight by **tensor tympani**; with **stapedius** it tightens further against loud noise) → the ossicles amplify it two ways — the **drum is much larger than the oval window** (book: ~55 vs ~3.2 mm²), and the **malleus works as a lever** → the stapes pushes a fluid wave through the cochlea, balanced by the **round window** → the **basilar membrane** moves where it resonates: **high pitch near the oval window** (short, stiff fibres), **low pitch toward the apex** (long, flexible fibres) → hair cells → cochlear nerve. | `[E19.04]` | ✔ (physiology; PY10.15) |

---

## 4. Clinical correlates — confirmed against Tier 1 (PubMed first)
**Grouped by what went wrong: the sensing part (inner ear, nerve) · the conducting part (canal, drum, ossicles) · the outside part (auricle) · the clues on the face.** Rates per 10,000 births. Clinical photos: diagrams only (D6).

**Rates, side by side.** The book quotes **no** rate in Ch 19, so no ✔✔ on a rate is possible: every Tier 1 figure is ✚ (More only, beyond Langman). A quoted background figure is a ≈ lead, never a ⚑.

| Lesion | Book | Tier 1 | Mark |
|---|---|---|---|
| Permanent sensorineural hearing loss found by newborn screening (laterality not given in the abstract) | not given | **23.6** per 10,000 screened live births (1,150 of 487,636, Queensland 2012–2019; R05jv) | ✚ |
| Genetic share of congenital hearing loss | 50 % | not retrieved from primary data (two reviews quote "more than half" — ≈ leads, §10) | ✔ |
| Congenital CMV → hearing loss | names CMV as a cause | cCMV in **0.58 %** (58 per 10,000) of newborns in high-income countries; **12.6 %** of them lose hearing (1 in 3 symptomatic, 1 in 10 without symptoms); cCMV causes **10–20 %** of childhood hearing loss — the **commonest non-genetic cause** (R05jw) · higher cCMV in low-income settings, 0.6–6.1 % (R05cb) | ✔✔ CMV causes sensorineural loss · ✚ the figures |
| Anotia / microtia | "common" | **2.86** per 10,000 live births (Texas registry, 1999–2005; 45 % isolated, 77 % one side, 94 % microtia; R05jx); registries range **0.83–17.4**, higher in Hispanic, Asian, Native American and Andean groups (R05jy) | ✚ |
| Preauricular tags and/or pits | not given | **0.93 %** (93 per 10,000) of 68,484 screened newborns; permanent hearing loss **8 vs 1.5 per 1,000** (80 vs 15 per 10,000), adjusted OR **4.9** (R05jz) · pits alone **2.4 %** (240 per 10,000) of 1,106 children up to 18, 0–6.6 % by ancestry, strongly familial (R05ka) | ✔✔ they flag other problems (hearing) · ✚ figures |
| Inner-ear malformation on CT in congenital hearing loss | not given | **85 %** of infants with **one-sided** loss vs **3.7 %** with **two-sided** loss (378 screen-referred infants; commonest: narrow cochlear-nerve canal; R05kb) | ✚ |
| Treacher Collins syndrome | no rate | not retrieved (a case series quotes 1 in 50,000 — ≈ lead) | ✔ |
| OAV spectrum (microtia + ≥ 1 major feature) | — (Ch 17) | 0.38 per 10,000 (R05is — Ch 17, D-078 d) | link, not re-checked |

**The sensing part didn't form or was damaged (sensorineural loss).**
- **Two kinds of loss:** damage to **hair cells or the VIII ganglion/nerve** → **sensorineural**; a fault in the **canal, drum or ossicles** → **conductive**. `[E19.04 CC]` ✔
- **About half genetic** — autosomal dominant, autosomal recessive or X-linked. `[E19.04 CC]` ✔ (no primary Tier 1 read; §10) · AN74.1 hook
- **Most non-genetic causes damage the sensing part:** infections in pregnancy (**rubella, cytomegalovirus, herpes simplex**), prematurity, maternal diabetes; **isotretinoin** (retinoids) can cause both kinds. `[E19.04 CC · R05jw]` ✔✔ CMV only (R05jw) · ✔ the rest · ✚ cCMV can start or worsen **after** birth, so a passed newborn screen does not rule it out (R05jw) · links **D-057** (rubella, CMV, retinoids, diabetes — Ch 9) — no new ⚑
- **Inner-ear malformations on imaging** are common when only **one** ear is affected and rare when both are (R05kb). `[E19.04 CC · R05kb]` ✚ (More / Tier D only, "beyond Langman")
- **Down syndrome:** either kind or both. `[E19.04 CC]` ✔ · AN75.1 hook

**The conducting part didn't open or move (conductive loss).**
- **Canal atresia:** a **meatal plug that never clears** leaves the canal closed → congenital deafness. `[E19.03 · R05jn]` ✔ (timing ⚑ a)
- **The stapes is the ossicle most often at fault**, and **stapes fixation** (ankylosis, usually both ears) the commonest problem — the book ties this to the footplate's mixed crest + mesoderm origin. `[E19.04 CC · R05jt, R05js]` ✔✔ fixation is the commonest stapes malformation (33 % of cases — 25 temporal bones from 18 patients, R05jt) · ✔ the origin argument (*mouse* mechanism, R05js)
- **Treacher Collins syndrome** — auricle, canal and ossicles can all be malformed → conductive loss of varying degree. `[E19.04 CC]` ✔ · links D-078 (first-arch syndromes, Ch 17)

**The outside part didn't shape (auricle and canal opening).**
- **Range:** from minor shape changes to a small, misshapen ear (**microtia**) or almost no ear (**anotia**). `[E19.04 CC · R05jx, R05jy]` ✔ · ✚ rates, sex and side (R05jx)
- **Preauricular pits** = shallow dimples in front of the ear, from a faulty first-arch infolding where the canal forms; **tags (appendages)** = extra skin bits from over-growth when ear-shaping genes misfire. `[E19.04 CC · R05jp]` ✔✔ pits as a first-arch anomaly (R05jp proposes exactly this) · ✔ tags

**The ear is a clue.**
- **Ear defects travel with others:** the auricle is crest-derived and crest also builds the **face, skull and heart**; ear findings are part of nearly every well-known chromosome syndrome — so an abnormal ear means **examine the baby fully** (Problem 3). `[E19.03, E19.04 CC · R05jz, R05is]` ✔✔ tags/pits flag hearing loss (R05jz) · ✔ the rest · links **D-078 d** (OAV spectrum, heart defects 27.8 %)
- **Low-set ears** flag syndromes because the ear starts low and should end level with the eyes. `[E19.03]` ✔ (map row; note f)

---

## 5. ⚑ Watch items → decision D-082 (owner picks)
- **(a) When the ear canal opens.** Book: the **meatal plug** forms at the start of **month 3** and dissolves in **month 7**. *Human* (R05jn): the plug spreads into a disc by 10 weeks, its inner part splits at 15 weeks, the canal is **open end to end by 16.5 weeks** and fully shaped by 18 weeks (clock not stated); R05jo (167 ears): canal skin **cornifies at 18 weeks** of gestation, then the debris clears outward. On either clock that is **month 4–5**, not month 7. Options: (1) default; (2) card: "the plug clears and the canal opens by about month 4–5; a plug that never clears leaves the canal closed", book month in More. *Recommended (2)* — two human series agree and the fact is visual (a scene will show it).
- **(b) The six hillocks.** Book: the auricle grows from **six hillocks** along arches 1 and 2. *Human* (R05jp, 22 Carnegie embryos CS13–23, 3D reconstructions): **hillocks were absent in most stages**; nerve supply (VII for almost all the auricle, V only the tragus and front of the canal) shows the auricle is **almost all arch 2**; R05jq (*human* fetuses 15–40 weeks): the auricular cartilage stays **one wavy plate** to late fetal life — the six-part funnel model "may have been biased by adult form". Both agree with the book that **arch 2 makes most of the ear** (✔✔). Options: (1) default — six hillocks on the card; (2) card: "the auricle grows from swellings round the first cleft — mostly from arch 2; the tragus from arch 1", the six hillocks named in More as "the classic model (His, 1885); recent human 3D studies rarely see six separate hillocks"; (3) drop the hillocks. *Recommended (2)* — exams still ask "six hillocks", so the name stays reachable.
- **(c) When the organ of Corti forms.** Book: the cochlear duct's cells form the **organ of Corti in week 7**. *Human* (R05jr, Leiden fetal cochleae): a **prosensory** strip at **10 weeks**, the **first hair cells from 12 weeks**, adult-like hair cells and ganglion at **20 weeks** — when hearing is thought to start (full text, X3a 22 Nov 2026: ultrasound gestational age in weeks + days; the paper itself equates 12 weeks of gestation with **week 10 of fetal development** — still later than week 7; 27 cochleae 10–20 wk; one at 11 wk 4 d showed early hair-cell marker changes in 1 of 3 sections, so onset may be late in week 11). The book's own figure shows the organ at 10 weeks, ~5 months and term. Options: (1) default; (2) card: "the cochlear duct is coiled by week 8; its sensory strip is present by about week 8–9 and hair cells from about week 10 (weeks after fertilization); the ear works by about mid-pregnancy", book week in More. *X3a fix:* the earlier wording put R05jr's gestation weeks beside the book's fertilization weeks — one clock per card (D-030). *Recommended (2)*.
- **(d) Note, not ⚑ — the ossicles' timing.** Book: the ossicles "appear during the first half of fetal life" and stay embedded until month 8. R05jl (*human*): all three are **cartilage models after CS21** (week 8, still embryonic) and **joined after CS22**. Order: R05jl's 3D reconstructions show the stapes recognisable at CS18 and malleus + incus at CS19, while R05jm's histology sees all three primordia at CS16 — so cards give no "first ossicle". The book's phrase reads best as bony ossicles, so no clash is shown; Tier D may add "the cartilage ossicles are already there and linked at the end of week 8" (beyond Langman).
- **(e) Note, not ⚑ — where the ear canal comes from (Ch 17's to-do).** 14e: first-arch tissue, **not** cleft 1 (older editions: cleft 1). *Human*: no study of the canal's origin by cell lineage was found; R05jp's nerve map (V supplies the **front** of the canal) fits a first-arch share but does not prove the whole canal is arch 1. *Chick/mouse* (R05ju): in chick the canal starts in **arch 2** surface, not at cleft 1; in mouse it depends on the **first-arch** tympanic ring — so the species differ. Cards follow 14e (the K1 rows `clefts` + `extear` already say "not from cleft 1", D-078 k); X1 to-do stays open for a human lineage source.
- **(f) Note, not ⚑ — how the ear "rises".** Book: jaw growth moves the ears from the neck to the side of the head at eye level. R05it (*human* Kyoto MRI, Ch 17): the ear moves **mainly sideways**, only appearing to rise relative to eyes and mouth. Not a contradiction of where it ends; the scene (§8) shows lateral drift + face growth, not a climb. Links D-078.
- **(g) Note, not ⚑ — cochlear turns.** Book: 2.5 turns by the end of week 8 (CS23). R05jk (*human*): coiling starts at CS18 and the duct has **more than two turns** just after the embryonic period (~weeks 9–10); its abstract gives no count at CS23, so no clash is shown. Cards say "about two and a half turns by the end of the embryonic period".
- **(h) Links, not new ⚑:** **D-078** (pouch 1, arches 1–2, ear canal note k, external-ear movement R05it, OAV spectrum, Treacher Collins as a first-arch syndrome) — Ch 19 agrees. **D-057** (rubella, CMV, retinoids, diabetes as teratogens) — Ch 19 repeats them for hearing; R05jw adds figures, no conflict. **D-079** (crest and placode ganglia; VIII nuclei, Ch 18) — the otic ganglion's mixed placode + crest origin agrees with R05iu/R05iv. **D-066** (arch muscles keep their arch nerve) — tensor tympani V3, stapedius VII. **D-030** (clocks) — applied throughout.
- **(i) Note — book internal:** the stapes footplate is given as "crest + paraxial mesoderm" only in the *Clinical Correlates* box; the main text says only "from the second arch". Cards: "the stapes is mostly second-arch crest; its footplate also has a mesoderm part" (Tier C).
- **(j) Note — book internal:** the area figures (drum ~55 mm², oval window ~3.2 mm²) are the book's; a cadaver study gives a larger adult drum (~59 mm², not added — §10). Cards say "the drum is much larger than the oval window" and give no area figures.
- **(k) Curriculum note:** NMC 2018 Vol I has **no ear development code** — **AN43.4** lists face, palate, tongue, branchial apparatus, pituitary, thyroid and eye (the ear is in none, except as part of the branchial apparatus). Adult codes: **AN40.1** external ear (core), **AN40.2** middle ear + auditory tube (core), **AN40.3** internal ear (non-core), **AN40.4** otitis externa and media (non-core — the mastoid line), **AN40.5** myringotomy (non-core); **AN43.3** histology of the cochlea and organ of Corti (non-core). Hearing physiology and deafness are **PY10.15–10.16** (physiology). AN74.1 (modes of inheritance) fits genetic hearing loss; AN75.1 (chromosomes) Down syndrome.

---

## 6. Top student misconceptions (refute in cards and Checks — craft §3.4)
1. **"The ear canal is the first pharyngeal cleft."** (map row) In 14e it grows in from **first-arch** surface tissue; cleft 1 is overgrown `[E19.03]` ✔ (note e).
2. **"The ossicles all come from one arch."** (map row) **Malleus + incus = arch 1; stapes = arch 2** `[E19.02 · R05jm]` ✔✔ incus arch 1 (R05jm) · ✔ malleus, stapes.
3. **"The inner ear grows out of the brain."** It is a **surface-ectoderm placode** that sinks in; only the nerve connects it to the hindbrain `[E19.01 · R05iu]` ✔✔.
4. **"The cochlea and the balance organs form separately."** Both come from the **same vesicle** — ventral half hears, dorsal half balances `[E19.01]` ✔.
5. **"The middle ear is a space in the skull bone."** It is the **pharynx's first pouch**, lined by endoderm and joined to the throat by the tube `[E19.02]` ✔.
6. **"The eardrum is just skin."** It has **three layers from three sources** — ectoderm, mesenchyme, endoderm `[E19.03 · R05jo]` ✔✔ (outer layer).
7. **"The auricle comes equally from arches 1 and 2."** **Arch 2 makes nearly all of it**; arch 1 only the tragus (and the canal) `[E19.03 · R05jp]` ✔✔.
8. **"Ears form where they sit."** They start **low, in the neck region**, and end level with the eyes as the face and jaw grow — so low-set ears are a clue `[E19.03 · R05it]` ✔ (note f).
9. **"The ossicles move freely from the start."** They lie **in mesenchyme until month 8** `[E19.02]` ✔.
10. **"Tensor tympani and stapedius share a nerve."** Each keeps its **arch's** nerve: V3 vs VII `[E19.02]` ✔.
11. **"The fetal ear canal is open all along."** It is **plugged** with cells for weeks before it opens `[E19.03 · R05jn]` ✔✔ (timing ⚑ a).
12. **"High notes are heard at the tip of the cochlea."** **High pitch near the oval window** (short stiff fibres), low pitch toward the apex `[E19.04]` ✔.
13. **"Congenital deafness is almost always genetic."** About **half**; infections — above all **CMV** — and other causes make up much of the rest `[E19.04 CC · R05jw]` ✔ · ✔✔ CMV is a cause · ✚ the commonest non-genetic one.
14. **"A passed newborn hearing screen rules out congenital CMV hearing loss."** cCMV loss can **start or worsen later** `[E19.04 CC · R05jw]` ✚ (More only, beyond Langman).
15. **"A small ear only matters for looks."** It often comes with **hearing loss** and **other defects** (face, skull, heart) — examine the whole baby `[E19.04 CC · R05jy, R05jz]` ✔✔ microtia with hearing loss (R05jy) · tags and pits flag hearing loss (R05jz).
16. **"Preauricular pits are leftovers of cleft 1."** The book (and R05jp) put them in **first-arch** infolding where the canal forms `[E19.04 CC · R05jp]` ✔✔.
17. **"The stapes footplate is pure second-arch cartilage."** It also has a **mesoderm** part, steered by crest `[E19.04 CC · R05js]` ✔ (*mouse* mechanism).

---

## 7. Curriculum map (R30 — NMC AN table; source note below)
**Source note:** read from **NMC *Competency Based UG Curriculum Vol I*** (`UG-Curriculum-Vol-I.pdf`, staged from Studio home `references\nmc\`, 22 Nov 2026). Vol I is the **2018** text; the 2024 MGMUHS reprint is not in `references\`, so **2024 wording is unchecked** (§10).

**Where Ch 19 sits (the prompt's guesses, checked):**
- **AN40.1** external ear — parts, blood and nerve supply (core, SH) ✔ · **AN40.2** middle ear + auditory tube — boundaries, contents, relations, functional anatomy (core, SH) ✔ · **AN40.3** internal ear features (**non-core**) · **AN40.4** otitis externa/media (non-core) · **AN40.5** myringotomy (non-core).
- **AN43.4** — development of face, palate, tongue, branchial apparatus, pituitary, thyroid, eye — **the ear is not named** (note k); used here only for the arch-derived parts (ossicles, auricle, canal).
- **AN43.3** — histology incl. cochlea / organ of Corti (non-core).
- **AN79** — general embryology (streak, notochord, neurulation, somites) — **no ear item**; placodes are not named.
- **AN74–AN75** genetics — AN74.1 modes of inheritance (genetic hearing loss) · AN75.1 chromosomal (Down syndrome) — hooks only.
- **Outside AN:** PY10.15 functional anatomy of the ear and physiology of hearing · PY10.16 deafness and hearing tests (both core physiology).

**Per concept (→ `tools/map/research.txt`):**
- E19.01.01 → AN40.3, AN43.3 · E19.01.02 → AN40.3 · E19.02.01 → AN40.2, AN43.4 · E19.03.01 → AN40.1, AN43.4 · E19.04.01 → AN74.1, AN75.1

---

## 8. Scene note — visual references (look, don't copy — RULES G5)
- **Placode → vesicle (CS10 → CS13):** a dorsal-oblique view of the hindbrain; a patch of surface ectoderm beside rhombomere 4–6 thickens, dimples, sinks and closes off (R05iu, R05iv); crest-coloured cells spill from its wall toward a ganglion. B2 "≈ day 22–30 · CS10–12". End on the **transverse section** with the vesicle beside the hindbrain (D9).
- **The vesicle splits and grows (CS13 → fetal):** dorsal half → three canal pouches whose centres press together and vanish (show the "hole-punch" moment); ventral half → a duct that coils to ~2.5 turns (R05jk Kyoto CT — look only, licence per dataset). Colour the two halves by job (balance vs hearing), with a pattern + label.
- **Cochlear cross-section (week 10 → term):** cartilage ring hollows into two scalae; duct in the middle; then the floor's hair cells appear (⚑ c — label with "~week 12 (newer evidence)" while open).
- **Middle ear assembly:** pouch 1 reaching out as the tubotympanic recess; three cartilage beads at the arch tops — recognisable in 3D at CS18–19 (R05jl; primordia already at CS16, R05jm), joining after CS22 — colour by **arch** (1 vs 2), never by germ-layer token alone (B3).
- **Ear canal and drum:** a funnel of first-arch surface pushing in, filling with a plug, then clearing (⚑ a — label the time per the owner's pick); the drum's three layers drawn as a sandwich (ectoderm · mesenchyme · endoderm) with tokens + patterns.
- **Auricle (week 6 → 8):** swellings round the end of cleft 1, arch 2 side growing over (R05jp); the ear drifting sideways as the face widens (R05it) — **never** a ring of six numbered hillocks as the main visual while ⚑ b is open (a "classic model" inset is fine).
- **Hearing (Tier D):** a straightened cochlea with a travelling wave; high pitch peaks near the oval window, low pitch near the apex.
- **Never from the book:** its placode, vesicle, cochlear-duct, scala, organ of Corti, canal, tympanic-cavity, ossicle, meatus, eardrum, hillock and auricle figures and its embryo photograph are copyrighted; every one is redrawn by us (D6, visual-style §16). Its patient photographs (anotia, microtia, tags, pit) are never shown — diagrams only.

## 9. Why learners struggle here (M05)
- **Three origins, one organ** — teach the ear as **placode (inner) · pouch (middle) · arches + surface (outer)** before any part name; one colour per source.
- **Arch bookkeeping** — malleus/incus vs stapes, V3 vs VII, tragus vs the rest: one rule ("arch 1 front and jaw, arch 2 back and face") carries them all (links Ch 17).
- **Endo- vs peri-lymph and the scalae** — draw the duct inside the bony tube before naming spaces.
- **Hillocks** — the classic six-hillock diagram is widely taught but weakly supported in human 3D data (⚑ b); teach "arch 2 makes most" first.
- **Clocks:** all embryonic events are after fertilization; fetal papers often give no clock (⚑ a, ⚑ c checked both ways).

## 10. X1 to-do — done 22 Nov 2026, with open items · X3a full texts 22 Nov 2026
- Done: real locators + sub-locators; two page spills, the two-column overlaps and the box title named (→ I1); staging from human specimens (R06/R08, R05iu, R05iv by Carnegie stage; R05jk, R05jl, R05jp Kyoto/Carnegie by CS; R05jm weeks of development; fetal clocks checked both ways); Tier A for 2 concepts (inner ear, middle ear); Tier B–D grouped by source tissue; clinical rows in 4 groups with rates per 10,000 (all ✚ — the book has none); 17 misconceptions; AN map from NMC Vol I (no ear development code); 18 new sources **R05jk–R05kb**. G-Sci fresh-eyes review: **pass with fixes, 7 MUST + 9 SHOULD, all applied** — ossicle order reworded (two human series differ), one ✔✔ narrowed to the incus, two misplaced or missing citations fixed, R05jr's "weeks of gestation" clock named, two lines rewritten further from the book's wording.
- **Human ear-canal origin** (Ch 17's to-do, note e): no lineage study found — still open.
- **Otic placode in humans:** O'Rahilly 1963 (PMID 14081992, no abstract) — full text to `references\papers\` if wanted; it would raise the placode line to ✔✔.
- **Rates not retrieved:** congenital aural atresia (registry), Treacher Collins, stapes fixation, inner-ear malformation types (Mondini, enlarged vestibular aqueduct), congenital rubella hearing-loss share today.
- **Genetic share of congenital hearing loss** (book 50 %): find a primary cohort (genetic testing in screen-referred infants) before Tier D gives a figure.
- **Human scalae / cartilage-shell timing** (book week 10) and **semicircular canal fusion** stages — Kyoto inner-ear series beyond the R05jk abstract.
- **Full texts:** R05jn (clock for 16.5 weeks, ⚑ a) and R05jk (turn count at CS23, note g) — *X3a (22 Nov 2026): not in PMC; owner PDF not supplied.* ~~R05jr (clock for 12 weeks, ⚑ c)~~ — **done X3a:** clock named (ultrasound gestational age; 12 wk ≈ fetal week 10), ⚑ c holds, its option 2 wording moved to one clock (D-082 c note).
- **Otic placode (O'Rahilly 1963, PMID 14081992):** *X3a:* not in PMC; still needs the owner PDF.
- **Eardrum size:** a cadaver study (Beger 2021, PMID 33048245) gives adult ~59 mm² and adult size from month 7 of pregnancy — add only if a card uses area figures (note j).
- **R01 3D Atlas / R04 Kyoto** ear models before the vesicle and labyrinth scenes (look only; R01 NC-ND, R04 licence per dataset).
- **2024 wording** of AN40.1–40.3 (MGMUHS reprint): not in `references\`.
