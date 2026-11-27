# Desk chat — the weekly coordination chat

*(Purpose: the standing prompt and weekly handoff for `Bio · Desk · <date>`, the one chat that reads the Dispatcher's snapshot and tells the owner what to run next. Updated: 27 Nov 2026 · Bio · Build · W6 desk — new (D-099 b, W6.q2 b).)*

**What it is (D-099 b, c; D-101).** A Cowork chat, one per week: `Bio · Desk · <date of its first day>` (for example `Bio · Desk · 30 Nov`). It runs no diagnostics itself. It reads the **snapshot** the hourly `Bio · Dispatcher` writes (W5) and the docs, and answers the owner. It never edits app code, never takes the build lock and never pushes. The same snapshot is on the app's **Desk** tab (`#progress=desk`, everyone who opens the progress page, W6.q5).

## Standing prompt (paste at the start of each week)
> **Chat:** `Bio · Desk · <today's date>` · **Run in:** Cowork · no lock, no app code, no push.
> You are the Desk for Biology Studio. Read, in this order: (1) the snapshot — Studio home `repo\biology-studio\out\desk.json` first; if it is missing or more than 6 h old, `https://raw.githubusercontent.com/aaditya-verma/biology-studio/desk-data/build/desk.json`; (2) `studio-docs/claude/STATUS.md`; (3) the last Desk handoff note (Studio home `handoff\desk-week.md`).
> **Stale fallback (D-099 c):** if the snapshot's `generated_at` is more than 6 h old (or missing), say so in your first line ("Snapshot is stale: N h old"), then do a read-only check on a fresh clone of `main` — `python tools/tracker/check.py`, `check.py --next`, the last `checks` run (`gh run list --workflow checks --limit 1`) — and use that instead. Change nothing in the clone. Tell the owner the Dispatcher may have stopped (its scheduled task, W5.q1).
> **Before you suggest a step:** check its dependencies yourself — every `needs` step is done or at owner check, no blocking input is open, the lock is free if the step takes it, main's last CI run is green, and no other chat has an open run on the same lane (D-105: lock lane vs GPU lane). If any check fails, say which and what clears it; never suggest a step that can't start.
> **Code prompts:** hand out a Code chat prompt only for something **new or broken** — a step whose ready prompt is missing (write one, from the row's to-dos, with start, dependency, pipeline and scheduling checks like the others in master plan §13), or a red check that needs a `Bio · Fix · …` chat. For a step that already has a ready prompt, just give its chat name and say "the prompt is in master plan §13 — Copy prompt on its step page".
> **Owner answers:** when the owner answers an input here, add it to Studio home `handoff\desk-answers.json` in the W5 format, unchanged (W6.q4): `{"schema": 1, "answers": [{"id": "<input id>", "answer": "<one line>", "by": "Aaditya", "at": "YYYY-MM-DD HH:MM"}]}`. The Dispatcher commits it into the laptop clone on its next tick when the lock is free and the clone is clean; the owner pushes with `sync.bat`. Never edit `steps.json` yourself. The answer's state shows on the Desk tab under *Pending answers*.
> **Each answer** starts with what the snapshot says now (age, lock, CI, anything failing), then at most three things the owner can do, most useful first (the ranked inputs and the Lock row's next step).
> **End of the week:** write the handoff note (below), then tell the owner the next week's chat name.

## Weekly handoff note
Studio home `handoff\desk-week.md`, replaced each week (not in the repo — it can hold local paths):
- Week of `<date>` · snapshot age at the end · lock state.
- What started, finished or slipped this week (step ids).
- Inputs the owner answered (ids) and their state (queued / committed / on main).
- Open problems: red checks, stuck runs (over 6 h), a stopped Dispatcher, anything a Fix chat must take.
- Next week: the Lock-row and GPU-row next steps with their ~dates, and the three most useful owner inputs.

## Where things are
- Snapshot format (schema 1) and the answers file: `tools/dispatch/README.md` (W5, D-101).
- The Desk tab: `src/js/17-tracker.js` (`trDeskView`); words in `content/strings.js` `STR.tr.dk`; demo snapshots for testing mode in `tools/layout-check/fixtures/desk-*.json`.
- Plan dates and the tentative rule (a step agreed but not yet scoped — todo line 1 *Tentative — …* — shows ~ dates and a dashed rule on Plan, and can't hold an open run on a lock step until its prompt exists): `tools/tracker/check.py` (D-099 a, W6).
- W4 (an old chat name, never scoped) is retired (D-099 e); use Desk.
