# M1 bake-off kit — shot M1-ps01 (primitive streak, days 15–17)

One shot spec (`shot.json`) + shared maths (`common/scene_math.py`) → three methods render the **same** shot; one overlay (`common/overlay.py`) puts identical day stamp, colour key, scale bar, axis gizmo and labels on all of them. Each run writes `render_stats.json` + `manifest.json` (RULES H7).

## Laptop layout (D:\Projects\biology_studio)
```
tools\m1-bakeoff\   this kit (later moves into the repo's tools/)
apps\               Blender portable (optional), ComfyUI — GPL/heavy, never in the repo
models\             TTS voices, AI weights (Laptop-only per RULES F4)
out\  → the kit writes to tools\m1-bakeoff\out\ (renders, frames — never committed)
repo\biology-studio\ (later, A0)
```

## One-time setup (~20 min, Anaconda Prompt)
1. **GPU facts:** `nvidia-smi` — note the GPU name, driver, memory (VRAM). `bakeoff.py hw` also records it.
2. **Blender 4.2 LTS or newer:** blender.org → Download → Windows installer (or portable zip into `apps\`).
3. **ffmpeg with NVENC:** `winget install Gyan.FFmpeg` then open a new prompt; `ffmpeg -hide_banner -encoders | findstr nvenc` should list `h264_nvenc`.
4. **Node.js LTS:** `winget install OpenJS.NodeJS.LTS` (three.js + Playwright install themselves on first run).
5. **Python bits (TTS):** `conda create -n bio python=3.11 -y` → `conda activate bio` →
   `pip install torch --index-url https://download.pytorch.org/whl/cu124` (GPU build first) →
   `pip install pillow numpy soundfile kokoro piper-tts`.
   Kokoro uses espeak-ng for unknown words: `winget install eSpeak-NG.eSpeak-NG`.

## Run (Anaconda Prompt, `conda activate bio`, `cd D:\Projects\biology_studio\tools\m1-bakeoff`)
- `python bakeoff.py quick` — 5 min: every 12th frame, s/frame estimates only (sanity check).
- `python bakeoff.py all` — the real run (Cycles is the long one). Leave the laptop plugged in.
- Method C (AI video) is manual: follow `C_ai\README.md`, then `python bakeoff.py ai <clip> --gen-seconds N --vram-peak-gb G` and `python bakeoff.py report`.
- Open `B_three\shot.html` is **not** double-clickable (needs the local server) — `record.mjs --headed` shows it live.

## What to send back
1. `out\RESULTS.md` — paste into the chat (or leave it; the chat can read it from the laptop).
2. Upload everything in `out\for_drive\` (clip-A…D.mp4, manifests, voice1/voice2 .wav) to Drive › Embryo Studio › renders › bakeoff.
3. Keep `out\blind_key.json` closed until you've rated T1.
