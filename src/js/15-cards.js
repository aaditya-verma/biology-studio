/* Biology Studio — cards: data loading, validateCitation, the mark suggester and cardCheck (the app's copy of tools/card-check, S1).
   Owner doc: docs/card-spec.md (format + rules, C2). The Python tool is the CI gate; `tools/card-check/check.py --parity` runs cardCheck() here on
   every card and every selftest case and fails if the two disagree — change both together.
   EDIT: limits in CARD_RULES (mirror LIMITS/VERBS/BUDGET/GATES in tools/card-check/check.py); data paths in CONFIG.cards. */
'use strict';
const CARD_RULES={
  verbs:['explain','describe','identify','label','locate','order','compare','distinguish','predict','name','trace','relate'],
  spatial:['identify','label','locate','order'],
  budget:{general:90,school:110,neet:140,mbbs:160,pg:200}, required:['general','mbbs'],
  marks:['✔✔','✔','⚑','✚','≈'], statuses:['draft','reviewed','shipped','retired'],
  limits:{sentence:25,newTerms:3,newTermsEx:5,minChecks:2,opt:[3,5]},
  gates:{'G-Sci':{checklist:['cited','sections','accuracy','flags','plus','noapprox'],lines:['body','fact','mis','adult']},
    'G-Learn':{checklist:['objective','checks','refutes','terms','budget','adult'],lines:['obj','terms','check','mis']},
    'G-A11y':{checklist:['alt','input','colour','text125'],lines:[]},
    'G-Owner':{checklist:['owner'],lines:[]}},
  needs:{reviewed:['G-Sci','G-Learn'],shipped:['G-Sci','G-Learn','G-A11y','G-Owner']}
};

/* ---------- data (fetched on first use; Studio only) ---------- */
const CD={src:null,srcP:null,idx:null,idxP:null,files:{},cal:null,calP:null,err:null};
const cdJson=u=>fetch(u,{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(u.split('/').pop()+' HTTP '+r.status);return r.json();});
function cdSources(){if(!CD.srcP)CD.srcP=cdJson(CONFIG.cards.sources).then(j=>(CD.src=j)).catch(e=>{CD.err=e.message;CD.srcP=null;throw e;});return CD.srcP;}
function cdIndex(){if(!CD.idxP)CD.idxP=cdJson(CONFIG.cards.dir+'index.json').then(j=>(CD.idx=j)).catch(e=>{CD.err=e.message;CD.idxP=null;throw e;});return CD.idxP;}
function cdCard(id){if(!CD.files[id])CD.files[id]=cdJson(CONFIG.cards.dir+encodeURIComponent(id)+'.json').catch(e=>{delete CD.files[id];throw e;});return CD.files[id];}
function cdCal(){if(!CD.calP)CD.calP=cdJson(CONFIG.cards.dir+'calibration.json').then(j=>(CD.cal=j)).catch(e=>{CD.calP=null;throw e;});return CD.calP;}
async function cardsCtx(){await Promise.all([cdSources(),mapLoad(),scIndexLoad()]);
  return {src:CD.src,mapIds:new Set(MAPD.C.map(c=>c.id)),mapTerms:Object.fromEntries(MAPD.C.map(c=>[c.id,c.terms||[]])),scenes:(SC.idx&&SC.idx.scenes)||[]};}

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
function cardLines(card){const L={obj:['obj'],terms:['terms'],body:[],fact:[],mis:[],check:[],adult:[]};
  for(const [lvl,t] of Object.entries(card.body||{}))cSentences(t).forEach((_,i)=>L.body.push(`body.${lvl}.${i+1}`));
  L.fact=(card.facts||[]).map(f=>f.id);L.mis=(card.misconceptions||[]).map(m=>m.id);L.check=(card.checks||[]).map(q=>q.id);if(card.adult)L.adult=['adult'];return L;}
const gateLines=(card,g)=>{const L=cardLines(card);return CARD_RULES.gates[g].lines.flatMap(k=>L[k]);};

/* ---------- cardCheck: mirror of tools/card-check/check.py card_check() ---------- */
function cardCheck(card,stem,ctx){
  const R=CARD_RULES,out=[],E=(code,line,msg)=>out.push({lvl:'E',code,line,msg}),W=(code,line,msg)=>out.push({lvl:'W',code,line,msg}),src=ctx.src;
  const isObj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
  const want={spec:'int',id:'str',version:'int',book:'str',status:'str',title:'str',tier:'str',objective:'dict',body:'dict',facts:'list',terms:'dict',misconceptions:'list',checks:'list',scene:'dict',made:'dict',review:'dict',log:'list'};
  const ok={int:Number.isInteger,str:x=>typeof x==='string',dict:isObj,list:Array.isArray};
  for(const [k,t] of Object.entries(want))if(!ok[t](card[k]))E('E-schema',k,`'${k}' missing or not ${t}`);
  if(out.length)return out;
  if(card.spec!==1||card.version<1||!R.statuses.includes(card.status)||!['A','B','C','D'].includes(card.tier))E('E-schema','card','spec must be 1, version ≥ 1, status draft/reviewed/shipped/retired, tier A–D');
  for(const k of ['by','role','agent','date'])if(!card.made[k])E('E-schema','made',`made.${k} missing`);
  const st=card.status,final=st==='reviewed'||st==='shipped';
  if(card.id!==stem)E('E-id','card',`id ${card.id} ≠ file name ${stem}`);
  if(!ctx.mapIds.has(card.id))E('E-id','card',`${card.id} is not a concept in map.json`);
  const ob=card.objective,verb=ob.verb||'',text=String(ob.text||'').trim();
  if(!text)E('E-objective','obj','objective text missing');
  else if(!R.verbs.includes(verb))E('E-objective','obj',`verb '${verb}' not in the list`);
  else if(!text.toLowerCase().startsWith(verb+' '))E('E-objective','obj',`objective must start with its verb '${verb}'`);
  else if(new RegExp('\\b(?:and|then|,)\\s+('+R.verbs.join('|')+')\\b').test(text.toLowerCase()))E('E-objective','obj','one verb per objective');
  const fids=card.facts.map(f=>f.id);
  for(const lvl of R.required)if(!String(card.body[lvl]||'').trim())E('E-level','body.'+lvl,`level '${lvl}' missing`);
  const sentRules=(txt,prefix)=>cSentences(txt).forEach((s,i)=>{const ln=prefix==='adult'?'adult':`${prefix}.${i+1}`;
    if(cWords(s)>R.limits.sentence)E('E-sentence',ln,`${cWords(s)} words > ${R.limits.sentence}`);
    const refs=cRefs(s);if(!refs.length&&!stripRefs(s).endsWith('?'))E('E-ref',ln,'sentence has no fact ref [f1] (only a question may go without)');
    for(const r of refs)if(!fids.includes(r))E('E-ref',ln,`ref ${r} points at no fact`);});
  for(const [lvl,txt] of Object.entries(card.body)){
    if(!(lvl in R.budget)){E('E-schema','body.'+lvl,`unknown level '${lvl}'`);continue;}
    if(cWords(txt)>R.budget[lvl])E('E-words','body.'+lvl,`${cWords(txt)} words > ${R.budget[lvl]} for ${lvl}`);
    sentRules(txt,'body.'+lvl);}
  if(card.adult)sentRules(card.adult,'adult');
  const seen=new Set(),reg=Object.fromEntries(src.registry.map(r=>[r.id,r]));
  for(const f of card.facts){const fid=String(f.id||'f?');
    if(typeof f.id!=='string'||!/^f\d+$/.test(fid)||seen.has(fid))E('E-schema',fid,'fact id must be f1, f2… and unique');seen.add(fid);
    if(typeof f.text!=='string'||!f.text.trim())E('E-schema',fid,'fact text missing or not text');
    for(const s of cSentences(f.text||''))if(cWords(s)>R.limits.sentence)E('E-sentence',fid,`${cWords(s)} words > ${R.limits.sentence}`);
    if(f.where!=='main'&&f.where!=='more')E('E-schema',fid,"where must be 'main' or 'more'");
    const v=validateCitation(f.cite,src);v.errors.forEach(e=>E('E-cite',fid,e));
    const mk=f.mark;
    if(!R.marks.includes(mk)){E('E-mark',fid,'mark missing or unknown');continue;}
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
    if(m.cite)validateCitation(m.cite,src).errors.forEach(e=>E('E-cite',mid,e));
    if(m.mark&&!R.marks.includes(m.mark))E('E-mark',mid,`unknown mark ${m.mark}`);
    if(m.mark==='≈')(final?E:W)(final?'E-approx':'W-approx',mid,'≈ blocks reviewed/shipped');}
  const qs=card.checks;
  if(qs.length<R.limits.minChecks)E('E-checks','checks',`${qs.length} checks < ${R.limits.minChecks}`);
  for(const q of qs){const qid=q.id||'q?',opts=q.options||[],[lo,hi]=R.limits.opt;
    if(q.type!=='mcq'&&q.type!=='order')E('E-check',qid,'type must be mcq or order');
    if(!String(q.prompt||'').trim())E('E-check',qid,'prompt missing');
    if(!(opts.length>=lo&&opts.length<=hi)||opts.some(o=>!(typeof o==='string'&&o.trim())))E('E-check',qid,`${lo}–${hi} non-empty options`);
    if(new Set(opts.filter(o=>typeof o==='string').map(o=>o.trim().toLowerCase())).size!==opts.length)E('E-check',qid,'options repeat — exactly one right answer');
    if(q.type==='mcq'&&!(Number.isInteger(q.answer)&&q.answer>=0&&q.answer<opts.length))E('E-check',qid,'answer must be the index of the one right option');
    if(q.type==='order'&&q.answer!==undefined&&q.answer!==null)E('E-check',qid,'an order check lists options in the right order; no answer field');
    if(!String(q.why||'').trim())E('E-check',qid,'why missing');
    if(q.tests!=='objective')E('E-check',qid,"tests must be 'objective' (H1)");
    if(q.refutes&&!mids.includes(q.refutes))E('E-check',qid,`refutes ${q.refutes}, which is not a misconception here`);}
  if(qs.length&&!qs.some(q=>q.refutes))E('E-checks','checks','no check refutes a misconception');
  if(R.spatial.includes(verb)&&!qs.some(q=>q.type==='order'))E('E-checks','checks',`spatial verb '${verb}' needs a spatial check (order)`);
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
