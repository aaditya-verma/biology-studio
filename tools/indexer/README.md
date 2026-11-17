# Book indexer (I1)

*(Purpose: turn any book PDF into derived index data, with no book text. Owner docs: `claude/README.md` (ids), `build/master-plan.md` §12. Updated: 17 Nov 2026 · Bio · Build · I1 index.)*

## Run (laptop, free tools)
1. `pip install pypdf` · Poppler for `pdftotext` (Windows: `conda install -c conda-forge poppler`).
2. Put the PDF anywhere local (never in the repo; RULES G1).
3. `python index_book.py --book books/E.json --pdf "<path>\Langmans Medical Embryology 14th Edition 2.pdf" --out ..\..\content\E\index`

Flags (RULES I5): `--dry-run` (no files written) · `--debug` (tagged `[tree] [terms] [pdf]` logs) · `--only <chapter no.>` · `--preview` (chapters 1–3).

## New book
Copy `books/E.json` to `books/<code>.json` (code from README). Edit the `_EDIT` keys: page offset, heading regex, box markers, glossary pages, index pages (or `null`), timeline pages, numeric tables, OCR fixes.

## Outputs (`content/<code>/index/`)
`tree.json` Part › Chapter › Section (`E05.02`), PDF + printed pages, boxes (Clinical Correlates / Molecular Regulation labels) · `terms.json` glossary term → chapters / sections / pages (`E.t.<slug>`) · `xrefs.json` section → section references + chapter × chapter shared terms · `timeline.json` day table + numeric tables (numbers only; Carnegie stage filled in X1) · `report.json` checks.

## Numbering
`.00` = chapter opener (text before the first ■ heading). `.01…` = each ■ heading in book order; Summary and Problems to Solve are the last two. Boxes and smaller subheads are not numbered; they belong to their section (K1 adds concepts `E05.02.01`).
