/* Biology Studio — boot: theme → device → storage → shell → router → service worker. Owner doc: build/design-plan.md §3. */
'use strict';
(async function boot(){
  applyTheme();deviceApply();onDevice(()=>{dbgPaint();});
  await stLoad();applyTheme();
  buildShell();shellEvents();dbgStart();
  mapLoad();scIndexLoad();routerStart();
  if(dbgOn('layout')){const b=document.createElement('button');b.className='btn';b.textContent='Check layout';b.style.cssText='position:fixed;z-index:71;left:8px;bottom:8px';
    b.onclick=()=>{const i=layoutAudit();console.table(i);toast(i.length?i.length+' layout issues (console)':'Layout clean');};document.body.appendChild(b);}
  if('serviceWorker' in navigator&&!FLAGS.test&&location.protocol==='https:')navigator.serviceWorker.register('sw.js').catch(e=>dlog('store','sw',e.message));
  window.BOOTED=true;
})();
