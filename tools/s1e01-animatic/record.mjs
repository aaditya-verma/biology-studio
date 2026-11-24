// S1E01 animatic — frames + MP4 (P1 ②). node record.mjs --cut lesson [--fps 15] [--preview (4 fps)] [--shots (one still per shot)] [--only S13] [--dry-run] [--debug] [--out dir]
// Serves Studio home itself, GPU Chromium, pipes JPEG frames to FFmpeg x264 crf 23 (D-045 E1) with the −14 LUFS cut audio. Output in out/ (never committed).
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { spawn } from 'node:child_process'; import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), HOME = path.resolve(process.env.BIO_HOME || (HERE.includes(path.sep + 'repo' + path.sep) ? path.join(HERE, '../../../..') : path.join(HERE, '../..')));
const { chromium } = await import(pathToFileURL(path.join(HOME, 'tools/m1-bakeoff/B_three/node_modules/playwright/index.mjs')));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; }, has = k => process.argv.includes(k);
const cut = arg('--cut', 'lesson'), fps = has('--preview') ? 4 : +arg('--fps', 15), OUT = path.resolve(arg('--out', path.join(HOME, 'tools/s1e01-animatic/out'))), [w, h] = cut === 'short' ? [720, 1280] : [1280, 720];
const MT = { '.html': 'text/html', '.mjs': 'text/javascript', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wav': 'audio/wav', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => { const p = path.join(HOME, decodeURIComponent(q.url.split('?')[0]).replace(/\/$/, '/index.html')); if (!p.startsWith(HOME) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MT[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); }).listen(0, '127.0.0.1');
const br = await chromium.launch({ args: ['--enable-gpu', '--ignore-gpu-blocklist', '--use-angle=d3d11'] }), pg = await br.newPage({ viewport: { width: w, height: h } });
pg.on('pageerror', e => { console.error('FAIL page', e.message); }); pg.on('console', m => { if (has('--debug') || m.type() === 'error') console.log('[page]', m.text()); });
await pg.goto(`http://127.0.0.1:${srv.address().port}/tools/s1e01-animatic/?record=1&cut=${cut}`); await pg.waitForFunction('window.ready===true', null, { timeout: 60000 });
const info = await pg.evaluate('window.info()'); console.log(cut, info.dur, 's', info.gpu);
if (has('--dry-run')) { await br.close(); srv.close(); process.exit(0); }
if (has('--shots')) { const d = path.join(OUT, 'stills'); fs.mkdirSync(d, { recursive: true }); for (const s of info.shots) { if (arg('--only') && s.id !== arg('--only')) continue; for (const k of cut === 'short' ? [.12, .45, .9] : [.3, .9]) { await pg.evaluate(t => window.seek(t), s.s + (s.e - s.s) * k); await pg.screenshot({ path: path.join(d, `${cut}_${s.id}_${Math.round(k * 100)}.jpg`), type: 'jpeg', quality: 85 }); } } }
else {
  const mp4 = path.join(OUT, `S1E01_${cut}.mp4`), ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-i', path.join(OUT, cut + '.wav'), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.ceil(info.dur * fps), t0 = Date.now();
  for (let i = 0; i < N; i++) { await pg.evaluate(t => window.seek(t), i / fps); const b = await pg.screenshot({ type: 'jpeg', quality: 88 }); if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 150 === 0) console.log(`frame ${i}/${N} ${((Date.now() - t0) / 1000).toFixed(0)} s`); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('done', mp4, (fs.statSync(mp4).size / 1e6).toFixed(1), 'MB', ((Date.now() - t0) / 1000).toFixed(0), 's');
}
await br.close(); srv.close();
