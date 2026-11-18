/* Biology Studio — saved state (RULES §A). Owner doc: build/design-plan.md §6. IndexedDB `biostudio` (D-019): stores state / answers / files.
   · A1: fields are only ever added; stFill() back-fills them on load, so old saves keep working (A4).
   · Writes are guarded (DrumPath v35 lesson): the stored rev is read and the new record written in ONE transaction;
     if another tab wrote since, this tab merges the stored copy in first (unions, furthest, newer) and tries again.
   · If the write can't be checked, nothing is written: the change is stashed in localStorage and merged back next start.
   · Save log: last 20 events, this device only (Settings › Storage). Testing mode keeps everything in memory. */
'use strict';
let state=null;
const STORE={mode:'mem',db:null,rev:0,timer:0,busy:false,again:false,err:null,merged:0};
/* EDIT: the saved shape. Add a field here AND a default in stFill (never rename or remove — A1). */
function stNew(){return {schema:1,rev:0,app:APP.v,created:Date.now(),settings:{theme:'system',motion:'system',t:0},last:{route:'today'},visited:{},answers:{}};}
function stFill(s){const d=stNew();s=s&&typeof s==='object'?s:{};
  for(const k of Object.keys(d))if(s[k]===undefined)s[k]=d[k];
  s.settings=Object.assign({},d.settings,s.settings);s.last=Object.assign({},d.last,s.last);
  if(typeof s.visited!=='object'||!s.visited)s.visited={};if(typeof s.answers!=='object'||!s.answers)s.answers={};
  return s;}
/* merge two saves: visited = newest time per id; answers = union by key, newer wins; settings = newer save wins; rev = max */
function stMerge(a,b){a=stFill(a);b=stFill(b);const newer=(b.savedAt||0)>(a.savedAt||0)?b:a,m=stFill(JSON.parse(JSON.stringify(newer)));
  m.settings=JSON.parse(JSON.stringify((b.settings.t||0)>(a.settings.t||0)?b.settings:a.settings));   // settings: the one changed last wins
  m.visited={...a.visited};for(const[k,t]of Object.entries(b.visited))m.visited[k]=Math.max(m.visited[k]||0,t);
  m.answers={...a.answers};for(const[k,v]of Object.entries(b.answers)){const o=m.answers[k];if(!o||(v&&v.t||0)>(o.t||0))m.answers[k]=v;}
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
    st.put(rec,'main');out={ok:true,from:cr,to:rec.rev};};});}

async function stLoad(){
  if(FLAGS.test){STORE.mode='mem';state=stFill(stNew());slog('load',{mode:'test'});return;}
  try{const db=await idbOpen();STORE.db=db;STORE.mode='idb';const s=await idbGet(db);state=stFill(s);STORE.rev=s?s.rev||0:0;
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
      if(r&&r.ok){STORE.rev=r.to;state.rev=r.to;slog('save',{from:r.from,to:r.to});break;}
      if(r&&r.why==='newer-app'){slog('refused',{why:'a newer app version saved here — reload'});toast('A newer version saved data here. Reload the app.');break;}
      const theirs=await idbGet(STORE.db);state=stMerge(state,theirs);STORE.rev=theirs?theirs.rev||0:0;STORE.merged++;slog('merge',{to:STORE.rev});
    }
  }catch(e){STORE.err=e.message;try{localStorage.setItem(CONFIG.keys.stash,JSON.stringify(state));}catch(_){}slog('save-failed',{err:e.message});STORE.db=null;}
  STORE.busy=false;if(STORE.again){STORE.again=false;stSave();}
}
/* resume: refresh from the store before the next save (stale tabs never overwrite newer data) */
async function stResume(){if(STORE.mode!=='idb'||!STORE.db)return;try{const s=await idbGet(STORE.db);if(s&&(s.rev||0)!==STORE.rev){state=stMerge(state,s);STORE.rev=s.rev||0;slog('resume-merge',{to:STORE.rev});}}catch(_){}}
document.addEventListener('visibilitychange',()=>{if(!document.hidden)stResume();});

/* backup (RULES A3): JSON file of the state record */
function stExport(){const blob=new Blob([JSON.stringify({kind:'biostudio-backup',app:APP.v,exported:new Date().toISOString(),state},null,1)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='biostudio-backup-'+new Date().toISOString().slice(0,10)+'.json';document.body.appendChild(a);a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},1000);slog('export');}
async function stImport(file){const j=JSON.parse(await file.text());if(!j||j.kind!=='biostudio-backup'||!j.state||typeof j.state!=='object')throw new Error(STR.importBad);
  if((j.app||0)>APP.v)throw new Error(STR.importNewer);
  const v=j.state.visited;if(v&&typeof v==='object')for(const k of Object.keys(v))if(typeof v[k]!=='number'||!/^E\d\d\.\d\d\.\d\d$/.test(k))delete v[k];
  state=stMerge(state,j.state);slog('import',{from:j.app});stSave();return true;}
const stTouch=(id)=>{state.visited[id]=Date.now();stSave();};
