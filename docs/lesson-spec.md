# Lesson spec — the one definition of a chapter lesson (RULES C2)

*(Purpose: the lesson file format that drives the chapter path (`#lessons`, `#lesson=<ch>`), the lesson bar on a card, Today's Study plan and Mixed review. Updated: 22 Nov 2026 · Bio · Build · L2 lessons (first version; after G-Learn/G-Eng round 1: no separate drill step, MBBS-based time model, Mixed review keeps card order; D-070). Change this spec first, then the code: `tools/lesson-check/` (Python, CI) and `src/js/20-lessons.js` (the app).)*

## 1. Where lessons live
- **One lesson per chapter:** `content/<book>/lessons/<ch>.json` (`content/E/lessons/E05.json`). Chapters with a lesson are listed in `CONFIG.learn.lessons` (order = the chapter path). L2 ships Part 0 (`E00`), Ch 5, Ch 6, Ch 7 and Ch 8.
- **A lesson is split into sittings** (owner pick, 22 Nov 2026): each sitting is one session of up to 15 min (`budget.max`; 10 min is a soft minimum), so a long chapter (Ch 6, 13 cards) is several sittings in one file. A card's steps are never split across two sittings.
- **Ids are permanent (A2):** lesson id `L-<ch>`, sitting ids `s1`, `s2`…, step ids `<card id>:<kind>` (`E05.02.01:check`). Progress is saved per step id, so regrouping sittings never loses progress. A step that is dropped goes into `retired` (never reused); lesson-check compares the file with the last commit (`git show HEAD:<file>`) and fails if a shipped step id disappears without being retired.
- Written by `tools/lesson-check/check.py --write` from the cards, the roadmap order and the time model below; checked by the same tool in CI.

## 2. Fields
```json
{"spec": 1, "id": "L-E05", "book": "E", "ch": "E05", "version": 1,
 "budget": {"min": 10, "max": 15},
 "prereq": ["E00.01.01", "E00.01.04", "E04.01.01"],
 "sittings": [{"id": "s1", "steps": [{"id": "E05.01.01:read", "card": "E05.01.01", "kind": "read", "est_s": 85}, …]}],
 "retired": []}
```
- `ch` — the chapter (`E00` = Part 0). Every card of the lesson belongs to this chapter.
- `prereq` — concept ids from **outside** the lesson that its cards need (`prereq` in `content/<book>/map.json`), roadmap order. The chapter path shows each one with its card status, or *Not in the app yet* when it has no Reviewed card.
- `sittings[].steps[]` — `kind` is one of `read` · `check` · `scene` · `drill` · `remember`; `est_s` = estimated seconds (§4), written by `--write`, recomputed by the check (stale = error).
- `retired` — step ids that were shipped and later dropped (never reused).

## 3. Steps — the order inside a card (G-Learn)
Cards follow **roadmap order** (`curriculum/roadmap.md`: prerequisites first). Each card adds, in this order:
1. **read** — open the card and read it. Done when the card is **Read** (B4).
2. **check** — its Check (every card has one). Done when one Check run has finished (any score — the status chip shows Understood only for a clean run, B4). *Skip for now* moves on and marks the step skipped (it stays open on the path).
3. **scene** — only when the card has a `scene` (no-scene cards skip it, D-058): explore *Try it* — turn it, scrub the days. Done by *Done*. A card's **3D drills** (`rotate` `day` `frames` `label` `folded`; today only E05.02.01 and E05.05.01) run **inside its Check** (D-054), so they get no step of their own; when a drill's latest answer was wrong, the scene step says so and suggests the Check again (G-Learn: a separate drill step only repeated the Check and took away the explore step). The kind **`drill`** is reserved — lesson-check rejects it.
4. **remember** — say each Remember prompt's answer aloud, then open it. Done by *Done*. (Prompts already join the deck on Read; this step does not move the deck.)

A lesson never blocks: any step can be opened from the path, and steps done outside the lesson (a card read from Cards) count.

## 4. Time model (`est_s`) — EDIT in `tools/lesson-check/check.py` `TIME`
- read = words of the **MBBS** body (medical students; General when a card has no MBBS) + This becomes… + Don't confuse, at 150 words/min, + 40 s (opening the card, moving on);
- check = 30 s per mcq + 45 s per order + 60 s per drill question;
- scene = 60 s · remember = 15 s per prompt.
- A sitting's time = the sum of its steps. **Error:** a sitting over `budget.max` (15 min). **Warning:** under `budget.min` (10 min) — allowed when the cards can't be cut into full sittings (cards are kept whole: Ch 6's 13 cards make five sittings, Ch 7 and Ch 8 a short second one).
- Sittings are cut by `--write`: the fewest sittings under `max`; among those the most even (smallest longest, then largest shortest), cards kept whole, roadmap order kept. `version` and `retired` follow the shipped copy (the last commit).
- The model is an estimate; owner check T9 times one real sitting.

## 5. lesson-check (C3) — `tools/lesson-check/check.py`
Fails (exit 1) on: unknown card id · a card that is not Reviewed (`CONFIG.learn.show` statuses: reviewed, shipped) or not in `index.json` · a card from another chapter · a card with no Check (`checks` empty) or no `check` step · steps out of order (§3) or a card split across sittings · a `scene` step on a card with no scene, a scene card without one, any `drill` step · a missing `remember` step on a card with prompts · duplicate step ids · a stale `est_s` · a sitting over budget · cards out of roadmap order · `prereq` not equal to the derived list · a shipped step id gone without `retired` (compared with the last commit — in CI, where the file equals HEAD, with HEAD~1; checkout `fetch-depth: 2`) · a lesson for a chapter outside `CONFIG.learn.lessons` · a Reviewed card of the chapter left out of its lesson (warning). Flags: `--dry-run` (list what would be checked/written), `--debug` (every rule), `--only <ch>`, `--preview` (the path as text: sittings, steps, minutes), `--write` (re-derive the files), `--selftest` (broken copies must each raise their code), `--json`.

## 6. How the app uses a lesson (L2 — `src/js/20-lessons.js`; layout: `build/design-plan.md` §2 Lessons rows, §4.11)
- **`#lessons`** — the chapter path: one row per lesson (chapter name, sittings, minutes, steps done of total, *Continue*). **`#lesson=<ch>`** — one lesson: *Continue where you stopped* (the first step not done or skipped), *Needs first* (prereq chips with status), then each sitting (minutes, steps done) and its steps grouped by card (status chip, ✓ done · ↷ skipped · ○ open; each opens the card at that step).
- **Lesson bar** on a card opened from a lesson (`#card=<id>&lesson=<ch>`): *Lesson · Ch 5 · Sitting 2 · step 3 of 12*, what to do now, *Go to it* (scrolls to Try it / the Check / Remember), *Done* / *Next step* / *Skip for now*, *Back to the lesson*. The Check run rules stay (D-053): the bar never shows card text. The last step of a sitting returns to the lesson with *Sitting done*.
- **Saved** in IndexedDB `biostudio` (add-only, A1): `state.lessons[<ch>] = {done: {<step id>: time}, skip: {<step id>: time}, last: <step id>, t}`. Merge: done/skip keep the earliest time per step; `last` from the newer copy.
- **Today (IB01):** *On the go* (≤ 5 min: up to `CONFIG.today.goPrompts` due Remember prompts via `#deck=go` + one Check) and *Study* (15–30 min: the next lesson sitting + the due prompts + *Checks to pass* — cards with a finished run that are not Understood yet — + optional Mixed review). The one Check = the whole Check of the Understood card least recently used in Mixed review (`#mix=go`, card order, card text hidden), or — before any card is Understood — the Check of the card you are on. A Check step done with a miss says *Not Understood yet*; the lesson's all-done line says when Checks are still to pass.
- **Mixed review (IB03, `#mix`):** `CONFIG.learn.mix.n` (8) questions from Checks of **Understood** cards across chapters, interleaved (no two in a row from one chapter while another has questions left); at most `perCard` (2) per card, **kept in the card's own order** (a card's later question never comes first — D-058 (5)); cards Understood before today are preferred (spaced, not massed) when there are enough. **No card text shown** (D-053) — only the question, then ✓/✗, the right answer, its why and *From the card: <title> · <chapter>* (the chapter shows only after answering). `types` mcq + order only (3D drills stay on their card). It **never changes a card's status** (B4): answers are kept as `mix:<card>:<q>` in `state.answers` and each run in `state.mix.runs` (`{t, n, ok, go}`, newest 60) — they feed recall stats only (Today: 30-day recall %). Opens once `minCards` (4) cards in `minChapters` (2) chapters are Understood; *One Check* (`#mix=go`) once one is.
