# Card spec — the one definition of a concept card (RULES C2)

*(Purpose: the card file format that drives Studio (draft + review), the card reader (L1) and the Remember deck. Updated: 19 Nov 2026 · Bio · Build · S1 studio (v1; terms exception + review-reset rule after the first round trip). Mirrors `docs/scene-spec.md`. Change this spec first, then the code: `tools/card-check/` (Python, CI) and `src/js/15-cards.js` (the same rules in the app's Studio — `card-check --parity` proves they agree).)*

## 1. Where cards live
- One JSON file per concept: `content/<book>/cards/<id>.json`; the list is `content/<book>/cards/index.json` (`{"spec":1,"book","cards":[{"id","title","status","version"}]}`).
- **Id = the concept id** in `content/<book>/map.json` (`E05.01.01`; README). **Permanent once shipped (A2)** — fix wording freely, never renumber or reuse; a retired card keeps its id with `status: "retired"` and is hidden.
- Addresses: `#studio` (card list, testing mode) · `#studio=<id>` · `#studio=<id>&pane=draft|review|sources&gate=G-Sci` · `#calib` (calibration). Later (L1): `#card=<id>`.
- Checked by `tools/card-check` (C3) before anything ships; CI runs it on every push.
- Derived look-up file: `content/<book>/sources.json` — registry ids (from `research/source-registry.md`), decision ids (from `claude/DECISIONS.md`), section ids + headings (from `content/<book>/index/tree.json`) and glossary term ids (from `index/terms.json`). Written by `card-check --write-sources`; card-check fails if it is out of date. The app's Studio reads only this file (headings and term names — no book text, G1).

## 2. Fields
| Field | Type | Rule |
|---|---|---|
| `spec` | 1 | this spec's version |
| `id` | concept id | = file name; must exist in `map.json` |
| `version` | int ≥ 1 | stays 1 until first ship, then bump on every change (as scenes, H7) |
| `book` | `"E"` | book code |
| `status` | `draft` · `reviewed` · `shipped` · `retired` | §5 |
| `title` | string | short, our words (G2); may differ from the map name |
| `tier` | `A`–`D` | depth tier (README) |
| `objective` | `{verb, text}` | **one testable objective, one verb** (H1, playbook §4.1): `verb` ∈ §3 list; `text` starts with that verb and joins no second one ("Explain … and order …" fails) |
| `body` | `{<level>: text}` | our-words body per audience level (D-016): `general` and `mbbs` required; `school`, `neet`, `pg` optional. Every sentence carries fact refs `[f1]` / `[f1,f2]` (§4) except a question (ends with `?`, the hook). Word budget per level (§3) |
| `facts` | [fact] | `{id:"f1", text, cite, mark, where:"main"\|"more", decision?, note?}` — one atomic claim each (playbook §3.1), our words, cited (§4) and marked (B7) |
| `terms` | `{new:[term id], known:[term id], exception?}` | glossary ids `E.t.<slug>` from `index/terms.json`; **≤ 3 new** (D2), or **≤ 5 with `exception: "D-0xx"`**, a logged DECISIONS entry saying why (first use: D-037); `known` = taught by a prerequisite in the map (not by this card's own scene) |
| `misconceptions` | [mis] | `{id:"m1", wrong, right, cite, mark}` — from the dossier §5 list; refutation = state the wrong idea, then correct it (playbook §3.4) |
| `checks` | [check] | ≥ 2: `{id:"q1", type:"mcq"\|"order", prompt, options:[3–5], answer, why, tests:"objective", refutes?:"m1"}` — `mcq`: `answer` = index of the **one** right option; `order`: `options` are listed in the right order, the app shuffles. ≥ 1 check refutes a misconception |
| `adult` | string | optional "this becomes…" line (D4), with fact refs |
| `scene` | `{id, day?}` | the scene that shows it (`sc-<id>`, scene-spec); the scene's `cards` should list this card |
| *reserved (C1 / L1)* | `remember`, `clinical`, `shows_up` | master plan §5 card parts not built in S1: **Remember** `[{q, a}]` recall prompts with fact refs · **Clinical link** text with fact refs (CC boxes) · **Where it shows up** `[concept id]`. AN codes come from `map.json`; Watch it / Try it come with R1 / L1. C1 adds them to this spec's rules and card-check before filling them (C2) |
| `made` | `{by, role, agent, date}` | who drafted it: person, crew role (playbook §1), which chat/agent, date — editable in Studio's draft pane |
| `review` | `{<gate>: review}` | §5 — `{result:"pass"\|"fail", by, role, agent, date, checklist:{item:true}, lines:{<line id>:"ok"\|"fix: note"}, notes}` — the latest review per gate; earlier rounds stay in `log` |
| `log` | [{date, ev, by}] | status changes and reviews, newest last |

## 3. Verbs, levels, budgets
- **Objective verbs:** `explain` `describe` `identify` `label` `locate` `order` `compare` `distinguish` `predict` `name` `trace` `relate`. Spatial verbs (`identify`, `label`, `locate`, `order`) need at least one spatial check (`order` now; `label` in L1) — playbook §4.6.
- **Levels and body budgets (words, refs not counted):** `general` 90 · `school` 110 · `neet` 140 · `mbbs` 160 · `pg` 200. Sentences ≤ 25 words (master plan §6). A level's text must make sense alone (B10: terms explained on first use at `general`).
- **New terms ≤ 3 per card** (D2); up to 5 only with a logged exception (`terms.exception`).

## 4. Citations + marks (B1, B6, B7) — `validate_citation`
- Grammar: `cite = sections [" · " sources]` · `sections = sec ("," sec)*` · `sec = E<ch>.<sec> [locator]` or a chapter `E<ch>` · `sources = src ("," src)*` · `src = R<nn>[a-z] [locator]` or a cross-chapter `E<ch>[.<sec>]`. Locators are short words after the id: `CC` (Clinical Correlates box), `Tbl 6.4`, `Fig 6.1`, `CS7`. No ranges (`E05.01, E05.02`, not `E05.01–02`).
- A cite with **no book section** (starts with `· `) is allowed only for ✚.
- `validate_citation(cite)`: every section id exists in `index/tree.json` (chapter ids in its chapters); every `R…` id exists in the registry (`sources.json`). In the app it is `validateCitation()` in `src/js/15-cards.js`; in tools `tools/card-check/citations.py`.
- **Mark rules:** ✔✔ needs a book section + ≥ 1 Tier 1 source · ✔ = book section (Tier 2–3 sources can't lift it) · ⚑ needs `decision: "D-0xx"` that exists in DECISIONS; the card gives the book answer, the newer evidence goes in a `more` fact · ✚ = no book section or beyond it, Tier 1 only, `where: "more"` only, text labelled "beyond Langman" · **≈ blocks** `reviewed` and `shipped`.
- **Mark suggester** (calibration): decision → ⚑; no book section → ✚; book + Tier 1 → ✔✔; else ✔. It proposes; the reviewer decides (a Tier 1 source can *disagree* — that is a ⚑, which only a person can see). `#calib` and `card-check --calibrate` score it against 5 dossier facts (`cards/calibration.json`); it must get 5/5.

## 5. Status, gates, reviewers (H2)
| Status | Needs | Set by |
|---|---|---|
| `draft` | card-check runs (≈ allowed, as a warning) | maker (Studio or a Content chat) |
| `reviewed` | card-check **0 errors**, no ≈; **G-Sci** and **G-Learn** = pass, every line `ok`, every checklist item ticked; each reviewer's `role` **and** `agent` differ from `made` (a different role, fresh eyes) | Studio, when both gates pass |
| `shipped` | reviewed + **G-A11y** pass (fresh eyes) + **G-Owner** pass (owner, `by` = the owner) | Studio / Content chat after the owner's OK |
| `retired` | — (hidden, id kept, A2) | owner |
- **Any content edit clears every pass and the review ticks** (a pass is for the card as reviewed); failed reviews stay as history. A `reviewed`/`shipped` card goes back to `draft`. Studio does this and says so; a chat editing a card by hand does the same and logs it.
- A new review starts blank; only a standing pass shows ticked.
- Gate checklists (shown on the review card): **G-Sci** — every fact cited + marked · cites point at the right sections · anatomy, timing, scale right vs book + Tier 1 · ⚑ has its D-entry and the book answer · ✚ only in More · no ≈. **G-Learn** — objective is one testable verb · Checks test the objective · ≥ 1 Check refutes a misconception · ≤ 3 new terms, explained at General · body within budget, one idea per sentence · "this becomes…" where it fits (D4). **G-A11y** — plain text alternatives for every visual · Checks work by keyboard + touch · no colour-only cue in text ("the orange layer") · 125 % text fits.
- Review lines (the "approve / fix line by line" rows): **G-Sci** signs every body sentence `body.<level>.<n>`, every fact `f<n>`, every misconception `m<n>` and `adult`; **G-Learn** signs `obj`, `terms`, every check `q<n>` and every misconception. G-A11y and G-Owner are checklist only. A line is `ok` or `fix: <note>`; any fix = fail, and the Studio copies a ready `Bio · Fix · <id>` prompt with the notes.
- Checklist item ids (stored in `checklist`): G-Sci `cited sections accuracy flags plus noapprox` · G-Learn `objective checks refutes terms budget adult` · G-A11y `alt input colour text125` · G-Owner `owner`.

## 6. card-check (C3) — `tools/card-check/check.py`
Errors (block): `E-schema` field missing/wrong type · `E-id` id ≠ file or not in map · `E-objective` missing, verb not allowed, not one verb · `E-cite` validate_citation failed · `E-mark` missing/unknown mark or breaks a §4 rule · `E-approx` ≈ in a reviewed/shipped card · `E-ref` body sentence without a fact ref, or a ref to no fact · `E-words` body over budget · `E-sentence` > 25 words · `E-terms` > 3 new (> 5 with an exception), an exception not in DECISIONS, or an unknown term id · `E-check` < 3 options, not exactly one answer, no `why`, `tests` ≠ objective · `E-checks` < 2 checks, none refutes a misconception, spatial verb without a spatial check · `E-mis` misconception field missing or uncited · `E-scene` scene not in `scenes/index.json`, or `day` not a number inside its days · `E-status` status not backed by the gates (§5) or a reviewer = the maker · `E-level` `general`/`mbbs` missing · `E-index` index.json out of step with the files · `E-sources` sources.json stale.
Warnings (draft only): `W-approx` ≈ present · `W-terms` a map term of this concept not in the card · `W-scene-cards` the scene doesn't list this card.
Flags (RULES I5): `--only <id>` · `--dry-run` (list what would be checked) · `--debug` (every rule as it runs) · `--preview` (one card's level texts as plain text, fast) · `--json` · `--write-sources` · `--calibrate` · `--parity` (runs the app's `cardCheck()` in headless Chromium on every card and compares error codes).
