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
  approval, no step ... (U1, D-076) a DECISIONS row dated from APPROVAL_SINCE that records an owner approval/pick, while no step in
                        steps.json names its D-id — the approved work has no step to carry it (warning; the 19 Nov depth canvas case)
  draft id clash ...... (U1, D-076) a committed draft (studio-docs/**/*-draft*.md) proposes a D-id that DECISIONS already uses for
                        another decision (its row does not name the draft), or two drafts propose the same id (error — renumber the draft)
  run surface ......... (W3, D-080) `surfaces` (top level) = where chats run (Code · Cowork) + rules, first match wins; each step's
                        `run {on, why}` — bad shape / unknown surface = error; no `run`, no rule, or an `on` the rules don't allow
                        (without `override`) = warning. --write fills a missing `run` from the rules; --next tags each step [Code]/[Cowork]
                        W3F (D-081): `hard` rules (GPU, tests, > 15 files, lock) make Code required — Cowork is an error; hard + a `split`
                        rule (connectors, artifacts, owner) → split, which needs run.handoff (error); `warn` = allowed, warned (Professor on Code)
  title token ......... (TTG) W-title-token: a `title`/`chat` word longer than TITLE_TOKEN_MAX (12) or a joined word (letters glued by
                        / . _ + \\ : @ = or a camelCase hump) may split mid-word on #progress=plan/board at 640×360 with 125–200 % text;
                        GLOSSARY terms (bold or backticked) and numbers are exempt (warning — approximates layout-check midword, §7);
                        --todo-tokens also checks to-do lines (step page only), one warning per step
Warnings never fail the run unless --strict. Exit 1 on any error.

Run from the repo root:
  python tools/tracker/check.py                 # check (CI)
  python tools/tracker/check.py --write         # re-derive `unblocks` + canonical formatting, then check
  python tools/tracker/check.py --write --dry-run   # show what --write would change, write nothing
  python tools/tracker/check.py --only C1       # one step (loops are still checked across all)
  python tools/tracker/check.py --preview       # quick text board: Now · Ready · Blocked · Done + your inputs
  python tools/tracker/check.py --debug         # print every rule as it runs
  python tools/tracker/check.py --todo-tokens   # also warn on to-do words that may break mid-word (one warning per step)
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
OPTIONAL = ["size", "proposed_by", "proposed_status", "proposed_on", "note", "uses", "est", "produces", "consumes", "runs", "improves", "run"]
LOCK_MAX_H = 24
# EDIT: approval rule (D-076) — rows dated on/after this day are checked; words that mark an owner approval in a DECISIONS row
APPROVAL_SINCE = dt.date(2026, 11, 22)
APPROVAL_RE = re.compile(r"approv|owner picks?\b|owner kept|confirmed by owner|owner OK|owner answers", re.I)
DRAFT_ID_RE = re.compile(r"(?:Proposed decision|Decision)s?:\s*\*\*(D-\d{3})\*\*")
MONTHS = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
ID_RE = re.compile(r"^(?:[A-Z][A-Z0-9]*|[A-Z][0-9]+[a-z]?|X1\.\d\d|IB\d\d|GATE)$")
# EDIT: W-title-token (TTG) — a step's `title`/`chat` word that would split mid-word on #progress=plan / #progress=board at 640×360
# with 125–200 % text. This only APPROXIMATES layout-check's midword rule (src/js/90-layout-audit.js §7), which measures the real
# line boxes in the browser and can't be reused from Python: here a word is too long, or two words glued with no break point.
TITLE_TOKEN_MAX = 12   # EDIT: longest plain word that still fits a Plan/Board cell at 640×360 and 200 % text (owner rule; the 13–14-letter X1 chapter words still fit today with CI green — reported, not retitled)
TOKEN_SPLIT_RE = re.compile(r"[\s\-\u2010\u2013\u2014]+")   # the browser may break at whitespace and at - ‐ – —
TOKEN_STRIP = "()[]{}<>\"'`‘’“”«»,;:!?.…*·→←↔"
JOINED_RE = re.compile(r"[^\W\d_]+[/._+\\:@＠=]+(?=[^\W\d_])|[a-z][A-Z]")   # ≥ 2 letter-runs glued by / . _ + \ : @ ＠ =, or a camelCase hump
NUMBER_RE = re.compile(r"^v?\d+(?:[.,:/x×]\d+)*[a-z]?%?$", re.I)          # 1abe465 is not a number but is short; 640x360, v21, 1.5, 22:30
DBG = False


def dbg(*a):
    if DBG:
        print("[tracker]", *a)


def load_refs():
    """Ids that exist in the owner docs (D-ids, T-ids, ready-prompt keys)."""
    dec = set(re.findall(r"^\| (D-\d{3}) \|", (DOCS / "claude" / "DECISIONS.md").read_text(encoding="utf-8"), re.M))
    chk = set(re.findall(r"^## (T\d+[a-z]?)\b", (DOCS / "build" / "owner-test-checklist.md").read_text(encoding="utf-8"), re.M))
    chk |= set(re.findall(r"\*\*(T\d+[a-z]) —", (DOCS / "build" / "owner-test-checklist.md").read_text(encoding="utf-8")))
    prompts = set(re.findall(r"^\*\*Ready prompt — (.+?)\*\*", (DOCS / "build" / "master-plan.md").read_text(encoding="utf-8"), re.M))
    rows = {}
    for m in re.finditer(r"^\| (D-\d{3}) \| ([^|]*)\|(.*)$", (DOCS / "claude" / "DECISIONS.md").read_text(encoding="utf-8"), re.M):
        rows[m.group(1)] = (m.group(2).strip(), m.group(3))
    drafts = []
    for p in sorted(DOCS.rglob("*-draft*.md")):
        head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:12])
        drafts.append((p.name, sorted(set(DRAFT_ID_RE.findall(head)))))
    gp = DOCS / "claude" / "GLOSSARY.md"   # optional: the Dispatcher's selftest clone (tools/dispatch/desk.py) has no GLOSSARY
    gloss_txt = gp.read_text(encoding="utf-8") if gp.exists() else ""
    gloss = {g.strip().strip(TOKEN_STRIP).strip().lower() for g in re.findall(r"\*\*([^*\n]+)\*\*", gloss_txt) + re.findall(r"`([^`\n]+)`", gloss_txt)}
    gloss.discard("")
    dbg(f"refs: {len(dec)} D-ids, T-ids {sorted(chk)}, {len(prompts)} prompts, drafts {drafts}, {len(gloss)} glossary terms")
    return {"dec": dec, "chk": chk, "prompts": prompts, "dec_rows": rows, "drafts": drafts, "gloss": gloss}


def row_date(txt):
    m = re.match(r"(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})", txt or "")
    return dt.date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1))) if m and m.group(2) in MONTHS else None


def check_refs(doc, refs):
    """D-076: an owner approval with no step (warning); a draft's proposed D-id that clashes (error)."""
    E, W = [], []
    named = set()
    for s in doc.get("steps", []):
        named |= set(re.findall(r"D-\d{3}", json.dumps(s, ensure_ascii=False)))
    for d, (when, txt) in sorted(refs.get("dec_rows", {}).items()):
        day = row_date(when)
        if day and day >= APPROVAL_SINCE and APPROVAL_RE.search(txt) and d not in named:
            W.append(f"{d}: owner approval with no step — add the step that carries it out to build/steps.json (or name {d} on it)")
    seen = {}
    for name, ids in refs.get("drafts", []):
        for d in ids:
            if d in seen:
                E.append(f"draft {name}: proposes {d}, also proposed by {seen[d]} — renumber one (next free id after DECISIONS)")
            seen.setdefault(d, name)
            row = refs.get("dec_rows", {}).get(d)
            if row and name not in row[1]:
                E.append(f"draft {name}: proposes {d}, but DECISIONS {d} is another decision — renumber the draft to the next free id")
    return E, W


def title_tokens(text, gloss):
    """W-title-token: the words of `text` that may split mid-word on the progress Plan/Board (see TITLE_TOKEN_MAX)."""
    out = []
    for raw in TOKEN_SPLIT_RE.split(str(text or "")):
        tok = raw.strip(TOKEN_STRIP)
        if not tok or tok.lower() in gloss or NUMBER_RE.match(tok):
            continue
        if len(tok) > TITLE_TOKEN_MAX:
            out.append(f"`{tok}` ({len(tok)} chars > {TITLE_TOKEN_MAX})")
        elif JOINED_RE.search(tok):
            out.append(f"`{tok}` (joined word)")
    return list(dict.fromkeys(out))


def check_titles(doc, refs, todo=False):
    """TTG: warn on title/chat words that may break mid-word on #progress=plan/board; `todo` (--todo-tokens) also checks to-do lines,
    folded into one warning per step (they only show on the step page, ul.tr-todo, which the midword audit doesn't check)."""
    W, gloss = [], refs.get("gloss", set())
    for s in doc.get("steps", []):
        sid = s.get("id", "?")
        for k in ("title", "chat"):
            for x in title_tokens(s.get(k), gloss):
                W.append(f"{sid}: W-title-token {k} word {x} may break mid-word on the progress Plan/Board (640×360, 125–200 % text) — use plain words")
        todo_lines = s.get("todo") if isinstance(s.get("todo"), list) else []   # a non-list todo is already an error in check()
        if todo:
            hits = list(dict.fromkeys(x for line in todo_lines if isinstance(line, str) for x in title_tokens(line, gloss)))
            if hits:
                W.append(f"{sid}: W-title-token {len(hits)} to-do word(s) may break mid-word on the step page: {', '.join(hits)}")
    return W


def read_lock():
    """STATUS § Lock line → (holder text or None, datetime IST or None)."""
    try:
        t = (DOCS / "claude" / "STATUS.md").read_text(encoding="utf-8")
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
    js = (ROOT / "src" / "js" / "17-tracker.js").read_text(encoding="utf-8")
    m = re.search(r"const TR_RULES=(\{.*?\});", js, re.S)
    if not m:
        return ["app: TR_RULES not found in src/js/17-tracker.js"]
    r = json.loads(m.group(1))
    want = {"statuses": STATUSES, "types": TYPES, "gates": GATES, "met": sorted(MET, key=STATUSES.index), "started": sorted(STARTED, key=STATUSES.index)}
    return [f"app: TR_RULES.{k} {r.get(k)} ≠ check.py {v}" for k, v in want.items() if r.get(k) != v]


def check(doc, refs, only=None, lock=(None, None), now=None, todo_tokens=False):
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
    E3, W3 = check_refs(doc, refs)
    E4, W4 = check_surface(doc)
    E2, W2 = E2 + E3 + E4, W2 + W3 + W4 + check_titles(doc, refs, todo_tokens)
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
    m = re.search(r"const PLAN_DEF=(\{.*?\});", js.read_text(encoding="utf-8"), re.S)
    if not m or json.loads(m.group(1)) != PLAN_DEF:
        return ["app: PLAN_DEF in src/js/17-plan.js ≠ check.py PLAN_DEF"], []
    src = f"const {{trPlan}}=require({json.dumps(str(js))});const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(trPlan(d.doc,d.today)));"
    r = subprocess.run(["node", "-e", src], input=json.dumps({"doc": doc, "today": today}), capture_output=True, text=True, encoding="utf-8", timeout=60)
    if r.returncode:
        return [f"app: trPlan failed in node: {r.stderr.strip()[:300]}"], []
    a, b = json.loads(r.stdout), plan(doc, today)
    if a != b:
        diff = [k for k in b if a.get(k) != b.get(k)]
        return [f"app: trPlan ≠ check.py plan() for {today} in {diff}"], []
    return [], []


# ---- W3 run surface (D-080) — mirror of trSurface() in src/js/17-plan.js; --selftest compares both (node) ----
SURF_DEF = {"on": ["Code", "Cowork"], "rules": []}
SURF_IF = ("lock", "uses", "type", "trait", "files_over")
SURF_RULE = ("if", "on", "why", "warn", "hard", "split")   # W3F: warn = allowed but warned · hard = Code is required · split = with a hard rule → split
RUN_KEYS = ("on", "why", "override", "traits", "files", "handoff")   # W3F: traits (surfaces.traits) · files = how many it touches · handoff = split note


def surf_cfg(doc):
    c = (doc or {}).get("surfaces")
    return c if isinstance(c, dict) else SURF_DEF


def surf_match(rule_if, s):
    """Every key in the rule's `if` must hold: lock (bool) · uses ("prof" = professor-only step, else in uses) · type (name or list)
    · trait (in run.traits) · files_over (run.files > n)."""
    if not isinstance(rule_if, dict):   # a malformed rule never matches (check_surface reports it)
        return False
    u = s.get("uses") or []
    run = s.get("run") if isinstance(s.get("run"), dict) else {}
    tr = run.get("traits") if isinstance(run.get("traits"), list) else []
    f = run.get("files")
    f = f if isinstance(f, (int, float)) and not isinstance(f, bool) else None
    for k, v in rule_if.items():
        if k == "lock" and bool(s.get("lock")) != bool(v):
            return False
        if k == "uses" and not ((u == ["prof"]) if v == "prof" else (v in u)):
            return False
        if k == "type" and s.get("type") not in (v if isinstance(v, list) else [v]):
            return False
        if k == "trait" and v not in tr:
            return False
        if k == "files_over" and not (f is not None and isinstance(v, (int, float)) and not isinstance(v, bool) and f > v):
            return False
    return True


def surface(doc, s):
    """Where a step's chat runs: {on, allowed (what the first matching rule allows), why, rule (index or None), fit, override, set,
    hard (a matching rule says Code is required), warn (on is allowed, but its rule warns on it)}.
    W3F: a hard rule and a `split` rule both matching → allowed ["split"] (a Code part + a Cowork part, joined by run.handoff)."""
    rule, ri, hard, spl = None, None, None, None
    cfg = surf_cfg(doc)
    rules = cfg.get("rules")
    for i, r in enumerate(rules if isinstance(rules, list) else []):
        if isinstance(r, dict) and surf_match(r.get("if"), s):
            if rule is None:
                rule, ri = r, i
            if r.get("hard") is True and hard is None:
                hard = (r, i)
            if r.get("split") is True and spl is None:
                spl = r
    names = cfg.get("on") if isinstance(cfg.get("on"), list) else []
    if hard and spl and "split" in names:
        rule, ri = {"on": ["split"], "why": f"{hard[0].get('why')} + {spl.get('why')}"}, hard[1]
    elif hard:   # G-Eng W3F: Code is required — the hard rule wins over an earlier match (a Professor step that runs tests stays Code, unwarned)
        rule, ri = hard
    allowed = [] if rule is None else (rule.get("on") if isinstance(rule.get("on"), list) else [rule.get("on")])
    run = s.get("run") if isinstance(s.get("run"), dict) else None
    on = run.get("on") if run else (allowed[0] if allowed else None)
    why = run.get("why") if run and run.get("why") else (rule.get("why") if rule else "")
    warn = rule.get("warn") if rule and isinstance(rule.get("warn"), list) else []
    return {"on": on, "allowed": allowed, "why": why, "rule": ri, "fit": on in allowed, "override": bool(run and run.get("override")),
            "set": run is not None, "hard": hard is not None, "warn": on in warn, "rule_why": (rule.get("why") if rule else None)}


def surf_fill(s, doc):
    """--write: a step with no `run` gets the first surface its rule allows, with the rule's why."""
    if "run" not in s and s.get("type") != "Idea":
        x = surface(doc, s)
        if x["on"]:
            s["run"] = {"on": x["on"], "why": x["why"]}
            return True
    return False


def check_surface(doc):
    E, W = [], []
    cfg = doc.get("surfaces")
    names = SURF_DEF["on"]
    if cfg is not None:
        if not isinstance(cfg, dict):
            return ["surfaces: must be an object"], []
        for k in cfg:
            if k not in ("on", "rules", "note", "traits"):
                E.append(f"surfaces: unknown key `{k}`")
        names = cfg.get("on")
        if not (isinstance(names, list) and names and all(isinstance(n, str) and n for n in names)):
            E.append("surfaces: `on` must be a list of surface names")
            names = SURF_DEF["on"]
        traits = cfg.get("traits", [])
        if not (isinstance(traits, list) and all(isinstance(x, str) and x for x in traits)):
            E.append("surfaces: `traits` must be a list of names")
            traits = []
        rules = cfg.get("rules")
        if not isinstance(rules, list):
            E.append("surfaces: `rules` must be a list")
            rules = []
        for i, r in enumerate(rules):
            if not isinstance(r, dict):
                E.append(f"surfaces: rule {i + 1}: must be an object")
                continue
            for k in r:
                if k not in SURF_RULE:
                    E.append(f"surfaces: rule {i + 1}: unknown key `{k}`")
            for k in ("hard", "split"):
                if k in r and not isinstance(r[k], bool):
                    E.append(f"surfaces: rule {i + 1}: `{k}` must be true or false")
            if "warn" in r and not (isinstance(r["warn"], list) and all(w in names and w in (r.get("on") if isinstance(r.get("on"), list) else [r.get("on")]) for w in r["warn"])):
                E.append(f"surfaces: rule {i + 1}: `warn` must be a list of surfaces this rule allows (its `on`)")
            if r.get("hard") is True and r.get("on") != "Code":
                E.append(f"surfaces: rule {i + 1}: a hard rule must say `on` Code")
            if isinstance(r.get("if"), dict) and "trait" in r["if"] and r["if"]["trait"] not in traits:
                E.append(f"surfaces: rule {i + 1}: trait `{r['if']['trait']}` not in surfaces.traits")
            if not isinstance(r.get("if"), dict) or any(k not in SURF_IF for k in r.get("if") or {}):
                E.append(f"surfaces: rule {i + 1}: `if` must be an object with keys from {list(SURF_IF)}")
            on = r.get("on") if isinstance(r.get("on"), list) else [r.get("on")]
            if not on or any(o not in names for o in on):
                E.append(f"surfaces: rule {i + 1}: `on` {r.get('on')} must be one of {names} (or a list of them)")
            if not (isinstance(r.get("why"), str) and r["why"].strip()):
                E.append(f"surfaces: rule {i + 1}: `why` missing")
    traits = cfg.get("traits") if isinstance(cfg, dict) and isinstance(cfg.get("traits"), list) else []
    for s in doc.get("steps", []):
        sid = s.get("id", "?")
        if s.get("type") == "Idea":
            continue
        run = s.get("run")
        if run is None:
            W.append(f"{sid}: no `run` {{on, why}} — check.py --write fills it from the surface rules (W3)")
            continue
        if not isinstance(run, dict):
            E.append(f"{sid}: `run` must be {{on, why}}")
            continue
        for k in run:
            if k not in RUN_KEYS:
                E.append(f"{sid}: run: unknown key `{k}`")
        if "traits" in run and not (isinstance(run["traits"], list) and all(x in traits for x in run["traits"])):
            E.append(f"{sid}: run.traits must be a list from surfaces.traits {traits}")
        if "files" in run and not (isinstance(run["files"], int) and not isinstance(run["files"], bool) and run["files"] >= 0):
            E.append(f"{sid}: run.files must be a whole number ≥ 0")
        if run.get("on") not in names:
            E.append(f"{sid}: run.on `{run.get('on')}` not one of {names}")
            continue
        if not (isinstance(run.get("why"), str) and run["why"].strip()):
            E.append(f"{sid}: run.why missing — say why it runs there")
        if "override" in run and not isinstance(run["override"], bool):
            E.append(f"{sid}: run.override must be true or false")
        if run.get("on") == "split" and not (isinstance(run.get("handoff"), str) and run["handoff"].strip()):
            E.append(f"{sid}: run.on split needs run.handoff — what the Code part hands the Cowork part (a handoff note)")
        if cfg is None:
            continue
        x = surface(doc, s)
        if x["hard"] and run.get("on") == "Cowork":
            E.append(f"{sid}: runs on Cowork but must run in Code ({x['rule_why']}) — Code is hard for the GPU, tests, > 15 files and the build lock; "
                     "override can't change it")
            continue
        if x["warn"]:
            W.append(f"{sid}: runs on {run['on']} — allowed, but the default is {x['allowed'][0]} ({x['rule_why']})")
            continue
        if x["rule"] is None:
            W.append(f"{sid}: no surface rule matches (type {s.get('type')}) — add one to `surfaces.rules`")
        elif not x["fit"] and not x["override"]:
            W.append(f"{sid}: runs on {run['on']} but the surface rules say {' or '.join(x['allowed'])} "
                     f"({cfg['rules'][x['rule']].get('why')}) — change run.on, or set run.override true and say why")
    return E, W


def surface_parity(doc):
    """Run trSurface() in node on every step of `doc`; differences are errors. No node → a warning (CI has node)."""
    js = ROOT / "src" / "js" / "17-plan.js"
    if not shutil.which("node"):
        return [], ["surface parity skipped: node not found"]
    src = (f"const {{trSurface}}=require({json.dumps(str(js))});const d=JSON.parse(require('fs').readFileSync(0,'utf8'));"
           "process.stdout.write(JSON.stringify(d.steps.map(s=>trSurface(d,s))));")
    r = subprocess.run(["node", "-e", src], input=json.dumps(doc), capture_output=True, text=True, encoding="utf-8", timeout=60)
    if r.returncode:
        return [f"app: trSurface failed in node: {r.stderr.strip()[:300]}"], []
    a, b = json.loads(r.stdout), [surface(doc, s) for s in doc["steps"]]
    bad = [s.get("id") for s, x, y in zip(doc["steps"], a, b) if x != y]
    return ([f"app: trSurface ≠ check.py surface() for {bad[:5]}"] if bad else []), []


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
    own = (surface(doc, {"type": "Review", "run": {"traits": ["owner"]}})["allowed"] or [None])[0]   # W3F: owner checks run where the owner rule says
    on = lambda c: surface(doc, by[c["step"]])["on"] if c["kind"] == "step" and c["step"] in by else (own if c["kind"] == "check" else None)
    tag = lambda c: f" [{on(c)}]" if on(c) else ""
    cell = lambda c: f"{c['step'] if c['kind'] == 'step' else c['id']}{tag(c)} ~{fmt_day(c['end'])}" + (" (slipped)" if c["slipped"] else "")
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
    nx = [c for r in ("lock", "gpu", "research") for c in P["rows"][r]["next"] if c["kind"] == "step" and c["step"] in by]
    if nx:
        hand = lambda s: f"; handoff: {s['run']['handoff']}" if isinstance(s.get("run"), dict) and s["run"].get("on") == "split" and s["run"].get("handoff") else ""
        out.append("- Run in: " + " · ".join(f"{c['step']} → {on(c)} ({surface(doc, by[c['step']])['why']}{hand(by[c['step']])})" for c in nx))
    if doc.get("surfaces"):
        mis = []
        for s in doc["steps"]:
            if s.get("type") == "Idea" or s.get("status") in ("done", "parked") or not isinstance(s.get("run"), dict):
                continue
            x = surface(doc, s)
            if x["hard"] and s["run"].get("on") == "Cowork":
                mis.append(f"{s['id']} (error: must run in Code)")
            elif x["rule"] is not None and not x["fit"] and not x["override"]:
                mis.append(f"{s['id']} (warning: rules say {' or '.join(map(str, x['allowed']))})")
            elif x["warn"]:
                mis.append(f"{s['id']} (allowed, default {x['allowed'][0]})")
        if mis:
            out.append("- Surface check: " + ", ".join(mis[:6]) + " — run.on vs the surface rules (check.py)")
    out.append(f"- Lock: {lock[0] or 'free'}")
    return "\n".join(out)


AUTO_A, AUTO_B = "<!-- next:auto -->", "<!-- /next:auto -->"


def write_next(text, dry):
    p = DOCS / "claude" / "STATUS.md"
    t = p.read_text(encoding="utf-8")
    if AUTO_A not in t or AUTO_B not in t:
        print(f"FAIL: STATUS § Next has no {AUTO_A} … {AUTO_B} block")
        return 1
    new = re.sub(re.escape(AUTO_A) + r".*?" + re.escape(AUTO_B), lambda m: f"{AUTO_A}\n{text}\n{AUTO_B}", t, flags=re.S)
    if dry:
        print("STATUS § Next auto block:", "unchanged" if new == t else "would change")
    elif new != t:
        p.write_text(new, encoding="utf-8", newline="\n")
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
    filled = [s["id"] for s in new["steps"] if surf_fill(s, new)]
    for s in new["steps"]:
        if s.get("unblocks") != unb[s["id"]]:
            changed.append(f"{s['id']}: unblocks {s.get('unblocks')} → {unb[s['id']]}")
        s["unblocks"] = unb[s["id"]]
    text = fmt(new)
    old = STEPS.read_text(encoding="utf-8")
    if dry:
        print("\n".join(changed) or "unblocks already current", "·", "format changes" if text != old else "format current",
              *([f"· run would be filled on {len(filled)}"] if filled else []))
        return doc
    if text != old:
        STEPS.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {STEPS.relative_to(ROOT)} ({len(changed)} unblocks changed" + (f", run filled on {len(filled)}: {', '.join(filled[:8])}" if filled else "") + ")")
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
    refs = dict(refs, dec_rows={}, drafts=[])  # the D-076 rules get their own cases below
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
        ("approval, no step = warning", ("REFS", lambda r: r.update(dec_rows={"D-002": ("1 Jan 2099", " owner approved the look |")})), "W:owner approval with no step"),
        ("approval named on a step", ("REFS", lambda r: r.update(dec_rows={"D-001": ("1 Jan 2099", " owner approved |")})), None),
        ("old approval ignored", ("REFS", lambda r: r.update(dec_rows={"D-002": ("1 Jan 2020", " owner approved |")})), None),
        ("draft id clash", ("REFS", lambda r: r.update(dec_rows={"D-001": ("1 Jan 2099", " L2 lessons |")}, drafts=[("look-draft.md", ["D-001"])])), "is another decision"),
        ("draft id twice", ("REFS", lambda r: r.update(drafts=[("a-draft.md", ["D-900"]), ("b-draft.md", ["D-900"])])), "also proposed by"),
        ("draft recorded = ok", ("REFS", lambda r: r.update(dec_rows={"D-900": ("1 Jan 2020", " see build/look-draft.md |")}, drafts=[("look-draft.md", ["D-900"])])), None),
    ]
    # W3 run surface (D-080): the good file gets rules + a fitting `run` on both steps; each case breaks one rule
    SURF = {"on": ["Code", "Cowork"], "rules": [{"if": {"uses": "prof"}, "on": ["Code", "Cowork"], "why": "prof"},
                                                {"if": {"lock": True}, "on": "Code", "why": "lock"},
                                                {"if": {"type": ["Research"]}, "on": "Cowork", "why": "docs"}]}
    good["surfaces"] = SURF
    for s in good["steps"]:
        s["run"] = {"on": "Code", "why": "takes the lock"}
    cases += [
        ("surface: no run = warning", lambda d: d["steps"][1].pop("run"), "W:no `run`"),
        ("surface: unknown surface", lambda d: d["steps"][1]["run"].__setitem__("on", "Phone"), "run.on `Phone`"),
        ("surface: why missing", lambda d: d["steps"][1]["run"].__setitem__("why", ""), "run.why missing"),
        ("surface: run unknown key", lambda d: d["steps"][1]["run"].__setitem__("where", "x"), "run: unknown key `where`"),
        ("surface: run not an object", lambda d: d["steps"][1].__setitem__("run", "Code"), "`run` must be"),
        ("surface: override not bool", lambda d: d["steps"][1]["run"].__setitem__("override", "yes"), "override must be"),
        ("surface: mismatch = warning", lambda d: d["steps"][1]["run"].__setitem__("on", "Cowork"), "W:the surface rules say Code"),
        ("surface: override silences", lambda d: d["steps"][1]["run"].update(on="Cowork", override=True), None),
        ("surface: no rule = warning", lambda d: (d["steps"][1].__setitem__("lock", False)), "W:no surface rule matches"),
        ("surface: prof either = ok", lambda d: (d["steps"][1].update(lock=False, uses=["prof"]), d["steps"][1]["run"].__setitem__("on", "Cowork")), None),
        ("surface: rule bad on", lambda d: d["surfaces"]["rules"][1].__setitem__("on", "Laptop"), "rule 2: `on`"),
        ("surface: rule bad if", lambda d: d["surfaces"]["rules"][1].__setitem__("if", {"colour": "red"}), "rule 2: `if`"),
        ("surface: rule no why", lambda d: d["surfaces"]["rules"][2].pop("why"), "rule 3: `why` missing"),
        ("surface: unknown key", lambda d: d["surfaces"].__setitem__("default", "Code"), "surfaces: unknown key"),
        ("surface: bad names", lambda d: d["surfaces"].__setitem__("on", []), "`on` must be a list"),
        ("surface: not an object", lambda d: d.__setitem__("surfaces", ["Code"]), "surfaces: must be an object"),
        ("surface: rules not a list", lambda d: d["surfaces"].__setitem__("rules", "lock → Code"), "`rules` must be a list"),
        ("surface: rule not an object", lambda d: d["surfaces"]["rules"].append("Code"), "rule 4: must be an object"),
        ("surface: rule unknown key", lambda d: d["surfaces"]["rules"][1].__setitem__("when", "now"), "rule 2: unknown key `when`"),
        ("surface: rule if a list", lambda d: d["surfaces"]["rules"][1].__setitem__("if", ["lock"]), "rule 2: `if`"),
    ]
    # W3F (owner's W3 answers): Professor default Cowork + warn on Code · hard Code (GPU, tests, > 15 files, lock) · split + handoff
    def w3f(d):
        d["surfaces"] = {"on": ["Code", "Cowork", "split"], "traits": ["tests", "connectors", "artifacts", "owner"], "rules": [
            {"if": {"uses": "prof"}, "on": ["Cowork", "Code"], "warn": ["Code"], "why": "prof"},
            {"if": {"uses": "gpu"}, "on": "Code", "hard": True, "why": "gpu"},
            {"if": {"trait": "tests"}, "on": "Code", "hard": True, "why": "tests"},
            {"if": {"files_over": 15}, "on": "Code", "hard": True, "why": "files"},
            {"if": {"lock": True}, "on": "Code", "hard": True, "why": "lock"},
            {"if": {"trait": "connectors"}, "on": "Cowork", "split": True, "why": "connectors"},
            {"if": {"trait": "owner"}, "on": "Cowork", "split": True, "why": "owner"},
            {"if": {"type": ["Build", "Fix"]}, "on": "Code", "why": "tie Code"},
            {"if": {"type": ["Research", "Ideation", "Review"]}, "on": "Cowork", "why": "tie Cowork"}]}
        return d
    v1 = lambda d, **kw: d["steps"][1].update(kw)
    cases += [
        ("W3F: good file with the full rules", lambda d: w3f(d), None),
        ("W3F: professor default Cowork = ok", lambda d: (w3f(d), v1(d, lock=False, uses=["prof"], type="Review", run={"on": "Cowork", "why": "p"})), None),
        ("W3F: professor on Code = warning", lambda d: (w3f(d), v1(d, lock=False, uses=["prof"], type="Review", run={"on": "Code", "why": "p"})), "W:allowed, but the default is Cowork"),
        ("W3F: lock on Cowork = error", lambda d: (w3f(d), d["steps"][1]["run"].update(on="Cowork")), "must run in Code"),
        ("W3F: hard ignores override", lambda d: (w3f(d), d["steps"][1]["run"].update(on="Cowork", override=True)), "override can't change it"),
        ("W3F: gpu on Cowork = error", lambda d: (w3f(d), v1(d, lock=False, uses=["gpu"], run={"on": "Cowork", "why": "x"})), "must run in Code"),
        ("W3F: > 15 files on Cowork = error", lambda d: (w3f(d), v1(d, lock=False, type="Research", run={"on": "Cowork", "why": "x", "files": 16})), "must run in Code"),
        ("W3F: 15 files on Cowork = ok", lambda d: (w3f(d), v1(d, lock=False, type="Research", run={"on": "Cowork", "why": "x", "files": 15})), None),
        ("W3F: tests trait on Cowork = error", lambda d: (w3f(d), v1(d, lock=False, type="Research", run={"on": "Cowork", "why": "x", "traits": ["tests"]})), "must run in Code"),
        ("W3F: connectors = Cowork", lambda d: (w3f(d), v1(d, lock=False, type="Build", run={"on": "Cowork", "why": "x", "traits": ["connectors"]})), None),
        ("W3F: lock + connectors on Code = warning (split)", lambda d: (w3f(d), d["steps"][1]["run"].update(traits=["connectors"])), "W:the surface rules say split"),
        ("W3F: split without handoff = error", lambda d: (w3f(d), d["steps"][1]["run"].update(on="split", traits=["connectors"])), "needs run.handoff"),
        ("W3F: split with handoff = ok", lambda d: (w3f(d), d["steps"][1]["run"].update(on="split", traits=["owner"], handoff="T-check notes → Code chat")), None),
        ("W3F: tie Build → Code", lambda d: (w3f(d), v1(d, lock=False, run={"on": "Cowork", "why": "x"})), "W:the surface rules say Code"),
        ("W3F: tie Research → Cowork", lambda d: (w3f(d), v1(d, lock=False, type="Research", run={"on": "Code", "why": "x"})), "W:the surface rules say Cowork"),
        ("W3F: unknown trait", lambda d: (w3f(d), d["steps"][1]["run"].update(traits=["magic"])), "run.traits must be"),
        ("W3F: files not whole", lambda d: (w3f(d), d["steps"][1]["run"].update(files=2.5)), "run.files must be"),
        ("W3F: rule trait not listed", lambda d: (w3f(d), d["surfaces"]["rules"][2]["if"].__setitem__("trait", "magic")), "not in surfaces.traits"),
        ("W3F: hard rule not Code", lambda d: (w3f(d), d["surfaces"]["rules"][1].__setitem__("on", "Cowork")), "a hard rule must say"),
        ("W3F: warn not a list", lambda d: (w3f(d), d["surfaces"]["rules"][0].__setitem__("warn", "Code")), "`warn` must be"),
        ("W3F: split not bool", lambda d: (w3f(d), d["surfaces"]["rules"][5].__setitem__("split", "yes")), "`split` must be"),
        ("W3F: professor + tests on Code = ok (hard wins)", lambda d: (w3f(d), v1(d, lock=False, uses=["prof"], type="Review", run={"on": "Code", "why": "p", "traits": ["tests"]})), None),
        ("W3F: professor + 40 files on Cowork = error", lambda d: (w3f(d), v1(d, lock=False, uses=["prof"], type="Review", run={"on": "Cowork", "why": "p", "files": 40})), "must run in Code"),
        ("W3F: warn outside the rule's on", lambda d: (w3f(d), d["surfaces"]["rules"][1].__setitem__("warn", ["Cowork"])), "`warn` must be a list of surfaces this rule allows"),
    ]
    ok = 0
    for name, mut, want in cases:
        d = copy.deepcopy(good)
        lock = (None, None)
        rr = refs
        if isinstance(mut, tuple):
            rr = copy.deepcopy(refs)
            mut[1](rr)
        elif mut == "LOCK":
            lock = ("Professor · Bio · Build · X · 1 Nov 2026, 10:00 IST", dt.datetime(2026, 11, 1, 10, tzinfo=dt.timezone.utc))
        else:
            mut(d)
        E, W = check(d, rr, lock=lock, now=dt.datetime(2026, 11, 19, tzinfo=dt.timezone.utc))
        if want is None:
            hit = not E and not W
        elif want.startswith("W:"):
            hit = any(want[2:] in w for w in W) and not E
        else:
            hit = any(want in x for x in E)
        ok += hit
        print(("PASS " if hit else "FAIL ") + name + ("" if hit else f"  E={E} W={W}"))
    n = len(cases)
    # TTG W-title-token: real cases. The CIR2 title as first pushed split "json" on progress-plan at 640x360 in CI (layout-check midword).
    # Not a title word: "Coderuns" in that CI log is the .nm row text joining the [Code] tag + the hidden "runs in Code" label + the
    # title — no title ever contains it, so don't test for it.
    tg = {"gloss": {"steps.json"}}
    cir2_old = "CI fix — main red on 1abe465 (card check: content/E/sources.json out of date)"
    tcases = [
        ("title token: CIR2 old title fires", lambda: any("`content/E/sources.json`" in w and "W-title-token" in w
                                                          for w in check_titles({"steps": [{"id": "CIR2", "title": cir2_old}]}, tg))),
        ("title token: CIR2 plain retitle quiet", lambda: not check_titles({"steps": [{"id": "CIR2", "chat": "Bio · Fix · CI red 1abe465",
                                                          "title": "CI fix — main red on 1abe465 (card check: sources list missed D-107)"}]}, tg)),
        ("title token: glossary term exempt", lambda: not title_tokens("read `steps.json` first", tg["gloss"]) and title_tokens("read map.json first", tg["gloss"])),
        ("title token: camelCase hump fires", lambda: title_tokens("mirror of trPlan in the app", tg["gloss"]) == ["`trPlan` (joined word)"]),
        ("title token: long word fires, hyphen splits, numbers exempt", lambda: title_tokens("gametogenesis", {}) and not title_tokens(
                                                          "mid-word break-point-free 640x360 v21 1.5 X1.02 (U3b) [Code]", {})),
        ("title token: to-do lines only with --todo-tokens, one warning per step", lambda: (
            not check_titles({"steps": [{"id": "Z", "title": "z", "todo": ["fix a/b", "fix c.d"]}]}, tg)
            and len(check_titles({"steps": [{"id": "Z", "title": "z", "todo": ["fix a/b", "fix c.d"]}]}, tg, todo=True)) == 1)),
        ("title token: warning only, never an error", lambda: (lambda EW: not EW[0] and any("W-title-token" in w for w in EW[1]))(
            check(dict(copy.deepcopy(good), steps=[dict(copy.deepcopy(good["steps"][0]), title=cir2_old, unblocks=[])]), dict(refs, gloss=set())))),
    ]
    for name, fn in tcases:
        n += 1
        hit = bool(fn())
        ok += hit
        print(("PASS " if hit else "FAIL ") + name)
    # W2: the scheduler on a known file gives the known plan, and the app's trPlan gives the same (node)
    fx = json.loads((ROOT / "tools" / "tracker" / "plan-fixture.json").read_text(encoding="utf-8"))
    got = plan(fx["doc"], fx["today"])
    for k, v in fx["expect"].items():
        n += 1
        hit = got.get(k) == v
        ok += hit
        print(("PASS " if hit else "FAIL ") + f"plan fixture: {k}" + ("" if hit else f"  got {json.dumps(got.get(k), ensure_ascii=False)}"))
    for name, d, t in (("plan parity (fixture)", fx["doc"], fx["today"]), ("plan parity (steps.json)", json.loads(STEPS.read_text(encoding="utf-8")), fx["today"])):
        n += 1
        E2, W2 = plan_parity(d, t)
        hit = not E2
        ok += hit
        print(("PASS " if hit else "FAIL ") + name + (f"  {W2[0]}" if W2 else "") + ("" if hit else f"  {E2}"))
    # W3: surface() picks the first matching rule; --write fills a missing run; the app's trSurface() agrees (node)
    d = copy.deepcopy(good)
    d["steps"][1].pop("run")
    d["steps"].append(dict(copy.deepcopy(d["steps"][1]), id="X1.05", type="Research", lock=False, inputs=[], unblocks=[]))
    checks = [("surface: first match wins", surface(d, d["steps"][1])["on"] == "Code" and surface(d, d["steps"][1])["rule"] == 1),
              ("surface: research → Cowork", surface(d, d["steps"][2])["on"] == "Cowork"),
              ("surface: --write fills run", surf_fill(d["steps"][1], d) and d["steps"][1]["run"] == {"on": "Code", "why": "lock"}),
              ("surface: --write keeps a set run", not surf_fill(d["steps"][0], d))]
    d2 = copy.deepcopy(d)
    d2["steps"][1]["run"] = {"on": "Cowork", "why": "x"}
    nt = next_text(d2, plan(d2, "2026-11-19"), (None, None))
    checks += [("surface: --next tags + Surface check line", "V1 [Cowork]" in nt and "- Surface check: V1" in nt)]
    for name, hit in checks:
        n += 1
        ok += hit
        print(("PASS " if hit else "FAIL ") + name)
    bad = copy.deepcopy(d)
    bad["surfaces"]["rules"][0]["if"] = ["lock"]
    bad["surfaces"]["rules"][1].pop("on")
    bad2 = dict(copy.deepcopy(d), surfaces=dict(d["surfaces"], rules="nope"))
    wd = w3f(copy.deepcopy(good))
    base = dict(copy.deepcopy(good["steps"][1]), needs=[], unblocks=[], inputs=[])
    for k, kw in enumerate([dict(lock=False, uses=["prof"], type="Review", run={"on": "Cowork", "why": "p"}),
                            dict(lock=False, uses=["prof"], type="Review", run={"on": "Code", "why": "p"}),
                            dict(lock=False, uses=["prof"], type="Review", run={"on": "Code", "why": "p", "traits": ["tests"]}),
                            dict(lock=False, uses=["prof"], type="Review", run={"on": "Cowork", "why": "p", "files": 40}),
                            dict(run={"on": "split", "why": "s", "traits": ["connectors"], "handoff": "h"}),
                            dict(lock=False, type="Research", run={"on": "Cowork", "why": "c", "traits": ["connectors", "owner"]}),
                            dict(lock=False, type="Research", run={"on": "Cowork", "why": "f", "files": 16}),
                            dict(lock=False, uses=["gpu"], type="Episode", run={"on": "Code", "why": "g", "traits": ["owner"]})]):
        wd["steps"].append(dict(copy.deepcopy(base), id=f"Z{k}", **kw))
    for name, doc in (("surface parity (cases)", d), ("surface parity (malformed rules)", bad), ("surface parity (rules not a list)", bad2),
                      ("surface parity (W3F rules: professor, split, files)", wd),
                      ("surface parity (steps.json)", json.loads(STEPS.read_text(encoding="utf-8")))):
        n += 1
        E2, W2 = surface_parity(doc)
        ok += not E2
        print(("PASS " if not E2 else "FAIL ") + name + (f"  {W2[0]}" if W2 else "") + (f"  {E2}" if E2 else ""))
    print(f"selftest {ok}/{n}")
    return ok == n


def main():
    global DBG
    for f in (sys.stdout, sys.stderr):   # Windows consoles default to cp1252; the schedule prints → · ◆
        if hasattr(f, "reconfigure"):
            f.reconfigure(encoding="utf-8")
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
    ap.add_argument("--todo-tokens", action="store_true", help="TTG: also warn on to-do words that may break mid-word (one warning per step)")
    ap.add_argument("--today", help="W2: plan from this date (YYYY-MM-DD, default today IST)")
    a = ap.parse_args()
    DBG = a.debug
    refs = load_refs()
    if a.selftest:
        return 0 if selftest(refs) else 1
    try:
        doc = json.loads(STEPS.read_text(encoding="utf-8"))
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
    E, W = check(doc, refs, a.only, lock, todo_tokens=a.todo_tokens)
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
