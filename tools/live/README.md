# tools/live — live progress page for every build job (D-089, RULES I9)

*(Purpose: how a chat shows the owner a long job as it runs. Updated: 22 Nov 2026 · Bio · Fix · split-screen test badge (U2F) — new; G-Eng round 2 fixes.)*

Every build job that takes more than about a minute runs through `live.py`: layout-check (full, `--preview`, `--only`, the selftest), stills, renders, `sync.bat --check`, and any long script. The chat opens the hub in the Claude app's browser pane **before** it waits, so the owner can watch the job instead of a silent terminal.

## Use
```
python tools/live/live.py --serve                     # the hub: http://localhost:8799/index.html
python tools/live/live.py "U2F layout-check full" --shots out/layout-check/shots -- python tools/layout-check/check.py
python tools/live/live.py "U2F guard" -- sync.bat --check
python tools/live/live.py "M1 render" --attach out/render.log --shots out/renders    # a job that is already running
python tools/live/live.py --selftest
```
- **Hub** (`index.html`): every run with its state, start time, elapsed time and screenshot count. It refreshes every 5 s while any run is going. **Run page** (`run-<name>.html`): state, the command, elapsed time, exit code, the last 80 lines of output and the newest 12 screenshots.
- `NAME` starts with the step id (`U2F layout-check full`). Running the same name again replaces that run.
- **Run mode** (`-- <command>`): the command runs in the repo root. The tool exits with the command's exit code, and a command that can't start gives exit 127 and a FAIL page. A `.bat` runs directly (`-- sync.bat --check`). **Never pass `cmd /c` from Git Bash**: Git Bash rewrites `/c` to `C:/`, and cmd then opens a shell instead of the batch file. The tool refuses that form.
- **Attach mode** (`--attach LOG`): the run is done once the log has content and has not grown for `--idle` seconds (default 60). It is FAIL when a line starts with `FAIL`, `FAILED`, `[sync] FAILED` or a Python `Traceback`.
- Relative `--shots` and `--attach` paths are read from the folder you start the tool in.
- Pages go to `out/live/` (gitignored). Screenshots are copied into `out/live/shots/<name>/`, so they can live anywhere. Delete `out/live/` to clear the hub.
- In the Claude desktop app, the local (gitignored) `.claude/launch.json` holds a config named **`live`**: `python tools/live/live.py --serve --port 8799`. The chat opens it with `preview_start {name: "live"}`, and adds the config first if it is missing.
- RULES I5's `--debug` / `--dry-run` / `--only` / `--preview` don't apply: this tool only wraps other jobs.

## EDIT
`REFRESH`, `TAIL`, `SHOTS`, `TICK` and `IDLE` at the top of `live.py`.
