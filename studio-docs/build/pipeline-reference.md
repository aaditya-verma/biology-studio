# Pipeline reference — Expected vs Measured

*(Purpose: laptop, phone, tablet, desktop, render and voice numbers; build only on Measured. Updated: 18 Nov 2026 · Bio · Fix · doc reconcile — ported from the uploaded copy (D-033): §2 phone + tablet + desktop, 1080p rows in §2–§3, §4 check 2.)*

Rule C4: build only on the **Measured** column. Expected values are rough starting guesses, to be replaced by measurements (M1 onwards). Fill "Checked on" with date + device. Local-first on the owner's NVIDIA laptop (D-014, RULES C12).

## 1. Laptop 1 — owner's render machine (fill first in M1)
| Item | Expected | Measured | Checked on |
|---|---|---|---|
| Maker / OS family | — | MSI · Windows x64 | 17 Nov 2026 · desktop-app bridge |
| GPU model + driver (`nvidia-smi`) | NVIDIA gaming GPU (owner: runs Adobe apps, F1 games) | | |
| VRAM | 6–16 GB (decides local video models) | | |
| CPU / RAM / free disk / OS version | — | | |
| Blender OptiX available | yes on RTX cards | | |
| ffmpeg NVENC (h264_nvenc / hevc_nvenc) works | yes | | |

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
| Phone model / Android / Chrome version | — | | |
| three.js on owner's phone: fps, 50k-triangle embryo scene | ≥ 30 fps | | |
| Triangles before stutter on the phone | ~150k | | |
| Tablet model / OS / browser (owner's or Professor's) | — (not recorded yet) | | |
| three.js on the tablet: fps at 150k triangles, portrait + landscape | ≥ 30 fps | | |
| Triangles before stutter on the tablet | ~300k | | |
| Laptop browser (Chrome) fps at 150k / 400k triangles, 1080p window | ≥ 60 / ≥ 30 fps | | |
| Drive stream: seconds to first frame, 720p (phone, mobile data) | 2–4 s | | |
| Drive stream: seconds to first frame, 1080p (tablet/laptop, Wi-Fi) | 2–5 s | | |
| Episode file size per minute, 720p H.264 | ~8–12 MB | | |
| Episode file size per minute, 1080p H.264 (proposed rung) | ~15–25 MB | | |
| Free storage on the phone for the cache | — | | |
| `tools/layout-check` full sweep time (13 sizes × orientations × 125 % × light/dark) | ~2–5 min on the laptop | | |

## 3. Production toolchain
| Item | Expected | Measured | Checked on |
|---|---|---|---|
| Blender Eevee 720p, seconds per frame | ~0.5–3 s on a gaming GPU | | |
| Blender Cycles + OptiX 720p, seconds per frame (64 spp, denoised) | ~2–10 s | | |
| Same at 1080p (decides the §8a 1080p rung) | ~2–2.5× the 720p time | | |
| 20 s shot at 24 fps, total — Blender Eevee / Cycles | ~5–15 min / ~20–60 min | | |
| 20 s shot — headless three.js recorded to frames (WebGL on GPU?) | minutes | | |
| 20 s shot — Wan 2.2 TI2V-5B (ComfyUI): time per ~5 s clip, VRAM peak, control, accuracy | — | | |
| 720p H.264 NVENC (p5, cq 23) — MB for 20 s, per method | ~3–5 MB | | |
| 720p H.264 x264 veryfast crf 23 — MB for 20 s (fallback) | ~3–5 MB | | |
| Local TTS voice 1 Kokoro-82M `af_heart`: quality, 20 terms, wpm | — | | |
| Local TTS voice 2 Piper `en_US-ryan-high`: same | — | | |
| Subtitle drift over 90 s after alignment | < 100 ms | | |
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

## 6. Known setup facts
- Book PDF: Langman 14e, 429 pp, ~211 MB; in Drive › Projects › Embryo Studio › book/ (uploaded 17 Nov 2026; keep private).
- Render machine: owner's MSI NVIDIA gaming laptop, Windows, Anaconda installed (D-014). Owner reads and approves on the phone.
- Network access in Claude sessions can be off; package installs and model downloads run on the laptop.
- The chat bridge (desktop app) can read/write files under connected folders; it can't run commands unless a device shell tool is offered.
- Exchange format between Blender and three.js: glTF (.glb).
- Second render machine: the Professor's Windows NVIDIA laptop (Laptop 2, D-025); setup in `build/setup-guide.md`.
- Viewing devices to support (D-033): phone, tablet, desktop/laptop — portrait and landscape; classes and test matrix in master plan §8a.

## 7. Laptop layout + M1 kit (D-023)
The **Studio home** can be any folder (D-025): kit paths are relative to the kit; Blender is found on PATH, in `C:\Program Files\Blender Foundation\` or in `<Studio home>\apps\blender*`. Owner's: `D:\Projects\biology_studio\` → `tools\m1-bakeoff\` (kit; later the repo's `tools/`) · `apps\` (Blender portable, ComfyUI — GPL/heavy, never in the repo) · `models\` (TTS voices, AI weights; laptop-only, F4) · `repo\biology-studio\` (from A0). Kit output stays in `tools\m1-bakeoff\out\` (never committed).
Kit: `shot.json` (one spec) + `common/scene_math.py` (shared geometry; `B_three/shot.js` mirrors it) + `common/overlay.py` (identical day stamp, colour key, scale bar, axis gizmo, labels on every method) → `A_blender/` (Cycles OptiX→CUDA fallback, Eevee; 64 spp; Standard view transform) · `B_three/` (three r170 vendored via npm, Playwright headless, logs the WebGL renderer) · `C_ai/` (Wan 2.2 TI2V-5B in ComfyUI, start image = three.js frame 0, seed 1517) · `D_tts/` (Kokoro + Piper) → `bakeoff.py` (hw, renders, NVENC + x264 encodes, manifests, blind clip-A…D for T1, `RESULTS.md`). Debug (RULES §I): run one step only (`bakeoff.py <step>`), `quick` (every 12th frame), `--every N`, `record.mjs --headed`, `common/preview2d.py` (flat preview, no GPU). Playwright is already in the kit, so `tools/layout-check` (A0) adds no new dependency.
