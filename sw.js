/* Biology Studio — service worker (PWA from day 1). Owner doc: build/design-plan.md §6.
   App shell: cache-first, refreshed in the background. map.json + scenes: network-first, cached copy offline.
   Cards + sources.json (Studio, testing mode) are network-first like scenes. studio-docs/ (progress map: steps.json, STATUS, master plan, backlog — W1) too,
   so the map is live after a push; the cached copy shows offline.
   three.js (lib/) and the 3D engine are cached on first use (not precached: first load stays light, H8).
   Registers only on https (GitHub Pages / artifact hosts), so a local http.server test never exercises it.
   H2: the reviewer's GitHub issues come from api.github.com (another origin) — never cached here; the app keeps its own copy in the saved state.
   EDIT: bump CACHE with APP.v (src/js/00-version.js) and the ?v= in index.html — old caches are deleted on activate (RULES C6). */
const CACHE='biostudio-v17';
const SHELL=['./','index.html','manifest.webmanifest','src/css/app.css?v=16','content/strings.js?v=16',
  'src/js/00-version.js?v=16','src/js/01-debug.js?v=14','src/js/02-config.js?v=15','src/js/03-device.js?v=1','src/js/04-storage.js?v=14','src/js/05-router.js?v=14',
  'src/js/06-shell.js?v=14','src/js/10-today.js?v=14','src/js/11-bookmap.js?v=10','src/js/12-settings.js?v=13','src/js/13-viewer.js?v=15','src/js/15-cards.js?v=15','src/js/16-studio.js?v=11','src/js/17-plan.js?v=16','src/js/17-tracker.js?v=16','src/js/18-learn.js?v=15','src/js/19-review.js?v=13','src/js/20-lessons.js?v=14','src/js/90-layout-audit.js?v=13','src/js/91-tests.js?v=16','src/js/99-boot.js?v=2',
  'assets/icon.svg','assets/icon-192.png','assets/icon-512.png','assets/icon-maskable-512.png','content/E/map.json','content/E/scenes/index.json'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==location.origin)return;
  if(u.pathname.endsWith('/map.json')||u.pathname.includes('/scenes/')||u.pathname.includes('/cards/')||u.pathname.includes('/lessons/')||u.pathname.endsWith('/sources.json')||u.pathname.includes('/studio-docs/')){e.respondWith(fetch(e.request).then(r=>{if(r.ok){const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));}return r;})
    .catch(()=>caches.match(e.request).then(h=>h||Response.error())));return;}
  e.respondWith(caches.match(e.request).then(hit=>{const net=fetch(e.request).then(r=>{if(r.ok){const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));}return r;})
    .catch(()=>hit||(e.request.mode==='navigate'?caches.match('index.html'):Response.error()));return hit||net;}));
});
