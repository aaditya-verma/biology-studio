#!/usr/bin/env python3
"""Biology Studio — CI status (CIG): what did the automatic checks (.github/workflows/checks.yml) say?

Uses the GitHub CLI (`gh`, signed in — setup guide §5). Lists the last 5 runs of the `checks` workflow and, for the
newest red one among them, the tail of `gh run view <id> --log-failed`. Writes everything to out/ci-status.txt
and prints it.

Run from the repo root (or double-click ci.bat):
  python tools/ci/status.py                 # last 5 runs + failed-log tail of the newest red one -> out/ci-status.txt
  python tools/ci/status.py --preview       # the 5 runs only, no log fetch (fast); writes the file too
  python tools/ci/status.py --only <run id> # just that run (its failed-log tail if it is red)
  python tools/ci/status.py --dry-run       # print the gh commands it would run; run nothing, write nothing
  python tools/ci/status.py --debug         # also print each gh command and its raw output size
Exit code: 0 = the newest finished run is not red (green, cancelled, or nothing finished yet), 1 = it is red, 2 = gh missing / not signed in / error.
Owner doc: studio-docs/build/setup-guide.md §6a. EDIT: WORKFLOW, RUNS, TAIL below.
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "out" / "ci-status.txt"
# EDIT: workflow name, how many runs to list, how many log lines to keep
WORKFLOW = "checks"
RUNS = 5
TAIL = 80
FIELDS = "databaseId,status,conclusion,headSha,displayTitle,createdAt,event,url"
DEBUG = False
# EDIT: where winget / the MSI put gh — used when gh is not on this window's PATH (a window opened before the install keeps the old PATH)
GH_PATHS = [r"C:\Program Files\GitHub CLI\gh.exe", r"C:\Program Files (x86)\GitHub CLI\gh.exe",
            str(Path.home() / "AppData" / "Local" / "Programs" / "GitHub CLI" / "gh.exe")]
GH = shutil.which("gh") or next((p for p in GH_PATHS if Path(p).exists()), None)


def gh(args, dry):
    cmd = [GH or "gh"] + args
    if dry or DEBUG:
        print("$ " + " ".join(cmd))
    if dry:
        return ""
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
    if DEBUG:
        print(f"  -> exit {r.returncode}, {len(r.stdout)} chars out, {len(r.stderr)} chars err")
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip() or f"gh exited {r.returncode}")
    return r.stdout


def state(run):
    if run.get("status") != "completed":
        return run.get("status") or "?"
    return run.get("conclusion") or "?"


def red(run):
    return run.get("status") == "completed" and run.get("conclusion") in ("failure", "timed_out", "startup_failure")


def line(run):
    mark = {"success": "PASS", "failure": "FAIL", "timed_out": "FAIL", "startup_failure": "FAIL",
            "cancelled": "stop", "skipped": "skip"}.get(state(run), state(run))
    when = (run.get("createdAt") or "").replace("T", " ").rstrip("Z")[:16]
    return f"{mark:<11} {run.get('databaseId')}  {when} UTC  {(run.get('headSha') or '')[:7]}  {run.get('displayTitle', '')[:70]}"


ERRORISH = re.compile(r"✗|^\s*E [A-Z]-|\bFAIL\b|Traceback|Error\b|error:|^\s*assert", re.I)


def clean(l):
    """gh prints "<job>\\t<step>\\t<timestamp> <text>"; keep the text."""
    parts = l.split("\t", 2)
    if len(parts) < 3:
        return l
    msg = parts[2]
    return msg.split(" ", 1)[1] if msg[:4].isdigit() and " " in msg else msg


def failed_tail(log, tail):
    """The failing step's name, its error-looking lines, and the last `tail` lines ending at the first ##[error]
    (gh's step column is often UNKNOWN STEP and the raw tail is post-job cleanup, so cut at the error)."""
    lines = [clean(l) for l in log.splitlines()]
    if not lines:   # e.g. a startup_failure run with no jobs: gh prints nothing
        return "(no failed-step log — the run may have failed before any job started)", [], [], 0
    err = next((i for i, l in enumerate(lines) if l.startswith("##[error]")), len(lines) - 1)
    start = next((i for i in range(err, -1, -1) if lines[i].startswith("##[group]Run ")), 0)
    step = lines[start][len("##[group]Run "):] if lines[start].startswith("##[group]Run ") else "(step not named in the log)"
    body = [l for l in lines[start:err + 1] if not l.startswith("##[group]") and not l.startswith("##[endgroup]")]
    hits = [l for l in body if ERRORISH.search(l)]
    return step, hits[-40:], lines[max(start, err + 1 - tail):err + 1], len(lines)


def main():
    for st in (sys.stdout, sys.stderr):   # Windows consoles default to cp1252
        try:
            st.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    global DEBUG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="one run id")
    ap.add_argument("--preview", action="store_true", help="list the runs only, no log fetch")
    ap.add_argument("--dry-run", action="store_true", help="print the gh commands; run nothing, write nothing")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--tail", type=int, default=TAIL, help=f"failed-log lines to keep (default {TAIL})")
    a = ap.parse_args()
    DEBUG = a.debug
    if not a.dry_run and not GH:
        print("ci-status: gh (GitHub CLI) not found — install it: winget install GitHub.cli, then gh auth login")
        return 2
    try:
        if a.only:
            runs = [json.loads(gh(["run", "view", a.only, "--json", FIELDS], a.dry_run) or "{}")]
        else:
            runs = json.loads(gh(["run", "list", "--workflow", WORKFLOW, "-L", str(RUNS), "--json", FIELDS], a.dry_run) or "[]")
        if a.dry_run:
            print(f"$ gh run view <newest red run id> --log-failed   (tail {a.tail} lines; skipped with --preview)")
            print(f"would write {OUT.relative_to(ROOT)}")
            return 0
        rep = [f"CI status — workflow '{WORKFLOW}'" + (f", run {a.only}" if a.only else f", last {len(runs)} runs"), ""]
        rep += [line(r) for r in runs] or ["(no runs found)"]
        done = [r for r in runs if r.get("status") == "completed"]
        newest_done = done[0] if done else None
        bad = next((r for r in runs if red(r)), None)
        label = "Newest red run" if bad is newest_done else "Older red run (a later run finished since — may be fixed)"
        rep.append("")
        if newest_done is None:
            rep.append("Newest finished run: none yet (still running) — run ci.bat again in a few minutes.")
        else:
            rep.append(f"Newest finished run: {state(newest_done).upper()} ({newest_done.get('databaseId')}, {(newest_done.get('headSha') or '')[:7]})")
        if bad is None:
            rep.append("No red run in this list.")
        elif a.preview:
            rep.append(f"{label}: {bad.get('databaseId')} — log not fetched (--preview). {bad.get('url', '')}")
        else:
            step, hits, tail, total = failed_tail(gh(["run", "view", str(bad["databaseId"]), "--log-failed"], False), a.tail)
            rep += [f"{label}: {bad.get('databaseId')} ({(bad.get('headSha') or '')[:7]}) {bad.get('url', '')}",
                    f"Failed step: {step}", "", "Error lines in that step:"] + (["  " + h for h in hits] or ["  (none matched — see the log below)"])
            rep += ["", f"Log up to the error ({len(tail)} lines; the failed-step log has {total}):", ""] + tail
    except (RuntimeError, json.JSONDecodeError) as e:
        print(f"ci-status: gh failed — {e}\n(signed in? run: gh auth status)")
        return 2
    text = "\n".join(rep) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(text + f"\nwrote {OUT.relative_to(ROOT)}")
    return 1 if newest_done is not None and red(newest_done) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:   # an unexpected crash must not look like a red run (exit 1)
        print(f"ci-status: unexpected error — {type(e).__name__}: {e}")
        sys.exit(2)
