/* Biology Studio — 3D viewer screen: #scene (list) · #scene=<id>&day=<d> · #day=<d>. Owner docs: build/design-plan.md §2 (3D viewer row), §4.2, §7;
   docs/scene-spec.md (format). The three.js side is src/js/14-scene3d.mjs, loaded only when a scene opens (first load stays light, H8).
   Layouts by class (C13): phone = canvas on top + controls in a bottom sheet (tabs) · phone landscape = full-height canvas │ side strip ·
   tablet portrait = canvas + bottom panel · tablet landscape + desktop = canvas │ side panel (all sections, hover labels, keys).
   Always on the stage (B2, H4): day/stage/size stamp, scale bar, axis gizmo, disclaimers. Rotating keeps day, camera, cut and tab (one engine, one canvas).
   EDIT: words in STR.vw; settings in CONFIG.viewer; scene data in content/<book>/scenes/. */
'use strict';
if(new URLSearchParams(location.search).has('still'))document.documentElement.classList.add('still');   // tools/stills: the stage alone
const SC={idx:null,idxP:null,err:null,files:{},loaded:{},viewing:null,eng:null,engP:null,engErr:null,canvas:null,ro:null,st:{},tab:'layers',labels:true,
  playing:0,lbl:[],blocked:[],ptr:new Map(),hover:null,meas:null,ready:false};

/* ---------- data ---------- */
function scIndexLoad(){if(!SC.idxP)SC.idxP=fetch(CONFIG.viewer.scenesUrl+'index.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(r.status);return r.json();})
  .then(j=>{SC.idx=j;dlog('viewer','index',j.scenes.length);return j;}).catch(e=>{SC.err=e.message;});return SC.idxP;}
function scFile(id){if(!SC.files[id])SC.files[id]=fetch(CONFIG.viewer.scenesUrl+encodeURIComponent(id)+'.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(STR.vw.noScene(id));return r.json();}).then(S=>(SC.loaded[id]=S));SC.files[id].catch(()=>{delete SC.files[id];});return SC.files[id];}
const scenesFor=cid=>SC.idx?SC.idx.scenes.filter(s=>s.cards.includes(cid)):[];
function scEngine(){if(!SC.engP)SC.engP=import(new URL(CONFIG.viewer.engine+'?v='+APP.v,document.baseURI).href);return SC.engP;}
const motionReduced=()=>{const m=state&&state.settings.motion||'system';return m==='reduce'||(m==='system'&&matchMedia('(prefers-reduced-motion: reduce)').matches);};
const fmtDay=d=>Math.abs(d-Math.round(d))<0.05?String(Math.round(d)):d.toFixed(1);

/* ---------- screens ---------- */
SCREENS.scene=function(v){
  if(!ROUTE.id){scStop();return scList(v);}
  const id=ROUTE.id,meta=SC.idx&&SC.idx.scenes.find(s=>s.id===id),S=SC.loaded[id];
  ROUTE.crumbs=[{label:STR.nav.scene,hash:'scene'},{label:S?S.title:meta?meta.title:id}];
  if(!S){v.innerHTML=`<p class="mut" role="status">${esc(STR.vw.loading)}</p>`;
    scFile(id).then(()=>{if(ROUTE.name==='scene'&&ROUTE.id===id)render();})
      .catch(e=>{if(ROUTE.name==='scene'&&ROUTE.id===id){view().innerHTML=`<div class="card"><h1>${esc(STR.vw.title)}</h1><p>${esc(e.message)}</p><button type="button" class="btn" data-go="scene">${esc(STR.vw.all)}</button></div>`;}});return;}
  if(SC.viewing&&SC.viewing!==id)scStop();SC.viewing=id;
  scViewer(v,S);
};
SCREENS.day=function(){scIndexLoad().then(()=>{const d=+ROUTE.day,s=SC.idx&&SC.idx.scenes.find(x=>d>=x.days[0]&&d<=x.days[1]);
  go(s?{name:'scene',id:s.id,day:d}:{name:'scene'},{replace:true});});view().innerHTML=`<p class="mut" role="status">${esc(STR.vw.loading)}</p>`;ROUTE.crumbs=[{label:STR.nav.scene}];};

function scList(v){
  ROUTE.crumbs=[{label:STR.nav.scene}];
  if(!SC.idx){v.innerHTML=`<h1>${esc(STR.vw.listTitle)}</h1><p class="mut" role="status">${esc(SC.err?STR.vw.loadFail+' ('+SC.err+')':STR.vw.loading)}</p>`;if(!SC.err)scIndexLoad().then(()=>{if(ROUTE.name==='scene'&&!ROUTE.id)render();});return;}
  v.innerHTML=`<h1>${esc(STR.vw.listTitle)}</h1><p class="mut" style="max-width:var(--measure)">${esc(STR.vw.listLead)}</p>
  <div class="vw-list">${SC.idx.scenes.map(s=>`<article class="card vw-item"><div class="row"><span class="mono mut">${esc(s.id)}</span><span class="sp"></span>${editBtn('scene',s.id,CONFIG.viewer.scenesUrl+s.id+'.json')}</div>
    <h2>${esc(s.title)}</h2><p class="sm">${esc(s.summary)}</p><p class="xs mut">${esc(STR.vw.daysRange(s.days))} · ${s.cards.map(esc).join(' · ')}</p>
    <button type="button" class="btn pri" data-go="scene=${esc(s.id)}">${esc(STR.vw.open)}</button></article>`).join('')}</div>`;
}

/* ---------- the viewer ---------- */
function scViewer(v,S){
  const st=SC.st[S.id]||(SC.st[S.id]={});
  if(ROUTE.day!=null&&isFinite(+ROUTE.day))st.day=+ROUTE.day;
  if(st.day==null)st.day=S.start_day??S.days[0].day;
  const K=S.days,d0=K[0].day,d1=K[K.length-1].day,lay=S.layers;
  const tok=t=>['epi','hypo','ecto','meso','endo','crest','ctx'].includes(t)?'L-'+t:t==='accent'?'L-acc':'L-none';
  const on=id=>st.layersOn?st.layersOn[id]!==false:(lay.find(l=>l.id===id)||{}).on!==false;
  const cut=st.cut||S.cut,dbg=dbgOn('viewer');
  const facts=S.facts.map(f=>`<li><span>${esc(f.text)}</span> <span class="xs mut">[${esc(f.cite)}]</span> <b class="mark" title="${esc(STR.marks[f.mark]||'')}">${esc(f.mark)}</b></li>`).join('');
  v.innerHTML=`<div class="vw" id="vw" data-id="${esc(S.id)}" data-tab="${esc(SC.tab)}">
  <section class="vw-stage stage-dark" id="vwStage" tabindex="0" aria-label="${esc(STR.vw.stageLabel(S.title))}" aria-describedby="vwLblList">
    <div class="vw-cv" id="vwCv"></div>
    <svg class="vw-lead" id="vwLead" aria-hidden="true"></svg><div class="vw-lbls" id="vwLbls" aria-hidden="true"></div>
    <div class="vw-stamp" id="vwStamp" role="status" aria-live="polite"></div>
    <div class="vw-disc" id="vwDisc"><button type="button" class="vw-dbtn" data-vw="disc" aria-expanded="${!!SC.discOpen}" aria-controls="vwDiscL">ⓘ ${esc(STR.vw.discLine(S.disclaimers))}</button>
      <ul id="vwDiscL">${S.disclaimers.map(d=>`<li>${esc(d)}</li>`).join('')}</ul></div>
    <canvas class="vw-giz" id="vwGiz" width="88" height="88" role="img" aria-label="${esc(STR.vw.gizmo)}"></canvas>
    <div class="vw-scale" id="vwScale" aria-hidden="true"><i></i><span></span></div>
    <p class="vw-msg" id="vwMsg" role="status">${esc(STR.vw.loading3d)}</p>
  </section>
  <section class="vw-panel" aria-label="${esc(STR.vw.controls)}">
    <div class="vw-head"><div class="row"><span class="mono mut">${esc(S.id)} · v${S.version}</span><span class="sp"></span>${editBtn('scene',S.id,CONFIG.viewer.scenesUrl+S.id+'.json')}</div>
      <h1 id="cpT" tabindex="-1">${esc(S.title)}</h1></div>
    <div class="vw-day" role="group" aria-label="${esc(STR.vw.dayGroup)}">
      <button type="button" class="btn icon" data-vw="dprev" aria-label="${esc(STR.vw.dayPrev)}" title="${esc(STR.vw.dayPrev)} ( [ )">${icon('back',20)}</button>
      <label class="vw-range"><span class="sr">${esc(STR.vw.day)}</span><input type="range" id="vwDay" min="${d0}" max="${d1}" step="0.1" value="${st.day}"></label>
      <button type="button" class="btn icon" data-vw="dnext" aria-label="${esc(STR.vw.dayNext)}" title="${esc(STR.vw.dayNext)} ( ] )">${icon('fwd',20)}</button>
      <button type="button" class="btn icon" data-vw="play" id="vwPlay" aria-label="${esc(STR.vw.play)}" title="${esc(STR.vw.play)} (Space)">${icon('play',20)}</button>
    </div>
    <div class="vw-keys" aria-hidden="true">${K.map(k=>`<span data-d="${k.day}" style="left:${(k.day-d0)/((d1-d0)||1)*100}%">${esc(STR.vw.dayShort(k.day))}</span>`).join('')}</div>
    <div class="seg vw-tabs" role="group" aria-label="${esc(STR.vw.sections)}">${['layers','cut','view','about'].concat(dbg?['debug']:[]).map(t=>`<button type="button" data-vw="tab" data-t="${t}" aria-pressed="${SC.tab===t}">${esc(STR.vw.tabs[t])}</button>`).join('')}</div>
    <div class="vw-sec" data-sec="layers"><h2 class="vw-h">${esc(STR.vw.heads.layers)}</h2><div class="vw-tg">${lay.map(l=>`<button type="button" class="vw-t" data-vw="layer" data-l="${esc(l.id)}" aria-pressed="${on(l.id)}"><span class="sw ${tok(l.token)}" aria-hidden="true"></span><span>${esc(l.label)}</span></button>`).join('')}</div></div>
    <div class="vw-sec" data-sec="cut"><h2 class="vw-h">${esc(STR.vw.heads.cut)}</h2>
      <div class="vw-tg"><button type="button" class="vw-t" data-vw="labels" aria-pressed="${SC.labels}"><span>${esc(STR.vw.labels)}</span></button>
      <button type="button" class="vw-t" data-vw="cut" aria-pressed="${!!cut.on}"><span>${esc(STR.vw.cut)}</span></button></div>
      <div class="seg" role="group" aria-label="${esc(STR.vw.cutAxis)}">${['x','y'].map(a=>`<button type="button" data-vw="axis" data-a="${a}" aria-pressed="${cut.axis===a}">${esc(STR.vw.cutAxes[a])}</button>`).join('')}</div>
      <label class="vw-range wide"><span class="sm">${esc(STR.vw.cutAt)}</span><input type="range" id="vwCut" min="-0.9" max="0.9" step="0.05" value="${cut.at}" aria-valuetext="${esc(STR.vw.cutText(cut.axis,cut.at))}" ${cut.on?'':'disabled'}></label></div>
    <div class="vw-sec" data-sec="view"><h2 class="vw-h">${esc(STR.vw.heads.view)}</h2><div class="vw-tg">${Object.keys(STR.vw.views).map(k=>`<button type="button" class="vw-t" data-vw="view" data-v="${k}"><span>${esc(STR.vw.views[k])}</span></button>`).join('')}
      <button type="button" class="vw-t" data-vw="zin" aria-label="${esc(STR.vw.zoomIn)}"><span>＋ ${esc(STR.vw.zoom)}</span></button><button type="button" class="vw-t" data-vw="zout" aria-label="${esc(STR.vw.zoomOut)}"><span>－ ${esc(STR.vw.zoom)}</span></button></div>
      <p class="xs mut vw-hint">${esc(DEV.input==='in-mouse'?STR.vw.hintMouse:STR.vw.hintTouch)}</p></div>
    <div class="vw-sec" data-sec="about"><h2 class="vw-h">${esc(STR.vw.heads.about)}</h2><p class="sm">${esc(S.summary)}</p><ul class="vw-facts sm">${facts}</ul>
      ${S.terms&&S.terms.length?`<h3 class="sm">${esc(STR.vw.termsT)}</h3><dl class="vw-terms sm">${S.terms.map(t=>`<dt>${esc(t.term)}</dt><dd>${esc(t.text)}</dd>`).join('')}</dl>`:''}
      <h3 class="sm">${esc(STR.vw.discT)}</h3><ul class="vw-facts xs mut">${S.disclaimers.map(d=>`<li>${esc(d)}</li>`).join('')}</ul>
      <p class="xs mut">${esc(STR.vw.cardsT)} ${S.cards.map(c=>`<button type="button" class="lk" data-go="concept=${esc(c)}">${esc(c)}</button>`).join(' ')}</p>
      <p class="xs mut">${esc(STR.vw.marksKey)}</p><p class="xs mut" id="vwTech"></p></div>
    ${dbg?`<div class="vw-sec" data-sec="debug"><h2 class="vw-h">${esc(STR.vw.heads.debug)}</h2><p class="xs mut">${esc(STR.vw.measHint)}</p>
      <div class="row"><button type="button" class="btn" data-vw="measure" id="vwMeas">${esc(STR.vw.measure)}</button><button type="button" class="btn" data-vw="dbgbox">${esc(STR.vw.boxes)}</button></div>
      <textarea id="vwMeasOut" readonly aria-label="${esc(STR.vw.measOut)}" rows="8"></textarea><div class="row"><button type="button" class="btn" data-vw="mcopy">${esc(STR.copy)}</button><span class="sm mut" id="vwMeasMsg" role="status"></span></div></div>`:''}
    <p class="sr" id="vwLblList"></p>
  </section></div>`;
  scMount(S,st);
}

/* one engine + one canvas for the whole session; a re-render moves the canvas into the new stage (rotate keeps everything) */
function scMount(S,st){
  const stage=$('#vwStage'),host=$('#vwCv');SC.ready=false;window.VW_READY=false;
  if(!SC.canvas){SC.canvas=document.createElement('canvas');SC.canvas.className='vw-canvas';SC.canvas.setAttribute('aria-hidden','true');scPointer(SC.canvas);}
  host.appendChild(SC.canvas);scDay(st.day,true);
  scEngine().then(mod=>{
    if(!$('#vwStage'))return;
    SC.mod=mod;   // stamp works even without WebGL (G-Eng)
    if(!SC.eng){const e=mod.createViewer(SC.canvas,()=>$('#vwStage'),{dprCap:CONFIG.viewer.dprCap,still:document.documentElement.classList.contains('still')});
      if(!e.ok){SC.engErr=e.err||'WebGL';throw new Error(SC.engErr);}SC.eng=e;}
    const E=SC.eng;E.onFrame(scOverlay);
    if(SC.cur!==S.id){E.setScene(S,{day:st.day,layersOn:st.layersOn,cut:st.cut,az:st.az,el:st.el,zoom:st.zoom});SC.cur=S.id;}else{E.setTokens();if(Math.abs(E.state().day-st.day)>1e-6)E.setDay(st.day);}
    if(dbgOn('viewer')&&S.debug!==true)E.setDebug(!!SC.dbgBoxes);
    if(SC.ro)SC.ro.disconnect();SC.ro=new ResizeObserver(()=>{const r=host.getBoundingClientRect();E.resize(r.width,r.height);});SC.ro.observe(host);
    const r=host.getBoundingClientRect();E.resize(r.width,r.height);
    $('#vwMsg').classList.add('hidden');$('#vwTech').textContent=STR.vw.tech(mod.REVISION,E.gpu());
    scLabelsDom(S);SC.ready=true;scDay(SC.st[S.id].day,true);requestAnimationFrame(()=>requestAnimationFrame(()=>{scOverlay();window.VW_READY=true;}));
  }).catch(e=>{console.error(e);scDay(SC.st[S.id].day,true);const m=$('#vwMsg');if(m){m.textContent=STR.vw.noGL+' ('+e.message+')';m.classList.remove('hidden');}});
}
function scSave(){const S=scCur();if(!S||!SC.eng)return;Object.assign(SC.st[S.id],SC.eng.state());}
function scCur(){const id=ROUTE.name==='scene'&&ROUTE.id;return id?SC.loaded[id]:null;}

/* day: stamp, slider, address (replaceState: scrubbing never floods history) */
function scDay(d,quiet){const S=scCur();if(!S)return;const K=S.days;d=Math.max(K[0].day,Math.min(K[K.length-1].day,Math.round(d*10)/10));
  SC.st[S.id].day=d;const sl=$('#vwDay');if(sl&&+sl.value!==d)sl.value=d;
  const p=(SC.mod||{}).stampOf?SC.mod.stampOf(S,d):null,stp=$('#vwStamp');
  if(p&&stp){const html=`<b>${esc(STR.vw.dayLong(p.day))}</b> · ${esc(p.stage)} · ${esc(p.size)}${p.mark==='≈'?' <span class="xs">'+esc(STR.approx)+'</span>':''}`;
    if(stp.innerHTML!==html)stp.innerHTML=html;   // write only on change: the live region speaks once per real change (G-A11y)
    if(sl)sl.setAttribute('aria-valuetext',STR.vw.dayLong(p.day)+', '+p.stage+', '+p.size);}
  else if(stp&&!p){stp.textContent=STR.vw.dayLong(Math.round(d));}
  $$('.vw-keys span').forEach(b=>b.classList.toggle('on',Math.abs(+b.dataset.d-d)<0.05));
  if(!quiet&&SC.eng)SC.eng.setDay(d);
  const now=parseHash(location.hash);if(now.name!=='scene'||now.id!==S.id)return;   // the user has moved on (Back, nav): never rewrite their entry (G-Eng)
  ROUTE.day=d;const h='#scene='+S.id+'&day='+fmtDay(d);if(location.hash!==h)history.replaceState(history.state,'',h);
  if(state){state.last.route=h.slice(1);clearTimeout(SC.saveT);SC.saveT=setTimeout(stSave,800);}
}

/* ---------- overlay: labels on structures (D8), stamp, scale bar, gizmo ---------- */
function scLabelsDom(S){
  const box=$('#vwLbls');if(!box)return;const items=[];
  const tok=id=>{const l=S.layers.find(x=>x.id===id);return l?l.token:'guide';};
  const cls=t=>['epi','hypo','ecto','meso','endo','crest','ctx'].includes(t)?'L-'+t:t==='accent'?'L-acc':'L-none';
  S.labels.forEach((l,i)=>items.push({k:'l'+i,at:l.at||l.layer,layer:l.layer,text:l.text,days:l.days,pri:l.priority||5,sw:tok(l.layer)==='guide'?'':cls(tok(l.layer))}));
  S.parts.filter(p=>p.kind==='axes').forEach(p=>Object.keys(STR.vw.axes).forEach(a=>items.push({k:'axis-'+a,at:'axis-'+a,layer:p.layer,text:STR.vw.axes[a],axis:true,pri:3})));
  S.parts.filter(p=>p.kind==='planes').forEach(p=>p.planes.forEach(pl=>items.push({k:'plane-'+pl.id,at:'plane-'+pl.id,layer:pl.layer,text:(S.layers.find(x=>x.id===pl.layer)||{}).label||pl.id,pri:4})));
  box.innerHTML=items.map(it=>`<span class="vw-lb${it.axis?' ax':''}" data-k="${it.k}">${it.sw?`<i class="sw ${it.sw}"></i>`:''}${esc(it.text)}</span>`).join('')+'<span class="vw-lb hov hidden" data-k="hover"></span>';
  SC.lbl=items;$$('.vw-lb',box).forEach(el=>{const it=items.find(x=>x.k===el.dataset.k);if(it){it.el=el;}});SC.hoverEl=$('.vw-lb.hov',box);
}
function scOverlay(){
  const S=scCur(),E=SC.eng,stage=$('#vwStage');if(!S||!E||!stage||!SC.ready)return;
  const W=stage.clientWidth,H=stage.clientHeight,A=E.anchors(),st=E.state(),day=st.day;
  const rel=el=>{if(!el||el.offsetParent===null)return null;const a=el.getBoundingClientRect(),b=stage.getBoundingClientRect();return {l:a.left-b.left-4,t:a.top-b.top-4,r:a.right-b.left+4,b:a.bottom-b.top+4};};
  const blocked=['#vwStamp','#vwDisc','#vwGiz','#vwScale'].map(s=>rel($(s))).filter(Boolean),placed=[],lines=[],seen=[];
  const hit=(r)=>blocked.concat(placed).some(o=>r.l<o.r&&r.r>o.l&&r.t<o.b&&r.b>o.t);
  const items=SC.lbl.slice().sort((a,b)=>(a.pri||5)-(b.pri||5)||((A[a.at]&&A[b.at])?A[a.at].s.y-A[b.at].s.y:0));   // subject first: small screens drop context labels (G-Art)
  for(const it of items){const el=it.el;if(!el)continue;const a=A[it.at];
    const show=SC.labels&&a&&st.layersOn[it.layer]!==false&&(!it.days||(day>=it.days[0]-1e-6&&day<=it.days[1]+1e-6));
    if(!show){el.classList.add('hidden');continue;}el.classList.remove('hidden');
    const w=el.offsetWidth,h=el.offsetHeight,x=a.s.x,y=a.s.y,g=it.axis?6:16;
    const cand=it.axis?[[x-w/2,y-h/2],[x+g,y-h/2],[x-w-g,y-h/2],[x-w/2,y-h-g],[x-w/2,y+g]]:[[x+g,y-h-g],[x-w-g,y-h-g],[x+g,y+g],[x-w-g,y+g],[x+g,y-h/2],[x-w-g,y-h/2],[x-w/2,y-h-2*g],[x-w/2,y+2*g]];
    let ok=null;for(const[cx,cy]of cand){const r={l:cx,t:cy,r:cx+w,b:cy+h};if(r.l<4||r.t<4||r.r>W-4||r.b>H-4)continue;if(!hit(r)){ok=r;break;}}
    if(!ok){el.classList.add('hidden');continue;}
    placed.push({l:ok.l-3,t:ok.t-3,r:ok.r+3,b:ok.b+3});el.style.transform=`translate(${Math.round(ok.l)}px,${Math.round(ok.t)}px)`;seen.push(it.text);
    if(!it.axis){const ex=Math.max(ok.l,Math.min(x,ok.r)),ey=y<ok.t?ok.t:y>ok.b?ok.b:(ok.t+ok.b)/2;lines.push(`<line x1="${x.toFixed(1)}" y1="${y.toFixed(1)}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}"/><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3"/>`);}}
  const svg=$('#vwLead');if(svg){svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.innerHTML=lines.join('');}
  const ll=$('#vwLblList');if(ll){const t=STR.vw.viewText(st.az,st.el,st.cut)+' '+STR.vw.labelsShown(seen);if(ll.textContent!==t)ll.textContent=t;}
  /* scale bar: a round length ~ 60–130 px (B2) */
  const ppm=E.pxPerMm(),nice=CONFIG.viewer.scaleSteps.filter(m=>m*ppm<=130).pop()||CONFIG.viewer.scaleSteps[0],sb=$('#vwScale');
  if(sb){sb.querySelector('i').style.width=Math.round(nice*ppm)+'px';sb.querySelector('span').textContent=STR.vw.mm(nice);}
  scGizmo(E.axisDirs());
  if(dbgOn('viewer')){const i=E.info();DBG.viewer=`viewer ${S.id} · tris ${i.triangles} · calls ${i.calls} · ${i.px} @${i.dpr} · three r${SC.mod.REVISION}`;}
}
function scGizmo(D){
  const c=$('#vwGiz');if(!c)return;const dpr=Math.min(devicePixelRatio||1,2),S=88;if(c.width!==S*dpr){c.width=c.height=S*dpr;}
  const g=c.getContext('2d'),cs=getComputedStyle($('#vwStage')),ink=cs.getPropertyValue('--ink').trim(),mut=cs.getPropertyValue('--muted').trim();
  g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,S,S);g.fillStyle='rgba(20,22,26,.72)';g.beginPath();g.arc(44,44,43,0,7);g.fill();
  const R=27,ax=[['cranial','Cr','Cd'],['dorsal','D','V'],['left','L','R']].map(([k,p,n])=>({k,p,n,v:D[k]})).sort((a,b)=>a.v.z-b.v.z);
  g.lineCap='round';g.font='700 12px '+getComputedStyle(document.body).fontFamily;g.textAlign='center';g.textBaseline='middle';
  const marks=[],ends=[];
  for(const a of ax){const x=a.v.x*R,y=a.v.y*R,len=Math.hypot(a.v.x,a.v.y);
    if(len<0.45){ends.push(a);continue;}   // points at or away from the viewer: drawn as a ring (dot = toward you, cross = away) — no stacked letters (G-Art)
    g.strokeStyle=mut;g.lineWidth=2;g.beginPath();g.moveTo(44,44);g.lineTo(44-x,44-y);g.stroke();
    g.strokeStyle=ink;g.lineWidth=2.6;g.beginPath();g.moveTo(44,44);g.lineTo(44+x,44+y);g.stroke();
    marks.push({s:a.p,X:x,Y:y,col:ink,z:a.v.z},{s:a.n,X:-x,Y:-y,col:mut,z:-a.v.z});}
  const put=[];marks.sort((p,q)=>q.z-p.z).forEach(m=>{let ang=Math.atan2(m.Y,m.X),r=R*1.36,px,py,tries=0;
    do{px=44+Math.cos(ang)*r;py=44+Math.sin(ang)*r;ang+=0.42;tries++;}while(tries<14&&put.some(o=>Math.hypot(o[0]-px,o[1]-py)<16));
    put.push([px,py]);g.fillStyle=m.col;g.fillText(m.s,px,py);});
  for(const a of ends){const toward=a.v.z>0;
    g.strokeStyle=ink;g.lineWidth=1.6;g.beginPath();g.arc(44,44,7,0,7);g.stroke();
    if(toward){g.fillStyle=ink;g.beginPath();g.arc(44,44,2.2,0,7);g.fill();}else{g.beginPath();g.moveTo(39.5,39.5);g.lineTo(48.5,48.5);g.moveTo(48.5,39.5);g.lineTo(39.5,48.5);g.stroke();}
    g.fillStyle=ink;g.fillText(a.p,44+14,44+13);}
}

/* ---------- input: touch + mouse + keys (§2 rule 5) ---------- */
function scPointer(cv){
  cv.addEventListener('pointerdown',e=>{const st=$('#vwStage');if(st&&document.activeElement!==st)st.focus({preventScroll:true});cv.setPointerCapture(e.pointerId);SC.ptr.set(e.pointerId,{x:e.clientX,y:e.clientY});scStop();});
  cv.addEventListener('pointermove',e=>{const p=SC.ptr.get(e.pointerId),E=SC.eng;if(!E)return;
    if(!p){if(e.pointerType==='mouse')scHover(e);return;}
    if(SC.ptr.size===1){E.orbitBy(-(e.clientX-p.x)*0.45,(e.clientY-p.y)*0.45);}
    else if(SC.ptr.size===2){const o=[...SC.ptr.entries()].find(([k])=>k!==e.pointerId)[1],d0=Math.hypot(p.x-o.x,p.y-o.y),d1=Math.hypot(e.clientX-o.x,e.clientY-o.y);if(d0>10)E.zoomBy(d1/d0);}
    p.x=e.clientX;p.y=e.clientY;});
  const up=e=>{SC.ptr.delete(e.pointerId);scSave();};cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);
  cv.addEventListener('pointerleave',()=>{if(SC.hoverEl)SC.hoverEl.classList.add('hidden');});
  cv.addEventListener('wheel',e=>{if(!SC.eng)return;e.preventDefault();SC.eng.zoomBy(Math.exp(-e.deltaY*0.0015));clearTimeout(SC.wt);SC.wt=setTimeout(scSave,200);},{passive:false});
  cv.addEventListener('dblclick',()=>scView('reset'));
}
function scHover(e){const E=SC.eng,el=SC.hoverEl,S=scCur();if(!E||!el||!S)return;const r=SC.canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,id=E.pick(x,y);
  if(!id){el.classList.add('hidden');return;}const l=S.layers.find(q=>q.id===id);el.textContent=l?l.label:id;el.classList.remove('hidden');
  el.style.transform=`translate(${Math.round(Math.min(x+14,r.width-el.offsetWidth-6))}px,${Math.round(Math.max(6,y-el.offsetHeight-10))}px)`;}
function scView(k){const S=scCur(),E=SC.eng;if(!S||!E)return;const c=S.camera,V={three:[c.azimuth_deg,c.elevation_deg],top:[-90,89],side:[-90,0],cut:null,reset:[c.azimuth_deg,c.elevation_deg]}[k];
  let t=V;if(k==='cut'){const cu=E.state().cut;t=cu.axis==='x'?[180,20]:[-90,20];}
  const z=k==='reset'?1:null,s0=E.state();if(motionReduced()){E.view(t[0],t[1],z);scSave();return;}
  const a0=s0.az,e0=s0.el,da=((t[0]-a0+540)%360)-180,de=t[1]-e0,z0=s0.zoom,T0=performance.now(),dur=CONFIG.viewer.tweenMs;
  const step=n=>{const u=Math.min(1,(n-T0)/dur),k2=u*u*(3-2*u);E.view(a0+da*k2,e0+de*k2,z!=null?z0+(z-z0)*k2:null);if(u<1)requestAnimationFrame(step);else scSave();};requestAnimationFrame(step);}
function scPlay(){const S=scCur();if(!S)return;if(SC.playing){scStop();return;}const K=S.days,d1=K[K.length-1].day;let d=SC.st[S.id].day;if(d>=d1-0.05)d=K[0].day;
  const b=$('#vwPlay');if(b){b.innerHTML=icon('pause',20);b.setAttribute('aria-label',STR.vw.pause);}const stp=$('#vwStamp');if(stp)stp.setAttribute('aria-live','off');
  if(motionReduced()){scDay(K.find(k=>k.day>=d-0.01).day);SC.playing=setInterval(()=>{if(scCur()!==S){scStop();return;}const cur=SC.st[S.id].day,n=K.find(k=>k.day>cur+0.01);if(!n){scStop();return;}scDay(n.day);},CONFIG.viewer.stepMs);return;}
  let t0=performance.now(),dd=d;scDay(dd);const tick=n=>{if(!SC.playing)return;if(scCur()!==S){scStop();return;}dd=d+(n-t0)/1000/CONFIG.viewer.secPerDay;if(dd>=d1){scDay(d1);scStop();return;}scDay(dd);SC.playing=requestAnimationFrame(tick);};SC.playing=requestAnimationFrame(tick);}
function scStop(){if(!SC.playing)return;cancelAnimationFrame(SC.playing);clearInterval(SC.playing);SC.playing=0;const b=$('#vwPlay');if(b){b.innerHTML=icon('play',20);b.setAttribute('aria-label',STR.vw.play);}
  const stp=$('#vwStamp');if(stp){stp.setAttribute('aria-live','polite');const t=stp.innerHTML;stp.innerHTML='';requestAnimationFrame(()=>{stp.innerHTML=t;});}}   // one announcement when Play stops

document.addEventListener('click',e=>{
  const b=e.target.closest('[data-vw]');if(!b||!b.closest('#vw'))return;const S=scCur(),E=SC.eng,a=b.dataset.vw;if(!S)return;const st=SC.st[S.id];
  if(a==='disc'){const o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',o);SC.discOpen=o;scOverlay();return;}
  if(a==='tab'){SC.tab=b.dataset.t;$('#vw').dataset.tab=SC.tab;$$('.vw-tabs [data-t]').forEach(x=>x.setAttribute('aria-pressed',x===b));return;}
  if(a==='dprev'){scStop();scDay(Math.ceil(st.day-1-1e-6));return;} if(a==='dnext'){scStop();scDay(Math.floor(st.day+1+1e-6));return;}
  if(a==='play'){scPlay();return;}
  if(!E)return;
  if(a==='layer'){const on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on);E.setLayer(b.dataset.l,on);scSave();return;}
  if(a==='labels'){SC.labels=!SC.labels;b.setAttribute('aria-pressed',SC.labels);scOverlay();return;}
  if(a==='cut'){const on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on);E.setCut({on});$('#vwCut').disabled=!on;scSave();return;}
  if(a==='axis'){E.setCut({axis:b.dataset.a});const cs=$('#vwCut');if(cs)cs.setAttribute('aria-valuetext',STR.vw.cutText(b.dataset.a,+cs.value));$$('[data-vw=axis]').forEach(x=>x.setAttribute('aria-pressed',x===b));scSave();return;}
  if(a==='view'){scView(b.dataset.v);return;} if(a==='zin'){E.zoomBy(1.25);scSave();return;} if(a==='zout'){E.zoomBy(0.8);scSave();return;}
  if(a==='measure'){scMeasure();return;} if(a==='dbgbox'){SC.dbgBoxes=!SC.dbgBoxes;E.setDebug(SC.dbgBoxes);return;}
  if(a==='mcopy'){const t=$('#vwMeasOut');navigator.clipboard.writeText(t.value).then(()=>{$('#vwMeasMsg').textContent=STR.copied;},()=>{t.select();$('#vwMeasMsg').textContent=STR.copyFail;});}
});
document.addEventListener('input',e=>{if(e.target.id==='vwDay'){scStop();scDay(+e.target.value);}
  else if(e.target.id==='vwCut'&&SC.eng){SC.eng.setCut({at:+e.target.value});e.target.setAttribute('aria-valuetext',STR.vw.cutText(SC.eng.state().cut.axis,+e.target.value));scSave();}});
document.addEventListener('keydown',e=>{
  if(ROUTE.name!=='scene'||!ROUTE.id||!SC.eng||$('dialog[open]'))return;if(e.ctrlKey||e.metaKey||e.altKey)return;   // browser shortcuts stay the browser's (G-Eng)
  if(!e.target.closest||!e.target.closest('#vw')||e.target.matches('input:not([type=range]),textarea,select'))return;   // keys only while focus is in the viewer (WCAG 2.1.4)
  const k=e.key,S=scCur(),st=S&&SC.st[S.id],onStage=e.target.id==='vwStage';if(!st)return;
  if(k==='['){e.preventDefault();scStop();scDay(Math.ceil(st.day-1-1e-6));}else if(k===']'){e.preventDefault();scStop();scDay(Math.floor(st.day+1+1e-6));}
  else if(k===' '&&!e.target.matches('button')){e.preventDefault();scPlay();}
  else if(onStage&&k.startsWith('Arrow')){e.preventDefault();SC.eng.orbitBy(k==='ArrowLeft'?-10:k==='ArrowRight'?10:0,k==='ArrowUp'?8:k==='ArrowDown'?-8:0);scSave();}
  else if(k==='+'||k==='='){SC.eng.zoomBy(1.25);scSave();}else if(k==='-'){SC.eng.zoomBy(0.8);scSave();}else if(k==='0'){scView('reset');}
  else if(k==='l'||k==='L'){$('[data-vw=labels]')?.click();}else if(k==='c'||k==='C'){$('[data-vw=cut]')?.click();}
});

/* leaving a scene (Back, nav, a link) stops Play + Measure before the router reads the new address (listener added before routerStart) */
function scLeave(){const r=parseHash(location.hash);if(r.name==='scene'&&r.id===SC.viewing)return;scStop();if(SC.meas)SC.meas=2;if(SC.ro){SC.ro.disconnect();SC.ro=null;}}
addEventListener('hashchange',scLeave);addEventListener('popstate',scLeave);

/* ---------- ?debug=viewer › Measure fps (owner's phone → pipeline reference §2, H8, C4) ---------- */
async function scMeasure(){
  const E=SC.eng,S0=scCur(),out=$('#vwMeasOut'),btn=$('#vwMeas');if(!E||!SC.idx||SC.meas)return;SC.meas=1;btn.disabled=true;
  const keep=E.state(),lines=[],wait=ms=>new Promise(r=>setTimeout(r,ms)),C=CONFIG.viewer.measure,cp=$('[data-vw=mcopy]'),msg=$('#vwMeasMsg');
  const total=SC.idx.scenes.length+C.stress.length;let n=0;if(cp)cp.disabled=true;   // Copy only once the run is done
  const stat=ft=>{const s=ft.slice(C.warmFrames).sort((a,b)=>a-b);if(!s.length)return {avg:0,p5:0,n:0};const avg=1000*s.length/s.reduce((a,b)=>a+b,0),p95=s[Math.floor(s.length*0.95)];return {avg:+avg.toFixed(1),p5:+(1000/p95).toFixed(1),n:s.length};};
  const left=()=>SC.meas===2||scCur()!==S0;
  const phase=async(name)=>{if(left())throw new Error('left');n++;if(msg)msg.textContent=STR.vw.measStep(n,total);out.value=lines.concat(STR.vw.measuring(name)).join('\n');E.continuous(true,C.orbitDegPerS);await wait(C.phaseMs);const r=stat(E.frameTimes()),i=E.info();E.continuous(false);
    lines.push(`${name}: ${r.avg} fps avg · ${r.p5} fps (5th pct) · ${i.triangles} tris · ${i.calls} calls`);out.value=lines.join('\n');return r;};
  lines.push(`Biology Studio v${APP.v} · ${new Date().toISOString().slice(0,16)} · ${DEV.cls} ${DEV.input} · screen ${screen.width}×${screen.height} @${devicePixelRatio} · canvas ${E.info().px} (dpr cap ${CONFIG.viewer.dprCap})`,
    `GPU ${E.gpu()} · three r${SC.mod.REVISION}`,navigator.userAgent);
  let aborted=false;
  try{for(const s of SC.idx.scenes){const S=await scFile(s.id);E.setScene(S,{day:(S.days[0].day+S.days[S.days.length-1].day)/2});await wait(300);await phase(s.id);}
    E.setScene(S0,keep);for(const n of C.stress){E.setStress(n);await wait(300);await phase(S0.id+' + '+Math.round(n/1000)+'k stress');}}
  catch(e){aborted=true;lines.push(STR.vw.measStopped(e&&e.message||String(e)));out.value=lines.join('\n');console.error('[viewer] measure',e);}   // never stop silently
  finally{E.continuous(false);E.setStress(0);SC.meas=0;if(cp)cp.disabled=false;if(msg)msg.textContent=aborted?'':STR.vw.measReady;
    if(!aborted&&scCur()===S0){E.setScene(S0,keep);btn.disabled=false;lines.push(STR.vw.measDone);out.value=lines.join('\n');scOverlay();}
    else{SC.cur=null;if(scCur())render();}}   // moved on mid-run: the next mount rebuilds its own scene (G-Eng)
}
