/* Biology Studio — Reviewer mode (H2, D-060 / D-061): a guided home for the human science reviewer (the Professor).
   Owner docs: build/design-plan.md §2 (Review rows) + §4.10, build/setup-guide.md §0 (Reviewer: start here), RULES C13, I5–I6, I8.
   #review (To review · What's new · My feedback) · #rcard=<id> (read a card + plain checklist + ✓ / ✎ / ? + note + how sure → a pre-filled
   GitHub Issue Form) · #rtour[=2|3] (3-screen guided tour, replayable) · #updates[=page] (plain-English updates from logs/build-log.md).
   My feedback reads her issues from the public GitHub API (no token): one call, cached in the saved state, conditional (ETag), never more
   than every CONFIG.review.refreshMs on its own; a rate limit (403/429) or offline keeps the cached list and says when it was checked.
   Issue state → words: open = Sent · open + label `fixing` = Being fixed · closed + milestone vN = Fixed in version N · closed ✓ = Done ·
   closed "not planned" = Closed, no change · closed ? = Answered. Nothing here writes to the repo — she presses Create on GitHub.
   Debug: ?debug=review (overlay line + a Debug section: parsed issues, Clear the saved list, Pretend to be). Demo: ?test=1&fixture=review.
   EDIT: words in STR.rv · settings in CONFIG.review · form field ids = REVIEW_FIELDS = .github/ISSUE_TEMPLATE/card-review.yml ids. */
'use strict';
const RV={idx:null,idxErr:null,cards:{},issues:null,src:'',http:0,rate:null,limitUntil:0,busy:false,err:'',upd:null,updErr:'',as:'',open:{},triedAt:0};   // triedAt: last call to GitHub, success or not — the 5-min window counts from it (G-Eng: no retry loop)
/* EDIT: the Issue Form's field ids (must match .github/ISSUE_TEMPLATE/card-review.yml and other-feedback.yml) */
const REVIEW_FIELDS={card:'card',verdict:'verdict',where:'where',sure:'sure',checklist:'checklist',note:'note'};
const RV_LIST=['facts','timing','gaps','words','adult','qs','mix','fig'],RV_VERD=['ok','fix','ask'],RV_SURE=['high','mid','low'],RV_WHERE=['obj','body','facts','mis','adult','clin','qs','rem'];
const RV_SYM={ok:'✓',fix:'✎',ask:'?'};

/* ---------- small helpers ---------- */
const rvLogin=()=>RV.as||CONFIG.review.login;
const rvTime=t=>t?new Date(t).toLocaleString([], {day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'}):'';
const rvDay=t=>t?new Date(t).toLocaleDateString([], {day:'numeric',month:'short'}):'';
const rvSaveR=()=>{state.review.t=Date.now();stSave();};
function rvTurnOn(){if(FLAGS.test||state.review.on)return;state.review.on=true;rvSaveR();buildShell();}   // the Review tab appears for her from the first visit

/* ---------- issues: parse (pure — appTests use these) ---------- */
/* title the app writes: "[review] E06.02.01 v1 ✎ Three strips of mesoderm" · general: "[feedback] …" */
function rvParseTitle(t){t=String(t||'');let m=t.match(/^\s*\[review\]\s*(E\d\d\.\d\d\.\d\d)\s+v(\d+)\s*(✓|✎|\?)?/u);
  if(m)return {kind:'card',card:m[1],ver:+m[2],verdict:m[3]?{'✓':'ok','✎':'fix','?':'ask'}[m[3]]:null};
  if(/^\s*\[feedback\]/i.test(t))return {kind:'other',card:null,ver:null,verdict:null};
  m=t.match(/(E\d\d\.\d\d\.\d\d)/);return m?{kind:'card',card:m[1],ver:null,verdict:null}:null;}
/* the form body: "### Card\n\nE06.02.01 v1 · …\n\n### Overall\n\n✎ Needs a fix" — fallback when she edited the title */
function rvParseBody(b){b=String(b||'');const sec=k=>{const m=b.match(new RegExp('###\\s*'+k+'\\s*\\n+([^\\n#][^\\n]*)','i'));return m?m[1].trim():'';};
  const c=sec('Card').match(/(E\d\d\.\d\d\.\d\d)\s*v?(\d+)?/),o=sec('Overall');
  return {card:c?c[1]:null,ver:c&&c[2]?+c[2]:null,verdict:/✓/.test(o)?'ok':/✎/.test(o)?'fix':/\?/.test(o)?'ask':null};}
function rvStateOf(it,verdict){const labels=(it.labels||[]).map(l=>typeof l==='string'?l:l.name);
  if(it.state==='open')return labels.includes(CONFIG.review.fixingLabel)?{st:'fixing'}:{st:'sent'};
  const mt=it.milestone&&String(it.milestone.title||'').match(/^v?\s*(\d+)$/i);
  if(mt)return {st:'fixed',fixedIn:+mt[1]};
  if(it.state_reason==='not_planned')return {st:'noChange'};
  return {st:verdict==='ask'?'answered':'done'};}
function rvParseIssue(it){if(!it||it.pull_request)return null;const t=rvParseTitle(it.title);const hasL=(it.labels||[]).some(l=>(l.name||l)===CONFIG.review.label);
  if(!t&&!hasL)return null;const b=rvParseBody(it.body),p=t||{kind:b.card?'card':'other',card:null,ver:null,verdict:null};
  const card=p.card||b.card,ver=p.ver??b.ver,verdict=p.verdict||b.verdict,s=rvStateOf(it,verdict);
  return {n:it.number,title:String(it.title||'').replace(/^\s*\[(review|feedback)\]\s*/i,'').replace(/^E\d\d\.\d\d\.\d\d\s+v\d+\s*[✓✎?]?\s*/u,''),kind:card?'card':'other',card,ver,verdict,...s,
    url:/^https:\/\/github\.com\//.test(it.html_url||'')?it.html_url:'',comments:it.comments||0,created:Date.parse(it.created_at)||0,closed:Date.parse(it.closed_at)||0,updated:Date.parse(it.updated_at)||0,by:(it.user&&it.user.login)||''};}
/* the saved list keeps only what the screens need (A1: small state) */
const rvCompact=it=>({number:it.number,title:it.title,state:it.state,state_reason:it.state_reason||null,labels:(it.labels||[]).map(l=>({name:l.name||l})),
  milestone:it.milestone?{title:it.milestone.title}:null,created_at:it.created_at,closed_at:it.closed_at,updated_at:it.updated_at,comments:it.comments,html_url:it.html_url,
  user:{login:it.user&&it.user.login},body:String(it.body||'').slice(0,600),pull_request:it.pull_request?1:undefined});
const rvMine=()=>(RV.issues||[]).map(rvParseIssue).filter(x=>x&&(!x.by||x.by.toLowerCase()===rvLogin().toLowerCase())).sort((a,b)=>b.created-a.created);

/* ---------- issues: fetch (live · fixture · cache) ---------- */
function rvUseCache(){const c=state.review.cache;if(c&&Array.isArray(c.items)){RV.issues=c.items;if(!RV.src)RV.src='cache';}}
async function rvFetch(force){
  if(RV.busy)return;const C=CONFIG.review,now=Date.now();
  if(FLAGS.fixture==='review'){if(RV.issues&&!force)return;RV.busy=true;try{const j=await cdJson(C.fixture);RV.issues=j.items.map(rvCompact);RV.src='fixture';RV.http=200;RV.err='';
      if(new URLSearchParams(location.search).get('rvlimit')==='1'){RV.err='limited';RV.http=403;RV.limitUntil=now+20*60e3;RV.src='cache';}   // demo: the rate-limit message over the "saved" list
      state.review.cache={at:now-(RV.err?95*60e3:0),etag:'',items:RV.issues,status:RV.http};}
    catch(e){RV.err='bad';RV.issues=RV.issues||[];dlog('review','fixture',e.message);}finally{RV.busy=false;setTimeout(rvPaint,0);}return;}
  rvUseCache();const c=state.review.cache;
  /* never paint from here: a screen calls rvFetch while it draws (G-Eng: no render ↔ fetch recursion); the screen shows RV.err itself */
  if(typeof navigator!=='undefined'&&navigator.onLine===false){RV.err='offline';return;}   // offline first, so it is named even inside the 5-min window (G-Eng r2)
  if(!force&&((c&&now-(c.at||0)<C.refreshMs)||now-RV.triedAt<C.refreshMs))return;
  if(RV.limitUntil>now){RV.err='limited';return;}
  RV.busy=true;RV.triedAt=now;setTimeout(rvPaint,0);
  const url=C.api+'?state=all&per_page=100&sort=created&direction=desc&creator='+encodeURIComponent(rvLogin());
  try{const h={Accept:'application/vnd.github+json'};if(c&&c.etag&&c.login===rvLogin())h['If-None-Match']=c.etag;
    const r=await fetch(url,{headers:h,cache:'no-store'});RV.http=r.status;
    const rem=r.headers.get('x-ratelimit-remaining'),reset=+r.headers.get('x-ratelimit-reset')||0,ra=+r.headers.get('retry-after')||0;
    RV.rate=rem==null?null:+rem;dlog('review','GET',r.status,'rate',rem);
    if(r.status===304){state.review.cache={...c,at:now,status:304};RV.err='';RV.src='live';}
    else if(r.ok){const j=await r.json();const items=(Array.isArray(j)?j:[]).map(rvCompact);
      RV.issues=items;RV.src='live';RV.err='';state.review.cache={at:now,etag:r.headers.get('etag')||'',items,status:200,login:rvLogin()};}
    else if(r.status===429||ra||(r.status===403&&rem==='0')){RV.err='limited';RV.limitUntil=ra?now+ra*1000:reset?reset*1000:now+15*60e3;}   // a 403 with calls left is not a rate limit (G-Eng)
    else if(r.status===404||r.status===422){RV.err='bad';}   // 422: an unknown login (Pretend to be)
    else RV.err='bad';
    rvSaveR();}
  catch(e){RV.err=navigator.onLine===false?'offline':'bad';dlog('review','fetch failed',e.message);}
  finally{RV.busy=false;setTimeout(rvPaint,0);}}

/* ---------- cards ---------- */
function rvLoad(){
  if(!RV.idx&&!RV.idxErr&&!RV._p)RV._p=cdIndex().then(j=>{RV.idx=j;},e=>{RV.idxErr=e.message;}).finally(()=>{RV._p=null;rvPaint();});
  cdSources().catch(()=>{});}
const rvCardsAll=()=>RV.idx?RV.idx.cards.filter(c=>c.status!=='retired'&&/^E(0[1-9]|[1-9]\d)/.test(c.id)):[];   // concept cards only (guide cards E00 are about the app)
/* To review / Waiting / Done for one card, from her issues (D-060: her ✓ = the human science pass for that version) */
function rvCardState(m,mine){const its=mine.filter(x=>x.card===m.id).sort((a,b)=>b.created-a.created),last=its[0];
  if(!last)return {k:'todo',why:'new'};
  if(last.st==='fixed')return {k:'todo',why:'fixed',last};
  if(last.ver!=null&&last.ver<(m.version||1))return {k:'todo',why:'changed',last};
  if(last.verdict==='ok'||last.st==='done'||last.st==='noChange'||last.st==='answered')return {k:'done',last};
  return {k:'wait',last};}
function rvSort(){const mine=rvMine(),out={todo:[],wait:[],done:[],drafts:[]};
  for(const m of rvCardsAll()){if(!CONFIG.review.show.includes(m.status)){out.drafts.push({m});continue;}
    const s=rvCardState(m,mine);out[s.k].push({m,...s});}
  return out;}
function rvNews(){return rvCardsAll().filter(m=>CONFIG.review.show.includes(m.status)&&(state.review.seen[m.id]||0)<(m.version||1));}

/* ---------- updates from logs/build-log.md (plain line <!--plain: …--> or the title) ---------- */
function rvParseLog(md){const out=[];
  for(const line of String(md||'').split('\n')){if(!/^- \d{1,2} [A-Z][a-z]{2} \d{4} · /.test(line))continue;
    const date=line.slice(2).split(' · ')[0],tm=line.match(/\*\*(.+?)\*\*/),pm=line.match(/<!--\s*plain:\s*([\s\S]+?)\s*-->/);
    const title=tm?tm[1]:'';
    out.push({date,key:date+'|'+title,plain:pm?pm[1]:'',title:title.replace(/\s*\((?:[^()]*\b(?:D-\d+|v\d+)\b[^()]*)\)/g,'').replace(/\s+/g,' ').trim()});}
  return out;}
function rvUpdLoad(){if(RV.upd||RV.updErr||RV._u)return;
  RV._u=fetch(CONFIG.review.updatesUrl,{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.text();})
    .then(t=>{RV.upd=rvParseLog(t);},e=>{RV.updErr=e.message;}).finally(()=>{RV._u=null;rvPaint();});}
function rvUpdNew(){if(!RV.upd)return 0;const k=state.review.updKey;if(!k)return RV.upd.filter(u=>u.date===RV.upd[0].date).length;   /* never looked: only the newest day counts as new */const i=RV.upd.findIndex(u=>u.key===k);return i<0?RV.upd.length:i;}
const rvUpdLi=(u,isNew,noDate)=>`<li class="rv-upd${u.plain?'':' rv-tech'}">${noDate?'':`<span class="xs mut">${esc(u.date)}</span>`}${isNew&&!noDate?` <span class="badge rv-new">${esc(STR.rv.newCard)}</span>`:''}<span class="rv-ut">${esc(u.plain||u.title)}</span></li>`;   // in a dated group: no date, New once on the group (G-Art)

/* ---------- the Issue Form link ---------- */
function rvCardTitle(id){const m=RV.idx&&RV.idx.cards.find(c=>c.id===id);return m?m.title:'';}
function rvFormUrl(id,ver,d){const C=CONFIG.review,F=REVIEW_FIELDS,v=d.verdict;
  const ticks=RV_LIST.map(k=>(d.list&&d.list[k]?'- [x] ':'- [ ] ')+STR.rv.list[k]).join('\n');
  const p=new URLSearchParams({template:C.form,labels:C.label,title:`[review] ${id} v${ver} ${RV_SYM[v]||''} ${rvCardTitle(id)}`.replace(/\s+/g,' ').trim()});
  p.set(F.card,`${id} v${ver} · ${rvCardTitle(id)}`);p.set(F.verdict,STR.rv.verdicts[v]||'');
  p.set(F.where,d.where?STR.rv.where[d.where]:STR.rv.whereAny);p.set(F.sure,d.sure?STR.rv.sure[d.sure]:'');
  p.set(F.checklist,ticks);let note=String(d.note||'').slice(0,1500);p.set(F.note,note);
  while((C.newIssue+'?'+p.toString()).length>C.maxUrl&&note.length>100){note=note.slice(0,Math.floor(note.length*0.85))+'…';p.set(F.note,note);}   // long non-Latin notes encode long (G-Eng)
  return C.newIssue+'?'+p.toString();}
const rvOtherUrl=()=>CONFIG.review.newIssue+'?'+new URLSearchParams({template:CONFIG.review.formOther,labels:CONFIG.review.label,title:'[feedback] '}).toString();
function rvFormOk(d){if(!d||!RV_VERD.includes(d.verdict))return false;if(d.verdict!=='ok'&&!String(d.note||'').trim())return false;return true;}
const rvDraft=id=>state.review.drafts[id]||(state.review.drafts[id]={list:{},verdict:'',where:'',sure:'',note:'',t:0});

/* ---------- shared pieces ---------- */
function rvStatusLine(){const c=state.review.cache,E=STR.rv;
  if(RV.busy){rvAnnounce(E.checking);return `<p class="xs mut">${esc(E.checking)}</p>`;}
  const at=c&&c.at?E.checkedAt(rvTime(c.at)):E.neverChecked;
  const msg=RV.err==='limited'?E.limited(rvTime(RV.limitUntil)):RV.err==='offline'?E.offline:RV.err==='bad'?E.loadBad:'';
  rvAnnounce(msg);return `<p class="xs ${msg?'rv-warn':'mut'}">${esc(msg?msg+' ':'')}${esc(at)}</p>`;}
/* one live region for the whole session (created once, only its text changes — G-A11y) */
function rvAnnounce(msg){let l=document.getElementById('rvLive');if(!l){l=document.createElement('div');l.id='rvLive';l.className='sr';l.setAttribute('role','status');document.body.appendChild(l);}
  if(msg&&l.textContent!==msg)setTimeout(()=>{l.textContent=msg;},50);}
const rvStChip=x=>{const E=STR.rv,w=x.st==='fixed'?E.states.fixed(x.fixedIn):E.states[x.st];return `<span class="rv-stw"><span class="rv-st st-${esc(x.st)}"><span class="rv-dot" aria-hidden="true"></span>${esc(w)}</span><span class="xs mut rv-sth">${esc(E.stateHelp[x.st]||'')}</span></span>`;};   // the meaning is printed (phones never show a hover title — G-Learn)
const rvVerd=v=>v?`<span class="rv-v v-${esc(v)}" role="img" aria-label="${esc(STR.rv.verdicts[v])}">${esc(RV_SYM[v])}</span>`:'';
function rvCardRow(x){const m=x.m,E=STR.rv,why=x.why==='changed'?E.changed:x.why==='fixed'?E.fixedBack:'',d=state.review.drafts[m.id];
  const sent=d&&d.sentAt&&!(x.last&&x.last.created>=d.sentAt-6e4);   // she opened GitHub but no issue shows yet
  return `<a class="lrow rv-row" href="#rcard=${esc(m.id)}"><span class="nm">${esc(m.title)}</span><span class="rv-sub xs">${why?`<span class="badge">${esc(why)}</span>`:''}${sent?`<span class="badge">${esc(E.sentOn(rvDay(d.sentAt)))}</span>`:''}${m.status==='draft'?`<span class="badge b-detail">draft</span>`:''}<span class="id">${esc(m.id)}</span></span></a>`;}
function rvMineLi(x){const E=STR.rv;
  return `<li class="rv-mine"><a href="${esc(x.url)}" target="_blank" rel="noopener" class="rv-ml">${rvVerd(x.verdict)}<span class="rv-mt"><b>${esc(x.kind==='card'?x.title||E.aboutCard(x.card):x.title||E.other)}</b>
    <span class="xs mut">${esc(x.card?E.aboutCard(x.card)+(x.ver?' · '+E.version(x.ver):''):E.other)} · ${esc(rvDay(x.created))}${x.comments?' · '+esc(E.replies(x.comments)):''}</span></span>${rvStChip(x)}<span class="sr">${esc(E.openGh)} ${esc(E.newTab)}</span></a></li>`;}

/* ---------- #review home ---------- */
SCREENS.review=function(v){const E=STR.rv;ROUTE.crumbs=[{label:E.title}];
  rvTurnOn();rvLoad();rvUseCache();rvUpdLoad();
  if(!state.review.tour&&FLAGS.fixture!=='review'&&!RV._tourGo){RV._tourGo=1;go({name:'rtour',step:1},{replace:true});return;}   // first visit: the tour (replayable)
  rvFetch(false);
  /* first visit (after the tour): everything there now is her starting point — What's new then lists only what changes after today (the demo keeps it all new) */
  if(!state.review.seenAt&&RV.idx&&(RV.upd||RV.updErr)&&FLAGS.fixture!=='review'){for(const m of rvCardsAll())state.review.seen[m.id]=Math.max(state.review.seen[m.id]||0,m.version||1);
    state.review.updKey=RV.upd&&RV.upd[0]?RV.upd[0].key:'';state.review.seenAt=Date.now();rvSaveR();}
  const S=rvSort(),mine=rvMine(),news=rvNews(),nu=rvUpdNew(),tab=ROUTE.view||'todo';
  const tabBtn=(k,n)=>`<button type="button" data-rvtab="${k}" data-fk="rvtab-${k}" aria-pressed="${tab===k}" aria-controls="rv-${k}">${esc(E.tabs[k])}${n?` <span class="rv-n" aria-hidden="true">${n}</span><span class="sr">, ${n}</span>`:''}</button>`;
  const todo=`<section class="card rv-pane" id="rv-todo" aria-labelledby="rvTodoT"><h2 id="rvTodoT">${esc(E.tabs.todo)}</h2>
      ${RV.idx?`<p class="sm mut">${esc(E.todoLead(S.todo.length))}</p>${S.todo.map(rvCardRow).join('')}`:`<p class="sm mut">${esc(RV.idxErr?STR.ln.loadFail:STR.ln.loading)}</p>`}
      ${S.wait.length?`<h3 class="sm rv-h3">${esc(E.waitingT)}</h3><p class="xs mut">${esc(E.waitingLead)}</p>${S.wait.map(rvCardRow).join('')}`:''}
      ${S.drafts.length?`<details class="rv-drafts"><summary><span class="sm"><b>${esc(E.draftsT)}</b> <span class="mut">(${S.drafts.length})</span></span></summary><p class="xs mut">${esc(E.draftsLead)}</p>${S.drafts.map(rvCardRow).join('')}</details>`:''}</section>`;
  const newsP=`<section class="card rv-pane" id="rv-news" aria-labelledby="rvNewsT"><h2 id="rvNewsT">${esc(E.tabs.news)}</h2><p class="sm mut">${esc(E.newsLead)}</p>
      ${news.length?`<h3 class="sm rv-h3">${esc(E.newsCards(news.length))}</h3>${news.map(m=>rvCardRow({m,why:(state.review.seen[m.id]?'changed':'')})).join('')}`:''}
      <h3 class="sm rv-h3">${esc(E.newsUpd)}</h3>${RV.upd?(RV.upd.length?`<ul class="rv-updl">${RV.upd.slice(0,CONFIG.review.updatesShow).map((u,i)=>rvUpdLi(u,i<nu)).join('')}</ul>`:`<p class="sm mut">${esc(E.updNone)}</p>`):`<p class="sm mut">${esc(RV.updErr?E.updFail:STR.ln.loading)}</p>`}
      ${!news.length&&!nu&&RV.upd?`<p class="sm mut">${esc(E.newsNone)}</p>`:''}
      <div class="row rv-acts"><a class="btn" href="#updates">${esc(E.updatesAll)}</a>${news.length||nu?`<button type="button" class="btn" data-rv="seen" data-fk="rv-seen">${esc(E.seenAll)}</button>`:''}</div></section>`;
  const mineP=`<section class="card rv-pane" id="rv-mine" aria-labelledby="rvMineT"><h2 id="rvMineT">${esc(E.tabs.mine)}</h2><p class="sm mut">${esc(E.mineLead)}</p>
      ${rvStatusLine()}${mine.length?`<ul class="rv-minel">${mine.map(rvMineLi).join('')}</ul>`:`<p class="sm">${esc(E.mineNone)}</p>`}
      <p class="xs mut">${esc(E.mineSign)}</p>
      <div class="row rv-acts"><button type="button" class="btn" data-rv="refresh" data-fk="rv-refresh"${RV.busy?' aria-disabled="true"':''}>${esc(E.refresh)}</button><a class="btn" href="${esc(rvOtherUrl())}" target="_blank" rel="noopener">${esc(E.otherBtn)}<span class="sr"> ${esc(E.newTab)}</span></a></div></section>`;
  v.innerHTML=`<div class="rv-home" data-tab="${esc(tab)}">
    <header class="rv-hd"><h1>${esc(E.hello(CONFIG.review.name))}</h1><p class="mut rv-lead">${esc(E.lead)}</p>
      <div class="row"><a class="btn" href="#rtour">${esc(state.review.tour?E.tourAgain:E.tour)}</a>${editBtn('screen','review','src/js/19-review.js + content/strings.js (STR.rv)')}</div></header>
    <div class="seg rv-tabs" role="group" aria-label="${esc(E.tabsL)}">${tabBtn('todo',S.todo.length)}${tabBtn('news',news.length+nu)}${tabBtn('mine',mine.filter(x=>x.st==='sent'||x.st==='fixing').length)}</div>
    <div class="rv-grid">${todo}${newsP}${mineP}</div>${dbgOn('review')?rvDebugHtml():''}</div>`;
  rvDbg();window.RV_READY=hashOf(ROUTE);
};
function rvDebugHtml(){const mine=rvMine(),c=state.review.cache;
  return `<section class="card rv-dbg"><h2>${esc(STR.rv.dbgT)}</h2><p class="mono">src ${esc(RV.src||'—')} · http ${RV.http||'—'} · rate ${RV.rate??'—'} · cache ${c&&c.at?Math.round((Date.now()-c.at)/60e3)+' min':'—'} · login ${esc(rvLogin())}</p>
    <div class="slog" tabindex="0">${mine.map(x=>esc(`#${x.n} ${x.card||'other'} v${x.ver??'?'} ${x.verdict||'-'} → ${x.st}${x.fixedIn?' v'+x.fixedIn:''}`)).join('\n')||'—'}</div>
    <div class="row"><button type="button" class="btn" data-rv="clear">${esc(STR.rv.dbgClear)}</button>
      <label class="sm">${esc(STR.rv.dbgAs)} <input type="text" id="rvAs" value="${esc(RV.as)}" placeholder="${esc(CONFIG.review.login)}"></label><button type="button" class="btn" data-rv="as">OK</button></div></section>`;}
function rvDbg(){const S=RV.idx?rvSort():null,c=state.review.cache;
  DBG.review=`review ${RV.src||'—'} · issues ${(RV.issues||[]).length} · http ${RV.http||'—'} · rate ${RV.rate??'—'} · cache ${c&&c.at?Math.round((Date.now()-c.at)/60e3)+'m':'—'}${S?' · todo '+S.todo.length:''}`;dbgPaint();}

/* ---------- #rcard=<id> — read the card, answer the plain checklist ---------- */
function rvBodyHtml(card,text){
  return esc(text).replace(/\s*\[(f\d+(?:\s*,\s*f\d+)*)\]/g,(m,ids)=>' '+ids.split(',').map(s=>`<sup class="rv-fn"><span class="sr">${esc(STR.rv.factN(''))}</span>${esc(s.trim().slice(1))}</sup>`).join(''));}
function rvCardHtml(card,lv){const E=STR.rv,src=CD.src||{},secN=src.sections||{};
  const reg=Object.fromEntries((src.registry||[]).map(r=>[r.id,r]));
  const secOf=c=>{try{const p=parseCite(c);return p.sections.map(x=>`${STR.rv.secOf(x.sec||x.ch)}${secN[x.sec||x.ch]?' “'+secN[x.sec||x.ch]+'”':''}`).concat(p.sources.map(x=>reg[x.id]?reg[x.id].name:x.id)).join(' · ');}catch(_){return c;}};   // sources by name, not id (G-Learn)
  const mk=f=>`<span class="rv-mk"><b>${esc(f.mark)}</b> ${esc(E.marks[f.mark]||'')}</span>`;
  const levels=Object.keys(card.body).filter(k=>E.levels[k]);
  const ck=q=>{let a='';if(q.type==='mcq')a=`<ol class="rv-opts" type="A">${q.options.map((o,i)=>`<li${i===q.answer?' class="rv-ok"':''}>${esc(o)}${i===q.answer?` <b>✓ ${esc(E.qRight)}</b>`:''}</li>`).join('')}</ol>`;
    else if(q.type==='order')a=`<p class="xs"><b>${esc(E.qOrder)}:</b></p><ol class="rv-opts">${q.options.map(o=>`<li>${esc(o)}</li>`).join('')}</ol>`;
    else a=`<p class="xs mut">${esc(E.q3d)}</p>`;
    return `<li class="rv-q"><p><b>${esc(q.prompt)}</b></p>${a}${q.why?`<p class="xs"><b>${esc(E.qWhy)}:</b> ${esc(q.why)}</p>`:''}</li>`;};
  return `<section class="rv-sec" id="rvs-obj"><h2 class="rv-h">${esc(E.objT)}</h2><p>${esc(card.objective&&card.objective.text||'')}</p></section>
   <section class="rv-sec" id="rvs-body"><h2 class="rv-h">${esc(E.bodyT)}</h2>
     ${levels.length>1?`<div class="row"><span class="sm mut">${esc(E.readFor)}</span><div class="seg" role="group" aria-label="${esc(E.readFor)}">${levels.map(l=>`<button type="button" data-rvlv="${l}" aria-pressed="${l===lv}">${esc(E.levels[l])}</button>`).join('')}</div></div>`:''}
     <p class="rv-body">${rvBodyHtml(card,card.body[lv]||'')}</p></section>
   <section class="rv-sec" id="rvs-facts"><h2 class="rv-h">${esc(E.factsT)}</h2><ol class="rv-facts">${card.facts.map(f=>`<li value="${esc(f.id.slice(1))}"><span>${esc(f.text)}</span><span class="xs mut rv-src">${esc(secOf(f.cite))} · ${mk(f)}</span></li>`).join('')}</ol></section>
   ${card.misconceptions&&card.misconceptions.length?`<section class="rv-sec" id="rvs-mis"><h2 class="rv-h">${esc(E.misT)}</h2><ul class="rv-mis">${card.misconceptions.map(m=>`<li><p><span class="bad">✗ ${esc(E.wrongL)}</span> ${esc(m.wrong)}</p><p><span class="good">✓ ${esc(E.rightL)}</span> ${esc(m.right)}</p></li>`).join('')}</ul></section>`:''}
   ${card.adult?`<section class="rv-sec" id="rvs-adult"><h2 class="rv-h">${esc(E.adultT)}</h2><p>${rvBodyHtml(card,card.adult)}</p></section>`:''}
   ${card.clinical?`<section class="rv-sec" id="rvs-clin"><h2 class="rv-h">${esc(E.clinT)}</h2><p>${rvBodyHtml(card,typeof card.clinical==='string'?card.clinical:card.clinical.text||'')}</p></section>`:''}
   <section class="rv-sec" id="rvs-qs"><h2 class="rv-h">${esc(E.qT)}</h2><ol class="rv-qs">${card.checks.map(ck).join('')}</ol></section>
   ${card.remember&&card.remember.length?`<section class="rv-sec" id="rvs-rem"><h2 class="rv-h">${esc(E.remT)}</h2><ul class="rv-rem">${card.remember.map(r=>`<li><p><b>${esc(r.q)}</b></p><p class="sm">${esc(E.remA)}: ${rvBodyHtml(card,r.a)}</p></li>`).join('')}</ul></section>`:''}`;}
function rvFormHtml(id,ver){const E=STR.rv,d=rvDraft(id),already=rvMine().some(x=>x.card===id&&x.ver===ver&&x.verdict==='ok');
  return `<h2 id="rvFormT">${esc(E.formT)}</h2>${already?`<p class="sm good">${esc(E.alreadyOk)}</p>`:''}
   <fieldset class="rv-fs"><legend class="rv-h">${esc(E.listT)}</legend>${RV_LIST.map(k=>`<label class="rv-tick"><input type="checkbox" data-rvf="list" value="${k}"${d.list[k]?' checked':''}><span>${esc(E.list[k])}</span></label>`).join('')}<p class="xs mut">${esc(E.listNote)}</p></fieldset>
   <fieldset class="rv-fs"><legend class="rv-h">${esc(E.verdictT)}</legend><div class="rv-verds">${RV_VERD.map(k=>`<button type="button" class="rv-vb v-${k}" data-rvf="verdict" value="${k}" aria-pressed="${d.verdict===k}"><b>${esc(E.verdicts[k])}</b><span class="xs">${esc(E.verdictHelp[k])}</span></button>`).join('')}</div></fieldset>
   <label class="rv-lab" for="rvWhere">${esc(E.whereT)}</label><select id="rvWhere" data-rvf="where"><option value="">${esc(E.whereAny)}</option>${RV_WHERE.map(k=>`<option value="${k}"${d.where===k?' selected':''}>${esc(E.where[k])}</option>`).join('')}</select>
   <label class="rv-lab" for="rvNote">${esc(E.noteT)}</label><textarea id="rvNote" data-rvf="note" rows="4" maxlength="1500" placeholder="${esc(E.notePh)}">${esc(d.note)}</textarea>
   <fieldset class="rv-fs"><legend class="rv-h">${esc(E.sureT)}</legend><div class="seg">${RV_SURE.map(k=>`<button type="button" data-rvf="sure" value="${k}" aria-pressed="${d.sure===k}">${esc(E.sure[k])}</button>`).join('')}</div></fieldset>
   <div id="rvSendBox">${rvSendHtml(id,ver)}</div>`;}
function rvSendHtml(id,ver){const E=STR.rv,d=rvDraft(id),needNote=d.verdict&&d.verdict!=='ok'&&!String(d.note||'').trim();
  return `<a class="btn pri rv-send" id="rvSend" data-rv="send" aria-describedby="rvSendHelp">${esc(E.send)}<span class="sr"> ${esc(E.newTab)}</span></a>
   <p class="xs mut" id="rvSendHelp" role="status">${esc(needNote?E.noteNeed:E.sendHelp)}</p><p class="xs mut">${esc(E.draftKept)} <button type="button" class="btn ghost rv-clear" data-rv="reset" data-fk="rv-reset">${esc(E.clear)}</button></p>`;}
/* Send is updated in place (the help line is a live region that must stay the same node — G-A11y) */
function rvSendSync(id,ver){const a=$('#rvSend');if(!a)return;const d=rvDraft(id),ok=rvFormOk(d);
  if(ok){a.href=rvFormUrl(id,ver,d);a.target='_blank';a.rel='noopener';a.removeAttribute('aria-disabled');a.removeAttribute('role');a.removeAttribute('tabindex');}
  else{a.removeAttribute('href');a.removeAttribute('target');a.setAttribute('role','link');a.setAttribute('aria-disabled','true');a.setAttribute('tabindex','0');}
  /* the help line always says what is needed now (G-A11y r2): after a tap on Send it stays a warning until that need is met */
  const h=$('#rvSendHelp');if(!h)return;const E=STR.rv,need=!d.verdict?'verdict':(d.verdict!=='ok'&&!String(d.note||'').trim())?'note':'';
  const warn=h.classList.contains('rv-warn')&&need,t=warn?(need==='verdict'?E.verdictNeed:E.noteNeed):need==='note'?E.noteNeed:E.sendHelp;
  if(!warn)h.classList.remove('rv-warn');if(h.textContent!==t)h.textContent=t;}
SCREENS.rcard=function(v,prev){const E=STR.rv,id=ROUTE.id;rvTurnOn();rvLoad();rvUseCache();rvFetch(false);
  ROUTE.crumbs=[{label:E.title,hash:'review'},{label:rvCardTitle(id)||id}];
  const card=RV.cards[id];
  if(!card){v.innerHTML=`<h1>${esc(rvCardTitle(id)||id)}</h1><p class="mut">${esc(STR.ln.loading)}</p>`;
    cdCard(id).then(c=>{RV.cards[id]=c;},e=>{RV.cards[id]={err:e.message};}).finally(()=>{if(ROUTE.name==='rcard'&&ROUTE.id===id)render({raw:'(loading)'});});return;}   // a 'route change' so focus moves to the card's h1 (G-A11y)
  if(card.err){v.innerHTML=`<h1>${esc(id)}</h1><p class="bad">${esc(STR.ln.noCard(id))}</p><a class="btn" href="#review">${esc(E.title)}</a>`;return;}
  const ver=card.version||1;if((state.review.seen[id]||0)<ver){state.review.seen[id]=ver;rvSaveR();}
  const lv=RV.open[id]||(card.body.mbbs?'mbbs':'general');
  v.innerHTML=`<div class="rv-card"><header class="rv-chd"><p class="xs mut"><span class="mono">${esc(id)}</span> · ${esc(E.version(ver))}${card.status==='draft'?' · <b>'+esc(E.draftNote)+'</b>':''}</p>
      <h1>${esc(card.title)}</h1><p class="sm mut">${esc(E.cardLead)}</p>
      <div class="row"><a class="btn" href="#card=${esc(id)}">${esc(E.asStudent)}</a><a class="btn rv-jump" href="#rvForm" data-rv="jump">${esc(E.formT)} ↓</a>${editBtn('card',id,'content/E/cards/'+id+'.json')}</div></header>
    <div class="rv-cols"><article class="rv-read" aria-label="${esc(card.title)}">${rvCardHtml(card,lv)}</article>
      <aside class="card rv-form" id="rvForm" aria-labelledby="rvFormT">${rvFormHtml(id,ver)}</aside></div></div>`;
  rvSendSync(id,ver);rvDbg();window.RV_READY=hashOf(ROUTE);
};

/* ---------- #rtour — 3 screens, replayable ---------- */
const RV_TOUR_ICON=['review','cards','progress'];
SCREENS.rtour=function(v){const E=STR.rv,n=E.tourS.length,i=Math.min(n,ROUTE.step||1),s=E.tourS[i-1];
  ROUTE.crumbs=[{label:E.title,hash:'review'},{label:E.tourT}];
  v.innerHTML=`<section class="card rv-tour" aria-labelledby="rvTourH"><p class="xs mut">${esc(E.tourT)} · ${esc(E.step(i,n))}</p>
    <div class="rv-tico" aria-hidden="true">${icon(RV_TOUR_ICON[i-1],56)}</div><h1 id="rvTourH">${esc(s.h)}</h1>
    <ol class="rv-tp">${s.p.map(p=>`<li>${esc(p)}</li>`).join('')}</ol>
    <div class="rv-dots" aria-hidden="true">${E.tourS.map((_,k)=>`<span class="${k===i-1?'on':''}"></span>`).join('')}</div>
    <div class="row rv-tnav">${i>1?`<button type="button" class="btn" data-rvt="${i-1}">${esc(E.tourBack)}</button>`:`<button type="button" class="btn ghost" data-rvt="done">${esc(E.tourSkip)}</button>`}<span class="sp"></span>
      ${i<n?`<button type="button" class="btn pri" data-rvt="${i+1}">${esc(E.tourNext)}</button>`:`<button type="button" class="btn pri" data-rvt="done">${esc(E.tourDone)}</button>`}</div></section>`;
  window.RV_READY=hashOf(ROUTE);
};

/* ---------- #updates ---------- */
SCREENS.updates=function(v){const E=STR.rv;ROUTE.crumbs=[{label:E.title,hash:'review'},{label:E.updT}];rvUpdLoad();
  const nu=rvUpdNew(),k=(ROUTE.page||1)*CONFIG.review.updatesPage,U=RV.upd||[];
  const groups=[];for(const [i,u] of U.slice(0,k).entries()){let g=groups[groups.length-1];if(!g||g.date!==u.date)groups.push(g={date:u.date,items:[]});g.items.push([u,i<nu]);}
  v.innerHTML=`<div class="rv-updp"><h1>${esc(E.updT)}</h1><p class="mut rv-lead">${esc(E.updLead)}</p>
    ${RV.upd?(U.length?groups.map(g=>`<section class="card rv-ug"><h2 class="sm">${esc(g.date)}${g.items.some(x=>x[1])?` <span class="badge rv-new">${esc(E.newCard)}</span>`:''}</h2><ul class="rv-updl">${g.items.map(([u,n])=>rvUpdLi(u,n,true)).join('')}</ul></section>`).join(''):`<p>${esc(E.updNone)}</p>`):`<p class="mut">${esc(RV.updErr?E.updFail:STR.ln.loading)}</p>`}
    ${U.length>k?`<p><button type="button" class="btn" data-rvpage="${(ROUTE.page||1)+1}" data-fk="rv-more">${esc(E.updMore)}</button></p>`:''}</div>`;
  window.RV_READY=hashOf(ROUTE);
};

/* ---------- repaint without losing place (lists change after a fetch) ---------- */
function rvPaint(){if(!['review','rcard','updates'].includes(ROUTE.name))return;
  if(ROUTE.name==='rcard'){const card=RV.cards[ROUTE.id];if(card&&!card.err)rvSendSync(ROUTE.id,card.version||1);rvDbg();return;}
  const y=scrollY;render();scrollTo(0,y);}

/* ---------- events ---------- */
document.addEventListener('click',e=>{
  const tb=e.target.closest('[data-rvtab]');if(tb){go({name:'review',view:tb.dataset.rvtab},{replace:true});return;}
  const tt=e.target.closest('[data-rvt]');if(tt){const s=tt.dataset.rvt;if(s==='done'){state.review.tour=Date.now();rvSaveR();go({name:'review'});}else go({name:'rtour',step:+s},{replace:true});return;}
  const pg=e.target.closest('[data-rvpage]');if(pg){const y=scrollY;go({name:'updates',page:+pg.dataset.rvpage},{replace:true});scrollTo(0,y);return;}
  const lv=e.target.closest('[data-rvlv]');if(lv&&ROUTE.name==='rcard'){RV.open[ROUTE.id]=lv.dataset.rvlv;const art=$('.rv-read'),card=RV.cards[ROUTE.id];if(art&&card){art.innerHTML=rvCardHtml(card,lv.dataset.rvlv);const b=$(`[data-rvlv="${lv.dataset.rvlv}"]`);if(b)b.focus();}return;}
  const f=e.target.closest('button[data-rvf]');if(f&&ROUTE.name==='rcard'){const d=rvDraft(ROUTE.id),k=f.dataset.rvf;d[k]=d[k]===f.value?'':f.value;d.t=Date.now();rvSaveR();
    $$(`button[data-rvf="${k}"]`).forEach(b=>b.setAttribute('aria-pressed',String(d[k]===b.value)));rvPaint();return;}
  const a=e.target.closest('[data-rv]');if(!a)return;const act=a.dataset.rv;
  if(act==='refresh'){if(!RV.busy){rvFetch(true);if(!RV.busy)rvPaint();}return;}   // offline / rate-limited: redraw so the message shows (G-Eng r2)
  if(act==='seen'){for(const m of rvCardsAll())state.review.seen[m.id]=Math.max(state.review.seen[m.id]||0,m.version||1);if(RV.upd&&RV.upd[0])state.review.updKey=RV.upd[0].key;state.review.seenAt=Date.now();rvSaveR();render();const t=$('#rvNewsT');if(t&&!$('[data-fk="rv-seen"]')){t.setAttribute('tabindex','-1');t.focus({preventScroll:true});}return;}   // the button is gone after: focus What's new (G-A11y r2)
  if(act==='jump'){e.preventDefault();const t=$('#rvForm');if(t){t.scrollIntoView({block:'start',behavior:'auto'});const h=$('#rvFormT');if(h){h.setAttribute('tabindex','-1');h.focus({preventScroll:true});}}return;}
  if(act==='send'){const d=rvDraft(ROUTE.id);if(!rvFormOk(d)){e.preventDefault();const h=$('#rvSendHelp');if(h){h.textContent=d.verdict?STR.rv.noteNeed:STR.rv.verdictNeed;h.classList.add('rv-warn');}return;}
    d.sentAt=Date.now();rvSaveR();toast(STR.rv.sentToast);dlog('review','send',ROUTE.id,d.verdict);
    if(FLAGS.test){window.RV_LAST_URL=a.getAttribute('href');if(FLAGS.fixture==='review'){e.preventDefault();}}   // the demo never leaves the app (layout-check reads the URL)
    return;}
  if(act==='reset'){state.review.drafts[ROUTE.id]={list:{},verdict:'',where:'',sure:'',note:'',t:Date.now()};rvSaveR();render();return;}   // an empty draft, newer — a merge with an older save can't bring the old answers back (G-Eng)
  if(act==='clear'){state.review.cache=null;RV.issues=null;RV.src='';RV.limitUntil=0;rvSaveR();render();return;}
  if(act==='as'){const i=$('#rvAs');RV.as=(i&&i.value.trim())||'';state.review.cache=null;RV.issues=null;rvFetch(true);return;}
});
document.addEventListener('keydown',e=>{const a=e.target.closest&&e.target.closest('#rvSend[aria-disabled="true"]');if(a&&(e.key==='Enter'||e.key===' ')){e.preventDefault();a.click();}});
document.addEventListener('change',e=>{const f=e.target.closest('[data-rvf]');if(!f||ROUTE.name!=='rcard')return;const d=rvDraft(ROUTE.id);
  if(f.dataset.rvf==='list')d.list[f.value]=f.checked;else if(f.dataset.rvf==='where')d.where=f.value;d.t=Date.now();rvSaveR();rvPaint();});
document.addEventListener('input',e=>{const f=e.target.closest('textarea[data-rvf="note"]');if(!f||ROUTE.name!=='rcard')return;const d=rvDraft(ROUTE.id);d.note=f.value;d.t=Date.now();rvSaveR();rvPaint();});
addEventListener('online',()=>{if(['review','rcard'].includes(ROUTE.name)){RV.err='';rvFetch(true);}});
