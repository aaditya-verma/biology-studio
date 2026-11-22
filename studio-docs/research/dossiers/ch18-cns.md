# Research dossier — Ch 18 · Central nervous system (for C-step cards + episodes)

*(Purpose: cited, marked facts, staging, misconceptions and clinical correlates for Ch 18, the ninth chapter of Part 2. It has 5 sections of 2–13 pages and 5 boxes, read in two halves: (1) spinal cord and brain — layers, alar/basal plates, spinal nerves, myelination, cord position, vesicles and flexures, hindbrain → forebrain; (2) regulation, cranial nerves and autonomic — molecular regulation, cranial nerves, sympathetic and parasympathetic, adrenal medulla. Cards draft from this file. Updated: 22 Nov 2026 · Bio · Research · X1 Ch 18 · by Aaditya. Own words only; no book sentences, figures or tables (RULES §G). Every list is regrouped in our own order, including the order inside table cells: the brainstem nuclei are grouped by job (moves muscle · runs glands and gut · senses), not as the book's table, and the cranial nerves by where their nucleus sits.)*

**How to read a line:** fact in our words · `[book section · registry source]` · mark (RULES B6–B7): **✔✔** book + Tier 1 agree · **✔** book only · **⚑** book vs Tier 1 disagree (D-entry) · **✚** beyond the book (Tier 1 only; More / Tier D only, "beyond Langman") · **≈** blocks final. **Species tag:** a line from mouse or chick says so (*mouse*). Those lines can confirm a mechanism; they never give a human day or number. **Rates** are per 10,000 births unless stated; "total" = live births + stillbirths + terminations.

**Citation check, read before you cite:** checked 22 Nov 2026. `tools/card-check/citations.py` matches `R\d\d[a-z]{0,2}`, so the new ids **R05iu–R05jj** parse. Every PMID was grepped in the registry before its id was given: the two-sites paper (PMID 11948562) is **already R05l** and is re-used, not re-added. Author lists are copied from the PubMed record (first three, then et al.). R05ed and R05bs stay retired. `sources.json` is rebuilt in this commit (`check.py --write-sources`, D-065 (6)). **Registry sources re-used:** R05l (two fusion sites), R05m (caudal neuropore at S2, spinal crest), R05t/R05u (folic acid trials), R05v/R05bt (US fortification), R05w (VANGL1), R05x/R05y (India NTD burden), R05br (MOMS fetal surgery), R05bu (valproate), R05ir (holoprosencephaly, California), R05ha/R05gp (Hirschsprung, Ch 15), R06/R08 (stage tables). **Read and not used:** Scoville & Milner 1957 (hippocampus and memory — no abstract, so it cannot carry a mark; note e), Horgos 2020 (fetal white-matter dissection — "gestational weeks" with no clock stated), Lee 2004 (conus most often at L1 in 210 MRIs — R05jc is larger and covers it).

**Ages — four clocks.** (1) The book's events are in **days or weeks after fertilization** (cranial neuropore day 25, caudal ~day 28, five vesicles by week 5, hemispheres from the start of week 5, Rathke pouch ~week 3, sympathetic crest week 5, corpus callosum by week 10) and **months** for fetal events (myelination from month 4, cord the length of the spine at month 3) — read as after fertilization (D-030). Its NTD scan and surgery ages ("12 weeks of gestation", "22 weeks of gestation") are **weeks of pregnancy** (last-period clock, ~2 weeks ahead). (2) Specimen papers give **Carnegie stages** with classic days (R05l, R05iu–R05ix: O'Rahilly & Müller, Carnegie collection) or **CS only** (R05iy, Kyoto) — matched by stage to R08 (`tools/indexer/carnegie.json`, D-030 a). R05iz gives **ovulation age** (= after fertilization); R05jf gives **weeks post-fertilisation** + CS. (3) **R05ja writes "postovulatory or gestational weeks"** for the same number — clock unclear, so its 4.5 weeks is read as "about week 5" and never moves a book date on its own. On a last-period clock 4.5 weeks would be ~2.5 weeks after fertilization, before any forebrain exists — so the post-ovulatory reading must be meant (⚑ b leans on that, not on the exact number). (4) The infant conus papers use **postmenstrual weeks** (R05jd) or term/preterm at birth (R05je) — after birth, so no conversion is needed for the "at birth" line.

**Section locators (checked against the PDF, 22 Nov 2026; printed page = PDF page − 19):**
- **E18.00 pp 313–314** — neural plate, folds, fusion and neuropores p 313; the three then five vesicles, flexures and ventricles pp 313–314.
- **E18.01 Spinal cord pp 314–324** — neuroepithelial, mantle and marginal layers pp 314–315; basal, alar, roof and floor plates + intermediate horn p 315; neuroblasts pp 316–318; neural crest p 318; glia p 318; spinal nerves pp 318–320; myelination p 320; positional changes of the cord pp 320–321; *Molecular regulation of nerve differentiation in the spinal cord* box **pp 321–322**; *Neural tube defects* box **pp 322–324** (types p 322–323, AFP, scans and fetal surgery p 323, causes and folic acid **p 324**).
- **E18.02 Brain pp 324–336** — brainstem vs higher centres p 324; myelencephalon pp 324–326 (the brainstem-nuclei table **p 326**); metencephalon and pons pp 326–327; cerebellum pp 327–329; mesencephalon p 329; diencephalon pp 329–331 (epiphysis p 329, thalamus/hypothalamus pp 329–331, pituitary p 331, *Hypophyseal defects* box **p 331**); telencephalon pp 331–335 (hemispheres p 331, corpus striatum and choroid plexus p 332, cortex and gyri p 333, olfactory bulbs pp 333–334, commissures pp 334–335); meninges p 335; CSF **pp 335–336**.
- **E18.03 Molecular regulation of brain development pp 336–338** — HOX and rhombomeres p 336; forebrain/midbrain genes, ANR and isthmus pp 336–338; dorsal/ventral patterning and SHH–cholesterol **p 338**; *Cranial defects* box **pp 338–341** (holoprosencephaly and schizencephaly pp 338–339, encephaloceles pp 339–340, anencephaly p 340, hydrocephalus and microcephaly p 341).
- **E18.04 Cranial nerves pp 338, 341–344** — the opening lines p 338; rhombomeres, motor nuclei and sensory ganglia pp 341–342; the origins table **p 343**; the ganglia (crest vs placode) table **p 344**.
- **E18.05 Autonomic nervous system pp 342–348** — sympathetic pp 342–346; parasympathetic pp 346–347; adrenal gland pp 346–348; *Pheochromocytomas* + *Congenital megacolon* box **p 348**.
- **E18.06 Summary pp 349–350** · **E18.07 Problems p 350**.

**I1 gaps** (tree.json) → I1 to-do:
- **Pages spill**, as the prompt expected: E18.00 ends **p 314** (I1 313); E18.01 ends **p 324** (I1 323 — the folic-acid end of the NTD box is on p 324); E18.02 ends **p 336** (I1 335 — CSF); E18.03 ends **p 338** (I1 337) and its box runs **pp 338–341**.
- **E18.04's pages are mostly another section's box.** I1 gives E18.04 pp 338–341, but those pages hold E18.03's *Cranial defects* box; the cranial-nerve text sits on p 338 (a few lines) and **pp 341–344** (with both tables), overlapping E18.05's start (p 342) because of the two-column layout.
- **One box filed under the wrong section:** *Pheochromocytomas* (PDF 367, p 348; also holds *Congenital megacolon*) is filed under **E18.04** but belongs to **E18.05** (adrenal medulla, crest migration). Cite its lines `E18.05 CC`.
- **Two untitled boxes + one cut title:** PDF 350 → *Hypophyseal defects* (E18.02); PDF 357 → *Cranial defects* (E18.03); the E18.01 molecular box's title stops at "Nerve" → *Molecular regulation of nerve differentiation in the spinal cord*.

---

## 1. Staging & scale — neural plate to the folded cortex (RULES B2)
Human anchors: **R06/R08** (stage definitions and classic ages), **R05l** (98 *human* embryos CS8–13, fusion sites), **R05iu** (20 *human* CS11 embryos), **R05iv** (24 *human* CS12 embryos), **R05iw** (88 *human* embryos CS18–20), **R05ix** (22 *human* embryos CS21–23, closing a 340-embryo series), **R05iy** (101 Kyoto MRIs CS13–23), **R05jf** (*human* 3D, 4.5–10 wk post-fertilisation, sympathetic trunks), **R05iz** (21 *human* cords, 5–13 wk), **R05ja** (*human* forebrain, microglia), **R05jc/R05jd/R05je** (adult and infant conus level). Days are the book's unless a source is named.

| When | Carnegie / clock | What happens `[section · source]` | Mark |
|---|---|---|---|
| Week 3 | CS8 | **Neural plate** — a long, thick ectoderm plate (a big placode) in front of the node `[E18.00, E18.06]` | ✔ (note j: the text says the start of week 3, the summary the middle) |
| Week 3 → 4 | CS10 | **Folds fuse**, first in the hindbrain–neck region, running both ways; a second, later site in the forebrain `[E18.00 · R05l]` | ✔✔ two sites · **⚑ d** which way the forebrain site runs (book: both ways; R05l: backwards only) |
| ~Day 24–25 | **CS11** | **Rostral neuropore closes** at the end of CS11 (the stage spans 13–20 somite pairs; book: 18–20 somites, day 25); the first marginal layer appears `[E18.00, E18.01 · R05iu]` | ✔✔ · ✚ marginal layer |
| ~Day 26–28 | **CS12** | **Caudal neuropore closes** (~25 somite pairs; book: ~3 days after the rostral), its last point at future S2; secondary neurulation starts below; **sulcus limitans** visible in cord and hindbrain; first nerve fibres in the hindbrain `[E18.00, E18.01 · R05iv, R05m]` | ✔✔ · ✚ S2, secondary neurulation |
| Week 4 (~day 28, R08 for CS13) | CS13 | **Three primary vesicles** (fore-, mid-, hindbrain) and **two flexures** (cervical, cephalic); the book's figure is labelled ~28 days, its text gives no day `[E18.00 · R08]` | ✔ · ✚ fore-, mid- and hindbrain neuromeres already at CS11 (R05iu) |
| Week 5 | CS14–15 | **Five secondary vesicles**; **pontine flexure** between the two hindbrain parts; hemispheres start to bulge (beginning of week 5) `[E18.00, E18.02]` | ✔ |
| Week 5 | **CS14** | **Sympathetic crest cells** gather beside the dorsal aorta (neck and upper chest first); spinal-nerve fibres reach them CS15–16 `[E18.05 · R05jf]` | ✔✔ (book: week 5) · ✚ order |
| ~Week 5 | clock unclear | **Microglia** enter the forebrain through the meninges, choroid plexus and ventricular zone `[E18.01 · R05ja]` | **⚑ b** |
| Week 7 | CS18–20 | Hemispheres expand fast and become separate; **choroid plexuses** of the 4th and lateral ventricles appear `[E18.02 · R05iw]` | ✔ · ✚ plexus stage |
| Week 8 | **CS21** | **Cortical plate** first appears (insula region) `[E18.02 · R05ix]` | ✚ |
| Weeks 7–8 | CS20 → 23 | Cerebellum grows from ~7 % to ~13 % of the hindbrain volume; the cerebellar plate already has an external germinal layer `[E18.02 · R05iy, R05ix]` | ✚ |
| End of week 8 | **CS23** | **Anterior commissure** crosses; superior and inferior colliculi can be told apart; brain tissue has grown ~164-fold since CS13 `[E18.02 · R05ix, R05iy]` | ✔ · ✚ commissure stage, volume (note f) |
| Week 10 | fetal | **First myelin** in the cervical cord (ventral marginal layer, oligodendrocytes) `[E18.01 · R05iz]` · **corpus callosum** appears (book) `[E18.02]` | **⚑ c** · ✔ |
| Week 12 | fetal | Cerebellar plate shows **vermis + hemispheres** `[E18.02]` | ✔ |
| Month 3 | fetal | Cord fills the whole spinal canal; nerves leave at their own level `[E18.01]` | ✔ |
| Month 4 → birth | fetal | Myelin makes nerve fibres look white; the spine and dura outgrow the cord; gyri and sulci form late in fetal life `[E18.01, E18.02]` | ✔ (⚑ c on the start) |
| Birth → early infancy | after birth | Cord end: book **L3**; ultrasound — above L2 in 92 % of term babies (R05je); between T12/L1 and L1/2 in 84 % of infants from term to ~5 months (40–63 postmenstrual wk, R05jd), but at L2–L4 in 78 % of preterm babies (30–39 wk, R05jd) `[E18.01 · R05jd, R05je]` | **⚑ a** |
| Adult | after birth | Cord end: book **L2–L3**; MRI in 504 adults — mean **lower third of L1** (range mid-T12 → upper L3) `[E18.01 · R05jc]` | **⚑ a** |

**Scale anchors (B2):** CS11 ~2.5–4.5 mm · CS12 ~3–5 mm · CS13 ~4–6 mm · CS18 ~11–14 mm · CS23 ~23–32 mm (R08 classic). The book's figures name **~27 mm at 8 weeks** and **70 mm at 12 weeks** — redraw our own scale bars.

---

## 2. Tier A facts — cited and marked
### E18.01.01 Neural tube layers · AN64.2, AN79.3
- **Three layers, inside → out:** the **ventricular (neuroepithelial) layer** that divides beside the lumen; the **mantle layer** of new neuroblasts → **grey matter**; the **marginal layer** of their fibres → **white matter** once myelinated. `[E18.01]` **✔** · ✚ the marginal layer appears first at CS11–12, in the hindbrain and cord (R05iu, R05iv)
- **One cell, many fates, in order:** neuroepithelial cells make **neuroblasts first** (which then stop dividing), **glioblasts next** (astrocytes, oligodendrocytes), and finally line the canal as **ependyma**. `[E18.01]` **✔**
- **Neuroblast shape changes:** round → two processes (bipolar) → one long axon + many dendrites (multipolar). `[E18.01]` **✔**
- **Microglia are the odd ones out** — they are not made by the tube. Book: from blood-vessel mesenchyme, in the second half of development. `[E18.01]` **⚑ b** — *human*: microglia enter from ~week 5, first through the meninges, choroid plexus and ventricular zone, then a second wave along vessels at ~12–13 weeks (R05ja); *mouse*: they come from yolk-sac myeloid progenitors (R05jb).

### E18.01.02 Alar and basal plates · AN64.2
- **Ventral = motor, dorsal = sensory.** Each side of the tube thickens into a ventral **basal plate** (motor horn) and a dorsal **alar plate** (sensory horn), split by the **sulcus limitans**; the **roof and floor plates** carry no neuroblasts — only crossing fibres. `[E18.01, E18.06]` **✔** · ✚ sulcus limitans visible by CS12 (R05iv)
- **A small lateral (intermediate) horn** between them holds the **sympathetic** preganglionic neurons — only at **T1–L2**. `[E18.01, E18.05]` **✔** (note h: one page says L2 or L3)
- **The plan continues into the brainstem**, opened out like a book (sensory now lateral, motor medial); the cerebellum and hemispheres are mostly alar. `[E18.02]` **✔**
- **Signals set the plates:** SHH from notochord then floor plate (ventral) vs BMPs from ectoderm then roof plate (dorsal) — two opposed gradients. `[E18.01 MR]` **✔** (links E18.01.07, Tier D)

### E18.02.01 Brain vesicles and flexures · AN64.2, AN79.3
- **Three → five.** Forebrain → **telencephalon + diencephalon**; midbrain stays one; hindbrain → **metencephalon + myelencephalon**. `[E18.00]` **✔**
- **Three bends:** cervical (hindbrain–cord), cephalic (midbrain) — both early; **pontine** (between the hindbrain halves) later. `[E18.00]` **✔**
- **Lumen → ventricles:** lateral ventricles (hemispheres) → interventricular foramina → 3rd (diencephalon) → narrow **cerebral aqueduct** (midbrain) → 4th (hindbrain) → **central canal**. `[E18.00, E18.02]` **✔**
- **Adult anchors (D4):** telencephalon → hemispheres; diencephalon → thalamus, hypothalamus, optic cup, posterior pituitary, pineal; midbrain → colliculi; metencephalon → pons + cerebellum; myelencephalon → medulla. `[E18.00, E18.02]` **✔**
- **Growth is uneven:** in Kyoto MRIs the forebrain grows fastest, from about a quarter of brain volume at CS13 to over half at CS23 (our division of R05iy's volumes). `[E18.02 · R05iy]` **✚**

### E18.05.02 Adrenal gland — two origins · (no NMC development code; note k)
- **Cortex from mesoderm, medulla from crest.** Week 5: coelomic lining between the mesentery root and the gonad sinks in → **fetal cortex**; a second wave wraps it → **definitive cortex**; crest cells invade from the medial side → **medulla**. `[E18.05]` **✔**
- **Medulla cells = modified sympathetic postganglionic neurons** (chromaffin cells): driven by preganglionic fibres, they release adrenaline and noradrenaline into the blood. `[E18.05]` **✔**
- **Fetal cortex works for the pregnancy:** it makes DHEA that the placenta turns into oestrogen, and shrinks fast after birth while the definitive cortex forms its three zones. `[E18.05]` **✔**
- **Crest guidance:** BMPs from the dorsal aorta pull crest to the sympathetic chain and the adrenal. `[E18.05]` **✔** (mechanism; no human source read)

### E18.01.05 Position of the cord end (Tier B; carried here because the map row flagged it) · AN57.2
- **The cord does not shrink — the spine and dura outgrow it.** Month 3: same length as the canal; later the column lengthens faster, so the cord end sits higher and lower roots slope down (**cauda equina**). `[E18.01]` **✔**
- **Levels:** book — L3 at birth, L2–L3 in adults; dural sac and subarachnoid space to **S2**; **filum terminale** to the coccyx. `[E18.01]` **⚑ a** — adults: mean lower L1 (T12–L3, R05jc); term babies: mostly at or above L1/2 (R05jd, R05je).
- **Lumbar puncture at L4–L5** clears the cord on either set of numbers. `[E18.01]` **✔** (safe in both)

---

## 3. Tier B–D facts (cards later; marked now)
**Brainstem nuclei grouped by job — one row per job, each brain level in the cells (our order, from input to output: senses · runs glands, gut and pupil · moves arch muscle · moves body-type muscle; the book's table runs the other way).** Then the remaining concepts **by mechanism** (things that are wired · things that are walled in · things that are signalled · things that migrate).

| Job (plate) | Midbrain | Metencephalon (pons) | Myelencephalon (medulla) | Cite | Mark |
|---|---|---|---|---|---|
| **Senses** (alar) | colliculi: visual (sup.), auditory (inf.) reflexes | V body sense; VII taste; VIII hearing + balance | IX/X gut + taste; skin sense; olivary nuclei | `[E18.02]` | ✔ |
| **Runs glands, gut, pupil** (basal, lateral) | Edinger–Westphal (III) → pupil | VII → submandibular, sublingual | IX, X → parotid, gut, airway | `[E18.02, E18.05]` | ✔ |
| **Moves arch muscle** (basal, middle) | — | V, VII | IX, X, XI | `[E18.02, E17]` | ✔ (links D-066) |
| **Moves body-type muscle** (basal, medial) — eye muscles, tongue | III, IV | VI | XII | `[E18.02]` | ✔ (IV starts in the metencephalon and moves up) |

| Concept | Fact (our words) | Cite | Mark |
|---|---|---|---|
| **Things that are wired** | | | |
| E18.01.03 Spinal nerves (B) · AN7.4, AN64.2 | Motor fibres leave the basal plate from **week 4** as the ventral root; sensory cell bodies sit **outside** the cord in crest-derived **dorsal root ganglia**, sending one process into the dorsal horn and one out with the motor fibres. The trunk splits at once into **dorsal rami** (back muscles, back skin, vertebral joints) and **ventral rami** (body wall, limbs, plexuses) — both mixed. | `[E18.01]` | ✔ · ✚ spinal crest from CS11, not yet in ganglia at CS12 (R05m, R05iv) · links D-066 |
| E18.01.04 Myelination (B) · AN64.2 | **Schwann cells** (crest) wrap **one** axon each in nerves; **oligodendrocytes** wrap **up to ~50** in cord and brain. Book: cord myelin from about month 4; some descending motor tracts not until year 1; tracts myelinate as they start to work. | `[E18.01 · R05iz]` | **⚑ c** (human cord: first myelin at week 10) · ✔ the rest |
| E18.04.01 Cranial nerves (B) · AN62.1, AN58.3, AN59.3 | 12 pairs; I and II are forebrain outgrowths, **III** the only one from the midbrain, the rest from the hindbrain. Motor nuclei inside the brainstem; sensory ganglia outside — from **crest + placodes** (nasal, otic, four epipharyngeal for V, VII, IX, X). Parasympathetic ganglia from crest, carried by **III, VII, IX, X**. **Rhombomeres** (8) set the motor nuclei of IV–VII and IX–XII, apparently guided by the somitomeres below. | `[E18.04]` | ✔ · links D-078 f (crest streams) · note l (all 12 nuclei by week 4) |
| E18.05.01 Sympathetic (B) · AN7.8, AN23.5 | Preganglionic cells in the lateral horn **T1–L2** → ventral root → **white ramus** (only T1–L2) → chain: synapse at that level, climb or descend, or pass through as **splanchnic** nerves (greater T5–9, lesser T10–11, least T12, lumbar) to the **pre-aortic** ganglia. Postganglionic fibres return to **all 31** spinal nerves by **grey rami** (vessels, sweat glands, hair muscles) or go to heart and lungs as cardiopulmonary nerves. All ganglia are crest, migrating in **week 5**. | `[E18.05 · R05jf]` | ✔ · ✔✔ crest ganglion cells beside the aorta at CS14 (week 5) only · ✚ trunks move from beside the aorta to beside the spine (CS15 → CS23) |
| E18.05.03 Parasympathetic (B) · AN7.1 | **Craniosacral:** brainstem (III → ciliary, VII → pterygopalatine + submandibular, IX → otic, X → organs as far as the proximal transverse colon) and **S2–S4** (pelvic splanchnics → distal colon, rectum, bladder, erectile tissue). Postganglionic cells sit **in or near the organ** (enteric ganglia); all crest. Transmitters: noradrenaline (sympathetic) vs acetylcholine (parasympathetic). | `[E18.05]` | ✔ |
| **Things that are walled in** | | | |
| E18.02.06 Ventricles and CSF (B) · AN63.1, AN56.2 | Where the wall makes no neuroblasts it stays one ependymal layer + vascular pia (**tela choroidea**) → **choroid plexus**, making **~400–500 mL CSF a day**; CSF flows lateral → 3rd → aqueduct → 4th → out through its median and lateral apertures → subarachnoid space → **arachnoid granulations** (superior sagittal sinus). | `[E18.02 · R05iw]` | ✔ · ✚ 4th + lateral plexuses at CS18–20 |
| E18.02.07 Meninges (B) · AN56.1 | From **mesoderm + crest**, from weeks 4–5: outer layer → **dura** (lines the venous sinuses; falx cerebri, tentorium, falx cerebelli); inner → **pia–arachnoid** (leptomeninges), split by the subarachnoid space. | `[E18.02]` | ✔ (map row's "pia/arachnoid largely crest" is the head finding, Ch 17 — book Ch 18 says mixed) |
| E18.02.04 Diencephalon and pituitary (B) · AN43.4, AN62.5 | Alar plates → **thalamus** (dorsal; may fuse as the massa intermedia) and **hypothalamus** (ventral; mammillary bodies; sleep, digestion, temperature, emotion) split by the hypothalamic sulcus; roof → 3rd-ventricle plexus + **pineal** (evaginates week 7). Pituitary from **two sources**: **Rathke pouch** (stomodeum ectoderm, ~week 3; cut off by the end of month 2) → anterior lobe + pars tuberalis + pars intermedia; **infundibulum** (diencephalon floor) → stalk + posterior lobe. | `[E18.02]` | ✔ |
| **Things that grow and fold** | | | |
| E18.02.02 Hindbrain (B) · AN64.2, AN60.1, AN58.3 | Medulla: plates splay so sensory sits lateral. Pons: basal-plate marginal layer → fibre bridge; **pontine nuclei** migrate in from the alar plate. **Cerebellum** from the **rhombic lips** (alar) → cerebellar plate → week 12 vermis + hemispheres, then the flocculonodular lobe (oldest part). An **external granular layer** on its surface keeps dividing; granule cells move **in** past Purkinje cells moving **out**; the cortex reaches full size **after birth**; deep nuclei (dentate) settle before birth. | `[E18.02 · R05iy, R05ix, R05iw]` | ✔ · ✚ external germinal layer already at CS21–23; cerebellum 7 % → 13 % of the hindbrain CS20 → CS23 |
| E18.02.03 Midbrain (B) · AN64.2, AN61.1 | Basal: III, IV, Edinger–Westphal; marginal layer → **crus cerebri**. Alar: two ridges split by a groove → **superior (visual)** and **inferior (auditory) colliculi**; alar cells also form the red nucleus and substantia nigra. | `[E18.02 · R05ix]` | ✔ · ✔✔ the two colliculi only (distinguishable at CS23) |
| E18.02.05 Cerebral hemispheres (B) · AN64.2, AN62.4 | Bud from the forebrain wall at the **start of week 5**; the floor bulge (**corpus striatum**) is split by the **internal capsule** into caudate and lentiform (putamen + globus pallidus) — basal ganglia. **Hippocampus** forms above the choroid fissure. Growth forward, up and down → frontal, parietal (dorsal), temporal, occipital lobes; the **insula** is overgrown. **Cortex builds inside-out:** each new wave of neuroblasts passes the earlier ones. Motor cortex rich in pyramidal cells, sensory in granular cells. **Commissures** use the lamina terminalis: anterior first, then hippocampal (fornix), then **corpus callosum** (by week 10); outside it — posterior, habenular, optic chiasm. Olfactory bulbs from crest–placode–telencephalon talk; nasal neurons reach them by **week 7**. | `[E18.02 · R05iw, R05ix]` | ✔ · ✚ cortical plate at CS21 · ✚ anterior commissure at CS23, within the book's "by the end of month 3" (note f) · note e (hippocampus function) |
| **Things that are signalled** | | | |
| E18.01.07 Dorsoventral patterning (D) · AN64.2 | BMP4/7 from overlying ectoderm → roof plate → a cascade (BMPs, activin, dorsalin) **high dorsally**; SHH from notochord → floor plate **high ventrally**. Their ratio sets transcription factors: dorsal **PAX3/7** → sensory; ventral-most **NKX2.2/NKX6.1** → ventral interneurons; just above, **NKX6.1 + PAX6** → motor neurons. | `[E18.01 MR]` | ✔ (*chick/mouse*-based; no human source) |
| E18.03.01 Brain patterning (D) · AN64.2 | Front–back: **HOX** in nested codes for the hindbrain's **8 rhombomeres** (3′ genes earlier, more anterior, more retinoic-acid sensitive; too much RA → rhombomeres take caudal identities); fore/midbrain use other homeobox genes (**LIM1, OTX2**, then OTX1, EMX1/2). Two organizers secrete **FGF8**: the **anterior neural ridge** → FOXG1 (telencephalon, retina) and the **isthmus** → EN1/EN2 + WNT1 (tectum, cerebellum). Dorsal: BMP4/7 → MSX1, LHX2 (cortex). Ventral: **SHH** → NKX2.1 (hypothalamus); SHH works only after cleavage and **cholesterol** attachment. Regions differ in **competence** to answer the same signal. | `[E18.03]` | ✔ (*mouse/chick*-based; links E01.05 shh, ra) |
| **Things that migrate** | | | |
| E18.05.04 Crest tumours (C) | **Pheochromocytoma** — chromaffin-cell tumour → excess adrenaline/noradrenaline (high blood pressure, fast heart, headache); ~10 % outside the adrenal; ~25 % familial, some with **RET** mutations. Neuroblastoma is the map row's second example (not in this chapter's text). | `[E18.05 CC]` | ✔ (rates not checked, §10) |

---

## 4. Clinical correlates — confirmed against Tier 1 (PubMed first)
**Grouped by what went wrong: the tube didn't close · the midline didn't split · the fluid couldn't drain · the brain didn't grow · the crest didn't arrive.** Rates per 10,000 births. Clinical photos: diagrams only (D6).

**Rates, side by side.** ✔✔ = Tier 1 within ~1.5× of the book; a quoted background figure is a ≈ lead, never a ⚑.

| Lesion | Book | Tier 1 | Mark |
|---|---|---|---|
| All NTDs | US ~1 in 1,500 after flour fortification (≈ 6.7); up to 1 in 200 in parts of northern China | **9.1** total (EUROCAT, 28 registries, 12.5 M births, no mandatory fortification, chromosomal cases excluded, R05jg) | ✔ — different populations (US after fortification vs unfortified Europe), so not a ✔✔ · ✚ the EUROCAT figure as context · ✚ India pooled 41–95 per 10,000 (R05x/R05y, heterogeneous) |
| Fortification effect | US fell ~25 % | spina bifida −31 %, anencephaly −16 % (R05bt); held through 2011 (R05v) | ✔✔ |
| Folic acid | 400 µg/day from ≥ 1 month before conception prevents 50–70 % | −72 % recurrence, RR 0.28 (randomised, R05t); first occurrence prevented (R05u) | ✔✔ |
| Anencephaly | 1 in 5,000 (2.0), more often female | **3.3** total (our division of R05jg's 4,162 cases by 12.5 M births); live-birth rate fell with terminations | ✔ — note g (denominators) |
| Spina bifida | not given | **4.6** total (our division of R05jg's 5,776 cases by 12.5 M births) | ✚ |
| Shunted hydrocephalus in myelomeningocele | 80–90 % | **82 %** shunted after birth repair vs 40 % after fetal repair (MOMS, R05br) | ✔✔ |
| Congenital hydrocephalus (no NTD) | not given | **4.65** total (EUROCAT, 4 regions; 48 % terminated; 34 % of live-born died in year 1, R05jh) | ✚ |
| Microcephaly (non-genetic) | not given | **1.53** (EUROCAT, 24 registries; 0.4–4.3 by registry — definitions differ, R05ji) | ✚ |
| Holoprosencephaly | 1 in 15,000 live births (0.67); 1 in 250 early miscarriages | 1.2 total births (California, R05ir) | ✔ — note g (denominators) |
| Encephaloceles | 1 in 12,000 (0.83) | not retrieved (§10) | ✔ |
| Dandy–Walker malformation | not in the book | **0.68** total, **0.27** live births (EUROCAT, 28 registries, 8 M births; half isolated, R05jj) | ✚ (beyond Langman) |
| Hirschsprung disease | no rate; rectum almost always, rectosigmoid 80 %, longer 10–20 % | **1.09** (EUROCAT, R05ha — Ch 15) | ✚ (link, not re-checked) |
| Spina bifida occulta | ~10 % of otherwise normal people, usually S1–S2 | not retrieved | ✔ |

**The tube didn't close (NTDs).**
- **Failure in weeks 3–4 → defects of cord, meninges, bone, muscle and skin.** Spina bifida = an open vertebral arch; **occulta** (skin-covered, cord normal, sometimes a hair tuft, found on X-ray) vs **cystica** — **meningocele** (meninges only) or **myelomeningocele** (neural tissue in the sac) — and **myeloschisis/rachischisis** (folds never rose; flat exposed tissue). Most are lumbosacral; cystica brings deficits below the level but usually normal intelligence. `[E18.01 CC]` ✔ · links D-064 (vertebral arch, ch10)
- **Cranial end → exencephaly → anencephaly** (exposed brain degenerates; brainstem stays; no swallowing → polyhydramnios in the last 2 months; seen on scan as a missing vault); **craniorachischisis** when the gap runs into the spine. `[E18.03 CC]` ✔
- **Hydrocephalus and Chiari II go with myelomeningocele:** as the spine lengthens, a cord held fast at its lower end drags the cerebellum down through the skull's opening, and CSF backs up; treated with a ventriculoperitoneal shunt. `[E18.01 CC · R05br]` ✔✔ (rate) · ✚ fetal repair halves shunting and lessens hindbrain herniation, at the cost of preterm birth (R05br)
- **Prenatal diagnosis:** ultrasound (vertebrae visible by **12 weeks of pregnancy**) + raised **AFP** in maternal serum and amniotic fluid; fetal surgery from **22 weeks of pregnancy**. `[E18.01 CC]` ✔ · ✚ the MOMS trial operated before 26 weeks of pregnancy (R05br) · links D-057 (AFP rises in many leaking defects)
- **Causes:** mostly **multifactorial** (recurrence risk rises after one affected child); hyperthermia, **valproate**, excess vitamin A; prevention — 400 µg/day for all who could conceive (≈ half of pregnancies are unplanned), **4 mg/day** from ≥ 1 month before through the first 3 months after a previous NTD or family history. `[E18.01 CC · R05t, R05u, R05bu]` ✔ · ✔✔ folic acid prevention (R05t, R05u) and valproate (R05bu) only · ✚ VANGL1 (PCP) mutations in NTD families (R05w) · links **D-057** (folic acid, valproate, hyperthermia) — no new ⚑. *The book's line that folic acid "may also" lower autism risk stays ✔ book-only — no Tier 1 read; cards don't use it.*
- **Encephaloceles:** a skull gap, most often the occipital squama; **meningocele** (meninges), **meningoencephalocele** (+ brain), **meningohydroencephalocele** (+ ventricle). Mostly an NTD, many preventable by folic acid. `[E18.03 CC]` ✔

**The midline didn't split.**
- **Holoprosencephaly:** loss of midline → hemispheres fail to separate. Alobar: one ventricle, fused or close eyes, single nasal chamber; milder: partial split, absent olfactory bulbs/corpus callosum; mildest: a single central incisor. Causes: **SHH** mutations, faulty **cholesterol** synthesis (**Smith–Lemli–Opitz**, 7-dehydrocholesterol reductase; ~5 % have HPE), SIX3, TGIF, ZIC2. `[E18.03 CC · R05ir]` ✔ · ✚ 41 % chromosomal, mostly trisomy 13 (R05ir) · links **D-078** (HPE face, Ch 17) — no new ⚑
- **Schizencephaly:** large hemisphere clefts, some with **EMX2** mutations. `[E18.03 CC]` ✔
- **Dandy–Walker malformation** (posterior fossa: cerebellar vermis + 4th ventricle) — not in the book; ~87 % found before birth, half with other anomalies. `[R05jj]` ✚ (More / Tier D only, "beyond Langman")

**The fluid couldn't drain.**
- **Hydrocephalus in newborns** — most often **aqueductal stenosis**: CSF of the lateral and 3rd ventricles can't reach the 4th, so the lateral ventricles swell; open sutures widen and the head grows. `[E18.03 CC · R05jh]` ✔ · ✚ rate and outcome (R05jh)
- **Craniopharyngioma** from Rathke-pouch remnants, usually above the sella: hydrocephalus, pituitary failure (diabetes insipidus, growth), visual loss; a **pharyngeal hypophysis** can stay in the pharynx roof. `[E18.02 CC]` ✔

**The brain didn't grow.**
- **Microcephaly** = a small vault because the **brain** is small; genetic (autosomal recessive) or prenatal insults (infection, drugs, radiation); intellectual disability in over half. `[E18.03 CC · R05ji]` ✔ · ✚ rate, and how much it depends on the 2 vs 3 SD cut-off (R05ji) · links D-057 b (Zika)
- **Toxoplasmosis** → calcifications, hydrocephalus or microcephaly; **many CNS defects are silent** (absent corpus callosum or cerebellum may cause little); the book names **maternal alcohol** as the leading cause of intellectual disability. `[E18.03 CC]` ✔ · links D-057 a (FASD)

**The crest didn't arrive.**
- **Hirschsprung disease** (congenital megacolon) — crest fails to colonize part of the colon/rectum, so no parasympathetic (enteric) ganglia; the aganglionic part stays contracted, the bowel above dilates. **RET** (10q11, a receptor tyrosine kinase; ligand **GDNF** from the mesenchyme) in most familial cases. `[E18.05 CC · R05ha, R05gp]` ✔ (✚ rate, Ch 15)
- **Pheochromocytoma** — §3 (E18.05.04).

---

## 5. ⚑ Watch items → decision D-079 (owner picks)
- **(a) Where the cord ends at birth and in adults.** Book: L3 at birth, L2–L3 in adults. *Human*: MRI of 504 adults — mean **lower third of L1**, range mid-T12 to upper L3, no change with age or sex (R05jc); ultrasound — above L2 in 92 % of term babies (R05je); between T12/L1 and L1/2 in 84 % of infants from term to ~5 months (40–63 postmenstrual weeks, R05jd), while 78 % of **preterm** babies (30–39 weeks) still sit at L2–L4 (R05jd) — so the book's L3 fits a baby born early, and the cord keeps rising a little after birth. Options: (1) default; (2) card: "at birth the cord ends around L1–L2; in adults around L1 (from T12 to L3)", book levels in More. *Recommended (2)* — three imaging series agree, and NMC **AN57.2** asks for this exact fact. Lumbar puncture at L4–L5 is safe on both (no clinical change). The map row `cordpos` now points here.
- **(b) Where microglia come from and when.** Book: from blood-vessel mesenchyme, in the second half of development. *Human* (R05ja): microglia-like cells enter the forebrain from **about week 5** (clock unclear — the abstract writes "postovulatory or gestational weeks"), first through the meninges, choroid plexus and ventricular zone, with a **second, vascular wave** at ~12–13 weeks; *mouse* fate mapping (R05jb): from yolk-sac myeloid progenitors, before E8. Options: (1) default; (2) card: "microglia are immune cells that come from outside the nervous system and enter it from about week 5; a later wave comes in with the blood vessels", book in More. *Recommended (2)* — the book's "vascular" route matches only the second wave.
- **(c) When myelination starts in the cord.** Book: about month 4. *Human* EM (R05iz, 21 cords): first myelinated fibres at **10 weeks after ovulation** (66 mm), ventral marginal layer, oligodendrocytes only. Options: (1) default; (2) card: "the first myelin appears in the cord at about week 10; it spreads from month 4, and some tracts finish after birth", book in More. *Recommended (2)* — one detailed human series; the book's month 4 fits "many fibres look white".
- **(d) Which way the forebrain fusion site runs.** *(Map: fusion belongs to Ch 6's neurulation concept, so this ⚑ sets no Ch 18 `research.txt` mark; Ch 6's row is not re-marked here — X1 to-do.)* Book (p 313): closure starts in the neck region and from a later forebrain site that closes **both** the front end and, running back, meets the neck wave. *Human* (R05l, 98 embryos CS8–13, 61 graphic reconstructions): two sites — α in the **rhombencephalic** region running both ways, and β in the prosencephalic region (beside the chiasmatic plate) running **backwards only**. Both agree on **two sites and two neuropores** (✔✔); only β's direction differs. Options: (1) default; (2) card: "the folds meet first at the hindbrain–neck border and zip both ways; a second meeting point in the forebrain zips backwards", book wording in More. *Recommended (2)* — the human series is graphic-reconstruction based, and the scene (§8) must pick one direction. Tier D may add "no evidence in humans for the four or five sites described in mice" (beyond Langman).
- **(e) Note, not ⚑ — the hippocampus's job.** The book (E18.02) gives olfaction as the hippocampus's primary function; standard neuroanatomy ties it to memory, but the classic paper (Scoville & Milner 1957) has no abstract to mark against. **Cards name the hippocampus by origin and position only and teach no function from this line**; Tier D may add "the adult hippocampus is best known for memory" once a Tier 1 abstract is read (§10).
- **(f) Note, not ⚑ (downgraded by G-Sci) — when the first commissure crosses.** Book: fibres cross the lamina terminalis **by** the end of month 3, the anterior commissure first, the corpus callosum by week 10 — a deadline, not an onset. R05ix (*human*): the anterior commissure appears at **CS23** (end of week 8) — inside that deadline, so no conflict. Tier D may add "the anterior commissure is already there at the end of week 8" (beyond Langman).
- **(g) Note, not ⚑ — rates with different denominators.** Anencephaly: book 2.0 per 10,000 **births** vs EUROCAT 3.3 **total** (with terminations; live-birth rates are far lower) — 1.65×. Holoprosencephaly: book 0.67 per 10,000 **live** births vs R05ir 1.2 **total** births. Each gap is the denominator; cards give the book figure and say "per birth" for anencephaly and "per live birth" for holoprosencephaly (D-043 b pattern).
- **(h) Note — book internal:** the lateral horn runs to **L2 or L3** in E18.01 but **T1–L2** in E18.05 (and its figure). Cards use T1–L2 (also the white-rami rule).
- **(i) Links, not new ⚑:** **D-057** (neural tube defects, folic acid, valproate, hyperthermia, AFP) — Ch 18 repeats Ch 9; the RCT and fortification lines agree. **D-064** (spina bifida occulta as an open arch, cranioschisis; ch10) — no new evidence. **D-078** (holoprosencephaly face; crest streams, note f) — Ch 18's rhombomere → motor-nucleus link adds nothing that conflicts. **D-066** (somites ↔ spinal-nerve segments) — consistent. **D-030** (clocks) — applied throughout.
- **(j) Note — book internal:** the neural plate appears at the **start** of week 3 in the text (E18.00) and in the **middle** of week 3 in the summary (E18.06); cards say "in week 3".
- **(k) Curriculum note:** NMC 2018 Vol I has **one** core CNS development code — **AN64.2** (neural tube, cord, medulla, pons, midbrain, hemispheres, cerebellum) — plus **AN64.3** open NTDs (non-core), **AN63.2** congenital hydrocephalus (non-core), **AN57.2** extent of the cord in child and adult (core — carries ⚑ a), **AN79.3** neurulation, **AN43.4** pituitary. **No code** for autonomic or adrenal development (only AN7.8 sympathetic vs spinal ganglia, non-core; AN23.5 the thoracic chain). AN74.3 (multifactorial inheritance) fits NTDs; AN75.1 (chromosomes) fits HPE's trisomy 13.
- **(l) Book slips (notes):** E18.04 says nuclei for **all 12** cranial nerves exist by week 4; R05iv sees the first nerve fibres only in the hindbrain at CS12 (~day 26–30), and I and II are not nuclei — cards say "the cranial nerves form during weeks 4–6" and avoid "all 12 by week 4" (✔ book-only, not used as a fact). **Linked ⚑s from other chapters do not set a Ch 18 concept's research.txt mark** (same rule as Ch 16–17).

---

## 6. Top student misconceptions (refute in cards and Checks — craft §3.4)
1. **"The basal plate is sensory."** (map row) Ventral **basal = motor**, dorsal **alar = sensory**; the sulcus limitans divides them `[E18.01]` ✔ (✚ the sulcus is visible by CS12, R05iv).
2. **"The spinal cord shrinks after birth / moves up."** It doesn't shrink or climb — the **spine and dura grow faster**, so its end sits at a higher vertebra `[E18.01]` ✔ (levels ⚑ a).
3. **"The cord reaches the sacrum in adults, so a lumbar puncture can hit it."** It ends well above L4 (book: L2–L3; imaging ≈ L1); the needle goes in at L4–L5 among the cauda equina `[E18.01]` ✔ (levels ⚑ a, R05jc).
4. **"Dorsal root ganglia are part of the cord."** They sit **outside** it and come from **neural crest** `[E18.01]` ✔.
5. **"Dorsal and ventral rami are sensory and motor."** **Roots** are pure (dorsal sensory, ventral motor); **rami** are mixed `[E18.01]` ✔.
6. **"Schwann cells and oligodendrocytes are the same cell in two places."** Schwann cells are **crest**, one axon each, in nerves; oligodendrocytes are **tube**-made, many axons each, in cord and brain `[E18.01 · R05iz]` ✔ · ✔✔ the oligodendrocyte clause (the only myelin makers in the human cord).
7. **"Microglia are made by the neural tube like other glia."** They come from **outside** — immune cells that move in `[E18.01 · R05ja]` ⚑ b (the book says vascular mesenchyme; both say not the tube).
8. **"The brain has five vesicles from the start."** **Three first**, five by week 5 `[E18.00]` ✔ (✚ the three regions are already marked by CS11, R05iu).
9. **"The cerebellum comes from the basal plate, so it's motor output."** From the **alar** plate (rhombic lips); the pons gets its bridge from basal-plate fibres `[E18.02]` ✔.
10. **"The cerebral cortex fills outside-in."** It fills **inside-out**: later neurons migrate **past** earlier ones `[E18.02]` ✔.
11. **"The whole pituitary comes from the brain."** (map row) The **anterior lobe** is Rathke pouch (mouth ectoderm); only the posterior lobe is brain `[E18.02]` ✔.
12. **"The midbrain splits into two vesicles like the others."** It **stays one** `[E18.00, E18.06]` ✔.
13. **"Hydrocephalus means too much CSF is made."** Usually it **can't drain** — most newborn cases are a narrow aqueduct `[E18.03 CC]` ✔.
14. **"Microcephaly is a skull problem."** The skull is small because the **brain** didn't grow `[E18.03 CC]` ✔.
15. **"Anencephaly means no brain at all."** The **brainstem** remains; the exposed forebrain degenerates `[E18.03 CC]` ✔.
16. **"Spina bifida always means paralysis."** **Occulta** usually causes nothing (~10 % have it); cystica's deficits depend on level and content `[E18.01 CC]` ✔.
17. **"Folic acid works if started once pregnancy is confirmed."** The tube closes by ~day 28 — start **before** conception `[E18.01 CC · R05t]` ✔✔ (links Ch 6 misconception 10).
18. **"The whole adrenal comes from one layer."** (map row) **Cortex = mesoderm, medulla = crest** `[E18.05]` ✔.
19. **"Sympathetic nerves only come from T1–L2, so only those spinal nerves carry them."** Only T1–L2 have **white** rami; **every** spinal nerve gets a **grey** ramus back `[E18.05]` ✔.
20. **"Parasympathetic ganglia sit in a chain like the sympathetic."** They sit **in or near** the organ (vagal, pelvic) or as four head ganglia `[E18.05]` ✔.
21. **"Hirschsprung disease is a muscle problem."** It is **missing nerve cells** — crest never arrived (links Ch 15 misconception 17) `[E18.05 CC]` ✔.

---

## 7. Curriculum map (R30 — NMC AN table; source note below)
**Source note:** read from **NMC *Competency Based UG Curriculum Vol I*** (`UG-Curriculum-Vol-I.pdf`, staged from Studio home `references\nmc\`, 22 Nov 2026). Vol I is the **2018** text; the 2024 MGMUHS reprint is not in `references\`, so **2024 wording is unchecked** (§10).

**Where Ch 18 sits (the prompt's guesses, checked):**
- **AN64.2** — development of neural tube, spinal cord, medulla, pons, midbrain, cerebral hemisphere and cerebellum (core, KH) ✔ — **the CNS development code**.
- **AN64.3** — types of open NTDs and their embryological basis (**non-core**) ✔ · **AN79.3** neurulation (core) ✔ · **AN79.5** NTDs (core, Ch 9 row).
- **AN57** spinal cord — AN57.1 external features · **AN57.2 extent in child and adult with clinical implication (core)** — ⚑ a · AN57.3–57.5.
- **AN58** medulla (AN58.3 cranial-nerve nuclei by functional group) · **AN59** pons (AN59.3) · **AN60** cerebellum (AN60.1) · **AN61** midbrain (AN61.1) · **AN62** cranial-nerve nuclei + hemispheres (AN62.1 nuclei by component; AN62.4 basal ganglia + limbic lobe; AN62.5 thalamus/hypothalamus).
- **AN63** ventricles — AN63.1 (core) · **AN63.2 congenital hydrocephalus (non-core)**.
- **AN56** meninges + CSF — AN56.1, AN56.2 (core).
- **AN7** introduction — AN7.1 plan of CNS/PNS/ANS · AN7.4 typical spinal nerve · AN7.8 sympathetic vs spinal ganglia (non-core) · **AN23.5** thoracic sympathetic chain.
- **AN43.4** — includes the **pituitary** (development + anomalies) ✔.
- **AN74–AN75** genetics — AN74.3 multifactorial (NTDs) · AN75.1 chromosomal (HPE, trisomy 13) — hooks only.
- **Not in Vol I:** adrenal or autonomic **development**; Dandy–Walker; Chiari; microcephaly. Hirschsprung appears only under physiology (PY, Ch 15 note).

**Per concept (→ `tools/map/research.txt`):**
- E18.01.01 → AN64.2, AN79.3 · E18.01.02 → AN64.2 · E18.01.03 → AN7.4, AN64.2 · E18.01.04 → AN64.2 · E18.01.05 → AN57.2 · E18.01.06 → AN64.3, AN79.5, AN50.4 · E18.01.07 → AN64.2
- E18.02.01 → AN64.2, AN79.3 · E18.02.02 → AN64.2, AN60.1, AN58.3 · E18.02.03 → AN64.2, AN61.1 · E18.02.04 → AN43.4, AN62.5 · E18.02.05 → AN64.2, AN62.4 · E18.02.06 → AN63.1, AN56.2 · E18.02.07 → AN56.1 · E18.02.08 → AN63.2, AN64.3, AN79.5
- E18.03.01 → AN64.2 · E18.04.01 → AN62.1, AN58.3, AN59.3 · E18.05.01 → AN7.8, AN23.5 · E18.05.02 → (none) · E18.05.03 → AN7.1 · E18.05.04 → (none)

---

## 8. Scene note — visual references (look, don't copy — RULES G5)
- **Closing the tube (CS10 → CS12):** dorsal view, folds meeting first at the hindbrain–neck border and zipping both ways, a second forebrain site zipping back (R05l; the book has it run both ways — ⚑ d, so the shot follows the owner's pick); two open ends (neuropores) close — rostral at CS11, caudal at CS12. B2 "≈ day 22–28 · CS10–12". Never draw the mouse's extra sites (⚑ d).
- **Layers and plates (cross-section, D9):** ventricular → mantle → marginal; then alar/basal swelling with the sulcus limitans as a groove; colour by role (pattern + label): motor (ventral) vs sensory (dorsal) — the exam cross-section to end on.
- **Spinal nerve assembly:** basal-plate axons out → crest ganglion beside the cord sends two processes → trunk → dorsal and ventral rami; label roots "pure", rami "mixed".
- **Cord vs spine (month 3 → adult):** side-by-side columns growing at two rates; the cord's tip stays while the vertebra numbers slide past it; label the book level "L3 at birth" with a "⚑ newer imaging: higher" tag while ⚑ a is open (B7); filum and cauda equina appear as the gap opens.
- **Three → five vesicles + flexures (CS13 → CS16):** a straight tube that balloons and bends — cervical, cephalic, then pontine; ventricles drawn as a lit-up inner cast (R05iy, Kyoto — look only, licence per dataset).
- **Hemispheres (week 5 → birth):** bud → C-shaped growth over the diencephalon dragging the ventricle, caudate and hippocampus into a C; insula sinks; gyri appear last. Inside-out cortex as waves of dots overtaking each other.
- **Cerebellum:** rhombic lips meet → plate → vermis + hemispheres; the external granular layer as a surface sheet raining cells inward past outward-moving Purkinje cells.
- **Pituitary:** two arrows meeting — mouth roof up, brain floor down — colour the two lobes by origin (ectoderm vs neural).
- **Sympathetic chain (CS14 → CS23):** crest beads beside the aorta that drift behind it to beside the spine (R05jf); white rami only on T1–L2, grey rami on every nerve.
- **Adrenal:** cortex rings (mesoderm) invaded by crest cords (medulla) from the medial side.
- **Never from the book:** its tube, layer, neuroblast, glia, nerve, cord-level, vesicle, flexure, cerebellum, diencephalon, pituitary, hemisphere, commissure, rhombomere, organizer, sympathetic and parasympathetic figures and its three tables are copyrighted; every one is redrawn by us (D6, visual-style §16). Its patient photographs (spina bifida, holoprosencephaly, encephalocele, anencephaly, hydrocephalus, microcephaly) are never shown — diagrams only.

## 9. Why learners struggle here (M05)
- **One rule hides under everything — ventral motor, dorsal sensory.** Teach it once in the cord; then show the brainstem as the same plan "opened like a book" before any nucleus names.
- **Five vesicles, five names, five ventricles** — one coloured cast of the lumen carries them all.
- **The nuclei table** (6 columns × 3 levels) — teach by **job**, as §3 does, then attach nerves.
- **Cord level** — learners picture the cord rising; show two rulers growing at different speeds (misconception 2).
- **Autonomic wiring** — white vs grey rami is a counting puzzle: white only where the lateral horn is (T1–L2), grey everywhere.
- **Clocks:** NTD scan and surgery ages are weeks of pregnancy; the rest are after fertilization; one microglia source mixes clocks (⚑ b).

## 10. X1 to-do — done 22 Nov 2026, with open items
- Done: real locators + sub-locators; four page spills, E18.04's overlapping pages, one misfiled box and two untitled boxes + one cut title named (→ I1); staging from human specimens (R06/R08, R05l, R05iu–R05ix by Carnegie stage; R05iy Kyoto by CS; R05iz ovulation age; R05jf weeks post-fertilisation; R05ja clock unclear; infant conus after birth); Tier A for 4 concepts (layers, alar/basal plates, vesicles and flexures, adrenal) + cord position; Tier B–D with the brainstem nuclei by job; clinical rows in 5 mechanism groups with rates per 10,000; 21 misconceptions; AN map from NMC Vol I; 16 sources **R05iu–R05jj** (R05l re-used). G-Sci fresh-eyes review: **pass with fixes, 7 MUST + 11 SHOULD, all applied** — the forebrain fusion direction became ⚑ d, the commissure timing went from ⚑ to note f, the brainstem table was re-ordered, and several ✔✔ were narrowed to the clause the abstract supports.
- **Rates not retrieved:** encephaloceles (book 1 in 12,000), spina bifida occulta (~10 %), pheochromocytoma (10 % extra-adrenal, 25 % familial), schizencephaly, Chiari II as a separate rate, anencephaly sex ratio.
- **Hippocampus function** (note e): a Tier 1 abstract (memory) before Tier D says it.
- **Human corpus callosum timing** (book week 10) — no human source with a stated clock retrieved.
- **Human cerebellar timeline after week 12** (EGL disappearance, foliation) and **human gyrification ages** — fetal MRI series next.
- **R05ja full text** for its clock (⚑ b); **R05iz full text** for the lumbar cord (⚑ c covers the cervical cord only).
- **R01 3D Atlas** CS13–23 brain models and **R04 Kyoto** brain MRIs (behind R05iy) before the vesicle and ventricle scenes (look only; R01 NC-ND, R04 licence per dataset); **R03 HDBR** CS12–22 sections for the cord layers scene (reference only).
- **Neuroblastoma** (map row cresttum) — not in this chapter's text; check where 14e mentions it before a card names it.
- **Ch 6 map row `neurul`** (E06.01.0x): consider its mark in light of ⚑ d at the next Ch 6 touch.
- **2024 wording** of AN64.2/64.3 and AN57.2 (MGMUHS reprint): not in `references\`.
