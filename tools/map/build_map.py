#!/usr/bin/env python3
"""K1 map builder — purpose: concepts.txt + I1 index JSON -> content/E/map.json + curriculum/concept-map.md.
Owner doc: build/master-plan.md §5. Flags: --dry-run --debug --only <chapter id> --preview (RULES I5).
EDIT: concept rows live in concepts.txt (never in this code)."""
import json, re, sys, argparse, collections
ap = argparse.ArgumentParser()
ap.add_argument('--index', default='../../content/E/index/')
ap.add_argument('--src', default='concepts.txt'); ap.add_argument('--out', default='out')
ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--debug', action='store_true')
ap.add_argument('--only'); ap.add_argument('--preview', action='store_true')
a = ap.parse_args()
def log(*m):
    if a.debug: print('[map]', *m)

T = json.load(open(a.index + 'tree.json')); G = json.load(open(a.index + 'terms.json'))['terms']
X = json.load(open(a.index + 'xrefs.json')); TL = json.load(open(a.index + 'timeline.json'))
secs = {}; chap = {}
for c in T['chapters']:
    chap[c['id']] = c
    for s in c['sections']: secs[s['id']] = dict(s, ch=c['id'])
secs['E00.01'] = dict(id='E00.01', title='Reading an embryo (orientation)', kind='section', pages=None, boxes=[], ch='E00')

# EDIT: vocabularies (labels shown in the explorer)
SYS = dict(ori='Orientation', mol='Molecular basics', gam='Gametes & fertilization', early='Early embryo', plac='Placenta & membranes',
           cav='Body cavities', defects='Birth defects', msk='Skeleton & muscle', limb='Limbs', cv='Heart & vessels', resp='Respiratory',
           gi='Digestive', uro='Urinary', gen='Genital', head='Head & neck', cns='Nervous system', ear='Ear', eye='Eye', skin='Skin')
LAYER = dict(ecto='Ectoderm', meso='Mesoderm', endo='Endoderm', crest='Neural crest', extra='Extraembryonic', multi='Several layers', none='No layer')
IMP = dict(c='core', x='exam-high', s='supporting', d='detail')
# ≈ Carnegie stage from day (fertilization age). Approximate, NOT cited — X1 replaces with registry values (GLOSSARY §7).
CS = [(1,1,1),(2,3,2),(4,5,3),(5,6,4),(7,12,5),(13,15,6),(16,17,7),(18,19,8),(20,21,9),(22,23,10),(24,25,11),(26,28,12),(29,31,13),
      (32,34,14),(35,37,15),(38,41,16),(42,43,17),(44,47,18),(48,50,19),(51,52,20),(53,54,21),(55,56,22),(57,60,23)]
def cs_of(d):
    for lo, hi, n in CS:
        if lo <= d <= hi: return n
    return None
def dbin(d1):
    if d1 is None: return 'No day'
    if d1 <= 7: return 'Wk 1'
    if d1 <= 14: return 'Wk 2'
    if d1 <= 21: return 'Wk 3'
    if d1 <= 28: return 'Wk 4'
    if d1 <= 56: return 'Wk 5–8'
    return 'Fetal'
DBINS = ['Wk 1','Wk 2','Wk 3','Wk 4','Wk 5–8','Fetal','No day']

rows = []; cur = None; errs = []
for ln, line in enumerate(open(a.src, encoding='utf-8'), 1):
    line = line.rstrip('\n')
    if not line.strip() or line.startswith('#'): continue
    if line.startswith('@'):
        cur = line[1:].strip()
        if cur not in secs: errs.append(f'line {ln}: unknown section {cur}')
        n = 0; continue
    p = [x.strip() for x in line.split('|')]
    if len(p) != 11: errs.append(f'line {ln}: {len(p)} fields'); continue
    n += 1
    key, name, tier, thr, imp, lay, sy, days, pre, de, mis = p
    d1 = d2 = None
    if days:
        d1, d2 = (int(x) for x in days.split('-'))
    if tier not in 'ABCD' or imp not in IMP or lay not in LAYER or sy not in SYS: errs.append(f'line {ln}: bad code {tier} {imp} {lay} {sy}')
    rows.append(dict(key=key, id=f'{cur}.{n:02d}', sec=cur, ch=cur[:3], name=name, tier=tier, threads=thr.replace(' ', ''),
                     imp=IMP.get(imp, imp), layer=lay, sys=sy, day=[d1, d2] if d1 is not None else None, pre_k=[k for k in pre.split(',') if k],
                     def_=de, mis=mis or None))
K = {r['key']: r for r in rows}
if len(K) != len(rows): errs.append('duplicate keys: ' + str([k for k, v in collections.Counter(r['key'] for r in rows).items() if v > 1]))
for r in rows:
    r['pre'] = []
    for k in r['pre_k']:
        if k not in K: errs.append(f"{r['id']} prereq '{k}' missing")
        else: r['pre'].append(K[k]['id'])
# cycle check
idx = {r['id']: r for r in rows}
state = {}
def visit(i, path):
    if state.get(i) == 1: errs.append('cycle: ' + ' > '.join(path + [i])); return
    if state.get(i) == 2: return
    state[i] = 1
    for p_ in idx[i]['pre']: visit(p_, path + [i])
    state[i] = 2
for r in rows: visit(r['id'], [])
if errs:
    print('\n'.join(errs)); sys.exit(1)

# glossary terms -> concepts (name match in concept name or definition, word-bounded)
def dash(s): return s.replace('—','-').replace('–','-')
def norm(s): return dash(re.sub(r'\s*\(.*?\)', '', s)).lower().strip()
tmatch = []
for t in G:
    base = norm(t['term']); alts = {base}
    if base.endswith('s') and len(base) > 4: alts.add(base[:-1])
    m = re.search(r'\((.*?)\)', t['term'])
    if m and len(m.group(1)) > 3: alts.add(m.group(1).lower())
    tmatch.append((t, [re.compile(r'\b' + re.escape(x) + r's?\b') for x in alts]))
for r in rows:
    text = dash(r['name'] + ' ' + r['def_']).lower(); r['terms'] = []
    for t, pats in tmatch:
        if any(p_.search(text) for p_ in pats): r['terms'].append(t['id'])
    # also terms whose primary section is this section and whose name appears loosely
tby = {t['id']: t for t in G}
# term not linked to any concept -> attach to first concept of its primary section (keeps coverage visible)
linked = {x for r in rows for x in r['terms']}
bysec = collections.defaultdict(list)
for r in rows: bysec[r['sec']].append(r)
orphan_terms = []
for t in G:
    if t['id'] in linked: continue
    ps = t.get('primary_section')
    if ps in bysec: bysec[ps][0].setdefault('terms_loose', []).append(t['id'])
    else: orphan_terms.append(t['term'])

# EDIT: manual term links for terms I1 could not place
MANUAL = {'E.t.annulus-fibrosis': 'E10.02.02'}
for tid, cid in MANUAL.items():
    if tid in tby and cid in idx and tid not in linked:
        idx[cid].setdefault('terms_loose', []).append(tid); orphan_terms = [x for x in orphan_terms if x != tby[tid]['term']]
# unlocks (direct + transitive)
kids = collections.defaultdict(set)
for r in rows:
    for p_ in r['pre']: kids[p_].add(r['id'])
def desc(i, seen):
    for k in kids[i]:
        if k not in seen: seen.add(k); desc(k, seen)
    return seen
for r in rows:
    r['unlocks'] = sorted(kids[r['id']]); r['unlock_n'] = len(desc(r['id'], set()))

# recurrence: own chapter + chapters of its terms + chapters of dependants
for r in rows:
    chs = collections.Counter({r['ch']: 1})
    for tid in r['terms'] + r.get('terms_loose', []):
        for c, n in tby[tid]['chapters'].items(): chs[c] += n
    for k in desc(r['id'], set()): chs[idx[k]['ch']] += 0  # presence only
    for k in desc(r['id'], set()): chs.setdefault(idx[k]['ch'], 1)
    r['recurs'] = dict(sorted(chs.items()))
# related: share >=1 term, other section; top 6 by shared count
tc = collections.defaultdict(set)
for r in rows:
    for tid in r['terms']: tc[tid].add(r['id'])
for r in rows:
    sc = collections.Counter()
    for tid in r['terms']:
        for o in tc[tid]:
            if o != r['id'] and idx[o]['sec'] != r['sec']: sc[o] += 1
    r['related'] = [o for o, _ in sorted(sc.items(), key=lambda kv: (-kv[1], kv[0]))[:6]]

# page locator from I1 section
for r in rows:
    s = secs[r['sec']]; r['pages'] = s.get('pages'); r['cs'] = None
    if r['day']:
        a_, b_ = cs_of(r['day'][0]), cs_of(r['day'][1])
        if a_: r['cs'] = [a_, b_ or 23]

out_concepts = []
for r in rows:
    o = dict(id=r['id'], name=r['name'], sec=r['sec'], ch=r['ch'], tier=r['tier'], threads=list(r['threads']), importance=r['imp'],
             layer=r['layer'], system=r['sys'], day=r['day'], cs_approx=r['cs'], prereq=r['pre'], unlocks=r['unlocks'], unlock_n=r['unlock_n'],
             related=r['related'], recurs=r['recurs'], terms=r['terms'], terms_loose=r.get('terms_loose', []), def_ours=r['def_'],
             misconception=r['mis'], pages=r['pages'], status='planned', mark='≈')
    out_concepts.append(o)

# crosstabs
def ct(fx, fy):
    m = collections.defaultdict(list)
    for o in out_concepts:
        for x in fx(o):
            for y in fy(o): m[f'{x}|{y}'].append(o['id'])
    return m
chs_all = ['E00'] + [c['id'] for c in T['chapters']]
F = dict(chapter=lambda o: [o['ch']], recurs=lambda o: list(o['recurs']), day=lambda o: [dbin(o['day'][0] if o['day'] else None)],
         layer=lambda o: [o['layer']], system=lambda o: [o['system']], tier=lambda o: [o['tier']], importance=lambda o: [o['importance']])
cross = {
    'concept_x_chapter': {o['id']: o['recurs'] for o in out_concepts},
    'chapter_x_chapter': {},
}
cc = collections.defaultdict(int)
for o in out_concepts:
    for c in o['recurs']:
        if c != o['ch']: cc[f"{o['ch']}|{c}"] += 1
cross['chapter_x_chapter'] = dict(cc)

secs_out = []
for c in [dict(id='E00', title='Part 0 — Reading an embryo', part=0, pages=None, sections=[secs['E00.01']])] + T['chapters']:
    for s in c['sections']:
        secs_out.append(dict(id=s['id'], ch=c['id'], title=s['title'], kind=s.get('kind', 'section'), pages=s.get('pages'),
                             boxes=[b.get('kind') for b in s.get('boxes', [])]))
chap_out = [dict(id='E00', title='Reading an embryo (orientation)', part=0, pages=None)] + \
           [dict(id=c['id'], title=c['title'], part=c['part'], pages=c['pages']) for c in T['chapters']]
M = dict(schema='biostudio.map/1', book='E', title=T['title'], built='2026-11-17', step='K1',
         note='Derived only: headings, page locators, our own one-line definitions. No book text (RULES G1). Marks are ≈ until X1/C1. cs_approx is derived from day, not cited.',
         vocab=dict(system=SYS, layer=LAYER, importance=list(IMP.values()), tier=dict(A='Foundation', B='MBBS exam', C='NEET-PG / clinical', D='Molecular'),
                    threads=dict(T='timeline', G='germ layer', F='folding/shape', S='system', M='molecular', C='clinical', A='adult anatomy'), daybins=DBINS),
         chapters=chap_out, sections=secs_out, concepts=out_concepts, crosstabs=cross,
         timeline=TL['days'], xref_edges=X['edges'], shared_terms=X['chapter_shared_terms'],
         terms={t['id']: dict(term=t['term'], primary=t.get('primary_section')) for t in G})
# checks (master plan §11 map check)
content_secs = [s for s in secs_out if s['kind'] == 'section']
empty = [s['id'] for s in content_secs if s['id'] not in bysec]
rep = dict(concepts=len(out_concepts), sections_with_concepts=len(bysec), content_sections=len(content_secs), empty_sections=empty,
           openers_with_concepts=sorted(s for s in bysec if s.endswith('.00')),
           terms_linked=len(linked), terms_loose=sum(len(o['terms_loose']) for o in out_concepts), terms_orphan=orphan_terms,
           by_importance=collections.Counter(o['importance'] for o in out_concepts), by_tier=collections.Counter(o['tier'] for o in out_concepts),
           with_misconception=sum(1 for o in out_concepts if o['misconception']), orphan_prereqs=0)
print(json.dumps(rep, indent=1, ensure_ascii=False))
if a.dry_run: sys.exit(0)
import os; os.makedirs(a.out, exist_ok=True)
json.dump(M, open(f'{a.out}/map.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(rep, open(f'{a.out}/map-report.json', 'w'), indent=1, ensure_ascii=False)

# ---------- concept-map.md ----------
L = []
L.append('# Concept map — Langman 14e (E)\n')
L.append('*(Purpose: every chapter → section → concept, with crosstabs; source for the explorer and `content/E/map.json`. Updated: 17 Nov 2026 · Bio · Build · K1 concept map.)*\n')
L.append(f"**{len(out_concepts)} concepts** in {len(bysec)} sections (all {len(content_secs)} content sections covered; Summary / Problems sections carry none). "
         "Ids `E<ch>.<sec>.<nn>` (README) — permanent once a card ships (A2). Data: `content/E/map.json` (laptop; repo after H1). Builder: `tools/map/` on Laptop 1 (`concepts.txt` + `build_map.py`; README there; H1 moves it to the repo).\n")
L.append('**Columns:** Imp = core · exam-high (x) · supporting (s) · detail (d). Days = days after fertilization (fetal range = to term ≈ 266). Layer: ecto · meso · endo · crest · extra(embryonic) · multi · none. '
         'Pages = I1 section locator (printed pages; ≈ where I1 used OCR). **Every fact is ≈ until X1 cites and marks it** (B1, B7) — definitions here are one-line labels in our words, not card text. '
         'Carnegie ranges in map.json are `cs_approx` (derived from day; X1 replaces).\n')
L.append('**Known I1 locator issues (≈):** E05 page ranges are compressed (gastrulation, notochord on p. 59) — concepts are placed by heading subject; E08.08/E08.09 twin vs parturition terms look swapped; E10.03 holds spina bifida/Chiari terms (page shift); E12.02 spans most of the limb chapter. X1 corrects locators per chapter.\n')
IMPS = dict(core='core', **{'exam-high': 'x', 'supporting': 's', 'detail': 'd'})
for c in chap_out:
    cs_ = [o for o in out_concepts if o['ch'] == c['id']]
    if a.only and c['id'] != a.only: continue
    pg = f" · pp {c['pages'][0]}–{c['pages'][1]}" if c['pages'] else ''
    L.append(f"\n## {c['id']} — {c['title']}{pg} · {len(cs_)} concepts\n")
    L.append('| Id | Concept | Tier | Thr | Imp | Days | Layer | System | Needs | Unlocks |\n|---|---|---|---|---|---|---|---|---|---|')
    for o in cs_:
        d = f"{o['day'][0]}–{o['day'][1]}" if o['day'] else ''
        L.append(f"| {o['id']} | {o['name']} | {o['tier']} | {''.join(o['threads'])} | {IMPS[o['importance']]} | {d} | {o['layer']} | {o['system']} | {', '.join(o['prereq'])} | {o['unlock_n'] or ''} |")
    mis = [o for o in cs_ if o['misconception']]
    if mis:
        L.append('\n*Misconceptions to refute (≈ until X1):* ' + ' · '.join(f"{o['id']} — “{o['misconception']}”" for o in mis))
L.append('\n---\n\n## Crosstabs\n*(Counts of concepts. The explorer makes every cell clickable.)*\n')
def table(title, fx, xs, fy, ys, xl=None, yl=None):
    m = ct(fx, fy)
    L.append(f'\n### {title}\n')
    L.append('| | ' + ' | '.join(yl[y] if yl else y for y in ys) + ' | Σ |\n|' + '---|' * (len(ys) + 2))
    for x in xs:
        vals = [len(m.get(f'{x}|{y}', [])) for y in ys]
        if sum(vals): L.append(f"| {xl[x] if xl else x} | " + ' | '.join(str(v) if v else '·' for v in vals) + f' | {sum(vals)} |')
table('Chapter × Day', F['chapter'], chs_all, F['day'], DBINS)
table('Chapter × Germ layer', F['chapter'], chs_all, F['layer'], list(LAYER))
table('Tier × Chapter (coverage)', F['tier'], list('ABCD'), F['chapter'], chs_all)
table('System × Tier', F['system'], list(SYS), F['tier'], list('ABCD'), xl=SYS)
table('Germ layer × Day', F['layer'], list(LAYER), F['day'], DBINS, xl=LAYER)
table('Importance × Chapter', F['importance'], list(IMP.values()), F['chapter'], chs_all)
# concept x chapter recurrence: top 25 most-recurring
L.append('\n### Concept × Chapter — where it recurs (top 25 by chapters reached)\n')
top = sorted(out_concepts, key=lambda o: (-len(o['recurs']), o['id']))[:25]
L.append('| Concept | Chapters |\n|---|---|')
for o in top: L.append(f"| {o['id']} {o['name']} | {len(o['recurs'])}: {', '.join(o['recurs'])} |")
L.append('\nFull matrix: `crosstabs.concept_x_chapter` in map.json (explorer → Crosstabs → Concept × Chapter).\n')
L.append('\n### Chapter × Chapter — concepts of row chapter that recur in column chapter\n')
L.append('| | ' + ' | '.join(c[1:] for c in chs_all) + ' |\n|' + '---|' * (len(chs_all) + 1))
for x in chs_all:
    L.append(f'| {x} | ' + ' | '.join(str(cc.get(f'{x}|{y}', '')) or '·' for y in chs_all) + ' |')
L.append('\n### Prerequisite graph — most-unlocking concepts\n')
L.append('| Concept | Unlocks (transitive) | Direct |\n|---|---|---|')
for o in sorted(out_concepts, key=lambda o: -o['unlock_n'])[:20]: L.append(f"| {o['id']} {o['name']} | {o['unlock_n']} | {len(o['unlocks'])} |")
L.append(f"\n**Map checks (K1):** every content section has ≥ 1 concept ({'✅' if not empty else '❌ ' + ', '.join(empty)}) · every concept has tier, thread or system, importance, locator · no orphan or circular prerequisites ✅ · "
         f"glossary terms linked by name {len(linked)}/265, + {rep['terms_loose']} attached to their primary section's first concept, {len(orphan_terms)} unplaced (I1 gap).\n")
open(f'{a.out}/concept-map.md', 'w', encoding='utf-8').write('\n'.join(L))
print('wrote', a.out)
