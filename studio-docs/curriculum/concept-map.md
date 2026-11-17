# Concept map — Langman 14e (E)

*(Purpose: every chapter → section → concept, with crosstabs; source for the explorer and `content/E/map.json`. Updated: 17 Nov 2026 · Bio · Research · X1 Ch 05 (AN + marks for E05).)*

**314 concepts** in 124 sections (all 116 content sections covered; Summary / Problems sections carry none). Ids `E<ch>.<sec>.<nn>` (README) — permanent once a card ships (A2). Data: `content/E/map.json`. Builder: `tools/map/` (`concepts.txt` + `research.txt` + `build_map.py`; README there).

**Columns:** Imp = core · exam-high (x) · supporting (s) · detail (d). Days = days after fertilization (fetal range = to term ≈ 266). Layer: ecto · meso · endo · crest · extra(embryonic) · multi · none. Pages = I1 section locator (printed pages; ≈ where I1 used OCR). AN = NMC 2024 competency codes (R30). Mark = weakest fact line in the chapter dossier (B7). **Every fact is ≈ until its chapter's X1 cites and marks it** (B1, B7; X1 done: E05) — definitions here are one-line labels in our words, not card text. Carnegie ranges in map.json: `cs` = cited (X1 chapters, D-030), `cs_approx` = derived from day.

**Known I1 locator issues (≈):** E05.01/E05.02 run pp 59–60 (I1: p 59; checked in X1) — concepts are placed by heading subject; E08.08/E08.09 twin vs parturition terms look swapped; E10.03 holds spina bifida/Chiari terms (page shift); E12.02 spans most of the limb chapter. X1 corrects locators per chapter.


## E00 — Reading an embryo (orientation) · 6 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E00.01.01 | Axes & planes | A | F | core |  | none | ori |  | 223 |  | ≈ |
| E00.01.02 | Days, weeks & Carnegie stages | A | T | core |  | none | ori |  | 2 |  | ≈ |
| E00.01.03 | Scale | A | T | core |  | none | ori |  |  |  | ≈ |
| E00.01.04 | Colour key | A | G | core |  | none | ori |  |  |  | ≈ |
| E00.01.05 | Reading a section | A | F | core |  | none | ori | E00.01.01 |  |  | ≈ |
| E00.01.06 | How to use the app | A |  | s |  | none | ori |  |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E00.01.02 — “Gestational age and fertilization age are the same number.”

## E01 — Introduction to Molecular Regulation and Signaling · pp 3–13 · 16 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E01.00.01 | Chromatin and nucleosomes | B | M | s |  | none | mol |  | 25 |  | ≈ |
| E01.01.01 | Gene structure: promoter, exons, introns | B | M | s |  | none | mol | E01.00.01 | 23 |  | ≈ |
| E01.01.02 | Transcription factors | B | M | x |  | none | mol | E01.01.01 | 21 |  | ≈ |
| E01.01.03 | Enhancers | B | M | s |  | none | mol | E01.01.02 |  |  | ≈ |
| E01.02.01 | Alternative splicing | B | M | s |  | none | mol | E01.01.01 |  |  | ≈ |
| E01.02.02 | DNA methylation and imprinting | D | M | s |  | none | mol | E01.00.01 |  |  | ≈ |
| E01.03.01 | Induction | A | M | core |  | none | mol | E01.01.02 | 17 |  | ≈ |
| E01.03.02 | Epithelial–mesenchymal interactions | B | M | s |  | none | mol | E01.03.01 |  |  | ≈ |
| E01.04.01 | Paracrine and juxtacrine signalling | B | M | x |  | none | mol | E01.03.01 | 15 |  | ≈ |
| E01.04.02 | Morphogen gradients | B | M | s |  | none | mol | E01.04.01 |  |  | ≈ |
| E01.05.01 | Sonic hedgehog (SHH) pathway | D | M | x |  | none | mol | E01.04.01 | 4 |  | ≈ |
| E01.05.02 | WNT pathway | D | M | s |  | none | mol | E01.04.01 |  |  | ≈ |
| E01.05.03 | TGF-β superfamily (BMPs, Nodal) | D | M | s |  | none | mol | E01.04.01 |  |  | ≈ |
| E01.05.04 | FGFs and receptor tyrosine kinases | D | M | s |  | none | mol | E01.04.01 | 2 |  | ≈ |
| E01.05.05 | Notch signalling | D | M | d |  | none | mol | E01.04.01 | 1 |  | ≈ |
| E01.05.06 | Retinoic acid | D | M | s |  | none | mol | E01.04.01 | 1 |  | ≈ |

*Misconceptions to refute (≈ until X1):* E01.02.02 — “Imprinting changes the DNA sequence.” · E01.03.01 — “Induction is a one-way, one-off signal (most are reciprocal and repeated).”

## E02 — Gametogenesis: Conversion of Germ Cells into Male and Female Gametes · pp 14–33 · 13 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E02.01.01 | Primordial germ cells | A | TG | x | 14–35 | multi | gam | E03.05.01 | 13 |  | ≈ |
| E02.01.02 | Teratomas from germ cells | C | C | s |  | multi | defects | E02.01.01 |  |  | ≈ |
| E02.02.01 | Mitosis | A |  | core |  | none | gam |  | 288 |  | ≈ |
| E02.02.02 | Meiosis | A | T | core |  | none | gam | E02.02.01 | 286 |  | ≈ |
| E02.02.03 | Nondisjunction and numerical abnormalities | B | C | x |  | none | defects | E02.02.02 | 1 |  | ≈ |
| E02.02.04 | Structural chromosome abnormalities | C | C | s |  | none | defects | E02.02.02 |  |  | ≈ |
| E02.02.05 | Mosaicism | B | C | s |  | none | defects | E02.02.01 |  |  | ≈ |
| E02.02.06 | Karyotype and genetic testing | C | C | d |  | none | defects | E02.02.03 |  |  | ≈ |
| E02.03.01 | Oogenesis | A | T | x |  | none | gam | E02.02.02 | 279 |  | ≈ |
| E02.03.02 | Follicle maturation | B |  | x |  | none | gam | E02.03.01 | 6 |  | ≈ |
| E02.03.03 | Spermatogenesis | A | T | x |  | none | gam | E02.02.02 | 274 |  | ≈ |
| E02.03.04 | Spermiogenesis | B |  | s |  | none | gam | E02.03.03 | 272 |  | ≈ |
| E02.03.05 | Abnormal gametes | C | C | d |  | none | gam | E02.03.01, E02.03.03 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E02.01.01 — “Germ cells start in the gonad.” · E02.02.02 — “Crossing over happens in meiosis II.” · E02.03.01 — “Women make new eggs every month.” · E02.03.04 — “Spermiogenesis is another word for spermatogenesis.”

## E03 — First Week of Development: Ovulation to Implantation · pp 34–49 · 17 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E03.01.01 | Ovarian cycle and its hormones | B |  | x |  | none | gam | E02.03.02 | 5 |  | ≈ |
| E03.01.02 | Ovulation | A | T | core | 0–0 | none | gam | E03.01.01 | 2 |  | ≈ |
| E03.01.03 | Corpus luteum | B |  | x |  | none | gam | E03.01.02 |  |  | ≈ |
| E03.01.04 | Oocyte transport | B |  | s | 0–1 | none | gam | E03.01.02 |  |  | ≈ |
| E03.02.01 | Capacitation and acrosome reaction | B |  | x | 0–1 | none | gam | E02.03.04 | 271 |  | ≈ |
| E03.02.02 | Fertilization | A | T | core | 0–1 | none | gam | E03.02.01, E02.03.01 | 270 |  | ≈ |
| E03.02.03 | Results of fertilization | A | T | core | 1–1 | none | gam | E03.02.02 | 268 |  | ≈ |
| E03.02.04 | Contraception and assisted reproduction | C | C | s |  | none | gam | E03.02.02 |  |  | ≈ |
| E03.03.01 | Cleavage and morula | A | T | core | 1–3 | none | early | E03.02.03 | 266 |  | ≈ |
| E03.03.02 | Compaction; inner and outer cell mass | B |  | s | 3–4 | none | early | E03.03.01 | 265 |  | ≈ |
| E03.04.01 | Blastocyst | A | T | core | 4–5 | multi | early | E03.03.02 | 264 |  | ≈ |
| E03.04.02 | Implantation begins | A | T | core | 6–7 | extra | early | E03.04.01 | 21 |  | ≈ |
| E03.05.01 | Epiblast and hypoblast | A | G | core | 7–8 | multi | early | E03.04.01 | 241 |  | ≈ |
| E03.05.02 | Anterior visceral endoderm sets the head end | D | MF | s | 7–8 | extra | early | E03.05.01 | 4 |  | ≈ |
| E03.05.03 | Embryonic stem cells | C | C | d |  | none | early | E03.05.01 |  |  | ≈ |
| E03.06.01 | Uterus at implantation | B |  | x |  | none | plac | E03.01.01 | 1 |  | ≈ |
| E03.06.02 | Menstrual cycle phases | B | T | s |  | none | plac | E03.06.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E03.01.02 — “Ovulation is always on day 14.” · E03.02.02 — “Fertilization happens in the uterus.” · E03.03.01 — “The embryo grows during cleavage.”

## E04 — Second Week of Development: Bilaminar Germ Disc · pp 50–58 · 13 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E04.00.01 | Cytotrophoblast and syncytiotrophoblast | A | G | core | 8–9 | extra | plac | E03.04.02 | 19 |  | ≈ |
| E04.01.01 | Bilaminar disc | A | GF | core | 8–9 | multi | early | E03.05.01 | 236 |  | ≈ |
| E04.01.02 | Amniotic cavity | A | G | x | 8–9 | extra | early | E04.01.01 | 2 |  | ≈ |
| E04.02.01 | Trophoblastic lacunae | B |  | s | 9–9 | extra | plac | E04.00.01 | 17 |  | ≈ |
| E04.02.02 | Primitive yolk sac and exocoelomic membrane | B | G | x | 9–9 | extra | early | E04.01.01 | 6 |  | ≈ |
| E04.03.01 | Uteroplacental circulation begins | A | T | core | 11–12 | extra | plac | E04.02.01 | 16 |  | ≈ |
| E04.03.02 | Extraembryonic mesoderm | B | G | x | 11–12 | extra | early | E04.02.02 | 4 |  | ≈ |
| E04.03.03 | Decidual reaction | B |  | s | 11–13 | none | plac | E04.03.01 |  |  | ≈ |
| E04.04.01 | Primary villi | B |  | x | 13–13 | extra | plac | E04.03.01 | 14 |  | ≈ |
| E04.04.02 | Secondary yolk sac | B | G | s | 13–13 | extra | early | E04.02.02 |  |  | ≈ |
| E04.04.03 | Chorionic cavity and connecting stalk | A | G | core | 13–13 | extra | early | E04.03.02 | 3 |  | ≈ |
| E04.04.04 | Abnormal implantation and ectopic pregnancy | C | C | x |  | extra | defects | E03.04.02 |  |  | ≈ |
| E04.04.05 | Hydatidiform mole and hCG | C | C | x |  | extra | defects | E04.00.01 |  |  | ≈ |

## E05 — Third Week of Development: Trilaminar Germ Disc · pp 59–71 · 20 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E05.00.01 | Prechordal plate | B | F | x | 14–18 | endo | early | E04.01.01 | 2 | AN78.4 | ✔ |
| E05.00.02 | Oropharyngeal and cloacal membranes | B | F | x | 14–21 | multi | early | E05.00.01 | 1 | AN79.1 | ✔ |
| E05.01.01 | Gastrulation in one picture | A | GF | core | 15–21 | multi | early | E04.01.01 | 224 | AN79.1 | ✔ |
| E05.01.02 | Primitive streak | A | TF | core | 15–28 | multi | early | E05.01.01, E00.01.01 | 221 | AN79.1 | ✔ |
| E05.01.03 | Cells move in | A | GF | core | 15–21 | meso | early | E05.01.02 | 215 | AN79.1 | ✔ |
| E05.01.04 | Three germ layers from the epiblast | A | G | core | 16–21 | multi | early | E05.01.03 | 9 | AN79.1 | ✔ |
| E05.02.01 | Notochord | A | F | core | 17–21 | meso | early | E05.01.03 | 84 | AN79.2, AN79.5 | ⚑ |
| E05.02.02 | Neurenteric canal | C | F | d | 17–18 | meso | early | E05.02.01 |  | AN79.2 | ✔✔ |
| E05.03.01 | Body axes are set | B | TF | core | 7–21 | multi | early | E03.05.02, E05.01.02 | 3 | AN79.1 | ✔ |
| E05.03.02 | Left–right signals | D | M | x | 16–20 | multi | early | E05.03.01 | 2 |  | ✔ |
| E05.03.03 | The node as organizer | D | M | s | 16–20 | multi | early | E05.01.02 | 78 | AN79.1 | ✔ |
| E05.04.01 | Fate map: three layers → what they become | A | GA | core |  | multi | early | E05.01.04 |  | AN79.1, AN79.4 | ✔ |
| E05.04.02 | Streak position decides mesoderm type | B | G | x | 15–21 | meso | early | E05.01.03 | 158 | AN79.1 | ✔ |
| E05.05.01 | Growth of the disc | A | F | core | 15–21 | multi | early | E05.01.01 | 64 | AN79.1 | ✔ |
| E05.05.02 | When gastrulation goes wrong | C | C | x | 15–21 | meso | defects | E05.01.01 |  | AN79.5, AN79.6 | ✔ |
| E05.05.03 | Sacrococcygeal teratoma | C | C | x |  | multi | defects | E05.01.02 |  | AN79.5 | ⚑ |
| E05.05.04 | Situs inversus and laterality defects | C | C | x |  | multi | defects | E05.03.02 | 1 | AN79.5 | ⚑ |
| E05.06.01 | Secondary and tertiary villi | B | T | x | 15–21 | extra | plac | E04.04.01 | 13 | AN78.2, AN80.3 | ✔ |
| E05.06.02 | Cytotrophoblast shell; stem and free villi | B |  | s | 15–21 | extra | plac | E05.06.01 |  | AN80.3 | ✔ |
| E05.06.03 | Villi join the embryo's circulation | B | T | s | 19–22 | extra | plac | E05.06.01 |  | AN80.3 | ✔ |

*Misconceptions to refute (cited in the chapter dossier):* E05.01.02 — “The primitive streak is permanent (it shrinks and vanishes).” · E05.01.03 — “The hypoblast becomes the endoderm (epiblast cells replace it).” · E05.01.04 — “Mesoderm comes from the hypoblast.” · E05.02.01 — “The notochord becomes the vertebral column.”

## E06 — Third to Eighth Weeks: The Embryonic Period · pp 72–95 · 23 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E06.00.01 | Embryonic period: weeks 3–8 | A | TC | core | 15–56 | multi | early | E05.01.04 | 7 |  | ≈ |
| E06.01.01 | Neural induction and neural plate | A | G | core | 18–19 | ecto | cns | E05.03.03, E05.02.01 | 77 |  | ≈ |
| E06.01.02 | Neurulation | A | F | core | 19–28 | ecto | cns | E06.01.01 | 73 |  | ≈ |
| E06.01.03 | Neuropores close | A | T | x | 25–28 | ecto | cns | E06.01.02 | 2 |  | ≈ |
| E06.01.04 | Neural crest cells | A | G | core | 19–28 | crest | cns | E06.01.02 | 46 |  | ≈ |
| E06.01.05 | Neural crest derivatives | B | GA | x |  | crest | cns | E06.01.04 | 10 |  | ≈ |
| E06.01.06 | Ectoderm derivatives and placodes | B | GA | x |  | ecto | cns | E06.01.01 | 18 |  | ≈ |
| E06.01.07 | Neural tube defects | C | C | x | 25–28 | ecto | defects | E06.01.03 | 1 |  | ≈ |
| E06.02.01 | Paraxial, intermediate and lateral plate mesoderm | A | G | core | 17–21 | meso | early | E05.04.02 | 154 |  | ≈ |
| E06.02.02 | Somites | A | TG | core | 20–35 | meso | msk | E06.02.01 | 59 |  | ≈ |
| E06.02.03 | Segmentation clock | D | M | s | 20–35 | meso | msk | E06.02.02, E01.05.05 |  |  | ≈ |
| E06.02.04 | Somite differentiation | A | G | core | 22–35 | meso | msk | E06.02.02 | 32 |  | ≈ |
| E06.02.05 | Intermediate mesoderm | A | G | x | 20–28 | meso | uro | E06.02.01 | 20 |  | ≈ |
| E06.02.06 | Lateral plate mesoderm | A | GF | core | 17–21 | meso | cav | E06.02.01 | 77 |  | ≈ |
| E06.02.07 | Vasculogenesis and angiogenesis | B | S | x | 17–28 | meso | cv | E06.02.01 | 8 |  | ≈ |
| E06.02.08 | Sites of blood formation | B | ST | x |  | meso | cv | E06.02.07 |  |  | ≈ |
| E06.02.09 | Capillary haemangiomas | C | C | d |  | meso | defects | E06.02.07 |  |  | ≈ |
| E06.03.01 | Body folding | A | F | core | 21–28 | multi | early | E05.05.01, E06.02.06 | 63 |  | ≈ |
| E06.03.02 | Foregut, midgut, hindgut | A | FG | core | 22–28 | endo | gi | E06.03.01 | 34 |  | ≈ |
| E06.03.03 | Endoderm derivatives | A | GA | x |  | endo | gi | E06.03.02 |  |  | ≈ |
| E06.04.01 | Hox genes pattern the head–tail axis | D | M | x |  | multi | mol | E01.01.02 | 1 |  | ≈ |
| E06.05.01 | External appearance in month 2 | B | T | s | 29–56 | multi | early | E06.03.01 | 3 |  | ≈ |
| E06.05.02 | Estimating embryo age | B | T | s | 20–56 | multi | early | E06.05.01, E06.02.02 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E06.00.01 — “The most dangerous time for teratogens is late pregnancy.” · E06.01.02 — “The neural tube closes all at once.” · E06.01.04 — “Neural crest is part of the CNS.” · E06.02.02 — “Somites are segments of the neural tube.” · E06.02.04 — “The dermatome forms the epidermis.” · E06.02.07 — “The two words mean the same thing.” · E06.03.01 — “The whole yolk sac becomes the gut.”

## E07 — The Gut Tube and the Body Cavities · pp 96–105 · 9 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E07.01.01 | Body plan after folding | A | F | core | 22–28 | multi | cav | E06.03.01, E06.01.02 |  |  | ≈ |
| E07.02.01 | Intraembryonic body cavity | A | FG | core | 19–28 | meso | cav | E06.02.06 | 5 |  | ≈ |
| E07.02.02 | Somatopleure vs splanchnopleure | A | G | x | 19–28 | meso | cav | E07.02.01 | 4 |  | ≈ |
| E07.03.01 | Serous membranes and mesenteries | A | A | core | 22–35 | meso | cav | E07.02.02 | 3 |  | ≈ |
| E07.03.02 | Body wall defects | C | C | x |  | multi | defects | E06.03.01 |  |  | ≈ |
| E07.04.01 | Septum transversum | B | F | x | 22–28 | meso | cav | E06.03.01 | 7 |  | ≈ |
| E07.04.02 | Separating pleural from pericardial cavities | B | F | x | 28–49 | meso | cav | E07.04.01 | 3 |  | ≈ |
| E07.05.01 | Diaphragm from four parts | A | FA | core | 28–56 | meso | cav | E07.04.01, E07.04.02 | 1 |  | ≈ |
| E07.05.02 | Congenital diaphragmatic hernia | C | C | x |  | meso | defects | E07.05.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E07.02.02 — “The somatopleure lines the gut.” · E07.03.02 — “Omphalocele and gastroschisis are the same defect.” · E07.05.01 — “The diaphragm forms where it ends up (it starts high in the neck).”

## E08 — Third Month to Birth: The Fetus and Placenta · pp 106–127 · 18 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E08.01.01 | Fetal period growth | B | T | s | 57–266 | multi | plac | E06.05.01 | 1 |  | ≈ |
| E08.01.02 | Growth restriction and prematurity | C | C | s |  | multi | defects | E08.01.01 |  |  | ≈ |
| E08.01.03 | Time of birth | A | T | x | 266–266 | none | plac | E00.01.02 | 1 |  | ≈ |
| E08.02.01 | Chorion and fetal membranes | B | G | core |  | extra | plac | E05.06.01 | 10 |  | ≈ |
| E08.02.02 | Preeclampsia | C | C | x |  | extra | defects | E04.03.01, E08.04.01 |  |  | ≈ |
| E08.03.01 | Chorion frondosum and laeve; deciduae | A | A | x | 57–120 | extra | plac | E08.02.01 | 7 |  | ≈ |
| E08.04.01 | Structure of the placenta | A | A | core | 120–266 | extra | plac | E08.03.01 | 6 |  | ≈ |
| E08.04.02 | The placental membrane | A | A | x |  | extra | plac | E08.04.01 | 1 |  | ≈ |
| E08.04.03 | Placenta as an endocrine organ | B |  | x |  | extra | plac | E08.04.01 |  |  | ≈ |
| E08.04.04 | Rh disease and fetal hydrops | C | C | x |  | extra | defects | E08.04.02 |  |  | ≈ |
| E08.04.05 | Placenta accreta and previa | C | C | x |  | extra | defects | E08.04.01 |  |  | ≈ |
| E08.05.01 | Umbilical cord | A | A | x | 28–266 | extra | plac | E04.04.03 | 2 |  | ≈ |
| E08.06.01 | Placenta at term | B |  | s | 250–266 | extra | plac | E08.04.01 |  |  | ≈ |
| E08.07.01 | Amniotic fluid | B |  | x |  | extra | plac | E04.01.02 | 1 |  | ≈ |
| E08.07.02 | Polyhydramnios and oligohydramnios | C | C | x |  | extra | defects | E08.07.01 |  |  | ≈ |
| E08.08.01 | Twins and their membranes | B |  | x |  | extra | plac | E03.04.01, E08.02.01 | 1 |  | ≈ |
| E08.08.02 | Twin complications | C | C | s |  | extra | defects | E08.08.01 |  |  | ≈ |
| E08.09.01 | Parturition (labour) | B |  | s | 266–266 | none | plac | E08.01.03 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E08.01.03 — “Forty weeks is counted from fertilization.” · E08.04.01 — “Maternal and fetal blood mix in the placenta.” · E08.04.02 — “The placenta blocks drugs and microbes.” · E08.05.01 — “Umbilical arteries carry oxygen-rich blood.” · E08.08.01 — “All identical twins share one placenta.”

## E09 — Birth Defects and Prenatal Diagnosis · pp 128–144 · 7 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E09.01.01 | Types of birth defects | B | C | x |  | none | defects | E06.00.01 | 3 |  | ≈ |
| E09.01.02 | Principles of teratology | A | CT | core | 15–56 | none | defects | E06.00.01 | 2 |  | ≈ |
| E09.01.03 | Key teratogens | B | C | x |  | none | defects | E09.01.02 | 1 |  | ≈ |
| E09.01.04 | Preventing birth defects | B | C | x |  | none | defects | E09.01.03 |  |  | ≈ |
| E09.02.01 | Prenatal screening | B | C | x |  | none | defects | E09.01.01 | 2 |  | ≈ |
| E09.02.02 | Amniocentesis and chorionic villus sampling | B | C | x |  | extra | defects | E09.02.01 |  |  | ≈ |
| E09.03.01 | Fetal therapy | C | C | d |  | none | defects | E09.02.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E09.01.02 — “Weeks 1–2 are the most sensitive (exposure then usually is all-or-none).”

## E10 — The Axial Skeleton · pp 147–159 · 11 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E10.01.01 | Two ways to make bone | A | S | core |  | meso | msk | E06.02.04 | 6 |  | ≈ |
| E10.01.02 | Neurocranium | B | SA | x |  | multi | msk | E10.01.01 | 2 |  | ≈ |
| E10.01.03 | Viscerocranium | B | S | x |  | crest | msk | E10.01.01, E17.01.01 |  |  | ≈ |
| E10.01.04 | Sutures and fontanelles | B | A | x | 266–266 | multi | msk | E10.01.02 | 1 |  | ≈ |
| E10.01.05 | Craniosynostosis and skull defects | C | C | x |  | multi | defects | E10.01.04 |  |  | ≈ |
| E10.01.06 | Skeletal dysplasias | C | C | x |  | meso | defects | E10.01.01 |  |  | ≈ |
| E10.02.01 | Vertebrae from sclerotomes | A | SF | core | 28–42 | meso | msk | E06.02.04, E05.02.01 | 5 |  | ≈ |
| E10.02.02 | Intervertebral disc | B | SA | x |  | meso | msk | E10.02.01 |  |  | ≈ |
| E10.02.03 | Vertebral defects | C | C | x |  | meso | defects | E10.02.01 |  |  | ≈ |
| E10.03.01 | Ribs and sternum | B | S | s |  | meso | msk | E10.02.01 | 1 |  | ≈ |
| E10.03.02 | Rib and sternum defects | C | C | d |  | meso | defects | E10.03.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E10.02.01 — “One somite makes one vertebra.”

## E11 — Muscular System · pp 160–166 · 13 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E11.00.01 | Where muscles come from | A | G | core |  | meso | msk | E06.02.04 | 12 |  | ≈ |
| E11.01.01 | Myoblasts fuse into fibres | B | S | s |  | meso | msk | E11.00.01 |  |  | ≈ |
| E11.02.01 | Primaxial domain and abaxial domain | B | S | s |  | meso | msk | E06.02.04 | 3 |  | ≈ |
| E11.02.02 | Epaxial and hypaxial muscles | B | SA | x |  | meso | msk | E11.02.01 | 2 |  | ≈ |
| E11.02.03 | Dermatomes and myotomes keep their nerve | A | SA | core |  | meso | msk | E06.02.04 | 1 |  | ≈ |
| E11.03.01 | Molecular regulation of muscle | D | M | d |  | meso | msk | E11.00.01 |  |  | ≈ |
| E11.04.01 | Patterning of muscles | D | S | d |  | meso | msk | E11.00.01 |  |  | ≈ |
| E11.05.01 | Head muscles | B | S | x |  | meso | head | E11.00.01 | 4 |  | ≈ |
| E11.06.01 | Tendons | D | S | d |  | meso | msk | E11.00.01 |  |  | ≈ |
| E11.07.01 | Limb muscles | B | S | x |  | meso | limb | E11.02.02, E12.01.01 | 1 |  | ≈ |
| E11.08.01 | Cardiac muscle | B | S | s |  | meso | cv | E11.00.01, E13.02.01 |  |  | ≈ |
| E11.09.01 | Smooth muscle | B | S | s |  | multi | msk | E11.00.01 |  |  | ≈ |
| E11.09.02 | Muscle defects | C | C | s |  | meso | defects | E11.00.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E11.02.02 — “Limb muscles are epaxial and supplied by dorsal rami.”

## E12 — Limbs · pp 167–178 · 8 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E12.01.01 | Limb buds | A | SF | core | 26–28 | meso | limb | E06.02.06 | 8 |  | ≈ |
| E12.01.02 | Shaping and rotating the limbs | A | F | core | 33–56 | meso | limb | E12.01.01 | 2 |  | ≈ |
| E12.01.03 | Limb bone growth | B | S | x | 42–266 | meso | limb | E10.01.01, E12.01.01 |  |  | ≈ |
| E12.02.01 | Apical ectodermal ridge | D | M | x | 26–49 | ecto | limb | E12.01.01, E01.05.04 |  |  | ≈ |
| E12.02.02 | Zone of polarizing activity | D | M | x | 28–49 | meso | limb | E12.01.01, E01.05.01 |  |  | ≈ |
| E12.02.03 | Limb musculature and innervation | B | SA | s |  | meso | limb | E11.07.01, E11.02.03 |  |  | ≈ |
| E12.02.04 | Limb defects | C | C | x |  | meso | defects | E12.01.02 |  |  | ≈ |
| E12.02.05 | Clubfoot and other limb anomalies | C | C | s |  | meso | defects | E12.01.02 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E12.01.02 — “Arms and legs rotate the same way.”

## E13 — Cardiovascular System · pp 179–222 · 26 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E13.00.01 | The heart works first | A | T | core | 21–22 | meso | cv | E06.02.07, E13.02.01 |  |  | ≈ |
| E13.01.01 | Primary heart field | B | SG | core | 16–18 | meso | cv | E05.04.02 | 20 |  | ≈ |
| E13.01.02 | Secondary heart field | B | S | x | 20–35 | meso | cv | E13.01.01 |  |  | ≈ |
| E13.02.01 | Heart tube forms | A | F | core | 19–22 | meso | cv | E13.01.01, E06.03.01 | 17 |  | ≈ |
| E13.02.02 | Parts of the heart tube | A | S | core | 22–28 | meso | cv | E13.02.01 | 14 |  | ≈ |
| E13.03.01 | Cardiac looping | A | F | core | 23–28 | meso | cv | E13.02.02 | 11 |  | ≈ |
| E13.03.02 | Dextrocardia and heterotaxy | C | C | x |  | meso | defects | E13.03.01, E05.05.04 |  |  | ≈ |
| E13.04.01 | Molecular regulation of the heart | D | M | s |  | meso | cv | E13.01.01 |  |  | ≈ |
| E13.05.01 | Sinus venosus | B | S | x | 28–56 | meso | cv | E13.02.02 | 1 |  | ≈ |
| E13.06.01 | How septa form | A | S | core | 27–37 | meso | cv | E13.03.01 | 9 |  | ≈ |
| E13.06.02 | Atrial septation | A | S | x | 28–42 | meso | cv | E13.06.01 | 3 |  | ≈ |
| E13.06.03 | Atrial septal defects | C | C | x |  | meso | defects | E13.06.02 |  |  | ≈ |
| E13.06.04 | AV canal and valves | B | S | x | 28–42 | meso | cv | E13.06.01 | 1 |  | ≈ |
| E13.06.05 | Outflow tract septation | A | SG | x | 35–56 | crest | cv | E13.06.01, E06.01.04 | 1 |  | ≈ |
| E13.06.06 | Ventricular septum | B | S | x | 35–49 | meso | cv | E13.06.01 | 1 |  | ≈ |
| E13.06.07 | VSD, tetralogy, transposition, truncus | C | C | x |  | multi | defects | E13.06.06, E13.06.05 |  |  | ≈ |
| E13.06.08 | Valve defects and hypoplastic left heart | C | C | s |  | meso | defects | E13.06.04 |  |  | ≈ |
| E13.07.01 | Conducting system | B | S | s |  | meso | cv | E13.05.01 |  |  | ≈ |
| E13.08.01 | Pharyngeal arch arteries and their fates | A | SA | core | 28–49 | meso | cv | E17.01.01 | 4 |  | ≈ |
| E13.08.02 | Recurrent laryngeal nerve asymmetry | B | A | x |  | none | cv | E13.08.01 |  |  | ≈ |
| E13.08.03 | Vitelline and umbilical arteries | B | SA | x |  | meso | cv | E06.02.07 |  |  | ≈ |
| E13.08.04 | Vitelline, umbilical and cardinal veins | B | SA | x | 28–56 | meso | cv | E06.02.07 | 3 |  | ≈ |
| E13.08.05 | Arterial defects | C | C | x |  | meso | defects | E13.08.01 |  |  | ≈ |
| E13.08.06 | Fetal circulation | A | S | core | 57–266 | multi | cv | E13.08.04, E13.06.02, E13.08.01, E08.05.01 | 1 |  | ≈ |
| E13.08.07 | Changes at birth and adult remnants | A | SA | core | 266–266 | multi | cv | E13.08.06 |  |  | ≈ |
| E13.08.08 | Lymphatic system | C | S | d |  | meso | cv | E13.08.04 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E13.06.02 — “The foramen ovale closes before birth.” · E13.08.01 — “All six arches are present at the same time.” · E13.08.06 — “The fetal lungs oxygenate the blood.”

## E14 — Respiratory System · pp 223–229 · 8 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E14.01.01 | Respiratory diverticulum | A | SG | core | 22–28 | endo | resp | E06.03.02 | 8 |  | ≈ |
| E14.01.02 | Tracheoesophageal fistula and oesophageal atresia | C | C | x |  | endo | defects | E14.01.01 |  |  | ≈ |
| E14.02.01 | Larynx | B | S | x | 28–70 | multi | resp | E14.01.01, E17.01.01 |  |  | ≈ |
| E14.03.01 | Bronchi and lung branching | B | S | x | 28–112 | endo | resp | E14.01.01 | 4 |  | ≈ |
| E14.03.02 | Lungs and pleura | B | S | s |  | meso | resp | E14.03.01, E07.04.02 |  |  | ≈ |
| E14.04.01 | Lung maturation phases | A | T | core | 35–266 | endo | resp | E14.03.01 | 1 |  | ≈ |
| E14.04.02 | Surfactant and preterm breathing | B | C | x | 168–266 | endo | resp | E14.04.01 |  |  | ≈ |
| E14.04.03 | Lung anomalies | C | C | s |  | endo | defects | E14.03.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E14.04.01 — “All alveoli form before birth.”

## E15 — Digestive System · pp 230–255 · 21 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E15.01.01 | Gut divisions and their arteries | A | SA | core | 22–28 | endo | gi | E06.03.02 | 22 |  | ≈ |
| E15.02.01 | Molecular regionalisation of the gut | D | M | d |  | endo | gi | E06.03.02, E01.05.06 |  |  | ≈ |
| E15.03.01 | Dorsal and ventral mesenteries | A | S | core | 28–35 | meso | gi | E07.03.01 | 2 |  | ≈ |
| E15.04.01 | Oesophagus | B | S | s | 28–56 | endo | gi | E14.01.01 |  |  | ≈ |
| E15.04.02 | Stomach rotation | A | F | core | 28–49 | endo | gi | E15.01.01 | 6 |  | ≈ |
| E15.04.03 | Omenta and lesser sac | B | A | x | 35–70 | meso | gi | E15.04.02, E15.03.01 | 1 |  | ≈ |
| E15.04.04 | Duodenum | B | S | x | 28–56 | endo | gi | E15.04.02 | 2 |  | ≈ |
| E15.04.05 | Liver and gallbladder | A | SG | core | 22–42 | endo | gi | E15.01.01, E07.04.01 | 2 |  | ≈ |
| E15.04.06 | Pyloric stenosis | C | C | x |  | endo | defects | E15.04.02 |  |  | ≈ |
| E15.04.07 | Spleen | B | S | x | 35–56 | meso | gi | E15.04.03 |  |  | ≈ |
| E15.05.01 | Molecular regulation of liver induction | D | M | d |  | endo | gi | E15.04.05, E01.05.04 |  |  | ≈ |
| E15.05.02 | Biliary atresia and duct anomalies | C | C | s |  | endo | defects | E15.04.05 |  |  | ≈ |
| E15.06.01 | Pancreas | A | S | core | 28–49 | endo | gi | E15.04.04 | 1 |  | ≈ |
| E15.06.02 | Annular pancreas and pancreas divisum | C | C | x |  | endo | defects | E15.06.01 |  |  | ≈ |
| E15.07.01 | Physiological umbilical herniation | A | F | core | 42–70 | endo | gi | E15.01.01 | 3 |  | ≈ |
| E15.07.02 | Midgut rotation | A | F | core | 42–77 | endo | gi | E15.07.01 | 2 |  | ≈ |
| E15.07.03 | Fixation and retroperitoneal parts | B | A | x | 70–84 | endo | gi | E15.07.02 |  |  | ≈ |
| E15.07.04 | Midgut defects | C | C | x |  | endo | defects | E15.07.02 |  |  | ≈ |
| E15.08.01 | Cloaca division | A | S | core | 28–49 | endo | gi | E15.01.01 | 7 |  | ≈ |
| E15.08.02 | Anal canal: two origins | A | SA | core | 49–63 | multi | gi | E15.08.01 |  |  | ≈ |
| E15.08.03 | Hindgut defects | C | C | x |  | multi | defects | E15.08.01, E06.01.04 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E15.04.07 — “The spleen is a gut (endoderm) organ.” · E15.07.01 — “Physiological herniation is an omphalocele.”

## E16 — Urogenital System · pp 256–283 · 23 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E16.00.01 | Three kidney systems | A | ST | core | 22–35 | meso | uro | E06.02.05 | 14 |  | ≈ |
| E16.01.01 | Mesonephros and its duct | B | S | x | 28–63 | meso | uro | E16.00.01 | 13 |  | ≈ |
| E16.01.02 | Metanephros: two sources | A | S | core | 35–266 | meso | uro | E16.01.01 | 5 |  | ≈ |
| E16.01.03 | Nephron formation | B | S | x |  | meso | uro | E16.01.02 |  |  | ≈ |
| E16.01.04 | Kidney ascent | B | F | x | 42–63 | meso | uro | E16.01.02 |  |  | ≈ |
| E16.01.05 | Renal anomalies | C | C | x |  | meso | defects | E16.01.02 |  |  | ≈ |
| E16.01.06 | Bladder and urethra | B | S | x | 35–84 | endo | uro | E15.08.01 | 1 |  | ≈ |
| E16.01.07 | Urachal anomalies | C | C | s |  | endo | defects | E16.01.06 |  |  | ≈ |
| E16.01.08 | Molecular regulation of kidney development | D | M | d |  | meso | uro | E16.01.02 | 1 |  | ≈ |
| E16.01.09 | Wilms tumour | C | C | s |  | meso | defects | E16.01.02, E16.01.08 |  |  | ≈ |
| E16.02.01 | Sex determination | A | M | core | 42–49 | none | gen | E03.02.03 | 10 |  | ≈ |
| E16.02.02 | Indifferent gonad | A | S | core | 35–49 | multi | gen | E02.01.01, E06.02.05 | 11 |  | ≈ |
| E16.02.03 | Testis | B | S | x | 49–84 | meso | gen | E16.02.02, E16.02.01 | 9 |  | ≈ |
| E16.02.04 | Ovary | B | S | s | 49–140 | meso | gen | E16.02.02 |  |  | ≈ |
| E16.02.05 | Genital ducts: two sets | A | S | core | 42–84 | meso | gen | E16.02.02, E16.01.01, E16.02.01, E16.02.03 | 6 |  | ≈ |
| E16.02.06 | Male ducts and glands | B | SA | x |  | multi | gen | E16.02.05 |  |  | ≈ |
| E16.02.07 | Female ducts and vagina | B | SA | x |  | meso | gen | E16.02.05 | 1 |  | ≈ |
| E16.02.08 | Uterine and vaginal anomalies | C | C | x |  | meso | defects | E16.02.07 |  |  | ≈ |
| E16.02.09 | External genitalia | A | S | core | 49–84 | multi | gen | E16.02.05, E16.02.01, E15.08.01 | 2 |  | ≈ |
| E16.02.10 | Hypospadias and epispadias | C | C | x |  | multi | defects | E16.02.09 |  |  | ≈ |
| E16.02.11 | Differences of sex development | C | C | x |  | multi | defects | E16.02.01, E16.02.09 |  |  | ≈ |
| E16.02.12 | Descent of the testis | A | F | core | 56–266 | meso | gen | E16.02.03 | 1 |  | ≈ |
| E16.02.13 | Inguinal hernia, hydrocele, cryptorchidism | C | C | x |  | meso | defects | E16.02.12 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E16.00.01 — “All three systems form the adult kidney together.” · E16.01.02 — “Nephrons and collecting ducts come from the same tissue.” · E16.02.01 — “Female development needs no genes at all.” · E16.02.05 — “Testosterone makes the paramesonephric ducts regress.”

## E17 — Head and Neck · pp 284–312 · 20 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E17.00.01 | What builds the head and neck | A | G | core |  | crest | head | E06.01.04, E06.02.02 | 28 |  | ≈ |
| E17.01.01 | Pharyngeal arches | A | SG | core | 22–35 | multi | head | E17.00.01 | 27 |  | ≈ |
| E17.01.02 | Arch derivatives | A | A | core |  | multi | head | E17.01.01 | 7 |  | ≈ |
| E17.01.03 | Stomodeum | B | S | s | 22–28 | ecto | head | E05.00.02 |  |  | ≈ |
| E17.02.01 | Pharyngeal pouches | A | GA | core | 28–56 | endo | head | E17.01.01 | 3 |  | ≈ |
| E17.03.01 | Pharyngeal clefts | B | S | x | 28–56 | ecto | head | E17.01.01 | 2 |  | ≈ |
| E17.03.02 | Arch and pouch defects | C | C | x |  | multi | defects | E17.03.01, E17.02.01 |  |  | ≈ |
| E17.04.01 | Molecular regulation of facial development | D | M | d |  | crest | head | E06.01.04 |  |  | ≈ |
| E17.05.01 | Tongue | A | SA | core | 28–56 | multi | head | E17.01.02, E11.05.01 | 3 |  | ≈ |
| E17.05.02 | Tongue-tie | C | C | d |  | multi | defects | E17.05.01 |  |  | ≈ |
| E17.06.01 | Thyroid descent | A | S | core | 24–49 | endo | head | E17.05.01 | 1 |  | ≈ |
| E17.06.02 | Thyroglossal cyst and ectopic thyroid | C | C | x |  | endo | defects | E17.06.01 |  |  | ≈ |
| E17.07.01 | Face from five prominences | A | FG | core | 28–70 | crest | head | E17.01.01 | 7 |  | ≈ |
| E17.07.02 | Nasal placodes and prominences | B | F | x | 35–49 | multi | head | E17.07.01 | 4 |  | ≈ |
| E17.08.01 | Intermaxillary segment | B | F | x | 42–56 | crest | head | E17.07.02 | 2 |  | ≈ |
| E17.09.01 | Secondary palate | A | F | core | 49–70 | crest | head | E17.08.01 | 1 |  | ≈ |
| E17.09.02 | Cleft lip and cleft palate | C | C | x |  | crest | defects | E17.09.01 |  |  | ≈ |
| E17.10.01 | Nasal cavities and sinuses | B | S | s | 42–266 | multi | head | E17.07.02 |  |  | ≈ |
| E17.11.01 | Teeth | B | S | s | 42–266 | multi | head | E17.07.01 | 1 |  | ≈ |
| E17.12.01 | Tooth regulation and defects | D | MC | d |  | multi | head | E17.11.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E17.01.01 — “Humans have gills or gill slits.” · E17.02.01 — “Inferior parathyroids come from pouch 4.” · E17.09.02 — “Cleft lip and cleft palate are one defect.”

## E18 — Central Nervous System · pp 313–350 · 21 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E18.01.01 | Neural tube layers | A | S | core | 28–56 | ecto | cns | E06.01.02 | 7 |  | ≈ |
| E18.01.02 | Alar and basal plates | A | S | core | 28–56 | ecto | cns | E18.01.01 | 4 |  | ≈ |
| E18.01.03 | Spinal nerves and dorsal root ganglia | B | SA | x | 28–42 | multi | cns | E18.01.02, E06.01.04 | 1 |  | ≈ |
| E18.01.04 | Myelination | B | S | s | 112–266 | multi | cns | E18.01.03 |  |  | ≈ |
| E18.01.05 | Position of the cord end | B | A | x | 84–266 | ecto | cns | E18.01.01 |  |  | ≈ |
| E18.01.06 | Spina bifida types | C | C | x |  | ecto | defects | E06.01.07, E10.02.01 |  |  | ≈ |
| E18.01.07 | Dorsoventral patterning of the tube | D | M | x |  | ecto | cns | E18.01.02, E01.05.01 |  |  | ≈ |
| E18.02.01 | Brain vesicles and flexures | A | F | core | 28–42 | ecto | cns | E06.01.02 | 16 |  | ≈ |
| E18.02.02 | Hindbrain: medulla, pons, cerebellum | B | S | x | 35–266 | ecto | cns | E18.02.01 |  |  | ≈ |
| E18.02.03 | Midbrain | B | S | s |  | ecto | cns | E18.02.01 |  |  | ≈ |
| E18.02.04 | Diencephalon and pituitary | B | S | x | 35–84 | multi | cns | E18.02.01 |  |  | ≈ |
| E18.02.05 | Cerebral hemispheres | B | S | x | 35–266 | ecto | cns | E18.02.01 |  |  | ≈ |
| E18.02.06 | Ventricles and CSF | B | S | s |  | ecto | cns | E18.02.01 |  |  | ≈ |
| E18.02.07 | Meninges | B | S | s |  | multi | cns | E18.01.01 |  |  | ≈ |
| E18.02.08 | Brain defects | C | C | x |  | ecto | defects | E18.02.01 |  |  | ≈ |
| E18.03.01 | Brain patterning | D | M | s |  | ecto | cns | E18.02.01, E06.04.01 |  |  | ≈ |
| E18.04.01 | Cranial nerves | B | SA | x | 35–56 | multi | cns | E18.01.02, E17.01.02 |  |  | ≈ |
| E18.05.01 | Sympathetic system | B | S | x | 35–56 | crest | cns | E06.01.05 | 2 |  | ≈ |
| E18.05.02 | Adrenal gland: two origins | A | SG | core | 42–266 | multi | cns | E18.05.01 | 1 |  | ≈ |
| E18.05.03 | Parasympathetic system | B | S | s |  | crest | cns | E06.01.05 |  |  | ≈ |
| E18.05.04 | Neural crest tumours | C | C | s |  | crest | defects | E18.05.02 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E18.01.02 — “The basal plate is sensory.” · E18.02.04 — “The whole pituitary comes from the brain.” · E18.05.02 — “The whole adrenal comes from one layer.”

## E19 — Ear · pp 351–359 · 5 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E19.01.01 | Otic vesicle and inner ear | A | S | core | 22–56 | ecto | ear | E06.01.06 | 2 |  | ≈ |
| E19.01.02 | Membranous and bony labyrinth | B | S | s |  | multi | ear | E19.01.01 |  |  | ≈ |
| E19.02.01 | Middle ear | A | SA | core | 28–266 | multi | ear | E17.02.01, E17.01.02 | 1 |  | ≈ |
| E19.03.01 | External ear | B | S | x | 42–140 | multi | ear | E17.03.01 |  |  | ≈ |
| E19.04.01 | Congenital hearing loss | C | C | s |  | multi | defects | E19.01.01, E19.02.01 |  |  | ≈ |

## E20 — Eye · pp 360–369 · 9 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E20.01.01 | Optic cup and lens vesicle | A | S | core | 22–42 | ecto | eye | E18.02.01, E06.01.06 | 8 |  | ≈ |
| E20.02.01 | Retina | A | S | core | 35–266 | ecto | eye | E20.01.01 | 1 |  | ≈ |
| E20.02.02 | Iris and ciliary body | B | S | x | 56–266 | multi | eye | E20.02.01 |  |  | ≈ |
| E20.03.01 | Lens | B | S | s | 35–266 | ecto | eye | E20.01.01 |  |  | ≈ |
| E20.04.01 | Choroid, sclera and cornea | B | S | s |  | multi | eye | E20.01.01 |  |  | ≈ |
| E20.05.01 | Vitreous and hyaloid artery | B | S | s |  | multi | eye | E20.01.01 |  |  | ≈ |
| E20.06.01 | Optic nerve | B | SA | x | 42–266 | ecto | eye | E20.01.01 |  |  | ≈ |
| E20.07.01 | Molecular regulation of the eye | D | M | x |  | ecto | eye | E20.01.01, E01.05.01 | 1 |  | ≈ |
| E20.07.02 | Eye defects | C | C | x |  | ecto | defects | E20.07.01 |  |  | ≈ |

*Misconceptions to refute (≈ until X1):* E20.02.01 — “Retinal detachment separates retina from choroid (it splits the two retinal layers).”

## E21 — Integumentary System · pp 370–376 · 7 concepts

| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks | AN | Mark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E21.01.01 | Epidermis | B | SG | x | 28–266 | multi | skin | E06.01.06, E06.01.05 | 5 |  | ≈ |
| E21.01.02 | Dermis | B | S | s |  | meso | skin | E06.02.04 |  |  | ≈ |
| E21.01.03 | Skin disorders | C | C | d |  | multi | defects | E21.01.01 |  |  | ≈ |
| E21.02.01 | Hair | B | S | s | 84–266 | ecto | skin | E21.01.01 |  |  | ≈ |
| E21.03.01 | Nails | B | S | d | 70–266 | ecto | skin | E21.01.01 |  |  | ≈ |
| E21.04.01 | Sweat glands | B | S | d |  | ecto | skin | E21.01.01 |  |  | ≈ |
| E21.05.01 | Mammary glands | B | S | s | 42–266 | ecto | skin | E21.01.01 |  |  | ≈ |

---

## Crosstabs
*(Counts of concepts. The explorer makes every cell clickable.)*


### Chapter × Day

| | Wk 1 | Wk 2 | Wk 3 | Wk 4 | Wk 5–8 | Fetal | No day | Σ |
|---|---|---|---|---|---|---|---|---|
| E00 | · | · | · | · | · | · | 6 | 6 |
| E01 | · | · | · | · | · | · | 16 | 16 |
| E02 | · | 1 | · | · | · | · | 12 | 13 |
| E03 | 11 | · | · | · | · | · | 6 | 17 |
| E04 | · | 11 | · | · | · | · | 2 | 13 |
| E05 | 1 | 2 | 14 | · | · | · | 3 | 20 |
| E06 | · | · | 12 | 4 | 1 | · | 6 | 23 |
| E07 | · | · | 2 | 5 | · | · | 2 | 9 |
| E08 | · | · | · | 1 | · | 6 | 11 | 18 |
| E09 | · | · | 1 | · | · | · | 6 | 7 |
| E10 | · | · | · | 1 | · | 1 | 9 | 11 |
| E11 | · | · | · | · | · | · | 13 | 13 |
| E12 | · | · | · | 3 | 2 | · | 3 | 8 |
| E13 | · | · | 4 | 8 | 2 | 2 | 10 | 26 |
| E14 | · | · | · | 3 | 1 | 1 | 3 | 8 |
| E15 | · | · | · | 8 | 5 | 1 | 7 | 21 |
| E16 | · | · | · | 2 | 10 | · | 11 | 23 |
| E17 | · | · | · | 7 | 5 | · | 8 | 20 |
| E18 | · | · | · | 4 | 6 | 2 | 9 | 21 |
| E19 | · | · | · | 2 | 1 | · | 2 | 5 |
| E20 | · | · | · | 1 | 4 | · | 4 | 9 |
| E21 | · | · | · | 1 | 1 | 2 | 3 | 7 |

### Chapter × Germ layer

| | ecto | meso | endo | crest | extra | multi | none | Σ |
|---|---|---|---|---|---|---|---|---|
| E00 | · | · | · | · | · | · | 6 | 6 |
| E01 | · | · | · | · | · | · | 16 | 16 |
| E02 | · | · | · | · | · | 2 | 11 | 13 |
| E03 | · | · | · | · | 2 | 2 | 13 | 17 |
| E04 | · | · | · | · | 11 | 1 | 1 | 13 |
| E05 | · | 5 | 1 | · | 3 | 11 | · | 20 |
| E06 | 5 | 9 | 2 | 2 | · | 5 | · | 23 |
| E07 | · | 7 | · | · | · | 2 | · | 9 |
| E08 | · | · | · | · | 14 | 2 | 2 | 18 |
| E09 | · | · | · | · | 1 | · | 6 | 7 |
| E10 | · | 7 | · | 1 | · | 3 | · | 11 |
| E11 | · | 12 | · | · | · | 1 | · | 13 |
| E12 | 1 | 7 | · | · | · | · | · | 8 |
| E13 | · | 21 | · | 1 | · | 3 | 1 | 26 |
| E14 | · | 1 | 6 | · | · | 1 | · | 8 |
| E15 | · | 3 | 16 | · | · | 2 | · | 21 |
| E16 | · | 15 | 2 | · | · | 5 | 1 | 23 |
| E17 | 2 | · | 3 | 6 | · | 9 | · | 20 |
| E18 | 12 | · | · | 3 | · | 6 | · | 21 |
| E19 | 1 | · | · | · | · | 4 | · | 5 |
| E20 | 6 | · | · | · | · | 3 | · | 9 |
| E21 | 4 | 1 | · | · | · | 2 | · | 7 |

### Tier × Chapter (coverage)

| | E00 | E01 | E02 | E03 | E04 | E05 | E06 | E07 | E08 | E09 | E10 | E11 | E12 | E13 | E14 | E15 | E16 | E17 | E18 | E19 | E20 | E21 | Σ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 6 | 1 | 5 | 7 | 5 | 7 | 13 | 5 | 5 | 1 | 2 | 2 | 2 | 10 | 2 | 9 | 7 | 8 | 4 | 2 | 2 | · | 105 |
| B | · | 8 | 4 | 7 | 6 | 7 | 6 | 2 | 7 | 5 | 5 | 7 | 2 | 9 | 4 | 5 | 8 | 6 | 12 | 2 | 5 | 6 | 123 |
| C | · | · | 4 | 2 | 2 | 4 | 2 | 2 | 6 | 1 | 4 | 1 | 2 | 6 | 2 | 5 | 7 | 4 | 3 | 1 | 1 | 1 | 60 |
| D | · | 7 | · | 1 | · | 2 | 2 | · | · | · | · | 3 | 2 | 1 | · | 2 | 1 | 2 | 2 | · | 1 | · | 26 |

### System × Tier

| | A | B | C | D | Σ |
|---|---|---|---|---|---|
| Orientation | 6 | · | · | · | 6 |
| Molecular basics | 1 | 8 | · | 8 | 17 |
| Gametes & fertilization | 8 | 6 | 2 | · | 16 |
| Early embryo | 17 | 10 | 2 | 3 | 32 |
| Placenta & membranes | 7 | 15 | · | · | 22 |
| Body cavities | 6 | 2 | · | · | 8 |
| Birth defects | 1 | 7 | 55 | · | 63 |
| Skeleton & muscle | 6 | 9 | · | 4 | 19 |
| Limbs | 2 | 3 | · | 2 | 7 |
| Heart & vessels | 10 | 12 | 1 | 1 | 24 |
| Respiratory | 2 | 4 | · | · | 6 |
| Digestive | 11 | 5 | · | 2 | 18 |
| Urinary | 3 | 4 | · | 1 | 8 |
| Genital | 5 | 4 | · | · | 9 |
| Head & neck | 8 | 7 | · | 2 | 17 |
| Nervous system | 8 | 14 | · | 2 | 24 |
| Ear | 2 | 2 | · | · | 4 |
| Eye | 2 | 5 | · | 1 | 8 |
| Skin | · | 6 | · | · | 6 |

### Germ layer × Day

| | Wk 1 | Wk 2 | Wk 3 | Wk 4 | Wk 5–8 | Fetal | No day | Σ |
|---|---|---|---|---|---|---|---|---|
| Ectoderm | · | · | 2 | 10 | 6 | 3 | 10 | 31 |
| Mesoderm | · | · | 17 | 19 | 11 | · | 41 | 88 |
| Endoderm | · | 1 | · | 12 | 4 | 2 | 11 | 30 |
| Neural crest | · | · | 1 | 1 | 4 | · | 7 | 13 |
| Extraembryonic | 2 | 9 | 3 | 1 | · | 3 | 13 | 31 |
| Several layers | 3 | 3 | 9 | 7 | 12 | 5 | 25 | 64 |
| No layer | 7 | 1 | 1 | · | 1 | 2 | 45 | 57 |

### Importance × Chapter

| | E00 | E01 | E02 | E03 | E04 | E05 | E06 | E07 | E08 | E09 | E10 | E11 | E12 | E13 | E14 | E15 | E16 | E17 | E18 | E19 | E20 | E21 | Σ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core | 5 | 1 | 2 | 7 | 4 | 8 | 10 | 4 | 2 | 1 | 2 | 2 | 2 | 9 | 2 | 9 | 7 | 8 | 4 | 2 | 2 | · | 93 |
| exam-high | · | 3 | 5 | 4 | 6 | 8 | 9 | 5 | 11 | 5 | 7 | 3 | 4 | 13 | 4 | 8 | 12 | 6 | 10 | 1 | 4 | 1 | 129 |
| supporting | 1 | 11 | 4 | 5 | 3 | 3 | 3 | · | 5 | · | 1 | 5 | 2 | 3 | 2 | 2 | 3 | 3 | 7 | 2 | 3 | 3 | 71 |
| detail | · | 1 | 2 | 1 | · | 1 | 1 | · | · | 1 | 1 | 3 | · | 1 | · | 2 | 1 | 3 | · | · | · | 3 | 21 |

### Concept × Chapter — where it recurs (top 25 by chapters reached)

| Concept | Chapters |
|---|---|
| E05.01.01 Gastrulation in one picture | 21: E01, E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E05.01.04 Three germ layers from the epiblast | 21: E01, E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E02.02.01 Mitosis | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E02.02.02 Meiosis | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E02.03.01 Oogenesis | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E02.03.03 Spermatogenesis | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E02.03.04 Spermiogenesis | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E03.02.01 Capacitation and acrosome reaction | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E03.02.02 Fertilization | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E03.02.03 Results of fertilization | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E03.03.01 Cleavage and morula | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E03.03.02 Compaction; inner and outer cell mass | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E03.04.01 Blastocyst | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E03.05.01 Epiblast and hypoblast | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E04.01.01 Bilaminar disc | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E04.03.02 Extraembryonic mesoderm | 20: E01, E02, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E05.01.02 Primitive streak | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E05.01.03 Cells move in | 20: E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E05.00.02 Oropharyngeal and cloacal membranes | 19: E01, E03, E04, E05, E06, E07, E08, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E05.04.01 Fate map: three layers → what they become | 19: E01, E03, E04, E05, E06, E07, E08, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E07.02.02 Somatopleure vs splanchnopleure | 19: E01, E03, E04, E05, E06, E07, E08, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E09.01.01 Types of birth defects | 19: E01, E02, E03, E04, E05, E06, E08, E09, E10, E11, E12, E13, E14, E16, E17, E18, E19, E20, E21 |
| E17.03.02 Arch and pouch defects | 19: E01, E02, E03, E04, E05, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E00.01.01 Axes & planes | 18: E00, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |
| E06.01.01 Neural induction and neural plate | 18: E01, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21 |

Full matrix: `crosstabs.concept_x_chapter` in map.json (explorer → Crosstabs → Concept × Chapter).


### Chapter × Chapter — concepts of row chapter that recur in column chapter

| | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E00 | · | · | · | · | · | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| E01 | · | · | 2 | 3 | · | 5 | 10 | 1 | 3 | 3 | 5 | 6 | 10 | 7 | 4 | 10 | 6 | 5 | 9 | 1 | 9 | 1 |
| E02 | · | · | · | 7 | 6 | 7 | 6 | 6 | 6 | 6 | 5 | 5 | 5 | 6 | 6 | 6 | 8 | 5 | 6 | 5 | 5 | 5 |
| E03 | · | 1 | 7 | · | 11 | 10 | 10 | 8 | 10 | 9 | 7 | 8 | 7 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 7 | 7 |
| E04 | · | 1 | 5 | 7 | · | 11 | 7 | 5 | 11 | 5 | 2 | 2 | 2 | 6 | 3 | 6 | 7 | 4 | 3 | 2 | 3 | 2 |
| E05 | · | 9 | 8 | 7 | 11 | · | 16 | 13 | 14 | 8 | 11 | 12 | 9 | 19 | 12 | 16 | 11 | 13 | 14 | 10 | 11 | 10 |
| E06 | · | 14 | 2 | 4 | 7 | 13 | · | 14 | 11 | 5 | 12 | 11 | 10 | 16 | 10 | 16 | 9 | 15 | 15 | 10 | 8 | 13 |
| E07 | · | 3 | · | 1 | 4 | 4 | 4 | · | 3 | 1 | 3 | 3 | 3 | 5 | 4 | 6 | 5 | 3 | 4 | 4 | 1 | 3 |
| E08 | · | · | · | 1 | 4 | 5 | 4 | 3 | · | 5 | · | · | 3 | 4 | 3 | 3 | · | 3 | 3 | · | 3 | · |
| E09 | · | 1 | 2 | 1 | 1 | 3 | 2 | · | 4 | · | 4 | 1 | 3 | 3 | 1 | · | 1 | 3 | 3 | 1 | 1 | 1 |
| E10 | · | 3 | · | · | · | 2 | 6 | 1 | · | 3 | · | 3 | 3 | 4 | 2 | 3 | 2 | 4 | 7 | 2 | 2 | 2 |
| E11 | · | 6 | 1 | 1 | 4 | 6 | 7 | 6 | 4 | 1 | 8 | · | 10 | 6 | 4 | 5 | 5 | 6 | 8 | 4 | 3 | 7 |
| E12 | · | 3 | 1 | 1 | 1 | 4 | 5 | 1 | 2 | 4 | 5 | 4 | · | 4 | 2 | 4 | 5 | 3 | 2 | 1 | 2 | 2 |
| E13 | · | 1 | · | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 4 | 2 | 3 | · | 2 | 3 | 3 | 5 | 1 | 1 | · | 1 |
| E14 | · | 1 | · | 1 | 3 | 3 | 3 | 3 | 2 | 1 | 2 | 2 | 3 | 4 | · | 4 | 5 | 5 | 2 | 1 | · | 1 |
| E15 | · | 4 | · | 2 | 5 | 6 | 13 | 12 | 5 | 5 | 2 | 4 | 8 | 15 | 9 | · | 13 | 9 | 8 | 5 | 4 | 2 |
| E16 | · | 3 | 2 | · | · | 3 | 4 | 1 | 2 | 3 | 1 | · | 2 | 4 | 2 | 5 | · | 2 | · | 1 | · | 1 |
| E17 | · | 4 | 1 | 1 | 3 | 5 | 7 | 4 | 3 | 3 | 5 | 4 | 4 | 6 | 7 | 5 | 4 | · | 11 | 8 | 5 | 4 |
| E18 | · | 3 | 1 | 1 | 2 | 7 | 10 | 4 | 3 | 2 | 6 | 5 | 5 | 8 | 3 | 6 | 8 | 8 | · | 3 | 5 | 3 |
| E19 | · | 2 | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 3 | 2 | 3 | 3 | 2 | 1 | 2 | 4 | 5 | · | 4 | 2 |
| E20 | · | 2 | 1 | · | · | · | 3 | 2 | · | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 4 | 3 | 3 | · | 2 |
| E21 | · | 2 | · | · | 1 | 2 | 2 | 2 | 2 | · | 1 | 2 | 2 | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | · |

### Prerequisite graph — most-unlocking concepts

| Concept | Unlocks (transitive) | Direct |
|---|---|---|
| E02.02.01 Mitosis | 288 | 2 |
| E02.02.02 Meiosis | 286 | 4 |
| E02.03.01 Oogenesis | 279 | 3 |
| E02.03.03 Spermatogenesis | 274 | 2 |
| E02.03.04 Spermiogenesis | 272 | 1 |
| E03.02.01 Capacitation and acrosome reaction | 271 | 1 |
| E03.02.02 Fertilization | 270 | 2 |
| E03.02.03 Results of fertilization | 268 | 2 |
| E03.03.01 Cleavage and morula | 266 | 1 |
| E03.03.02 Compaction; inner and outer cell mass | 265 | 1 |
| E03.04.01 Blastocyst | 264 | 3 |
| E03.05.01 Epiblast and hypoblast | 241 | 4 |
| E04.01.01 Bilaminar disc | 236 | 4 |
| E05.01.01 Gastrulation in one picture | 224 | 3 |
| E00.01.01 Axes & planes | 223 | 2 |
| E05.01.02 Primitive streak | 221 | 4 |
| E05.01.03 Cells move in | 215 | 3 |
| E05.04.02 Streak position decides mesoderm type | 158 | 2 |
| E06.02.01 Paraxial, intermediate and lateral plate mesoderm | 154 | 4 |
| E05.02.01 Notochord | 84 | 3 |

**Map checks (K1):** every content section has ≥ 1 concept (✅) · every concept has tier, thread or system, importance, locator · no orphan or circular prerequisites ✅ · glossary terms linked by name 205/265, + 60 attached to their primary section's first concept, 0 unplaced (I1 gap).
