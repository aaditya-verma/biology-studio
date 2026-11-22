/* Biology Studio — shell: top bar (Back · trail · Search · Up), nav (U2: floating bar + More sheet on phone portrait, side strip on phone landscape,
   rail with labels on tablet + desktop), Back dock (D-084), theme, render, ✎ edit hooks, keys, toast.
   Owner doc: build/design-plan.md §3–§4 (layouts per class, §8a). EDIT: nav items in CONFIG.nav, words in STR, icons below. */
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
/* EDIT: icons (24×24 stroke) */
const ICONS={cards:'<rect x="4" y="5" width="13" height="15" rx="2"/><path d="M8 3h10a2 2 0 0 1 2 2v12"/><path d="M7.5 10h6M7.5 14h4"/>',today:'<path d="M4 6h16v14H4z"/><path d="M4 10h16M9 3v4M15 3v4"/>',map:'<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>',
  settings:'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
  scene:'<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/>',fwd:'<path d="M9 5l7 7-7 7"/>',
  play:'<path d="M7 4.5v15l12-7.5z"/>',pause:'<path d="M8 5v14M16 5v14"/>',
  back:'<path d="M15 5l-7 7 7 7"/>',up:'<path d="M12 19V5M5 12l7-7 7 7"/>',sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.4 1.4M17.6 17.6L19 19M5 19l1.4-1.4M17.6 6.4L19 5"/>',
  studio:'<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/><path d="M14 20h6"/>',
  progress:'<circle cx="5" cy="6" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="19" cy="12" r="2.5"/><path d="M7.5 6h3.5l5.5 5M7.5 18h3.5l5.5-5"/>',
  review:'<path d="M9 4H6a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-3"/><rect x="9" y="2.5" width="6" height="3.5" rx="1"/><path d="M8.5 13.5l2.5 2.5 4.5-5"/>',
  moon:'<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',search:'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',more:'<circle cx="5.5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="18.5" cy="12" r="1.6"/>',close:'<path d="M6 6l12 12M18 6L6 18"/>'};
const icon=(k,sz=22)=>`<svg viewBox="0 0 24 24" width="${sz}" height="${sz}" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[k]||''}</svg>`;

/* theme: device / light / dark (saved in state.settings.theme; localStorage mirror so first paint is right) */
function themeMode(){return (state&&state.settings.theme)||(()=>{try{return localStorage.getItem(CONFIG.keys.theme)||'system';}catch(_){return 'system';}})();}
function applyTheme(){const m=themeMode(),dark=m==='dark'||(m==='system'&&matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.dataset.theme=dark?'dark':'light';const meta=$('meta[name=theme-color]');if(meta)meta.content=getComputedStyle(document.documentElement).getPropertyValue('--bg').trim();}
function setTheme(m){state.settings.theme=m;state.settings.t=Date.now();try{localStorage.setItem(CONFIG.keys.theme,m);}catch(_){}applyTheme();stSave();render();}
try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>{if(themeMode()==='system'){applyTheme();render();}});}catch(_){}

/* H2: Reviewer mode adds Review after Cards (6 items, labels shrink like testing mode); testing mode keeps its own nav (Review by address) */
const rvNavOn=()=>!FLAGS.test&&!!(state&&state.review&&state.review.on);
const navItems=()=>{const n=CONFIG.nav.slice();if(rvNavOn())n.splice(Math.max(1,n.indexOf('cards')+1),0,CONFIG.navReview);return n.concat(FLAGS.test?CONFIG.navTest:[]);};
function buildShell(){
  const bar=CONFIG.navBar;   // U2: items in the phone-portrait bar get data-bar; the rest show in rails and in the More sheet
  // D-087 (owner's Strava pattern): icon in a pill + label under it; a logo mark tops the tablet/desktop rail; More = tiles (icon, name, one line, new-dot)
  $('#nav').innerHTML=`<span class="nlogo" aria-hidden="true"><img src="assets/icon.svg" alt="" width="40" height="40"></span>`
    +navItems().map(k=>`<button type="button" data-nav="${k}"${bar.includes(k)?' data-bar':''} aria-label="${esc(STR.nav[k])}" title="${esc(STR.nav[k])} — ${esc(STR.navHint[k])}"><span class="nic">${icon(k)}</span><span class="nl" aria-hidden="true">${esc(STR.nav[k])}</span></button>`).join('')
    +`<button type="button" id="moreb" data-bar aria-haspopup="dialog" aria-label="${esc(STR.more)}" title="${esc(STR.moreT)}"><span class="nic">${icon('more')}</span><span class="nl" aria-hidden="true">${esc(STR.more)}</span></button>`;
  $('#moreL').innerHTML=navItems().filter(k=>!bar.includes(k)).map(k=>`<button type="button" class="mtile" data-nav="${k}" data-sheet><span class="mic">${icon(k,24)}</span><b>${esc(STR.nav[k])}</b><span class="md">${esc(STR.navShort[k]||'')}</span></button>`).join('');
  $('#dkfold').setAttribute('aria-label',STR.dockFold);$('#dkfold').title=STR.dockFold;dockFoldSet(dockFolded());
  $('#moreT').textContent=STR.moreT;$('#moreX').textContent=STR.close;
  $('#srchb').innerHTML=icon('search',20);$('#srchb').setAttribute('aria-label',STR.searchGo);$('#srchb').title=STR.searchGo;
  $('#dock').innerHTML=icon('back',22)+`<span class="sr">${esc(STR.back)}</span>`;$('#dock').title=STR.back;
  $('#editChatL').textContent=STR.editChat;$('#editCopy').textContent=STR.copy;$('#editClose').textContent=STR.close;$('#editTxt').setAttribute('aria-label',STR.editT);
  $('#brand').textContent=STR.app;toastRegion();
  $('#backb').innerHTML=icon('back',20);$('#backb').setAttribute('aria-label',STR.back);$('#backb').title=STR.back;
  $('#upb').innerHTML=icon('up',20);$('#upb').setAttribute('aria-label',STR.up);$('#upb').title=STR.up;
  document.documentElement.classList.toggle('rvnav',rvNavOn());
  if(FLAGS.test){$('#testflag').textContent=STR.testShort;$('#testflag').title=STR.testFlag;$('#testflag').classList.remove('hidden');document.documentElement.classList.add('test');}
}
const navOf=r=>({concept:'map',x:'map',colours:'settings',day:'scene',calib:'studio',step:'progress',card:'cards',deck:'today',lessons:'cards',lesson:'cards',mix:'today',rcard:'review',rtour:'review',updates:'review'}[r.name]||r.name);
function syncShell(){
  $$('#nav [data-nav]').forEach(b=>{if(b.dataset.nav===navOf(ROUTE))b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
  const cr=ROUTE.crumbs||[{label:STR.nav[navOf(ROUTE)]||STR.app}];
  $('#crumbs').innerHTML=cr.map((c,i)=>i<cr.length-1?`<button type="button" data-go="${esc(c.hash)}">${esc(c.label)}</button><span aria-hidden="true">›</span>`:`<b>${esc(c.label)}</b>`).join('');
  const home=!upOf(ROUTE);$('#upb').classList.toggle('hidden',home);
  const cb=canBack();$('#backb').classList.toggle('hidden',!cb);document.documentElement.classList.toggle('can-back',cb);$('#dock').classList.toggle('hidden',!cb);   // D-084: Back whenever there is history (never at the first step: Back there would arm "leave")
  const off=!CONFIG.navBar.includes(navOf(ROUTE)),mb=$('#moreb');if(mb){if(off)mb.setAttribute('aria-current','page');else mb.removeAttribute('aria-current');}   // a page reached from More lights More on the bar
  $$('#moreL [data-nav]').forEach(b=>{if(b.dataset.nav===navOf(ROUTE))b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
  navNewSync();barShow(true);document.documentElement.classList.toggle('rm',typeof motionReduced==='function'&&motionReduced());
  document.title=cr[cr.length-1].label+' · '+STR.app;
  const ae=document.activeElement;if(ae&&ae!==document.body&&!ae.getClientRects().length)view().focus({preventScroll:true});   // the dock/Back just hid under focus: keep focus in the page
}

/* screens register themselves: SCREENS[name]=fn(view) */
const SCREENS={};
const view=()=>$('#view');
function render(prev){
  const t0=performance.now(),f=SCREENS[ROUTE.name]||SCREENS[CONFIG.home];ROUTE.crumbs=null;
  const ae=document.activeElement,inView=ae&&ae.closest&&ae.closest('#view'),keep=inView&&ae.id&&ae.matches('select,input,textarea')?ae.id:null,   // a control in the page caused this: keep focus on it
    fk=inView&&!keep&&ae.dataset&&ae.dataset.fk?ae.dataset.fk:null,   // …or a button that marks itself with data-fk (Studio, calibration)
    sel=keep&&ae.matches('input[type=text],input:not([type]),textarea')?[ae.selectionStart,ae.selectionEnd,ae.scrollTop]:null;   // caret + scroll survive a redraw
  try{f(view(),prev||{});}catch(e){console.error(e);view().innerHTML=`<div class="card"><b>${esc(STR.drawFail)}</b><p class="mut">${esc(e.message)}</p></div>`;}
  syncShell();if(FLAGS.test)testBanner();cueSoon();
  const fkEl=fk&&document.querySelector(`#view [data-fk="${CSS.escape(fk)}"]`);
  if(keep&&document.getElementById(keep)){const k=document.getElementById(keep);k.focus({preventScroll:true});if(sel&&k.setSelectionRange){try{k.setSelectionRange(sel[0],sel[1]);k.scrollTop=sel[2];}catch(_){}}}
  else if(fkEl)fkEl.focus({preventScroll:true});
  else if(prev&&prev.raw!==undefined&&prev.raw!==ROUTE.raw&&!$('dialog[open]')){   // route changed: move focus to the new page (screen readers hear it; Tab starts here)
    const t=$('#view [data-focus-first]')||$('#cpT')||$('#view h1');if(t){   // data-focus-first: a page can ask for a different target (W2: Back to the map focuses the node you came from)
      if(!t.hasAttribute('tabindex'))t.setAttribute('tabindex','-1');t.focus({preventScroll:DEV.cls==='dev-d'});}}
  dbgNote('render '+ROUTE.name+' '+(performance.now()-t0).toFixed(1)+' ms');
}
function testBanner(){if(!$('#view .banner.tb'))view().insertAdjacentHTML('afterbegin',`<p class="banner tb">${esc(STR.testFlag)}</p>`);}

/* ✎ edit hooks (testing mode): show id + file path, copy a ready "edit this" prompt (RULES I6) */
const editBtn=(kind,id,file)=>`<button type="button" class="edit" data-edit="${esc(kind)}|${esc(id)}|${esc(file)}" aria-label="Edit ${esc(kind)} ${esc(id)}" title="Edit ${esc(id)} (${esc(file)})">✎</button>`;
function editPrompt(kind,id,file){
  const chat='Bio · Fix · '+id;
  return `Chat: ${chat}\nItem: ${kind} ${id}\nFile: ${file}\n\nRead claude/STATUS.md, claude/RULES.md (A2, I5–I6, C8, C13) and the owner doc for this item.\nFix ${kind} ${id}: <say what is wrong>.\nChange only ${file} (ids stay — A2), run tools/layout-check --preview if it is UI, commit by route A.\nEnd with STATUS, build log, gates, usage check.`;}
function openEdit(kind,id,file){const d=$('#editdlg');$('#editT').textContent='✎ '+kind+' '+id;$('#editChat').textContent='Bio · Fix · '+id;
  $('#editTxt').value=editPrompt(kind,id,file);$('#editMsg').textContent='';d.showModal();}

function toastRegion(){let t=$('#toast');if(!t){t=document.createElement('div');t.id='toast';t.className='toast off';t.setAttribute('role','status');document.body.appendChild(t);}return t;}   // created at start (buildShell), so the first message is heard too (H2 G-A11y; L1F to-do)
function toast(msg){const t=toastRegion();
  t.textContent=msg;t.classList.remove('off');clearTimeout(t._h);t._h=setTimeout(()=>t.classList.add('off'),2200);}   // 'off' = visually gone, still in the accessibility tree

/* events (one delegated listener) */
function shellEvents(){
  document.addEventListener('click',e=>{
    const ed=e.target.closest('[data-edit]');if(ed){e.preventDefault();e.stopPropagation();const[k,i,f]=ed.dataset.edit.split('|');openEdit(k,i,f);return;}
    const n=e.target.closest('[data-nav]');if(n){if(n.hasAttribute('data-sheet'))$('#moresh').close();go(n.dataset.nav);return;}
    const g=e.target.closest('[data-go]');if(g){go(g.dataset.go);return;}
    if(e.target.closest('#brand')){go(CONFIG.home);return;}
    if(e.target.closest('#backb')||e.target.closest('#dock')){goBack();return;}
    if(e.target.closest('#dkfold')){dockFoldSet(!dockFolded(),true);return;}
    if(e.target.closest('#moreb')){$('#moresh').showModal();return;}
    if(e.target.closest('#moreX')){$('#moresh').close();return;}
    if(e.target===$('#moresh')){const b=e.target.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)$('#moresh').close();return;}   // only a tap on the backdrop (outside the sheet) closes it
    if(e.target.closest('#srchb')){searchGo();return;}
    if(e.target.closest('#upb')){goUp();return;}
  });
  $('#editClose').onclick=()=>$('#editdlg').close();
  $('#editCopy').onclick=async()=>{try{await navigator.clipboard.writeText($('#editTxt').value);$('#editMsg').textContent=STR.copied;}catch(_){$('#editTxt').select();$('#editMsg').textContent=STR.copyFail;}};
  /* desktop keys (§8a rule 5): / search · Esc back (or close) */
  document.addEventListener('keydown',e=>{
    if(e.target.matches('input,textarea,select')){if(e.key==='Escape')e.target.blur();return;}
    if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!$('dialog[open]')&&!e.target.closest('[contenteditable]')){e.preventDefault();searchGo();}
    else if(e.key==='Escape'&&!$('dialog[open]')&&(canBack()||upOf(ROUTE))){goBack();}
  });
  barScroll();sheetDrag();
  document.addEventListener('focusin',e=>{const b=e.target;if(b&&b.closest&&b.closest('.seg'))b.scrollIntoView({block:'nearest',inline:'nearest'});});   // G-A11y: a focused tab in a scrolled pill comes into view
  document.addEventListener('scroll',e=>{const t=e.target;if(t&&t.nodeType===1&&(t.matches('[data-cue]')||t.matches('.seg')))cueOne(t);},{capture:true,passive:true});
  addEventListener('resize',cueSoon);document.addEventListener('click',()=>setTimeout(cueAll,60));onDevice(cueSoon);
  try{document.fonts&&document.fonts.ready.then(cueAll);}catch(_){}
}
/* D-087: scroll cues — a side panel ([data-cue]) with content hidden below shows a fade + "More ↓"; a pill (.seg) that scrolls sideways fades its hidden end */
function cueOne(el){
  if(el.matches('.seg')){const sl=el.scrollLeft,mx=el.scrollWidth-el.clientWidth;el.classList.toggle('ovf-r',mx>2&&sl<mx-2);el.classList.toggle('ovf-l',mx>2&&sl>2);return;}
  let c=el.querySelector(':scope>.cue');if(!c){c=document.createElement('div');c.className='cue';c.setAttribute('aria-hidden','true');c.textContent=STR.moreBelow;el.appendChild(c);}
  else if(c!==el.lastElementChild)el.appendChild(c);
  const s=getComputedStyle(el),scrolls=/(auto|scroll)/.test(s.overflowY);
  el.classList.toggle('cue-on',scrolls&&el.scrollHeight-el.clientHeight>8&&el.scrollTop+el.clientHeight<el.scrollHeight-8);}
function cueAll(){$$('[data-cue],.seg').forEach(cueOne);}
let cueT=0;function cueSoon(){cancelAnimationFrame(cueT);cueT=requestAnimationFrame(()=>requestAnimationFrame(cueAll));}
/* D-087: new-dot badges — a nav item with something new for you (Review: cards changed since your last look); the More button carries the dot of its tiles */
function navNew(k){try{return k==='review'&&typeof RV!=='undefined'&&!!RV.idx&&!!(state&&state.review&&state.review.seenAt)&&rvNews().length>0;}catch(_){return false;}}
function navNewSync(){let more=false;
  $$('[data-nav]').forEach(b=>{const k=b.dataset.nav,on=navNew(k),host=b.querySelector('.nic,.mic');if(!host)return;let d=host.querySelector('.ndot');
    if(on&&!d){d=document.createElement('i');d.className='ndot';d.setAttribute('aria-hidden','true');host.appendChild(d);}else if(!on&&d)d.remove();
    const nm=STR.nav[k]+(on?' ('+STR.newMark+')':'');if(b.matches('#nav button'))b.setAttribute('aria-label',nm);else{const t=b.querySelector('b');if(t)t.textContent=nm;}
    if(on&&!CONFIG.navBar.includes(k))more=true;});
  const mb=$('#moreb');if(mb){const h=mb.querySelector('.nic');let d=h.querySelector('.ndot');if(more&&!d){d=document.createElement('i');d.className='ndot';d.setAttribute('aria-hidden','true');h.appendChild(d);}else if(!more&&d)d.remove();
    mb.setAttribute('aria-label',STR.more+(more?' ('+STR.newMark+')':''));}}
/* D-087: the Back dock folds into a small handle; the choice is kept on this device (localStorage, never in state — A1) */
function dockFolded(){try{return localStorage.getItem(CONFIG.keys.dockFold)==='1';}catch(_){return false;}}
function dockFoldSet(on,user){document.documentElement.classList.toggle('dock-fold',on);try{localStorage.setItem(CONFIG.keys.dockFold,on?'1':'0');}catch(_){}
  const b=$('#dkfold');if(b){const t=on?STR.dockOpen:STR.dockFold;b.setAttribute('aria-label',t);b.title=t;const i=b.querySelector('i');if(i)i.textContent=on?'›':'‹';}   // the label says the action (G-A11y: no aria-expanded on top of it)
  if(user&&!on)setTimeout(()=>{const d=$('#dock');if(d&&d.getClientRects().length)d.focus();},30);}
/* D-087: a dialog on phone portrait is a bottom sheet — drag its grip (or its top edge) down to close it; a short drag springs back */
function sheetDrag(){let d=null,y0=0,dy=0;
  document.addEventListener('pointerdown',e=>{const dl=e.target.closest('dialog[open]');if(!dl||DEV.cls!=='dev-p')return;const r=dl.getBoundingClientRect();
    if(!(e.target.closest('.grip')||e.clientY-r.top<CONFIG.sheet.gripH))return;d=dl;y0=e.clientY;dy=0;d.classList.add('drag');try{d.setPointerCapture(e.pointerId);}catch(_){}});
  document.addEventListener('pointermove',e=>{if(!d)return;dy=Math.max(0,e.clientY-y0);d.style.transform=dy?`translateY(${dy}px)`:'';},{passive:true});
  const end=cancel=>{if(!d)return;const dl=d;d=null;dl.classList.remove('drag');
    if(!cancel&&dy>Math.min(CONFIG.sheet.closePx,dl.offsetHeight*CONFIG.sheet.closeFrac)){const motion=!(typeof motionReduced==='function'&&motionReduced());dl.style.transform=motion?'translateY(100%)':'';setTimeout(()=>{dl.close();dl.style.transform='';},motion?200:0);}
    else dl.style.transform='';};   // a short drag or a cancelled one springs back
  document.addEventListener('pointerup',()=>end(false));document.addEventListener('pointercancel',()=>end(true));}
/* U2 — Search one tap from every screen (D-084 (5)): the Book map's search box, focused */
function searchGo(){const f=()=>{const q=$('#bmq');if(q&&q.getClientRects().length){q.focus();if(q.select)q.select();return true;}return false;};   // only a visible box (phones show one pane at a time)
  if(ROUTE.name==='map'&&f())return;go('map');let n=0;(function w(){if(!f()&&n++<40)setTimeout(w,50);})();}
/* U2 — the floating bar hides on scroll down, comes back on scroll up, and stays away while the keyboard is up (a text field has focus) — D-084 (6) */
const TYPING='input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=button]),textarea,select';
function barShow(on){document.documentElement.classList.toggle('bar-away',!on);}
function barScroll(){let y=scrollY;onDevice(()=>barShow(true));   // a rotation always brings the bar back
  addEventListener('scroll',()=>{const d=scrollY-y;if(Math.abs(d)<8)return;
    if(DEV.cls==='dev-p'&&!(document.activeElement&&document.activeElement.matches(TYPING)))barShow(d<0||scrollY<40||(innerHeight+scrollY>=document.documentElement.scrollHeight-4));y=scrollY;},{passive:true});
  document.addEventListener('focusin',e=>{if(DEV.cls==='dev-p'&&e.target.matches(TYPING))barShow(false);});
  document.addEventListener('focusout',e=>{if(e.target.matches(TYPING))setTimeout(()=>{const a=document.activeElement;if(!a||!a.matches(TYPING))barShow(true);},60);});
}
