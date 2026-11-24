# S1E01 animatic (P1 ②)

*(Purpose: the three.js animatic of S1E01 — scratch voice, three cuts, player, recorder, layout check. Owner docs: `studio-docs/episodes/S1E01/storyboard.md`, `studio-docs/build/visual-style.md` §1/§10/§12. Created 25 Nov 2026, `Bio · Episode · S1E01 animatic`, D-104.)*

**Where it runs:** Studio home `tools\s1e01-animatic\`. This repo copy is the versioned record of the same files. Audio (`audio/`) and everything in `out/` stay out of the repo. If an edit is made here, copy it to Studio home before running, and the other way round.

Run from the repo root, through `tools/live/live.py` (RULES I9):
1. `voice.py` (venv-bio python) — Kokoro `af_heart`, one WAV per line, speed per cut (Lesson 0.80 · General 0.75 · Short 0.80, D-104), table-read pronunciation dictionary → `timings.json` (planned and measured).
2. `timeline.py` — shot times = measured lines + scripted holds; captions aligned to words; −14 LUFS cut audio → `out/`.
3. `check.mjs` — 5 sizes × 3 cuts: caption bands, overlaps, leaders, frame edges, the N4 path inside its sheet → `out/check.json`, `out/layout/`.
4. `record.mjs --cut lesson|general|short` — 720p MP4; `--shots` = stills. `sheet.py` = contact sheets.

Player: serve Studio home, open `/tools/s1e01-animatic/` with `?cut=` · `?t=` · `?debug=1` · `?boxes=1` · `?test=1` (✎ hooks) · `?safe=1` · `?rm=1`.

**EDIT:** positions in `bands.mjs`, cameras and states in `shots.mjs`. **Stubs, labelled on screen:** N1 host card · N3 + N4 marked cell and `t-meso` · N6 ectoderm token · N8, N9 schematics.
