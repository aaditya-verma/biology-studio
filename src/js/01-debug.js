/* Biology Studio — debug flags, tagged logs and the overlay (RULES I5). Owner doc: build/design-plan.md §7.
   Flags: ?test=1 (testing mode: ✎ edit hooks, overlay — tap it to shrink, nothing saved) · ?debug=1 (all areas) or ?debug=map,viewer,studio,tracker,learn,layout,store,router,device,test (learn: card id, status, level, deck size + due) (tracker: load time, issues, lock age + a Debug section on #progress/#step; viewer: fps, triangles, draw calls + Measure fps; studio: loads, card-check counts, gate decisions, exports + overlay line).
   Flags also survive in sessionStorage (Settings › Testing mode). Off by default; never on in published output. */
'use strict';
const FLAGS=(()=>{
  const q=new URLSearchParams(location.search);let saved={};
  try{saved=JSON.parse(sessionStorage.getItem('biostudio.flags'))||{};}catch(_){}
  const test=q.has('test')?q.get('test')!=='0':!!saved.test;
  const dq=q.get('debug')??saved.debug??'';
  const debug=new Set(dq===''||dq==='0'?[]:dq==='1'?['all']:dq.split(',').map(s=>s.trim()).filter(Boolean));
  if(test&&!debug.size&&dq!=='0')debug.add('test');   // ?test=1&debug=0 = testing mode without the overlay (clean screenshots)
  return {test,debug,boxes:q.has('boxes')};
})();
const dbgOn=area=>FLAGS.debug.has('all')||FLAGS.debug.has(area);
function dlog(area,...a){if(dbgOn(area))console.log('['+area+']',...a);}
function setFlags(o){Object.assign(FLAGS,o);try{sessionStorage.setItem('biostudio.flags',JSON.stringify({test:FLAGS.test,debug:[...FLAGS.debug].join(',')}));}catch(_){}}

/* overlay: version, route + ids, fps, state size, device class, viewport, dpr, pointer */
const DBG={el:null,fps:0,frames:0,t0:0,timer:0,extra:'',viewer:'',studio:'',tracker:'',learn:''};
function dbgStart(){
  if(!FLAGS.debug.size)return;
  if(!DBG.el){DBG.el=document.createElement('div');DBG.el.id='dbg';DBG.el.setAttribute('aria-hidden','true');document.body.appendChild(DBG.el);
    /* tap or click shrinks it to one line so it never hides the page (T3c note, L1); the choice lasts this session */
    try{if(sessionStorage.getItem('biostudio.dbgmin')==='1')DBG.el.classList.add('min');}catch(_){}
    DBG.el.title='Tap to shrink or expand';DBG.el.addEventListener('click',()=>{const m=DBG.el.classList.toggle('min');try{sessionStorage.setItem('biostudio.dbgmin',m?'1':'0');}catch(_){}});}
  if(FLAGS.boxes)document.documentElement.classList.add('dbg-boxes');
  const tick=t=>{DBG.frames++;if(!DBG.t0)DBG.t0=t;if(t-DBG.t0>=1000){DBG.fps=Math.round(DBG.frames*1000/(t-DBG.t0));DBG.frames=0;DBG.t0=t;}if(DBG.el)requestAnimationFrame(tick);};
  requestAnimationFrame(tick);
  clearInterval(DBG.timer);DBG.timer=setInterval(dbgPaint,500);dbgPaint();
}
function dbgPaint(){
  if(!DBG.el)return;
  const d=typeof DEV!=='undefined'?DEV:{};let size='—';
  try{size=typeof state!=='undefined'?(JSON.stringify(state).length/1024).toFixed(1)+' KB':'—';}catch(_){}
  const r=typeof ROUTE!=='undefined'?ROUTE:{};
  DBG.el.textContent=[appVerLine(),
    'route  #'+(location.hash.slice(1)||'—'),
    'ids    '+(r.id||r.ch||'—'),
    'fps    '+DBG.fps+' · state '+size+(typeof STORE!=='undefined'?' · rev '+STORE.rev+' · '+STORE.mode:''),
    'device '+(d.cls||'?')+' · '+(d.input||'?')+' · '+innerWidth+'×'+innerHeight+' @'+devicePixelRatio,
    'flags  '+(FLAGS.test?'test ':'')+[...FLAGS.debug].join(','),
    dbgOn('viewer')&&typeof ROUTE!=='undefined'&&ROUTE.name==='scene'?DBG.viewer:'',
    dbgOn('studio')&&typeof ROUTE!=='undefined'&&(ROUTE.name==='studio'||ROUTE.name==='calib')?DBG.studio:'',
    dbgOn('tracker')&&typeof ROUTE!=='undefined'&&(ROUTE.name==='progress'||ROUTE.name==='step')?DBG.tracker:'',
    dbgOn('learn')&&typeof ROUTE!=='undefined'&&['card','cards','deck'].includes(ROUTE.name)?DBG.learn:'',
    DBG.extra].filter(Boolean).join('\n');
}
function dbgNote(s){DBG.extra=s;dbgPaint();}
