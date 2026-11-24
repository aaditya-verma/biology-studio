#!/usr/bin/env python3
"""Biology Studio — dispatcher tick (W5, D-099, D-101): routine checks, the Desk snapshot, Desk answers.
Owner doc: tools/dispatch/README.md. Run by the scheduled task `Bio · Dispatcher` (hourly), from the dispatcher's own clone.

Each tick:
  1. reads origin/main in THIS clone (<Studio home>/dispatch/clone) — the laptop clone is only looked at (git state) …
  2. runs the routine checks (report only: a failing check is a row, never a crash);
  3. lists every pipeline task (steps, open runs, handoffs, code-queue, scheduled tasks), read-only;
  4. … and gets one commit of valid Desk answers (never pushed; the owner runs sync.bat);
  5. writes <laptop clone>/out/desk.json (untracked; Desk reads it first) and publishes the same content as build/desk.json to branch `desk-data` on a content change or after PUBLISH_H hours — never touches main.
desk.json is PUBLIC: ids, states and counts only — no answer text, no local paths, no task descriptions.

  python tools/dispatch/desk.py --tick              # everything
  python tools/dispatch/desk.py --tick --dry-run    # read and print; no fetch, no file, no commit, no push
  python tools/dispatch/desk.py --preview           # short text board; changes nothing
  python tools/dispatch/desk.py --only checks       # one section as JSON; changes nothing
  python tools/dispatch/desk.py --selftest          # temporary repos, no network
  --debug  print every git command · --home <dir>  Studio home (default: found from this file, or BIO_STUDIO_HOME)
Exit: 0 = tick done (failing checks are rows) · 1 = could not publish or commit · 2 = tick could not run.
Lines starting `NOTIFY: ` are for the owner; each is printed once, until it changes.
"""
import time, argparse, contextlib, copy, datetime as dt, hashlib, importlib.util, io, json, os, re, shutil, signal, subprocess, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True      # loading check.py must not write into a clone

ROOT = Path(__file__).resolve().parents[2]
# EDIT: settings
BRANCH = "desk-data"          # the only branch ever pushed
REMOTE_FILE = "build/desk.json"
SCHEMA = 1
PUBLISH_H = 5                 # publish unchanged content after this long …
STALE_H = 6                   # … so it stays under D-099's stale limit (readers compare generated_at)
RUN_FLAG_H = 6                # an open run older than this is flagged
LOCK_FLAG_H = 24              # same limit as check.py LOCK_MAX_H
NEXT_N = 5
ANSWER_MAX = 2000
TICK_LOCK_MIN = 30            # a tick lock file older than this is a crashed tick
GIT_TIMEOUT = 120
GH_TIMEOUT = 60
HANDOFF_SKIP = {"code-queue.md", "desk-answers.json"}   # EDIT: handoff files read as something else
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
VOLATILE = ("generated_at", "age_h")      # never count as a content change
SECTIONS = ("source", "now", "lock", "next", "inputs", "running", "slips", "ci", "checks", "pipeline", "answers")
STEPS_REL = "studio-docs/build/steps.json"
DEBUG = False


class DeskError(Exception):
    """str() is fixed wording and may be published; `detail` (stderr …) stays on this laptop (stdout, NOTIFY)."""
    def __init__(self, msg, detail=""):
        super().__init__(msg)
        self.detail = detail


def why_public(e):
    return str(e) if isinstance(e, DeskError) else type(e).__name__


def why_local(e):
    d = e.detail if isinstance(e, DeskError) else str(e)
    return public(why_public(e) + (f": {d}" if d else ""))


class Ctx:
    """Where things are. `now` and `ci_runs` can be replaced by the selftest."""
    def __init__(self, root, home, now=None, ci_runs=None, tasks_dir=None, dry=False):
        self.root, self.home = Path(root), Path(home)
        self.laptop = self.home / "repo" / "biology-studio"
        self.handoff = self.home / "handoff"
        self.out = self.root / "out" / "dispatch"
        self.tasks = Path(tasks_dir) if tasks_dir else Path.home() / ".claude" / "scheduled-tasks"
        self.now = now or dt.datetime.now(IST)
        self.ci_runs, self.dry = ci_runs, dry
        self.online = self.laptop_fetched = None       # None = not fetched (dry run or preview)
        self._chk = self._doc = self._plan = self._ci = None

    @property
    def chk(self):
        if self._chk is None:
            self._chk = load_module(self.root / "tools" / "tracker" / "check.py", "desk_tracker")
        return self._chk

    @property
    def doc(self):
        if self._doc is None:
            self._doc = json.loads((self.root / STEPS_REL).read_text(encoding="utf-8"))
        return self._doc

    @property
    def plan(self):
        if self._plan is None:
            self._plan = self.chk.plan(self.doc, self.now.astimezone(IST).date().isoformat())
        return self._plan


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run_cmd(cmd, cwd=None, data=b"", timeout=GIT_TIMEOUT, env=None):
    """(code, stdout, stderr). Output goes to files, and a timeout kills the whole process tree: with pipes, a grandchild
    (git-remote-https, a credential helper) keeps subprocess.run waiting long after the timeout on Windows."""
    what = Path(cmd[0]).stem
    with tempfile.TemporaryFile() as i, tempfile.TemporaryFile() as o, tempfile.TemporaryFile() as e:
        i.write(data)
        i.seek(0)
        try:
            pr = subprocess.Popen(cmd, cwd=cwd, stdin=i, stdout=o, stderr=e, env=env, start_new_session=os.name != "nt")
        except OSError as x:
            raise DeskError(f"{what} not found", str(x))
        try:
            code = pr.wait(timeout)
        except BaseException as x:
            if os.name == "nt":
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(pr.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                with contextlib.suppress(OSError):
                    os.killpg(pr.pid, signal.SIGKILL)
            if isinstance(x, subprocess.TimeoutExpired):
                raise DeskError(f"{what} timed out")
            raise
        o.seek(0)
        e.seek(0)
        return code, o.read().decode("utf-8", "replace"), e.read().decode("utf-8", "replace")


def git(cwd, *args, data=b"", ok=False, env=None):
    """git in cwd → stdout. ok=True: return (code, stdout, stderr) instead of raising."""
    if DEBUG:
        print("$ git " + " ".join(args))
    full = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never", GIT_ASKPASS="", SSH_ASKPASS="", GIT_OPTIONAL_LOCKS="0", **(env or {}))
    code, o, e = run_cmd(["git", "-c", "core.askPass=", "-c", "http.lowSpeedLimit=1000", "-c", "http.lowSpeedTime=60", "-C", str(cwd), *args], data=data, env=full)
    if ok:
        return code, o, e
    if code:
        raise DeskError(f"git {args[0]} failed", (e or o).strip()[-200:])
    return o


def public(text):
    """Backstop for text that may be published: one short line, no local paths, tokens, e-mails or user@host."""
    t = str(text).encode("utf-8", "replace").decode("utf-8")
    t = re.sub(r"(https?://)[^\s@/]+@", r"\1", t)
    t = re.sub(r"\b(?:gh[pousr]_|github_pat_)\w+", "<token>", t)
    t = re.sub(r"\b[\w.+-]+@[\w.()-]+", "<address>", t)
    t = re.sub(r"(?i)(?<![a-z])[a-z]:[\\/][^'\"<>|:;,]*|\\\\[^'\"<>|:;,]+|~[\\/][^\s'\"]*|(?<![\w:/.])/(?:home|Users|tmp|mnt|opt|root|private|var|c|d)/[^'\"<>|:;,]*", "<path>", t)
    t = re.sub(r"\b[0-9a-f]{40}\b", "<sha>", t)      # a new id every try would make the same notice look new
    return " ".join(t.split())[:240]


def stamp(d):
    return d.astimezone(IST).strftime("%Y-%m-%d %H:%M IST")


def parse_stamp(s):
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d %H:%M IST").replace(tzinfo=IST)
    except (TypeError, ValueError):
        return None


def age_h(ctx, when):
    return None if when is None else round((ctx.now - when).total_seconds() / 3600, 1)


def dirty_paths(clone):
    return [x[3:] for x in git(clone, "status", "--porcelain", "-uall").splitlines() if x]


# ---- sections ----
def s_source(ctx):
    return {"commit": git(ctx.root, "rev-parse", "HEAD").strip()[:7], "branch": "main"}


def step_cell(ctx, c):
    s = next(x for x in ctx.doc["steps"] if x["id"] == c["step"])
    todo = s.get("todo") or []
    return {"id": c["id"], "title": s["title"], "chat": s["chat"], "row": ctx.chk.plan_res(s)[0], "status": s["status"],
            "start": c["start"], "end": c["end"], "slipped": c["slipped"],
            "tentative": bool(todo and str(todo[0]).lower().startswith("tentative"))}


def s_now(ctx):
    return [step_cell(ctx, c) for r in ("lock", "gpu", "research") for c in ctx.plan["rows"][r]["now"] if c["kind"] == "step"]


def s_next(ctx):
    cells = [c for r in ctx.plan["rows"].values() for k in ("next", "later") for c in r[k] if c["kind"] == "step" and c["start"]]
    pos = {x: i for i, x in enumerate(ctx.doc.get("queue") or [])}
    cells.sort(key=lambda c: (c["start"], pos.get(c["step"], 10 ** 6), c["id"]))
    return [step_cell(ctx, c) for c in cells[:NEXT_N]]


def lock_state(ctx, root):
    """The lock line of a clone, through its own check.py reader; a missing line is an error, not 'free'."""
    t = (Path(root) / "studio-docs/claude/STATUS.md").read_text(encoding="utf-8")
    if not re.search(r"^- Build lock: .+$", t, re.M):
        raise DeskError("STATUS has no '- Build lock:' line")
    chk = ctx.chk if Path(root) == ctx.root else load_module(Path(root) / "tools/tracker/check.py", "desk_tracker_lock")
    return chk.read_lock()


def holder_chat(ctx, holder):
    m = re.search(r"`([^`]+)`", holder or "")
    return m.group(1) if m else (ctx.chk.lock_chat(holder) if holder else None)


def s_lock(ctx):
    holder, when = lock_state(ctx, ctx.root)
    a = age_h(ctx, when)
    return {"state": "held" if holder else "free", "chat": public(holder_chat(ctx, holder)) if holder else None,
            "since": stamp(when) if when else None, "age_h": a, "old": bool(a is not None and a > LOCK_FLAG_H),
            "since_reason": "the lock line has no readable date" if holder and not when else None}


def s_inputs(ctx):
    asks = {x["id"]: x for s in ctx.doc["steps"] for x in s.get("inputs", [])}
    return [dict(id=r["id"], step=r["step"], kind=r["kind"], unblocks=r["unblocks"], blocks=r["blocks"], asked=r["asked"] or None,
                 ask=asks[r["id"]]["ask"] if r["id"] in asks else None) for r in ctx.plan["ranked"]]


def s_running(ctx):
    out = []
    for s in ctx.doc["steps"]:
        for r in s.get("runs") or []:
            if not (isinstance(r, dict) and r.get("start") and not r.get("end")):
                continue
            when = None
            if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", str(r["start"])):
                when = dt.datetime.strptime(r["start"], "%Y-%m-%d %H:%M").replace(tzinfo=IST)
            a = age_h(ctx, when)
            out.append({"step": s["id"], "chat": r.get("chat"), "by": r.get("by"), "start": r["start"], "age_h": a,
                        "old": None if a is None else a > RUN_FLAG_H, "old_reason": "the run has a date but no time" if a is None else None})
    return out


def s_slips(ctx):
    return [{"step": k, "end": v["end"]} for k, v in ctx.plan["dates"].items() if v["slipped"]]


def ci_runs(ctx, st):
    if ctx._ci is None:
        runs = ctx.ci_runs
        try:
            if callable(runs):
                runs = runs()
            elif runs is None:
                if not st.GH:
                    raise DeskError("gh (GitHub CLI) not found")
                cmd = [st.GH, "run", "list", "--workflow", st.WORKFLOW, "-b", "main", "-L", str(st.RUNS), "--json", st.FIELDS]
                code, o, e = run_cmd(cmd + (["-R", st.REPO] if st.REPO else []), cwd=ctx.root, timeout=GH_TIMEOUT)
                if code:
                    raise DeskError("gh failed", e.strip()[-200:])
                runs = json.loads(o or "[]")
            ctx._ci = (runs, None)
        except (DeskError, ValueError) as e:
            ctx._ci = (None, e)
    if ctx._ci[1]:
        raise ctx._ci[1]
    return ctx._ci[0]


def s_ci(ctx):
    st = load_module(ctx.root / "tools" / "ci" / "status.py", "desk_ci")
    runs = ci_runs(ctx, st)
    head = git(ctx.root, "rev-parse", "HEAD").strip()
    done = next((r for r in runs if r.get("status") == "completed"), None)
    mine = next((r for r in runs if r.get("headSha") == head), None)
    return {"newest_finished": None if not done else {"state": st.state(done), "red": st.red(done), "commit": (done.get("headSha") or "")[:7],
                                                      "run": done.get("databaseId"), "url": done.get("url")},
            "main_head": {"commit": head[:7], "state": st.state(mine) if mine else None,
                          "reason": None if mine else "no run listed for this commit"}}


# ---- routine checks: each returns (state, detail); state pass | warn | fail | unknown ----
def c_tracker(ctx):
    E, W = ctx.chk.check(ctx.doc, ctx.chk.load_refs(), None, ctx.chk.read_lock(), ctx.now)
    E += ctx.chk.parity()
    lock_w = [w for w in W if w.startswith("build lock")]      # its text holds an age (would change every hour); lock_age has it
    W = [w for w in W if w not in lock_w]
    return ("fail" if E else "warn" if W else "pass"), f"{len(E)} errors, {len(W)} warnings" + (f"; first: {(E + W)[0]}" if E + W else "")


def c_next(ctx):
    txt = ctx.chk.next_text(ctx.doc, ctx.plan, ctx.chk.read_lock())
    t = (ctx.root / "studio-docs/claude/STATUS.md").read_text(encoding="utf-8")
    m = re.search(re.escape(ctx.chk.AUTO_A) + r"(.*?)" + re.escape(ctx.chk.AUTO_B), t, re.S)
    if not m:
        return "fail", "STATUS § Next has no auto block"
    cut = lambda x: [re.sub(r"~\d+ \w+|est\. from \d+ \w+", "", l) for l in x.strip().splitlines()]   # dates move every day
    if cut(m.group(1)) == cut(txt):
        return "pass", "schedule builds; STATUS § Next agrees"
    return "warn", "schedule builds; STATUS § Next differs (check.py --next --write)"


def c_ci(ctx):
    d = s_ci(ctx)
    n = d["newest_finished"]
    if not n:
        return "unknown", "no finished run listed"
    if n["red"]:
        return "fail", f"newest finished run on {n['commit']} is red"
    if d["main_head"]["state"] != "success":
        return "warn", f"main {d['main_head']['commit']} is not confirmed green ({d['main_head']['state'] or 'no run'})"
    return "pass", f"main {d['main_head']['commit']} is green"


def laptop_state(ctx):
    """Branch, dirty paths, ahead/behind this clone's origin/main. Reads only."""
    lp = ctx.laptop
    if not (lp / ".git").exists():
        raise DeskError("laptop clone not found")
    s = {"branch": git(lp, "rev-parse", "--abbrev-ref", "HEAD").strip(), "dirty": dirty_paths(lp),
         "head": git(lp, "rev-parse", "HEAD").strip(), "origin": git(ctx.root, "rev-parse", "origin/main").strip(), "ahead": None, "behind": None}
    if git(lp, "cat-file", "-e", s["origin"], ok=True)[0] == 0:
        s["ahead"], s["behind"] = (int(x) for x in git(lp, "rev-list", "--left-right", "--count", f"HEAD...{s['origin']}").split())
    return s


def c_laptop(ctx):
    s = laptop_state(ctx)
    bad = ["could not fetch there"] if ctx.laptop_fetched is False else []
    if s["branch"] != "main":
        bad.append(f"on branch {s['branch']}")
    if s["dirty"]:
        bad.append(f"{len(s['dirty'])} uncommitted files")
    if s["ahead"] is None:
        bad.append("not in sync with origin/main (count unknown: not fetched there)")
    else:
        bad += ([f"{s['ahead']} commits to push (sync.bat)"] if s["ahead"] else []) + ([f"{s['behind']} commits to pull"] if s["behind"] else [])
    return ("warn", "; ".join(bad)) if bad else ("pass", "clean and in sync")


def c_lock(ctx):
    d = s_lock(ctx)
    if d["state"] == "free":
        return "pass", "free"
    if d["age_h"] is None:
        return "warn", "held; no readable date"
    return ("warn", f"held by {d['chat']} for over {LOCK_FLAG_H} h") if d["old"] else ("pass", f"held by {d['chat']}")


def c_runs(ctx):
    runs = s_running(ctx)
    old = [r["step"] for r in runs if r["old"]]
    unk = [r["step"] for r in runs if r["old"] is None]
    if old:
        return "warn", f"open over {RUN_FLAG_H} h: {', '.join(old)}"
    return ("unknown", f"no start time: {', '.join(unk)}") if unk else ("pass", f"{len(runs)} open")


def c_conflicts(ctx):
    bad = []
    have = (ctx.laptop / ".git").exists()
    if have:
        if git(ctx.laptop, "ls-files", "-u").strip():
            bad.append("laptop clone has unmerged files")
        g = Path(git(ctx.laptop, "rev-parse", "--absolute-git-dir").strip())
        if any((g / x).exists() for x in ("rebase-merge", "rebase-apply", "MERGE_HEAD")):
            bad.append("a merge or rebase is in progress in the laptop clone")
    code, out, err = git(ctx.root, "grep", "-lE", r"^(<{7}|>{7}) ", "HEAD", "--", ok=True)
    if code > 1:
        raise DeskError("git grep failed", err)
    files = [x.split(":", 1)[1] for x in out.splitlines()]
    if files:
        bad.append("conflict markers in " + ", ".join(files[:5]))
    if bad:
        return "fail", "; ".join(bad)
    return ("pass", "none") if have else ("unknown", "none on main; laptop clone not found")


# a handoff is committed when a line reads "[<step>] committed <sha or date>" (p1-s1e01's "committed by the scheduled task" is not one)
COMMITTED_RE = re.compile(r"^[>*\s]*(?:[\w.]+ )?committed (?:[0-9a-f]{7,40}\b|\d{1,2} [A-Z][a-z]{2}\b)", re.I | re.M)
D_ROW_RE = re.compile(r"^\| (D-\d{3}) \|([^|]*)\|(.*)$", re.M)


def d_key(row):
    m = re.search(r"\*\*(.+?)\*\*", row)
    return re.sub(r"\W+", "", (m.group(1) if m else row)[:60]).lower()


def c_dids(ctx):
    bad = []
    seen = {}
    for i, _, txt in D_ROW_RE.findall((ctx.root / "studio-docs/claude/DECISIONS.md").read_text(encoding="utf-8")):
        if i in seen:
            bad.append(f"{i} is used twice in DECISIONS")
        seen.setdefault(i, d_key(txt))
    bad += ctx.chk.check_refs(ctx.doc, ctx.chk.load_refs())[0]
    parked = {}
    for p in sorted(ctx.handoff.glob("*/d*-row*.md")) if ctx.handoff.exists() else []:
        readme = p.parent / "README.md"
        if readme.exists() and COMMITTED_RE.search(readme.read_text(encoding="utf-8", errors="replace")):
            continue
        for i, _, txt in D_ROW_RE.findall(p.read_text(encoding="utf-8", errors="replace")):
            if i in seen and seen[i] != d_key(txt):
                bad.append(f"handoff {p.parent.name}: {i} is another decision in DECISIONS")
            if i in parked and parked[i] != p.parent.name:
                bad.append(f"{i} is proposed by handoffs {parked[i]} and {p.parent.name}")
            parked.setdefault(i, p.parent.name)
    if bad:
        return "fail", "; ".join(dict.fromkeys(bad))
    return ("pass", "none") if ctx.handoff.exists() else ("unknown", "none in DECISIONS; handoff folder not found")


CHECKS = [("tracker", c_tracker), ("next", c_next), ("ci", c_ci), ("laptop", c_laptop), ("lock_age", c_lock),
          ("open_runs", c_runs), ("conflicts", c_conflicts), ("d_ids", c_dids)]


def s_checks(ctx):
    rows = []
    if ctx.online is False:
        rows.append({"id": "network", "state": "warn", "detail": "origin not reached"})
    for name, fn in CHECKS:
        try:
            state, detail = fn(ctx)
        except Exception as e:      # a check that cannot run is a row, never a crash
            state, detail = "unknown", why_public(e)
        rows.append({"id": name, "state": state, "detail": public(detail)})
    return rows


# ---- pipeline tasks, read-only ----
def p_steps(ctx):
    by = {s["id"]: s for s in ctx.doc["steps"]}
    holder = ctx.chk.read_lock()[0]
    out = []
    for s in ctx.doc["steps"]:
        if s["type"] == "Idea" or s["status"] in ("done", "parked"):
            continue
        wait = s["status"] in ("idea", "planned", "ready", "proposed")      # started steps wait for nothing here
        why = ctx.chk.startable(s, by, None) if wait else []
        if wait and s.get("lock") and holder and holder_chat(ctx, holder) != s["chat"]:
            why.append("the build lock")
        out.append({"id": s["id"], "status": s["status"], "chat": s["chat"], "waits_for": why, "end": (ctx.plan["dates"].get(s["id"]) or {}).get("end")})
    return out


def p_handoffs(ctx):
    if not ctx.handoff.exists():
        raise DeskError("handoff folder not found")
    open_, done = [], 0
    for p in sorted(ctx.handoff.iterdir()):
        if p.name in HANDOFF_SKIP:
            continue
        f = p / "README.md" if p.is_dir() else p
        if p.is_dir() and not f.exists():
            open_.append({"id": public(p.name), "committed": None, "reason": "no README"})
        elif f.suffix == ".md":
            if COMMITTED_RE.search(f.read_text(encoding="utf-8", errors="replace")):
                done += 1
            else:
                open_.append({"id": public(p.name), "committed": False, "reason": "no Committed line"})
    return {"open": open_, "committed": done}


def p_queue(ctx):
    f = ctx.handoff / "code-queue.md"
    if not f.exists():
        raise DeskError("code-queue.md not found")
    part, idx, open_, done = None, None, [], 0
    for l in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if l.startswith("## "):
            part = "queue" if l.startswith("## Queue") else "waiting" if l.startswith("## Waiting") else None
            idx = None
        elif part and l.startswith("|"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if idx is None:
                low = [x.lower() for x in c]
                idx = {k: low.index(k) for k in ("item", "handoff", "state") if k in low}
                continue
            if set("".join(c)) <= set("-: "):
                continue
            if "item" not in idx or "state" not in idx or max(idx.values()) >= len(c):
                open_.append({"id": None, "in": part, "state": None, "reason": "row not readable"})
                continue
            st = c[idx["state"]]
            if "✅" in st:
                done += 1
                continue
            open_.append({"id": public(re.sub(r"[*`]", "", c[idx.get("handoff", idx["item"])])), "in": part,
                          "state": "open" if "⏳" in st else None, "reason": None if "⏳" in st else "state mark not recognised"})
    return {"open": open_, "done": done}


def p_tasks(ctx):
    """Scheduled tasks: the folder names are readable, schedule and on/off are not — so null + reason, never a guess."""
    if not ctx.tasks.exists():
        raise DeskError("scheduled-tasks folder not found")
    return [{"id": public(p.parent.name), "enabled": None, "reason": "on/off is not in a readable file"} for p in sorted(ctx.tasks.glob("*/SKILL.md"))
            if p.parent.name.startswith(("bio-", "biology-"))]


def s_pipeline(ctx):
    out, why = {}, {}
    for k, fn in (("steps", p_steps), ("handoffs", p_handoffs), ("code_queue", p_queue), ("scheduled", p_tasks)):
        try:
            out[k] = fn(ctx)
        except Exception as e:
            out[k], why[k] = None, why_public(e)
    out["reasons"] = why
    return out


# ---- Desk answers ----
def valid_at(at):
    try:
        return isinstance(at, str) and dt.datetime.strptime(at, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M") == at
    except ValueError:
        return False


def answer_text(a, at):
    d = dt.date.fromisoformat(at[:10])
    return f"{a.strip()} (owner, {d.day} {d.strftime('%b %Y')}, Desk)"


def one_line(s, n):
    """a non-empty, UTF-8 encodable single line of at most n characters"""
    try:
        s.encode("utf-8")
    except (UnicodeEncodeError, AttributeError):
        return False
    return 0 < len(s.strip()) and len(s) <= n and not any(ord(c) < 32 or ord(c) in (0x7f, 0x85, 0x2028, 0x2029) for c in s)


def read_answers(ctx):
    f = ctx.handoff / "desk-answers.json"
    if not f.exists():
        return []
    try:
        d = json.loads(f.read_text(encoding="utf-8-sig"))
    except ValueError as e:
        raise DeskError("desk-answers.json is not valid JSON", str(e))
    if not isinstance(d, dict) or d.get("schema") != 1 or not isinstance(d.get("answers"), list):
        raise DeskError('desk-answers.json must be {"schema": 1, "answers": [...]}')
    return d["answers"]


def judge(rows, doc):
    """[(row, state, reason)] — state: ok | done | bad. Judged against the LAPTOP clone's steps.json."""
    inputs = {x["id"]: x for s in doc["steps"] for x in s.get("inputs", [])}
    texts = {}
    for r in rows:
        if isinstance(r, dict) and isinstance(r.get("id"), str):
            texts.setdefault(r["id"], set()).add(str(r.get("answer")).strip())
    out, took = [], set()
    for r in rows:
        why = state = None
        rid = r.get("id") if isinstance(r, dict) else None
        x = inputs.get(rid) if isinstance(rid, str) else None
        if x is None:
            why = "no such input" if isinstance(rid, str) else "not an object with an id"
        elif not one_line(r.get("answer"), ANSWER_MAX):
            why = f"answer must be one line of 1–{ANSWER_MAX} characters"
        elif r.get("by") != doc.get("owner"):
            why = "`by` must be the owner"
        elif x.get("for") == "prof":
            why = "a professor input"
        elif not valid_at(r.get("at")):
            why = "`at` must be YYYY-MM-DD HH:MM"
        elif len(texts[rid]) > 1:
            why = "queued twice with different answers"
        elif x["status"] != "open":
            same = str(x.get("answer") or "").startswith(r["answer"].strip() + " (owner, ")
            state, why = ("done", None) if same else ("bad", f"the input is already {x['status']} with another answer")
        else:
            state = "done" if rid in took else "ok"
            took.add(rid)
        out.append((r, state or "bad", why))
    return out


def blocked_why(ctx):
    """Why nothing may be committed into the laptop clone now (None = go)."""
    if ctx.online is None:
        return "not fetched (dry run or preview)"
    if not ctx.online:
        return "origin not reached"
    if not ctx.laptop_fetched:
        return "could not fetch in the laptop clone"
    s = laptop_state(ctx)
    if s["branch"] != "main":
        return "laptop clone is not on main"
    if s["dirty"]:
        return "laptop clone has uncommitted files"
    if s["head"] != s["origin"]:
        return "laptop clone is not in sync with origin/main"
    if lock_state(ctx, ctx.laptop)[0] or lock_state(ctx, ctx.root)[0]:
        return "the build lock is held"
    return None


def apply_answers(ctx, commit=True):
    """Validate, and (commit=True) commit the valid ones into the laptop clone. Never pushes."""
    rows = read_answers(ctx)
    res = {"rows": [], "committed": [], "error": None}
    if not rows:
        return res
    doc = json.loads(git(ctx.laptop, "show", "HEAD:" + STEPS_REL))      # what is committed, not what is being edited
    judged = judge(rows, doc)
    ok = [r for r, st, _ in judged if st == "ok"]
    blocked = blocked_why(ctx) if ok else None
    if ok and not blocked and commit:
        try:
            commit_answers(ctx, doc, ok)
            res["committed"] = [r["id"] for r in ok]
        except Exception as e:
            res["error"], res["detail"] = why_public(e), why_local(e)
    known = {x["id"] for s in ctx.doc["steps"] for x in s.get("inputs", [])}
    main_open = {x["id"] for s in ctx.doc["steps"] for x in s.get("inputs", []) if x["status"] == "open"}
    seen = set()
    for r, st, why in judged:
        i = r.get("id") if isinstance(r, dict) and isinstance(r.get("id"), str) else None
        if (st == "ok" and i in res["committed"]) or (st == "done" and i in main_open and i not in {x["id"] for x in ok}):
            st, why = "committed", "waiting for sync.bat"     # answered in the laptop clone, still open on origin/main
        elif st == "ok":
            st, why = "queued", res["error"] or blocked or "next tick"
        if st != "done" and (i, st) not in seen:
            seen.add((i, st))
            res["rows"].append({"id": i if i in known else None, "state": st, "reason": why})      # an unknown id is free text: not published
    return res


def commit_answers(ctx, doc, ok):
    """One commit of exactly our bytes on exactly the HEAD we checked (compare-and-swap), else nothing.
    The laptop clone equals this clone (blocked_why), so the new file is validated in memory with this clone's check.py —
    the same check()/fmt() that `check.py --write` runs — before anything is written."""
    lp, sj, chk = ctx.laptop, ctx.laptop / STEPS_REL, ctx.chk
    head = git(lp, "rev-parse", "HEAD").strip()
    before = sj.read_bytes()
    if before.decode("utf-8").replace("\r\n", "\n") != chk.fmt(doc):
        raise DeskError("steps.json is not in canonical form (check.py --write first)")
    want, new = copy.deepcopy(doc), {r["id"]: r for r in ok}
    for s in want["steps"]:
        for x in s.get("inputs", []):
            if x["id"] in new:
                x["status"], x["answer"] = "answered", answer_text(new[x["id"]]["answer"], new[x["id"]]["at"])
    trial, unb = copy.deepcopy(want), chk.derive_unblocks(want["steps"])
    if any(chk.surf_fill(s, trial) for s in trial["steps"]) or any(s["unblocks"] != unb[s["id"]] for s in want["steps"]):
        raise DeskError("check.py --write would change more than the answered inputs (run it first)")
    errs = chk.check(want, chk.load_refs(), None, (None, None), ctx.now)[0] + chk.parity()
    if errs:
        raise DeskError("check.py fails with these answers", errs[0])
    blob_bytes = chk.fmt(want).encode("utf-8")
    disk = blob_bytes.replace(b"\n", b"\r\n") if b"\r\n" in before else blob_bytes
    old_blob = git(lp, "rev-parse", f"{head}:{STEPS_REL}").strip()
    blob = git(lp, "hash-object", "-w", "--no-filters", "--stdin", data=blob_bytes).strip()
    with tempfile.TemporaryDirectory(prefix="desk-index-") as td:      # a private index: nothing anyone staged can get in
        env = {"GIT_INDEX_FILE": str(Path(td) / "index")}
        git(lp, "read-tree", head, env=env)
        git(lp, "update-index", "--cacheinfo", f"100644,{blob},{STEPS_REL}", env=env)
        tree = git(lp, "write-tree", env=env).strip()
    sha = git(lp, "commit-tree", tree, "-p", head, "-m", "Desk answers: " + ", ".join(new)).strip()
    tmp = Path(git(lp, "rev-parse", "--absolute-git-dir").strip()) / "desk-steps.tmp"

    def put(data):
        tmp.write_bytes(data)
        for left in range(4, -1, -1):      # a virus scanner or editor may hold the file for a moment (Windows)
            try:
                return os.replace(tmp, sj)
            except PermissionError:
                if not left:
                    raise
                time.sleep(0.2)

    def ready():
        if git(lp, "symbolic-ref", "-q", "HEAD", ok=True)[1].strip() != "refs/heads/main":
            raise DeskError("laptop clone is not on main")
        if lock_state(ctx, lp)[0]:
            raise DeskError("the build lock is held")
        if dirty_paths(lp) != [STEPS_REL] or sj.read_bytes() != disk:
            raise DeskError("something else changed in the laptop clone meanwhile")

    try:
        why = blocked_why(ctx)      # again, as late as possible
        if why or sj.read_bytes() != before:
            raise DeskError(why or "steps.json changed meanwhile")
        put(disk)
        git(lp, "update-index", "--cacheinfo", f"100644,{blob},{STEPS_REL}")
        ready()      # last look
        git(lp, "update-ref", "-m", "Desk answers", "refs/heads/main", sha, head)      # fails if HEAD moved
    except BaseException as first:
        if git(lp, "rev-parse", f"HEAD:{STEPS_REL}", ok=True)[1].strip() == blob:
            if isinstance(first, Exception):
                print("another commit carried the answers: " + why_local(first))
                return
            raise
        # undo only our own edit: the index entry even if the file cannot be put back
        left = None
        try:
            if sj.read_bytes() == disk:
                put(before)
        except OSError as e:
            left = e
        code, staged, _ = git(lp, "ls-files", "-s", "--", STEPS_REL, ok=True)
        if code == 0 and blob in staged and git(lp, "update-index", "--cacheinfo", f"100644,{old_blob},{STEPS_REL}", ok=True)[0]:
            left = left or DeskError("index not restored")
        if left:
            raise DeskError("the tick's own edit is left in steps.json of the laptop clone", why_local(left))
        raise


def s_answers(ctx):
    return apply_answers(ctx, commit=False)["rows"]


FNS = dict(source=s_source, now=s_now, lock=s_lock, next=s_next, inputs=s_inputs, running=s_running, slips=s_slips,
           ci=s_ci, checks=s_checks, pipeline=s_pipeline, answers=s_answers)


def build(ctx, only=None, answers=None):
    d, why = {"schema": SCHEMA, "generated_at": stamp(ctx.now), "stale_after_h": STALE_H}, {}
    for k in SECTIONS:
        if only and k != only:
            continue
        try:
            d[k] = answers if k == "answers" and answers is not None else FNS[k](ctx)
        except Exception as e:
            d[k], why[k] = None, why_public(e)
            if DEBUG:
                print(f"[desk] {k}: {why_local(e)}")
    d["reasons"] = why
    return d


def strip(v):
    if isinstance(v, dict):
        return {k: strip(x) for k, x in v.items() if k not in VOLATILE}
    return [strip(x) for x in v] if isinstance(v, list) else v


def digest(d):
    return hashlib.sha256(json.dumps(strip(d), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ---- publish ----
def fetch(ctx):
    """`online` is about this clone only; a laptop clone that cannot fetch only holds back answers."""
    for clone, attr, args in ((ctx.root, "online", ["--prune", "origin", "+refs/heads/*:refs/remotes/origin/*"]), (ctx.laptop, "laptop_fetched", ["origin"])):
        try:
            git(clone, "fetch", "-q", *args)
            setattr(ctx, attr, True)
        except DeskError as e:
            setattr(ctx, attr, False)
            print(f"{attr}: no — {why_local(e)}")


def published(ctx):
    """(tip sha or None, its desk.json or None)"""
    code, out, _ = git(ctx.root, "rev-parse", "-q", "--verify", f"refs/remotes/origin/{BRANCH}", ok=True)
    if code:
        return None, None
    code, txt, _ = git(ctx.root, "show", f"refs/remotes/origin/{BRANCH}:{REMOTE_FILE}", ok=True)
    try:
        return out.strip(), json.loads(txt) if code == 0 else None
    except ValueError:
        return out.strip(), None


def why_publish(ctx, d):
    old = published(ctx)[1]
    if not isinstance(old, dict):
        return "first snapshot"
    if digest(old) != digest(d):
        return "content changed"
    at = parse_stamp(old.get("generated_at"))
    if at is None or (ctx.now - at).total_seconds() >= PUBLISH_H * 3600:
        return f"unchanged for {PUBLISH_H} h"
    return None


def publish(ctx, d):
    """One commit holding only build/desk.json on top of origin/desk-data, made without touching any working tree. Never forced."""
    if BRANCH in ("main", "master") or not re.match(r"^[a-z][a-z-]+$", BRANCH):
        raise DeskError("refusing to publish to this branch")
    folder, name = REMOTE_FILE.split("/")
    err = ""
    for attempt in (1, 2):
        tip = published(ctx)[0]
        blob = git(ctx.root, "hash-object", "-w", "--stdin", data=text_of(d)).strip()
        sub = git(ctx.root, "mktree", data=f"100644 blob {blob}\t{name}\n".encode()).strip()
        tree = git(ctx.root, "mktree", data=f"040000 tree {sub}\t{folder}\n".encode()).strip()
        msg = f"desk.json {d['generated_at']} (main {(d.get('source') or {}).get('commit')})"
        sha = git(ctx.root, "commit-tree", tree, "-m", msg, *(["-p", tip] if tip else [])).strip()
        code, _, err = git(ctx.root, "push", "-q", "origin", f"{sha}:refs/heads/{BRANCH}", ok=True)
        if code == 0:
            git(ctx.root, "update-ref", f"refs/remotes/origin/{BRANCH}", sha)
            return sha[:7]
        if attempt == 1:
            fetch(ctx)
    raise DeskError("push rejected twice", err)


def text_of(d):
    return (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def write_local(ctx, d):
    """Every tick: <laptop clone>/out/desk.json (gitignored), what Desk reads first. Same bytes as a publish; swapped in whole."""
    p = ctx.laptop / "out" / "desk.json"
    if not ctx.laptop.exists():
        raise OSError("laptop clone not found")
    p.parent.mkdir(exist_ok=True)
    tmp = p.with_name("desk.json.tmp")
    tmp.write_bytes(text_of(d))
    os.replace(tmp, p)


# ---- tick ----
def tick_lock(ctx):
    """The lock file holds our own id, so a late tick never removes a newer tick's lock."""
    ctx.out.mkdir(parents=True, exist_ok=True)
    p, me = ctx.out / "tick.lock", f"{os.getpid()}-{dt.datetime.now().timestamp()}"
    if p.exists() and dt.datetime.now().timestamp() - p.stat().st_mtime > TICK_LOCK_MIN * 60:
        p.unlink(missing_ok=True)
    try:
        with open(p, "x") as f:
            f.write(me)
    except FileExistsError:
        raise DeskError("another tick is running")
    return p, me


def tick_unlock(lock):
    with contextlib.suppress(OSError):
        if lock[0].read_text() == lock[1]:
            lock[0].unlink(missing_ok=True)


def notify(ctx, msgs):
    """Print each message once; print it again only after it went away and came back."""
    f = ctx.out / "notified.json"
    try:
        old = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        old = []
    old = old if isinstance(old, list) else []
    for m in msgs:
        if m not in old:
            print("NOTIFY: " + m)
    f.write_text(json.dumps(msgs, ensure_ascii=False), encoding="utf-8")


def tick(ctx):
    lockf = None
    if not ctx.dry:
        if ctx.root.resolve() == ctx.laptop.resolve():
            raise DeskError("run the tick from the dispatcher's own clone, not the laptop clone (README)")
        lockf = tick_lock(ctx)
    try:
        return tick_body(ctx)
    except Exception as e:      # told once, not every hour
        if lockf:
            e.told = True
            notify(ctx, ["The dispatcher tick could not run: " + why_local(e)])
        raise
    finally:
        if lockf:
            tick_unlock(lockf)


def tick_body(ctx):
    if not ctx.dry:
        fetch(ctx)
        if dirty_paths(ctx.root):
            raise DeskError("the dispatcher clone has changed files")
        if ctx.online and git(ctx.root, "rev-parse", "HEAD") != git(ctx.root, "rev-parse", "origin/main"):
            raise DeskError("the dispatcher clone is not at origin/main (git pull --ff-only first)")
    rc, msgs, ans = 0, [], None
    try:
        ans = apply_answers(ctx, commit=not ctx.dry)
        wait = [r["id"] for r in ans["rows"] if r["state"] == "committed"]
        bad = [f"{r['id']} ({r['reason']})" for r in ans["rows"] if r["state"] == "bad"]
        if wait:
            msgs.append(f'Desk answers committed: {", ".join(wait)}. Run: sync.bat "Desk answers"')
        if bad:
            msgs.append("Desk answers refused: " + "; ".join(bad))
        if ans["error"]:
            rc = 1
            msgs.append("Desk answers not committed: " + ans["detail"])
    except Exception as e:
        rc = 1
        msgs.append("Desk answers not read: " + why_local(e))
    d = build(ctx, answers=ans["rows"] if ans else None)
    red = [r["id"] for r in (d["checks"] or []) if r["state"] == "fail"]
    if red:
        msgs.append("Checks failing: " + ", ".join(red))
    if ctx.dry:
        w = why_publish(ctx, d)
        print(preview_text(d))
        print("dry run: would " + (f"publish ({w})" if w else "not publish (unchanged)") + "; nothing written")
        return 0
    try:
        write_local(ctx, d)
    except OSError as e:
        rc = 1
        msgs.append("out/desk.json not written: " + public(e))
    w = why_publish(ctx, d) if ctx.online else None
    if not ctx.online:
        rc = 1
        print("not published: origin not reached")
        last = parse_stamp((published(ctx)[1] or {}).get("generated_at"))
        if last is None or (ctx.now - last).total_seconds() > STALE_H * 3600:
            msgs.append(f"desk.json on {BRANCH} is over {STALE_H} h old: origin not reached")
    elif w:
        try:
            print(f"published {BRANCH} {publish(ctx, d)} ({w})")
        except DeskError as e:
            rc = 1
            print("not published: " + why_local(e))
            msgs.append("desk.json not published: " + why_local(e))
    else:
        print("not published: unchanged")
    notify(ctx, msgs)
    print(preview_text(d))
    return rc


def preview_text(d):
    size = lambda v: "unknown" if v is None else len(v)
    L = [f"desk · {d['generated_at']} · main {(d.get('source') or {}).get('commit')}"]
    L.append("lock: " + ("unknown" if not d["lock"] else d["lock"]["state"] + (f" · {d['lock']['chat']}" if d["lock"]["chat"] else "")))
    L.append("now: " + ("unknown" if d["now"] is None else ", ".join(c["id"] for c in d["now"]) or "nothing"))
    L.append("next: " + ("unknown" if d["next"] is None else ", ".join(f"{c['id']} {c['start']}" for c in d["next"])))
    L.append(f"your inputs: {size(d['inputs'])} · answers pending: {size(d['answers'])}")
    L += [f"  {r['state']:<8}{r['id']:<11}{r['detail']}" for r in d["checks"] or []]
    p = d["pipeline"] or {}
    L.append(f"pipeline: steps {size(p.get('steps'))} · open handoffs {size((p.get('handoffs') or {}).get('open'))} · "
             f"queue {size((p.get('code_queue') or {}).get('open'))} · scheduled {size(p.get('scheduled'))}")
    L += [f"unknown {k}: {v}" for k, v in {**d["reasons"], **p.get("reasons", {})}.items()]
    return "\n".join(L)


# ---- selftest: temporary repos, no network ----
def selftest():
    res = []

    def case(name, good, extra=""):
        res.append(bool(good))
        print(("ok  " if good else "BAD ") + name + ("" if good else f"  {extra}"))

    tmp = Path(tempfile.mkdtemp(prefix="desk-selftest-"))
    try:
        for n, fn in enumerate(SELFTESTS):
            try:
                fn(Fixture(tmp / str(n)), case)
            except Exception as e:
                case(fn.__name__, False, f"{type(e).__name__}: {e}")
    finally:
        def writable(f, p, _):
            os.chmod(p, 0o700)
            f(p)
        shutil.rmtree(tmp, onerror=writable)
    good = sum(res)
    print(f"{'PASS' if good == len(res) else 'FAIL'}: dispatch selftest {good}/{len(res)}")
    return 0 if good == len(res) else 1


NOW = dt.datetime(2026, 11, 24, 18, 0, tzinfo=IST)
GREEN = {"status": "completed", "conclusion": "success", "databaseId": 1, "url": "u"}
A1 = {"id": "T1.q1", "answer": "Option A", "by": "Owner", "at": "2026-11-24 17:00"}


class Fixture:
    """home/{origin.git, repo/biology-studio, dispatch/clone, handoff, tasks}: the real tools on a tiny steps.json."""
    def __init__(self, home):
        self.home = home
        self.origin, self.lap, self.clone = home / "origin.git", home / "repo" / "biology-studio", home / "dispatch" / "clone"
        (home / "handoff").mkdir(parents=True)
        (home / "dispatch").mkdir()
        (home / "tasks" / "bio-x").mkdir(parents=True)
        (home / "tasks" / "bio-x" / "SKILL.md").write_text("secret words")
        git(home, "init", "-q", "--bare", "-b", "main", str(self.origin))
        git(home, "init", "-q", "-b", "main", str(self.lap))
        for f in ["tools/tracker/check.py", "tools/ci/status.py"] + ["src/js/" + p.name for p in (ROOT / "src/js").glob("17-*.js")]:
            self.put(f, (ROOT / f).read_text(encoding="utf-8"))
        self.put(".gitignore", "out/\n__pycache__/\n")
        self.put("studio-docs/claude/DECISIONS.md", "| D-001 | 1 Jan 2026 | **First** x | y | z |\n")
        self.put("studio-docs/build/owner-test-checklist.md", "x\n")
        self.put("studio-docs/build/master-plan.md", "x\n")
        self.chk = load_module(self.lap / "tools/tracker/check.py", "fx_check")
        self.status("free")
        inp = lambda i, **k: dict({"id": i, "kind": "decide", "ask": "which?", "asked_in": "c", "asked": "2026-11-20", "answer": None, "status": "open", "d": None}, **k)
        step = lambda i, **k: dict({"id": i, "title": i, "type": "Build", "chat": f"Bio · Build · {i}", "status": "planned", "needs": [], "unblocks": [],
                                    "lock": True, "gates": {}, "check": None, "decisions": [], "prompt": None, "log": "—", "todo": [], "inputs": []}, **k)
        self.doc = {"schema": 2, "owner": "Owner", "collaborator": "Prof", "queue": ["T1", "T2"], "steps": [
            step("T1", unblocks=["T2"], inputs=[inp("T1.q1"), inp("T1.q2", status="closed", answer="x"), inp("T1.q3", **{"for": "prof"})]),
            step("T2", needs=["T1"], todo=["Tentative — x"])]}
        self.steps()
        self.user(self.lap)
        git(self.lap, "remote", "add", "origin", str(self.origin))
        self.push("seed")
        git(home, "clone", "-q", "-c", "core.autocrlf=false", str(self.origin), str(self.clone))
        self.user(self.clone)

    def user(self, c):
        for k, v in (("user.name", "t"), ("user.email", "t@example.invalid"), ("core.autocrlf", "false")):
            git(c, "config", k, v)

    def put(self, f, t):
        p = self.lap / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8", newline="\n")

    def status(self, lock):
        self.put("studio-docs/claude/STATUS.md", f"# S\n\n## Lock\n- Build lock: {lock}\n\n<!-- next:auto -->\nx\n<!-- /next:auto -->\n")

    def steps(self):
        self.put(STEPS_REL, self.chk.fmt(self.doc))

    def push(self, msg="x"):
        git(self.lap, "add", "-A")
        git(self.lap, "commit", "-q", "-m", msg)
        git(self.lap, "push", "-q", "-u", "origin", "main")
        if self.clone.exists():
            git(self.clone, "pull", "-q", "--ff-only")

    def push_only(self):
        git(self.lap, "push", "-q")
        git(self.clone, "pull", "-q", "--ff-only")

    def queue(self, *rows, raw=None):
        (self.home / "handoff" / "desk-answers.json").write_text(raw if raw is not None else json.dumps({"schema": 1, "answers": rows}), encoding="utf-8")

    def ctx(self, now=NOW, ci="green", **k):
        head = git(self.clone, "rev-parse", "HEAD").strip()
        return Ctx(self.clone, self.home, now=now, ci_runs=[dict(GREEN, headSha=head)] if ci == "green" else ci, tasks_dir=self.home / "tasks", **k)

    def run(self, **k):
        b = io.StringIO()
        try:
            with contextlib.redirect_stdout(b):
                rc = tick(self.ctx(**k))
        except DeskError as e:
            return 2, str(e)
        return rc, b.getvalue()

    def remote(self):
        code, t, _ = git(self.origin, "show", f"{BRANCH}:{REMOTE_FILE}", ok=True)
        return json.loads(t) if code == 0 else None

    def ncommits(self):
        return int(git(self.origin, "rev-list", "--count", BRANCH))

    def lapinput(self, i="T1.q1"):
        d = json.loads((self.lap / STEPS_REL).read_text(encoding="utf-8"))
        return next(x for s in d["steps"] for x in s["inputs"] if x["id"] == i)

    def row(self, d, i):
        return next(r for r in d["checks"] if r["id"] == i)

    def hook(self, repo, name):
        p = repo / "hooks" / name
        p.parent.mkdir(exist_ok=True)
        p.write_text("#!/bin/sh\nexit 1\n", newline="\n")
        os.chmod(p, 0o755)
        return p


def t_publish(f, case):
    main = git(f.origin, "rev-parse", "main")
    rc, out = f.run()
    d = f.remote()
    case("first tick publishes", rc == 0 and d and d["schema"] == 1, out)
    case("main is untouched, the branch holds one file", git(f.origin, "rev-parse", "main") == main and git(f.origin, "ls-tree", "-r", "--name-only", BRANCH).strip() == REMOTE_FILE)
    case("every section known", all(d[k] is not None for k in SECTIONS) and not d["reasons"], d["reasons"])
    case("next has dates and the tentative flag", {c["id"]: c["tentative"] for c in d["next"]} == {"T1": False, "T2": True} and all(c["start"] for c in d["next"]), d["next"])
    loc = f.lap / "out/desk.json"
    same = loc.read_bytes().decode() == git(f.origin, "show", f"{BRANCH}:{REMOTE_FILE}")
    case("local out/desk.json: same content as published, untracked", same and not dirty_paths(f.lap))
    f.run(now=NOW + dt.timedelta(hours=1))
    case("unchanged after 1 h: no publish", f.ncommits() == 1)
    case("the local file is rewritten every tick", json.loads(loc.read_bytes())["generated_at"] == "2026-11-24 19:00 IST")
    f.run(now=NOW + dt.timedelta(hours=5))
    case("unchanged after 5 h: publishes", f.ncommits() == 2)
    f.status("held by `Bio · Build · T1`, since 24 Nov 2026, 12:00 IST")
    f.push()
    f.run(now=NOW + dt.timedelta(hours=5.5))
    d = f.remote()
    case("content change publishes; lock age", f.ncommits() == 3 and (d["lock"]["state"], d["lock"]["chat"], d["lock"]["age_h"]) == ("held", "Bio · Build · T1", 11.5), d["lock"])
    case("no task descriptions or paths in the public file", "secret words" not in json.dumps(d) and not any(x in json.dumps(d) for x in (f.home.as_posix(), json.dumps(str(f.home))[1:-1])))
    rc, out = f.run(dry=True, now=NOW + dt.timedelta(hours=20))
    case("dry run writes nothing", rc == 0 and f.ncommits() == 3 and "nothing written" in out, out)


def t_rejected(f, case):
    f.run()
    hook = f.hook(f.origin, "pre-receive")
    rc, out = f.run(now=NOW + dt.timedelta(hours=6))
    case("push rejected: reported, no crash, nothing forced", rc == 1 and "NOTIFY: desk.json not published" in out and f.ncommits() == 1, out)
    rc, out = f.run(now=NOW + dt.timedelta(hours=7))
    case("the same notice is not repeated", rc == 1 and "NOTIFY" not in out, out)
    hook.unlink()
    git(f.lap, "fetch", "-q", "origin", BRANCH)
    tip = git(f.lap, "rev-parse", "FETCH_HEAD").strip()
    sha = git(f.lap, "commit-tree", tip + "^{tree}", "-p", tip, "-m", "someone else").strip()
    git(f.lap, "push", "-q", "origin", f"{sha}:refs/heads/{BRANCH}")
    c = f.ctx(now=NOW + dt.timedelta(hours=8))
    publish(c, build(c))
    case("branch moved meanwhile: retried on top, theirs kept", f.ncommits() == 3)


def t_offline(f, case):
    git(f.clone, "remote", "set-url", "origin", str(f.home / "gone.git"))
    f.queue(A1)
    rc, out = f.run()
    case("offline: no crash, not published", rc == 1 and "not published" in out, out)
    d = json.loads((f.lap / "out/desk.json").read_text(encoding="utf-8"))
    case("offline: a network row, answers stay queued", f.row(d, "network")["state"] == "warn" and d["answers"][0]["state"] == "queued" and f.lapinput()["status"] == "open")


def t_ci(f, case):
    def nogh():
        raise DeskError("gh (GitHub CLI) not found")
    d = build(f.ctx(ci=nogh))
    case("gh missing: ci null + reason, row unknown", d["ci"] is None and "gh" in d["reasons"]["ci"] and f.row(d, "ci")["state"] == "unknown")
    case("red CI is a failing row", f.row(build(f.ctx(ci=[dict(GREEN, conclusion="failure", headSha="abc")])), "ci")["state"] == "fail")
    case("a green run of another commit is not green", f.row(build(f.ctx(ci=[dict(GREEN, headSha="abc")])), "ci")["state"] == "warn")


def t_answers(f, case):
    f.queue(A1)
    main = git(f.origin, "rev-parse", "main")
    before = git(f.lap, "rev-parse", "HEAD").strip()
    old = json.loads((f.lap / STEPS_REL).read_text(encoding="utf-8"))
    rc, out = f.run()
    x = f.lapinput()
    case("valid answer committed", rc == 0 and x["status"] == "answered" and x["answer"] == "Option A (owner, 24 Nov 2026, Desk)", out)
    case("never pushed; owner gets the sync line", git(f.origin, "rev-parse", "main") == main and 'NOTIFY: Desk answers committed: T1.q1. Run: sync.bat "Desk answers"' in out, out)
    case("only steps.json in the commit, tree clean", git(f.lap, "diff", "--name-only", before, "HEAD").strip() == STEPS_REL and not dirty_paths(f.lap))
    new = json.loads((f.lap / STEPS_REL).read_text(encoding="utf-8"))
    for s in new["steps"] + old["steps"]:
        s["inputs"] = [y for y in s["inputs"] if y["id"] != "T1.q1"]
    case("only that input changed", new == old)
    head = git(f.lap, "rev-parse", "HEAD")
    f.run(now=NOW + dt.timedelta(hours=1))
    d = f.remote()
    case("second tick: not committed again, still waits for sync", git(f.lap, "rev-parse", "HEAD") == head and d["answers"] == [{"id": "T1.q1", "state": "committed", "reason": "waiting for sync.bat"}], d["answers"])
    case("answer text is not published", "Option A" not in json.dumps(d))
    git(f.lap, "push", "-q")
    git(f.clone, "pull", "-q", "--ff-only")
    f.run(now=NOW + dt.timedelta(hours=2))
    case("after the push the answer is no longer pending", f.remote()["answers"] == [])


def t_bad_answers(f, case):
    j = lambda *rows: [s for _, s, _ in judge(list(rows), f.doc)]
    for name, r in (("unknown id", dict(A1, id="T9.q1")), ("empty answer", dict(A1, answer=" ")), ("two lines", dict(A1, answer="a\nb")),
                    ("not the owner", dict(A1, by="Prof")), ("professor input", dict(A1, id="T1.q3")), ("bad date", dict(A1, at="2026-13-40 10:00")),
                    ("already closed", dict(A1, id="T1.q2")), ("not an object", "x"), ("id is a list", {"id": []})):
        case("refused: " + name, j(r) == ["bad"], j(r))
    case("duplicate, same text: applied once", j(A1, A1) == ["ok", "done"])
    case("duplicate, different text: both refused", j(A1, dict(A1, answer="B")) == ["bad", "bad"])
    f.queue(raw="{not json")
    rc, out = f.run()
    case("broken answers file: reported, snapshot still published", rc == 1 and "NOTIFY: Desk answers not read" in out and f.remote()["answers"] is None, out)


def t_blocked(f, case):
    f.queue(A1)
    (f.lap / "new.txt").write_text("x")
    f.run()
    d = f.remote()
    case("dirty clone: answer stays queued, row warns", d["answers"][0]["state"] == "queued" and f.row(d, "laptop")["state"] == "warn" and f.lapinput()["status"] == "open")
    (f.lap / "new.txt").unlink()
    f.status("held by `Bio · Build · T1`, since 24 Nov 2026, 12:00 IST")
    f.push()
    f.run()
    case("lock held: answer stays queued", f.remote()["answers"][0]["reason"] == "the build lock is held" and f.lapinput()["status"] == "open")
    f.status("free")
    f.push()
    f.put("x.txt", "x")
    git(f.lap, "add", "-A")
    git(f.lap, "commit", "-q", "-m", "unpushed")
    f.run()
    case("unpushed commit: answer stays queued", "not in sync" in f.remote()["answers"][0]["reason"])
    f.put("studio-docs/claude/STATUS.md", "no lock line\n")
    f.push()
    f.run()
    case("missing lock line is not 'free'", f.remote()["lock"] is None and f.lapinput()["status"] == "open")


def t_restore(f, case):
    f.queue(A1)
    before = (f.lap / STEPS_REL).read_bytes()
    real, seen = globals()["git"], []

    def at(verb, act):      # run `act` just before git <verb> in the laptop clone, once
        def g(cwd, *a, **k):
            if a[0] == verb and Path(cwd) == f.lap and "GIT_INDEX_FILE" not in (k.get("env") or {}) and not seen:
                seen.append(1)
                act()
            return real(cwd, *a, **k)
        seen.clear()
        globals()["git"] = g

    def boom():
        raise DeskError("git update-ref failed", "user bob@PC.(none) C:/Users/First Last/x ghp_secret")

    try:
        at("update-ref", boom)
        rc, out = f.run()
        pub = json.dumps(f.remote())
        case("commit fails: own edit restored, tree clean", rc == 1 and (f.lap / STEPS_REL).read_bytes() == before and not dirty_paths(f.lap), out)
        case("failure detail is not published", "update-ref failed" in pub and not any(x in pub for x in ("bob", "First", "Last", "ghp_")), pub[-300:])

        def other_commit():
            f.put("studio-docs/claude/note.md", "n")
            real(f.lap, "add", "studio-docs/claude/note.md")
            real(f.lap, "commit", "-q", "-m", "other", "--", "studio-docs/claude/note.md")
        at("update-ref", other_commit)
        rc, out = f.run()
        case("HEAD moved meanwhile: not committed, undone, theirs kept", rc == 1 and not dirty_paths(f.lap) and f.lapinput()["status"] == "open" and real(f.lap, "log", "-1", "--format=%s").strip() == "other" and "committed: T1" not in out, out)
        f.push_only()

        def branch():
            real(f.lap, "symbolic-ref", "HEAD", "refs/heads/side")
        real(f.lap, "branch", "side")
        at("symbolic-ref", branch)
        m = real(f.lap, "rev-parse", "main")
        rc, out = f.run()
        case("branch switched meanwhile: main not moved, undone", rc == 1 and real(f.lap, "rev-parse", "main") == m and not dirty_paths(f.lap), out)
        real(f.lap, "symbolic-ref", "HEAD", "refs/heads/main")

        def lock():
            f.status("held by `Bio · Build · T1`, since 24 Nov 2026, 17:59 IST")
        at("symbolic-ref", lock)
        rc, out = f.run()
        case("lock taken meanwhile: not committed, only their edit left", rc == 1 and real(f.lap, "rev-parse", "main") == m and dirty_paths(f.lap) == ["studio-docs/claude/STATUS.md"], out)
        f.status("free")
        osr = os.replace

        def held(a, b):
            if str(b) == str(f.lap / STEPS_REL) and held.n:
                raise PermissionError("held")
            held.n += str(b) == str(f.lap / STEPS_REL)
            return osr(a, b)
        held.n = 0
        os.replace = held
        try:
            at("update-ref", boom)
            rc, out = f.run()
        finally:
            os.replace = osr
        case("undo blocked by a file lock: the owner is told, index undone", rc == 1 and "own edit is left in steps.json" in out and not real(f.lap, "diff", "--cached", "--name-only").strip(), out)
        real(f.lap, "reset", "-q", "--hard")

        def swept():
            real(f.lap, "commit", "-q", "-am", "theirs")
        at("update-ref", swept)
        rc, out = f.run()
        case("another commit carried the answer: reported as committed", "Desk answers committed: T1.q1" in out and f.lapinput()["status"] == "answered", out)
        real(f.lap, "reset", "-q", "--hard", m.strip())

        def other_edit():
            f.put(STEPS_REL, (f.lap / STEPS_REL).read_text(encoding="utf-8") + " ")
        at("update-index", other_edit)
        h = real(f.lap, "rev-parse", "HEAD")
        rc, out = f.run()
        case("another chat's edit meanwhile: not committed, their file kept", rc == 1 and real(f.lap, "rev-parse", "HEAD") == h and (f.lap / STEPS_REL).read_text(encoding="utf-8").endswith(" "), out)
    finally:
        globals()["git"] = real
    real(f.lap, "reset", "-q", "--hard")

    edited = json.loads((f.lap / STEPS_REL).read_text(encoding="utf-8"))
    edited["steps"][0]["inputs"][0].update(status="answered", answer=answer_text(A1["answer"], A1["at"]))
    f.put(STEPS_REL, f.chk.fmt(edited))
    rc, out = f.run()
    case("same answer only edited, not committed: not called committed", f.remote()["answers"][0]["state"] == "queued" and "NOTIFY: Desk answers committed" not in out, out)
    real(f.lap, "reset", "-q", "--hard")
    f.doc["steps"][0]["status"] = "nonsense"
    f.steps()
    f.push()
    rc, out = f.run()
    case("check.py fails: nothing committed, restored, tracker row fails", rc == 1 and not dirty_paths(f.lap) and f.lapinput()["status"] == "open" and f.row(f.remote(), "tracker")["state"] == "fail", out)


def t_crlf(f, case):
    git(f.lap, "config", "core.autocrlf", "true")
    (f.lap / STEPS_REL).unlink()
    git(f.lap, "checkout", "--", STEPS_REL)
    f.put(".keep", "")
    (f.lap / ".keep").unlink()
    f.queue(A1)
    rc, out = f.run()
    blob = git(f.lap, "cat-file", "-p", "HEAD:" + STEPS_REL)
    case("CRLF clone: committed as LF, tree clean", rc == 0 and f.lapinput()["status"] == "answered" and "\r" not in blob and b"\r\n" in (f.lap / STEPS_REL).read_bytes() and not dirty_paths(f.lap), out)


def t_robust(f, case):
    start = time.time()
    child = "import subprocess,sys; subprocess.run([sys.executable,'-c','import time; time.sleep(25)'])"
    try:
        run_cmd([sys.executable, "-c", child], timeout=2)
        good = False
    except DeskError as e:
        good = "timed out" in str(e)
    case("a timeout kills the whole tree", good and time.time() - start < 12, time.time() - start)
    f.queue({"id": "\ud800", "answer": "x"}, dict(A1, answer="\ud800"), {"id": "T1.q1 the real answer is B", "answer": "x"})
    (f.clone / "out/dispatch").mkdir(parents=True, exist_ok=True)
    (f.clone / "out/dispatch/notified.json").write_text("5")
    rc, out = f.run()
    d = f.remote()
    case("bad unicode and odd files: no crash, published", rc == 0 and [x["state"] for x in d["answers"]] == ["bad"] * 3, (rc, out))
    case("an unknown answer id is not published", "real answer" not in json.dumps(d) and all(x["id"] in (None, "T1.q1") for x in d["answers"]), d["answers"])
    git(f.lap, "remote", "set-url", "origin", str(f.home / "gone.git"))
    f.queue(A1)
    rc, out = f.run(now=NOW + dt.timedelta(hours=1))
    d = f.remote()
    case("laptop clone cannot fetch: still published, answers wait", rc == 0 and d["answers"][0]["reason"] == "could not fetch in the laptop clone" and "could not fetch" in f.row(d, "laptop")["detail"], out)
    tree = lambda: {str(p): p.read_bytes() for p in f.lap.rglob("*") if p.is_file()}
    a = tree()
    f.run(dry=True)
    with contextlib.redirect_stdout(io.StringIO()):
        preview_text(build(f.ctx(dry=True)))
    case("dry run and preview leave the laptop clone byte-identical", tree() == a)
    case("dry run says not fetched", build(f.ctx(dry=True), "answers")["answers"][0]["reason"] == "not fetched (dry run or preview)")
    c = f.ctx()
    (a1, a2) = tick_lock(c), None
    a1[0].write_text("newer tick")
    tick_unlock(a1)
    case("a late tick keeps a newer tick's lock", a1[0].exists())
    a1[0].unlink()
    (f.clone / "x.txt").write_text("x")
    r1, r2 = f.run(), f.run()
    note = json.loads((f.clone / "out/dispatch/notified.json").read_text())
    case("a tick that cannot run is recorded for one notice", r1[0] == r2[0] == 2 and len(note) == 1 and "changed files" in note[0], note)
    leaks = ["C:\\Users\\First Last\\x", "\\\\srv\\share\\x", "/opt/a", "~/a", "ghp_abc123", "bob@PC.(none)"]
    got = [public("a " + x) for x in leaks]
    case("backstop removes paths, tokens, addresses", not any(w in g for g in got for w in ("First", "Last", "srv", "/opt", "~", "abc123", "bob")), got)


def t_checks(f, case):
    f.put("studio-docs/claude/DECISIONS.md", "| D-001 | 1 Jan 2026 | **First** x | y | z |\n| D-001 | 2 Jan 2026 | **Other** x | y | z |\n")
    f.push()
    case("D-id used twice", f.row(build(f.ctx()), "d_ids")["state"] == "fail")
    f.put("studio-docs/claude/DECISIONS.md", "| D-001 | 1 Jan 2026 | **First** x | y | z |\n")
    f.push()
    h = f.home / "handoff" / "a"
    h.mkdir()
    (h / "d-row.md").write_text("| D-001 | 3 Jan 2026 | **Third** x | y | z |\n")
    case("D-id clash with a handoff", "a: D-001" in f.row(build(f.ctx()), "d_ids")["detail"])
    (h / "README.md").write_text("Committed abc1234, 1 Jan 2026\n")
    case("a committed handoff is not a clash", f.row(build(f.ctx()), "d_ids")["state"] == "pass")
    f.put("studio-docs/a.md", "<" * 7 + " HEAD\nx\n" + ">" * 7 + " b\n")
    f.push()
    case("conflict markers on main", f.row(build(f.ctx()), "conflicts")["state"] == "fail")
    f.doc["steps"][0].update(status="in progress", runs=[{"chat": "Bio · Build · T1", "by": "Owner", "start": "2026-11-24 10:00", "outcome": "partial"}])
    f.steps()
    f.push()
    d = build(f.ctx())
    case("open run over 6 h flagged", f.row(d, "open_runs")["state"] == "warn" and d["running"][0]["old"] is True and [c["id"] for c in d["now"]] == ["T1"], d["running"])
    f.doc["steps"][0]["runs"][0]["start"] = "2026-11-24"
    f.steps()
    f.push()
    case("run without a time: null + reason", build(f.ctx())["running"][0]["old"] is None)
    f.status("held by `Bio · Build · T1`, since 22 Nov 2026, 12:00 IST")
    f.push()
    case("old lock flagged", f.row(build(f.ctx()), "lock_age")["state"] == "warn")
    (f.clone / STEPS_REL).write_text("{")
    d = build(f.ctx())
    case("unreadable steps.json: nulls + reasons, no crash", d["next"] is None and "next" in d["reasons"] and f.row(d, "tracker")["state"] == "unknown")


def t_pipeline(f, case):
    (f.home / "handoff" / "code-queue.md").write_text(
        "## Queue\n| # | Item | Handoff | State | Commit |\n|---|---|---|---|---|\n| 1 | A | `a` | ✅ done | x |\n| 2 | B | `b` | ⏳ open | |\n| 3 | C | `c` | ?? | |\n", encoding="utf-8")
    for n, t in (("a", "Committed abc1234, 1 Jan 2026"), ("b", "x\ncommitted by the scheduled task"), ("c", None)):
        (f.home / "handoff" / n).mkdir()
        if t:
            (f.home / "handoff" / n / "README.md").write_text(t)
    p = build(f.ctx())["pipeline"]
    case("code queue: open, done, unknown mark", p["code_queue"]["done"] == 1 and [x["state"] for x in p["code_queue"]["open"]] == ["open", None], p["code_queue"])
    case("handoffs: a committed line needs a sha or date", p["handoffs"]["committed"] == 1 and [(x["id"], x["committed"]) for x in p["handoffs"]["open"]] == [("b", False), ("c", None)], p["handoffs"])
    case("scheduled task state is null + reason", p["scheduled"] == [{"id": "bio-x", "enabled": None, "reason": "on/off is not in a readable file"}])
    shutil.rmtree(f.home / "handoff")
    p = build(f.ctx())["pipeline"]
    case("no handoff folder: null + reason", p["handoffs"] is None and "handoffs" in p["reasons"])


def t_guards(f, case):
    c = f.ctx()
    c.root = c.laptop
    try:
        tick(c)
        good = False
    except DeskError as e:
        good = "own clone" in str(e)
    case("refuses to tick from the laptop clone", good)
    (f.clone / "out/dispatch").mkdir(parents=True, exist_ok=True)
    lk = f.clone / "out/dispatch/tick.lock"
    lk.write_text("")
    rc, out = f.run()
    case("a second tick at the same time stops", rc == 2 and "another tick" in out and lk.exists(), out)
    lk.unlink()
    f.put("y.txt", "y")
    git(f.lap, "add", "-A")
    git(f.lap, "commit", "-q", "-m", "y")
    git(f.lap, "push", "-q")
    rc, out = f.run()
    case("stale dispatcher clone stops", rc == 2 and "not at origin/main" in out, out)
    got = public("https://tok@h/r")
    case("a token in a URL is removed, the URL kept", got == "https://h/r", got)


SELFTESTS = [t_publish, t_rejected, t_offline, t_ci, t_answers, t_bad_answers, t_blocked, t_restore, t_crlf, t_robust, t_checks, t_pipeline, t_guards]


def find_home(arg):
    if arg or os.environ.get("BIO_STUDIO_HOME"):
        return Path(arg or os.environ["BIO_STUDIO_HOME"])
    for p in ROOT.parents:
        if (p / "handoff").is_dir() and (p / "repo").is_dir():
            return p
    raise DeskError("Studio home not found (a folder with handoff/ and repo/): use --home or BIO_STUDIO_HOME")


def main():
    global DEBUG
    for st in (sys.stdout, sys.stderr):
        if hasattr(st, "reconfigure"):
            st.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tick", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--only", choices=SECTIONS)
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--home")
    a = ap.parse_args()
    DEBUG = a.debug
    if a.selftest:
        return selftest()
    if not (a.tick or a.preview or a.only or a.dry_run):
        ap.print_help()
        return 2
    try:
        ctx = Ctx(ROOT, find_home(a.home), dry=a.dry_run or not a.tick)
        if a.only:
            print(json.dumps(build(ctx, a.only), ensure_ascii=False, indent=1))
            return 0
        if a.preview:
            print(preview_text(build(ctx)))
            return 0
        return tick(ctx)
    except Exception as e:      # never a traceback, never mistaken for exit 1
        # told = the tick already sent its one notice; a second tick at once is normal
        quiet = getattr(e, "told", False) or "another tick" in str(e) or not a.tick or a.dry_run
        print(("desk: " if quiet else "NOTIFY: The dispatcher tick could not start: ") + why_local(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
