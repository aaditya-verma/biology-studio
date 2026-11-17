#!/usr/bin/env python3
"""index_book.py — I1 book indexer for Biology Studio (any book).

Purpose: turn a book PDF into DERIVED data only (no book sentences):
  tree.json      Part > Chapter > Section tree, page locators, <code><ch>.<sec> ids, boxes
  terms.json     glossary terms -> chapters / sections / pages (term map)
  xrefs.json     section -> section cross-reference graph (+ chapter x chapter shared terms)
  timeline.json  day table from the book's timeline pages + numeric tables (numbers only)
  report.json    checks: all chapters present, % glossary terms placed
Owner docs: claude/README.md (ids), build/master-plan.md §12 (I1). RULES G1-G3, I5, I6.

Needs: Python 3.10+, pypdf, poppler `pdftotext` (all free).
Usage:
  python index_book.py --book books/E.json --pdf "<path to pdf>" --out ../../content/E/index
  flags: --dry-run (no files written) --debug (verbose) --only <chapter no.> --preview (chapters 1-3)
"""
import argparse, json, os, re, subprocess, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

DBG = False
def log(area, *a):
    if DBG: print(f"[{area}]", *a, file=sys.stderr)

# ---------------------------------------------------------------- text
LIGS = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "’": "'", "‘": "'", "“": '"', "”": '"'}
def clean(s):
    for a, b in LIGS.items(): s = s.replace(a, b)
    return unicodedata.normalize("NFKC", s)

OCR_FIX = {}
ABBREV_SKIP = set()
def fix(s):
    for a, b in OCR_FIX.items(): s = s.replace(a, b)
    return s

def page_texts(pdf):
    """One string per PDF page (index 0 = pdf page 1)."""
    out = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, check=True).stdout
    pages = fix(clean(out.decode("utf-8", "replace"))).split("\f")
    return pages[:-1] if pages and not pages[-1].strip() else pages

def norm(s):
    """Lowercase search form: join hyphenated line breaks, collapse spaces."""
    s = re.sub(r"(\w)[-—–][ \t]*\n[ \t]*(\w)", r"\1\2", s)
    s = re.sub(r"[^\w]+", " ", s.lower())
    return " " + re.sub(r"\s+", " ", s).strip() + " "

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def titlecase(s):
    small = {"of", "and", "the", "to", "in", "a", "an", "from", "for", "with", "on", "at", "by"}
    w = re.sub(r"\s+", " ", s).strip().lower().split(" ")
    return " ".join(x if (i and x in small) else x[:1].upper() + x[1:] for i, x in enumerate(w))

# ---------------------------------------------------------------- tree
def outline_items(pdf):
    import pypdf
    r = pypdf.PdfReader(str(pdf))
    items = []
    def walk(o, d):
        for x in o:
            if isinstance(x, list): walk(x, d + 1)
            else:
                p = r.get_destination_page_number(x)
                items.append({"title": clean(x.title).strip(), "depth": d, "pdf": None if p is None else p + 1})
    walk(r.outline, 0)
    return items

def build_tree(cfg, pages, only=None, preview=False):
    items = [i for i in outline_items(cfg["_pdf"]) if i["pdf"]]
    off = cfg["page_offset"]
    parts, chapters, cur_part = [], [], None
    skip = set(cfg.get("skip_outline_titles", []))
    for k, it in enumerate(items):
        nxt = next((j["pdf"] for j in items[k + 1:] if j["pdf"] > it["pdf"]), len(pages) + 1)
        if re.match(cfg.get("parts_pattern", r"^Part \d"), it["title"]):
            cur_part = {"part": len(parts) + 1, "title": re.sub(r"^Part \d+\s*", "", it["title"]), "pdf_first": it["pdf"], "chapters": []}
            parts.append(cur_part)
        elif cur_part and it["depth"] >= 1 and it["title"] not in skip:
            n = len(chapters) + 1
            ch = {"ch": n, "id": f"{cfg['code']}{n:02d}", "title": it["title"], "part": cur_part["part"],
                  "pdf_first": it["pdf"], "pdf_last": nxt - 1}
            chapters.append(ch); cur_part["chapters"].append(ch["id"])
    hre = re.compile(cfg["heading"]["regex"])
    special = cfg["heading"]["special"]
    boxes = {k: re.compile(v) for k, v in cfg.get("boxes", {}).items()}
    upper = re.compile(r"^[A-Z0-9 ,:;'\-–—()/&]+$")
    rej = re.compile(cfg["heading"].get("reject_regex", r"(?!x)x"))
    tfix = cfg["heading"].get("title_fixes", {})
    def fix_title(t):
        t = " " + re.sub(r"\s+", " ", t) + " "
        for a, b in tfix.items(): t = t.replace(a, b)
        return t.strip()
    for ch in chapters:
        if only and ch["ch"] != only: continue
        if preview and ch["ch"] > 3: continue
        secs = [{"sec": 0, "id": f"{ch['id']}.00", "title": "Chapter opener", "kind": "opener",
                 "pdf_first": ch["pdf_first"], "boxes": []}]
        for p in range(ch["pdf_first"], ch["pdf_last"] + 1):
            lines = [l.strip() for l in pages[p - 1].split("\n")]
            i = 0
            while i < len(lines):
                l = lines[i]; kind = title = None
                m = hre.match(l)
                if m and (sum(c.isalpha() for c in m.group(1)) < cfg["heading"].get("min_letters", 3)
                          or rej.search(fix_title(m.group(1)))): m = None   # figure label, not a heading
                if m:
                    title, j = m.group(1), i + 1
                    while j < len(lines) and lines[j] and upper.match(lines[j]) and sum(c.isalpha() for c in lines[j]) >= 2:
                        title += " " + lines[j]; j += 1
                    kind, i, title = "section", j - 1, fix_title(title)
                else:
                    s = re.sub(r"^(?:I|l|\||■)\s+", "", l)
                    if s in special: kind, title = special[s], titlecase(s)
                if kind:
                    secs.append({"sec": len(secs), "id": f"{ch['id']}.{len(secs):02d}", "title": titlecase(title) if kind == "section" else title,
                                 "kind": kind, "pdf_first": p, "boxes": []})
                    log("tree", secs[-1]["id"], secs[-1]["title"], "pdf", p)
                else:
                    for bk, bre in boxes.items():
                        if bre.match(l):
                            secs[-1]["boxes"].append({"kind": bk, "pdf": p, "title": box_title(bk, l, lines[i + 1:i + 9])})
                i += 1
        for mh in cfg["heading"].get("manual", []):          # EDIT hook: headings OCR merged into body text
            if mh["chapter"] == ch["ch"]:
                secs.append({"sec": 0, "id": "", "title": titlecase(mh["title"]), "kind": "section", "pdf_first": mh["pdf"], "boxes": [], "manual": True})
        if any(s.get("manual") for s in secs):
            secs = [secs[0]] + sorted(secs[1:], key=lambda s: (s["pdf_first"], s["kind"] != "section", not s.get("manual")))
            order = {"section": 0, "summary": 1, "problems": 2}
            secs = [secs[0]] + sorted(secs[1:], key=lambda s: (order.get(s["kind"], 0), s["pdf_first"]))
            for n, s in enumerate(secs): s["sec"], s["id"] = n, f"{ch['id']}.{n:02d}"
        for a, b in zip(secs, secs[1:] + [None]):
            a["pdf_last"] = max(a["pdf_first"], (b["pdf_first"] if b else ch["pdf_last"] + 1) - (0 if b and b["pdf_first"] == a["pdf_first"] else 1)) if b else ch["pdf_last"]
            a["pages"] = [a["pdf_first"] - off, a["pdf_last"] - off]
        if len(secs) > 1 and secs[1]["pdf_first"] == ch["pdf_first"] and not secs[0]["boxes"]:
            secs[0]["note"] = "opener shares its first page with section 01"
        ch["pages"] = [ch["pdf_first"] - off, ch["pdf_last"] - off]
        ch["sections"] = secs
    return {"book": cfg["code"], "title": cfg["title"], "page_offset": off,
            "locator_note": "pdf = PDF page number; pages = printed page (pdf - offset). Titles are headings only (labels), no book text.",
            "parts": parts, "chapters": chapters}

def box_title(kind, line, nxt):
    """Short label of a box (navigation only). Molecular boxes carry the title in the line itself."""
    if kind == "molecular":
        t = line
        for x in nxt:
            if not x or len(x.split()) > 4 or not re.match(r"^[A-Za-z]", x): break
            if any(len(w) >= 4 and w[0].islower() for w in x.split()[1:]): break
            t += " " + x
        return re.sub(r"\s+", " ", t).strip()
    t = []
    for x in nxt:
        if not x:
            if t: break
            continue
        if not re.match(r"^[A-Z][A-Za-z ,:'()\-]+$", x) or len(x.split()) > 6: break
        if any(len(w) >= 4 and w[0].islower() for w in x.split()): break   # body text, not a label (RULES G1)
        t.append(x)
        if len(t) == 3: break
    t = " ".join(t)
    return t if sum(c.isalpha() for c in t) >= 4 else None

# ---------------------------------------------------------------- terms
_R = {}
def _reader(pdf):
    import pypdf
    if pdf not in _R: _R[pdf] = pypdf.PdfReader(str(pdf))
    return _R[pdf]

def column_lines(pdf, p, ncols, width=None, height=None):
    """Lines of one page read column by column (two-column glossaries)."""
    if not width:
        box = _reader(pdf).pages[p - 1].mediabox
        width, height = int(float(box.width)), int(float(box.height))
    w = width / ncols
    for c in range(ncols):
        out = subprocess.run(["pdftotext", "-enc", "UTF-8", "-f", str(p), "-l", str(p), "-x", str(int(c * w)), "-y", "0",
                              "-W", str(int(w)), "-H", str(height), str(pdf), "-"], capture_output=True, check=True).stdout
        yield from fix(clean(out.decode("utf-8", "replace"))).split("\n")

def parse_glossary(cfg, pages, body):
    """Glossary entries -> terms. A new entry = line after a full stop whose first letter matches the
    current letter header and sorts after the previous term (filters continuation sentences)."""
    g = cfg["glossary"]
    entries, prev_end, letter, prev = [], True, "A", ""
    for p in range(g["pdf_first"], g["pdf_last"] + 1):
        for l in column_lines(cfg["_pdf"], p, g.get("columns", 2), g.get("width"), g.get("height")):
            l = re.sub(r"^(?:[0-9|I'_.,-]\s+)(?=[A-Z])", "", l.strip())  # OCR junk before a term
            if not l or l.startswith("Glossary of Key Terms") or re.match(r"^Part \d", l): continue
            if re.fullmatch(r"[A-Z]", l): letter, prev_end = l, True; continue
            first = l.split()[0].lower()
            start = prev_end and l[0].isupper() and l[0].upper() in (letter, chr(ord(letter) + 1)) and first[:3] >= prev[:3]
            if start:
                letter = l[0].upper(); prev = first
                entries.append([p, l])
            elif entries:
                entries[-1][1] += " " + l
            prev_end = l.endswith(".") or l.endswith(".)")
    terms = []
    for p, text in entries:
        t = split_term(text, body)
        if t: terms.append({"term": t, "glossary_pdf": p})
        else: log("terms", "no term in:", text[:40])
    seen, out = set(), []
    for t in terms:
        k = slug(t["term"])
        if k and k not in seen:
            seen.add(k); out.append(t)
    return out

def split_term(text, body):
    """Return the term at the start of a glossary entry (the definition is NOT kept)."""
    w = text.split()
    best = None
    for k in range(1, min(7, len(w))):
        cand = w[:k]; j = k
        if j < len(w) and w[j].startswith("("):
            while j < len(w) and not w[j].endswith(")"): j += 1
            j += 1
            cand = w[:j]
        if j >= len(w): break
        nxt = w[j]
        if not nxt[:1].isupper(): continue
        c = " ".join(cand)
        if best is None: best = c
        if variants(c) and any(v in body for v in variants(c)): best = c
    return best.rstrip(",;:") if best else None

def variants(term):
    t = term.lower()
    out = set()
    base = re.sub(r"\s*\([^)]*\)\s*", " ", t).strip()
    for par in re.findall(r"\(([^)]*)\)", term):
        p = par.strip()
        # alone only if an abbreviation (AER) or 2+ words (lesser peritoneal sac); single words like "plate" over-match
        if len(p) >= 2 and p.lower() not in ABBREV_SKIP and (any(c.isupper() for c in p) or len(p.split()) >= 2):
            out.add(p.lower())
        out.add(re.sub(r"\s*\([^)]*\)\s*", " " + p.lower() + " ", t).strip())
    out.add(base)
    for v in list(out):
        out.add(v + "s"); out.add(v + "es")
        if v.endswith("um"): out.add(v[:-2] + "a")
        if v.endswith("us"): out.add(v[:-2] + "i")
        if v.endswith("is"): out.add(v[:-2] + "es")
        if v.endswith("s"): out.add(v[:-1])
    return {" " + re.sub(r"[^\w]+", " ", v).strip() + " " for v in out if len(v.strip()) >= 3}

def place_terms(cfg, terms, tree, pages):
    code = cfg["code"]
    secpage = {}
    for ch in tree["chapters"]:
        for s in ch.get("sections", []):
            for p in range(s["pdf_first"], s["pdf_last"] + 1): secpage.setdefault(p, s["id"])
    pnorm = {p: norm(pages[p - 1]) for p in secpage}
    chpages = {c["id"]: c["pdf_last"] - c["pdf_first"] + 1 for c in tree["chapters"]}
    for t in terms:
        vs = variants(t["term"])
        hits = defaultdict(int)
        for p, txt in pnorm.items():
            n = sum(txt.count(v) for v in vs)
            if n: hits[p] = n
        bysec, bych = Counter(), Counter()
        for p, n in hits.items():
            bysec[secpage[p]] += n; bych[secpage[p][:len(code) + 2]] += n
        t["id"] = f"{code}.t.{slug(t['term'])}"
        t["hits"] = sum(hits.values())
        t["chapters"] = dict(sorted(bych.items()))
        t["sections"] = dict(sorted(bysec.items()))
        t["pdf_pages"] = sorted(hits)
        dens = {c: n / chpages[c] ** 0.5 for c, n in bych.items()}
        t["primary_chapter"] = max(dens, key=lambda c: (dens[c], -int(c[len(code):]))) if bych else None
        prim = {s: n for s, n in bysec.items() if t["primary_chapter"] and s.startswith(t["primary_chapter"])}
        t["primary_section"] = max(prim, key=lambda s: (prim[s], s)) if prim else None
        t["placed"] = bool(hits)
        log("terms", t["id"], t["hits"], t["primary_section"])
    return terms

# ---------------------------------------------------------------- xrefs
def build_xrefs(cfg, tree, pages, terms):
    code, off = cfg["code"], cfg["page_offset"]
    secs = [s for ch in tree["chapters"] for s in ch.get("sections", [])]
    sec_of = {}
    for s in secs:
        for p in range(s["pdf_first"], s["pdf_last"] + 1): sec_of.setdefault(p, s["id"])
    fig_page, tab_page = {}, {}
    for p in sec_of:
        for m in re.finditer(r"FIGURE (\d+)\.(\d+)", pages[p - 1]): fig_page.setdefault((int(m[1]), int(m[2])), p)
        for m in re.finditer(r"^Table (\d+)\.(\d+)\s*$", pages[p - 1], re.M): tab_page.setdefault((int(m[1]), int(m[2])), p)
    edges = defaultdict(Counter)
    for p, src in sec_of.items():
        chn = int(src[len(code):len(code) + 2])
        txt = re.sub(r"^\s*Chapter\s*\d+\s*-.*$", "", pages[p - 1], flags=re.M)        # drop running header
        txt = re.sub(r"^FIGURE \d+\.\d+.*$", "", txt, flags=re.M)                       # captions are not references
        for m in re.finditer(r"\bp(?:p)?\.\s?(\d{1,3})\b", txt):
            tp = int(m[1]) + off
            if tp in sec_of: edges[(src, sec_of[tp])]["page"] += 1
        for m in re.finditer(r"\bChapters? (\d{1,2})\b", txt):
            n = int(m[1])
            if 1 <= n <= len(tree["chapters"]) and n != chn: edges[(src, f"{code}{n:02d}")]["chapter"] += 1
        for kind, rx, where in (("figure", r"\bFigs?\.\s?(\d{1,2})\.(\d{1,2})", fig_page), ("table", r"\bTables? (\d{1,2})\.(\d{1,2})", tab_page)):
            for m in re.finditer(rx, txt):
                key = (int(m[1]), int(m[2]))
                if key[0] != chn:
                    tgt = sec_of.get(where.get(key)) or f"{code}{key[0]:02d}"
                    edges[(src, tgt)][kind] += 1
    out = [{"from": a, "to": b, "n": sum(c.values()), "by": dict(c)} for (a, b), c in edges.items() if a != b]
    log("xrefs", len(out), "edges")
    out.sort(key=lambda e: (e["from"], -e["n"]))
    chs = [c["id"] for c in tree["chapters"] if c.get("sections")]
    shared = {a: {b: 0 for b in chs} for a in chs}
    for t in terms:
        cs = [c for c, n in t.get("chapters", {}).items() if n >= 1 and c in shared]
        for a in cs:
            for b in cs:
                if a != b: shared[a][b] += 1
    return {"book": code, "note": "edges from explicit references in the text (page, chapter, figure, table). chapter_shared_terms = glossary terms found in both chapters.",
            "edges": out, "chapter_shared_terms": shared}

# ---------------------------------------------------------------- timeline
def cs_label(cfg, d0, d1):
    """Carnegie stage(s) for a day range from the config's stage table (X1, D-030); None if no table. EDIT: carnegie.json."""
    if not cfg.get("carnegie"): return None
    tab = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), cfg["carnegie"]), encoding="utf-8"))["stages"]
    hit = [s["cs"] for s in tab if s["day_from"] <= d1 and d0 <= s["day_to"]]
    return "/".join(f"CS{n:02d}" for n in hit) or None

def build_timeline(cfg, pages, terms):
    tl = cfg["timeline"]; rx = re.compile(tl["day_regex"])
    tvar = [(t, variants(t["term"])) for t in terms]
    days = []
    for p in range(tl["pdf_first"], tl["pdf_last"] + 1):
        for m in rx.finditer(pages[p - 1]):
            cap = norm(m[3])
            linked = [t["id"] for t, vs in tvar if any(v in cap for v in vs)]
            d0 = int(m[1]); d1 = int(m[2]) if m[2] else d0
            log("timeline", "day", d0, d1, linked)
            days.append({"day_from": d0, "day_to": d1, "week": (d0 - 1) // 7 + 1, "cs": cs_label(cfg, d0, d1),
                         "terms": linked, "sections": sorted({t["primary_section"] for t in terms if t["id"] in linked and t.get("primary_section")}),
                         "pdf": p})
    days.sort(key=lambda d: d["day_from"])
    tables = []
    alltxt = "\n".join(pages)
    for t in cfg.get("numeric_tables", []):
        m = re.search(t["start"], alltxt, re.M)
        if not m: tables.append({"id": t["id"], "error": "not found"}); continue
        nums, started = [], False
        for l in alltxt[m.end():].split("\n")[1:200]:
            l = l.strip()
            if not l: continue
            if re.fullmatch(r"\d{1,4}(?:\s?[—–-]\s?\d{1,4})?", l):
                started = True
                a = [int(x) for x in re.split(r"\s?[—–-]\s?", l)]
                nums.append(a if len(a) > 1 else a[0])
            elif started: break
        k = len(t["cols"])
        rows = [dict(zip(t["cols"], nums[i:i + k])) for i in range(0, len(nums) - k + 1, k)]
        tab = {"id": t["id"], "label": t["label"], "rows": rows}
        if t.get("expected_rows") and len(rows) < t["expected_rows"]:
            tab["incomplete"] = f"{len(rows)}/{t['expected_rows']} rows read (OCR); finish by hand from the book"
        log("timeline", t["id"], len(rows), "rows")
        tables.append(tab)
    return {"book": cfg["code"], "note": "numbers only; cs = Carnegie stage(s) for the day from the config's stage table (R08 via carnegie.json, D-030; GLOSSARY §7); 'CS06/CS07' = overlapping ranges. Event labels are NOT stored; 'terms' are our glossary ids found in the chart caption.",
            "days": days, "tables": tables}

# ---------------------------------------------------------------- main
def main():
    global DBG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", required=True); ap.add_argument("--pdf", required=True); ap.add_argument("--out", default="out")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--debug", action="store_true")
    ap.add_argument("--only", type=int, help="chapter number"); ap.add_argument("--preview", action="store_true", help="chapters 1-3 only")
    a = ap.parse_args(); DBG = a.debug
    cfg = json.loads(Path(a.book).read_text(encoding="utf-8")); cfg["_pdf"] = a.pdf
    OCR_FIX.update(cfg.get("ocr_fixes", {})); ABBREV_SKIP.update(cfg.get("abbrev_skip", []))
    pages = page_texts(a.pdf)
    log("pdf", len(pages), "pages")
    tree = build_tree(cfg, pages, a.only, a.preview)
    body = norm("\n".join(pages[p - 1] for c in tree["chapters"] for p in range(c["pdf_first"], c["pdf_last"] + 1)))
    terms = place_terms(cfg, parse_glossary(cfg, pages, body), tree, pages) if cfg.get("glossary") else []
    xrefs = build_xrefs(cfg, tree, pages, terms)
    timeline = build_timeline(cfg, pages, terms) if cfg.get("timeline") else {"book": cfg["code"], "days": [], "tables": []}
    n_ch = len(tree["chapters"]); placed = sum(t["placed"] for t in terms)
    report = {"book": cfg["code"], "chapters_found": n_ch, "chapters_indexed": sum(1 for c in tree["chapters"] if c.get("sections")),
              "sections": sum(len(c.get("sections", [])) for c in tree["chapters"]),
              "boxes": Counter(b["kind"] for c in tree["chapters"] for s in c.get("sections", []) for b in s["boxes"]),
              "glossary_terms": len(terms), "placed": placed, "placed_pct": round(100 * placed / max(1, len(terms)), 1),
              "unplaced": [t["term"] for t in terms if not t["placed"]],
              "xref_edges": len(xrefs["edges"]), "timeline_days": len(timeline["days"]),
              "index_pages": "missing from PDF" if not cfg.get("index") else "used",
              "check_chapters_ok": n_ch == 21 if cfg["code"] == "E" else None,
              "check_glossary_ok": placed / max(1, len(terms)) >= 0.9}
    print(json.dumps({k: v for k, v in report.items() if k != "unplaced"}, indent=1, default=dict))
    old = Path(a.out) / "tree.json"                       # RULES A2: ids are permanent — warn on any change
    if old.exists() and not (a.only or a.preview):
        prev = {s["id"]: s["title"] for c in json.loads(old.read_text(encoding="utf-8"))["chapters"] for s in c.get("sections", [])}
        now = {s["id"]: s["title"] for c in tree["chapters"] for s in c.get("sections", [])}
        moved = [f"{k}: {prev[k]!r} -> {now.get(k)!r}" for k in prev if now.get(k) != prev[k]]
        report["id_changes"] = moved
        if moved: print(f"[ids] WARNING {len(moved)} section ids changed vs existing tree.json — log a decision before shipping:", *moved[:10], sep="\n  ")
    if a.dry_run: print("[dry-run] nothing written"); return
    out = Path(a.out)
    if a.only or a.preview:
        out = out / "partial"; print("[partial run] writing to", out, "(full outputs untouched)")
    out.mkdir(parents=True, exist_ok=True)
    for name, obj in (("tree", tree), ("terms", {"book": cfg["code"], "source": "Glossary of Key Terms (terms only, no definitions)", "terms": terms}),
                      ("xrefs", xrefs), ("timeline", timeline), ("report", report)):
        (out / f"{name}.json").write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=dict), encoding="utf-8")
    print("wrote", out)

if __name__ == "__main__":
    main()
