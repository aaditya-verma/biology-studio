"""Map compare (MAPF) — purpose: CI's map check. Is the committed content/E/map.json the same build as a fresh one?
Strict on everything (keys, strings, ints, list lengths, order) except floats, which may differ by one step of the
4-decimal rounding (R4 in layout.py): Linux and Windows maths libraries can land a value either side of a rounding edge
(22 Nov 2026: one rim ring r 0.96 on Windows, 0.9601 on Linux). /layout/hash is skipped — it is a digest of those floats.
A stale map (missing fields, other terms, other counts) still fails.
Use:  python map_compare.py FRESH.json COMMITTED.json   ·   python map_compare.py --selftest
EDIT: TOL and SKIP below; keep TOL at one R4 step unless layout.py's rounding changes."""
import json, sys

TOL = 1e-4 + 1e-9          # one 4-decimal step (+ float slack: 0.9601 - 0.96 = 1.0000000000000009e-4)
SKIP = {'/layout/hash'}


def diffs(a, b, p='', out=None, cap=20):
    out = [] if out is None else out
    if len(out) >= cap or p in SKIP: return out
    if type(a) is not type(b):   # strict, numbers too: 1 vs 1.0 is a different build (same code writes the same types)
        out.append(f'{p or "/"}: type {type(a).__name__} vs {type(b).__name__}'); return out
    if isinstance(a, dict):
        ka, kb = list(a), list(b)
        if ka != kb:
            miss = [k for k in kb if k not in a]; extra = [k for k in ka if k not in b]
            out.append(f'{p or "/"}: keys differ (fresh lacks {miss[:5]}, fresh adds {extra[:5]})' if (miss or extra) else f'{p or "/"}: key order differs')
            return out
        for k in ka: diffs(a[k], b[k], f'{p}/{k}', out, cap)
    elif isinstance(a, list):
        if len(a) != len(b): out.append(f'{p}: length {len(a)} vs {len(b)}'); return out
        for i, (x, y) in enumerate(zip(a, b)): diffs(x, y, f'{p}[{i}]', out, cap)
    elif isinstance(a, float) or isinstance(b, float):
        if abs(a - b) > TOL: out.append(f'{p}: {a} vs {b} (more than one R4 step)')
    elif a != b:
        out.append(f'{p}: {str(a)[:60]!r} vs {str(b)[:60]!r}')
    return out


def selftest():
    base = {'layout': {'hash': 'aa', 'n': 3}, 'concepts': [{'id': 'E01', 'ring': {'r': 0.96}, 'terms': ['t1'], 'n': 2, 'x1': True}]}
    def m(f):
        c = json.loads(json.dumps(base)); f(c); return c
    cases = [
        ('identical', base, True),
        ('one R4 step (Linux vs Windows)', m(lambda c: c['concepts'][0]['ring'].update(r=0.9601)), True),
        ('hash differs only', m(lambda c: c['layout'].update(hash='bb')), True),
        ('two R4 steps', m(lambda c: c['concepts'][0]['ring'].update(r=0.9602)), False),
        ('missing term (stale / cp1252 build)', m(lambda c: c['concepts'][0].update(terms=[])), False),
        ('missing field (stale map)', m(lambda c: c['concepts'][0].pop('n')), False),
        ('int count differs', m(lambda c: c['concepts'][0].update(n=3)), False),
        ('bool differs', m(lambda c: c['concepts'][0].update(x1=False)), False),
        ('string differs', m(lambda c: c['concepts'][0].update(id='E02')), False),
        ('layout n differs', m(lambda c: c['layout'].update(n=4)), False),
        ('int vs float (1 vs 1.0)', m(lambda c: c['concepts'][0].update(n=2.0)), False),
    ]
    bad = 0
    for name, c, want in cases:
        got = not diffs(c, base)
        if got != want: bad += 1
        print(('ok  ' if got == want else 'BAD ') + name)
    print(f'{"PASS" if not bad else "FAIL"}: map compare selftest {len(cases) - bad}/{len(cases)}')
    return 1 if bad else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv: sys.exit(selftest())
    if len(sys.argv) != 3: print(__doc__); sys.exit(2)
    fresh, committed = (json.load(open(f, encoding='utf-8')) for f in sys.argv[1:3])
    d = diffs(fresh, committed)
    if d:
        print(f'FAIL: {sys.argv[2]} is not the same build as {sys.argv[1]} — rebuild it (python -X utf8 build_map.py) and commit it:')
        for x in d: print('  ' + x)
        sys.exit(1)
    print(f'PASS: map.json matches a fresh build (floats within one R4 step; /layout/hash skipped)')
