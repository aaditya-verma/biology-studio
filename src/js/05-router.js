/* Biology Studio — addresses + history (master plan §8). Owner doc: build/design-plan.md §3.
   Every place has an address: #today · #map · #map=E05 · #concept=E05.02.01 · #x=layer&y=day · #settings · #colours
   · #scene · #scene=sc-E00.01.04&day=16 · #day=16 (V1; later: #card= · #ep=…&t=). Back/Forward = the browser's history; Up = the parent address.
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
  if(name==='x'){r.x=p.get('x')||CONFIG.xt.x;r.y=p.get('y')||CONFIG.xt.y;if(p.get('cell'))r.cell=p.get('cell');}
  return r;}
function hashOf(r){switch(r.name){case 'map':return r.ch?'map='+r.ch:'map';case 'concept':return 'concept='+r.id;
  case 'scene':return r.id?'scene='+r.id+(r.day!=null?'&day='+(Math.abs(r.day-Math.round(r.day))<0.05?Math.round(r.day):(+r.day).toFixed(1)):''):'scene';
  case 'day':return 'day='+r.day;
  case 'x':return 'x='+r.x+'&y='+r.y+(r.cell?'&cell='+encodeURIComponent(r.cell):'');default:return r.name;}}
function upOf(r){switch(r.name){case 'concept':return {name:'map',ch:r.ch};case 'map':return r.ch?{name:'map'}:{name:'today'};
  case 'x':return {name:'map'};case 'scene':return r.id?{name:'scene'}:{name:'today'};case 'day':return {name:'scene'};case 'colours':return {name:'settings'};default:return r.name===CONFIG.home?null:{name:CONFIG.home};}}
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
  if(!history.state)history.replaceState({bs:'app'},'',location.hash||'#'+CONFIG.home);   // every entry is marked: reloads never add a second basedlog('router',prev.raw,'→',ROUTE.raw);
  if(state&&ROUTE.name!=='settings'&&ROUTE.name!=='colours'){state.last.route=hashOf(ROUTE);stSave();}
  render(prev||{});}
