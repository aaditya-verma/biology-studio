/* Biology Studio — learning core (L1): card list #cards · card reader #card=<id> · Remember deck #deck · Today's review queue.
   Owner docs: docs/card-spec.md §7 (how the reader uses a card), build/design-plan.md §2 (Card row) + §4.8, master plan §9; RULES B4, A1, C13, H1, H5.
   Statuses (B4): Read (card open CONFIG.learn.readMs) → Understood (its Check passed: every question right in one run) → Can explain (self-check after Understood).
   Remember deck: each card's remember[] prompts join on Read; spacing CONFIG.learn.deckDays (1 · 3 · 7 days). Saved in IndexedDB `biostudio` (state.cards, state.deck — add-only, A1).
   Try it = the card's scene in the V1 viewer, inline (13-viewer.js scViewer(…,{inline:true})). Watch it = "Coming soon" until L3.
   Layout per class (C13): phone = 3D on top, text below · phone landscape = 3D │ text · tablet portrait = 3D on top, text at reading width ·
   tablet landscape = 3D │ text · desktop = 3D │ text │ card rail. Partial repaints (check, level, explain) keep the 3D, scroll and focus.
   EDIT: words in STR.ln; settings in CONFIG.learn; card data in content/<book>/cards/ (never in code). */
'use strict';
const LN={idx:null,err:null,ck:{},ex:{},open:{},gone:new Set(),readT:0,deck:null};   // gone = cards that failed to load (kept apart so the reader retries, G-Eng)
const DAY=864e5;
const lnDay0=t=>{const d=new Date(t);d.setHours(0,0,0,0);return d.getTime();};
const lnAddDays=(t,n)=>{const d=new Date(lnDay0(t));d.setDate(d.getDate()+n);return d.getTime();};
const lnDayLabel=t=>{const d0=lnDay0(Date.now());return t<=d0?STR.ln.todayW:t<=d0+DAY+36e5?STR.ln.tomorrow:STR.ln.day(t);};

/* ---------- data ---------- */
const lnVisible=m=>m&&m.status!=='retired'&&(CONFIG.learn.show.includes(m.status)||FLAGS.test);
function lnLoad(){return cdIndex().then(j=>{LN.idx=j;return j;}).catch(e=>{LN.err=e.message;throw e;});}
const lnList=()=>LN.idx?LN.idx.cards.filter(lnVisible):[];
async function lnCard(id){const c=await cdCard(id);LN.open[id]=c;LN.gone.delete(id);return c;}
const lnShuffle=a=>{const r=a.slice();for(let i=r.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[r[i],r[j]]=[r[j],r[i]];}return r;};

/* ---------- statuses (B4) ---------- */
const lnRec=id=>state.cards[id]||(state.cards[id]={checks:0,best:0,t:0});
function lnStatus(id){const c=state.cards[id];return !c?'none':c.exp?'exp':c.und?'und':c.read?'read':'none';}
function lnSet(id,k){const c=lnRec(id);if(c[k])return false;c[k]=Date.now();c.t=c[k];dlog('learn',id,k);stSave();return true;}
/* a ring that fills by step (0 · ⅓ · ⅔ · full) + the word: shape and text, never colour alone (H5); SVG, so no font can drop it */
const lnPie=s=>{const f={none:0,read:1/3,und:2/3,exp:1}[s],a=f*2*Math.PI,x=(7+6*Math.sin(a)).toFixed(2),y=(7-6*Math.cos(a)).toFixed(2);
  return `<svg class="ln-pie" viewBox="0 0 14 14" width="14" height="14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-width="1.6"/>${f>=1?'<circle cx="7" cy="7" r="6" fill="currentColor"/>':f>0?`<path d="M7 7V1A6 6 0 ${f>.5?1:0} 1 ${x} ${y}z" fill="currentColor"/>`:''}</svg>`;};
const lnChip=id=>{const s=lnStatus(id);return `<span class="ln-st st-${s}" title="${esc(STR.ln.stHelp[s])}">${lnPie(s)} ${esc(STR.ln.st[s])}</span>`;};

/* ---------- Remember deck ---------- */
function lnDeckAdd(card){const now=Date.now();let n=0;
  for(const r of card.remember||[]){const k=card.id+'#'+r.id;if(!state.deck[k]){state.deck[k]={step:0,due:lnAddDays(now,CONFIG.learn.deckDays[0]),n:0,lapses:0,t:now};n++;}}
  if(n){dlog('learn','deck +',n,card.id);stSave();}return n;}
/* the live deck: prompts of cards a learner can see; once a card is loaded, only the prompts it still has (one filter for Today, Cards and #deck — G-Eng) */
const lnDeckLive=x=>{const m=LN.idx&&LN.idx.cards.find(c=>c.id===x.id);if(LN.idx&&!lnVisible(m))return false;const c=LN.open[x.id];return !c||(c.remember||[]).some(r=>r.id===x.r);};
const lnDeckAll=()=>Object.entries(state.deck).map(([k,v])=>({k,id:k.split('#')[0],r:k.split('#')[1],...v})).filter(lnDeckLive);
const lnDeckDue=()=>{const now=Date.now();return lnDeckAll().filter(x=>x.due<=now).sort((a,b)=>a.due-b.due||a.k.localeCompare(b.k));};
const lnNextDue=()=>{const a=lnDeckAll().sort((a,b)=>a.due-b.due);return a.length?a[0].due:null;};
/* got → next step (1 → 3 → 7 → 7 days); not yet → back to step 0 (+1 day) */
function lnDeckGrade(k,ok){const d=state.deck[k];if(!d)return;const D=CONFIG.learn.deckDays,now=Date.now();
  if(ok){d.step=(d.step||0)+1;d.due=lnAddDays(now,D[Math.min(d.step,D.length-1)]);}else{d.step=0;d.due=lnAddDays(now,D[0]);d.lapses=(d.lapses||0)+1;}
  d.n=(d.n||0)+1;d.t=now;dlog('learn','deck',k,ok?'got':'not yet','→',new Date(d.due).toDateString());stSave();}

/* ---------- text helpers ---------- */
const lnLevels=card=>{const L=CONFIG.learn.levels.filter(l=>card.body[l]);for(const l of Object.keys(card.body))if(!L.includes(l))L.push(l);return L;};
const lnLevel=card=>{const L=lnLevels(card),l=state.settings.level;return L.includes(l)?l:L[0];};
const lnFact=(card,id)=>card.facts.find(f=>f.id===id);
/* a sentence keeps its refs as one small inline link-button that opens the facts behind it (cite + mark). Inline in the sentence, so the
   44 px target rule's inline exception applies (WCAG 2.5.8; layout-audit skips inline <a>); Enter and Space both open it. */
function lnRich(card,text,key){let n=0;
  return esc(text).replace(/\s*\[(f\d+(?:\s*,\s*f\d+)*)\]([.,;:!?]?)/g,(m,ids,pu)=>{const k=key+'-'+(n++),list=ids.split(',').map(s=>s.trim());
    return `<a href="#" role="button" class="ln-ref" data-ln="ref" data-k="${k}" aria-expanded="false" aria-controls="lnR-${k}" aria-label="${esc(STR.ln.factsFor(list.map(x=>x.slice(1))))}">${list.map(x=>x.slice(1)).join(',')}</a><span class="ln-refbox hidden" id="lnR-${k}" role="note">${list.map(x=>{const f=lnFact(card,x);return f?`<span>${esc(f.text)} <span class="xs mut">[${esc(f.cite)}]</span> <b class="mark" title="${esc(STR.marks[f.mark]||'')}">${esc(f.mark)}</b></span>`:'';}).join('')}</span>`.replace(/^/,pu);});}   // punctuation first: the ref and its box follow the sentence (G-A11y)
const lnPlain=t=>stripRefs(t);
const lnFactLi=f=>`<li><span>${esc(f.text)}</span> <span class="xs mut">[${esc(f.cite)}]</span> <b class="mark" title="${esc(STR.marks[f.mark]||'')}">${esc(f.mark)}</b>${f.decision?` <span class="xs mut">${esc(f.decision)}</span>`:''}</li>`;

/* ---------- #cards ---------- */
SCREENS.cards=function(v){
  ROUTE.crumbs=[{label:STR.ln.cardsT}];
  if(!LN.idx){v.innerHTML=`<h1>${esc(STR.ln.cardsT)}</h1><p class="mut" role="status">${esc(LN.err?STR.ln.loadFail+' ('+LN.err+')':STR.ln.loading)}</p>`;
    if(!LN.err)lnLoad().then(()=>{if(ROUTE.name==='cards')render();},()=>{if(ROUTE.name==='cards')render();});return;}
  const L=lnList(),cnt={none:0,read:0,und:0,exp:0};L.forEach(c=>cnt[lnStatus(c.id)]++);
  const groups={};for(const c of L){const g=c.id.slice(0,3);(groups[g]||(groups[g]=[])).push(c);}
  const order=CONFIG.learn.groups.filter(g=>groups[g]).concat(Object.keys(groups).filter(g=>!CONFIG.learn.groups.includes(g)).sort());
  const due=lnDeckDue().length,all=lnDeckAll().length;
  v.innerHTML=`<h1>${esc(STR.ln.cardsT)}</h1><p class="mut ln-lead">${esc(STR.ln.cardsLead)}</p>
  <div class="ln-list">
    <section class="card ln-sum" aria-labelledby="lnSumT"><h2 id="lnSumT">${esc(STR.ln.progressT)}</h2>
      <ul class="ln-counts">${['none','read','und','exp'].map(s=>`<li><span class="ln-st st-${s}">${lnPie(s)} ${esc(STR.ln.st[s])}</span> <b>${cnt[s]}</b></li>`).join('')}</ul>
      <h3 class="sm">${esc(STR.ln.deckT)}</h3><p class="sm">${esc(all?(due?STR.ln.due(due):STR.ln.dueNone):STR.ln.deckEmpty)}</p>
      ${all?`<button type="button" class="btn${due?' pri':''}" data-go="deck">${esc(due?STR.ln.deckStart(due):STR.ln.deckT)}</button>`:''}</section>
    ${order.map(g=>`<section class="card ln-grp" aria-labelledby="lnG-${esc(g)}"><h2 id="lnG-${esc(g)}">${esc(STR.ln.groups[g]||STR.ln.groupOf(g))}</h2>
      ${groups[g].map(c=>`<button type="button" class="lrow ln-row" data-go="card=${esc(c.id)}"><span class="nm">${esc(c.title)}</span>${lnChip(c.id)}<span class="id">${esc(c.id)}</span></button>`).join('')}</section>`).join('')}
  </div>${editBtn('screen','cards','src/js/18-learn.js + content/strings.js')}`;
  window.LN_READY='cards';   // tools/layout-check waits for this
};

/* ---------- #card=<id> ---------- */
SCREENS.card=function(v){
  const id=ROUTE.id;
  ROUTE.crumbs=[{label:STR.ln.cardsT,hash:'cards'},{label:(LN.open[id]&&LN.open[id].title)||id}];
  const meta=LN.idx&&LN.idx.cards.find(c=>c.id===id),card=LN.open[id];LN.gone.delete(id);
  if(!LN.idx||!card){v.innerHTML=`<p class="mut" role="status">${esc(STR.ln.loading)}</p>`;
    Promise.all([LN.idx?null:lnLoad(),lnCard(id),scIndexLoad()]).then(()=>{if(ROUTE.name==='card'&&ROUTE.id===id)render();})
      .catch(e=>{if(ROUTE.name==='card'&&ROUTE.id===id)v.innerHTML=`<div class="card"><h1>${esc(STR.ln.cardsT)}</h1><p>${esc(STR.ln.noCard(id))} <span class="xs mut">${esc(e.message)}</span></p><button type="button" class="btn" data-go="cards">${esc(STR.ln.cardsT)}</button></div>`;});return;}
  if(!lnVisible(meta)){v.innerHTML=`<div class="card"><h1>${esc(card.title)}</h1><p>${esc(STR.ln.notYet)}</p><button type="button" class="btn" data-go="cards">${esc(STR.ln.cardsT)}</button></div>`;return;}
  state.last.card=id;
  /* Read after readMs on the card (B4); the deck takes its prompts then */
  clearTimeout(LN.readT);if(!state.cards[id]||!state.cards[id].read)LN.readT=setTimeout(()=>{if(ROUTE.name==='card'&&ROUTE.id===id){lnSet(id,'read');lnDeckAdd(card);lnPaint('status');lnPaint('remember');}},CONFIG.learn.readMs);
  const lv=lnLevel(card),L=lnLevels(card),sc=card.scene&&card.scene.id,list=lnList(),i=list.findIndex(c=>c.id===id),prev=list[i-1],next=list[i+1];
  const grp=list.filter(c=>c.id.slice(0,3)===id.slice(0,3));
  v.innerHTML=`<div class="ln-card" id="lnCard" data-id="${esc(id)}">
  <header class="ln-head"><div class="row"><span class="mono mut">${esc(id)} · ${esc(STR.tierShort(card.tier))}${card.kind==='guide'?' · ⓘ':''}</span><span class="sp"></span><span id="lnStatus">${lnChip(id)}</span>${editBtn('card',id,CONFIG.cards.dir+id+'.json')}</div>
      <h1 id="cpT" tabindex="-1">${esc(card.title)}</h1>
      ${L.length>1?`<div class="seg ln-lv" role="group" aria-label="${esc(STR.ln.level)}">${L.map(l=>`<button type="button" data-ln="level" data-l="${esc(l)}" aria-pressed="${l===lv}">${esc(STR.ln.levels[l]||l)}</button>`).join('')}</div><p class="xs mut">${esc(STR.ln.levelHelp)}</p>`:''}
    <section class="ln-obj"><h2 class="ln-h">${esc(STR.ln.objT)}</h2><p><b>${esc(card.objective.text)}</b></p></section></header>
  <div class="ln-media">
    <section class="ln-try" aria-labelledby="lnTryT"><div class="row"><h2 id="lnTryT" class="ln-h">${esc(STR.ln.tryT)}</h2><span class="xs mut">${esc(STR.ln.tryLead)}</span></div><div id="lnVw"></div></section>
    <section class="ln-watch" aria-labelledby="lnWatchT"><h2 id="lnWatchT" class="ln-h">${esc(STR.ln.watchT)}</h2><span class="badge">${esc(STR.ln.soon)}</span><span class="xs mut">${esc(STR.ln.watchSoon)}</span></section>
  </div>
  <article class="ln-text" aria-labelledby="cpT">

    <section class="ln-body" id="lnBody">${lnBodyHtml(card,lv)}</section>
    ${card.adult?`<section class="ln-adult"><h2 class="ln-h">${esc(STR.ln.adultT)}</h2><p>${lnRich(card,card.adult,'adult')}</p></section>`:''}
    ${card.clinical?`<section class="ln-clin"><h2 class="ln-h">${esc(STR.ln.clinicalT)}</h2><p>${lnRich(card,card.clinical,'clin')}</p></section>`:''}
    ${card.misconceptions.length?`<section class="ln-mis"><h2 class="ln-h">${esc(STR.ln.misT)}</h2>${card.misconceptions.map(m=>`<div class="ln-mi"><p><span class="ln-x" aria-hidden="true">✗</span> <span class="sr">${esc(STR.ln.wrongL)}</span><s>${esc(m.wrong)}</s></p><p><span class="ln-ok" aria-hidden="true">✓</span> <span class="sr">${esc(STR.ln.rightL)}</span>${esc(m.right)} <span class="xs mut">[${esc(m.cite)}]</span> <b class="mark" title="${esc(STR.marks[m.mark]||'')}">${esc(m.mark)}</b></p></div>`).join('')}</section>`:''}
    <section class="ln-check card" id="lnCheck" aria-labelledby="lnCkT">${lnCheckHtml(card)}</section>
    <section class="ln-expl" id="lnExpl" aria-labelledby="lnExT">${lnExplHtml(card)}</section>
    <section class="ln-rem" id="lnRem" aria-labelledby="lnRmT">${lnRemHtml(card)}</section>
    ${card.shows_up&&card.shows_up.length?`<section class="ln-shows"><h2 class="ln-h">${esc(STR.ln.showsT)}</h2><div class="ln-chips">${card.shows_up.map(x=>{const c=LN.idx.cards.find(q=>q.id===x&&lnVisible(q)),m=MAPD.byId[x];
      return `<button type="button" class="btn sm" data-go="${c?'card='+esc(x):'concept='+esc(x)}">${esc(c?c.title:m?m.name:x)} <span class="xs mut">${esc(x)}</span></button>`;}).join('')}</div></section>`:''}
    ${card.facts.some(f=>f.where==='more')?`<details class="ln-more"><summary><span class="ln-h">${esc(STR.ln.moreT)}</span></summary><p class="xs mut">${esc(STR.ln.moreLead)}</p><ul class="ln-facts sm">${card.facts.filter(f=>f.where==='more').map(lnFactLi).join('')}</ul></details>`:''}
    <details class="ln-src"><summary><span class="ln-h">${esc(STR.ln.sourcesT)}</span></summary><ul class="ln-facts sm">${card.facts.filter(f=>f.where==='main').map(lnFactLi).join('')}</ul><p class="xs mut">${esc(STR.ln.marksKey)}</p></details>
    <nav class="ln-pn row" aria-label="${esc(STR.ln.cardRail)}">${prev?`<button type="button" class="btn" data-go="card=${esc(prev.id)}">${icon('back',18)} ${esc(prev.title)}</button>`:''}<span class="sp"></span>${next?`<button type="button" class="btn" data-go="card=${esc(next.id)}">${esc(next.title)} ${icon('fwd',18)}</button>`:''}</nav>
  </article>
  <nav class="ln-rail card" aria-label="${esc(STR.ln.cardRail)}"><h2 class="ln-h">${esc(STR.ln.groups[id.slice(0,3)]||STR.ln.groupOf(id.slice(0,3)))}</h2>
    ${grp.map(c=>`<button type="button" class="lrow ln-row" data-go="card=${esc(c.id)}"${c.id===id?' aria-current="page"':''}><span class="nm">${esc(c.title)}</span>${lnChip(c.id)}</button>`).join('')}</nav>
  </div>`;
  /* Try it: the card's scene, inline (one engine + canvas, V1) */
  const host=$('#lnVw');
  SC.inline=sc||null;
  if(sc&&host){
    scFile(sc).then(S=>{if(ROUTE.name!=='card'||ROUTE.id!==id||!$('#lnVw'))return;
      const st=SC.st[S.id]||(SC.st[S.id]={});if(card.scene.day!=null&&(LN.lastCard!==id||st.day==null))st.day=card.scene.day;LN.lastCard=id;   // a new card opens at its own day; rotate / back from full 3D keep yours
      scViewer($('#lnVw'),S,{inline:true});})
    .catch(e=>{const h=$('#lnVw');if(h)h.innerHTML=`<p class="mut sm">${esc(e.message)}</p>`;});}
  window.LN_READY='card='+id;
  if(dbgOn('learn'))DBG.learn=`learn ${id} · ${lnStatus(id)} · level ${lv} · deck ${lnDeckAll().length} (${lnDeckDue().length} due)`;
};
function lnBodyHtml(card,lv){return `<h2 class="sr">${esc(STR.ln.levels[lv]||lv)}</h2><p>${lnRich(card,card.body[lv],'b')}</p>`;}

/* ---------- Check (H1: Checks test the objective; one right answer; explain on a miss) ---------- */
function lnCkNew(card){const perm=q=>{const ix=q.options.map((_,k)=>k);let p=lnShuffle(ix);for(let n=0;q.type==='order'&&n<20&&p.every((k,j)=>k===j);n++)p=lnShuffle(ix);return p;};   // an order item never starts solved (G-Eng, G-Learn)
  return {i:0,res:[],perm:Object.fromEntries(card.checks.map(q=>[q.id,perm(q)])),pick:null,done:false};}
function lnCheckHtml(card){const id=card.id,ck=LN.ck[id],n=card.checks.length,rec=state.cards[id]||{};
  const head=`<h2 id="lnCkT" class="ln-h">${esc(STR.ln.checkT)}</h2>`;
  if(!ck)return head+`<p class="sm">${esc(STR.ln.checkLead(n))}</p>${rec.und?`<p class="sm"><span class="ln-ok" aria-hidden="true">✓</span> ${esc(STR.ln.passedBefore)}</p>`:''}<button type="button" class="btn pri" data-ln="start" data-fk="ln-start">${esc(rec.und?STR.ln.checkAgain:STR.ln.checkStart)}</button>`;
  if(ck.done){const r=ck.res.filter(Boolean).length,pass=r===n;
    return head+`<p class="ln-res" tabindex="-1" id="lnRes"><span class="${pass?'ln-ok':'ln-x'}" aria-hidden="true">${pass?'✓':'✗'}</span> ${esc(pass?STR.ln.passed(r,n):STR.ln.failed(r,n))}</p><button type="button" class="btn" data-ln="start" data-fk="ln-start">${esc(STR.ln.checkAgain)}</button>`;}
  const q=card.checks[ck.i],perm=ck.perm[q.id],answered=ck.pick!==null,last=ck.i===n-1;
  let body='';
  if(q.type==='mcq'){body=`<div class="ln-opts" role="group" aria-labelledby="lnQ">${perm.map(k=>{const right=k===q.answer,mine=ck.pick===k;
      const mark=answered?(right?' ok':mine?' no':''):'';
      return `<button type="button" class="ln-opt${mark}" data-ln="pick" data-o="${k}" ${answered?'aria-disabled="true"':''} data-fk="ln-o${k}">${answered&&(right||mine)?`<span aria-hidden="true">${right?'✓':'✗'}</span> `:''}${esc(q.options[k])}${answered&&right?` <span class="sr">— ${esc(STR.ln.right)}</span>`:answered&&mine?` <span class="sr">— ${esc(STR.ln.wrong)}</span>`:''}</button>`;}).join('')}</div>`;}
  else{const ord=ck.ord||(ck.ord=perm.slice());
    body=`<p class="xs mut">${esc(STR.ln.orderHint)}</p><ol class="ln-order">${ord.map((k,j)=>`<li><span class="ln-ot">${esc(q.options[k])}</span>${answered?(ck.pickOk[j]?` <span class="ln-ok" aria-hidden="true">✓</span><span class="sr"> — ${esc(STR.ln.rightPlace)}</span>`:` <span class="ln-x" aria-hidden="true">✗</span><span class="sr"> — ${esc(STR.ln.wrongPlace)}</span>`):`<span class="ln-mv"><button type="button" class="btn icon" data-ln="mv" data-j="${j}" data-d="-1" aria-label="${esc(STR.ln.up(q.options[k]))}" ${j===0?'disabled':''} data-fk="ln-u${k}">${icon('up',18)}</button><button type="button" class="btn icon ln-dn" data-ln="mv" data-j="${j}" data-d="1" aria-label="${esc(STR.ln.down(q.options[k]))}" ${j===ord.length-1?'disabled':''} data-fk="ln-d${k}">${icon('up',18)}</button></span>`}</li>`).join('')}</ol>
      ${answered?'':`<button type="button" class="btn pri" data-ln="order" data-fk="ln-order">${esc(STR.ln.checkOrder)}</button>`}`;}
  const ok=answered&&ck.res[ck.i];
  const fb=answered?`<div class="ln-fb" id="lnFb" tabindex="-1"><p><b><span class="${ok?'ln-ok':'ln-x'}" aria-hidden="true">${ok?'✓':'✗'}</span> ${esc(ok?STR.ln.right:STR.ln.wrong)}</b>
      ${!ok&&q.type==='mcq'?' '+esc(STR.ln.rightWas(q.options[q.answer])):''}</p>
      ${!ok&&q.type==='order'?`<p class="sm">${esc(STR.ln.rightOrder)}</p><ol class="sm">${q.options.map(o=>`<li>${esc(o)}</li>`).join('')}</ol>`:''}
      <p class="sm">${esc(q.why)}</p>
      <button type="button" class="btn pri" data-ln="next" data-fk="ln-next">${esc(last?STR.ln.finish:STR.ln.next)}</button></div>`:'';
  return head+`<p class="xs mut">${esc(STR.ln.qOf(ck.i+1,n))}</p><p class="ln-q" id="lnQ"><b>${esc(q.prompt)}</b></p>${body}${fb}`;}
function lnCheckAct(card,a,b){const id=card.id;let ck=LN.ck[id],focus=null;
  if(a==='start'){ck=LN.ck[id]=lnCkNew(card);focus='#lnQ';}
  else if(!ck)return;
  else if(a==='pick'){if(ck.pick!==null)return;const q=card.checks[ck.i];ck.pick=+b.dataset.o;ck.res[ck.i]=ck.pick===q.answer;lnLog(card,q,ck.res[ck.i]);focus='#lnFb';}
  else if(a==='mv'){const j=+b.dataset.j,d=+b.dataset.d,o=ck.ord,k=o[j];if(j+d<0||j+d>=o.length)return;[o[j],o[j+d]]=[o[j+d],o[j]];
    const edge=(d<0&&j+d===0)||(d>0&&j+d===o.length-1);focus=`[data-fk="${(d<0)!==edge?'ln-u':'ln-d'}${k}"]`;}   // same button again, or the other one at an end
  else if(a==='order'){const q=card.checks[ck.i];ck.pick=ck.ord.slice();ck.pickOk=ck.ord.map((k,j)=>k===j);ck.res[ck.i]=ck.pickOk.every(Boolean);lnLog(card,q,ck.res[ck.i]);focus='#lnFb';}
  else if(a==='next'){if(ck.i<card.checks.length-1){ck.i++;ck.pick=null;ck.ord=null;ck.pickOk=null;focus='#lnQ';}
    else{ck.done=true;const r=ck.res.filter(Boolean).length,rec=lnRec(id);rec.checks=(rec.checks||0)+1;rec.best=Math.max(rec.best||0,r/card.checks.length);rec.t=Date.now();
      if(r===card.checks.length){lnSet(id,'read');lnDeckAdd(card);lnSet(id,'und');}stSave();focus='#lnRes';lnPaint('status');lnPaint('expl');lnPaint('remember');}}
  lnPaint('check');const f=focus&&$(focus);if(f){if(f.id==='lnQ'&&!f.hasAttribute('tabindex'))f.setAttribute('tabindex','-1');f.focus({preventScroll:false});}}
/* every answer is kept (answers store, union-merged — A1): card:<id>:<q> → {t, ok} */
function lnLog(card,q,ok){state.answers['card:'+card.id+':'+q.id]={t:Date.now(),ok,v:card.version};stSave();}

/* ---------- Can explain (after Understood) ---------- */
function lnExplHtml(card){const id=card.id,s=lnStatus(id),ex=LN.ex[id]||{},head=`<h2 id="lnExT" class="ln-h">${esc(STR.ln.explT)}</h2>`;
  if(s==='exp')return head+`<p class="sm"><span class="ln-ok" aria-hidden="true">✓</span> ${esc(STR.ln.explDone)}</p>`;
  if(s!=='und')return head+`<p class="sm mut">${esc(STR.ln.explNeed)}</p>`;
  return head+`<p class="sm">${esc(STR.ln.explLead)}</p><p class="sm"><b>${esc(card.objective.text)}</b></p>
    ${ex.shown?`<div class="ln-model" id="lnModel" tabindex="-1"><h3 class="sm">${esc(STR.ln.explModel)}</h3><p class="sm">${esc(lnPlain(card.body[lnLevel(card)]))}</p></div>
      <div class="row"><button type="button" class="btn pri" data-ln="exyes" data-fk="ln-exyes">${esc(STR.ln.explYes)}</button><button type="button" class="btn" data-ln="exno" data-fk="ln-exno">${esc(STR.ln.explNo)}</button></div>`
    :`<button type="button" class="btn" data-ln="exshow" data-fk="ln-exshow">${esc(STR.ln.explShow)}</button>`}`;}

/* ---------- Remember prompts on the card ---------- */
function lnRemHtml(card){const ks=(card.remember||[]).map(r=>state.deck[card.id+'#'+r.id]).filter(Boolean),nd=ks.length?Math.min(...ks.map(d=>d.due)):null;
  return `<h2 id="lnRmT" class="ln-h">${esc(STR.ln.rememberT)}</h2><p class="xs mut">${esc(ks.length?STR.ln.inDeck+' · '+STR.ln.nextDue(lnDayLabel(nd)):STR.ln.rememberLead((card.remember||[]).length))}</p>
  <ul class="ln-rq">${(card.remember||[]).map(r=>`<li><details><summary>${esc(r.q)}</summary><p class="sm">${esc(lnPlain(r.a))}</p></details></li>`).join('')}</ul>`;}

/* partial repaints: the 3D, scroll and focus stay (no full render) */
function lnPaint(what){const card=LN.open[ROUTE.id];if(ROUTE.name!=='card'||!card)return;
  const el={check:'#lnCheck',expl:'#lnExpl',remember:'#lnRem',status:'#lnStatus'}[what],h=$(el);if(!h)return;
  h.innerHTML=what==='check'?lnCheckHtml(card):what==='expl'?lnExplHtml(card):what==='remember'?lnRemHtml(card):lnChip(card.id);
  if(what==='status')$$('.ln-rail [aria-current] .ln-st').forEach(x=>{x.outerHTML=lnChip(card.id);});}

/* ---------- #deck: one session ---------- */
SCREENS.deck=function(v){
  ROUTE.crumbs=[{label:STR.ln.deckT}];window.LN_READY=null;setTimeout(()=>{if(ROUTE.name==='deck'&&!$('#view [role=status].mut'))window.LN_READY='deck';},0);
  if(!LN.idx&&!LN.err){v.innerHTML=`<p class="mut" role="status">${esc(STR.ln.loading)}</p>`;lnLoad().then(()=>{if(ROUTE.name==='deck')render();},()=>{if(ROUTE.name==='deck')render();});return;}
  const need=[...new Set(lnDeckAll().map(x=>x.id))].filter(id=>!LN.open[id]&&!LN.gone.has(id));
  if(need.length){v.innerHTML=`<p class="mut" role="status">${esc(STR.ln.loading)}</p>`;
    Promise.all(need.map(id=>lnCard(id).catch(()=>{LN.gone.add(id);}))).then(()=>{if(ROUTE.name==='deck')render();});return;}
  const all=lnDeckAll().filter(x=>LN.open[x.id]);
  if(!LN.deck){const due=all.filter(x=>x.due<=Date.now()),nd=lnNextDue();
    v.innerHTML=`<div class="ln-deck"><h1>${esc(STR.ln.deckT)}</h1><p class="mut ln-lead">${esc(STR.ln.deckLead)}</p>
      <section class="card ln-dk">${!all.length?`<p>${esc(STR.ln.deckEmpty)}</p><button type="button" class="btn pri" data-go="cards">${esc(STR.ln.cardsT)}</button>`
      :due.length?`<p><b>${esc(STR.ln.due(due.length))}</b></p><button type="button" class="btn pri" data-ln="dstart" data-fk="ln-dstart">${esc(STR.ln.deckStart(Math.min(due.length,CONFIG.learn.deckSession)))}</button>`
      :`<p>${esc(STR.ln.dueNone)} ${nd?esc(STR.ln.nextOn(lnDayLabel(nd))):''}</p><button type="button" class="btn" data-ln="dstart" data-early="1" data-fk="ln-dstart">${esc(STR.ln.practise)}</button>`}</section></div>`;return;}
  const s=LN.deck;
  if(s.i>=s.q.length){const g=s.got;s.done=true;v.innerHTML=`<div class="ln-deck"><h1>${esc(STR.ln.deckT)}</h1><section class="card ln-dk"><p id="lnDkEnd" tabindex="-1">${esc(STR.ln.deckDone(g,s.n))}${s.early?' '+esc(STR.ln.earlyNote):''}</p>
      <div class="row"><button type="button" class="btn pri" data-go="today">${esc(STR.ln.back)}</button><button type="button" class="btn" data-go="cards">${esc(STR.ln.cardsT)}</button></div></section></div>`;return;}   // kept until you leave #deck (a rotate re-render shows it again)
  const x=s.q[s.i],card=LN.open[x.id],r=card.remember.find(q=>q.id===x.r);
  v.innerHTML=`<div class="ln-deck"><h1>${esc(STR.ln.deckT)}</h1>
    <section class="card ln-dk" aria-labelledby="lnDkQ"><div class="row"><span class="xs mut">${esc(STR.ln.deckLeft(s.q.length-s.i))}</span><span class="sp"></span><button type="button" class="lk xs" data-go="card=${esc(x.id)}">${esc(card.title)} · ${esc(x.id)}</button></div>
      <p class="ln-dq" id="lnDkQ" tabindex="-1"><b>${esc(r.q)}</b></p>
      ${s.shown?`<div class="ln-da" id="lnDkA" tabindex="-1"><p>${esc(lnPlain(r.a))}</p></div>
        <div class="row ln-grade"><button type="button" class="btn pri" data-ln="dgot" data-fk="ln-dgot">✓ ${esc(STR.ln.gotIt)}</button><button type="button" class="btn" data-ln="dno" data-fk="ln-dno">↻ ${esc(STR.ln.notYetD)}</button></div>`
      :`<button type="button" class="btn pri" data-ln="dshow" data-fk="ln-dshow">${esc(STR.ln.showAns)}</button>`}
    </section></div>`;
};
function lnDeckAct(a,b){
  if(a==='dstart'){const all=lnDeckAll().filter(x=>LN.open[x.id]);
    const q=(b.dataset.early?all.sort((p,q)=>p.due-q.due):all.filter(x=>x.due<=Date.now()).sort((p,q)=>p.due-q.due)).slice(0,CONFIG.learn.deckSession);
    LN.deck={q,i:0,n:q.length,got:0,shown:false,again:new Set(),early:!!b.dataset.early};render();$('#lnDkQ')?.focus();return;}
  const s=LN.deck;if(!s||!s.q)return;const x=s.q[s.i];
  if(a==='dshow'){s.shown=true;render();$('#lnDkA')?.focus();return;}
  if(a==='dgot'||a==='dno'){const ok=a==='dgot';
    if(!s.again.has(x.k)){if(x.due<=Date.now())lnDeckGrade(x.k,ok);if(ok)s.got++;}   // the first answer sets the schedule — only for a due prompt: practising early never moves a prompt on (G-Learn, method 12)
    if(!ok&&!s.again.has(x.k)){s.again.add(x.k);s.q.push(x);}  // a miss comes back once at the end of the session
    s.i++;s.shown=false;render();($('#lnDkQ')||$('#lnDkEnd'))?.focus();}}

/* ---------- Today: review queue + cards (design plan §4.1; full Today plan = L2) ---------- */
function lnTodayHtml(){
  const L=lnList(),due=lnDeckDue().length,all=lnDeckAll().length,last=state.last.card&&L.find(c=>c.id===state.last.card);
  const done=L.filter(c=>lnStatus(c.id)!=='none').length,firstNew=L.find(c=>lnStatus(c.id)==='none');
  return `<section class="card ln-today"><h2>${esc(STR.ln.today.deckT)}</h2><p class="sm">${esc(all?(due?STR.ln.due(due):STR.ln.dueNone+' '+(lnNextDue()?STR.ln.nextOn(lnDayLabel(lnNextDue())):'')):STR.ln.deckEmpty)}</p>
      ${all?`<button type="button" class="btn${due?' pri':''}" data-go="deck">${esc(due?STR.ln.today.review:STR.ln.deckT)}</button>`:''}</section>
    <section class="card ln-today"><h2>${esc(STR.ln.today.cardsT)}</h2><p class="sm">${esc(LN.idx?STR.ln.started(done,L.length):STR.ln.loading)}</p>
      ${last?`<button type="button" class="lrow" data-go="card=${esc(last.id)}"><span class="nm">${esc(STR.ln.today.cont)}: ${esc(last.title)}</span>${lnChip(last.id)}</button>`:''}
      ${firstNew&&(!last||firstNew.id!==last.id)?`<button type="button" class="lrow" data-go="card=${esc(firstNew.id)}"><span class="nm">${esc(done?firstNew.title:STR.ln.today.start+' · '+firstNew.title)}</span>${lnChip(firstNew.id)}</button>`:''}
      <p style="margin-top:8px"><button type="button" class="btn" data-go="cards">${esc(STR.ln.today.all)}</button></p></section>`;}

/* ---------- events (one delegated listener) ---------- */
document.addEventListener('click',e=>{const b=e.target.closest('[data-ln]');if(!b)return;const a=b.dataset.ln;
  if(b.getAttribute('aria-disabled')==='true')return;
  if(a.startsWith('d')&&ROUTE.name==='deck'){lnDeckAct(a,b);return;}
  const card=LN.open[ROUTE.id];if(ROUTE.name!=='card'||!card)return;
  if(a==='ref'){e.preventDefault();const o=b.getAttribute('aria-expanded')!=='true',box=document.getElementById('lnR-'+b.dataset.k);b.setAttribute('aria-expanded',o);if(box)box.classList.toggle('hidden',!o);return;}
  if(a==='level'){const l=b.dataset.l;state.settings.level=l;state.settings.t=Date.now();stSave();$('#lnBody').innerHTML=lnBodyHtml(card,l);
    $$('.ln-lv [data-l]').forEach(x=>x.setAttribute('aria-pressed',x===b));if(LN.ex[card.id]&&LN.ex[card.id].shown)lnPaint('expl');return;}
  if(['start','pick','mv','order','next'].includes(a)){lnCheckAct(card,a,b);return;}
  if(a==='exshow'){LN.ex[card.id]={shown:true};lnPaint('expl');$('#lnModel')?.focus();return;}
  if(a==='exyes'){lnSet(card.id,'exp');LN.ex[card.id]=null;lnPaint('expl');lnPaint('status');$('#lnExT')?.setAttribute('tabindex','-1');$('#lnExT')?.focus();return;}
  if(a==='exno'){LN.ex[card.id]=null;lnPaint('expl');$('#lnExT')?.setAttribute('tabindex','-1');$('#lnExT')?.focus();}
});
document.addEventListener('keydown',e=>{if(e.key===' '&&e.target.matches&&e.target.matches('a.ln-ref')){e.preventDefault();e.target.click();}});   // role=button: Space too
addEventListener('hashchange',()=>{clearTimeout(LN.readT);if(parseHash(location.hash).name!=='deck'&&LN.deck&&(!LN.deck.q||LN.deck.done))LN.deck=null;});
