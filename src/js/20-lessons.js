/* Biology Studio — lessons (L2, D-070): chapter path #lessons · one lesson #lesson=<ch> · lesson bar on a card (#card=<id>&lesson=<ch>[&step=<kind>])
   · Today plans On the go / Study (IB01) · Mixed review #mix · #mix=go (IB03).
   Owner docs: docs/lesson-spec.md (format + how the app uses it), build/design-plan.md §2 (Lessons, Mixed review rows) + §4.1 + §4.11; RULES A1, B4, C13, D-053.
   A lesson = one chapter in sittings of 10–15 min; each card adds read → check → scene|drill → remember (lesson-spec §3). Progress per step id in
   state.lessons[<ch>] = {done, skip, last, t} (add-only, A1). A step done outside the lesson counts (read = card Read; check = a finished run;
   drill = every drill question's latest answer right). Resume = the first step that is neither done nor skipped. A lesson never blocks.
   Mixed review: Checks (mcq + order) of Understood cards across chapters, interleaved, no card text (D-053); answers mix:<card>:<q> + state.mix.runs —
   recall stats only, never a card status (B4).
   EDIT: words in STR.ls; settings in CONFIG.learn (lessons, lessonDir, mix) + CONFIG.today; lesson data in content/<book>/lessons/ (never in code). */
'use strict';
const LS={les:{},err:{},load:{},mix:null,cur:null,view:'go'};   // cur = the lesson step the bar shows (card screen); view = Today's plan switch (U3, ephemeral — never saved, A1)

/* ---------- data ---------- */
function lsLoad(ch){if(LS.les[ch])return Promise.resolve(LS.les[ch]);if(LS.load[ch])return LS.load[ch];
  return LS.load[ch]=cdJson(CONFIG.learn.lessonDir+ch+'.json').then(j=>{LS.les[ch]=j;delete LS.err[ch];dlog('lessons','loaded',ch,j.sittings.length+' sittings');return j;})
    .catch(e=>{LS.err[ch]=e.message;delete LS.load[ch];throw e;});}
const lsLoadAll=()=>Promise.all(CONFIG.learn.lessons.map(ch=>lsLoad(ch).catch(()=>null)));
const lsName=ch=>STR.ln.groups[ch]||STR.ln.groupOf(ch);
const lsSteps=L=>L.sittings.flatMap((s,si)=>s.steps.map((st,k)=>({...st,sit:s.id,si,k})));
const lsMin=s=>Math.max(1,Math.round(s.steps.reduce((a,x)=>a+(x.est_s||0),0)/60));   // a sitting's minutes (est_s written by lesson-check)
const lsCardsOf=L=>[...new Set(lsSteps(L).map(s=>s.card))];
/* lesson cards' files: needed for drill steps and the bar's card names (36 small files; already cached by the reader) */
const lsNeedCards=L=>lsCardsOf(L).filter(id=>!LN.open[id]&&!LN.gone.has(id));
const lsLoadCards=L=>Promise.all(lsNeedCards(L).map(id=>lnCard(id).catch(()=>{LN.gone.add(id);})));

/* ---------- progress (state.lessons, A1) ---------- */
const lsRec=ch=>state.lessons[ch]||(state.lessons[ch]={done:{},skip:{},last:null,t:0});
function lsDone(ch,st){const r=state.lessons[ch],c=state.cards[st.card]||{};
  if(r&&r.done&&r.done[st.id])return true;
  if(st.kind==='read')return !!c.read;
  if(st.kind==='check')return (c.checks||0)>0||!!c.und;
  if(st.kind==='drill'){const card=LN.open[st.card];if(!card)return !!c.und;   // card file not loaded yet: a clean run had every drill right
    const d=card.checks.filter(lnIsDrill);return d.length>0&&d.every(q=>{const a=state.answers['card:'+st.card+':'+q.id];return !!(a&&a.ok);});}
  return false;}
const lsSkipped=(ch,st)=>!!(state.lessons[ch]&&state.lessons[ch].skip&&state.lessons[ch].skip[st.id]);
const lsState=(ch,st)=>lsDone(ch,st)?'done':lsSkipped(ch,st)?'skip':'open';
function lsMark(ch,id,k){const r=lsRec(ch);if(r[k][id])return;r[k][id]=Date.now();r.t=Date.now();dlog('lessons',k,id);stSave();}
/* where to resume: the first open step; when none is open, the first skipped one; null = all done */
function lsResume(ch,L){const a=lsSteps(L);return a.find(s=>lsState(ch,s)==='open')||a.find(s=>lsState(ch,s)==='skip')||null;}
function lsCount(ch,L){const a=lsSteps(L);return {n:a.length,done:a.filter(s=>lsState(ch,s)==='done').length};}
const lsHash=(ch,st)=>'card='+st.card+'&lesson='+ch+'&step='+st.kind;
/* the next lesson to work on (Today · Study): the first lesson in path order with an open step */
function lsNextLesson(){for(const ch of CONFIG.learn.lessons){const L=LS.les[ch];if(!L)continue;const st=lsResume(ch,L);if(st&&lsState(ch,st)==='open')return {ch,L,st};}
  for(const ch of CONFIG.learn.lessons){const L=LS.les[ch];if(!L)continue;const st=lsResume(ch,L);if(st)return {ch,L,st};}return null;}

/* small parts */
const LS_MARK={done:'✓',skip:'↷',open:'○'};
const lsBarHtml=(n,d)=>`<div class="ls-prog" role="img" aria-label="${esc(STR.ls.stepsDone(d,n))}"><span style="width:${n?Math.round(100*d/n):0}%"></span></div>`;
const lsLoading=(v,msg)=>{v.innerHTML=`<p class="mut" role="status"></p>`;const s=v.querySelector('[role=status]');setTimeout(()=>{if(s.isConnected)s.textContent=msg||STR.ls.loading;},50);};   // empty live region first, then the words: announced (G-A11y)

/* ---------- #lessons — the chapter path ---------- */
SCREENS.lessons=function(v){
  ROUTE.crumbs=[{label:STR.ls.pathT}];window.LS_READY=null;
  const miss=CONFIG.learn.lessons.filter(ch=>!LS.les[ch]&&!LS.err[ch]);
  if(miss.length||!LN.idx){lsLoading(v);Promise.all([lsLoadAll(),LN.idx?null:lnLoad().catch(()=>null)]).then(()=>{if(ROUTE.name==='lessons')render();});return;}
  const nx=lsNextLesson();
  v.innerHTML=`<div class="ls-path"><h1>${esc(STR.ls.pathT)}</h1><p class="mut ls-lead">${esc(STR.ls.pathLead)}</p>
    ${nx?`<section class="card ls-cont" aria-labelledby="lsContT"><h2 id="lsContT">${esc(STR.ls.contT)}</h2><p class="sm">${esc(lsName(nx.ch))} · ${esc(STR.ls.sitN(nx.st.si+1))} · ${esc(STR.ls.kind[nx.st.kind])}: ${esc(lnTitle(nx.st.card))}</p>
      <button type="button" class="btn pri" data-go="${esc(lsHash(nx.ch,nx.st))}">${esc(STR.ls.contBtn)}</button></section>`:''}
    <ol class="ls-chs">${CONFIG.learn.lessons.map((ch,i)=>{const L=LS.les[ch];
      if(!L)return `<li class="card ls-ch"><h2>${esc(lsName(ch))}</h2><p class="sm mut">${esc(STR.ls.loadFail)} <span class="xs">${esc(LS.err[ch]||'')}</span></p></li>`;
      const c=lsCount(ch,L),mins=L.sittings.reduce((a,s)=>a+lsMin(s),0);
      return `<li class="card ls-ch"><div class="row"><span class="ls-n" aria-hidden="true">${i+1}</span><h2 id="lsC-${esc(ch)}">${esc(lsName(ch))}</h2></div>
        <p class="sm">${esc(STR.ls.chLine(L.sittings.length,mins,lsCardsOf(L).length))}</p>${lsBarHtml(c.n,c.done)}<p class="xs mut">${esc(STR.ls.stepsDone(c.done,c.n))}</p>
        <button type="button" class="btn${c.done&&c.done<c.n?' pri':''}" data-go="lesson=${esc(ch)}" aria-describedby="lsC-${esc(ch)}">${esc(c.done===c.n?STR.ls.openDone:c.done?STR.ls.contBtn:STR.ls.startBtn)}</button></li>`;}).join('')}</ol>
    ${editBtn('screen','lessons','src/js/20-lessons.js + '+CONFIG.learn.lessonDir)}</div>`;
  window.LS_READY='lessons';
  if(dbgOn('lessons'))DBG.lessons=`lessons ${CONFIG.learn.lessons.join(' ')} · next ${nx?nx.st.id:'—'}`;
};
const lnTitle=id=>{const m=LN.idx&&LN.idx.cards.find(c=>c.id===id);return m?m.title:id;};

/* ---------- #lesson=<ch> — one lesson ---------- */
SCREENS.lesson=function(v){
  const ch=ROUTE.ch;ROUTE.crumbs=[{label:STR.ls.pathT,hash:'lessons'},{label:lsName(ch)}];window.LS_READY=null;
  if(!CONFIG.learn.lessons.includes(ch)){v.innerHTML=`<div class="card"><p>${esc(STR.ls.noLesson(ch))}</p><button type="button" class="btn" data-go="lessons">${esc(STR.ls.pathT)}</button></div>`;return;}
  const L=LS.les[ch];
  if(!L||!LN.idx||lsNeedCards(L).length||(!MAPD.M&&!MAPD.err)){
    if(LS.err[ch]){v.innerHTML=`<div class="card"><p>${esc(STR.ls.loadFail)} <span class="xs mut">${esc(LS.err[ch])}</span></p><button type="button" class="btn" data-go="lessons">${esc(STR.ls.pathT)}</button></div>`;delete LS.err[ch];return;}
    lsLoading(v);Promise.all([lsLoad(ch).then(lsLoadCards),LN.idx?null:lnLoad().catch(()=>null),MAPD.M?null:mapLoad().catch(()=>null)]).then(()=>{if(ROUTE.name==='lesson'&&ROUTE.ch===ch)render();},()=>{if(ROUTE.name==='lesson'&&ROUTE.ch===ch)render();});return;}
  const c=lsCount(ch,L),st=lsResume(ch,L),mins=L.sittings.reduce((a,s)=>a+lsMin(s),0);
  const pre=(L.prereq||[]).map(id=>{const m=LN.idx.cards.find(x=>x.id===id&&lnVisible(x)),cm=MAPD.byId&&MAPD.byId[id];
    return m?`<button type="button" class="lrow ln-row" data-go="card=${esc(id)}"><span class="nm">${esc(m.title)}</span>${lnChip(id)}<span class="id">${esc(id)}</span></button>`
      :`<div class="lrow ls-na"><span class="nm">${esc(cm?cm.name:id)}</span><span class="badge">${esc(STR.ls.notInApp)}</span><span class="id">${esc(id)}</span></div>`;}).join('');
  v.innerHTML=`<div class="ls-les" data-ch="${esc(ch)}">
  <header class="ls-head"><div class="row"><span class="mono mut">${esc(L.id)} · v${esc(L.version)}</span><span class="sp"></span>${editBtn('lesson',ch,CONFIG.learn.lessonDir+ch+'.json')}</div>
    <h1>${esc(lsName(ch))}</h1><p class="sm">${esc(STR.ls.chLine(L.sittings.length,mins,lsCardsOf(L).length))}</p>${lsBarHtml(c.n,c.done)}<p class="xs mut">${esc(STR.ls.stepsDone(c.done,c.n))}</p>
    ${st?`<div class="ls-go"><p class="sm"><b>${esc(lsState(ch,st)==='skip'?STR.ls.backSkipped:STR.ls.resumeT)}</b> ${esc(STR.ls.sitN(st.si+1))} · ${esc(STR.ls.kind[st.kind])}: ${esc(lnTitle(st.card))}</p>
      <button type="button" class="btn pri" data-go="${esc(lsHash(ch,st))}" data-fk="ls-go">${esc(c.done?STR.ls.contBtn:STR.ls.startBtn)}</button></div>`
      :`<p class="sm"><span class="ln-ok" aria-hidden="true">✓</span> ${esc(lsCardsOf(L).some(id=>lnStatus(id)==='read')?STR.ls.allDoneRetry:STR.ls.allDone)}</p>`}
    <p class="xs mut">${esc(STR.ls.howLead)}</p></header>
  ${pre?`<section class="card ls-pre" aria-labelledby="lsPreT"><h2 id="lsPreT">${esc(STR.ls.preT)}</h2><p class="xs mut">${esc(STR.ls.preLead)}</p>${pre}</section>`:''}
  <div class="ls-sits">${L.sittings.map((s,si)=>{const ss=lsSteps(L).filter(x=>x.si===si),d=ss.filter(x=>lsState(ch,x)==='done').length,cards=[...new Set(ss.map(x=>x.card))];
    return `<section class="card ls-sit" aria-labelledby="lsS-${si}"><h2 id="lsS-${si}">${esc(STR.ls.sitN(si+1))} <span class="sm mut">· ${esc(STR.ls.aboutMin(lsMin(s)))}</span></h2>
      <p class="xs mut">${esc(STR.ls.stepsDone(d,ss.length))}${d===ss.length?' · '+esc(STR.ls.sitDone):''}</p>
      <ol class="ls-cards">${cards.map(id=>`<li><div class="ls-crow"><button type="button" class="lrow ln-row" data-go="${esc(lsHash(ch,ss.find(x=>x.card===id)))}"><span class="nm">${esc(lnTitle(id))}</span>${lnChip(id)}</button></div>
        <ul class="ls-steps" aria-label="${esc(STR.ls.stepsOf(lnTitle(id)))}">${ss.filter(x=>x.card===id).map(x=>{const k=lsState(ch,x);
          return `<li><button type="button" class="ls-step ls-${k}" data-go="${esc(lsHash(ch,x))}"><span aria-hidden="true">${LS_MARK[k]}</span> ${esc(STR.ls.kind[x.kind])}<span class="sr"> — ${esc(STR.ls.stState[k])}</span></button></li>`;}).join('')}</ul></li>`).join('')}</ol></section>`;}).join('')}</div>
  </div>`;
  window.LS_READY='lesson='+ch;
  if(dbgOn('lessons'))DBG.lessons=`lesson ${ch} v${L.version} · ${c.done}/${c.n} · resume ${st?st.id:'—'}`;
};

/* ---------- lesson bar on a card (#card=<id>&lesson=<ch>[&step=<kind>]) ---------- */
/* the step the bar is on: the one the address names, else this card's first open step, else its last step */
function lsCurStep(){const ch=ROUTE.lesson,L=ch&&LS.les[ch];if(!L||ROUTE.name!=='card')return null;
  const mine=lsSteps(L).filter(s=>s.card===ROUTE.id);if(!mine.length)return null;
  return mine.find(s=>s.kind===ROUTE.step)||mine.find(s=>lsState(ch,s)==='open')||mine[mine.length-1];}
function lsAfter(ch,L,st){const a=lsSteps(L),i=a.findIndex(s=>s.id===st.id);return a.slice(i+1).find(s=>lsState(ch,s)!=='done')||null;}
/* the card screen calls this (18-learn.js): an empty bar host when the card was opened from a lesson */
function lsBarHost(){if(!ROUTE.lesson)return '';if(!LS.les[ROUTE.lesson])lsLoad(ROUTE.lesson).then(lsBarPaint,lsBarPaint);   // a failed load paints the failure, never an endless Loading (G-Eng)
  return `<section class="ls-bar" id="lsBar" aria-labelledby="lsBarT"></section>`;}
const lsBarFoot=()=>ROUTE.lesson?`<div class="ls-foot" id="lsFoot"></div>`:'';
function lsBarPaint(){const h=$('#lsBar');if(!h)return;const ch=ROUTE.lesson,L=LS.les[ch],st=lsCurStep();
  if(!L||!st){h.innerHTML=`<h2 id="lsBarT" class="ln-h">${esc(STR.ls.barT(lsName(ch),''))}</h2>`+(L||LS.err[ch]?`<p class="sm">${esc(L?STR.ls.notInLesson:STR.ls.loadFail)} <button type="button" class="lk" data-go="lesson=${esc(ch)}">${esc(STR.ls.backLesson)}</button></p>`:`<p class="xs mut" role="status">${esc(STR.ls.loading)}</p>`);return;}
  LS.cur=st;const r=lsRec(ch);if(r.last!==st.id){r.last=st.id;stSave();}if(dbgOn('lessons'))DBG.lessons=`bar ${ch} ${st.id} ${lsState(ch,st)}`;
  const all=lsSteps(L),sit=all.filter(s=>s.si===st.si),pos=sit.findIndex(s=>s.id===st.id)+1,k=lsState(ch,st),mine=all.filter(s=>s.card===st.card);
  const nx=lsAfter(ch,L,st),sitEnd=!nx||nx.si!==st.si,run=lnRun(st.card);
  const doneBtn=['scene','drill','remember'].includes(st.kind)&&k!=='done';
  const go=k!=='done'||st.kind==='check'?`<button type="button" class="btn" data-ls="goto" data-fk="ls-goto">${esc(STR.ls.goto[st.kind])}</button>`:'';
  const nextBtn=k==='done'||doneBtn?`<button type="button" class="btn${k==='done'?' pri':''}" data-ls="next" data-fk="ls-next">${esc(doneBtn?STR.ls.doneNext:sitEnd?STR.ls.endSit:STR.ls.nextStep)}</button>`:'';   // read/check move on by themselves: no dead button
  const skip=st.kind==='check'&&k==='open'&&!run?`<button type="button" class="btn" data-ls="skip" data-fk="ls-skip">${esc(STR.ls.skip)}</button>`:'';
  h.innerHTML=`<div class="row"><h2 id="lsBarT" class="ln-h">${esc(STR.ls.barT(lsName(ch),st.si+1))}</h2><span class="xs mut">${esc(STR.ls.stepOf(pos,sit.length))}</span></div>
    <ol class="ls-mine" aria-label="${esc(STR.ls.stepsOf(lnTitle(st.card)))}">${mine.map(s=>{const sk=lsState(ch,s);return `<li class="ls-${sk}${s.id===st.id?' cur':''}"${s.id===st.id?' aria-current="step"':''}><span aria-hidden="true">${LS_MARK[sk]}</span> ${esc(STR.ls.kind[s.kind])}<span class="sr"> — ${esc(STR.ls.stState[sk])}</span></li>`;}).join('')}</ol>
    <p class="sm ls-now" id="lsNow"><b>${esc(k==='done'?STR.ls.doneNow(STR.ls.kind[st.kind]):STR.ls.now)}</b> ${esc(k==='done'?'':STR.ls.how[st.kind])}${k==='skip'?' '+esc(STR.ls.wasSkipped):''}${st.kind==='scene'&&lsDrillMiss(st.card)?' '+esc(STR.ls.drillRetry):''}${st.kind==='check'&&k==='done'&&!['und','exp'].includes(lnStatus(st.card))?' '+esc(STR.ls.notUndYet):''}</p>
    <div class="row ls-acts">${go}${nextBtn}${skip}<span class="sp"></span><button type="button" class="lk" data-go="lesson=${esc(ch)}">${esc(STR.ls.backLesson)}</button></div>`;
  const f=$('#lsFoot');if(f)f.innerHTML=`<p class="sm"><b>${esc(STR.ls.barT(lsName(ch),st.si+1))}</b> · ${esc(STR.ls.stepOf(pos,sit.length))} · ${esc(STR.ls.kind[st.kind])}: ${esc(STR.ls.stState[k])}</p>
    <div class="row">${k==='done'||doneBtn?`<button type="button" class="btn${k==='done'?' pri':''}" data-ls="next">${esc(doneBtn?STR.ls.doneNext:sitEnd?STR.ls.endSit:STR.ls.nextStep)}</button>`:''}<button type="button" class="lk" data-ls="top">${esc(STR.ls.toBar)}</button></div>`;}
/* scroll to the part of the card the step is about */
function lsGoto(kind){const sel={read:'#lnBody',check:'#lnCheck',scene:'#lnTry',drill:'#lnCheck',remember:'#lnRem'}[kind],el=sel&&$(sel);if(!el)return;
  el.scrollIntoView({block:'start',behavior:motionReduced()?'auto':'smooth'});
  const f=kind==='check'||kind==='drill'?($('[data-ln="start"]')||$('#lnQ')):kind==='scene'?($('#vwStage')||$('#lnTryT')):el;   // the stage is focusable (tabindex 0, labelled) — a bare canvas is not (G-A11y)
  if(f){if(!f.matches('button,canvas')&&!f.hasAttribute('tabindex'))f.setAttribute('tabindex','-1');f.focus({preventScroll:true});}}
function lsMove(ch,L,st){const nx=lsAfter(ch,L,st);
  if(!nx||nx.si!==st.si){toast(STR.ls.sitDoneT(st.si+1));go('lesson='+ch);return;}
  if(nx.card===st.card){history.replaceState(history.state,'','#'+lsHash(ch,nx));ROUTE.step=nx.kind;ROUTE.raw=lsHash(ch,nx);if(state)state.last.route=ROUTE.raw;lsBarPaint();lsGoto(nx.kind);$('#lsNow')?.setAttribute('tabindex','-1');return;}
  document.activeElement?.blur?.();go(lsHash(ch,nx));}   // another card: no button keeps focus — the shell focuses the new card's title (G-A11y: a second Enter must not tick a step)
document.addEventListener('click',e=>{const b=e.target.closest('[data-ls]');if(!b||ROUTE.name!=='card'||!ROUTE.lesson)return;
  const ch=ROUTE.lesson,L=LS.les[ch],st=lsCurStep();if(!L||!st)return;const a=b.dataset.ls;
  if(a==='goto'){lsGoto(st.kind);return;}
  if(a==='top'){const t=$('#lsBar');if(t){t.scrollIntoView({block:'start',behavior:motionReduced()?'auto':'smooth'});$('#lsBarT')?.setAttribute('tabindex','-1');$('#lsBarT')?.focus({preventScroll:true});}return;}
  if(a==='skip'){lsMark(ch,st.id,'skip');lsMove(ch,L,st);return;}
  if(a==='next'){if(['scene','drill','remember'].includes(st.kind))lsMark(ch,st.id,'done');else if(lsState(ch,st)!=='done')return;lsMove(ch,L,st);}});
/* the reader repaints the bar when a status changes (Read, a finished run) — 18-learn.js lnPaint */
function lsOnCard(){if(ROUTE.name==='card'&&ROUTE.lesson)lsBarPaint();}

/* ---------- Mixed review (#mix) + one quick Check (#mix=go) ---------- */
const lsMixT=()=>CONFIG.learn.mix.types;   // Check types Mixed review asks (3D drills stay on their card) — CONFIG.learn.mix.types
const lsUnd=()=>lnList().filter(c=>['und','exp'].includes(lnStatus(c.id))&&!LN.gone.has(c.id));   // a card whose file failed to load is left out (G-Eng)
const lsChs=a=>new Set(a.map(c=>c.id.slice(0,3))).size;
/* a drill question of this card whose latest answer was wrong (the scene step suggests the Check again) */
const lsDrillMiss=id=>{const c=LN.open[id];return !!c&&c.checks.some(q=>lnIsDrill(q)&&state.answers['card:'+id+':'+q.id]&&!state.answers['card:'+id+':'+q.id].ok);};
/* cards with a finished Check run that is not yet clean: Study offers them again (G-Learn) */
const lsRetry=()=>lnList().filter(c=>lnStatus(c.id)==='read'&&((state.cards[c.id]||{}).checks||0)>0);
function lsMixBuild(cards,go){
  const M=CONFIG.learn.mix,qs=id=>LN.open[id]?LN.open[id].checks.filter(q=>lsMixT().includes(q.type)):[];   // card order kept: a card's own later question never comes first (G-Learn, D-058 (5))
  const pickQs=id=>{const a=qs(id);if(a.length<=M.perCard)return a;const keep=new Set(lnShuffle([...a.keys()]).slice(0,M.perCard));return a.filter((_,i)=>keep.has(i));};
  /* spaced, not massed: prefer cards Understood at least restDays ago, when there are enough of them */
  const old=cards.filter(c=>{const u=(state.cards[c.id]||{}).und;return u&&u<=lnDay0(Date.now())-(M.restDays-1)*864e5;});if(old.length>=M.minCards&&lsChs(old)>=M.minChapters)cards=old;
  if(go){const last=id=>Math.max(0,...Object.entries(state.answers).filter(([k])=>k.startsWith('mix:'+id+':')).map(([,v])=>v.t||0));
    const pick=cards.filter(c=>qs(c.id).length).sort((a,b)=>last(a.id)-last(b.id))[0];return pick?qs(pick.id).map(q=>({id:pick.id,q})):[];}
  const by={};for(const c of lnShuffle(cards))(by[c.id.slice(0,3)]||(by[c.id.slice(0,3)]=[])).push({id:c.id,qs:pickQs(c.id)});
  const chs=lnShuffle(Object.keys(by)),out=[];let lastCh=null,lastId=null;
  while(out.length<CONFIG.learn.mix.n){let added=false;
    for(const ch of chs){if(out.length>=CONFIG.learn.mix.n)break;const pool=by[ch].filter(x=>x.qs.length);if(!pool.length)continue;
      if(ch===lastCh&&chs.some(o=>o!==ch&&by[o].some(x=>x.qs.length)))continue;   // never two in a row from one chapter while another has questions
      const x=pool.find(p=>p.id!==lastId)||pool[0];out.push({id:x.id,q:x.qs.shift()});by[ch].push(by[ch].shift());lastCh=ch;lastId=x.id;added=true;}
    if(!added)break;}
  return out;}
function lsMixNew(go){const items=lsMixBuild(lsUnd(),go);
  LS.mix={go:!!go,items,i:0,res:[],pick:null,ord:null,pickOk:null,perm:Object.fromEntries(items.map((x,i)=>[i,lnShuffle([...Array((x.q.options||[]).length).keys()])])),done:false,t:Date.now()};
  for(const [i,x] of items.entries())if(x.q.type==='order'){let p=LS.mix.perm[i];for(let k=0;k<20&&p.every((v,j)=>v===j);k++)p=LS.mix.perm[i]=lnShuffle(p);}   // never starts solved
  dlog('lessons','mix',go?'go':'run',items.map(x=>x.id+':'+x.q.id).join(' '));}
/* recall stats (B4: Mixed review never sets a status) */
function lsRecall(){const runs=(state.mix&&state.mix.runs)||[],since=Date.now()-CONFIG.learn.mix.recallDays*864e5,r=runs.filter(x=>x.t>=since);
  const n=r.reduce((a,x)=>a+x.n,0),ok=r.reduce((a,x)=>a+x.ok,0);return {last:runs[runs.length-1]||null,n,ok,pct:n?Math.round(100*ok/n):null,today:runs.some(x=>x.t>=lnDay0(Date.now()))};}
SCREENS.mix=function(v){
  const go=ROUTE.view==='go';ROUTE.crumbs=[{label:STR.ls.mixT}];window.LS_READY=null;
  if(!LN.idx){lsLoading(v);lnLoad().then(()=>{if(ROUTE.name==='mix')render();},()=>{if(ROUTE.name==='mix')render();});return;}
  const und=lsUnd(),need=und.map(c=>c.id).filter(id=>!LN.open[id]&&!LN.gone.has(id));
  if(need.length){lsLoading(v);Promise.all(need.map(id=>lnCard(id).catch(()=>{LN.gone.add(id);}))).then(()=>{if(ROUTE.name==='mix')render();});return;}
  const R=lsRecall(),head=`<h1>${esc(go?STR.ls.goCheckT:STR.ls.mixT)}</h1><p class="mut ls-lead">${esc(go?STR.ls.goCheckLead:STR.ls.mixLead)}</p>`;
  const enough=go?und.some(c=>LN.open[c.id]&&LN.open[c.id].checks.some(q=>lsMixT().includes(q.type))):und.length>=CONFIG.learn.mix.minCards&&lsChs(und)>=CONFIG.learn.mix.minChapters;
  if(!enough||(LS.mix&&LS.mix.go===go&&!LS.mix.items.length)){LS.mix=null;v.innerHTML=`<div class="ls-mix">${head}<section class="card"><p>${esc(go?STR.ls.goNeed:STR.ls.mixNeed(CONFIG.learn.mix.minCards,CONFIG.learn.mix.minChapters,und.length))}</p>
    <div class="row"><button type="button" class="btn pri" data-go="lessons">${esc(STR.ls.pathT)}</button><button type="button" class="btn" data-go="today">${esc(STR.ln.back)}</button></div></section></div>`;window.LS_READY='mix';return;}
  const s=LS.mix;
  if(!s||s.go!==go){v.innerHTML=`<div class="ls-mix">${head}<section class="card"><p class="sm">${esc(go?STR.ls.goCheckOne:STR.ls.mixFrom(und.length,new Set(und.map(c=>c.id.slice(0,3))).size))}</p>
    ${R.n?`<p class="xs mut">${esc(STR.ls.recallLine(R.ok,R.n,R.pct,CONFIG.learn.mix.recallDays))}</p>`:''}
    <button type="button" class="btn pri" data-lsm="start" data-fk="ls-mstart">${esc(STR.ls.mixStart)}</button></section></div>`;window.LS_READY='mix';return;}
  if(s.done){const ok=s.res.filter(Boolean).length;
    v.innerHTML=`<div class="ls-mix">${head}<section class="card"><p id="lsMixEnd" tabindex="-1"><b>${esc(STR.ls.mixDone(ok,s.items.length))}</b></p><p class="xs mut">${esc(STR.ls.mixNoStatus)}</p>
      ${R.n?`<p class="xs mut">${esc(STR.ls.recallLine(R.ok,R.n,R.pct,CONFIG.learn.mix.recallDays))}</p>`:''}
      <div class="row"><button type="button" class="btn pri" data-go="today">${esc(STR.ln.back)}</button><button type="button" class="btn" data-lsm="start">${esc(STR.ls.mixAgain)}</button></div></section></div>`;window.LS_READY='mix';return;}
  const x=s.items[s.i],q=x.q,answered=s.pick!==null,ck={perm:{[q.id]:s.perm[s.i]},pick:s.pick,ord:s.ord,pickOk:s.pickOk},ok=answered&&s.res[s.i];
  const body=q.type==='mcq'?lnOptsHtml(q,ck,answered,o=>o):`<p class="xs mut">${esc(STR.ln.orderHint)}</p>`+lnOrderHtml(q,ck,answered,k=>`<span class="ln-ot">${esc(q.options[k])}</span>`,k=>q.options[k]);
  s.ord=ck.ord;
  v.innerHTML=`<div class="ls-mix">${head}<section class="card ln-check ls-mq" aria-labelledby="lnQ">
    <div class="row"><span class="xs mut">${esc(STR.ln.qOf(s.i+1,s.items.length))}</span></div>
    <p class="ln-q" id="lnQ" tabindex="-1"><b>${esc(q.prompt)}</b></p>${body}
    ${answered?`<div class="ln-fb" id="lnFb" tabindex="-1"><p><b><span class="${ok?'ln-ok':'ln-x'}" aria-hidden="true">${ok?'✓':'✗'}</span> ${esc(ok?STR.ln.right:STR.ln.wrong)}</b>${ok?'':lnRightHtml(LN.open[x.id],q,ck)}</p>
      <p class="sm">${esc(q.why)}</p><p class="xs mut">${esc(STR.ls.fromCard(lnTitle(x.id)))} · ${esc(lsName(x.id.slice(0,3)))}</p>
      <button type="button" class="btn pri" data-lsm="next" data-fk="ls-mnext">${esc(s.i===s.items.length-1?STR.ln.finish:STR.ln.next)}</button></div>`:''}
  </section></div>`;
  window.LS_READY='mix';
  if(dbgOn('lessons'))DBG.lessons=`mix ${go?'go':'run'} · ${s.i+1}/${s.items.length} · ${x.id}:${q.id}`;
};
function lsMixLog(x,ok){state.answers['mix:'+x.id+':'+x.q.id]={t:Date.now(),ok,v:LN.open[x.id].version};}
document.addEventListener('click',e=>{if(ROUTE.name!=='mix')return;const b=e.target.closest('[data-lsm],[data-ln]');if(!b)return;
  if(b.getAttribute('aria-disabled')==='true')return;const a=b.dataset.lsm||b.dataset.ln,s=LS.mix;let focus=null;
  if(a==='start'){lsMixNew(ROUTE.view==='go');render();(LS.mix.items.length?$('#lnQ'):null)?.focus();return;}
  if(!s||s.done)return;const x=s.items[s.i];
  if(a==='pick'){if(s.pick!==null)return;s.pick=+b.dataset.o;s.res[s.i]=s.pick===x.q.answer;lsMixLog(x,s.res[s.i]);stSave();focus='#lnFb';}
  else if(a==='mv'){const j=+b.dataset.j,d=+b.dataset.d,o=s.ord,k=o[j];if(j+d<0||j+d>=o.length)return;[o[j],o[j+d]]=[o[j+d],o[j]];const edge=(d<0&&j+d===0)||(d>0&&j+d===o.length-1);focus=`[data-fk="${(d<0)!==edge?'ln-u':'ln-d'}${k}"]`;}
  else if(a==='order'){s.pick=s.ord.slice();s.pickOk=s.ord.map((k,j)=>k===j);s.res[s.i]=s.pickOk.every(Boolean);lsMixLog(x,s.res[s.i]);stSave();focus='#lnFb';}
  else if(a==='next'){if(s.pick===null)return;
    if(s.i<s.items.length-1){s.i++;s.pick=null;s.ord=null;s.pickOk=null;focus='#lnQ';}
    else{s.done=true;const m=state.mix;m.runs.push({t:Date.now(),n:s.items.length,ok:s.res.filter(Boolean).length,go:s.go});if(m.runs.length>CONFIG.learn.mix.keep)m.runs.splice(0,m.runs.length-CONFIG.learn.mix.keep);m.t=Date.now();stSave();focus='#lsMixEnd';}}
  else return;
  render();const f=focus&&$(focus);if(f){if(!f.hasAttribute('tabindex'))f.setAttribute('tabindex','-1');f.focus();}});
/* a finished Mixed review is cleared when you leave it (the next visit starts fresh) */
addEventListener('hashchange',()=>{if(parseHash(location.hash).name!=='mix'&&LS.mix&&(LS.mix.done||!LS.mix.items.length))LS.mix=null;});

/* ---------- Today plans (IB01; design plan §4.1) ---------- */
/* U3 (D-087, P4): On the go / Study as a switch on one plan card, not two side-by-side cards; the due-prompts item is shared and
   shown once regardless of which is selected (it used to repeat in both — G-Art r1 #? / audit §1). */
function lsTodayPrimary(){   // the hero's one Start button: whatever "On the go" would send you to first
  const due=lnDeckDue().length,und=lsUnd(),R=lsRecall(),L=lnList(),cur=state.last.card&&L.find(c=>c.id===state.last.card),firstRead=L.find(c=>lnStatus(c.id)==='read');
  if(due)return'deck=go';
  const ckGo=und.length?{hash:'mix=go'}:(cur||firstRead)?{hash:'card='+(cur||firstRead).id}:null;
  return ckGo?ckGo.hash:'lessons';}
function lsTodayHtml(){
  if(!LN.idx)return `<section class="card wide"><p class="mut sm" role="status">${esc(STR.ln.loading)}</p></section>`;
  const T=CONFIG.today,due=lnDeckDue().length,und=lsUnd(),R=lsRecall(),nx=lsNextLesson(),L=lnList();
  const cur=state.last.card&&L.find(c=>c.id===state.last.card),firstRead=L.find(c=>lnStatus(c.id)==='read');
  /* On the go: due prompts + one Check (a Mixed-review run of one Understood card, else the Check of the card you are on) */
  const ckGo=und.length?{hash:'mix=go',label:STR.ls.goCheck,done:R.today}:(cur||firstRead)?{hash:'card='+(cur||firstRead).id,label:STR.ls.goCheckCard((cur||firstRead).title),done:false}:null;
  const retry=lsRetry(),mixOn=und.length>=CONFIG.learn.mix.minCards&&lsChs(und)>=CONFIG.learn.mix.minChapters;
  let iq=0;const item=(n,t,meta,btn,done)=>{const id='lsTi'+(++iq);btn=(btn||'').replace('<button ',`<button aria-describedby="${id}" `);return `<li class="ls-ti${done?' ls-done':''}"><span class="ls-tn" aria-hidden="true">${done?'✓':n}</span><div><p class="sm" id="${id}"><b>${esc(t)}</b>${meta?` <span class="xs mut">${esc(meta)}</span>`:''}${done?`<span class="sr"> — ${esc(STR.ls.doneToday)}</span>`:''}</p>${btn}</div></li>`;};
  const dueItem=item(1,due?STR.ls.tDeck(due):STR.ls.tDeckNone,due?STR.ls.aboutMin(Math.max(1,Math.round(Math.min(due,T.goPrompts)*T.promptS/60))):(lnDeckAll().length&&lnNextDue()?STR.ln.nextOn(lnDayLabel(lnNextDue())):STR.ln.deckEmpty),due?`<button type="button" class="btn sm" data-go="deck=go">${esc(STR.ln.today.review)}</button>`:'',!due&&lnDeckAll().length>0);
  const nxSit=nx&&nx.L.sittings[nx.st.si],study=LS.view==='study';
  let rest;
  if(study){const studyLesson=nx?item(2,STR.ls.tLesson(lsName(nx.ch),nx.st.si+1),STR.ls.aboutMin(lsMin(nxSit)),`<button type="button" class="btn sm pri" data-go="${esc(lsHash(nx.ch,nx.st))}">${esc(STR.ls.contBtn)}</button>`,false)
      :item(2,STR.ls.tLessonsDone,'',`<button type="button" class="btn sm" data-go="lessons">${esc(STR.ls.pathT)}</button>`,true);
    rest=studyLesson+(retry.length?item(3,STR.ls.tRetry(retry.length),retry[0].title,`<button type="button" class="btn sm" data-go="card=${esc(retry[0].id)}">${esc(STR.ls.retryBtn)}</button>`,false):'')+(mixOn?item(retry.length?4:3,STR.ls.tMix,STR.ls.optional,`<button type="button" class="btn sm" data-go="mix">${esc(STR.ls.mixT)}</button>`,R.today):'');
  }else rest=ckGo?item(2,ckGo.label,STR.ls.aboutMin(Math.round(T.checkS/60)),`<button type="button" class="btn sm" data-go="${esc(ckGo.hash)}">${esc(STR.ls.startBtn)}</button>`,ckGo.done):'';
  return `<section class="card ls-plan" aria-labelledby="lsPlanT"><h2 id="lsPlanT">${esc(STR.ls.planT)}</h2>
      <div class="seg" role="group" aria-label="${esc(STR.ls.planT)}"><button type="button" data-td-view="go" aria-current="${!study}">${esc(STR.ls.goT)}</button><button type="button" data-td-view="study" aria-current="${study}">${esc(STR.ls.studyT)}</button></div>
      <p class="xs mut">${esc(study?STR.ls.studyLead:STR.ls.goLead(Math.round(T.goMax)))}</p>
      <ol class="ls-tl">${dueItem}${rest}</ol>
      ${study&&R.n?`<p class="xs mut">${esc(STR.ls.recallLine(R.ok,R.n,R.pct,CONFIG.learn.mix.recallDays))}</p>`:''}</section>`;}
document.addEventListener('click',e=>{const b=e.target.closest('[data-td-view]');if(!b)return;LS.view=b.dataset.tdView;render();});

/* ---------- tests hook (91-tests.js calls lsTests) ---------- */
function lsTests(t){
  const W={sittings:[{id:'s1',steps:[{id:'E05.01.01:read',card:'E05.01.01',kind:'read',est_s:60},{id:'E05.01.01:check',card:'E05.01.01',kind:'check',est_s:90},{id:'E05.01.01:scene',card:'E05.01.01',kind:'scene',est_s:60}]},
    {id:'s2',steps:[{id:'E05.01.02:read',card:'E05.01.02',kind:'read',est_s:60}]}]};
  const bk={l:state.lessons,c:state.cards,a:state.answers};state.lessons={};state.cards={};state.answers={};
  try{
    t('lesson: resume = first open step',lsResume('E05',W).id==='E05.01.01:read');
    state.cards['E05.01.01']={read:1,checks:0};t('lesson: Read counts the read step',lsResume('E05',W).id==='E05.01.01:check');
    state.lessons.E05={done:{},skip:{'E05.01.01:check':1},last:null,t:1};t('lesson: a skipped step is passed over, then comes back last',lsResume('E05',W).id==='E05.01.01:scene');
    state.lessons.E05.done['E05.01.01:scene']=1;state.lessons.E05.done['E05.01.02:read']=1;t('lesson: only skipped left → resume there',lsResume('E05',W).id==='E05.01.01:check');
    state.cards['E05.01.01'].checks=1;t('lesson: a finished run counts the check step (any score)',lsResume('E05',W)===null&&lsCount('E05',W).done===4);
    t('lesson: sitting minutes from est_s',lsMin(W.sittings[0])===4);
    t('lesson address',lsHash('E05',W.sittings[0].steps[1])==='card=E05.01.01&lesson=E05&step=check');
  }finally{state.lessons=bk.l;state.cards=bk.c;state.answers=bk.a;}
  {const r=parseHash('#card=E05.01.01&lesson=E05&step=check');t('route card in a lesson',r.lesson==='E05'&&r.step==='check'&&hashOf(r)==='card=E05.01.01&lesson=E05&step=check',JSON.stringify(r));
    t('route bad lesson/step dropped',parseHash('#card=E05.01.01&lesson=x&step=y').lesson===undefined);
    t('up: card in a lesson → the lesson · lesson → path · path → today',JSON.stringify(upOf(r))==='{"name":"lesson","ch":"E05"}'&&JSON.stringify(upOf(parseHash('#lesson=E05')))==='{"name":"lessons"}'&&JSON.stringify(upOf(parseHash('#lessons')))==='{"name":"today"}');
    t('route mix + mix=go + deck=go',parseHash('#mix').view==='run'&&parseHash('#mix=go').view==='go'&&parseHash('#deck=go').view==='go'&&hashOf(parseHash('#mix=go'))==='mix=go');}
  {const s=stFill({});t('saved shape has lessons + mix',typeof s.lessons==='object'&&Array.isArray(s.mix.runs));
    const m=stMerge({lessons:{E05:{done:{a:5},skip:{},last:'a',t:1}},mix:{runs:[{t:1,n:8,ok:6}],t:1}},{lessons:{E05:{done:{a:3,b:4},skip:{c:2},last:'b',t:2}},mix:{runs:[{t:1,n:8,ok:6},{t:2,n:8,ok:7}],t:2}});
    t('merge lessons: earliest done, union, newer last · mix runs union',m.lessons.E05.done.a===3&&m.lessons.E05.done.b===4&&m.lessons.E05.skip.c===2&&m.lessons.E05.last==='b'&&m.mix.runs.length===2,JSON.stringify(m.lessons)+JSON.stringify(m.mix));}
  /* Mixed review: interleaved, Understood only, no drills */
  {const fake=['E05.01.01','E05.01.02','E06.01.01','E07.02.01','E08.03.01'].map(id=>({id})),bkO=LN.open;LN.open={};
    for(const c of fake)LN.open[c.id]={id:c.id,version:1,checks:[{id:'q1',type:'mcq',options:['a','b','c'],answer:0},{id:'q2',type:'mcq',options:['a','b','c'],answer:0},{id:'q3',type:'mcq',options:['a','b','c'],answer:0},{id:'q4',type:'day',options:[16,17],answer:0}]};
    const it=lsMixBuild(fake,false);let rep=false;for(let i=1;i<it.length;i++)if(it[i].id.slice(0,3)===it[i-1].id.slice(0,3))rep=true;
    t('mix: n questions, never two in a row from one chapter, no drills',it.length===CONFIG.learn.mix.n&&!rep&&it.every(x=>lsMixT().includes(x.q.type))&&it.every((x,i)=>it.slice(i+1).every(y=>y.id!==x.id||+y.q.id.slice(1)>+x.q.id.slice(1))),it.map(x=>x.id.slice(0,3)).join(''));
    t('mix go: one card, all its mcq/order',(()=>{const g=lsMixBuild(fake,true);return g.length===3&&new Set(g.map(x=>x.id)).size===1;})());
    LN.open=bkO;}
}
