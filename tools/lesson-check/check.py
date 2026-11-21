#!/usr/bin/env python3
"""Biology Studio — lesson-check (RULES C3; docs/lesson-spec.md §5). Every lesson in content/<book>/lessons/ against the lesson spec.

A lesson = one chapter, split into sittings of 10–15 min; each card adds read → check → scene|drill → remember (lesson-spec §3).
Errors block (exit 1); warnings never fail. CI runs it on every push.

Run from the repo root:
  python tools/lesson-check/check.py                 # check every lesson
  python tools/lesson-check/check.py --only E05 --debug
  python tools/lesson-check/check.py --preview       # the chapter path as text: sittings, steps, minutes (fast)
  python tools/lesson-check/check.py --write         # (re)build the lesson files from the cards, roadmap order and the time model
  python tools/lesson-check/check.py --write --dry-run   # show what --write would change, write nothing
  python tools/lesson-check/check.py --json          # machine-readable results
  python tools/lesson-check/check.py --selftest      # broken copies of a lesson must each raise their code
Owner doc: docs/lesson-spec.md. EDIT: time model in TIME, budget in BUDGET, step kinds in KINDS.
"""
import argparse, copy, json, math, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOK = "E"
CARDS = ROOT / "content" / BOOK / "cards"
LESSONS = ROOT / "content" / BOOK / "lessons"
MAP = ROOT / "content" / BOOK / "map.json"
ROADMAP = ROOT / "studio-docs" / "curriculum" / "roadmap.md"
CONFIG_JS = ROOT / "src" / "js" / "02-config.js"

# EDIT: lesson-spec §3–§4
KINDS = ["read", "check", "scene", "drill", "remember"]
DRILLS = {"rotate", "day", "frames", "label", "folded"}
SHOW = {"reviewed", "shipped"}           # mirror CONFIG.learn.show
TIME = {"wpm": 150, "read_base": 40, "q": 30, "q_order": 45, "q_drill": 60, "scene": 60, "drill": 60, "prompt": 15}   # read = MBBS text (medical students) + 40 s (opening the card, moving on); G-Learn L2
BUDGET = {"min": 10, "max": 15}          # minutes per sitting
STEP_RE = re.compile(r"^E\d\d\.\d\d\.\d\d:(%s)$" % "|".join(KINDS))
DBG = False


def dbg(*a):
    if DBG:
        print("  ·", *a)


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def config_lessons():
    t = CONFIG_JS.read_text(encoding="utf-8")
    m = re.search(r"lessons:\s*\[([^\]]*)\]", t)
    return re.findall(r"'(E\d\d)'", m.group(1)) if m else []


def roadmap_order():
    out = []
    for x in re.findall(r"E\d\d\.\d\d\.\d\d", ROADMAP.read_text(encoding="utf-8")):
        if x not in out:
            out.append(x)
    return out


def load_world():
    idx = load_json(CARDS / "index.json")
    cards = {}
    for f in sorted(CARDS.glob("E*.json")):
        c = load_json(f)
        cards[c["id"]] = c
    m = load_json(MAP)
    return {"index": {c["id"]: c for c in idx["cards"]}, "cards": cards, "map": {c["id"]: c for c in m["concepts"]},
            "order": roadmap_order(), "lessons": config_lessons()}


def words(t):
    return len(re.sub(r"\[f[\d,\s f]+\]", "", t or "").split())


def card_steps(c):
    """the step kinds a card adds, in order (lesson-spec §3)"""
    k = ["read", "check"]
    if c.get("scene"):   # every scene card explores Try it; drills run inside its Check (D-054), so no separate drill step (G-Learn L2)
        k.append("scene")
    if c.get("remember"):
        k.append("remember")
    return k


def est(c, kind):
    if kind == "read":
        w = words(c["body"].get("mbbs") or c["body"].get("general")) + words(c.get("adult")) + sum(words(m.get("wrong")) + words(m.get("right")) for m in c.get("misconceptions", []))
        return round(w / TIME["wpm"] * 60 + TIME["read_base"])
    if kind == "check":
        return sum(TIME["q_drill"] if q.get("type") in DRILLS else TIME["q_order"] if q.get("type") == "order" else TIME["q"] for q in c.get("checks", []))
    if kind == "remember":
        return TIME["prompt"] * len(c.get("remember", []))
    return TIME[kind]


def chapter_cards(W, ch):
    ids = [i for i, m in W["index"].items() if i.startswith(ch + ".") and m.get("status") in SHOW]
    return sorted(ids, key=lambda i: (W["order"].index(i) if i in W["order"] else 10 ** 6, i))


def derived_prereq(W, ids):
    out = []
    for i in ids:
        for p in W["map"].get(i, {}).get("prereq", []):
            if p not in ids and p not in out:
                out.append(p)
    return sorted(out, key=lambda i: (W["order"].index(i) if i in W["order"] else 10 ** 6, i))


def split(blocks, mx):
    """fewest contiguous sittings with each ≤ mx seconds; among those, the most even (smallest longest, then largest shortest). blocks = seconds per card"""
    n = len(blocks)
    pre = [0]
    for b in blocks:
        pre.append(pre[-1] + b)
    seg = lambda a, b: pre[b] - pre[a]
    for k in range(max(1, math.ceil(pre[-1] / mx)), n + 1):
        # best[j][m] = (longest, -shortest, cuts) for the first j cards in m sittings
        best = {(0, 0): (0, -10 ** 9, [])}
        for m in range(1, k + 1):
            for j in range(m, n + 1):
                cand = None
                for i in range(m - 1, j):
                    if (i, m - 1) not in best or seg(i, j) > mx:
                        continue
                    lo, nsh, cuts = best[(i, m - 1)]
                    v = (max(lo, seg(i, j)), max(nsh, -seg(i, j)), cuts + [list(range(i, j))])
                    if cand is None or v[:2] < cand[:2]:
                        cand = v
                if cand:
                    best[(j, m)] = cand
        if (n, k) in best:
            return best[(n, k)][2]
    return None


def build(W, ch, old=None):
    ids = chapter_cards(W, ch)
    steps_by = []
    for i in ids:
        c = W["cards"][i]
        steps_by.append([{"id": f"{i}:{k}", "card": i, "kind": k, "est_s": est(c, k)} for k in card_steps(c)])
    cuts = split([sum(s["est_s"] for s in b) for b in steps_by], BUDGET["max"] * 60) or [list(range(len(ids)))]
    L = {"spec": 1, "id": f"L-{ch}", "book": BOOK, "ch": ch, "version": (old or {}).get("version", 1), "budget": dict(BUDGET),
         "prereq": derived_prereq(W, ids),
         "sittings": [{"id": f"s{n + 1}", "steps": [s for j in part for s in steps_by[j]]} for n, part in enumerate(cuts)],
         "retired": list((old or {}).get("retired", []))}
    if old:   # a shipped step id that is no longer made goes to retired (A2)
        now = {s["id"] for x in L["sittings"] for s in x["steps"]}
        for x in old.get("sittings", []):
            for s in x.get("steps", []):
                if s.get("id") not in now and s.get("id") not in L["retired"]:
                    L["retired"].append(s["id"])
        if json.dumps({k: v for k, v in L.items() if k != "version"}, sort_keys=True) != json.dumps({k: v for k, v in old.items() if k != "version"}, sort_keys=True):
            L["version"] = old.get("version", 1) + 1
    return L


def head_version(path):
    """the shipped copy: HEAD's, or — when the file equals HEAD's (CI checks the pushed commit itself) — the commit before (needs fetch-depth ≥ 2)"""
    rel = path.relative_to(ROOT).as_posix()
    cur = path.read_text(encoding="utf-8") if path.exists() else None
    for ref in ("HEAD", "HEAD~1"):
        try:
            r = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{rel}"], capture_output=True, text=True, timeout=20)
        except Exception:
            return None
        if r.returncode != 0 or not r.stdout.strip():
            return None
        if r.stdout != cur or ref == "HEAD~1":
            return json.loads(r.stdout)
    return None


def check_lesson(W, L, path_name, head=None):
    E, Wn = [], []
    e = lambda code, msg: E.append(f"{code}: {msg}")
    w = lambda code, msg: Wn.append(f"{code}: {msg}")
    ch = L.get("ch")
    dbg("lesson", path_name, ch)
    if L.get("spec") != 1:
        e("E-spec", "spec must be 1")
    if not re.fullmatch(r"E\d\d", ch or ""):
        e("E-ch", f"bad chapter `{ch}`")
        return E, Wn
    if path_name != f"{ch}.json":
        e("E-file", f"file must be named {ch}.json")
    if L.get("id") != f"L-{ch}":
        e("E-id", f"id must be L-{ch}")
    if ch not in W["lessons"]:
        e("E-scope", f"{ch} is not in CONFIG.learn.lessons {W['lessons']}")
    b = L.get("budget") or {}
    mx, mn = b.get("max", BUDGET["max"]), b.get("min", BUDGET["min"])
    if mx > BUDGET["max"]:
        e("E-budget", f"budget.max {mx} > {BUDGET['max']} min")
    seen, cards_in, card_sit = set(), [], {}
    sits = L.get("sittings") or []
    if not sits:
        e("E-empty", "no sittings")
    for si, s in enumerate(sits):
        if s.get("id") != f"s{si + 1}":
            e("E-sid", f"sitting {si + 1} id must be s{si + 1}")
        tot = 0
        for st in s.get("steps") or []:
            sid, cid, kind = st.get("id"), st.get("card"), st.get("kind")
            dbg(" step", sid)
            if sid in seen:
                e("E-dup", f"duplicate step {sid}")
            seen.add(sid)
            if not isinstance(sid, str) or not STEP_RE.match(sid) or sid != f"{cid}:{kind}":
                e("E-stepid", f"step id `{sid}` must be <card>:<kind> with kind in {KINDS}")
                continue
            c = W["cards"].get(cid)
            if not c or cid not in W["index"]:
                e("E-card", f"{sid}: unknown card {cid}")
                continue
            if W["index"][cid].get("status") not in SHOW or c.get("status") not in SHOW:
                e("E-status", f"{sid}: card {cid} is `{c.get('status')}`, not Reviewed")
            if not cid.startswith(ch + "."):
                e("E-chapter", f"{sid}: card {cid} is not in {ch}")
            if not c.get("checks"):
                e("E-nocheck", f"{cid}: card has no Check")
            if cid not in cards_in:
                cards_in.append(cid)
                card_sit[cid] = si
            elif card_sit[cid] != si:
                e("E-split", f"{cid}: steps split across sittings")
            x = est(c, kind)
            if st.get("est_s") != x:
                e("E-est", f"{sid}: est_s {st.get('est_s')} ≠ {x} (run --write)")
            tot += x
        if tot > mx * 60:
            e("E-time", f"{s.get('id')}: {tot / 60:.1f} min > {mx} min budget")
        elif tot < mn * 60:
            w("W-short", f"{s.get('id')}: {tot / 60:.1f} min < {mn} min (allowed when the chapter can't make full sittings)")
    # per card: the right kinds, in order, contiguous
    flat = [st for s in sits for st in (s.get("steps") or [])]
    for cid in cards_in:
        c = W["cards"].get(cid)
        if not c:
            continue
        got = [st.get("kind") for st in flat if st.get("card") == cid]
        want = card_steps(c)
        if got != want:
            if "check" not in got and c.get("checks"):
                e("E-nocheck", f"{cid}: no check step")
            if "scene" in got and not c.get("scene"):
                e("E-scene", f"{cid}: scene step but the card has no scene")
            if "drill" in got:
                e("E-drill", f"{cid}: a drill step — drills run inside the Check; a scene card gets a scene step (lesson-spec §3)")
            e("E-order", f"{cid}: steps {got} ≠ {want}")
        pos = [k for k, st in enumerate(flat) if st.get("card") == cid]
        if pos and pos[-1] - pos[0] + 1 != len(pos):
            e("E-order", f"{cid}: its steps are not together")
    want_cards = chapter_cards(W, ch)
    if [c for c in cards_in if c in want_cards] != [c for c in want_cards if c in cards_in]:
        e("E-roadmap", f"cards not in roadmap order: {cards_in}")
    for cid in want_cards:
        if cid not in cards_in:
            w("W-missing", f"Reviewed card {cid} is not in the lesson")
    if L.get("prereq") != derived_prereq(W, cards_in):
        e("E-prereq", f"prereq {L.get('prereq')} ≠ derived {derived_prereq(W, cards_in)}")
    ret = L.get("retired") or []
    for r in ret:
        if r in seen:
            e("E-reuse", f"retired step {r} is used again")
    if head:
        for s in head.get("sittings", []):
            for st in s.get("steps", []):
                if st.get("id") not in seen and st.get("id") not in ret:
                    e("E-gone", f"shipped step {st.get('id')} removed without `retired` (A2)")
    return E, Wn


def minutes(L):
    return [round(sum(st["est_s"] for st in s["steps"]) / 60, 1) for s in L["sittings"]]


def preview(L, W):
    print(f"{L['id']} · {L['ch']} · {len(L['sittings'])} sittings · {sum(minutes(L))} min · needs first: {', '.join(L['prereq']) or '—'}")
    for s, m in zip(L["sittings"], minutes(L)):
        print(f"  {s['id']} · {m} min")
        cur = None
        for st in s["steps"]:
            if st["card"] != cur:
                cur = st["card"]
                print(f"    {cur} {W['cards'][cur]['title']}")
            print(f"      {st['kind']:<9}{st['est_s']:>4} s")


def selftest(W):
    base = build(W, "E05")
    cases = [
        ("unknown card", lambda L: L["sittings"][0]["steps"].__setitem__(0, dict(L["sittings"][0]["steps"][0], id="E05.99.99:read", card="E05.99.99")), "E-card"),
        ("not Reviewed", lambda L: W["cards"]["E05.01.01"].__setitem__("status", "draft"), "E-status"),
        ("missing Check step", lambda L: L["sittings"][0]["steps"].pop(1), "E-nocheck"),
        ("over budget", lambda L: (L["budget"].__setitem__("max", 3)), "E-time"),
        ("stale estimate", lambda L: L["sittings"][0]["steps"][0].__setitem__("est_s", 1), "E-est"),
        ("scene on a no-scene card", lambda L: None, None),
        ("drill step (reserved: drills run in the Check)", lambda L: [st.__setitem__("kind", "drill") or st.__setitem__("id", st["card"] + ":drill") for st in L["sittings"][0]["steps"] if st["id"] == "E05.01.01:scene"], "E-drill"),
        ("steps out of order", lambda L: L["sittings"][0]["steps"].insert(0, L["sittings"][0]["steps"].pop(1)), "E-order"),
        ("duplicate step", lambda L: L["sittings"][0]["steps"].append(dict(L["sittings"][0]["steps"][0])), "E-dup"),
        ("roadmap order", lambda L: L["sittings"].__setitem__(0, {"id": "s1", "steps": L["sittings"][0]["steps"][4:8] + L["sittings"][0]["steps"][:4] + L["sittings"][0]["steps"][8:]}), "E-roadmap"),
        ("prereq wrong", lambda L: L["prereq"].pop(), "E-prereq"),
        ("other chapter's card", lambda L: L["sittings"][-1]["steps"].extend([{"id": "E06.00.01:" + k, "card": "E06.00.01", "kind": k, "est_s": est(W["cards"]["E06.00.01"], k)} for k in card_steps(W["cards"]["E06.00.01"])]), "E-chapter"),
        ("shipped step gone", lambda L: L["sittings"][-1]["steps"].pop(), "E-gone"),
        ("chapter outside L2 scope", lambda L: L.__setitem__("ch", "E09") or L.__setitem__("id", "L-E09"), "E-scope"),
    ]
    # scene-on-no-scene needs a no-scene chapter
    b6 = build(W, "E06")
    bad = 0
    E0, _ = check_lesson(W, base, "E05.json", head=base)
    if E0:
        print("FAIL: the clean E05 lesson has errors:", E0)
        bad += 1
    for name, f, code in cases:
        Wc = copy.deepcopy(W)
        if name == "scene on a no-scene card":
            L = copy.deepcopy(b6)
            for st in L["sittings"][0]["steps"]:
                if st["id"] == "E06.00.01:remember":
                    st.update(id="E06.00.01:scene", kind="scene", est_s=TIME["scene"])
            E, _ = check_lesson(Wc, L, "E06.json", head=None)
            code = "E-scene"
        else:
            L = copy.deepcopy(base)
            W_bak = W["cards"]["E05.01.01"].get("status")
            if name == "not Reviewed":
                Wc["cards"]["E05.01.01"]["status"] = "draft"
            else:
                f(L)
            fname = "E09.json" if name == "chapter outside L2 scope" else "E05.json"
            E, _ = check_lesson(Wc, L, fname, head=base if name == "shipped step gone" else None)
            W["cards"]["E05.01.01"]["status"] = W_bak
        hit = any(x.startswith(code) for x in E)
        print(f"  {'ok ' if hit else 'BAD'} {name} → {code}{'' if hit else ' (got ' + '; '.join(E) + ')'}")
        bad += 0 if hit else 1
    # split: never over budget, cards whole
    for ch in W["lessons"]:
        L = build(W, ch)
        if any(m > BUDGET["max"] for m in minutes(L)):
            print(f"  BAD split {ch}: {minutes(L)}")
            bad += 1
    n = len(cases) + 2
    print(f"{'PASS' if not bad else 'FAIL'}: selftest {n - bad}/{n}")
    return 1 if bad else 0


def main():
    global DBG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="one chapter, e.g. E05")
    ap.add_argument("--debug", action="store_true", help="print every rule as it runs")
    ap.add_argument("--dry-run", action="store_true", help="list what would be checked / written, write nothing")
    ap.add_argument("--preview", action="store_true", help="the chapter path as text (fast)")
    ap.add_argument("--write", action="store_true", help="(re)build lesson files from cards + roadmap + time model")
    ap.add_argument("--json", action="store_true", help="machine-readable results")
    ap.add_argument("--selftest", action="store_true", help="broken copies must each raise their code")
    a = ap.parse_args()
    DBG = a.debug
    W = load_world()
    if a.selftest:
        return selftest(W)
    chs = [c for c in W["lessons"] if not a.only or c == a.only]
    if a.write:
        LESSONS.mkdir(parents=True, exist_ok=True)
        for ch in chs:
            p = LESSONS / f"{ch}.json"
            old = head_version(p)   # the shipped copy decides version + retired (A2); an unshipped draft is simply rebuilt
            L = build(W, ch, old)
            txt = json.dumps(L, ensure_ascii=False, indent=1) + "\n"
            if a.dry_run:
                print(f"would write {p.relative_to(ROOT)}: {len(L['sittings'])} sittings {minutes(L)} min" + ("" if p.exists() and p.read_text(encoding='utf-8') == txt else " (changed)"))
            elif not p.exists() or p.read_text(encoding="utf-8") != txt:
                p.write_text(txt, encoding="utf-8")
                print(f"wrote {p.relative_to(ROOT)} · v{L['version']} · {minutes(L)} min")
        if a.dry_run:
            return 0
    files = sorted(LESSONS.glob("E*.json")) if LESSONS.exists() else []
    files = [f for f in files if not a.only or f.stem == a.only]
    if a.dry_run:
        for f in files:
            print("would check", f.relative_to(ROOT))
        for ch in chs:
            if not (LESSONS / f"{ch}.json").exists():
                print("missing", f"content/{BOOK}/lessons/{ch}.json")
        return 0
    res, errs, warns = {}, 0, 0
    for ch in chs:
        if not (LESSONS / f"{ch}.json").exists():
            res[ch] = {"errors": [f"E-nofile: content/{BOOK}/lessons/{ch}.json missing (CONFIG.learn.lessons)"], "warnings": []}
    for f in files:
        L = load_json(f)
        E, Wn = check_lesson(W, L, f.name, head_version(f))
        res[f.stem] = {"errors": E, "warnings": Wn, "minutes": minutes(L) if not E or all(s.get("steps") for s in L.get("sittings", [])) else None}
        if a.preview and not any(x.startswith("E-card") for x in E):
            preview(L, W)
    for k, r in res.items():
        errs += len(r["errors"])
        warns += len(r["warnings"])
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, r in res.items():
            print(f"{'✓' if not r['errors'] else '✗'} {k}: {len(r['errors'])} errors, {len(r['warnings'])} warnings" + (f" · sittings {r.get('minutes')} min" if r.get("minutes") else ""))
            for x in r["errors"]:
                print("   ERROR", x)
            for x in r["warnings"]:
                print("   warn ", x)
        print(f"{'PASS' if not errs else 'FAIL'}: {len(res)} lesson(s), {errs} errors, {warns} warnings")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
