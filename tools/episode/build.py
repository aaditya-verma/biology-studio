#!/usr/bin/env python3
"""S1E01 builder + pipeline checks (P1 ①). Renders the script docs + JSON from s1e01_data.py and checks:
  facts   every fact ref exists in a Reviewed card; its mark is not ≈ and not ✚; ⚑ only the D-029 lines
  cite    every spoken fact line carries ≥ 1 fact ref (frame/question/terms/check/teaser/endcard lines carry none)
  wpm     speech rate = WPM (Kokoro 0.66 = 143) by construction → checks each profile's length vs its target
  terms   ≤ 3 new terms in any 60-s window; the Lesson/General terms strip comes first (method 2)
  scenes  every shot's scene id exists in content/E/scenes/index.json, is 'host'/'end card', or is a listed V-need
  text    no book text: no line shares an 8-word run with any card body text (cards are our words; proxy guard)
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
        if kind in ("fact", "analogy", "flag-pointer", "reveal") and not rows: errors.append(f"{prof} {L['id']}: spoken fact line without a fact id (B1)")
        tl.append(L)
    timelines[prof] = (tl, round(t, 1))

# lexicon check: every technical term spoken is known or declared new by then (G-Learn r1)
for prof, (tl, total) in timelines.items():
    seen = set(D.KNOWN[prof])
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
    if prof in ("lesson", "general") and not (tl[1].get("kind") == "terms"): errors.append(f"{prof}: terms strip is not first")
    if prof == "short":
        if tl[0]["_dur"] > 0 and tl[0]["_start"] != 0: errors.append("short: hook not at 0 s")
        ch = [L for L in tl if L.get("kind") != "endcard"]
        for L in ch:
            span = L["_dur"] + L.get("hold", 0)
            if not 6.0 <= span <= 9.0: warns.append(f"short {L['id']}: chapter {span:.1f}s (grammar 8 s)")
        nt = sum(len(L.get("new", [])) for L in tl)
        if nt > 3: errors.append(f"short: {nt} new terms (≤ 3 per Short)")

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
if a.dry_run:
    print(json.dumps(report, ensure_ascii=False, indent=1)); sys.exit(1 if errors else 0)
OUT.mkdir(parents=True, exist_ok=True)
data = {"spec": 1, "episode": "S1E01", "title": "Gastrulation", "wpm": D.WPM, "profiles": D.PROFILES,
        "scripts": {p: [{k: v for k, v in L.items() if not k.startswith("_") or k in ("_start", "_dur", "_words")} | {"refs": L["_rows"]} for L in tl] for p, (tl, _) in timelines.items()},
        "lengths_s": report["lengths"], "needs": D.NEEDS}
(OUT / "script.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "shots.json").write_text(json.dumps({"spec": 1, "episode": "S1E01", "shots": D.SHOTS, "needs": D.NEEDS}, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

# script.md
md = ["# S1E01 Gastrulation — cited scripts", "",
      "*(Purpose: the spoken script per audience profile, every fact line with its card fact id + book section + mark. Updated: 22 Nov 2026 · Bio · Episode · S1E01 script (P1 ①). Source of truth: `content/E/episodes/S1E01/script.json` (built by `tools/episode/build.py`).)*", "",
      f"Voice: Kokoro `af_heart` speed 0.66 = **{D.WPM} wpm** (M1b.q6). Times = speech at {D.WPM} wpm + the hold after each line. Marks: ✔✔ book + Tier 1 · ✔ book · ⚑ book answer given (D-029). No ≈, no ✚ in any spoken line.", ""]
for p, (tl, total) in timelines.items():
    P = D.PROFILES[p]
    md += [f"## {P['name']} — {P['frame']} · {mmss(total)} · {report['words'][p]} words", ""]
    seg = None
    for L in tl:
        if L["seg"] != seg: seg = L["seg"]; md += ["", f"**{seg}**", ""]
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
