# Third-party licences (RULES H10)

*(Purpose: every library, model and asset the project uses, with its licence and where it may live. Updated: 18 Nov 2026 · Bio · Build · A0 shell (app uses no third-party code: system fonts, own icons).)*

**Stub.** Licences below are ≈ until checked against each project's own licence file (do that before A0 ships). "Repo" = may be committed; "Laptop" = installed per person, never committed.

| Name | Used by | Licence | Lives |
|---|---|---|---|
| three.js 0.170.0 | `tools/m1-bakeoff/B_three` | MIT | npm install (node_modules ignored); vendored into the app at A0 |
| Playwright | `B_three/record.mjs`; `tools/layout-check` (Python) + CI | Apache-2.0 | npm / pip install |
| GitHub Actions `checkout`, `setup-python`, `upload-artifact` | CI | MIT | GitHub-hosted |
| pypdf | `tools/indexer` | BSD-3-Clause | pip |
| Poppler (pdftotext) | `tools/indexer` | GPL-2.0+ | Laptop (external program) |
| Blender 4.2 LTS+ | `A_blender` | GPL-3.0+ (our scripts and renders are ours) | Laptop |
| ffmpeg | kit encodes | LGPL/GPL (build-dependent) | Laptop |
| NumPy | kit | BSD-3-Clause | pip |
| Pillow | `common/overlay.py`; layout-check contact sheets | MIT-CMU (HPND) | pip |
| PyTorch | `D_tts` | BSD-3-Clause | pip |
| soundfile | `D_tts` | BSD-3-Clause | pip |
| Kokoro-82M + `af_heart` | `D_tts` (V-a) | Apache-2.0 | Laptop `models/` |
| Piper + `en_US-ryan-high` | `D_tts` (V-b) | GPL-3.0 (engine); voice per its MODEL_CARD | Laptop `models/` |
| ComfyUI | `C_ai` | GPL-3.0 | Laptop `apps/` |
| Wan 2.2 5B | `C_ai` (O4, filler only, H9) | Apache-2.0 | Laptop `models/` |
| Z-Anatomy meshes | video only (D-021) | CC BY-SA 4.0 (BodyParts3D CC BY-SA 2.1 JP) | Laptop/Drive only — never repo/app |

Credit line for any video using Z-Anatomy (D-021): "Adult anatomy: Z-Anatomy (CC BY-SA 4.0), based on BodyParts3D © DBCLS (CC BY-SA 2.1 JP), modified".
