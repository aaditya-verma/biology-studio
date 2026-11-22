/* Biology Studio — debug flags, tagged logs and the overlay (RULES I5). Owner doc: build/design-plan.md §7.
   Flags: ?test=1 (testing mode: ✎ edit hooks, overlay — tap it to shrink, nothing saved) · ?debug=1 (all areas) or ?debug=map,viewer,studio,tracker,learn,review,layout,store,router,device,test (learn: card id, status, level, deck size + due) (review: source live/fixture/cache, issues, last check + HTTP status, rate left, cache age + a Debug section on #review) (tracker: load time, issues, lock age + a Debug section on #progress/#step; viewer: fps, triangles, draw calls + Measure fps; studio: loads, card-check counts, gate decisions, exports + overlay line).
   Flags also survive in sessionStorage (Settings › Testing mode). Off by default; never on in published output. */
'use strict';
const FLAGS=(()=>{
  const q=new URLSearchParams(location.search);let saved={};
  try{saved=JSON.parse(sessionStorage.getItem('biostudio.flags'))||{};}catch(_){}
  const test=q.has('test')?q.get('test')!=='0':!!saved.test;
  const dq=q.get('debug')??saved.debug??'';
  const debug=new Set(dq===''||dq==='0'?[]:dq==='1'?['all']:dq.split(',').map(s=>s.trim()).filter(Boolean));
  if(test&&!debug.size&&dq!=='0')debug.add('test');   // ?test=1&debug=0 = testing mode without the overlay (clean screenshots)
  return {test,debug,boxes:q.has('boxes'),fixture:test&&q.get('fixture')||''};   // H2: ?test=1&fixture=review — demo reviewer issues (CONFIG.review.fixture)   // ?test=1&fixture=drills: a card's demo copy from tools/layout-check/fixtures/ (V2 — every drill type)
})();
const dbgOn=area=>FLAGS.debug.has('all')||FLAGS.debug.has(area);
function dlog(area,...a){if(dbgOn(area))console.log('['+area+']',...a);}
function setFlags(o){Object.assign(FLAGS,o);try{sessionStorage.setItem('biostudio.flags',JSON.stringify({test:FLAGS.test,debug:[...FLAGS.debug].join(',')}));}catch(_){}}

/* overlay: version, route + ids, fps, state size, device class, viewport, dpr, pointer */
const DBG={el:null,fps:0,frames:0,t0:0,timer:0,extra:'',viewer:'',studio:'',tracker:'',learn:'',review:'',lessons:'',ladder:''};
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
  if(dbgOn('layout'))addEventListener('pointermove',e=>{DBG.ladder=dbgLadderAt(e.clientX,e.clientY);},{passive:true});   // U2: ladder level under the pointer
}
/* U2 (design-plan §7): which ladder level (L0–L4) paints the surface under a point — the nearest ancestor with an opaque background;
   'stage' inside the 3D island (.stage-dark). EDIT: nothing — the levels are read live from :root, so a token change shows here. */
function dbgLadderAt(x,y){
  let el=document.elementFromPoint(x,y);if(!el)return '';
  if(el.closest('.stage-dark'))return 'stage (#14161A island)';
  const cs=getComputedStyle(document.documentElement),probe=document.createElement('i');document.body.appendChild(probe);
  const rgb=v=>{probe.style.color=v;return getComputedStyle(probe).color;};
  const lv={};['L0','L1','L2','L3','L4'].forEach(k=>{lv[rgb(cs.getPropertyValue('--'+k).trim())]=k;});
  let out='';for(;el&&el!==document.documentElement;el=el.parentElement){const b=getComputedStyle(el).backgroundColor;
    if(b&&b!=='transparent'&&!/,\s*0\)$/.test(b)){out=(lv[b]||'off-ladder '+b)+' · '+el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(el.classList[0]?'.'+el.classList[0]:'');break;}}
  probe.remove();return out||((lv[rgb(getComputedStyle(document.body).backgroundColor)]||'page')+' · body');
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
    'device '+(typeof devLine==='function'&&d.cls?devLine():'?')+' · '+(d.input||'?')+' @'+devicePixelRatio,
    'flags  '+(FLAGS.test?'test ':'')+[...FLAGS.debug].join(','),
    dbgOn('viewer')&&typeof ROUTE!=='undefined'&&ROUTE.name==='scene'?DBG.viewer:'',
    dbgOn('studio')&&typeof ROUTE!=='undefined'&&(ROUTE.name==='studio'||ROUTE.name==='calib')?DBG.studio:'',
    dbgOn('tracker')&&typeof ROUTE!=='undefined'&&(ROUTE.name==='progress'||ROUTE.name==='step')?DBG.tracker:'',
    dbgOn('learn')&&typeof ROUTE!=='undefined'&&['card','cards','deck'].includes(ROUTE.name)?DBG.learn:'',
    dbgOn('lessons')&&typeof ROUTE!=='undefined'&&['lessons','lesson','mix','card'].includes(ROUTE.name)?DBG.lessons:'',
    dbgOn('review')&&typeof ROUTE!=='undefined'&&['review','rcard','rtour','updates'].includes(ROUTE.name)?DBG.review:'',
    dbgOn('layout')&&DBG.ladder?'ladder '+DBG.ladder:'',
    DBG.extra].filter(Boolean).join('\n');
}
function dbgNote(s){DBG.extra=s;dbgPaint();}
