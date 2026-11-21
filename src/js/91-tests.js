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
  // progress map (W1, D-040): addresses, Up, nav only in testing mode, rules on a fixture
  ['progress','progress=board','progress=inputs','step=C1','step=X1.07'].forEach(h=>t('route '+h,hashOf(parseHash('#'+h))===h,hashOf(parseHash('#'+h))));
  t('progress bad view → map',parseHash('#progress=nope').view==='map'&&hashOf(parseHash('#progress=map'))==='progress');
  t('up step → progress',JSON.stringify(upOf(parseHash('#step=C1')))===JSON.stringify({name:'progress'}));
  t('progress nav only in testing mode',navItems().includes('progress')===!!FLAGS.test);
  t('plan: route',parseHash('#progress=plan').view==='plan'&&hashOf(parseHash('#progress=plan'))==='progress=plan');
  t('plan: scheduler loaded',typeof trPlan==='function'&&PLAN_DEF.rows.length===5&&PLAN_DEF.rows.every(r=>STR.tr.pl.rows[r]));
  (()=>{const d={queue:['B'],steps:[{id:'A',type:'Build',status:'done',lock:true,needs:[],inputs:[]},{id:'B',type:'Build',status:'planned',lock:true,needs:['A'],inputs:[]},
      {id:'C',type:'Research',status:'ready',lock:false,needs:['A'],inputs:[]},{id:'D',type:'Review',status:'planned',lock:false,uses:['prof'],needs:[],inputs:[]}]},P=trPlan(d,'2026-11-21');
    t('plan: dates + rows + prof never planned',P.dates.B.start==='2026-11-21'&&P.dates.B.row==='lock'&&P.dates.C.row==='research'&&!P.dates.D&&P.prof.length===1&&P.critical.length>0);})();
  t('tracker rules',TR_RULES.statuses.length===9&&TR_RULES.met.join()==='owner check,done'&&Object.keys(TR_SLUG).length===9&&TR_RULES.statuses.every(s=>STR.tr.st[s]&&STR.tr.stShort[s]&&STR.tr.stHelp[s]));
  (()=>{const S=[{id:'A',status:'done',needs:[],inputs:[]},{id:'B',status:'owner check',needs:['A'],inputs:[]},{id:'C',status:'ready',needs:['B'],inputs:[],lock:true,chat:'Bio · Build · C'},
      {id:'D',status:'planned',needs:['C'],inputs:[{id:'D.q1',status:'open',blocks:true}]}],by={};S.forEach(s=>by[s.id]=s);
    t('can start when needs met (owner check counts)',trBlockers(by.C,by,{text:null}).length===0);
    t('lock held by another chat blocks',trBlockers(by.C,by,trLockOf('- Build lock: Professor · Bio · Build · X · 1 Nov 2026, 10:00 IST')).some(b=>b.k==='lock'));
    t('own lock does not block',trBlockers(by.C,by,trLockOf('- Build lock: Aaditya · Bio · Build · C · 1 Nov 2026, 10:00 IST')).length===0&&trBlockers(by.C,by,trLockOf('- Build lock: Aaditya · Bio · Build · C2 · 1 Nov 2026, 10:00 IST')).length===1);
    t('unmet need + blocking answer listed',(()=>{const b=trBlockers(by.D,by,{text:null});return b.length===2&&b[0].id==='C'&&b[1].k==='input';})());
    t('depths',JSON.stringify(trDepths(S))===JSON.stringify({A:0,B:1,C:2,D:3}));
    t('loop is cut, flagged',(()=>{const L=[{id:'X',status:'planned',needs:['Y']},{id:'Y',status:'planned',needs:['X']}];const d=trDepths(L);return d.X!=null&&trIssues({steps:L}).some(i=>i.includes('loop'));})());
    t('started with unmet need flagged',trIssues({steps:[{id:'P',status:'planned',needs:[]},{id:'Q',status:'in progress',needs:['P']}]}).length===1);})();
  t('lock line parsed',(()=>{const L=trLockOf('## Lock\n- Build lock: Aaditya · Bio · Build · W1 · 19 Nov 2026, 21:49 IST\n');return L.text&&L.at===Date.UTC(2026,10,19,16,19)&&trLockOf('- Build lock: free (x)').text===null;})());
  t('prompt extracted',(()=>{const keep=TR.plan;TR.plan='x\n**Ready prompt — K9** (chat)\n> line one\n> line two\n\n**Ready prompt — K10**\n> other';const p=trPrompt('K9');TR.plan=keep;return p==='line one\nline two';})());
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
  // L1 learning core: addresses, Up, nav, statuses, deck spacing, back-fill + merge (A1)
  ['cards','card=E05.01.01','deck'].forEach(h=>t('route '+h,hashOf(parseHash('#'+h))===h,hashOf(parseHash('#'+h))));
  t('card bad id → list',parseHash('#card=nope').name==='cards'&&parseHash('#card=').name==='cards');
  t('up card → cards · deck → today',JSON.stringify(upOf(parseHash('#card=E05.01.01')))===JSON.stringify({name:'cards'})&&JSON.stringify(upOf(parseHash('#deck')))===JSON.stringify({name:'today'}));
  t('cards in the learner nav',CONFIG.nav.includes('cards')&&navOf(parseHash('#card=E05.01.01'))==='cards');
  t('learn config',CONFIG.learn.deckDays.join()==='1,3,7'&&CONFIG.learn.show.includes('reviewed')&&!CONFIG.learn.show.includes('draft'));
  t('L1 fields back-filled',(()=>{const f=stFill({rev:2,visited:{}});return f.cards&&f.deck&&f.settings.level==='general'&&f.last.card===null;})());
  t('L1 merge: statuses keep earliest, deck newer wins',(()=>{const m=stMerge({cards:{a:{read:5,checks:1,best:.5,t:5}},deck:{'a#r1':{step:1,due:9,t:3}},savedAt:1},{cards:{a:{read:7,und:8,checks:2,best:1,t:8}},deck:{'a#r1':{step:0,due:4,t:6}},savedAt:2});
    return m.cards.a.read===5&&m.cards.a.und===8&&m.cards.a.checks===2&&m.cards.a.best===1&&m.deck['a#r1'].step===0;})());
  t('deck day maths',(()=>{const t0=new Date(2026,10,21,22,30).getTime();return new Date(lnAddDays(t0,1)).getDate()===22&&new Date(lnAddDays(t0,7)).getDate()===28&&new Date(lnAddDays(t0,3)).getHours()===0;})());
  t('status pie shapes',['none','read','und','exp'].every(s=>lnPie(s).includes('<svg'))&&STR.ln.st.exp&&STR.ln.st.und);
  t('guide card rules (D-050)',appCite('APP Deck')==='Deck'&&appCite('APP')===''&&appCite('E05.01')===null&&CARD_RULES.marks.includes('ⓘ'));
  t('L1F viewer strings intact',typeof STR.vw.discT==='string'&&typeof STR.vw.termsT==='string'&&typeof STR.vw.discShort==='function');
  t('L1F backup name = local date',stLocalDate(new Date(2026,10,21,0,30))==='2026-11-21'&&stLocalDate(new Date(2026,0,5,23,59))==='2026-01-05');
  t('L1F due line + fold strings (D-053)',STR.ln.dueOn(STR.ln.tomorrow)==='Due tomorrow'&&!!STR.ln.hidT&&!!STR.ln.readAgain&&typeof STR.ln.srcBook==='function'&&lnRun('none-such')===false);
  t('L1F Sources lists sections + registry, guide says app facts',(()=>{const c={facts:[{cite:'E05.01, E06.06 Tbl 6.4 · R06 CS6',where:'main',text:'x',mark:'✔✔'}],misconceptions:[]},g={facts:[{cite:'APP Card',where:'main',text:'y',mark:'ⓘ'}],misconceptions:[]};
    const a=lnSrcHtml(c),b=lnSrcHtml(g);return a.includes('E05.01')&&a.includes('E06.06')&&a.includes('R06')&&!b.includes('R0')&&b.includes(STR.ln.srcApp.slice(0,10));})());
  t('strings for learn',STR.ln&&STR.nav.cards&&STR.navHint.cards&&typeof STR.ln.passed==='function'&&STR.marks['ⓘ']);
  // tokens present (B3)
  const cs=getComputedStyle(document.documentElement);t('germ tokens set',['epi','hypo','ecto','meso','endo','crest','ctx'].every(k=>cs.getPropertyValue('--g-'+k).trim()));
  t('accent set',cs.getPropertyValue('--accent').trim().toLowerCase()==='#994774');
  // strings: every nav item has a label
  t('strings for nav',CONFIG.nav.every(k=>STR.nav[k]&&STR.navHint[k]));
  // Reviewer mode (H2, D-061): addresses, Up, title/body parse, issue state → words, form link, card sorting, log parse, saved shape
  ['review','review=news','review=mine','rcard=E06.02.01','rtour','rtour=3','updates','updates=2'].forEach(h=>t('route '+h,hashOf(parseHash('#'+h))===h,hashOf(parseHash('#'+h))));
  t('review bad tab → todo',parseHash('#review=nope').view==='todo'&&hashOf(parseHash('#review=todo'))==='review');
  t('rcard bad id → review',parseHash('#rcard=xyz').name==='review');
  t('rtour step: out of range → 1',parseHash('#rtour=9').step===1&&parseHash('#rtour=2').step===2);
  t('up rcard/rtour/updates → review',['rcard=E06.02.01','rtour=2','updates'].every(h=>upOf(parseHash('#'+h)).name==='review'));
  t('strings for review nav',STR.nav.review&&STR.navHint.review&&STR.rv.tourS.length===3);
  t('review nav off in testing mode',!navItems().includes('review')||!FLAGS.test);
  const pt=rvParseTitle('[review] E06.02.01 v2 ✎ Three strips');t('review title parse',pt.card==='E06.02.01'&&pt.ver===2&&pt.verdict==='fix',JSON.stringify(pt));
  t('review title ✓ and ?',rvParseTitle('[review] E05.01.01 v1 ✓ x').verdict==='ok'&&rvParseTitle('[review] E05.01.01 v1 ? x').verdict==='ask');
  t('review feedback title',rvParseTitle('[feedback] hi').kind==='other'&&rvParseTitle('hello')===null);
  const pb=rvParseBody('### Card\n\nE05.02.01 v1 · Notochord\n\n### Overall\n\n? Question');t('review body parse',pb.card==='E05.02.01'&&pb.ver===1&&pb.verdict==='ask',JSON.stringify(pb));
  const I=(o)=>Object.assign({number:1,title:'[review] E05.01.01 v1 ✎ x',state:'open',labels:[{name:'review'}],milestone:null,created_at:'2026-11-21T06:00:00Z',user:{login:CONFIG.review.login}},o);
  t('state open → sent',rvParseIssue(I()).st==='sent');
  t('state fixing label',rvParseIssue(I({labels:[{name:'review'},{name:CONFIG.review.fixingLabel}]})).st==='fixing');
  const fx=rvParseIssue(I({state:'closed',milestone:{title:'v12'}}));t('state closed + milestone → fixed in 12',fx.st==='fixed'&&fx.fixedIn===12);
  t('state closed not planned',rvParseIssue(I({state:'closed',state_reason:'not_planned'})).st==='noChange');
  t('state closed ✓ → done, ? → answered',rvParseIssue(I({state:'closed',title:'[review] E05.01.01 v1 ✓ x'})).st==='done'&&rvParseIssue(I({state:'closed',title:'[review] E05.01.01 v1 ? x'})).st==='answered');
  t('pull requests left out',rvParseIssue(I({pull_request:{}}))===null);
  t('card state: none → todo · same-version ✎ → wait · ✓ → done · older version → todo changed · fixed → todo',
    rvCardState({id:'E05.01.01',version:1},[]).k==='todo'&&rvCardState({id:'E05.01.01',version:1},[rvParseIssue(I())]).k==='wait'
    &&rvCardState({id:'E05.01.01',version:1},[rvParseIssue(I({title:'[review] E05.01.01 v1 ✓ x'}))]).k==='done'
    &&rvCardState({id:'E05.01.01',version:2},[rvParseIssue(I({title:'[review] E05.01.01 v1 ✓ x'}))]).why==='changed'
    &&rvCardState({id:'E05.01.01',version:1},[fx]).why==='fixed');
  {const u=new URL(rvFormUrl('E05.01.01',1,{list:{facts:true},verdict:'fix',where:'body',sure:'mid',note:'Day 16, not 15'})),q=u.searchParams,F=REVIEW_FIELDS;
    t('form link: template, label, title, fields',q.get('template')===CONFIG.review.form&&q.get('labels')===CONFIG.review.label&&/^\[review\] E05\.01\.01 v1 ✎/.test(q.get('title'))
      &&q.get(F.card).startsWith('E05.01.01 v1')&&q.get(F.verdict)===STR.rv.verdicts.fix&&q.get(F.where)===STR.rv.where.body&&q.get(F.sure)===STR.rv.sure.mid
      &&q.get(F.checklist).startsWith('- [x] ')&&q.get(F.checklist).includes('- [ ] ')&&q.get(F.note)==='Day 16, not 15',u.search.slice(0,120));
    t('form link round-trips its own title',rvParseTitle(q.get('title')).verdict==='fix');}
  t('form needs a verdict, a note for ✎ / ?',!rvFormOk({verdict:''})&&!rvFormOk({verdict:'fix',note:' '})&&rvFormOk({verdict:'ok',note:''})&&rvFormOk({verdict:'ask',note:'why?'}));
  {const L=rvParseLog('# Build log\n\n- 21 Nov 2026 · **L1 polish (app v10, D-056 proposed)** · Fix chat · by A. <!--plain: Card fixes.-->\n- 20 Nov 2026 · **X1 Research · Ch 8** · notes\nnot a line');
    t('updates parse: plain line, else title without ids',L.length===2&&L[0].plain==='Card fixes.'&&L[0].title==='L1 polish'&&L[1].plain===''&&L[1].title==='X1 Research · Ch 8',JSON.stringify(L));}
  {const s=stFill({});t('saved shape has review',s.review&&s.review.on===false&&typeof s.review.seen==='object'&&typeof s.review.drafts==='object');
    const m=stMerge({review:{seen:{a:1},drafts:{x:{t:1,note:'old'}},t:1}},{review:{seen:{a:2,b:1},drafts:{x:{t:2,note:'new'}},on:true,t:2}});
    t('merge review: higher seen, newer draft, newer on',m.review.seen.a===2&&m.review.seen.b===1&&m.review.drafts.x.note==='new'&&m.review.on===true,JSON.stringify(m.review));}
  if(typeof lsTests==='function')lsTests(t);   // L2 lessons, Today plans, Mixed review (20-lessons.js)
  dlog('test',out.filter(x=>!x.ok).length+' failed of '+out.length);return out;
}
