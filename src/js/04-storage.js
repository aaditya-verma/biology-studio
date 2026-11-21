/* Biology Studio — saved state (RULES §A). Owner doc: build/design-plan.md §6. L1 adds cards (statuses) + deck (Remember) + settings.level. L2 adds lessons (step progress) + mix (Mixed review runs). IndexedDB `biostudio` (D-019): stores state / answers / files.
   · A1: fields are only ever added; stFill() back-fills them on load, so old saves keep working (A4).
   · Writes are guarded (DrumPath v35 lesson): the stored rev is read and the new record written in ONE transaction;
     if another tab wrote since, this tab merges the stored copy in first (unions, furthest, newer) and tries again.
   · If the write can't be checked, nothing is written: the change is stashed in localStorage and merged back next start.
   · Save log: last 20 events, this device only (Settings › Storage). Testing mode keeps everything in memory.
   · L1F (T7, G-Eng): the in-memory state now carries what was written — `app` = the running version from load on, `savedAt` = the last
     successful write — so a backup shows the truth and merges pick the newer copy correctly. The backup file name uses the local date. */
'use strict';
let state=null;
const STORE={mode:'mem',db:null,rev:0,timer:0,busy:false,again:false,err:null,merged:0};
/* EDIT: the saved shape. Add a field here AND a default in stFill (never rename or remove — A1). */
function stNew(){return {schema:1,rev:0,app:APP.v,created:Date.now(),settings:{theme:'system',motion:'system',level:CONFIG.learn.level,t:0},last:{route:'today',card:null},visited:{},answers:{},
  cards:{},   // L1: {<card id>:{read,und,exp: first time (ms) each status was reached · checks: runs · best: best score · t: last change}} (B4)
  deck:{},    // L1: Remember deck {<card id>#<r id>:{step, due (ms, local midnight), n: reviews, lapses, t: last change}}
  lessons:{}, // L2: {<ch>:{done:{<step id>: first time}, skip:{<step id>: time}, last: step id the bar showed, t: last change}} (docs/lesson-spec.md §6)
  mix:{runs:[],t:0},   // L2: Mixed review runs [{t, n, ok, go}] (newest CONFIG.learn.mix.keep) — recall stats only (B4)
  review:{on:false,tour:0,seen:{},seenAt:0,updKey:'',drafts:{},cache:null,t:0}};}   // H2 Reviewer mode: on (Review tab) · tour (time seen) · seen {card id: version at last visit} · seenAt (last 'Mark all as seen') · updKey (newest update seen) · drafts {card id: form answers not sent yet} · cache {at, items, etag, status} of her GitHub issues · t: last change
function stFill(s){const d=stNew();s=s&&typeof s==='object'?s:{};
  for(const k of Object.keys(d))if(s[k]===undefined)s[k]=d[k];
  s.settings=Object.assign({},d.settings,s.settings);s.last=Object.assign({},d.last,s.last);
  if(typeof s.visited!=='object'||!s.visited)s.visited={};if(typeof s.answers!=='object'||!s.answers)s.answers={};
  if(typeof s.cards!=='object'||!s.cards||Array.isArray(s.cards))s.cards={};if(typeof s.deck!=='object'||!s.deck||Array.isArray(s.deck))s.deck={};   // L1 back-fill (A1, A4)
  if(typeof s.review!=='object'||!s.review||Array.isArray(s.review))s.review={};s.review=Object.assign({},d.review,s.review);   // H2 back-fill
  for(const k of ['seen','drafts'])if(typeof s.review[k]!=='object'||!s.review[k]||Array.isArray(s.review[k]))s.review[k]={};
  if(typeof s.lessons!=='object'||!s.lessons||Array.isArray(s.lessons))s.lessons={};   // L2 back-fill (A1, A4)
  for(const ch of Object.keys(s.lessons)){const r=s.lessons[ch];if(!r||typeof r!=='object'){delete s.lessons[ch];continue;}for(const k of ['done','skip'])if(typeof r[k]!=='object'||!r[k]||Array.isArray(r[k]))r[k]={};}
  if(typeof s.mix!=='object'||!s.mix||Array.isArray(s.mix))s.mix={};if(!Array.isArray(s.mix.runs))s.mix.runs=[];if(typeof s.mix.t!=='number')s.mix.t=0;
  return s;}
/* merge two saves: visited = newest time per id; answers = union by key, newer wins; settings = newer save wins; rev = max */
function stMerge(a,b){a=stFill(a);b=stFill(b);const newer=(b.savedAt||0)>(a.savedAt||0)?b:a,m=stFill(JSON.parse(JSON.stringify(newer)));
  m.settings=JSON.parse(JSON.stringify((b.settings.t||0)>(a.settings.t||0)?b.settings:a.settings));   // settings: the one changed last wins
  m.visited={...a.visited};for(const[k,t]of Object.entries(b.visited))m.visited[k]=Math.max(m.visited[k]||0,t);
  m.answers={...a.answers};for(const[k,v]of Object.entries(b.answers)){const o=m.answers[k];if(!o||(v&&v.t||0)>(o.t||0))m.answers[k]=v;}
  /* L1: card statuses never go back — each status keeps its earliest time; counts keep the larger; deck prompt = the one changed last */
  m.cards={};for(const id of new Set([...Object.keys(a.cards),...Object.keys(b.cards)])){const x=a.cards[id]||{},y=b.cards[id]||{},o=(x.t||0)>(y.t||0)?{...y,...x}:{...x,...y};   // keep any future field (A1); then the rules
    for(const k of ['read','und','exp']){const v=[x[k],y[k]].filter(n=>typeof n==='number'&&n>0);if(v.length)o[k]=Math.min(...v);else delete o[k];}
    o.checks=Math.max(x.checks||0,y.checks||0);o.best=Math.max(x.best||0,y.best||0);o.t=Math.max(x.t||0,y.t||0);m.cards[id]=o;}
  m.deck={...a.deck};for(const[k,v]of Object.entries(b.deck)){const o=m.deck[k];if(!o||(v&&v.t||0)>(o.t||0))m.deck[k]=v;}
  /* L2: lessons — done/skip keep the earliest time per step (union); last from the copy changed last · mix runs = union by time */
  m.lessons={};for(const ch of new Set([...Object.keys(a.lessons),...Object.keys(b.lessons)])){const x=a.lessons[ch]||{done:{},skip:{},t:0},y=b.lessons[ch]||{done:{},skip:{},t:0},o={done:{},skip:{},last:((y.t||0)>(x.t||0)?y:x).last||null,t:Math.max(x.t||0,y.t||0)};
    for(const k of ['done','skip'])for(const src of [x[k]||{},y[k]||{}])for(const[id,t]of Object.entries(src))o[k][id]=o[k][id]?Math.min(o[k][id],t):t;m.lessons[ch]=o;}
  {const seen=new Set();m.mix={runs:[...a.mix.runs,...b.mix.runs].filter(r=>r&&typeof r.t==='number'&&!seen.has(r.t)&&seen.add(r.t)).sort((p,q)=>p.t-q.t).slice(-CONFIG.learn.mix.keep),t:Math.max(a.mix.t||0,b.mix.t||0)};}
  /* H2: reviewer — on/tour from the copy changed last; seen = the higher version per card; drafts = newer per card; cache = the newer check */
  {const x=a.review,y=b.review,n=(y.t||0)>(x.t||0)?y:x;m.review={...n,seen:{...x.seen},drafts:{...x.drafts}};
    for(const[k,v]of Object.entries(y.seen))m.review.seen[k]=Math.max(m.review.seen[k]||0,v);
    for(const[k,v]of Object.entries(y.drafts)){const o=m.review.drafts[k];if(!o||(v&&v.t||0)>(o.t||0))m.review.drafts[k]=v;}
    m.review.tour=Math.max(x.tour||0,y.tour||0);m.review.seenAt=Math.max(x.seenAt||0,y.seenAt||0);
    m.review.cache=((y.cache&&y.cache.at)||0)>((x.cache&&x.cache.at)||0)?y.cache:x.cache;}
  m.rev=Math.max(a.rev||0,b.rev||0);m.created=Math.min(a.created||Infinity,b.created||Infinity);return m;}

/* save log (this device only) */
let SLOG_MEM=[];
function slogRead(){if(STORE.mode!=='idb')return SLOG_MEM.slice();try{const l=JSON.parse(localStorage.getItem(CONFIG.keys.slog));return Array.isArray(l)?l:[];}catch(_){return [];}}
function slog(ev,o){const e=Object.assign({t:Date.now(),app:APP.v,ev},o||{}),l=slogRead();l.push(e);while(l.length>CONFIG.saveLogMax)l.shift();
  if(STORE.mode!=='idb')SLOG_MEM=l;else try{localStorage.setItem(CONFIG.keys.slog,JSON.stringify(l));}catch(_){}
  dlog('store',ev,o||'');return e;}

/* IndexedDB plumbing */
const idbReq=r=>new Promise((res,rej)=>{r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});
function idbOpen(){return new Promise((res,rej)=>{if(!window.indexedDB)return rej(new Error('IndexedDB not available'));
  const r=indexedDB.open(CONFIG.idb.name,CONFIG.idb.ver);
  r.onupgradeneeded=()=>{const db=r.result;CONFIG.idb.stores.forEach(n=>{if(!db.objectStoreNames.contains(n))db.createObjectStore(n);});};
  r.onsuccess=()=>{const db=r.result;db.onversionchange=()=>{db.close();STORE.db=null;};res(db);};r.onerror=()=>rej(r.error);r.onblocked=()=>rej(new Error('blocked by another tab'));});}
async function idbGet(db){const tx=db.transaction('state','readonly');return (await idbReq(tx.objectStore('state').get('main')))||null;}
/* one readwrite transaction: write only if the stored rev is the one this tab last saw */
function idbPut(db){return new Promise((res,rej)=>{let tx,out=null;try{tx=db.transaction('state','readwrite');}catch(e){return rej(e);}
  tx.oncomplete=()=>res(out);tx.onerror=tx.onabort=()=>{if(out&&!out.ok)res(out);else rej(tx.error||new Error('aborted'));};
  const st=tx.objectStore('state'),g=st.get('main');
  g.onsuccess=()=>{const cur=g.result,cr=cur?cur.rev||0:0;
    if(cur&&cr!==STORE.rev){out={ok:false,why:'changed',cur:cr};try{tx.abort();}catch(_){}return;}
    if(cur&&(cur.app||0)>APP.v){out={ok:false,why:'newer-app',cur:cr};try{tx.abort();}catch(_){}return;}
    const rec=JSON.parse(JSON.stringify(state));rec.rev=cr+1;rec.app=APP.v;rec.savedAt=Date.now();
    st.put(rec,'main');out={ok:true,from:cr,to:rec.rev,at:rec.savedAt};};});}

async function stLoad(){
  if(FLAGS.test){STORE.mode='mem';state=stFill(stNew());slog('load',{mode:'test'});return;}
  try{const db=await idbOpen();STORE.db=db;STORE.mode='idb';const s=await idbGet(db);state=stFill(s);STORE.rev=s?s.rev||0:0;
    if((state.app||0)<APP.v){slog('app',{from:state.app||0,to:APP.v});state.app=APP.v;}   // the running version owns the record from now on (a newer one stays: writes are refused, idbPut)
    let stash=null;try{stash=JSON.parse(localStorage.getItem(CONFIG.keys.stash));}catch(_){}
    if(stash){state=stMerge(state,stash);localStorage.removeItem(CONFIG.keys.stash);slog('stash-merged');stSave();}
    if(navigator.storage&&navigator.storage.persist)navigator.storage.persist().catch(()=>{});
    try{localStorage.setItem(CONFIG.keys.theme,state.settings.theme);}catch(_){}
    slog('load',{rev:STORE.rev,visited:Object.keys(state.visited).length});
  }catch(e){STORE.mode='mem';STORE.err=e.message;state=stFill(stNew());slog('load-failed',{err:e.message});}
}
function stSave(){if(STORE.mode!=='idb')return;clearTimeout(STORE.timer);STORE.timer=setTimeout(stWrite,CONFIG.saveDelayMs);}
async function stWrite(){
  if(STORE.busy){STORE.again=true;return;}STORE.busy=true;
  try{for(let i=0;i<3;i++){
      if(!STORE.db)STORE.db=await idbOpen();
      const r=await idbPut(STORE.db);
      if(r&&r.ok){STORE.rev=r.to;state.rev=r.to;state.savedAt=r.at;state.app=Math.max(state.app||0,APP.v);slog('save',{from:r.from,to:r.to});break;}   // memory = what was written (T7 G-Eng)
      if(r&&r.why==='newer-app'){slog('refused',{why:'a newer app version saved here — reload'});toast('A newer version saved data here. Reload the app.');break;}
      const theirs=await idbGet(STORE.db);state=stMerge(state,theirs);STORE.rev=theirs?theirs.rev||0:0;STORE.merged++;slog('merge',{to:STORE.rev});
    }
  }catch(e){STORE.err=e.message;try{localStorage.setItem(CONFIG.keys.stash,JSON.stringify(state));}catch(_){}slog('save-failed',{err:e.message});STORE.db=null;}
  STORE.busy=false;if(STORE.again){STORE.again=false;stSave();}
}
/* resume: refresh from the store before the next save (stale tabs never overwrite newer data) */
async function stResume(){if(STORE.mode!=='idb'||!STORE.db)return;try{const s=await idbGet(STORE.db);if(s&&(s.rev||0)!==STORE.rev){state=stMerge(state,s);STORE.rev=s.rev||0;slog('resume-merge',{to:STORE.rev});}}catch(_){}}
document.addEventListener('visibilitychange',()=>{if(!document.hidden)stResume();});

/* backup (RULES A3): JSON file of the state record; named by the LOCAL date (05:02 IST on 21 Nov is the 21st, not UTC's 20th — T7) */
const stLocalDate=(d=new Date())=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
function stExport(){const blob=new Blob([JSON.stringify({kind:'biostudio-backup',app:APP.v,exported:new Date().toISOString(),state},null,1)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='biostudio-backup-'+stLocalDate()+'.json';document.body.appendChild(a);a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},1000);slog('export');}
async function stImport(file){const j=JSON.parse(await file.text());if(!j||j.kind!=='biostudio-backup'||!j.state||typeof j.state!=='object')throw new Error(STR.importBad);
  if((j.app||0)>APP.v)throw new Error(STR.importNewer);
  const v=j.state.visited;if(v&&typeof v==='object')for(const k of Object.keys(v))if(typeof v[k]!=='number'||!/^E\d\d\.\d\d\.\d\d$/.test(k))delete v[k];
  const c=j.state.cards;if(c&&typeof c==='object')for(const k of Object.keys(c))if(!/^E\d\d\.\d\d\.\d\d$/.test(k)||!c[k]||typeof c[k]!=='object')delete c[k];
  const num=(o,ks)=>{for(const k of ks)if(k in o){const n=+o[k];if(isFinite(n))o[k]=n;else delete o[k];}};   // a backup is outside data: numbers stay numbers (G-Eng)
  if(c&&typeof c==='object')for(const k of Object.keys(c))num(c[k],['read','und','exp','checks','best','t']);
  const dk=j.state.deck;if(dk&&typeof dk==='object')for(const k of Object.keys(dk)){if(!/^E\d\d\.\d\d\.\d\d#r\d+$/.test(k)||!dk[k]||typeof dk[k]!=='object'){delete dk[k];continue;}num(dk[k],['due','step','n','lapses','t']);if(typeof dk[k].due!=='number')delete dk[k];}
  const ls=j.state.lessons;if(ls&&typeof ls==='object')for(const k of Object.keys(ls)){const r=ls[k];if(!/^E\d\d$/.test(k)||!r||typeof r!=='object'){delete ls[k];continue;}   // L2 (G-Eng: outside data)
    for(const f of ['done','skip']){if(!r[f]||typeof r[f]!=='object'){r[f]={};continue;}for(const id of Object.keys(r[f]))if(!/^E\d\d\.\d\d\.\d\d:(read|check|scene|drill|remember)$/.test(id)||!isFinite(+r[f][id]))delete r[f][id];else r[f][id]=+r[f][id];}
    if(typeof r.last!=='string')r.last=null;num(r,['t']);}
  const mx=j.state.mix;if(mx&&typeof mx==='object'){mx.runs=Array.isArray(mx.runs)?mx.runs.filter(r=>r&&typeof r==='object').map(r=>({t:+r.t,n:+r.n,ok:+r.ok,go:!!r.go})).filter(r=>isFinite(r.t)&&isFinite(r.n)&&isFinite(r.ok)):[];num(mx,['t']);}
  state=stMerge(state,j.state);slog('import',{from:j.app});stSave();return true;}
const stTouch=(id)=>{state.visited[id]=Date.now();stSave();};
