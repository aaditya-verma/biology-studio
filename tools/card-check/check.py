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
TYPES = ["mcq", "order", "rotate", "day", "frames", "label", "folded", "trace"]   # card-spec §2a (V2 drills, D-054; trace V3, D-075)
TRACE_IN = ("epiblast", "streak", "mesoderm", "endoderm")   # where a tracer path can end (scene-spec §6 tracer)
SPATIAL_TYPES = {"order", "frames", "label", "rotate"}
DRILL = {"alt_words": 40, "frame_words": 25, "tol": (10, 45), "tol_default": 25, "zoom": (0.5, 6), "pins": (2, 4), "items": (2, 5), "label_words": 3}
BUDGET = {"general": 90, "school": 110, "neet": 140, "mbbs": 160, "pg": 200}
REQUIRED_LEVELS = ["general", "mbbs"]
MARKS = ["✔✔", "✔", "⚑", "✚", "≈", "ⓘ"]
KINDS = ["concept", "guide"]   # guide = a Part 0 card about the app itself (D-050): facts cite APP <screen>, mark ⓘ
APP_LOCS = ["Today", "Cards", "Card", "Check", "Explain", "Deck", "Try it", "Watch it", "Status", "Settings", "Lessons", "Mixed review"]
APP_RE = re.compile(r"^APP(?: (.+))?$")
STATUSES = ["draft", "reviewed", "shipped", "retired"]
LIMITS = {"sentence_words": 25, "new_terms": 3, "new_terms_exception": 5, "min_checks": 2, "options": (3, 5), "remember": (2, 5), "shows_up": 6}
GATES = {   # EDIT: review-card checklists (card-spec §5); lines = which review lines the gate signs off
    "G-Sci": {"checklist": ["cited", "sections", "accuracy", "flags", "plus", "noapprox"], "lines": ["body", "fact", "mis", "adult", "clinical", "remember"]},
    "G-Learn": {"checklist": ["objective", "checks", "refutes", "terms", "budget", "adult"], "lines": ["obj", "terms", "check", "mis", "remember", "shows"]},
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
    L = {"obj": ["obj"], "terms": ["terms"], "body": [], "fact": [], "mis": [], "check": [], "adult": [], "clinical": [], "remember": [], "shows": []}
    for lvl, txt in (card.get("body") or {}).items():
        L["body"] += [f"body.{lvl}.{i + 1}" for i in range(len(sentences(txt)))]
    L["fact"] = [f.get("id") for f in card.get("facts") or []]
    L["mis"] = [m.get("id") for m in card.get("misconceptions") or []]
    L["check"] = [q.get("id") for q in card.get("checks") or []]
    if card.get("adult"):
        L["adult"] = ["adult"]
    if card.get("clinical"):
        L["clinical"] = ["clinical"]
    L["remember"] = [r.get("id") for r in card.get("remember") or [] if isinstance(r, dict)]
    if card.get("shows_up"):
        L["shows"] = ["shows_up"]
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
            "facts": list, "terms": dict, "misconceptions": list, "checks": list, "made": dict, "review": dict, "log": list, "remember": list}
    for k, t in want.items():
        if not (is_int(card.get(k)) if t is int else isinstance(card.get(k), t)):
            E("E-schema", k, f"'{k}' missing or not {t.__name__}")
    if "scene" in card and not isinstance(card.get("scene"), dict):   # optional (D-058): no scene yet → Try it says Coming soon
        E("E-schema", "scene", "'scene' must be an object, or left out when the concept has no scene yet")
    if out:
        return out
    # 1b. shapes inside the fields (a badly typed card is reported, never a traceback — G-Eng R3)
    if not all(isinstance(v, str) for v in card["body"].values()):
        E("E-schema", "body", "every level text must be text")
    for k in ["facts", "misconceptions", "checks"]:
        if any(not isinstance(x, dict) for x in card[k]):
            E("E-schema", k, f"each item in '{k}' must be an object")
    for k in ["new", "known"]:
        v = card["terms"].get(k, [])
        if not isinstance(v, list) or any(not isinstance(t, str) for t in v):
            E("E-schema", "terms", f"terms.{k} must be a list of glossary ids")
    if not isinstance(card["objective"].get("verb", ""), str) or not isinstance(card["objective"].get("text", ""), str):
        E("E-schema", "obj", "objective verb and text must be text")
    for q in card["checks"]:
        if isinstance(q, dict) and "options" in q and not isinstance(q["options"], list):
            E("E-schema", "checks", "check options must be a list")
    if out:
        return out
    if card["spec"] != 1 or card["version"] < 1 or card["status"] not in STATUSES or card["tier"] not in "ABCD" or len(card["tier"]) != 1:
        E("E-schema", "card", "spec must be 1, version ≥ 1, status draft/reviewed/shipped/retired, tier A–D")
    for k in ["by", "role", "agent", "date"]:
        if not card["made"].get(k):
            E("E-schema", "made", f"made.{k} missing")
    st = card["status"]
    final = st in ("reviewed", "shipped")
    kind = card.get("kind", "concept")
    guide = kind == "guide"
    if kind not in KINDS:
        E("E-schema", "card", f"kind must be one of {', '.join(KINDS)}")
    elif guide and not str(card["id"]).startswith("E00."):
        E("E-kind", "card", "a guide card lives in Part 0 (E00) only")
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
            ln = f"{prefix}.{i + 1}" if prefix not in ("adult", "clinical") else prefix
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
    if "clinical" in card and not (isinstance(card["clinical"], str) and card["clinical"].strip()):
        E("E-schema", "clinical", "clinical must be text (leave it out if the concept has no clinical link)")
    elif card.get("clinical"):
        sent_rules(card["clinical"], "clinical")
    # 5b. Remember prompts (card-spec §2: recall Q + answer with fact refs to main facts)
    rlo, rhi = LIMITS["remember"]
    rem = card["remember"]
    if not (rlo <= len(rem) <= rhi):
        E("E-remember", "remember", f"{len(rem)} prompts — need {rlo}–{rhi}")
    main_ids = [f.get("id") for f in card["facts"] if f.get("where") == "main"]
    rseen = set()
    for r in rem:
        if not isinstance(r, dict):
            E("E-remember", "remember", "each prompt is {id, q, a}")
            continue
        rid = jstr(r.get("id") or "r?")
        if not re.fullmatch(r"r\d+", rid) or rid in rseen:
            E("E-remember", rid, "prompt id must be r1, r2… and unique")
        rseen.add(rid)
        q, ans = jstr(r.get("q") or "").strip(), jstr(r.get("a") or "").strip()
        if not q.endswith("?"):
            E("E-remember", rid, "q must be a question (ends with ?)")
        if not ans:
            E("E-remember", rid, "a (the answer) missing")
        for t in (q, ans):
            if words(t) > LIMITS["sentence_words"]:
                E("E-sentence", rid, f"{words(t)} words > {LIMITS['sentence_words']}")
        refs = [x.strip() for m in REF_RE.findall(ans) for x in m.split(",")]
        if ans and not refs:
            E("E-ref", rid, "answer has no fact ref [f1]")
        for x in refs:
            if x not in main_ids:
                E("E-ref", rid, f"ref {x} is not a main fact (Remember tests the card, not More)")
    # 5c. Where it shows up (concept ids)
    if "shows_up" in card:
        su = card["shows_up"]
        if not isinstance(su, list) or not su or len(su) > LIMITS["shows_up"]:
            E("E-shows", "shows_up", f"shows_up must be a list of 1–{LIMITS['shows_up']} concept ids")
        else:
            for x in su:
                if x not in ctx["map_ids"] or x == card["id"]:
                    E("E-shows", "shows_up", f"{jstr(x)} is not another concept in map.json")
            if len(set(map(jstr, su))) != len(su):
                E("E-shows", "shows_up", "concept ids repeat")
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
        if app_cite(f.get("cite")) is not None:
            app_rules(f.get("cite"), f.get("mark"), fid, guide, E)
            continue
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
        if m.get("cite") and app_cite(m["cite"]) is not None:
            app_rules(m["cite"], m.get("mark"), mid, guide, E)
        elif m.get("cite"):
            errs, _ = validate_citation(m["cite"], src)
            for e in errs:
                E("E-cite", mid, e)
            if m.get("mark") == "ⓘ":
                E("E-mark", mid, "ⓘ needs an APP cite in a guide card")
        if m.get("mark") and m["mark"] not in MARKS:
            E("E-mark", mid, f"unknown mark {m['mark']}")
        if m.get("mark") == "≈":
            (E if final else W)("E-approx" if final else "W-approx", mid, "≈ blocks reviewed/shipped")
    # 9. checks (H1: test the objective; one right answer; refute a misconception) + 3D drills (card-spec §2a)
    qs = card["checks"]
    scn = card.get("scene")   # optional (D-058)
    SF = ctx.get("scene_files", {}).get(scn.get("id")) if scn else None
    if len(qs) < LIMITS["min_checks"]:
        E("E-checks", "checks", f"{len(qs)} checks < {LIMITS['min_checks']}")
    for q in qs:
        qid = q.get("id") or "q?"
        ty = q.get("type")
        if ty not in TYPES:
            E("E-check", qid, f"type must be one of {', '.join(TYPES)}")
        if not (q.get("prompt") or "").strip():
            E("E-check", qid, "prompt missing")
        opts = q.get("options") or []
        lo, hi = LIMITS["options"]
        if ty in ("mcq", "order", "rotate", "label", "trace") or ty not in TYPES:
            if not (lo <= len(opts) <= hi) or any(not (isinstance(o, str) and o.strip()) for o in opts):
                E("E-check", qid, f"{lo}–{hi} non-empty options")
            if len(set(o.strip().lower() for o in opts if isinstance(o, str))) != len(opts):
                E("E-check", qid, "options repeat — exactly one right answer")
        if ty in ("mcq", "rotate", "day", "trace") and not (is_int(q.get("answer")) and 0 <= q["answer"] < len(opts)):
            E("E-check", qid, "answer must be the index of the one right option")
        if ty in ("order", "frames", "label", "folded") and q.get("answer") is not None:
            E("E-check", qid, f"a{'n' if ty == 'order' else ''} {ty} check has no answer field (card-spec §2a)")
        if ty in DRILL_TYPES:
            if not scn:
                E("E-drill", qid, "a 3D drill needs the card's scene (card-spec §2a) — this card has none")
            drill_rules(q, qid, ty, opts, SF, E)
        if not (q.get("why") or "").strip():
            E("E-check", qid, "why missing (the explanation shown after answering)")
        if q.get("tests") != "objective":
            E("E-check", qid, "tests must be 'objective' (H1)")
        if q.get("refutes") and q["refutes"] not in mids:
            E("E-check", qid, f"refutes {q['refutes']}, which is not a misconception here")
    if qs and not any(q.get("refutes") for q in qs):
        E("E-checks", "checks", "no check refutes a misconception (playbook §3.4)")
    if verb in SPATIAL and not any(q.get("type") in SPATIAL_TYPES for q in qs):
        E("E-checks", "checks", f"spatial verb '{verb}' needs a spatial check (order, frames, label or rotate)")
    # 10. scene (optional, D-058: left out = no 3D yet)
    sc = scn.get("id") if scn else None
    S = next((s for s in ctx["scenes"] if s["id"] == sc), None)   # scenes/index.json (scene-check keeps it in step with the files), as the app does
    if not scn:
        pass
    elif not sc or not S:
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


DRILL_TYPES = ("rotate", "day", "frames", "label", "folded", "trace")


def scene_anchors(S):
    """Anchors a scene draws (scene-spec §7) — mirror of sceneAnchors() in src/js/15-cards.js."""
    out = set()
    for p in S.get("parts", []):
        k = p.get("kind")
        if k == "disc":
            out |= set((p.get("layers") or {}).keys())
        elif k == "notochord":
            L = p.get("layers") or {}
            if "notochord" in L:
                out |= {"noto-cord", "noto-plate", "notochord"}
            if "prechordal" in L:
                out.add("prechordal")
        elif k == "axes":
            out |= {"axis-" + a for a in ("cranial", "caudal", "left", "right", "dorsal", "ventral")}
        elif k == "planes":
            out |= {"plane-" + str(pl.get("id")) for pl in p.get("planes", [])}
        elif k == "ruler":
            out.add("ruler")
        elif k == "tracer":
            out.add("tracer-" + str(p.get("id")))
    return out


def view_angle(a1, e1, a2, e2):
    """Angle between two orbit-camera orientations (degrees) — mirror of viewAngle() in src/js/14-scene3d.mjs."""
    import math

    def basis(az, el):
        a, e = math.radians(az), math.radians(el)
        b = [math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)]
        n = math.hypot(b[1], b[0]) or 1
        r = [-b[1] / n, b[0] / n, 0]
        u = [b[1] * r[2] - b[2] * r[1], b[2] * r[0] - b[0] * r[2], b[0] * r[1] - b[1] * r[0]]
        return [r, u, b]
    A, B = basis(a1, e1), basis(a2, e2)
    tr = sum(A[i][j] * B[i][j] for i in range(3) for j in range(3))
    return math.degrees(math.acos(max(-1, min(1, (tr - 1) / 2))))


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def view_of(v, S):
    """a show.view or a target → (az, el) or None"""
    if isinstance(v, str):
        m = next((w for w in S.get("views", []) if w.get("id") == v), None)
        return (m["azimuth_deg"], m["elevation_deg"]) if m else None
    if isinstance(v, dict) and num(v.get("azimuth_deg")) and num(v.get("elevation_deg")):
        return (v["azimuth_deg"], v["elevation_deg"])
    return None


def show_rules(sh, S, qid, E, where="show"):
    """a drill's `show` state (card-spec §2a) against its scene"""
    if not isinstance(sh, dict):
        E("E-check", qid, f"{where} missing (the scene state the drill opens at)")
        return
    d = sh.get("day")
    if not num(d):
        E("E-check", qid, f"{where}.day must be a number")
    elif S and not (S["days"][0]["day"] <= d <= S["days"][-1]["day"]):
        E("E-drill", qid, f"{where}.day {d} outside the scene's days {S['days'][0]['day']}–{S['days'][-1]['day']}")
    if "view" in sh and S and view_of(sh["view"], S) is None:
        E("E-drill", qid, f"{where}.view {sh['view']} is not a view of {S['id']}")
    z = sh.get("zoom", 1)
    if not (num(z) and DRILL["zoom"][0] <= z <= DRILL["zoom"][1]):
        E("E-check", qid, f"{where}.zoom outside {DRILL['zoom'][0]}–{DRILL['zoom'][1]}")
    c = sh.get("cut")
    if c is not None and not (isinstance(c, dict) and c.get("axis") in ("x", "y") and num(c.get("at")) and -0.9 <= c["at"] <= 0.9 and isinstance(c.get("on"), bool)):
        E("E-check", qid, f"{where}.cut must be {{axis x|y, at −0.9…0.9, on}}")
    elif c is not None and "slab_mm" in c and not (num(c["slab_mm"]) and 0.002 <= c["slab_mm"] <= 0.5 and c.get("axis") == "x"):
        E("E-check", qid, f"{where}.cut.slab_mm must be 0.002–0.5 on a cross-section (axis x)")
    ly = sh.get("layers")
    if ly is not None:
        if not isinstance(ly, dict) or any(not isinstance(v, bool) for v in ly.values()):
            E("E-check", qid, f"{where}.layers must map layer ids to true/false")
        elif S:
            ids = {l.get("id") for l in S.get("layers", [])}
            for k in ly:
                if k not in ids:
                    E("E-drill", qid, f"{where}.layers: {k} is not a layer of {S['id']}")


def drill_rules(q, qid, ty, opts, S, E):
    """3D drills (card-spec §2a); S = the card's scene file (None if missing — E-scene reports that)"""
    def alt():
        a = q.get("alt")
        if not (isinstance(a, str) and a.strip()):
            E("E-check", qid, "alt missing (the drill's text alternative)")
        elif len(a.split()) > DRILL["alt_words"]:
            E("E-check", qid, f"alt over {DRILL['alt_words']} words")
    if ty == "rotate":
        show_rules(q.get("show"), S, qid, E)
        alt()
        tol = q.get("tol_deg", DRILL["tol_default"])
        if not (num(tol) and DRILL["tol"][0] <= tol <= DRILL["tol"][1]):
            E("E-check", qid, f"tol_deg outside {DRILL['tol'][0]}–{DRILL['tol'][1]}")
            tol = DRILL["tol_default"]
        t = view_of(q.get("target"), S) if S and isinstance(q.get("target"), str) else None
        if not isinstance(q.get("target"), str):
            E("E-check", qid, "target must be a scene view id")
        elif S and t is None:
            E("E-drill", qid, f"target {q['target']} is not a view of {S['id']}")
        sv = view_of((q.get("show") or {}).get("view"), S) if S and isinstance(q.get("show"), dict) else None
        if S and isinstance(q.get("show"), dict) and "view" not in q["show"]:
            E("E-check", qid, "show.view needed (the start view)")
        if t and sv and view_angle(sv[0], sv[1], t[0], t[1]) <= tol:
            E("E-drill", qid, f"starts within {tol}° of the target — already solved")
    elif ty == "day":
        show_rules(q.get("show"), S, qid, E)
        alt()
        lo, hi = LIMITS["options"]
        if not (lo <= len(opts) <= hi) or any(not num(o) for o in opts):
            E("E-check", qid, f"{lo}–{hi} day numbers as options")
        elif len(set(opts)) != len(opts):
            E("E-check", qid, "options repeat — exactly one right answer")
        elif S:
            for o in opts:
                if not (S["days"][0]["day"] <= o <= S["days"][-1]["day"]):
                    E("E-drill", qid, f"day option {o} outside the scene's days")
            a, sd = q.get("answer"), (q.get("show") or {}).get("day") if isinstance(q.get("show"), dict) else None
            if is_int(a) and 0 <= a < len(opts) and num(sd) and opts[a] != sd:
                E("E-drill", qid, f"the right option (day {opts[a]}) is not the day shown ({sd})")
    elif ty == "frames":
        lo, hi = LIMITS["options"]
        if not (lo <= len(opts) <= hi) or any(not isinstance(o, dict) for o in opts):
            E("E-check", qid, f"{lo}–{hi} frames {{text, show}} as options")
        else:
            texts = []
            for i, o in enumerate(opts):
                tx = o.get("text")
                if not (isinstance(tx, str) and tx.strip()):
                    E("E-check", qid, f"frame {i + 1}: text missing (its text alternative)")
                elif len(tx.split()) > DRILL["frame_words"]:
                    E("E-check", qid, f"frame {i + 1}: text over {DRILL['frame_words']} words")
                else:
                    texts.append(tx.strip().lower())
                show_rules(o.get("show"), S, qid, E, f"frame {i + 1} show")
            if len(set(texts)) != len(texts):
                E("E-check", qid, "frame texts repeat")
    elif ty == "label":
        show_rules(q.get("show"), S, qid, E)
        alt()
        if any(isinstance(o, str) and len(o.split()) > DRILL["label_words"] for o in opts):
            E("E-check", qid, f"label options ≤ {DRILL['label_words']} words (D8)")
        pins = q.get("pins")
        lo, hi = DRILL["pins"]
        if not (isinstance(pins, list) and lo <= len(pins) <= hi and all(isinstance(p, dict) for p in pins)):
            E("E-check", qid, f"{lo}–{hi} pins {{at, answer}}")
        else:
            an = scene_anchors(S) if S else None
            ans = []
            for i, p in enumerate(pins):
                if an is not None and p.get("at") not in an:
                    E("E-drill", qid, f"pin {i + 1}: anchor {p.get('at')} is not drawn by {S['id']}")
                a = p.get("answer")
                if not (is_int(a) and 0 <= a < len(opts)):
                    E("E-check", qid, f"pin {i + 1}: answer must be an option index")
                else:
                    ans.append(a)
            if len(set(ans)) != len(ans):
                E("E-drill", qid, "two pins share a label — each pin needs its own")
    elif ty == "trace":   # V3 (D-075): a marked cell's path in the scene; where does it end up?
        show_rules(q.get("show"), S, qid, E)
        alt()
        tid = q.get("tracer")
        T = next((p for p in S.get("parts", []) if p.get("kind") == "tracer" and p.get("id") == tid), None) if S else None
        if not (isinstance(tid, str) and tid.strip()):
            E("E-check", qid, "tracer must be the id of a scene tracer part")
        elif S and T is None:
            E("E-drill", qid, f"tracer {tid} is not a tracer part of {S['id']}")
        if q.get("ends") not in TRACE_IN:
            E("E-check", qid, f"ends must be where the path ends: {' · '.join(TRACE_IN)}")
        if "mask_day" in q and not isinstance(q["mask_day"], bool):
            E("E-check", qid, "mask_day must be true/false")
        P = (T.get("path") or []) if T else []
        sd = q["show"].get("day") if isinstance(q.get("show"), dict) else None
        if P and all(num(k.get("day")) for k in P) and num(sd):
            if not (P[0]["day"] <= sd <= P[-1]["day"]):
                E("E-drill", qid, f"show.day {sd} outside the path's days {P[0]['day']}–{P[-1]['day']}")
            else:
                at = [k for k in P if k["day"] <= sd + 1e-9][-1]
                if at.get("in") != "epiblast":
                    E("E-drill", qid, f"on show.day {sd} the cell has already left the epiblast — start where the path is still in it")
            if q.get("ends") in TRACE_IN and P[-1].get("in") != q["ends"]:
                E("E-drill", qid, f"ends {q['ends']} but the path ends in {P[-1].get('in')}")
        a = q.get("answer")
        if is_int(a) and 0 <= a < len(opts) and isinstance(opts[a], str) and opts[a].strip():
            w = opts[a].strip().lower()
            for f in ("prompt", "alt"):
                if w in str(q.get(f) or "").lower():
                    E("E-drill", qid, f"the right option '{opts[a]}' is in the {f} — answerable from the words (D-065)")
    elif ty == "folded":
        if not (len(opts) == 2 and all(isinstance(o, str) and o.strip() for o in opts)) or len(set(o.strip().lower() for o in opts if isinstance(o, str))) != len(opts):
            E("E-check", qid, "exactly 2 different options (e.g. Folded · Not yet folded)")
        its = q.get("items")
        lo, hi = DRILL["items"]
        if not (isinstance(its, list) and lo <= len(its) <= hi and all(isinstance(i, dict) for i in its)):
            E("E-check", qid, f"{lo}–{hi} items {{show, answer 0|1, text}}")
        else:
            for i, it in enumerate(its):
                if it.get("answer") not in (0, 1) or isinstance(it.get("answer"), bool):
                    E("E-check", qid, f"item {i + 1}: answer must be 0 or 1")
                tx = it.get("text")
                if not (isinstance(tx, str) and tx.strip()) or len(str(tx).split()) > DRILL["frame_words"]:
                    E("E-check", qid, f"item {i + 1}: text of 1–{DRILL['frame_words']} words needed (its text alternative)")
                show_rules(it.get("show"), S, qid, E, f"item {i + 1} show")
            if {it.get("answer") for it in its} != {0, 1}:
                E("E-check", qid, "items must use both answers (else it is guessable)")


def app_cite(cite):
    """'APP Deck' -> 'Deck' ('' for a bare APP); None if the cite is not an app cite (D-050)."""
    if not isinstance(cite, str):
        return None
    m = APP_RE.match(cite.strip().strip("[]").strip())
    return (m.group(1) or "") if m else None


def app_rules(cite, mk, line, guide, E):
    """Guide cards (D-050): a fact about the app cites APP <screen> and is marked ⓘ; checked against the app by the owner (T7)."""
    loc = app_cite(cite)
    if not guide:
        E("E-cite", line, "APP cites belong to guide cards only (kind: guide)")
    elif loc and loc not in APP_LOCS:
        E("E-cite", line, f"unknown app screen '{loc}' ({', '.join(APP_LOCS)})")
    if mk != "ⓘ":
        E("E-mark", line, "an APP cite is marked ⓘ")


def mark_rules(f, p, fid, card, src, final, E, W):
    mk = f.get("mark")
    if mk not in MARKS:
        E("E-mark", fid, f"mark missing or unknown ({' '.join(MARKS)})")
        return
    if mk == "ⓘ":
        E("E-mark", fid, "ⓘ needs an APP cite in a guide card")
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
    M = json.loads((ROOT / "content" / book / "map.json").read_text(encoding="utf-8"))
    sp = ROOT / "content" / book / "sources.json"
    return {"src": json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else build_sources(book),
            "map_ids": {c["id"] for c in M["concepts"]}, "map_terms": {c["id"]: c.get("terms", []) for c in M["concepts"]},
            "scenes": json.loads((ROOT / "content" / book / "scenes" / "index.json").read_text(encoding="utf-8"))["scenes"],
            "scene_files": {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "content" / book / "scenes").glob("sc-*.json")}}


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
    if not sp.exists() or {k: v for k, v in json.loads(sp.read_text(encoding="utf-8")).items()} != fresh:
        glob.append({"lvl": "E", "code": "E-sources", "line": "sources.json", "msg": "out of date — run with --write-sources"})
    cards = {}
    for p in files:
        try:
            cards[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            res[p.stem] = [{"lvl": "E", "code": "E-schema", "line": "file", "msg": f"not JSON: {e}"}]
            continue
        res[p.stem] = card_check(cards[p.stem], p.stem, ctx)
    ip = cdir / "index.json"
    if not a.only:
        idx = json.loads(ip.read_text(encoding="utf-8")) if ip.exists() else {"cards": []}
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
        c = json.loads(p.read_text(encoding="utf-8"))
        print(f"## {c['id']} · {c['title']} · {c['status']} v{c['version']}\nObjective: {c['objective'].get('text')}")
        for lvl, t in c["body"].items():
            print(f"\n[{lvl} · {words(t)}/{BUDGET.get(lvl, '?')} words]\n{strip_refs(t)}")
        print()
    return 0


def calibrate(a):
    src = build_sources(a.book)
    cal = json.loads((ROOT / "content" / a.book / "cards" / "calibration.json").read_text(encoding="utf-8"))
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
    st = json.loads((Path(__file__).resolve().parent / "selftest.json").read_text(encoding="utf-8"))
    ctx = load_ctx(a.book)
    base = json.loads((ROOT / "content" / a.book / "cards" / f"{st['base']}.json").read_text(encoding="utf-8"))
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
    cases = json.loads((Path(__file__).resolve().parent / "selftest.json").read_text(encoding="utf-8"))
    ctx = load_ctx(a.book)
    base = json.loads((ROOT / "content" / a.book / "cards" / f"{cases['base']}.json").read_text(encoding="utf-8"))
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
    for st in (sys.stdout, sys.stderr):   # Windows consoles default to cp1252: print ✓ ✗ ⚑ without -X utf8 / PYTHONUTF8
        try:
            st.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
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
        p.write_text(json.dumps(build_sources(a.book), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
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
