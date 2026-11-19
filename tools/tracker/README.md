# tools/tracker — progress map data + check (W1, D-040)

*(Purpose: the format of `studio-docs/build/steps.json` and how chats update it. Updated: 19 Nov 2026 · Bio · Build · W1 progress map.)*

`studio-docs/build/steps.json` is the **owner doc for step status, dependencies, gates, owner checks and owner inputs**. The app draws it at
https://aaditya-verma.github.io/biology-studio/#progress (Map · Board · Your inputs) and `#step=<id>`, reading it live from the repo.

## Every chat that changes a step
1. Edit the step's row (status, gates, check, log, todo, inputs). Add a new step as a new row at the end of its lane.
2. `python tools/tracker/check.py --write` — re-derives `unblocks` and formats the file. Then `python tools/tracker/check.py` must PASS (CI runs it).
3. Collaborator chats (the Professor) **don't change `status`** — they set `proposed_by`, `proposed_status`, `proposed_on`; the owner's next chat confirms (sets `status`, deletes the three fields) or rejects (deletes them).

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

## check.py
`--write` (`--dry-run` shows changes) · `--only <id>` · `--preview` (text board + inputs) · `--debug` · `--strict` (warnings fail) · `--selftest` · `--json`.
Errors: unknown ids (steps, D-ids, T-ids, gates, prompt keys, input ids), loops, a started step with unmet needs, ready with a blocking input open, done with open gates/check, stale `unblocks`, the app's `TR_RULES` ≠ the checker's. Warnings: lock older than 24 h, an unconfirmed proposal.
