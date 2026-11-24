/* S1E01 animatic — stage + player (P1 ②; RULES H3–H6, C13, I5, I6). Owner docs: episodes/S1E01/storyboard.md, visual-style §1/§10, scene-spec §8.
   Serve Studio home (serve.py) and open /tools/s1e01-animatic/ (works the same from the repo's tools/s1e01-animatic/).
   URL: ?cut=lesson|general|short · ?t=12.5 · ?debug=1|layout|timing · ?boxes=1 (bands drawn) · ?test=1 (✎ hooks) · ?safe=1 (Shorts UI) · ?rm=1 (reduced motion) · ?record=1 (bare stage, seek by window.seek).
   Data: content/E/episodes/S1E01/*.json + scenes (read only) · out/timeline.json + out/<cut>.wav (Studio home, never committed). EDIT: positions in bands.mjs, shots in shots.mjs. */
import { BANDS, MIN_PX } from './bands.mjs';
import { SHOTS, LABELS, T_MESO, GHOSTS, COMPRESSED, CLARITY, LATE, FROM_START, ALT } from './shots.mjs';
const here = new URL('.', location.href), inRepo = /\/repo\/[^/]+\/tools\//.test(here.pathname);
const REPO = new URL(inRepo ? '../../' : '../../repo/biology-studio/', here), MEDIA = new URL(inRepo ? '../../../../tools/s1e01-animatic/out/' : 'out/', here);
const Q = new URLSearchParams(location.search), dbg = k => { const d = Q.get('debug'); return d === '1' || (d || '').split(',').includes(k); };
const REC = Q.has('record'), MQ = matchMedia('(prefers-reduced-motion: reduce)'); let RM = Q.has('rm') || MQ.matches; MQ.addEventListener('change', () => { RM = Q.has('rm') || MQ.matches; draw(); });
const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = new URL('src/css/app.css', REPO); document.head.prepend(css); await new Promise(r => { css.onload = css.onerror = r; });
const E = await import(new URL('src/js/14-scene3d.mjs', REPO));
const J = u => fetch(u).then(r => { if (!r.ok) throw new Error(u + ' ' + r.status); return r.json(); });
const [TL, shotsJ, script, s4, s5] = await Promise.all([J(new URL('timeline.json', MEDIA)), J(new URL('content/E/episodes/S1E01/shots.json', REPO)), J(new URL('content/E/episodes/S1E01/script.json', REPO)),
  J(new URL('content/E/scenes/sc-E00.01.04.json', REPO)), J(new URL('content/E/scenes/sc-E05.02.01.json', REPO))]);
await document.fonts.ready;
const META = Object.fromEntries(shotsJ.shots.map(s => [s.id, s]));
const SC = { 'sc-E00.01.04': s4, 'sc-E05.02.01': s5 };
for (const s of Object.values(SC)) s.parts.push(T_MESO, ...GHOSTS);   // N4 stub: in memory only; the engine draws no tracer (state.trace stays null)
const variants = {};
function sceneOf(seg) {   // opacity / ectoderm-token variants of a scene, cached (N6 stub: "Ectoderm" carries the ecto token once it is named)
  const k = JSON.stringify([seg.scene, seg.op || 0, seg.ecto || 0]);
  if (!variants[k]) { const c = structuredClone(SC[seg.scene]); for (const l of c.layers) { if (seg.op && seg.op[l.id] != null) l.opacity = seg.op[l.id]; if (seg.ecto && l.id === 'epiblast') l.token = 'ecto'; if (l.id === 'streak') l.ring = false; } c._k = k; variants[k] = c; }
  return variants[k];
}
const st = { cut: Q.get('cut') || 'lesson', t: +(Q.get('t') || 0), play: false, caps: true, full: false };
const el = (h) => { const d = document.createElement('template'); d.innerHTML = h.trim(); return d.content.firstChild; }, esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const app = document.getElementById('app'); if (REC) document.body.classList.add('rec');
app.setAttribute('role', 'main'); app.innerHTML = `<h1 class="vh">S1E01 Gastrulation animatic</h1><div class="stagebox"><div class="stage stage-dark" role="img"><canvas aria-hidden="true"></canvas><div class="ov" aria-hidden="true"></div></div></div>` + (REC ? '' : `<div class="side"><div class="ctl" role="group" aria-label="Player">
 <button class="keep" id="pp" aria-label="Play">▶</button><button id="prev" aria-label="Previous shot">⏮</button><button id="next" aria-label="Next shot">⏭</button>
 <input type="range" id="sk" min="0" step="0.05" aria-label="Position"><select id="cut" aria-label="Cut"><option value="lesson">MBBS Lesson</option><option value="general">General</option><option value="short">Short</option></select>
 <button id="cc" aria-pressed="true" aria-label="Captions">CC</button><button class="keep" id="fs" aria-label="Full screen">⛶</button></div><div class="panel" id="tr" tabindex="0" role="region" aria-label="Transcript"></div></div><audio id="au" preload="auto"></audio>`);
const stage = app.querySelector('.stage'), box = app.querySelector('.stagebox'), ov = app.querySelector('.ov'), canvas = app.querySelector('canvas'), $ = s => app.querySelector(s), au = $('#au');
const V = E.createViewer(canvas, () => stage, { dprCap: 2, still: REC });
if (!V.ok) { box.textContent = 'This animatic needs WebGL: ' + V.err; throw new Error(V.err); }
V.setTokens();
const isShort = () => st.cut === 'short', B = () => isShort() ? BANDS.short : BANDS.lesson;
let W = 0, H = 0;
function layout() {
  const iw = innerWidth, ih = innerHeight, land = iw > ih;
  document.body.classList.toggle('pl', !REC && !st.full && land && ih < 500); document.body.classList.toggle('wide', !REC && !st.full && land && ih >= 500); document.body.classList.toggle('full', st.full);
  const a = isShort() ? 9 / 16 : 16 / 9; let mw = iw, mh = ih;
  if (!REC && !st.full) { if (land && ih < 500) mw = iw - 145; else if (land) mw = iw - Math.max(280, iw * 0.3); else mh = isShort() ? ih - 260 : Math.min(ih * 0.6, iw / a); }
  W = Math.min(mw, mh * a); H = W / a; W = Math.round(W); H = Math.round(H);
  stage.style.setProperty('--sw', W + 'px'); stage.style.setProperty('--sh', H + 'px'); V.resize(W, H); key = ''; draw();
}
let key = '', sceneNow = null, camNow = null;
const lerp = (a, b, t) => a + (b - a) * t, ease = t => t * t * (3 - 2 * t), clamp = t => Math.max(0, Math.min(1, t));
/* the engine's orthographic camera, mirrored for the overlay (placeCamera in 14-scene3d.mjs) */
function proj(p) { const c = camNow, d = (u, v) => u[0] * v[0] + u[1] * v[1] + u[2] * v[2]; return { x: (d(c.r, p) / (2 * c.hw) - c.pan + 0.5) * W, y: (0.5 - d(c.u, p) / (2 * c.hh) + c.shift) * H }; }
function camera(seg, f, S, day) {
  const e = RM ? 1 : ease(f), [a, b] = seg.v; let az = lerp(a[0], b[0], e), elv = lerp(a[1], b[1], e), zoom = lerp(a[2], b[2], e) * (!isShort() && H < 260 && !seg.cut.on ? 0.68 : 1);   // phone-portrait Lesson: the disc stays above the axes stack
  const A = az * Math.PI / 180, L = elv * Math.PI / 180, back = [Math.cos(L) * Math.cos(A), Math.cos(L) * Math.sin(A), Math.sin(L)], n = Math.hypot(back[0], back[1]), r = [-back[1] / n, back[0] / n, 0];
  const u = [back[1] * r[2] - back[2] * r[1], back[2] * r[0] - back[0] * r[2], back[0] * r[1] - back[1] * r[0]];
  const fit = E.keyState(S, day).fit_mm / S.units.mm_per_unit, view = fit / zoom, asp = W / H, hh = asp >= 1 ? view / 2 : view / 2 / asp, hw = asp >= 1 ? hh * asp : view / 2;
  return { az, elv, zoom, r, u, hh, hw, pan: 0, shift: 0 };
}
const cellAt = (S, day, id = 't-meso') => { const d = S.days; return E.traceAt(S, id, Math.max(15, day)); };
const pt = a => [a.x, a.y, a.z];
/* one frame at time t */
function draw() {
  const C = TL[st.cut], t = Math.max(0, Math.min(C.dur - 0.001, st.t)), shot = C.shots.findLast(s => s.s <= t) || C.shots[0], m = META[shot.id], F = clamp((t - shot.s) / (shot.e - shot.s));
  const segs = SHOTS[shot.id + '_' + st.cut] || SHOTS[shot.id], seg = segs.findLast(s => s.f[0] <= F) || segs[0], f = clamp((F - seg.f[0]) / (seg.f[1] - seg.f[0]));
  const line = C.lines.findLast(l => l.s <= t), cap = line && line.caps.find(c => t >= c.s && t < c.e), lines = C.lines.filter(l => l.shot === shot.id);
  let S = null, day = null; const is3 = !!seg.scene;
  canvas.style.visibility = is3 ? 'visible' : 'hidden';
  if (is3) {
    S = sceneOf(seg); day = lerp(seg.day[0], seg.day[1], f);
    camNow = camera(seg, f, S, day);
    const k = S._k; if (key !== k) { V.setScene(S, { day, cut: seg.cut, az: camNow.az, el: camNow.elv, zoom: camNow.zoom, trace: null }); key = k; sceneNow = S; } else { V.setCut({ slab_mm: 0, ...seg.cut }); V.setDay(day); V.view(camNow.az, camNow.elv, camNow.zoom); }
    /* frame the focus (or the subject) in the subject band */
    const an = V.anchors(false); let fp = [0, 0, 0];
    if (seg.focus === 'cell') fp = pt(cellAt(S, day)); else if (seg.fx) fp = [lerp(seg.fx[0], seg.fx[1], RM ? 1 : ease(f)) * E.keyState(S, day).params.length_units / 2, 0, 0]; else if (seg.focus && an[seg.focus]) fp = an[seg.focus].p;
    const b = B().subject, cy = seg.cy ?? (isShort() ? 0.51 : seg.cut.on ? (H < 260 && seg.cyP ? seg.cyP : 0.385) : H < 260 ? 0.33 : 0.45), cx = seg.cx ?? (isShort() || seg.fx ? 0.5 : seg.cut.on ? 0.43 : 0.525); const c = camNow, dt = (u, v) => u[0] * v[0] + u[1] * v[1] + u[2] * v[2], kf = RM || !seg.focus || isShort() || seg.fx ? 1 : ease(f) * 0.5 + 0.5;
    c.pan = dt(c.r, fp) * kf / (2 * c.hw) - (cx - 0.5); c.shift = dt(c.u, fp) * kf / (2 * c.hh) - (0.5 - cy);
    V.setPan(c.pan); V.setShift(c.shift);
  }
  overlay({ C, t, shot, m, seg, f, F, line, cap, lines, S, day, is3 });
  if (!REC) ui(C, t, line, shot);
  const lv = document.getElementById('dbg'); if (lv) lv.textContent = `${st.cut} ${shot.id} ${F.toFixed(2)} t=${t.toFixed(2)}/${C.dur}\nday ${day == null ? '-' : day.toFixed(2)} ${W}×${H} ${V.info().triangles} tris`;
}
const termsOf = id => { const m = META[id], gen = st.cut === 'general'; let a = ((gen && m.labels_general) || m.labels || []).filter(x => !(LATE[id] || []).includes(x)); if (id === 'S12') a = ['Epiblast', ...a]; if (id === 'S23') a = ['Mesoderm', ...(gen ? ['Epiblast', 'Old bottom layer', 'One each'] : ['Becomes endoderm', 'Is replaced'])]; return [...new Set(a)]; };
const extraTags = id => [META[id].tag, META[id].tag_also].flat().concat(st.cut !== 'short' && CLARITY.test(id) ? 'Exaggerated for clarity' : [], st.cut !== 'short' && COMPRESSED.test(id) ? 'Time compressed' : [], id === 'S16' ? 'Book version' : [], META[id].clinical ? 'Clinical link' : []).filter(Boolean).filter((x, i, A) => A.indexOf(x) === i);
const PAD = 'rgb(10 11 13/.82)';
function overlay(o) {
  const { C, t, shot, m, seg, f, cap, lines, S, day, is3 } = o, sh = isShort(), b = B(), px = (n, min = 0) => Math.max(min, n) + 'px', Y = p => p / 100 * H, X = p => p / 100 * W;
  const fsCap = Math.max(MIN_PX.caption, sh ? W * 0.058 : H * 0.05), fsTag = Math.max(MIN_PX.tag, sh ? Math.min(W * 0.045, 99) : H * 0.045), fsLab = Math.max(MIN_PX.label, sh ? W * 0.058 : H * 0.047), fsSt = Math.max(sh ? 9 : MIN_PX.tag, sh ? W * 0.032 : H * 0.032);
  let h = '', svg = '';
  const words = lines.flatMap(l => l.words);
  if (is3) {
    const u = S.units.mm_per_unit, an = V.anchors(false), ppu = H / (2 * camNow.hh), an2 = {}, Pm = E.keyState(S, day).params, dL = Pm.length_units, dW = Pm.width_ratio * dL, disc = S.parts.find(p => p.kind === 'disc'); for (const k in an) an2[k] = proj(an[k].p);
    if (an.node) an2.node = proj([an.node.p[0] - 0.08, 0, an.node.p[2]]);
    if (an.mesoderm && !seg.cut.on) { const c = cellAt(S, seg.cellDay || day); an2.mesoderm = proj([c.x, -c.y, an.mesoderm.p[2]]); }   // the mirror of the marked cell: always inside the sheet
    const hl = dL / 2, te = disc.epiblast_thick, g0 = disc.gap, th = disc.hypoblast_thick, side = seg.cut.on && seg.cut.axis === 'y', head = seg.cut.on && seg.cut.axis === 'x';
    const x0 = head ? seg.cut.at * hl : -hl, x1 = seg.cut.slab_mm ? x0 + seg.cut.slab_mm / u : hl, y0 = side ? seg.cut.at * dW / 2 : -dW / 2, onCut = p => side ? [p[0], y0, p[2]] : head ? [x0, p[1], p[2]] : p;   // on a section the marked cells are drawn on the cut face, in their layer
    const hwid = x => { const c = Math.max(-1, Math.min(1, x / hl)); return dW / 2 * Math.sqrt(1 - c * c) * (1 + 0.5 * (Pm.pear || 0) * c); }, U = E.keyState(S, day).u, mK = (disc.meso_delay ? (Pm.meso ?? 0, 0.75 * Math.max(0, (U - 0.3) / 0.7)) : Pm.meso || 0) * 0.97, eK = (Pm.endo || 0) * 0.97, anc = -0.47 * dL, inner = (k, x) => k > 0.02 ? hwid(anc + (x - anc) / k) * k : 0;
    const corners = []; { const N = 24; for (let i = 0; i <= N; i++) { const x = head ? x0 + (x1 - x0) * i / N : -hl + dL * i / N, w = hwid(x); for (const z of [-g0 - th, te]) { corners.push([x, side ? y0 : w, z], [x, side ? w : -w, z]); } } }
    const bx = { l: 1e9, r: -1e9, t: 1e9, b: -1e9 }; for (const c of corners) { const q = proj(c); bx.l = Math.min(bx.l, q.x); bx.r = Math.max(bx.r, q.x); bx.t = Math.min(bx.t, q.y); bx.b = Math.max(bx.b, q.y); } bx.t -= camNow.zoom * H * 0.006;
    const path = cellAt(S, seg.cellDay || day), cp = path && proj(onCut(pt(path))), gr0 = Math.max(4, H * 0.011) * (sh ? 0.62 : 1);
    if (seg.glow && an.streak) { const A = proj([-0.82 * hl, 0, te]), N2 = proj([an.node ? an.node.p[0] : 0, 0, te]); svg += `<line x1="${A.x}" y1="${A.y}" x2="${N2.x}" y2="${N2.y}" stroke="#ECEDEF" stroke-opacity="${RM ? 0.35 : 0.25 + 0.2 * clamp(f * 3)}" stroke-width="${W * 0.045}" stroke-linecap="round" style="filter:blur(${W * 0.012}px)"/>`; }
    if (seg.lit && side) { const q = (a, b, z0, z1, st) => { const P = [[a, z0], [b, z0], [b, z1], [a, z1]].map(([x, z]) => { const p = proj([x, y0, z]); return p.x + ',' + p.y; }).join(' '); svg += `<polygon points="${P}" ${st}/>`; }; q(-hl, hl, -g0 - th, -0.005, 'fill="#14161A" fill-opacity=".5"'); q(-hl, hl, 0, te, `fill="var(--g-${seg.ecto ? 'ecto' : 'epi'})" fill-opacity=".72" stroke="#ECEDEF" stroke-width="1.5"`); }   // "left on top": the cut face of the top layer lit, the rest dimmed
    if (seg.ghost) for (const g of GHOSTS) { const a = E.traceAt(S, g.id, day), p = proj(onCut(pt(a))), q = seg.gsq && a.in !== 'endoderm' ? (RM ? 1.25 : 1 + 0.5 * Math.sin(Math.PI * clamp(f))) : 1; svg += `<ellipse cx="${p.x}" cy="${p.y}" rx="${gr0 / q}" ry="${gr0 * q}" fill="var(--g-ctx)" stroke="#14161A" stroke-width="1.5"/>`; }
    if (seg.stream) { const n = an.node; if (n) for (let i = 0; i < 4; i++) { const q = ((RM ? 0 : t * 0.25) + i / 4) % 1, p = proj([n.p[0] + q * (Pm.noto || 0.5) * 0.9, 0, -0.1]); svg += `<circle cx="${p.x}" cy="${p.y}" r="${Math.max(3, H * 0.008)}" fill="var(--g-ctx)" stroke="#fff" stroke-width="1.5"/>`; } }
    const kr = Math.max(0.55, Math.min(1, (sh ? W : H) / 560)); const dbl = (x, y, rx, ry) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="none" stroke="#14161A" stroke-width="${7.5 * kr}"/><ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="none" stroke="#fff" stroke-width="${6 * kr}"/><ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="none" stroke="var(--accent-on-dark)" stroke-width="${3.5 * kr}"/>`;
    const qi = seg.check && o.line ? C.lines.filter(l => l.shot === shot.id).findIndex(l => l.id === o.line.id) : -1, cellOn = seg.check ? o.line && /^(L31a|G15a)$/.test(o.line.id) : seg.cell; o.cellOn = cellOn;
    if (cellOn && cp) { const Rc = Math.max(5, sh ? W * 0.017 : H * 0.017) * (shot.id === 'S12' ? 0.65 : 1), sq = seg.squash && !RM ? 1 + 0.5 * Math.sin(Math.PI * clamp(f)) : 1, al = seg.cell || 1;
      svg += `<g opacity="${al}"><ellipse cx="${cp.x}" cy="${cp.y}" rx="${Rc / sq}" ry="${Rc * sq}" fill="var(--g-ctx)" stroke="#14161A"/>${dbl(cp.x, cp.y, Rc / sq + 3, Rc * sq + 3)}</g>`; an2.cell = cp; }
    const zS = camNow.zoom; if (seg.ring === 'caudal') { const c = proj([-0.75 * hl, 0, te]); an2.streak = c; svg += dbl(c.x, c.y, zS * H * 0.045, zS * H * 0.075); }
    else if (seg.ring && an2[seg.ring]) { const p = an2[seg.ring]; svg += seg.ring === 'streak' ? dbl(p.x, p.y, zS * H * 0.03, zS * H * 0.085) : dbl(p.x, p.y, zS * H * 0.035, zS * H * 0.03); }
    if (seg.entry) { const p = proj([-0.82 * hl, 0, te]); svg += dbl(p.x, p.y, H * 0.03, H * 0.03); an2.streak = p; }
    /* labels (visual-style §12): on the spoken word, outside the outline, chip + leader ≤ 25 % of the width; R right · L left · U above · D below · LE left elbow (Short) */
    const want = (seg.lab || (st.cut === 'general' && m.labels_general ? m.labels_general : m.labels)).slice(); if (seg.check) { want.length = 0; if (cellOn) want.push('Mesoderm'); }
    const s1 = head ? Math.sign(camNow.r[1]) || 1 : 1, zL = { epiblast: te * 0.4, hypoblast: -g0 - th / 2, endoderm: -g0 - th / 2, mesoderm: (-g0 + 0.015) / 2 }, front = k => -0.94 + 1.94 * k;
    const place = (name, ak) => {
      if (side && ak in zL) { const z = zL[ak], P = fx => proj([fx * hl, y0, z]); if (ak === 'epiblast') return { ty: sh ? 'U' : 'R', p: P(sh ? 0.5 : 0.96) }; if (ak === 'hypoblast') return { ty: sh ? 'D' : 'R', p: P(Math.max(0.95, front(eK) + 0.01)) }; if (ak === 'endoderm') return { ty: 'D', p: P(-0.94 + (front(eK) + 0.94) * 0.6) }; return { ty: sh ? 'LE' : 'L', p: P(-0.93) }; }
      if (head && ak in zL) { const z = zL[ak], w = ak === 'mesoderm' ? inner(mK, x0) : ak === 'endoderm' ? inner(eK, x0) : hwid(x0), P = k => proj([x0, k * s1 * w, z]); if (ak === 'mesoderm' && sh) return { ty: 'LE', p: P(-0.95) }; if (sh) return { ty: ak === 'epiblast' ? 'U' : 'D', p: P(-0.4) }; return { ty: 'R', p: P(0.96) }; }
      if (seg.cut.on) return { ty: sh && name === 'Marked cell' && head ? 'D' : 'U', p: an2[ak] };
      if (ak === 'epiblast' && !sh) return { ty: 'R', p: proj([0, -0.82 * dW / 2, te]) };
      if (!sh && name === 'Marked cell' && an2[ak].x < (bx.l + bx.r) / 2) return { ty: 'L', p: an2[ak] };
      return { ty: sh ? 'U' : 'R', p: an2[ak] };
    };
    const L = []; for (const name of want) { const [ak] = LABELS[name] || [null]; if (!ak || !(ak in an2) || (LATE[shot.id] || []).includes(name)) continue; const re = LABELS[name][1], w = words.find(x => re.test(x[0])), on = seg.check || seg.lab || (FROM_START[shot.id] || []).includes(name) || !w || t >= w[1] - 0.05; if (on) L.push({ name, ...place(name, ak) }); }
    const TOK = { Epiblast: 'epi', Ectoderm: 'ecto', Hypoblast: 'hypo', Mesoderm: 'meso', Endoderm: 'endo', Notochord: 'meso' }, gap = fsLab * 1.55, lw = Math.max(1.5, (sh ? W : H) / 240), wp = q => q.name.length * fsLab * 0.55 + fsLab * 2.1;
    const lead = (P, pts) => { const d = [P, ...pts].map(q => q.x + ',' + q.y).join(' '); svg += `<polyline points="${d}" fill="none" stroke="#14161A" stroke-width="${lw + 2}"/><polyline data-ld="${Math.hypot(P.x - pts[pts.length - 1].x, P.y - pts[pts.length - 1].y) / W * 100}" points="${d}" fill="none" stroke="#fff" stroke-width="${lw}"/><circle cx="${P.x}" cy="${P.y}" r="${lw * 1.6}" fill="#fff" stroke="#14161A"/>`; };
    const tag = (q, lx, ly) => { h += `<div class="lab" data-k="label" data-ty="${q.ty}" style="left:${lx}px;top:${ly}px;font-size:${fsLab}px"><i class="sw L-${TOK[q.name] || 'ctx'}"></i>${esc(q.name)}</div>`; };
    const zTop = sh ? Y(38) + fsLab * 0.8 : Y(17), zBot = sh ? Y(63.5) - fsLab * 0.8 : Y(80), maxR = X(sh ? 86 : 96);
    for (const [ty, dir] of [['U', -1], ['D', 1]]) { const G = L.filter(q => q.ty === ty).sort((a, c) => a.p.x - c.p.x); G.forEach(q => { q.w = wp(q); q.lx = Math.max(X(4) + q.w / 2, Math.min(maxR - q.w / 2, q.p.x)); q.ly = dir < 0 ? Math.max(zTop, bx.t - fsLab * 1.15) : Math.min(zBot, bx.b + fsLab * 1.15); });
      for (let n = 1; n < G.length; n++) { const a = G[n - 1], c = G[n], need = (a.w + c.w) / 2 + fsLab * 0.4 - (c.lx - a.lx); if (need <= 0) continue; if (G.length === 2 && a.w + c.w + fsLab < maxR - X(4)) { a.lx -= need / 2; c.lx += need / 2; const lo = X(4) + a.w / 2 - a.lx, hi = c.lx + c.w / 2 - maxR; if (lo > 0) { a.lx += lo; c.lx += lo; } else if (hi > 0) { a.lx -= hi; c.lx -= hi; } } else { a.ly += dir * gap; c.lx = Math.min(maxR - c.w / 2, Math.max(c.lx, a.p.x + c.w / 2 + fsLab * 0.4)); } }
      for (const q of G) { q.ly = Math.max(zTop, q.ly); if (dir > 0 && L.some(k => k.ty === 'LE')) q.ly = Math.min(zBot, q.ly + gap * 1.2); lead(q.p, [{ x: q.lx, y: q.ly - dir * fsLab * 0.6 }]); tag(q, q.lx, q.ly); } }
    { const G = L.filter(q => q.ty === 'R').sort((a, c) => a.p.y - c.p.y), mid = G.reduce((a, q) => a + q.p.y, 0) / (G.length || 1); let last = -1e9; G.forEach((q, i) => { const w = wp(q), lx = Math.min(maxR - w, Math.max(bx.r + W * 0.025, q.p.x + W * 0.04)); let ly = seg.cut.on ? mid + (i - (G.length - 1) / 2) * gap : Math.max(Y(16), Math.min(H < 260 ? Y(50) : Y(60), q.p.y)); ly = Math.max(ly, last + gap); last = ly; lead(q.p, [{ x: lx, y: ly }]); tag(q, lx + w / 2, ly); }); }
    for (const q of L.filter(q => q.ty === 'L')) { const w = wp(q), lx = Math.max(X(3), Math.min(q.p.x, bx.l) - W * 0.03 - w); const ly = seg.cut.on ? q.p.y : Math.min(q.p.y, Y(48)); lead(q.p, [{ x: lx + w, y: ly }]); tag(q, lx + w / 2, ly); }
    for (const q of L.filter(q => q.ty === 'LE')) { const w = wp(q), ex = Math.max(X(5), Math.min(q.p.x, bx.l) - W * 0.025), lx = Math.max(X(4) + w / 2, ex + w * 0.1), ly = Math.min(zBot, bx.b + fsLab * 1.2); lead(q.p, [{ x: ex, y: q.p.y }, { x: ex, y: ly - fsLab * 0.6 }]); tag(q, lx, ly); }
    window._bx = { l: bx.l / W * 100, r: bx.r / W * 100, t: bx.t / H * 100, b: bx.b / H * 100, sec: seg.cut.on, close: !!(seg.focus || seg.fx || zS > 4) };
    /* stamp (N11: counts back on a rewind), scale bar, axes, honesty tag */
    let sd = day, pre = ''; if (seg.rewind && !RM && t - shot.s < 1.2) { sd = lerp(seg.rewind, day, clamp((t - shot.s) / 1.2)); pre = '◀ '; } if (seg.day[0] > seg.day[1] && f < 1) pre = '◀ ';
    const sp = E.stampOf(SC[seg.scene], sd), stamp = `${pre}Day ${sp.day} · ${sp.stage} · ${sp.size}`;
    const maxBar = sh ? X(b.blockW) * 0.8 : W * 0.14, mm = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1].filter(v => v / u * ppu <= maxBar).pop() || 0.01, bar = mm / u * ppu;
    const dirOf = v => ({ x: camNow.r[0] * v[0] + camNow.r[1] * v[1] + camNow.r[2] * v[2], y: -(camNow.u[0] * v[0] + camNow.u[1] * v[1] + camNow.u[2] * v[2]) }), ax = { cranial: dirOf([1, 0, 0]), left: dirOf([0, 1, 0]), dorsal: dirOf([0, 0, 1]) }, N = { cranial: ['Cr', 'Cd'], left: ['L', 'R'], dorsal: ['D', 'V'] }, gz = sh ? Y(b.axes[1] - b.axes[0]) : Math.max(56, H * 0.17), gf = sh ? Math.max(Math.min(10.5, gz * 0.27), W * 0.03) : Math.max(MIN_PX.tag, H * 0.03), gr = gz / 2 - gf * 1.05;
    let g = ''; const used = []; for (const k of Object.keys(N).sort((a, c) => Math.hypot(ax[c].x, ax[c].y) - Math.hypot(ax[a].x, ax[a].y))) { const d = ax[k], l = Math.hypot(d.x, d.y); if (l < 0.3) continue; const hlt = seg.axes && k === 'cranial'; for (const s of [1, -1]) { const ux = d.x / l * s, uy = d.y / l * s, tx = gz / 2 + ux * (gr + gf * 0.5), ty = gz / 2 + uy * (gr + gf * 0.5); if (used.some(q => Math.hypot(q.x - tx, q.y - ty) < gf * 1.15)) continue; used.push({ x: tx, y: ty }); g += `<line x1="${gz / 2}" y1="${gz / 2}" x2="${gz / 2 + ux * gr * 0.9}" y2="${gz / 2 + uy * gr * 0.9}" stroke="${hlt ? 'var(--accent-on-dark)' : '#fff'}" stroke-width="${hlt ? 3.5 : 1.5}"/><text x="${tx}" y="${ty + gf * 0.36}" font-size="${gf}" font-weight="700" fill="#fff" text-anchor="middle">${N[k][s > 0 ? 0 : 1]}</text>`; } }
    const giz = `<svg style="position:static;width:${gz}px;height:${gz}px;background:${PAD};border-radius:6px;flex:none">${g}</svg>`, barH = `<div data-k="scale" style="flex:none"><div style="width:${bar}px;height:${Math.max(3, H * 0.006)}px;background:#fff;outline:1px solid #14161A"></div><span class="chip" style="font-size:${fsSt}px">${mm >= 1 ? mm + ' mm' : mm * 1000 + ' µm'}</span></div>`;
    const tags = [m.tag, !sh && CLARITY.test(shot.id) && (seg.check ? cellOn : true) ? 'Exaggerated for clarity' : '', !sh && H >= 260 && COMPRESSED.test(shot.id) ? 'Time compressed' : '', seg.book ? '⚑ Book version' : ''].filter(Boolean).filter((x, i, A) => A.indexOf(x) === i).join(' · ');
    if (sh) { h += `<div class="abs" data-k="stamp" style="left:0;right:0;text-align:center;top:${Y(b.stamp[0])}px"><span class="chip" style="font-size:${fsSt}px;line-height:${Y(2)}px">${stamp}</span></div>`;
      h += `<div class="abs" data-k="axes" style="left:${X(b.left)}px;top:${Y(b.axes[0])}px;height:${Y(b.axes[1] - b.axes[0])}px;width:${X(b.blockW)}px;display:flex;flex-direction:column;justify-content:space-between;align-items:flex-start">${giz}</div><div class="abs" style="left:${X(b.left) + gz + Math.max(8, W * 0.02)}px;top:${Y(b.axes[0] + 2)}px">${barH}</div>`;
      if (m.tag) h += `<div class="abs" data-k="tag" style="left:${X(b.left)}px;top:${Y(b.tag[0])}px"><span class="chip" style="font-size:${fsTag}px;line-height:${Y(3)}px;white-space:nowrap">${tags}</span></div>`; }
    else h += `<div class="abs" data-k="stack" style="left:${X(b.safe)}px;bottom:${H - Y(b.stackBottom)}px;display:flex;gap:${Math.max(6, H * 0.012)}px;align-items:flex-end">${giz}<div style="display:flex;flex-direction:column;gap:${Math.max(2, H * 0.01)}px;align-items:flex-start"><span class="chip" data-k="stamp" style="font-size:${fsSt}px">${stamp}</span>${barH}<span class="chip" data-k="tag" style="font-size:${fsTag}px">${tags}</span></div></div>`;
    if (cellOn || seg.ghost || seg.ecto) h += `<div class="stub" data-k="stub" style="font-size:${fsTag * 0.85}px;${sh ? `right:${X(b.right)}px;top:${Y(25)}px` : `right:${X(5)}px;top:${Y(5)}px`}">STUB ${[cellOn || seg.ghost ? 'N3 N4' : '', seg.ecto ? 'N6' : ''].filter(Boolean).join(' ')}</div>`;
    if (seg.hostInset) h += `<div class="abs" data-k="host" style="right:${X(14)}px;top:${Y(57)}px;width:${X(28)}px;height:${Y(7)}px;background:#2A2D33;border:2px dashed #A9AEB7;display:grid;place-items:center;font-size:${fsTag}px;line-height:1.25;text-align:center">Nani cut-in · N1</div>`;
  } else if (seg.host) {
    h += `<div class="card" style="font-size:${fsLab}px"><div class="in"${seg.strip ? ' style="position:absolute;left:5%;top:15%;max-width:44%;padding:.5em .8em;font-size:.85em"' : ''}>Host placeholder<b>Nani</b>${esc(seg.host)}<br><span class="mut" style="color:#D6D8DC">cam_lesson 16:9 (planned, N1)</span></div></div>`;
    if (seg.strip) { const l = lines[0]; h += `<div class="terms" style="left:50%;transform:translateX(-50%);bottom:${H - Y(80)}px;flex-wrap:nowrap;white-space:nowrap;font-size:${fsLab * 1.1}px">${l.new.filter(n => { const w0 = n.split(' ')[0].toLowerCase(), w = l.words.find(x => x[0].toLowerCase().startsWith(w0)); return !w || t >= w[1] - 0.05; }).map(n => `<i>${esc(n)}</i>`).join('')}</div>`; }
  } else if (seg.diagram) {
    const ad = seg.diagram === 'adult', w = words.find(x => LABELS[m.labels[0]][1].test(x[0])), on = !w || t >= w[1] - 0.05, cx = W * 0.4, cy = H * 0.4, r = H * 0.125, lw = Math.max(1.5, H / 240), ring = (x, y, rx, ry) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#A9AEB7" stroke="#fff" stroke-width="6"/><ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="none" stroke="var(--accent-on-dark)" stroke-width="3.5"/>`;
    const grow = ad ? 1 : on ? lerp(0.22, 0.55, RM ? 1 : clamp((t - (w ? w[1] : 0)) / 1.2)) : 0.16, tx = cx + r * 1.55, ty = cy + r * 0.85;
    if (ad) { for (const s of [-1, 1]) svg += `<rect x="${cx - r * 1.7}" y="${cy + s * r * 1.4 - r * 0.75}" width="${r * 3.4}" height="${r * 1.5}" rx="${r * 0.25}" fill="var(--g-ctx)" opacity=".55"/>`; svg += `<ellipse cx="${cx}" cy="${cy}" rx="${r * 1.75}" ry="${r * 0.5}" fill="#606875" stroke="#ECEDEF"/>` + ring(cx, cy, r * 0.6, r * 0.33); }
    else { svg += `<path d="M${cx - r * 3} ${cy - r} C${cx - r} ${cy - r * 1.6} ${cx + r} ${cy - r * 1.4} ${cx + r * 1.6} ${cy + r * 0.2} C${cx + r * 1.8} ${cy + r} ${cx + r} ${cy + r * 1.5} ${cx} ${cy + r * 1.3} L${cx - r * 3} ${cy + r * 1.3} Z" fill="var(--g-ctx)" opacity=".6" stroke="#ECEDEF"/>` + ring(tx, ty, r * grow, r * grow);
      for (const [T, x, y] of [['Cr', cx - r * 3.35, cy + r * 0.2], ['Cd', cx + r * 2.5, cy + r * 0.95], ['D', cx + r * 0.9, cy - r * 1.2], ['V', cx - r, cy + r * 1.75]]) svg += `<text x="${x}" y="${y}" font-size="${Math.max(MIN_PX.tag, H * 0.04)}" font-weight="700" fill="#fff" text-anchor="middle">${T}</text>`; }
    const ax = ad ? cx : tx, ay = ad ? cy : ty, lx = W * 0.6, ly = cy - r * 0.9;
    if (on) { svg += `<line x1="${ax}" y1="${ay}" x2="${lx}" y2="${ly}" stroke="#14161A" stroke-width="${lw + 2}"/><line data-ld="${Math.hypot(ax - lx, ay - ly) / W * 100}" x1="${ax}" y1="${ay}" x2="${lx}" y2="${ly}" stroke="#fff" stroke-width="${lw}"/><circle cx="${ax}" cy="${ay}" r="${lw * 1.6}" fill="#fff" stroke="#14161A"/>`; h += `<div class="lab" data-k="label" style="left:${lx}px;top:${ly}px;font-size:${fsLab}px;transform:translate(0,-50%)"><i class="sw L-ctx"></i>${m.labels[0]}</div>`; }
    window._bx = null; h += `<div class="abs" data-k="stack" style="left:${X(5)}px;bottom:${H - Y(84)}px;display:flex;gap:8px;align-items:flex-end"><span class="chip" data-k="stamp" style="font-size:${fsSt}px">${ad ? 'Adult · schematic · scale not given' : on ? 'Fetus / newborn · schematic · scale not given' : 'End of week 4 · schematic · scale not given'}</span><span class="chip" data-k="tag" style="font-size:${fsTag}px">${m.tag}</span></div><div class="stub" data-k="stub" style="font-size:${fsTag * 0.85}px;right:${X(5)}px;top:${Y(5)}px">STUB ${ad ? 'N8' : 'N9'}</div>`;
  }
  if (seg.endcard) h += `<div class="abs" data-k="title" style="left:0;right:0;text-align:center;top:${Y(b.title[0])}px;line-height:${Y(6)}px"><span class="chip" style="font:400 ${W * 0.062}px/1.3 var(--font-display)">Gastrulation · Part 1</span></div>`;
  if (!sh) h += `<div class="abs" data-k="part" style="left:${X(5)}px;top:${Y(m.clinical ? 14 : 5)}px"><span class="chip" style="font-size:${Math.max(MIN_PX.label, H * 0.045)}px">Gastrulation · Part 1</span></div>`;
  if (m.clinical) h += `<div class="abs" data-k="clin" style="left:${X(5)}px;top:${Y(5)}px"><span class="chip" style="font-size:${Math.max(12, H * 0.067)}px">Clinical link</span></div>`;
  const ch = sh && lines[0] && lines[0].title; if (ch) h += `<div class="abs" data-k="title" style="left:0;right:0;text-align:center;top:${Y(b.title[0])}px;line-height:${Y(6)}px"><span class="chip" style="font:400 ${W * 0.066}px/1.3 var(--font-display);letter-spacing:.1em;opacity:${clamp((t - shot.s) / 0.3)}">${esc(ch)}</span></div>`;
  if (seg.check) { const l = o.line, Ls = C.lines, q = l && l.kind === 'check', ps = q && t > l.e; const ql = Ls.find(k => /^(L32|G16)$/.test(k.id)), done = l && /^(L32a|G16a)$/.test(l.id), open = ql && t >= ql.words[ql.words.length - (st.cut === 'lesson' ? 4 : 5)][1];
    if (open) { const chips = st.cut === 'lesson' ? ['Becomes endoderm', 'Is replaced'] : ['Epiblast', 'Old bottom layer', 'One each'], right = st.cut === 'lesson' ? 1 : 0; h += `<div class="terms" data-k="chips" style="left:50%;transform:translateX(-50%);top:${Y(14)}px;font-size:${fsLab}px;flex-wrap:nowrap;white-space:nowrap">${chips.map((c, i) => `<i style="${done && i === right ? 'outline:3px solid var(--accent-on-dark)' : done ? 'opacity:.6' : ''}">${done && i === right ? '✓ ' : ''}${c}</i>`).join('')}</div>`; }
    if (ps) { const k = clamp((t - l.e) / Math.max(0.1, l.hold)); h += `<div class="abs" data-k="pause" style="left:35%;width:30%;top:${Y(81.5)}px;height:${Math.max(4, H * 0.012)}px;background:#ffffff55"><div style="width:${100 - k * 100}%;height:100%;background:#fff"></div></div><div class="abs" data-k="think" style="left:0;right:0;text-align:center;top:${Y(75)}px"><span class="chip" style="font-size:${fsTag}px">Think…</span></div>`; } }
  if (st.caps && cap) { const bt = sh ? b.caption[1] : b.caption[1] - 1.5; h += `<div class="cap" data-k="cap" style="bottom:${H - Y(bt)}px;font-size:${fsCap}px;max-width:${X(b.capMaxW)}px">${cap.lines.map(x => `<span>${esc(x)}</span>`).join('<br>')}</div>`; }
  if (Q.has('safe') && sh) h += `<div class="abs" style="inset:auto 0 0 0;height:25%;background:#f003"></div><div class="abs" style="inset:0 0 0 auto;width:14%;background:#f003"></div><div class="abs" style="inset:0 0 auto 0;height:14%;background:#f003"></div>`;
  if (Q.has('boxes')) for (const [k, v] of Object.entries(b)) if (Array.isArray(v)) h += `<div class="abs" style="left:0;right:0;top:${Y(v[0])}px;height:${Y(v[1] - v[0])}px;outline:1px solid #ff2bd0;color:#ff2bd0;font:10px monospace">${k}</div>`;
  const A0 = termsOf(shot.id).filter(x => !seg.check || h.includes(x)), lb = `${ALT[shot.id] || ''}.${A0.length ? ' Labels: ' + A0.join(', ') + '.' : ''}${m.tag ? ' ' + m.tag + '.' : ''}`; if (stage.getAttribute('aria-label') !== lb) stage.setAttribute('aria-label', lb);
  ov.innerHTML = `<svg viewBox="0 0 ${W} ${H}">${svg}</svg>` + h;
}
/* ---------- player ---------- */
let lastLine = null;
const mmss = s => Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
function transcript() {
  const C = TL[st.cut], seen = new Set(), scr = l => { if (seen.has(l.shot)) return ''; seen.add(l.shot); const A = [...termsOf(l.shot), ...extraTags(l.shot), ...(l.title && st.cut === 'short' ? [l.title] : [])]; return A.length ? `<small>On screen: ${A.map(esc).join(' · ')}</small>` : ''; };
  $('#tr').innerHTML = C.lines.map(l => `<button class="ln" data-l="${l.id}"><small>${mmss(l.s)} · ${l.shot} · ${l.id}</small>${esc(l.text)}${scr(l)}</button>` + (Q.get('test') === '1' ? `<button class="edit" data-e="${l.shot}|${l.id}" aria-label="Edit ${l.shot} ${l.id}" title="content/E/episodes/S1E01/script.json ${l.id} · shots.json ${l.shot}">✎ ${l.shot}</button>` : '')).join(''); lastLine = null;
}
function ui(C, t, line) { const s = $('#sk'); s.max = C.dur; if (!s._down) s.value = t; s.setAttribute('aria-valuetext', mmss(t)); if (line && line.id !== lastLine) { lastLine = line.id; $('#tr').querySelectorAll('.ln').forEach(b => { const on = b.dataset.l === line.id; b.classList.toggle('on', on); if (on) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); if (on && st.play && Date.now() - ($('#tr')._u || 0) > 5000) $('#tr').scrollTop = b.offsetTop - $('#tr').offsetTop - 40; }); } }
function load() { const C = TL[st.cut]; st.t = Math.min(st.t, C.dur - 0.01); if (!REC) { $('#cut').value = st.cut; au.src = new URL(st.cut + '.wav', MEDIA); au.currentTime = st.t; transcript(); } key = ''; layout(); }
function setPlay(p) { st.play = p; $('#pp').textContent = p ? '⏸' : '▶'; $('#pp').setAttribute('aria-label', p ? 'Pause' : 'Play'); if (p) { if (st.t >= TL[st.cut].dur - 0.1) st.t = 0; au.currentTime = st.t; au.play().catch(() => setPlay(false)); loop(); } else au.pause(); }
function loop() { if (!st.play) return; st.t = au.currentTime; if (au.ended) { setPlay(false); return; } draw(); requestAnimationFrame(loop); }
const seek = t => { st.t = Math.max(0, Math.min(TL[st.cut].dur - 0.01, t)); if (au) au.currentTime = st.t; draw(); };
if (!REC) {
  const sk = $('#sk'); sk.onpointerdown = () => sk._down = true; addEventListener('pointerup', () => sk._down = false); sk.onkeydown = e => { const d = { ArrowRight: 5, ArrowUp: 5, ArrowLeft: -5, ArrowDown: -5 }[e.key]; if (d) { e.preventDefault(); seek(st.t + d); } if (e.key === 'Home') { e.preventDefault(); seek(0); } if (e.key === 'End') { e.preventDefault(); seek(1e9); } };
  for (const k of ['wheel', 'touchmove']) $('#tr').addEventListener(k, () => $('#tr')._u = Date.now(), { passive: true });
  $('#pp').onclick = () => setPlay(!st.play); $('#sk').oninput = e => seek(+e.target.value); $('#cut').onchange = e => { setPlay(false); st.cut = e.target.value; st.t = 0; load(); };
  $('#cc').onclick = e => { st.caps = !st.caps; e.target.setAttribute('aria-pressed', st.caps); draw(); };
  const fsState = () => { $('#fs').setAttribute('aria-label', st.full ? 'Exit full screen' : 'Full screen'); $('#fs').setAttribute('aria-pressed', st.full); };
  $('#fs').onclick = () => { st.full = !st.full; fsState(); if (st.full) { document.documentElement.requestFullscreen?.().then(() => screen.orientation?.lock?.(isShort() ? 'portrait' : 'landscape')).catch(() => {}); } else if (document.fullscreenElement) document.exitFullscreen(); layout(); };
  document.addEventListener('fullscreenchange', () => { if (!document.fullscreenElement && st.full) { st.full = false; fsState(); } layout(); });
  const step = d => { const S = TL[st.cut].shots, i = S.findLastIndex(s => s.s <= st.t + 0.01); seek(S[Math.max(0, Math.min(S.length - 1, i + d))].s); };
  $('#prev').onclick = () => step(-1); $('#next').onclick = () => step(1);
  $('#tr').onclick = e => { const b = e.target.closest('.ln'), ed = e.target.closest('.edit'); if (b) seek(TL[st.cut].lines.find(l => l.id === b.dataset.l).s); if (ed) { const [s, l] = ed.dataset.e.split('|'), p = `Bio · Fix · S1E01 ${s}: in content/E/episodes/S1E01/ (script.json ${l}, shots.json ${s}) and tools/s1e01-animatic/shots.mjs, change: `; navigator.clipboard?.writeText(p); } };
  addEventListener('keydown', e => { if (e.key === 'Escape' && st.full) return $('#fs').click(); if (/INPUT|SELECT|BUTTON/.test(e.target.tagName) && e.key !== 'k') return; if (e.key === ' ' || e.key === 'k') { e.preventDefault(); setPlay(!st.play); } if (e.key === 'ArrowRight') seek(st.t + 5); if (e.key === 'ArrowLeft') seek(st.t - 5); });
}
if (Q.get('debug')) document.body.append(el('<div id="dbg"></div>'));
addEventListener('resize', layout); load();
/* recorder + checks */
window.seek = t => { st.t = t; draw(); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); };
window.info = () => ({ dur: TL[st.cut].dur, shots: TL[st.cut].shots, lines: TL[st.cut].lines, W, H, gpu: V.gpu(), bands: B() });
window.craft = () => ({ bx: window._bx, ld: [...ov.querySelectorAll('[data-ld]')].map(e => +e.dataset.ld) });
window.boxes = () => { const s = stage.getBoundingClientRect(); return [...ov.querySelectorAll('[data-k]')].map(e => { const r = e.getBoundingClientRect(); return { k: e.dataset.k, l: (r.left - s.left) / s.width * 100, r: (r.right - s.left) / s.width * 100, t: (r.top - s.top) / s.height * 100, b: (r.bottom - s.top) / s.height * 100, txt: e.textContent.slice(0, 40), fs: parseFloat(getComputedStyle(e).fontSize), vis: r.left >= 0 && r.right <= innerWidth + 0.5 && r.bottom <= innerHeight + 0.5 }; }); };
window.cellCheck = () => {   // scene-check's tracer rule on the stub: inside the mesoderm sheet whenever both keys around it say so
  const out = []; for (let d = 15; d <= 17.001; d += 0.01) { const a = E.traceAt(s4, 't-meso', d), ks = E.keyState(s4, d), p = ks.params, L = p.length_units, W2 = p.width_ratio * L / 2, m = 0.75 * Math.max(0, (ks.u - 0.3) / 0.7);
    const inside = (x, y) => { const c = x / (L / 2); return Math.abs(c) <= 1 && Math.abs(y) <= W2 * Math.sqrt(1 - c * c) * (1 + 0.5 * p.pear * c); }, anc = -0.47 * L, k = m * 0.97; let bad = !inside(a.x, a.y); if (a.in === 'mesoderm' || a.z < -0.03) bad ||= !(k > 0 && inside(anc + (a.x - anc) / k, a.y / k)); out.push({ day: +d.toFixed(2), in: a.in, bad }); }
  return out; };
window.ready = true;
