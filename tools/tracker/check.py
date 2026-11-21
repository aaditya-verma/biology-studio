#!/usr/bin/env python3
"""Biology Studio — progress map check (W1, D-040) + scheduler (W2, D-063). Owner doc: studio-docs/build/steps.json (format: tools/tracker/README.md).

Checks steps.json against the rules the app's #progress page also uses (src/js/17-tracker.js):
  unknown ids ......... step ids in needs, D-ids (claude/DECISIONS.md), owner checks T-ids (build/owner-test-checklist.md),
                        gate ids, ready-prompt keys (build/master-plan.md §13 "Ready prompt — <key>"), input ids <step>.q<n>
  loops ............... a step that (indirectly) needs itself
  unmet needs ......... ready / in progress / gates / owner check / done while a needed step is not done (or in owner check),
                        or ready while one of its own blocking owner inputs is open
  done but open ....... done with a gate not pass/na, or its owner check not pass/na
  old lock ............ claude/STATUS.md § Lock held for more than 24 h (warning — ask the holder, RULES I8)
  unconfirmed ......... proposed_by set (a collaborator's proposed status change) and not yet confirmed by the owner (warning);
                        status "proposed" without proposed_by; the owner proposing to himself (error)
  derived ............. `unblocks` must equal the reverse of every `needs` (fix: --write)
  parity .............. the app's TR_RULES (src/js/17-tracker.js) equal the vocabularies here
Warnings never fail the run unless --strict. Exit 1 on any error.

Run from the repo root:
  python tools/tracker/check.py                 # check (CI)
  python tools/tracker/check.py --write         # re-derive `unblocks` + canonical formatting, then check
  python tools/tracker/check.py --write --dry-run   # show what --write would change, write nothing
  python tools/tracker/check.py --only C1       # one step (loops are still checked across all)
  python tools/tracker/check.py --preview       # quick text board: Now · Ready · Blocked · Done + your inputs
  python tools/tracker/check.py --debug         # print every rule as it runs
  python tools/tracker/check.py --selftest      # each rule fires on a known-bad file; plan fixture; app ↔ checker plan parity (node)
  python tools/tracker/check.py --next          # W2: the schedule a chat reads first (rows, critical path, your inputs ranked)
  python tools/tracker/check.py --next --write  # … and refresh the auto block in STATUS § Next (--dry-run: show only)
  python tools/tracker/check.py --next --today 2026-11-22 --json   # plan from a date, as JSON
EDIT: vocabularies below (keep src/js/17-tracker.js TR_RULES in step — the in-app test compares them).
"""
import argparse, copy, datetime as dt, json, math, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "studio-docs"
STEPS = DOCS / "build" / "steps.json"

# EDIT: vocabularies (mirror TR_RULES in src/js/17-tracker.js)
STATUSES = ["idea", "planned", "ready", "in progress", "gates", "owner check", "done", "parked", "proposed"]
TYPES = ["Ideation", "Build", "Research", "Content", "Episode", "Review", "Fix", "Idea"]
GATES = ["G-Sci", "G-Learn", "G-Story", "G-Art", "G-Eng", "G-A11y", "G-Owner"]
GATE_STATES = ["open", "pass", "fail", "na"]
CHECK_STATES = ["open", "pass", "fail", "na"]
INPUT_KINDS = ["decide", "ask", "action"]
INPUT_STATES = ["open", "answered", "closed"]
MET = {"done", "owner check"}            # a need counts as met when the needed step is done or only waits on the owner's check
STARTED = {"ready", "in progress", "gates", "owner check", "done"}
STEP_KEYS = ["id", "title", "type", "chat", "status", "needs", "unblocks", "lock", "gates", "check", "decisions", "prompt", "log", "todo", "inputs"]
OPTIONAL = ["size", "proposed_by", "proposed_status", "proposed_on", "note", "uses", "est", "produces", "consumes", "runs", "improves"]
LOCK_MAX_H = 24
ID_RE = re.compile(r"^(?:[A-Z][A-Z0-9]*|[A-Z][0-9]+[a-z]?|X1\.\d\d|IB\d\d|GATE)$")
DBG = False


def dbg(*a):
    if DBG:
        print("[tracker]", *a)


def load_refs():
    """Ids that exist in the owner docs (D-ids, T-ids, ready-prompt keys)."""
    dec = set(re.findall(r"^\| (D-\d{3}) \|", (DOCS / "claude" / "DECISIONS.md").read_text(), re.M))
    chk = set(re.findall(r"^## (T\d+[a-z]?)\b", (DOCS / "build" / "owner-test-checklist.md").read_text(), re.M))
    chk |= set(re.findall(r"\*\*(T\d+[a-z]) —", (DOCS / "build" / "owner-test-checklist.md").read_text()))
    prompts = set(re.findall(r"^\*\*Ready prompt — (.+?)\*\*", (DOCS / "build" / "master-plan.md").read_text(), re.M))
    dbg(f"refs: {len(dec)} D-ids, T-ids {sorted(chk)}, {len(prompts)} prompts")
    return {"dec": dec, "chk": chk, "prompts": prompts}


def read_lock():
    """STATUS § Lock line → (holder text or None, datetime IST or None)."""
    try:
        t = (DOCS / "claude" / "STATUS.md").read_text()
    except OSError:
        return None, None
    m = re.search(r"^- Build lock: (.+)$", t, re.M)
    if not m or m.group(1).startswith("free"):
        return None, None
    d = re.search(r"(\d{1,2} [A-Z][a-z]{2} \d{4}), (\d{1,2}):(\d{2}) IST", m.group(1))
    when = None
    if d:
        when = dt.datetime.strptime(f"{d.group(1)} {d.group(2)}:{d.group(3)}", "%d %b %Y %H:%M").replace(tzinfo=dt.timezone(dt.timedelta(hours=5, minutes=30)))
    return m.group(1), when


def derive_unblocks(steps):
    order = {s["id"]: i for i, s in enumerate(steps)}
    out = {s["id"]: [] for s in steps}
    for s in steps:
        for n in s.get("needs", []):
            if n in out:
                out[n].append(s["id"])
    return {k: sorted(v, key=lambda x: order[x]) for k, v in out.items()}


def find_loops(steps):
    by = {s["id"]: s for s in steps}
    loops, state = [], {}

    def visit(i, path):
        state[i] = 1
        for n in by[i].get("needs", []):
            if n not in by:
                continue
            if state.get(n) == 1:
                cyc = path[path.index(n):] + [n]
                loops.append(" → ".join(cyc))
            elif not state.get(n):
                visit(n, path + [n])
        state[i] = 2

    for s in steps:
        if not state.get(s["id"]):
            visit(s["id"], [s["id"]])
    return loops


def parity():
    """TR_RULES in the app (src/js/17-tracker.js) must equal the vocabularies here — one rule set in two places."""
    js = (ROOT / "src" / "js" / "17-tracker.js").read_text()
    m = re.search(r"const TR_RULES=(\{.*?\});", js, re.S)
    if not m:
        return ["app: TR_RULES not found in src/js/17-tracker.js"]
    r = json.loads(m.group(1))
    want = {"statuses": STATUSES, "types": TYPES, "gates": GATES, "met": sorted(MET, key=STATUSES.index), "started": sorted(STARTED, key=STATUSES.index)}
    return [f"app: TR_RULES.{k} {r.get(k)} ≠ check.py {v}" for k, v in want.items() if r.get(k) != v]


def check(doc, refs, only=None, lock=(None, None), now=None):
    E, W = [], []
    steps = doc.get("steps", [])
    owner, collab = doc.get("owner"), doc.get("collaborator")
    if not owner:
        E.append("file: `owner` missing")
    ids = [s.get("id") for s in steps]
    by = {s.get("id"): s for s in steps}
    dupes = {i for i in ids if ids.count(i) > 1}
    for i in sorted(d for d in dupes if d):
        E.append(f"{i}: id used twice")
    unb = derive_unblocks([s for s in steps if s.get("id")])
    input_ids = []
    for s in steps:
        sid = s.get("id", "?")
        if only and sid != only:
            continue
        dbg("step", sid, s.get("status"))
        e = lambda m: E.append(f"{sid}: {m}")
        for k in STEP_KEYS:
            if k not in s:
                e(f"field `{k}` missing")
        for k in s:
            if k not in STEP_KEYS and k not in OPTIONAL:
                e(f"unknown field `{k}`")
        if not isinstance(sid, str) or not ID_RE.match(sid):
            e("bad step id (README § Id formats)")
        if s.get("status") not in STATUSES:
            e(f"status `{s.get('status')}` not one of {STATUSES}")
        if s.get("type") not in TYPES:
            e(f"type `{s.get('type')}` not one of {TYPES}")
        if not str(s.get("chat", "")).startswith(("Bio · ", "Embryo · ")):
            e("chat name must be `Bio · <Type> · <Step>`")
        for k in ("needs", "unblocks", "decisions", "todo", "inputs"):
            if k in s and not isinstance(s[k], list):
                e(f"`{k}` must be a list")
        needs = s.get("needs") if isinstance(s.get("needs"), list) else []
        for n in needs:
            if n not in by:
                e(f"needs unknown step `{n}`")
            if n == sid:
                e("needs itself")
        if isinstance(s.get("unblocks"), list) and s["unblocks"] != unb.get(sid, []):
            e(f"`unblocks` is derived — expected {unb.get(sid, [])} (run --write)")
        if not isinstance(s.get("lock"), bool):
            e("`lock` must be true/false")
        g = s.get("gates")
        if not isinstance(g, dict):
            e("`gates` must be an object {gate: state}")
            g = {}
        for k, v in g.items():
            if k not in GATES:
                e(f"unknown gate `{k}`")
            if v not in GATE_STATES:
                e(f"gate {k} state `{v}` not one of {GATE_STATES}")
        c = s.get("check")
        if c is not None:
            if not isinstance(c, dict) or "id" not in c:
                e("`check` must be null or {id, state}")
                c = None
            else:
                if c["id"] not in refs["chk"]:
                    e(f"owner check `{c['id']}` not in build/owner-test-checklist.md")
                if c.get("state") not in CHECK_STATES:
                    e(f"check state `{c.get('state')}` not one of {CHECK_STATES}")
        for d in s.get("decisions", []) if isinstance(s.get("decisions"), list) else []:
            if d not in refs["dec"]:
                e(f"decision `{d}` not in claude/DECISIONS.md")
        if s.get("prompt") is not None and s.get("prompt") not in refs["prompts"]:
            e(f"ready prompt `{s.get('prompt')}` not in build/master-plan.md §13")
        for x in s.get("inputs", []) if isinstance(s.get("inputs"), list) else []:
            xi = x.get("id", "?") if isinstance(x, dict) else "?"
            ee = lambda m: E.append(f"{sid} › {xi}: {m}")
            if not isinstance(x, dict):
                ee("input must be an object")
                continue
            input_ids.append(xi)
            if not re.match(rf"^{re.escape(sid)}\.q\d+$", str(xi)):
                ee(f"input id must be `{sid}.q<n>`")
            for k in ("kind", "ask", "asked_in", "asked", "status"):
                if not x.get(k):
                    ee(f"`{k}` missing")
            if x.get("kind") and x["kind"] not in INPUT_KINDS:
                ee(f"kind `{x['kind']}` not one of {INPUT_KINDS}")
            if x.get("status") and x["status"] not in INPUT_STATES:
                ee(f"status `{x['status']}` not one of {INPUT_STATES}")
            if x.get("asked") and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(x["asked"])):
                ee("`asked` must be YYYY-MM-DD")
            if x.get("d") and x["d"] not in refs["dec"]:
                ee(f"decision `{x['d']}` not in claude/DECISIONS.md")
            if x.get("status") in ("answered", "closed") and not x.get("answer"):
                ee("answered/closed input needs its `answer`")
        st = s.get("status")
        unmet = [n for n in needs if n in by and by[n].get("status") not in MET]
        if st in STARTED and unmet:
            e(f"status `{st}` but needs not met: {', '.join(f'{n} ({by[n].get('status')})' for n in unmet)}")
        if st == "ready":
            bl = [x.get("id") for x in s.get("inputs", []) if isinstance(x, dict) and x.get("blocks") and x.get("status") == "open"]
            if bl:
                e(f"ready but blocking owner input open: {', '.join(bl)}")
        if st == "done":
            og = [k for k, v in g.items() if v not in ("pass", "na")]
            if og:
                e(f"done with open gates: {', '.join(og)}")
            if c and c.get("state") not in ("pass", "na"):
                e(f"done with owner check {c['id']} {c.get('state')}")
        pb, ps = s.get("proposed_by"), s.get("proposed_status")
        if st == "proposed" and not pb:
            e("status `proposed` needs `proposed_by`")
        if pb or ps:
            if not (pb and ps and s.get("proposed_on")):
                e("a proposal needs proposed_by + proposed_status + proposed_on")
            elif pb == owner:
                e("the owner sets status directly — no proposal needed")
            elif ps not in STATUSES:
                e(f"proposed_status `{ps}` not one of {STATUSES}")
            else:
                W.append(f"{sid}: {pb} proposes `{st}` → `{ps}` ({s.get('proposed_on')}) — owner to confirm")
    dup_in = {i for i in input_ids if input_ids.count(i) > 1}
    for i in sorted(dup_in):
        E.append(f"input id `{i}` used twice")
    for lp in find_loops([s for s in steps if s.get("id") in by and isinstance(s.get("needs"), list)]):
        E.append(f"dependency loop: {lp}")
    holder, when = lock
    if holder and when:
        age = ((now or dt.datetime.now(dt.timezone.utc)) - when).total_seconds() / 3600
        dbg(f"lock: {holder} · {age:.1f} h")
        if age > LOCK_MAX_H:
            W.append(f"build lock held {age:.0f} h (> {LOCK_MAX_H} h): {holder} — ask the holder (RULES I8)")
    elif holder:
        W.append(f"build lock line has no readable date: {holder}")
    E2, W2 = check_w2(doc)
    if only:
        E2 = [x for x in E2 if x.startswith(only + ":")]
        W2 = [x for x in W2 if x.startswith(only + ":")]
    return E + E2, W + W2


# ---- W2 scheduler (D-063) — mirror of trPlan() in src/js/17-plan.js; --selftest compares both (node) ----
# EDIT: PLAN_DEF must equal PLAN_DEF in src/js/17-plan.js (parity checks it)
PLAN_DEF = {"day_min": [180, 180, 180, 180, 180, 360, 360], "chat_min": 60, "check_min": 15, "input_min": 10, "horizon": 120,
            "chats": {"Ideation": 0.5, "Build": 1, "Research": 1, "Content": 1, "Episode": 2, "Review": 0.5, "Fix": 0.5, "Idea": 1},
            "rows": ["lock", "gpu", "research", "owner", "prof"], "exclusive": ["lock", "gpu"], "met": ["done", "owner check"],
            "running": ["in progress", "gates"], "waiting": ["ready", "planned"], "unplanned": ["idea", "parked", "proposed"]}
USES = ["gpu", "research", "prof"]
RUN_OUTCOMES = ["done", "partial", "stopped", "fail"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?$")


def _js_round(x):
    return int(math.floor(x + 0.5))


def plan_day(iso, add):
    return (dt.date.fromisoformat(iso) + dt.timedelta(days=add)).isoformat()


def plan_cal(doc):
    c = dict(PLAN_DEF)
    c.update((doc or {}).get("calendar") or {})
    c["off"] = ((doc or {}).get("calendar") or {}).get("off") or []
    ch = dict(PLAN_DEF["chats"])
    ch.update(((doc or {}).get("calendar") or {}).get("chats") or {})
    c["chats"] = ch
    return c


def plan_res(s):
    u, r = s.get("uses") or [], []
    if len(u) == 1 and u[0] == "prof":
        return ["prof"]
    if s.get("lock"):
        r.append("lock")
    if "gpu" in u:
        r.append("gpu")
    if s.get("type") == "Research" or "research" in u:
        r.append("research")
    return r or ["owner"]


def plan_chats(s, cal):
    e = s.get("est") or {}
    if isinstance(e.get("chats"), (int, float)) and not isinstance(e.get("chats"), bool):
        return e["chats"]
    return cal["chats"].get(s.get("type"), 1)


def plan(doc, today):
    """Same answer as trPlan(doc, today) in the app — see src/js/17-plan.js for the rules in words."""
    cal = plan_cal(doc)
    steps = doc.get("steps", [])
    by = {s["id"]: s for s in steps}
    pos = {s["id"]: i for i, s in enumerate(steps)}
    q = doc.get("queue") or []
    qi = {}
    for i, x in enumerate(q):
        qi.setdefault(x, i)
    pri = lambda s: qi[s["id"]] if s["id"] in qi else len(q) + pos[s["id"]]
    items, item = [], {}

    def add(it):
        items.append(it)
        item[it["id"]] = it

    for s in steps:
        c = s.get("check")
        if s.get("status") == "owner check" and c and c.get("state") == "open":
            add(dict(id=f"{s['id']}·{c['id']}", step=s["id"], kind="check", row="owner", res=["owner"], mins=cal["check_min"], deps=[], pri=-1, done=False))
        for x in s.get("inputs", []):
            if x.get("status") == "open" and x.get("blocks") and x.get("for") != "prof":
                add(dict(id=x["id"], step=s["id"], kind="input", row="owner", res=["owner"], mins=cal["input_min"], deps=[], pri=-1, done=False))
    for s in steps:
        res = plan_res(s)
        row = res[0]
        if s.get("status") in PLAN_DEF["met"] or row == "prof" or s.get("type") == "Idea":
            continue
        if s.get("status") in PLAN_DEF["unplanned"]:
            add(dict(id=s["id"], step=s["id"], kind="step", row=row, res=res, mins=0, deps=[], pri=pri(s), never=True, done=False))
            continue
        est, ran = plan_chats(s, cal), len(s.get("runs") or [])
        running = s.get("status") in PLAN_DEF["running"]
        left = max(0.5, est - ran) if running else est
        deps = list(s.get("needs", [])) + [x["id"] for x in s.get("inputs", []) if x.get("status") == "open" and x.get("blocks") and x.get("for") != "prof"]
        live = any(isinstance(r, dict) and r.get("start") and not r.get("end") for r in s.get("runs") or [])
        add(dict(id=s["id"], step=s["id"], kind="step", row=row, res=res, mins=_js_round(left * cal["chat_min"]), deps=deps, pri=pri(s),
                 running=running, live=live, done=False, slipped=ran > est, wait=int((s.get("est") or {}).get("days") or 0)))
    order = sorted(items, key=lambda a: (0 if a.get("running") else 1, a["pri"], pos[a["step"]], a["id"]))
    finished = {s["id"] for s in steps if s.get("status") in PLAN_DEF["met"]}
    met = lambda d: d in finished or (d in by and by[d].get("status") == "owner check")
    end_of = lambda d: item[d]["end"] if d in item and item[d]["end"] else today
    wait_ok = lambda x, day: not x.get("wait") or plan_day(max([today] + [end_of(d) for d in x["deps"]]), x["wait"]) <= day
    busy = {}
    for it in order:
        it.update(left=it["mins"], start=None, end=None)
    last = None
    for n in range(cal["horizon"]):
        day = plan_day(today, n)
        budget = 0 if day in cal["off"] else cal["day_min"][dt.date.fromisoformat(day).weekday()]
        while budget > 0:
            it = next((x for x in order if not x["done"] and not x.get("never") and all(met(d) for d in x["deps"]) and wait_ok(x, day)
                       and all(r not in busy or busy[r] == x["id"] for r in x["res"])), None)
            if not it:
                break
            if it["start"] is None:
                it["start"] = day
                for r in it["res"]:
                    if r in PLAN_DEF["exclusive"]:
                        busy[r] = it["id"]
            take = min(it["left"], budget)
            it["left"] -= take
            budget -= take
            if it["left"] <= 0:
                it.update(done=True, end=day)
                last = day
                finished.add(it["id"])
                for r in it["res"]:
                    if busy.get(r) == it["id"]:
                        del busy[r]
    sched = [x for x in items if x["end"]]
    tgt = item["GATE"] if "GATE" in item and item["GATE"]["end"] else None
    if tgt is None:
        for b in sched:
            if tgt is None or b["end"] > tgt["end"] or (b["end"] == tgt["end"] and b["pri"] > tgt["pri"]):
                tgt = b
    critical = []
    while tgt:
        critical.insert(0, {"id": tgt["id"], "step": tgt["step"]})
        nxt = None
        for b in (item[d] for d in tgt["deps"] if d in item and item[d]["end"]):
            if nxt is None or b["end"] > nxt["end"]:
                nxt = b
        tgt = nxt
    rows = {r: {"now": [], "next": [], "later": []} for r in PLAN_DEF["rows"]}
    for x in sorted([x for x in items if x["row"] != "prof"], key=lambda a: (a["start"] or "9", a["pri"], pos[a["step"]])):
        R = rows[x["row"]]
        cell = dict(id=x["id"], step=x["step"], kind=x["kind"], start=x["start"], end=x["end"], mins=x["mins"], slipped=bool(x.get("slipped")))
        if x.get("live") or (x["start"] == today and x["kind"] != "step"):
            R["now"].append(cell)
        elif not R["next"] and x["start"]:
            R["next"].append(cell)
        else:
            R["later"].append(cell)
    down = {}
    for s in steps:
        for n in s.get("needs", []):
            down.setdefault(n, []).append(s["id"])

    def reach(i):
        seen, st = set(), [i]
        while st:
            c = st.pop()
            for k in down.get(c, []):
                if k not in seen:
                    seen.add(k)
                    st.append(k)
        return len([k for k in seen if k in by and by[k].get("status") != "done"])

    ranked = []
    for s in steps:
        r = 0 if s.get("status") == "done" else reach(s["id"])
        for x in s.get("inputs", []):
            if x.get("status") == "open" and x.get("for") != "prof":
                ranked.append(dict(id=x["id"], step=s["id"], kind=x.get("kind") or None, unblocks=r, blocks=bool(x.get("blocks")), asked=x.get("asked") or ""))
        c = s.get("check")
        if s.get("status") == "owner check" and c and c.get("state") == "open":
            ranked.append(dict(id=c["id"], step=s["id"], kind="check", unblocks=r, blocks=False, asked=c.get("since") or ""))
    ranked.sort(key=lambda a: (0 if a["blocks"] else 1, -a["unblocks"], a["asked"], a["id"]))
    prof = []
    for s in steps:
        if plan_res(s)[0] == "prof" and s.get("status") != "done":
            prof.append(dict(id=s["id"], step=s["id"], kind="step", improves=s.get("improves") or ""))
        for x in s.get("inputs", []):
            if x.get("for") == "prof" and x.get("status") == "open":
                prof.append(dict(id=x["id"], step=s["id"], kind=x.get("kind") or None, improves=x.get("improves") or ""))
    dates = {x["id"]: dict(start=x["start"], end=x["end"], row=x["row"], mins=x["mins"], slipped=bool(x.get("slipped"))) for x in items if x["kind"] == "step"}
    return {"today": today, "end": last, "critical": critical, "rows": rows, "ranked": ranked, "prof": prof, "dates": dates}


def check_w2(doc):
    """W2 rules: calendar/queue/est/uses/produces/consumes/runs shapes, resource overlap, professor never blocks, outputs have producers."""
    E, W = [], []
    steps = doc.get("steps", [])
    by = {s.get("id"): s for s in steps}
    cal = doc.get("calendar")
    if cal is not None:
        if not isinstance(cal, dict):
            E.append("calendar: must be an object")
        else:
            dm = cal.get("day_min", PLAN_DEF["day_min"])
            if not (isinstance(dm, list) and len(dm) == 7 and all(isinstance(v, int) and v >= 0 for v in dm)):
                E.append("calendar: day_min must be 7 whole minutes, Mon…Sun")
            if isinstance(dm, list) and dm and not any(dm):
                W.append("calendar: day_min is all 0 — nothing gets a date")
            for k in ("chat_min", "check_min", "input_min", "horizon"):
                if k in cal and not (isinstance(cal[k], int) and cal[k] > 0):
                    E.append(f"calendar: {k} must be a whole number > 0")
            for d in cal.get("off", []):
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(d)):
                    E.append(f"calendar: off day `{d}` must be YYYY-MM-DD")
            for k in cal:
                if k not in ("day_min", "chat_min", "check_min", "input_min", "horizon", "off", "chats", "note"):
                    E.append(f"calendar: unknown key `{k}`")
    for x in doc.get("queue") or []:
        if x not in by:
            E.append(f"queue: unknown step `{x}`")
    producer = {}
    for s in steps:
        for o in s.get("produces") or []:
            if o in producer:
                E.append(f"{s.get('id')}: output `{o}` also produced by {producer[o]}")
            producer[o] = s.get("id")

    def ancestors(i):
        seen, st = set(), [i]
        while st:
            c = st.pop()
            for n in (by.get(c) or {}).get("needs", []):
                if n not in seen:
                    seen.add(n)
                    st.append(n)
        return seen

    profonly = {s.get("id") for s in steps if (s.get("uses") or []) == ["prof"]}
    held = {}
    for s in steps:
        sid = s.get("id", "?")
        e = lambda m: E.append(f"{sid}: {m}")
        est = s.get("est")
        if est is not None:
            if not isinstance(est, dict) or any(k not in ("chats", "owner_min", "days") for k in est):
                e("`est` must be {chats, owner_min, days}")
            elif "days" in est and not (isinstance(est["days"], int) and not isinstance(est["days"], bool) and est["days"] >= 0):
                e("`est` days must be whole days ≥ 0")
            elif ("chats" in est and not (isinstance(est["chats"], (int, float)) and est["chats"] >= 0)) or ("owner_min" in est and not (isinstance(est["owner_min"], int) and est["owner_min"] >= 0)):
                e("`est` chats ≥ 0, owner_min whole minutes ≥ 0")
        for u in s.get("uses") or []:
            if u not in USES:
                e(f"uses `{u}` not one of {USES}")
        for n in s.get("needs", []):
            if n in profonly:
                e(f"needs {n}, a professor-only step — the professor never blocks (D-063)")
        for x in s.get("inputs", []):
            if isinstance(x, dict) and x.get("for") not in (None, "prof"):
                e(f"input {x.get('id')}: `for` must be \"prof\" or absent")
            if isinstance(x, dict) and x.get("for") == "prof" and x.get("blocks"):
                e(f"input {x.get('id')} is for the professor and blocks — the professor never blocks (D-063)")
        anc = ancestors(sid)
        for o in s.get("consumes") or []:
            if o not in producer:
                e(f"consumes `{o}` but no step produces it")
            elif producer[o] != sid and producer[o] not in anc:
                e(f"consumes `{o}` from {producer[o]} but does not need it (add {producer[o]} to needs)")
        runs = s.get("runs")
        if runs is not None:
            if not isinstance(runs, list):
                e("`runs` must be a list")
                runs = []
            for k, r in enumerate(runs):
                if not isinstance(r, dict):
                    e(f"run {k + 1}: must be an object")
                    continue
                for f in ("chat", "by", "start", "outcome"):
                    if not r.get(f):
                        e(f"run {k + 1}: `{f}` missing")
                for f in r:
                    if f not in ("chat", "by", "start", "end", "outcome", "commit", "note"):
                        e(f"run {k + 1}: unknown field `{f}`")
                if r.get("chat") and not str(r["chat"]).startswith(("Bio · ", "Embryo · ")):
                    e(f"run {k + 1}: chat must be `Bio · <Type> · <Step>`")
                for f in ("start", "end"):
                    if r.get(f) and not DATE_RE.match(str(r[f])):
                        e(f"run {k + 1}: `{f}` must be YYYY-MM-DD or YYYY-MM-DD HH:MM")
                if r.get("start") and r.get("end") and str(r["end"]) < str(r["start"]):
                    e(f"run {k + 1}: ends before it starts")
                if r.get("outcome") and r["outcome"] not in RUN_OUTCOMES:
                    e(f"run {k + 1}: outcome `{r['outcome']}` not one of {RUN_OUTCOMES}")
        if s.get("status") in ("in progress", "gates", "owner check", "done") and s.get("type") not in ("Idea",) and not runs:
            W.append(f"{sid}: started but no `runs` — add the chat's run line (INSTRUCTIONS §4)")
        if any(isinstance(r, dict) and r.get("start") and not r.get("end") for r in runs or []):   # an open run = a chat working on it now
            for r in plan_res(s):
                if r in PLAN_DEF["exclusive"]:
                    if r in held:
                        E.append(f"{sid}: an open run on `{r}` at the same time as {held[r]} — one chat per {r} row (close the other run's `end`)")
                    held[r] = sid
    return E, W


def plan_parity(doc, today):
    """Run trPlan() in node on the same data; differences are errors. No node → a warning (CI has node)."""
    js = ROOT / "src" / "js" / "17-plan.js"
    if not shutil.which("node"):
        return [], ["plan parity skipped: node not found"]
    m = re.search(r"const PLAN_DEF=(\{.*?\});", js.read_text(), re.S)
    if not m or json.loads(m.group(1)) != PLAN_DEF:
        return ["app: PLAN_DEF in src/js/17-plan.js ≠ check.py PLAN_DEF"], []
    src = f"const {{trPlan}}=require({json.dumps(str(js))});const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(trPlan(d.doc,d.today)));"
    r = subprocess.run(["node", "-e", src], input=json.dumps({"doc": doc, "today": today}), capture_output=True, text=True, timeout=60)
    if r.returncode:
        return [f"app: trPlan failed in node: {r.stderr.strip()[:300]}"], []
    a, b = json.loads(r.stdout), plan(doc, today)
    if a != b:
        diff = [k for k in b if a.get(k) != b.get(k)]
        return [f"app: trPlan ≠ check.py plan() for {today} in {diff}"], []
    return [], []


def ist_today():
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=5, minutes=30)).date().isoformat()


def fmt_day(iso):
    if not iso:
        return "no date"
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b')}"


def next_text(doc, P, lock):
    """The short schedule a chat reads first (INSTRUCTIONS §2) and STATUS § Next shows between the auto markers."""
    by = {s["id"]: s for s in doc["steps"]}
    name = lambda i: by[i]["title"] if i in by else i
    cell = lambda c: f"{c['step'] if c['kind'] == 'step' else c['id']} ~{fmt_day(c['end'])}" + (" (slipped)" if c["slipped"] else "")
    lab = {"lock": "Lock", "gpu": "GPU", "research": "Research", "owner": "You (no lock)"}
    out = [f"Schedule (auto · check.py --next · est. from {fmt_day(P['today'])}; order fixed, dates move):"]
    for r in ("lock", "gpu", "research", "owner"):
        R = P["rows"][r]
        now = [cell(c) + " now" for c in R["now"]]
        if len(now) > 3:
            now = now[:3] + [f"+{len(now) - 3} more now"]
        parts = now + [cell(c) + " next" for c in R["next"]] + [cell(c) for c in R["later"] if c["end"]][:3]
        if parts:
            out.append(f"- {lab[r]}: " + " → ".join(parts))
    if P["critical"]:
        last = P["critical"][-1]
        end = (P["dates"].get(last["id"]) or {}).get("end") or P["end"]
        out.append(f"- Critical path: {' → '.join(c['id'] for c in P['critical'])} (ends ~{fmt_day(end)})")
    top = P["ranked"][:3]
    if top:
        out.append("- Your inputs first: " + " · ".join(f"{x['id']} ({'blocks a start · ' if x['blocks'] else ''}unblocks {x['unblocks']})" for x in top))
    if P["prof"]:
        out.append(f"- Professor (optional, {len(P['prof'])}): " + " · ".join(x["id"] for x in P["prof"][:3]))
    out.append(f"- Lock: {lock[0] or 'free'}")
    return "\n".join(out)


AUTO_A, AUTO_B = "<!-- next:auto -->", "<!-- /next:auto -->"


def write_next(text, dry):
    p = DOCS / "claude" / "STATUS.md"
    t = p.read_text()
    if AUTO_A not in t or AUTO_B not in t:
        print(f"FAIL: STATUS § Next has no {AUTO_A} … {AUTO_B} block")
        return 1
    new = re.sub(re.escape(AUTO_A) + r".*?" + re.escape(AUTO_B), lambda m: f"{AUTO_A}\n{text}\n{AUTO_B}", t, flags=re.S)
    if dry:
        print("STATUS § Next auto block:", "unchanged" if new == t else "would change")
    elif new != t:
        p.write_text(new)
        print("wrote STATUS § Next auto block")
    return 0


def fmt(doc):
    """Canonical text: one key per line inside each step, short lists inline, one line per input — readable diffs."""
    j = lambda v: json.dumps(v, ensure_ascii=False)
    head = [f' {j(k)}: {j(v)}' for k, v in doc.items() if k != "steps"]
    rows = []
    for s in doc["steps"]:
        lines = []
        for k in STEP_KEYS + [k for k in OPTIONAL if k in s] + [k for k in s if k not in STEP_KEYS and k not in OPTIONAL]:
            if k not in s:
                continue
            v = s[k]
            if k in ("inputs", "todo") and v:
                inner = ",\n".join(f"    {j(x)}" for x in v)
                lines.append(f'   {j(k)}: [\n{inner}\n   ]')
            else:
                lines.append(f'   {j(k)}: {j(v)}')
        rows.append("  {\n" + ",\n".join(lines) + "\n  }")
    return "{\n" + ",\n".join(head) + ',\n "steps": [\n' + ",\n".join(rows) + "\n ]\n}\n"


def write(doc, dry):
    new = copy.deepcopy(doc)
    unb = derive_unblocks(new["steps"])
    changed = []
    for s in new["steps"]:
        if s.get("unblocks") != unb[s["id"]]:
            changed.append(f"{s['id']}: unblocks {s.get('unblocks')} → {unb[s['id']]}")
        s["unblocks"] = unb[s["id"]]
    text = fmt(new)
    old = STEPS.read_text()
    if dry:
        print("\n".join(changed) or "unblocks already current", "·", "format changes" if text != old else "format current")
        return doc
    if text != old:
        STEPS.write_text(text)
    print(f"wrote {STEPS.relative_to(ROOT)} ({len(changed)} unblocks changed)")
    return new


def lock_chat(holder):
    """'<name> · <chat name> · <date>' → the chat name (exact match, like the app)."""
    c = re.sub(r"^[^·]*· ", "", holder or "")
    return re.sub(r" · \d{1,2} [A-Z][a-z]{2} \d{4}.*$", "", c).strip()


def startable(s, by, lock_holder):
    """Same rule as trCanStart() in the app: what stops a step starting now."""
    why = [f"{n} ({by[n].get('status')})" for n in s.get("needs", []) if n in by and by[n].get("status") not in MET]
    why += [f"your answer {x.get('id')}" for x in s.get("inputs", []) if isinstance(x, dict) and x.get("blocks") and x.get("status") == "open"]
    if s.get("lock") and lock_holder and lock_chat(lock_holder) != s.get("chat"):
        why.append("the build lock")
    return why


def preview(doc, lock):
    steps = [s for s in doc["steps"] if s["type"] != "Idea"]
    by = {s["id"]: s for s in doc["steps"]}
    col = {"Now": [], "Ready": [], "Blocked": [], "Done": []}
    for s in steps:
        st = s["status"]
        if st in ("in progress", "gates", "owner check"):
            col["Now"].append(s)
        elif st == "done":
            col["Done"].append(s)
        elif st in ("ready", "planned") and not startable(s, by, lock[0]):
            col["Ready"].append(s)
        elif st in ("ready", "planned", "idea", "proposed"):
            col["Blocked"].append(s)
    for k, v in col.items():
        print(f"{k} ({len(v)}): " + ", ".join(f"{s['id']}" + (f" [{s['status']}]" if k == "Now" else "") for s in v))
    ins = sorted([(x["asked"], x["id"], x["ask"]) for s in doc["steps"] for x in s["inputs"] if x["status"] == "open"])
    print(f"Your inputs ({len(ins)}, oldest first):")
    for a, i, t in ins:
        print(f"  {a} {i}: {t[:90]}")
    print("Lock:", lock[0] or "free")


def selftest(refs):
    """Each rule must fire on a small known-bad file (and stay quiet on a good one)."""
    good = {"owner": "Aaditya", "collaborator": "Professor", "steps": [
        {"id": "A0", "title": "a", "type": "Build", "chat": "Bio · Build · A0", "status": "done", "needs": [], "unblocks": ["V1"], "lock": True,
         "gates": {"G-Eng": "pass"}, "check": {"id": "T2", "state": "pass"}, "decisions": ["D-001"], "prompt": None, "log": "", "todo": [], "inputs": [],
         "runs": [{"chat": "Bio · Build · A0", "by": "Aaditya", "start": "2026-11-18", "end": "2026-11-18", "outcome": "done"}]},
        {"id": "V1", "title": "b", "type": "Build", "chat": "Bio · Build · V1", "status": "ready", "needs": ["A0"], "unblocks": [], "lock": True,
         "gates": {}, "check": None, "decisions": [], "prompt": None, "log": "", "todo": [],
         "inputs": [{"id": "V1.q1", "kind": "ask", "ask": "x", "asked_in": "Bio · X", "asked": "2026-11-19", "answer": None, "status": "open", "d": None}]}]}
    cases = [
        ("good file", lambda d: d, None),
        ("unknown need", lambda d: d["steps"][1]["needs"].append("ZZ9"), "needs unknown step"),
        ("unknown D-id", lambda d: d["steps"][0]["decisions"].append("D-999"), "not in claude/DECISIONS.md"),
        ("unknown T-id", lambda d: d["steps"][0].__setitem__("check", {"id": "T99", "state": "pass"}), "not in build/owner-test-checklist.md"),
        ("unknown gate", lambda d: d["steps"][0]["gates"].__setitem__("G-Fun", "pass"), "unknown gate"),
        ("unknown prompt", lambda d: d["steps"][0].__setitem__("prompt", "Nope"), "ready prompt"),
        ("loop", lambda d: (d["steps"][0]["needs"].append("V1"), d["steps"][1].__setitem__("unblocks", ["A0"])), "dependency loop"),
        ("ready, unmet", lambda d: d["steps"][0].__setitem__("status", "planned"), "needs not met"),
        ("in progress, unmet", lambda d: (d["steps"][0].__setitem__("status", "gates"), d["steps"][1].__setitem__("status", "in progress")), "needs not met"),
        ("done, gate open", lambda d: d["steps"][0]["gates"].__setitem__("G-Eng", "open"), "done with open gates"),
        ("done, check open", lambda d: d["steps"][0].__setitem__("check", {"id": "T2", "state": "open"}), "done with owner check"),
        ("blocking input", lambda d: d["steps"][1]["inputs"][0].__setitem__("blocks", True), "blocking owner input"),
        ("unblocks stale", lambda d: d["steps"][0].__setitem__("unblocks", []), "`unblocks` is derived"),
        ("bad status", lambda d: d["steps"][1].__setitem__("status", "doing"), "status `doing`"),
        ("bad input id", lambda d: d["steps"][1]["inputs"][0].__setitem__("id", "A0.q1"), "input id must be"),
        ("proposed w/o by", lambda d: d["steps"][1].__setitem__("status", "proposed"), "needs `proposed_by`"),
        ("owner proposes", lambda d: d["steps"][1].update(proposed_by="Aaditya", proposed_status="done", proposed_on="2026-11-19"), "owner sets status directly"),
        ("collab proposal = warning", lambda d: d["steps"][1].update(proposed_by="Professor", proposed_status="in progress", proposed_on="2026-11-19"), "W:owner to confirm"),
        ("old lock = warning", "LOCK", "W:ask the holder"),
    ]
    cases += [
        ("uses unknown", lambda d: d["steps"][1].__setitem__("uses", ["laser"]), "uses `laser`"),
        ("est bad", lambda d: d["steps"][1].__setitem__("est", {"chats": -1}), "`est` chats"),
        ("prof blocks", lambda d: d["steps"][1]["inputs"][0].update({"for": "prof", "blocks": True}), "the professor never blocks"),
        ("needs prof-only step", lambda d: (d["steps"][0].__setitem__("uses", ["prof"]),), "professor-only step"),
        ("consumes no producer", lambda d: d["steps"][1].__setitem__("consumes", ["dossier-x"]), "no step produces it"),
        ("consumes not needed", lambda d: (d["steps"].append(dict(copy.deepcopy(d["steps"][0]), id="B2", unblocks=[], produces=["out-b"], check=None, gates={}, decisions=[])), d["steps"][1].__setitem__("consumes", ["out-b"])), "does not need it"),
        ("run bad date", lambda d: d["steps"][0].__setitem__("runs", [{"chat": "Bio · Build · A0", "by": "Aaditya", "start": "19/11", "outcome": "done"}]), "must be YYYY-MM-DD"),
        ("run bad outcome", lambda d: d["steps"][0].__setitem__("runs", [{"chat": "Bio · Build · A0", "by": "Aaditya", "start": "2026-11-19", "outcome": "meh"}]), "outcome `meh`"),
        ("two open runs on the lock", lambda d: (d["steps"][1].__setitem__("runs", [{"chat": "Bio · Build · V1", "by": "Aaditya", "start": "2026-11-19", "outcome": "partial"}]), d["steps"].append(dict(copy.deepcopy(d["steps"][1]), id="B3", inputs=[], unblocks=[]))), "open run on `lock`"),
        ("queue unknown", lambda d: d.__setitem__("queue", ["ZZ9"]), "queue: unknown step"),
        ("calendar bad", lambda d: d.__setitem__("calendar", {"day_min": [60, 60]}), "day_min must be 7"),
        ("calendar all zero = warning", lambda d: d.__setitem__("calendar", {"day_min": [0] * 7}), "W:nothing gets a date"),
        ("two producers", lambda d: (d["steps"][0].__setitem__("produces", ["x"]), d["steps"][1].__setitem__("produces", ["x"])), "also produced by"),
        ("input for bad", lambda d: d["steps"][1]["inputs"][0].__setitem__("for", "boss"), "`for` must be"),
        ("run unknown field", lambda d: d["steps"][0]["runs"][0].__setitem__("mood", "ok"), "unknown field `mood`"),
        ("run bad chat", lambda d: d["steps"][0]["runs"][0].__setitem__("chat", "my chat"), "chat must be"),
        ("run ends first", lambda d: d["steps"][0]["runs"][0].update(start="2026-11-19", end="2026-11-18"), "ends before it starts"),
        ("started, no runs = warning", lambda d: d["steps"][0].pop("runs"), "W:no `runs`"),
    ]
    ok = 0
    for name, mut, want in cases:
        d = copy.deepcopy(good)
        lock = (None, None)
        if mut == "LOCK":
            lock = ("Professor · Bio · Build · X · 1 Nov 2026, 10:00 IST", dt.datetime(2026, 11, 1, 10, tzinfo=dt.timezone.utc))
        else:
            mut(d)
        E, W = check(d, refs, lock=lock, now=dt.datetime(2026, 11, 19, tzinfo=dt.timezone.utc))
        if want is None:
            hit = not E and not W
        elif want.startswith("W:"):
            hit = any(want[2:] in w for w in W) and not E
        else:
            hit = any(want in x for x in E)
        ok += hit
        print(("PASS " if hit else "FAIL ") + name + ("" if hit else f"  E={E} W={W}"))
    # W2: the scheduler on a known file gives the known plan, and the app's trPlan gives the same (node)
    n = len(cases)
    fx = json.loads((ROOT / "tools" / "tracker" / "plan-fixture.json").read_text())
    got = plan(fx["doc"], fx["today"])
    for k, v in fx["expect"].items():
        n += 1
        hit = got.get(k) == v
        ok += hit
        print(("PASS " if hit else "FAIL ") + f"plan fixture: {k}" + ("" if hit else f"  got {json.dumps(got.get(k), ensure_ascii=False)}"))
    for name, d, t in (("plan parity (fixture)", fx["doc"], fx["today"]), ("plan parity (steps.json)", json.loads(STEPS.read_text()), fx["today"])):
        n += 1
        E2, W2 = plan_parity(d, t)
        hit = not E2
        ok += hit
        print(("PASS " if hit else "FAIL ") + name + (f"  {W2[0]}" if W2 else "") + ("" if hit else f"  {E2}"))
    print(f"selftest {ok}/{n}")
    return ok == n


def main():
    global DBG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="re-derive `unblocks` and rewrite in canonical format")
    ap.add_argument("--dry-run", action="store_true", help="with --write: show changes, write nothing")
    ap.add_argument("--only", help="check one step id")
    ap.add_argument("--preview", action="store_true", help="quick text board + your inputs")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--strict", action="store_true", help="warnings fail too")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true", help="print {errors, warnings} as JSON (with --next: the plan as JSON)")
    ap.add_argument("--next", action="store_true", help="W2: print the schedule (rows, critical path, ranked inputs); with --write also STATUS § Next auto block")
    ap.add_argument("--today", help="W2: plan from this date (YYYY-MM-DD, default today IST)")
    a = ap.parse_args()
    DBG = a.debug
    refs = load_refs()
    if a.selftest:
        return 0 if selftest(refs) else 1
    try:
        doc = json.loads(STEPS.read_text())
    except (OSError, ValueError) as ex:
        print(f"FAIL: cannot read {STEPS.relative_to(ROOT)}: {ex}")
        return 1
    if a.next:
        lock = read_lock()
        E, W = check(doc, refs, None, lock)
        E += parity()
        if E:
            print("FAIL: fix these first (check.py):\n" + "\n".join("ERROR " + e for e in E))
            return 1
        today = a.today or ist_today()
        P = plan(doc, today)
        if DBG:
            print(json.dumps(P, ensure_ascii=False, indent=1))
        txt = next_text(doc, P, lock)
        print(json.dumps(P, ensure_ascii=False) if a.json else txt)
        return write_next(txt, a.dry_run) if a.write else 0
    if a.write:
        pre = [e for e in check(doc, refs)[0] if "`unblocks` is derived" not in e and "not in build/" not in e and "not in claude/" not in e]
        if any(k in e for e in pre for k in ("field `", "must be", "id used twice", "bad step id")):
            print("FAIL: fix these before --write:\n" + "\n".join("ERROR " + e for e in pre))
            return 1
        doc = write(doc, a.dry_run)
    if a.only and a.only not in {s.get("id") for s in doc.get("steps", [])}:
        print(f"FAIL: no step `{a.only}`")
        return 1
    lock = read_lock()
    E, W = check(doc, refs, a.only, lock)
    E += parity()
    if a.preview and not E:
        preview(doc, lock)
    if a.json:
        print(json.dumps({"errors": E, "warnings": W}, ensure_ascii=False, indent=1))
    else:
        for x in E:
            print("ERROR", x)
        for x in W:
            print("WARN ", x)
        n = len(doc.get("steps", []))
        print(f"{'FAIL' if E or (a.strict and W) else 'PASS'}: {n} steps · {len(E)} errors · {len(W)} warnings")
    return 1 if E or (a.strict and W) else 0


if __name__ == "__main__":
    sys.exit(main())
