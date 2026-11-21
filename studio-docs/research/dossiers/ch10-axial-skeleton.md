# Research dossier — Ch 10 · The axial skeleton (for C-step cards + episodes)

*(Purpose: cited, marked facts, staging, misconceptions and clinical correlates for Ch 10, the first chapter of Part 2, systems-based embryology. Cards draft from this file, and it sets the Part 2 dossier pattern. Updated: 21 Nov 2026 · Bio · Research · X1 Ch 10 · by Aaditya. Own words only; no book sentences, figures or tables (RULES §G). Pattern: `ch09-birth-defects-prenatal-dx.md`.)*

**How to read a line:** fact in our words · `[book section · registry source]` · mark (RULES B6–B7): **✔✔** book + Tier 1 agree · **✔** book only · **⚑** book vs Tier 1 disagree (D-entry) · **✚** beyond the book (More / Tier D only, "beyond Langman") · **≈** blocks final. **Species tag:** a Tier 1 line from chick, mouse or axolotl says so. Those lines can confirm a mechanism, but they never give a human day or number.

**Citation check (X1.09.q2), read before you cite anything above R05z:** checked 21 Nov 2026. `tools/card-check/citations.py` now matches `R\d\d[a-z]{0,2}` in `SRC_RE` and in `parse_registry` (the C2 chat fixed it; X1.09.q2 answered). So the two-letter ids used below, **R05ce–R05dc**, parse and validate, and `sources.json` is rebuilt in this commit with them. Nothing in this dossier depends on a dropped id.

**Ages — three clocks in one chapter.** Embryo events (somite, sclerotome, resegmentation, chondrification) are **days or weeks after fertilization** (D-030). The ossicle and fetal-skull months are fetal months after fertilization. **Fontanelle, suture and spinal-curve ages are after birth.** The spina bifida scan in E10.02's box says "26-week-old fetus" without naming its clock (likely gestational weeks) ≈. Every card number is labelled with its clock. On screen the embryology clock wins (D-030), and postnatal ages say "after birth".

**Section locators (checked against the PDF, 21 Nov 2026; printed page = PDF page − 19):**
- **E10.00** p 147 (the opener shares the page with E10.01)
- **E10.01 pp 147–156:**
  - p 147: somite → sclerotome → mesenchyme, and the three sources of skeletal mesenchyme
  - p 148: the two ossification modes (spicules figure, endochondral figure)
  - p 149: skull sources figure, membranous neurocranium, newborn skull
  - p 150: fontanelles, chondrocranium
  - p 151: viscerocranium, face proportions
  - **CC "Craniofacial defects and skeletal dysplasias" pp 151–156:** crest vulnerability, cranioschisis, meningocele, craniosynostosis defined p 151; mechanisms, FGF/FGFR, suture shapes, causes, achondroplasia, thanatophoric, hypochondroplasia, cleidocranial p 152; **gene table p 153**; figures pp 154–155; **acromegaly and microcephaly p 156**
- **E10.02 pp 156–158:** the vertebra p 156; resegmentation, disc, arteries and nerves, spinal curves p 157; **CC "Vertebral defects" pp 157–158**, with spina bifida, the AFP test and the lemon-sign scan on **p 158**
- **E10.03 pp 158–159:** ribs and sternum p 158; **CC "Rib defects / Defects of the sternum" pp 158–159**
- **E10.04** Summary p 159 · **E10.05** Problems p 159

**I1 gaps** (tree.json) → I1 to-do:
- **E10.01** is recorded as pp 147–155, but its CC box runs onto **p 156** (acromegaly, microcephaly), which I1 files under E10.02.
- **E10.02** is recorded as pp 156–157, but its CC box ends on **p 158** (spina bifida cystica, AFP, lemon sign), filed under E10.03. This is the "E10.03 holds spina bifida/Chiari terms" note in concept-map.md, now explained.
- **E10.03** is recorded as p 158, but its sternum box ends on **p 159**, which it shares with the Summary.
- Same shape of gap as E09.01/E09.02 and Ch 8: the I1 page ranges stop at the last heading page and miss boxes that spill over.

---

## 1. Staging & scale — sclerotome to cartilage column (RULES B2)
Ch 10 gives two embryo times: sclerotome mesenchyme at the **end of week 4**, and cells migrating around the cord in **week 4**. Everything else is fetal or after birth. Unlike Ch 8–9, the **Tier 1 sources for this chapter include human specimen data**: serial sections, graphic reconstructions, 3D reconstruction and MRI of staged embryos. The book itself gives none. So the stages below come from those sources (R08 classic stage ages, D-030), not from the book.

| When (after fertilization) | Carnegie | What happens `[section · source]` | Size cue | Mark |
|---|---|---|---|---|
| Day ~22–23 → day ~32 (week 4) | CS10 → CS13 | Sclerotome appears in the earliest somites from CS10. By the end of week 4 the ventromedial somite wall has broken up into loose mesenchyme that wraps the notochord and neural tube `[E10.00, E10.02 · R05m]` | 4–12 somites at CS10 (R05m) | ✔✔ (the book's "end of week 4" is when the sclerotome is mesenchyme along most of the axis; it *starts* earlier, at CS10, in the cranial somites) |
| Weeks 5–6 (7–13 mm CRL) | ~CS15–CS17 (7 mm is the CS14/15 edge) | **Resegmentation seen in human embryos:** each forming vertebral body takes the caudal half of one sclerotome and the cranial half of the next; the disc forms at the old mid-sclerotome `[E10.02 · R05cj]` | 7–13 mm CRL (R05cj) | ✔✔ (human histology, 7 embryos) |
| Days ~42–48 | CS17–CS18 | **Vertebral column starts to chondrify**; the craniovertebral junction is chondrifying by day 45 (CS18) `[· R05ce, R05cf]` | — | ✚ (the book gives no stage) |
| Days ~50–53 | CS20–CS21 | Cartilaginous anterior arch of the atlas appears `[· R05cf]` | — | ✚ |
| End of week 8 (~day 56) | CS23 | **33–34 cartilaginous vertebrae**, column 20–33 mm long, in flexion; a typical vertebra is a U-shaped cartilage: centrum + two neural processes, **no spinous process**, laminae joined only by fibrous tissue — the arch is **normally open at the back** at this stage (it resembles total rachischisis; dorsal growth varies). Sternal bands almost fully joined `[· R05cg, R05ci]` | column 20–33 mm (R05cg) | ✚ |
| Early fetal period (week 9 on) | — | Laminae unite, **ossification begins**, joint cavities appear `[· R05cg]`; the neural arches of C1–C2 are still open at day 77 `[· R05cf]` | — | ✚ |
| Month 4 (fetal) | — | The ear ossicles start to ossify; the book calls them the first bones to become *fully* ossified `[E10.01]` | — | ✔ |
| After birth: 1–3 months, ~18 months, 5–7 years, adult | — | Posterior fontanelle closes, then the anterior; the vault holds nearly all of its capacity by 5–7 years; some sutures stay open into adulthood `[E10.01]` | — | anterior ✔✔ (R05cx) · posterior **⚑ D-064 a** (the book gives two times) |
| As the vertebrae form (embryo / fetus) | — | **Primary curves** (thoracic, sacral) are set `[E10.02]` | — | ✔ |
| After birth | — | **Secondary curves**: cervical with head control, lumbar with walking `[E10.02]` | — | ✔ |

**Scene note:** the hero scene is **"Shift by half"**. A dorsal, see-through view of 3 somite pairs (sclerotome `--g-meso`, with the caudal halves in a second pattern) beside the notochord and neural tube (`--g-ecto`). The halves slide and join into vertebral bodies; the myotome (also `--g-meso`, but labelled, B3) stays put and ends up **bridging** the disc; then the intersegmental artery is shown running over the body and the spinal nerve leaving at the disc.
- Day and size are stamped: "weeks 5–6 · ~7–13 mm CRL".
- It ends on the transverse section with the vertebra as a **U-shaped cartilage open at the back** (CS23, R05cg) — D9 shape-before-names. The closing label is "normal at 8 weeks — the arch closes in the fetal period" (misconception 5).
- The skull scene is a colour-by-source map: crest `--g-crest`, paraxial mesoderm `--g-meso`, lateral plate `--g-ctx` with its label. It shows membranous vault vs cartilaginous base, and the frontal/parietal crest–mesoderm boundary at the coronal suture (R05cp).
- **R01 check before building:** confirm that the 3D Atlas models show cartilage or skeleton at CS17–23 (look only, NC-ND). This is not yet checked (§10).

## 2. Tier A facts — cited and marked
### E10.01.01 Two ways to make bone · AN2.2, AN2.4, AN26.6
- The skeleton comes from mesenchyme of three origins: **paraxial mesoderm** (somites and, in the head, somitomeres), the **parietal layer of lateral plate mesoderm** (girdles, limbs, sternum) and **neural crest** (face and part of the skull). `[E10.00, E10.04]` **✔**
- Mesenchyme cells migrate and can become fibroblasts, chondroblasts or osteoblasts. `[E10.00]` **✔**
- **Intramembranous ossification:** in the flat bones of the vault, mesenchyme in the dermis turns **straight into bone**, with no cartilage stage. Needle-like spicules radiate out from primary ossification centres. `[E10.00, E10.01]` **✔**
- **Endochondral ossification:** in most bones (skull base, limbs; the vertebrae too, from precartilaginous bodies — E10.02), mesenchyme first makes a **hyaline cartilage model**. Blood vessels invade its centre and bring osteoblasts. Chondrocytes towards the shaft enlarge, mineralise their matrix and die, and osteoblasts lay bone on it. Later, secondary centres form in the ends, and **growth plates** of dividing chondrocytes keep the bone growing. `[E10.00, E10.02, E10.04]` **✔**
- Membrane bones grow by adding bone on the outer surface while osteoclasts remove it from the inside. `[E10.01]` **✔**
- Which route a bone takes decides which diseases hit it: the **FGFR3** dysplasias act on endochondral growth, so long bones and the skull base are short while the membranous vault is spared and looks large. `[E10.01 CC · R05cv]` **✔✔** (R05cv: > 95 % of achondroplasia carries the same FGFR3 point mutation, a gain of function that acts mainly on the cartilage growth plate)

### E10.02.01 Vertebrae from sclerotomes · AN79.4, AN50.1
- Vertebrae come from the **sclerotome**, the ventromedial part of each somite. During week 4 its cells move around the neural tube and notochord and meet cells from the somite on the other side. `[E10.02 · R05m]` **✔✔** (R05m, human serial sections: sclerotome from CS10)
- **Resegmentation:** each sclerotome's caudal half grows into and joins the cranial half of the sclerotome below it, so **one vertebra is built from parts of two neighbouring somites**. `[E10.02, E10.04 · R05cj, R05ck, R05cl]` **✔✔**
  - R05cj: seen directly in 7 human embryos of 7–13 mm CRL, weeks 5–6.
  - R05ck and R05cl (chick–quail grafts, *chick*): one somite's cells end up in the adjacent halves of two vertebrae and the disc between them. Vertebral body, neural arch, processes and rib are all two-somite structures; only the rib head is one-somite.
  - ✚ refinements in §5 c.
- The cells at the middle of the original sclerotome do not multiply. They fill the gap between two cartilage vertebral bodies and help make the **intervertebral disc**. `[E10.02]` **✔** (✚ *mouse*: the disc forms from the caudal-sclerotome domain, but the gene boundary and the resegmentation boundary do not line up exactly, and the cervical region differs — R05cn)
- Because of the shift, each **myotome bridges a disc** and attaches to two vertebrae, which is what lets the muscles move the spine. `[E10.02 · R05cl]` **✔✔** (R05cl, *chick*: intersegmental muscles and their skeletal attachments come from the same somite)
- The shift also moves the **intersegmental arteries**: they start out between sclerotomes and end up over the middle of the vertebral bodies. **Spinal nerves** end up beside the discs and leave through the intervertebral foramina. `[E10.02 · R05cj]` **✔✔** (R05cj: the definitive vertebral body forms in close relation to the intersegmental artery)
- **HOX genes** pattern the shapes of the different vertebrae (cervical, thoracic, lumbar and so on). `[E10.02]` **✔**
- A typical vertebra has a vertebral arch around the vertebral foramen, a body, transverse processes and usually a spinous process. `[E10.02]` **✔** (✚ at the end of week 8 there is not yet a spinous process and the arch is normally still open at the back — R05cg)
- The notochord disappears from the vertebral bodies but persists and enlarges between them as the **nucleus pulposus**, later ringed by the circular fibres of the **annulus fibrosus**. `[E10.02 · R05co]` **✔✔** (R05co, *mouse* Noto-cre lineage tracing: nucleus pulposus cells descend from the notochord)
- **Primary curves** (thoracic, sacral) form with the vertebrae; **secondary curves** follow after birth (cervical when the head is held up, lumbar when walking starts). `[E10.02]` **✔**

## 3. Tier B–D facts (cards later; marked now)
| Concept | Fact (our words) | Cite | Mark |
|---|---|---|---|
| E10.01.02 Neurocranium (B) · AN26.1, AN26.3, AN26.6 | Two parts: the **membranous neurocranium** (the flat bones of the vault) and the **chondrocranium** (the base). The vault comes from **neural crest and paraxial mesoderm**, ossifies in membrane and grows by apposition. The chondrocranium starts as **separate cartilages** that fuse and ossify endochondrally. Its landmark is the **rostral end of the notochord at the pituitary (sella turcica)**: in front of it, the **prechordal** cartilages are **neural crest**; behind it, the **chordal** cartilages come from **occipital sclerotomes** (paraxial mesoderm). | `[E10.01, E10.04 · R05cp]` | ✔ · ✔✔ for the vault boundary (R05cp, *mouse* Wnt1-Cre lineage tracing: the frontal bone is crest-derived and the parietal mesodermal, so the coronal suture sits on a crest–mesoderm interface; a tongue of crest lies between the two parietals, where the sagittal suture forms) |
| E10.01.03 Viscerocranium (B) · AN26.4 | The face bones come mainly from **pharyngeal arches 1 and 2** (Ch 17). The **maxillary process** of arch 1 gives the maxilla, zygomatic bone and part of the temporal bone. The **mandibular process** holds **Meckel cartilage**: the mandible forms *around* it by **intramembranous** ossification, and Meckel cartilage vanishes except for the **sphenomandibular ligament**. The dorsal tips of arch 1 and arch 2 give the **incus, malleus and stapes**. The ossicles start ossifying in month 4, the first bones to be **fully** ossified. Facial mesenchyme, including the nasal and lacrimal bones, is **neural crest**. The newborn face is small for its skull because there are almost no paranasal sinuses and the jaws are small; teeth and sinuses change that. | `[E10.01]` | ✔ |
| E10.01.04 Sutures and fontanelles (B) · AN26.2 | At birth the vault bones are separated by **sutures** of connective tissue. Where more than two bones meet, the gaps are wide **fontanelles**; the largest is the **anterior** fontanelle, where the two frontals meet the two parietals. They let the bones **overlap (mould) at birth**; soon after, the bones return and the skull looks large and round, with the vault big for the small face. Open sutures let the vault keep growing with the brain. A 5–7-year-old has nearly all of its cranial capacity, and some sutures stay open into adulthood. Feeling the anterior fontanelle in the first years tells a clinician whether ossification and intracranial pressure are normal. | `[E10.01]` | ✔ · anterior by ~18 months **✔✔** (text and figure legend agree — "middle of the second year"; R05cx, single-centre CT, 464 scans: closed in 16 % at 10 months, 53 % at 16, 88 % at 20, already in 3–5 % at 5–6 months) · posterior **⚑ D-064 a**: the book gives 1–2 months in the text and ~3 months in the figure legend; R05cy (CT, NZ) — posterior open in no NZ European infant scanned, and in 17 % of Māori/Pasifika under 1 month and 7 % at 1–3 months |
| E10.01.05 Craniosynostosis and skull defects (C) · AN79.5 (NTD part; no competency names craniosynostosis) | **Cranioschisis**: the vault fails to form because the cranial neuropore stays open, and the brain, exposed to amniotic fluid, degenerates (**anencephaly**, lethal). Smaller skull gaps let meninges (**cranial meningocele**) or brain (**meningoencephalocele**) herniate; these can be repaired, and the deficit depends on how much brain is damaged. **Craniosynostosis** = early closure of one or more sutures, a feature of > 100 genetic syndromes. Suture growth is poorly understood but sits at **crest–mesoderm boundaries**; ephrin-B1 (EFNB1, a cell-repelling signal) keeps sutures open, and its loss gives **craniofrontonasal syndrome** (coronal synostosis + wide-set eyes). MSX2 and TWIST1 control crest proliferation in the frontal bones (**Boston-type** craniosynostosis; **Saethre–Chotzen**: coronal synostosis + polydactyly). FGFR1 and FGFR2 drive cell division and bone differentiation; mutations, often a single amino-acid change, give **Pfeiffer, Apert, Jackson–Weiss and Crouzon**. **Shape tells the suture:** sagittal → long narrow skull with frontal and occipital bossing (**scaphocephaly**); both coronals → short tall skull (**brachycephaly**); one coronal → asymmetric flattening (**plagiocephaly**). Causes are mostly genetic; others are vitamin D deficiency, teratogens (phenytoin, retinoids, valproate, methotrexate, cyclophosphamide) and fetal constraint (oligohydramnios, multiple pregnancy). | `[E10.01 CC, E10.01 gene table p 153, E10.04 · R05cp, R05cq, R05cr, R05cs]` | ✔ · ✔✔ crest–mesoderm suture boundary (R05cp, *mouse*) · **⚑ D-064 b** (how common): book 1 in 2,500 births, sagittal 57 %, coronal 20–25 %. R05cq (Atlanta 1989–2003): 4.3 per 10,000 births, i.e. ~1 in 2,300, which agrees. R05cs (Finland 1987–2010): 6.0 per 10,000 live births, rising from 5.0 to 7.5; sagittal 3.9 per 10,000, ~65 % of cases. R05cr (Netherlands 2008–2013): **7.2 per 10,000 (~1 in 1,400)**, sagittal 44 %, a significant yearly rise. So the book's figure is the older registry rate |
| E10.01.06 Skeletal dysplasias (C) · AN74.4 | Crest cells leaving the neuroectoderm are a common teratogen target, so craniofacial defects are common (Ch 17). **Achondroplasia** is the commonest skeletal dysplasia, mainly of the long bones, with a large skull, small midface, short fingers and exaggerated spinal curves; it is autosomal dominant, and most cases are new mutations. **Thanatophoric dysplasia** is the commonest lethal neonatal dysplasia: type I has short curved femurs, with or without a cloverleaf skull; type II has straighter, longer femurs and a severe **cloverleaf skull** (kleeblattschädel: all sutures close early and the brain bulges through the anterior and sphenoid fontanelles). **Hypochondroplasia** is a milder achondroplasia. All three are **FGFR3** mutations that disturb endochondral bone, so long bones and the skull base suffer. **Cleidocranial dysostosis**: late-closing fontanelles, poorly mineralised sutures with frontal, parietal and occipital bossing, and small or absent clavicles. **Acromegaly**: the book attributes it to congenital hyperpituitarism with excess growth hormone, enlarging face, hands and feet, sometimes as gigantism. **Microcephaly**: the brain fails to grow, so the skull does not expand; often significant intellectual disability; prenatal alcohol is one cause. | `[E10.01 CC, E10.01 gene table p 153 · R05ct, R05cu, R05cv, R05db, R05dc]` | ✔ · ✔✔ achondroplasia 1 in 20,000 (R05ct, meta-analysis of 52 studies: 4.6 per 100,000 worldwide ≈ 1 in 21,700, higher in North Africa and the Middle East; R05cu, US registries: 1 in 16,670–27,780) · ✔✔ new mutations (book 90 %; R05cv > 80 %; R05cu: de novo risk rises with paternal age, aOR 2.8–5.0 from 25 years up) · ✔✔ thanatophoric 1 in 40,000 (R05cu: 1 in 33,330–47,620) · ✚ cleidocranial dysostosis is caused by **RUNX2** variants (R05db, 453 patients); the book names no gene · **⚑ D-064 d** (acromegaly): R05dc — a GH-secreting pituitary adenoma causes **acromegaly in adults and gigantism in children**; it is an acquired tumour, not a congenital condition |
| E10.02.02 Intervertebral disc (B) · AN79.5, AN50.2 | Disc = **nucleus pulposus** (notochord remnant) inside the **annulus fibrosus** (circular fibres from sclerotome mesenchyme at the old mid-segment). | `[E10.02 · R05co]` | ✔✔ (R05co, *mouse*: nucleus pulposus cells are notochord-descended). ✚ the notochord runs up through the centra and the dens into the skull base at the end of week 8 (R05ch) |
| E10.02.03 Vertebral defects (C) · AN50.4, AN53.4, AN79.5 | Making and reshuffling segments is complicated, so errors are fairly common: a lopsided fusion of neighbouring vertebrae, or a **hemivertebra**, gives **scoliosis**. The number of vertebrae often differs from normal. **Klippel–Feil**: fused cervical vertebrae, so reduced movement and a short neck. **Cleft vertebra (spina bifida)**: the arches fail to fuse. In **spina bifida occulta** only the bony arch is open, under skin, with no deficit. In **spina bifida cystica** the neural tube itself fails to close, the arches do not form and neural tissue is exposed; the deficit depends on level and extent. Cystica affects ~1 in 2,500 births, is often preventable with folic acid before conception (Ch 6), shows on ultrasound, and raises amniotic-fluid AFP when neural tissue is open (Ch 9). In some cases the skull scan shows a **"lemon sign"** because the brain is pulled down (Arnold–Chiari, Ch 18). | `[E10.02 CC · R05cj, R05cz, R05cg]` | ✔ · ✔✔ two kinds of vertebral-body defect, failure of formation (hemivertebra) and failure of segmentation (fusion), already visible in a 13 mm embryo and a 70 mm fetus (R05cj) · ✚ Klippel–Feil looks far commoner than the often-quoted 1 in 40,000 (a figure not in Langman): 17 of 2,917 neck CTs at one US level I trauma emergency department, ~1 in 172, all single-level fusions (Samartzis type I) at C5–C6 or C2–C3 — a broader case definition than the clinical syndrome (R05cz) · ✚ the vertebral arch is normally still open at 8 weeks (R05cg) — an occulta-type defect is a normal fetal closure that fails to happen. For spina bifida rates and folic acid see the Ch 6 dossier (R05t, R05u, R05v) |
| E10.03.01 Ribs and sternum (B) · AN21.1, AN21.2 | The **bony rib** comes from sclerotome cells that **stay in paraxial mesoderm** and grow out from the **costal processes** of the thoracic vertebrae. The **costal cartilages** come from sclerotome cells that **cross the lateral somitic frontier** into lateral plate mesoderm (Ch 11). The **sternum** forms separately in the **parietal layer of lateral plate mesoderm** of the ventral body wall: **two sternal bands**, one each side of the midline, fuse into cartilage models of the manubrium, the sternebrae and the xiphoid. | `[E10.03, E10.04 · R05cl, R05ci]` | ✔ · ✔✔ rib from two neighbouring somites except the costal head (R05cl, *chick*) · ✚ the sternal bands are almost fully united by the end of week 8 (R05ci) |
| E10.03.02 Rib and sternum defects (D) · AN35.9 | **Extra ribs**, usually lumbar or cervical. **Cervical ribs** occur in ~1 % of people, usually on C7, and can press on the brachial plexus or subclavian artery, giving numbness in the arm. **Cleft sternum** is very rare: the bands fail to meet in the midline, so the chest organs lie under skin and soft tissue alone. Small ossification centres and early fusion of sternal segments are seen especially in babies with heart defects (20–50 %); **multiple manubrial centres** in 6–20 % of children, more so in Down syndrome. **Pectus excavatum** = a sunken sternum; **pectus carinatum** = a keel-like forward sternum with a laterally flattened chest; both may come from abnormal body-wall closure or from abnormal costal cartilage and sternum formation. | `[E10.03 CC · R05cw, R05ci, R05da]` | ✔ · ✔✔ cervical rib ~1 % (R05cw, 141 studies, 77,924 people: 1.1 % in the healthy, 29.5 % in thoracic outlet syndrome; more than half unilateral) · ✚ fetal C7 costal elements often have an ossific centre, yet adult cervical ribs are uncommon (R05ci) · ✔✔ cleft sternum very rare (R05da: 1 in 50,000–100,000 live births, the commonest of the sternal fusion defects in R05da's scheme, pectus aside; mostly partial superior; inferior clefts go with pentalogy of Cantrell, Ch 7) |

## 4. Clinical correlates — confirmed against Tier 1 (PubMed first)
| Correlate | Embryology in one line | Book `[section]` | Tier 1 | Mark |
|---|---|---|---|---|
| Anencephaly / cranioschisis | Cranial neuropore stays open → no vault → exposed brain degenerates | `[E10.01 CC]` | Ch 6 / Ch 9 dossiers (NTDs) | ✔ |
| Cranial meningocele, meningoencephalocele | Small skull gap; meninges ± brain herniate; often repairable | `[E10.01 CC]` | — | ✔ |
| Craniosynostosis (sagittal, coronal, unicoronal) | Early suture closure at a crest–mesoderm boundary; skull grows along the open sutures | `[E10.01 CC]` | R05cp (*mouse*), R05cq, R05cr, R05cs | ✔✔ mechanism · ⚑ D-064 b rate |
| Syndromic synostosis (Apert, Crouzon, Pfeiffer, Saethre–Chotzen, Boston, craniofrontonasal) | FGFR1/2, TWIST1, MSX2, EFNB1 | `[E10.01 CC, gene table]` | — | ✔ |
| Achondroplasia / hypochondroplasia / thanatophoric | FGFR3 gain of function at the growth plate → endochondral bone short, membranous vault spared | `[E10.01 CC]` | R05ct, R05cu, R05cv | ✔✔ |
| Cleidocranial dysostosis | Generalised dysplasia: open fontanelles, bossing, absent clavicles | `[E10.01 CC]` | R05db (RUNX2) | ✔ · ✚ gene |
| Acromegaly / gigantism | Excess growth hormone | `[E10.01 CC]` | R05dc | ⚑ D-064 d |
| Microcephaly | Brain fails to grow → skull fails to expand | `[E10.01 CC]` | Ch 9 (Zika, alcohol) | ✔ |
| Hemivertebra → congenital scoliosis; segmentation failure → fusion | Errors in forming or reshuffling sclerotome segments | `[E10.02 CC]` | R05cj | ✔✔ |
| Klippel–Feil | Fused cervical segments | `[E10.02 CC]` | R05cz | ✔ · ✚ prevalence |
| Spina bifida occulta vs cystica | Arch fails to fuse (occulta) vs tube fails to close (cystica) | `[E10.02 CC]` | R05cg; Ch 6 dossier | ✔ |
| Cervical rib | Costal element of C7 grows out | `[E10.03 CC]` | R05cw, R05ci | ✔✔ |
| Cleft sternum | Sternal bands fail to meet | `[E10.03 CC]` | R05da | ✔✔ |
| Pectus excavatum / carinatum | Body-wall closure or costal cartilage / sternum formation | `[E10.03 CC]` | — | ✔ |

## 5. ⚑ Watch items and the resegmentation question → decision D-064 (owner picks)
- **(a) When the posterior fontanelle closes — the book gives two times.**
  - The anterior is consistent: "by 18 months" in the text and "around the middle of the second year" in the newborn-skull legend are the same age, and R05cx (single-centre CT, 464 scans) fits it — 53 % closed at 16 months, 88 % at 20, with wide spread (3–5 % already closed at 5–6 months). **✔✔**
  - The posterior differs inside the book: **1–2 months** after birth in the text, **about 3 months** in the legend. R05cy (CT, NZ) found it open in no NZ European infant scanned, in 17 % of Māori/Pasifika under 1 month and 7 % at 1–3 months — consistent with "within the first 2–3 months".
  - Strictly this is a book-internal clash, not book vs Tier 1; it is logged as a ⚑ so the card never quotes one figure as settled. The honest card line is "posterior within the first 2–3 months; anterior usually in the second year, about half by 16 months". Options in D-064.
- **(b) How common craniosynostosis is.**
  - Book: 1 in 2,500 births (≈ 4 per 10,000); sagittal 57 % and coronal 20–25 % of cases.
  - Older population registry (R05cq, Atlanta 1989–2003): 4.3 per 10,000 (≈ 1 in 2,300), which agrees; sagittal was 39 % of nonsyndromic cases.
  - Newer national registries: Finland 6.0 per 10,000 live births (5.0 in 1987, 7.5 in 2010), with sagittal ≈ 65 % of cases (R05cs) — though in live births the rise was significant only in the syndromic group; Netherlands 2008–2013 **7.2 per 10,000 ≈ 1 in 1,400**, sagittal 44 %, a significant yearly rise (R05cr).
  - The sagittal share (39–65 %) brackets the book's 57 %. The overall rate in newer registries is 1.5–1.8× the book's. Options in D-064.
- **(c) Resegmentation, carried forward as asked. A teaching note, not a ⚑: the evidence confirms the book.**
  - The book's account is that each vertebra = caudal half of one sclerotome + cranial half of the next, with the disc at the old mid-segment, myotomes bridging discs, arteries over the bodies and nerves at the discs.
  - It is supported **in humans** by histology of 7 staged embryos at 7–13 mm (R05cj), in **chick** by single-somite and one-and-a-half-somite quail grafts (R05ck, R05cl — body, arch, processes and rib are two-somite structures, the rib head one-somite), and in **axolotl** fate maps (R05dd) — so it is a general vertebrate mechanism, not a chick quirk.
  - The refinements are ✚, not a disagreement:
    - The split is **not an exact half**. In chick, sclerotome cells shift in a region-specific way that depends on their dorsoventral position (the "resegmentation-shift" model, R05cm).
    - In mouse, the boundary marked by rostral/caudal genes does **not** coincide with the resegmentation boundary, and the cervical region differs (R05cn).
  - So "roughly half" is accurate and "exactly half" over-promises. Options in D-064 c: (1) teach the book's halves and put the refinement in More; (2) say "about half" in the card body.
  - **Misconception 1 ("one somite makes one vertebra") stands either way.**
- **(d) What causes acromegaly.**
  - Book: congenital hyperpituitarism with excess growth hormone.
  - Tier 1 (R05dc, JAMA review): GH-secreting pituitary adenomas (12 % of pituitary adenomas) cause **acromegaly in adults and gigantism in children**. It is an acquired tumour, which makes it an odd entry in a congenital-defects box.
  - Options in D-064.
- **(e) Curriculum note, not a ⚑.** The X1 Ch 10 prompt expected the axial codes at **AN8/AN9**. In the NMC AN table **AN8 = features of individual bones (upper limb)** and **AN9 = pectoral region**. The axial skeleton sits at:
  - **AN2.2, AN2.4** (laws of ossification; cartilage)
  - **AN21.1–21.2** (sternum, ribs, thoracic vertebrae)
  - **AN26.1–26.7** (skull osteology; AN26.6 membrane bones; AN26.5 atlas and axis)
  - **AN35.9** (cervical rib)
  - **AN50.1–50.4** (vertebral column curvatures, joints, scoliosis and spina bifida)
  - **AN53.4** (sacralisation)
  - **AN74.4** (genetic basis of achondroplasia)
  - **AN79.4 / AN79.5** (somites; nucleus pulposus)
  
  **No competency names craniosynostosis, fontanelles or Klippel–Feil.** See §7.

Until decided: cards, Checks and scenes give the **book answer**; More carries "⚑ Newer evidence (D-064)" lines; on-screen ages are labelled with their clock (after fertilization vs after birth).

## 6. Top student misconceptions (refute in cards and Checks — craft §3.4)
1. **"One somite makes one vertebra."** Each vertebra is built from the caudal half of one sclerotome and the cranial half of the next. That is why a muscle can reach across a disc to two vertebrae, and why a single somite's cells end up in two vertebrae `[E10.02 · R05cj, R05ck, R05cl]` ✔✔. (Already in the map row; the hero scene's job.)
2. **"Bone forms in two ways, so cartilage turns into bone."** In endochondral ossification the cartilage is a **model that is replaced**: chondrocytes enlarge and die, and osteoblasts arriving with blood vessels lay bone on the calcified matrix `[E10.00, E10.04]` ✔. In intramembranous ossification there is **no cartilage at all**.
3. **"Membrane bone forms inside a membrane."** It forms directly from mesenchyme (in the dermis for the vault). "Membrane" names the absence of a cartilage stage, not a sheet `[E10.00, E10.01]` ✔.
4. **"The whole skull is membrane bone" or "the whole skull is cartilage bone."** The vault and the mandible (formed around Meckel cartilage) are membranous; the skull base and the arch-cartilage derivatives (ossicles, styloid, hyoid) come from cartilage `[E10.01]` ✔.
5. **"An open vertebral arch in the embryo is a defect."** At the end of week 8 a typical vertebra is a U-shaped cartilage, still open at the back; the laminae unite in the early fetal period. Spina bifida occulta is that closure failing to happen `[E10.02 CC · R05cg]` ✚. *(Use in More only; the card body keeps the book's definition.)*
6. **"Spina bifida occulta is a mild neural tube defect."** In occulta only the bony arch is open and the cord is normal. In cystica the neural tube itself has failed to close. They are different events at different times `[E10.02 CC]` ✔.
7. **"The notochord becomes the vertebral column."** It disappears from the vertebral bodies; what remains is the **nucleus pulposus** of each disc `[E10.02 · R05co]` ✔✔ (also on the E05 notochord row).
8. **"Spinal nerves run over the vertebral bodies."** After resegmentation the **intersegmental arteries** run over the bodies, and the nerves leave beside the discs through the intervertebral foramina `[E10.02]` ✔.
9. **"Neural crest only makes nerves and pigment cells."** It makes the face skeleton, the nasal and lacrimal bones, part of the vault (frontal) and the prechordal skull base `[E10.01, E10.04 · R05cp]` ✔✔.
10. **"The fontanelles close at birth."** They let the bones mould during birth and close afterwards: the posterior within the first couple of months, the anterior usually in the second year `[E10.01 · R05cx]` ✔✔ (timing ⚑ D-064 a).
11. **"Achondroplasia affects every bone equally."** FGFR3 acts on endochondral growth, so long bones and the skull base are short while the membranous vault keeps growing and looks large `[E10.01 CC · R05cv]` ✔✔.
12. **"A child with achondroplasia has an affected parent."** Most cases are new mutations; older fathers carry more risk `[E10.01 CC · R05cv, R05cu]` ✔✔.
13. **"The sternum comes from the ribs" (or from somites).** It forms on its own from two bands in lateral plate (parietal) mesoderm that fuse in the midline `[E10.03]` ✔. The costal cartilages come from sclerotome cells that crossed into lateral plate; the bony ribs come from sclerotome that stayed put.
14. **"A cervical rib always causes symptoms."** About 1 in 100 people have one, and most never know; it is much commoner among people with thoracic outlet syndrome `[E10.03 CC · R05cw]` ✔✔.
15. **"The ossicles are the first bones to start ossifying."** The book's claim is that they are the first to be **fully** ossified (from month 4). Starting first and finishing first are different questions `[E10.01]` ✔.
16. **"Skull shape doesn't tell you which suture fused."** It usually does: sagittal → long and narrow; both coronals → short and tall; one coronal → asymmetric `[E10.01 CC]` ✔.

## 7. Curriculum map (R30 — NMC AN table; see the source note below)
**Source note:** nmc.org.in **could not be read this chat**. Chrome refused it (site blocked by your Chrome site permissions), and the fetcher got a client error on the Vol I PDF. So the codes below were read from the **MGMUHS reprint of the NMC Anatomy CBME table** (w.e.f. 2024–25, "Amended as per AC-52/2025", 82 topics / 413 competencies, the same count as NMC Vol I 2024). That is the same kind of source X1 Ch 05 used. AN79.4/79.5 match the wording X1 Ch 09 read on nmc.org.in. The rest should be re-read on nmc.org.in when the site is allowed (§10).
- **AN2 — General features of bones & joints:** AN2.2 laws of ossification, epiphysis types · AN2.4 types of cartilage.
- **AN21 — Thoracic cage:** AN21.1 sternum, typical rib, typical thoracic vertebra · AN21.2 atypical ribs and thoracic vertebrae.
- **AN26 — Skull osteology:** AN26.1 skull position and individual bones · AN26.2 the five normae (sutures and fontanelles sit here; no separate skull-at-birth competency) · AN26.3 cranial cavity, foramina · AN26.4 mandible · AN26.5 atlas and axis · AN26.6 bones that ossify in membrane · AN26.7 C7.
- **AN35.9** — compression of the subclavian artery and lower trunk of the brachial plexus by a cervical rib.
- **AN50 — Vertebral column:** AN50.1 curvatures · AN50.2 intervertebral and other joints · AN50.3 lumbar puncture · AN50.4 anatomical basis of scoliosis, lordosis, prolapsed disc, spondylolisthesis and spina bifida.
- **AN53.4** — clinical importance of abdominopelvic bones (sacralisation of a lumbar vertebra).
- **AN74.4** — genetic basis and clinical features of achondroplasia.
- **AN79.4** somites · **AN79.5** embryological basis of malformations, **nucleus pulposus**, sacrococcygeal teratoma, NTDs (already on the E05 rows).
- **Not in the curriculum:** craniosynostosis, fontanelle closure times, Klippel–Feil, cleft sternum, pectus deformities.

Mapping:
- E10.01.01 → **AN2.2, AN2.4, AN26.6**
- E10.01.02 → **AN26.1, AN26.3, AN26.6**
- E10.01.03 → **AN26.4**
- E10.01.04 → **AN26.2**
- E10.01.05 → **AN79.5** (anencephaly and meningocele are NTDs)
- E10.01.06 → **AN74.4**
- E10.02.01 → **AN79.4, AN50.1**
- E10.02.02 → **AN79.5, AN50.2**
- E10.02.03 → **AN50.4, AN53.4, AN79.5**
- E10.03.01 → **AN21.1, AN21.2**
- E10.03.02 → **AN35.9**

Codes sit on the Ch 10 rows of `tools/map/research.txt` → map.json `an`.

## 8. Visual references for scenes (look, don't copy — RULES G5)
- **Resegmentation shift (CS14–17):** R05cj (human sections, look only), R05cl (graft maps, *chick*), R02 VHE sections CS14–17 for the sclerotome condensations.
- **Cartilage column at CS23:** R05cg–R05ci (graphic reconstructions: U-shaped vertebrae, no spinous processes, open laminae, sternal bands almost joined), R05cf (3D craniovertebral junction, CS18–CS23).
- **Body axis and chondrification onset:** R05ce (Kyoto MRI, CS13–17, R04 collection).
- **Skull sources:** R05cp (crest–mesoderm map of the vault, *mouse*); our own map for the human chondrocranium (prechordal vs chordal) from the book's text, not its figure.
- **R01 3D Atlas:** check whether its CS17–23 models include cartilage or skeleton (§10). NC-ND, reference only.

## 9. Why learners struggle here (M05)
- **Half-segment shift.** Students picture somites stacking straight into vertebrae; the shift and the bridging muscle are hard to see in a flat diagram. Use one 3D animation and a Check that asks where a labelled somite's cells end up.
- **Two ossification words that sound alike.** Tie each to an example and a disease: vault and mandible → membrane; base, limbs, vertebrae → cartilage → FGFR3 dysplasias.
- **Three clocks.** Embryo days, fetal months and after-birth months sit side by side in one chapter. Label every number.
- **Embryology vs osteology.** The NMC competencies here are mostly adult osteology (AN21, AN26, AN50). The development story is what makes the adult features stick, so link each card to its adult structure (D4).

## 10. X1 to-do — done 21 Nov 2026, with open items
- Done: real locators + I1 gaps; staging with human specimen data; Tier A for E10.01.01 and E10.02.01; Tier B–D table; clinical correlates; 16 misconceptions; AN map (reprint); ⚑ D-064 a, b, d + resegmentation note c + curriculum note e; Ch 10 rows in `research.txt`; map rebuilt.
- **Re-read AN2, AN21, AN26, AN35.9, AN50, AN53.4 and AN74.4 on nmc.org.in.** Blocked this chat by your Chrome site permissions; allow nmc.org.in or read it yourself.
- **R01 3D Atlas:** confirm the CS17–23 models show the cartilage column before any vertebra scene (look only).
- **Tier 1 for the sternal-defect figures** (20–50 % in congenital heart disease; multiple manubrial centres 6–20 %, commoner in Down syndrome). None retrieved.
- **Tier 1 for the ossicles** (start of ossification in month 4; first to be fully ossified).
- **Pectus excavatum / carinatum frequency.** Not retrieved; not needed for the B–D cards.
- **Human (not chick or mouse) evidence on the exact resegmentation split.** None found beyond R05cj.
