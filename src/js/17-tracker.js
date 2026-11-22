/* Biology Studio — progress map (W1, D-040) + scheduler view (W2, D-063): #progress (Map) · #progress=board · #progress=plan · #progress=inputs · #step=<id>.
   Plan maths: src/js/17-plan.js trPlan() (pure, same as tools/tracker/check.py plan()).
   Owner doc for the data: studio-docs/build/steps.json (format: tools/tracker/README.md); layouts: build/design-plan.md §2 (progress rows).
   Reads live from the deployed repo (GitHub Pages): steps.json, STATUS.md (§ Lock), master-plan.md (§13 ready prompts), ideas-backlog.md.
   Nothing here saves; the page only reads. Rules mirror tools/tracker/check.py (TR_RULES is compared by `check.py`; keep them in step).
   Debug: ?debug=tracker (overlay line + a Debug section with load times, depths and the in-page rule check). ✎ points at steps.json rows.
   EDIT: words in STR.tr, paths in CONFIG.tracker, status looks in app.css § 9 (.st-*), sizes in TR_SIZE. */
'use strict';
/* EDIT: vocabularies — JSON-style on purpose: tools/tracker/check.py parses this object and fails if it differs from its own */
const TR_RULES={"statuses":["idea","planned","ready","in progress","gates","owner check","done","parked","proposed"],
  "types":["Ideation","Build","Research","Content","Episode","Review","Fix","Idea"],
  "gates":["G-Sci","G-Learn","G-Story","G-Art","G-Eng","G-A11y","G-Owner"],
  "met":["owner check","done"],"started":["ready","in progress","gates","owner check","done"]};
const TR_SLUG={'idea':'idea','planned':'plan','ready':'ready','in progress':'now','gates':'gates','owner check':'check','done':'done','parked':'parked','proposed':'prop'};
/* EDIT: map sizes (CSS px) — node height ≥ --tap; columns shrink to min, then the map scrolls inside its own frame (§2 rule 6) */
const TR_SIZE={nodeH:48,rowH:60,colMin:64,colMax:150,laneLabelW:92,headH:36,gap:12};
const TR={D:null,err:null,loading:null,lock:{text:null,at:null,h:null},plan:'',backlog:'',at:0,ms:0,issues:[],P:null,lastNode:null,tapHl:null,
  show:{done:false,ideas:true}};
try{Object.assign(TR.show,JSON.parse(sessionStorage.getItem('biostudio.tracker'))||{});}catch(_){}

function trLoad(force){
  if(TR.loading&&!force)return TR.loading;
  const C=CONFIG.tracker,t0=performance.now(),get=(u,json)=>fetch(u,{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(u+' HTTP '+r.status);return json?r.json():r.text();});
  TR.err=null;
  TR.loading=Promise.all([get(C.steps,true),get(C.status).catch(()=>''),get(C.plan).catch(()=>''),get(C.backlog).catch(()=>'')])
    .then(([d,st,plan,bl])=>{if(!d||!Array.isArray(d.steps))throw new Error(STR.tr.badFile);TR.D=d;TR.plan=plan;TR.backlog=bl;TR.lock=trLockOf(st);TR.at=Date.now();TR.ms=Math.round(performance.now()-t0);
      TR.P=trPlanNow(d);TR.issues=trIssues(d);dlog('tracker','loaded',d.steps.length,'steps',TR.ms+' ms','issues',TR.issues.length,'lock',TR.lock.text||'free');})
    .catch(e=>{TR.err=e.message;dlog('tracker','load failed',e.message);});
  return TR.loading;}

/* ---- rules (pure; same as check.py) ---- */
const trBy=()=>{const m={};(TR.D?TR.D.steps:[]).forEach(s=>m[s.id]=s);return m;};
function trLockOf(statusText){   // STATUS § Lock: "- Build lock: <name> · <chat> · 19 Nov 2026, 21:49 IST" or "free (…)"
  const m=/^- Build lock: (.+)$/m.exec(statusText||'');if(!m||/^free/.test(m[1]))return {text:null,at:null,h:null};
  const d=/(\d{1,2}) ([A-Z][a-z]{2}) (\d{4}), (\d{1,2}):(\d{2}) IST/.exec(m[1]);let at=null;
  if(d){const mo='JanFebMarAprMayJunJulAugSepOctNovDec'.indexOf(d[2])/3;at=Date.UTC(+d[3],mo,+d[1],+d[4],+d[5])-330*60000;}
  const chat=m[1].replace(/^[^·]*· /,'').replace(/ · \d{1,2} [A-Z][a-z]{2} \d{4}.*$/,'').trim();   // "<name> · <chat name> · <date>" → chat name
  return {text:m[1],chat,at,h:at?(Date.now()-at)/3600000:null};}
function trBlockers(s,by,lock){   // what stops this step starting now (empty = can start)
  const why=[];(s.needs||[]).forEach(n=>{const o=by[n];if(o&&!TR_RULES.met.includes(o.status))why.push({k:'need',id:n,st:o.status});});
  (s.inputs||[]).forEach(x=>{if(x.blocks&&x.status==='open')why.push({k:'input',id:x.id});});
  if(s.lock&&lock&&lock.text&&(!s.chat||lock.chat!==s.chat))why.push({k:'lock',who:lock.text});   // held by another chat (exact chat name)
  return why;}
const trCanStartNow=(s,by,lock)=>['ready','planned'].includes(s.status)&&!trBlockers(s,by,lock).length;
function trDepths(vis){   // longest path from a visible root; a loop (never in checked data) is cut, not followed
  const set=new Set(vis.map(s=>s.id)),by={},d={},on=new Set();vis.forEach(s=>by[s.id]=s);
  const f=id=>{if(d[id]!=null)return d[id];if(on.has(id))return 0;on.add(id);
    const ns=(by[id].needs||[]).filter(n=>set.has(n));d[id]=ns.length?Math.max(...ns.map(f))+1:0;on.delete(id);return d[id];};
  vis.forEach(s=>f(s.id));return d;}
function trIssues(D){   // the in-page mirror of check.py's main rules — a banner if a push skipped CI
  const out=[],by={};D.steps.forEach(s=>by[s.id]=s);
  D.steps.forEach(s=>{
    if(!TR_RULES.statuses.includes(s.status))out.push(s.id+': status '+s.status);
    (s.needs||[]).forEach(n=>{if(!by[n])out.push(s.id+': needs unknown '+n);});
    if(TR_RULES.started.includes(s.status))(s.needs||[]).forEach(n=>{if(by[n]&&!TR_RULES.met.includes(by[n].status))out.push(s.id+': '+s.status+' but '+n+' is '+by[n].status);});
    if(s.status==='done'){Object.entries(s.gates||{}).forEach(([g,v])=>{if(v!=='pass'&&v!=='na')out.push(s.id+': done, '+g+' '+v);});
      if(s.check&&!['pass','na'].includes(s.check.state))out.push(s.id+': done, '+s.check.id+' '+s.check.state);}});
  const seen={},on=new Set(),loop=id=>{if(on.has(id))return true;if(seen[id])return false;seen[id]=1;on.add(id);const r=(by[id].needs||[]).some(n=>by[n]&&loop(n));on.delete(id);return r;};
  D.steps.forEach(s=>{if(loop(s.id))out.push(s.id+': dependency loop');});
  return [...new Set(out)];}
function trPrompt(key){   // master plan §13: "**Ready prompt — <key>** …" followed by "> " lines
  if(!key||!TR.plan)return null;const L=TR.plan.split('\n'),i=L.findIndex(l=>l.startsWith('**Ready prompt — '+key+'**'));if(i<0)return null;
  const out=[];for(let j=i+1;j<L.length;j++){const l=L[j];if(l.startsWith('>'))out.push(l.replace(/^>\s?/,''));else if(out.length||(l.trim()&&!l.startsWith('>')))break;}
  return out.join('\n').trim()||null;}
function trIdeaText(s){const n=+s.id.slice(2),m=new RegExp('^'+n+'\\. \\*\\*(.+?)\\*\\* \\(([SML])\\) — (.+)$','m').exec(TR.backlog||'');return m?m[3].replace(/\*\*?|`/g,''):null;}
function trInputs(){   // every open owner item: inputs, open owner checks waiting on you, proposals — oldest first
  const out=[];TR.D.steps.forEach(s=>{
    (s.inputs||[]).forEach(x=>{if(x.status==='open')out.push({id:x.id,kind:x.kind,date:x.asked,text:x.ask,step:s,d:x.d,chat:x.asked_in,blocks:!!x.blocks});});
    if(s.status==='owner check'&&s.check&&s.check.state==='open')out.push({id:s.check.id,kind:'check',date:s.check.since||'',text:STR.tr.checkAsk(s.check.id,s.title,s.check.by),step:s,chat:s.chat});
    if(s.proposed_by)out.push({id:s.id+'·p',kind:'confirm',date:s.proposed_on||'',text:STR.tr.propAsk(s.proposed_by,s.status,s.proposed_status),step:s,chat:s.chat});});
  return out.sort((a,b)=>(a.date||'9').localeCompare(b.date||'9')||a.id.localeCompare(b.id,undefined,{numeric:true}));}

function trToday(){const t=new Date(Date.now()+330*60000);return t.toISOString().slice(0,10);}   // IST date, like check.py ist_today()
function trPlanFresh(){if(TR.D&&(!TR.P||TR.P.today!==trToday()))TR.P=trPlanNow(TR.D);return TR.P;}   // the app may stay open past IST midnight
function trPlanNow(d){try{return typeof trPlan==='function'?trPlan(d,trToday()):null;}catch(e){dlog('tracker','plan failed',e.message);return null;}}
const trDay=iso=>{if(!iso)return '';const [y,m,d]=iso.split('-').map(Number);return d+' '+'JanFebMarAprMayJunJulAugSepOctNovDec'.substr((m-1)*3,3);};

/* ---- shared bits ---- */
const trSw=st=>`<span class="tr-sw st-${TR_SLUG[st]||'plan'}" aria-hidden="true"></span>`;
const trTi=s=>s.title.startsWith(s.id+' ')?s.title.slice(s.id.length+1):s.title;   // titles often start with their id — show it once
const trSt=st=>`<span class="tr-st">${trSw(st)}${esc(STR.tr.st[st]||st)}</span>`;
const trEdit=(id,what)=>editBtn('step',id,'studio-docs/build/steps.json (row '+id+(what?' › '+what:'')+')');
const trGh=p=>CONFIG.tracker.repo+p;
function trHead(view){const T=STR.tr,n=TR.D?trInputs().length:0,L=TR.lock;
  const lock=L.text?`<p class="banner tr-lock${L.h>24?' bad':''}">${esc(T.lockHeld(L.text))}${L.h!=null?' · '+esc(T.ago(L.h)):''}${L.h>24?' · <b>'+esc(T.lockOld)+'</b>':''}</p>`:`<p class="sm mut tr-lock">${esc(T.lockFree)}</p>`;
  return `<div class="tr-head"><h1>${esc(T.title)}</h1><div class="seg" role="group" aria-label="${esc(T.views)}">${['map','board','plan','inputs'].map(k=>`<button type="button" data-go="${k==='map'?'progress':'progress='+k}"${view===k?' aria-current="page"':''}>${esc(T.v[k])}${k==='inputs'&&n?` <span class="tr-n-badge">${n}</span>`:''}</button>`).join('')}</div>
    <button type="button" class="btn" data-tract="refresh">${esc(T.refresh)}</button>${editBtn('screen','progress','src/js/17-tracker.js + studio-docs/build/steps.json')}</div>
    ${lock}${TR.issues.length?`<p class="banner bad" role="status"><b>${esc(T.issuesT(TR.issues.length))}</b> ${esc(TR.issues.slice(0,4).join(' · '))}</p>`:''}`;}
const trFoot=()=>`<p class="xs mut tr-data">${esc(STR.tr.dataLine(TR.D.updated,new Date(TR.at)))}</p>${dbgOn('tracker')?trDebug():''}`;
function trDebug(){const vis=TR.D.steps.filter(s=>s.type!=='Idea'),dp=trDepths(vis),by=trBy();
  DBG.tracker=`tracker ${TR.D.steps.length} steps · ${TR.ms} ms · issues ${TR.issues.length} · lock ${TR.lock.text?(TR.lock.h!=null?TR.lock.h.toFixed(1)+' h':'? h'):'free'}`;dbgPaint();
  return `<details class="card tr-dbg"><summary>Debug · tracker</summary><pre class="mono">${esc(JSON.stringify({fetchMs:TR.ms,steps:TR.D.steps.length,issues:TR.issues,lock:TR.lock,
    show:TR.show,plan:TR.P?{today:TR.P.today,end:TR.P.end,critical:TR.P.critical,dates:TR.P.dates,ranked:TR.P.ranked.slice(0,8)}:null,canStart:vis.filter(s=>trCanStartNow(s,by,TR.lock)).map(s=>s.id),depth:dp},null,1))}</pre></details>`;}
function trWait(v,crumbs){ROUTE.crumbs=crumbs;window.TR_READY=null;
  if(TR.err){v.innerHTML=`<div class="card"><b>${esc(STR.tr.loadFail)}</b><p class="mut">${esc(TR.err)}</p><button type="button" class="btn" data-tract="refresh">${esc(STR.tr.refresh)}</button></div>`;window.TR_READY=ROUTE.raw;return true;}
  if(!TR.D){v.innerHTML=`<p class="empty">${esc(STR.tr.loading)}</p>`;const r=ROUTE.raw;trLoad().then(()=>{if(ROUTE.raw===r)render();});return true;}
  return false;}

/* ---- #progress: Map · Board · Your inputs ---- */
SCREENS.progress=function(v){
  const view=ROUTE.view||'map';if(trWait(v,[{label:STR.tr.title}]))return;
  ROUTE.crumbs=[{label:STR.tr.title,hash:'progress'}];if(view!=='map')ROUTE.crumbs.push({label:STR.tr.v[view]});
  v.innerHTML=`<div class="tr" data-view="${view}">${trHead(view)}${view==='board'?trBoard():view==='plan'?trPlanView():view==='inputs'?trInputsView():trMapShell()}${trFoot()}</div>`;
  if(view==='map'){TR.tapHl=null;trDrawMap();const back=TR.lastNode&&$(`.tr-node[data-go="step=${CSS.escape(TR.lastNode)}"]`);if(back){back.setAttribute('data-focus-first','');requestAnimationFrame(()=>back.scrollIntoView({block:'nearest',inline:'nearest'}));}TR.lastNode=null;}   // Back from a step → the shell focuses the node you came from (W1 to-do)
  window.TR_READY=ROUTE.raw;};
function trMapShell(){const T=STR.tr,D=TR.D,nd=D.steps.filter(s=>s.status==='done'&&s.type!=='Idea').length,ni=D.steps.filter(s=>s.type==='Idea').length;
  return `<div class="row tr-tools"><div class="seg" role="group" aria-label="${esc(T.showT)}">
    <button type="button" data-tract="done" aria-pressed="${TR.show.done}">${esc(T.showDone(nd))}</button>
    <button type="button" data-tract="ideas" aria-pressed="${TR.show.ideas}">${esc(T.showIdeas(ni))}</button></div>
    <span class="xs mut">${esc(DEV.cls==='dev-p'||DEV.cls==='dev-tp'?T.flowDown:T.flowRight)}${matchMedia('(pointer:coarse)').matches?' '+esc(T.tapTwice):''} <b class="tr-scrollhint hidden">${esc(T.scrollHint)}</b></span></div>
   <div class="card tr-mapc"><div class="tr-mapw" tabindex="0" role="region" aria-label="${esc(T.mapLabel)}"><div class="tr-map"></div></div></div>
   <div class="tr-below">${TR.show.ideas?trIdeas():''}${trKey()}</div>`;}
function trDrawMap(){
  const wrap=$('.tr-mapw'),box=$('.tr-map');if(!wrap||!box)return;
  const k=parseFloat(getComputedStyle(document.documentElement).fontSize)/16||1,Z={};   // sizes follow the text size (125 % text → bigger boxes, G-Art R2)
  Object.entries(TR_SIZE).forEach(([n,v])=>Z[n]=Math.round(v*Math.max(1,k)));
  const by=trBy(),vis=TR.D.steps.filter(s=>s.type!=='Idea'&&(TR.show.done||s.status!=='done')),dp=trDepths(vis);
  const vert=DEV.cls==='dev-p'||DEV.cls==='dev-tp',lanes=TR_RULES.types.filter(t=>t!=='Idea'&&vis.some(s=>s.type===t));
  const nD=Math.max(0,...Object.values(dp))+1,avail=wrap.clientWidth-2,slot={},cnt={};
  vis.forEach(s=>{const k=s.type+'|'+dp[s.id];slot[s.id]=cnt[k]=(cnt[k]||0);cnt[k]++;});
  const maxAt=(f)=>Math.max(1,...Object.entries(cnt).filter(([k])=>f(k)).map(([,n])=>n));
  let col,W,H;const pos={};
  if(vert){   // lanes are columns, depth runs down; same lane + depth stacks downwards
    col=Math.max(Z.colMin,Math.min(Z.colMax,Math.floor(avail/lanes.length)));
    const rows=[];for(let d=0;d<nD;d++)rows.push(maxAt(k=>+k.split('|')[1]===d));
    const y0=[];let y=Z.headH;rows.forEach((n,d)=>{y0[d]=y;y+=n*Z.rowH;});
    vis.forEach(s=>{pos[s.id]={x:lanes.indexOf(s.type)*col+Z.gap/2,y:y0[dp[s.id]]+slot[s.id]*Z.rowH,w:col-Z.gap};});
    W=lanes.length*col;H=y;
  }else{      // lanes are rows, depth runs right; same lane + depth stacks downwards inside the lane
    col=Math.max(Z.colMin+16,Math.min(Z.colMax+30,Math.floor((avail-Z.laneLabelW)/nD)));
    const y0={};let y=0;lanes.forEach(l=>{y0[l]=y;y+=maxAt(k=>k.startsWith(l+'|'))*Z.rowH+Z.gap;});
    vis.forEach(s=>{pos[s.id]={x:Z.laneLabelW+dp[s.id]*col+Z.gap/2,y:y0[s.type]+Z.gap/2+slot[s.id]*Z.rowH,w:col-Z.gap};});
    W=Z.laneLabelW+nD*col;H=y;
    TR._laneY=y0;}
  const wide=col>=118,T=STR.tr;
  let edges='';vis.forEach(s=>(s.needs||[]).forEach(n=>{const a=pos[n],b=pos[s.id];if(!a||!b)return;const met=TR_RULES.met.includes(by[n].status);
    // orthogonal routes through the gutters only (never across another box): leave on the right, run in the gap, enter from the top (vertical) or left (horizontal)
    const x1=a.x+a.w,y1=a.y+Z.nodeH/2,g1=x1+Z.gap/2,gy=b.y-Z.gap/2;let d;
    if(vert)d=`M${x1} ${y1}H${g1}V${gy}H${b.x+b.w/2}V${b.y}`;
    else{const g2=b.x-Z.gap/2,y2=b.y+Z.nodeH/2;d=g2-g1<1?`M${x1} ${y1}H${g1}V${y2}H${b.x}`:`M${x1} ${y1}H${g1}V${gy}H${g2}V${y2}H${b.x}`;}
    edges+=`<path d="${d}" class="${met?'met':'wait'}" data-a="${esc(n)}" data-b="${esc(s.id)}" marker-end="url(#trArr)"/>`;}));
  const lab=vert?lanes.map((l,i)=>`<div class="tr-lane v" style="left:${i*col}px;width:${col}px">${esc((col<96?T.laneShort:T.lane)[l]||l)}</div>`).join('')
    :lanes.map(l=>`<div class="tr-lane h" style="top:${TR._laneY[l]}px;height:${Z.rowH}px;width:${Z.laneLabelW-8}px">${esc(T.lane[l]||l)}</div>`).join('');
  const nodes=vis.map(s=>{const p=pos[s.id],go=trCanStartNow(s,by,TR.lock),bl=['ready','planned','idea'].includes(s.status)&&trBlockers(s,by,TR.lock).length;
    return `<button type="button" class="tr-node st-${TR_SLUG[s.status]}${go?' go':''}" style="left:${p.x}px;top:${p.y}px;width:${p.w}px;height:${Z.nodeH}px" data-go="step=${esc(s.id)}"
      aria-label="${esc(T.nodeLabel(s.id,s.title,T.st[s.status],go,bl))}" title="${esc(s.id+' · '+s.title+' · '+T.st[s.status])}"><b>${esc(s.id)}</b><span>${esc(wide?T.st[s.status]:T.stShort[s.status])}${go&&wide?' ◎':''}</span></button>`;}).join('');
  box.style.width=W+'px';box.style.height=H+'px';const sh=$('.tr-scrollhint');if(sh)sh.classList.toggle('hidden',W<=avail+1);
  box.innerHTML=`${lab}<svg class="tr-edges" width="${W}" height="${H}" aria-hidden="true"><defs><marker id="trArr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L8 4L0 8z"/></marker></defs>${edges}</svg>${nodes}`;
  box.onpointerover=box.onfocusin=ev=>{const n=ev.target.closest('.tr-node'),sv=$('svg.tr-edges',box);if(!sv)return;const id=n&&n.dataset.go.slice(5);
    sv.classList.toggle('dim',!!id);$$('path[data-a]',sv).forEach(p=>p.classList.toggle('hl',!!id&&(p.dataset.a===id||p.dataset.b===id)));};
  const hl=id=>{const sv=$('svg.tr-edges',box);if(!sv)return;sv.classList.toggle('dim',!!id);$$('path[data-a]',sv).forEach(p=>p.classList.toggle('hl',!!id&&(p.dataset.a===id||p.dataset.b===id)));};
  box.onclick=ev=>{const n=ev.target.closest('.tr-node');if(!n)return;const id=n.dataset.go.slice(5),touch=ev.detail>0&&TR._ptr==='touch';TR._ptr=null;
    if(touch&&TR.tapHl!==id){ev.preventDefault();ev.stopPropagation();TR.tapHl=id;hl(id);toast(STR.tr.tapAgain);return;}   // touch only: tap 1 shows its lines, tap 2 opens (W1 to-do); keyboard, mouse and screen readers open at once
    TR.tapHl=null;TR.lastNode=id;};
  box.onpointerdown=ev=>{TR._ptr=ev.pointerType;};
  box.onpointerleave=ev=>{if(ev.pointerType==='touch')return;const sv=$('svg.tr-edges',box);if(sv){sv.classList.remove('dim');$$('path.hl',sv).forEach(p=>p.classList.remove('hl'));}};
  box.onfocusout=()=>{const sv=$('svg.tr-edges',box);if(sv){sv.classList.remove('dim');$$('path.hl',sv).forEach(p=>p.classList.remove('hl'));}};
  dlog('tracker','map',vert?'vertical':'horizontal',vis.length,'nodes',lanes.length,'lanes',nD,'levels','col',col,'px',W+'×'+H);}
function trIdeas(){const T=STR.tr,I=TR.D.steps.filter(s=>s.type==='Idea');
  return `<section class="card tr-ideas" aria-labelledby="trIdT"><h2 id="trIdT">${esc(T.ideasT(I.length))}</h2><p class="sm mut">${esc(T.ideasLead)}</p>
    <div class="tr-igrid">${I.map(s=>`<button type="button" class="tr-idea st-${TR_SLUG[s.status]}" data-go="step=${esc(s.id)}"><span class="mono">${esc(s.id)}</span> ${esc(s.title)}${s.size?` <span class="xs mut">${esc(s.size)}</span>`:''}</button>`).join('')}</div></section>`;}
function trKey(){const T=STR.tr,used=new Set(TR.D.steps.map(s=>s.status));
  return `<section class="card tr-key" aria-labelledby="trKeyT"><h2 id="trKeyT">${esc(T.keyT)}</h2><ul class="tr-keyl">${TR_RULES.statuses.filter(s=>used.has(s)).map(s=>`<li>${trSw(s)}<span><b>${esc(T.st[s])}</b> <span class="xs mut">${esc(T.stHelp[s])}</span></span></li>`).join('')}
    <li><span class="tr-sw st-ready go" aria-hidden="true"></span><span><b>◎ ${esc(T.goT)}</b> <span class="xs mut">${esc(T.goHelp)}</span></span></li>
    <li><svg width="36" height="12" aria-hidden="true" class="tr-edges"><path d="M2 6H34" class="met"/></svg><span>${esc(T.edgeMet)}</span></li>
    <li><svg width="36" height="12" aria-hidden="true" class="tr-edges"><path d="M2 6H34" class="wait"/></svg><span>${esc(T.edgeWait)}</span></li></ul></section>`;}
function trBoard(){const T=STR.tr,by=trBy(),S=TR.D.steps.filter(s=>s.type!=='Idea'),col={now:[],ready:[],blocked:[],done:[]};
  S.forEach(s=>{const st=s.status;if(['in progress','gates','owner check'].includes(st))col.now.push(s);else if(st==='done')col.done.push(s);
    else if(['ready','planned'].includes(st)&&!trBlockers(s,by,TR.lock).length)col.ready.push(s);else if(st!=='parked')col.blocked.push(s);});
  const card=(s,k)=>{let sub='';const bl=trBlockers(s,by,TR.lock);
    if(k==='now'){const g=Object.values(s.gates||{}),p=g.filter(x=>x==='pass'||x==='na').length;sub=(g.length?T.gatesN(p,g.length):'')+(s.check?' · '+s.check.id+' '+(T.ck[s.check.state]||s.check.state):'');}
    else if(k==='ready')sub=s.chat;else if(k==='blocked')sub=T.needsShort(bl.map(trWhy));else sub=(s.log||'').split(' · ')[0];
    return `<div class="row tr-bc"><button type="button" class="lrow tr-card" data-go="step=${esc(s.id)}">${trSw(s.status)}<span class="nm"><b class="mono">${esc(s.id)}</b> ${esc(trTi(s))}<br><span class="xs mut">${esc(T.st[s.status])}${sub?' · '+esc(sub):''}</span></span></button>${trEdit(s.id)}</div>`;};
  const n=TR.D.steps.filter(s=>s.type==='Idea').length;
  return `<div class="tr-board">${['now','ready','blocked','done'].map(k=>`<section class="card tr-col" aria-labelledby="trB-${k}"><h2 id="trB-${k}">${esc(T.col[k])} <span class="tr-n-badge">${col[k].length}</span></h2><p class="xs mut">${esc(T.colHelp[k])}</p>${col[k].map(s=>card(s,k)).join('')||`<p class="sm mut">${esc(STR.none)}</p>`}</section>`).join('')}</div>
    <p class="sm mut"><button type="button" class="lk" data-go="progress">${esc(T.ideasOnMap(n))}</button></p>`;}
function trPlanView(){const T=STR.tr,P=trPlanFresh(),by=trBy();
  if(!P)return `<p class="empty">${esc(T.loadFail)}</p>`;
  const L=T.pl,nm=c=>c.kind==='check'?L.checkItem(c.id.split('·')[1]):c.kind==='input'?L.inputItem(c.id):(by[c.step]?trTi(by[c.step]):c.step);
  const when=c=>c.start?L.when(trDay(c.start),trDay(c.end||c.start)):L.noDate;
  const crit=new Set(P.critical.map(c=>c.id)),st=c=>by[c.step]?T.st[by[c.step].status]:'';
  const cell=c=>`<button type="button" class="lrow tr-pi${crit.has(c.id)?' crit':''}" data-go="step=${esc(c.step)}">${by[c.step]?trSw(by[c.step].status):''}<span class="nm"><b class="mono">${esc(c.kind==='step'?c.step:c.id.split('·').pop())}</b>${c.kind==='step'&&by[c.step]?trRunTag(by[c.step]):''} ${esc(nm(c))}<br><span class="xs mut">${c.kind==='step'&&st(c)?esc(st(c))+' · ':''}${esc(when(c))}${c.mins?' · '+esc(L.mins(c.mins)):''}</span>${c.slipped?` <span class="badge bad">${esc(L.slipped)}</span>`:''}${crit.has(c.id)?` <span class="tr-crit" aria-hidden="true">◆</span><span class="sr">${esc(L.critSr)}</span>`:''}</span></button>`;
  const list=a=>a.length>3?a.slice(0,3).map(cell).join('')+`<details class="tr-pmore"><summary class="lk">${esc(L.moreN(a.length-3))}</summary>${a.slice(3).map(cell).join('')}</details>`:a.map(cell).join('');
  const rows=['lock','gpu','research','owner'].map(r=>{const R=P.rows[r];if(!R.now.length&&!R.next.length&&!R.later.length)return '';
    return `<section class="card tr-prow" aria-labelledby="trPR-${r}"><h2 id="trPR-${r}">${esc(L.rows[r])}</h2><p class="xs mut">${esc(L.rowHelp[r])}</p><div class="tr-pcols">${['now','next','later'].map(k=>`<div class="tr-pcol"><h3 class="tr-pch">${esc(L.cols[k])}</h3>${list(R[k])||`<p class="sm mut">${esc(L.empty)}</p>`}</div>`).join('')}</div></section>`;}).join('');
  const cp=P.critical.length?`<div class="links tr-cp">${P.critical.map((c,i)=>{const it=P.dates[c.id];return `${i?'<span aria-hidden="true">→</span>':''}<button type="button" class="lk" data-go="step=${esc(c.step)}"><span aria-hidden="true">◆</span><span class="mono">${esc(c.id.split('·').pop())}</span>${it&&it.end?' ~'+esc(trDay(it.end)):''}</button>`;}).join('')}</div>`:`<p class="sm mut">${esc(L.noEnd)}</p>`;
  const you=P.ranked.slice(0,5).map(x=>`<li><button type="button" class="lrow" data-go="step=${esc(x.step)}"><span class="nm"><b class="mono">${esc(x.id)}</b> ${esc(by[x.step]?trTi(by[x.step]):x.step)}<br><span class="xs mut">${esc(T.kind[x.kind]||x.kind||'')} · ${esc(L.unblocksN(x.unblocks))}${x.blocks?' · '+esc(L.blocking):''}</span></span></button></li>`).join('');
  const prof=P.prof.map(x=>`<li><button type="button" class="lrow" data-go="step=${esc(x.step)}"><span class="nm"><b class="mono">${esc(x.id)}</b> ${esc(by[x.step]?trTi(by[x.step]):x.step)}${x.improves?`<br><span class="xs mut">${esc(L.improves(x.improves))}</span>`:''}</span></button></li>`).join('');
  const runs=[];TR.D.steps.forEach(s=>(s.runs||[]).forEach(r=>runs.push({s,r})));runs.sort((a,b)=>String(b.r.start).localeCompare(String(a.r.start)));
  const cal0=planCal(TR.D),est=s=>planChats(s,cal0);
  const runList=runs.slice(0,15).map(({s,r})=>{const n=(s.runs||[]).length,e=est(s),slip=n>e;
    return `<li class="row tr-run"><span class="mono xs">${esc(trDay(String(r.start).slice(0,10)))}${String(r.start).length>10?' '+esc(String(r.start).slice(11)):''}</span><button type="button" class="lk" data-go="step=${esc(s.id)}"><span class="mono">${esc(s.id)}</span></button><span class="sm nm">${esc(r.chat)} · ${esc(L.outcome[r.outcome]||r.outcome)}${r.by?' · '+esc(r.by):''}</span><span class="xs mut">${esc(L.estVsRun(e,n))}</span>${slip?`<span class="badge bad">${esc(L.slipped)}</span>`:''}</li>`;}).join('');
  const cal=planCal(TR.D),hrs=cal.day_min.map((m,i)=>L.days[i]+' '+L.mins(m)).join(' · ');
  return `<p class="sm mut">${esc(L.lead)}</p>
    <section class="card tr-pend" aria-labelledby="trPE"><h2 id="trPE">${esc(L.endT)}</h2><p class="tr-pbig">${(()=>{const c=P.critical[P.critical.length-1],it=c&&P.dates[c.id];return it&&it.end?esc(L.endLine(c.id,trDay(it.end)))+(by[c.step]?` <span class="sm mut">${esc(trTi(by[c.step]))}</span>`:''):esc(L.noEnd);})()}</p>
      <h3 class="tr-pch">${esc(L.critT)}</h3><p class="xs mut">${esc(L.critHelp)}</p>${cp}</section>
    <div class="tr-prows">${rows}</div>
    <div class="tr-pside"><section class="card" aria-labelledby="trPY"><h2 id="trPY">${esc(L.youT)}</h2><p class="xs mut">${esc(L.youHelp)}</p><ol class="tr-plist">${you||`<li class="sm mut">${esc(STR.none)}</li>`}</ol>
      <p class="sm"><button type="button" class="lk" data-go="progress=inputs">${esc(L.allInputs(trInputs().length))}</button></p></section>
    <section class="card" aria-labelledby="trPP"><h2 id="trPP">${esc(L.profT)}</h2><p class="xs mut">${esc(L.profHelp)}</p><ul class="tr-plist">${prof||`<li class="sm mut">${esc(L.noProf)}</li>`}</ul></section></div>
    <section class="card tr-pruns" aria-labelledby="trPRu"><h2 id="trPRu">${esc(L.runsT)}</h2><p class="xs mut">${esc(L.runsHelp)}</p><ul class="tr-runs">${runList}</ul></section>
    <p class="xs mut tr-pcal">${esc(L.calT)}: ${esc(L.calLine(hrs,cal.off.join(', ')))} ${editBtn('step','calendar','studio-docs/build/steps.json › calendar')}</p>`;}
// W3 run surface (D-080): [Code]/[Cowork] from trSurface() (17-plan.js); a run.on the rules don't allow shows ⚠ unless override
function trRunTag(s){const x=typeof trSurface==='function'&&TR.D?trSurface(TR.D,s):null;   // one trSurface() per cell
  if(!x||!x.on||s.type==='Idea')return '';const off=x.rule!=null&&!x.fit&&!x.override;
  return ` <span class="badge tr-on${off?' bad':''}" aria-hidden="true">${esc(x.on)}${off?' ⚠':''}</span><span class="sr">${esc(STR.tr.pl.runSr(x.on))}</span>`;}
function trRunLine(s){const T=STR.tr.pl,x=typeof trSurface==='function'&&TR.D?trSurface(TR.D,s):null;if(!x||!x.on)return esc(s.type==='Idea'?STR.none:T.runNone);
  const off=x.rule!=null&&!x.fit&&!x.override;return `<b>${esc(x.on)}</b>${x.why?' — '+esc(x.why):''}${off?` <span class="badge bad">⚠ ${esc(T.runOff(x.allowed.join(' / ')))}</span>`:''}${x.override?` <span class="xs mut">(${esc(T.runOver)})</span>`:''} ${trEdit(s.id,'run')}`;}
function trWhy(b){const T=STR.tr;return b.k==='need'?b.id+' ('+(T.st[b.st]||b.st)+')':b.k==='input'?T.yourAnswer(b.id):T.theLock;}
function trInputsView(){const T=STR.tr,L=trInputs();
  return `<p class="sm mut">${esc(T.inputsLead(L.length))}</p><ol class="tr-inputs">${L.map((x,i)=>`<li class="card tr-in">
    <div class="row"><span class="badge tr-k-${esc(x.kind)}">${esc(T.kind[x.kind]||x.kind)}</span><span class="mono">${esc(x.id)}</span><span class="xs mut">${esc(x.date?T.asked(x.date):'')}</span>${x.blocks?`<span class="badge bad">${esc(T.blocksStart)}</span>`:''}<span class="sp"></span>${x.kind==='check'||x.kind==='confirm'?'':trEdit(x.step.id,'inputs '+x.id)}</div>
    <p class="tr-ask">${esc(x.text)}</p>
    <p class="xs mut">${esc(T.askedIn(x.chat))}${x.d?' · '+esc(x.d):''}</p>
    <div class="row"><button type="button" class="lk" data-go="step=${esc(x.step.id)}">${esc(T.openStep(x.step.id))}</button>${x.d?`<a class="lk" href="${esc(trGh('studio-docs/claude/DECISIONS.md'))}" target="_blank" rel="noopener">${esc(x.d)} ↗</a>`:''}
      <button type="button" class="btn" data-tract="reply" data-i="${i}">${esc(T.copyReply)}</button></div></li>`).join('')}</ol>`;}

/* ---- #step=<id> ---- */
SCREENS.step=function(v){
  if(trWait(v,[{label:STR.tr.title,hash:'progress'},{label:ROUTE.id||'?'}]))return;
  const T=STR.tr,by=trBy(),s=by[ROUTE.id];ROUTE.crumbs=[{label:T.title,hash:'progress'},{label:s?s.id:(ROUTE.id||'?')}];
  if(!s){v.innerHTML=`<div class="tr">${trHead('')}<p class="empty">${esc(T.noStep(ROUTE.id))}</p></div>`;window.TR_READY=ROUTE.raw;return;}
  TR.lastNode=s.id;   // Back to the map focuses the last step you looked at (rail clicks too — G-A11y N4)
  const bl=trBlockers(s,by,TR.lock),notYet=['ready','planned','idea','proposed','parked'].includes(s.status),pr=trPrompt(s.prompt);
  const chip=id=>{const o=by[id];return o?`<button type="button" class="lk" data-go="step=${esc(id)}">${trSw(o.status)}<span class="mono">${esc(id)}</span> ${esc(T.st[o.status])}${TR_RULES.met.includes(o.status)?' ✓':''}</button>`:`<span class="lk">${esc(id)} ?</span>`;};
  const ideaTxt=s.type==='Idea'?trIdeaText(s):null;
  // red only for a real block (a step or your answer); the lock alone, ideas and parked items get a calm note (G-Art R1)
  const hard=bl.filter(b=>b.k!=='lock'),lockB=bl.find(b=>b.k==='lock');
  const can=!notYet?'':['parked','idea'].includes(s.status)?`<p class="tr-wait">${esc(T.afterGate)}</p>`
      :hard.length?`<p class="tr-cant"><b>${esc(T.cantStart)}</b> ${esc(T.needsShort(bl.map(trWhy)))}</p>`
      :lockB?`<p class="tr-wait">${esc(T.waitsLock(lockB.who))}</p>`:`<p class="tr-can"><b>◎ ${esc(T.canStart)}</b></p>`;
  const prop=s.proposed_by?`<p class="banner"><b>${esc(T.propBanner(s.proposed_by,s.status,s.proposed_status,s.proposed_on))}</b></p>`:'';
  const list=TR.D.steps.filter(o=>o.type!=='Idea');
  const lanes=TR_RULES.types.filter(t=>t!=='Idea'&&list.some(o=>o.type===t));
  const rail=lanes.map(l=>`<p class="tr-rh">${esc(T.lane[l]||l)}</p>`+list.filter(o=>o.type===l).map(o=>`<button type="button" class="lrow tr-rr" data-go="step=${esc(o.id)}"${o.id===s.id?' aria-current="true"':''}>${trSw(o.status)}<span class="nm"><span class="mono">${esc(o.id)}</span> ${esc(trTi(o))}</span></button>`).join('')).join('');
  const gates=Object.entries(s.gates||{}),inputs=(s.inputs||[]).slice().sort((a,b)=>(a.status==='open'?0:1)-(b.status==='open'?0:1));
  const facts=`<dl class="tr-dl">
    <dt>${esc(T.needs)}</dt><dd><div class="links">${(s.needs||[]).map(chip).join('')||esc(STR.none)}</div></dd>
    <dt>${esc(T.unblocks)}</dt><dd><div class="links">${(s.unblocks||[]).length>8?(s.unblocks.slice(0,6).map(chip).join('')+`<span class="sm mut">${esc(T.more(s.unblocks.length-6))}</span>`):((s.unblocks||[]).map(chip).join('')||esc(STR.none))}</div></dd>
    <dt>${esc(T.gatesT)}</dt><dd>${gates.length?`<ul class="tr-gl">${gates.map(([g,st])=>`<li><span class="tr-g g-${esc(st)}" aria-hidden="true">${{pass:'✓',open:'○',fail:'✗',na:'–'}[st]||'?'}</span>${esc(g)} · ${esc(T.gs[st]||st)}</li>`).join('')}</ul>`:esc(STR.none)}</dd>
    <dt>${esc(T.checkT)}</dt><dd>${s.check?`<a href="${esc(trGh('studio-docs/build/owner-test-checklist.md'))}" target="_blank" rel="noopener">${esc(s.check.id)} ↗</a> · ${esc(T.ck[s.check.state]||s.check.state)}${s.check.by?' · '+esc(s.check.by):''}`:esc(STR.none)}</dd>
    <dt>${esc(T.decT)}</dt><dd><div class="links">${(s.decisions||[]).map(d=>`<a class="lk" href="${esc(trGh('studio-docs/claude/DECISIONS.md'))}" target="_blank" rel="noopener">${esc(d)} ↗</a>`).join('')||esc(STR.none)}</div></dd>
    <dt>${esc(T.logT)}</dt><dd class="sm">${esc(s.log||STR.none)}</dd>
    <dt>${esc(T.pl.runT)}</dt><dd class="sm">${trRunLine(s)}</dd>
    <dt>${esc(T.pl.planT)}</dt><dd class="sm">${(()=>{const P0=trPlanFresh(),it=P0&&P0.dates[s.id];if(!it)return esc(TR_RULES.met.includes(s.status)?T.st[s.status]:STR.none);
      return esc(T.pl.planLine(it.start?T.pl.when(trDay(it.start),trDay(it.end||it.start)):T.pl.noDate,T.pl.rows[it.row]||it.row))+(it.slipped?` <span class="badge bad">${esc(T.pl.slipped)}</span>`:'')+(TR.P.critical.some(c=>c.id===s.id)?` <span class="tr-crit"><span aria-hidden="true">◆</span> ${esc(T.pl.critT)}</span>`:'');})()}
      ${(s.runs||[]).length?`<br><span class="xs mut">${esc(T.pl.runsN(s.runs.length))}: ${esc(s.runs.map(r=>trDay(String(r.start).slice(0,10))+' '+(T.pl.outcome[r.outcome]||r.outcome)).join(' · '))}</span>`:''}</dd></dl>`;
  const ins=inputs.length?`<section class="card"><h2>${esc(T.inputsT)}</h2>${inputs.map(x=>`<div class="tr-si${x.status==='open'?'':' closed'}"><div class="row"><span class="badge tr-k-${esc(x.kind)}">${esc(T.kind[x.kind]||x.kind)}</span><span class="mono">${esc(x.id)}</span><span class="badge">${esc(T.is[x.status]||x.status)}</span>${trEdit(s.id,'inputs '+x.id)}</div>
      <p class="tr-ask">${esc(x.ask)}</p>${x.answer?`<p class="sm"><b>${esc(T.answerT)}</b> ${esc(x.answer)}</p>`:''}<p class="xs mut">${esc(T.askedIn(x.asked_in))} · ${esc(T.asked(x.asked))}${x.d?' · '+esc(x.d):''}</p></div>`).join('')}</section>`:'';
  const todo=(s.todo||[]).length?`<section class="card"><h2>${esc(T.todoT)}</h2><ul class="sm tr-todo">${s.todo.map(t=>`<li>${esc(t)}</li>`).join('')}</ul></section>`:'';
  const prompt=s.type==='Idea'?'':`<section class="card tr-pr"><h2>${esc(T.promptT)}</h2><p class="sm"><span class="mut">${esc(T.chatName)}</span> <b class="tr-chat">${esc(s.chat)}</b></p>
    ${pr?`<details${notYet&&!bl.length?' open':''}><summary class="row" style="min-height:var(--tap);cursor:pointer"><b>${esc(T.showPrompt)}</b><span class="xs mut">${esc(T.promptFrom(s.prompt))}</span></summary><pre class="tr-ptxt">${esc(pr)}</pre></details>`
      :`<p class="sm mut">${esc(s.prompt?T.promptMissing(s.prompt):T.noPrompt)}</p>`}
    <div class="row"><button type="button" class="btn${notYet&&!bl.length?' pri':''}" data-tract="copyp">${esc(pr?T.copyPrompt:T.copyChat)}</button></div></section>`;
  v.innerHTML=`<div class="tr trs"><nav class="tr-rail card" aria-label="${esc(T.stepsNav)}">${rail}</nav>
    <article class="tr-main" aria-labelledby="cpT"><div class="row"><span class="mono mut">${esc(s.id)}</span>${trEdit(s.id)}<span class="sp"></span><span class="xs mut">${esc(T.lane[s.type]||s.type)}</span></div>
      <h1 id="cpT" tabindex="-1">${esc(s.title)}</h1><div class="row tr-meta">${trSt(s.status)}${s.lock?`<span class="badge">${esc(T.takesLock)}</span>`:''}${s.size?`<span class="badge">${esc(T.size(s.size))}</span>`:''}</div>
      ${prop}${can}${ideaTxt?`<p class="tr-idea-t">${esc(ideaTxt)}</p><p class="xs mut">${esc(T.ideaFrom)}</p>`:''}</article>
    <aside class="tr-facts card" aria-labelledby="trFT"><h2 id="trFT">${esc(T.factsT)}</h2>${facts}</aside>
    <div class="tr-rest">${prompt}${todo}${ins}</div></div>${trFoot()}`;
  const cur=$('.tr-rail [aria-current="true"]');if(cur&&DEV.cls!=='dev-p'&&DEV.cls!=='dev-pl'&&DEV.cls!=='dev-tp'){const r=$('.tr-rail');r.scrollTop=Math.max(0,cur.offsetTop-r.clientHeight/3);}
  window.TR_READY=ROUTE.raw;};

/* ---- events (one delegated listener each, added once) ---- */
document.addEventListener('click',async e=>{const b=e.target.closest('[data-tract]');if(!b||!b.closest('#view'))return;const a=b.dataset.tract,T=STR.tr;
  if(a==='refresh'){TR.D=null;TR.err=null;trLoad(true).then(()=>{render();toast(TR.err?T.loadFail:T.refreshed);});render();return;}
  if(a==='done'||a==='ideas'){TR.show[a]=!TR.show[a];try{sessionStorage.setItem('biostudio.tracker',JSON.stringify(TR.show));}catch(_){}render();return;}
  let txt='';
  if(a==='copyp'){const s=trBy()[ROUTE.id],p=s&&trPrompt(s.prompt);const rl=s?trSurface(TR.D,s):null,run=rl&&rl.on?'\n'+T.runLine(rl.on,rl.why):'';txt=s?(p?T.chatLine(s.chat)+run+'\n\n'+p:s.chat+run):'';}
  if(a==='reply'){const x=trInputs()[+b.dataset.i];if(x)txt=T.replyText(x.id,x.step.chat,x.text);}
  if(!txt)return;
  try{await navigator.clipboard.writeText(txt);toast(STR.copied);}catch(_){$('#editT').textContent=T.copyByHand;$('#editChat').textContent=a==='copyp'?trBy()[ROUTE.id].chat:((trInputs()[+b.dataset.i]||{}).step||{}).chat||'';$('#editTxt').value=txt;$('#editMsg').textContent=STR.copyFail;$('#editdlg').showModal();}
  dlog('tracker','copied',a,txt.length,'chars');});
let trRz=0;addEventListener('resize',()=>{clearTimeout(trRz);trRz=setTimeout(()=>{if(ROUTE.name==='progress'&&(ROUTE.view||'map')==='map'&&TR.D)trDrawMap();},120);});
onDevice(()=>{if(!(ROUTE.name==='progress'&&(ROUTE.view||'map')==='map'&&TR.D))return;   // keep the focused node and the map's sideways scroll across the redraw
  const go=document.activeElement&&document.activeElement.dataset?document.activeElement.dataset.go:null,w=$('.tr-mapw'),sl=w?w.scrollLeft/Math.max(1,w.scrollWidth):0;
  render();const w2=$('.tr-mapw');if(w2)w2.scrollLeft=sl*w2.scrollWidth;if(go){const el=document.querySelector(`#view [data-go="${CSS.escape(go)}"]`);if(el)el.focus({preventScroll:true});}});   // the map's flow turns with the device; other views switch in CSS only (place kept)
