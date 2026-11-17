# Source registry — who we trust, for what

*(Owner doc for sources **and tools**. Created 17 Nov 2026, D-011. Add a source or tool here before citing or installing it anywhere.)*

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
| R07 | **EHDAA2** human developmental anatomy ontology (Bard 2012; OBO Foundry; github.com/obophenotype/human-developmental-anatomy-ontology). ~14,000 structure/stage/"develops from" facts, CS1–20. Inactive since ~2022. Related: **Uberon** (cross-species anatomy), **HsapDv** (human stages) | K1 skeleton: concept ids, part-of and develops-from links, stage ranges, synonyms. Map to book sections; book wins on conflict | CC BY 4.0 → may import data, credited |

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
| R30 | **NMC Competency Based UG Curriculum for the Indian Medical Graduate, 2024** — Anatomy (AN): 82 topics, 413 competencies; general embryology topics start at 76 (intro, gametogenesis & fertilization, second week…) | Tag every card with its AN code(s) in I1/X1; drives Tier B; coverage gap list |

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
