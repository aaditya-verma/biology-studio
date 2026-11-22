/* Biology Studio — Settings (theme, motion (V1, H5), storage + save log, backup, Reviewer mode (H2), testing mode, version) and the Colour key (D-031 re-check on this screen).
   Owner doc: build/design-plan.md §4.4–4.5. EDIT: words in STR; colour tokens in src/css/app.css :root. */
'use strict';
SCREENS.settings=function(v){
  ROUTE.crumbs=[{label:STR.settingsTitle}];const th=state.settings.theme,L=slogRead().slice().reverse();
  const fmt=e=>new Date(e.t).toLocaleString([], {month:'short',day:'numeric',hour:'2-digit',minute:'2-digit',second:'2-digit'})+'  '+e.ev+(e.to!=null?' → rev '+e.to:'')+(e.err?'  '+e.err:'')+(e.why?'  '+e.why:'');
  v.innerHTML=`<h1>${esc(STR.settingsTitle)}</h1><div class="settings">
   <section class="card"><h2>${esc(STR.themeT)}</h2><div class="seg" role="group" aria-label="${esc(STR.themeT)}">${Object.entries(STR.themes).map(([k,l])=>`<button type="button" data-theme-set="${k}" aria-current="${th===k}">${esc(l)}</button>`).join('')}</div>
     <h3 class="sm" style="margin-top:12px">${esc(STR.motionT)}</h3><div class="seg" role="group" aria-label="${esc(STR.motionT)}">${Object.entries(STR.motions).map(([k,l])=>`<button type="button" data-motion-set="${k}" aria-current="${(state.settings.motion||'system')===k}">${esc(l)}</button>`).join('')}</div><p class="xs mut">${esc(STR.motionHint)}</p></section>
   <section class="card"><h2>${esc(STR.colourKeyT)}</h2><p class="sm mut">${esc(STR.colourKeyHint)}</p><div class="row" style="margin:8px 0">${['epi','hypo','ecto','meso','endo','crest','ctx'].map(k=>`<span class="sw L-${k}" title="${esc(STR.ckLayers[k])}"></span>`).join('')}</div>
     <button type="button" class="btn" data-go="colours">${esc(STR.colourKeyT)}</button></section>
   <section class="card"><h2>${esc(STR.storageT)}</h2><p class="sm">${STORE.mode==='idb'?esc(STR.saved)+' · IndexedDB '+esc(CONFIG.idb.name)+' · '+esc(STR.rev)+' '+STORE.rev:esc(STR.savedTest)}${STORE.err?` · <span class="bad">${esc(STORE.err)}</span>`:''}</p>
     <h3 class="sm">${esc(STR.saveLog)}</h3><div class="slog" tabindex="0">${L.length?L.map(e=>esc(fmt(e))).join('\n'):'—'}</div></section>
   <section class="card"><h2>${esc(STR.backupT)}</h2><p class="sm mut">${esc(STR.exportHint)}</p><div class="row">
     <button type="button" class="btn" data-act="export">${esc(STR.exportB)}</button>
     <label class="btn">${esc(STR.importB)}<input type="file" accept="application/json,.json" data-act="import" class="sr"></label></div></section>
   <section class="card"><h2>${esc(STR.rv.setT)}</h2><p class="sm mut">${esc(STR.rv.setHint)}</p><div class="row"><button type="button" class="btn" data-act="rvmode"${FLAGS.test?' disabled':''}>${esc(state.review.on?STR.rv.setOff:STR.rv.setOn)}</button><a class="btn" href="#review">${esc(STR.rv.title)}</a></div></section>
   <section class="card"><h2>${esc(STR.testT)}</h2><p class="sm mut">${esc(STR.testHint)}</p><button type="button" class="btn" data-act="testmode">${esc(FLAGS.test?STR.testOff:STR.testOn)}</button></section>
   <section class="card"><h2>${esc(STR.versionT)}</h2><p class="mono">${esc(appVerLine())}</p><p class="xs mut">${esc(DEV.cls)} · ${esc(DEV.input)} · ${innerWidth}×${innerHeight}</p></section>
  </div>`;
};
document.addEventListener('click',e=>{
  const t=e.target.closest('[data-theme-set]');if(t){setTheme(t.dataset.themeSet);return;}
  const mo=e.target.closest('[data-motion-set]');if(mo){state.settings.motion=mo.dataset.motionSet;state.settings.t=Date.now();stSave();render();return;}
  if(e.target.closest('[data-act=export]')){stExport();return;}
  if(e.target.closest('[data-act=rvmode]')){state.review.on=!state.review.on;state.review.t=Date.now();stSave();buildShell();render();return;}   // H2: show / hide the Review tab
  if(e.target.closest('[data-act=testmode]')){setFlags({test:!FLAGS.test,debug:new Set(FLAGS.test?[]:['test'])});location.reload();}
});
document.addEventListener('change',async e=>{if(!e.target.matches('[data-act=import]'))return;const f=e.target.files[0];if(!f)return;
  try{await stImport(f);toast(STR.importOk);render();}catch(err){toast(err.message||STR.importBad);}e.target.value='';});

/* Colour key — measured live on this screen (WCAG contrast of every D-031 token against every ladder level L0–L4, worst counts — U2) */
function cssRGB(c){const x=document.createElement('span');x.style.color=c;document.body.appendChild(x);const m=getComputedStyle(x).color.match(/[\d.]+/g).map(Number);x.remove();return m.slice(0,3);}
function relLum([r,g,b]){const f=v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;};return .2126*f(r)+.7152*f(g)+.0722*f(b);}
function contrast(a,b){const A=relLum(cssRGB(a)),B=relLum(cssRGB(b));return (Math.max(A,B)+.05)/(Math.min(A,B)+.05);}
function ckMeasure(){const cs=getComputedStyle(document.documentElement),g=k=>cs.getPropertyValue(k).trim(),bg=g('--bg'),out={};
  for(const k of ['epi','hypo','ecto','meso','endo','crest','ctx']){const fill=g('--g-'+k),edge=g('--g-'+k+'-edge'),text=g('--g-'+k+'-text');
    out[k]={fill,edge,text,cFill:contrast(fill,bg),cEdge:contrast(edge,bg),cText:contrast(text,fill)};}
  const dark=document.documentElement.dataset.theme==='dark',acc=dark?g('--accent-on-dark'):g('--accent'),sf=['--L0','--L1','--L2','--L3','--L4'].map(g);   // U2: every ladder level (D-077), worst one counts
  for(const k of Object.keys(out)){const r=out[k];r.cFill=Math.min(...sf.map(s=>contrast(r.fill,s)));r.cEdge=Math.min(...sf.map(s=>contrast(r.edge,s)));}   // worst of page, card, panel
  out.accent={fill:acc,cFill:Math.min(...sf.map(s=>contrast(acc,s))),cText:dark?contrast('#14161A',acc):contrast(g('--accent-ink'),acc),
    cAccentText:Math.min(...sf.map(s=>contrast(g('--accent-text'),s)))};
  out.ui={lineStrong:Math.min(...sf.map(s=>contrast(g('--line-strong'),s))),muted:Math.min(...sf.map(s=>contrast(g('--muted'),s))),heat3:contrast(g('--heat-ink-hi'),g('--heat3'))};
  out.bg=bg;return out;}
SCREENS.colours=function(v){
  ROUTE.crumbs=[{label:STR.settingsTitle,hash:'settings'},{label:STR.ckTitle}];const m=ckMeasure(),f=n=>n.toFixed(2);
  const okEdge=r=>r.cFill>=3.5||r.cEdge>=3.5;
  v.innerHTML=`<h1>${esc(STR.ckTitle)}</h1><p class="mut" style="max-width:var(--measure)">${esc(STR.ckLead)}</p>
  <div class="ckey">${['epi','hypo','ecto','meso','endo','crest','ctx'].map(k=>{const r=m[k];return `<div class="ck"><div class="fill L-${k}" style="color:var(--g-${k}-text)"><span style="background:var(--g-${k});padding:0 4px;border-radius:4px">${esc(STR.ckLayers[k])}</span></div>
     <div class="t"><b>--g-${k}</b> ${esc(r.fill)} · ${esc(STR.ckPattern[k])}<br>${esc(STR.ckFill)} ${f(r.cFill)}:1 · ${esc(STR.ckEdge)} ${f(r.cEdge)}:1 <span class="${okEdge(r)?'ok':'bad'}">${okEdge(r)?'✓':'✗'}</span><br>${esc(STR.ckText)} ${f(r.cText)}:1 <span class="${r.cText>=4.5?'ok':'bad'}">${r.cText>=4.5?'✓':'✗'}</span></div></div>`;}).join('')}
   <div class="ck"><div class="fill" style="background:var(--surface);color:var(--ink);justify-content:center;align-items:center"><span class="look" style="display:inline-block;width:34px;height:34px"></span></div>
     <div class="t"><b>--accent</b> ${esc(m.accent.fill)}<br>${esc(STR.ckAccent)}<br>${esc(STR.ckRing)} ${f(m.accent.cFill)}:1 <span class="${m.accent.cFill>=3?'ok':'bad'}">${m.accent.cFill>=3?'✓':'✗'}</span> · ${esc(STR.ckBtnText)} ${f(m.accent.cText)}:1 <span class="${m.accent.cText>=4.5?'ok':'bad'}">${m.accent.cText>=4.5?'✓':'✗'}</span></div></div></div>
  <p class="xs mut" style="margin-top:12px">background ${esc(m.bg)} · D-031 · ${editBtn('token','--g-*','src/css/app.css :root')}</p>`;
  window.CK_LAST=m;   // read by tools/layout-check (colour re-check)
};
