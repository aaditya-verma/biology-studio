# Patch note — `studio-docs/build/visual-style.md` §1 (M1b.q10 = B) · placeholder **D-103**

*(Not applied. Drafted 22 Nov 2026 in `Bio · Episode · S1E01 script` (P1 ①); the commit task or the ② chat applies it after G-Art reads the animatic frames. Owner answer: M1b.q10 = B, 22 Nov 2026 12:19 IST — anatomy shots also use the 68–72 % caption band; axes + scale bar move top-left.)*

## 1. Replace the "Bands" bullet in §1
**Old:**
> - Bands, never overlapping: chapter title 15–21 % from the top · day/stage 22–24 % · legend chip (segment mode, §11) 25–27 % · captions 55–65 %, max width 70 % (**host shots with no axes/scale: 68–72 %, bottom-anchored at 72 %** — owner M1b.q9, D-059; anatomy shots keep 55–65 % until M1b.q10) · axes + scale bar bottom-left at 66–71 % (RULES H4, B2) · honesty tag or media tag on a second line at 71–74 % (§13, §15).

**New:**
> - Bands, never overlapping (D-059, D-103): chapter title 15–21 % from the top · day/stage 22–24 % · legend chip (segment mode, §11) 25–27 % · **top-left block** (left inset 4 %, ≤ 30 % of the width): axes + scale bar 28–34 %, honesty tag or media tag below them at 35–37 % (RULES H4, B2; §13, §15) · subject 38–64 % · **captions 68–72 % on every shot (host and anatomy), bottom-anchored at 72 %**, max width 70 %; a second line grows upward (to ~64 %) and stays above the 75 % Shorts UI (owner M1b.q9 + M1b.q10 = B).

## 2. Add one bullet under it
> - Anatomy framing for the band: `cam_short` frames the named structure inside 38–64 % and clear of the top-left block; a caption's second line may overlap the subject's lower edge only on a host shot. G-Art checks the 9:16 frame at phone size with `--safe` on (§9).

## 3. Header
Add to the Updated line: `Updated: <date> · <commit chat> — §1 bands: anatomy captions 68–72 %, axes + scale bar + tag top-left (M1b.q10 = B, D-<id>)`.

## Why this layout (for the D-entry)
- 68–72 % for both shot kinds keeps one caption position through a Short (no jump on host ↔ anatomy cuts).
- Axes + scale bar can't stay at 66–71 % bottom-left: they would sit inside the caption band.
- Top-left under the legend chip keeps them off the right action rail (14 %) and away from the centred title; the honesty tag stays next to the scale bar (§15 "beside the scale bar").
- The subject zone shrinks from ~28–54 % + 72 % to 38–64 % (≈ 500 px at 1080×1920). Rejected: axes top-right (action rail), axes inside the title band (crowds the 4-word title), tag on the caption line (two kinds of text in one band).

## Lessons (16:9) — unchanged
§10's Lesson frame (bottom-left stack above 84 %, captions 85–95 %) is not touched by M1b.q10.

## Knock-on checks (commit chat or ②)
- `tools/m1b-host/captions.py` already anchors at 72 % (v7c) — no change.
- The animatic overlay (②) and later render overlay read these bands from one config (`// EDIT:` home, RULES I6), not per shot.
- G-A11y: captions ≥ 4.5:1 scrim, tag cap ≥ 32 px at 1080 — unchanged.
