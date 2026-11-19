#!/usr/bin/env python3
"""Biology Studio — progress map check (W1, D-040). Owner doc: studio-docs/build/steps.json (format: tools/tracker/README.md).

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
  python tools/tracker/check.py --selftest      # each rule fires on a known-bad file
EDIT: vocabularies below (keep src/js/17-tracker.js TR_RULES in step — the in-app test compares them).
"""
import argparse, copy, datetime as dt, json, re, sys
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
OPTIONAL = ["size", "proposed_by", "proposed_status", "proposed_on", "note"]
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
    return E, W


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
         "gates": {"G-Eng": "pass"}, "check": {"id": "T2", "state": "pass"}, "decisions": ["D-001"], "prompt": None, "log": "", "todo": [], "inputs": []},
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
    print(f"selftest {ok}/{len(cases)}")
    return ok == len(cases)


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
    ap.add_argument("--json", action="store_true", help="print {errors, warnings} as JSON")
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
