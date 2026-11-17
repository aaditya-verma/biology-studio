# Biology Studio

Turns a biology book or topic into a concept map, cited concept cards and story-led 3D videos. First book: Langman's Medical Embryology 14e (code `E`).

- **Start here:** [`studio-docs/build/setup-guide.md`](studio-docs/build/setup-guide.md)
- **Project docs** (the single shared copy): `studio-docs/`. Read `claude/STATUS.md` first.
- **App** (A0 shell, v1): `index.html` + `src/` + `content/strings.js` — plain scripts, no build step. Run locally: `python -m http.server` here, open http://localhost:8000. Testing mode `?test=1`, debug `?debug=1`. Design: `studio-docs/build/design-plan.md`.
- **Checks:** `python tools/layout-check/check.py [--preview]` (Playwright) — also in CI on every push.
- `tools/` — kits and scripts (`m1-bakeoff`, `indexer`, `map`, `layout-check`) · `content/E/` — derived data only (index, map).
- Licences: [`THIRD_PARTY.md`](THIRD_PARTY.md).

No book text, figures or page images are kept here (RULES §G). Public from 18 Nov 2026 (D-035); the app: https://aaditya-verma.github.io/biology-studio/
