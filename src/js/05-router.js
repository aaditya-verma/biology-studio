/* Biology Studio — addresses + history (master plan §8). Owner doc: build/design-plan.md §3.
   Every place has an address: #today · #map · #map=E05 · #concept=E05.02.01 · #x=layer&y=day · #settings · #colours
   · #scene · #scene=sc-E00.01.04&day=16 · #day=16 (V1) · #studio · #studio=E05.01.01[&gate=G-Learn] · #calib (S1, testing mode)
   · #progress · #progress=board · #progress=plan (W2) · #progress=inputs · #step=C1 (W1 progress map) · #cards · #card=E05.01.01 · #deck (L1 learning core; later: #ep=…&t=)
   · #lessons · #lesson=E05 · #card=E05.01.01&lesson=E05&step=check · #mix · #mix=go · #deck=go (L2 lessons, Today plans, Mixed review — docs/lesson-spec.md)
   · #review · #review=news · #review=mine · #rcard=E06.02.01 · #rtour · #rtour=2 · #updates · #updates=2 (H2 Reviewer mode). Back/Forward = the browser's history; Up = the parent address.
   Android Back stays in the app: the first history entry is a base #today; Back at home asks once, a second press within 2 s leaves.
   U2 (D-084): one in-app history — history.state.n counts the app's steps (1 = the first page above the base); Back shows whenever n > 1
   (canBack), on root tabs and in panels too; closeStack(name) leaves a run of panel steps (concept → linked concept …) in one go.
   Session only (A1): n lives in the browser's history entries, the step names in memory. */
'use strict';
let ROUTE={name:'today',raw:'today'};
const HIST={n:1,names:{},busy:false,push:false};   // busy: a Back/close is in flight (double taps ignored); push: the next unmarked entry is a new step   // n of the current entry; names[n] = route name at that step (this session)
const canBack=()=>HIST.n>1;
function parseHash(h){h=(h||'').replace(/^#/,'');if(!h)return {name:CONFIG.home,raw:''};
  let p;try{p=new URLSearchParams(h.replace(/^([a-z]+)$/,'$1='));}catch(_){return {name:CONFIG.home,raw:h,unknown:true};}   // URLSearchParams decodes; a bad escape never throws past here
  const name=[...p.keys()][0]||CONFIG.home,r={name,raw:h};
  if(!CONFIG.routes.includes(name))return {name:CONFIG.home,raw:h,unknown:true};
  if(name==='map'&&p.get('map'))r.ch=p.get('map');
  if(name==='concept'){r.id=p.get('concept');r.ch=(r.id||'').slice(0,3);}
  if(name==='scene'){r.id=p.get('scene')||null;const d=p.get('day');if(r.id&&d!=null&&d!==''&&isFinite(+d))r.day=+d;}
  if(name==='day'){const d=p.get('day');r.day=isFinite(+d)?+d:null;}
  if(name==='studio'){r.id=p.get('studio')||null;const g=p.get('gate');if(r.id&&g&&Object.hasOwn(CARD_RULES.gates,g))r.gate=g;}
  if(name==='progress'){const v=p.get('progress');r.view=['board','plan','inputs'].includes(v)?v:'map';}
  if(name==='step')r.id=p.get('step')||null;
  if(name==='card'){r.id=p.get('card')||null;if(!r.id||!/^E\d\d\.\d\d\.\d\d$/.test(r.id))return {name:'cards',raw:h};
    const ls=p.get('lesson'),sk=p.get('step');if(ls&&CONFIG.learn.lessons.includes(ls)){r.lesson=ls;if(['read','check','scene','drill','remember'].includes(sk))r.step=sk;}}   // L1 reader; a bad id → the card list · L2: opened from a lesson
  if(name==='lesson'){r.ch=p.get('lesson');if(!r.ch||!/^E\d\d$/.test(r.ch))return {name:'lessons',raw:h};}
  if(name==='mix')r.view=p.get('mix')==='go'?'go':'run';
  if(name==='deck')r.view=p.get('deck')==='go'?'go':'all';
  if(name==='review'){const v=p.get('review');r.view=['news','mine'].includes(v)?v:'todo';}   // H2 Reviewer mode
  if(name==='rcard'){r.id=p.get('rcard')||null;if(!r.id||!/^E\d\d\.\d\d\.\d\d$/.test(r.id))return {name:'review',raw:h,view:'todo'};}
  if(name==='rtour'){const s=+p.get('rtour');r.step=s>=1&&s<=3?Math.floor(s):1;}
  if(name==='updates'){const n=+p.get('updates');r.page=n>=1?Math.floor(n):1;}
  if(name==='x'){r.x=p.get('x')||CONFIG.xt.x;r.y=p.get('y')||CONFIG.xt.y;if(p.get('cell'))r.cell=p.get('cell');}
  return r;}
function hashOf(r){switch(r.name){case 'map':return r.ch?'map='+r.ch:'map';case 'concept':return 'concept='+r.id;
  case 'scene':return r.id?'scene='+r.id+(r.day!=null?'&day='+(Math.abs(r.day-Math.round(r.day))<0.05?Math.round(r.day):(+r.day).toFixed(1)):''):'scene';
  case 'day':return 'day='+r.day;
  case 'studio':return r.id?'studio='+r.id+(r.gate&&r.gate!=='G-Sci'?'&gate='+r.gate:''):'studio';
  case 'card':return 'card='+r.id+(r.lesson?'&lesson='+r.lesson+(r.step?'&step='+r.step:''):'');
  case 'lesson':return 'lesson='+r.ch;case 'mix':return r.view==='go'?'mix=go':'mix';case 'deck':return r.view==='go'?'deck=go':'deck';
  case 'review':return r.view&&r.view!=='todo'?'review='+r.view:'review';case 'rcard':return 'rcard='+r.id;
  case 'rtour':return r.step&&r.step>1?'rtour='+r.step:'rtour';case 'updates':return r.page&&r.page>1?'updates='+r.page:'updates';
  case 'progress':return r.view&&r.view!=='map'?'progress='+r.view:'progress';case 'step':return r.id?'step='+r.id:'progress';
  case 'x':return 'x='+r.x+'&y='+r.y+(r.cell?'&cell='+encodeURIComponent(r.cell):'');default:return r.name;}}
function upOf(r){switch(r.name){case 'concept':return {name:'map',ch:r.ch};case 'map':return r.ch?{name:'map'}:{name:'today'};
  case 'x':return {name:'map'};case 'scene':return r.id?{name:'scene'}:{name:'today'};case 'day':return {name:'scene'};case 'colours':return {name:'settings'};
  case 'studio':return r.id?{name:'studio'}:{name:'today'};case 'calib':return {name:'studio'};case 'step':return {name:'progress'};case 'card':return r.lesson?{name:'lesson',ch:r.lesson}:{name:'cards'};case 'deck':return {name:'today'};
  case 'lesson':return {name:'lessons'};case 'lessons':case 'mix':return {name:'today'};
  case 'rcard':case 'rtour':case 'updates':return {name:'review'};default:return r.name===CONFIG.home?null:{name:CONFIG.home};}}
function go(r,opts={}){const h='#'+(typeof r==='string'?r:hashOf(r));HIST.push=!opts.replace;
  if(opts.replace){history.replaceState(history.state,'',h);routeChanged();}
  else if(location.hash===h)routeChanged();else location.hash=h;}   // a hash change = one history entry
function goUp(){const u=upOf(ROUTE);if(u)go(u);}
function goBack(){if(HIST.busy)return;if(canBack()){HIST.busy=true;setTimeout(()=>{HIST.busy=false;},700);history.back();}else{const u=upOf(ROUTE);if(u)go(u);}}   // U2: Back never leaves the app — with no step behind, it goes Up
function closeStack(name){if(HIST.busy)return;   // D-084 (3): ✕ closes the whole panel stack — back past every consecutive step of this route name
  let k=0;while(HIST.n-k>1&&HIST.names[HIST.n-k]===name)k++;
  if(k&&HIST.names[HIST.n-k]!==undefined&&HIST.names[HIST.n-k]!==name){HIST.busy=true;setTimeout(()=>{HIST.busy=false;},700);history.go(-k);}else{const u=upOf(ROUTE);if(u)go(u,{replace:true});}}
const LEAVE={armed:0};
function routerStart(){
  const target=location.hash||'#'+CONFIG.home;
  if(!(history.state&&history.state.bs)){history.replaceState({bs:'base',n:0},'','#'+CONFIG.home);history.pushState({bs:'app',n:1},'',target);}
  addEventListener('popstate',e=>{
    if(e.state&&e.state.bs==='base'){          // Back pressed at the first page
      if(Date.now()-LEAVE.armed<CONFIG.leaveWindowMs){history.back();return;}
      LEAVE.armed=Date.now();toast(STR.leaveHint);history.pushState({bs:'app',n:1},'','#'+CONFIG.home);routeChanged();return;}
    /* a step between two entries with the same address fires no hashchange: re-read the step here (G-Eng round 2) */
    setTimeout(()=>{const st=history.state;if(st&&st.n!=null&&st.n!==HIST.n)routeChanged();HIST.busy=false;},0);
  });
  addEventListener('hashchange',routeChanged);
  routeChanged();
}
function routeChanged(){const prev=ROUTE;ROUTE=parseHash(location.hash);
  const st0=history.state||{bs:'app'},fresh=HIST.push||!history.state;HIST.push=false;HIST.busy=false;   // an unmarked entry reached by Back (pre-v18 history) counts down, a new one up
  if(st0.n==null)history.replaceState(Object.assign({},st0,{n:st0.bs==='base'?0:fresh?HIST.n+1:Math.max(1,HIST.n-1)}),'',location.hash||'#'+CONFIG.home);   // every entry is marked: reloads never add a second base; a new step = n + 1
  HIST.n=Math.max(1,history.state.n|0);HIST.names[HIST.n]=ROUTE.name;
  dlog('router',prev.raw,'→',ROUTE.raw);
  if(state&&!['settings','colours','studio','calib','progress','step'].includes(ROUTE.name)){state.last.route=hashOf(ROUTE);stSave();}
  render(prev||{});}
