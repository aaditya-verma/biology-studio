/* Biology Studio — addresses + history (master plan §8). Owner doc: build/design-plan.md §3.
   Every place has an address: #today · #map · #map=E05 · #concept=E05.02.01 · #x=layer&y=day · #settings · #colours
   · #scene · #scene=sc-E00.01.04&day=16 · #day=16 (V1) · #studio · #studio=E05.01.01[&gate=G-Learn] · #calib (S1, testing mode)
   · #progress · #progress=board · #progress=plan (W2) · #progress=inputs · #step=C1 (W1 progress map) · #cards · #card=E05.01.01 · #deck (L1 learning core; later: #ep=…&t=)
   · #review · #review=news · #review=mine · #rcard=E06.02.01 · #rtour · #rtour=2 · #updates · #updates=2 (H2 Reviewer mode). Back/Forward = the browser's history; Up = the parent address.
   Android Back stays in the app: the first history entry is a base #today; Back at home asks once, a second press within 2 s leaves. */
'use strict';
let ROUTE={name:'today',raw:'today'};
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
  if(name==='card'){r.id=p.get('card')||null;if(!r.id||!/^E\d\d\.\d\d\.\d\d$/.test(r.id))return {name:'cards',raw:h};}   // L1 reader; a bad id → the card list
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
  case 'card':return 'card='+r.id;
  case 'review':return r.view&&r.view!=='todo'?'review='+r.view:'review';case 'rcard':return 'rcard='+r.id;
  case 'rtour':return r.step&&r.step>1?'rtour='+r.step:'rtour';case 'updates':return r.page&&r.page>1?'updates='+r.page:'updates';
  case 'progress':return r.view&&r.view!=='map'?'progress='+r.view:'progress';case 'step':return r.id?'step='+r.id:'progress';
  case 'x':return 'x='+r.x+'&y='+r.y+(r.cell?'&cell='+encodeURIComponent(r.cell):'');default:return r.name;}}
function upOf(r){switch(r.name){case 'concept':return {name:'map',ch:r.ch};case 'map':return r.ch?{name:'map'}:{name:'today'};
  case 'x':return {name:'map'};case 'scene':return r.id?{name:'scene'}:{name:'today'};case 'day':return {name:'scene'};case 'colours':return {name:'settings'};
  case 'studio':return r.id?{name:'studio'}:{name:'today'};case 'calib':return {name:'studio'};case 'step':return {name:'progress'};case 'card':return {name:'cards'};case 'deck':return {name:'today'};
  case 'rcard':case 'rtour':case 'updates':return {name:'review'};default:return r.name===CONFIG.home?null:{name:CONFIG.home};}}
function go(r,opts={}){const h='#'+(typeof r==='string'?r:hashOf(r));
  if(opts.replace){history.replaceState(history.state,'',h);routeChanged();}
  else if(location.hash===h)routeChanged();else location.hash=h;}   // a hash change = one history entry
function goUp(){const u=upOf(ROUTE);if(u)go(u);}
function goBack(){history.back();}
const LEAVE={armed:0};
function routerStart(){
  const target=location.hash||'#'+CONFIG.home;
  if(!(history.state&&history.state.bs)){history.replaceState({bs:'base'},'','#'+CONFIG.home);history.pushState({bs:'app'},'',target);}
  addEventListener('popstate',e=>{
    if(e.state&&e.state.bs==='base'){          // Back pressed at the first page
      if(Date.now()-LEAVE.armed<CONFIG.leaveWindowMs){history.back();return;}
      LEAVE.armed=Date.now();toast(STR.leaveHint);history.pushState({bs:'app'},'','#'+CONFIG.home);routeChanged();}
  });
  addEventListener('hashchange',routeChanged);
  routeChanged();
}
function routeChanged(){const prev=ROUTE;ROUTE=parseHash(location.hash);
  if(!history.state)history.replaceState({bs:'app'},'',location.hash||'#'+CONFIG.home);   // every entry is marked: reloads never add a second base
  dlog('router',prev.raw,'→',ROUTE.raw);
  if(state&&!['settings','colours','studio','calib','progress','step'].includes(ROUTE.name)){state.last.route=hashOf(ROUTE);stSave();}
  render(prev||{});}
