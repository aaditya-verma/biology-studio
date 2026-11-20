# Third-party licences (RULES H10)

*(Purpose: every library, model and asset the project uses, with its licence and where it may live. Updated: 20 Nov 2026 · Bio · Fix · Visual style 2 port — real-media section mirroring the registry § Media (D-046). Before: 18 Nov 2026 · Bio · Build · V1 viewer — three.js r170 vendored into the app; its licence checked against the file.)*

Licences marked ✔ were checked against the project's own licence file; the rest stay ≈ until checked. "Repo" = may be committed; "Laptop" = installed per person, never committed.

| Name | Used by | Licence | Lives |
|---|---|---|---|
| three.js r170 (0.170.0) | **app 3D viewer** (`lib/three-r170/three.module.min.js`, sha256 `08fd7545…c39e7`, from the `r170` tag of mrdoob/three.js `build/`); `tools/m1-bakeoff/B_three` (npm) | MIT ✔ (`lib/three-r170/LICENSE`, © 2010-2024 three.js authors) | **Repo** (vendored, pinned — RULES C5, D-006/D-019); kit: npm install |
| Playwright | `B_three/record.mjs`; `tools/layout-check`, `tools/stills` (Python) + CI (pinned 1.63.0) | Apache-2.0 | npm / pip install |
| GitHub Actions `checkout`, `setup-python`, `upload-artifact` | CI | MIT | GitHub-hosted |
| pypdf | `tools/indexer` | BSD-3-Clause | pip |
| Poppler (pdftotext) | `tools/indexer` | GPL-2.0+ | Laptop (external program) |
| Blender 4.2 LTS+ | `A_blender` | GPL-3.0+ (our scripts and renders are ours) | Laptop |
| ffmpeg | kit encodes | LGPL/GPL (build-dependent) | Laptop |
| NumPy | kit; `tools/stills` (image compare) | BSD-3-Clause | pip |
| Pillow | `common/overlay.py`; layout-check contact sheets | MIT-CMU (HPND) | pip |
| PyTorch | `D_tts` | BSD-3-Clause | pip |
| soundfile | `D_tts` | BSD-3-Clause | pip |
| Kokoro-82M + `af_heart` | `D_tts` (V-a) | Apache-2.0 | Laptop `models/` |
| Piper + `en_US-ryan-high` | `D_tts` (V-b) | GPL-3.0 (engine); voice per its MODEL_CARD | Laptop `models/` |
| ComfyUI | `C_ai` | GPL-3.0 | Laptop `apps/` |
| Wan 2.2 5B | `C_ai` (O4, filler only, H9) | Apache-2.0 | Laptop `models/` |
| Z-Anatomy meshes | video only (D-021) | CC BY-SA 4.0 (BodyParts3D CC BY-SA 2.1 JP) | Laptop/Drive only — never repo/app |

Credit line for any video using Z-Anatomy (D-021): "Adult anatomy: Z-Anatomy (CC BY-SA 4.0), based on BodyParts3D © DBCLS (CC BY-SA 2.1 JP), modified".

## Real images and footage in videos (D-046)
Mirror of `studio-docs/research/source-registry.md` § Media (owner of the rows; rules: `studio-docs/build/visual-style.md` §16). CC0, CC BY or public domain only — never CC BY-SA, NC or ND. Videos only; these files never enter the repo or app.

| Id | What | Credit | Licence | Lives |
|---|---|---|---|---|
| — | *(none yet)* | | | |
