/* Biology Studio — shell: top bar, nav (bottom bar on phone/tablet portrait, rail elsewhere), theme, render, ✎ edit hooks, keys, toast.
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
  moon:'<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',close:'<path d="M6 6l12 12M18 6L6 18"/>'};
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
  $('#nav').innerHTML=navItems().map(k=>`<button type="button" data-nav="${k}" aria-label="${esc(STR.nav[k])}" title="${esc(STR.nav[k])} — ${esc(STR.navHint[k])}">${icon(k)}<span aria-hidden="true">${esc(STR.nav[k])}</span></button>`).join('');
  $('#editChatL').textContent=STR.editChat;$('#editCopy').textContent=STR.copy;$('#editClose').textContent=STR.close;$('#editTxt').setAttribute('aria-label',STR.editT);
  $('#brand').textContent=STR.app;toastRegion();
  $('#backb').innerHTML=icon('back',20);$('#backb').setAttribute('aria-label',STR.back);$('#backb').title=STR.back;
  $('#upb').innerHTML=icon('up',20);$('#upb').setAttribute('aria-label',STR.up);$('#upb').title=STR.up;
  document.documentElement.classList.toggle('rvnav',rvNavOn());
  if(FLAGS.test){$('#testflag').textContent=STR.testShort;$('#testflag').title=STR.testFlag;$('#testflag').classList.remove('hidden');document.documentElement.classList.add('test');}
}
const navOf=r=>({concept:'map',x:'map',colours:'settings',day:'scene',calib:'studio',step:'progress',card:'cards',deck:'today',rcard:'review',rtour:'review',updates:'review'}[r.name]||r.name);
function syncShell(){
  $$('#nav [data-nav]').forEach(b=>{if(b.dataset.nav===navOf(ROUTE))b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
  const cr=ROUTE.crumbs||[{label:STR.nav[navOf(ROUTE)]||STR.app}];
  $('#crumbs').innerHTML=cr.map((c,i)=>i<cr.length-1?`<button type="button" data-go="${esc(c.hash)}">${esc(c.label)}</button><span aria-hidden="true">›</span>`:`<b>${esc(c.label)}</b>`).join('');
  const home=!upOf(ROUTE);$('#upb').classList.toggle('hidden',home);$('#backb').classList.toggle('hidden',home);   // no Back/Up at home (Back there would arm "leave")
  document.title=cr[cr.length-1].label+' · '+STR.app;
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
  syncShell();if(FLAGS.test)testBanner();
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
    const n=e.target.closest('[data-nav]');if(n){go(n.dataset.nav);return;}
    const g=e.target.closest('[data-go]');if(g){go(g.dataset.go);return;}
    if(e.target.closest('#brand')){go(CONFIG.home);return;}
    if(e.target.closest('#backb')){goBack();return;}
    if(e.target.closest('#upb')){goUp();return;}
  });
  $('#editClose').onclick=()=>$('#editdlg').close();
  $('#editCopy').onclick=async()=>{try{await navigator.clipboard.writeText($('#editTxt').value);$('#editMsg').textContent=STR.copied;}catch(_){$('#editTxt').select();$('#editMsg').textContent=STR.copyFail;}};
  /* desktop keys (§8a rule 5): / search · Esc back (or close) */
  document.addEventListener('keydown',e=>{
    if(e.target.matches('input,textarea,select')){if(e.key==='Escape')e.target.blur();return;}
    if(e.key==='/'){const q=$('#bmq');if(q){e.preventDefault();q.focus();}}
    else if(e.key==='Escape'&&!$('dialog[open]')&&upOf(ROUTE)){goBack();}
  });
}
