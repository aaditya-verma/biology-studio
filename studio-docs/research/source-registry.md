# Source registry — who we trust, for what

*(Purpose: owner doc for sources **and tools**. Created 17 Nov 2026, D-011. Updated: 20 Nov 2026 · Bio · Research · X1 Ch 08 (R05ap–bk added with PMIDs; R30 AN80 wording read). Before: 20 Nov 2026 · X1 Ch 07 (R05z–ao added with PMIDs; R06 stage chapters CS9–19 read for Ch 7; R30 AN79 checked against NMC Vol I 2024). Before: 19 Nov 2026 · X1 Ch 06 (R05l–y; R08 full table; R02 ages, D-039 c). Before: S1 studio (PMIDs added to R05a, R05b, R05e, R05j, R05k so pasted PubMed links resolve; `content/E/sources.json` is derived from this file by `tools/card-check --write-sources`). Before: 17 Nov 2026 · X1 Ch 05 (R05a–j, R08 added; R30 copy noted). Add a source or tool here before citing or installing it anywhere.)*

**Rule in one line:** Langman 14e is the spine. Trusted outside sources **confirm**, **correct** (logged, never silent), **add depth** (labelled), and shape **how** we teach and draw. RULES B6–B8, G5.

## How sources show up
- **Citation:** book section first, then source id + locator — `[E05.02 · R01 CS8]`.
- **Confidence mark on every fact line:**
  - **✔✔** book + a Tier 1 source agree (target for every Tier A card)
  - **✔** book only (fine; R-check pending)
  - **⚑** book and a Tier 1 source disagree → `claude/DECISIONS.md` entry; card gives the book answer (exam answer) + a "Newer evidence" line in More
  - **✚** beyond the book, Tier 1 only → allowed in More and Tier D only, labelled "beyond Langman"
  - **≈** uncited or low confidence → blocks final (RULES B1)
- **Licence decides use, not quality.** NC / ND / "no reuse" sources are **reference only**: we look, then draw our own. Only CC BY (or MIT/Apache) assets may ship, credited (RULES G4–G5; one CC BY-SA exception, T07 / D-021).

## Tier 0 — spine
| Id | Source | Use | Licence |
|---|---|---|---|
| R00 | Langman's Medical Embryology, 14e (Sadler) | Every fact's primary citation, by section `E<ch>.<sec>` | © — own words only (RULES §G) |

## Tier 1 — human specimens & peer-reviewed evidence (may confirm, correct, add)
| Id | Source | Best for | Licence → our use |
|---|---|---|---|
| R01 | **3D Atlas of Human Embryology** — de Bakker et al., *Science* 2016; 3dembryoatlas.com. 14 interactive 3D-PDF models, CS7–CS23 (days 15–60), built from ~15,000 annotated sections of 34 Carnegie embryos | Checking our 3D scenes: shape, organ position, timing, growth numbers. Its authors found textbook figures with organs in the wrong place or time — so it is our main fact-check for scenes | CC BY-NC-ND → **reference only**; never import or trace meshes |
| R02 | **Virtual Human Embryo** (Carnegie collection, DREM/HEIRLOOM; ehd.org, LSUHSC). Labelled serial sections + 3D reconstructions for all 23 stages | Stage size/age facts; "reading a section" (E00.01.05); cut-plane checks | No open licence stated → reference only |
| R03 | **HDBR Atlas** (Newcastle/UCL, hdbr.org). 3D models CS12–16, annotated H&E CS14–22, gene expression | Part 2 systems (heart, CNS); molecular Tier D | Data on request → reference only unless granted |
| R04 | **Kyoto Collection** MRI datasets (Shiota, Yamada, Takakuwa et al.); some 3D models in MorphoMuseuM / *Data in Brief* | Organ morphogenesis CS13–23 (brain, liver, stomach, ear) | **Per dataset** — some are CC BY → candidates for imported meshes after a licence check |
| R05 | **Peer-reviewed papers via PubMed** (open access preferred). First entry: de Bree, de Bakker, Oostra, *PLoS ONE* 2018 — human notochord formation, CS8–15 | Topic-specific corrections and depth | Per paper (that one: CC BY) |
| R06 | **O'Rahilly & Müller 1987**, *Developmental Stages in Human Embryos* (Carnegie Inst.) | Definition of Carnegie stages (CS01–23) | Historic — reference |
| R08 | **NMHM Human Developmental Anatomy Center stage table** (National Museum of Health and Medicine, custodian of the Carnegie Collection; medicalmuseum.health.mil › HDAC, "Developmental Stages in Human Embryos" table + R06 stage PDFs). Stage → length + age ranges | Day ranges per Carnegie stage for `timeline.json` `cs` and GLOSSARY §7 (via `tools/indexer/carnegie.json`) | US federal work — likely public domain ≈ (check before any reuse beyond numbers) → numbers cited, nothing copied |
| R07 | **EHDAA2** human developmental anatomy ontology (Bard 2012; OBO Foundry; github.com/obophenotype/human-developmental-anatomy-ontology). ~14,000 structure/stage/"develops from" facts, CS1–20. Inactive since ~2022. Related: **Uberon** (cross-species anatomy), **HsapDv** (human stages) | K1 skeleton: concept ids, part-of and develops-from links, stage ranges, synonyms. Map to book sections; book wins on conflict | CC BY 4.0 → may import data, credited |

### R05 papers in use (Tier 1; cite as `R05a` etc.; facts only, own words — licence decides any reuse)
| Id | Paper | Used for | Licence → our use |
|---|---|---|---|
| R05a | de Bree K, de Bakker BS, Oostra RJ. The development of the human notochord. *PLoS ONE* 2018;13:e0205752. doi:10.1371/journal.pone.0205752 · PMID 30346967 | Notochord order/timing (⚑ D-029); neurenteric canal; prechordal plate; CS day ranges | CC BY 4.0 → may adapt with credit |
| R05b | Tyser RCV et al. Single-cell transcriptomic characterization of a gastrulating human embryo. *Nature* 2021;600:285–289. doi:10.1038/s41586-021-04158-y · PMID 34789876 | Human gastrula at CS7 (16–19 d): cell types present | © Springer Nature (author manuscript in PMC) → facts only |
| R05c | Cui L et al. Spatial transcriptomic characterization of a Carnegie stage 7 human embryo. *Nat Cell Biol* 2025;27:360–369. doi:10.1038/s41556-024-01597-3 | AVE present in human CS7; early mesoderm subtypes | © Springer Nature → facts only |
| R05d | Xiao Z et al. 3D reconstruction of a gastrulating human embryo. *Cell* 2024;187:2855–2874. doi:10.1016/j.cell.2024.03.041 | CS8 3D reference (signalling centres) — not yet used for a mark | © Elsevier → facts only |
| R05e | Kwon GS, Viotti M, Hadjantonakis AK. The endoderm of the mouse embryo arises by dynamic widespread intercalation of embryonic and extraembryonic lineages. *Dev Cell* 2008;15:509–520. doi:10.1016/j.devcel.2008.07.017 · PMID 18854136 | ✚ (mouse) — old layer cells mix into gut endoderm; label species | © Elsevier (author manuscript in PMC) → facts only |
| R05f | O'Rahilly R, Müller F. Developmental stages in human embryos: revised and new measurements. *Cells Tissues Organs* 2010;192:73–84. doi:10.1159/000289817 | Stage ≠ age; ages are estimates (D-030) | © Karger → abstract facts only |
| R05g | Swamy R, Embleton N, Hale J. Sacrococcygeal teratoma over two decades. *Prenat Diagn* 2008;28:1048–51. doi:10.1002/pd.2122 | SCT birth prevalence ~1 in 27,000 (⚑ D-030) | © Wiley → facts only |
| R05h | Hambraeus M et al. Sacrococcygeal teratoma: a population-based study. *J Pediatr Surg* 2016;51:481–5. doi:10.1016/j.jpedsurg.2015.09.007 | SCT ~1 in 14,000 (southern Sweden) | © Elsevier → facts only |
| R05i | Ayed A et al. Sacrococcygeal teratoma, West Midlands 1995–2012. *Prenat Diagn* 2015;35:1037–47. doi:10.1002/pd.4641 | SCT 0.30 per 10,000 births; mostly diagnosed prenatally | © Wiley → facts only |
| R05j | Breuer K et al. Exome sequencing in cardiovascular laterality defects. *Eur J Hum Genet* 2022;30:946–954. doi:10.1038/s41431-022-01100-2 · PMID 35474353 | Laterality defects ~1.1/10,000; mostly with complex CHD | Open access in PMC (licence ≈ check before reuse) → facts only |
| R05k | Huybrechts KF et al. Antidepressant use in pregnancy and the risk of cardiac defects. *N Engl J Med* 2014;370:2397–407. doi:10.1056/NEJMoa1312828 · PMID 24941178 | SSRIs: no substantial heart-defect increase after adjustment (⚑ D-030) | © MMS (PMC author manuscript) → facts only |
| R05l | O'Rahilly R, Müller F. The two sites of fusion of the neural folds and the two neuropores in the human embryo. *Teratology* 2002;65:162–70. doi:10.1002/tera.10007 · PMID 11948562 | Neural-fold fusion starts in the hindbrain region and runs both ways (✔✔); second forebrain site (✚); neuropores (Ch 6) | © Wiley → facts only |
| R05m | O'Rahilly R, Müller F. Somites, spinal ganglia, and centra … in staged human embryos. *Cells Tissues Organs* 2003;173:75–92. doi:10.1159/000068948 · PMID 12649586 | Somite counts define CS9–12; 4 occipital; max 38–39 somites (⚑ D-039 a); sclerotome from CS10; spinal crest from CS11; caudal neuropore at future S2 | © Karger → facts only |
| R05n | Müller F, O'Rahilly R. Somitic-vertebral correlation and vertebral levels in the human embryo. *Am J Anat* 1986;177:3–19. doi:10.1002/aja.1001770103 · PMID 3535481 | 4 occipital + 8 cervical-region somites; 38–39 units by CS17 | © Wiley → facts only |
| R05o | Ivanovs A et al. Highly potent human haematopoietic stem cells first emerge in the intraembryonic aorta-gonad-mesonephros region. *J Exp Med* 2011;208:2417–27. doi:10.1084/jem.20111688 · PMID 22042975 | Definitive HSCs first in the AGM dorsal aorta (✔✔ Ch 6) | Open in PMC (JEM licence ≈ check before reuse) → facts only |
| R05p | Charbord P, Tavian M, Humeau L, Péault B. Early ontogeny of the human marrow from long bones. *Blood* 1996;87:4109–19. PMID 8639768 | Marrow blood formation from ~10.5–15 weeks (⚑ D-039 d) | © ASH → facts only |
| R05q | Matsuda M et al. Recapitulating the human segmentation clock with pluripotent stem cells. *Nature* 2020;580:124–9. doi:10.1038/s41586-020-2144-9 · PMID 32238941 | ✚ human clock period ~5 h (in vitro); HES7, DKK1 | © Springer Nature → facts only |
| R05r | Kilcline C, Frieden IJ. Infantile hemangiomas: how common are they? *Pediatr Dermatol* 2008;25:168–73. doi:10.1111/j.1525-1470.2008.00626.x · PMID 18429772 | Old incidence figures unreliable (⚑ D-039 e) | © Wiley → facts only |
| R05s | Munden A et al. Prospective study of infantile haemangiomas. *Br J Dermatol* 2014;170:907–13. doi:10.1111/bjd.12804 · PMID 24641194 | IH incidence 4.5 % in a prospective birth cohort (⚑ D-039 e) | PMC author manuscript → facts only |
| R05t | MRC Vitamin Study Research Group. Prevention of neural tube defects. *Lancet* 1991;338:131–7. PMID 1677062 | Folic acid: 72 % fewer recurrent NTDs (RCT) | © Elsevier → facts only |
| R05u | Czeizel AE, Dudás I. Prevention of the first occurrence of neural-tube defects by periconceptional vitamin supplementation. *N Engl J Med* 1992;327:1832–5. doi:10.1056/NEJM199212243272602 · PMID 1307234 | First-occurrence NTDs prevented (RCT) | © MMS → facts only |
| R05v | Williams J et al. Updated estimates of NTDs prevented by mandatory folic acid fortification — United States, 1995–2011. *MMWR* 2015;64:1–5. PMID 25590678 | Fortification lowered and holds US NTD prevalence | US federal work, likely public domain ≈ → facts only |
| R05w | Kibar Z et al. Mutations in VANGL1 associated with neural-tube defects. *N Engl J Med* 2007;356:1432–7. doi:10.1056/NEJMoa060651 · PMID 17409324 | VANGL1 (planar cell polarity) mutations in NTD families | © MMS → facts only |
| R05x | Bhide P et al. Systematic review of birth prevalence of NTDs in India. *Birth Defects Res A* 2013;97:437–43. doi:10.1002/bdra.23153 · PMID 23873811 | ✚ India NTD birth prevalence ~4.1/1,000 | © Wiley → facts only |
| R05y | Sinha A et al. Burden of NTDs in India: systematic review and meta-analysis. *Childs Nerv Syst* 2024;40:4123–35. doi:10.1007/s00381-024-06627-x · PMID 39365302 | ✚ India pooled ~9.5/1,000 (very heterogeneous) | Open access in PMC (licence ≈) → facts only |
| R05z | Mekonen HK, Hikspoors JPJM, Mommen G, Köhler SE, Lamers WH. Development of the ventral body wall in the human embryo. *J Anat* 2015. doi:10.1111/joa.12380 · PMID 26467243 | Human 3D, CS15–23: body-wall muscles, ribs, sternum spread ventrally; "closure" by differential growth (⚑ D-043 a); sternal bars fuse after CS20 (✚) | Open access in PMC (licence ≈ check before reuse) → facts only |
| R05aa | Merrell AJ et al. Muscle connective tissue controls development of the diaphragm and is a source of congenital diaphragmatic hernias. *Nat Genet* 2015. doi:10.1038/ng.3250 · PMID 25807280 | **Mouse:** pleuroperitoneal folds make the central tendon + muscle connective tissue; Gata4 fibroblast defects → CDH (✔✔ Ch 7, label species) | © Springer Nature (PMC author manuscript) → facts only |
| R05ab | McGivern MR, Best KE, Rankin J et al. Epidemiology of congenital diaphragmatic hernia in Europe: a register-based study. *Arch Dis Child Fetal Neonatal Ed* 2015. doi:10.1136/archdischild-2014-306174 · PMID 25411443 | CDH 2.3 / 10,000 births (EUROCAT, 12 million births) (⚑ D-043 b) | © BMJ → facts only |
| R05ac | Politis MD et al. Prevalence and mortality in children with congenital diaphragmatic hernia: a multicountry study. *Ann Epidemiol* 2021. doi:10.1016/j.annepidem.2020.11.007 · PMID 33253899 | CDH 2.6 / 10,000 (19 countries); mortality ~38 % (⚑ D-043 b) | PMC author manuscript → facts only |
| R05ad | Burgos CM, Frenckner B, Luco M et al. (CDH Study Group). Right versus left congenital diaphragmatic hernia — what's the difference? *J Pediatr Surg* 2017. doi:10.1016/j.jpedsurg.2017.10.027 · PMID 29122292 | 84 % of 3,754 CDH left-sided | © Elsevier → facts only |
| R05ae | Feldkamp ML, Canfield MA, Krikov S et al. Gastroschisis prevalence patterns in 27 surveillance programs from 24 countries, ICBDSR, 1980–2017. *Birth Defects Res* 2024. doi:10.1002/bdr2.2306 · PMID 38411327 | Gastroschisis 3.06 / 10,000; rising; highest in mothers < 20 | Open access in PMC (licence ≈) → facts only |
| R05af | Mastroiacovo P et al. Gastroschisis and associated defects: an international study. *Am J Med Genet A* 2007. doi:10.1002/ajmg.a.31607 · PMID 17357116 | 14.1 % non-isolated; chromosomal rare | © Wiley → facts only |
| R05ag | Nembhard WN, Bergman JEH, Politis MD et al. A multi-country study of prevalence and early childhood mortality among children with omphalocele. *Birth Defects Res* 2020. doi:10.1002/bdr2.1822 · PMID 33067932 | Omphalocele 2.6 / 10,000; ~1/3 die by early childhood | Open access in PMC (licence ≈) → facts only |
| R05ah | Williams AP, Marayati R, Beierle EA. Pentalogy of Cantrell. *Semin Pediatr Surg* 2019. doi:10.1053/j.sempedsurg.2019.04.006 · PMID 31072457 | Five components of Cantrell pentalogy | PMC author manuscript → facts only |
| R05ai | Nakamura T, Yamada S et al. Three-dimensional morphogenesis of the omental bursa from four recesses in staged human embryos. *J Anat* 2020;237:166–75. doi:10.1111/joa.13174 · PMID 32064626 | Human CS13–21: diaphragm cuts off the infracardiac bursa at CS17–18 (diaphragm staging) | Open access in PMC (licence ≈) → facts only |
| R05aj | Hayashi S et al. Pleuroperitoneal canal closure and the fetal adrenal gland. *Anat Rec* 2011. doi:10.1002/ar.21351 · PMID 21370493 | ✚ final canal closure behind the adrenal by lateral spreading (human, CRL 11–40 mm) | © Wiley → facts only |
| R05ak | Godlewski G et al. Liver development in the rat and in man during the embryonic period (Carnegie stages 11–23). *Microsc Res Tech* 1997;39:314–27. PMID 9407542 | Septum transversum gives liver stroma from CS12 | © Wiley → facts only |
| R05al | Neo DT, Martin CL, Carmichael SL. Are individual-level risk factors for gastroschisis modified by neighborhood-level socioeconomic factors? *Birth Defects Res* 2023. doi:10.1002/bdr2.2224 · PMID 37439400 | Young maternal age and low/normal BMI = strong gastroschisis risk factors | PMC author manuscript → facts only |
| R05am | Feldkamp ML, Botto LD, Amar E et al. Cloacal exstrophy: an epidemiologic study from the ICBDSR. *Am J Med Genet C* 2011. doi:10.1002/ajmg.c.30317 · PMID 22002951 | ✚ cloacal exstrophy ~1 in 130,000; ~55 % with omphalocele | © Wiley → facts only |
| R05an | Syngelaki A et al. Diagnosis of fetal non-chromosomal abnormalities on routine ultrasound examination at 11–13 weeks' gestation. *Ultrasound Obstet Gynecol* 2019. doi:10.1002/uog.20844 · PMID 31408229 | ✚ first-trimester scan detects gastroschisis, exomphalos, ectopia cordis, Cantrell | © Wiley → facts only |
| R05ao | Hikspoors JPJM et al. The development of the dorsal mesentery in human embryos and fetuses. *Semin Cell Dev Biol* 2019;92:18–26. doi:10.1016/j.semcdb.2018.08.009 · PMID 30142441 | Continuous dorsal mesentery; widest at stomach + duodenum (✔✔ Ch 7) | © Elsevier → facts only |
| R05ap | Jukic AM, Baird DD, Weinberg CR, McConnaughey DR, Wilcox AJ. Length of human pregnancy and contributors to its natural variation. *Hum Reprod* 2013;28:2848–55. doi:10.1093/humrep/det297 · PMID 23922246 | Median ovulation → birth 268 d (✔✔ Ch 8 birth timing); natural range ~37 d | PMC open access (licence ≈) → facts only |
| R05aq | Wilcox AJ, Weinberg CR, Baird DD. Timing of sexual intercourse in relation to ovulation. *N Engl J Med* 1995;333:1517–21. doi:10.1056/NEJM199512073332301 · PMID 7477165 | Conception only from a 6-day window ending on ovulation day | © NEJM → facts only |
| R05ar | Robinson HP, Fleming JE. A critical evaluation of sonar "crown-rump length" measurements. *Br J Obstet Gynaecol* 1975;82:702–10. doi:10.1111/j.1471-0528.1975.tb00710.x · PMID 1182090 | CRL dating ±4.7 d (one scan), ±2.7 d (three) — ⚑ D-044 b | © Wiley → facts only |
| R05as | Selbing A, Fjällbrant B. Accuracy of conceptual age estimation from fetal crown-rump length. *J Clin Ultrasound* 1984;12:343–6. doi:10.1002/jcu.1870120606 · PMID 6438162 | CRL vs known insemination date: −7 to +4 d (5th–95th) | © Wiley → facts only |
| R05at | Gordijn SJ et al. Consensus definition of fetal growth restriction: a Delphi procedure. *Ultrasound Obstet Gynecol* 2016;48:333–9. doi:10.1002/uog.15884 · PMID 26909664 | FGR vs SGA definitions (size + Doppler/growth signs) | © Wiley → facts only |
| R05au | Woods KA, Camacho-Hübner C, Savage MO, Clark AJ. IUGR and postnatal growth failure associated with deletion of the IGF-I gene. *N Engl J Med* 1996;335:1363–7. doi:10.1056/NEJM199610313351805 · PMID 8857020 | IGF1 deletion → IUGR (human case) | © NEJM → facts only |
| R05av | Barker DJ. Fetal origins of coronary heart disease. *BMJ* 1995;311:171–4. doi:10.1136/bmj.311.6998.171 · PMID 7613432 | Fetal-origins (Barker) hypothesis | PMC (licence ≈) → facts only |
| R05aw | Goldenberg RL, Culhane JF, Iams JD, Romero R. Epidemiology and causes of preterm birth. *Lancet* 2008;371:75–84. doi:10.1016/S0140-6736(08)60074-4 · PMID 18177778 | Preterm definition, routes, US 12–13 %, risk factors | © Elsevier → facts only |
| R05ax | Ohuma EO et al. National, regional, and global estimates of preterm birth in 2020. *Lancet* 2023;402:1261–71. doi:10.1016/S0140-6736(23)00878-4 · PMID 37805217 | ✚ 9.9 % of births preterm worldwide (2020) | © Elsevier (check OA) → facts only |
| R05ay | Abalos E et al. Global and regional estimates of preeclampsia and eclampsia: a systematic review. *Eur J Obstet Gynecol Reprod Biol* 2013;170:1–7. doi:10.1016/j.ejogrb.2013.05.005 · PMID 23746796 | Preeclampsia 4.6 % of deliveries (2.7–8.2 %) | © Elsevier → facts only |
| R05az | Zhou Y, Damsky CH, Fisher SJ. Preeclampsia is associated with failure of human cytotrophoblasts to mimic a vascular adhesion phenotype. *J Clin Invest* 1997;99:2152–64. doi:10.1172/JCI119388 · PMID 9151787 | Endovascular cytotrophoblast switch; fails in preeclampsia | PMC open access (licence ≈) → facts only |
| R05ba | Costea DM, Gunn LK, Hargreaves C, Howell RJ, Chard T. Delayed luteo-placental shift of progesterone production in IVF pregnancy. *Int J Gynaecol Obstet* 2000;68:123–9. doi:10.1016/s0020-7292(99)00177-0 · PMID 10717816 | Placental progesterone share rises 4–9 wk after conception (normal pregnancies) — ⚑ D-044 a | © Elsevier → facts only |
| R05bb | Simister NE. Placental transport of immunoglobulin G. *Vaccine* 2003;21:3365–9. doi:10.1016/s0264-410x(03)00334-7 · PMID 12850341 | Fetal IgG rises from early 2nd trimester, most in 3rd; FcRn | © Elsevier → facts only |
| R05bc | Palmeira P et al. IgG placental transfer in healthy and pathological pregnancies. *Clin Dev Immunol* 2012:985646. doi:10.1155/2012/985646 · PMID 22235228 | Only IgG crosses; FcRn on syncytiotrophoblast | Open access (CC BY ≈) → facts only |
| R05bd | Legler TJ. RhIg for the prevention of Rh immunization and IVIg for the treatment of affected neonates. *Transfus Apher Sci* 2020;59:102950. doi:10.1016/j.transci.2020.102950 · PMID 33004277 | Ante- + postnatal anti-D cut HDFN; targeted prophylaxis by fetal RhD | © Elsevier → facts only |
| R05be | Brace RA, Wolf EJ. Normal amniotic fluid volume changes throughout pregnancy. *Am J Obstet Gynecol* 1989;161:382–8. doi:10.1016/0002-9378(89)90527-9 · PMID 2764058 | Volume nomogram 8–43 wk; plateau ~780 mL (22–39 wk) | © Elsevier → facts only |
| R05bf | Thummala MR, Raju TN, Langenberg P. Isolated single umbilical artery anomaly and the risk for congenital malformations: a meta-analysis. *J Pediatr Surg* 1998;33:580–5. doi:10.1016/s0022-3468(98)90320-7 · PMID 9574755 | SUA 0.55 % of live-born; 27 % with a malformation | © Elsevier → facts only |
| R05bg | Voskamp BJ et al. Relationship of isolated single umbilical artery to fetal growth, aneuploidy and perinatal mortality. *Ultrasound Obstet Gynecol* 2013;42:622–8. doi:10.1002/uog.12541 · PMID 23775879 | ✚ isolated SUA: no extra aneuploidy | © Wiley → facts only |
| R05bh | Jauniaux E, Bunce C, Grønbeck L, Langhoff-Roos J. Prevalence and main outcomes of placenta accreta spectrum: a systematic review and meta-analysis. *Am J Obstet Gynecol* 2019;221:208–18. doi:10.1016/j.ajog.2019.01.233 · PMID 30716286 | ✚ accreta spectrum 0.17 % of births; hysterectomy ~52 % | © Elsevier → facts only |
| R05bi | Wee LY, Fisk NM. The twin-twin transfusion syndrome. *Semin Neonatol* 2002;7:187–202. doi:10.1053/siny.2002.0106 · PMID 12234743 | TTTS 10–15 % of monochorionic twins; AV anastomoses | © Elsevier → facts only |
| R05bj | Hoekstra C et al. Dizygotic twinning. *Hum Reprod Update* 2008;14:37–47. doi:10.1093/humupd/dmm036 · PMID 18024802 | Twins ~13 / 1,000 maternities; MZ rate ~constant, DZ varies — ⚑ D-044 c | © OUP → facts only |
| R05bk | Jin H, Han Y, Zenker J. Cellular mechanisms of monozygotic twinning: clues from assisted reproduction. *Hum Reprod Update* 2024;30:692–705. doi:10.1093/humupd/dmae022 · PMID 38996087 | ✚ MZ chorionicity vs split timing; dichorionic MZ after blastocyst transfer | PMC open access (licence ≈) → facts only |

## Tier 2 — other textbooks (confirm only)
| Id | Source | Use |
|---|---|---|
| R10 | Moore, Persaud & Torchia, *The Developing Human* | Second opinion on any book fact; clinical correlates |
| R11 | Schoenwolf et al., *Larsen's Human Embryology* | Molecular / mechanism depth for Tier D |
| R12 | Gilbert, *Developmental Biology* 6e (NCBI Bookshelf, free, search-only) | Mechanisms (signalling, gastrulation movements) — mostly non-human models; label species |

Tier 2 can raise ✔ to ✔✔ only when it states the same fact independently. It can't create ⚑ or ✚ on its own.

## Tier 3 — teaching references (how to explain; not a fact source)
| Id | Source | Use | Licence |
|---|---|---|---|
| R20 | **UNSW Embryology** (Dr Mark Hill) — large free site; Carnegie stage table, timelines, collections | Sequencing ideas, stage overview, "one-minute" summaries as a length benchmark | Educational only, no reuse without permission → reference only |
| R21 | **OpenStax Anatomy & Physiology 2e**, ch 28 Development | Plain-language level for Tier A wording | CC BY 4.0 → may adapt with credit |
| R22 | MedEdPORTAL *Embryonic Folding* animated module (Lowrie et al. 2007) | Benchmark for how folding is animated (long + cross sections together) | Reference |

## Curriculum
| Id | Source | Use |
|---|---|---|
| R30 | **NMC Competency Based UG Curriculum for the Indian Medical Graduate, 2024** — Anatomy (AN): 82 topics, 413 competencies; general embryology topics start at 76 (intro, gametogenesis & fertilization, second week…) | Tag every card with its AN code(s) in I1/X1; drives Tier B; coverage gap list. X1 Ch 05 read the AN table from a university reprint (MGMUHS Anatomy CBME 2024, w.e.f. 2024–25). **X1 Ch 07 (20 Nov 2026):** AN79.1–79.6, AN52.4–52.6, AN47.14, AN25.2 read from a copy of NMC *Competency Based UG Curriculum Vol I 2024* (hosted by Amala IMS IQAC) — AN79 wording matches the reprint ✔; other topics confirm per chapter. **X1 Ch 08 (20 Nov 2026):** AN80.1–80.7 read from a teaching-site copy of the AN list (≈ until checked against NMC Vol I with AN81 in Ch 9) |

## Teaching-science sources
Listed with what we took from each in `research/teaching-methods.md` (M01–M08).

## Tools & open-source projects (added 17 Nov 2026, D-018)
All free. **Use** column follows RULES F4/G4: *Repo* = code may be vendored in the repo; *Laptop* = installed on the owner's laptop only (GPL/AGPL/NC or heavy), never copied into the repo; outputs are ours unless noted. Licences checked 17 Nov 2026 — re-check before install. Model choices are decided by M1 measurements, not by this list.

| Id | Tool | Step | Does | Licence → use |
|---|---|---|---|---|
| T01 | **Blender** | M1, V1, P1 | Modelling, animation, Cycles/OptiX + Eevee renders | GPL → Laptop; renders ours |
| T02 | **Blender MCP** (`ahujasid/mcp-for-blender`, was `blender-mcp`) | M1, V1 | Lets Claude drive Blender scenes on the laptop | MIT → Laptop |
| T03 | **three.js** | V1, app | Interactive 3D in cards + headless shots | MIT → Repo (pinned, vendored, D-006) |
| T04 | **glTF-Transform** + **meshoptimizer** | V1 | Shrink .glb for phones | MIT → Laptop build step |
| T05 | **model-viewer** (Google) | app (option) | Quick 3D preview | Apache 2.0 → Repo if used |
| T06 | **Poly Haven** | V1 | HDRIs, textures | CC0 → Repo/renders |
| T07 | **Z-Anatomy** (adult 3D atlas, Blender; from BodyParts3D) | V1, P1 | Adult anatomy for "this becomes…" shots (D4) | CC BY-SA 4.0 (+ BodyParts3D CC BY-SA 2.1 JP) → **rendered video only (D-021)**: video released CC BY-SA 4.0 + credit "Adult anatomy: Z-Anatomy (CC BY-SA 4.0), based on BodyParts3D © DBCLS (CC BY-SA 2.1 JP), modified"; meshes never in repo/app |
| T10 | **Docling** (IBM) | I1 | PDF → headings, sections, tables (local) | MIT → Laptop |
| T11 | **MinerU** | I1 (backup) | Strong on formulas | MinerU licence (Apache 2.0 + extra terms) → Laptop |
| T12 | **PyMuPDF** | I1 | Fast text + outline extraction | AGPL → Laptop |
| T13 | **Cytoscape.js** | K1 explorer | Clickable concept graph, no bundler | MIT → Repo |
| T20 | **Wan 2.2 TI2V-5B** (+ **ComfyUI**) | M1 | Local AI video for backgrounds/transitions; never embryo facts (D5) | Apache 2.0 weights; ComfyUI GPL → Laptop. Wan 2.5+ closed — skip |
| T21 | **RIFE** / **Real-ESRGAN** | P1 | Frame interpolation / upscaling | MIT / BSD → Laptop |
| T22 | **Manim Community** / **Motion Canvas** | P1 | 2D diagrams, labels, timelines | MIT → Laptop |
| T23 | **Remotion** | M1 (compare only) | Video from React | Free for individuals / ≤3 people; needs a bundler (vs C5) → Laptop only |
| T30 | **Kokoro-82M** | M1, P1 | Fast local narration, incl. Hindi | Apache 2.0 → Laptop |
| T31 | **Chatterbox** (Resemble AI) | M1 | Expressive voice + cloning | MIT → Laptop |
| T32 | **Piper** (`OHF-Voice/piper1-gpl`) | M1 | CPU TTS | GPL-3.0; voices licensed per voice → Laptop |
| T33 | **XTTS v2** | — | Voice cloning | Non-commercial (CPML) → Laptop only if ever used, credited (F4) |
| T34 | **WhisperX** | P1 | Word-level subtitle timing (forced alignment) | BSD → Laptop |
| T35 | **ffmpeg** (NVENC) | P1 | Assemble, encode, burn subtitles | LGPL/GPL → Laptop |
| T40 | **ts-fsrs** | app | Spaced-repetition scheduling (FSRS) | MIT → Repo |
| T41 | **Dexie.js** | app | IndexedDB wrapper (`biostudio`, A1) | Apache 2.0 → Repo |
| T42 | **Workbox** | app | Offline caching (PWA) | MIT → Repo |
| T50 | **PubMed** connector | X1 | Tier-1 paper search | Connected |
| T51 | **Hugging Face** connector | M1, X1 | Find models + check licences; paper search | Connected 17 Nov 2026 |

## Not used
Exam-coaching blogs, flashcard decks, YouTube channels, AI-written pages, Wikipedia (may point to a source; never cited).
