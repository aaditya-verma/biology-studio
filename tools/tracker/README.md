# tools/tracker — progress map data + check (W1, D-040)

*(Purpose: the format of `studio-docs/build/steps.json` and how chats update it. Updated: 22 Nov 2026 · Bio · Design · U1 look canvas (approval + draft-id rules, D-077). Before: 22 Nov 2026 · Bio · Fix · open-run first (step 2: open run pushed first, closed at the end). Before: 21 Nov 2026 · Bio · Build · W2 scheduler (schema 2, D-063). Before: 19 Nov 2026 · Bio · Build · W1 progress map.)*

`studio-docs/build/steps.json` is the **owner doc for step status, dependencies, gates, owner checks and owner inputs**. The app draws it at
https://aaditya-verma.github.io/biology-studio/#progress (Map · Board · Your inputs) and `#step=<id>`, reading it live from the repo.

## Every chat that changes a step
1. Edit the step's row (status, gates, check, log, todo, inputs). Add a new step as a new row at the end of its lane.
2. Add a **run** to the step's `runs` (chat, by, start, end, outcome; commit if known) — every chat that worked on it, even a partial one. **Open run first** (RULES I8 (8)): right after the start checks, write the run with no `end` (outcome `partial`) and push it (route A) or have the owner run `sync.bat` (route B), before any other work; at the end, close it (set `end`, `outcome`, `commit`).
3. `python tools/tracker/check.py --write` — re-derives `unblocks` and formats the file. Then `python tools/tracker/check.py` must PASS (CI runs it).
4. Collaborator chats (the Professor) **don't change `status`** — they set `proposed_by`, `proposed_status`, `proposed_on`; the owner's next chat confirms (sets `status`, deletes the three fields) or rejects (deletes them).

## Row fields
| Field | What |
|---|---|
| `id` | Permanent (RULES A2). Build ids from README (`M1`, `C1`…), `W1`, `X1.<ch>` per chapter, `GATE`, `IB<nn>` = backlog item, Ideation rows `PB UR QB DR`, later `D1 G1`. |
| `title`, `type` | Short name; type = chat type = map lane: Ideation · Build · Research · Content · Episode · Review · Fix · Idea. |
| `chat` | `Bio · <Type> · <Step>` — the name the next chat uses. |
| `status` | idea · planned · ready · in progress · gates · owner check · done · parked · proposed. |
| `needs` / `unblocks` | Step ids it needs; `unblocks` is **derived** (never hand-edit). A need is met when that step is `done` or `owner check`. |
| `lock` | true = the chat takes the build lock (STATUS § Lock). |
| `gates` | `{"G-Eng": "open"|"pass"|"fail"|"na"}`. |
| `check` | `null` or `{"id": "T2", "state": "open"|"pass"|"fail"|"na", "since": "YYYY-MM-DD", "by": "Professor"}` (since/by optional). |
| `decisions` | D-ids. `prompt` = key of `**Ready prompt — <key>**` in master plan §13 (or null). |
| `log` | Last build-log line (short). `todo` = carried pendencies that are not the owner's. |
| `inputs` | What the owner owes: `{"id": "C1.q1", "kind": "decide"|"ask"|"action", "ask", "asked_in", "asked": "YYYY-MM-DD", "answer", "status": "open"|"answered"|"closed", "d": "D-037", "blocks": true?}`. `blocks: true` = the step can't start until answered. |
| `size` | Ideas only: S/M/L from the backlog. |
| `uses` | W2: extra resources it holds while it runs — `gpu`, `research`, or `["prof"]` (a professor-only step: optional, never needed by another step). The lock comes from `lock`. Row = first of lock · gpu · research · owner. |
| `est` | W2: `{"chats": 1, "owner_min": 15, "days": 7}` — chats it takes (default by type: `calendar.chats` or PLAN_DEF), your minutes, and whole days to wait after its needs end (e.g. GATE's 7 days of use). |
| `produces` / `consumes` | W2: named outputs (`dossier-ch10`, `cards-ch6-8`…). A consumed output needs a producer, and the consumer must (indirectly) need that producer. |
| `runs` | W2: `[{"chat", "by", "start": "YYYY-MM-DD[ HH:MM]", "end", "outcome": "done"\|"partial"\|"stopped"\|"fail", "commit", "note"}]` — no `end` = a chat is working on it now (two open runs on the lock or GPU row fail CI). More runs than `est.chats` = slipped. |
| `improves` | W2: for professor-only steps — what her input would improve (shown on Plan). Inputs take `for: "prof"` + `improves` too; a professor input may not `blocks`. |

## Top-level fields (W2, D-063)
`calendar` = `{"day_min": [Mon…Sun minutes of your chat time], "chat_min": 60, "check_min": 15, "input_min": 10, "off": ["YYYY-MM-DD"], "chats": {type: chats}, "note"}` · `queue` = the plan order for priority (D-047; steps not in it follow in file order). Dates are never stored — the app and `--next` compute them from today.

**Draft id clash (error, D-077):** a committed `studio-docs/**/*-draft*.md` whose `Decision: **D-nnn**` line (first 12 lines) names a D-id that DECISIONS uses for another decision, or two drafts propose the same id.

## check.py
`--next` (the schedule: rows, critical path, your inputs ranked — what a chat reads first; `--json`, `--today YYYY-MM-DD`; `--write` refreshes the auto block in STATUS § Next) · `--write` (`--dry-run` shows changes) · `--only <id>` · `--preview` (text board + inputs) · `--debug` · `--strict` (warnings fail) · `--selftest` · `--json`.
Errors: unknown ids (steps, D-ids, T-ids, gates, prompt keys, input ids), loops, a started step with unmet needs, ready with a blocking input open, done with open gates/check, stale `unblocks`, the app's `TR_RULES` ≠ the checker's. Warnings: lock older than 24 h, an unconfirmed proposal, a started step without `runs`, **an owner approval with no step** (a DECISIONS row from 22 Nov 2026 that records an approval or pick while no step names its D-id — D-077).
W2 errors: bad `calendar`/`queue`/`est`/`uses`/`runs`, a professor input that blocks or a need on a professor-only step, an output consumed without a producer or without needing it, two open runs on the lock or GPU row. `--selftest` also runs the scheduler on `plan-fixture.json` and compares the app's `trPlan()` (node) with `plan()` on the fixture and on the real file.
