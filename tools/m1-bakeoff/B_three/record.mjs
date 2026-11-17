// Method B: headless three.js → PNG frames. Run from the kit folder:
//   node B_three/record.mjs --out out/B_three [--every N] [--headed]
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const KIT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const out = path.resolve(KIT, arg('--out', 'out/B_three'));
const every = Number(arg('--every', 1));
const headed = process.argv.includes('--headed');
fs.mkdirSync(path.join(out, 'frames'), { recursive: true });

const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const p = path.join(KIT, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(KIT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch({
  headless: !headed,
  args: ['--enable-gpu', '--ignore-gpu-blocklist', '--use-angle=d3d11', '--enable-unsafe-swiftshader'],
});
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
page.on('console', m => console.log('[page]', m.text()));
page.on('pageerror', e => console.error('[page error]', e.message));
await page.goto(`http://localhost:${port}/B_three/shot.html`);
await page.waitForFunction('window.ready === true', null, { timeout: 60000 });
const info = await page.evaluate('window.appInfo');
console.log('[B] WebGL renderer:', info.gpu, '| three r' + info.three);

const t0 = Date.now(), per = [];
for (let f = 0; f < info.frames; f += every) {
  const tf = Date.now();
  const url = await page.evaluate(n => window.renderFrame(n), f);
  fs.writeFileSync(path.join(out, 'frames', String(f).padStart(4, '0') + '.png'), Buffer.from(url.split(',')[1], 'base64'));
  per.push((Date.now() - tf) / 1000);
  if (f % 48 === 0) console.log(`[B] frame ${f} ${per.at(-1).toFixed(3)}s`);
}
const total = (Date.now() - t0) / 1000, mean = per.reduce((a, b) => a + b, 0) / per.length;
const stats = {
  method: 'B_three_headless', tool: `three.js r${info.three} + Playwright Chromium ${browser.version()}`,
  engine: `WebGL via ${info.gpu}`, frames_rendered: per.length, frames_total: info.frames, every,
  sec_total: +total.toFixed(1), sec_per_frame_mean: +mean.toFixed(4), sec_first_frame: +per[0].toFixed(3),
  est_sec_full_shot: +(mean * info.frames).toFixed(1),
  settings: { res: [1280, 720], antialias: true, headless: !headed },
};
fs.writeFileSync(path.join(out, 'render_stats.json'), JSON.stringify(stats, null, 2));
console.log('[B] done', JSON.stringify(stats));
await browser.close(); server.close();
