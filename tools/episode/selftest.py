"""S1E01 builder selftest (P1F, D-107): mutation tests for build.py's spec-2 checks: each case edits a copy of s1e01_data.py and expects the named error (or a clean build).
Usage: python tools/episode/selftest.py (exit 1 on any failed case). EDIT: CASES below."""
import shutil, subprocess, sys, json, os, re
from pathlib import Path
SRC = Path(__file__).resolve().parent; REPO = SRC.parents[1]
import tempfile; T = Path(tempfile.mkdtemp(prefix='ep-selftest-')) / 'mut'
base = (SRC / 's1e01_data.py').read_text(encoding='utf-8')
spec1 = (lambda s: s[:s.index('# ---------------- Spec 2')])(base)
spec1 = spec1.replace('dict(id="L02b", seg="Open", shot="S02b", text="To answer that, meet three parts first.", facts=[], hold=0.3, kind="primer"),',
  'dict(id="L02", seg="Open", shot="S02b", text="Three terms first: germ layers, primitive node, notochord.", facts=[], new=["germ layers", "primitive node", "notochord"], hold=1.0, kind="terms"),')
spec1 = re.sub(r'  dict\(id="L02[cde]".*\n', '', spec1)
spec1 = spec1.replace('dict(id="G02b", seg="Open", shot="S02e", text="To answer that, meet three parts first.", facts=[], hold=0.3, kind="primer"),',
  'dict(id="G02", seg="Open", shot="S02e", text="Three words first: epiblast, primitive streak, gastrulation.", facts=[], new=["epiblast", "primitive streak", "gastrulation"], hold=1.0, kind="terms"),')
spec1 = re.sub(r'  dict\(id="G02[cde]".*\n', '', spec1)
CASES = [
  ('spec 1 file still builds', lambda s: spec1, None),
  ('idea over 60 s', lambda s: s.replace('to="L04"', 'to="L08"').replace('frm="L05", to="L08"', 'frm="L09", to="L09"').replace('frm="L09", to="L12"', 'frm="L10", to="L12"'), '20-60 s'),
  ('gap between ideas', lambda s: s.replace('frm="L09", to="L12"', 'frm="L10", to="L12"'), 'contiguous'),
  ('missing check_by', lambda s: s.replace('check_by="L32", title="The first cells in"', 'check_by="", title="The first cells in"'), 'no check_by'),
  ('check_by not a check', lambda s: s.replace('check_by="L32"', 'check_by="L30"'), 'not a Check line'),
  ('break on a short hold', lambda s: s.replace('frm="L18", to="L22"', 'frm="L18", to="L21"').replace('frm="L23"', 'frm="L22"'), '>= 1.5 s'),
  ('break between Check and reveal', lambda s: s.replace('frm="G13", to="G17", ', 'frm="G13", to="G15", objective="x", check_by="G16", title="x"), dict(id="S1E01.G.i05", frm="G16", to="G17", '), 'between a Check'),
  ('break inside the primer', lambda s: s.replace('frm="L01", to="L04"', 'frm="L01", to="L02e"').replace('frm="L05", to="L08"', 'frm="L03", to="L08"'), 'cold open'),
  ('title too long', lambda s: s.replace('title="The groove")', 'title="The groove marks the axis")'), '1-4 words'),
  ('primer term not new', lambda s: s.replace('new=["notochord"], hold=2.0', 'hold=2.0'), "not in L02e new[]"),
  ('primer end hold', lambda s: s.replace('new=["notochord"], hold=2.0', 'new=["notochord"], hold=1.0'), 'end hold'),
  ('four parts', lambda s: s.replace('{"term": "notochord"', '{"term": "germ layers", "line": "L02c", "card": "E05.01.01", "token": "x", "view": "x"}, {"term": "notochord"'), '4 parts'),
  ('review term not Part 0/core', lambda s: s.replace('"gastrulation": "E00.01.02"', '"gastrulation": "E05.02.01"'), 'review term'),
  ('retired id reused', lambda s: s.replace('RETIRED = ["L02", "G02"]', 'RETIRED = ["L02", "G02", "L03"]'), 'retired id'),
  ('retired shot used', lambda s: s.replace('SHOTS_RETIRED = ["S02"]', 'SHOTS_RETIRED = ["S02", "S03"]'), 'retired shot'),
  ('4 new terms in 60 s', lambda s: s.replace('new=["ectoderm", "mesoderm", "endoderm"]', 'new=["ectoderm", "mesoderm", "endoderm", "gastrulation"]').replace('"gastrulation": "E00.01.02"', ''), '4 new terms'),
]
bad = 0
for name, f, want in CASES:
    if T.exists(): shutil.rmtree(T)
    shutil.copytree(SRC, T, ignore=shutil.ignore_patterns('out', '__pycache__'))
    (T / 's1e01_data.py').write_text(f(base), encoding='utf-8')
    r = subprocess.run([sys.executable, str(T / 'build.py'), '--repo', str(REPO), '--dry-run'], capture_output=True, text=True, encoding='utf-8')
    try: errs = json.loads(r.stdout)['errors']
    except Exception: errs = ['CRASH ' + r.stderr[-400:]]
    ok = (not errs) if want is None else any(want in e for e in errs)
    bad += not ok
    print('PASS' if ok else 'FAIL', name, '' if ok else errs[:4])
shutil.rmtree(T, ignore_errors=True)
print('selftest', len(CASES) - bad, '/', len(CASES)); sys.exit(1 if bad else 0)
