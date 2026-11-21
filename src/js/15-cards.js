/* Biology Studio — cards: data loading, validateCitation, the mark suggester and cardCheck (the app's copy of tools/card-check, S1).
   Owner doc: docs/card-spec.md (format + rules, C2). The Python tool is the CI gate; `tools/card-check/check.py --parity` runs cardCheck() here on
   every card and every selftest case and fails if the two disagree — change both together.
   EDIT: limits in CARD_RULES (mirror LIMITS/VERBS/BUDGET/GATES in tools/card-check/check.py); data paths in CONFIG.cards. */
'use strict';
const CARD_RULES={
  verbs:['explain','describe','identify','label','locate','order','compare','distinguish','predict','name','trace','relate'],
  spatial:['identify','label','locate','order'],
  types:['mcq','order','rotate','day','frames','label','folded'], spatialTypes:['order','frames','label','rotate'],   // card-spec §2a (V2 drills, D-054)
  drill:{altWords:40,frameWords:25,tol:[10,45],tolDefault:25,zoom:[0.5,6],pins:[2,4],items:[2,5],labelWords:3},
  budget:{general:90,school:110,neet:140,mbbs:160,pg:200}, required:['general','mbbs'],
  marks:['✔✔','✔','⚑','✚','≈','ⓘ'], kinds:['concept','guide'], appLocs:['Today','Cards','Card','Check','Explain','Deck','Try it','Watch it','Status','Settings'], statuses:['draft','reviewed','shipped','retired'],
  limits:{sentence:25,newTerms:3,newTermsEx:5,minChecks:2,opt:[3,5],remember:[2,5],showsUp:6},
  gates:{'G-Sci':{checklist:['cited','sections','accuracy','flags','plus','noapprox'],lines:['body','fact','mis','adult','clinical','remember']},
    'G-Learn':{checklist:['objective','checks','refutes','terms','budget','adult'],lines:['obj','terms','check','mis','remember','shows']},
    'G-A11y':{checklist:['alt','input','colour','text125'],lines:[]},
    'G-Owner':{checklist:['owner'],lines:[]}},
  needs:{reviewed:['G-Sci','G-Learn'],shipped:['G-Sci','G-Learn','G-A11y','G-Owner']}
};

/* ---------- data (fetched on first use; Studio only) ---------- */
const CD={src:null,srcP:null,idx:null,idxP:null,files:{},cal:null,calP:null,err:null};
const cdJson=u=>fetch(u,{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(u.split('/').pop()+' HTTP '+r.status);return r.json();});
function cdSources(){if(!CD.srcP)CD.srcP=cdJson(CONFIG.cards.sources).then(j=>(CD.src=j)).catch(e=>{CD.err=e.message;CD.srcP=null;throw e;});return CD.srcP;}
function cdIndex(){if(!CD.idxP)CD.idxP=cdJson(CONFIG.cards.dir+'index.json').then(j=>(CD.idx=j)).catch(e=>{CD.err=e.message;CD.idxP=null;throw e;});return CD.idxP;}
function cdCard(id){if(!CD.files[id])CD.files[id]=cdJson((FLAGS.fixture&&CONFIG.cards.fixtures[id]?CONFIG.cards.fixtures[id]:CONFIG.cards.dir+encodeURIComponent(id)+'.json')).catch(e=>{delete CD.files[id];throw e;});return CD.files[id];}
function cdCal(){if(!CD.calP)CD.calP=cdJson(CONFIG.cards.dir+'calibration.json').then(j=>(CD.cal=j)).catch(e=>{CD.calP=null;throw e;});return CD.calP;}
async function cardsCtx(){await Promise.all([cdSources(),mapLoad(),scIndexLoad()]);
  const sceneFiles=Object.fromEntries(await Promise.all(((SC.idx&&SC.idx.scenes)||[]).map(s=>scFile(s.id).then(S=>[s.id,S],()=>[s.id,null]))));   // drills check against the scene file (V2)
  return {src:CD.src,mapIds:new Set(MAPD.C.map(c=>c.id)),mapTerms:Object.fromEntries(MAPD.C.map(c=>[c.id,c.terms||[]])),scenes:(SC.idx&&SC.idx.scenes)||[],sceneFiles};}

/* ---------- text helpers (same as check.py: strip_refs, words, sentences) ---------- */
const REF_RX=()=>/\[(f\d+(?:\s*,\s*f\d+)*)\]/g;
const stripRefs=t=>String(t||'').replace(REF_RX(),'').replace(/\s+([.,;:!?])/g,'$1').trim();
const cWords=t=>stripRefs(t).split(/\s+/).filter(w=>/[\p{L}\p{N}_]/u.test(w)).length;
const cSentences=t=>String(t||'').trim().split(/(?<=[.!?])\s+/).map(s=>s.trim()).filter(Boolean);
const cRefs=s=>[...String(s).matchAll(REF_RX())].flatMap(m=>m[1].split(',').map(x=>x.trim()));

/* ---------- citations (card-spec §4; tools/card-check/citations.py) ---------- */
const SEC_RX=/^(E\d\d)(?:\.(\d\d))?(?:\s+(.+))?$/, SRC_RX=/^(R\d\d[a-z]?)(?:\s+(.+))?$/;
const locOk=l=>l==null||/^(CC|MR|Tbl \d+\.\d+|Fig \d+\.\d+|CS\d{1,2}(?:[–-]\d{1,2})?|p \d+)$/.test(l);
function parseCite(cite){
  if(typeof cite!=='string'||!cite.trim())throw new Error('empty citation');
  const c=cite.trim().replace(/^\[+|\]+$/g,'').trim();
  if(/E\d\d(?:\.\d\d)?\s*[–-]\s*\d/.test(c))throw new Error('no ranges — write each section (E05.01, E05.02)');
  const parts=c.split('·').map(p=>p.trim());if(parts.length>2)throw new Error("one ' · ' only (sections · sources)");
  const left=parts[0],right=parts.length===2?parts[1]:'',out={sections:[],sources:[],xrefs:[]};
  if(left)for(const tok of left.split(',').map(t=>t.trim())){const m=tok.match(SEC_RX);if(!m)throw new Error(`'${tok}' is not a book section (E05.01)`);
    if(!locOk(m[3]))throw new Error(`unknown locator '${m[3]}' (CC, Tbl 6.4, Fig 6.1, CS7)`);out.sections.push({ch:m[1],sec:m[2]?m[1]+'.'+m[2]:null,loc:m[3]||null});}
  if(right)for(const tok of right.split(',').map(t=>t.trim())){let m=tok.match(SRC_RX);
    if(m){if(!locOk(m[2]))throw new Error(`unknown locator '${m[2]}' after ${m[1]}`);out.sources.push({id:m[1],loc:m[2]||null});continue;}
    m=tok.match(SEC_RX);if(m){out.xrefs.push({ch:m[1],sec:m[2]?m[1]+'.'+m[2]:null});continue;}
    throw new Error(`'${tok}' is not a registry source (R06 CS6) or a cross-chapter ref (E10)`);}
  if(!out.sections.length&&!out.sources.length)throw new Error('cites nothing');
  return out;}
function validateCitation(cite,src){
  let p;try{p=parseCite(cite);}catch(e){return {errors:[e.message],parsed:null};}
  const errs=[],reg=Object.fromEntries(src.registry.map(r=>[r.id,r]));
  for(const s of [...p.sections,...p.xrefs]){if(s.sec&&!src.sections[s.sec])errs.push(`section ${s.sec} is not in index/tree.json`);else if(!s.sec&&!src.chapters[s.ch])errs.push(`chapter ${s.ch} is not in index/tree.json`);}
  for(const s of p.sources){if(!reg[s.id])errs.push(`${s.id} is not in the source registry`);else if(s.id==='R00')errs.push('R00 is the book — cite its section instead');}
  return {errors:errs,parsed:p};}
function suggestMark(parsed,decision,src){if(!parsed)return '≈';if(decision)return '⚑';if(!parsed.sections.length)return '✚';
  const reg=Object.fromEntries(src.registry.map(r=>[r.id,r]));return parsed.sources.some(s=>(reg[s.id]||{}).tier===1)?'✔✔':'✔';}

/* ---------- review lines (card-spec §5) ---------- */
function cardLines(card){const L={obj:['obj'],terms:['terms'],body:[],fact:[],mis:[],check:[],adult:[],clinical:[],remember:[],shows:[]};
  for(const [lvl,t] of Object.entries(card.body||{}))cSentences(t).forEach((_,i)=>L.body.push(`body.${lvl}.${i+1}`));
  L.fact=(card.facts||[]).map(f=>f.id);L.mis=(card.misconceptions||[]).map(m=>m.id);L.check=(card.checks||[]).map(q=>q.id);if(card.adult)L.adult=['adult'];if(card.clinical)L.clinical=['clinical'];
  L.remember=(card.remember||[]).filter(r=>r!==null&&typeof r==='object'&&!Array.isArray(r)).map(r=>r.id);const su=card.shows_up;if(Array.isArray(su)?su.length:(su!==null&&typeof su==='object'?Object.keys(su).length:su))L.shows=['shows_up'];return L;}
const gateLines=(card,g)=>{const L=cardLines(card);return CARD_RULES.gates[g].lines.flatMap(k=>L[k]);};

/* ---------- cardCheck: mirror of tools/card-check/check.py card_check() ---------- */
/* guide cards (D-050): a fact about the app cites `APP <screen>` and is marked ⓘ — same rules as check.py app_cite/app_rules */
function appCite(c){if(typeof c!=='string')return null;const m=/^APP(?: (.+))?$/.exec(c.trim().replace(/^\[+|\]+$/g,'').trim());return m?(m[1]||''):null;}
function appRules(cite,mk,line,guide,E){const loc=appCite(cite);
  if(!guide)E('E-cite',line,'APP cites belong to guide cards only (kind: guide)');
  else if(loc&&!CARD_RULES.appLocs.includes(loc))E('E-cite',line,`unknown app screen '${loc}' (${CARD_RULES.appLocs.join(', ')})`);
  if(mk!=='ⓘ')E('E-mark',line,'an APP cite is marked ⓘ');}
function cardCheck(card,stem,ctx){
  const R=CARD_RULES,out=[],E=(code,line,msg)=>out.push({lvl:'E',code,line,msg}),W=(code,line,msg)=>out.push({lvl:'W',code,line,msg}),src=ctx.src;
  const isObj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
  const want={spec:'int',id:'str',version:'int',book:'str',status:'str',title:'str',tier:'str',objective:'dict',body:'dict',facts:'list',terms:'dict',misconceptions:'list',checks:'list',scene:'dict',made:'dict',review:'dict',log:'list',remember:'list'};
  const ok={int:Number.isInteger,str:x=>typeof x==='string',dict:isObj,list:Array.isArray};
  for(const [k,t] of Object.entries(want))if(!ok[t](card[k]))E('E-schema',k,`'${k}' missing or not ${t}`);
  if(out.length)return out;
  /* shapes inside the fields (a badly typed card is reported, never a crash — G-Eng R3) */
  if(!Object.values(card.body).every(v=>typeof v==='string'))E('E-schema','body','every level text must be text');
  for(const k of ['facts','misconceptions','checks'])if(card[k].some(x=>!isObj(x)))E('E-schema',k,`each item in '${k}' must be an object`);
  for(const k of ['new','known']){const v=k in card.terms?card.terms[k]:[];if(!Array.isArray(v)||v.some(t=>typeof t!=='string'))E('E-schema','terms',`terms.${k} must be a list of glossary ids`);}
  const ov='verb' in card.objective?card.objective.verb:'',ot='text' in card.objective?card.objective.text:'';
  if(typeof ov!=='string'||typeof ot!=='string')E('E-schema','obj','objective verb and text must be text');
  for(const q of card.checks)if(isObj(q)&&'options' in q&&!Array.isArray(q.options))E('E-schema','checks','check options must be a list');
  if(out.length)return out;
  if(card.spec!==1||card.version<1||!R.statuses.includes(card.status)||!['A','B','C','D'].includes(card.tier))E('E-schema','card','spec must be 1, version ≥ 1, status draft/reviewed/shipped/retired, tier A–D');
  for(const k of ['by','role','agent','date'])if(!card.made[k])E('E-schema','made',`made.${k} missing`);
  const st=card.status,final=st==='reviewed'||st==='shipped',kind=card.kind??'concept',guide=kind==='guide';
  if(!R.kinds.includes(kind))E('E-schema','card',`kind must be one of ${R.kinds.join(', ')}`);
  else if(guide&&!String(card.id).startsWith('E00.'))E('E-kind','card','a guide card lives in Part 0 (E00) only');
  if(card.id!==stem)E('E-id','card',`id ${card.id} ≠ file name ${stem}`);
  if(!ctx.mapIds.has(card.id))E('E-id','card',`${card.id} is not a concept in map.json`);
  const ob=card.objective,verb=ob.verb||'',text=String(ob.text||'').trim();
  if(!text)E('E-objective','obj','objective text missing');
  else if(!R.verbs.includes(verb))E('E-objective','obj',`verb '${verb}' not in the list`);
  else if(!text.toLowerCase().startsWith(verb+' '))E('E-objective','obj',`objective must start with its verb '${verb}'`);
  else if(new RegExp('\\b(?:and|then|,)\\s+('+R.verbs.join('|')+')\\b').test(text.toLowerCase()))E('E-objective','obj','one verb per objective');
  const fids=card.facts.map(f=>f.id);
  for(const lvl of R.required)if(!String(card.body[lvl]||'').trim())E('E-level','body.'+lvl,`level '${lvl}' missing`);
  const sentRules=(txt,prefix)=>cSentences(txt).forEach((s,i)=>{const ln=(prefix==='adult'||prefix==='clinical')?prefix:`${prefix}.${i+1}`;
    if(cWords(s)>R.limits.sentence)E('E-sentence',ln,`${cWords(s)} words > ${R.limits.sentence}`);
    const refs=cRefs(s);if(!refs.length&&!stripRefs(s).endsWith('?'))E('E-ref',ln,'sentence has no fact ref [f1] (only a question may go without)');
    for(const r of refs)if(!fids.includes(r))E('E-ref',ln,`ref ${r} points at no fact`);});
  for(const [lvl,txt] of Object.entries(card.body)){
    if(!(lvl in R.budget)){E('E-schema','body.'+lvl,`unknown level '${lvl}'`);continue;}
    if(cWords(txt)>R.budget[lvl])E('E-words','body.'+lvl,`${cWords(txt)} words > ${R.budget[lvl]} for ${lvl}`);
    sentRules(txt,'body.'+lvl);}
  if(card.adult)sentRules(card.adult,'adult');
  if('clinical' in card&&!(typeof card.clinical==='string'&&card.clinical.trim()))E('E-schema','clinical','clinical must be text (leave it out if the concept has no clinical link)');
  else if(card.clinical)sentRules(card.clinical,'clinical');
  /* Remember prompts + Where it shows up (card-spec §2) */
  const [rlo,rhi]=R.limits.remember,rem=card.remember;
  if(!(rem.length>=rlo&&rem.length<=rhi))E('E-remember','remember',`${rem.length} prompts — need ${rlo}–${rhi}`);
  const mainIds=card.facts.filter(f=>f.where==='main').map(f=>f.id),rseen=new Set();
  for(const r of rem){if(!isObj(r)){E('E-remember','remember','each prompt is {id, q, a}');continue;}
    const rid=String(r.id||'r?');if(!/^r\d+$/.test(rid)||rseen.has(rid))E('E-remember',rid,'prompt id must be r1, r2… and unique');rseen.add(rid);
    const q=String(r.q||'').trim(),a=String(r.a||'').trim();
    if(!q.endsWith('?'))E('E-remember',rid,'q must be a question (ends with ?)');
    if(!a)E('E-remember',rid,'a (the answer) missing');
    for(const t of [q,a])if(cWords(t)>R.limits.sentence)E('E-sentence',rid,`${cWords(t)} words > ${R.limits.sentence}`);
    const refs=cRefs(a);if(a&&!refs.length)E('E-ref',rid,'answer has no fact ref [f1]');
    for(const x of refs)if(!mainIds.includes(x))E('E-ref',rid,`ref ${x} is not a main fact (Remember tests the card, not More)`);}
  if('shows_up' in card){const su=card.shows_up;
    if(!Array.isArray(su)||!su.length||su.length>R.limits.showsUp)E('E-shows','shows_up',`shows_up must be a list of 1–${R.limits.showsUp} concept ids`);
    else{for(const x of su)if(!ctx.mapIds.has(x)||x===card.id)E('E-shows','shows_up',`${String(x)} is not another concept in map.json`);
      if(new Set(su.map(String)).size!==su.length)E('E-shows','shows_up','concept ids repeat');}}
  const seen=new Set(),reg=Object.fromEntries(src.registry.map(r=>[r.id,r]));
  for(const f of card.facts){const fid=String(f.id||'f?');
    if(typeof f.id!=='string'||!/^f\d+$/.test(fid)||seen.has(fid))E('E-schema',fid,'fact id must be f1, f2… and unique');seen.add(fid);
    if(typeof f.text!=='string'||!f.text.trim())E('E-schema',fid,'fact text missing or not text');
    for(const s of cSentences(f.text||''))if(cWords(s)>R.limits.sentence)E('E-sentence',fid,`${cWords(s)} words > ${R.limits.sentence}`);
    if(f.where!=='main'&&f.where!=='more')E('E-schema',fid,"where must be 'main' or 'more'");
    if(appCite(f.cite)!==null){appRules(f.cite,f.mark,fid,guide,E);continue;}
    const v=validateCitation(f.cite,src);v.errors.forEach(e=>E('E-cite',fid,e));
    const mk=f.mark;
    if(!R.marks.includes(mk)){E('E-mark',fid,'mark missing or unknown');continue;}
    if(mk==='ⓘ'){E('E-mark',fid,'ⓘ needs an APP cite in a guide card');continue;}
    if(!v.parsed)continue;const p=v.parsed,t1=p.sources.some(s=>(reg[s.id]||{}).tier===1);
    if(mk==='✔✔'&&!(p.sections.length&&t1))E('E-mark',fid,'✔✔ needs a book section and a Tier 1 source');
    if(mk==='✔'&&!p.sections.length)E('E-mark',fid,'✔ needs a book section');
    if(mk==='⚑'){if(!f.decision||!src.decisions.includes(f.decision))E('E-mark',fid,'⚑ needs decision: D-0xx that exists in DECISIONS');
      if(!card.facts.some(x=>x.where==='more'))E('E-mark',fid,"⚑ needs the newer evidence as a 'more' fact");}
    if(mk==='✚'){if(f.where!=='more')E('E-mark',fid,'✚ lives in More only');if(!t1)E('E-mark',fid,'✚ needs a Tier 1 source');
      if(!String(f.text||'').toLowerCase().includes('beyond langman'))E('E-mark',fid,"✚ text must say 'beyond Langman'");}
    if(mk==='≈')(final?E:W)(final?'E-approx':'W-approx',fid,'≈ blocks reviewed/shipped (B1)');}
  const tn=card.terms.new||[],tk=card.terms.known||[];
  const ex=card.terms.exception;
  if(ex!=null&&!src.decisions.includes(ex))E('E-terms','terms',`terms exception ${ex} is not in DECISIONS`);
  else if(tn.length>(ex?R.limits.newTermsEx:R.limits.newTerms))E('E-terms','terms',`${tn.length} new terms > ${ex?R.limits.newTermsEx+' (D2 exception '+ex+')':R.limits.newTerms+' (D2)'}`);
  for(const t of [...tn,...tk])if(!src.terms[t])E('E-terms','terms',`${t} is not a glossary term`);
  for(const t of ctx.mapTerms[card.id]||[])if(![...tn,...tk].includes(t))W('W-terms','terms',`map term ${t} not in the card's terms`);
  const mids=[];
  for(const m of card.misconceptions){const mid=m.id||'m?';mids.push(mid);
    for(const k of ['wrong','right','cite','mark'])if(!m[k])E('E-mis',mid,`${k} missing`);
    if(m.cite&&appCite(m.cite)!==null)appRules(m.cite,m.mark,mid,guide,E);
    else if(m.cite){validateCitation(m.cite,src).errors.forEach(e=>E('E-cite',mid,e));if(m.mark==='ⓘ')E('E-mark',mid,'ⓘ needs an APP cite in a guide card');}
    if(m.mark&&!R.marks.includes(m.mark))E('E-mark',mid,`unknown mark ${m.mark}`);
    if(m.mark==='≈')(final?E:W)(final?'E-approx':'W-approx',mid,'≈ blocks reviewed/shipped');}
  const qs=card.checks,SF=(ctx.sceneFiles||{})[card.scene.id]||null;
  if(qs.length<R.limits.minChecks)E('E-checks','checks',`${qs.length} checks < ${R.limits.minChecks}`);
  for(const q of qs){const qid=q.id||'q?',opts=q.options||[],[lo,hi]=R.limits.opt,ty=q.type,known=R.types.includes(ty);
    if(!known)E('E-check',qid,`type must be one of ${R.types.join(', ')}`);
    if(!String(q.prompt||'').trim())E('E-check',qid,'prompt missing');
    if(['mcq','order','rotate','label'].includes(ty)||!known){
      if(!(opts.length>=lo&&opts.length<=hi)||opts.some(o=>!(typeof o==='string'&&o.trim())))E('E-check',qid,`${lo}–${hi} non-empty options`);
      if(new Set(opts.filter(o=>typeof o==='string').map(o=>o.trim().toLowerCase())).size!==opts.length)E('E-check',qid,'options repeat — exactly one right answer');}
    if(['mcq','rotate','day'].includes(ty)&&!(Number.isInteger(q.answer)&&q.answer>=0&&q.answer<opts.length))E('E-check',qid,'answer must be the index of the one right option');
    if(['order','frames','label','folded'].includes(ty)&&q.answer!==undefined&&q.answer!==null)E('E-check',qid,`a ${ty} check has no answer field (card-spec §2a)`);
    if(DRILL_TYPES.includes(ty))drillRules(q,qid,ty,opts,SF,E);
    if(!String(q.why||'').trim())E('E-check',qid,'why missing');
    if(q.tests!=='objective')E('E-check',qid,"tests must be 'objective' (H1)");
    if(q.refutes&&!mids.includes(q.refutes))E('E-check',qid,`refutes ${q.refutes}, which is not a misconception here`);}
  if(qs.length&&!qs.some(q=>q.refutes))E('E-checks','checks','no check refutes a misconception');
  if(R.spatial.includes(verb)&&!qs.some(q=>R.spatialTypes.includes(q.type)))E('E-checks','checks',`spatial verb '${verb}' needs a spatial check (order, frames, label or rotate)`);
  const sc=card.scene.id,S=ctx.scenes.find(s=>s.id===sc);
  if(!sc||!S)E('E-scene','scene',`scene ${sc} not found`);
  else{if(!S.cards.includes(card.id))W('W-scene-cards','scene',`${sc} does not list ${card.id}`);
    const d=card.scene.day;if(d!=null&&!(typeof d==='number'&&S.days[0]<=d&&d<=S.days[1]))E('E-scene','scene',`day ${d} outside ${sc} days ${S.days[0]}–${S.days[1]}`);}
  if(R.needs[st])for(const g of R.needs[st]){const r=card.review[g]||{};
    if(r.result!=='pass'){E('E-status',g,`${st} needs ${g} = pass`);continue;}
    for(const k of ['by','role','agent','date'])if(!r[k])E('E-status',g,`${g}.${k} missing`);
    if(g!=='G-Owner'&&(r.role===card.made.role||r.agent===card.made.agent))E('E-status',g,`${g} reviewer must differ from the maker (role and agent)`);
    if(g==='G-Owner'&&r.role!=='Owner')E('E-status',g,"G-Owner is the owner's");
    const miss=R.gates[g].checklist.filter(c=>!(r.checklist||{})[c]);if(miss.length)E('E-status',g,`${g} checklist not ticked: ${miss.join(', ')}`);
    for(const ln of gateLines(card,g)){const v=(r.lines||{})[ln];if(v!=='ok')E('E-status',g,`${g} line ${ln} is ${v||'not reviewed'}`);}}
  return out;}

/* ---------- 3D drills (card-spec §2a) — mirror of drill_rules() in tools/card-check/check.py (--parity) ---------- */
const DRILL_TYPES=['rotate','day','frames','label','folded'];
function sceneAnchors(S){const out=new Set();
  for(const p of S.parts||[]){const k=p.kind;
    if(k==='disc')Object.keys(p.layers||{}).forEach(x=>out.add(x));
    else if(k==='notochord'){const L=p.layers||{};if('notochord' in L)['noto-cord','noto-plate','notochord'].forEach(x=>out.add(x));if('prechordal' in L)out.add('prechordal');}
    else if(k==='axes')['cranial','caudal','left','right','dorsal','ventral'].forEach(a=>out.add('axis-'+a));
    else if(k==='planes')(p.planes||[]).forEach(pl=>out.add('plane-'+pl.id));
    else if(k==='ruler')out.add('ruler');}
  return out;}
/* same maths as viewAngle() in 14-scene3d.mjs (the engine may not be loaded in Studio) */
function cdViewAngle(a1,e1,a2,e2){const B=(az,el)=>{const a=az*Math.PI/180,e=el*Math.PI/180,b=[Math.cos(e)*Math.cos(a),Math.cos(e)*Math.sin(a),Math.sin(e)],n=Math.hypot(b[1],b[0])||1,r=[-b[1]/n,b[0]/n,0];
  return [r,[b[1]*r[2]-b[2]*r[1],b[2]*r[0]-b[0]*r[2],b[0]*r[1]-b[1]*r[0]],b];};const A=B(a1,e1),C=B(a2,e2);let tr=0;for(let i=0;i<3;i++)for(let j=0;j<3;j++)tr+=A[i][j]*C[i][j];
  return Math.acos(Math.max(-1,Math.min(1,(tr-1)/2)))*180/Math.PI;}
const cdNum=x=>typeof x==='number'&&isFinite(x);
function cdViewOf(v,S){if(typeof v==='string'){const m=(S.views||[]).find(w=>w.id===v);return m?[m.azimuth_deg,m.elevation_deg]:null;}
  if(v&&typeof v==='object'&&!Array.isArray(v)&&cdNum(v.azimuth_deg)&&cdNum(v.elevation_deg))return [v.azimuth_deg,v.elevation_deg];return null;}
function showRules(sh,S,qid,E,where='show'){const D=CARD_RULES.drill;
  if(!sh||typeof sh!=='object'||Array.isArray(sh)){E('E-check',qid,`${where} missing (the scene state the drill opens at)`);return;}
  const d=sh.day;if(!cdNum(d))E('E-check',qid,`${where}.day must be a number`);
  else if(S&&!(S.days[0].day<=d&&d<=S.days[S.days.length-1].day))E('E-drill',qid,`${where}.day ${d} outside the scene's days`);
  if('view' in sh&&S&&cdViewOf(sh.view,S)===null)E('E-drill',qid,`${where}.view ${sh.view} is not a view of ${S.id}`);
  const z=sh.zoom===undefined?1:sh.zoom;if(!(cdNum(z)&&z>=D.zoom[0]&&z<=D.zoom[1]))E('E-check',qid,`${where}.zoom outside ${D.zoom[0]}–${D.zoom[1]}`);
  const c=sh.cut;if(c!==undefined&&c!==null&&!(typeof c==='object'&&['x','y'].includes(c.axis)&&cdNum(c.at)&&c.at>=-0.9&&c.at<=0.9&&typeof c.on==='boolean'))E('E-check',qid,`${where}.cut must be {axis x|y, at −0.9…0.9, on}`);
  else if(c!==undefined&&c!==null&&'slab_mm' in c&&!(cdNum(c.slab_mm)&&c.slab_mm>=0.002&&c.slab_mm<=0.5&&c.axis==='x'))E('E-check',qid,`${where}.cut.slab_mm must be 0.002–0.5 on a cross-section (axis x)`);
  const ly=sh.layers;if(ly!==undefined&&ly!==null){if(typeof ly!=='object'||Array.isArray(ly)||Object.values(ly).some(v=>typeof v!=='boolean'))E('E-check',qid,`${where}.layers must map layer ids to true/false`);
    else if(S){const ids=new Set((S.layers||[]).map(l=>l.id));for(const k of Object.keys(ly))if(!ids.has(k))E('E-drill',qid,`${where}.layers: ${k} is not a layer of ${S.id}`);}}}
function drillRules(q,qid,ty,opts,S,E){const D=CARD_RULES.drill,[lo,hi]=CARD_RULES.limits.opt,isInt=Number.isInteger,obj=x=>x&&typeof x==='object'&&!Array.isArray(x),wc=t=>String(t).split(/\s+/).filter(Boolean).length;
  const alt=()=>{const a=q.alt;if(!(typeof a==='string'&&a.trim()))E('E-check',qid,"alt missing (the drill's text alternative)");else if(wc(a)>D.altWords)E('E-check',qid,`alt over ${D.altWords} words`);};
  if(ty==='rotate'){showRules(q.show,S,qid,E);alt();
    let tol=q.tol_deg===undefined?D.tolDefault:q.tol_deg;if(!(cdNum(tol)&&tol>=D.tol[0]&&tol<=D.tol[1])){E('E-check',qid,`tol_deg outside ${D.tol[0]}–${D.tol[1]}`);tol=D.tolDefault;}
    const t=S&&typeof q.target==='string'?cdViewOf(q.target,S):null;
    if(typeof q.target!=='string')E('E-check',qid,'target must be a scene view id');else if(S&&t===null)E('E-drill',qid,`target ${q.target} is not a view of ${S.id}`);
    const sv=S&&obj(q.show)?cdViewOf(q.show.view,S):null;
    if(S&&obj(q.show)&&!('view' in q.show))E('E-check',qid,'show.view needed (the start view)');
    if(t&&sv&&cdViewAngle(sv[0],sv[1],t[0],t[1])<=tol)E('E-drill',qid,`starts within ${tol}° of the target — already solved`);}
  else if(ty==='day'){showRules(q.show,S,qid,E);alt();
    if(!(opts.length>=lo&&opts.length<=hi)||opts.some(o=>!cdNum(o)))E('E-check',qid,`${lo}–${hi} day numbers as options`);
    else if(new Set(opts).size!==opts.length)E('E-check',qid,'options repeat — exactly one right answer');
    else if(S){for(const o of opts)if(!(S.days[0].day<=o&&o<=S.days[S.days.length-1].day))E('E-drill',qid,`day option ${o} outside the scene's days`);
      const a=q.answer,sd=obj(q.show)?q.show.day:null;if(isInt(a)&&a>=0&&a<opts.length&&cdNum(sd)&&opts[a]!==sd)E('E-drill',qid,`the right option (day ${opts[a]}) is not the day shown (${sd})`);}}
  else if(ty==='frames'){
    if(!(opts.length>=lo&&opts.length<=hi)||opts.some(o=>!obj(o)))E('E-check',qid,`${lo}–${hi} frames {text, show} as options`);
    else{const texts=[];opts.forEach((o,i)=>{const tx=o.text;
        if(!(typeof tx==='string'&&tx.trim()))E('E-check',qid,`frame ${i+1}: text missing (its text alternative)`);
        else if(wc(tx)>D.frameWords)E('E-check',qid,`frame ${i+1}: text over ${D.frameWords} words`);else texts.push(tx.trim().toLowerCase());
        showRules(o.show,S,qid,E,`frame ${i+1} show`);});
      if(new Set(texts).size!==texts.length)E('E-check',qid,'frame texts repeat');}}
  else if(ty==='label'){showRules(q.show,S,qid,E);alt();
    if(opts.some(o=>typeof o==='string'&&wc(o)>D.labelWords))E('E-check',qid,`label options ≤ ${D.labelWords} words (D8)`);
    const pins=q.pins;
    if(!(Array.isArray(pins)&&pins.length>=D.pins[0]&&pins.length<=D.pins[1]&&pins.every(obj)))E('E-check',qid,`${D.pins[0]}–${D.pins[1]} pins {at, answer}`);
    else{const an=S?sceneAnchors(S):null,ans=[];pins.forEach((p,i)=>{
        if(an&&!an.has(p.at))E('E-drill',qid,`pin ${i+1}: anchor ${p.at} is not drawn by ${S.id}`);
        if(!(isInt(p.answer)&&p.answer>=0&&p.answer<opts.length))E('E-check',qid,`pin ${i+1}: answer must be an option index`);else ans.push(p.answer);});
      if(new Set(ans).size!==ans.length)E('E-drill',qid,'two pins share a label — each pin needs its own');}}
  else if(ty==='folded'){
    if(!(opts.length===2&&opts.every(o=>typeof o==='string'&&o.trim()))||new Set(opts.filter(o=>typeof o==='string').map(o=>o.trim().toLowerCase())).size!==opts.length)E('E-check',qid,'exactly 2 different options (e.g. Folded · Not yet folded)');
    const its=q.items;
    if(!(Array.isArray(its)&&its.length>=D.items[0]&&its.length<=D.items[1]&&its.every(obj)))E('E-check',qid,`${D.items[0]}–${D.items[1]} items {show, answer 0|1, text}`);
    else{its.forEach((it,i)=>{if(it.answer!==0&&it.answer!==1)E('E-check',qid,`item ${i+1}: answer must be 0 or 1`);
        const tx=it.text;if(!(typeof tx==='string'&&tx.trim())||wc(tx)>D.frameWords)E('E-check',qid,`item ${i+1}: text of 1–${D.frameWords} words needed (its text alternative)`);
        showRules(it.show,S,qid,E,`item ${i+1} show`);});
      const set=new Set(its.map(it=>it.answer));if(!(set.size===2&&set.has(0)&&set.has(1)))E('E-check',qid,'items must use both answers (else it is guessable)');}}}

/* selftest cases (tools/card-check/selftest.json) — same path rules as check.py apply_case */
function cardApplyCase(card,cs){const c=JSON.parse(JSON.stringify(card));
  const walk=path=>{const ks=path.split('.');let o=c;for(const k of ks.slice(0,-1))o=Array.isArray(o)?o[+k]:(o[k]=o[k]||{});return [o,ks[ks.length-1]];};
  for(const [p,v] of Object.entries(cs.set||{})){const [o,k]=walk(p);if(Array.isArray(o))o[+k]=v;else if(v===null)delete o[k];else o[k]=v;}
  for(const p of cs.del||[]){const [o,k]=walk(p);delete o[k];}return c;}
/* every card file (+ optional selftest cases) → findings; used by --parity and the Studio list */
async function cardsCheckAll(cases){const ctx=await cardsCtx(),idx=await cdIndex(),out={};
  for(const it of idx.cards){try{out[it.id]=cardCheck(await cdCard(it.id),it.id,ctx);}catch(e){out[it.id]=[{lvl:'E',code:'E-schema',line:'file',msg:e.message}];}}
  if(cases){const base=await cdCard(cases.base);for(const cs of cases.cases){const c=cardApplyCase(base,cs);out['case: '+cs.name]=cardCheck(c,c.id,ctx);}}
  return out;}
