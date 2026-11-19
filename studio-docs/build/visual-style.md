# Visual style — how our videos look

*(Purpose: owner doc for the look of rendered video and app 3D — frame, chapter grammar, titles, tissue, palette, focus, dust, light. Created: 20 Nov 2026 · Bio · Fix · Visual style port (D-041; from the owner's reel QR03, research/quality-references.md). Germ-layer colours: D-031 / RULES B3. Gates that use it: G-Art (look) and G-Sci (playbook §2 video checklist, item 8).)*

## 1. Frame (Short, 9:16)
- Design and master at 1080×1920; ship the 720×1280 rendition until the 1080p rung is Measured (RULES H8, D-033).
- Safe zones (at 1080×1920): top 14 %, bottom 25 %, right 14 % (action rail), left 4 %. `--safe` overlays the Instagram Reels + YouTube Shorts UI.
- Bands, never overlapping: chapter title 15–21 % from the top · day/stage 22–24 % · captions 55–65 %, max width 70 % · axes + scale bar bottom-left at 67–74 % (RULES H4, B2).
- Captions (D-032 kinetic captions): ≤ 2 lines, ≤ 28 characters per line, cap height ≥ 40 px at 1080, weight ≥ 600, scrim ≥ 4.5:1; burned in on Shorts, toggleable (VTT) in the app; Devanagari +15 % size.
- Fps: 30 at 720p (60 only once Measured). End card + cover frame: key structure and title inside the centre 4:5 crop (Instagram grid).
- Landscape cuts (Explainer/MBBS, tablet/desktop): same elements; title top-left, layout per design-plan §2 (RULES C13).

## 2. Chapter grammar — Short profile only (D-041 (3))
- 6 chapters × 8 s = 48 s (fits the ≤ 60 s Short with the end card).
- Ch 1 hook question (D3) · ch 2–5 one idea each (D2) · ch 6 payoff = section view (D9) + "this becomes…" (D4).
- Inside 8 s: 2–4 shots, a cut every 1–3 s; the ch 1 hook lands by 1 s; final 1.5–2 s hold after the reveal (D-032).
- ≈ 17–20 spoken words per chapter (130–150 wpm, H6); ≤ 3 new terms per Short (D2).
- Explainer / MBBS cuts keep their longer beats (D-032 learning pace).

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
- Reduced motion: orbits and push-ins become cuts; no rack focus; no dust.
- No flashing above 3 per second (H5).

## 9. Debug + edit
- Debug: `?debug=grade` (app) and `--swatch` (render) show the swatch-chip frame + ΔE00 per layer; `--safe` overlays the safe zones.
- Edit points: tokens and grade values live in one file per tool, marked `// EDIT:` / `# EDIT:` (RULES I6).
