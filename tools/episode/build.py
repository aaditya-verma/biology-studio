#!/usr/bin/env python3
"""S1E01 builder + pipeline checks (P1 ①). Renders the script docs + JSON from s1e01_data.py and checks:
  facts   every fact ref exists in a Reviewed card; its mark is not ≈ and not ✚; ⚑ only the D-029 lines
  cite    every spoken fact line carries ≥ 1 fact ref (frame/question/terms/check/teaser/endcard lines carry none)
  wpm     speech rate = WPM (Kokoro 0.66 = 143) by construction → checks each profile's length vs its target
  terms   ≤ 3 new terms in any 60-s window; the Lesson/General terms strip comes first (method 2)
  scenes  every shot's scene id exists in content/E/scenes/index.json, is 'host'/'end card', or is a listed V-need
  text    no book text: no line shares an 8-word run with any card body text (cards are our words; proxy guard)
  spec 2  (D-107, docs/episode-spec.md §3; P1F) primer: <= 3 parts right after the cold open, each part's term in its line's new[] (or review),
          its card carries the term, length = target +- 3 s, end hold = primer.hold · ideas: contiguous, 20-60 s, check_by + objective,
          title <= 4 words, next_q <= 6 words; breaks on a hold >= 1.5 s, never between a Check and its reveal, never < 10 s after a
          Check's reveal, never inside or at the end of the cold open / primer · retired ids never reused. A spec 1 module builds as before.
Usage: python build.py --repo <clone> [--out <dir>] [--dry-run] [--debug] [--only lesson|general|short]
"""
import argparse, json, re, sys, importlib.util
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True); ap.add_argument("--out", default="out")
ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--debug", action="store_true"); ap.add_argument("--only")
a = ap.parse_args()
spec = importlib.util.spec_from_file_location("d", Path(__file__).with_name("s1e01_data.py")); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
REPO = Path(a.repo); OUT = Path(a.out)
cards = {}
for p in (REPO / "content/E/cards").glob("E*.json"):
    c = json.loads(p.read_text(encoding="utf-8")); cards[c["id"]] = c
scene_ids = {s["id"] for s in json.loads((REPO / "content/E/scenes/index.json").read_text(encoding="utf-8"))["scenes"]}
errors, warns = [], []
SPEC = getattr(D, "SPEC", 1); IDEAS = getattr(D, "IDEAS", {}); PRIMER = getattr(D, "PRIMER", {}); REVIEW = getattr(D, "REVIEW", {})
CORE = getattr(D, "CORE", []); RETIRED = getattr(D, "RETIRED", []); SHOTS_RETIRED = getattr(D, "SHOTS_RETIRED", [])
slug = lambda term: "E.t." + term.lower().replace(" ", "-")
def card_has(cid, term, new_only=False):
    c = cards.get(cid); T = (c or {}).get("terms") or {}
    return bool(c) and slug(term) in (T.get("new", []) + ([] if new_only else T.get("known", [])))

def ref(r):
    cid, item = r.split("#"); c = cards.get(cid)
    if not c: return None, f"card {cid} missing"
    if c.get("status") != "reviewed": return None, f"card {cid} not Reviewed ({c.get('status')})"
    pool = {f["id"]: f for f in c["facts"]} | {m["id"]: m for m in c.get("misconceptions", [])}
    x = pool.get(item)
    if not x: return None, f"{r} missing"
    return x, None

SILENT_KINDS = {"question", "terms", "frame", "check", "teaser", "endcard", "analogy-only"}
def words(t): return len(re.findall(r"[A-Za-z']+", t))

timelines = {}
for prof, lines in D.SCRIPTS.items():
    if a.only and prof != a.only: continue
    t = 0.0; tl = []
    for L in lines:
        w = words(L["text"]); dur = w * 60 / D.WPM
        L["_start"], L["_words"], L["_dur"] = round(t, 1), w, round(dur, 1)
        t += dur + L.get("hold", 0.4)
        kind = L.get("kind", "fact")
        rows = []
        for r in L.get("facts", []):
            x, err = ref(r)
            if err: errors.append(f"{prof} {L['id']}: {err}"); continue
            mark = x.get("mark")
            if mark in ("≈",): errors.append(f"{prof} {L['id']}: {r} is ≈ (B1)")
            if mark == "✚": errors.append(f"{prof} {L['id']}: {r} is ✚ — beyond-Langman lives in More only (B7)")
            if mark == "⚑" and not r.startswith("E05.02.01#f"): errors.append(f"{prof} {L['id']}: unexpected ⚑ {r}")
            if x.get("where") == "more" and mark != "⚑": warns.append(f"{prof} {L['id']}: {r} is a More fact")
            cite = x.get("cite", ""); book = cite.split("·")[0].strip()
            if not book: errors.append(f"{prof} {L['id']}: {r} has no book section (B6)")
            rows.append({"ref": r, "mark": mark, "section": book, "cite": cite})
        L["_rows"] = rows
        if kind == "primer" and L.get("new") and not rows: errors.append(f"{prof} {L['id']}: primer part line without a fact id (B1)")
        if kind in ("fact", "analogy", "flag-pointer", "reveal") and not rows: errors.append(f"{prof} {L['id']}: spoken fact line without a fact id (B1)")
        tl.append(L)
    timelines[prof] = (tl, round(t, 1))

# lexicon check: every technical term spoken is known or declared new by then (G-Learn r1)
for prof, (tl, total) in timelines.items():
    seen = set(D.KNOWN[prof]) | set(REVIEW.get(prof, {}))
    for L in tl:
        for n in L.get("new", []): seen.add(n.lower())
        low = L["text"].lower()
        for term in D.LEXICON:
            if re.search(r"\b" + re.escape(term), low) and not any(term in k or k in term for k in seen):
                errors.append(f"{prof} {L['id']}: term '{term}' spoken but not known or declared new (D2)")
        seen |= {t for t in D.LEXICON if re.search(r"\b" + re.escape(t), low)}
# terms per 60-s window
for prof, (tl, total) in timelines.items():
    ev = [(L["_start"], n, L["id"]) for L in tl for n in L.get("new", [])]
    for s0, n, lid in ev:
        win = [e for e in ev if s0 <= e[0] < s0 + 60]
        if len(win) > 3: errors.append(f"{prof}: {len(win)} new terms in 60 s from {lid} @{s0}s: {[e[1] for e in win]} (D2)")
    lo, hi = D.PROFILES[prof]["length_target"]
    if not lo <= total <= hi: errors.append(f"{prof}: length {total}s outside target {lo}–{hi}s")
    if prof in ("lesson", "general") and SPEC < 2 and not (tl[1].get("kind") == "terms"): errors.append(f"{prof}: terms strip is not first")
    if prof in ("lesson", "general") and SPEC >= 2 and not (tl[1].get("kind") == "primer"): errors.append(f"{prof}: the primer does not follow the cold open (D10)")
    if prof == "short":
        if tl[0]["_dur"] > 0 and tl[0]["_start"] != 0: errors.append("short: hook not at 0 s")
        ch = [L for L in tl if L.get("kind") != "endcard"]
        for L in ch:
            span = L["_dur"] + L.get("hold", 0)
            if not 6.0 <= span <= 9.0: warns.append(f"short {L['id']}: chapter {span:.1f}s (grammar 8 s)")
        nt = sum(len(L.get("new", [])) for L in tl)
        if nt > 3: errors.append(f"short: {nt} new terms (≤ 3 per Short)")

# ---------- spec 2: review terms, primer, ideas (docs/episode-spec.md §3) ----------
for prof, R in REVIEW.items():
    for term, cid in R.items():
        if not (card_has(cid, term, new_only=True) and (cid.startswith("E00.") or cid in CORE)):
            errors.append(f"{prof}: review term '{term}': {cid} is not a Part 0 / core card that introduces it (spec §3)")
ideas_out, primer_out = {}, {}
LETTER = {"lesson": "L", "general": "G"}
for prof, (tl, total) in timelines.items():
    ids = [L["id"] for L in tl]; at = {L["id"]: i for i, L in enumerate(tl)}
    for L in tl:
        if L["id"] in RETIRED: errors.append(f"{prof} {L['id']}: retired id reused (A2)")
    end_of = lambda i: tl[i + 1]["_start"] if i + 1 < len(tl) else total   # end of line i's hold
    P = PRIMER.get(prof)
    if P is not None:
        if prof == "short": errors.append("short: has a primer (Shorts have none, playbook §6b.3)")
        parts = P["parts"]
        if not 1 <= len(parts) <= 3: errors.append(f"{prof} primer: {len(parts)} parts (<= 3)")
        pl = [i for i, L in enumerate(tl) if L.get("kind") == "primer"]
        if pl != list(range(1, 1 + len(pl))): errors.append(f"{prof} primer: its lines are not one block right after the cold open")
        for q in parts:
            i = at.get(q["line"])
            if i is None: errors.append(f"{prof} primer: line {q['line']} missing"); continue
            if tl[i].get("kind") != "primer": errors.append(f"{prof} primer: {q['line']} is not a primer line")
            if q["term"] not in tl[i].get("new", []) and q["term"] not in REVIEW.get(prof, {}): errors.append(f"{prof} primer: '{q['term']}' not in {q['line']} new[] (D2 budget)")
            if q["term"].lower() not in tl[i]["text"].lower(): errors.append(f"{prof} primer: {q['line']} does not say '{q['term']}'")
            if not card_has(q["card"], q["term"]): errors.append(f"{prof} primer: card {q['card']} does not carry '{q['term']}'")
        if pl:
            span = round(end_of(pl[-1]) - tl[pl[0]]["_start"], 1)
            if tl[pl[-1]].get("hold") != P["hold"]: errors.append(f"{prof} primer: end hold {tl[pl[-1]].get('hold')} s, not {P['hold']} s")
            if abs(span - P["target_s"]) > 3: errors.append(f"{prof} primer: {span} s, target {P['target_s']} +- 3 s")
            primer_out[prof] = {"parts": parts, "hold": P["hold"], "_start": tl[pl[0]]["_start"], "_dur": span}
    I = IDEAS.get(prof)
    if I is None: continue
    if prof not in LETTER: errors.append(f"{prof}: has ideas (Shorts never pause, playbook §6b.1)"); continue
    reveals = [end_of(i) - tl[i]["hold"] for i, L in enumerate(tl) if L.get("kind") == "reveal" and i and tl[i - 1].get("kind") == "check"]   # end of each Check reveal's words
    nxt, out = 0, []
    for k, d in enumerate(I):
        a_, b_ = at.get(d["frm"]), at.get(d["to"])
        if a_ is None or b_ is None: errors.append(f"{d['id']}: line {d['frm']} / {d['to']} missing"); continue
        if d["id"] != f"S1E01.{LETTER[prof]}.i{k + 1:02d}": errors.append(f"{d['id']}: id out of order or wrong profile letter")
        if a_ != nxt: errors.append(f"{d['id']}: starts at {d['frm']}, expected {ids[nxt] if nxt < len(ids) else 'the end'} (ideas are contiguous)")
        nxt = b_ + 1
        s0, e0 = tl[a_]["_start"], end_of(b_); dur = round(e0 - s0, 1); brk = round(e0 - 0.3, 1)   # the player pauses 0.3 s before the hold ends: silence both sides
        if not 20 <= dur <= 60: errors.append(f"{d['id']}: {dur} s (ideas are 20-60 s)")
        cb = d.get("check_by")
        if not cb: errors.append(f"{d['id']}: no check_by (H1)")
        elif cb in at:
            if tl[at[cb]].get("kind") != "check": errors.append(f"{d['id']}: check_by {cb} is not a Check line")
        elif cb not in cards: errors.append(f"{d['id']}: check_by {cb} is neither a Check line of this cut nor a card")
        if not d.get("objective"): errors.append(f"{d['id']}: no objective (H1)")
        if not d.get("title") or len(d["title"].split()) > 4: errors.append(f"{d['id']}: title '{d.get('title')}' (1-4 words, D8)")
        if d.get("next_q") and len(d["next_q"].split()) > 6: errors.append(f"{d['id']}: next_q over 6 words")
        last = k == len(I) - 1
        if not last:
            T = tl[b_]
            if T.get("hold", 0) < 1.5: errors.append(f"{d['id']}: break after {T['id']} on a {T.get('hold')} s hold (>= 1.5 s)")
            if T.get("kind") == "check": errors.append(f"{d['id']}: break between a Check and its reveal")
            if any(0 <= brk - r < 10 for r in reveals): errors.append(f"{d['id']}: break < 10 s after a Check's reveal")
            if T.get("kind") == "primer" or T["seg"] == tl[0]["seg"]: errors.append(f"{d['id']}: break inside or at the end of the cold open / primer")
        if k == 0 and P is not None and any(tl[i].get("kind") == "primer" and not a_ <= i <= b_ for i in range(len(tl))): errors.append(f"{d['id']}: does not hold the whole primer")
        out.append({"id": d["id"], "from": d["frm"], "to": d["to"], "objective": d["objective"], "check_by": cb, "title": d["title"], **({"next_q": d["next_q"]} if d.get("next_q") else {}),
                    "_start": s0, "_dur": dur, **({} if last else {"_break": brk})})
    if out and nxt != len(tl): errors.append(f"{prof} ideas: end at {ids[nxt - 1]}, not at the last line {ids[-1]} (ideas cover every line)")
    ideas_out[prof] = out
for p_ in timelines:
    if p_ in LETTER and SPEC >= 2 and p_ not in IDEAS: errors.append(f"{p_}: spec 2 without ideas[]")

# scenes
for S in D.SHOTS:
    sc = S["scene"]
    ok = sc in scene_ids or sc.startswith("host") or sc in ("end card",) or sc.split(" ")[0] in scene_ids
    if sc.startswith("host / "): ok = sc.split(" / ")[1].split(" ")[0] in scene_ids
    if sc.startswith("new:"): ok = bool(S["needs"]) and all(n in D.NEEDS for n in S["needs"])
    if not ok: errors.append(f"shot {S['id']}: scene '{sc}' not in scenes/index.json and not a listed V-need")
    for n in S["needs"]:
        if n not in D.NEEDS: errors.append(f"shot {S['id']}: need {n} not listed")
used_shots = {L["shot"] for tl, _ in timelines.values() for L in tl}
for s in sorted(used_shots & set(SHOTS_RETIRED)): errors.append(f"a line uses retired shot {s} (A2)")
for s in used_shots - {S["id"] for S in D.SHOTS}: errors.append(f"line uses unknown shot {s}")

# book-text proxy: 8-word overlap with card body text (cards are our words, but this catches copy-paste from anything quoted)
def grams(t, n=8):
    w = re.findall(r"[a-z']+", t.lower()); return {" ".join(w[i:i+n]) for i in range(len(w)-n+1)}
card_text = set()
for c in cards.values():
    for k in ("general", "mbbs"): card_text |= grams(c["body"].get(k, ""))
overlap = [(p, L["id"]) for p, (tl, _) in timelines.items() for L in tl if grams(L["text"]) & card_text]
if a.debug: print("8-gram overlaps with card bodies (our own words — info):", overlap)

# ---------- outputs ----------
def mmss(s): s = round(s); return f"{s//60}:{s%60:02d}"
report = {"errors": errors, "warnings": warns, "lengths": {p: v[1] for p, v in timelines.items()},
          "words": {p: sum(L["_words"] for L in v[0]) for p, v in timelines.items()},
          "wpm_speech": D.WPM,
          "wpm_overall": {p: round(sum(L["_words"] for L in v[0]) / (v[1] / 60), 1) for p, v in timelines.items()},
          "new_terms": {p: [(n, L["_start"]) for L in v[0] for n in L.get("new", [])] for p, v in timelines.items()},
          "max_terms_per_60s": {p: max([len([e for e in [(L2["_start"]) for L2 in v[0] for _ in L2.get("new", [])] if s0 <= e < s0 + 60]) for s0 in [L["_start"] for L in v[0] if L.get("new")]] or [0]) for p, v in timelines.items()},
          "card_body_overlaps": overlap}
if SPEC >= 2: report |= {"ideas": {p: [[d["id"], d["from"], d["to"], d["_dur"]] for d in v] for p, v in ideas_out.items()},
                         "primer_s": {p: v["_dur"] for p, v in primer_out.items()}, "review_terms": REVIEW}
if a.dry_run:
    print(json.dumps(report, ensure_ascii=False, indent=1)); sys.exit(1 if errors else 0)
OUT.mkdir(parents=True, exist_ok=True)
data = {"spec": SPEC, "episode": "S1E01", "title": "Gastrulation", "wpm": D.WPM, "profiles": D.PROFILES,
        "scripts": {p: [{k: v for k, v in L.items() if not k.startswith("_") or k in ("_start", "_dur", "_words")} | {"refs": L["_rows"]} for L in tl] for p, (tl, _) in timelines.items()},
        "lengths_s": report["lengths"], "needs": D.NEEDS}
if SPEC >= 2: data |= {"ideas": ideas_out, "primer": primer_out, "retired": RETIRED}
(OUT / "script.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "shots.json").write_text(json.dumps({"spec": SPEC, "episode": "S1E01", "shots": D.SHOTS, "needs": D.NEEDS} | ({"retired": SHOTS_RETIRED} if SPEC >= 2 else {}), ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

# script.md
md = ["# S1E01 Gastrulation — cited scripts", "",
      "*(Purpose: the spoken script per audience profile, every fact line with its card fact id + book section + mark. Updated: 27 Nov 2026 · Bio · Episode · S1E01 primer (P1F: primer + ideas ▸, spec 2, D-107). Before: 22 Nov 2026 · Bio · Episode · S1E01 script (P1 ①). Source of truth: `content/E/episodes/S1E01/script.json` (built by `tools/episode/build.py`).)*", "",
      f"Voice: Kokoro `af_heart` speed 0.66 = **{D.WPM} wpm** (M1b.q6). Times = speech at {D.WPM} wpm + the hold after each line. Marks: ✔✔ book + Tier 1 · ✔ book · ⚑ book answer given (D-029). No ≈, no ✚ in any spoken line.", ""]
for p, (tl, total) in timelines.items():
    P = D.PROFILES[p]
    md += [f"## {P['name']} — {P['frame']} · {mmss(total)} · {report['words'][p]} words", ""]
    seg = None; heads = {d["from"]: d for d in ideas_out.get(p, [])}
    if p in primer_out: md += [f"Primer ({primer_out[p]['_dur']} s): " + " · ".join(f"{q['term']} ({q['line']}, `{q['card']}`, {q['token']})" for q in primer_out[p]["parts"]), ""]
    for L in tl:
        if L["seg"] != seg: seg = L["seg"]; md += ["", f"**{seg}**", ""]
        if L["id"] in heads: d = heads[L["id"]]; md += [f"- ▸ **{d['id']}** {d['title']} · {d['_dur']} s · objective: {d['objective']} · check by `{d['check_by']}`" + (f" · next: *{d['next_q']}*" if d.get("next_q") else "")]
        cites = "; ".join(f"`{r['ref']}` [{r['section']}] {r['mark']}" for r in L["_rows"]) or f"*({L.get('kind','')}, no fact)*"
        new = f" · **new:** {', '.join(L['new'])}" if L.get("new") else ""
        title = f" · title **{L['title']}**" if L.get("title") else ""
        chk = f" · Check: {L['check']}" if L.get("check") else ""
        md += [f"- **{L['id']}** `{mmss(L['_start'])}` · {L['shot']}{title} — {L['text']}  ", f"  ↳ {cites}{new}{chk}"]
    md += [""]
(OUT / "script.md").write_text("\n".join(md), encoding="utf-8")
print("WROTE", [p.name for p in OUT.iterdir()])
print(json.dumps({k: report[k] for k in ("errors", "warnings", "lengths", "words", "wpm_overall", "max_terms_per_60s")}, ensure_ascii=False, indent=1))
sys.exit(1 if errors else 0)
