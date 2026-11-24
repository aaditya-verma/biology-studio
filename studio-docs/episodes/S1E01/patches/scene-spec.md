# Patch note — `docs/scene-spec.md` (M1b.q10 = B) · placeholder **D-103**

*(Not applied. Drafted 22 Nov 2026 in `Bio · Episode · S1E01 script` (P1 ①). Spec first, then code — the engine change comes with ② / R1.)*

## 1. §8 "Always on screen" — add after the first paragraph
> **In video** (shot sheets, §10) the same overlays are drawn by the render/animatic overlay, placed by the frame bands in `build/visual-style.md` — Short (9:16, §1): axes + scale bar + honesty/media tag in the top-left block (28–37 %), captions 68–72 % bottom-anchored at 72 %, on host and anatomy shots alike (M1b.q10 = B, D-<id>); Lesson (16:9, §10): bottom-left stack above 84 %, captions 85–95 %. A shot never places them itself.

## 2. §10 shot-sheet table — add one row
> | `overlay` | `"short"` \| `"lesson"` (derived from the camera used) | which band layout the overlay uses; never set per label. scene-check (P1/R1) fails a `cam_short` framing whose named structure falls outside 38–64 % or under the top-left block at its first label |

## 3. Header
Add: `Updated: <date> · <commit chat> — §8 video overlays follow visual-style §1/§10 bands; §10 `overlay` (M1b.q10 = B, D-<id>)`.

## Not part of this patch (V-step needs listed in `storyboard.md`)
N3 tracer in video, N4 `t-meso`, N7 shot `show` state — separate spec changes, not M1b.q10.
