// S1E01 animatic — layout + stub checks (P1 ②). node check.mjs [--only 375x812] [--debug] [--dry-run] [--preview (every 4th caption)] [--scope p1f] → out/check.json, out/layout/*.jpg. Exit 1 on any error.
// --scope p1f (P1F, D-107): the primer shots + every idea pause only, 6 sizes (phone / tablet / desktop × portrait + landscape, C13); primer labels also meet MM2 (text ≤ 12 % of the short side from the dot, visual-style §12).
// Bands: captions inside the caption band (Short: one line 68–72 %, two lines ≥ 64 %, never below 72 %; Lesson 85–95 %) · nothing overlaps the caption or leaves the frame · N4 path never ahead of its sheet.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), HOME = path.resolve(process.env.BIO_HOME || (HERE.includes(path.sep + 'repo' + path.sep) ? path.join(HERE, '../../../..') : path.join(HERE, '../..'))), OUT = path.join(HOME, 'tools/s1e01-animatic/out');
const { chromium } = await import(pathToFileURL(path.join(HOME, 'tools/m1-bakeoff/B_three/node_modules/playwright/index.mjs')));
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; }, has = k => process.argv.includes(k);
const MT = { '.html': 'text/html', '.mjs': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wav': 'audio/wav', '.js': 'text/javascript' };
const srv = http.createServer((q, r) => { const p = path.join(HOME, decodeURIComponent(q.url.split('?')[0]).replace(/\/$/, '/index.html')); if (!p.startsWith(HOME) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MT[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); }).listen(0, '127.0.0.1');
const P1F = arg('--scope') === 'p1f', PRIMER = /^S02[b-f]$/;
const VPS = [[375, 812], [812, 375], [768, 1024], [1024, 768], [1440, 900], ...(P1F ? [[900, 1440]] : [])].filter(v => !arg('--only') || v.join('x') === arg('--only'));
if (has('--dry-run')) { console.log(VPS); process.exit(0); }
fs.mkdirSync(path.join(OUT, 'layout'), { recursive: true });
const br = await chromium.launch({ args: ['--enable-gpu', '--ignore-gpu-blocklist', '--use-angle=d3d11'] }), errs = [], rep = {};
const ov = (a, c) => Math.min(a.r, c.r) - Math.max(a.l, c.l) > 0.3 && Math.min(a.b, c.b) - Math.max(a.t, c.t) > 0.3;
const pauses = {}, mm2 = [], mm2Carry = [];
for (const [w, h] of VPS) for (const cut of P1F ? ['lesson', 'general'] : ['lesson', 'general', 'short']) {
  const pg = await br.newPage({ viewport: { width: w, height: h }, hasTouch: w < 1200 }); pg.on('pageerror', e => errs.push(`${w}x${h} ${cut} page: ${e.message}`));
  await pg.goto(`http://127.0.0.1:${srv.address().port}/tools/s1e01-animatic/?cut=${cut}`); await pg.waitForFunction('window.ready===true', null, { timeout: 60000 });
  const info = await pg.evaluate('window.info()'), caps = info.lines.flatMap(l => l.caps.map(c => ({ t: (c.s + c.e) / 2, n: c.lines.length, shot: l.shot }))).filter(c => !P1F || PRIMER.test(c.shot)), b = info.bands.caption, seen = new Set();
  if (P1F) for (const s of info.shots.filter(s => PRIMER.test(s.id))) { const l = info.lines.filter(l => l.shot === s.id).at(-1); if (l && s.e - l.e > 0.25) caps.push({ t: +(s.e - 0.15).toFixed(2), n: 0, shot: s.id, hold: 1 }); } caps.sort((a, c) => a.t - c.t);
  let lo = 1e9, hi = -1, n = 0, minFs = 1e9;
  for (let i = 0; i < caps.length; i += has('--preview') ? 4 : 1) {
    const c = caps[i]; await pg.evaluate(t => window.seek(t), c.t); const B = await pg.evaluate('window.boxes()'), k = B.find(x => x.k === 'cap'); n++; const id = `${w}x${h} ${cut} ${c.shot} @${c.t.toFixed(1)}`;
    if (P1F) await pg.screenshot({ path: path.join(OUT, 'layout', `${w}x${h}_${cut}_${c.shot}_${c.t.toFixed(1)}${c.hold ? '_hold' : ''}.jpg`), type: 'jpeg', quality: 80 });
    if (!k && c.hold) { for (const x of B) { if (x.l < -0.3 || x.r > 100.3 || x.t < -0.3 || x.b > 100.3) errs.push(`${id} ${x.k} "${x.txt}" leaves the frame`); if (x.k === 'label') B.forEach((y, yi) => { if (y !== x && ['label', 'stack', 'axes', 'tag', 'title', 'stub', 'part', 'chips', 'scale'].includes(y.k) && (y.k !== 'label' || yi > B.indexOf(x)) && ov(x, y)) errs.push(`${id} label "${x.txt}" over ${y.k} "${y.txt}"`); }); } const cr3 = await pg.evaluate('window.craft()'), sw3 = Math.min(info.W, info.H); for (const d of cr3.ld) { const pc = d / 100 * info.W / sw3 * 100; mm2.push(pc); if (pc > 12.5) errs.push(`${id} MM2 label ${pc.toFixed(1)} % of the short side from its dot (≤ 12 %)`); } continue; }
    if (!k) { errs.push(id + ' no caption'); continue; }
    if (c.shot === 'S23') { const z = await pg.evaluate(`(()=>{const a=document.querySelector('[aria-label*="three-layer cut for two"]'),o=(a?a.textContent:'');const m=/Labels: ([^.]*)\./.exec(a?a.getAttribute('aria-label'):'');return {ok:!!a,extra:m?m[1].split(', ').filter(x=>!o.includes(x)):[]}})()`); if (!z.ok || z.extra.length) errs.push(`${id} S23 aria-label tells the answer early: ${z.ok ? z.extra : 'no stage label'}`); }
    lo = Math.min(lo, k.t); hi = Math.max(hi, k.b); minFs = Math.min(minFs, ...B.map(x => x.fs));
    const top = cut === 'short' && c.n > 1 ? info.bands.capTop : b[0];
    if (k.t < top - 0.3 || k.b > b[1] + 0.3) errs.push(`${id} caption ${k.t.toFixed(1)}–${k.b.toFixed(1)} % outside ${top}–${b[1]}: "${k.txt}"`);
    if (k.r - k.l > info.bands.capMaxW + 0.5) errs.push(`${id} caption ${(k.r - k.l).toFixed(0)} % wide: "${k.txt}"`);
    if (!k.vis) errs.push(id + ' caption off screen');
    const cr = await pg.evaluate('window.craft()'); for (const l of cr.ld) if (l > (w < 400 ? 27 : 25.5)) errs.push(`${id} leader ${l.toFixed(0)} % of the width`);
    if (cr.bx && !cr.bx.close) { const z = cr.bx; if (cut === 'short' && z.b > k.t + 0.5) errs.push(`${id} caption over the subject (${z.b.toFixed(0)} > ${k.t.toFixed(0)})`); if (cut !== 'short' && z.b > 84.5) errs.push(`${id} subject runs under the captions (${z.b.toFixed(0)})`);
      for (const x of B) if ((x.k === 'label' || (x.k === 'stack' && (z.sec || w < 400))) && ov(x, z) && Math.min(x.r, z.r) - Math.max(x.l, z.l) > 1 && Math.min(x.b, z.b) - Math.max(x.t, z.t) > 1) errs.push(`${id} ${x.k} "${x.txt}" on the subject`); }
    for (const x of B) {
      if (x.k === 'cap') continue;
      if (ov(x, k)) errs.push(`${id} ${x.k} "${x.txt}" under the caption`);
      if (x.l < -0.3 || x.r > 100.3 || x.t < -0.3 || x.b > 100.3) errs.push(`${id} ${x.k} "${x.txt}" leaves the frame`);
      if (x.k === 'label') B.forEach((y, yi) => { if (y !== x && ['label', 'stack', 'axes', 'tag', 'title', 'stub', 'host', 'part', 'chips', 'scale'].includes(y.k) && (y.k !== 'label' || yi > B.indexOf(x)) && ov(x, y)) errs.push(`${id} label "${x.txt}" over ${y.k} "${y.txt}"`); });
    }
    if (P1F) { const L = B.filter(x => x.k === 'label'), cr2 = await pg.evaluate('window.craft()'), sw = Math.min(info.W, info.H); for (const d of cr2.ld) { const px = d / 100 * info.W, pc = px / sw * 100; mm2.push(pc); if (pc > 12.5) errs.push(`${id} MM2 label ${pc.toFixed(1)} % of the short side from its dot (≤ 12 %)`); } if (L.length > 6) errs.push(`${id} ${L.length} labels (≤ 6)`); }
    if (!seen.has(c.shot) && (P1F ? PRIMER : /^(S01|S04|S06|S07|S11|S13|S20|S21|S23|SS2|SS4|SS6)$/).test(c.shot)) { seen.add(c.shot); await pg.screenshot({ path: path.join(OUT, 'layout', `${w}x${h}_${cut}_${c.shot}.jpg`), type: 'jpeg', quality: 80 }); }
  }
  for (const d of P1F ? info.ideas.filter(d => d.brk != null) : []) {   // the held frame at each idea pause: no caption, nothing off frame or overlapping
    await pg.evaluate(t => window.seek(t), d.brk); const B = await pg.evaluate('window.boxes()'), id = `${w}x${h} ${cut} pause ${d.id} @${d.brk}`;
    if (B.some(x => x.k === 'cap')) errs.push(`${id} caption on the held frame`);
    { const crp = await pg.evaluate('window.craft()'), swp = Math.min(info.W, info.H); for (const dd of crp.ld) { const pc = dd / 100 * info.W / swp * 100; if (pc > 12.5) (PRIMER.test(d.shot || '') || /L.i01$/.test(d.id) ? errs : mm2Carry).push(`${id} MM2 label ${pc.toFixed(1)} % of the short side from its dot (≤ 12 %)`); } }   /* pause frames on P1 ② shots: MM2 is carried to R1 (render check MM1–MM8, D-107), reported, not failed */
    for (const x of B) { if (x.l < -0.3 || x.r > 100.3 || x.t < -0.3 || x.b > 100.3) errs.push(`${id} ${x.k} "${x.txt}" leaves the frame`); if (x.k === 'label') B.forEach((y, yi) => { if (y !== x && ['label', 'stack', 'axes', 'tag', 'title', 'stub', 'part', 'chips', 'scale'].includes(y.k) && (y.k !== 'label' || yi > B.indexOf(x)) && ov(x, y)) errs.push(`${id} label "${x.txt}" over ${y.k} "${y.txt}"`); }); }
    pauses[`${w}x${h} ${cut}`] = (pauses[`${w}x${h} ${cut}`] || 0) + 1; await pg.screenshot({ path: path.join(OUT, 'layout', `${w}x${h}_${cut}_pause_${d.id.slice(-3)}.jpg`), type: 'jpeg', quality: 80 });
  }
  if (await pg.evaluate('document.documentElement.scrollWidth>innerWidth')) errs.push(`${w}x${h} ${cut} page scrolls sideways`);
  rep[`${w}x${h} ${cut}`] = { frame: `${info.W}×${info.H}`, captions: n, top: +lo.toFixed(1), bottom: +hi.toFixed(1), minFont: +minFs.toFixed(1) }; console.log(`${w}x${h}`, cut, JSON.stringify(rep[`${w}x${h} ${cut}`]));
  if (cut === 'lesson' && !P1F) for (const c of await pg.evaluate('window.cellCheck()')) if (c.bad) errs.push(`t-meso day ${c.day}: outside ${c.in}`);
  await pg.close();
}
await br.close(); srv.close(); fs.writeFileSync(path.join(OUT, P1F ? 'check-p1f.json' : 'check.json'), JSON.stringify({ rep, errs, ...(P1F ? { pauses, mm2_max: +Math.max(0, ...mm2).toFixed(1), mm2_carried_to_R1: mm2Carry } : {}) }, null, 1));
if (P1F && mm2Carry.length) console.log(`MM2 on P1 ② pause frames, carried to R1: ${mm2Carry.length}`);
if (P1F) console.log('pause frames', JSON.stringify(pauses), 'MM2 max', Math.max(0, ...mm2).toFixed(1), '% of the short side');
console.log(errs.length ? `FAIL ${errs.length} errors` : 'PASS 0 errors'); for (const e of errs.slice(0, 40)) console.log(' -', e);
process.exit(errs.length ? 1 : 0);
