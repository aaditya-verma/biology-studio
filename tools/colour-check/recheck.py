"""Biology Studio — colour re-check for the light + dark tokens on every ladder level (D-031 method, D-034 limits, D-077 values).
Owner doc: build/design-plan.md §1 · RULES B3, H5 · DECISIONS D-031, D-034, D-077 (U2 re-check logged in the U2 decision).
What it measures (every number printed, nothing guessed):
  1. WCAG 2.x contrast of each germ-layer edge (and fill) against every ladder level L0-L4  → edge or fill >= 3.5 (D-034)
  2. accent-text >= 4.5, line-strong >= 3.0, muted >= 4.5, ink >= 4.5 on every level; heat-scale text >= 4.5 on its cell
  3. CIEDE2000 between every pair of layer edges and between the accent and every edge, under normal, deutan, protan and
     tritan vision (Machado 2009, severity 1.0, applied in linear RGB) — D-031 asks pairs >= 15 or a pattern + label to carry them (H5)
Use:  python -X utf8 tools/colour-check/recheck.py            report (exit 1 on a contrast failure)
      python -X utf8 tools/colour-check/recheck.py --json     machine-readable
      python -X utf8 tools/colour-check/recheck.py --selftest
EDIT: the values below must match src/css/app.css :root (layout-check's colour key re-measures them in the browser). """
import sys, json, itertools, math

# EDIT: tokens as built in U2 (app.css :root). Light ladder + edges = D-077; dark = D-031/D-034 unchanged.
THEMES = {
  'light': {
    'ladder': {'L0': '#F3F1EC', 'L1': '#EBE9E3', 'L2': '#E3E1DA', 'L3': '#DBD8D0', 'L4': '#D2CFC6'},
    'fill': {'epi': '#56B4E9', 'hypo': '#BDD9B8', 'ecto': '#0072B2', 'meso': '#D55E00', 'endo': '#E6CF3A', 'crest': '#009E73', 'ctx': '#828A99'},
    'edge': {'epi': '#146DA0', 'hypo': '#45723D', 'ecto': '#006CA9', 'meso': '#AB4B00', 'endo': '#75680F', 'crest': '#007656', 'ctx': '#606875'},
    'ui': {'ink': '#1B1D21', 'muted': '#55585F', 'accent-text': '#873E66', 'line-strong': '#747169', 'accent': '#994774'},
    'heat': [('#E3E1DA', '#1B1D21'), ('#C9C6BD', '#1B1D21'), ('#A9A59B', '#1B1D21'), ('#66625A', '#F3F1EC'), ('#3D3F45', '#F3F1EC')],
  },
  'dark': {
    'ladder': {'L0': '#252930', 'L1': '#1F2228', 'L2': '#1A1D22', 'L3': '#16181C', 'L4': '#121417'},
    'fill': {'epi': '#56B4E9', 'hypo': '#BDD9B8', 'ecto': '#0072B2', 'meso': '#D55E00', 'endo': '#E6CF3A', 'crest': '#009E73', 'ctx': '#828A99'},
    'edge': {'epi': '#56B4E9', 'hypo': '#BDD9B8', 'ecto': '#0082CA', 'meso': '#D55E00', 'endo': '#E6CF3A', 'crest': '#009E73', 'ctx': '#828A99'},
    'ui': {'ink': '#ECEDEF', 'muted': '#A9AEB7', 'accent-text': '#C77BA2', 'line-strong': '#737985', 'accent': '#C77BA2'},
    'heat': [('#2A2E35', '#ECEDEF'), ('#3E434C', '#ECEDEF'), ('#596069', '#ECEDEF'), ('#9AA0AA', '#14161A'), ('#DCDDE0', '#14161A')],
  },
}
LIMITS = {'edge': 3.5, 'accent-text': 4.5, 'line-strong': 3.0, 'muted': 4.5, 'ink': 4.5, 'heat': 4.5, 'de_pair': 15.0}

def s2l(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]

def lum(h):
    r, g, b = s2l(h); return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    A, B = lum(a), lum(b); return (max(A, B) + 0.05) / (min(A, B) + 0.05)

MACHADO = {'deutan': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
           'protan': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
           'tritan': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]}

def mul(m, v): return [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]

def lab(lin):
    X = mul([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]], lin)
    X = [X[0] / 0.95047, X[1], X[2] / 1.08883]
    f = [x ** (1 / 3) if x > 0.008856 else 7.787 * x + 16 / 116 for x in X]
    return (116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2]))

def seen(h, vision):
    l = s2l(h)
    if vision != 'normal': l = [min(1, max(0, x)) for x in mul(MACHADO[vision], l)]
    return lab(l)

def de00(p, q):
    L1, a1, b1 = p; L2, a2, b2 = q
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))); a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1 = math.degrees(math.atan2(b1, a1p)) % 360; h2 = math.degrees(math.atan2(b2, a2p)) % 360
    dL, dC = L2 - L1, C2p - C1p
    if C1p * C2p == 0: dh = 0
    else:
        dh = h2 - h1
        if dh > 180: dh -= 360
        elif dh < -180: dh += 360
    dH = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lb, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0: hb = h1 + h2
    elif abs(h1 - h2) > 180: hb = (h1 + h2 + 360) / 2 if h1 + h2 < 360 else (h1 + h2 - 360) / 2
    else: hb = (h1 + h2) / 2
    T = 1 - 0.17 * math.cos(math.radians(hb - 30)) + 0.24 * math.cos(math.radians(2 * hb)) + 0.32 * math.cos(math.radians(3 * hb + 6)) - 0.2 * math.cos(math.radians(4 * hb - 63))
    dth = 30 * math.exp(-((hb - 275) / 25) ** 2); Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lb - 50) ** 2 / math.sqrt(20 + (Lb - 50) ** 2); Sc = 1 + 0.045 * Cbp; Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dL / Sl) ** 2 + (dC / Sc) ** 2 + (dH / Sh) ** 2 + Rt * (dC / Sc) * (dH / Sh))

VISIONS = ['normal', 'deutan', 'protan', 'tritan']

def run(themes=THEMES):
    out, fails = {}, []
    for th, t in themes.items():
        r = {'edge_on_level': {}, 'ui_on_level': {}, 'heat': [], 'de_edges_worst': None, 'de_accent_worst': None}
        for k in t['edge']:
            row = {}
            for lv, bg in t['ladder'].items():
                ce, cf = contrast(t['edge'][k], bg), contrast(t['fill'][k], bg)
                row[lv] = round(max(ce, cf), 2)
                if max(ce, cf) < LIMITS['edge']: fails.append(f"{th} {k} edge/fill {max(ce, cf):.2f} on {lv} < {LIMITS['edge']}")
            r['edge_on_level'][k] = row
        for k in ('ink', 'muted', 'accent-text', 'line-strong'):
            row = {lv: round(contrast(t['ui'][k], bg), 2) for lv, bg in t['ladder'].items()}
            r['ui_on_level'][k] = row
            for lv, v in row.items():
                if v < LIMITS[k]: fails.append(f"{th} {k} {v} on {lv} < {LIMITS[k]}")
        for i, (cell, ink) in enumerate(t['heat']):
            v = round(contrast(cell, ink), 2); r['heat'].append(v)
            if v < LIMITS['heat']: fails.append(f"{th} heat{i} text {v} < {LIMITS['heat']}")
        worst = (999, None, None)
        for (a, ca), (b, cb) in itertools.combinations(t['edge'].items(), 2):
            for v in VISIONS:
                d = de00(seen(ca, v), seen(cb, v))
                if d < worst[0]: worst = (d, f'{a}/{b}', v)
        r['de_edges_worst'] = {'de': round(worst[0], 1), 'pair': worst[1], 'vision': worst[2]}
        worst = (999, None, None)
        for k, c in t['edge'].items():
            for v in VISIONS:
                d = de00(seen(t['ui']['accent'], v), seen(c, v))
                if d < worst[0]: worst = (d, k, v)
        r['de_accent_worst'] = {'de': round(worst[0], 1), 'edge': worst[1], 'vision': worst[2]}
        out[th] = r
    return out, fails

def report(out, fails):
    for th, r in out.items():
        print(f'== {th} ==')
        lv = list(next(iter(r['edge_on_level'].values())).keys())
        print('  layer edge (or fill) vs ' + ' '.join(f'{x:>5}' for x in lv))
        for k, row in r['edge_on_level'].items(): print(f'  {k:<22}' + ' '.join(f'{row[x]:5.2f}' for x in lv) + f'   min {min(row.values()):.2f}')
        for k, row in r['ui_on_level'].items(): print(f'  {k:<22}' + ' '.join(f'{row[x]:5.2f}' for x in lv) + f'   min {min(row.values()):.2f}')
        print('  heat text 0-4          ' + ' '.join(f'{v:5.2f}' for v in r['heat']))
        e, a = r['de_edges_worst'], r['de_accent_worst']
        print(f"  CIEDE2000 worst edge pair {e['de']} ({e['pair']}, {e['vision']})" + ('' if e['de'] >= LIMITS['de_pair'] else ' — under 15: pattern + label carry it (H5)'))
        print(f"  CIEDE2000 accent vs nearest edge {a['de']} ({a['edge']}, {a['vision']})")
    print('PASS' if not fails else 'FAIL:\n  ' + '\n  '.join(fails))

def selftest():
    ok = abs(contrast('#000000', '#FFFFFF') - 21) < 0.01 and abs(contrast('#777777', '#777777') - 1) < 1e-9
    ok &= de00(seen('#336699', 'normal'), seen('#336699', 'normal')) < 1e-9
    # Sharma 2005 test pair 1: (50, 2.6772, -79.7751) vs (50, 0, -82.7485) = 2.0425
    ok &= abs(de00((50, 2.6772, -79.7751), (50, 0, -82.7485)) - 2.0425) < 1e-3
    bad = {'light': dict(THEMES['light'], edge=dict(THEMES['light']['edge'], epi='#9CC7E0'))}
    ok &= any('epi' in f for f in run(bad)[1]) and not run()[1]
    print('selftest', 'PASS' if ok else 'FAIL'); return 0 if ok else 1

if __name__ == '__main__':
    if '--selftest' in sys.argv: sys.exit(selftest())
    o, f = run()
    if '--json' in sys.argv: print(json.dumps({'results': o, 'fails': f}, indent=1))
    else: report(o, f)
    sys.exit(1 if f else 0)
