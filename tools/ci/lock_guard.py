#!/usr/bin/env python3
"""Biology Studio — sync.bat lock guard (U2 part 2, D-087 (5); RULES I8). Owner doc: studio-docs/build/setup-guide.md §6a.

Why: the X1 Ch 20 research commit (10b13d5) ran `sync.bat`, whose `git add -A` swept U2's unfinished app files into main,
so app v18 went live before its gates. Now, while STATUS § Lock shows the build lock held, sync.bat may not sweep
app files (src/ index.html sw.js assets/ tools/) that nobody staged:

  exit 0  "all"     — lock free, or --lock-ok (this sync line is from the chat that holds the lock), or no unstaged app changes: commit everything (git add -A)
  exit 0  "staged"  — lock held + unstaged app changes + something already staged (the chat's `git add` line named its files):
                      commit only what is staged; the app files are left in the tree untouched and listed
  exit 1            — lock held + unstaged app changes + nothing staged: stop, nothing committed (says what to do)
Prints the mode on the last line (`MODE=all` / `MODE=staged`) for sync.bat. Flags: --lock-ok, --dry-run (print only), --selftest.
EDIT: the app areas in APP below.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS = ROOT / "studio-docs" / "claude" / "STATUS.md"
APP = ("src/", "index.html", "sw.js", "assets/", "tools/")   # EDIT: the areas only the lock holder commits


def lock_holder(text):
    m = re.search(r"^- Build lock: (.+)$", text, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    return None if v.lower().startswith("free") else v


def is_app(path):
    p = path.replace("\\", "/").strip('"')
    return any(p == a or p.startswith(a) for a in APP)


def parse_status(porcelain):
    """git status --porcelain=v1 -z → (staged paths, unstaged-or-untracked paths). -z: NUL-separated, never quoted;
    a rename / copy is "R  new" NUL "old" (the old path is its own field and is skipped)."""
    staged, loose = [], []
    f = porcelain.split("\0")
    i = 0
    while i < len(f):
        line = f[i]
        i += 1
        if len(line) < 4:
            continue
        x, y, path = line[0], line[1], line[3:]
        if x in "RC":
            i += 1
        if x == "?":
            loose.append(path)
            continue
        if x not in " ?":
            staged.append(path)
        if y not in " ?":
            loose.append(path)
    return staged, loose


def decide(holder, staged, loose, lock_ok):
    app_loose = sorted({p for p in loose if is_app(p)})
    if not holder or lock_ok or not app_loose:
        return 0, "all", app_loose
    if staged:
        return 0, "staged", app_loose
    return 1, "stop", app_loose


def selftest():
    cases = [
        ("free", [], ["src/js/06-shell.js"], False, (0, "all")),
        ("Aaditya · `Bio · Build · U2 look tokens` · 22 Nov", [], ["studio-docs/research/x.md"], False, (0, "all")),
        ("Aaditya · `Bio · Build · U2 look tokens` · 22 Nov", [], ["src/css/app.css", "studio-docs/x.md"], False, (1, "stop")),   # 10b13d5's case
        ("Aaditya · `Bio · Build · U2 look tokens` · 22 Nov", ["studio-docs/research/ch20.md"], ["src/css/app.css"], False, (0, "staged")),
        ("Aaditya · `Bio · Build · U2 look tokens` · 22 Nov", [], ["src/css/app.css"], True, (0, "all")),
        ("Aaditya · `Bio · Build · U2 look tokens` · 22 Nov", ["tools/ci/lock_guard.py"], [], False, (0, "all")),   # app file STAGED, nothing loose: a git add line named it - allowed (D-087)
    ]
    bad = 0
    for raw, st, lo, ok, want in cases:
        h = lock_holder("- Build lock: " + raw)
        got = decide(h, st, lo, ok)[:2]
        bad += got != want
        print(("ok " if got == want else "BAD"), raw[:20], st, lo, ok, "->", got)
    st, lo = parse_status(" M src/js/06-shell.js\0M  studio-docs/a.md\0?? tools/ci/new.py\0R  b.md\0a.md\0?? my file.md\0")
    pg = st == ["studio-docs/a.md", "b.md"] and lo == ["src/js/06-shell.js", "tools/ci/new.py", "my file.md"]
    bad += not pg
    print("ok " if pg else "BAD", "porcelain parse", st, lo)
    print(("PASS" if not bad else "FAIL") + f": lock guard selftest {len(cases) + 1 - bad}/{len(cases) + 1}")
    return 1 if bad else 0


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    holder = lock_holder(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else None
    gs = subprocess.run(["git", "status", "--porcelain=v1", "-z", "-uall"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if gs.returncode != 0:   # fail closed: never fall back to "commit everything" (G-Eng)
        print("[sync] STOP: git status failed - " + (gs.stderr or "").strip()[:300])
        print("MODE=stop")
        return 1
    staged, loose = parse_status(gs.stdout)
    code, mode, app_loose = decide(holder, staged, loose, "--lock-ok" in args)
    if mode == "staged":
        print(f"[sync] The build lock is held by {holder}.")
        print("[sync] Committing only the files you staged (your chat's git add line). Left in place, NOT committed (they belong to the lock holder):")
        for p in app_loose:
            print("         " + p)
        other = sorted({p for p in loose if not is_app(p)} - {"content/E/sources.json"})
        if other:
            print("[sync] Also left out (changed, not staged - add them with git add first if they are yours):")
            for p in other:
                print("         " + p)
    elif mode == "stop":
        print(f"[sync] STOP: the build lock is held by {holder}, and these app files are changed but not staged:")
        for p in app_loose:
            print("         " + p)
        print("[sync] They belong to the chat that holds the lock — sync.bat won't sweep them into your commit (D-087).")
        print("[sync] If this sync line came from THAT chat:  sync.bat \"message\" --lock-ok")
        print("[sync] Otherwise run your chat's  git add <your files>  line first, then the same sync.bat line again (only staged files are committed).")
    print("MODE=" + mode)
    return code


if __name__ == "__main__":
    sys.exit(main())
