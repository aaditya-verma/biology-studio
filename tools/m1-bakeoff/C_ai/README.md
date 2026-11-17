# Method C — local open video model (Wan 2.2 TI2V-5B in ComfyUI)

**Model:** `Wan-AI/Wan2.2-TI2V-5B` (registry T20) — Apache 2.0 (checked on Hugging Face, 17 Nov 2026). ComfyUI is GPL → stays in `apps/`, never in the repo.
**Fits?** ComfyUI's own guide says the 5B model runs in about 8 GB VRAM with its offloading. We measure: note the peak in Task Manager › Performance › GPU › Dedicated GPU memory.
**Role if chosen:** backgrounds/transitions only. It may never carry embryo anatomy without G-Sci (RULES D5, H9).

## Steps (~40 min the first time, mostly downloads)
1. Download **ComfyUI portable for Windows (NVIDIA)** from github.com/comfyanonymous/ComfyUI → Releases. Unzip to `D:\Projects\biology_studio\apps\ComfyUI`.
2. Run `run_nvidia_gpu.bat`. In the browser: **Workflow › Browse templates › Video › "Wan 2.2 5B video generation"** (text/image to video). It offers to download the 3 model files it needs — accept (~16 GB → `apps\ComfyUI\...\models`).
3. **Start image (for control):** load `out\B_three\frames\0000.png` (from the three.js run) into the Load Image node. Size 1280×704, length 121 frames (≈5 s at 24 fps). Seed **1517**.
4. **Prompt:** paste `ai_prompt` from `shot.json`. Negative: `text, letters, watermark, blur, camera shake, cartoon face`.
5. Press **Run**. The console prints `Prompt executed in N seconds` → that's `--gen-seconds`. Watch the dedicated GPU memory peak.
6. The video lands in `apps\ComfyUI\ComfyUI\output\`. Then, in the kit folder:
   `python bakeoff.py ai "D:\Projects\biology_studio\apps\ComfyUI\ComfyUI\output\<file>.mp4" --gen-seconds N --vram-peak-gb G`
   It loops the ~5 s clip to 20 s (a 20 s shot would need 4 chained runs: ×4 the time — note that), adds the day/scale/gizmo overlay (no structure labels: we can't know where the model put things), encodes with NVENC and writes the manifest.
7. Then run `python bakeoff.py report` again.

## If it does not fit (out-of-memory even with offloading)
Free online first: the Hugging Face Space for Wan 2.2 (ZeroGPU, free daily quota, needs a HF login) with the same prompt + start image; download the clip and run step 6 with `--online`. Note that the image and prompt leave the laptop (C12).
**Paid:** none suggested — for this job (non-anatomy filler) the free route is enough.
