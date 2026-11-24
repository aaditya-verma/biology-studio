# tools/dispatch — the dispatcher tick (W5, D-099, D-101)

*(Purpose: what `desk.py` does each hour, the two files it reads and writes for Desk, and the scheduled task's prompt. Updated: 24 Nov 2026 · Bio · Build · W5 dispatcher — new.)*

One scheduled task, `Bio · Dispatcher`, runs `desk.py --tick` every hour. It reports and commits owner answers; it starts no jobs (that is W5b).

## Use
```
python tools/dispatch/desk.py --preview           # text board, changes nothing
python tools/dispatch/desk.py --only checks       # one section as JSON, changes nothing
python tools/dispatch/desk.py --tick --dry-run    # what a tick would do; no fetch, nothing written
python tools/dispatch/desk.py --tick              # from the dispatcher clone only
python tools/dispatch/desk.py --selftest          # temporary repos, no network (also in CI)
```
Exit 0 = tick done (a failing check is a row, not an error) · 1 = could not publish or commit · 2 = tick could not run. `NOTIFY: ` lines are for the owner, each printed once.

## Where it runs
- **Dispatcher clone:** `<Studio home>\dispatch\clone`, always at `origin/main` and clean. Never edit in it. It is separate so the tick never moves the laptop clone's branch or files.
- **Laptop clone:** `<Studio home>\repo\biology-studio`. The tick fetches in it, reads its git state, and commits Desk answers there.
- Set up once: `git clone https://github.com/aaditya-verma/biology-studio.git <Studio home>\dispatch\clone`

## The snapshot: `out\desk.json`, then `build/desk.json` on branch `desk-data`
**Read `<Studio home>\repo\biology-studio\out\desk.json` first** (untracked, rewritten every tick, same content). Missing or over 6 h old → read the branch.

Desk (and W6's Desk tab) read it at `https://raw.githubusercontent.com/aaditya-verma/biology-studio/desk-data/build/desk.json`. The branch holds only this file; a push to it runs no CI and never touches `main`.
- Published when the content changes, or after 5 h. **Over 6 h since `generated_at` = stale.** `generated_at` and `age_h` alone never count as a change.
- **Public:** ids, states and counts. No answer text, local paths or task descriptions.
- Schema 1: `generated_at` (IST) · `stale_after_h` · `source` (main commit) · `now` · `lock` · `next` (5, with dates) · `inputs` (ranked) · `running` · `slips` · `ci` · `checks` (`id`, `state` pass/warn/fail/unknown, `detail`) · `pipeline` (`steps`, `handoffs`, `code_queue`, `scheduled`, `reasons`) · `answers` (`id`, `state`, `reason`) · `reasons`.
- A section that can't be read is `null`, with the cause in `reasons`. Scheduled tasks' on/off state is in no readable file, so `enabled` is always `null`.

## Desk answers — Studio home `handoff\desk-answers.json`
Desk writes it; the tick only reads it.
```json
{"schema": 1, "answers": [{"id": "U3b.q1", "answer": "one line", "by": "Aaditya", "at": "2026-11-24 17:00"}]}
```
- Committed only when the input is open and not the professor's, `by` is the owner, and the id isn't queued twice with different answers — and the lock is free, the laptop clone is clean, on `main` and equal to `origin/main`. Otherwise it stays `queued` (with the reason) or is `bad`.
- The commit holds `steps.json` only, with only those inputs changed. **Never pushed:** the owner gets the `sync.bat` line. The file is checked in memory first (the same rules as `check.py --write`), and the commit is made from exactly those bytes on exactly the HEAD that was checked; if anything moved, the tick undoes its own edit and tries again next hour. Git hooks do not run on it.
- States: `queued` · `committed` (waiting for sync.bat) · `bad`. Once on `origin/main` it leaves the list. Desk may then delete its line.

## The scheduled task (owner creates it: W5.q1)
Name `Bio · Dispatcher`, hourly, on this laptop. Prompt:
> Run one dispatcher tick for Biology Studio. Unattended: never ask questions, never push to main, never edit files yourself, never create, edit or delete scheduled tasks. Studio home = `D:\Projects\biology_studio`.
> 1. `git -C D:\Projects\biology_studio\dispatch\clone pull --ff-only` (if it fails, carry on: the tick reports it).
> 2. `python -X utf8 D:\Projects\biology_studio\dispatch\clone\tools\dispatch\desk.py --tick`
> 3. For each output line starting `NOTIFY: `, send me one push notification with that text. No such line = no notification.
> 4. If step 2 printed nothing at all, a Python traceback, or Python could not start it, send me one notification saying so. Otherwise send nothing else. Do not repair anything.
> 5. Reply with the tick's first line and stop.

## EDIT
Settings at the top of `desk.py` (`BRANCH`, `PUBLISH_H`, `STALE_H`, `RUN_FLAG_H`, `LOCK_FLAG_H`, `NEXT_N`, `HANDOFF_SKIP`).
