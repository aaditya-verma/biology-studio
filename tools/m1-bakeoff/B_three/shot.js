// Method B: three.js scene for shot M1-ps01. Mirrors common/scene_math.py — keep them in step.
import * as THREE from 'three';

const lerp = (a, b, t) => a + (b - a) * t;
const clamp01 = t => Math.max(0, Math.min(1, t));
const smooth = t => { t = clamp01(t); return t * t * (3 - 2 * t); };

function progress(shot, frame) {
  const tl = shot.timeline, t = frame / shot.fps;
  const a = tl.hold_start_s, b = shot.duration_s - tl.hold_end_s;
  return smooth((t - a) / (b - a));
}

function state(shot, frame) {
  const u = progress(shot, frame), d = shot.disc;
  const L = lerp(...d.length_units, u);
  const md = shot.mesoderm.delay, ed = shot.endoderm.delay;
  const s = {
    u, L, wr: lerp(...d.width_ratio, u), pear: lerp(...d.pear, u),
    tip: lerp(...shot.streak.tip_frac, u),
    meso: lerp(...shot.mesoderm.spread, clamp01((u - md) / (1 - md))),
    endo: lerp(...shot.endoderm.spread, clamp01((u - ed) / (1 - ed))),
  };
  s.yc = shot.layers.cut_y_frac * (s.wr * L / 2);
  return s;
}

function outline(L, wr, pear, n) {
  const pts = [];
  for (let i = 0; i < n; i++) {
    const a = 2 * Math.PI * i / n, x = (L / 2) * Math.cos(a);
    pts.push([x, (wr * L / 2) * Math.sin(a) * (1 + 0.5 * pear * (x / (L / 2)))]);
  }
  return pts;
}
const scaleFrom = (pts, ax, k) => pts.map(([x, y]) => [ax + k * (x - ax), k * y]);
function clipYGe(pts, yc) {
  const out = [];
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i], q = pts[(i + 1) % pts.length], pin = p[1] >= yc, qin = q[1] >= yc;
    if (pin) out.push(p);
    if (pin !== qin) { const t = (yc - p[1]) / (q[1] - p[1]); out.push([p[0] + t * (q[0] - p[0]), yc]); }
  }
  return out;
}
function ccw(pts) {
  let a = 0;
  for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; a += p[0] * q[1] - q[0] * p[1]; }
  return a > 0 ? pts : pts.slice().reverse();
}

function build(shot, frame) {
  const s = state(shot, frame), lay = shot.layers, n = shot.disc.segments;
  const { L, yc } = s, te = lay.epiblast_thick, g = lay.gap, th = lay.hypoblast_thick;
  const col = shot.colors, op = shot.opacity, parts = [];
  const add = (name, poly, z0, z1, opacity = 1, colour) => {
    if (poly.length >= 3) parts.push({ name, poly: ccw(poly), z0, z1, color: colour || col[name], opacity });
  };
  const disc = outline(L, s.wr, s.pear, n);
  add('hypoblast', clipYGe(disc, yc), -g - th, -g);
  add('epiblast', clipYGe(disc, yc), 0, te, op.epiblast);
  const ax = -L / 2 + 0.03 * L;
  if (s.meso > 0.02) add('mesoderm', clipYGe(scaleFrom(disc, ax, s.meso * 0.97), yc), -g + 0.035, -0.02, op.mesoderm);
  if (s.endo > 0.02) add('endoderm', clipYGe(scaleFrom(disc, ax, s.endo * 0.97), yc - 0.004), -g - th - 0.005, -g + 0.005);
  const st = shot.streak, x0 = -L / 2 + st.start_frac * L, x1 = -L / 2 + s.tip * L, w = st.width / 2;
  add('streak', [[x0, -w], [x1, -w], [x1, w], [x0, w]], te, te + st.height);
  const nd = shot.node, circle = [];
  for (let i = 0; i < 32; i++) circle.push([x1 + nd.radius * Math.cos(2 * Math.PI * i / 32), nd.radius * Math.sin(2 * Math.PI * i / 32)]);
  add('node', circle, te, te + nd.height, 1, col.streak);
  return parts;
}

function prismGeometry(poly, z0, z1) {
  const n = poly.length, pos = [];
  let cx = 0, cy = 0; poly.forEach(([x, y]) => { cx += x; cy += y; }); cx /= n; cy /= n;
  const tri = (a, b, c) => pos.push(...a, ...b, ...c);
  for (let i = 0; i < n; i++) {
    const p = poly[i], q = poly[(i + 1) % n];
    tri([cx, cy, z1], [p[0], p[1], z1], [q[0], q[1], z1]);          // top
    tri([cx, cy, z0], [q[0], q[1], z0], [p[0], p[1], z0]);          // bottom
    tri([p[0], p[1], z0], [q[0], q[1], z0], [q[0], q[1], z1]);      // side
    tri([p[0], p[1], z0], [q[0], q[1], z1], [p[0], p[1], z1]);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.computeVertexNormals(); // non-indexed → flat normals, same as Blender flat shading
  return g;
}

export async function init(canvas) {
  const shot = await (await fetch('/shot.json')).json();
  const W = shot.width, H = shot.height;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.NoToneMapping;
  renderer.setClearColor(new THREE.Color(shot.colors.background));
  const scene = new THREE.Scene();
  const hw = shot.camera.ortho_width_units / 2, hh = hw * H / W;
  const cam = new THREE.OrthographicCamera(-hw, hw, hh, -hh, 0.1, 200);
  const e = THREE.MathUtils.degToRad(shot.camera.elevation_deg), D = shot.camera.distance;
  cam.position.set(0, -D * Math.cos(e), D * Math.sin(e));
  cam.up.set(0, 0, 1);
  cam.lookAt(0, 0, 0);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x303540, 0.9));
  const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-3, -4, 8); scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.7); fill.position.set(4, 5, 2); scene.add(fill);
  const mats = {}, meshes = {};
  const mat = p => mats[p.name] ||= new THREE.MeshStandardMaterial({
    color: new THREE.Color(p.color), roughness: 0.55, metalness: 0,
    transparent: p.opacity < 1, opacity: p.opacity, depthWrite: p.opacity >= 1, side: THREE.DoubleSide,
  });
  const order = { hypoblast: 0, endoderm: 1, mesoderm: 2, epiblast: 3, streak: 4, node: 5 };

  function renderFrame(frame) {
    const parts = build(shot, frame), seen = new Set();
    for (const p of parts) {
      const geo = prismGeometry(p.poly, p.z0, p.z1);
      if (meshes[p.name]) { meshes[p.name].geometry.dispose(); meshes[p.name].geometry = geo; }
      else { meshes[p.name] = new THREE.Mesh(geo, mat(p)); meshes[p.name].renderOrder = order[p.name]; scene.add(meshes[p.name]); }
      meshes[p.name].visible = true; seen.add(p.name);
    }
    for (const [n, m] of Object.entries(meshes)) if (!seen.has(n)) m.visible = false;
    renderer.render(scene, cam);
  }
  const gl = renderer.getContext(), dbg = gl.getExtension('WEBGL_debug_renderer_info');
  const gpu = dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : 'unknown';
  return { shot, renderFrame, gpu, threeVersion: THREE.REVISION };
}
