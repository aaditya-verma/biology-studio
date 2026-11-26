# Episode spec — the one definition of an episode's data (RULES C2)

*(Purpose: the episode file format the episode builder writes, the render pipeline (R1) reads and the player (L3) plays: script lines per profile, shots, builder checks; spec 2 adds learner-paced **ideas** and the **"Meet the parts" primer** (D-107). Created: 26 Nov 2026 · Bio · Fix · video craft (spec 1 written down as built for S1E01, spec 2 added; docs only, no code yet).)*

## 1. Where episodes live
- **Data (source of truth):** `content/E/episodes/<id>/` — `script.json` (lines per profile), `shots.json` (shot list), `checks.json` (the builder's check report, not the in-video Checks). Episode id `S<season>E<nn>` (`S1E01`).
- **Human-readable copies:** `studio-docs/episodes/<id>/` (brief, script, table read, storyboard); `script.md` is written by the builder, never edited by hand (D-102 (9)).
- **Builder:** `tools/episode/build.py` (+ per-episode data module, e.g. `s1e01_data.py`; `render_docs.py`). It writes the JSON and runs the pipeline checks (lexicon, terms per 60 s, lengths, wpm).
- **Ids are permanent (A2):** line ids, shot ids, idea ids. A dropped id goes into the file's `retired` list and is never reused.

## 2. Spec 1 (as built, S1E01)
**`script.json`**
| Field | Meaning |
|---|---|
| `spec` | format version (`1`, or `2` once §3 fields are present) |
| `episode`, `title` | id + title |
| `wpm` | the script's speech rate by construction (143, D-102 (1)) |
| `profiles{}` | one entry per cut: `lesson` (MBBS Lesson), `general` (General Lesson cut), `short` (9:16 Short) — name, frame, level, depth, type, `length_target` [min, max] s, language, host |
| `scripts{}` | per profile, an ordered list of **lines** (below) |
| `lengths_s{}` | built length per profile (s) |
| `needs{}` | `N1…`: visual/tool needs, each with its owning step |

**Line** (`scripts.<profile>[]`): `id` (profile letter + number: `L` Lesson, `G` General, `R` Short; suffix `a` for a Check's reveal, e.g. `L31a`) · `seg` (segment: a 60–120 s group of ideas, e.g. `"2 The dive"`; chapters are ideas, §3) · `shot` (shot id) · `text` (spoken words) · `facts[]` (card fact refs `E05.01.03#f1`) · `refs[]` (ref, mark, section, cite — filled by the builder from the cards) · `new[]` (new terms introduced on this line, D2) · `hold` (s of picture after the words) · `kind` (optional: `question`, `terms`, `frame`, `reveal`, `check`, `flag-pointer`, `analogy`, `teaser`, `endcard`) · `check` (on `kind: check`: what the Check asks) · `title` (Short chapter title, ≤ 4 words, D8). Fields starting `_` are computed by the builder (`_start`, `_words`, `_dur`); never edit them.

**`shots.json`:** `spec`, `episode`, `shots[]` (`id`, `kind`, `scene`, `day`, `what`, `cams`, `key`, `labels[]`, `tag`, `needs[]`), `needs{}`.

**`checks.json`:** builder report — `errors[]`, `warnings[]`, `lengths`, `words`, `wpm_speech`, `wpm_overall`, `new_terms`, `max_terms_per_60s`.

## 3. Spec 2 — ideas + primer (D-107; add only)
Spec 2 only **adds** fields; a spec 1 file stays valid and plays as **Watch** (no idea pauses, no primer chips, no Skip offer; a spec 1 `kind: terms` strip plays as part of the video; C1 opt-in).

**Idea** = one learning objective (H1), 20–60 s, ending on a reveal hold. Episode → segment (60–120 s, `seg`) → idea. Studio playbook §6b.1 has the craft rules.

```json
"ideas": {
  "lesson": [
    {"id": "S1E01.L.i01", "from": "L01", "to": "L07",
     "objective": "<one testable objective (H1)>", "check_by": "<Check line id, quiz item or card id>",
     "title": "<≤ 4 words>", "next_q": "<≤ 6 words, optional>"}
  ],
  "general": [ … ]
},
"primer": {
  "lesson": {"parts": [
    {"term": "<GLOSSARY term>", "line": "L02", "card": "<card id>", "token": "<colour token>", "view": "<still view or ≤ 15° turntable>"}
  ], "hold": 2.0},
  "general": { … }
},
"retired": []
```
| Field | Rule |
|---|---|
| `ideas.<profile>[]` | Lesson profiles only (`lesson`, `general`); **never** `short` (Shorts never pause). Ordered and contiguous, covering every line from the first to the last; the first idea holds the cold open and the primer. |
| `id` | `<episode>.<profile letter>.i<nn>` (`S1E01.L.i03`, `S1E01.G.i02`); permanent (A2). |
| `from`, `to` | first + last line id (inclusive). The break is at the end of `to`'s hold. |
| `objective` | one testable objective (H1); one idea = one objective (RULES D2). |
| `check_by` | what tests the objective (H1): an in-video Check line id (`L31`), an episode-quiz item, or a card id whose Check tests it. Required; the builder fails an idea without one. |
| `title` | ≤ 4 words (D8); shown in the app (idea pause panel, scrubber tick, transcript head), never in the frame. |
| `next_q` | optional, ≤ 6 words: the open loop the voice already set up (playbook §6b.1). |
| `primer.<profile>` | Lesson profiles only. `parts[]` ≤ 3: `term` (GLOSSARY), `line` (the line that names it), `card` (its concept card), `token` (colour token + pattern = the episode's colour key), `view`. `hold` = end hold, s (2.0). |

**Builder checks (spec 2):** each idea 20–60 s; ideas contiguous and non-overlapping; every break lands at a reveal hold ≥ 1.5 s with no speech within 0.3 s either side, never mid-line, never between a Check and its reveal, never within 10 s after a reveal of a Check, never inside or at the end of the cold open (≤ 10 s) or of the primer (the first idea runs from the cold open through the primer to the first reveal in segment 1); the builder **proposes** breaks snapped to the nearest hold and the story director signs them (G-Story). Primer terms go in their line's `new[]` and count toward D2's ≤ 3 new terms in any rolling 60 s (`max_terms_per_60s`); a term introduced in Part 0, an earlier Part or on a Ready-to-watch core card counts as review (decided at build time, not per learner). Every idea has a `check_by`. `chapters.vtt` (R1) is written from `ideas[]`, one cue per idea titled `title` (chapters = ideas; segments are coarse groups).

## 4. Versioning
- `spec` goes 1 → 2 only when §3 fields are added; readers accept both.
- A new field is added, never renamed or repurposed; removing a field needs a D-entry and a reader update in the same change.
