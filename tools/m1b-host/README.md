# M1b host-shot kit — Nani Koshika, shot M1b-hs01

*(Purpose: make the 5-s 9:16 host test shot on Laptop 1. Owner docs: `build/studio-playbook.md` §5b (host), `build/visual-style.md` (look), `build/pipeline-reference.md` §7 (kit layout). Updated: 21 Nov 2026 · Bio · Build · M1b v7 results — v7c (owner M1b.q9): captions band 68–72 %, shot B pulled back + panned left (`shift_x`), temples end on the body, mouth ×1.3 darker, shawl wool sheen + a dim glow behind the shawl in B (`quality.plate.shawl_lift`). v7b: gate skips body samples touching shawl/book/face parts or the frame edge (hands/arms own region, still gated), grey = skipped in `sep_*.png`; bokeh kept off the host (`quality.plate.bokeh_host_margin`); floor contact shadow (`quality.contact`); `quality.rim.low_boost` hook, off (D-058). Before: Bio · Build · M1b v6 results — v7: rim glow on the body (`quality.rim`) for the host-vs-plate gate, red/green gate overlays `out\review\sep_<tag>.png` (D-052). Before: 21 Nov 2026 · Bio · Build · M1b host results — v6: `t1b` one-run step, two-pass loudness (`loud.py`), body-vs-plate gate + ink outline, per-clip manifests, `--onion` (D-051). Made: 20 Nov 2026 · Bio · Build · M1b host shot.)*

**Where it runs:** Studio home `tools\m1b-host\` (paths to `apps\` and `handoff\` are relative to it). The repo copy `tools/m1b-host/` is the versioned record of the same files.

Our own 3D host in Blender (route H-a, D-047): same mesh, materials and seed from every angle, so the identity holds by construction. No AI model in the shot. The Canva AI images are a look reference only.

## Files
| File | Does |
|---|---|
| `host.json` | The one spec: palette, line, voice, 2 shots, expressions, captions, safe zones, grade. **Edit here.** |
| `lipsync.py` | Kokoro `af_heart` says the line → `line.wav`, word timings, per-frame visemes (phoneme shape × audio envelope). |
| `blender_host.py` | Builds the host (v2: cloth-sim shawl + fringe, sculpted face, eyes with lids, oval glasses + chain, arms, leather book, library plate); renders the sheet (studio plate) or the shot (library plate). Every part is guarded → `out\build_log_<mode>.json`. |
| `tex.py` | Generated textures (ours): shawl wool + cream vine embroidery, leather cover → `out\tex\`. |
| `de.py` | ΔE00 vs the germ-layer tokens, worst of normal/deut/prot/trit (used by `palette`). |
| `loud.py` | Two-pass loudness (H6, D-051): measure → gain + 4×-oversampled limiter → loudnorm `linear=true` → AAC → re-measure every mp4 (−14 LUFS ±0.5, true peak ≤ −1.5 dBTP). `python loud.py out\audio\line.wav` tests it alone. |
| `captions.py` | Kinetic captions: ASS (burned) + VTT (app), EN and HI tracks, key word = colour + weight + scale. |
| `m1b.py` | Runner: `check · tts · tex · sheet · shot · palette · captions · encode · report · compare` (+ QA in report). `t1b` = only what owner check T1b needs, one run at 720×1280. |

Flags on every step (RULES I5): `--dry-run` (print, write nothing) · `--debug` (verbose + saves `out\debug\host_*.blend` to open and nudge `# EDIT:` values) · `--only A|B|<tile>` · `--preview` (360×640, 8 samples). Also `--cycles`, `--nvenc`, `--safe` (paints safe zones; review only), `--reduced-motion` (H5 variant), `--palette-pass` (Standard transform, for ΔE), `--no-sim` (procedural shawl, fast look-dev), `--strict` (stop on the first failing part), `--onion` (compare: ours at 50 % over the ref, silhouettes aligned → `out\review\onion_*.png`).

**Quality pass (v2):** all new knobs live in `host.json` → `quality` (tex, shawl, face, arms, book, plate). The cloth sim result is cached in `out\cache\shawl_<hash>.json` and re-used until a shawl/arm/book/body value changes. `compare` writes `out\review\compare_sheet.png`, `compare_shot.png`, `compare_expressions.png` (ours vs the Canva refs, local only).

## Setup (once, ~10 min)
1. Copy this folder to `D:\Projects\biology_studio\tools\m1b-host\` (the chat already put it there).
2. **Fonts (OFL, free):** download **Inter** (static: Regular, Bold, Black) and **Noto Sans Devanagari** (Bold) from fonts.google.com. Unzip the `.ttf`/`.otf` files into `D:\Projects\biology_studio\apps\fonts\`.
3. Same `bio` conda env as M1 (Kokoro, soundfile, numpy, pillow). Blender 4.5 LTS and FFmpeg 7.1.1 as in M1.
4. `python m1b.py check`: the output should show Blender, ffmpeg, libass `yes`, your GPU, the fonts, and `kokoro`.

## Run (Anaconda Prompt → `conda activate bio` → `cd D:\Projects\biology_studio\tools\m1b-host`)
1. **v7b check first (~5 min): `python m1b.py all --preview`** → open `out\RESULTS.md` (Host vs plate lines) and `out\review\sep_*.png` (green = OK, red = fails, grey = skipped as contact/frame edge). Front sheet still red on the lower curve → raise `quality.contact.dark` (0.45 → 0.55); shot B crown red → raise `quality.plate.bokeh_host_margin`. Repeat. Then:
2. **For T1b: `python m1b.py t1b`** — one run, 720×1280: tex → sheet → shot → palette → captions → encode → report → compare (~10–20 min on the GTX 1060; keep it plugged in). Re-uses `out\audio\line.wav` (voice unchanged).
3. Optional: `python m1b.py shot --reduced-motion`, then `captions --reduced-motion`, then `encode --reduced-motion`.
4. Optional: `python m1b.py compare --onion` for the onion boards.

## What the gates check (report → QA)
- **Loudness:** every mp4 −14 LUFS ±0.5 and true peak ≤ −1.5 dBTP, measured after AAC.
- **Host vs plate (G-A11y):** the body edge must reach ≥ 3:1 against the real background behind it (sheet front + the middle frame of each shot camera) on ≥ 90 % of edge samples. v7 passes it with a view-dependent rim glow on the pearl (`quality.rim`, D-052); the ink outline (`quality.outline`) stays off, fallback only. `palette` writes `out\review\sep_<tag>.png`: green = sample ≥ 3:1, red = fails, grey = skipped (within 2 probe steps of shawl, book, face parts or the frame edge — contact, not figure/ground; D-058).
- **Colour vs germ-layer tokens:** swatches ≥ 15 always; rendered pixels gated only for tokens on screen in the shot (`tokens_on_screen`, [] = info). Embroidery thread vs endoderm is measured on rendered pixels and listed.
- **Captions:** scrim contrast ≥ 4.5:1 for text and key word on the brightest frame behind them.

## Send back
- Paste `out\RESULTS.md` into the chat (it lists QA pass/fail, loudness per clip, ΔE, host-vs-plate, sizes).
- **Upload the files inside `out\for_drive\`, not the folder itself**, to Drive › renders › bakeoff › host. It holds this version only: 3 clips (cap-en, cap-hi, clean), one `.manifest.json` per clip, the 2 sheets, the VTTs and RESULTS.md. Older versions stay in `out\video\` on the laptop (never overwritten).
- Then do owner check **T1b** (`build/owner-test-checklist.md`).

## If something looks wrong
- **Face too high or low, or covered by captions:** change `face_at_pct` (add it to host.json, default 38) or the shot `dist`/`lens_mm`.
- **Mouth out of sync:** raise or lower `line.voice.speed`; check `out\audio\words.json` says `timings: kokoro`.
- **Grade missing:** `render_stats_*.json` shows `"grade": "skipped: …"` and QA fails. Paste the error into the chat.
- **Devanagari shows boxes:** the font is missing from `apps\fonts\`.
- **A part failed (RESULTS says `failed parts [...]`):** paste the `PART FAILED` lines from the console (or `out\build_log_*.json`). The render still ran without that part.
- **Shawl looks wrong after a change:** delete `out\cache\` to force a fresh sim; `--no-sim` shows the pre-sim drape.
