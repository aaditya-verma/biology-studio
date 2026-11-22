"""Biology Studio — citations: validate_citation, the mark suggester and the sources.json look-up (docs/card-spec.md §1, §4; RULES B1, B6–B7).

validate_citation(cite, src) -> (errors, parsed) — section ids must exist in content/<book>/index/tree.json, R-ids in
research/source-registry.md (via sources.json, which build_sources() writes from those files + DECISIONS + terms.json).
The app has the same rules in src/js/15-cards.js (validateCitation, suggestMark); `check.py --parity` proves they agree.
EDIT: the grammar lives in SEC_RE / SRC_RE; tier headings in TIER_HEADS.
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


def parse_registry(md):
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
        short = re.split(r"\s[—–]\s|\. |\(", src)[0].strip()[:70]
        doi = re.search(r"doi:\s*(10\.\S+?)(?=[\s|,;]|$)", src)
        pmid = re.search(r"PMID\s*(\d+)", src)
        out.append({"id": m.group(1), "tier": tier, "name": short, "licence": lic[:80],
                    "ref_only": bool(re.search(r"\bNC\b|\bND\b|reference only|no reuse|Reference$|Historic", lic)),
                    "doi": doi.group(1).rstrip(".") if doi else None, "pmid": pmid.group(1) if pmid else None})
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
    return {"spec": 1, "book": book, "note": "Derived by tools/card-check --write-sources from source-registry.md, DECISIONS.md, index/tree.json, index/terms.json. Do not edit by hand.",
            "registry": reg, "decisions": dec, "chapters": chs, "sections": secs,
            "terms": {t["id"]: t["term"] for t in terms["terms"]}}


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
