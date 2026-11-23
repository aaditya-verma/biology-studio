"""Biology Studio — citations: validate_citation, the mark suggester and the sources.json look-up (docs/card-spec.md §1, §4; RULES B1, B6–B7).

validate_citation(cite, src) -> (errors, parsed) — section ids must exist in content/<book>/index/tree.json, R-ids in
research/source-registry.md (via sources.json, which build_sources() writes from those files + DECISIONS + terms.json).
The app has the same rules in src/js/15-cards.js (validateCitation, suggestMark); `check.py --parity` proves they agree.
SR1 (D-098): each registry row also gets title, note (our one line), url (DOI first, else PubMed, else the row's checked
`url https://…`), pubmed, species (from our own words) and computed usedBy + chapters; link_errors() is the CI link check and
source_index_md() writes studio-docs/research/source-index.md (one anchor per source). card-spec.md §1a is the format.
EDIT: the grammar lives in SEC_RE / SRC_RE; tier headings in TIER_HEADS; species words in SPECIES; link shape in LINK_OK.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "studio-docs"
SEC_RE = re.compile(r"^(E\d\d)(?:\.(\d\d))?(?:\s+(.+))?$")          # E05.01 [locator] · E10 (chapter)
SRC_RE = re.compile(r"^(R\d\d[a-z]{0,2})(?:\s+(.+))?$")                  # R06 CS6 · R05b
# EDIT: registry section headings → tier
TIER_HEADS = [("## Tier 0", 0), ("## Tier 1", 1), ("## Tier 2", 2), ("## Tier 3", 3), ("## Curriculum", "C"), ("## Teaching-science", None), ("## Tools", None), ("## Not used", None)]


def _plain(s):
    return re.sub(r"[*_`]", "", s).strip()


# EDIT (SR1, D-098; G-Learn r1): species words looked for in the CITATION TITLE only (the registry has no species column; notes say
# things like "never a human day") — order = display order. An explicit `species mouse, chick` token in the row's Source cell wins.
SPECIES = [("human", r"\bhumans?\b|\bpatients?\b|\bwomen\b|\binfants?\b|\bnewborns?\b|\bpregnan|\bfetus|\bfetal\b|\bchildren\b|\bbirths?\b|\btrials?\b|\bprevalence\b|\bpopulation|\bpregnancy\b|\bneonat|\bpreeclampsia\b|\bfamilies\b|\brct\b|\bdeliveries\b|\bpreterm\b|\blive-?born\b|\bconception\b|\bsonar\b|\bultrasound\b|\bneural.tube defects?\b|\bdiaphragmatic hernia\b|\bteratoma\b|\bumbilical artery\b"),
           ("mouse", r"\bmouse\b|\bmice\b|\bmurine\b"), ("chick", r"\bchick\b|\bchicken\b|\bavian\b"), ("rat", r"\brats?\b"),
           ("zebrafish", r"\bzebrafish\b"), ("frog", r"\bxenopus\b|\bfrogs?\b"), ("pig", r"\bpigs?\b|\bporcine\b"),
           ("primate", r"\bmacaques?\b|\bmonkeys?\b|\bprimates?\b|\bmarmosets?\b"), ("cells", r"\bin vitro\b|\bpluripotent\b|\borganoids?\b|\bembryoids?\b|\bgastruloids?\b")]
SPECIES_TOK = re.compile(r"\bspecies\s+([a-z, ]+?)(?=\s+·|$)")
URL_RE = re.compile(r"\burl\s+(https?://[^\s|()]+)")


def _cut(t, n):
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0].rstrip(",;:·—– ") + "…"


def _title(src, cited):
    """the source cell without its link tokens (doi, PMID, PMC, url …) — the citation as we wrote it. A row with no DOI/PMID
    (an atlas, database, site, book) keeps only its name: the text before the first ' (' or sentence end (G-Learn r1)."""
    keep = [seg for seg in re.split(r"\s+·\s+", src) if not re.match(r"^(doi:|PMID|PMC|url\b|https?://)", seg.strip(), re.I)]
    t = re.sub(r"\s*doi:\s*10\.\S+", "", " · ".join(keep)).strip()
    if not cited:
        t = re.split(r"\s\(|\.\s", t)[0]
    t = t.rstrip(" .;,") + "."
    return t if len(t) <= 200 else _clause(t, 200)


# EDIT (SR1 G-Learn r1): working-note bits a learner never sees in a note — marks, decision ids, chapter tags, process codes, paths, section ids
NOTE_STRIP = [r"\([^()]*(?:[⚑✚✔≈]|D-\d{3}|\bCh \d+|\bX\d|\bK\d|\bI1\b|Tier [A-D]|§|\.json|\.md|\bE\d\d\.\d\d)[^()]*\)",
              r"[⚑✚✔≈]+", r"\bD-\d{3}(?: [a-z]\d?)?\b", r"\bCh(?:apter)? \d+\b", r"\b(?:K\d|X\d\w*|I1|Tier [A-D])\b",
              r"\S+\.(?:json|md|py)\b", r"§\s*\d+", r"\bE\d\d(?:\.\d\d){0,2}\b", r"\blabel species\b"]
NOTE_BAD = re.compile(r"[⚑✚✔≈]|\bD-\d{3}\b|\bCh \d+\b|\b(?:K\d|X\d\w*|I1)\b|\.json\b|\.md\b|§|\bE\d\d\.\d\d\b")


def _clause(t, n):
    """cut at a clause boundary (; or sentence end), never mid-word; a single long clause is cut at a word with …"""
    if len(t) <= n:
        return t
    for sep in (r"(?<=[;.])\s+", r"(?<=,)\s+"):   # G-Learn r2: a clause, else a comma-part, before a word cut
        out = ""
        for p in re.split(sep, t):
            if len(out) + len(p) + 1 > n:
                break
            out = (out + " " + p).strip()
        if len(out) >= 40:
            return out.rstrip(";,: ")
    return _cut(t, n)


def _note(use):
    """our one-line note: the first part of the Best-for / Use cell, cleaned of working-note bits (NOTE_STRIP) — our own words,
    never an abstract or a quote (RULES §G). A learner note in research/source-notes.json wins over it."""
    t = re.split(r"\s+·\s+|\s\*?Full text", use)[0]
    for rx in NOTE_STRIP:
        t = re.sub(rx, "", t)
    t = re.sub(r"\(\s*[,;:]?\s*\)", "", t)
    t = re.sub(r"\s+([,;:.)])", r"\1", re.sub(r"\s+", " ", t)).strip(" ;,:—–-")
    t = re.sub(r"^[;,:\s]+|[;,:\s]+$", "", t)
    t = re.sub(r"^\((?:[a-z, +]+)\)\s*[—–-]\s*", "", t, flags=re.I)   # G-Learn r2: a leading "(mouse) —" — the species tag already says it
    t = t[:1].upper() + t[1:]
    return _clause(t, 160)


def _notes():
    p = DOCS / "research" / "source-notes.json"
    return json.loads(p.read_text(encoding="utf-8")).get("notes", {}) if p.exists() else {}


NOTES = {}


def parse_registry(md):
    NOTES.clear()
    NOTES.update(_notes())
    out, tier = [], None
    for line in md.splitlines():
        for head, t in TIER_HEADS:
            if line.startswith(head):
                tier = t
        m = re.match(r"^\|\s*(R\d\d[a-z]{0,2})\s*\|(.+)\|\s*$", line)
        if not m or tier is None:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        src = _plain(cells[0])
        lic = _plain(cells[-1]) if len(cells) >= 3 else ""
        use = _plain(cells[1]) if len(cells) >= 2 else ""
        short = re.split(r"\s[—–]\s|\. |\(", src)[0].strip()[:70]
        doi = re.search(r"doi:\s*(10\.\S+)", src)   # G-Eng r1: a DOI ends only at whitespace — old SICI DOIs hold ';' '<' '>'
        pmid = re.search(r"PMID\s*(\d+)", src)
        doi = doi.group(1).rstrip(".,;") if doi else None
        pmid = pmid.group(1) if pmid else None
        web = URL_RE.search(src)
        pub = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None
        url = f"https://doi.org/{doi_url(doi)}" if doi else pub or (web.group(1).rstrip(".,;") if web else None)   # SR1: DOI first, else PubMed, else the row's checked web url
        cited = bool(doi or pmid)
        title = _title(src, cited)
        tl = re.sub(r"non-?human", "", (title + " " + re.split(r"[:;,.]", _plain(use))[0][:40]).lower())   # title + the note's opening words (e.g. "Mouse: …")
        tok = SPECIES_TOK.search(src)
        species = [x.strip() for x in tok.group(1).split(",") if x.strip()] if tok else [k for k, rx in SPECIES if re.search(rx, tl)]
        out.append({"id": m.group(1), "tier": tier, "name": short, "licence": lic[:80],
                    "ref_only": bool(re.search(r"\bNC\b|\bND\b|reference only|no reuse|Reference$|Historic", lic)),
                    "doi": doi, "pmid": pmid,
                    "title": title, "note": NOTES.get(m.group(1)) or _note(use), "url": url, "pubmed": pub,
                    "species": species})
    return out


def doi_url(doi):
    from urllib.parse import quote
    return quote(doi, safe="/:;()._-")


def _tp_plain(t):
    """G-Art r1: what a student reads about a tool — the plain part before the first bracket, dash or clause (hashes, rule ids,
    file paths and step codes stay in THIRD_PARTY.md, which the Tools tab links to)"""
    t = re.sub(r"[*`]", "", t)
    t = re.split(r"\s*\(|\s+—\s+|;\s", t)[0]
    t = re.sub(r"\s*(?:registry T\d+|RULES [A-I]\d+|D-\d{3}\S*)", "", t)
    return re.sub(r"\s+", " ", t).strip(" ;,:—–-")


def _third_party(md):
    """THIRD_PARTY.md first table (| Name | Used by | Licence | Lives |) → [{name, use, licence, lives}], shortened (the file stays
    the owner doc, RULES H10). Stops at the first line after that table that is not a row (G-Eng r1: the assets table is not tools)."""
    out, inside = [], False
    for line in md.splitlines():
        if line.startswith("| Name"):
            inside = True
            continue
        if not inside:
            continue
        if not line.startswith("|"):
            break
        if line.startswith("|---"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 4 and c[0] not in ("", "—", "-"):
            out.append({"name": _cut(_tp_plain(c[0]), 80), "use": _clause(_tp_plain(c[1]), 110), "licence": _clause(_tp_plain(c[2]), 90), "lives": _clause(_tp_plain(c[3]), 60)})
    return out


def _used_by(book, ids):
    """computed back-links per Rxx: cards (facts + misconceptions), lessons (through their cards), dossiers (any mention)"""
    cards = {}
    for p in sorted((ROOT / "content" / book / "cards").glob("*.json")):
        if p.stem in ("index", "calibration"):
            continue
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if c.get("status") == "retired":
            continue
        got = {}
        for x in c.get("facts", []) + c.get("misconceptions", []):
            for i in re.findall(r"R\d\d[a-z]{0,2}", str(x.get("cite") or "")):
                got.setdefault(i, set()).add(x.get("mark") or "≈")
        cards[p.stem] = got
    lessons = {}
    for p in sorted((ROOT / "content" / book / "lessons").glob("*.json")):
        try:
            L = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        lessons[p.stem] = {s.get("card") for st in L.get("sittings", []) for s in st.get("steps", [])}
    dos = {p.stem: set(re.findall(r"(?<![A-Za-z0-9])(R\d\d[a-z]{0,2})(?![a-z0-9])", p.read_text(encoding="utf-8")))
           for p in sorted((DOCS / "research" / "dossiers").glob("ch*.md"))}
    out = {}
    for i in ids:
        cs = sorted(k for k, v in cards.items() if i in v)
        mk = set().union(*[cards[k][i] for k in cs]) if cs else set()
        out[i] = {"cards": cs, "lessons": sorted(k for k, v in lessons.items() if v & set(cs)),
                  "dossiers": sorted(k for k, v in dos.items() if i in v),
                  "marks": [m for m in ("✔✔", "✔", "⚑", "✚", "≈") if m in mk]}   # the marks of the card lines that cite it (Research filter)
    return out


def build_sources(book="E"):
    """The derived look-up the app's Studio reads (no book text: headings + term names only, G1)."""
    tree = json.loads((ROOT / "content" / book / "index" / "tree.json").read_text(encoding="utf-8"))
    terms = json.loads((ROOT / "content" / book / "index" / "terms.json").read_text(encoding="utf-8"))
    reg = parse_registry((DOCS / "research" / "source-registry.md").read_text(encoding="utf-8"))
    dec = sorted(set(re.findall(r"^\|\s*(D-\d{3})\s*\|", (DOCS / "claude" / "DECISIONS.md").read_text(encoding="utf-8"), re.M)))
    secs, chs = {}, {}
    for c in tree["chapters"]:
        chs[c["id"]] = c["title"]
        for s in c["sections"]:
            secs[s["id"]] = s["title"]
    used = _used_by(book, [r["id"] for r in reg])
    for r in reg:   # SR1 (D-098): back-links + the chapters a source serves (its dossiers' chapters and its cards' chapters)
        r["usedBy"] = used[r["id"]]
        r["chapters"] = sorted({"E" + d[2:4] for d in r["usedBy"]["dossiers"]} | {c[:3] for c in r["usedBy"]["cards"]})
    tp = ROOT / "THIRD_PARTY.md"
    return {"spec": 1, "book": book, "note": "Derived by tools/card-check --write-sources from source-registry.md, DECISIONS.md, index/tree.json, index/terms.json, the cards, lessons, dossiers and THIRD_PARTY.md. Do not edit by hand.",
            "registry": reg, "decisions": dec, "chapters": chs, "sections": secs,
            "terms": {t["id"]: t["term"] for t in terms["terms"]},
            "third_party": _third_party(tp.read_text(encoding="utf-8")) if tp.exists() else []}


# EDIT (SR1): the shape a link may have — card-check checks it offline (E-link) on every push: the CI link check
LINK_OK = re.compile(r"^https://(doi\.org/10\.\d{4,9}/\S+|pubmed\.ncbi\.nlm\.nih\.gov/\d+/|[a-z0-9.-]+\.[a-z]{2,}(/\S*)?)$", re.I)


def link_errors(src):
    """every registry url/pubmed link is https and well formed; a DOI url matches its doi, a PubMed url its PMID"""
    errs = []
    for r in src["registry"]:
        for k in ("url", "pubmed"):
            u = r.get(k)
            if u and (not LINK_OK.match(u) or re.search(r"[<>\s\"']", u)):
                errs.append(f"{r['id']}: {k} '{u}' is not a well-formed https link")
        if r.get("doi") and r.get("url") != f"https://doi.org/{doi_url(r['doi'])}":
            errs.append(f"{r['id']}: url should be the DOI link")
        if r.get("pmid") and r.get("pubmed") != f"https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/":
            errs.append(f"{r['id']}: PubMed link does not match PMID {r['pmid']}")
    return errs


def source_index_md(src):
    """studio-docs/research/source-index.md — one anchor per Rxx (#r05f) with its DOI / PubMed / web link and back-links.
    The registry and the dossiers point here (SR1). Derived: written by --write-sources, checked by card-check (E-srcindex)."""
    L = ["# Source index — every registry source, linked", "",
         "*(Purpose: derived link page for `research/source-registry.md` — one anchor per source id (`source-index.md#r05f`), its DOI, PubMed or web link, "
         "and where it is used (dossiers, cards). Written by `python tools/card-check/check.py --write-sources` (SR1, D-098) — do not edit by hand; edit the registry row. "
         "Links + our own one-line note only — no abstracts or quotes (RULES §G).)*", ""]
    for r in src["registry"]:
        u = r["usedBy"]
        L.append(f"### {r['id']}")
        L.append(r["title"] + (f" — *{r['note']}*" if r.get("note") else ""))
        links = []
        if r.get("doi"):
            links.append(f"[DOI ↗]({r['url']})")
        elif r.get("url") and r["url"] != r.get("pubmed"):
            links.append(f"[Web ↗]({r['url']})")
        if r.get("pubmed"):
            links.append(f"[PubMed ↗]({r['pubmed']})")
        meta = [f"Tier {r['tier']}"] + ([", ".join(r["species"])] if r["species"] else []) + ([r["licence"]] if r.get("licence") else [])
        L.append("- " + " · ".join((links or ["no link"]) + meta))
        if u["dossiers"]:
            L.append("- Dossiers: " + ", ".join(f"[{d}](dossiers/{d}.md)" for d in u["dossiers"]))
        if u["cards"]:
            L.append("- Cards: " + ", ".join(u["cards"]))
        L.append("")
    return "\n".join(L)


def _loc_ok(loc):
    return loc is None or bool(re.match(r"^(CC|MR|Tbl \d+\.\d+|Fig \d+\.\d+|CS\d{1,2}(?:[–-]\d{1,2})?|p \d+)$", loc))


def parse_cite(cite):
    """'E05.01, E05.07 · R06 CS6, E10' -> {'sections':[...], 'sources':[...], 'xrefs':[...]} or raises ValueError."""
    if not isinstance(cite, str) or not cite.strip():
        raise ValueError("empty citation")
    c = cite.strip().strip("[]").strip()
    if re.search(r"E\d\d(?:\.\d\d)?\s*[–-]\s*\d", c):
        raise ValueError("no ranges — write each section (E05.01, E05.02)")
    parts = [p.strip() for p in c.split("·")]
    if len(parts) > 2:
        raise ValueError("one ' · ' only (sections · sources)")
    left = parts[0]
    right = parts[1] if len(parts) == 2 else ""
    out = {"sections": [], "sources": [], "xrefs": []}
    if left:
        for tok in [t.strip() for t in left.split(",")]:
            m = SEC_RE.match(tok)
            if not m:
                raise ValueError(f"'{tok}' is not a book section (E05.01)")
            if not _loc_ok(m.group(3)):
                raise ValueError(f"unknown locator '{m.group(3)}' (CC, Tbl 6.4, Fig 6.1, CS7)")
            out["sections"].append({"ch": m.group(1), "sec": m.group(1) + "." + m.group(2) if m.group(2) else None, "loc": m.group(3)})
    if right:
        for tok in [t.strip() for t in right.split(",")]:
            m = SRC_RE.match(tok)
            if m:
                if not _loc_ok(m.group(2)):
                    raise ValueError(f"unknown locator '{m.group(2)}' after {m.group(1)}")
                out["sources"].append({"id": m.group(1), "loc": m.group(2)})
                continue
            m = SEC_RE.match(tok)
            if m:
                out["xrefs"].append({"ch": m.group(1), "sec": m.group(1) + "." + m.group(2) if m.group(2) else None})
                continue
            raise ValueError(f"'{tok}' is not a registry source (R06 CS6) or a cross-chapter ref (E10)")
    if not out["sections"] and not out["sources"]:
        raise ValueError("cites nothing")
    return out


def validate_citation(cite, src):
    """-> (errors, parsed). src = build_sources() output."""
    try:
        p = parse_cite(cite)
    except ValueError as e:
        return [str(e)], None
    errs = []
    reg = {r["id"]: r for r in src["registry"]}
    for s in p["sections"] + p["xrefs"]:
        if s["sec"] and s["sec"] not in src["sections"]:
            errs.append(f"section {s['sec']} is not in index/tree.json")
        elif not s["sec"] and s["ch"] not in src["chapters"]:
            errs.append(f"chapter {s['ch']} is not in index/tree.json")
    for s in p["sources"]:
        if s["id"] not in reg:
            errs.append(f"{s['id']} is not in the source registry")
        elif s["id"] == "R00":
            errs.append("R00 is the book — cite its section instead")
    return errs, p


def suggest_mark(parsed, decision, src):
    """Mark suggester (card-spec §4): decision → ⚑; no book section → ✚; book + Tier 1 → ✔✔; else ✔."""
    if parsed is None:
        return "≈"
    if decision:
        return "⚑"
    if not parsed["sections"]:
        return "✚"
    reg = {r["id"]: r for r in src["registry"]}
    if any(reg.get(s["id"], {}).get("tier") == 1 for s in parsed["sources"]):
        return "✔✔"
    return "✔"
