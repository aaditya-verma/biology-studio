# Research dossier — Ch 17 · Head and neck (for C-step cards + episodes)

*(Purpose: cited, marked facts, staging, misconceptions and clinical correlates for Ch 17, the eighth chapter of Part 2 — 15 sections (many under a page) and 5 boxes; read in two halves (arches and pouches: arches, pouches, clefts, molecular regulation of the face, tongue, thyroid · face and teeth: face, intermaxillary segment, palate, nasal cavities, teeth). Cards draft from this file. Updated: 22 Nov 2026 · Bio · Research · X1 Ch 17 · by Aaditya. Own words only; no book sentences, figures or tables (RULES §G) — every list below is regrouped in our own order; the arch derivatives are grouped by tissue (skeleton · muscle · nerve · artery), never as the book's table.)*

**How to read a line:** fact in our words · `[book section · registry source]` · mark (RULES B6–B7): **✔✔** book + Tier 1 agree · **✔** book only · **⚑** book vs Tier 1 disagree (D-entry) · **✚** beyond the book (Tier 1 only; More / Tier D only, "beyond Langman") · **≈** blocks final. **Species tag:** a line from mouse or chick says so (*mouse*). Those lines can confirm a mechanism; they never give a human day or number. **Rates** are per 10,000 births unless stated; "total" = live births + stillbirths + terminations.

**Citation check, read before you cite:** checked 22 Nov 2026. `tools/card-check/citations.py` matches `R\d\d[a-z]{0,2}`, so the new ids **R05ib–R05it** parse. Every PMID was grepped in the registry before its id was given (none was there); author lists copied from the PubMed record (first three, then et al.). R05ed and R05bs stay retired. `sources.json` is rebuilt in this commit (`check.py --write-sources`, D-065 (6)). Registry sources re-used: **R05fa** (22q11 review), **R05ez** (22q11 in conotruncal defects), **R05ew** (human arch arteries), **R05bu** (valproate), **R05bv** (ondansetron and clefts), R06/R08 (stage tables). **Read and not used:** Mossey & Modell 2012 (no figures in the abstract), Burdi & Silvey 1969 (palate closure by sex — no abstract, so the book's "females close about a week later" stays ✔ book only), Fagman & Nilsson 2010 (thyroid review, chick/mouse/zebrafish only), Stoll 2023 (Robin sequence, a single French registry — the meta-analysis R05ip covers it).

**Ages — three clocks.** (1) The book's events are in **days or weeks after fertilization** (arches weeks 4–5, nasal pits week 5, upper lip weeks 6–7, shelves rise in week 7, thyroid in place week 7) and in **months** for fetal events (tonsil lymphoid tissue months 3–5, thyroid works from the end of month 3, bell stage month 3) — read as after fertilization (D-030). Its holoprosencephaly window (days 19–21) is after fertilization too. (2) Specimen papers give **Carnegie stages** (R05ib, R05ic, R05ii, R05ij, R05ik, R05if) or **weeks post conception** (R05id, R05ie) — both after fertilization; matched to the classic R08 day ranges (`tools/indexer/carnegie.json`). (3) **R05ih gives "gestational weeks" with no clock stated** — it may be last-period (obstetric, ~2 weeks ahead) — so it is not used to move a book date (note g). Kyoto papers (R04 collection: R05ib, R05it) stage by CS and are compared by stage, not by day (D-030 a).

**Section locators (checked against the PDF, 22 Nov 2026; printed page = PDF page − 19):**
- **E17.00** pp 284–285 — opener (where head mesenchyme comes from) p 284; the arch-derivatives table and the start of the arches text p 285.
- **E17.01 Pharyngeal arches pp 286–290** — what an arch is p 286; first arch pp 286–287; second arch pp 287–289; third arch pp 289–290; fourth and sixth arches **p 290**.
- **E17.02 Pharyngeal pouches pp 290–291** — first and second pouch p 290; third and fourth pouch + the pouch table **p 291**.
- **E17.03 Pharyngeal clefts pp 291–292** — the ear-canal correction pp 291–292, the cervical sinus **p 292**.
- **E17.04 Molecular regulation of facial development pp 292–297** — crest streams and rhombomeres pp 292–293; pouch endoderm signals pp 293–294; *Clinical Correlates* box **pp 294–297** (ectopic thymus/parathyroid and branchial fistulas pp 294–295; crest-related craniofacial defects — Treacher Collins, Robin sequence, 22q11.2 deletion, hemifacial microsomia — pp 295–297).
- **E17.05 Tongue pp 297–298** — swellings p 297; nerve supply p 298; *tongue-tie* box p 298.
- **E17.06 Thyroid gland pp 298–300** — origin and descent pp 298–299; *thyroglossal cyst / fistula and ectopic thyroid* box **pp 299–300**.
- **E17.07 Face pp 300–303** — prominences, nasal pits, upper lip, nasolacrimal duct p 300; nose p 301; the face-sources table p 303.
- **E17.08 Intermaxillary segment p 301** ✔.
- **E17.09 Secondary palate pp 301–302** + the *facial clefts* box **pp 305–308** (cleft lip and palate, van der Woude, oblique and median clefts, holoprosencephaly, causes and rates).
- **E17.10 Nasal cavities p 302** ✔.
- **E17.11 Teeth pp 302, 308–310** (pp 303–307 hold figures and the clefts box).
- **E17.12 Molecular regulation of tooth development pp 310–311** + *tooth anomalies* box **p 311**.
- **E17.13 Summary pp 311–312** · **E17.14 Problems p 312**.

**I1 gaps** (tree.json) → I1 to-do:
- **Seven short sections spill one page**, as the prompt expected: E17.01 ends **p 290** (I1 289), E17.02 **p 291** (I1 290), E17.03 **p 292** (I1 291), E17.05 **p 298** (I1 297), E17.06 **p 300** (I1 299), E17.07 **p 301** + table p 303 (I1 300), E17.09 **p 302** (I1 301); and E17.11 ends **p 310** (I1 309), E17.12 **p 311** (I1 310), E17.13 **p 312** (I1 311).
- **Two boxes filed under the wrong section:** the *tongue-tie* box (PDF 317, p 298) is the **tongue's** (E17.05), not the thyroid's; the *facial clefts* box (PDF 324, pp 305–308) belongs to the **face/palate** (cite `E17.09 CC`), not to Teeth.
- **The E17.04 box (PDF 313) holds three topics**, two of them about E17.02–E17.03 (ectopic thymus/parathyroid, branchial fistulas). Cite those lines `E17.04 CC` as filed, and name it *Pouch, cleft and crest defects*.
- **Three untitled boxes in I1:** PDF 313 → *Pouch, cleft and crest defects*; PDF 318 → *Thyroglossal cyst and ectopic thyroid*; PDF 324 → *Facial clefts*; PDF 330 → *Tooth anomalies* (four, counting the last).

---

## 1. Staging & scale — first arch to the erupted tooth (RULES B2)
Human anchors: **R06/R08** (stage definitions and classic ages), **R05ii** (185 *human* embryos, neural crest), **R05ij** (145 *human* embryos CS9–23, somites, rhombomeres, arches), **R05ik** (10 *human* CS23 skulls), **R05ic** (43 *human* embryos/fetuses, lip and palate, weeks 4–12), **R05ib** (22 *human* samples, Kyoto CT/MRI, palate CS21 → fetal), **R05id/R05ie** (Carnegie collection, 7–10 wk post conception), **R05if** (*human* SEM CS16 → fetal, nasal septum), **R05ig** (*human* thymus), **R05it** (171 Kyoto MRIs CS17–23, external ear). Days are the book's unless a source is named.

| When | Carnegie / clock | What happens `[section · source]` | Mark |
|---|---|---|---|
| Week 3 → 4 | CS9–11 | **Cranial crest** leaves the neural folds before the front neuropore closes; trigeminal, facial and post-otic crest seen by CS10; crest-free gaps in Rh 1, 3, 5 by CS11 `[E17.04 · R05ii]` | ✔✔ timing and gaps at Rh 3, 5 · note f (Rh 1) |
| Week 4 | CS10 → CS13 | **Arches appear head first**: arch 1 (CS10), 2 (CS11), 3 (CS12), 4 (CS13); the 6th stays small; aortic arches segment from CS9 `[E17.01 · R06, R05ij]` | ✔✔ |
| ~Day 24 → 30 | CS11–13 | **Stomodeum** ringed by the first prominences; the oropharyngeal membrane breaks (~day 30 in the book) `[E17.01]` | ✔ |
| End of week 4 | CS11 → CS15 | **Lower lip and jaw**: the two mandibular prominences appear (CS11) and are fully merged by CS15 `[E17.07 · R05ic]` | ✔✔ (book gives no week for the merge — ✚ CS15) |
| Week 5 | CS13–14 | **Pouches 1–4** in the pharyngeal wall; occipital myotomes 1–4 send the **hypoglossal cord** forward (CS13–14) → tongue muscles `[E17.02, E17.05 · R05ii]` | ✔ pouches · ✔✔ tongue muscle source |
| ~Week 4 (book; ~6 mm in a week-5 figure) | CS12–13 → CS16 | **Tongue swellings** (two lateral + tuberculum impar), then copula and epiglottal swelling; tongue prominent by CS16 `[E17.05 · R05ic]` | ✔ (✚ CS16) |
| Week 5 | ~CS14–15 | **Nasal placodes → pits**, ringed by medial and lateral nasal prominences `[E17.07]` | ✔ |
| Weeks 5–6 | CS15–17 | **Primary palate** from the merged medial nasal prominences `[E17.08 · R05ie]` | ✔✔ (R05ie: weeks 5–6 post conception) |
| Weeks 6–7 | CS16 → CS20 | **Upper lip**: medial nasal + maxillary prominences appear by CS16 and are fully merged by **CS20** (~day 51–53) `[E17.07 · R05ic]` | ✔✔ (merged by CS20 = days 51–53, ~1 week after the book's 7-week figure — within stage ranges, not logged) |
| Week 6 | CS16–17 | **Palatal shelves** bud from the maxillary prominences (median palatine process CS16, lateral CS17), hanging beside the tongue `[E17.09 · R05ic]` | ✔✔ |
| Week 6–7 | CS16–19 | **Oronasal membrane** breaks → primitive choanae `[E17.10]` | ✔ · the septum is present from the start (R05if) **⚑** b |
| Week 7 | ~CS18–19 | **Thyroid** reaches the front of the trachea; isthmus + two lobes `[E17.06]` | ✔ (no human stage retrieved) |
| Week 7 (book) / **CS23, end of week 8 (days 56–60)** (specimens) | CS21 → CS23 | **Shelves rise** above the tongue: not yet up at CS21–22, up and touching or fused in most CS23 embryos; head lifts, Meckel cartilage and tongue move forward `[E17.09 · R05ib, R05ic, R05id]` | **⚑ timing** (D-078 a) · ✔✔ the tongue must move first |
| Week 8 | CS23 | **Arch skeleton in cartilage**: hyoid with both horns, ring-shaped cricoid, arytenoids condensing; bone plate over most of Meckel cartilage `[E17.01 · R05ik]` | ✔✔ |
| Weeks 9 → 12 | fetal | **Palate fusion**: looks closed from outside at week 9, fully fused only by week 12; septum joins the palate `[E17.09 · R05ic]` | ✚ (book shows a fused palate at 10 weeks) |
| Week 6 → month 3 | fetal | **Teeth**: dental lamina by week 6, **bud** ~8 wk, **cap** ~10 wk, **bell** ~month 3; permanent buds form in month 3 `[E17.11]` | ✔ (no human source retrieved, §10) |
| Months 3–5 | fetal | **Palatine tonsil** fills with lymphoid tissue `[E17.02]` | ✔ |
| End of month 3 | fetal | **Thyroid starts working** (colloid follicles) `[E17.06 · R05ih]` | ✔ book · R05ih: follicles + T4 from 11 "gestational weeks", clock unclear (note g) |
| 6–24 months after birth | postnatal | Milk teeth erupt; permanent buds wake ~year 6 `[E17.11]` | ✔ |

**Scale on screen (B2):** book days and weeks (after fertilization); CS from R08. Lengths: tongue swellings ~6 mm (book figure, week 5); palate CS23 ≈ 27–32 mm CR (R05ik); 7 → 10 wk = 18 → 49 mm CR (R05ie).

---

## 2. Tier A facts — cited and marked
### E17.00.01 What builds the head and neck · AN43.4
- **Four sources of head mesenchyme:** paraxial mesoderm (somites + somitomeres), lateral plate mesoderm, **neural crest**, and thickened ectoderm patches (**placodes**). `[E17.00]` **✔**
- **Who makes what, by tissue:** *crest* — the whole face skeleton (viscerocranium), part of the skull, and the face's dermis, tendons, dentin, pia/arachnoid and gland stroma; *paraxial mesoderm* — most of the skull base and vault, **every voluntary head muscle**, back-of-head dermis, meninges behind the forebrain; *lateral plate* — laryngeal cartilages (arytenoid, cricoid) and local connective tissue; *crest + placodes* — the sensory ganglia of V, VII, IX, X. `[E17.00]` **✔** · ✔✔ placodes help build the arch ganglia (R05ii, *human*) · links D-066 (head muscles, somitomeres) and D-064 (skull)
- **Crest leaves early.** In human embryos cranial crest emigrates from the folds before the front neuropore closes, from CS9–10. `[E17.04 · R05ii]` **✔✔**

### E17.01.01 Pharyngeal arches · AN43.4, AN25.6
- **What an arch is:** a bar of mesenchyme (paraxial/lateral-plate mesoderm + crest) covered by ectoderm outside and endoderm inside; between arches, **clefts** outside and **pouches** inside. `[E17.01]` **✔**
- **Four parts per arch:** its own **cartilage** (skeleton), **muscle**, **cranial nerve** and **artery**. A muscle keeps its arch's nerve wherever it migrates — that is how its origin is traced. `[E17.01, E17.13]` **✔**
- **When:** weeks 4–5, head end first — arch 1 at CS10, 2 at CS11, 3 at CS12, 4 at CS13. `[E17.01 · R06, R05ij]` **✔✔**
- **Not gills.** "Branchial" is the old name; human arches look gill-like but never make gills, and the clefts never open into the pouches. `[E17.01]` **✔**
- **Arteries:** each arch carries an aortic arch artery from the aortic sac (Ch 13). `[E17.01, E13 · R05ew]` ✔ · links D-068 a (pulmonary arteries)

### E17.01.02 Arch derivatives · AN43.4, AN28.1, AN33.2, AN38.1, AN40.2, AN26.6
Grouped **by tissue**, not by arch (the table in §3 has the full map).
- **Nerve is the key:** 1 → **V** (muscles: V3; skin of the face: V1–V3) · 2 → **VII** · 3 → **IX** · 4 → **X, superior laryngeal** · 6 → **X, recurrent laryngeal**. `[E17.01]` **✔**
- **Skeleton:** arch 1 cartilage (**Meckel**) leaves the **malleus + incus** and a ligament; the **mandible and maxilla form in membrane** around it, not from it; arch 2 (**Reichert**) → hyoid (lesser horn + upper body), the stylohyoid ligament and styloid above it, and the **stapes** in the ear; arch 3 → greater horn + lower hyoid body; arches 4 + 6 → laryngeal cartilages. `[E17.01]` **✔** · ✔✔ hyoid horns, cricoid ring and bone over Meckel cartilage at CS23 (R05ik) · note h (book gives two origins for the laryngeal cartilages)
- **Muscle:** arch 1 → chewing + four small ones (two tensors — veli palatini, tympani — and two floor-of-mouth muscles — mylohyoid, anterior digastric); arch 2 → **facial expression** + stapedius, stylohyoid, posterior digastric; arch 3 → **stylopharyngeus only**; arch 4 → pharyngeal constrictors, levator veli palatini, cricothyroid (throat → palate → larynx); arch 6 → intrinsic larynx muscles. `[E17.01]` **✔** · links D-066 (arch muscle lists)

### E17.02.01 Pharyngeal pouches · AN43.4, AN35.2, AN36.1, AN40.2
- **Four pouches, one rudiment**; their **endoderm** lining makes glands and the middle ear. `[E17.02]` **✔**
- **By destination:** *ear* — pouch 1 → tubotympanic recess → **middle-ear cavity + auditory tube**; *throat* — pouch 2 → **palatine tonsil** (lymphoid tissue months 3–5) + tonsillar fossa; *immune* — pouch 3 ventral → **thymus**; *calcium* — pouch 3 dorsal → **inferior parathyroid**, pouch 4 dorsal → **superior parathyroid**, pouch 4 ventral → **ultimobranchial body → C cells** (calcitonin). `[E17.02]` **✔** · ✔✔ thymic epithelium from pouch 3 alone (R05ig, *human*)
- **The swap:** the thymus drags the pouch-3 parathyroid **down past** the pouch-4 one, so pouch 3 ends up **inferior**. `[E17.02]` **✔**
- **Glands need crest.** Pouch endoderm makes the gland cells; crest mesenchyme makes the stroma and is needed for them to differentiate — why 22q11 hits thymus and parathyroids. `[E17.04 CC]` **✔**

### E17.05.01 Tongue · AN39.1, AN43.4
- **Front from arch 1, back from 3 (+ 4):** two lateral swellings overgrow the tuberculum impar → **anterior two-thirds** (body); copula/hypobranchial eminence (arches 2–4), overgrown by arch 3 → **posterior third** (root); arch 4 → epiglottis and the very back. The **terminal sulcus** marks the join; the **foramen caecum** sits at its apex. `[E17.05]` **✔**
- **Four nerves, read as a map:** touch front **V3**, back **IX**, far back **X** (superior laryngeal); taste front **VII** (chorda tympani), back IX. Arch 2 is overgrown, so VII gives **taste only**. `[E17.05]` **✔**
- **Muscles from the back of the head:** most tongue muscles come from **occipital somites** → **XII**. `[E17.05 · R05ii, R05ij]` **✔✔** (*human*: occipital myotomes 1–4 form the hypoglossal cord at CS13–14; somites 1–4 lie caudal to arch 4)

### E17.06.01 Thyroid descent · AN43.4, AN35.2
- **Starts in the tongue, ends in the neck.** A midline endoderm thickening in the pharynx floor — between tuberculum impar and copula, at the future **foramen caecum** — buds down **in front of the gut**, staying tied to the tongue by the **thyroglossal duct**, which later disappears. `[E17.06]` **✔**
- **Path:** in front of the hyoid and the laryngeal cartilages, reaching the front of the trachea in **week 7** with an isthmus and two lobes. `[E17.06]` **✔**
- **Two cell types, two origins:** follicular cells (T3/T4) from the midline bud; **C cells** (calcitonin) from the ultimobranchial body (pouch 4). `[E17.06, E17.02]` **✔**
- **When it works:** end of month 3 (first colloid follicles). `[E17.06 · R05ih]` ✔ · R05ih (45 *human* thyroids, 7–33 wk): follicles and T4 from 11 "gestational weeks" — clock unclear (note g)

### E17.07.01 Face from five prominences · AN43.4, AN28.2
- **Five around the mouth:** one **frontonasal** (above), two **maxillary** (sides), two **mandibular** (below) — crest-filled, from the end of week 4. `[E17.07]` **✔**
- **Then the nose ring:** nasal placodes sink into pits (week 5), raising **medial and lateral nasal prominences**. `[E17.07]` **✔**
- **What becomes what, by face region:** *forehead + nose bridge* ← frontonasal; *crest and tip of nose, philtrum* ← medial nasal (merged); *alae* ← lateral nasal; *cheeks + outer upper lip* ← maxillary; *lower lip + jaw* ← mandibular (merged). `[E17.07, E17.08]` **✔**
- **The upper lip is four pieces:** two medial nasal + two maxillary prominences; the **lateral nasal prominences play no part**. Human specimens: parts appear by CS16, fully merged by **CS20**. `[E17.07 · R05ic]` **✔✔**
- **Lower jaw first:** the mandibular prominences merge by CS15, before the upper lip. `[E17.07 · R05ic]` ✚ (More only, beyond Langman)
- **Nasolacrimal duct** from an ectodermal cord in the groove between maxillary and lateral nasal prominences. `[E17.07]` **✔**

### E17.09.01 Secondary palate · AN43.4
- **Two palates.** *Primary* — the small front triangle from the intermaxillary segment (weeks 5–6, R05ie). *Secondary* — most of the palate, from two **palatal shelves** of the maxillary prominences. `[E17.08, E17.09 · R05ie]` **✔✔**
- **Down, then up, then zip.** Shelves grow down beside the tongue (week 6), **rise** to horizontal above it, meet and fuse; in front they join the primary palate at the **incisive foramen**; the septum joins above. `[E17.09]` **✔** · ✔✔ the sequence (R05ib, R05ic)
- **When they rise:** book — week 7. *Human* specimens — not yet raised at CS21–22, raised in most at **CS23 (end of week 8, days 56–60)** (R05ib, Kyoto, 22 samples; R05ic, 43 specimens; R05id, stage 23). `[E17.09 · R05ib, R05ic, R05id]` **⚑** (D-078 a)
- **The tongue must get out of the way.** As the head lifts and the mandible (Meckel cartilage) grows forward, the tongue drops and moves forward, freeing the shelves. `[E17.09, E17.04 CC · R05ib, R05id]` **✔✔** (Robin sequence is this step failing)
- **Fusion takes weeks:** looks closed at week 9, fully fused by week 12. `[E17.09 · R05ic]` ✚ (More only, beyond Langman)

---

## 3. Tier B–D facts (cards later; marked now)
**Arch derivatives by tissue — one row per tissue, each arch in the cells.** Then the remaining concepts grouped **by mechanism** (things that get buried · things that migrate · things that open · things that are signalled), not the book's order.

| Tissue | Arch 1 | Arch 2 | Arch 3 | Arch 4 | Arch 6 | Cite | Mark |
|---|---|---|---|---|---|---|---|
| **Nerve** | V (V3 motor; V1–V3 face skin) | VII | IX | X — superior laryngeal | X — recurrent laryngeal | `[E17.01]` | ✔ |
| **Skeleton** | malleus, incus, sphenomandibular ligament (Meckel); maxilla, zygoma, part of temporal, mandible in membrane | lesser horn + upper hyoid body, stylohyoid lig., styloid, stapes | greater horn + lower hyoid body | laryngeal cartilages (with 6) | laryngeal cartilages (with 4) | `[E17.01 · R05ik]` | ✔ · ✔✔ hyoid + cricoid at CS23 · note h |
| **Muscle** | chewing (masseter, temporalis, both pterygoids); tensor veli palatini, tensor tympani; mylohyoid, ant. digastric | facial expression, stapedius, stylohyoid, post. digastric | stylopharyngeus | constrictors, levator veli palatini, cricothyroid | intrinsic larynx | `[E17.01]` | ✔ (links D-066) |
| **Artery** | (mostly gone; part of maxillary a.) | (mostly gone) | common + start of internal carotid | aortic arch (L), subclavian (R) | pulmonary + ductus (L) | `[E13 · R05ew]` | ✔ · ⚑ pulmonary origin = **D-068 a** (link) |

| Concept | Fact (our words) | Cite | Mark |
|---|---|---|---|
| **Things that get buried** | | | |
| E17.03.01 Pharyngeal clefts (B) · AN43.4, AN40.1 | Four clefts at week 5, all temporary. **The ear canal does not come from cleft 1** (14e corrects older books): it grows in from first-arch surface ectoderm while the second arch builds most of the outer ear and closes cleft 1. Arch 2 then grows down over arches 3–4 to meet the epicardial ridge, burying clefts 2–4 in a **cervical sinus** that normally vanishes. | `[E17.03, E17.13]` | ✔ (no human source retrieved; misconception 4) |
| **Things that migrate** | | | |
| E17.02.01 (B depth) | Thymus moves down and medially to the front of the chest and meets its partner; its tail may stay in the thyroid or as nests; it grows until puberty and is later fatty. Inferior parathyroids vary most in final place (sometimes at the carotid fork). | `[E17.02, E17.04 CC]` | ✔ |
| E17.06.01 (B depth) | Thyroid descent and the C-cell merger (above). | `[E17.06]` | ✔ |
| **Things that open** | | | |
| E17.01.03 Stomodeum (B) · AN43.4 | The primitive mouth: an ectoderm pit ringed by the first prominences, sealed by the **oropharyngeal membrane** (ectoderm on endoderm) that breaks ~day 30. | `[E17.01]` | ✔ |
| E17.07.02 Nasal placodes and prominences (B) · AN43.4, AN37.1 | Placodes appear on the frontonasal prominence under forebrain induction (end week 4); sink into pits in week 5; medial and lateral rims become the nasal prominences. | `[E17.07]` | ✔ |
| E17.08.01 Intermaxillary segment (B) · AN43.4 | The two medial nasal prominences merge deep as well as at the surface → (inside out) the **primary palate**, the **upper-jaw piece carrying the four incisors**, and the **philtrum** of the lip; continuous above with the front of the septum. Weeks 5–6. | `[E17.08 · R05ie]` | ✔ · ✔✔ timing |
| E17.10.01 Nasal cavities and sinuses (B) · AN37.1, AN37.2 | Nasal pits deepen (week 6); the **oronasal membrane** breaks → primitive choanae just behind the primary palate; once the secondary palate forms, definitive choanae sit at the nasal–pharynx junction. **Septum:** book — grows down to meet the palate; *human* SEM — present from the start as the tissue between the primary choanae, met by the shelves when they rise. Paranasal sinuses bud from the lateral wall, reach full size at puberty. | `[E17.10 · R05if]` | ✔ · **⚑** septum (D-078 b) |
| **Things that are signalled** | | | |
| E17.04.01 Molecular regulation of the face (D) · AN43.4 | Crest edge set by **BMP** then **WNT1** (EMT). Hindbrain crest from **rhombomeres** in three streams — R1–2 (+ caudal midbrain) → arch 1; R4 → arch 2; R6–7 → arches 4–6; R3 and R5 give few cells. The streams guide the ganglion axons back to R2, R4, R6–7. **Pouch endoderm, not crest, patterns the arch skeleton** (pouches form even without crest; FGFs drive the lateral endoderm movement; each pouch: FGF8 front, BMP7 back, PAX1 dorsal (the text says PAX2 — note l), SHH in back of pouches 2–3); the mesenchyme's answer depends on the code crest carries: **arch 1 Hox-free (OTX2)**, arch 2 HOXA2, arches 3–6 paralogue-3 HOX. Frontonasal crest is patterned by ectoderm + forebrain signals (SHH, FGF8). | `[E17.04]` | ✔ (mechanism *mouse/chick*) · ✔✔ *human* crest gaps at Rh 3, 5 and cardiac crest from Rh 6–7 via arch 3 at CS12 (R05ii) · note f (Rh 1) |
| E17.11.01 Teeth (B) | **Epithelium + crest mesenchyme.** Dental lamina (C-shaped, week 6) → 10 buds per jaw → **bud → cap → bell** (≈ 8 wk, 10 wk, month 3). Cap: outer and inner dental epithelium + stellate reticulum over the **dental papilla** (crest). **Inner epithelium → ameloblasts → enamel** (from the tip down); **papilla → odontoblasts → dentin** (for life) and pulp; root sheath shapes the root; **cementoblasts → cementum**; **periodontal ligament** outside. Milk teeth erupt 6–24 months; permanent buds (month 3) wait until ~year 6. | `[E17.11]` | ✔ (no human source retrieved, §10) |
| E17.12.01 Tooth regulation and defects (D) | Epithelium leads until the bud stage, then the mesenchyme leads; incisor-to-molar identity from a mesenchymal HOX code; WNTs, BMPs, FGFs, SHH, MSX1/2. **Enamel knot** = the tooth's signalling centre (FGF4, SHH, BMP2/4), gone by end of cap stage (BMP4 may time its death; FGF4 like the AER). Defects: natal teeth (mostly lower incisors), wrong number/shape/size, tetracycline staining, enamel defects with rickets. | `[E17.12, E17.12 CC]` | ✔ (*mouse* mechanism) |

---

## 4. Clinical correlates — confirmed against Tier 1 (PubMed first)
**Grouped by what went wrong: crest cells failed · a buried cleft stayed open · a migrating gland stopped short · prominences or shelves didn't merge · the midline was missing · a membrane didn't let go.** Rates per 10,000 births. Clinical photos: diagrams only (D6).

**Rates, side by side.** ✔✔ = Tier 1 within ~1.5× of the book; ⚑ = a larger gap from a population source.

| Lesion | Book | Tier 1 | Mark |
|---|---|---|---|
| Cleft lip ± palate | ~1 in 700 (≈ 14) | **9.92** (IPDTOC, 54 registries, 7.5 M births, total, R05il); 9.1 (EUROCAT, 6 M births, R05im) ≈ 1 in 1,000 | ✔✔ |
| CL ± P sex ratio | 65 % male | M/F **1.70** (≈ 63 % male, R05im) | ✔✔ |
| Cleft palate alone | ~1 in 1,500 (≈ 6.7) | **3.3** per 10,000 live births (meta-analysis, 59 studies, all cleft palate — isolation not stated, R05in) ≈ 1 in 3,000 | **⚑** (D-078 e) |
| 22q11.2 deletion | ~1 in 4,000 (2.5) | **4.7** (≥ 1 in 2,148; newborn screening, Ontario, R05io); a 2020 review: 1 in 4–6,000 (R05fa) | **⚑** (D-078 c) |
| Robin sequence | ~1 in 8,500 (1.2) | **0.95** (meta-analysis, 34 studies, live births, R05ip); 1.8 (Netherlands, R05iq) | ✔✔ |
| Hemifacial microsomia / OAV spectrum | ~1 in 5,600 (1.8) | **0.38** (EUROCAT, 34 registries, OAVS = microtia + one major feature, R05is) ≈ 1 in 26,000 | **⚑** (D-078 d) — definitions differ |
| Holoprosencephaly | not given | **1.2** (California, total births; 41 % chromosomal, mostly trisomy 13, R05ir) | ✚ |
| Treacher Collins | 1 in 50,000 (0.2) | not retrieved (§10) | ✔ |
| Branchial cyst/fistula, thyroglossal cyst, lingual thyroid, tongue-tie, natal teeth | not given | not retrieved (§10) | — |

**Crest cells failed (arch 1 and the crest-built glands).**
- **22q11.2 deletion** (DiGeorge / velocardiofacial): the commonest human deletion; heart and **aortic-arch** defects, small thymus (T-cell infections), small parathyroids (low calcium, seizures), mild facial signs, learning difficulties, later psychiatric illness; **TBX1** in the deleted interval can cause it alone. `[E17.04 CC · R05io, R05fa, R05ez]` ✔ features · **⚑ rate** (c) · links **D-068 d** (half of interrupted aortic arch carries the deletion, R05ez) — a link, not new.
- **Treacher Collins** (mandibulofacial dysostosis): small maxilla, mandible and zygoma; cleft palate; outer and middle ear defects with conductive deafness; down-slanting eyes, lower-lid notch. Autosomal dominant, **TCOF1** (treacle keeps crest cells alive and dividing; migration is normal); ~60 % new mutations. `[E17.04 CC]` ✔ (no Tier 1 retrieved)
- **Robin sequence:** small jaw → tongue sits back and stays between the shelves → **cleft palate** + airway obstruction (R05ip); genetic, environmental or a deformation (chin pressed on chest in oligohydramnios). About a third of babies with cleft palate fit Robin sequence (R05iq) ✚ (More only, beyond Langman). `[E17.04 CC · R05ip, R05iq, R05ib]` ✔✔ rate · ✔✔ mechanism (shelves rise only when the tongue moves, R05ib)
- **Hemifacial microsomia / OAV spectrum** (Goldenhar): small flat maxilla, temporal and zygoma, often one-sided (65 % asymmetric); microtia/anotia, ear tags, epibulbar dermoids, vertebral defects; heart defects common (book 50 % "other"; R05is 27.8 % heart). `[E17.04 CC · R05is]` ✔ features · **⚑ rate** (d)
- **Crest and the heart:** crest also septates the outflow tract, so craniofacial defects travel with truncus, tetralogy and TGA; crest is easily killed by alcohol and retinoic acid. `[E17.04 CC · R05ii]` ✔ · ✔✔ *human* cardiac crest from Rh 6–7 (R05ii) · links D-057 (teratogens)

**A buried cleft stayed open.**
- **Lateral cervical (branchial) cyst** — a left-over cervical sinus, usually just below the angle of the jaw, along the **front of sternocleidomastoid**; often shows later in life. **External fistula** when arch 2 fails to cover arches 3–4; **internal fistula** (rare) opens near the tonsil when the cleft–pouch membrane breaks. `[E17.04 CC]` ✔ (rate not retrieved)

**A migrating gland stopped short.**
- **Ectopic thymus / parathyroid** along the descent path; inferior parathyroids wander most (sometimes at the carotid fork). `[E17.04 CC]` ✔
- **Thyroglossal cyst** — always **midline**, anywhere on the path, about half at or just below the hyoid; may become a fistula after a rupture. **Ectopic (lingual) thyroid** — commonest at the tongue base behind the foramen caecum; same diseases as a normal thyroid. `[E17.06 CC]` ✔ (rates not retrieved)

**Prominences or shelves didn't merge (clefts).**
- **The incisive foramen splits clefts in two:** *in front* — lip, upper jaw (between lateral incisor and canine), up to the foramen — failed **maxillary + medial nasal** merging (one or both sides); *behind* — secondary palate, uvula — failed **shelf** fusion (a tongue held up by a small jaw, shelves too small, shelves that never rise, or edges that meet but do not fuse); *both*. `[E17.09 CC]` ✔
- **CL ± P and isolated CP are separate conditions** (different causes, sex ratios, risks): CL ± P more in males and in Asian and Native American populations; CP more in females (book: female shelves close ~1 week later). `[E17.09 CC · R05il, R05im]` ✔✔ CL ± P rate and sex ratio · ⚑ CP rate (e) · ✔ sex timing (book only)
- **Most are multifactorial** (AN74.3); some syndromic — **van der Woude** (IRF6, lower-lip pits) the commonest; teratogens: anticonvulsants, especially **valproate**; maternal **smoking**. `[E17.09 CC · R05bu, R05bv]` ✔ · links **D-057** (R05bu valproate ~10 % major malformations; R05bv ondansetron clefts +2.7 per 10,000) — links, not new. Associated anomalies in ~29 % of CL ± P (R05im) ✚ (More only, beyond Langman).
- **Oblique facial cleft** (maxillary + lateral nasal fail along the nasolacrimal groove; duct exposed) and **median cleft lip** (medial nasal prominences fail to meet — warns of missing midline brain). `[E17.09 CC]` ✔

**The midline was missing.**
- **Holoprosencephaly face:** too little midline tissue → close-set or single eye, single nostril or proboscis, single ventricle; set very early (**days 19–21**); SHH mutations, cholesterol defects, alcohol. `[E17.09 CC · R05ir]` ✔ · ✚ rate 1.2 (R05ir) · Ch 18 owns the brain side.

**A membrane didn't let go.**
- **Tongue-tie (ankyloglossia):** the frenulum, normally the only anchor left after cell death, reaches the tip. `[E17.05 CC]` ✔ (rate not retrieved — §10)
- **Tooth anomalies:** natal teeth; number, shape, size; tetracycline stains; enamel defects (vitamin D). `[E17.12 CC]` ✔

---

## 5. ⚑ Watch items → decision D-078 (owner picks)
- **(a) When the palatal shelves rise.** Book: week 7 (shelves vertical at ~6.5 wk, horizontal at ~7.5 wk). *Human* specimens: not raised at CS21–22, raised in five of eight CS23 embryos (four already fused) and in all three early fetuses (R05ib, Kyoto, 22 samples); fusion starts abruptly at CS23 (R05ic, 43 specimens); shelves move during stage 23 (R05id) — i.e. **end of week 8 (~day 56–60)**. Options: (1) default; (2) card: "the shelves rise at the end of week 8 and fuse over weeks 9–12", book week in More. *Recommended (2)* — three independent human series agree.
- **(b) How the nasal septum meets the palate.** Book: the septum grows down to join the newly fused palate. R05if (*human* SEM, CS16 → fetal): the septum does **not** grow down; it is the tissue between the primary choanae, present from the start, and the shelves reach it when they rise. Options: (1) default; (2) card: "the rising shelves meet the septum", book wording in More. *Recommended (2).* Not used as a misconception while (b) is open — the book wording stays the card default (B7).
- **(c) How common 22q11.2 deletion is.** Book: ~1 in 4,000. R05io (unbiased newborn screening, 30,074 Ontario blood spots): at least **1 in 2,148** (4.7 per 10,000; 95 % CI 2.5–7.8). R05fa (2020 review): 1 in 4–6,000. Clinic-based counts miss mild cases. Options: (1) default; (2) card: "about 1 in 2,000–4,000 births — many mild cases are missed", book in More. *Recommended (2).* Links D-068 d.
- **(d) How common hemifacial microsomia is.** Book: 1 in 5,600. R05is (EUROCAT, 34 registries, 1990–2009): OAV spectrum **3.8 per 100,000** (~1 in 26,000) — but defined as microtia plus one major feature; milder one-sided cases are missed. Partly definitional (as D-043 b). Options: (1) default; (2) card: "rare — about 1 in 5,000 to 1 in 25,000 depending on how it is counted", both in More. *Recommended (2).*
- **(e) How common isolated cleft palate is.** Book: ~1 in 1,500. R05in (meta-analysis, 59 studies, 21 M live births): **3.3 per 10,000** (~1 in 3,000) — all cleft palate, isolation not stated. Live births only (terminations and stillbirths excluded), heterogeneous studies; the matching ICBDSR cleft-palate paper was not found (§10). Options: (1) default; (2) card: "about 1 in 2,000–3,000", book in More. *Recommended (1) until a registry source is read* — keep the exam figure, and say "rarer than cleft lip" (true in both).
- **(f) Note, not ⚑ (downgraded by G-Sci) — which rhombomeres feed arch 1.** Book: R1 and R2 (with caudal midbrain) → arch 1. R05ii (185 *human* embryos): pre-otic crest is continuous at CS10 and crest-free zones appear at **Rh 1, 3 and 5** only from CS11 — so Rh 1 may still contribute early; no conflict shown. Tier D may add "in human embryos rhombomere 1, like 3 and 5, is crest-free from CS11" (beyond Langman).
- **(g) Note, not ⚑ — when the thyroid starts working.** Book: end of month 3. R05ih (45 *human* thyroids): follicles and T4 from **11 "gestational weeks"** — if that is a last-period clock, ~9 weeks after fertilization (earlier than the book); if post-conception, it fits. Cards keep the book until the full text gives the clock (§10).
- **(h) Note, not ⚑ — the book gives the laryngeal cartilages two origins:** lateral plate mesoderm (E17.00) and fused arch 4 + 6 cartilages (E17.01, table). Not contradictory if the 4th/6th "arch" mesenchyme there is lateral plate; cards say "from the arch 4 and 6 region" and Tier D adds "lateral-plate mesoderm". R05ik confirms the cartilages at CS23 but not their source. Links **D-072 e** (what seals the larynx) — no new evidence.
- **(i) Links, not new ⚑:** **D-068** (arch arteries, 22q11 ↔ IAA) — Ch 17 repeats Ch 13; only the rate is new (c). **D-066** (head muscles from somitomeres; arch muscle lists) — Ch 17's lists agree with Ch 11; *human* hypoglossal cord from occipital myotomes 1–4 (R05ii) supports the tongue line. **D-064** (skull, craniosynostosis) — no new evidence. **D-057** (valproate, smoking, ondansetron and clefts) — no new evidence. **D-030** (clocks) — applied throughout.
- **(j) Curriculum note:** NMC 2018 Vol I has **one** core code for all head-and-neck development — **AN43.4** (face, palate, tongue, branchial apparatus, pituitary, thyroid, eye) — and **no code for teeth or nasal-cavity development** (teeth appear only as DE1.1/DE5.1 "parts of the tooth" and FM3.1 eruption for age). **AN39.1** asks for the "embryological basis of the nerve supply" of the tongue (core, SH) — the tongue card must deliver it. **AN25.6** (arch arteries) is **non-core**. **SU19.1–19.2** (cleft lip and palate, core) and **SU22.1/22.5** (thyroid, parathyroid applied anatomy) are the surgery hooks.
- **(l) Book slips (notes):** p 286 dates the five prominences to "42 days" while its own figure says ~24 days and E17.07 says the end of week 4 — cards use the end of week 4; the pouch text names PAX2 for the dorsal pouch endoderm but its figure legend says PAX1 — Tier D uses PAX1, both noted. **Linked ⚑s from other chapters (e.g. D-068 a on the artery row) do not set a Ch 17 concept's research.txt mark** — same rule as Ch 16.
- **(k) Book update to keep (not a ⚑):** 14e says the **first cleft does not form the ear canal** (first-arch ectoderm invaginates instead). Many older books and exam keys still say it does. Our map rows `clefts` (Ch 17) and `extear` (Ch 19) said the old version — **both fixed in this commit** (concepts.txt summaries), and misconception 4 refutes it.

## 6. Top student misconceptions (refute in cards and Checks — craft §3.4)
1. **"Humans have gills or gill slits as embryos."** (map row) Arches look gill-like; no gills form and the clefts never open into the pouches `[E17.01]` ✔.
2. **"Arches only make the neck."** They build the **face** too — the first arch makes most of it `[E17.01]` ✔.
3. **"A muscle is supplied by the nerve of the region it ends up in."** It keeps the nerve of **its own arch** wherever it migrates — each arch has its own cartilage, muscle, nerve and artery (map row) `[E17.01]` ✔.
4. **"The first cleft becomes the ear canal."** Not in 14e: first-arch ectoderm grows in; all clefts close `[E17.03]` ✔ (note k).
5. **"Meckel cartilage turns into the mandible."** The mandible forms **in membrane around** it; Meckel leaves the malleus, incus and a ligament `[E17.01 · R05ik]` ✔✔.
6. **"Inferior parathyroids come from pouch 4."** (map row) **Pouch 3** — pulled down by the thymus `[E17.02]` ✔.
7. **"The thymus comes from pouches 3 and 4."** From **pouch 3** only `[E17.02 · R05ig]` ✔✔.
8. **"C cells are thyroid follicle cells."** They come from the **ultimobranchial body** (pouch 4) `[E17.02, E17.06]` ✔.
9. **"The thyroid starts in the neck."** It starts at the **tongue** (foramen caecum) and descends (map row) — why cysts are midline anywhere from tongue to neck `[E17.06]` ✔.
10. **"Thyroglossal cysts are at the side of the neck."** Always **midline**; branchial cysts are **lateral** (front of sternocleidomastoid) `[E17.04 CC, E17.06 CC]` ✔.
11. **"Taste on the front of the tongue is trigeminal."** Touch V3, taste **VII** (chorda tympani) `[E17.05]` ✔.
12. **"Tongue muscles come from the arches."** Mostly from **occipital somites** → XII `[E17.05 · R05ii]` ✔✔.
13. **"The face is one sheet that folds."** (map row) It is **five prominences** (then two nasal pairs) that grow and merge `[E17.07]` ✔.
14. **"The lateral nasal prominence makes the side of the upper lip."** It makes the **ala**; the lip is medial nasal + maxillary `[E17.07]` ✔.
15. **"Cleft lip and cleft palate are one defect."** (map row) Two failures either side of the **incisive foramen**, with different causes and sex ratios `[E17.09 CC · R05im]` ✔✔.
16. **"Cleft palate means a hole into the nose at the front."** Front clefts (lip, jaw) are anterior to the foramen; the palate cleft is posterior `[E17.09 CC]` ✔.
17. **"The shelves grow sideways from the start."** They hang **down** beside the tongue, then rise `[E17.09 · R05ib]` ✔✔ (timing ⚑ a).
18. **"Robin sequence is a cleft that causes a small jaw."** The **small jaw comes first** and blocks the shelves `[E17.04 CC · R05ib]` ✔✔.
19. **"Enamel and dentin come from the same layer."** Enamel ← ectoderm (ameloblasts); dentin, pulp, cementum ← crest mesenchyme `[E17.11]` ✔.
20. **"Permanent teeth form after the milk teeth fall out."** Their buds form in **month 3 of pregnancy** and wait `[E17.11]` ✔.

## 7. Curriculum map (R30 — NMC AN table; source note below)
**Source note:** read from **NMC *Competency Based UG Curriculum Vol I*** (`UG-Curriculum-Vol-I.pdf`, staged from Studio home `references\nmc\`, 22 Nov 2026). Vol I is the **2018** text; the 2024 MGMUHS reprint is not in `references\`, so **2024 wording is unchecked** (§10).

**Where Ch 17 sits (the prompt's guesses, checked):**
- **AN43.4** — development and developmental basis of congenital anomalies of face, palate, tongue, branchial apparatus, pituitary, thyroid and eye (core) ✔ — **the one development code for the chapter**; no teeth, no nasal cavity.
- **AN35** neck — **AN35.2** thyroid (core) ✔ · **AN35.8** thyroid swellings (non-core) — thyroglossal cyst.
- **AN36** — **AN36.1** palatine tonsil + soft palate (core) ✔ (pouch 2; palate) · AN36.2 Waldeyer ring.
- **AN37** — **AN37.1** nasal septum + lateral wall (core) · **AN37.2** paranasal sinuses (core) ✔.
- **AN38.1** larynx (core) ✔ — arch 4/6 cartilages and muscles.
- **AN39.1** tongue incl. "embryological basis of nerve supply" (core, SH) ✔.
- **AN40.1** external ear · **AN40.2** middle ear + auditory tube (core) ✔ — pouch 1, cleft 1, ossicles (Ch 19 owns the ear).
- **AN28.1** facial-expression muscles + nerve · **AN28.2** sensory supply of face (core) — arch 2 muscles, V1–V3 skin.
- **AN33.2** muscles of mastication (core) — arch 1 muscles. **AN26.6** membrane bones (non-core) — mandible, maxilla.
- **AN25.6** aortic arch arteries (non-core) — the arch arteries.
- **AN74.3** multifactorial inheritance (core) — clefts. **AN75.1** chromosomal aberrations (core) — 22q11.2 deletion. AN74.4 lists no head-and-neck condition; **AN75.3** (non-core) includes Patau syndrome — trisomy 13 is the commonest chromosomal cause of holoprosencephaly (R05ir), a More link.

| Concept | AN codes |
|---|---|
| E17.00.01 What builds the head and neck | AN43.4 |
| E17.01.01 Pharyngeal arches | AN43.4, AN25.6 |
| E17.01.02 Arch derivatives | AN43.4, AN28.1, AN33.2, AN38.1, AN40.2, AN26.6 |
| E17.01.03 Stomodeum | AN43.4 |
| E17.02.01 Pharyngeal pouches | AN43.4, AN35.2, AN36.1, AN40.2 |
| E17.03.01 Pharyngeal clefts | AN43.4, AN40.1 |
| E17.03.02 Arch and pouch defects | AN43.4, AN75.1 |
| E17.04.01 Molecular regulation of facial development | AN43.4 |
| E17.05.01 Tongue | AN39.1, AN43.4 |
| E17.05.02 Tongue-tie | AN39.1 |
| E17.06.01 Thyroid descent | AN43.4, AN35.2 |
| E17.06.02 Thyroglossal cyst and ectopic thyroid | AN43.4, AN35.8 |
| E17.07.01 Face from five prominences | AN43.4, AN28.2 |
| E17.07.02 Nasal placodes and prominences | AN43.4, AN37.1 |
| E17.08.01 Intermaxillary segment | AN43.4 |
| E17.09.01 Secondary palate | AN43.4 |
| E17.09.02 Cleft lip and cleft palate | AN43.4, AN74.3 |
| E17.10.01 Nasal cavities and sinuses | AN37.1, AN37.2 |
| E17.11.01 Teeth | — (no AN code) |
| E17.12.01 Tooth regulation and defects | — (no AN code) |

**Outside AN (for the More line only):** SU19.1–19.2 cleft lip and palate · SU22.1 thyroid · SU22.5 parathyroid · DE1.1/DE5.1 parts of the tooth · FM3.1 tooth eruption for age.

## 8. Scene note — visual references (look, don't copy — RULES G5)
- **Arches appear (CS10 → CS13):** side view, bars rising head-first, one colour per arch (pattern + label, H5); a cut-away shows cartilage, muscle, nerve and artery in each — the "four parts" rule as one repeated icon. B2 stamp "≈ day 22–32 · CS10–13".
- **Arch → adult (D4):** each arch's colour flows to its adult parts on a skull-and-neck outline (malleus/incus, stapes, hyoid horns, larynx); nerve lines stay attached to their muscles as they migrate.
- **Pouches (week 5 → 7):** inside view of the pharynx; buds leave the wall; the thymus slides down **past** the pouch-4 parathyroid (the swap) — end on the adult neck from behind with four parathyroids labelled by pouch (D9 cross-section: thyroid with parathyroids behind).
- **Arch 2 grows down (week 5–6):** a collar over arches 3–4 burying clefts 2–4 in the cervical sinus; ghost line along the front of sternocleidomastoid = where a lateral cyst would sit.
- **Thyroid descent (weeks 4 → 7):** midline bud from the foramen caecum on a dotted path in front of hyoid and larynx; dots = possible cyst/ectopic sites, all on the midline.
- **Face (weeks 4 → 10):** front view, five prominences → nasal ring → merge; colour-match each prominence to its adult region (frontonasal → forehead/bridge, medial nasal → philtrum/tip, lateral nasal → ala, maxillary → cheek/outer lip, mandibular → chin). External ears drift outward and up with growth (R05it, Kyoto — look only).
- **Palate (CS21 → week 12):** frontal cut through the mouth: shelves down beside a high tongue → head lifts, jaw grows forward, tongue drops → shelves up and fuse to each other and to the septum. Label "≈ CS23 · week 8 (specimens); book: week 7" (⚑ a). End on the palate from below with the incisive foramen as the front/back line — the same line that sorts the clefts.
- **Teeth (week 6 → birth):** one tooth through bud, cap, bell; two colours (ectoderm enamel organ vs crest papilla) + patterns; the enamel knot glowing and fading.
- **Never from the book:** its arch, nerve, skeleton, pouch, tongue, thyroid, face, palate, nasal and tooth figures and its three tables are copyrighted; every one is redrawn by us (D6, visual-style §16). Its patient photographs (cervical cyst, Robin, 22q11, hemifacial microsomia, clefts, holoprosencephaly, thyroglossal cyst) are never shown — diagrams only.

## 9. Why learners struggle here (M05)
- **A 4 × 5 grid** (cartilage, muscle, nerve, artery × arches 1, 2, 3, 4, 6) — teach the **nerve column first**: once the nerve is known, the muscles follow.
- **Pouch 3 ends up below pouch 4** — show the swap as motion, not a list.
- **Two surfaces, two names:** clefts (outside, ectoderm) vs pouches (inside, endoderm) — always one colour each.
- **The tongue's four nerves** — a map of where each arch's lining ended up, not a list to memorize.
- **Front vs back clefts** — one landmark (incisive foramen) sorts every facial cleft.
- **Clocks:** book weeks vs Carnegie stages for the palate (⚑ a); the thyroid source's clock is unclear (note g).

## 10. X1 to-do — done 22 Nov 2026, with open items
- Done: real locators + sub-locators; seven short-section spills, two misfiled boxes and four untitled boxes named (→ I1); staging from human specimens (R06/R08 by stage; R05ii, R05ij, R05ik, R05ic, R05ib, R05if by Carnegie stage; R05id/R05ie by weeks post conception; R05ih clock unclear); Tier A for 8 concepts (head sources, arches, arch derivatives, pouches, tongue, thyroid, face, secondary palate); Tier B–D with the arch table by tissue; clinical rows in 6 mechanism groups with rates per 10,000; 20 misconceptions; AN map from NMC Vol I; 19 sources **R05ib–R05it** (R05il–R05is clinical); G-Sci fresh-eyes review: pass with fixes, 9 MUST + 13 SHOULD, all applied (⚑ f downgraded to a note).
- **Rates not retrieved:** Treacher Collins (book 1 in 50,000), branchial cysts/fistulas, thyroglossal cyst (classic autopsy ~7 % has no PubMed abstract found), lingual/ectopic thyroid, tongue-tie (only a breastfeeding meta-analysis found), natal teeth, median cleft, van der Woude lip-pit figures.
- **ICBDSR/IPDTOC cleft-palate-alone paper** — needed before D-078 e can move to option 2.
- **Human tooth timing** (lamina, bud, cap, bell; book weeks only) — no human Tier 1 retrieved; Kyoto or Ooë-type human series next.
- **Human thyroid stage** (bud CS, in place week 7): none retrieved; **R05ih full text** for its clock (note g).
- **Human EAM origin** (14e's correction): no human Tier 1 retrieved; Ch 19 (ear) X1 should look.
- **Female shelves close ~1 week later** (book): Burdi & Silvey 1969 has no abstract — read the full text or find a newer human series before a card says it.
- **R01 3D Atlas:** check CS13–23 face and pharynx models before the arch, pouch and face scenes (look only, NC-ND). **R04 Kyoto:** the palate CT/MRI series behind R05ib for the palate scene (licence per dataset).
- **Full texts not read:** R05ib (stage-by-stage shelf positions), R05ic, R05if, R05ig (thymus stage), R05ii (crest tables).
- **2024 wording** of AN43.4 (MGMUHS reprint): not in `references\`.
