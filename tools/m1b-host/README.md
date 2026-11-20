# M1b host-shot kit — Nani Koshika, route H-a (3D in Blender)

*(Purpose: make the M1b Step 2 test — character sheet (front, side, 6 expressions) + one 5-s 9:16 two-angle shot of the host saying "What if a flat disc had to build a whole body?", lip-synced to Kokoro `af_heart` ×0.9, with kinetic captions (Latin + one Devanagari line). Owner docs: `studio-docs/build/studio-playbook.md` §5b, `build/visual-style.md`, DECISIONS D-048/D-049, owner check T1b. Created 20 Nov 2026 · Bio · Build · M1b host shot (Step 2).)*

| File | What it does |
|---|---|
| `spec.py` | **Every value you may change** (`# EDIT:`) — line, voice, colours, expressions, performance, cameras, captions |
| `host.py` | Runner: `check → tts → sheet → shot → captions → encode → report` |
| `blender_host.py` | Runs inside Blender: builds Nani from primitives, face rig, lights, cameras; renders sheet / shot / ΔE masks |
| `captions.py` | Kinetic captions (Pillow + raqm for Devanagari), safe-zone overlay |
| `de.py` | ΔE00 vs D-031 tokens + accent in normal/deutan/protan/tritan vision |

## One-time setup (~10 min) — reuses the M1 toolchain
1. Blender 4.5 LTS is already in Studio home `apps\` (M1). If `host.py check` can't find it: `set BLENDER=D:\Projects\biology_studio\apps\<blender folder>\blender.exe`.
2. Python venv from M1 (Kokoro already works there). Add: `pip install --upgrade pillow soundfile` (Pillow wheels bundle raqm, needed for Devanagari).
3. Fonts (OFL, free) → `D:\Projects\biology_studio\apps\fonts\`: **Inter-Bold.ttf** (fonts.google.com/specimen/Inter → Get font → Download, unzip, take `static\Inter_24pt-Bold.ttf` and rename to `Inter-Bold.ttf`) and **NotoSansDevanagari-Bold.ttf** (fonts.google.com/noto/specimen/Noto+Sans+Devanagari → Download, take `static\NotoSansDevanagari-Bold.ttf`). Without them the kit falls back to Segoe UI Bold + Nirmala UI and says so in the manifest.

## Run (Anaconda Prompt, venv on, `cd D:\Projects\biology_studio\repo\biology-studio\tools\m1b-host`)
1. `python host.py selftest` — 1 s, no GPU: captions + visemes + ΔE helper → PASS.
2. `python host.py check` — finds Blender, FFmpeg, Kokoro, fonts, GPU, the reference.
3. `python host.py all --preview` — **smoke test, ~5–10 min**: 540×960, 16 samples. Look at `out\M1b-host01-preview\for_drive\`.
4. `python host.py all` — the real run (1080×1920 master, 64 Eevee samples; expect ~10–25 min on the GTX 1060). Leave it plugged in.
- One part only: `python host.py sheet --only doubt` · `python host.py shot --only B` · `python host.py captions --safe` (draws safe zones).
- Every step: `--dry-run` (print the plan) · `--debug` (verbose; saves `host_*.blend` so you can open the scene in Blender) · `--only` · `--preview`.
- Cycles instead of Eevee: `ENGINE = "CYCLES"` in `spec.py` (~3× slower, better glass).

## What you get (`out\M1b-host01\` — never committed)
- `for_drive\M1b-host01_character-sheet.png` — front, side, 6 expressions (incl. open-eye surprise + doubt), palette, measured ΔE00.
- `for_drive\M1b-host01_720x1280_captioned.mp4` (ship) · `_clean.mp4` (no captions; the app toggles a VTT) · `_1080x1920_captioned_master.mp4` · `.en.vtt`.
- `for_drive\M1b-host01_manifest.json` (H7: scene hash, tools, GPU, settings, seed, voice, timings, ΔE, licences, AI disclosure) · `RESULTS.md` (paste into the next chat).
- Upload `for_drive\` to **Drive › Biology Studio › renders › bakeoff › host**, then do owner check **T1b**.

## If something breaks
First run of a new Blender scene may need a fix round: run with `--debug`, copy the last 30 lines of the window into the chat.
