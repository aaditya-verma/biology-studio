"""K2 map data — purpose: per-concept links (needs, unlocks, back_in, becomes, defect) and precomputed Embryo-map positions
(ring = day, wedge = system, side = cone height) for content/E/map.json, plus the --preview contact sheet and --selftest.
Owner doc: tools/map/README.md § Map data (spec, D-071). Called by build_map.py; no packages (Python 3 stdlib only).
EDIT: layout numbers live in LAYOUT below (one home, RULES I6); cited links live in links.txt (never in code)."""
import math, random, re, os, collections

# EDIT: layout block — bump 'version' whenever a number here or the placement rule changes (K3/K4 read it).
LAYOUT = dict(
    version=1, seed=71,                      # D-071 — fixed seed: same input = same output, byte for byte
    phone_px=360, edge_px=12,                # smallest test width (design-plan §2)
    dot_zoom=1.5,                            # owner pick 22 Nov 2026 (K2): on a 360 px phone the map opens on Parts/Chapters and concept
                                             # dots appear from 1.5× zoom; the no-overlap check is at that zoom: radius 360 × 1.5 / 2 − 12 = 258 px.
                                             # 768 px and wider (tablets, laptops) show every dot at 1×.
    dot_px=8, gap_px=2,                      # dot diameter and the minimum clear gap between two dots (at dot_zoom on a phone)
    # Day scale → normalised radius (0 = centre, 1 = map edge). ONE monotonic scale for the whole map, built from bands:
    # one band per Carnegie stage CS1–CS23 (days 1–60), three fetal bands (squeezed ×fetal_w) and a rim band for "no day".
    # Band width = base_w + per_w × (dots in that band), scaled to fill band_r — so busy stages are wide (stretch) and
    # empty ones stay visible. A dot sits at its exact day inside its band and may move only within that band.
    toolkit_r=0.16,                          # Toolkit disc (E00 + E01, no day): r ≤ toolkit_r, drawn at the centre
    rim_gap=0.04,                            # empty ring between Birth (end of fetal2) and the No-day rim band, so rim dots never read as late fetal
    band_r=[0.19, 0.985],                    # first band starts here; rim band ends here
    base_t=0.004,                            # narrowest band (a stage with no dots stays visible)
    fetal_bands=[[61, 90], [91, 180], [181, 266]],
    term_day=266,
    wedge_gap_deg=1.5, wedge_min_deg=9.0, wedge_pow=0.9, start_deg=-90.0,
    wedge_edge_px=2,                         # clear space between a dot and its wedge's border lines
    # wedge order clockwise from the top (G-Art 22 Nov 2026: related systems side by side; day-less wedges meet at the top seam)
    wedge_order=['mol', 'gam', 'early', 'plac', 'cav', 'cv', 'resp', 'gi', 'uro', 'gen', 'limb', 'msk', 'head', 'cns', 'ear', 'eye', 'skin', 'defects'],
    # guide rings: label → first day of that week (fertilization age); Birth = term
    guides=[['Wk 1', 1], ['Wk 2', 8], ['Wk 3', 15], ['Wk 4', 22], ['Wk 5', 29], ['Wk 6', 36], ['Wk 7', 43], ['Wk 8', 50], ['Birth', 266]],
    iters=3000, pack=0.8,                  # pack: room per dot as a share of min_centre² (hex packing ≈ 0.87); 0.8 fits and settles with 0 overlaps
)
TOOLKIT_CH = ('E00', 'E01')                                     # EDIT: chapters drawn as the Toolkit at the centre (D-071 a)
NON_ORGAN = ('ori', 'mol', 'defects', 'early', 'gam', 'plac')   # EDIT: systems a defect cannot borrow its wedge from
# Carnegie stage → day range (≈, fertilization age). ONE home: build_map.py imports it from here. EDIT here only.
CS = [(1,1,1),(2,3,2),(4,5,3),(5,6,4),(7,12,5),(13,15,6),(16,17,7),(18,19,8),(20,21,9),(22,23,10),(24,25,11),(26,28,12),(29,31,13),
      (32,34,14),(35,37,15),(38,41,16),(42,43,17),(44,47,18),(48,50,19),(51,52,20),(53,54,21),(55,56,22),(57,60,23)]
CS_LO = {n: lo for lo, hi, n in CS}
R4 = lambda v: round(v + 0.0, 4)


def band_of(d, L=LAYOUT):
    """Band key for a day: ('cs', n) for days 1–60, ('fetal', i) after, ('rim', 0) for None."""
    if d is None: return ('rim', 0)
    if d <= 60:
        d = max(1, d)
        for lo, hi, n in CS:
            if lo <= d <= hi: return ('cs', n)
    for i, (lo, hi) in enumerate(L['fetal_bands']):
        if d <= hi: return ('fetal', i)
    return ('fetal', len(L['fetal_bands']) - 1)


def band_days(key, L=LAYOUT):
    k, n = key
    if k == 'cs':   # the ≈ table overlaps (CS3 4–5, CS4 5–6): a shared day belongs to the earlier stage, as in band_of
        lo, hi, _ = CS[n - 1]
        if n > 1: lo = max(lo, CS[n - 2][1] + 1)
        return lo, hi
    if k == 'fetal': return tuple(L['fetal_bands'][n])
    return None, None


def make_scale(cell, theta, dmin, L=LAYOUT):
    """cell: Counter{(wedge system, band key): dots}; theta: {system: wedge angle, radians} → ordered bands [{key, lo, hi, r0, r1, n}].
    A band is as wide as its most crowded wedge needs: dots × dmin² × pack ÷ (wedge angle × band radius) — at least base_t.
    Spare width goes to the Carnegie bands (stretch, in proportion to need); fetal bands keep their need (squeeze)."""
    keys = [('cs', n) for n in range(1, 24)] + [('fetal', i) for i in range(len(L['fetal_bands']))] + [('rim', 0)]
    cnt = collections.Counter()
    for (sy, k), n in cell.items(): cnt[k] += n
    a, b = L['band_r']; b_ = b - (L['rim_gap'] if cnt.get(('rim', 0)) else 0.0); mid = {k: (a + b) / 2 for k in keys}; fit = True
    for _ in range(40):
        t = {}
        for k in keys:
            need = max([n * dmin * dmin * L['pack'] / (theta[sy] * mid[k]) for (sy, kk), n in cell.items() if kk == k] or [0.0])
            t[k] = 0.0 if (k[0] == 'rim' and not cnt.get(k)) else max(L['base_t'], need)
        T = sum(t.values()); spare = (b_ - a) - T; fit = spare >= 0
        if fit:
            cs_t = sum(v for k, v in t.items() if k[0] == 'cs')
            w = {k: v + (spare * v / cs_t if k[0] == 'cs' else 0.0) for k, v in t.items()}
        else:
            w = {k: v * (b_ - a) / T for k, v in t.items()}
        r = a
        for k in keys:
            if k[0] == 'rim': r += b - b_
            mid[k] = r + w[k] / 2; r += w[k]
    r = a; out = []
    for k in keys:
        if k[0] == 'rim': r += b - b_
        lo, hi = band_days(k, L)
        out.append(dict(key='%s%s' % (k[0], k[1] if k[0] != 'rim' else ''), lo=lo, hi=hi, r0=R4(r), r1=R4(r + w[k]), n=cnt.get(k, 0)))
        r += w[k]
    return out, fit, T


def day_r(d, scale, L=LAYOUT):
    """Exact radius for a day on the scale (None → middle of the rim band)."""
    key = band_of(d, L); kk = '%s%s' % (key[0], key[1] if key[0] != 'rim' else '')
    bd = next(x for x in scale if x['key'] == kk)
    if d is None: return (bd['r0'] + bd['r1']) / 2, bd
    lo, hi = bd['lo'], bd['hi']; f = (min(max(d, lo), hi) - lo + 0.5) / (hi - lo + 1)
    return bd['r0'] + (bd['r1'] - bd['r0']) * f, bd


def read_links(path, idx, docs_dir):
    """links.txt → {from: {'becomes': [...], 'defect': [...]}}, errors. Each anchor must match exactly ONE line of its dossier."""
    out = collections.defaultdict(lambda: dict(becomes=[], defect=[])); errs = []; cache = {}
    if not os.path.exists(path): return out, [f'links file missing: {path}']
    for ln, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'): continue
        p = line.split('|', 4)
        if len(p) != 5: errs.append(f'links line {ln}: needs 5 fields'); continue
        kind, frm, to, doc, anchor = (x.strip() if i < 4 else x for i, x in enumerate(p))
        if kind not in ('becomes', 'defect'): errs.append(f'links line {ln}: kind {kind!r}'); continue
        if frm not in idx: errs.append(f'links line {ln}: unknown concept {frm}'); continue
        if idx[frm]['sys'] == 'defects': errs.append(f'links line {ln}: {frm} is itself a defect concept'); continue
        if kind == 'defect':
            if to not in idx: errs.append(f'links line {ln}: unknown defect concept {to}'); continue
            if idx[to]['sys'] != 'defects': errs.append(f'links line {ln}: {to} is not in system "defects"'); continue
        elif not to or len(to) > 140: errs.append(f'links line {ln}: becomes label empty or > 140 chars'); continue
        fp = os.path.join(docs_dir, doc)
        if fp not in cache:
            if not os.path.exists(fp): errs.append(f'links line {ln}: no dossier {doc}'); continue
            cache[fp] = open(fp, encoding='utf-8').read().split('\n')
        hits = [i for i, l in enumerate(cache[fp], 1) if anchor in l]
        if len(hits) != 1: errs.append(f'links line {ln}: anchor matches {len(hits)} lines in {doc} (need exactly 1): {anchor!r}'); continue
        cite = dict(doc='research/dossiers/' + doc, line=hits[0], anchor=anchor)
        out[frm][kind].append(dict(to=to, cite=cite))
    for f in out:
        for k in ('becomes', 'defect'): out[f][k].sort(key=lambda x: (x['to'], x['cite']['line']))
    return out, errs


def back_in(c, by, kids_all, terms_of):
    """Same thread in a later chapter: concepts in later chapters that share a thread letter with c AND are linked to it
    (a dependant of c, or a shared glossary term). Best one per later chapter, at most 6, nearest chapter first."""
    own = int(c['ch'][1:]); th = set(c['threads'])
    cand = collections.defaultdict(list)
    for o in by.values():
        if int(o['ch'][1:]) <= own or not (th & set(o['threads'])): continue
        shared = len(terms_of[c['id']] & terms_of[o['id']]); dep = o['id'] in kids_all[c['id']]
        if not (shared or dep): continue
        cand[o['ch']].append((-(shared + (2 if dep else 0)), o['id']))
    return [sorted(v)[0][1] for ch, v in sorted(cand.items())][:6]


def place_day(c, by, links_rev):
    """(day, src) for the ring. Toolkit → (None, 'toolkit'). A cited defect → the start of its sensitive period = the earliest
    start day among the concepts that cite it ('from:<id>'); if none of them has a day, its own day/stage, else no day.
    Others: own day ('day'), else the first day of its cited Carnegie stage ('cs'), else no day ('none' → rim band).
    No guessing from section or chapter medians (G-Art 22 Nov 2026): an undated concept waits on the rim for its X1."""
    if c['ch'] in TOOLKIT_CH: return None, 'toolkit'
    def own(o):
        if o['day']: return o['day'][0], 'day'
        if o.get('cs'): return CS_LO[o['cs'][0]], 'cs'
        return None, None
    if c['id'] in links_rev:
        ds = [(own(by[f])[0], f) for f in links_rev[c['id']] if own(by[f])[0] is not None]
        if ds:
            d, f = min(ds); return d, 'from:' + f
    d, s_ = own(c)
    return (d, s_) if d is not None else (None, 'none')


def compute(out_concepts, kids_all, sys_order, links_path, docs_dir, L=LAYOUT, log=lambda *m: None):
    """Adds links / ring / wedge / pos / side / shape to every concept (in place) and returns (layout block, report, errors)."""
    by = {o['id']: o for o in out_concepts}
    idx = {o['id']: dict(sys=o['system']) for o in out_concepts}
    links, errs = read_links(links_path, idx, docs_dir)
    if errs: return None, None, errs
    rev = collections.defaultdict(list)
    for f, v in links.items():
        for x in v['defect']: rev[x['to']].append(f)
    terms_of = {o['id']: set(o['terms']) for o in out_concepts}
    # wedge system: a defect concept borrows the organ system of the first concept that cites it, else of its first organ prereq
    def wsys(o):
        if o['system'] != 'defects': return o['system']
        for f in sorted(rev.get(o['id'], [])) + o['prereq']:
            s = by[f]['system']
            if s not in NON_ORGAN: return s
        return 'defects'
    nodes = []
    for o in out_concepts:
        d, src = place_day(o, by, rev)
        tk = o['ch'] in TOOLKIT_CH
        nodes.append(dict(id=o['id'], tk=tk, day=d, src=src, sys=None if tk else wsys(o)))
    R_px = L['phone_px'] * L['dot_zoom'] / 2 - L['edge_px']; dmin = (L['dot_px'] + L['gap_px']) / R_px
    cnt = collections.Counter(n['sys'] for n in nodes if not n['tk'])
    order = [s for s in L['wedge_order'] if cnt.get(s)] + [s for s in sys_order if cnt.get(s) and s not in L['wedge_order']]
    total = 360.0 - L['wedge_gap_deg'] * len(order)
    # wedges first: angle ∝ dots^wedge_pow (min width), fixed system order, clockwise from the top
    w = {s: cnt[s] ** L['wedge_pow'] for s in order}
    for _ in range(6):
        k = total / sum(w.values()); w = {s: max(L['wedge_min_deg'], v * k) for s, v in w.items()}
    k = total / sum(w.values()); w = {s: v * k for s, v in w.items()}
    wedges = {}; a = L['start_deg']
    for s in order:
        wedges[s] = [R4(a), R4(a + w[s])]; a += w[s] + L['wedge_gap_deg']
    theta = {s: math.radians(w[s]) for s in order}
    per_cell = collections.Counter((n['sys'], band_of(n['day'], L)) for n in nodes if not n['tk'])
    scale, fit, need_T = make_scale(per_cell, theta, dmin, L)
    log('scale', 'fits (spare → CS bands)' if fit else 'over-full: all bands scaled down', '— bands need', round(need_T, 3), 'of', round(L['band_r'][1] - L['band_r'][0], 3))
    for n in nodes:
        if n['tk']: n['r0'], n['lo'], n['hi'], n['band'] = 0.0, 0.0, L['toolkit_r'], 'toolkit'
        else:
            r, bd = day_r(n['day'], scale, L); n['r0'], n['lo'], n['hi'], n['band'] = r, bd['r0'], bd['r1'], bd['key']
    # initial positions: deterministic golden-angle spread inside each wedge, seeded jitter
    rnd = random.Random(L['seed']); GA = 0.6180339887498949
    bysys = collections.defaultdict(list)
    for n in nodes: bysys['_tk' if n['tk'] else n['sys']].append(n)
    for s, ns in sorted(bysys.items()):
        ns.sort(key=lambda n: (n['r0'], n['id']))
        for i, n in enumerate(ns):
            if s == '_tk':
                rr = L['toolkit_r'] * 0.92 * math.sqrt((i + 0.5) / len(ns)); th = 2 * math.pi * ((i * GA) % 1.0)
                n['x'], n['y'] = rr * math.cos(th), rr * math.sin(th)
            else:
                a0, a1 = wedges[s]; pad = min(2.0, (a1 - a0) * 0.1)
                f = ((i * GA) + rnd.random() * 0.05) % 1.0
                th = math.radians(a0 + pad + (a1 - a0 - 2 * pad) * f)
                n['x'], n['y'] = n['r0'] * math.cos(th), n['r0'] * math.sin(th)
    # relaxation: push apart any pair closer than dmin; keep each dot in its wedge and within slack of its day radius
    dm = dmin * 1.04                          # small safety margin so rounding to 4 decimals never re-creates an overlap
    def clamp(n):
        r = math.hypot(n['x'], n['y']); th = math.atan2(n['y'], n['x'])
        if n['tk']:
            r = min(r, L['toolkit_r'])
        else:
            r = min(max(r, n['lo']), min(n['hi'], 1.0 - L['dot_px'] / 2 / R_px))
            a0, a1 = (math.radians(v) for v in wedges[n['sys']])
            half = math.asin(min(1.0, (L['dot_px'] / 2 + L['wedge_edge_px']) / R_px / max(r, 1e-6)))   # whole dot + edge space inside the wedge
            lo, hi = a0 + half, a1 - half
            if lo > hi: lo = hi = (a0 + a1) / 2
            t = th
            while t < a0 - math.pi: t += 2 * math.pi
            while t > a1 + math.pi: t -= 2 * math.pi
            th = min(max(t, lo), hi)
        n['x'], n['y'] = r * math.cos(th), r * math.sin(th)
    for n in nodes: clamp(n)
    grid_cell = dm
    for it in range(L['iters']):
        grid = collections.defaultdict(list)
        for i, n in enumerate(nodes): grid[(int(math.floor(n['x'] / grid_cell)), int(math.floor(n['y'] / grid_cell)))].append(i)
        moved = 0
        for i, n in enumerate(nodes):
            gx, gy = int(math.floor(n['x'] / grid_cell)), int(math.floor(n['y'] / grid_cell))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for j in grid.get((gx + dx, gy + dy), ()):
                        if j <= i: continue
                        m = nodes[j]; vx, vy = m['x'] - n['x'], m['y'] - n['y']; dd = math.hypot(vx, vy)
                        if dd >= dm: continue
                        if dd < 1e-9:
                            ang = 2 * math.pi * ((i * 7919 + j * 104729) % 1000) / 1000.0; vx, vy, dd = math.cos(ang), math.sin(ang), 1.0
                            push = dm / 2
                        else:
                            push = (dm - dd) / 2 + 1e-6
                        ux, uy = vx / dd, vy / dd
                        n['x'] -= ux * push; n['y'] -= uy * push; m['x'] += ux * push; m['y'] += uy * push
                        moved += 1
        for n in nodes: clamp(n)
        if not moved: log('layout settled after', it, 'passes'); break
    # write fields (rounded → byte-stable)
    for n in nodes:
        o = by[n['id']]; r = math.hypot(n['x'], n['y']); a_ = math.degrees(math.atan2(n['y'], n['x']))
        if not n['tk']:   # express the angle inside its wedge's own range [a0, a1] (wedges run start_deg … start_deg + 360)
            while a_ < wedges[n['sys']][0] - 1e-6: a_ += 360.0
            while a_ > wedges[n['sys']][0] + 360.0: a_ -= 360.0
        lk = links.get(n['id'], dict(becomes=[], defect=[]))
        o['links'] = dict(needs=list(o['prereq']), unlocks=list(o['unlocks']), back_in=back_in(o, by, kids_all, terms_of),
                          becomes=lk['becomes'], defect=lk['defect'])
        o['ring'] = dict(r=R4(r), r_day=R4(n['r0']), band=n['band'], day=n['day'], src=n['src'])
        o['wedge'] = dict(sys='toolkit' if n['tk'] else n['sys'], a=R4(a_))
        o['pos'] = dict(x=R4(n['x']), y=R4(n['y']))
        o['side'] = dict(h=None if n['band'] == 'rim' else R4(n['r0']))   # cone height = r_day; no day → null (K4: a shelf above Birth); ground = pos
        o['shape'] = 'defect' if n['id'] in rev else 'dot'
    block = dict(version=L['version'], seed=L['seed'], step='K2', decision='D-071',
                 units='normalised: r 0 = centre, 1 = map edge; pos x right, y down (SVG); angles in degrees, 0 = right, clockwise; side.h 0 = apex (Toolkit) … 1 = top',
                 phone=dict(px=L['phone_px'], dot_zoom=L['dot_zoom'], edge_px=L['edge_px'], dot_px=L['dot_px'], gap_px=L['gap_px'], min_center=R4(dmin)),
                 scale=dict(toolkit_r=L['toolkit_r'], band_r=L['band_r'], base_t=L['base_t'], pack=L['pack'], rim_gap=L['rim_gap'], term_day=L['term_day'],
                            rule='one monotonic day scale: a band per Carnegie stage CS1–CS23 (days 1–60), 3 fetal bands, a rim band for no day (after an empty rim_gap); a band is as wide as its most crowded wedge needs (dots × min_centre² × pack ÷ (wedge angle × band radius), at least base_t); spare width goes to the CS bands only (stretch), fetal bands keep their need (squeeze); in a band, r_day = r0 + (r1 − r0) × (day − lo + 0.5) ÷ (hi − lo + 1); a dot may move only inside its band (ring.r); Toolkit E00 + E01 inside toolkit_r',
                            bands=scale,
                            breakpoints=[[b['lo'], b['r0']] for b in scale if b['lo'] is not None] + [[L['term_day'], next(b['r1'] for b in scale if b['key'] == 'fetal2')]]),
                 wedges=dict(order=order, deg=wedges, edge_px=L['wedge_edge_px'], rule='order = layout wedge_order, clockwise from the top; angle ∝ dots^%s, min %s°, gap %s°; a dot keeps its whole disc + edge_px inside its wedge; wedge.a is given inside [a0, a1]' % (L['wedge_pow'], L['wedge_min_deg'], L['wedge_gap_deg'])),
                 rings=[dict(label=lb, day=d, r=R4(day_r(d, scale, L)[0])) for lb, d in L['guides']] + ([dict(label='No day yet', day=None, r=next(b['r0'] for b in scale if b['key'] == 'rim'))] if any(b['key'] == 'rim' and b['n'] for b in scale) else []),
                 toolkit=list(TOOLKIT_CH))
    import hashlib   # positions fingerprint: changes whenever any dot or band moves (e.g. after an X1) — K3/K4 key caches on it
    block['hash'] = hashlib.sha256(repr([(o['id'], o['pos']['x'], o['pos']['y'], o['ring']['r_day']) for o in out_concepts] + [(b['key'], b['r0'], b['r1']) for b in scale]).encode()).hexdigest()[:16]
    rep = dict(placed=len(nodes), rim_no_day=sum(1 for n in nodes if n['src'] == 'none'), toolkit=sum(n['tk'] for n in nodes), day_src=dict(collections.Counter(n['src'].split(':')[0] for n in nodes)),
               becomes=sum(len(v['becomes']) for v in links.values()), defect_links=sum(len(v['defect']) for v in links.values()),
               defect_nodes=len(rev), defect_concepts_uncited=sorted(o['id'] for o in out_concepts if o['system'] == 'defects' and o['id'] not in rev),
               wedges={s: cnt[s] for s in order})
    return block, rep, []


def overlaps(out_concepts, block):
    """Pairs of dots closer than the phone minimum (centre distance), measured on the stored (rounded) positions."""
    ph = block['phone']; dmin = (ph['dot_px'] + ph['gap_px']) / (ph['px'] * ph['dot_zoom'] / 2 - ph['edge_px']) - 1e-9   # exact, not the rounded field
    P = [(o['id'], o['pos']['x'], o['pos']['y']) for o in out_concepts]
    bad = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            d = math.hypot(P[i][1] - P[j][1], P[i][2] - P[j][2])
            if d < dmin: bad.append((P[i][0], P[j][0], round(d, 4)))
    return bad


# ---------- --preview: SVG contact sheet (rings + side, light + dark) for G-Art ----------
# EDIT: token values copied from src/css/app.css (D-031) — the app itself never hard-codes them (B3); this sheet is a review image.
TOK = dict(light=dict(bg='#FAFAF7', ink='#1B1D21', muted='#55585F', line='#DCDAD3', accent='#994774', pat='#111111',
                      ecto='#0072B2', meso='#D55E00', endo='#E6CF3A', crest='#009E73', ctx='#828A99'),
           dark=dict(bg='#14161A', ink='#ECEDEF', muted='#A9AEB7', line='#343840', accent='#B76491', pat='#111111',
                     ecto='#0082CA', meso='#D55E00', endo='#E6CF3A', crest='#009E73', ctx='#828A99'))
LAYER_FILL = dict(ecto='ecto', meso='meso', endo='endo', crest='crest', extra='ctx', none='ctx', multi='multi')


def _defs(t, p):
    T = TOK[t]
    return (f'<defs>'
            f'<pattern id="{p}ecto" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="{T["ecto"]}"/><circle cx="2" cy="2" r=".9" fill="#fff"/></pattern>'
            f'<pattern id="{p}meso" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="{T["meso"]}"/><rect width=".8" height="4" fill="{T["pat"]}"/></pattern>'
            f'<pattern id="{p}endo" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="{T["endo"]}"/><rect width="4" height=".8" fill="{T["pat"]}"/></pattern>'
            f'<pattern id="{p}crest" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="{T["crest"]}"/><path d="M0 0L4 4M4 0L0 4" stroke="{T["pat"]}" stroke-width=".6"/></pattern>'
            f'<pattern id="{p}ctx" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="3" fill="{T["ctx"]}"/><circle cx="1.5" cy="1.5" r=".55" fill="{T["pat"]}"/></pattern>'
            f'</defs>')


def _mark(o, x, y, t, p, s):
    T = TOK[t]; f = LAYER_FILL[o['layer']]; r = s / 2
    esc = lambda v: str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    tip = f'<title>{o["id"]} {esc(o["name"])} · {o["ring"]["src"]}</title>'
    if f == 'multi':
        body = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{T["meso"]}"/><path d="M{x:.1f} {y:.1f}L{x:.1f} {y - r:.1f}A{r:.1f} {r:.1f} 0 0 1 {x + r * .866:.1f} {y + r * .5:.1f}Z" fill="{T["ecto"]}"/>'
                f'<path d="M{x:.1f} {y:.1f}L{x + r * .866:.1f} {y + r * .5:.1f}A{r:.1f} {r:.1f} 0 0 1 {x - r * .866:.1f} {y + r * .5:.1f}Z" fill="{T["endo"]}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{r * .38:.1f}" fill="{T["bg"]}"/>')
        fill = 'none'
    else:
        body = ''; fill = f'url(#{p}{f})'
    if o['shape'] == 'defect':
        d = r * 1.25
        return f'<g>{tip}<path d="M{x:.1f} {y - d:.1f}L{x + d:.1f} {y:.1f}L{x:.1f} {y + d:.1f}L{x - d:.1f} {y:.1f}Z" fill="{fill if f != "multi" else T["ctx"]}" stroke="{T["ink"]}" stroke-width="1.2"/></g>'
    return f'<g>{tip}{body}<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{T["ink"]}" stroke-width=".6"/></g>'


def _rings_panel(out_concepts, block, t, p, ox, oy, W, M, names):
    """W = drawn map width at the checked zoom (phone px × dot_zoom), M = outer margin for wedge names."""
    T = TOK[t]; R = W / 2 - block['phone']['edge_px']; cx, cy = ox + M + W / 2, oy + M + W / 2
    s = block['phone']['dot_px']; L = [f'<rect x="{ox}" y="{oy}" width="{W + 2 * M}" height="{W + 2 * M}" fill="{T["bg"]}"/>']
    last = -99
    for rg in block['rings']:
        L.append(f'<circle cx="{cx}" cy="{cy}" r="{rg["r"] * R:.1f}" fill="none" stroke="{T["line"]}" stroke-width="1"/>')
        y = cy - rg['r'] * R
        if last - y >= 11 or last < 0:
            L.append(f'<text x="{cx + R * 0.0 + 3}" y="{y + 10:.1f}" font-size="9" fill="{T["muted"]}" paint-order="stroke" stroke="{T["bg"]}" stroke-width="2.5">{rg["label"]}</text>'); last = y
    tk = block['scale']['toolkit_r'] * R
    L.append(f'<circle cx="{cx}" cy="{cy}" r="{tk:.1f}" fill="none" stroke="{T["muted"]}" stroke-dasharray="2 2"/>')
    L.append(f'<text x="{cx}" y="{cy + tk + 10:.1f}" font-size="9" fill="{T["muted"]}" text-anchor="middle">Toolkit</text>')
    for wi, (sname, (a0, a1)) in enumerate(block['wedges']['deg'].items()):
        ra = math.radians(a0)
        L.append(f'<line x1="{cx + tk * math.cos(ra):.1f}" y1="{cy + tk * math.sin(ra):.1f}" x2="{cx + R * math.cos(ra):.1f}" y2="{cy + R * math.sin(ra):.1f}" stroke="{T["line"]}" stroke-width="1"/>')
        am = math.radians((a0 + a1) / 2); off = 14 + (16 if (a1 - a0) < 14 and wi % 2 else 0)   # stagger narrow neighbours
        lx, ly = cx + (R + off) * math.cos(am), cy + (R + off) * math.sin(am)
        anc = 'start' if math.cos(am) > 0.3 else ('end' if math.cos(am) < -0.3 else 'middle')
        L.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="10" fill="{T["ink"]}" text-anchor="{anc}" dominant-baseline="middle">{names.get(sname, sname).replace("&", "&amp;")}</text>')
    for o in out_concepts:
        L.append(_mark(o, cx + o['pos']['x'] * R, cy + o['pos']['y'] * R, t, p, s))
    return '\n'.join(L)


def _side_panel(out_concepts, block, t, p, ox, oy, W, H):
    T = TOK[t]; s = block['phone']['dot_px']; cx = ox + W / 2; top, bot = oy + 64, oy + H - 16; Rw = W / 2 - 40
    L = [f'<rect x="{ox}" y="{oy}" width="{W}" height="{H}" fill="{T["bg"]}"/>',
         f'<path d="M{cx} {bot}L{cx - Rw} {top}M{cx} {bot}L{cx + Rw} {top}" stroke="{T["line"]}" fill="none"/>']
    last = 1e9
    for rg in block['rings']:
        y = bot - rg['r'] * (bot - top)
        L.append(f'<line x1="{ox + 4}" y1="{y:.1f}" x2="{ox + W - 4}" y2="{y:.1f}" stroke="{T["line"]}" stroke-dasharray="1 3"/>')
        if last - y >= 11:
            L.append(f'<text x="{ox + 4}" y="{y - 2:.1f}" font-size="9" fill="{T["muted"]}">{rg["label"]}</text>'); last = y
    for o in sorted(out_concepts, key=lambda o: o['pos']['y']):   # back to front
        h = o['side']['h'] if o['side']['h'] is not None else 0.985   # no day: a shelf at the top, inside the panel
        L.append(_mark(o, cx + o['pos']['x'] * Rw, bot - h * (bot - top) + o['pos']['y'] * 26, t, p, s))   # slight tilt: y → depth
    return '\n'.join(L)


def preview_svg(out_concepts, block, names=None):
    names = names or {}
    W = int(block['phone']['px'] * block['phone']['dot_zoom']); M = 96; Wp = W + 2 * M; H = 520; pad = 12; head = 30
    tot_w = pad * 3 + Wp * 2; tot_h = head + pad * 3 + Wp + H + 40
    P = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{tot_w}" height="{tot_h}" viewBox="0 0 {tot_w} {tot_h}" font-family="system-ui,sans-serif">',
         f'<rect width="{tot_w}" height="{tot_h}" fill="#888"/>',
         f'<text x="{pad}" y="20" font-size="13" fill="#fff">K2 Embryo map preview (D-071) · layout v{block["version"]} · seed {block["seed"]} · {len(out_concepts)} concepts · drawn at the checked size: 360 px phone × {block["phone"]["dot_zoom"]} zoom = {W} px, dot {block["phone"]["dot_px"]} px, gap ≥ {block["phone"]["gap_px"]} px · ◆ = birth defect</text>']
    for k, t in enumerate(('light', 'dark')):
        ox = pad + k * (Wp + pad)
        P.append(_defs(t, t[0]))
        P.append(_rings_panel(out_concepts, block, t, t[0], ox, head + pad, W, M, names))
        P.append(_side_panel(out_concepts, block, t, t[0], ox, head + pad * 2 + Wp, Wp, H))
        P.append(f'<text x="{ox + 6}" y="{head + pad + 14}" font-size="11" font-weight="600" fill="{TOK[t]["ink"]}">Rings · {t}</text>')
        P.append(f'<text x="{ox + 6}" y="{head + pad * 2 + Wp + 14}" font-size="11" font-weight="600" fill="{TOK[t]["ink"]}">Side (cone, height = day) · {t}</text>')
    ly = head + pad * 3 + Wp + H + 14; lx = pad
    P.append(_defs('light', 'g'))
    for lab, f in (('Ectoderm', 'ecto'), ('Mesoderm', 'meso'), ('Endoderm', 'endo'), ('Neural crest', 'crest'), ('Extraembryonic / no layer', 'ctx')):
        P.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" fill="url(#g{f})" stroke="#000" stroke-width=".5"/><text x="{lx + 16}" y="{ly + 10}" font-size="11" fill="#fff">{lab}</text>'); lx += 16 + len(lab) * 6.3 + 14
    P.append(f'<text x="{lx}" y="{ly + 10}" font-size="11" fill="#fff">◔ several layers · ◆ defect</text>')
    P.append('</svg>')
    return '\n'.join(P)
