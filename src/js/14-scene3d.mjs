/* Biology Studio — 3D scene engine (three.js r170, vendored in lib/three-r170/). Owner docs: docs/scene-spec.md (format, C2),
   build/design-plan.md §2 (3D viewer row) + §7. Loaded on demand by src/js/13-viewer.js (first load stays light, H8).
   Geometry mirrors tools/m1-bakeoff/common/scene_math.py (same names + formulas): outline → half-plane clip → prisms.
   Colours, edges and patterns come ONLY from the CSS tokens read off the stage element (RULES B3) — never from scene files.
   EDIT: lights + materials in makeRenderer(); pattern drawings in PATTERNS; budgets in CONFIG.viewer (02-config.js). */
import * as THREE from '../../lib/three-r170/three.module.min.js';

const lerp = (a, b, t) => a + (b - a) * t, clamp01 = t => Math.max(0, Math.min(1, t)), smooth = t => { t = clamp01(t); return t * t * (3 - 2 * t); };
export const REVISION = THREE.REVISION;

/* ---------- 1. tokens → colours + pattern textures (B3: colour + pattern + label, always) ---------- */
// EDIT: one pattern per token (design plan §1). Drawn in ink over the fill, 64 px tile, 4 periods.
const PATTERNS = {
  epi: (g, ink) => { g.strokeStyle = ink; g.lineWidth = 1.6; for (let y = 8; y < 64; y += 16) for (let x = 8; x < 64; x += 16) { g.beginPath(); g.arc(x, y, 3.4, 0, 7); g.stroke(); } },
  hypo: (g, ink) => { g.fillStyle = ink; for (let x = 0; x < 64; x += 8) g.fillRect(x, 0, 1.6, 64); },
  ecto: (g, ink) => { g.fillStyle = ink; for (let y = 4; y < 64; y += 10.67) for (let x = 4; x < 64; x += 10.67) { g.beginPath(); g.arc(x, y, 2, 0, 7); g.fill(); } },
  meso: (g, ink) => { g.strokeStyle = ink; g.lineWidth = 1.6; for (let k = -64; k < 128; k += 10.67) { g.beginPath(); g.moveTo(k, 64); g.lineTo(k + 64, 0); g.stroke(); } },
  endo: (g, ink) => { g.fillStyle = ink; for (let y = 0; y < 64; y += 8) g.fillRect(0, y, 64, 1.6); },
  crest: (g, ink) => { g.strokeStyle = ink; g.lineWidth = 1.4; for (let k = -64; k < 128; k += 12.8) { g.beginPath(); g.moveTo(k, 64); g.lineTo(k + 64, 0); g.moveTo(k, 0); g.lineTo(k + 64, 64); g.stroke(); } },
  ctx: (g, ink) => { g.fillStyle = ink; for (let i = 0; i < 90; i++) { const x = (i * 37) % 64, y = (i * 23 + (i >> 3) * 7) % 64; g.fillRect(x, y, 1.6, 1.6); } },
  accent: () => {}, guide: () => {},
};
export function readTokens(el) {
  const cs = getComputedStyle(el), v = k => cs.getPropertyValue(k).trim();
  const T = {};
  for (const k of ['epi', 'hypo', 'ecto', 'meso', 'endo', 'crest', 'ctx']) T[k] = { fill: v('--g-' + k), edge: v('--g-' + k + '-edge') || v('--g-' + k), text: v('--g-' + k + '-text') };
  T.accent = { fill: v('--accent'), edge: v('--accent-on-dark') || v('--accent'), text: v('--accent-ink') || '#fff' };
  T.guide = { fill: v('--muted'), edge: v('--ink'), text: v('--ink') };
  T.bg = v('--stage-bg') || v('--bg'); T.patInk = v('--pat-ink'); T.patInkLight = v('--pat-ink-light');
  return T;
}
function patternTexture(T, token) {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d'); g.fillStyle = T[token].fill; g.fillRect(0, 0, 64, 64);
  (PATTERNS[token] || PATTERNS.guide)(g, token === 'ecto' ? T.patInkLight : T.patInk);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return t;
}

/* ---------- 2. geometry (mirror of scene_math.py) ---------- */
function outline(L, wr, pear, n) {
  const pts = [];
  for (let i = 0; i < n; i++) { const a = 2 * Math.PI * i / n, x = (L / 2) * Math.cos(a); pts.push([x, (wr * L / 2) * Math.sin(a) * (1 + 0.5 * pear * (x / (L / 2)))]); }
  return pts;
}
const scaleFrom = (pts, ax, k) => pts.map(([x, y]) => [ax + k * (x - ax), k * y]);
/* Sutherland–Hodgman clip of a closed polygon to the half-plane p[axis] >= c (axis 0 = x, 1 = y) */
function clipGe(pts, axis, c) {
  const out = [];
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i], q = pts[(i + 1) % pts.length], pin = p[axis] >= c, qin = q[axis] >= c;
    if (pin) out.push(p);
    if (pin !== qin) { const t = (c - p[axis]) / (q[axis] - p[axis]); out.push([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]); }
  }
  return out;
}
function ccw(pts) { let a = 0; for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; a += p[0] * q[1] - q[0] * p[1]; } return a > 0 ? pts : pts.slice().reverse(); }
const PW = 0.6;   // EDIT: world units per pattern tile (4 periods → one period ≈ 0.15 units = 15 µm)
/* prism from a closed outline; side faces lying on the cut line go to group 1 (opaque "cap" — G-Art: the slice must read) */
function prismGeometry(poly, z0, z1, cut) {
  const n = poly.length, pos = [], uv = [], cap = [], capUv = [];
  let cx = 0, cy = 0; poly.forEach(([x, y]) => { cx += x; cy += y; }); cx /= n; cy /= n;
  const P = (A, B, x, y, z, u, v) => { A.push(x, y, z); B.push(u / PW, v / PW); };
  const onCut = q => cut && Math.abs(q[cut.ax] - cut.c) < 0.008;
  for (let i = 0; i < n; i++) {
    const p = poly[i], q = poly[(i + 1) % n];
    P(pos, uv, cx, cy, z1, cx, cy); P(pos, uv, p[0], p[1], z1, p[0], p[1]); P(pos, uv, q[0], q[1], z1, q[0], q[1]);   // top
    P(pos, uv, cx, cy, z0, cx, cy); P(pos, uv, q[0], q[1], z0, q[0], q[1]); P(pos, uv, p[0], p[1], z0, p[0], p[1]);   // bottom
    const up = p[0] + p[1], uq = q[0] + q[1], A = onCut(p) && onCut(q) ? cap : pos, B = A === cap ? capUv : uv;   // sides: pattern along the rim
    P(A, B, p[0], p[1], z0, up, z0); P(A, B, q[0], q[1], z0, uq, z0); P(A, B, q[0], q[1], z1, uq, z1);
    P(A, B, p[0], p[1], z0, up, z0); P(A, B, q[0], q[1], z1, uq, z1); P(A, B, p[0], p[1], z1, up, z1);
  }
  const g = new THREE.BufferGeometry(), nMain = pos.length / 3;
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos.concat(cap), 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv.concat(capUv), 2));
  g.addGroup(0, nMain, 0); if (cap.length) g.addGroup(nMain, cap.length / 3, 1);
  g.computeVertexNormals();
  return g;
}

/* scene params at a day: eased between the two neighbouring keys (spec §2, §4) */
export function keyState(scene, day) {
  const K = scene.days, d = Math.max(K[0].day, Math.min(K[K.length - 1].day, day));
  let i = 0; while (i < K.length - 2 && d > K[i + 1].day) i++;
  const a = K[i], b = K[Math.min(i + 1, K.length - 1)], span = b.day - a.day, u = span > 0 ? smooth((d - a.day) / span) : 0;
  const pa = {}, pb = {};
  for (let j = 0; j <= i; j++) Object.assign(pa, K[j].params || {});
  Object.assign(pb, pa, b.params || {});
  const p = {}; for (const k of Object.keys(pb)) p[k] = typeof pb[k] === 'number' ? lerp(pa[k] ?? pb[k], pb[k], u) : pb[k];
  const lin = span > 0 ? (d - a.day) / span : 0;
  return { day: d, u, lin, a, b, params: p, size_mm: lerp(a.size_mm, b.size_mm, u) };
}
/* stamp text pieces (spec §8). On a key day: that key's stage + cited size. Between keys: the day span, the stage pair and the
   eased size — never a key's mark (G-Sci: a cited value is shown only where it was cited). */
export function stampOf(scene, day) {
  const s = keyState(scene, day), d = s.day, at = scene.days.find(k => Math.abs(k.day - d) < 0.05);
  const fmt = mm => mm >= 1 ? mm.toFixed(2).replace(/0$/, '') : mm.toFixed(mm < 0.3 ? 2 : 1);
  if (at) return { day: String(at.day), stage: at.stage, size: '≈' + fmt(at.size_mm) + ' mm', mark: at.mark, onKey: true };
  const whole = Math.abs(d - Math.round(d)) < 0.05, dayTxt = whole ? String(Math.round(d)) : Math.floor(d) + '–' + Math.ceil(d);
  const pad = c => c.replace(/^CS0?/, '').padStart(2, '0');
  const stage = s.a.stage === s.b.stage ? s.a.stage : s.a.stage + '–' + pad(s.b.stage);
  return { day: dayTxt, stage, size: '≈' + fmt(s.size_mm) + ' mm', mark: '', onKey: false };
}

/* disc pieces at a state — the M1 build() with a general cut and the scene's layer map */
function discPieces(part, p, cut) {
  const n = part.segments || 96, te = part.epiblast_thick, g = part.gap, th = part.hypoblast_thick;
  const L = p.length_units, wr = p.width_ratio, pear = p.pear || 0, disc = outline(L, wr, pear, n);
  const ax = cut && cut.on ? (cut.axis === 'x' ? 0 : 1) : -1, c0 = ax === 0 ? cut.at * (L / 2) : ax === 1 ? cut.at * (wr * L / 2) : 0;
  const clip = (poly, eps = 0) => ax < 0 ? poly : clipGe(poly, ax, c0 - eps);
  const out = [], M = part.layers || {};
  const add = (name, poly, z0, z1, layerKey = name) => { if (M[layerKey] && poly.length >= 3) out.push({ name, layer: M[layerKey], poly: ccw(poly), z0, z1 }); };
  add('hypoblast', clip(disc), -g - th, -g);
  add('epiblast', clip(disc), 0, te);
  const anc = -L / 2 + 0.03 * L;
  const meso = p.meso || 0, endo = p.endo || 0;
  if (meso > 0.02) add('mesoderm', clip(scaleFrom(disc, anc, meso * 0.97), 0.002), -g + 0.035, -0.02);
  if (endo > 0.02) add('endoderm', clip(scaleFrom(disc, anc, endo * 0.97), 0.004), -g - th - 0.005, -g + 0.005);
  if ((p.tip_frac || 0) > 0.02) {
    const st = part.streak, x0 = -L / 2 + st.start_frac * L, x1 = -L / 2 + p.tip_frac * L, w = st.width / 2;
    add('streak', clip([[x0, -w], [x1, -w], [x1, w], [x0, w]], 0.001), te - st.height, te - 0.008);   // a groove sunk into the epiblast…
    const lw = w * 0.55;                                                                                 // …with raised edges [E05.01]
    add('lip-l', clip([[x0, w], [x1, w], [x1, w + lw], [x0, w + lw]], 0.001), te, te + 0.03, 'streak');
    add('lip-r', clip([[x0, -w - lw], [x1, -w - lw], [x1, -w], [x0, -w]], 0.001), te, te + 0.03, 'streak');
    const nd = part.node, circle = [];
    for (let i = 0; i < 32; i++) circle.push([x1 + nd.radius * Math.cos(2 * Math.PI * i / 32), nd.radius * Math.sin(2 * Math.PI * i / 32)]);
    add('node', clip(circle, 0.001), te, te + nd.height);
  }
  return { pieces: out, L, wr, te, g, th, cutAxis: ax, cutAt: c0 };
}
/* the delays act inside each key-to-key step: a layer starts spreading after `delay` of the step (scene_math.state) */
function delayed(scene, day, part) {
  const s = keyState(scene, day), p = { ...s.params };
  const ka = s.a.params || {}, kb = s.b.params || {};
  const pa = {}; for (const k of scene.days) { if (k.day > s.a.day) break; Object.assign(pa, k.params || {}); }
  for (const [k, dly] of [['meso', part.meso_delay || 0], ['endo', part.endo_delay || 0]]) {
    if (kb[k] === undefined && ka[k] === undefined) continue;
    const from = pa[k] ?? 0, to = kb[k] ?? from, t = clamp01((s.u - dly) / (1 - dly));
    p[k] = lerp(from, to, t);
  }
  return p;
}

/* ---------- 3. the viewer ---------- */
export function createViewer(canvas, stageOf, opt = {}) {   // stageOf(): the CURRENT stage element (re-renders replace it)
  const dprCap = opt.dprCap || 2;
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, preserveDrawingBuffer: !!opt.still, powerPreference: 'default' }); }
  catch (e) { return { ok: false, err: e.message }; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, dprCap));
  renderer.toneMapping = THREE.NoToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene3 = new THREE.Scene(), root = new THREE.Group(); scene3.add(root);
  canvas.addEventListener('webglcontextlost', e => e.preventDefault());   // Android may drop the context in the background…
  canvas.addEventListener('webglcontextrestored', () => { V.dirty = true; if (V.scene) api.setTokens(); });   // …redraw when it returns
  // EDIT: lights (soft key from front-left above, cool fill, hemisphere ambient) — clarity first, playbook §6.1
  scene3.add(new THREE.HemisphereLight(0xffffff, 0x3a404c, 1.6));
  const key = new THREE.DirectionalLight(0xffffff, 1.8); key.position.set(-3, -4, 8); scene3.add(key);
  const fill = new THREE.DirectionalLight(0xdfe8ff, 0.6); fill.position.set(4, 5, 2); scene3.add(fill);
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.01, 400); cam.up.set(0, 0, 1);
  const V = { scene: null, day: 0, layersOn: {}, cut: { on: false, axis: 'y', at: -0.3 }, az: -90, el: 55, zoom: 1, fitU: 6,
    T: null, mats: {}, edgeMats: {}, objs: [], anchors: {}, dirty: true, w: 1, h: 1, cont: false, raf: 0, onFrame: null,
    ft: [], stress: null, orbit: 0, dbg: null, hoverables: [] };

  function tokenOf(layerId) { const L = V.scene.layers.find(l => l.id === layerId); return L ? L.token : 'guide'; }
  function opacityOf(layerId) { const L = V.scene.layers.find(l => l.id === layerId); return L && L.opacity != null ? L.opacity : 1; }
  function mat(layerId) {
    if (V.mats[layerId]) return V.mats[layerId];
    const tok = tokenOf(layerId), op = opacityOf(layerId);
    const m = new THREE.MeshStandardMaterial({ color: 0xffffff, map: patternTexture(V.T, tok), roughness: 0.62, metalness: 0,
      transparent: op < 1, opacity: op, depthWrite: op >= 1, side: THREE.DoubleSide });
    return (V.mats[layerId] = m);
  }
  function capMat(layerId) {   // the cut face: opaque, same pattern, a touch lighter
    const k = 'cap:' + layerId; if (V.mats[k]) return V.mats[k];
    return (V.mats[k] = new THREE.MeshStandardMaterial({ color: 0xffffff, map: mat(layerId).map, roughness: 0.7, metalness: 0, emissive: 0xffffff, emissiveIntensity: 0.07, side: THREE.DoubleSide }));
  }
  /* edges in the layer's edge token; a layer with ring:true is outlined in the accent ("look here" ring, never a fill — B3, D-036) */
  function edgeMat(layerId) { const L = V.scene.layers.find(l => l.id === layerId) || {}, tok = tokenOf(layerId), k = L.ring ? 'ring' : tok;
    return V.edgeMats[k] ||= new THREE.LineBasicMaterial({ color: new THREE.Color(L.ring ? V.T.accent.edge : V.T[tok].edge) }); }
  function guideMat(alpha) { return new THREE.MeshBasicMaterial({ color: new THREE.Color(V.T.guide.fill), transparent: alpha < 1, opacity: alpha, depthWrite: alpha >= 1, side: THREE.DoubleSide }); }
  function disposeMats() { for (const [k, m] of Object.entries(V.mats)) { if (!k.startsWith('cap:') && m.map) m.map.dispose(); m.dispose(); } V.mats = {};
    for (const m of Object.values(V.edgeMats)) m.dispose(); V.edgeMats = {}; }
  const ORDER = { hypoblast: 0, endoderm: 1, mesoderm: 2, streak: 3, epiblast: 4, 'lip-l': 5, 'lip-r': 5, node: 5 };

  function clear() {
    for (const o of V.objs) { root.remove(o); o.traverse(c => { if (c.geometry && !c.userData.keepGeo) c.geometry.dispose(); if (c.material && c.userData.ownMat) [].concat(c.material).forEach(m => m.dispose()); }); }
    V.objs = []; V.anchors = {}; V.hoverables = [];
  }
  function addObj(o, layer) { o.userData.layer = layer; root.add(o); V.objs.push(o); return o; }

  /* rebuild every part for the current day + cut (cheap: a few thousand triangles) */
  function build() {
    clear(); if (!V.scene) return;
    const S = V.scene, u = S.units.mm_per_unit;
    for (const part of S.parts) {
      if (part.kind === 'disc') {
        const p = delayed(S, V.day, part), D = discPieces(part, p, V.cut);
        for (const pc of D.pieces) {
          const geo = prismGeometry(pc.poly, pc.z0, pc.z1, D.cutAxis >= 0 ? { ax: D.cutAxis, c: D.cutAt } : null), m = new THREE.Mesh(geo, [mat(pc.layer), capMat(pc.layer)]);
          m.renderOrder = ORDER[pc.name] ?? 3; m.visible = V.layersOn[pc.layer] !== false; addObj(m, pc.layer); V.hoverables.push(m);
          const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 35), edgeMat(pc.layer)); e.visible = m.visible; e.renderOrder = m.renderOrder; addObj(e, pc.layer);
          if (!pc.name.startsWith('lip')) V.anchors[pc.name] = { layer: pc.layer, p: anchorFor(pc, D) };
        }
        V.discL = D.L; V.discW = D.wr * D.L;
      } else if (part.kind === 'axes') {
        const len = part.length_mm / u, c = new THREE.Color(V.T.guide.edge), z = 0.11;
        const dirs = { cranial: [1, 0, 0], caudal: [-1, 0, 0], left: [0, 1, 0], right: [0, -1, 0], dorsal: [0, 0, 1], ventral: [0, 0, -1] };
        const g = new THREE.Group();
        for (const [k, d] of Object.entries(dirs)) {
          const v = new THREE.Vector3(...d), l = k === 'dorsal' || k === 'ventral' ? len * 0.6 : len;
          const a = new THREE.ArrowHelper(v, new THREE.Vector3(0, 0, z), l, c, l * 0.1, l * 0.05); a.traverse(o => { o.userData.keepGeo = true; o.userData.ownMat = true; }); g.add(a);
          V.anchors['axis-' + k] = { layer: part.layer, p: [d[0] * l * 1.2, d[1] * l * 1.2, z + d[2] * l * 1.2], axis: k };
        }
        g.visible = V.layersOn[part.layer] !== false; addObj(g, part.layer);
      } else if (part.kind === 'planes') {
        const s = part.size_mm / u;
        for (const pl of part.planes) {
          const geo = new THREE.PlaneGeometry(s, pl.normal === 'z' ? s * 0.8 : s * 0.6), m = new THREE.Mesh(geo, guideMat(0.16)); m.userData.ownMat = true;
          if (pl.normal === 'x') m.rotation.set(Math.PI / 2, Math.PI / 2, 0);
          else if (pl.normal === 'y') m.rotation.set(Math.PI / 2, 0, 0);
          const dash = { x: [0.12, 0.08], y: null, z: [0.03, 0.05] }[pl.normal];   // each plane its own edge: dashed · solid · dotted (G-Art)
          const lm = dash ? new THREE.LineDashedMaterial({ color: new THREE.Color(V.T.guide.edge), dashSize: dash[0], gapSize: dash[1] }) : new THREE.LineBasicMaterial({ color: new THREE.Color(V.T.guide.edge) });
          const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo), lm); if (dash) e.computeLineDistances(); e.userData.ownMat = true; m.add(e);
          m.renderOrder = 8; m.visible = V.layersOn[pl.layer] !== false; addObj(m, pl.layer);
          const h = s / 2, hv = (pl.normal === 'z' ? s * 0.8 : s * 0.6) / 2;
          V.anchors['plane-' + pl.id] = { layer: pl.layer, p: pl.normal === 'x' ? [0, h * 0.95, -hv * 0.9] : pl.normal === 'y' ? [-h * 0.95, 0, hv * 0.9] : [h * 0.95, -hv * 0.95, 0] };   // own outer corner, away from the crossing
        }
      } else if (part.kind === 'ruler') {
        const len = part.length_mm / u, tick = part.tick_mm / u, [x0, y0] = part.at, g = new THREE.Group();
        const bar = new THREE.Mesh(new THREE.BoxGeometry(len, 0.18, 0.02), guideMat(1)); bar.userData.ownMat = true; bar.position.set(x0 + len / 2, y0, 0); g.add(bar);
        const pts = [];
        for (let i = 0, nT = Math.round(len / tick); i <= nT; i++) { const x = x0 + i * tick, big = i % 5 === 0 ? 0.55 : 0.32; pts.push(x, y0 + 0.09, 0.012, x, y0 + 0.09 + big, 0.012); }
        const tg = new THREE.BufferGeometry(); tg.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
        const tl = new THREE.LineSegments(tg, new THREE.LineBasicMaterial({ color: new THREE.Color(V.T.guide.edge) })); tl.userData.ownMat = true; g.add(tl);
        g.visible = V.layersOn[part.layer] !== false; addObj(g, part.layer);
        V.anchors.ruler = { layer: part.layer, p: [x0 + len / 2, y0 - 0.3, 0] };
      }
    }
    if (V.stress) { const k = new THREE.Mesh(V.stress.geo, V.stress.mat); k.position.set(0, 0, -1.2); k.userData.keepGeo = true; addObj(k, '_stress'); }   // opaque, single pass: N test triangles = N drawn
    if (V.scene.debug || V.dbg) {   // I5: world axes + bounding boxes
      const ah = new THREE.AxesHelper(2); ah.userData.ownMat = true; addObj(ah, '_debug');
      for (const m of V.hoverables) { const b = new THREE.BoxHelper(m, 0xff2bd0); b.userData.ownMat = true; addObj(b, '_debug'); }
    }
    V.dirty = true;
  }
  /* label anchor for a piece: the cut face when the cut reaches it, else the rim facing the camera (spec §7) */
  function anchorFor(pc, D) {
    const zm = (pc.z0 + pc.z1) / 2, xs = pc.poly.map(q => q[0]), ys = pc.poly.map(q => q[1]);
    if (pc.name === 'streak') return [(Math.min(...xs) + Math.max(...xs)) / 2, 0, pc.z1];   // the groove's floor line, seen through the epiblast
    if (pc.name === 'node') return [Math.max(...xs) - 0.02, 0, pc.z1];
    if (D.cutAxis >= 0) {
      const on = pc.poly.filter(q => Math.abs(q[D.cutAxis] - D.cutAt) < 0.02);
      if (on.length >= 2) { const o = 1 - D.cutAxis, vs = on.map(q => q[o]), lo = Math.min(...vs), hi = Math.max(...vs);
        let m = pc.name === 'endoderm' ? lo + 0.7 * (hi - lo) : pc.name === 'epiblast' ? lo + 0.35 * (hi - lo) : (lo + hi) / 2;
        if (pc.name === 'hypoblast') {   // the hypoblast shows only where the endoderm has not replaced it (G-Art: the dot must sit on its own layer)
          const en = D.pieces.find(x => x.name === 'endoderm'), eo = en && en.poly.filter(q => Math.abs(q[D.cutAxis] - D.cutAt) < 0.02).map(q => q[o]);
          if (eo && eo.length >= 2) { const elo = Math.min(...eo), ehi = Math.max(...eo), left = elo - lo, right = hi - ehi; m = right >= left ? (ehi + hi) / 2 : (lo + elo) / 2; }
          else m = lo + 0.78 * (hi - lo);
        }
        return D.cutAxis === 1 ? [m, D.cutAt, zm] : [D.cutAt, m, zm]; }
    }
    if (pc.name === 'epiblast') return [0.28 * D.L, 0.16 * D.L * D.wr, pc.z1];
    const a = THREE.MathUtils.degToRad(V.az), dx = Math.cos(a), dy = Math.sin(a);
    let best = pc.poly[0], bv = -Infinity; for (const q of pc.poly) { const v = q[0] * dx + q[1] * dy + (pc.name === 'endoderm' ? q[0] * 0.35 : pc.name === 'mesoderm' ? -q[0] * 0.25 : 0); if (v > bv) { bv = v; best = q; } }
    return [best[0], best[1], zm];
  }

  function placeCamera() {
    const a = THREE.MathUtils.degToRad(V.az), e = THREE.MathUtils.degToRad(V.el), R = 60;
    cam.position.set(R * Math.cos(e) * Math.cos(a), R * Math.cos(e) * Math.sin(a), R * Math.sin(e)); cam.lookAt(0, 0, 0);
    const view = V.fitU / V.zoom, asp = V.w / V.h;
    let hh, hw; if (asp >= 1) { hh = view / 2; hw = hh * asp; } else { hw = view / 2; hh = hw / asp; }
    cam.left = -hw; cam.right = hw; cam.top = hh; cam.bottom = -hh; cam.updateProjectionMatrix();
  }
  const pxPerUnit = () => V.h / (cam.top - cam.bottom);
  function project(p) { const v = new THREE.Vector3(...p).project(cam); return { x: (v.x + 1) / 2 * V.w, y: (1 - v.y) / 2 * V.h, z: v.z }; }
  /* screen directions of the body axes, for the gizmo (unit 2D vectors + how much each points at the viewer) */
  function axisDirs() {
    const out = {}, m = cam.matrixWorldInverse;
    for (const [k, d] of Object.entries({ cranial: [1, 0, 0], left: [0, 1, 0], dorsal: [0, 0, 1] })) { const v = new THREE.Vector3(...d).transformDirection(m); out[k] = { x: v.x, y: -v.y, z: v.z }; }
    return out;
  }
  function frame(t) {
    V.raf = 0;
    if (V.cont) { if (V.orbit) { V.az += V.orbit * 16 / 1000 * 12; } V.dirty = true; }
    if (V.dirty) {
      placeCamera(); renderer.render(scene3, cam); V.dirty = false;
      if (V.onFrame) V.onFrame();
      const now = performance.now(); if (V.cont) { if (V.lastT) V.ft.push(now - V.lastT); V.lastT = now; }
    }
    if (V.cont) V.raf = requestAnimationFrame(frame);
  }
  function kick() { V.dirty = true; if (!V.raf) V.raf = requestAnimationFrame(frame); }

  const api = {
    ok: true, three: THREE.REVISION,
    gpu() { try { const gl = renderer.getContext(), d = gl.getExtension('WEBGL_debug_renderer_info'); return d ? gl.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'WebGL'; } catch (_) { return '?'; } },
    setTokens() { const el = stageOf(); if (!el || !el.isConnected) return; V.T = readTokens(el); disposeMats();
      renderer.setClearColor(new THREE.Color(V.T.bg)); if (V.scene) build(); kick(); },
    setScene(S, st = {}) {
      V.scene = S; V.fitU = S.camera.fit_mm / S.units.mm_per_unit; V.day = st.day ?? S.start_day ?? S.days[0].day;
      V.layersOn = { ...(st.layersOn || Object.fromEntries(S.layers.map(l => [l.id, l.on !== false]))) };
      V.cut = { ...(st.cut || S.cut) }; V.az = st.az ?? S.camera.azimuth_deg; V.el = st.el ?? S.camera.elevation_deg; V.zoom = st.zoom ?? 1;
      disposeMats();
      if (!V.T) api.setTokens(); else build(); kick();
    },
    state() { return { day: V.day, layersOn: { ...V.layersOn }, cut: { ...V.cut }, az: V.az, el: V.el, zoom: V.zoom }; },
    setDay(d) { const K = V.scene.days; V.day = Math.max(K[0].day, Math.min(K[K.length - 1].day, d)); build(); kick(); },
    setLayer(id, on) { V.layersOn[id] = on; for (const o of V.objs) if (o.userData.layer === id) o.visible = on; kick(); },
    setCut(c) { Object.assign(V.cut, c); build(); kick(); },
    view(az, el, zoom) { if (az != null) V.az = az; if (el != null) V.el = Math.max(-89, Math.min(89, el)); if (zoom != null) V.zoom = Math.max(0.35, Math.min(10, zoom)); build(); kick(); },
    orbitBy(dAz, dEl) { V.az += dAz; V.el = Math.max(-89, Math.min(89, V.el + dEl)); kick(); api.rebuildSoon(); },
    rebuildSoon() { clearTimeout(V.rb); V.rb = setTimeout(() => { build(); kick(); }, 120); },   // rim-facing anchors follow the camera
    zoomBy(f) { V.zoom = Math.max(0.35, Math.min(10, V.zoom * f)); kick(); },
    resize(w, h) { V.w = Math.max(1, w); V.h = Math.max(1, h); renderer.setSize(V.w, V.h, false); kick(); },
    anchors() { const out = {}; for (const [k, a] of Object.entries(V.anchors)) out[k] = { ...a, s: project(a.p) }; return out; },
    pxPerMm() { return pxPerUnit() / V.scene.units.mm_per_unit; },
    axisDirs, onFrame(f) { V.onFrame = f; }, render: kick,
    pick(x, y) { const r = new THREE.Raycaster(), v = new THREE.Vector2(x / V.w * 2 - 1, -(y / V.h) * 2 + 1); r.setFromCamera(v, cam);
      const hit = r.intersectObjects(V.hoverables.filter(m => m.visible), false)[0]; return hit ? hit.object.userData.layer : null; },
    info() { const i = renderer.info.render; return { triangles: i.triangles, calls: i.calls, dpr: renderer.getPixelRatio(), px: Math.round(V.w * renderer.getPixelRatio()) + '×' + Math.round(V.h * renderer.getPixelRatio()) }; },
    setDebug(on) { V.dbg = on; build(); kick(); },
    /* benchmark (?debug=viewer › Measure): render continuously with a slow orbit; frame times → fps */
    continuous(on, orbitDegPerS = 0) { V.cont = on; V.orbit = orbitDegPerS ? orbitDegPerS / 12 : 0; V.ft = []; V.lastT = 0; kick(); },
    frameTimes() { return V.ft.slice(); },
    setStress(tris) { if (V.stress) { V.stress.geo.dispose(); V.stress.mat.dispose(); V.stress = null; }
      if (tris > 0) { const radial = 16, tub = Math.max(8, Math.round(tris / (2 * radial))); V.stress = { geo: new THREE.TorusKnotGeometry(0.9, 0.22, tub, radial), mat: new THREE.MeshStandardMaterial({ color: 0x8a909c, roughness: 0.6 }), tris: tub * radial * 2 }; }
      build(); kick(); return V.stress ? V.stress.tris : 0; },
    dispose() { cancelAnimationFrame(V.raf); clear(); disposeMats(); renderer.dispose(); },
  };
  return api;
}
