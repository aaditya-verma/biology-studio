/* Biology Studio — Studio screens (S1; testing mode only): #studio (cards, new draft, calibration link) · #studio=<id>[&gate=G-Learn] (draft │ review │ sources)
   · #calib (score 5 dossier facts). Owner docs: docs/card-spec.md (format, gates, rules), build/design-plan.md §2 (Studio row) + §4.7.
   Layouts by class (C13): phone portrait + landscape = review only, line by line · tablet portrait = draft over review (sources below) ·
   tablet landscape = draft │ review (sources under draft) · desktop = draft │ review │ sources (3 panes).
   Nothing is saved (testing mode): a card leaves the app only by Copy JSON / Download, then a chat commits it (route A) — card-check runs in CI.
   EDIT: words in STR.st; rules in CARD_RULES (15-cards.js); roles in CONFIG.cards.roles. */
'use strict';
const ST={draft:{},orig:{},who:{by:'',role:'',agent:''},rv:{},imp:{card:'',text:'',sec:'',loc:'',fact:''},cal:{},ctx:null,ctxP:null,timer:0,focus:null,live:''};
const sdToday=()=>new Date().toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});   // E2: absolute dates
const sdPid=p=>'stp-'+p.replace(/[^\w]/g,'_');
function sdLoad(){if(!ST.ctxP)ST.ctxP=Promise.all([cardsCtx(),cdIndex()]).then(([c])=>(ST.ctx=c)).catch(e=>{ST.ctxP=null;CD.err=e.message;throw e;});return ST.ctxP;}
const sdCard=id=>ST.draft[id]||null;
async function sdOpen(id){if(ST.draft[id])return ST.draft[id];const c=await cdCard(id);if(!ST.draft[id]){ST.draft[id]=JSON.parse(JSON.stringify(c));ST.orig[id]=JSON.stringify(c);}return ST.draft[id];}
const sdDirty=id=>ST.draft[id]&&JSON.stringify(ST.draft[id])!==ST.orig[id];
const sdFind=c=>ST.ctx&&c?cardCheck(c,c.id,ST.ctx):[];
const sdCount=F=>({e:F.filter(i=>i.lvl==='E').length,w:F.filter(i=>i.lvl==='W').length});
const sdBadge=s=>`<span class="badge st-s-${esc(s)}">${esc(STR.st.status[s]||s)}</span>`;
function sdDbg(c){if(!dbgOn('studio'))return;const n=c?sdCount(sdFind(c)):null;DBG.studio='studio '+(c?c.id+' · '+c.status+' · gate '+(ROUTE.gate||'G-Sci')+' · '+n.e+' E · '+n.w+' W'+(sdDirty(c.id)?' · edited':''):'—');}
addEventListener('beforeunload',e=>{if(Object.keys(ST.draft).some(sdDirty)){e.preventDefault();e.returnValue='';}});

/* ---------- #studio ---------- */
SCREENS.studio=function(v){
  const S=STR.st;ROUTE.crumbs=ROUTE.id?[{label:S.title,hash:'studio'},{label:ROUTE.id}]:[{label:S.title}];window.ST_READY=null;
  if(!FLAGS.test){v.innerHTML=`<h1>${esc(S.title)}</h1><div class="card"><p><b>${esc(S.needTest)}</b></p><p class="sm mut">${esc(S.needTestHint)}</p><button type="button" class="btn pri" data-act="testmode">${esc(STR.testOn)}</button></div>`;return;}
  if(!ST.ctx){v.innerHTML=`<h1>${esc(S.title)}</h1><p class="${CD.err?'bad':'mut'}" role="status">${esc(CD.err?S.loadFail+' ('+CD.err+')':S.loading)}</p>${CD.err?`<button type="button" class="btn" data-st-act="retry" data-fk="retry">${esc(STR.retry||'Retry')}</button>`:''}`;
    if(!CD.err)sdLoad().then(()=>{dlog('studio','loaded',CD.idx.cards.length,'cards');if(ROUTE.name==='studio')render();},()=>{if(ROUTE.name==='studio')render();});return;}
  if(ROUTE.id){const c=sdCard(ROUTE.id);
    if(!c){v.innerHTML=`<h1>${esc(S.title)}</h1><p class="mut" role="status">${esc(S.loading)}</p>`;const id=ROUTE.id;
      sdOpen(id).then(()=>{if(ROUTE.name==='studio'&&ROUTE.id===id)render();},e=>{if(ROUTE.name==='studio'&&ROUTE.id===id)v.innerHTML=`<h1>${esc(S.title)}</h1><p class="bad" role="status">${esc(S.noCard(id))} (${esc(e.message)})</p><button type="button" class="btn" data-st-act="retry" data-fk="retry">${esc(STR.retry)}</button>`;});return;}
    if(ST.imp.card!==c.id)ST.imp={card:c.id,text:'',sec:'',loc:'',fact:''};   // the import box belongs to one card
    sdCardScreen(v,c);sdDbg(c);
    if(ST.focus){const f=document.getElementById(ST.focus);ST.focus=null;if(f)f.focus();}}
  else{sdHome(v);sdDbg(null);}
  window.ST_READY=ROUTE.raw||'studio';
};
function sdHome(v){
  const S=STR.st,ids=[...new Set([...CD.idx.cards.map(c=>c.id),...Object.keys(ST.draft)])];
  const rows=ids.map(id=>{const c=ST.draft[id]||null,meta=c||CD.idx.cards.find(x=>x.id===id),F=c?sdCount(sdFind(c)):null;
    return `<button type="button" class="lrow st-row" data-go="studio=${esc(id)}">${sdBadge(meta.status)}<span class="nm">${esc(meta.title)}${c&&sdDirty(id)?` <span class="xs st-dirty">${esc(S.dirty)}</span>`:''}</span><span class="id">${esc(id)} · ${esc(S.version(meta.version))}${F?' · '+(F.e?F.e+' E':'✓'):''}</span></button>`;}).join('');
  const have=new Set(ids),cand=MAPD.C.filter(c=>c.x1&&c.tier==='A'&&!have.has(c.id));
  v.innerHTML=`<h1>${esc(S.title)}</h1><p class="mut" style="max-width:var(--measure)">${esc(S.lead)}</p>
  <div class="st-home">
   <section class="card"><h2>${esc(S.cardsT)}</h2>${rows||`<p class="mut">${esc(S.none)}</p>`}</section>
   <section class="card"><h2>${esc(S.newT)}</h2><p class="sm mut">${esc(S.newHint)}</p>${cand.length?`<label class="sm" for="sdNew">${esc(S.newPick)}</label>
     <div class="row"><select id="sdNew">${cand.map(c=>`<option value="${esc(c.id)}">${esc(c.id)} · ${esc(c.name)}</option>`).join('')}</select><button type="button" class="btn" data-st-act="new">${esc(S.newB)}</button></div>`:`<p class="sm">${esc(S.newNone)}</p>`}</section>
   <section class="card"><h2>${esc(S.calibT)}</h2><p class="sm mut">${esc(S.calibHint)}</p><button type="button" class="btn" data-go="calib">${esc(S.calibB)}</button></section>
  </div>`;
}
function sdNew(id){const c=MAPD.byId[id];if(!c)return;const sc=scenesFor(id)[0],d=sdToday();
  ST.draft[id]={spec:1,id,version:1,book:CONFIG.book,status:'draft',title:c.name,tier:c.tier,objective:{verb:'explain',text:''},body:{general:'',mbbs:''},
    facts:[{id:'f1',text:'',cite:c.sec,mark:'≈',where:'main'}],terms:{new:[],known:(c.terms||[]).slice()},misconceptions:[],checks:[],remember:[],scene:{id:sc?sc.id:''},
    made:{by:ST.who.by||'',role:'Lead scientist',agent:'Studio (testing mode)',date:d},review:{},log:[{date:d,ev:'draft started in Studio',by:'Lead scientist · Studio'}]};
  ST.orig[id]='';go('studio='+id);}

/* ---------- #studio=<id>: header + three panes ---------- */
function sdCardScreen(v,c){
  const S=STR.st,F=sdFind(c),n=sdCount(F),gate=ROUTE.gate||'G-Sci';
  v.innerHTML=`<div class="st" data-gate="${esc(gate)}">
   <header class="st-head card"><div class="row"><h1 id="cpT">${esc(c.title)}</h1>${sdBadge(c.status)}<span class="xs mut mono">${esc(c.id)} · ${esc(S.version(c.version))}</span>
     <span id="sdDirty" class="xs st-dirty${sdDirty(c.id)?'':' hidden'}">${esc(S.dirty)}</span><span class="sp"></span>${editBtn('card',c.id,CONFIG.cards.dir+c.id+'.json')}</div>
     <div class="row st-bar"><details class="st-findbox"><summary id="sdChip" class="sm">${sdChip(n)}</summary><ul id="sdFind" class="st-find">${sdFindHtml(F)}</ul></details>
     <span class="sp"></span><button type="button" class="btn" data-st-act="copy">${esc(S.copyJson)}</button><button type="button" class="btn" data-st-act="download">${esc(S.download)}</button></div></header>
   <p id="sdLive" class="sr" aria-live="polite">${esc(S.findings(n.e,n.w))}</p><p id="sdRvLive" class="sr" aria-live="polite"></p><p class="banner st-phone">${esc(S.phoneNote)}</p>
   <section class="st-pane st-draft" aria-labelledby="sdDraftH"><div class="pane"><h2 id="sdDraftH" tabindex="-1">${esc(S.panes.draft)}</h2>${sdDraftHtml(c)}</div></section>
   <section class="st-pane st-review" aria-labelledby="sdRevH"><div class="pane" id="sdReview">${sdReviewHtml(c,gate)}</div></section>
   <section class="st-pane st-src" aria-labelledby="sdSrcH"><div class="pane"><h2 id="sdSrcH">${esc(S.panes.sources)}</h2>${sdSrcHtml(c)}</div></section>
  </div>`;
}
const sdChip=n=>n.e||n.w?`<span class="${n.e?'bad':'warn'}">${esc(STR.st.findings(n.e,n.w))}</span>`:`<span class="ok">✓ ${esc(STR.st.clean)}</span>`;
const sdFindHtml=F=>F.length?F.map(i=>`<li class="st-f ${i.lvl}"><b>${i.lvl==='E'?'✗':'!'} ${esc(i.code)}</b> <button type="button" class="lk xs" data-st-line="${esc(i.line)}">${esc(i.line)}</button> ${esc(i.msg)}</li>`).join(''):`<li class="mut">${esc(STR.st.findNone)}</li>`;

/* ---------- draft pane (form; every field has one data-p path into the card) ---------- */
function sdField(label,path,val,kind,opts={}){const id=sdPid(path),k=kind||'str';
  if(opts.select)return `<div class="st-fl"><label for="${id}">${esc(label)}</label><select id="${id}" data-p="${esc(path)}" data-k="${k}">${opts.select.map(([v,l])=>`<option value="${esc(v)}"${String(v)===String(val??'')?' selected':''}>${esc(l)}</option>`).join('')}</select></div>`;
  if(opts.area){const t=Array.isArray(val)?val.join('\n'):(val??'');return `<div class="st-fl wide"><label for="${id}">${esc(label)}</label><textarea id="${id}" data-p="${esc(path)}" data-k="${k}" rows="${Math.max(2,Math.min(9,Math.ceil(String(t).length/56)+1))}">${esc(t)}</textarea>${opts.after||''}</div>`;}
  const t=Array.isArray(val)?val.join(', '):(val??'');return `<div class="st-fl${opts.wide?' wide':''}"><label for="${id}">${esc(label)}</label><input type="text" id="${id}" data-p="${esc(path)}" data-k="${k}" value="${esc(t)}"${opts.ph?` placeholder="${esc(opts.ph)}"`:''}${opts.num?' inputmode="decimal"':''} autocomplete="off" spellcheck="${opts.nospell?'false':'true'}">${opts.after||''}</div>`;}
function sdDraftHtml(c){
  const S=STR.st,R=CARD_RULES,marks=R.marks.map(m=>[m,m+' — '+(STR.marks[m]||'')]),secOf=(MAPD.byId[c.id]||{}).sec||'';
  const lv=Object.keys(c.body),addable=Object.keys(R.budget).filter(l=>!lv.includes(l));
  const fact=(f,i)=>`<fieldset class="st-item" id="sdFact${i}"><legend>${esc(f.id)}</legend>${sdField(S.fText,`facts.${i}.text`,f.text,'str',{area:1})}
    ${sdField(S.fCite,`facts.${i}.cite`,f.cite,'str',{wide:1,nospell:1,ph:secOf+' · R06 CS6',after:`<span class="xs" data-cite-of="${i}">${sdCiteNote(f)}</span>`})}
    <div class="st-grid">${sdField(S.fMark,`facts.${i}.mark`,f.mark,'str',{select:marks})}${sdField(S.fWhere,`facts.${i}.where`,f.where,'str',{select:[['main',S.where.main],['more',S.where.more]]})}
    ${sdField(S.fDecision,`facts.${i}.decision`,f.decision,'opt',{nospell:1,ph:'D-029'})}</div>
    <button type="button" class="btn ghost sm" data-st-act="rmfact" data-i="${i}">${esc(S.removeFact)} ${esc(f.id)}</button></fieldset>`;
  const mis=(m,i)=>`<fieldset class="st-item" id="sdMis${i}"><legend>${esc(m.id)}</legend>${sdField(S.fWrong,`misconceptions.${i}.wrong`,m.wrong,'str',{wide:1})}${sdField(S.fRight,`misconceptions.${i}.right`,m.right,'str',{wide:1})}
    <div class="st-grid">${sdField(S.fCite,`misconceptions.${i}.cite`,m.cite,'str',{nospell:1})}${sdField(S.fMark,`misconceptions.${i}.mark`,m.mark,'str',{select:marks})}</div></fieldset>`;
  const chk=(q,i)=>`<fieldset class="st-item" id="sdChk${i}"><legend>${esc(q.id)}</legend>${sdField(S.fPrompt,`checks.${i}.prompt`,q.prompt,'str',{wide:1})}
    <div class="st-grid">${sdField(S.fType,`checks.${i}.type`,q.type,'str',{select:[['mcq',S.types.mcq],['order',S.types.order]]})}
    ${q.type==='mcq'?sdField(S.fAnswer,`checks.${i}.answer`,q.answer,'int',{select:(q.options||[]).map((o,j)=>[j,(j+1)+'. '+o.slice(0,40)])}):''}
    ${sdField(S.fRefutes,`checks.${i}.refutes`,q.refutes,'opt',{select:[['','—'],...c.misconceptions.map(m=>[m.id,m.id])]})}</div>
    ${sdField(S.fOptions,`checks.${i}.options`,q.options,'lines',{area:1})}${sdField(S.fWhy,`checks.${i}.why`,q.why,'str',{wide:1})}</fieldset>`;
  return `<div class="st-form">
   <fieldset class="st-item"><legend>${esc(S.makerT)}</legend><div class="st-grid">${sdField(S.rBy,'made.by',c.made.by,'str',{})}${sdField(S.rRole,'made.role',c.made.role,'str',{select:[['','—'],...CONFIG.cards.roles.filter(r=>r!=='Owner').map(r=>[r,r])]})}${sdField(S.rAgent,'made.agent',c.made.agent,'str',{wide:1})}</div></fieldset>
   <div class="st-grid">${sdField(S.fTitle,'title',c.title,'str',{wide:1})}${sdField(S.fTier,'tier',c.tier,'str',{select:['A','B','C','D'].map(t=>[t,t])})}</div>
   <div class="st-grid">${sdField(S.fVerb,'objective.verb',c.objective.verb,'str',{select:R.verbs.map(x=>[x,x])})}${sdField(S.fObjective,'objective.text',c.objective.text,'str',{area:1})}</div>
   <h3>${esc(S.fBody)}</h3>${lv.map(l=>sdField(S.fLevel(l),'body.'+l,c.body[l],'str',{area:1,after:`<span class="xs mut" data-count="${esc(l)}">${esc(S.words(cWords(c.body[l]),R.budget[l]||'?'))}</span>${R.required.includes(l)?'':` <button type="button" class="btn ghost sm" data-st-act="rmlevel" data-l="${esc(l)}">${esc(S.removeLevel)} · ${esc(S.fLevel(l))}</button>`}`})).join('')}
   ${addable.length?`<div class="row">${addable.map(l=>`<button type="button" class="btn sm" data-st-act="addlevel" data-l="${esc(l)}">+ ${esc(S.fLevel(l))}</button>`).join('')}</div>`:''}
   <h3>${esc(S.fFacts)}</h3>${c.facts.map(fact).join('')}<button type="button" class="btn" data-st-act="addfact">+ ${esc(S.addFact)}</button>
   <h3>${esc(S.fTerms)}</h3><p class="xs mut">${esc(S.termsHint)}</p><div class="st-grid">${sdField(S.fNew,'terms.new',c.terms.new,'list',{wide:1,nospell:1})}${sdField(S.fKnown,'terms.known',c.terms.known,'list',{wide:1,nospell:1})}${sdField(S.fException,'terms.exception',c.terms.exception,'opt',{nospell:1,ph:'D-037'})}</div>
   <h3>${esc(S.fMis)}</h3>${c.misconceptions.map(mis).join('')}<button type="button" class="btn" data-st-act="addmis">+ ${esc(S.addMis)}</button>
   <h3>${esc(S.fChecks)}</h3>${c.checks.map(chk).join('')}<button type="button" class="btn" data-st-act="addcheck">+ ${esc(S.addCheck)}</button>
   <h3>${esc(S.fRemember)}</h3>${(c.remember||[]).map((r,i)=>`<fieldset class="st-item" id="sdRem${i}"><legend>${esc(r.id)}</legend>${sdField(S.fQ,`remember.${i}.q`,r.q,'str',{wide:1})}${sdField(S.fA,`remember.${i}.a`,r.a,'str',{wide:1})}
    <button type="button" class="btn ghost sm" data-st-act="rmrem" data-i="${i}">${esc(S.removeRem)} ${esc(r.id)}</button></fieldset>`).join('')}<button type="button" class="btn" data-st-act="addrem">+ ${esc(S.addRem)}</button>
   ${sdField(S.fClinical,'clinical',c.clinical,'opt',{area:1})}${sdField(S.fShows,'shows_up',c.shows_up,'optlist',{wide:1,nospell:1,ph:S.showsHint})}
   <h3>${esc(S.fScene)}</h3>${sdField(S.fAdult,'adult',c.adult,'opt',{area:1})}
   <div class="st-grid">${sdField(S.fScene,'scene.id',c.scene.id,'str',{select:[['','—'],...((SC.idx&&SC.idx.scenes)||[]).map(s=>[s.id,s.id+' · '+s.title])]})}${sdField(S.fDay,'scene.day',c.scene.day,'num',{nospell:1,num:1})}</div>
  </div>`;
}
function sdCiteNote(f){if(!ST.ctx)return '';const v=validateCitation(f.cite,ST.ctx.src),s=suggestMark(v.parsed,f.decision,ST.ctx.src);
  return v.errors.length?`<span class="bad">✗ ${esc(v.errors.join('; '))}</span>`:`<span class="ok">✓ ${esc(STR.st.citeOk)}</span> · <span class="mut">${esc(STR.st.suggested(s))}</span>`;}
function sdSetPath(o,path,v){const ks=path.split('.');for(const k of ks.slice(0,-1))o=Array.isArray(o)?o[+k]:(o[k]=o[k]||{});const k=ks[ks.length-1];
  if(v===undefined){if(Array.isArray(o))o.splice(+k,1);else delete o[k];}else if(Array.isArray(o))o[+k]=v;else o[k]=v;}
function sdConv(val,k){switch(k){case 'lines':return val.split('\n').map(s=>s.trim()).filter(Boolean);case 'list':return val.split(/[\s,]+/).filter(Boolean);case 'optlist':{const l=val.split(/[\s,]+/).filter(Boolean);return l.length?l:undefined;}
  case 'int':return val===''?undefined:parseInt(val,10);case 'num':return val===''?undefined:+val;case 'opt':return val.trim()===''?undefined:val;default:return val;}}
function sdTouched(c){   // any content edit: drop the review ticks; clear every pass (failed reviews stay as history); a reviewed/shipped card goes back to draft
  Object.keys(ST.rv).filter(k=>k.startsWith(c.id+'|')).forEach(k=>delete ST.rv[k]);
  const passes=Object.keys(c.review||{}).filter(g=>c.review[g].result==='pass');passes.forEach(g=>delete c.review[g]);
  const reopen=c.status==='reviewed'||c.status==='shipped';if(reopen)c.status='draft';
  if(reopen||passes.length){c.log.push({date:sdToday(),ev:(reopen?'reopened; ':'')+'passes cleared ('+passes.join(', ')+'): content changed',by:'Studio'});toast(STR.st.reopened);dlog('studio','passes cleared',c.id,passes);return true;}
  return false;}
function sdLive(now){clearTimeout(ST.timer);const f=()=>{const c=sdCard(ROUTE.id);if(!c||ROUTE.name!=='studio')return;const F=sdFind(c);
  const n=sdCount(F),ch=$('#sdChip');if(ch)ch.innerHTML=sdChip(n);const lv=$('#sdLive'),lt=STR.st.findings(n.e,n.w);if(lv&&lv.textContent!==lt)lv.textContent=lt;sdDbg(c);const fl=$('#sdFind');if(fl)fl.innerHTML=sdFindHtml(F);
  $$('[data-count]').forEach(el=>{const l=el.dataset.count;el.textContent=STR.st.words(cWords(c.body[l]),CARD_RULES.budget[l]||'?');});
  $$('[data-cite-of]').forEach(el=>{const f=c.facts[+el.dataset.citeOf];if(f)el.innerHTML=sdCiteNote(f);});
  const d=$('#sdDirty');if(d)d.classList.toggle('hidden',!sdDirty(c.id));
  const rv=$('#sdReview');if(rv&&!rv.contains(document.activeElement))rv.innerHTML=sdReviewHtml(c,ROUTE.gate||'G-Sci');};   // never redraw under the reviewer's focus
  if(now)f();else ST.timer=setTimeout(f,CONFIG.cards.checkDelayMs);}
document.addEventListener('input',e=>{
  if(ROUTE.name!=='studio')return;const el=e.target.closest('[data-p]');
  if(el){const c=sdCard(ROUTE.id);if(!c)return;
    if(el.dataset.k==='num'&&el.value.trim()!==''&&!Number.isFinite(+el.value)){el.setAttribute('aria-invalid','true');return;}   // keep the last good number
    el.removeAttribute('aria-invalid');sdSetPath(c,el.dataset.p,sdConv(el.value,el.dataset.k));
    if(sdTouched(c)||/^checks\.\d+\.type$/.test(el.dataset.p)){render();return;}   // status reset or a field set that changes the form
    const om=el.dataset.p.match(/^checks\.(\d+)\.options$/),as=om&&document.getElementById(sdPid(`checks.${om[1]}.answer`));   // keep the answer list in step without a redraw (caret stays put)
    if(as){const q=c.checks[+om[1]];as.innerHTML=(q.options||[]).map((o,j)=>`<option value="${j}"${j===q.answer?' selected':''}>${esc((j+1)+'. '+o.slice(0,40))}</option>`).join('');}
    sdLive();return;}
  const w=e.target.closest('[data-st-who]');if(w){ST.who[w.dataset.stWho]=w.value;sdRvSoft();return;}   // never redraw a field being typed in
  const n=e.target.closest('[data-st-note]');if(n){const r=sdRv(ROUTE.id,ROUTE.gate||'G-Sci');r.notes[n.dataset.stNote]=n.value;return;}
  const im=e.target.closest('[data-st-imp]');if(im){ST.imp[im.dataset.stImp]=im.value;sdImpRefresh();return;}
});

/* ---------- review pane: one review card per gate, line by line ---------- */
function sdRv(id,g){const k=id+'|'+g;if(!ST.rv[k]){const st=(sdCard(id).review||{})[g],r=st&&st.result==='pass'?st:{},lines={},notes={};   // a new review starts blank; only a standing pass is shown ticked
  for(const [ln,val] of Object.entries(r.lines||{})){if(val==='ok')lines[ln]='ok';else{lines[ln]='fix';notes[ln]=String(val).replace(/^fix:\s*/,'');}}
  ST.rv[k]={checklist:Object.assign({},r.checklist||{}),lines,notes};}return ST.rv[k];}
function sdLineHtml(c,ln){const S=STR.st,src=ST.ctx&&ST.ctx.src,refs=t=>esc(stripRefs(t))+(cRefs(t).length?` <sup class="mono mut">${esc(cRefs(t).join(','))}</sup>`:'');
  if(ln==='obj')return `<b>${esc(c.objective.verb)}</b> · ${esc(c.objective.text)}`;
  if(ln==='terms')return `${c.terms.new.map(t=>`<b>${esc(src&&src.terms[t]||t)}</b>`).join(', ')}${c.terms.known.length?` · <span class="mut">${c.terms.known.map(t=>esc(src&&src.terms[t]||t)).join(', ')}</span>`:''}`;
  if(ln==='adult')return refs(c.adult);
  if(ln==='clinical')return `<span class="xs mut">${esc(S.fClinical)}</span> ${refs(c.clinical)}`;
  if(ln==='shows_up')return `<span class="xs mut">${esc(S.fShows)}</span> ${(c.shows_up||[]).map(x=>`<span class="mono">${esc(x)}</span> ${esc((MAPD.byId[x]||{}).name||'?')}`).join(' · ')}`;
  const rr=(c.remember||[]).find(x=>x&&x.id===ln);if(rr)return `<span class="xs mut">${esc(S.fRemember)}</span> ${esc(rr.q)} → ${refs(rr.a)}`;
  let m=ln.match(/^body\.(\w+)\.(\d+)$/);if(m)return `<span class="xs mut">${esc(S.fLevel(m[1]))}</span> ${refs(cSentences(c.body[m[1]]||'')[+m[2]-1]||'')}`;
  const f=c.facts.find(x=>x.id===ln);if(f)return `${esc(f.text)} <span class="mono xs">[${esc(f.cite)}]</span> <b class="mark" title="${esc(STR.marks[f.mark]||'')}">${esc(f.mark)}</b>${f.where==='more'?' <span class="badge">More</span>':''}${f.decision?` <span class="badge">${esc(f.decision)}</span>`:''}`;
  const mi=c.misconceptions.find(x=>x.id===ln);if(mi)return `✗ ${esc(mi.wrong)} → ✓ ${esc(mi.right)} <span class="mono xs">[${esc(mi.cite)}]</span> <b class="mark">${esc(mi.mark)}</b>`;
  const q=c.checks.find(x=>x.id===ln);if(q)return `${esc(q.prompt)}<ol class="st-opts">${(q.options||[]).map((o,j)=>`<li>${esc(o)}${q.type==='mcq'&&j===q.answer?` <b class="ok">✓ ${esc(S.ans)}</b>`:''}</li>`).join('')}</ol>${q.type==='order'?`<span class="xs mut">${esc(S.order)}</span> · `:''}<span class="xs">${esc(q.why)}</span>${q.refutes?` <span class="badge">${esc(q.refutes)}</span>`:''}`;
  return esc(ln);}
function sdCanPass(c,g){const r=sdRv(c.id,g),G=CARD_RULES.gates[g],w=ST.who,F=sdFind(c).filter(i=>i.lvl==='E'&&i.code!=='E-status');
  const who=w.by&&w.role&&w.agent&&(g==='G-Owner'?w.role==='Owner':(w.role!==c.made.role&&w.agent!==c.made.agent));
  const standing=((c.review||{})[g]||{}).result==='pass';   // already passed: an edit clears it, then it can be passed again
  return {who:!!who&&!standing,all:G.checklist.every(k=>r.checklist[k])&&gateLines(c,g).every(l=>r.lines[l]==='ok'),clean:!F.length,anyFix:gateLines(c,g).some(l=>r.lines[l]==='fix')};}
function sdReviewHtml(c,g){
  const S=STR.st,r=sdRv(c.id,g),G=CARD_RULES.gates[g],L=gateLines(c,g),cp=sdCanPass(c,g),done=(c.review||{})[g],w=ST.who,same=w.role&&w.agent&&(w.role===c.made.role||w.agent===c.made.agent)&&g!=='G-Owner';
  return `<h2 id="sdRevH">${esc(S.panes.review)}</h2>
   <div class="seg st-gates" role="group" aria-label="${esc(S.gateT)}">${Object.keys(CARD_RULES.gates).map(k=>`<button type="button" data-st-gate="${k}" data-fk="gate-${k}" aria-pressed="${k===g}">${esc(k)}${(c.review||{})[k]?` ${c.review[k].result==='pass'?'✓':'✗'}`:''}</button>`).join('')}</div>
   <p class="sm"><b>${esc(S.gateQ[g])}</b></p><p id="sdGateDone" tabindex="-1" class="sm ${done?(done.result==='pass'?'ok':'bad'):''}">${done?esc(S.gateDone(g,done.result,done.by+' · '+done.role+' · '+done.date)):''}</p>
   <fieldset class="st-who"><legend>${esc(S.reviewer)}</legend><p class="xs mut">${esc(S.maker(c.made))}</p>
     <div class="st-grid"><div class="st-fl"><label for="sdBy">${esc(S.rBy)}</label><input type="text" id="sdBy" data-st-who="by" value="${esc(w.by)}" autocomplete="name"></div>
     <div class="st-fl"><label for="sdRole">${esc(S.rRole)}</label><select id="sdRole" data-st-who="role"><option value="">—</option>${CONFIG.cards.roles.map(x=>`<option${x===w.role?' selected':''}>${esc(x)}</option>`).join('')}</select></div>
     <div class="st-fl wide"><label for="sdAgent">${esc(S.rAgent)}</label><input type="text" id="sdAgent" data-st-who="agent" value="${esc(w.agent)}" placeholder="Bio · Review · E05.01.01"></div></div>
     <p id="sdWhoNote" class="sm bad">${same?esc(S.sameAsMaker):''}</p></fieldset>
   <h3>${esc(S.checklistT)}</h3><div class="st-cks">${G.checklist.map(k=>`<label class="st-ck"><input type="checkbox" id="sdCk-${k}" data-layout-skip data-st-ck="${k}"${r.checklist[k]?' checked':''}> <span>${esc(S.checklist[k])}</span></label>`).join('')}</div>
   <h3>${esc(S.linesT)}</h3>${L.length?L.map(ln=>{const v=r.lines[ln]||'';return `<div class="st-line" id="ln-${esc(ln.replace(/\./g,'-'))}" data-v="${v}">
     <div class="st-lt"><span class="st-lid mono">${esc(ln)}</span> ${sdLineHtml(c,ln)}</div>
     <div class="st-lb" role="group" aria-label="${esc(ln)}"><button type="button" class="btn sm" data-st-v="ok" data-ln="${esc(ln)}" aria-pressed="${v==='ok'}">✓ ${esc(S.ok)}</button><button type="button" class="btn sm" data-st-v="fix" data-ln="${esc(ln)}" aria-pressed="${v==='fix'}">✎ ${esc(S.fix)}</button></div>
     ${v==='fix'?`<div class="st-fl wide"><label for="sdN-${esc(ln)}" class="sr">${esc(S.fixNote)} ${esc(ln)}</label><input type="text" id="sdN-${esc(ln)}" data-st-note="${esc(ln)}" value="${esc(r.notes[ln]||'')}" placeholder="${esc(S.fixNote)}"></div>`:''}</div>`;}).join(''):`<p class="sm mut">${esc(S.noLines)}</p>`}
   <div class="row st-res"><button type="button" class="btn pri" data-st-act="pass"${cp.who&&cp.all&&cp.clean?'':' disabled'}>✓ ${esc(S.pass)} ${esc(g)}</button>
     <button type="button" class="btn" data-st-act="fail"${cp.anyFix&&cp.who?'':' disabled'}>✗ ${esc(S.fail)}</button>
     ${done&&done.result==='fail'?`<button type="button" class="btn" data-st-act="fixprompt">${esc(S.fixPrompt)}</button>`:''}</div>
   <p class="xs mut">${esc(S.passNeeds)}</p>`;
}
function sdRvSoft(){const c=sdCard(ROUTE.id);if(!c)return;const g=ROUTE.gate||'G-Sci',cp=sdCanPass(c,g),w=ST.who,
  same=w.role&&w.agent&&(w.role===c.made.role||w.agent===c.made.agent)&&g!=='G-Owner',n=$('#sdWhoNote'),txt=same?STR.st.sameAsMaker:'';
  if(n&&n.textContent!==txt){n.textContent=txt;const lv=$('#sdRvLive');if(lv)lv.textContent=txt;}   // announced once, from a region outside the redrawn pane
  const p=$('[data-st-act=pass]'),f=$('[data-st-act=fail]');if(p)p.disabled=!(cp.who&&cp.all&&cp.clean);if(f)f.disabled=!(cp.anyFix&&cp.who);}
function sdRvRefresh(){const c=sdCard(ROUTE.id);if(!c)return;const p=$('#sdReview');if(!p)return;const a=document.activeElement,id=a&&a.id;
  p.innerHTML=sdReviewHtml(c,ROUTE.gate||'G-Sci');if(id&&document.getElementById(id))document.getElementById(id).focus({preventScroll:true});}
function sdDecide(c,g,result){const r=sdRv(c.id,g),w=ST.who,d=sdToday(),lines={};
  for(const ln of gateLines(c,g))lines[ln]=r.lines[ln]==='ok'?'ok':r.lines[ln]==='fix'?'fix: '+(r.notes[ln]||''):'';
  c.review=c.review||{};c.review[g]={result,by:w.by,role:w.role,agent:w.agent,date:d,checklist:Object.fromEntries(CARD_RULES.gates[g].checklist.map(k=>[k,!!r.checklist[k]])),lines,notes:''};
  c.log.push({date:d,ev:g+' '+result,by:w.role+' · '+w.agent});
  if(result==='pass'){for(const [st,need] of [['reviewed',CARD_RULES.needs.reviewed],['shipped',CARD_RULES.needs.shipped]]){
      const ok=need.every(k=>(c.review[k]||{}).result==='pass'),order=CARD_RULES.statuses.indexOf(st)>CARD_RULES.statuses.indexOf(c.status);
      if(ok&&order&&!sdFind(Object.assign({},c,{status:st})).some(i=>i.lvl==='E')){c.status=st;c.log.push({date:d,ev:'status → '+st,by:'Studio'});if(st==='reviewed')toast(STR.st.promoted);}}}
  else toast(STR.st.failed(g));
  dlog('studio','decide',c.id,g,result,'→',c.status);ST.focus='sdGateDone';render();
  const say=STR.st.gateDone(g,result,ST.who.by+' · '+ST.who.role)+(c.status==='reviewed'&&result==='pass'?' · '+STR.st.status.reviewed:'');
  setTimeout(()=>{const lv=$('#sdRvLive');if(lv)lv.textContent=say;},60);}   // after the redraw, so the new region is in place before it speaks
function sdFixPrompt(c,g){const r=c.review[g],fx=Object.entries(r.lines||{}).filter(([,v])=>String(v).startsWith('fix'));
  return `Chat: Bio · Fix · ${c.id}\nCard ${c.id} failed ${g} (${r.by}, ${r.role}, ${r.date}).\n\nRead claude/STATUS.md, claude/RULES.md (A2, B1, B6–B7, H1–H2) and docs/card-spec.md.\nFix these lines in ${CONFIG.cards.dir}${c.id}.json:\n${fx.map(([k,v])=>'- '+k+': '+v.replace(/^fix:\s*/,'')).join('\n')}\n\nKeep the id (A2), run tools/card-check, send it back to ${g} (a different reviewer), commit by route A.\nEnd with STATUS, build log, gates, usage check.`;}
async function sdCopy(text,okMsg){try{await navigator.clipboard.writeText(text);toast(okMsg);}catch(_){const d=$('#editdlg');$('#editT').textContent=STR.st.exportT;$('#editChat').textContent='';$('#editTxt').value=text;$('#editMsg').textContent=STR.copyFail;d.showModal();}}

/* ---------- sources pane: import links → a cited line; sections; registry ---------- */
function sdImpParse(t,src){t=(t||'').trim();if(!t)return null;const reg=src.registry;let m;
  if(/^\[?\s*(E\d\d|·)/.test(t))return {kind:'cite',cite:t.replace(/^\[|\]$/g,'').trim()};
  if((m=t.match(/^(R\d\d[a-z]?)(?:\s+(.+))?$/)))return {kind:'reg',hit:reg.find(r=>r.id===m[1])||null,id:m[1],loc:m[2]||''};
  if((m=t.match(/pubmed\.ncbi\.nlm\.nih\.gov\/(\d+)/i)||t.match(/^(?:PMID:?\s*)?(\d{6,9})$/i)))return {kind:'pmid',key:m[1],hit:reg.find(r=>r.pmid===m[1])||null};
  if((m=t.match(/(10\.\d{4,9}\/[^\s"<>]+)/)))return {kind:'doi',key:m[1].replace(/[.,;]$/,''),hit:reg.find(r=>r.doi&&r.doi.toLowerCase()===m[1].replace(/[.,;]$/,'').toLowerCase())||null};
  if((m=t.match(/\b(PMC\d+)\b/i)))return {kind:'pmc',key:m[1].toUpperCase(),hit:null};
  return {kind:'?',key:t,hit:null};}
function sdImpOut(c){const S=STR.st,src=ST.ctx.src,p=sdImpParse(ST.imp.text,src);if(!p)return `<p class="sm mut">${esc(S.importNone)}</p>`;
  let cite;if(p.kind==='cite')cite=p.cite;
  else if(p.hit){const loc=(ST.imp.loc||p.loc||'').trim(),sec=(ST.imp.sec||'').trim();cite=(sec?sec+' · ':'· ')+p.hit.id+(loc?' '+loc:'');}
  else{const key=p.key||ST.imp.text.trim();return `<p class="sm bad">${esc(S.notInReg)}</p><label class="sm" for="sdRegRow">${esc(S.regRow)}</label>
    <textarea id="sdRegRow" readonly rows="3">| R05? | <authors>. <title>. <journal> <year>. ${esc(p.kind==='doi'?'doi:'+key:p.kind==='pmid'?'PMID '+key:key)} | <used for> | <licence> → <our use> |</textarea>`;}
  const v=validateCitation(cite,src),mk=suggestMark(v.parsed,null,src),txt=(ST.imp.fact||'').trim(),line=`${txt||'<fact in our words>'} [${cite}] ${mk}`;
  return `${p.hit?`<p class="sm"><b>${esc(p.hit.id)}</b> · ${esc(p.hit.name)} · ${esc(S.tier(p.hit.tier))}${p.hit.ref_only?` · <span class="badge">${esc(S.refOnly)}</span>`:''}<br><span class="xs mut">${esc(p.hit.licence)}</span></p>`:''}
   <p class="sm"><b>${esc(S.lineT)}</b></p><p class="st-cline">${esc(line)}</p>
   <p class="xs">${v.errors.length?`<span class="bad">✗ ${esc(v.errors.join('; '))}</span>`:`<span class="ok">✓ ${esc(S.citeOk)}</span> · ${esc(S.suggested(mk))}`}</p>
   <div class="row"><button type="button" class="btn sm" data-st-act="addimp"${v.errors.length||!txt?' disabled':''}>+ ${esc(S.addAsFact)}</button><button type="button" class="btn sm" data-st-act="copyline" data-line="${esc(line)}">${esc(S.copyLine)}</button></div>`;}
function sdImpRefresh(){const c=sdCard(ROUTE.id),o=$('#sdImpOut');if(c&&o)o.innerHTML=sdImpOut(c);}
function sdSrcHtml(c){const S=STR.st,src=ST.ctx.src,ch=c.id.slice(0,3);if(!ST.imp.sec)ST.imp.sec=(MAPD.byId[c.id]||{}).sec||'';
  const secs=Object.entries(src.sections).filter(([k])=>k.startsWith(ch+'.'));
  return `<div class="st-fl wide"><label for="sdImp" class="st-big">${esc(S.importT)}</label><input type="text" id="sdImp" data-st-imp="text" value="${esc(ST.imp.text)}" placeholder="${esc(S.importPh)}" autocomplete="off" spellcheck="false"></div>
   <div class="st-grid"><div class="st-fl"><label for="sdImpSec">${esc(S.secT)}</label><input type="text" id="sdImpSec" data-st-imp="sec" value="${esc(ST.imp.sec)}" spellcheck="false"></div>
   <div class="st-fl"><label for="sdImpLoc">${esc(S.locT)}</label><input type="text" id="sdImpLoc" data-st-imp="loc" value="${esc(ST.imp.loc)}" placeholder="CS7" spellcheck="false"></div></div>
   <div class="st-fl wide"><label for="sdImpTxt">${esc(S.fText)}</label><textarea id="sdImpTxt" data-st-imp="fact" rows="2">${esc(ST.imp.fact)}</textarea></div>
   <div id="sdImpOut" aria-live="polite">${sdImpOut(c)}</div>
   <h3>${esc(S.sectionsT(ch))}</h3><div class="links">${secs.map(([k,t])=>`<button type="button" class="lk" data-st-sec="${esc(k)}" title="${esc(t)}"><span class="mono">${esc(k)}</span> ${esc(t.length>34?t.slice(0,33)+'…':t)}</button>`).join('')}</div>
   <details class="st-reg"><summary>${esc(S.registryT)} (${src.registry.length})</summary><ul class="sm">${src.registry.map(r=>`<li><b class="mono">${esc(r.id)}</b> · ${esc(r.name)} · ${esc(S.tier(r.tier))}${r.ref_only?` · ${esc(S.refOnly)}`:''}</li>`).join('')}</ul></details>`;}

/* ---------- clicks ---------- */
document.addEventListener('click',e=>{
  if(ROUTE.name!=='studio'&&ROUTE.name!=='calib')return;
  const cal=e.target.closest('[data-cal]');if(cal){ST.cal[cal.dataset.cal]=cal.dataset.m;render();return;}
  if(e.target.closest('[data-cal-retry]')){CD.err=null;render();return;}
  if(ROUTE.name!=='studio')return;
  const a=e.target.closest('[data-st-act]'),c=sdCard(ROUTE.id);
  if(a){const k=a.dataset.stAct;
    if(k==='new'){sdNew($('#sdNew').value);return;}
    if(k==='retry'){CD.err=null;render();return;}
    if(!c)return;
    const nid=(arr,p)=>p+(Math.max(0,...arr.map(x=>+String(x.id).slice(1)||0))+1);
    if(k==='copy'||k==='download')dlog('studio','export',k,c.id,c.status,'v'+c.version);
    if(k==='copy'){sdCopy(JSON.stringify(c,null,1)+'\n',STR.st.copiedJson);ST.orig[c.id]=JSON.stringify(c);sdLive(true);return;}
    if(k==='download'){const b=new Blob([JSON.stringify(c,null,1)+'\n'],{type:'application/json'}),u=URL.createObjectURL(b),l=document.createElement('a');l.href=u;l.download=c.id+'.json';document.body.appendChild(l);l.click();l.remove();setTimeout(()=>URL.revokeObjectURL(u),2000);ST.orig[c.id]=JSON.stringify(c);sdLive(true);return;}
    const content={addfact:()=>c.facts.push({id:nid(c.facts,'f'),text:'',cite:(MAPD.byId[c.id]||{}).sec||'',mark:'≈',where:'main'}),rmfact:()=>c.facts.splice(+a.dataset.i,1),
      addmis:()=>c.misconceptions.push({id:nid(c.misconceptions,'m'),wrong:'',right:'',cite:'',mark:'✔'}),
      addcheck:()=>c.checks.push({id:nid(c.checks,'q'),type:'mcq',prompt:'',options:['','',''],answer:0,why:'',tests:'objective'}),
      addlevel:()=>{c.body[a.dataset.l]='';},addrem:()=>{c.remember=c.remember||[];c.remember.push({id:nid(c.remember,'r'),q:'',a:''});},rmrem:()=>c.remember.splice(+a.dataset.i,1),rmlevel:()=>{delete c.body[a.dataset.l];},
      addimp:()=>{const p=sdImpParse(ST.imp.text,ST.ctx.src),cite=p.kind==='cite'?p.cite:((ST.imp.sec?ST.imp.sec+' · ':'· ')+p.hit.id+((ST.imp.loc||p.loc)?' '+(ST.imp.loc||p.loc):'')),v=validateCitation(cite,ST.ctx.src);
        c.facts.push({id:nid(c.facts,'f'),text:ST.imp.fact.trim(),cite,mark:suggestMark(v.parsed,null,ST.ctx.src),where:v.parsed&&v.parsed.sections.length?'main':'more'});toast(STR.st.added);}};
    if(content[k]){content[k]();sdTouched(c);
      const fo={addfact:()=>sdPid(`facts.${c.facts.length-1}.text`),addmis:()=>sdPid(`misconceptions.${c.misconceptions.length-1}.wrong`),addcheck:()=>sdPid(`checks.${c.checks.length-1}.prompt`),addlevel:()=>sdPid('body.'+a.dataset.l),addrem:()=>sdPid(`remember.${c.remember.length-1}.q`)}[k];
      ST.focus=fo?fo():'sdDraftH';render();return;}
    if(k==='copyline'){sdCopy(a.dataset.line,STR.st.lineCopied);return;}
    const g=ROUTE.gate||'G-Sci';
    if(k==='pass'||k==='fail'){sdDecide(c,g,k);return;}
    if(k==='fixprompt'){sdCopy(sdFixPrompt(c,g),STR.copied);return;}
    return;}
  const gb=e.target.closest('[data-st-gate]');if(gb&&c){go({name:'studio',id:c.id,gate:gb.dataset.stGate},{replace:true});return;}
  const lb=e.target.closest('[data-st-v]');if(lb&&c){const g=ROUTE.gate||'G-Sci',r=sdRv(c.id,g),ln=lb.dataset.ln,v=lb.dataset.stV;r.lines[ln]=r.lines[ln]===v?'':v;sdRvRefresh();
    if(r.lines[ln]==='fix'){const n=document.getElementById('sdN-'+ln);if(n)n.focus();}else{const b=$(`[data-st-v="${v}"][data-ln="${CSS.escape(ln)}"]`);if(b)b.focus({preventScroll:true});}return;}
  const ck=e.target.closest('[data-st-ck]');if(ck&&c){const r=sdRv(c.id,ROUTE.gate||'G-Sci');r.checklist[ck.dataset.stCk]=ck.checked;sdRvRefresh();return;}
  const sb=e.target.closest('[data-st-sec]');if(sb){ST.imp.sec=sb.dataset.stSec;const i=$('#sdImpSec');if(i)i.value=ST.imp.sec;sdImpRefresh();return;}
  const fl=e.target.closest('[data-st-line]');if(fl&&c){sdFocusLine(c,fl.dataset.stLine);return;}
});
function sdFocusLine(c,ln){let id=null;const ri=(c.remember||[]).findIndex(r=>r&&r.id===ln),fi=c.facts.findIndex(f=>f.id===ln),mi=c.misconceptions.findIndex(m=>m.id===ln),qi=c.checks.findIndex(q=>q.id===ln),m=ln.match(/^body\.(\w+)/);
  if(ri>=0)id=sdPid(`remember.${ri}.q`);else if(fi>=0)id=sdPid(`facts.${fi}.text`);else if(mi>=0)id=sdPid(`misconceptions.${mi}.wrong`);else if(qi>=0)id=sdPid(`checks.${qi}.prompt`);else if(m)id=sdPid('body.'+m[1]);
  else id={obj:sdPid('objective.text'),terms:sdPid('terms.new'),scene:sdPid('scene.id'),adult:sdPid('adult'),clinical:sdPid('clinical'),shows_up:sdPid('shows_up'),remember:sdPid('remember.0.q'),card:sdPid('title'),checks:sdPid('checks.0.prompt')}[ln];
  let el=id&&document.getElementById(id);if(!el||!el.offsetParent)el=document.getElementById('ln-'+ln.replace(/\./g,'-'));   // phone: the review line
  if(el){el.scrollIntoView({block:'center'});if(el.matches('input,textarea,select'))el.focus({preventScroll:true});else{el.setAttribute('tabindex','-1');el.focus({preventScroll:true});}}}

/* ---------- #calib: score 5 dossier facts ---------- */
SCREENS.calib=function(v){
  const S=STR.st;ROUTE.crumbs=[{label:S.title,hash:'studio'},{label:S.calTitle}];window.ST_READY=null;
  if(!FLAGS.test){go('studio',{replace:true});return;}
  if(!CD.cal||!ST.ctx){v.innerHTML=`<h1>${esc(S.calTitle)}</h1><p class="${CD.err?'bad':'mut'}" role="status">${esc(CD.err?S.loadFail+' ('+CD.err+')':S.loading)}</p>${CD.err?`<button type="button" class="btn" data-cal-retry data-fk="retry">${esc(STR.retry||'Retry')}</button>`:''}`;
    if(!CD.err)Promise.all([sdLoad(),cdCal()]).then(()=>{if(ROUTE.name==='calib')render();},e=>{CD.err=CD.err||e.message;if(ROUTE.name==='calib')render();});return;}
  const src=ST.ctx.src,F=CD.cal.facts.map(f=>{const vv=validateCitation(f.cite,src);return Object.assign({},f,{sug:suggestMark(vv.parsed,f.decision,src),errs:vv.errors});});
  const you=F.filter(f=>ST.cal[f.id]===f.mark).length,rules=F.filter(f=>f.sug===f.mark&&!f.errs.length).length;
  v.innerHTML=`<h1 id="cpT">${esc(S.calTitle)}</h1><p class="mut" style="max-width:var(--measure)">${esc(S.calLead)}</p>
   <p class="card st-score" role="status"><b>${esc(S.calScore(you,F.length,rules))}</b></p>
   <div class="st-cal">${F.map(f=>{const p=ST.cal[f.id];return `<section class="card"><p>${esc(f.text)}</p><p class="mono xs">[${esc(f.cite)}]${f.decision?' · '+esc(f.decision):''} · ${esc(f.concept)}</p>
     <div class="seg" role="group" aria-label="${esc(S.calYou)} ${esc(f.id)}">${CARD_RULES.marks.map(m=>`<button type="button" data-cal="${esc(f.id)}" data-m="${esc(m)}" data-fk="cal-${esc(f.id)}-${esc(m)}" aria-pressed="${p===m}" aria-label="${esc(m+' '+(STR.marks[m]||''))}" title="${esc(STR.marks[m])}">${esc(m)}</button>`).join('')}</div>
     ${p?`<p class="sm">${esc(S.calYou)} <b>${esc(p)}</b> ${p===f.mark?'<span class="ok">✓</span>':'<span class="bad">✗</span>'} · ${esc(S.calDossier)} <b>${esc(f.mark)}</b> · ${esc(S.calRules)} <b>${esc(f.sug)}</b> ${f.sug===f.mark?'<span class="ok">✓</span>':'<span class="bad">✗</span>'}</p><p class="xs mut">${esc(STR.marks[f.mark])}</p>`:''}</section>`;}).join('')}</div>
   <section class="card"><h2>${esc(S.calRulesT)}</h2><p class="sm">${esc(S.calRules1)}</p>${editBtn('file','calibration',CONFIG.cards.dir+'calibration.json')}</section>`;
  window.ST_READY='calib';
};
