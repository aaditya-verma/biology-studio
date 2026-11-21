# Pipeline reference — Expected vs Measured

*(Purpose: laptop, phone, tablet, desktop, render and voice numbers; build only on Measured. Updated: 21 Nov 2026 · Bio · Build · V2 3D drills — §2 notochord scene row (owner fps open, T8) + stills row. Before: 21 Nov 2026 · Bio · Build · M1b host results — §3 host rows from the v5 RESULTS.md, §5 log rows, §7 host kit (D-051). Before: 21 Nov 2026 · Bio · Fix · M1b merge — §1 idle row (P8 · 6 W · 43 °C, from M1b Step 1). Before: 20 Nov 2026 · Bio · Build · M1 bake-off (part 2) — Laptop 1 + toolchain recorded, §3 Measured, §5 log, §6 driver/FFmpeg pin; before: 19 Nov 2026 · Bio · Build · V1 viewer — §2 viewer rows; before: 18 Nov 2026 · Bio · Fix · doc reconcile — ported from the uploaded copy (D-033): §2 phone + tablet + desktop, 1080p rows in §2–§3, §4 check 2.)*

Rule C4: build only on the **Measured** column. Expected values are rough starting guesses, to be replaced by measurements (M1 onwards). Fill "Checked on" with date + device. Local-first on the owner's NVIDIA laptop (D-014, RULES C12).

## 1. Laptop 1 — owner's render machine (fill first in M1)
| Item | Expected | Measured | Checked on |
|---|---|---|---|
| Maker / OS family | — | MSI · Windows x64 | 17 Nov 2026 · desktop-app bridge |
| GPU model + driver (`nvidia-smi`) | NVIDIA gaming GPU (owner: runs Adobe apps, F1 games) | **GTX 1060 (Pascal, no RT/tensor cores)** · driver **581.57**, CUDA 13.0 (renders ran on 551.86; encodes re-run on 581.57). 580 branch = last for Pascal → stay on it | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| VRAM | 6–16 GB (decides local video models) | **6 GB** (6144 MiB) — bottom of range; Wan 2.2 5B not run (M1 Method C) | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| CPU / RAM / free disk / OS version | — | i7-8750H 6C/12T · 16 GB (15.9) · 298 GB free on D: · Windows 10 Home 22H2 (19045) | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| Blender OptiX available | yes on RTX cards | **yes** — Blender 4.5.10 LTS Cycles ran OPTIX on the GTX 1060 (no RT cores, so no hardware ray-trace speed-up) | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| ffmpeg NVENC (h264_nvenc / hevc_nvenc) works | yes | **yes** — h264_nvenc, hevc_nvenc listed (av1_nvenc listed but Pascal has no AV1 encoder — don't use). **FFmpeg pinned to 7.1.1** (gyan full build): 8.x+ needs a newer NVENC API than the 580 driver | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| Toolchain (Studio home `apps\`, caches on D:) | — | Blender 4.5.10 LTS portable · Node 26.13 · Python 3.11.9 venv · three.js r170 + Playwright Chromium 159 · Kokoro-82M (CUDA) · Piper `en_US-ryan-high` (CPU) | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| GPU temperature at idle | — | **P8 · 6 W · 43 °C** (NVIDIA overlay off, Power management mode Normal; replaces the earlier ~80 °C reading) | owner, 20 Nov 2026 |

**How to fill:** `python bakeoff.py hw` (kit, §7) writes all of these to `out\hw.json`. By hand: Anaconda Prompt → `nvidia-smi` (top-right box: driver + CUDA; middle: GPU name, `xxxxMiB` total = VRAM) · Task Manager › Performance › GPU (Dedicated GPU memory) / CPU / Memory · Blender › Edit › Preferences › System › Cycles Render Devices › OptiX (your GPU listed = yes).

### 1b. Laptop 2 — the Professor's (filled in T5 from `out\hw.json`)
| Item | Expected | Measured | Checked on |
|---|---|---|---|
| Maker / OS family | Windows x64, NVIDIA (owner, 17 Nov) | | |
| GPU model + driver / VRAM | — | | |
| CPU / RAM / free disk / OS version | — | | |
| Blender OptiX / ffmpeg NVENC | — | | |
| `bakeoff.py quick` s/frame per method | — | | |

Numbers measured on one laptop are labelled with it; a step built on Measured numbers names which laptop (C4). Manifests already record the GPU (H7).

## 2. Viewing devices & playback (phone · tablet · desktop — D-033)
| Item | Expected | Measured | Checked on |
|---|---|---|---|
| Phone model / Android / Chrome version | — | GPU Adreno 740 (Snapdragon 8 Gen 2 class) · Chrome 158 Android · screen 360×804 CSS px @3 (canvas capped @2 → 660×632) · model name hidden by Chrome's reduced user agent — owner to add | owner's phone, 19 Nov 2026 |
| three.js on owner's phone: fps, 50k-triangle embryo scene | ≥ 30 fps | **60 fps avg (display rate), 5th pct 53.8** at ~51k triangles (portrait, canvas 660×632 @2) | owner's phone (Adreno 740, Chrome 158), 19 Nov 2026, app v3 Measure |
| Triangles before stutter on the phone | ~150k | **> 300k** (60 fps avg, 5th pct 50 at 301k; ceiling not reached) | owner's phone (Adreno 740, Chrome 158), 19 Nov 2026, app v3 Measure |
| three.js on the phone: the 3 Part 0 scenes (~1–2.5k triangles each; `?debug=viewer` › Measure) | ≥ 30 fps (display rate) | **60–62 fps avg · 5th pct 50–52** (sc-E00.01.01 / .02 / .04) | owner's phone (Adreno 740, Chrome 158), 19 Nov 2026, app v3 Measure |
| three.js on the phone with +50k / +150k / +300k test triangles (Measure) | ≥ 30 / ≥ 30 / ? fps | **60 / 60 / 60 fps avg · 5th pct 53.8 / 53.8 / 50** | owner's phone (Adreno 740, Chrome 158), 19 Nov 2026, app v3 Measure |
| Headless stills (SwiftShader, 960×540) — 8 stills, cloud workspace | — | 3 scenes: 852–2 460 triangles, 9–22 draw calls; run ≈ 7 s (19 Nov 2026) | cloud (not a device) |
| three.js on the phone: sc-E05.02.01 notochord (~2.9–3k triangles, 27 draw calls; Measure) | ≥ 30 fps (display rate) | *(owner: T8 step 7)* | |
| Headless stills — 11 stills, 4 scenes, cloud workspace | — | 882–2 990 triangles, 15–27 draw calls (sc-E05.02.01 the largest); still Chromium matches the CI baselines pixel-for-pixel (21 Nov 2026) | cloud (not a device) |
| Tablet model / OS / browser (owner's or Professor's) | — (not recorded yet) | GPU Adreno 730 (Snapdragon 8 Gen 1 class) · Chrome 157 Android (desktop UA) · screen 1024×640 CSS px @2.5 (≈2560×1600) · model hidden — owner to add | owner's tablet, 19 Nov 2026 |
| three.js on the tablet: fps at 150k triangles, portrait + landscape | ≥ 30 fps | **Portrait: ~60 fps (display rate) at 1–2.5k (3 scenes), ~100k, ~300k and ~600k drawn triangles; 5th-percentile 52–57 fps** (canvas 1197×1046 @2). Landscape not measured yet | owner's tablet (Adreno 730, Chrome 157), 19 Nov 2026, app v2 Measure |
| Triangles before stutter on the tablet | ~300k | **> 600k** (no drop below the display rate at 600k drawn triangles; ceiling not reached) | owner's tablet, 19 Nov 2026 |
| Laptop browser (Chrome) fps at 150k / 400k triangles, 1080p window | ≥ 60 / ≥ 30 fps | | |
| Drive stream: seconds to first frame, 720p (phone, mobile data) | 2–4 s | | |
| Drive stream: seconds to first frame, 1080p (tablet/laptop, Wi-Fi) | 2–5 s | | |
| Episode file size per minute, 720p H.264 | ~8–12 MB | | |
| Episode file size per minute, 1080p H.264 (proposed rung) | ~15–25 MB | | |
| Free storage on the phone for the cache | — | | |
| `tools/layout-check` full sweep time (13 sizes × orientations × 125 % × light/dark) | ~2–5 min on the laptop | V1: 924 checks ≈ 6 min in the cloud workspace (not the laptop) | cloud |

## 3. Production toolchain
| Item | Expected | Measured | Checked on |
|---|---|---|---|
| Blender Eevee 720p, seconds per frame | ~0.5–3 s on a gaming GPU | **1.81 s** (Eevee Next) | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| Blender Cycles + OptiX 720p, seconds per frame (64 spp, denoised) | ~2–10 s | **5.60 s** (OptiX, OptiX denoise) | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| Same at 1080p (decides the 1080p rung, design plan §2) | ~2–2.5× the 720p time | **not measured** — kit ran 720p only; pending (M1 to-do; D-033 rung waits) | |
| 20 s shot at 24 fps, total — Blender Eevee / Cycles | ~5–15 min / ~20–60 min | **14.5 min / 44.8 min** (866 s / 2 689 s wall, 480/480 frames) → a 90 s episode ≈ 65 min Eevee / 3.4 h Cycles | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| 20 s shot — headless three.js recorded to frames (WebGL on GPU?) | minutes | **8.9 s** (0.019 s/frame; 10.9 s wall) — WebGL on the GPU via ANGLE/D3D11, not SwiftShader | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| 20 s shot — Wan 2.2 TI2V-5B (ComfyUI): time per ~5 s clip, VRAM peak, control, accuracy | — | **not run** — 6 GB is likely too small locally; probably online-only (free tier) — pending, D-045 | |
| 720p H.264 NVENC (p5, cq 23) — MB for 20 s, per method | ~3–5 MB | Cycles **0.63** · Eevee **2.75** · three.js **0.78** MB; encode 8.0 / 5.3 / 3.4 s | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| 720p H.264 x264 veryfast crf 23 — MB for 20 s (fallback) | ~3–5 MB | Cycles **0.26** · Eevee **0.30** · three.js **0.27** MB; encode 5.3 / 3.9 / 3.0 s — **x264 smaller and no slower** than Pascal NVENC at 720p/20 s | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| Local TTS voice 1 Kokoro-82M `af_heart`: quality, 20 terms, wpm | — | GPU: load 43 s; 20 terms + sentence in 20.1 s (first term 15.7 s warm-up, then ~0.15 s each); **165 wpm**. Quality + wrong terms: T1 | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| Local TTS voice 2 Piper `en_US-ryan-high`: same | — | CPU: 49.7 s total (includes Python start per call); **197 wpm** (fast for teaching). Quality + wrong terms: T1 | owner's MSI, 20 Nov 2026 · `out\hw.json` |
| Subtitle drift over 90 s after alignment | < 100 ms | | |
| **Host shot M1b-hs01 (Nani, 5 s, 150 frames, Eevee Next, AgX Punchy, cloth-sim shawl, library plate)** — shot render at 360×640, 8 samples | — | **93.4 s** (0.62 s/frame) · v5 preview | owner's MSI, 21 Nov 2026 03:53 · `tools\m1b-host\out\RESULTS.md` |
| Host shot — same at 720×1280 ship (`m1b.py t1b`) | ~4× preview ≈ 6–8 min | **not measured** — v6 ship run pending (T1b) | |
| Host character sheet (8 tiles + cloth sim 70 frames) at preview | — | **55.8 s** (sim 32.4 s) · v5 | owner's MSI, 21 Nov 2026 · `out\build_log_sheet.json` |
| Kokoro `af_heart` host line (4.6 s, speed 0.66) | — | load 3.2 s (warm) · synth 1.26 s · **143 wpm** · step 12.2 s | owner's MSI, 21 Nov 2026 · manifest v5 |
| Host clip size, 5 s 360×640 x264 veryfast crf 20 | — | **0.29–0.30 MB** (clean / cap-en / cap-hi) | owner's MSI, 21 Nov 2026 · v5 |
| Host loudness, v5 (single-pass loudnorm + −2 dB limiter) | −14 LUFS / ≤ −1 dBTP | **−15.17 LUFS / −1.10 dBTP** → missed −14 (D-051 fix) | owner's MSI, 21 Nov 2026 · `out\loudness.json` |
| Host loudness, v6 method (two-pass, `loud.py`) on the same line | −14 ±0.5 / ≤ −1.5 dBTP | **−14.05 LUFS / −2.1 dBTP after AAC**, linear mode (gain +14.7 dB, limiter −2.5 dBTP) | cloud workspace, 21 Nov 2026, FFmpeg — **not the laptop**; laptop value comes with v6 |
| ffmpeg NVENC assemble time for 90 s | < 30 s | | |

## 4. Checks to run (M1 bake-off)
0. Record §1 (`bakeoff.py hw`, or by hand as above).
1. Same 20 s shot M1-ps01 via Blender (Eevee and Cycles/OptiX), headless three.js and Wan 2.2 5B (`bakeoff.py all` + `C_ai\README.md`). Time, effort, file size, accuracy vs Ch 5 and R01 CS7 (look only). Time one method at 1080p too.
2. Play each clip on the phone; note smoothness and label readability (T1). Then one clip on a tablet (both orientations) and the laptop: labels legible, not oversized.
3. TTS: 20 terms × 2 voices; mark mispronounced terms; Kokoro's phonemes (in `tts_stats.json`) seed the pronunciation dictionary.
4. Stream one clip from Drive on the phone over mobile data; time to first frame.
5. Open a 50k-triangle test scene in the phone browser; read fps (V1 if not done here). V1 adds the tablet and laptop rows of §2.

## 5. Results log
| Date | Check | Result | Action |
|---|---|---|---|
| 17 Nov 2026 | Kit dry-run in the cloud workspace (no GPU) | Shared geometry, projection, labels, overlay and x264 encode work: 2D spec preview, 480 frames in 18 s (CPU), 20 s clip 0.43 MB. **Not a laptop measurement** | Run the kit on the laptop |
| 17 Nov 2026 | Laptop render runs | Pending — chat bridge can move files but not run commands | Owner: `python bakeoff.py all` |
| 20 Nov 2026 | M1 kit run, Laptop 1 (`bakeoff.py all`) | Done: Cycles 44.8 min, Eevee 14.5 min, three.js 9 s for the 20 s shot; NVENC + x264 both OK; Kokoro + Piper OK; 3 blind clips. Method C (AI) not run. 1080p not timed | T1 on the phone; owner picks D-024/D-045; 1080p + Method C pending |
| 20 Nov 2026 | Encode | Pascal NVENC (p5 cq 23) files 2.4–9× larger than x264 veryfast crf 23 and not faster at 20 s | Re-measure on a 90 s assemble in R1; default encoder per D-045 |
| 21 Nov 2026 | M1b host kit v1–v5 previews, Laptop 1 (`m1b.py all --preview`) | 5 preview rounds 23:37 → 03:53 IST; v5: no failed parts, QA pass, but −15.17 LUFS (target −14) and ΔE on rendered px info-only | D-051: two-pass loudness, body-vs-plate gate + outline, per-clip manifests; owner runs `m1b.py t1b` (v6, 720p) |

## 6. Known setup facts
- Book PDF: Langman 14e, 429 pp, ~211 MB; in Drive › Projects › Embryo Studio › book/ (uploaded 17 Nov 2026; keep private).
- Render machine: owner's MSI NVIDIA gaming laptop, Windows, Anaconda installed (D-014). Owner reads and approves on the phone.
- Laptop 1 driver: Pascal's last branch is 580 → keep driver 581.x; FFmpeg stays **7.1.1** for NVENC (8.x+ needs a newer NVENC API); Blender stays on 4.5 LTS until a newer release is checked against Pascal. Pin these in R1's kit README.
- Network access in Claude sessions can be off; package installs and model downloads run on the laptop.
- The chat bridge (desktop app) can read/write files under connected folders; it can't run commands unless a device shell tool is offered.
- Exchange format between Blender and three.js: glTF (.glb).
- Second render machine: the Professor's Windows NVIDIA laptop (Laptop 2, D-025); setup in `build/setup-guide.md`.
- Viewing devices to support (D-033): phone, tablet, desktop/laptop — portrait and landscape; classes and test matrix in `build/design-plan.md` §2.

## 7. Laptop layout + M1 kit (D-023)
The **Studio home** can be any folder (D-025): kit paths are relative to the kit; Blender is found on PATH, in `C:\Program Files\Blender Foundation\` or in `<Studio home>\apps\blender*`. Owner's: `D:\Projects\biology_studio\` → `tools\m1-bakeoff\` (kit; later the repo's `tools/`) · `apps\` (Blender portable, ComfyUI — GPL/heavy, never in the repo) · `models\` (TTS voices, AI weights; laptop-only, F4) · `repo\biology-studio\` (from A0). Kit output stays in `tools\m1-bakeoff\out\` (never committed).
**Host kit (M1b, D-048/D-049/D-051):** Studio home `tools\m1b-host\` (runs there; the repo `tools/m1b-host/` holds the same files as the record): `host.json` (one spec) · `lipsync.py` (Kokoro → visemes) · `tex.py` (our textures) · `blender_host.py` (model, cloth sim, plates, probes) · `captions.py` (ASS + VTT, EN/HI) · `de.py` (ΔE00, CVD) · `loud.py` (two-pass loudness) · `m1b.py` (runner; `t1b` = what owner check T1b needs). Output `out\` (never committed) → `out\for_drive\` = this version only, one manifest per clip.
Kit: `shot.json` (one spec) + `common/scene_math.py` (shared geometry; `B_three/shot.js` mirrors it) + `common/overlay.py` (identical day stamp, colour key, scale bar, axis gizmo, labels on every method) → `A_blender/` (Cycles OptiX→CUDA fallback, Eevee; 64 spp; Standard view transform) · `B_three/` (three r170 vendored via npm, Playwright headless, logs the WebGL renderer) · `C_ai/` (Wan 2.2 TI2V-5B in ComfyUI, start image = three.js frame 0, seed 1517) · `D_tts/` (Kokoro + Piper) → `bakeoff.py` (hw, renders, NVENC + x264 encodes, manifests, blind clip-A…D for T1, `RESULTS.md`). Debug (RULES §I): run one step only (`bakeoff.py <step>`), `quick` (every 12th frame), `--every N`, `record.mjs --headed`, `common/preview2d.py` (flat preview, no GPU). Playwright is already in the kit, so `tools/layout-check` (A0) adds no new dependency.
