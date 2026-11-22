# Research dossier — Ch 16 · Urogenital system (for C-step cards + episodes)

*(Purpose: cited, marked facts, staging, misconceptions and clinical correlates for Ch 16, the seventh chapter of Part 2 — only five sections, but the two big ones (urinary, genital) run 11 and 15 pages with 9 boxes; read in two halves (urinary: kidney systems → metanephros → ascent → bladder and urethra; genital: sex determination → gonads → ducts → external genitalia → descent). Cards draft from this file. Updated: 22 Nov 2026 · Bio · Research · X1 Ch 16 · by Aaditya. Own words only; no book sentences, figures or tables (RULES §G) — every list below is regrouped in our own order (by time, by mechanism or by adult destination), never the book's. Pattern: `ch15-digestive.md`.)*

**How to read a line:** fact in our words · `[book section · registry source]` · mark (RULES B6–B7): **✔✔** book + Tier 1 agree · **✔** book only · **⚑** book vs Tier 1 disagree (D-entry) · **✚** beyond the book (Tier 1 only; More / Tier D only, "beyond Langman") · **≈** blocks final. **Species tag:** a Tier 1 line from mouse, rat or chick says so (*mouse*). Those lines can confirm a mechanism; they never give a human day or number. **Rates** are per 10,000 births unless stated; "total" = live births + stillbirths + terminations.

**Citation check, read before you cite:** checked 22 Nov 2026. `tools/card-check/citations.py` matches `R\d\d[a-z]{0,2}`, so the new ids **R05hg–R05ia** parse. Every PMID was grepped in the registry before its id was given (none was there); author lists copied from the PubMed record (first three, then et al.). R05ed and R05bs stay retired. `sources.json` is rebuilt in this commit (`check.py --write-sources`, D-065 (6)). Registry sources re-used: **R05gk** (human cloaca), **R05am** (cloacal exstrophy, ICBDSR), R06/R08 (stage tables). **Three abstracts were read and not used** (no figure for the claim): Wiesel 2005 EUROSCAN renal (PMID 16053904), Cools 2017 CAIS tumours (PMID 28719895), Barisic 2013 Fraser syndrome (PMID 23532946) — §10.

**Ages — three clocks.** (1) The book's embryonic events are in **weeks after fertilization** (pronephros week 4, metanephros week 5, gonads show their sex in week 7, urethral folds close end of month 3) and in **prenatal months** for fetal events (vagina canalized month 5) — read as after fertilization (D-030). **But its testis-descent numbers are "weeks' gestation"** (inguinal region ~12, canal by 28, scrotum by 33) — the obstetric (last-period) clock, ~2 weeks ahead. (2) Specimen papers give **Carnegie stages** (R05hg) or **weeks post conception** (R05hp); matched to the classic R08 day ranges (`tools/indexer/carnegie.json`: CS14 31–35 d, CS17 42–44, CS20 51–53, CS23 ~56–60). (3) Nephron-count, descent and newborn papers use **gestational age from the last period** (R05hi ~36 wk, R05hj, R05hy 24–28 wk). **R05hh's clock is unclear** — it starts kidney development at "4 weeks of gestation", which only fits post-conception weeks — so it is used for the nephron number only, never for a date. **The book uses "gestation" loosely:** its Leydig-cell "eighth week of gestation" sits among post-fertilization embryonic events and is read as week 8 after fertilization (~CS23); only the descent figures (12/28/33 wk) are read as LMP (D-030). Every card number carries its clock.

**Section locators (checked against the PDF, 22 Nov 2026; printed page = PDF page − 19):**
- **E16.00** p 256 (opener shares the page with E16.01).
- **E16.01 Urinary system pp 256–266** — sub-locators: kidney systems, pronephros p 256; mesonephros pp 256–257; metanephros + collecting system pp 257–259; excretory system (nephron) pp 259–260; *molecular regulation of kidney development* **pp 260–261**; *renal tumours and defects* box **pp 261–262** (dysplasia/agenesis, Potter sequence, polycystic disease, ciliopathies p 261; Wilms p 261; duplicated and ectopic ureter p 262); position of the kidney p 263; function of the kidney p 263; *abnormal location* box **pp 263–264** (pelvic, horseshoe, accessory arteries); bladder and urethra pp 263–266 (cloaca division p 263, urachus and sinus parts p 264, trigone p 266, prostate buds p 266); *bladder defects* box **p 266** (urachal fistula/cyst/sinus, bladder exstrophy, cloacal exstrophy). Range right.
- **E16.02 Genital system pp 267–282** — sub-locators: sex determination p 267; gonads, germ-cell arrival pp 267–268; indifferent gonad p 268; testis pp 268–269; ovary pp 269–270; genital ducts, indifferent stage p 270; male ducts pp 270–272; female ducts p 272; *molecular regulation of genital duct development* **pp 273–274**; vagina p 274 (+ Gartner remnants); *uterine and vaginal defects* box **p 275**; external genitalia, indifferent stage p 276; male pp 276–277; *male genital defects* box **pp 277–278** (hypospadias, epispadias, micropenis, bifid penis); female p 278; *DSD* box **pp 279–280**; descent of the testis pp 278–281; descent of the ovary p 281; *hernias and cryptorchidism* box **p 282**. Recorded 267–281.
- **E16.03** Summary **pp 282–283** (recorded 282 only) · **E16.04** Problems p 283.

**I1 gaps** (tree.json) → I1 to-do:
- **E16.02** ends **p 282**, not 281 — the *hernias and cryptorchidism* box (PDF 301) and the last lines of descent sit on p 282, which I1 also gives to the Summary. I1 lists that box under E16.02 (right) but outside its page range.
- **E16.03** ends p 283, not 282 (the summary's genital half runs onto the Problems page).
- **Four untitled boxes** in I1: E16.01 PDF 285 → *Bladder defects*; E16.02 PDF 294 → *Uterine and vaginal defects*; PDF 296 → *Defects in the male genitalia*; PDF 301 → *Hernias and cryptorchidism*. Cite them as `E16.01 CC` / `E16.02 CC`.
- Unlike Ch 9–15, the two long sections' ranges are right; only the end spills (same two-column shape).

---

## 1. Staging & scale — kidney ridge to newborn (RULES B2)
Human anchors: **R05hg** (3D reconstructions, 28 *human* embryos CS14–23, Carnegie + French collections), **R05hh** (135 *human* kidney specimens 4–23 wk), **R05hi/R05hj** (*human* nephron counts), **R05gk** (*human* cloaca 4–10 wk, Ch 15), **R05hp** (*human* germ cells 5–14 wk post conception), **R05ho** (*human* SRY/SOX9/DAX1), **R05hr** (*human* female tract 5–22 wk), **R05hu/R05ht** (*human* fetal phallus 5–22 wk), **R05hy** (178 *human* fetuses, descent). Days are the book's unless a source is named.

| When | Carnegie / clock | What happens `[section · source]` | Mark |
|---|---|---|---|
| Start of week 4 → end of week 4 | ~CS10–12 | **Pronephros**: 7–10 solid cell groups in the neck region, never working, gone by the end of week 4 `[E16.01]` | ✔ (no human source retrieved) |
| Week 4 → end of month 2 | ~CS11 → fetal | **Mesonephros**: tubules with glomeruli from upper thoracic to L3 level; drain into the **mesonephric (Wolffian) duct**; mid-month 2 a big oval organ beside the gonad (urogenital ridge); most tubules gone by the end of month 2 `[E16.01]` | ✔ |
| Weeks 3–4 → early week 5 | — (weeks post conception) | **Germ cells**: yolk-sac wall from 3–4 wk, in the hindgut lining from wk 4, in the gonad area from early wk 5; from 6 wk they travel along nerve fibres through the dorsal mesentery `[E16.02 · R05hp]` | **✔✔** (book: arrive start of wk 5, invade wk 6) · ✚ the nerve-fibre route |
| Week 5 | CS14 | **Metanephros** (the lasting kidney) appears; the **ureteric bud** grows from the mesonephric duct into the metanephric tissue `[E16.01 · R05hg]` | **✔✔** (R05hg: metanephros CS14–23) |
| Weeks 4–7 | ~CS11 → CS19 | **Cloaca** divides: urogenital sinus in front, anorectal canal behind (Ch 15) `[E16.01 · R05gk]` | **✔✔** (R05gk: membrane breaks ~6.5 wk) |
| Weeks 5–8 | CS14 → CS23 | **Kidney ascent** from the pelvis to the lumbar region; first blood supply from the iliac arteries (8 of 9 embryos) or the IMA, the final renal artery may be new growth from the aorta (capillary cluster in 2 embryos, CS21–22) `[E16.01 · R05hg]` | ✔✔ ascent · **⚑ how the arteries change** (D-076 i) |
| Week 6 | ~CS16–17 | **Indifferent gonad** with primitive sex cords; both duct pairs present (paramesonephric duct forms beside the mesonephric) `[E16.02]` | ✔ |
| Week 7 | ~CS18–20 | **Gonad shows its sex**: testis cords + tunica albuginea in XY; SRY rises as the sex cords form `[E16.02 · R05ho]` | ✔ week (book) · **✔✔** SRY with sex-cord formation (R05ho) |
| Week 8 | ~CS23 | **Leydig cells** start testosterone; Sertoli cells make AMH → paramesonephric ducts regress in XY `[E16.02]` | ✔ |
| Week 10 → 12 | fetal | Glomerular capillaries from wk 10; **urine from wk 12** into the amniotic fluid `[E16.01]` | ✔ (no human source retrieved) |
| End of month 3 | fetal | **Urethral folds close** over the urethral plate → penile urethra; human specimens show canalization of the plate (opening zipper, ~8–16 weeks of gestation) then fusion of the folds (closing zipper, under way proximally by ~9.5–11 weeks) `[E16.02 · R05hu]` | ✔✔ fusion · ✔ timing (R05hu full text: weeks of gestation estimated from heel–toe length; the paper also says "weeks fetal age" for the same specimens; no week for the end of closure) · **⚑ the glans part** (D-076 b) |
| Month 3 | fetal | **Ovary**: cortical cords split into primordial follicles around oogonia `[E16.02]` | ✔ |
| Month 5 (book) · by 21 wk of gestation (R05hr, heel–toe "gestational" age; ≈ 19 wk after fertilization if last-period based) | fetal | **Vaginal plate canalized**; in the one intact 21-wk specimen, the whole lining carries the sinus marker (FOXA1) `[E16.02 · R05hr]` | ✔✔ timing · **⚑ origin** (D-076 a) |
| ~12 wk gestation (LMP) | fetal | Testis at the inner inguinal ring `[E16.02]` | ✔ |
| 24–28 wk gestation (LMP) | fetal | **Testis passes the inguinal canal** — fast: 75 % of testes go through between 24 and 28 wk `[E16.02 · R05hy]` | **✔✔** (book: by 28 wk) |
| ~33 wk gestation | fetal | Testis in the scrotum `[E16.02]` | ✔ |
| ~36 wk gestation (LMP) | fetal | **Last nephrons form**; count plateaus ~36 wk `[E16.01 · R05hi, R05hj]` | **⚑** (D-076 c — book: until birth) |
| Birth | — | ~**1 million nephrons** per kidney (range ~200,000 to >2.5 million); 97 % of boys have both testes down (Finland 2.4 % not; Denmark 9 %) `[E16.01, E16.02 CC · R05hi, R05hz]` | **✔✔** nephrons · ✔✔ testes with note (varies by country) |

**Scale for scenes (B2):** CS14 embryo ~5–7 mm; ascent-phase embryo CS17–23 ~11–30 mm (R08 ranges); the 7-week gonad is a ridge a fraction of a millimetre wide — "not to scale" whenever it is enlarged beside the kidney. Descent shots are fetal (≥ 12 wk gestation): label "weeks of pregnancy".

---

## 2. Tier A facts — cited and marked
### E16.00.01 Three kidney systems · AN52.7
- **One ridge, three kidneys in a row.** All come from **intermediate mesoderm** along the back wall, head end first, each overlapping the last: **pronephros** (neck, never works, gone by the end of week 4) → **mesonephros** (chest to upper lumbar, may work briefly) → **metanephros** (pelvis, week 5, the **permanent kidney**). `[E16.01, E16.03]` **✔** · ✔✔ for the metanephros at CS14 (R05hg)
- **What survives from each:** pronephros — nothing; mesonephros — its **duct** and some tubules become male genital ducts (and vestiges in the female); metanephros — the kidney. `[E16.01, E16.02]` **✔**
- **Urinary and genital systems share a start:** the same ridge, and at first both drain into the cloaca. `[E16.00, E16.03]` **✔**

### E16.01.02 Metanephros: two sources · AN52.7, AN52.2
- **Two tissues, one kidney.** The **ureteric bud** (from the mesonephric duct) makes the **collecting system**: ureter, pelvis, major and minor calyces, collecting ducts. The **metanephric blastema** (mesoderm capping each bud tip) makes the **nephrons**: Bowman capsule through the distal tubule. `[E16.01]` **✔** (book; R05hh's abstract confirms human–mouse differences in timing, lobes and niche layout but not the two origins — full text, §10)
- **They need each other.** The bud only branches inside blastema; the blastema only makes nephrons where a bud tip touches it. No contact → no kidney (agenesis). `[E16.01, E16.01 CC]` **✔** (mechanism ✔✔ in *mouse*, §3)
- **Branching:** the bud forks into the future major calyces, then keeps forking (about a dozen generations); early generations merge into the minor calyces, later ones stretch into the pyramids. `[E16.01]` **✔**
- **When it stops.** Book: nephrons form until birth (~1 million per kidney); none are added after. Human counts: no new nephrons after **~36 weeks of pregnancy** (R05hi; count plateaus at 36 wk, R05hj); average ~0.9–1 million, range ~200,000 to >2.5 million; low birth weight → fewer `[E16.01 · R05hh, R05hi, R05hj]` **✔✔** number · **⚑ end point** (D-076 c)

### E16.02.01 Sex determination · AN52.8
- **The switch is on the Y.** **SRY** (short arm of Y) makes a transcription factor — the testis-determining factor — that tips the gonad into a testis. `[E16.02]` **✔✔** (R05ho: SRY in XY gonads as the sex cords form; R05hq)
- **The ovary is not "nothing happening".** Ovary development needs its own genes — **WNT4** (with DAX1, which opposes SOX9). `[E16.02 MR · R05hq, R05ho]` **✔✔** (R05hq: female development "cannot be considered a default"; R05ho: DAX1 before SRY's peak)
- **Genetic sex at fertilization; visible gonadal sex in week 7.** `[E16.02]` **✔** (book; R05ho gives no week — only that SRY rises as the sex cords form, ✔✔ for that; its "18 wk" is weeks of gestation)
- **Downstream of SRY: SOX9 → SF1 → Sertoli + Leydig cells; FGF9** draws mesonephric cells into the ridge. `[E16.02 MR]` **✔** (mechanism largely *mouse*; ✚ R05ho: in humans SOX9 is also transcribed in the early ovary — high levels mark the testis)

### E16.02.02 Indifferent gonad · AN52.8
- **Genital ridge + germ cells.** Coelomic epithelium thickens over mesenchyme medial to the mesonephros and sends in **primitive sex cords**; until week 7 an XX and an XY gonad look the same. `[E16.02]` **✔**
- **Germ cells come from outside.** Made in the epiblast, parked in the yolk-sac wall by week 3, they move through the hindgut lining and dorsal mesentery and reach the ridges **early week 5**, entering them in week 6. Without them the gonad does not form. `[E16.02 · R05hp]` **✔✔** (*human*: yolk sac 3–4 wk, hindgut wk 4, gonad area early wk 5) · ✚ from 6 wk they follow sympathetic nerve fibres; strays may give extragonadal germ-cell tumours (R05hp)

### E16.02.05 Genital ducts: two sets · AN52.8
- **Everyone starts with both.** Mesonephric (Wolffian) and paramesonephric (Müllerian) ducts are present in both sexes at week 6. `[E16.02]` **✔**
- **Two testis hormones, two jobs.** **Testosterone** (Leydig cells, from week 8) **keeps and builds** the mesonephric duct → efferent ductules, epididymis, ductus deferens, seminal vesicle, ejaculatory duct. **AMH** (Sertoli cells) **removes** the paramesonephric duct (leaving the appendix testis). `[E16.02, E16.02 MR · R05hq]` **✔✔**
- **No testis → the reverse.** Without testosterone the mesonephric duct regresses; without AMH the paramesonephric duct becomes uterine tube, uterus, cervix and upper vagina (book: oestrogen helps). `[E16.02, E16.03 · R05hq]` **✔✔** AMH removes the Müllerian ducts (R05hq) · ✔ the role of oestrogen (book only)
- **Checks test the two hormones separately** — the commonest exam slip is "testosterone makes the Müllerian ducts regress" (§6).

### E16.02.09 External genitalia · AN52.8, AN46.3
- **One starting kit.** Genital tubercle, urethral (cloacal) folds and genital swellings; at the end of week 6 the sexes cannot be told apart. `[E16.02]` **✔**
- **DHT, not testosterone, shapes the male form.** Testosterone is turned into **dihydrotestosterone** by 5α-reductase in the target tissue; DHT receptors drive the phallus, urethra and scrotum. `[E16.02 MR, E16.02]` **✔✔** (R05hq: 5α-reductase type 2 in genital skin and urogenital sinus)
- **Homologues, grouped by what fuses in the male:** *fused in the male, open in the female* — urethral folds → **penile urethra / labia minora** (✔✔ R05hu), genital swellings → **scrotum / labia majora**, urogenital groove → closed urethra / **vestibule**; *one part that grows more in the male* — tubercle → **penis / clitoris**. `[E16.02, E16.03 · R05hu]` ✔✔ folds · ✔ the rest
- **How the urethra closes.** Folds close over the endodermal **urethral plate** by the end of month 3 (book). *Human* specimens: the plate first **canalizes** into a groove, then the folds **fuse** ventrally. `[E16.02 · R05hu, R05ht]` **✔✔** · **⚑ the glans segment** (D-076 b: book — an ectodermal cord from the glans tip; R05ht — no ectodermal ingrowth, the whole urethra including the glans is endodermal plate)
- **Ultrasound trap:** early in the fetal period the tubercle is as big or bigger in females, so tubercle length misleads in months 3–4. `[E16.02]` **✔**

### E16.02.12 Descent of the testis · AN46.1, AN44.4, AN52.8
- **Starts high, ends outside.** The testis forms behind the peritoneum at lumbar level and must cross the abdominal wall. `[E16.02]` **✔**
- **The guide: the gubernaculum** — a jelly-like band from the lower pole to the inguinal region. It swells (grows in length, mass and water) just before the testis passes through; the testis then crosses the canal quickly. `[E16.02 · R05hy]` **✔✔** (*human*, 178 fetuses)
- **Timeline (weeks of pregnancy):** at the inguinal region ~12 wk, through the canal by 28 wk (*human*: 75 % between 24 and 28 wk), in the scrotum by ~33 wk. `[E16.02 · R05hy]` **✔✔**
- **What makes it move (book: not fully clear):** gubernaculum outgrowth, rising abdominal pressure, then gubernacular regression; androgens and AMH influence it. `[E16.02]` **✔** (R05hy supports growth of the gubernaculum as the key step)
- **It keeps its lumbar blood supply** — the testicular artery stays an aortic branch from kidney level. `[E16.02]` **✔**
- **Wrappings, outside in (as a surgeon meets them):** external spermatic fascia ← external oblique; cremaster muscle + fascia ← internal oblique; internal spermatic fascia ← transversalis fascia; tunica vaginalis ← processus vaginalis (peritoneum). The transversus abdominis gives **no layer** (it arches over the path). `[E16.02]` **✔** (anatomy, AN44.4/AN46.1)

---

## 3. Tier B–D facts (cards later; marked now)
**Grouped by adult destination — the kidney, the lower urinary tract, the testis line, the ovary line — then the molecular layer; not the book's order.**

| Concept | Fact (our words) | Cite | Mark |
|---|---|---|---|
| **The kidney** | | | |
| E16.01.01 Mesonephros and its duct (B) · AN52.7 | Tubules form an S-loop with a glomerulus and Bowman capsule, draining sideways into the mesonephric duct; head-end tubules regress while tail-end ones are still forming; by end of month 2 most are gone. In males caudal tubules + the duct join the genital system. | `[E16.01]` | ✔ |
| E16.01.03 Nephron formation (B) · AN52.7, AN52.2 | Under each new collecting-duct tip the cap cells form a **renal vesicle → S-shaped tubule**; capillaries fill one end (glomerulus); the far end opens into the collecting duct; the tubule lengthens into proximal tubule, loop of Henle and distal tubule. Glomerular capillaries from wk 10, urine from wk 12; lobulation at birth fades in infancy by nephron growth, not new nephrons. | `[E16.01]` | ✔ (book) · **⚑** end of nephrogenesis (D-076 c) |
| E16.01.04 Kidney ascent (B) · AN52.7, AN47.5 | The kidney "rises" from the pelvis mainly because the body grows below it and uncurls; its arteries come from ever higher levels, lower ones usually vanish — leftovers = **accessory renal arteries** to the poles. Fetal kidneys are not needed for waste removal (the placenta does it); urine makes amniotic fluid. | `[E16.01 · R05hg]` | ✔✔ ascent CS14–23 · **⚑** the ladder model (D-076 i) |
| E16.01.08 Molecular regulation (D) · AN52.7 | Blastema: **WT1** makes it able to respond; it sends **GDNF** (→ RET on the bud) and **HGF** (→ MET) → bud grows and branches. Bud sends **FGF2, BMP7** (keep the cap alive, dividing) and **WNT9B, WNT6** → **PAX2** (condense) and **WNT4** (become epithelium, make tubules); matrix switches to laminin + collagen IV; E-cadherin, syndecan appear. | `[E16.01 MR]` | ✔ (*mouse* mechanism; R05hh: some human marker patterns differ) |
| **The lower urinary tract** | | | |
| E16.01.06 Bladder and urethra (B) · AN52.7, AN48.2, AN49.2 | Urorectal septum splits the cloaca (weeks 4–7); its tip = **perineal body**. Urogenital sinus: upper part → **bladder** (apex tied to the navel by the **urachus → median umbilical ligament**); pelvic part → prostatic + membranous urethra (male) / whole urethra (female); phallic part → penile urethra / vestibule. Mesonephric duct ends are absorbed into the bladder wall → **trigone** (mesoderm at first, later lined by endoderm); ureters open separately and move up, the ducts move down and become ejaculatory ducts. Urethral lining endoderm, muscle + connective tissue splanchnic mesoderm; **prostate** buds from the urethra end of month 3 (female: urethral and paraurethral glands). | `[E16.01 · R05gk]` | ✔ (cloaca ✔✔ R05gk) |
| **The testis line** | | | |
| E16.02.03 Testis (B) · AN52.8, AN46.1, AN52.2 | XY: sex cords run deep → **testis (medullary) cords**, a hilum network → **rete testis**; a thick **tunica albuginea** cuts them off from the surface. Cords = germ cells + **Sertoli** cells (from surface epithelium); **Leydig** cells between them from ridge mesenchyme; testosterone from week 8. Cords stay solid until **puberty** (then seminiferous tubules). | `[E16.02 · R05ho]` | ✔ (✚ R05ho: SRY protein persists in Sertoli cells at 18 wk) |
| E16.02.06 Male ducts and glands (B) · AN52.8, AN46.2, AN48.2 | Epigenital mesonephric tubules → **efferent ductules**; paragenital tubules → **paradidymis**; duct → **epididymis** (coiled), **ductus deferens** (thick muscle), **ejaculatory duct**; top end → **appendix epididymis**; seminal vesicle buds from the duct; **prostate** and bulbourethral glands from the urethra (endoderm). | `[E16.01, E16.02]` | ✔ |
| **The ovary line** | | | |
| E16.02.04 Ovary (B) · AN52.8, AN52.2 | XX: first cords break up and give way to a vascular medulla; the surface keeps growing and sends **cortical cords** (week 7) that split (month 3) into clusters → **primordial follicles** (oogonium + follicular cells). No tunica albuginea. | `[E16.02]` | ✔ |
| E16.02.07 Female ducts and vagina (B) · AN52.8, AN48.2 | Paramesonephric duct: cranial and horizontal parts → **uterine tube**; caudal parts fuse → **uterine canal** (body + cervix); fusion lifts a transverse fold → **broad ligament** (tube on top, ovary behind), splitting the pelvis into uterovesical and rectouterine pouches; mesenchyme → myometrium + perimetrium. Vagina: **sinovaginal bulbs** → solid **vaginal plate**, canalized by month 5; fornices from the paramesonephric side; **hymen** between vagina and sinus. Mesonephric remnants: epoophoron, paroophoron, **Gartner cyst**. Ovary descends only to the pelvic brim; cranial genital ligament → suspensory ligament; caudal → ovarian ligament + **round ligament** (into the labia majora). | `[E16.02 · R05hr]` | ✔ · **⚑** vaginal lining origin (D-076 a) |
| **Molecular layer** | | | |
| E16.02.01 (D depth) | SRY ± SOX9 → FGF9 (mesonephric cells enter the ridge) → SF1 → Sertoli and Leydig differentiation; SOX9 + SF1 → AMH; SF1 → testosterone enzymes; testosterone/DHT bind one receptor; WNT4 → DAX1 ⊣ SOX9; book names a possible ovary target gene known only from *mouse*. | `[E16.02 MR]` | ✔ (mostly *mouse*; R05ho: human SOX9 and DAX1 patterns differ from mouse) |

---

## 4. Clinical correlates — confirmed against Tier 1 (PubMed first)
**Grouped by what went wrong: the bud and blastema didn't meet or misbuilt · the kidney didn't climb right · a channel stayed open or the wall didn't close · the ducts didn't fuse · the folds didn't close · the hormone signal was wrong · the testis didn't finish its trip.** Rates per 10,000 births. DSD wording follows the 2006 consensus (R05ia): **46,XX DSD, 46,XY DSD, ovotesticular DSD, sex-chromosome DSD** — never "hermaphrodite" or "intersex"; the book's "mental retardation" (WAGR) is written **intellectual disability**.

**Rates, side by side.** ✔✔ = same order of magnitude.

| Lesion | Book | Tier 1 | Mark |
|---|---|---|---|
| Bilateral renal agenesis | 1 in 10,000 | not retrieved (§10) | ✔ |
| ARPKD | 1 in 5,000 | a quoted 1 in 20,000 (background sentence in a 31-patient cohort, R05hm) — **unverified**, no primary population figure retrieved | **≈** lead (note g) |
| ADPKD | 1 in 500–1,000 births | **3.3–4.0 per 10,000** diagnosed (EU point prevalence, R05hn) — a different measure (people known to have it), not birth frequency | ✔ (note g — no conflict) |
| Horseshoe kidney | 1 in 600 | not retrieved | ✔ |
| Wilms tumour cause | "due to WT1 mutations" | **only a minority** of Wilms tumours carry WT1 mutations; ~2 % familial (R05hl) | **⚑ D-076 f** |
| Bladder exstrophy | 2 per 10,000 | **0.21** total (2.07 per 100,000; 22 ICBDSR programmes, 26 M births; M:F ~2:1; 71 % isolated; R05hk) | **⚑ D-076 d** (~10× lower) |
| Cloacal exstrophy | 1 in 30,000 (≈ 0.33) | ~1 in 130,000 (≈ 0.08; R05am) | **⚑ D-076 d** |
| Uterine anomalies (all) | no overall rate | **5.5 %** of unselected women; arcuate commonest (3.9 %); septate commonest in women with miscarriage/infertility (R05hs) | ✚ |
| Hypospadias | 3–5 per 1,000 (30–50), doubled in 15–20 yr | **20.9** total (27 programmes, range 2.1–39.1); up **1.6×** over 1980–2010 (R05hv) | **⚑ D-076 e** |
| Epispadias | 1 in 30,000 (≈ 0.33) | **0.24** per 10,000 (epispadias without exstrophy; 10 ICBDMS systems, ~6.3 M births, c. 1970–85; rates varied between systems; nearly all male; R05ms) | **✔✔** (within 1.5×) |
| Classic CAH (21-hydroxylase) | ~60 % of DSDs; 90 % of CAH is 21-OH | **1 in 16,008** newborns screened (Texas, R05hw) | ✚ (rate) · ✔ shares |
| Klinefelter (47,XXY) | 1 in 1,000 males | **~1 in 650** males (153 per 100,000; Denmark, R05hx); only ~¼ ever diagnosed | **⚑ D-076 h** |
| Cryptorchidism | 97 % descended at birth; < 1 % stay undescended | at birth **2.4 %** (Finland) – **9.0 %** (Denmark); at 3 months **1.0–1.9 %** (R05hz) | **✔✔** at birth (Finland) · note: varies by country, still 1–2 % at 3 months |
| CAIS testicular cancer | 33 % before age 50 | no figure retrieved (abstracts read had none; §10) | ✔ (≈ for any card: G-Sci note) |
| MRKH (Müllerian aplasia) | no rate | **1 in 4,982** live female births (≈ 2.0 per 10,000 girls; Danish national registry, born 1974–96; kidney anomalies in 34 % of those imaged; R05mq) | ✚ |
| Androgen insensitivity (46,XY girls and women only; people with AIS raised male not counted) | no rate | **4.1 per 100,000** live-born girls (≈ 0.41 per 10,000; every known 46,XY female in Denmark since 1960; median age at diagnosis 7.5 y; R05mr) | ✚ |
| Posterior urethral valves *(beyond Langman)* | not in book | lower urinary tract obstruction **3.34** per 10,000 births, **63 %** of it PUV (≈ 2.1 per 10,000; West Midlands register, 851,419 births, 1995–2007; total prevalence incl. stillbirths and terminations; R05mt); **18.3 %** of children with PUV (almost all boys) have kidney failure by age 5 (9 European registries; R05mu) | ✚ |
| Testicular cancer after corrected cryptorchidism *(beyond Langman)* | not given | pooled **OR 3.99** (2.80–5.71; 6 studies, 371,681 men, operated before adulthood); also raised, less, in the other testis; authors conclude surgery in the first year lowers the risk (R05mv) | ✚ |

**The bud and blastema didn't meet, or misbuilt (kidney):**
- **Renal agenesis** — no bud–blastema signalling (book names gene examples: SALL1/Townes–Brock, PAX2/renal coloboma, EYA1/branchio-oto-renal). **Bilateral** → no urine → **Potter sequence**: oligohydramnios, compressed face (Potter facies), club feet, small lungs (links Ch 14 lung hypoplasia). `[E16.01 CC]` ✔
- **Multicystic dysplastic kidney** — bud fails to branch, nephrons fail; ducts in undifferentiated tissue; can involute to look like agenesis. `[E16.01 CC]` ✔
- **Polycystic kidney disease** — ARPKD (collecting-duct cysts, huge kidneys, failure in infancy or childhood) vs ADPKD (cysts from every segment, failure usually in adults); both are **ciliopathies**, like Bardet–Biedl and Meckel–Gruber syndromes. `[E16.01 CC · R05hm, R05hn]` ✔ biology · ≈ ARPKD rate (note g)
- **Duplicated ureter** — early split of one bud (partial or complete); **two buds** → the extra one may open ectopically (vagina, urethra, vestibule → constant dribbling). `[E16.01 CC]` ✔
- **Wilms tumour** — childhood kidney cancer from nephron precursors, usually by age 5; syndromes link it to **11p13**: WAGR (with aniridia from nearby PAX6), Denys–Drash. Most tumours, though, have no WT1 mutation. `[E16.01 CC · R05hl]` ⚑ f · links PA28.14, PE21.7

**The kidney didn't climb right:**
- **Pelvic kidney** — stuck below the umbilical-artery fork; **horseshoe kidney** — lower poles fused, caught under the **inferior mesenteric artery** root, ureters cross in front; **accessory renal arteries** — leftover ascent vessels (cutting one can kill a pole). `[E16.01 CC · R05hg]` ✔ · ✚ R05hg: early renal supply from iliac arteries or the IMA in *human* embryos (fits pelvic-kidney supply)

**A channel stayed open, or the wall didn't close:**
- **Urachal fistula / cyst / sinus** — all, part or the top of the allantois lumen persists (urine at the navel; a cyst; a blind sinus off the bladder). Compare the vitelline remnants of Ch 15. `[E16.01 CC]` ✔
- **Bladder exstrophy** — lower body-wall closure failure; bladder lining exposed, **epispadias always** present; **cloacal exstrophy** — worse closure failure plus a faulty urorectal septum (imperforate anus, split genitalia, often omphalocele). Link D-043 a (body-wall model). `[E16.01 CC · R05hk, R05am]` ✔ biology · ⚑ d rates

**The ducts didn't fuse:**
- **By structure.** *Uterus* — fusion failure from mild to total: **arcuate** (a dimple), **bicornuate** (two horns, one cervix), **didelphys** (two uteri and cervices, sometimes two vaginas); one duct short → **rudimentary horn** (often closed off → pain, rupture risk). *Cervix* — both ducts short → **cervical atresia**. *Vagina* — sinovaginal bulbs absent → **vaginal atresia** (a small Müllerian pouch around the cervix); not fused → **double vagina**. `[E16.02 CC · R05hs]` ✔ · ✚ R05hs prevalence (5.5 %) and that a **septate** uterus (a resorption failure the book's box doesn't name) is the commonest in high-risk women

**The folds didn't close:**
- **Hypospadias** — incomplete fold fusion: opening on the underside, near the glans (commonest), on the shaft or at the base; worst case a slit with split scrotum. Book links the rise to endocrine disruptors (a hypothesis, Ch 9). `[E16.02 CC · R05hv]` ⚑ e rate
- **Epispadias** — opening on the top; usually with bladder exstrophy. `[E16.02 CC · R05ms]` ✔ · ✔✔ rate (book 1 in 30,000; ICBDMS 0.24 per 10,000, nearly all boys)
- **Micropenis** — too little androgen (hypogonadism, hypothalamus/pituitary); length < −2.5 SD; **bifid/double penis** from a split tubercle. `[E16.02 CC]` ✔

**The hormone signal was wrong (DSD):**
- **46,XX DSD — congenital adrenal hyperplasia** (commonest cause of atypical genitalia; **21-hydroxylase** in ~90 %): adrenal androgens virilize an XX fetus; salt-wasting risk; rarer 11β- and 17α-hydroxylase forms (17α: no sex steroids, so XX look typical until puberty, XY under-virilized). `[E16.02 CC · R05hw]` ✔ · ✚ R05hw: 1 in 16,008, most missed until newborn screening even with atypical genitalia
- **46,XY DSD — androgen insensitivity**: receptor absent/faulty → testes + AMH present, so **no uterus or tubes**, but female-typical external genitalia (complete) or atypical (partial); short vagina; testes in the groin or labia; tumour risk (book 33 %, unverified, §10). **5α-reductase deficiency**: no DHT → under-virilized external genitalia at birth with male internal ducts. **AMH deficiency**: male external genitalia with a uterus and tubes. **XY gonadal dysgenesis (Swyer)**: SRY mutation → streak gonads, female-typical body, no puberty. `[E16.02 CC · R05hq]` ✔
- **Ovotesticular DSD** — ovarian and testicular tissue (ovotestis in ~⅔); karyotype 46,XX in ~70 %. `[E16.02 CC]` ✔
- **Sex-chromosome DSD** — **Klinefelter 47,XXY** (small testes, low testosterone, reduced fertility, gynaecomastia ~⅓; non-disjunction); **Turner 45,X** (streak gonads, short stature, heart and kidney anomalies; Ch 2). `[E16.02 CC · R05hx]` ⚑ h rate

**The testis didn't finish its trip:**
- **Cryptorchidism** — testis in the abdomen or canal; often finishes by 3 months; low androgen is one cause; untreated → no mature sperm; renal anomalies in 3–5 %. `[E16.02 CC · R05hz]` ✔✔ (varies by country; 1–2 % at 3 months)
- **Congenital indirect inguinal hernia** — the processus vaginalis stays open (bowel can follow it into the scrotum); **hydrocele** — patchy closure leaves fluid-filled pockets. `[E16.02 CC]` ✔ (closure age: book says both "at birth or shortly after" and "in the first year" — note j)

---

## 5. ⚑ Watch items → decision D-076 (owner picks)
- **(a) Where the vaginal lining comes from.** Book: dual origin — upper vagina from the uterine canal (paramesonephric), lower from the urogenital sinus. R05hr (*human*, 5–21 wk of gestation, PAX2 vs FOXA1 staining): the sinus-type lining spreads upward until, by 21 wk, the **whole vaginal epithelium is sinus-derived**; the muscle wall and fornices question is separate. *X3a (R05hr full text, 22 Nov 2026):* the finding is a **marker reading** (PAX2 → FOXA1 boundary moving up from 12 to 16 wk of gestation), not lineage tracing; the authors set aside stromal induction (unpublished recombinants) but themselves ask whether Müllerian cells could switch on FOXA1 as they mature under hormones, and call for 18–21 wk specimens — so "sinus-derived" is their interpretation; this supports option (2), which is true either way. Options: (1) default; (2) card: "the vagina forms from a plate built by both the uterine canal and the sinus" (true either way), the lining finding in More. *Recommended (2).*
- **(b) The urethra in the glans.** Book: an ectodermal cord grows in from the glans tip and canalizes. R05ht (36 *human* fetal phalluses, 5–22 wk): no ectodermal ingrowth — the endodermal urethral plate reaches the tip and the whole urethra, glans included, forms from it, its lining turning squamous; R05hu agrees (plate canalizes, folds fuse). Options: (1) default (exam answer); (2) card: "the urethral plate forms the urethra; the glans part's origin is debated", both in More; (3) teach endoderm throughout. *Recommended (2).*
- **(c) When nephrons stop forming.** Book: until birth. R05hi (review) and R05hj (11 *human* kidney pairs): no new nephrons after **~36 weeks of pregnancy**, the count plateaus at 36 wk (R05hh's "34–37 wk" is on an unclear clock and is not used). R05hi/R05hj do not cover babies born before 36 wk; see X2c below. Options: (1) default; (2) card: "in a baby born at term, all nephrons are already formed — none are added later", book wording in More. *Recommended (2).* **X2c (22 Nov 2026) — babies born early:** R05mw (*human* autopsy kidneys, 28 kidneys from preterm babies who lived 2–68 days vs kidneys from 32 stillborn controls of the same gestational age): nephron formation is still going at a preterm birth and **carries on after it, and the kidney matures faster than in the womb** (more glomerular generations, a narrower nephrogenic zone); the authors suggest fewer working nephrons, with more abnormal glomeruli and larger corpuscles. So "no new nephrons after birth" fails for preterm babies too — it supports option (2)'s "born at term" wording. A link, not a new ⚑.
- **(d) Exstrophy rates.** Bladder: book 2 per 10,000; ICBDSR **0.21** (R05hk) — about 10× lower. Cloacal: book 1 in 30,000; ICBDSR ~1 in 130,000 (R05am, already in the registry). Options: (1) default; (2) cards quote the ICBDSR figures ("about 1 in 50,000"; "about 1 in 130,000"), book figures in More. *Recommended (2).* Links D-043. **X2c:** the 1987 ICBDMS pooled study (10 systems, ~6.3 M births; R05ms) gives bladder exstrophy **0.33** per 10,000 — also ~6× below the book; supports (2).
- **(e) Hypospadias rate and trend.** Book: 3–5 per 1,000, doubled in 15–20 years. R05hv (27 programmes, 1980–2010): **20.9 per 10,000** (~1 in 480), programmes 2.1–39.1, up 1.6× over 31 years. Options: (1) default; (2) card: "about 1 in 500 births, varies by country, rising", book in More. *Recommended (2).*
- **(f) What causes Wilms tumour.** Book: mutations in WT1 at 11p13. R05hl: WT1 is mutated in only a minority of tumours and excluded in most familial cases; the 11p13 link is strongest in syndromes (WAGR, Denys–Drash). Options: (1) default; (2) card: "linked to WT1 (11p13), especially in syndromes like WAGR; most tumours have other changes". *Recommended (2).*
- **(g) Note, not ⚑ (downgraded by G-Sci) — polycystic kidney frequencies.** ARPKD: book 1 in 5,000; the only Tier 1 hit (R05hm) quotes 1 in 20,000 in a background sentence of a 31-patient cohort — unverified, so it is a ≈ lead and cards keep the book figure until a primary population source is found (§10). ADPKD: book 1 in 500–1,000 births vs R05hn 3.3–4.0 per 10,000 *diagnosed* people — different measures, no real conflict; cards say "commoner, usually found in adults".
- **(h) Klinefelter frequency.** Book: 1 in 1,000 males. R05hx (Danish national registry, prenatal karyotypes): **~1 in 650**, only a quarter ever diagnosed. Options: (1) default; (2) card "about 1 in 500–1,000 males, mostly undiagnosed". *Recommended (2).*
- **(i) How the kidney's arteries change during ascent.** Book: a ladder — ever-higher aortic branches take over, lower ones regress. R05hg (28 *human* embryos, 3D, CS14–23): the mesonephric arteries never reach the metanephros; early supply from the primitive iliac arteries (8 of 9) or the IMA; a capillary cluster from the aorta at CS21–22 suggests the final renal artery is **new growth**. One group; the authors say it contradicts the ladder model. Options: (1) default; (2) default + one More line. *Recommended (2)* (accessory arteries are still "leftover ascent vessels" in both views). Links D-068.
- **(j) Note, not ⚑ — the book disagrees with itself on processus vaginalis closure:** descent text says the canal is sealed at or shortly after birth, the hernia box says in the first year. No Tier 1 retrieved (§10); cards say "usually closes around birth or in infancy".
- **(k) Links, not new ⚑ (note):** **D-074 n** — Ch 16 restates the urorectal septum and cloacal division (weeks 4–7), consistent with R05gk; the perineal body at the septum's tip ✔. **D-074 c** — anorectal malformations come back only inside cloacal exstrophy; no new evidence. **D-043** a — bladder and cloacal exstrophy as body-wall closure failures (same model); rates are (d). **D-068** — umbilical arteries form the fork the kidney rises through (and later the medial umbilical ligaments, Ch 13); renal arteries are (i). **D-030** — clocks (descent figures are LMP; embryonic ones post-fertilization).
- **(l) Curriculum note:** NMC 2018 Vol I has one core code each for **urinary (AN52.7)** and **reproductive (AN52.8)** development; adult codes **AN46.1** (testis incl. descent), **AN46.2** epididymis, **AN46.3** penis, **AN44.4–44.5** inguinal canal + hernia, **AN48.2** pelvic viscera, **AN47.5** abdominal viscera (kidney), **AN49.2** perineal body, **AN52.2** histology; **AN75.1** chromosomal aberrations (Klinefelter, Turner). No AN code names renal agenesis, polycystic kidney, horseshoe kidney, exstrophy, hypospadias, uterine anomalies or any DSD; they sit in other subjects (PA28.12 cystic kidney, PA28.14 renal tumours, PE21.7 Wilms, SU30.2 undescended testis). **AN74 has no urogenital item.**
- **(m) Lead, not ⚑:** CAIS tumour risk — book 33 % before 50; centres increasingly question routine gonadectomy, but no abstract read gave a figure. Find a Tier 1 figure before any card quotes a risk.

## 6. Top student misconceptions (refute in cards and Checks — craft §3.4)
1. **"All three kidney systems build the adult kidney together."** (map row) Only the **metanephros** becomes the kidney; the pronephros vanishes, the mesonephros leaves its duct to the male genital tract `[E16.01 · R05hg]` ✔✔.
2. **"Nephrons and collecting ducts come from the same tissue."** (map row) Two tissues: **blastema → nephrons**, **ureteric bud → collecting system** `[E16.01]` ✔.
3. **"The ureteric bud comes from the kidney."** It grows **from the mesonephric duct**, which is why ureter and genital-duct anomalies travel together (ectopic ureter into the vagina, renal anomalies with uterine ones) `[E16.01, E16.01 CC]` ✔.
4. **"The kidney climbs up."** It mostly stays while the body grows below it and straightens `[E16.01]` ✔ (mechanism book only; ✔✔ that ascent happens, CS14–23, R05hg).
5. **"Kidneys clean the fetus's blood."** The **placenta** does; fetal urine's job is amniotic fluid — hence Potter sequence `[E16.01]` ✔.
6. **"You keep making nephrons after birth."** No new nephrons after ~36 wk of pregnancy (book: after birth) `[E16.01 · R05hi]` ⚑ c (*Checks ask "in a baby born at term, can nephron number rise after birth?" — no in both*).
7. **"Female is the default — the ovary needs no genes."** (map row) The ovary needs **WNT4** (and others); "default" only describes the ducts and genitalia without testis hormones `[E16.02 MR · R05hq]` ✔✔.
8. **"Testosterone makes the Müllerian ducts regress."** (map row) **AMH** (Sertoli) removes them; testosterone (Leydig) keeps the Wolffian ducts `[E16.02 · R05hq]` ✔✔.
9. **"Testosterone itself shapes the penis and scrotum."** (map row) **DHT** does — hence 5α-reductase deficiency `[E16.02 MR · R05hq]` ✔✔.
10. **"Germ cells start in the gonad."** They come from the epiblast via the yolk sac and hindgut, arriving in week 5 `[E16.02 · R05hp]` ✔✔.
11. **"Sertoli and Leydig cells come from the same place."** Sertoli from surface (coelomic) epithelium, Leydig from ridge mesenchyme `[E16.02]` ✔.
12. **"The scrotum and labia minora match."** Scrotum ↔ **labia majora** (swellings) ✔; penile urethra ↔ **labia minora** (folds) ✔✔ `[E16.02 · R05hu]`.
13. **"Hypospadias means the opening is on top."** That is **epispadias**; hypospadias = underside `[E16.02 CC]` ✔.
14. **"The transversus abdominis gives a covering too."** It arches over the path — **no layer** `[E16.02]` ✔.
15. **"The testis drags its blood supply from the scrotum."** It keeps its **aortic** artery from kidney level — why testicular pain and lymph go to the back `[E16.02]` ✔.
16. **"Undescended testis at birth is always abnormal for life."** Most finish by 3 months `[E16.02 CC · R05hz]` ✔✔.
17. **"Ambiguous genitalia = ovotesticular DSD."** The commonest cause is **CAH** in a 46,XX baby `[E16.02 CC · R05hw]` ✔.
18. **"Androgen insensitivity → a uterus."** No: the testes still make **AMH**, so the Müllerian ducts regress `[E16.02 CC · R05hq]` ✔✔.
19. **"The bladder lining is all endoderm from the start."** The **trigone** begins as mesoderm (absorbed ducts), later overgrown by endoderm `[E16.01]` ✔.
20. **"The ovary comes from the Müllerian duct."** It comes from the **gonadal ridge** (coelomic epithelium + mesenchyme + germ cells); the Müllerian duct makes the tube, uterus and upper vagina `[E16.02]` ✔.

## 7. Curriculum map (R30 — NMC AN table; source note below)
**Source note:** read from **NMC *Competency Based UG Curriculum Vol I*** (`UG-Curriculum-Vol-I.pdf`, staged from Studio home `references\nmc\`, 22 Nov 2026). Vol I is the **2018** text; the 2024 MGMUHS reprint is not in `references\`, so **2024 wording is unchecked** (§10).

**Where Ch 16 sits (the prompt's guesses, checked):**
- **AN52.7** — development of the urinary system (core) ✔ — "development" only: **no "and congenital anomalies"** (unlike AN52.5/52.6), so anomaly cards cite AN52.7 for the development they explain.
- **AN52.8** — development of the male and female reproductive system (core) ✔ — same: development only.
- **AN46.1** — testis: coverings, internal structure, … **descent of testis** with applied anatomy (core) ✔ · **AN46.2** epididymis ✔ · **AN46.3** penis ✔ (AN46.4 varicocele, AN46.5 phimosis — not embryology).
- **AN44.4** inguinal canal (core) ✔ · **AN44.5** anatomical basis of inguinal hernia (core) ✔.
- **AN48.2** male and female pelvic viscera (core) ✔ — bladder, uterus, vagina, prostate, ductus deferens.
- **AN47.5** major abdominal viscera (core) — the adult kidney's position and relations (the prompt didn't name it; added).
- **AN49.2** perineal body ✔ (urorectal septum tip; shared with Ch 15).
- **AN52.2** histology of kidney, ureter, bladder, testis, epididymis, vas, prostate, penis, ovary, uterus, tube, cervix ✔ — tagged on nephron, testis, ovary.
- **AN79.4** somites and intra-embryonic coelom — the genital ridge is coelomic epithelium, but **not tagged** (the code is Ch 5–6).
- **AN74 genetics** — AN74.4 lists achondroplasia, CF, vitamin-D-resistant rickets, haemophilia, DMD, sickle cell: **no urogenital condition**. **AN75.1** (structural + numerical chromosome aberrations, core) is the code for Klinefelter and Turner — tagged on DSD.

| Concept | AN codes |
|---|---|
| E16.00.01 Three kidney systems | AN52.7 |
| E16.01.01 Mesonephros and its duct | AN52.7 |
| E16.01.02 Metanephros: two sources | AN52.7, AN52.2 |
| E16.01.03 Nephron formation | AN52.7, AN52.2 |
| E16.01.04 Kidney ascent | AN52.7, AN47.5 |
| E16.01.05 Renal anomalies | AN52.7 |
| E16.01.06 Bladder and urethra | AN52.7, AN48.2, AN49.2 |
| E16.01.07 Urachal anomalies | AN52.7 |
| E16.01.08 Molecular regulation of kidney development | AN52.7 |
| E16.01.09 Wilms tumour | AN52.7 |
| E16.02.01 Sex determination | AN52.8 |
| E16.02.02 Indifferent gonad | AN52.8 |
| E16.02.03 Testis | AN52.8, AN46.1, AN52.2 |
| E16.02.04 Ovary | AN52.8, AN52.2 |
| E16.02.05 Genital ducts: two sets | AN52.8 |
| E16.02.06 Male ducts and glands | AN52.8, AN46.2, AN48.2 |
| E16.02.07 Female ducts and vagina | AN52.8, AN48.2 |
| E16.02.08 Uterine and vaginal anomalies | AN52.8 |
| E16.02.09 External genitalia | AN52.8, AN46.3 |
| E16.02.10 Hypospadias and epispadias | AN52.8, AN46.3 |
| E16.02.11 Differences of sex development | AN52.8, AN75.1 |
| E16.02.12 Descent of the testis | AN46.1, AN44.4, AN52.8 |
| E16.02.13 Inguinal hernia, hydrocele, cryptorchidism | AN44.5, AN46.1 |

**Outside AN (for the More line only):** PA28.12 cystic kidney disease, PA28.14 renal tumours, PE21.7 Wilms tumour, SU30.2 undescended testis.

## 8. Scene note — visual references (look, don't copy — RULES G5)
- **Three kidneys (CS10 → CS14):** one long ridge lighting up head → tail; pronephros fades as the mesonephros grows, the metanephros appears low in the pelvis with the ureteric bud touching its cap. End on the adult kidney with "only this one stays" (D4).
- **Bud meets cap (CS14–17):** the branching tree inside a cap of blastema, two colours with a label and pattern each (H5, bud vs blastema — both `--g-meso` with distinct patterns); show one renal vesicle → S-tubule → nephron.
- **Ascent (CS14–23):** R05hg-style view (look only): kidney rising through the umbilical-artery fork past the IMA; early iliac supply as a dashed vessel labelled "one study" (⚑ i). B2 stamp "≈ day 33–58 · CS14–23".
- **Indifferent → testis/ovary (weeks 6–7):** split screen from the same ridge; germ cells arriving from the hindgut (R05hp route). Cross-section at the end (D9): gonad medial to the mesonephros, both ducts lateral.
- **Two ducts, two hormones:** a two-switch diagram (testosterone keeps Wolffian, AMH removes Müllerian) — never one "male hormone" arrow.
- **External genitalia (weeks 6 → 12):** one starting kit, two outcomes with colour-matched homologues; urethral plate canalizing then folds zipping (R05hu, look only).
- **Descent (12 → 33 wk of pregnancy):** gubernaculum swelling, processus vaginalis leading, wall layers wrapping in order (transversus arching over). Label "weeks of pregnancy" (D-030).
- **Never from the book:** its nephric-tubule, calyx, nephron, gene, horseshoe, cloaca/bladder, gonad, duct, vagina, uterine-anomaly, genitalia, descent and hernia figures are copyrighted; every one is redrawn by us (D6, visual-style §16). The book's clinical photographs (polycystic kidney, duplications, horseshoe kidney, exstrophy, hypospadias, atypical genitalia) are not reproduced; real imaging only per §16 (CC0/CC BY/PD), and **no photographs of genitalia of real people** in any card or episode — diagrams only (D6 humane rule).

## 9. Why learners struggle here (M05)
- **Two systems on one ridge** — kidneys and gonads share the ridge, ducts and the cloaca; teach the ridge once and hang both on it.
- **Names in pairs:** mesonephric/paramesonephric, Wolffian/Müllerian, medullary/cortical cords, epi-/paragenital tubules — always show the pair together, one colour each.
- **Hormone logic:** two testis hormones × two duct sets + a third (DHT) for the outside — a 2×2 grid plus one row beats prose; DSD cases are then "which box failed?".
- **Homologues** across the sexes — one starting kit, three parts, two outcomes.
- **Clocks:** embryonic weeks for gonads and ducts, weeks of pregnancy for descent and nephron counts.
- **Sensitive topic:** DSD wording follows the 2006 consensus (R05ia), person-first, no "sex reversal" or "hermaphrodite" in card text.

## 10. To-do — X1 done 22 Nov 2026; X2c gaps run 22 Nov 2026 · X3a full texts 22 Nov 2026
- **Done (X1, 22 Nov 2026):** real locators + sub-locators per subhead for the two long sections; two I1 range gaps (E16.02 → p 282, E16.03 → p 283) and four untitled boxes named; staging from human specimens (R05hg by Carnegie stage; R05hp, R05ho, R05hr, R05hu, R05ht by week; R05hi, R05hj, R05hy, R05hz by gestation, LMP; R05hh for nephron number only, clock unclear); Tier A for all seven Tier A concepts; Tier B–D by destination; clinical correlates in seven mechanism groups with rates per 10,000 where retrieved; 20 misconceptions; AN map from NMC Vol I; 21 new sources R05hg–R05ia; D-076 a–f, h, i ⚑ + notes g, j–m. **G-Sci (fresh-eyes reviewer agent): pass with fixes — 6 MUST, 8 SHOULD, all applied** (R05hh's clock, the preterm claim removed, three overclaimed ✔✔ marks, ARPKD ⚑ → ≈ lead, ADPKD → note, cryptorchidism note, book-order lists reordered, box title, R05am/R05hr rows, missing topics listed here, one misconception).
- **Done (X2c, 22 Nov 2026):** rates for **epispadias** (✔✔, R05ms), **MRKH** (✚, R05mq) and **AIS** (✚, R05mr); G-Sci adds **posterior urethral valves** (✚ rate + kidney failure, R05mt, R05mu) and **cryptorchidism → testicular cancer** (✚ OR 3.99, R05mv); **preterm nephrogenesis** (R05mw → D-076 c, link; no new ⚑); D-076 d gets a second ICBDSR-family figure (R05ms).

**Still open (X2c searched 22 Nov 2026 unless noted):**
- **Rates not retrieved:** bilateral renal agenesis, multicystic dysplastic kidney, horseshoe kidney, duplex ureter, 5α-reductase deficiency, ovotesticular DSD, congenital inguinal hernia — EUROCAT abstracts give subgroup shares and outcomes, not rates; EUROCAT's own prevalence tables are web data, not PubMed (registry check before using).
- **G-Sci adds still open:** unilateral renal agenesis (no rate in the abstracts found), vesicoureteric reflux and PUJ obstruction (not searched to the end), orchidopexy timing as a guideline (SU30.2 — R05mv gives the authors' conclusion only), infertility after cryptorchidism, 5α-reductase deficiency virilizing at puberty — each needs a Tier 1 source; none added as ✚ without one.
- **ARPKD primary population rate** (note g): the only hit is still R05hm's quoted 1 in 20,000.
- **CAIS tumour risk** (note m): reviews only (risk low in childhood, rises in adulthood; no figure) — needs a primary cohort before any card quotes a risk.
- **Processus vaginalis closure age** (note j): no Tier 1 retrieved.
- **Human stage for pronephros and mesonephros** (book weeks only): no human Tier 1 retrieved — R02 VHE sections CS10–16 (look only) would settle the CS.
- **Urine from week 12, glomerular capillaries from week 10, human SRY onset day, AMH and testosterone onset:** no human Tier 1 retrieved; R05ho full text would raise the week-7 line's CS.
- **Full texts (X3a, 22 Nov 2026):** **R05hr** and **R05hu read** (PMC) — both age by heel–toe length ("weeks of gestation"; R05hr calls it a rough estimate); R05hu urethra row narrowed to ✔ timing; R05hr caveat added to D-076 a. **Still open:** R05hh — PMC sends no full text (publisher block); R05hg, R05ho — not in PMC, owner PDF not supplied (`references\papers\` is empty).
- **R01 3D Atlas:** check the CS14–23 models for the metanephros, gonad and ducts before the "three kidneys" and "two ducts" scenes (look only, NC-ND) — a browser/owner step, not PubMed.
- **2024 wording** of AN52.7/52.8 (MGMUHS reprint): not in `references\`.
