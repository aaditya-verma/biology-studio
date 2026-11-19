#!/usr/bin/env python3
"""Biology Studio — card-check (RULES C3; docs/card-spec.md §6). Every card in content/<book>/cards/ against the card spec.

Errors block (exit 1); warnings are allowed in drafts only. Same rules as the app's Studio (src/js/15-cards.js cardCheck) —
`--parity` runs that code in headless Chromium on every card and compares the error codes line by line.

Run from the repo root:
  python tools/card-check/check.py                 # check every card + index.json + sources.json
  python tools/card-check/check.py --only E05.01.01 --debug
  python tools/card-check/check.py --preview --only E05.01.01   # the card's level texts as plain text + word counts (fast)
  python tools/card-check/check.py --dry-run       # list what would be checked
  python tools/card-check/check.py --write-sources # rebuild content/<book>/sources.json (registry, decisions, sections, terms)
  python tools/card-check/check.py --calibrate     # mark suggester vs the dossier marks (cards/calibration.json) — must be 5/5
  python tools/card-check/check.py --parity        # Python ↔ app rules agree (needs Playwright + Chromium, or CHROME=/path)
  python tools/card-check/check.py --json          # machine-readable results
  python tools/card-check/check.py --selftest      # broken copies of a card must each raise their error (selftest.json)
Owner doc: docs/card-spec.md. EDIT: limits in LIMITS, verbs in VERBS, gate checklists in GATES (keep 15-cards.js in step — --parity).
"""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from citations import ROOT, build_sources, validate_citation, suggest_mark  # noqa: E402

# EDIT: limits (card-spec §3) — mirror CARD_RULES in src/js/15-cards.js
VERBS = ["explain", "describe", "identify", "label", "locate", "order", "compare", "distinguish", "predict", "name", "trace", "relate"]
SPATIAL = {"identify", "label", "locate", "order"}
BUDGET = {"general": 90, "school": 110, "neet": 140, "mbbs": 160, "pg": 200}
REQUIRED_LEVELS = ["general", "mbbs"]
MARKS = ["✔✔", "✔", "⚑", "✚", "≈"]
STATUSES = ["draft", "reviewed", "shipped", "retired"]
LIMITS = {"sentence_words": 25, "new_terms": 3, "new_terms_exception": 5, "min_checks": 2, "options": (3, 5)}
GATES = {   # EDIT: review-card checklists (card-spec §5); lines = which review lines the gate signs off
    "G-Sci": {"checklist": ["cited", "sections", "accuracy", "flags", "plus", "noapprox"], "lines": ["body", "fact", "mis", "adult"]},
    "G-Learn": {"checklist": ["objective", "checks", "refutes", "terms", "budget", "adult"], "lines": ["obj", "terms", "check", "mis"]},
    "G-A11y": {"checklist": ["alt", "input", "colour", "text125"], "lines": []},
    "G-Owner": {"checklist": ["owner"], "lines": []},
}
NEEDS = {"reviewed": ["G-Sci", "G-Learn"], "shipped": ["G-Sci", "G-Learn", "G-A11y", "G-Owner"]}
REF_RE = re.compile(r"\[(f\d+(?:\s*,\s*f\d+)*)\]")
DEBUG = False


def dbg(*a):
    if DEBUG:
        print("[card]", *a)


def jstr(x):   # JS String(x) for the values a card can hold
    return x if isinstance(x, str) else json.dumps(x) if isinstance(x, (list, dict)) else ("true" if x is True else "false" if x is False else str(x))


def strip_refs(t):
    return re.sub(r"\s+([.,;:!?])", r"\1", REF_RE.sub("", jstr(t or ""))).strip()


def words(t):
    return len([w for w in strip_refs(t).split() if re.search(r"[\w\d]", w)])


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", jstr(t or "").strip()) if s.strip()]


def review_lines(card):
    """Every review line id by kind (card-spec §5)."""
    L = {"obj": ["obj"], "terms": ["terms"], "body": [], "fact": [], "mis": [], "check": [], "adult": []}
    for lvl, txt in (card.get("body") or {}).items():
        L["body"] += [f"body.{lvl}.{i + 1}" for i in range(len(sentences(txt)))]
    L["fact"] = [f.get("id") for f in card.get("facts") or []]
    L["mis"] = [m.get("id") for m in card.get("misconceptions") or []]
    L["check"] = [q.get("id") for q in card.get("checks") or []]
    if card.get("adult"):
        L["adult"] = ["adult"]
    return L


def gate_lines(card, gate):
    L = review_lines(card)
    return [x for k in GATES[gate]["lines"] for x in L[k]]


def is_int(x):   # same as JS Number.isInteger: no bools, 1.0 counts
    return (type(x) is int) or (type(x) is float and x.is_integer())


def card_check(card, stem, ctx):
    """-> list of {lvl:'E'|'W', code, line, msg}. ctx: src, map_ids, map_terms, scenes."""
    out = []

    def E(code, line, msg):
        out.append({"lvl": "E", "code": code, "line": line, "msg": msg}); dbg("E", code, line, msg)

    def W(code, line, msg):
        out.append({"lvl": "W", "code": code, "line": line, "msg": msg}); dbg("W", code, line, msg)

    src = ctx["src"]
    # 1. schema
    want = {"spec": int, "id": str, "version": int, "book": str, "status": str, "title": str, "tier": str, "objective": dict, "body": dict,
            "facts": list, "terms": dict, "misconceptions": list, "checks": list, "scene": dict, "made": dict, "review": dict, "log": list}
    for k, t in want.items():
        if not (is_int(card.get(k)) if t is int else isinstance(card.get(k), t)):
            E("E-schema", k, f"'{k}' missing or not {t.__name__}")
    if out:
        return out
    if card["spec"] != 1 or card["version"] < 1 or card["status"] not in STATUSES or card["tier"] not in "ABCD" or len(card["tier"]) != 1:
        E("E-schema", "card", "spec must be 1, version ≥ 1, status draft/reviewed/shipped/retired, tier A–D")
    for k in ["by", "role", "agent", "date"]:
        if not card["made"].get(k):
            E("E-schema", "made", f"made.{k} missing")
    st = card["status"]
    final = st in ("reviewed", "shipped")
    # 2. id
    if card["id"] != stem:
        E("E-id", "card", f"id {card['id']} ≠ file name {stem}")
    if card["id"] not in ctx["map_ids"]:
        E("E-id", "card", f"{card['id']} is not a concept in map.json")
    # 3. objective — one testable verb
    ob = card["objective"]
    verb, text = ob.get("verb", ""), (ob.get("text") or "").strip()
    if not text:
        E("E-objective", "obj", "objective text missing")
    elif verb not in VERBS:
        E("E-objective", "obj", f"verb '{verb}' not in the list ({', '.join(VERBS)})")
    elif not text.lower().startswith(verb + " "):
        E("E-objective", "obj", f"objective must start with its verb '{verb}'")
    elif re.search(r"\b(?:and|then|,)\s+(" + "|".join(VERBS) + r")\b", text.lower()):
        E("E-objective", "obj", "one verb per objective (split it into two cards or two beats)")
    # 4–5. body levels, budgets, sentences, refs
    fids = [f.get("id") for f in card["facts"]]
    for lvl in REQUIRED_LEVELS:
        if not (card["body"].get(lvl) or "").strip():
            E("E-level", f"body.{lvl}", f"level '{lvl}' missing")

    def sent_rules(txt, prefix):
        for i, s in enumerate(sentences(txt)):
            ln = f"{prefix}.{i + 1}" if prefix != "adult" else "adult"
            if words(s) > LIMITS["sentence_words"]:
                E("E-sentence", ln, f"{words(s)} words > {LIMITS['sentence_words']}")
            refs = [r.strip() for m in REF_RE.findall(s) for r in m.split(",")]
            if not refs and not strip_refs(s).endswith("?"):
                E("E-ref", ln, "sentence has no fact ref [f1] (only a question may go without)")
            for r in refs:
                if r not in fids:
                    E("E-ref", ln, f"ref {r} points at no fact")

    for lvl, txt in card["body"].items():
        if lvl not in BUDGET:
            E("E-schema", f"body.{lvl}", f"unknown level '{lvl}' ({', '.join(BUDGET)})")
            continue
        if words(txt) > BUDGET[lvl]:
            E("E-words", f"body.{lvl}", f"{words(txt)} words > {BUDGET[lvl]} for {lvl}")
        sent_rules(txt, f"body.{lvl}")
    if card.get("adult"):
        sent_rules(card["adult"], "adult")
    # 6. facts: cited + marked (B1, B6, B7)
    seen = set()
    for f in card["facts"]:
        fid = jstr(f.get("id") or "f?")
        if not isinstance(f.get("id"), str) or not re.fullmatch(r"f\d+", fid) or fid in seen:
            E("E-schema", fid, "fact id must be f1, f2… and unique")
        seen.add(fid)
        if not isinstance(f.get("text"), str) or not f["text"].strip():
            E("E-schema", fid, "fact text missing or not text")
        for s in sentences(f.get("text", "")):
            if words(s) > LIMITS["sentence_words"]:
                E("E-sentence", fid, f"{words(s)} words > {LIMITS['sentence_words']}")
        if f.get("where") not in ("main", "more"):
            E("E-schema", fid, "where must be 'main' or 'more'")
        errs, p = validate_citation(f.get("cite"), src)
        for e in errs:
            E("E-cite", fid, e)
        mark_rules(f, p, fid, card, src, final, E, W)
    # 7. terms (D2 + glossary)
    tn, tk = card["terms"].get("new", []), card["terms"].get("known", [])
    ex = card["terms"].get("exception")
    if ex is not None and ex not in src["decisions"]:
        E("E-terms", "terms", f"terms exception {ex} is not in DECISIONS")
    elif len(tn) > (LIMITS["new_terms_exception"] if ex else LIMITS["new_terms"]):
        E("E-terms", "terms", f"{len(tn)} new terms > " + (f"{LIMITS['new_terms_exception']} (D2 exception {ex})" if ex else f"{LIMITS['new_terms']} (D2)"))
    for t in tn + tk:
        if t not in src["terms"]:
            E("E-terms", "terms", f"{t} is not a glossary term (index/terms.json)")
    for t in ctx["map_terms"].get(card["id"], []):
        if t not in tn + tk:
            W("W-terms", "terms", f"map term {t} not in the card's terms")
    # 8. misconceptions
    mids = []
    for m in card["misconceptions"]:
        mid = m.get("id") or "m?"
        mids.append(mid)
        for k in ["wrong", "right", "cite", "mark"]:
            if not m.get(k):
                E("E-mis", mid, f"{k} missing")
        if m.get("cite"):
            errs, _ = validate_citation(m["cite"], src)
            for e in errs:
                E("E-cite", mid, e)
        if m.get("mark") and m["mark"] not in MARKS:
            E("E-mark", mid, f"unknown mark {m['mark']}")
        if m.get("mark") == "≈":
            (E if final else W)("E-approx" if final else "W-approx", mid, "≈ blocks reviewed/shipped")
    # 9. checks (H1: test the objective; one right answer; refute a misconception)
    qs = card["checks"]
    if len(qs) < LIMITS["min_checks"]:
        E("E-checks", "checks", f"{len(qs)} checks < {LIMITS['min_checks']}")
    for q in qs:
        qid = q.get("id") or "q?"
        if q.get("type") not in ("mcq", "order"):
            E("E-check", qid, "type must be mcq or order")
        if not (q.get("prompt") or "").strip():
            E("E-check", qid, "prompt missing")
        opts = q.get("options") or []
        lo, hi = LIMITS["options"]
        if not (lo <= len(opts) <= hi) or any(not (isinstance(o, str) and o.strip()) for o in opts):
            E("E-check", qid, f"{lo}–{hi} non-empty options")
        if len(set(o.strip().lower() for o in opts if isinstance(o, str))) != len(opts):
            E("E-check", qid, "options repeat — exactly one right answer")
        if q.get("type") == "mcq" and not (is_int(q.get("answer")) and 0 <= q["answer"] < len(opts)):
            E("E-check", qid, "answer must be the index of the one right option")
        if q.get("type") == "order" and q.get("answer") is not None:
            E("E-check", qid, "an order check lists options in the right order; no answer field")
        if not (q.get("why") or "").strip():
            E("E-check", qid, "why missing (the explanation shown after answering)")
        if q.get("tests") != "objective":
            E("E-check", qid, "tests must be 'objective' (H1)")
        if q.get("refutes") and q["refutes"] not in mids:
            E("E-check", qid, f"refutes {q['refutes']}, which is not a misconception here")
    if qs and not any(q.get("refutes") for q in qs):
        E("E-checks", "checks", "no check refutes a misconception (playbook §3.4)")
    if verb in SPATIAL and not any(q.get("type") == "order" for q in qs):
        E("E-checks", "checks", f"spatial verb '{verb}' needs a spatial check (order)")
    # 10. scene
    sc = card["scene"].get("id")
    S = next((s for s in ctx["scenes"] if s["id"] == sc), None)   # scenes/index.json (scene-check keeps it in step with the files), as the app does
    if not sc or not S:
        E("E-scene", "scene", f"scene {sc} not found")
    else:
        if card["id"] not in S.get("cards", []):
            W("W-scene-cards", "scene", f"{sc} does not list {card['id']}")
        d = card["scene"].get("day")
        if d is not None and not (isinstance(d, (int, float)) and not isinstance(d, bool) and S["days"][0] <= d <= S["days"][1]):
            E("E-scene", "scene", f"day {d} outside {sc} days {S['days'][0]}–{S['days'][1]}")
    # 11. status backed by the gates; reviewer ≠ maker (H2)
    if st in NEEDS:
        for g in NEEDS[st]:
            r = card["review"].get(g) or {}
            if r.get("result") != "pass":
                E("E-status", g, f"{st} needs {g} = pass")
                continue
            for k in ["by", "role", "agent", "date"]:
                if not r.get(k):
                    E("E-status", g, f"{g}.{k} missing")
            if g != "G-Owner" and (r.get("role") == card["made"].get("role") or r.get("agent") == card["made"].get("agent")):
                E("E-status", g, f"{g} reviewer must differ from the maker (role and agent)")
            if g == "G-Owner" and r.get("role") != "Owner":
                E("E-status", g, "G-Owner is the owner's")
            miss = [c for c in GATES[g]["checklist"] if not (r.get("checklist") or {}).get(c)]
            if miss:
                E("E-status", g, f"{g} checklist not ticked: {', '.join(miss)}")
            for ln in gate_lines(card, g):
                v = (r.get("lines") or {}).get(ln)
                if v != "ok":
                    E("E-status", g, f"{g} line {ln} is {v or 'not reviewed'}")
    return out


def mark_rules(f, p, fid, card, src, final, E, W):
    mk = f.get("mark")
    if mk not in MARKS:
        E("E-mark", fid, f"mark missing or unknown ({' '.join(MARKS)})")
        return
    if p is None:
        return
    reg = {r["id"]: r for r in src["registry"]}
    tier1 = any(reg.get(s["id"], {}).get("tier") == 1 for s in p["sources"])
    if mk == "✔✔" and not (p["sections"] and tier1):
        E("E-mark", fid, "✔✔ needs a book section and a Tier 1 source")
    if mk == "✔" and not p["sections"]:
        E("E-mark", fid, "✔ needs a book section")
    if mk == "⚑":
        if not f.get("decision") or f["decision"] not in src["decisions"]:
            E("E-mark", fid, "⚑ needs decision: D-0xx that exists in DECISIONS")
        if not any(x.get("where") == "more" for x in card["facts"]):
            E("E-mark", fid, "⚑ needs the newer evidence as a 'more' fact")
    if mk == "✚":
        if f.get("where") != "more":
            E("E-mark", fid, "✚ lives in More only")
        if not tier1:
            E("E-mark", fid, "✚ needs a Tier 1 source")
        if "beyond langman" not in jstr(f.get("text") or "").lower():
            E("E-mark", fid, "✚ text must say 'beyond Langman'")
    if mk == "≈":
        (E if final else W)("E-approx" if final else "W-approx", fid, "≈ blocks reviewed/shipped (B1)")


def load_ctx(book):
    M = json.loads((ROOT / "content" / book / "map.json").read_text())
    sp = ROOT / "content" / book / "sources.json"
    return {"src": json.loads(sp.read_text()) if sp.exists() else build_sources(book),
            "map_ids": {c["id"] for c in M["concepts"]}, "map_terms": {c["id"]: c.get("terms", []) for c in M["concepts"]},
            "scenes": json.loads((ROOT / "content" / book / "scenes" / "index.json").read_text())["scenes"]}


def check_all(a):
    book = a.book
    cdir = ROOT / "content" / book / "cards"
    files = sorted(p for p in cdir.glob("*.json") if p.stem not in ("index", "calibration"))
    if a.only:
        files = [p for p in files if p.stem == a.only]
    if a.dry_run:
        print(f"would check {len(files)} card(s): {', '.join(p.stem for p in files)} · + index.json, sources.json")
        return 0, {}
    ctx = load_ctx(book)
    res, glob = {}, []
    fresh = build_sources(book)
    sp = cdir.parent / "sources.json"
    if not sp.exists() or {k: v for k, v in json.loads(sp.read_text()).items()} != fresh:
        glob.append({"lvl": "E", "code": "E-sources", "line": "sources.json", "msg": "out of date — run with --write-sources"})
    cards = {}
    for p in files:
        try:
            cards[p.stem] = json.loads(p.read_text())
        except Exception as e:
            res[p.stem] = [{"lvl": "E", "code": "E-schema", "line": "file", "msg": f"not JSON: {e}"}]
            continue
        res[p.stem] = card_check(cards[p.stem], p.stem, ctx)
    ip = cdir / "index.json"
    if not a.only:
        idx = json.loads(ip.read_text()) if ip.exists() else {"cards": []}
        want = [{"id": c["id"], "title": c["title"], "status": c["status"], "version": c["version"]} for c in cards.values()]
        if sorted(idx.get("cards", []), key=lambda x: x["id"]) != sorted(want, key=lambda x: x["id"]):
            glob.append({"lvl": "E", "code": "E-index", "line": "index.json", "msg": "out of step with the card files (id, title, status, version)"})
    if glob:
        res["_global"] = glob
    return 0, res


def report(res, as_json):
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    ne = nw = 0
    for cid, items in res.items():
        e = [i for i in items if i["lvl"] == "E"]; w = [i for i in items if i["lvl"] == "W"]
        ne += len(e); nw += len(w)
        if not as_json:
            print(f"{'✗' if e else '✓'} {cid}: {len(e)} errors, {len(w)} warnings")
            for i in items:
                print(f"   {i['lvl']} {i['code']:<14} {i['line']:<16} {i['msg']}")
    if not as_json:
        print(f"{'FAIL' if ne else 'PASS'}: {len(res)} item(s), {ne} errors, {nw} warnings")
    return 1 if ne else 0


def preview(a):
    cdir = ROOT / "content" / a.book / "cards"
    for p in sorted(cdir.glob("*.json")):
        if p.stem in ("index", "calibration") or (a.only and p.stem != a.only):
            continue
        c = json.loads(p.read_text())
        print(f"## {c['id']} · {c['title']} · {c['status']} v{c['version']}\nObjective: {c['objective'].get('text')}")
        for lvl, t in c["body"].items():
            print(f"\n[{lvl} · {words(t)}/{BUDGET.get(lvl, '?')} words]\n{strip_refs(t)}")
        print()
    return 0


def calibrate(a):
    src = build_sources(a.book)
    cal = json.loads((ROOT / "content" / a.book / "cards" / "calibration.json").read_text())
    ok = 0
    for f in cal["facts"]:
        errs, p = validate_citation(f["cite"], src)
        s = suggest_mark(p, f.get("decision"), src)
        hit = s == f["mark"] and not errs
        ok += hit
        print(f"{'✓' if hit else '✗'} {f['id']} dossier {f['mark']:<2} · suggested {s:<2} · [{f['cite']}]{' · ' + '; '.join(errs) if errs else ''}")
    n = len(cal["facts"])
    print(f"{'PASS' if ok == n else 'FAIL'}: calibration {ok}/{n} against {cal['source']}")
    return 0 if ok == n else 1


def apply_case(card, case):
    """Shared with the app (15-cards.js cardApplyCase): dotted paths, numbers index lists; null deletes a key."""
    import copy
    c = copy.deepcopy(card)

    def walk(path):
        ks = path.split(".")
        o = c
        for k in ks[:-1]:
            o = o[int(k)] if isinstance(o, list) else o.setdefault(k, {})
        return o, ks[-1]
    for path, v in (case.get("set") or {}).items():
        o, k = walk(path)
        if isinstance(o, list):
            o[int(k)] = v
        elif v is None:
            o.pop(k, None)
        else:
            o[k] = v
    for path in case.get("del") or []:
        o, k = walk(path)
        o.pop(k, None)
    return c


def selftest(a):
    st = json.loads((Path(__file__).resolve().parent / "selftest.json").read_text())
    ctx = load_ctx(a.book)
    base = json.loads((ROOT / "content" / a.book / "cards" / f"{st['base']}.json").read_text())
    bad = 0
    for case in st["cases"]:
        c = apply_case(base, case)
        codes = sorted({i["code"] for i in card_check(c, c.get("id"), ctx) if i["lvl"] == "E"})
        ok = case["expect"] in codes
        bad += not ok
        print(f"{'✓' if ok else '✗'} {case['name']:<34} expect {case['expect']:<12} got {', '.join(codes) or '—'}")
    print(f"{'PASS' if not bad else 'FAIL'}: selftest {len(st['cases']) - bad}/{len(st['cases'])}")
    return 1 if bad else 0


def parity(a):
    """Run the app's cardCheck() (src/js/15-cards.js) on every card and compare with this file's results."""
    import asyncio, functools, http.server, os, socketserver, threading
    _, py = check_all(argparse.Namespace(book=a.book, only=None, dry_run=False))
    py = {k: sorted(f"{i['lvl']} {i['code']} {i['line']}" for i in v) for k, v in py.items() if k != "_global"}
    cases = json.loads((Path(__file__).resolve().parent / "selftest.json").read_text())
    ctx = load_ctx(a.book)
    base = json.loads((ROOT / "content" / a.book / "cards" / f"{cases['base']}.json").read_text())
    for cs in cases["cases"]:
        c = apply_case(base, cs)
        py["case: " + cs["name"]] = sorted(f"{i['lvl']} {i['code']} {i['line']}" for i in card_check(c, c.get("id"), ctx))

    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x):
            pass
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    async def go():
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            kw = {"args": ["--no-sandbox"]}
            if os.environ.get("CHROME"):
                kw["executable_path"] = os.environ["CHROME"]
            try:
                b = await p.chromium.launch(**kw)
            except Exception:
                b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
            pg = await b.new_page()
            await pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/?test=1&debug=0#studio")
            await pg.wait_for_function("window.BOOTED", timeout=20000)
            r = await pg.evaluate("cs=>cardsCheckAll(cs).then(R=>Object.fromEntries(Object.entries(R).map(([k,v])=>[k,v.map(i=>i.lvl+' '+i.code+' '+i.line).sort()])))", cases)
            await b.close()
            return r
    js = asyncio.run(go())
    srv.shutdown()
    bad = 0
    for cs in cases["cases"]:   # the app must also raise each case's expected code
        k = "case: " + cs["name"]
        if not any(x.startswith("E " + cs["expect"] + " ") for x in js.get(k, [])):
            bad += 1
            print(f"✗ {k}: app misses {cs['expect']}")
    for cid in sorted(set(py) | set(js)):
        if py.get(cid) != js.get(cid):
            bad += 1
            print(f"✗ {cid}\n   python: {py.get(cid)}\n   app:    {js.get(cid)}")
        else:
            print(f"✓ {cid}: {len(py[cid])} findings agree")
    print(f"{'PASS' if not bad else 'FAIL'}: parity on {len(set(py) | set(js))} card(s)")
    return 1 if bad else 0


def main():
    global DEBUG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", default="E")
    ap.add_argument("--only", help="one card id")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--preview", action="store_true", help="level texts as plain text + word counts (fast)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-sources", action="store_true")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--parity", action="store_true")
    ap.add_argument("--selftest", action="store_true", help="broken copies of a card must each raise their code (selftest.json)")
    a = ap.parse_args()
    DEBUG = a.debug
    if a.write_sources:
        p = ROOT / "content" / a.book / "sources.json"
        p.write_text(json.dumps(build_sources(a.book), ensure_ascii=False, indent=1) + "\n")
        print(f"wrote {p.relative_to(ROOT)}")
        return 0
    if a.preview:
        return preview(a)
    if a.calibrate:
        return calibrate(a)
    if a.parity:
        return parity(a)
    if a.selftest:
        return selftest(a)
    _, res = check_all(a)
    if a.dry_run:
        return 0
    return report(res, a.json)


if __name__ == "__main__":
    sys.exit(main())
