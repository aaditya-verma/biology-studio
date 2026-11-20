# Visual style — how our videos look

*(Purpose: owner doc for the look of rendered video and app 3D — frame, chapter grammar, titles, tissue, palette, focus, dust, light; formats, segment colours, labels, mixed media, clinical slots, recaps, honesty tags, media licences. Updated: 20 Nov 2026 · Bio · Fix · Visual style 2 port — §10–§16 from QR04 + QR05 (D-046). Created: 20 Nov 2026 · Bio · Fix · Visual style port (D-041; from the owner's reel QR03, research/quality-references.md). Germ-layer colours: D-031 / RULES B3. Gates that use it: G-Art (look, §1–§15) and G-Sci (playbook §2 video checklist, items 8 and 13–18).)*

## 1. Frame (Short, 9:16)
- Design and master at 1080×1920; ship the 720×1280 rendition until the 1080p rung is Measured (RULES H8, D-033).
- Safe zones (at 1080×1920): top 14 %, bottom 25 %, right 14 % (action rail), left 4 %. `--safe` overlays the Instagram Reels + YouTube Shorts UI.
- Bands, never overlapping: chapter title 15–21 % from the top · day/stage 22–24 % · legend chip (segment mode, §11) 25–27 % · captions 55–65 %, max width 70 % · axes + scale bar bottom-left at 66–71 % (RULES H4, B2) · honesty tag or media tag on a second line at 71–74 % (§13, §15).
- Captions (D-032 kinetic captions): ≤ 2 lines, ≤ 28 characters per line, cap height ≥ 40 px at 1080, weight ≥ 600, scrim ≥ 4.5:1; burned in on Shorts, toggleable (VTT) in the app; Devanagari +15 % size.
- Fps: 30 at 720p (60 only once Measured). End card + cover frame: key structure and title inside the centre 4:5 crop (Instagram grid).
- Lesson (16:9): see §10.

## 2. Chapter grammar — Short profile only (D-041 (3))
- 6 chapters × 8 s = 48 s (fits the ≤ 60 s Short with the end card).
- Ch 1 hook question (D3) · ch 2–5 one idea each (D2) · ch 6 payoff = section view (D9) + "this becomes…" (D4).
- Inside 8 s: 2–4 shots, a cut every 1–3 s; the ch 1 hook lands by 1 s; final 1.5–2 s hold after the reveal (D-032).
- ≈ 17–20 spoken words per chapter (130–150 wpm, H6); ≤ 3 new terms per Short (D2).
- Lessons keep their longer beats (D-032 learning pace; §10).

## 3. Chapter titles (RULES D8 as amended, D-041 (1))
- ≤ 4 words, thin caps; weight Regular 400 or heavier at the 720p ship (Light 300 only once 1080p is Measured).
- Tracking +8–12 %; cap height ≥ 48 px at 1080 wide (≥ 32 px at 720).
- Soft dark scrim behind → contrast ≥ 4.5:1 (H5).
- 0.3 s fade in; holds for the whole chapter. No title on the hook chapter if it would cover the question's first frame (G-Story calls it).
- Fonts (free, OFL): Josefin Sans or Inter; Devanagari: Mukta or Noto Sans Devanagari. Add to the registry (§ Tools) before first use (F4).

## 4. Tissue — "glassy"
- Blender (Cycles/Eevee): Principled BSDF, random-walk subsurface scattering (SSS); thin coat + transmission on membranes only; warm backlight for rim glow.
- App (three.js): cheap fake — fresnel rim + soft shading; no real transmission (phone budget, H8).
- Translucency must never suggest a cavity that isn't there, and real cavities (amniotic, yolk sac, intraembryonic coelom) must still read as cavities (G-Sci item 8).

## 5. Palette (D-041 (2))
- The warm pink grade touches background, light and `--g-ctx` only; applied as one LUT pass (app and render).
- Germ layers always use D-031 tokens. After the grade, each layer's own in-focus pixels (ID mask) stay within ΔE00 ≤ 8 of its token, and every layer pair stays ≥ ΔE00 15 under deutan/protan/tritan simulation. Debug: `?debug=grade` / render flag `--swatch` also shows a swatch-chip frame; result in the render manifest (H7).
- Plum `--accent` = ring + label, never a fill (D-036); ring ≥ 3:1 against its local background (halo if needed); label text near-white on a dark scrim ≥ 4.5:1 — never plum text. M1 kit `shot.json` still fills streak + node → align in M1 (steps.json M1 to-do).
- Colour never the only cue (H5): stripe/dot surface pattern per layer, period ≥ 6 px, visible at 720p after compression, plus labels. A defocused layer loses its pattern → label every layer the voice names.

## 6. Macro depth of field
- The named structure is in focus ≥ 0.5 s before its label appears, and sharp end to end.
- A rack focus may act as a second "look here" cue (with the plum ring, not instead of it).
- Scale bar always on — macro framing hides size.
- App on phone: no real-time DOF; use a pre-blurred backdrop.

## 7. Dust (D-041 (4))
- Background only: out of focus, slow, sparse; app ≤ 300 instanced points.
- Never inside a cavity, never sharp, never over a label; must not read as cells.
- Off when reduced motion is on (H5).

## 8. Light and camera
- Soft key from cranial-dorsal; warm backlight; low haze.
- One camera move per shot (slow orbit or push-in); none during a label's first 0.5 s.
- Reduced motion: orbits and push-ins become cuts; no rack focus; no dust. App viewer only (rendered video can't follow it): label fades, dissolves and colour morphs stay; the dashed hidden-anchor state is skipped (the label leaves at once); leader lines re-anchor on the cut (§12).
- No flashing above 3 per second (H5).

## 9. Debug + edit
- Debug: `?debug=grade` (app) and `--swatch` (render) show the swatch-chip frame + ΔE00 per layer; `--safe` overlays the safe zones.
- Edit points: tokens and grade values live in one file per tool, marked `// EDIT:` / `# EDIT:` (RULES I6).

## 10. Two formats (D-046 (1))
| | **Short** (cinematic) | **Lesson** (teaching) |
|---|---|---|
| Frame | 9:16, §1 | 16:9, master 1920×1080, ship 1280×720 (RULES H8) |
| Length | ≤ 60 s, 6 × 8 s (§2) | 6–10 min per Part, 3–5 segments of 60–120 s |
| Pace | cut every 1–3 s | hold 1–2 s after each reveal; ≤ 3 new terms/min (D2) |
| Job | hook + one idea | teach the Part fully, exam-ready |
| Clinical | hook only (§14) | fixed slots (§14) |
| Recap | none | opener + teaser (§15) |
- Lesson = the former **Explainer/MBBS profile**, renamed and given a 16:9 frame. General cuts of a Lesson use the same frame.
- **Lesson frame:** safe areas 5 % on every side (graphics). Keep the bottom 15 % free of labels (player controls + captions). Bands: title + Part chip top-left (title, Part chip: cap ≥ 48 px / ≥ 32 px at 1080 high; the §14 "Clinical link" tag replaces the title during the slot, the Part chip stays) · segment legend top-right · subject in the centre ⅔ · labels outside the subject's outline · bottom-left, stacked upwards from the 84 % line: (a) scale bar + honesty tag (§15), (b) axes, (c) day/stage · media tag bottom-right above 84 % (§13) · captions 85–95 % from the top (the app lifts them while player controls show).
- **One scene, two cameras:** each shot has `cam_short` + `cam_lesson` on the same scene state (scene spec §10); never re-model for a format. A Short = a trailer for one Lesson segment, ending on "Full Part in the app".
- App on a phone in portrait (`dev-p`): the inline Lesson player is a preview, transcript/cards below (C13); tap opens full-screen landscape (`dev-pl`). Captions are VTT, sized by device class. Every on-screen label's term also appears in the transcript at that timestamp. G-Art checks one 16:9 frame at 210 px high and at 1080 (design-plan §2, Player 16:9).

## 11. Colour continuity — segment mode (D-046 (2))
- **Two colour modes per shot, never mixed:** *layer mode* (D-031 germ-layer tokens) or *segment mode* (regions inside one layer, e.g. the heart tube — splanchnic mesoderm of the primary + secondary heart fields, E13.01–E13.02). A legend chip names the mode ("Colours = heart regions"). A neural-crest overlay ring (`--g-crest` outline + label, never fill) is allowed in segment mode, e.g. crest joining the outflow ridges (E13.06). A layer ↔ segment switch is allowed at a cut only with a legend-chip change.
- **Segment tokens** `--s-<organ>-<seg>`, ≤ 6 per organ, in `content/E/segments.json` (id, name, token, pattern, derivatives, section cite). Ids are permanent (A2). Each segment token is ≥ ΔE00 15 from every D-031 token, `--g-ctx`, `--accent` and every other segment, also under CVD simulation; §5's after-grade ΔE00 ≤ 8 rule applies to segments too; each has a pattern (H5). Every segment and derivative carries a cite + mark (B1, B7).
- **Colour = origin.** A segment keeps its colour in every Part, Short, card and app 3D, and into its adult derivative. Heart example: sinus venosus · primitive atrium · primitive ventricle · bulbus cordis (incl. conus cordis + truncus arteriosus) each hold one hue from tube to adult chambers (e.g. conus cordis, the middle of the bulbus → outflow tracts of both ventricles, E13.03).
- **Split:** when one segment divides (truncus → roots of the aorta + pulmonary trunk, E13.06), the two products take a light and a dark tint of the parent hue — both ≥ ΔE00 15 apart and from segments on screen, both keep the parent pattern at different densities, each labelled.
- **Merge:** when one is absorbed into another (sinus venosus right horn → smooth part of the right atrium, E13.05), show two colours meeting at a seam, never a blend. Adult anchor shots keep the origin patches (D4).
- Fertilisation (E03.02.03) has no germ layers yet: it uses layer mode plus two chromosome tints (tokens `--s-zyg-mat`, `--s-zyg-pat` in segments.json) — each chromosome keeps its parent's colour; every nucleus after syngamy shows both, never blended. Zona pellucida (acellular coat) and corona radiata (follicle cells) use `--g-ctx`.
- Within one mode, colour changes only by a morph on screen, never at a cut (playbook §6.6).
- Hue sets per organ are chosen with the swatch page when that chapter's X1 runs (heart: X1 Ch 13), not before.
- Debug: `?debug=segments` / `--swatch` adds segment chips + ΔE00; `# EDIT:` in segments.json.

## 12. Labels + leader lines
- Text: 1–3 words, GLOSSARY term (D8). Weight ≥ 600. Near-white on a dark scrim ≥ 4.5:1. Cap height ≥ 40 px at 1080 (Short) / ≥ 32 px at 1080 high (Lesson). Devanagari +15 %.
- **Colour chip:** a small swatch before the text in the structure's token colour + pattern (colour never alone, H5).
- **Leader line:** 2 px at 1080 (3 px at 720) — Short width / Lesson height — near-white with a 1 px dark edge (≥ 3:1 on any background). Ends in a 6 px dot on the surface. Straight, or one elbow; ≤ 25 % of frame width; never crosses another line or label, and touches the named structure only at its dot.
- **Anchored in 3D:** the dot tracks the surface as it moves. If the anchor is hidden, the line becomes dashed for ≤ 1 s, then the label leaves.
- **Count:** ≤ 3 labels at once (Short), ≤ 6 (Lesson). Fade in 0.3 s as the voice names it (D8); Short: fade out when the voice moves on; Lesson: the leader line and chip dim (text stays ≥ 4.5:1) until the segment ends; the oldest label leaves when a 7th arrives.
- The plum `--accent` ring and its label arrive together (D-036); the label goes on the side away from the frame edge.
- Debug: `?debug=labels` shows anchors, hit boxes and overlaps.

## 13. Mixed media
- **Allowed types:** our 3D (default) · our 2D diagram/section · microscopy · ultrasound · X-ray / CT / MRI · real footage (e.g. IVF lab) · host (AI, H9). Every non-own item passes §16 first.
- **Media tag** on every non-3D shot: "Real image · <credit>", "Ultrasound · <credit>", "Diagram". Cap ≥ 32 px at 1080, weight ≥ 600, scrim ≥ 4.5:1; bottom-right (Lesson, §10) or bottom-left on the second line beside the scale bar (Short, §1). 3D needs no tag. A thin 1 px border marks real imagery.
- **Real images stay real:** no warm grade (exposure/neutral only), no recolouring to tokens, no cloning, no AI upscaling or "enhance". Crop, resize, contrast allowed and logged (ledger, §16).
- **Overlay mode:** to teach on a real image, draw token-coloured outlines (≥ 3:1, dark halo) + labels on top (toggleable in the app). The image underneath is untouched.
- **Bridge cut:** align the 3D camera to the real image's view; 0.5–1 s dissolve; the outline carries across the cut so the viewer sees "this model = that real thing".
- Real images keep orientation (H4) and a scale bar from source data; if none: "scale not given".
- Short: ≤ 1 media switch per 8-s chapter; no patient imaging in Shorts. Lesson: real media ≤ ~20 % of runtime (guide, not rule).

## 14. Clinical-correlate slots (D-046 (4))
- **Lesson:** after a normal process is taught, a "Clinical link" slot, 15–30 s, ≤ 2 per Part. Grammar: replay the normal step (2 s) → accent ring on the step that fails → result (diagram) → one line on why it matters → back to normal.
- Same model + colours as the lesson, so the fault is visible as a change of the normal. Diagram by default; real imaging only under §16 and D6 (humane).
- Cites the book's clinical section + mark (B1, B7); NEET-PG flag on the card. Heart example: unequal division of the conus (conotruncal septum displaced forward) → tetralogy of Fallot (E13.06.07). Fertilisation example: assisted reproduction (concept E03.02.04, §E03.02).
- **Short:** clinical only as the opening mystery (D3), answered by the end; no patient imaging.
- Tag "Clinical link" top-left for the whole slot.

## 15. Series recap + honesty tags
**Recap (Lesson):**
- **Opener ≤ 15 s:** retrieval question first ("Which region becomes the ventricles' outflow tracts?"), 2 s pause, then 3 beats from the last Part's end states.
- **Continuity:** Part N starts on Part N−1's last frame — same scene state, colours, camera (`endstate.json` per Part, scene spec §10; the render check diffs it).
- **Teaser ≤ 5 s:** a question for the next Part. Part chip ("Heart · Part 3") top-left throughout.
- Season recap episodes stay (D7). Shorts stand alone: Part number on the end card only.

**Honesty tags** (RULES B2, extended):
- Fixed list: **Exaggerated for clarity** · **Not to scale** · **Time compressed** · **Colours illustrative** · **Simplified**.
- One tag at a time, ≤ 4 words, beside the scale bar (§1, §10); on for the whole shot where true (it appears with the shot, never mid-shot). If two apply, show the first in this order: Not to scale > Exaggerated for clarity > Time compressed > Simplified > Colours illustrative; the rest go in the shot sheet + description.
- Cap height ≥ 32 px at 1080; weight ≥ 600; scrim ≥ 4.5:1.
- **Exaggeration may change** size, thickness, spacing, speed, transparency. **Never** number, order, side, topology or sequence (D5).
- Shot sheet field `exaggerations[]`: what · how much · why. If it touches an exam fact (e.g. thickness of cardiac jelly), the voice says so.

## 16. Licence rules — footage, X-rays, other real imagery (D-046 (3))
| Source / licence | Use |
|---|---|
| Our own 3D + diagrams | Default; also the free fallback for everything below |
| Public domain (e.g. US federal: NIH/NLM, NMHM) | Yes, credited; check each item (some collections mix in copyrighted items) |
| CC0 · CC BY 4.0 (Wikimedia Commons per file, open-access papers' figures + supplementary videos) | Yes, credited |
| CC BY-SA | **No** (D-046 (3)) — it would make the whole video BY-SA; D-021 stays limited to Z-Anatomy meshes. Draw our own instead |
| NC / ND / NC-SA (e.g. many radiology teaching sites — check each one's licence) | Reference only (RULES G5): look, then draw our own |
| Stock, YouTube, clinic IVF videos, textbook images | No, unless a written licence is logged |
- **Patient imaging** (X-ray, ultrasound, photos): only from licensed sources that state consent + de-identification, or owner-supplied cases with written consent. Strip DICOM metadata; crop burned-in text (name, date, hospital, ID); no identifying features. Humane framing (D6, playbook §8.5).
- **Real embryo footage:** only from CC BY published supplements or PD; never from clinic marketing.
- **AI** never makes or "enhances" real-looking medical images (H9).
- **Ledger:** each item gets a row in the "Media" table of `research/source-registry.md` (ids `M01`…), mirrored in `THIRD_PARTY.md`: URL, author, licence, date retrieved, changes made, where used. Licence page saved as PDF in Drive › research/licences/. On-screen credit tag (§13) + full credit in the description.
