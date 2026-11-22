/* Biology Studio — 3D viewer screen: #scene (list) · #scene=<id>&day=<d> · #day=<d>. Owner docs: build/design-plan.md §2 (3D viewer row), §4.2, §7;
   docs/scene-spec.md (format). The three.js side is src/js/14-scene3d.mjs, loaded only when a scene opens (first load stays light, H8).
   Layouts by class (C13): phone = canvas on top + controls in a bottom sheet (tabs) · phone landscape = full-height canvas │ side strip ·
   tablet portrait = canvas + bottom panel · tablet landscape + desktop = canvas │ side panel (all sections, hover labels, keys).
   Always on the stage (B2, H4): day/stage/size stamp, scale bar, axis gizmo, disclaimers. Rotating keeps day, camera, cut and tab (one engine, one canvas).
   V2 drills (card-spec §2a, D-054): scViewer(…,{inline:true, drill}) = the same stage in drill mode — labels off, no day row, stamp masked for
   `day`, numbered pins for `label`, turn buttons; SC.drill holds it (set by 18-learn.js). Context loss: a message + Restart 3D (V1 note).
   V3 trace (D-075): SC.drill.trace = the tracer id → the engine draws the marked cell; the drill keeps a day row (◀ slider ▶ Play) over the path's
   days (SC.drill.d0…d1, steps = its key days; reduced motion = key to key); the cell keeps its label; its disclaimer goes first in the notes (B2).
   EDIT: words in STR.vw; settings in CONFIG.viewer; scene data in content/<book>/scenes/. */
'use strict';
if(new URLSearchParams(location.search).has('still'))document.documentElement.classList.add('still');   // tools/stills: the stage alone
const SC={idx:null,idxP:null,err:null,files:{},loaded:{},viewing:null,eng:null,engP:null,engErr:null,canvas:null,ro:null,st:{},tab:'layers',labels:true,
  playing:0,lbl:[],blocked:[],ptr:new Map(),hover:null,meas:null,ready:false,drill:null,pinFocus:-1};

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
/* o.inline (L1 card · Try it): the same stage (stamp, scale, gizmo, labels, disclaimers — B2, H4) with a compact panel
   (title, day row, Open full 3D) inside the card; one engine + canvas still (SC.inline = the card's scene id). */
function scViewer(v,S,o={}){
  const st=SC.st[S.id]||(SC.st[S.id]={});
  if(ROUTE.day!=null&&isFinite(+ROUTE.day))st.day=+ROUTE.day;
  if(st.day==null)st.day=S.start_day??S.days[0].day;
  const K=S.days,d0=K[0].day,d1=K[K.length-1].day,lay=S.layers;
  const tok=t=>['epi','hypo','ecto','meso','endo','crest','ctx'].includes(t)?'L-'+t:t==='accent'?'L-acc':'L-none';
  const on=id=>st.layersOn?st.layersOn[id]!==false:(lay.find(l=>l.id===id)||{}).on!==false;
  const cut=st.cut||S.cut,dbg=dbgOn('viewer'),tr=scTr(),disc=scDiscs(S),R0=tr?tr.d0:d0,R1=tr?tr.d1:d1;   // V3: a trace drill scrubs its path's days
  const facts=S.facts.map(f=>`<li><span>${esc(f.text)}</span> <span class="xs mut">[${esc(f.cite)}]</span> <b class="mark" title="${esc(STR.marks[f.mark]||'')}">${esc(f.mark)}</b></li>`).join('');
  v.innerHTML=`<div class="vw${o.inline?' inl':''}${o.drill?' drill dt-'+esc(o.drill.type):''}" id="vw" data-id="${esc(S.id)}" data-tab="${esc(SC.tab)}">
  <section class="vw-stage stage-dark" id="vwStage" tabindex="0" aria-label="${esc(STR.vw.stageLabel(S.title))}" aria-describedby="${o.drill?'lnQ ':''}vwLblList">
    <div class="vw-cv" id="vwCv"></div>
    <svg class="vw-lead" id="vwLead" aria-hidden="true"></svg><div class="vw-lbls" id="vwLbls" aria-hidden="true"></div>
    <div class="vw-stamp" id="vwStamp" role="status" aria-live="polite"></div>
    <div class="vw-disc" id="vwDisc"><button type="button" class="vw-dbtn" data-vw="disc" aria-expanded="${!!SC.discOpen}" aria-controls="vwDiscL">ⓘ <span class="d-long">${esc(STR.vw.discLine(disc))}</span><span class="d-short">${esc(STR.vw.discShort(disc))}</span></button>
      <ul id="vwDiscL">${disc.map(d=>`<li>${esc(d)}</li>`).join('')}</ul></div>
    <canvas class="vw-giz" id="vwGiz" width="88" height="88" role="img" aria-label="${esc(STR.vw.gizmo)}"></canvas>
    <div class="vw-scale" id="vwScale" aria-hidden="true"><i></i><span></span></div>
    <p class="vw-msg" id="vwMsg" role="status">${esc(STR.vw.loading3d)}</p>
    <div class="vw-lost hidden" id="vwLost" role="alert"><p>${esc(STR.vw.lost)}</p><button type="button" class="btn" data-vw="relaunch">${esc(STR.vw.relaunch)}</button></div>
  </section>
  <section class="vw-panel" aria-label="${esc(STR.vw.controls)}" data-cue>
    ${o.drill?`<div class="vw-head row"><h3 class="vw-it">${esc(STR.vw.drillT)}</h3><span class="sp"></span>${editBtn('scene',S.id,CONFIG.viewer.scenesUrl+S.id+'.json')}</div>
      <div class="vw-turn row" role="group" aria-label="${esc(STR.vw.turnGroup)}">${tr?`<span class="vw-dl xs" aria-hidden="true">${esc(STR.vw.turnShort)}</span>`:''}${[['l','back'],['r','fwd'],['u','up'],['d','up']].map(([d,ic])=>`<button type="button" class="btn icon${d==='d'?' ln-dn':''}" data-vw="turn" data-d="${d}" aria-label="${esc(STR.vw.turn[d])}" title="${esc(STR.vw.turn[d])}">${icon(ic,20)}</button>`).join('')}
      <button type="button" class="btn sm" data-vw="dreset">${esc(STR.vw.dReset)}</button></div>`
    :o.inline?`<div class="vw-head row"><h3 class="vw-it" title="${esc(S.id)} · v${S.version}">${esc(S.title)}</h3><span class="sp"></span>${editBtn('scene',S.id,CONFIG.viewer.scenesUrl+S.id+'.json')}</div>`
    :`<div class="vw-head"><div class="row"><span class="mono mut">${esc(S.id)} · v${S.version}</span><span class="sp"></span>${editBtn('scene',S.id,CONFIG.viewer.scenesUrl+S.id+'.json')}</div>
      <h1 id="cpT" tabindex="-1">${esc(S.title)}</h1></div>`}
    ${o.drill&&!tr?'':`<div class="vw-day" role="group" aria-label="${esc(STR.vw.dayGroup)}">${tr?`<span class="vw-dl xs" aria-hidden="true">${esc(STR.vw.day)}</span>`:''}
      <button type="button" class="btn icon" data-vw="dprev" aria-label="${esc(tr?STR.vw.trPrev:STR.vw.dayPrev)}" title="${esc(tr?STR.vw.trPrev:STR.vw.dayPrev)} ( [ )">${icon('back',20)}</button>
      <div class="vw-range"><label class="vw-rl"><span class="sr">${esc(STR.vw.day)}</span><input type="range" id="vwDay" min="${R0}" max="${R1}" step="0.1" value="${st.day}"></label>
      ${tr?'':`<div class="vw-keys" aria-hidden="true">${K.map(k=>{const q=(k.day-d0)/((d1-d0)||1);return `<span data-d="${k.day}" style="--p:${q.toFixed(4)}">${esc(STR.vw.dayShort(k.day))}</span>`;}).join('')}</div>`}</div>
      <button type="button" class="btn icon" data-vw="dnext" aria-label="${esc(tr?STR.vw.trNext:STR.vw.dayNext)}" title="${esc(tr?STR.vw.trNext:STR.vw.dayNext)} ( ] )">${icon('fwd',20)}</button>
      <button type="button" class="btn icon" data-vw="play" id="vwPlay" aria-label="${esc(STR.vw.play)}" title="${esc(STR.vw.play)} (Space)">${icon('play',20)}</button>
    </div>
    `}
    ${o.drill?'':o.inline?`<div class="row vw-inl-act"><button type="button" class="btn sm" data-go="scene=${esc(S.id)}&day=${esc(fmtDay(st.day))}" id="vwFull" title="${esc(STR.ln.openFull)}">${icon('scene',18)} <span class="vf-t">${esc(STR.ln.openFull)}</span></button><span class="xs mut">${esc(DEV.input==='in-mouse'?STR.vw.hintMouse:STR.vw.hintTouch)}</span></div>`:`
    <div class="seg vw-tabs" role="group" aria-label="${esc(STR.vw.sections)}">${['layers','cut','view','about'].concat(dbg?['debug']:[]).map(t=>`<button type="button" data-vw="tab" data-t="${t}" aria-current="${SC.tab===t}">${esc(STR.vw.tabs[t])}</button>`).join('')}</div>
    <div class="vw-sec" data-sec="layers"><h2 class="vw-h">${esc(STR.vw.heads.layers)}</h2><div class="vw-tg">${lay.filter(l=>!l.drill).map(l=>`<button type="button" class="vw-t" data-vw="layer" data-l="${esc(l.id)}" role="switch" aria-checked="${on(l.id)}"><span class="sw ${tok(l.token)}" aria-hidden="true"></span><span>${esc(l.label)}</span></button>`).join('')}</div></div>
    <div class="vw-sec" data-sec="cut"><h2 class="vw-h">${esc(STR.vw.heads.cut)}</h2>
      <div class="vw-tg"><button type="button" class="vw-t" data-vw="labels" role="switch" aria-checked="${SC.labels}"><span>${esc(STR.vw.labels)}</span></button>
      <button type="button" class="vw-t" data-vw="cut" role="switch" aria-checked="${!!cut.on}"><span>${esc(STR.vw.cut)}</span></button></div>
      <div class="seg" role="group" aria-label="${esc(STR.vw.cutAxis)}">${['x','y'].map(a=>`<button type="button" data-vw="axis" data-a="${a}" aria-current="${cut.axis===a}">${esc(STR.vw.cutAxes[a])}</button>`).join('')}</div>
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
      <div class="row"><button type="button" class="btn" data-vw="measure" id="vwMeas">${esc(STR.vw.measure)}</button><button type="button" class="btn" data-vw="dbgbox">${esc(STR.vw.boxes)}</button><button type="button" class="btn" data-vw="lose">${esc(STR.vw.lose)}</button></div>
      <textarea id="vwMeasOut" readonly aria-label="${esc(STR.vw.measOut)}" rows="8"></textarea><div class="row"><button type="button" class="btn" data-vw="mcopy">${esc(STR.copy)}</button><span class="sm mut" id="vwMeasMsg" role="status"></span></div></div>`:''}`}
    <p class="sr" id="vwLblList"></p>
  </section></div>`;
  scMount(S,st);
}

/* V3: the open trace drill (or null), the notes with a drawn tracer's disclaimer first (B2: the cell is drawn larger), the day steps */
const scTr=()=>SC.drill&&SC.drill.type==='trace'?SC.drill:null;
function scDiscs(S){const t=scTr(),p=t&&S.parts.find(x=>x.kind==='tracer'&&x.id===t.trace);return p&&p.disclaimer?[p.disclaimer,...S.disclaimers]:S.disclaimers;}
/* one engine + one canvas for the whole session; a re-render moves the canvas into the new stage (rotate keeps everything) */
function scMount(S,st){
  const stage=$('#vwStage'),host=$('#vwCv');SC.ready=false;window.VW_READY=false;
  if(!SC.canvas){SC.canvas=document.createElement('canvas');SC.canvas.className='vw-canvas';SC.canvas.setAttribute('aria-hidden','true');scPointer(SC.canvas);}
  host.appendChild(SC.canvas);scDay(st.day,true);setTimeout(vwKeysFit,0);
  scEngine().then(mod=>{
    if(!$('#vwStage'))return;
    SC.mod=mod;   // stamp works even without WebGL (G-Eng)
    if(!SC.eng){const e=mod.createViewer(SC.canvas,()=>$('#vwStage'),{dprCap:CONFIG.viewer.dprCap,still:document.documentElement.classList.contains('still'),
        onLost:()=>{dlog('viewer','context lost');clearTimeout(SC.lostT);SC.lostT=setTimeout(()=>{if(SC.eng&&SC.eng.lost())$('#vwLost')?.classList.remove('hidden');},CONFIG.viewer.lostMs);},   // Android may restore on its own: wait a moment
        onRestored:()=>{dlog('viewer','context restored');clearTimeout(SC.lostT);$('#vwLost')?.classList.add('hidden');scOverlay();}});
      if(!e.ok){SC.engErr=e.err||'WebGL';throw new Error(SC.engErr);}SC.eng=e;}
    const E=SC.eng;E.onFrame(scOverlay);E.setPan(SC.drill?0:scStart(S).pan);E.setShift(SC.drill?(SC.drill.shift??(SC.drill.type==='label'?CONFIG.viewer.drillShift:0)):scStart(S).shift);   // drills: the subject sits below the stamp + notes plate (G-Art); phone: the scene's start framing (L1F)
    const trace=scTr()?scTr().trace:null;   // V3: the marked cell only in its trace drill (never Try it)
    if(SC.cur!==S.id){E.setScene(S,{day:st.day,layersOn:st.layersOn,cut:st.cut,az:st.az,el:st.el,zoom:st.zoom??scStart(S).zoom,trace});SC.cur=S.id;}else{E.setTokens();if((E.state().trace||null)!==trace){E.setTrace(trace);dlog('viewer','trace',trace||'off');}if(Math.abs(E.state().day-st.day)>1e-6)E.setDay(st.day);}
    if(dbgOn('viewer')&&S.debug!==true)E.setDebug(!!SC.dbgBoxes);
    if(SC.ro)SC.ro.disconnect();SC.ro=new ResizeObserver(()=>{const r=host.getBoundingClientRect();E.resize(r.width,r.height);});SC.ro.observe(host);
    const r=host.getBoundingClientRect();E.resize(r.width,r.height);
    $('#vwMsg').classList.add('hidden');const tech=$('#vwTech');if(tech)tech.textContent=STR.vw.tech(mod.REVISION,E.gpu());   // the inline viewer (L1) has no About tab
    scLabelsDom(S);SC.ready=true;if(document.fonts&&document.fonts.status!=='loaded')document.fonts.ready.then(()=>{if(SC.ready)scOverlay();});   // L1F (G-Art): labels measured before the web font loads would grow afterwards — place them again
    scDay(SC.st[S.id].day,true);setTimeout(vwKeysFit,0);requestAnimationFrame(()=>requestAnimationFrame(()=>{if(SC.drill&&SC.drill.frame)scFrameDrill();scOverlay();requestAnimationFrame(()=>{scOverlay();window.VW_READY=true;});}));
  }).catch(e=>{console.error(e);scDay(SC.st[S.id].day,true);const m=$('#vwMsg');if(m){m.textContent=STR.vw.noGL+' ('+e.message+')';m.classList.remove('hidden');}});
}
/* L1F: start framing. Phone portrait uses the scene's camera.phone {zoom, shift} (scene-spec §3) while the learner has not zoomed; other classes 1 / 0 */
function scStart(S){const p=DEV.cls==='dev-p'&&S.camera&&S.camera.phone,c=(v,a,b)=>Math.max(a,Math.min(b,+v||0));return p?{zoom:c(p.zoom||1,1,4),shift:c(p.shift,0,0.3),pan:c(p.pan,-0.3,0.3)}:{zoom:1,shift:0,pan:0};}
/* L1F (T8): a drill on a scene with a ruler opens with the embryo + the whole ruler clear of the stamp, notes plate, gizmo and scale bar
   (scene-spec §8a): zoom out if needed, then move the subject into the free band. Only while the view is still the drill's start view;
   the result becomes the drill's Start view (SC.frames keeps it per drill, so a re-render or rotate reuses it once the learner has turned). */
function scFrameDrill(){const E=SC.eng,d=SC.drill,stage=$('#vwStage');if(!E||!d||!stage)return;const memo=(SC.frames||(SC.frames={}))[d.key],st=E.state(),h=d.home;
  const atHome=Math.abs(st.az-h.az)<0.5&&Math.abs(st.el-h.el)<0.5&&Math.abs(st.zoom-(memo?memo.zoom:d.zoom0))<1e-3;
  if(!atHome){if(memo){d.shift=memo.shift;d.home={...h,zoom:memo.zoom};E.setShift(memo.shift);}return;}
  E.setShift(0);E.view(null,null,d.zoom0);let b=E.screenBox();
  if(d.trace&&b){const d0=st.day,P=[];for(const k of d.steps){E.setDay(k);const a=E.anchors(false)['tracer-'+d.trace];if(a)P.push(a.s);}E.setDay(d0);   // V3 (G-Art): frame the cell's whole path (every key day) + room around it, so its layers read
    const m=Math.max(CONFIG.viewer.frame.trace,0.14*Math.min(b.W,b.H));   /* margin from the short side (phone landscape is ~190 px tall) */if(P.length)b={...b,l:Math.min(...P.map(q=>q.x))-m,r:Math.max(...P.map(q=>q.x))+m,t:Math.min(...P.map(q=>q.y))-m,b:Math.max(...P.map(q=>q.y))+m};}
  if(!b||!b.W||!b.H)return;
  if(d.pins){const A=E.anchors(false),P=d.pins.map(p=>A[p.at]).filter(Boolean).map(a=>a.s),m=CONFIG.viewer.frame.pin;   // label drills: frame the pinned structures (+ room for their pins), not the whole cut face
    if(P.length)b={...b,l:Math.min(...P.map(q=>q.x))-m,r:Math.max(...P.map(q=>q.x))+m,t:Math.min(...P.map(q=>q.y))-m+CONFIG.viewer.frame.padTop,b:Math.max(...P.map(q=>q.y))+m-CONFIG.viewer.frame.pad};}
  const sr=stage.getBoundingClientRect(),rel=el=>{if(!el||el.offsetParent===null)return null;const a=el.getBoundingClientRect();return {t:a.top-sr.top-6,b:a.bottom-sr.top+6};};
  const ov=(d.trace?['#vwStamp','#vwDisc']:['#vwStamp','#vwDisc','#vwGiz','#vwScale']).map(x=>rel($(x))).filter(Boolean),H=b.H,W=b.W;   // V3 (G-Art): a trace frames by the full-width bands only — the gizmo and scale bar are corner boxes (phone landscape had a 40 px band); layout-check checks the cell stays clear of them
  const up=r=>(r.t+r.b)/2<H/2,top=Math.max(8,...ov.filter(up).map(r=>r.b)),bot=Math.min(H-8,...ov.filter(r=>!up(r)).map(r=>r.t));   // an overlay belongs to the band its middle is in
  const padT=d.trace?CONFIG.viewer.frame.pad:CONFIG.viewer.frame.padTop,padO=CONFIG.viewer.frame.pad,bw=b.r-b.l+2*padO,bh=b.b-b.t+padT+padO;
  const k=Math.min(d.trace?CONFIG.viewer.frame.traceMaxIn:CONFIG.viewer.frame.maxIn,(W-16)/bw,Math.max(40,bot-top)/bh),z=Math.max(0.35,b.zoom*k),y0=(0.5+b.shift)*H,cy=(b.t-padT+b.b+padO)/2,cy2=y0+(cy-y0)*(z/b.zoom);
  const sh=Math.max(-0.45,Math.min(0.45,b.shift+((top+bot)/2-cy2)/H));
  d.shift=sh;d.home={...h,zoom:z};SC.frames[d.key]={zoom:z,shift:sh};{const ks=Object.keys(SC.frames);if(ks.length>20)delete SC.frames[ks[0]];}   // keep the last 20 (G-Eng nit)
  E.setShift(sh);E.view(null,null,z);scSave();
  dlog('viewer','drill framed',d.key,'zoom',z.toFixed(2),'shift',sh.toFixed(2),'free',Math.round(top)+'–'+Math.round(bot));}
function scSave(){const S=scCur();if(!S||!SC.eng)return;const {trace,...st}=SC.eng.state();Object.assign(SC.st[S.id],st);}   // V3: the marked cell is the drill's, never saved into the scene's view (Try it)
function scCur(){const id=ROUTE.name==='scene'?ROUTE.id:ROUTE.name==='card'?SC.inline:null;return id?SC.loaded[id]||null:null;}

/* day: stamp, slider, address (replaceState: scrubbing never floods history) */
function scDay(d,quiet){const S=scCur();if(!S)return;const K=S.days,tr=scTr();d=Math.max(tr?tr.d0:K[0].day,Math.min(tr?tr.d1:K[K.length-1].day,Math.round(d*10)/10));   // a trace keeps its path's days (V3)
  SC.st[S.id].day=d;const sl=$('#vwDay');if(sl&&+sl.value!==d)sl.value=d;
  const p=(SC.mod||{}).stampOf?SC.mod.stampOf(S,d):null,stp=$('#vwStamp');
  if(SC.drill&&SC.drill.mask&&stp){const html=`<b>${esc(STR.vw.masked)}</b>`;if(stp.innerHTML!==html)stp.innerHTML=html;}   // day drill: the day is the question (D-054); scale bar stays
  else if(p&&stp){const html=`<b>${esc(STR.vw.dayLong(p.day))}</b> · ${esc(p.stage)} · ${esc(p.size)}${p.mark==='≈'?' <span class="xs">'+esc(STR.approx)+'</span>':''}`;
    if(stp.innerHTML!==html)stp.innerHTML=html;   // write only on change: the live region speaks once per real change (G-A11y)
    if(sl)sl.setAttribute('aria-valuetext',STR.vw.dayLong(p.day)+', '+p.stage+', '+p.size);}
  else if(stp&&!p){stp.textContent=STR.vw.dayLong(Math.round(d));}
  let kc=false;$$('.vw-keys span').forEach(b=>{const o=Math.abs(+b.dataset.d-d)<0.05;if(o!==b.classList.contains('on')){b.classList.toggle('on',o);kc=true;}});if(kc)vwKeysFit();   // re-fit only when the current label changes (Play calls this every frame)
  const fl=$('#vwFull');if(fl)fl.dataset.go='scene='+S.id+'&day='+fmtDay(d);   // Try it › Open full 3D keeps the day
  if(!quiet&&SC.eng)SC.eng.setDay(d);
  if(tr&&!quiet)dlog('viewer','trace',tr.trace,'day',d);   // V3 (I5)
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
  const pins=SC.drill&&SC.drill.pins||[];
  box.innerHTML=items.map(it=>`<span class="vw-lb${it.axis?' ax':''}" data-k="${it.k}">${it.sw?`<i class="sw ${it.sw}"></i>`:''}${esc(it.text)}</span>`).join('')+'<span class="vw-lb hov hidden" data-k="hover"></span>'
    +pins.map((p,i)=>`<span class="vw-pin hidden" data-pin="${i}">${p.n}</span>`).join('');
  SC.lbl=items;$$('.vw-lb',box).forEach(el=>{const it=items.find(x=>x.k===el.dataset.k);if(it){it.el=el;}});SC.hoverEl=$('.vw-lb.hov',box);
}
/* pin spots: offsets on a 10 px grid covering the whole stage, nearest first (a slight preference for above: the pin reads before the layer under it) */
function scPinGrid(W,H,min){const k=Math.round(W)+'x'+Math.round(H)+':'+min,c=SC.pinGrids||(SC.pinGrids={});if(c[k])return c[k];if(Object.keys(c).length>6)SC.pinGrids={};const g=[];
  for(let dx=-W;dx<=W;dx+=10)for(let dy=-H;dy<=H;dy+=10){const d=Math.hypot(dx,dy);if(d>=min)g.push([dx,dy,d+(dy>0?4:0)]);}g.sort((p,q)=>p[2]-q[2]);SC.pinGrids[k]=g;return g;}
function scOverlay(){
  const S=scCur(),E=SC.eng,stage=$('#vwStage');if(!S||!E||!stage||!SC.ready)return;
  const sp=$('#vwStamp');if(sp)stage.style.setProperty('--stamp-h',sp.offsetHeight+'px');   // the notes plate sits under the stamp's real height (a wrapped stamp never covers it — CI fonts, V2)
  const W=stage.clientWidth,H=stage.clientHeight,A=E.anchors(!SC.drill||SC.drill.labels),st=E.state(),day=st.day;   // occlusion raycasts only when labels can show (G-Eng)
  const rel=el=>{if(!el||el.offsetParent===null)return null;const a=el.getBoundingClientRect(),b=stage.getBoundingClientRect();return {l:a.left-b.left-4,t:a.top-b.top-4,r:a.right-b.left+4,b:a.bottom-b.top+4};};
  const blocked=['#vwStamp','#vwDisc','#vwGiz','#vwScale'].map(s=>rel($(s))).filter(Boolean),placed=[],lines=[],seen=[];
  const ov=(r,o)=>r.l<o.r&&r.r>o.l&&r.t<o.b&&r.b>o.t,hit=r=>blocked.some(o=>ov(r,o))||placed.some(o=>ov(r,o));
  const lblOn=SC.drill?SC.drill.labels:SC.labels&&!(SC.runOff&&ROUTE.name==='card'),segs=[];   // L1F (G-Learn): no Try it labels while a Check run is open — they would answer it
  /* leader lines never cross each other or another label (V1 note: phone landscape at 125 %) */
  const cross=(a,b,c,d)=>{const o=(p,q,r)=>Math.sign((q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x));return o(a,b,c)!==o(a,b,d)&&o(c,d,a)!==o(c,d,b);};
  const segHitsRect=(a,b,r)=>{const P=[{x:r.l,y:r.t},{x:r.r,y:r.t},{x:r.r,y:r.b},{x:r.l,y:r.b}];return [0,1,2,3].some(i=>cross(a,b,P[i],P[(i+1)%4]));};
  /* L1F: the axis arrows are obstacles — a label never sits on one (T7 phone note: "Primitive streak" on the cranial arrow) */
  const o0=A['axis-o'],arrows=[],inR=(p,r)=>p.x>r.l&&p.x<r.r&&p.y>r.t&&p.y<r.b;
  if(o0&&st.layersOn[o0.layer]!==false)for(const k of Object.keys(STR.vw.axes)){const t=A['axis-'+k];if(t)arrows.push([o0.s,{x:o0.s.x+(t.s.x-o0.s.x)/o0.len,y:o0.s.y+(t.s.y-o0.s.y)/o0.len}]);}
  const onArrow=r=>arrows.some(([p,q])=>segHitsRect(p,q,r)||inR(p,r)||inR(q,r));
  /* drill pins first: each in the first free spot around its structure — never under the stamp, notes plate, gizmo, scale bar or another pin (T8).
     Once a label drill is answered, each pin carries its structure's label right beside it: pin + label are placed as one box, before any other label. */
  const pinAt={},PZ=22,late=[];SC.lbl.forEach(it=>{it.done=null;if(it.el)delete it.el.dataset.pinno;});
  (SC.drill&&SC.drill.pins||[]).forEach((p,i)=>{const el=$(`.vw-pin[data-pin="${i}"]`),a=A[p.at];if(!el)return;
    if(!a){el.classList.add('hidden');return;}el.classList.remove('hidden');el.classList.toggle('on',SC.pinFocus===i);
    const lab=lblOn&&SC.lbl.find(it=>it.at===p.at&&it.el&&(!it.days||(day>=it.days[0]-1e-6&&day<=it.days[1]+1e-6)));
    if(lab)lab.el.classList.remove('hidden');const lw=lab?lab.el.offsetWidth+4:0,lh=lab?lab.el.offsetHeight:0,BW=PZ+lw,BH=Math.max(PZ,lh);
    const x=a.s.x,y=a.s.y,o=CONFIG.viewer.pinOffset;
    /* nearest free spot: pin centres on a 10 px grid around the structure (never on it), nearest first; the label goes right of the pin, or left of it */
    const grid=scPinGrid(W,H,o+PZ/2);   // nearest first, over the whole stage (cached per stage size — G-Eng)
    const free=(bw,bh)=>{let first=null;for(const[dx,dy]of grid){const cx=x+dx,cy=y+dy;for(const side of bw>PZ?['r','l']:['r']){const l=side==='r'?cx-PZ/2:cx-bw+PZ/2,t=cy-bh/2,r={l,t,r:l+bw,b:t+bh,side};
        if(r.l<4||r.t<4||r.r>W-4||r.b>H-4)continue;if(!first)first=r;if(hit(r)||onArrow(r))continue;const c={x:cx,y:cy};
        if(segs.some(([q0,q1])=>cross({x,y},c,q0,q1))||placed.some(q=>segHitsRect({x,y},c,q)))continue;return {r,first};}}return {r:null,first};};
    let f=free(BW,BH),both=!!(lab&&f.r);if(lab&&!f.r)f=free(PZ,PZ);   // no room for pin + label: the pin alone (its label then goes with the others)
    const bw=both?BW:PZ,bh=both?BH:PZ,ok=f.r||f.first||{l:Math.max(4,Math.min(W-bw-4,x+o)),t:Math.max(4,Math.min(H-bh-4,y-o-bh)),side:'r'};ok.r=ok.l+bw;ok.b=ok.t+bh;   // a pin always shows (it is the question)
    if(dbgOn('viewer')&&!f.r)dlog('viewer','pin',i+1,'had no free spot');
    const pl=ok.side==='l'?ok.r-PZ:ok.l,pt=ok.t+(bh-PZ)/2;placed.push({l:ok.l-3,t:ok.t-3,r:ok.r+3,b:ok.b+3});pinAt[p.at]={l:pl,t:pt,r:pl+PZ,b:pt+PZ};const c={x:pl+PZ/2,y:pt+PZ/2};segs.push([{x,y},c]);
    el.style.transform=`translate(${Math.round(pl)}px,${Math.round(pt)}px)`;lines.push(`<line x1="${x.toFixed(1)}" y1="${y.toFixed(1)}" x2="${c.x.toFixed(1)}" y2="${c.y.toFixed(1)}"/><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3"/>`);
    if(both){lab.el.style.transform=`translate(${Math.round(ok.side==='l'?ok.l:ok.l+PZ+4)}px,${Math.round(ok.t+(bh-lh)/2)}px)`;lab.done=SC.drill.key;seen.push(lab.text);}
    else if(lab)late.push({lab,n:i+1,c});});
  /* last resort (tight stages, 125 % text): a pinned label with no room beside its pin goes to the nearest free spot, carrying the pin's number */
  for(const {lab,n,c} of late){lab.el.dataset.pinno=n;const w=lab.el.offsetWidth,h=lab.el.offsetHeight;let r=null;
    for(const[dx,dy]of scPinGrid(W,H,0)){const q={l:c.x+dx-w/2,t:c.y+dy-h/2};q.r=q.l+w;q.b=q.t+h;if(q.l<4||q.t<4||q.r>W-4||q.b>H-4||hit(q)||onArrow(q)||segs.some(([p0,p1])=>segHitsRect(p0,p1,q)))continue;r=q;break;}
    if(!r){delete lab.el.dataset.pinno;continue;}   // still no room: the Check feedback names it (Pin n: …)
    placed.push({l:r.l-3,t:r.t-3,r:r.r+3,b:r.b+3});lab.el.style.transform=`translate(${Math.round(r.l)}px,${Math.round(r.t)}px)`;lab.done=SC.drill.key;seen.push(lab.text);}
  const pinned=it=>lblOn&&SC.drill&&pinAt[it.at];
  const items=SC.lbl.slice().sort((a,b)=>(pinned(b)?1:0)-(pinned(a)?1:0)||(a.pri||5)-(b.pri||5)||((A[a.at]&&A[b.at])?A[a.at].s.y-A[b.at].s.y:0));   // pinned structures first (answered label drill), then subject first: small screens drop context labels (G-Art)
  for(const it of items){const el=it.el;if(!el)continue;if(SC.drill&&it.done===SC.drill.key)continue;const a=A[it.at],pr=pinned(it);
    const guideLbl=(SC.drill||SC.runOff)&&(it.at==='ruler'||(!!a&&!!a.tracer));   // the ruler keeps its length label in a drill (G-Art: "1 mm" must read); the marked cell keeps "Marked cell" (V3, B3)
    const off=a&&(a.s.x<2||a.s.y<2||a.s.x>W-2||a.s.y>H-2);   // a structure off the stage gets no label (G-Art: no leader running off the edge)
    const inDays=!it.days||(day>=it.days[0]-1e-6&&day<=it.days[1]+1e-6);
    const show=pr?inDays:(lblOn||guideLbl)&&a&&!a.hid&&!off&&st.layersOn[it.layer]!==false&&inDays;   // a pinned structure's label shows beside its pin (its pin already points at it)
    if(!show){el.classList.add('hidden');continue;}el.classList.remove('hidden');
    const w=el.offsetWidth,h=el.offsetHeight,x=a?a.s.x:0,y=a?a.s.y:0,g=it.axis?6:16;
    const cand=pr?[[pr.r+4,pr.t+(PZ-h)/2],[pr.l-4-w,pr.t+(PZ-h)/2],[pr.l+PZ/2-w/2,pr.b+4],[pr.l+PZ/2-w/2,pr.t-h-4],[pr.r+4,pr.b+2],[pr.l-4-w,pr.b+2],[pr.r+4,pr.t-h-2],[pr.l-4-w,pr.t-h-2]]
      :it.axis?[[x-w/2,y-h/2],[x+g,y-h/2],[x-w-g,y-h/2],[x-w/2,y-h-g],[x-w/2,y+g]]:[1,2.2,3.6].flatMap(k=>{const G=g*k;return [[x+G,y-h-G],[x-w-G,y-h-G],[x+G,y+G],[x-w-G,y+G],[x+G,y-h/2],[x-w-G,y-h/2],[x-w/2,y-h-2*G],[x-w/2,y+2*G]];});   // a second, farther ring (L1F: arrows and pins take near spots)
    if(!it.axis&&!pr){const cl=v=>Math.max(4,Math.min(W-4-w,v));cand.push(...cand.map(([cx,cy])=>[cl(cx),cy]).filter(([cx],j)=>cx!==cand[j][0]));}   // L1F: a long label slides in from the stage edge instead of being dropped (phone 360 px)
    const lead=r=>{const ex=Math.max(r.l,Math.min(x,r.r)),ey=y<r.t?r.t:y>r.b?r.b:(r.t+r.b)/2;return [{x,y},{x:ex,y:ey}];};
    const tryAt=(list,withLead)=>{for(const[cx,cy]of list){const r={l:cx,t:cy,r:cx+w,b:cy+h};if(r.l<4||r.t<4||r.r>W-4||r.b>H-4)continue;if(hit(r))continue;
        if(!it.axis&&onArrow(r))continue;
        if(withLead){const [a1,b1]=lead(r);if(segs.some(([p,q])=>cross(a1,b1,p,q))||placed.some(o=>segHitsRect(a1,b1,o)))continue;}
        if(!it.axis&&segs.some(([p,q])=>segHitsRect(p,q,r)))continue;
        return r;}return null;};
    let ok=pr?tryAt(cand,false):tryAt(cand,!it.axis),led=!pr&&!it.axis;
    if(!ok&&pr&&a&&!off){const c2=[[x+g,y-h-g],[x-w-g,y-h-g],[x+g,y+g],[x-w-g,y+g],[x+g,y-h/2],[x-w-g,y-h/2]];ok=tryAt(c2,true);led=!!ok;}   // no room beside the pin: by its structure, with a leader
    if(!ok){el.classList.add('hidden');continue;}
    placed.push({l:ok.l-3,t:ok.t-3,r:ok.r+3,b:ok.b+3});el.style.transform=`translate(${Math.round(ok.l)}px,${Math.round(ok.t)}px)`;seen.push(it.text);
    if(led){const [p0,p1]=lead(ok),ex=p1.x,ey=p1.y;segs.push([p0,p1]);const cell=!!(a&&a.tracer),dl=Math.hypot(ex-x,ey-y)||1,sx=cell?x+(ex-x)*Math.min(1,CONFIG.viewer.frame.cellGap/dl):x,sy=cell?y+(ey-y)*Math.min(1,CONFIG.viewer.frame.cellGap/dl):y;   // V3: the leader stops at the marked cell's ring (no dot on it — G-Art)
      lines.push(`<line x1="${sx.toFixed(1)}" y1="${sy.toFixed(1)}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}"/>`+(cell?'':`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3"/>`));}}
  const svg=$('#vwLead');if(svg){svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.innerHTML=lines.join('');}
  const ll=$('#vwLblList');if(ll){const t=STR.vw.viewText(st.az,st.el,st.cut)+' '+STR.vw.labelsShown(seen);if(ll.textContent!==t)ll.textContent=t;}
  /* scale bar: a round length ~ 60–130 px (B2) */
  const dp=$('#vwDisc'),dr=dp&&dp.offsetParent!==null?dp.getBoundingClientRect():null,sr0=stage.getBoundingClientRect(),room=dr&&dr.bottom>sr0.bottom-60?Math.max(30,sr0.right-dr.right-40):130;   // L1F: a notes plate at the bottom leaves the bar this much room
  const ppm=E.pxPerMm(),nice=CONFIG.viewer.scaleSteps.filter(m=>m*ppm<=Math.min(130,room)).pop()||CONFIG.viewer.scaleSteps[0],sb=$('#vwScale');
  if(sb){sb.querySelector('i').style.width=Math.round(nice*ppm)+'px';sb.querySelector('span').textContent=STR.vw.mm(nice);}
  scGizmo(E.axisDirs());
  if(dbgOn('viewer')){const i=E.info(),tc=scTr()&&A['tracer-'+scTr().trace];DBG.viewer=`viewer ${S.id} · tris ${i.triangles} · calls ${i.calls} · ${i.px} @${i.dpr} · three r${SC.mod.REVISION}`+(tc?` · trace ${scTr().trace} d${fmtDay(day)} in ${tc.in}`:'');}   // V3: the marked cell's layer (I5)
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
  cv.addEventListener('dblclick',()=>{if(SC.drill&&SC.drill.home&&SC.eng){const h=SC.drill.home;SC.eng.view(h.az,h.el,h.zoom);scSave();return;}scView('reset');});   // in a drill: back to its start view (G-Eng)
}
function scHover(e){const E=SC.eng,el=SC.hoverEl,S=scCur();if(!E||!el||!S||SC.drill||(SC.runOff&&ROUTE.name==='card'))return;   // hover names a structure: never in a drill (it would answer it)
  const r=SC.canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,id=E.pick(x,y);
  if(!id){el.classList.add('hidden');return;}const l=S.layers.find(q=>q.id===id);el.textContent=l?l.label:id;el.classList.remove('hidden');
  el.style.transform=`translate(${Math.round(Math.min(x+14,r.width-el.offsetWidth-6))}px,${Math.round(Math.max(6,y-el.offsetHeight-10))}px)`;}
function scView(k){const S=scCur(),E=SC.eng;if(!S||!E)return;const c=S.camera,V={three:[c.azimuth_deg,c.elevation_deg],top:[-90,89],side:[-90,0],cut:null,reset:[c.azimuth_deg,c.elevation_deg]}[k];
  let t=V;if(k==='cut'){const cu=E.state().cut;t=cu.axis==='x'?[180,20]:[-90,20];}
  const z=k==='reset'?scStart(S).zoom:null,s0=E.state();if(motionReduced()){E.view(t[0],t[1],z);scSave();return;}
  const a0=s0.az,e0=s0.el,da=((t[0]-a0+540)%360)-180,de=t[1]-e0,z0=s0.zoom,T0=performance.now(),dur=CONFIG.viewer.tweenMs;
  const step=n=>{const u=Math.min(1,(n-T0)/dur),k2=u*u*(3-2*u);E.view(a0+da*k2,e0+de*k2,z!=null?z0+(z-z0)*k2:null);if(u<1)requestAnimationFrame(step);else scSave();};requestAnimationFrame(step);}
function scPlay(){const S=scCur();if(!S)return;if(SC.playing){scStop();return;}const tr=scTr(),K=tr?tr.steps.map(day=>({day})):S.days,d1=K[K.length-1].day;let d=SC.st[S.id].day;if(d>=d1-0.05)d=K[0].day;   // V3: a trace plays its path (reduced motion: path key to key)
  const b=$('#vwPlay');if(b){b.innerHTML=icon('pause',20);b.setAttribute('aria-label',STR.vw.pause);}const stp=$('#vwStamp');if(stp)stp.setAttribute('aria-live','off');
  if(motionReduced()){scDay(K.find(k=>k.day>=d-0.01).day);SC.playing=setInterval(()=>{if(scCur()!==S){scStop();return;}const cur=SC.st[S.id].day,n=K.find(k=>k.day>cur+0.01);if(!n){scStop();return;}scDay(n.day);},CONFIG.viewer.stepMs);return;}
  let t0=performance.now(),dd=d;scDay(dd);const tick=n=>{if(!SC.playing)return;if(scCur()!==S){scStop();return;}dd=d+(n-t0)/1000/CONFIG.viewer.secPerDay;if(dd>=d1){scDay(d1);scStop();return;}scDay(dd);SC.playing=requestAnimationFrame(tick);};SC.playing=requestAnimationFrame(tick);}
/* ◀ ▶ and [ ]: a whole day — in a trace drill, the previous / next key of the path (V3) */
function scStep(d,dir){const tr=scTr();if(!tr)return dir>0?Math.floor(d+1+1e-6):Math.ceil(d-1-1e-6);const k=dir>0?tr.steps.find(x=>x>d+0.01):tr.steps.slice().reverse().find(x=>x<d-0.01);return k??d;}
function scStop(){if(!SC.playing)return;cancelAnimationFrame(SC.playing);clearInterval(SC.playing);SC.playing=0;const b=$('#vwPlay');if(b){b.innerHTML=icon('play',20);b.setAttribute('aria-label',STR.vw.play);}
  const stp=$('#vwStamp');if(stp){stp.setAttribute('aria-live','polite');const t=stp.innerHTML;stp.innerHTML='';requestAnimationFrame(()=>{stp.innerHTML=t;});}}   // one announcement when Play stops

document.addEventListener('click',e=>{
  const b=e.target.closest('[data-vw]');if(!b||!b.closest('#vw'))return;const S=scCur(),E=SC.eng,a=b.dataset.vw;if(!S)return;const st=SC.st[S.id];
  if(a==='relaunch'){try{SC.eng&&SC.eng.dispose();}catch(_){}SC.eng=null;if(SC.canvas)SC.canvas.remove();SC.canvas=null;SC.cur=null;render();return;}
  if(a==='disc'){const o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',o);SC.discOpen=o;scOverlay();return;}
  if(a==='tab'){SC.tab=b.dataset.t;$('#vw').dataset.tab=SC.tab;$$('.vw-tabs [data-t]').forEach(x=>x.setAttribute('aria-current',x===b));return;}
  if(a==='dprev'||a==='dnext'){scStop();scDay(scStep(st.day,a==='dnext'?1:-1));return;}
  if(a==='play'){scPlay();return;}
  if(!E)return;
  if(a==='layer'){const on=b.getAttribute('aria-checked')!=='true';b.setAttribute('aria-checked',on);E.setLayer(b.dataset.l,on);scSave();return;}
  if(a==='labels'){SC.labels=!SC.labels;b.setAttribute('aria-checked',SC.labels);scOverlay();return;}
  if(a==='cut'){const on=b.getAttribute('aria-checked')!=='true';b.setAttribute('aria-checked',on);E.setCut({on});$('#vwCut').disabled=!on;scSave();return;}
  if(a==='axis'){E.setCut({axis:b.dataset.a});const cs=$('#vwCut');if(cs)cs.setAttribute('aria-valuetext',STR.vw.cutText(b.dataset.a,+cs.value));$$('[data-vw=axis]').forEach(x=>x.setAttribute('aria-current',x===b));scSave();return;}
  if(a==='view'){scView(b.dataset.v);return;} if(a==='zin'){E.zoomBy(1.25);scSave();return;} if(a==='zout'){E.zoomBy(0.8);scSave();return;}
  if(a==='turn'){const d=b.dataset.d,T=CONFIG.viewer.turn;E.orbitBy(d==='l'?-T.az:d==='r'?T.az:0,d==='u'?T.el:d==='d'?-T.el:0);scSave();return;}
  if(a==='dreset'){if(SC.drill&&SC.drill.home){const h=SC.drill.home;E.view(h.az,h.el,h.zoom);scSave();}return;}
  if(a==='lose'){const okL=E.loseContext(800);$('#vwMeasMsg').textContent=okL?STR.vw.loseOk:STR.vw.loseNo;return;}
  if(a==='measure'){scMeasure();return;} if(a==='dbgbox'){SC.dbgBoxes=!SC.dbgBoxes;E.setDebug(SC.dbgBoxes);return;}
  if(a==='mcopy'){const t=$('#vwMeasOut');navigator.clipboard.writeText(t.value).then(()=>{$('#vwMeasMsg').textContent=STR.copied;},()=>{t.select();$('#vwMeasMsg').textContent=STR.copyFail;});}
});
document.addEventListener('input',e=>{if(e.target.id==='vwDay'){scStop();scDay(+e.target.value);}
  else if(e.target.id==='vwCut'&&SC.eng){SC.eng.setCut({at:+e.target.value});e.target.setAttribute('aria-valuetext',STR.vw.cutText(SC.eng.state().cut.axis,+e.target.value));scSave();}});
document.addEventListener('keydown',e=>{
  if(!scCur()||!SC.eng||$('dialog[open]'))return;if(e.ctrlKey||e.metaKey||e.altKey)return;   // browser shortcuts stay the browser's (G-Eng)
  if(!e.target.closest||!e.target.closest('#vw')||e.target.matches('input:not([type=range]),textarea,select'))return;   // keys only while focus is in the viewer (WCAG 2.1.4)
  const k=e.key,S=scCur(),st=S&&SC.st[S.id],onStage=e.target.id==='vwStage';if(!st)return;
  if(SC.drill&&(scTr()?['l','L','c','C','0']:['[',']',' ','l','L','c','C','0']).includes(k))return;   // a drill keeps its day, cut and labels (the answer must not be one key away); a trace scrubs its day (V3)
  if(k==='['){e.preventDefault();scStop();scDay(scStep(st.day,-1));}else if(k===']'){e.preventDefault();scStop();scDay(scStep(st.day,1));}
  else if(k===' '&&!e.target.matches('button')){e.preventDefault();scPlay();}
  else if(onStage&&k.startsWith('Arrow')){e.preventDefault();SC.eng.orbitBy(k==='ArrowLeft'?-10:k==='ArrowRight'?10:0,k==='ArrowUp'?8:k==='ArrowDown'?-8:0);scSave();}
  else if(k==='+'||k==='='){SC.eng.zoomBy(1.25);scSave();}else if(k==='-'){SC.eng.zoomBy(0.8);scSave();}else if(k==='0'){scView('reset');}
  else if(k==='l'||k==='L'){$('[data-vw=labels]')?.click();}else if(k==='c'||k==='C'){$('[data-vw=cut]')?.click();}
});

/* leaving a scene (Back, nav, a link) stops Play + Measure before the router reads the new address (listener added before routerStart) */
function scLeave(){const r=parseHash(location.hash);if(r.name==='scene'&&r.id===SC.viewing)return;if(r.name!=='card')SC.inline=null;scStop();if(SC.meas)SC.meas=2;if(SC.ro){SC.ro.disconnect();SC.ro=null;}}
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
/* D-087: day labels never touch — big text or a narrow slider hides the ones that would (the current day and the ends first) */
function vwKeysFit(){$$('.vw-keys').forEach(k=>{const sp=[...k.children];if(!sp.length||!k.getClientRects().length||!k.offsetWidth)return;sp.forEach(x=>x.classList.remove('kh'));
  const r=x=>x.getBoundingClientRect(),keep=[];const pri=sp.slice().sort((a,b)=>(b.classList.contains('on')-a.classList.contains('on'))||((b===sp[0]||b===sp[sp.length-1])-(a===sp[0]||a===sp[sp.length-1])));
  pri.forEach(x=>{const q=r(x);if(keep.some(o=>q.left<o.right+6&&q.right>o.left-6))x.classList.add('kh');else keep.push(q);});});}
addEventListener('resize',()=>setTimeout(vwKeysFit,120));try{document.fonts&&document.fonts.ready.then(()=>vwKeysFit());}catch(_){}
if(typeof onDevice==='function')onDevice(()=>setTimeout(vwKeysFit,120));
