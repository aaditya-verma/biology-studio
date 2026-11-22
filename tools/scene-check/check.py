#!/usr/bin/env python3
"""Biology Studio — scene-check (RULES C3): every scene file passes before it ships.

Checks content/<book>/scenes/*.json against docs/scene-spec.md (the only definition of the format, C2):
ids + file names + index, required fields, day keys (ascending; stage + size + cite + mark on each), layer tokens only
(no colour values anywhere — B3), parts/labels point at real layers, labels <= 3 words (D8), facts cited + marked (B1, B7),
disclaimers present (B2), cards exist in the K1 map, stamp size vs geometry (scale bar honesty, +-15 %), debug off (I5),
stills days inside the range (C11). V3 (D-075): `tracer` parts — a marked cell's path keyed by day; the path must sit inside the disc and
never run ahead of the tissue (sampled every 0.05 day against the same geometry as src/js/14-scene3d.mjs: outline, delays, sheet spread).

Run from the repo root:  python tools/scene-check/check.py [--only sc-E00.01.04] [--preview] [--debug] [--dry-run] [--book E] [--selftest]
  --preview  skip the map.json card lookup (fast)    --debug  print every check    --dry-run  list what would be checked
  --selftest broken copies of a real scene must each fail with the right message (CI)
Exit code 1 on any error. Writes out/scene-check/report.md. Owner doc: docs/scene-spec.md §9. EDIT: allowed values below.
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# EDIT: allowed values (keep in step with docs/scene-spec.md)
TOKENS = {"epi", "hypo", "ecto", "meso", "endo", "crest", "ctx", "guide"}   # no "accent": never a fill (B3) — use "ring": true (D-036)
MARKS = {"✔✔", "✔", "⚑", "✚", "≈"}
KINDS = {"disc", "notochord", "axes", "planes", "ruler", "tracer"}
TRACE_IN = {"epiblast", "streak", "mesoderm", "endoderm"}   # EDIT (V3): where a marked cell can be (spec §6 tracer)
TRACE_STEP = 0.05   # days between path samples
DISC_PIECES = {"epiblast", "hypoblast", "mesoderm", "endoderm", "streak", "node"}
PARAMS = {"length_units": (1e-6, 1e4), "width_ratio": (0.05, 1), "pear": (0, 0.6), "tip_frac": (0, 1), "meso": (0, 1), "endo": (0, 1),
          "streak_scale": (0.5, 4), "noto": (0, 1), "noto_plate": (0, 1), "noto_rod": (0, 1)}   # EDIT: allowed ranges (spec §6)
NOTO_PIECES = {"notochord", "prechordal"}
NOTO_ANCHORS = {"noto-cord", "noto-plate", "notochord", "prechordal"}
ID_RE = re.compile(r"^sc-(?:[A-Z]\d\d\.\d\d\.\d\d|S\d+E\d\d-\d\d)$")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?(?:[0-9a-fA-F]{2})?\b")
SIZE_TOL = 0.15


# ---------- geometry mirror of src/js/14-scene3d.mjs (keyState, delayed, outline, scaleFrom) — for tracer paths (V3) ----------
def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _lerp(a, b, t):
    return a + (b - a) * t


def key_state(S, day):
    K = S["days"]
    d = max(K[0]["day"], min(K[-1]["day"], day))
    i = 0
    while i < len(K) - 2 and d > K[i + 1]["day"]:
        i += 1
    a, b = K[i], K[min(i + 1, len(K) - 1)]
    span = b["day"] - a["day"]
    u = _smooth((d - a["day"]) / span) if span > 0 else 0
    pa = {}
    for j in range(i + 1):
        pa.update(K[j].get("params") or {})
    pb = dict(pa)
    pb.update(b.get("params") or {})
    p = {k: (_lerp(pa.get(k, v), v, u) if isinstance(v, (int, float)) else v) for k, v in pb.items()}
    return a, b, u, p


def delayed(S, day, disc):
    a, b, u, p = key_state(S, day)
    ka, kb = a.get("params") or {}, b.get("params") or {}
    pa = {}
    for k in S["days"]:
        if k["day"] > a["day"]:
            break
        pa.update(k.get("params") or {})
    for k, dly in (("meso", disc.get("meso_delay", 0)), ("endo", disc.get("endo_delay", 0))):
        if k not in kb and k not in ka:
            continue
        fr = pa.get(k, 0)
        to = kb.get(k, fr)
        t = max(0.0, min(1.0, (u - dly) / (1 - dly)))
        p[k] = _lerp(fr, to, t)
    return p


def _outline(L, wr, pear, n=96):
    import math
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x = (L / 2) * math.cos(a)
        pts.append((x, (wr * L / 2) * math.sin(a) * (1 + 0.5 * pear * (x / (L / 2)))))
    return pts


def _inside(poly, x, y):
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def tracer_where(S, disc, day, fx, fy):
    """→ (x, y) in units + what is drawn at that day: disc outline, mesoderm + endoderm sheets (None when not drawn), streak box, midline gap."""
    p = delayed(S, day, disc)
    L = p["length_units"]
    wr = p["width_ratio"]
    disc_poly = _outline(L, wr, p.get("pear", 0), disc.get("segments", 96))
    anc = -L / 2 + 0.03 * L

    def sc(k):
        return [(anc + k * (x - anc), k * y) for x, y in disc_poly]
    meso = sc(p.get("meso", 0) * 0.97) if p.get("meso", 0) > 0.02 else None
    endo = sc(p.get("endo", 0) * 0.97) if p.get("endo", 0) > 0.02 else None
    st = None
    if p.get("tip_frac", 0) > 0.02:
        k = p.get("streak_scale", 1)
        sd = disc.get("streak", {})
        nd = disc.get("node", {})
        st = (-L / 2 + sd.get("start_frac", 0) * L, -L / 2 + p["tip_frac"] * L + k * nd.get("radius", 0), k * sd.get("width", 0) / 2 * 1.55)   # x0, x1 (to the node's tip), half width with the lips (engine: w + 0.55 w)
    return fx * L / 2, fy * wr * L / 2, disc_poly, meso, endo, st, disc.get("meso_midline_gap", 0)


def check_tracer(S, p, disc, layer_by_id, lo, hi, err, say):
    tid = str(p.get("id", ""))
    if not re.match(r"^t-[a-z0-9-]+$", tid):
        err(f"tracer {tid}: id must be t-<lower-case letters, digits, dashes>")
    L = layer_by_id.get(p.get("layer"))
    if not L:
        err(f"tracer {tid}: layer `{p.get('layer')}` not in layers")
    elif not (L.get("drill") is True and L.get("token") == "ctx" and L.get("ring") is True):
        err(f"tracer {tid}: its layer must be drill-only (`drill: true`) with token ctx + ring (spec §5, B3: an accent ring, never a fill)")
    r = p.get("radius_mm", 0.006)
    if not (isinstance(r, (int, float)) and 0.002 <= r <= 0.02):
        err(f"tracer {tid}: radius_mm {r} outside 0.002–0.02")
    if "min_px" in p:
        if not (isinstance(p["min_px"], (int, float)) and 4 <= p["min_px"] <= 12):
            err(f"tracer {tid}: min_px outside 4–12")
        if not str(p.get("disclaimer", "")).strip():
            err(f"tracer {tid}: min_px draws the cell larger — a `disclaimer` must say so (B2)")
    P = p.get("path") or []
    if not isinstance(P, list) or len(P) < 2:
        err(f"tracer {tid}: path needs ≥ 2 keys")
        return
    prev = None
    for q in P:
        d = q.get("day")
        if not isinstance(d, (int, float)):
            err(f"tracer {tid}: a path key without a day")
            return
        if prev is not None and d <= prev:
            err(f"tracer {tid}: path days not ascending at {d}")
        prev = d
        if not lo - 1e-9 <= d <= hi + 1e-9:
            err(f"tracer {tid}: path day {d} outside the scene's days {lo}–{hi}")
        if q.get("in") not in TRACE_IN:
            err(f"tracer {tid}: day {d}: in `{q.get('in')}` not one of {' '.join(sorted(TRACE_IN))}")
        for ax in ("x", "y"):
            if not (isinstance(q.get(ax), (int, float)) and -1 <= q[ax] <= 1):
                err(f"tracer {tid}: day {d}: {ax} must be −1…1 (share of the half-length / half-width)")
    if any(not isinstance(q.get(ax), (int, float)) for q in P for ax in ("x", "y")) or any(q.get("in") not in TRACE_IN for q in P) or not disc:
        return
    if any(P[i + 1]["day"] <= P[i]["day"] for i in range(len(P) - 1)):
        return
    if P[0]["in"] != "epiblast":
        err(f"tracer {tid}: the path must start in the epiblast (all three layers come from it — card-spec §2a trace)")
    for q in P:   # every key on the disc; a streak key on the streak drawn that day
        x, y, dp, meso, endo, st, mg = tracer_where(S, disc, q["day"], q["x"], q["y"])
        if not _inside(dp, x, y):
            err(f"tracer {tid}: day {q['day']}: ({q['x']}, {q['y']}) is off the disc")
        if q["in"] == "streak" and not (st and st[0] <= x <= st[1] and abs(y) <= st[2]):
            err(f"tracer {tid}: day {q['day']}: an `in: streak` key must sit on the streak drawn that day")
    d, n = P[0]["day"], 0
    while d <= P[-1]["day"] + 1e-9:   # between two keys in the same sheet, the cell stays inside that sheet as drawn (never ahead of the tissue)
        i = 0
        while i < len(P) - 2 and d > P[i + 1]["day"]:
            i += 1
        a, b = P[i], P[i + 1]
        if a["in"] == b["in"] and a["in"] in ("mesoderm", "endoderm"):
            t = _smooth((d - a["day"]) / (b["day"] - a["day"]))
            x, y, dp, meso, endo, st, mg = tracer_where(S, disc, d, _lerp(a["x"], b["x"], t), _lerp(a["y"], b["y"], t))
            sheet = meso if a["in"] == "mesoderm" else endo
            if not sheet or not _inside(sheet, x, y) or (a["in"] == "mesoderm" and abs(y) < mg):
                err(f"tracer {tid}: day {round(d, 2)}: the cell is outside the {a['in']} drawn that day (the path runs ahead of the tissue)")
                break
            n += 1
        d += TRACE_STEP
    say(f"tracer {tid}: {len(P)} keys, {n} sheet samples inside")


def check_scene(path, S, concepts, dbg):
    E, W = [], []
    say = (lambda m: print("   ·", m)) if dbg else (lambda m: None)
    err = E.append
    sid = S.get("id", "?")
    for f in ("spec", "id", "version", "book", "cards", "title", "summary", "units", "days", "layers", "parts", "labels", "facts", "camera", "cut", "disclaimers", "debug"):
        if f not in S:
            err(f"missing field `{f}`")
    if E:
        return E, W
    if S["spec"] != 1:
        err(f"spec {S['spec']} (this checker knows 1)")
    if S["id"] != path.stem:
        err(f"id {S['id']} ≠ file name {path.stem}")
    if not ID_RE.match(S["id"]):
        err(f"id {S['id']} does not match sc-<card id> / sc-<episode>-<shot> (README)")
    if not (isinstance(S["version"], int) and S["version"] >= 1):
        err("version must be an int ≥ 1 (H7)")
    if not S["cards"]:
        err("cards: at least one")
    if concepts is not None:
        for c in S["cards"]:
            if c not in concepts:
                err(f"card {c} is not in map.json")
    say(f"cards {S['cards']}")
    mm = S["units"].get("mm_per_unit")
    if not (isinstance(mm, (int, float)) and mm > 0):
        err("units.mm_per_unit must be > 0")
        mm = 0.1
    # day keys (B2, B7)
    K = S["days"]
    if not K:
        err("days: at least one key")
    prev = None
    for k in K:
        d = k.get("day")
        if not isinstance(d, (int, float)):
            err(f"day key without a number: {k}")
            continue
        if prev is not None and d <= prev:
            err(f"day keys not ascending at {d}")
        prev = d
        if not re.match(r"^CS(0[1-9]|1\d|2[0-3])$", str(k.get("stage", ""))):
            err(f"day {d}: stage must be CS01–CS23")
        if not (isinstance(k.get("size_mm"), (int, float)) and k["size_mm"] > 0):
            err(f"day {d}: size_mm missing (B2)")
        if not str(k.get("cite", "")).strip():
            err(f"day {d}: cite missing (B1)")
        if k.get("mark") not in MARKS:
            err(f"day {d}: mark must be one of {' '.join(sorted(MARKS))} (B7)")
        if "fit_mm" in k and not (isinstance(k["fit_mm"], (int, float)) and k["fit_mm"] > 0):
            err(f"day {d}: fit_mm must be > 0 (spec §4)")
        for p, v in (k.get("params") or {}).items():
            if p not in PARAMS:
                err(f"day {d}: unknown param `{p}` (spec §6)")
            elif not (isinstance(v, (int, float)) and PARAMS[p][0] <= v <= PARAMS[p][1]):
                err(f"day {d}: {p} = {v} outside {PARAMS[p][0]}–{PARAMS[p][1]}")
    days = [k["day"] for k in K if isinstance(k.get("day"), (int, float))]
    lo, hi = (min(days), max(days)) if days else (0, 0)
    sd = S.get("start_day", lo)
    if not lo <= sd <= hi:
        err(f"start_day {sd} outside {lo}–{hi}")
    # layers (B3)
    ids = [l.get("id") for l in S["layers"]]
    if len(ids) != len(set(ids)):
        err("layer ids repeat")
    for l in S["layers"]:
        if l.get("token") not in TOKENS:
            err(f"layer {l.get('id')}: token `{l.get('token')}` not allowed (B3: {' '.join(sorted(TOKENS))})")
        if not str(l.get("label", "")).strip():
            err(f"layer {l.get('id')}: label missing (B3: colour + pattern + label)")
        if "ring" in l and not isinstance(l["ring"], bool):
            err(f"layer {l.get('id')}: ring must be true/false")
        if "drill" in l and not isinstance(l["drill"], bool):
            err(f"layer {l.get('id')}: drill must be true/false")
        op = l.get("opacity", 1)
        if not (isinstance(op, (int, float)) and 0.2 <= op <= 1):
            err(f"layer {l.get('id')}: opacity {op} outside 0.2–1")
    layer_ids = set(ids)
    layer_by_id = {l.get("id"): l for l in S["layers"]}
    drill_layers = {l.get("id") for l in S["layers"] if l.get("drill") is True}
    anchors = set()
    tracer_ids = []
    # parts
    for p in S["parts"]:
        k = p.get("kind")
        if k not in KINDS:
            err(f"part kind `{k}` unknown (spec §6)")
            continue
        if k == "disc":
            for piece, lid in (p.get("layers") or {}).items():
                if piece not in DISC_PIECES:
                    err(f"disc: unknown piece `{piece}`")
                if lid not in layer_ids:
                    err(f"disc: piece {piece} → layer `{lid}` not in layers")
                if lid in drill_layers:
                    err(f"disc: piece {piece} → drill-only layer `{lid}` (spec §5: drill layers draw only a drill's marked cell)")
                anchors.add(piece)
            for f in ("epiblast_thick", "gap", "hypoblast_thick", "streak", "node"):
                if f not in p:
                    err(f"disc: missing `{f}`")
            # stamp size vs geometry at every key (the scale bar must agree with the stamp)
            cur = {}
            for kk in K:
                cur.update(kk.get("params") or {})
                if "length_units" not in cur:
                    err(f"day {kk.get('day')}: disc needs length_units")
                    continue
                if not isinstance(cur["length_units"], (int, float)):
                    continue   # already reported by the param range check
                geo = cur["length_units"] * mm
                if kk.get("size_mm") and abs(geo - kk["size_mm"]) / kk["size_mm"] > SIZE_TOL:
                    err(f"day {kk['day']}: disc length {geo:.3f} mm vs stamp {kk['size_mm']} mm (> ±{int(SIZE_TOL*100)} %)")
                say(f"day {kk.get('day')}: geometry {geo:.3f} mm · stamp {kk.get('size_mm')} mm")
        elif k == "notochord":
            if not any(q.get("kind") == "disc" for q in S["parts"][:S["parts"].index(p)]):
                err("notochord: needs a disc part before it (it reads the node and outline)")
            for piece, lid in (p.get("layers") or {}).items():
                if piece not in NOTO_PIECES:
                    err(f"notochord: unknown piece `{piece}`")
                if lid not in layer_ids:
                    err(f"notochord: piece {piece} → layer `{lid}` not in layers")
            if "notochord" in (p.get("layers") or {}):
                anchors |= {"noto-cord", "noto-plate", "notochord"}
            if "prechordal" in (p.get("layers") or {}):
                anchors.add("prechordal")
            if not (isinstance(p.get("radius"), (int, float)) and p["radius"] > 0):
                err("notochord: radius must be > 0")
            z = p.get("zone", 0.12)
            if not (isinstance(z, (int, float)) and 0.02 <= z <= 0.4):
                err("notochord: zone outside 0.02–0.4")
            pc = p.get("prechordal") or {}
            if not (0 < pc.get("at_frac", 0) < 1 and 0 < pc.get("radius_frac", 0) < 0.2):
                err("notochord: prechordal{at_frac 0–1, radius_frac 0–0.2} needed")
            cur = {}
            for kk in K:
                cur.update(kk.get("params") or {})
                if cur.get("noto_rod", 0) > cur.get("noto_plate", 0) + 1e-9:
                    err(f"day {kk.get('day')}: noto_rod > noto_plate (a rod only forms from the plate, spec §6)")
        elif k == "tracer":
            before = [q for q in S["parts"][:S["parts"].index(p)] if q.get("kind") == "disc"]
            if not before:
                err("tracer: needs a disc part before it (it reads the outline, layer depths and streak)")
            tracer_ids.append(p.get("id"))
            anchors.add("tracer-" + str(p.get("id")))
            check_tracer(S, p, before[0] if before else None, layer_by_id, lo, hi, err, say)
        elif k == "axes":
            if p.get("layer") not in layer_ids:
                err("axes: layer missing")
            anchors |= {"axis-" + a for a in ("cranial", "caudal", "left", "right", "dorsal", "ventral")}
        elif k == "planes":
            for pl in p.get("planes", []):
                if pl.get("normal") not in ("x", "y", "z"):
                    err(f"plane {pl.get('id')}: normal must be x, y or z")
                if pl.get("layer") not in layer_ids:
                    err(f"plane {pl.get('id')}: layer missing")
                anchors.add("plane-" + str(pl.get("id")))
        elif k == "ruler":
            if p.get("layer") not in layer_ids:
                err("ruler: layer missing")
            for f in ("length_mm", "tick_mm", "at"):
                if f not in p:
                    err(f"ruler: missing `{f}`")
            anchors.add("ruler")
    if len(tracer_ids) != len(set(tracer_ids)):
        err("tracer ids repeat")
    # labels (D8)
    for l in S["labels"]:
        if l.get("layer") not in layer_ids:
            err(f"label `{l.get('text')}`: layer `{l.get('layer')}` not in layers")
        at = l.get("at", l.get("layer"))
        if at not in anchors:
            err(f"label `{l.get('text')}`: anchor `{at}` is drawn by no part")
        if len(str(l.get("text", "")).split()) > 3:
            err(f"label `{l.get('text')}`: more than 3 words (D8)")
        ld = l.get("days")
        if ld and not (isinstance(ld, list) and len(ld) == 2 and lo - 1e-6 <= ld[0] <= ld[1] <= hi + 1e-6):
            err(f"label `{l.get('text')}`: days {ld} outside {lo}–{hi}")
        if "priority" in l and not (isinstance(l["priority"], int) and l["priority"] >= 1):
            err(f"label `{l.get('text')}`: priority must be an int ≥ 1")
    for t in S.get("terms", []):
        if not str(t.get("term", "")).strip() or not str(t.get("text", "")).strip() or "mark" in t:
            err(f"term {t}: needs term + text, no mark (terms are not facts)")
    # facts (B1, B6–B7)
    if not S["facts"]:
        err("facts: at least one (About)")
    for f in S["facts"]:
        if not str(f.get("text", "")).strip() or not str(f.get("cite", "")).strip():
            err(f"fact without text or cite: {f}")
        if f.get("mark") not in MARKS:
            err(f"fact mark `{f.get('mark')}` not allowed")
        if f.get("mark") == "≈":
            W.append(f"≈ fact (labelled, blocks 'final'): {f.get('text')[:60]}")
    # camera, cut, disclaimers, stills, debug
    c = S["camera"]
    for f in ("azimuth_deg", "elevation_deg", "fit_mm"):
        if not isinstance(c.get(f), (int, float)):
            err(f"camera.{f} missing")
    if isinstance(c.get("fit_mm"), (int, float)) and c["fit_mm"] <= 0:
        err("camera.fit_mm must be > 0")
    if "phone" in c:   # L1F: phone-portrait start framing (scene-spec §3)
        ph = c["phone"]
        if not isinstance(ph, dict) or set(ph) - {"zoom", "shift", "pan"}:
            err("camera.phone must be {zoom, shift, pan}")
        else:
            if not (isinstance(ph.get("zoom", 1), (int, float)) and 1 <= ph.get("zoom", 1) <= 4):
                err("camera.phone.zoom must be 1–4")
            if not (isinstance(ph.get("shift", 0), (int, float)) and 0 <= ph.get("shift", 0) <= 0.3):
                err("camera.phone.shift must be 0–0.3")
            if not (isinstance(ph.get("pan", 0), (int, float)) and -0.3 <= ph.get("pan", 0) <= 0.3):
                err("camera.phone.pan must be −0.3…0.3")
    vids = []
    for v in S.get("views", []):
        vids.append(v.get("id"))
        if not re.match(r"^[a-z][a-z0-9-]*$", str(v.get("id", ""))):
            err(f"view {v.get('id')}: id must be lower-case letters, digits, dashes")
        if not (isinstance(v.get("azimuth_deg"), (int, float)) and isinstance(v.get("elevation_deg"), (int, float)) and -89 <= v["elevation_deg"] <= 89):
            err(f"view {v.get('id')}: azimuth_deg + elevation_deg −89…89 needed")
        if not str(v.get("label", "")).strip() or len(str(v.get("label", "")).split()) > 3:
            err(f"view {v.get('id')}: label of 1–3 words needed")
    if len(vids) != len(set(vids)):
        err("view ids repeat")
    cu = S["cut"]
    if cu.get("axis") not in ("x", "y") or not (isinstance(cu.get("at"), (int, float)) and -0.9 <= cu["at"] <= 0.9):
        err("cut: axis x|y and at −0.9…0.9")
    if not S["disclaimers"]:
        err("disclaimers: at least one (B2 — e.g. 'colours illustrative')")
    for d in S.get("stills", days):
        if not lo <= d <= hi:
            err(f"stills day {d} outside {lo}–{hi}")
    if S["debug"] is not False:
        err("debug must be false in a shipped scene (I5)")
    return E, W


def selftest(book):
    """Broken copies of the real trace scene must each fail with the right message; the original must pass (CI)."""
    import copy
    src = ROOT / "content" / book / "scenes" / "sc-E00.01.04.json"
    S0 = json.loads(src.read_text(encoding="utf-8"))

    def tr(S):
        return next(p for p in S["parts"] if p.get("kind") == "tracer")

    def path(i, **kv):
        return lambda S: tr(S)["path"][i].update(kv)
    cases = [
        ("original passes", lambda S: None, None),
        ("path starts outside the epiblast", path(0, **{"in": "mesoderm"}), "must start in the epiblast"),
        ("unknown in", path(2, **{"in": "notochord"}), "not one of"),
        ("path ahead of the tissue (endoderm far cranial on day 15.9)", path(3, x=0.7), "runs ahead of the tissue"),
        ("streak key off the streak", path(2, y=0.6), "must sit on the streak"),
        ("path days not ascending", path(2, day=15.2), "not ascending"),
        ("path day outside the scene", path(-1, day=18), "outside the scene's days"),
        ("off the disc", path(0, x=0.99, y=0.9), "off the disc"),
        ("x outside −1…1", path(1, x=1.4), "must be −1…1"),
        ("layer not drill-only", lambda S: next(l for l in S["layers"] if l["id"] == "tracer").pop("drill"), "drill-only"),
        ("min_px with no disclaimer", lambda S: tr(S).pop("disclaimer"), "disclaimer"),
        ("a disc piece on the drill layer", lambda S: S["parts"][0]["layers"].__setitem__("node", "tracer"), "drill-only layer"),
        ("tracer before the disc", lambda S: S["parts"].insert(0, S["parts"].pop()), "needs a disc part before it"),
        ("bad tracer id", lambda S: tr(S).__setitem__("id", "endo"), "id must be t-"),
        ("one path key", lambda S: tr(S).__setitem__("path", tr(S)["path"][:1]), "needs ≥ 2 keys"),
    ]
    ok = 0
    for name, f, want in cases:
        S = copy.deepcopy(S0)
        f(S)
        try:
            E, _ = check_scene(src, S, None, False)
        except Exception as ex:   # a crash is a failed case
            E = [f"crash {type(ex).__name__}: {ex}"]
        good = (not E) if want is None else any(want in e for e in E)
        ok += good
        print(("PASS " if good else "FAIL ") + name + ("" if good else f" — got {E[:3]}"))
    print(f"selftest: {ok}/{len(cases)}")
    return 0 if ok == len(cases) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", default="E")
    ap.add_argument("--only")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.book)
    sdir = ROOT / "content" / a.book / "scenes"
    files = sorted(p for p in sdir.glob("sc-*.json") if not a.only or p.stem == a.only)
    if a.dry_run:
        print(f"would check {len(files)} scene(s) in {sdir.relative_to(ROOT)}: " + ", ".join(p.stem for p in files))
        return 0
    concepts = None
    if not a.preview:
        m = json.loads((ROOT / "content" / a.book / "map.json").read_text(encoding="utf-8"))
        concepts = {c["id"] for c in m["concepts"]}
    errors, warns, lines = 0, 0, []
    idx = json.loads((sdir / "index.json").read_text(encoding="utf-8"))
    listed = {s["id"]: s for s in idx.get("scenes", [])}
    for p in files:
        raw = p.read_text(encoding="utf-8")
        try:
            S = json.loads(raw)
        except json.JSONDecodeError as ex:
            errors += 1
            lines.append(f"- **{p.stem}**: ❌ not valid JSON ({ex})")
            continue
        if a.debug:
            print(f"── {p.stem}")
        try:
            E, W = check_scene(p, S, concepts, a.debug)
        except Exception as ex:   # a malformed file is a report line, not a traceback
            E, W = [f"could not check: {type(ex).__name__}: {ex}"], []
        for m in HEX_RE.findall(raw):
            E.append(f"colour value {m} in the scene file — use a layer token (B3)")
        ent = listed.get(S.get("id"))
        if not ent:
            E.append("not listed in index.json")
        else:
            for f in ("title", "cards"):
                if ent.get(f) != S.get(f):
                    E.append(f"index.json {f} differs from the scene")
            if S.get("days") and ent.get("days") != [S["days"][0]["day"], S["days"][-1]["day"]]:
                E.append("index.json days differ from the scene's first/last key")
        errors += len(E); warns += len(W)
        lines.append(f"- **{p.stem}** v{S.get('version')}: " + ("✅" if not E else f"❌ {len(E)}") + (f" · {len(W)} note(s)" if W else ""))
        lines += [f"  - ❌ {e}" for e in E] + [f"  - ≈ {w}" for w in W]
    if not a.only:
        for sid in listed:
            if not (sdir / f"{sid}.json").exists():
                errors += 1
                lines.append(f"- ❌ index.json lists {sid} but the file is missing")
    out = ROOT / "out" / "scene-check"
    out.mkdir(parents=True, exist_ok=True)
    rep = f"# Scene check\n\n{len(files)} scene(s) · {errors} error(s) · {warns} note(s)\n\n" + "\n".join(lines) + "\n"
    (out / "report.md").write_text(rep, encoding="utf-8")
    print(rep)
    print(("FAIL" if errors else "PASS") + f": {errors} errors · report out/scene-check/report.md")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
