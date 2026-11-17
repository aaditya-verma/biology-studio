/* Biology Studio — service worker (PWA from day 1). Owner doc: build/design-plan.md §6.
   App shell: cache-first, refreshed in the background. map.json: network-first, cached copy offline.
   Registers only on https (GitHub Pages / artifact hosts), so a local http.server test never exercises it.
   EDIT: bump CACHE with APP.v (src/js/00-version.js) and the ?v= in index.html — old caches are deleted on activate (RULES C6). */
const CACHE='biostudio-v1';
const SHELL=['./','index.html','manifest.webmanifest','src/css/app.css?v=1','content/strings.js?v=1',
  'src/js/00-version.js?v=1','src/js/01-debug.js?v=1','src/js/02-config.js?v=1','src/js/03-device.js?v=1','src/js/04-storage.js?v=1','src/js/05-router.js?v=1',
  'src/js/06-shell.js?v=1','src/js/10-today.js?v=1','src/js/11-bookmap.js?v=1','src/js/12-settings.js?v=1','src/js/90-layout-audit.js?v=1','src/js/91-tests.js?v=1','src/js/99-boot.js?v=1',
  'assets/icon.svg','assets/icon-192.png','assets/icon-512.png','assets/icon-maskable-512.png','content/E/map.json'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==location.origin)return;
  if(u.pathname.endsWith('/map.json')){e.respondWith(fetch(e.request).then(r=>{if(r.ok){const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));}return r;})
    .catch(()=>caches.match(e.request).then(h=>h||Response.error())));return;}
  e.respondWith(caches.match(e.request).then(hit=>{const net=fetch(e.request).then(r=>{if(r.ok){const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));}return r;})
    .catch(()=>hit||(e.request.mode==='navigate'?caches.match('index.html'):Response.error()));return hit||net;}));
});
