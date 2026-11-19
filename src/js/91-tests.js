/* Biology Studio — in-app tests, run under ?test=1 by tools/layout-check (and by hand: appTests() in the console).
   Owner doc: build/design-plan.md §7. Pure checks only; nothing here writes to storage. EDIT: add a case per new module. */
'use strict';
function appTests(){
  const out=[],t=(name,ok,info)=>out.push({name,ok:!!ok,info:info||''});
  // device classes (§8a matrix)
  const dc=[[360,640,0,'dev-p'],[640,360,0,'dev-pl'],[932,430,0,'dev-pl'],[768,1024,0,'dev-tp'],[1024,768,0,'dev-tl'],[1180,820,0,'dev-tl'],[1366,1024,0,'dev-tl'],[1024,1366,0,'dev-tp'],
    [1280,720,1,'dev-d'],[1366,768,1,'dev-d'],[1920,1080,1,'dev-d'],[800,1280,0,'dev-tp']];
  dc.forEach(([w,h,f,e])=>t('device '+w+'×'+h+(f?' mouse':' touch'),deviceClass(w,h,!!f)===e,deviceClass(w,h,!!f)));
  // router: parse ↔ hash round trip, Up
  ['today','map','map=E05','concept=E05.02.01','x=layer&y=day','settings','colours','scene','scene=sc-E00.01.04','scene=sc-E00.01.04&day=16','scene=sc-E00.01.04&day=15.5','day=16'].forEach(h=>t('route '+h,hashOf(parseHash('#'+h))===h,hashOf(parseHash('#'+h))));
  t('route unknown → home',parseHash('#nope').name===CONFIG.home);
  t('up concept → chapter',JSON.stringify(upOf(parseHash('#concept=E05.02.01')))===JSON.stringify({name:'map',ch:'E05'}));
  t('up home → none',upOf(parseHash('#today'))===null);
  // 3D viewer addresses (V1)
  t('scene day parsed',parseHash('#scene=sc-E00.01.04&day=16').day===16&&parseHash('#scene=sc-E00.01.04').day===undefined);
  t('scene bad day ignored',parseHash('#scene=sc-E00.01.04&day=x').day===undefined);
  t('up scene → list',JSON.stringify(upOf(parseHash('#scene=sc-E00.01.04')))===JSON.stringify({name:'scene'}));
  // Studio (S1)
  ['studio','studio=E05.01.01','studio=E05.01.01&gate=G-Learn','calib'].forEach(h=>t('route '+h,hashOf(parseHash('#'+h))===h,hashOf(parseHash('#'+h))));
  t('studio gate default dropped',hashOf(parseHash('#studio=E05.01.01&gate=G-Sci'))==='studio=E05.01.01');
  t('studio bad gate ignored',parseHash('#studio=E05.01.01&gate=nope').gate===undefined&&parseHash('#studio=E05.01.01&gate=constructor').gate===undefined);
  t('up studio card → list',JSON.stringify(upOf(parseHash('#studio=E05.01.01')))===JSON.stringify({name:'studio'}));
  t('up calib → studio',JSON.stringify(upOf(parseHash('#calib')))===JSON.stringify({name:'studio'}));
  t('studio nav only in testing mode',navItems().includes('studio')===!!FLAGS.test);
  t('card rules mirror spec',CARD_RULES.budget.general===90&&CARD_RULES.budget.mbbs===160&&CARD_RULES.limits.sentence===25&&CARD_RULES.limits.newTerms===3);
  t('cite parse',(()=>{const p=parseCite('E05.01, E06.06 Tbl 6.4 · R06 CS6, E10');return p.sections.length===2&&p.sources[0].id==='R06'&&p.xrefs[0].ch==='E10';})());
  t('cite range refused',(()=>{try{parseCite('E05.01–02');return false;}catch(_){return true;}})());
  t('words skip refs',cWords('Three layers form [f1].')===3&&cSentences('A b [f1]. C d? E.').length===3);
  t('strings for studio',STR.st&&Object.keys(STR.st.checklist).length===17&&STR.nav.studio);
  t('viewer config',CONFIG.viewer&&CONFIG.viewer.dprCap===2&&CONFIG.viewer.scaleSteps.length>3);
  t('strings for viewer',STR.vw&&Object.keys(STR.vw.axes).length===6&&STR.vw.tabs.layers);
  t('motion setting back-filled',stFill({}).settings.motion==='system');
  // storage: fill keeps old saves working (A1/A4); merge never drops (unions)
  const old={rev:3,visited:{a:5}};const f=stFill(JSON.parse(JSON.stringify(old)));t('fill back-fills',f.settings&&f.answers&&f.last&&f.visited.a===5&&f.rev===3);
  const m=stMerge({rev:2,visited:{a:1,b:9},answers:{q:{t:1,v:'x'}},savedAt:1},{rev:4,visited:{a:7},answers:{q:{t:5,v:'y'},r:{t:2}},savedAt:2});
  t('merge unions',m.visited.a===7&&m.visited.b===9&&m.answers.q.v==='y'&&m.answers.r&&m.rev===4);
  // tokens present (B3)
  const cs=getComputedStyle(document.documentElement);t('germ tokens set',['epi','hypo','ecto','meso','endo','crest','ctx'].every(k=>cs.getPropertyValue('--g-'+k).trim()));
  t('accent set',cs.getPropertyValue('--accent').trim().toLowerCase()==='#994774');
  // strings: every nav item has a label
  t('strings for nav',CONFIG.nav.every(k=>STR.nav[k]&&STR.navHint[k]));
  dlog('test',out.filter(x=>!x.ok).length+' failed of '+out.length);return out;
}
