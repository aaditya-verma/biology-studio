/* Biology Studio — scheduler (W2, D-063): estimated dates, resource rows, critical path, ranked owner inputs, professor suggestions.
   Owner doc for the data: studio-docs/build/steps.json (calendar, queue, est, uses, produces/consumes, runs — format: tools/tracker/README.md).
   PURE: no DOM, no clock — trPlan(doc, today) gives the same answer as tools/tracker/check.py plan() (check.py --selftest runs both on
   tools/tracker/plan-fixture.json and on the real steps.json and fails if they differ). Loaded by the app before 17-tracker.js and by node in CI.
   Order never reshuffles (D-047): priority = doc.queue, then file order. Only dates move — with today, status, est, runs and the calendar.
   Idea rows are not planned (they ride on the step that builds them). est.days = calendar days to wait after the needs end (e.g. 7 days of use before GATE).
   EDIT: defaults in PLAN_DEF (keep tools/tracker/check.py PLAN_DEF identical — parity checks it). All times are whole minutes. */
'use strict';
const PLAN_DEF={"day_min":[180,180,180,180,180,360,360],"chat_min":60,"check_min":15,"input_min":10,"horizon":120,
  "chats":{"Ideation":0.5,"Build":1,"Research":1,"Content":1,"Episode":2,"Review":0.5,"Fix":0.5,"Idea":1},
  "rows":["lock","gpu","research","owner","prof"],"exclusive":["lock","gpu"],"met":["done","owner check"],
  "running":["in progress","gates"],"waiting":["ready","planned"],"unplanned":["idea","parked","proposed"]};

function planDay(iso,add){const [y,m,d]=iso.split('-').map(Number),t=new Date(Date.UTC(y,m-1,d+add));
  return t.getUTCFullYear()+'-'+String(t.getUTCMonth()+1).padStart(2,'0')+'-'+String(t.getUTCDate()).padStart(2,'0');}
function planWeekday(iso){const [y,m,d]=iso.split('-').map(Number);return (new Date(Date.UTC(y,m-1,d)).getUTCDay()+6)%7;}   // Mon = 0
function planCal(doc){const c=Object.assign({},PLAN_DEF,(doc&&doc.calendar)||{});c.off=(doc&&doc.calendar&&doc.calendar.off)||[];
  c.chats=Object.assign({},PLAN_DEF.chats,(doc&&doc.calendar&&doc.calendar.chats)||{});return c;}
function planRes(s){   // the resources a step holds while it runs; first one = its row
  const u=s.uses||[],r=[];
  if(u.length===1&&u[0]==='prof')return ['prof'];
  if(s.lock)r.push('lock');if(u.includes('gpu'))r.push('gpu');if(s.type==='Research'||u.includes('research'))r.push('research');
  if(!r.length)r.push('owner');return r;}
function planChats(s,cal){return s.est&&typeof s.est.chats==='number'?s.est.chats:(cal.chats[s.type]!=null?cal.chats[s.type]:1);}

function trPlan(doc,today){
  const cal=planCal(doc),steps=(doc&&doc.steps)||[],by={},pos={};steps.forEach((s,i)=>{by[s.id]=s;pos[s.id]=i;});
  const q=(doc&&doc.queue)||[],qi={};q.forEach((id,i)=>{if(qi[id]==null)qi[id]=i;});
  const pri=s=>qi[s.id]!=null?qi[s.id]:q.length+pos[s.id];
  const items=[],item={};
  const add=it=>{items.push(it);item[it.id]=it;};
  // owner items: open owner checks + blocking open inputs (small, on the owner row)
  steps.forEach(s=>{
    if(s.status==='owner check'&&s.check&&s.check.state==='open')add({id:s.id+'·'+s.check.id,step:s.id,kind:'check',row:'owner',res:['owner'],mins:cal.check_min,deps:[],pri:-1,done:false});
    (s.inputs||[]).forEach(x=>{if(x.status==='open'&&x.blocks&&x.for!=='prof')add({id:x.id,step:s.id,kind:'input',row:'owner',res:['owner'],mins:cal.input_min,deps:[],pri:-1,done:false});});});
  // steps
  steps.forEach(s=>{
    const res=planRes(s),row=res[0];
    if(PLAN_DEF.met.includes(s.status)||row==='prof'||s.type==='Idea')return;
    if(PLAN_DEF.unplanned.includes(s.status)){add({id:s.id,step:s.id,kind:'step',row,res,mins:0,deps:[],pri:pri(s),never:true,done:false});return;}
    const est=planChats(s,cal),ran=(s.runs||[]).length,running=PLAN_DEF.running.includes(s.status);
    const left=running?Math.max(0.5,est-ran):est;
    const deps=(s.needs||[]).slice();(s.inputs||[]).forEach(x=>{if(x.status==='open'&&x.blocks&&x.for!=='prof')deps.push(x.id);});
    const live=(s.runs||[]).some(r=>r&&r.start&&!r.end);   // an open run = a chat is working on it right now
    add({id:s.id,step:s.id,kind:'step',row,res,mins:Math.round(left*cal.chat_min),deps,pri:pri(s),running,live,done:false,slipped:ran>est,wait:s.est&&s.est.days|0});});
  // priority: running steps first (no pre-emption), owner items, then queue/file order
  const order=items.slice().sort((a,b)=>((b.running?1:0)-(a.running?1:0))||(a.pri-b.pri)||(pos[a.step]-pos[b.step])||(a.id<b.id?-1:a.id>b.id?1:0));
  const finished=new Set(steps.filter(s=>PLAN_DEF.met.includes(s.status)).map(s=>s.id));
  const isMetDep=d=>finished.has(d)||(by[d]&&by[d].status==='owner check');
  const endOf=d=>item[d]&&item[d].end?item[d].end:today;   // a need met before today counts as ending today
  const waitOk=(x,day)=>!x.wait||planDay(x.deps.reduce((m,d)=>endOf(d)>m?endOf(d):m,today),x.wait)<=day;
  const busy={};   // resource → item id holding it (started, not finished)
  order.forEach(it=>{it.left=it.mins;it.start=null;it.end=null;});
  let last=null;
  for(let n=0;n<cal.horizon;n++){
    const day=planDay(today,n);let budget=cal.off.includes(day)?0:cal.day_min[planWeekday(day)];
    while(budget>0){
      const it=order.find(x=>!x.done&&!x.never&&x.deps.every(isMetDep)&&waitOk(x,day)&&x.res.every(r=>!busy[r]||busy[r]===x.id));
      if(!it)break;
      if(it.start==null){it.start=day;it.res.forEach(r=>{if(PLAN_DEF.exclusive.includes(r))busy[r]=it.id;});}
      const take=Math.min(it.left,budget);it.left-=take;budget-=take;
      if(it.left<=0){it.done=true;it.end=day;last=day;finished.add(it.id);it.res.forEach(r=>{if(busy[r]===it.id)delete busy[r];});}}}
  // critical path: back from GATE (or the latest end) through the need that ends last
  const sched=items.filter(x=>x.end);let tgt=item.GATE&&item.GATE.end?item.GATE:sched.reduce((a,b)=>!a||b.end>a.end||(b.end===a.end&&b.pri>a.pri)?b:a,null);
  const critical=[];while(tgt){critical.unshift({id:tgt.id,step:tgt.step});const prev=tgt.deps.map(d=>item[d]).filter(x=>x&&x.end);
    tgt=prev.reduce((a,b)=>!a||b.end>a.end?b:a,null);}
  // rows: Now (running / started today) · Next (first waiting) · Later (rest), in time order
  const rows={};PLAN_DEF.rows.forEach(r=>rows[r]={now:[],next:[],later:[]});
  items.filter(x=>x.row!=='prof').slice().sort((a,b)=>((a.start||'9')<(b.start||'9')?-1:(a.start||'9')>(b.start||'9')?1:0)||(a.pri-b.pri)||(pos[a.step]-pos[b.step])).forEach(x=>{
    const R=rows[x.row];const cell={id:x.id,step:x.step,kind:x.kind,start:x.start,end:x.end,mins:x.mins,slipped:!!x.slipped};
    if(x.live||(x.start===today&&x.kind!=='step'))R.now.push(cell);else if(!R.next.length&&x.start)R.next.push(cell);else R.later.push(cell);});
  // owner inputs ranked by how much each unblocks (a blocking input counts 100 more), then oldest
  const down={};steps.forEach(s=>(s.needs||[]).forEach(n=>{(down[n]=down[n]||[]).push(s.id);}));
  const reach=id=>{const seen=new Set(),st=[id];while(st.length){const c=st.pop();(down[c]||[]).forEach(k=>{if(!seen.has(k)){seen.add(k);st.push(k);}});}
    return [...seen].filter(k=>by[k]&&by[k].status!=='done').length;};
  const ranked=[];steps.forEach(s=>{const r=s.status==='done'?0:reach(s.id);   // an answer on a finished step holds nothing up
    (s.inputs||[]).forEach(x=>{if(x.status==='open'&&x.for!=='prof')ranked.push({id:x.id,step:s.id,kind:x.kind||null,unblocks:r,blocks:!!x.blocks,asked:x.asked||''});});
    if(s.status==='owner check'&&s.check&&s.check.state==='open')ranked.push({id:s.check.id,step:s.id,kind:'check',unblocks:r,blocks:false,asked:s.check.since||''});});
  ranked.sort((a,b)=>((b.blocks?1:0)-(a.blocks?1:0))||(b.unblocks-a.unblocks)||(a.asked<b.asked?-1:a.asked>b.asked?1:0)||(a.id<b.id?-1:a.id>b.id?1:0));
  // professor: optional suggestions, never on a needs chain
  const prof=[];steps.forEach(s=>{
    if(planRes(s)[0]==='prof'&&s.status!=='done')prof.push({id:s.id,step:s.id,kind:'step',improves:s.improves||''});
    (s.inputs||[]).forEach(x=>{if(x.for==='prof'&&x.status==='open')prof.push({id:x.id,step:s.id,kind:x.kind||null,improves:x.improves||''});});});
  const dates={};items.forEach(x=>{if(x.kind==='step')dates[x.id]={start:x.start,end:x.end,row:x.row,mins:x.mins,slipped:!!x.slipped};});
  return {today,end:last,critical,rows,ranked,prof,dates};}

// W3 run surface (D-080): where a step's chat runs — Code or Cowork. Rules live in steps.json `surfaces` (first match wins);
// each step's `run {on, why, override?}` says where it actually runs. Same answer as check.py surface() (--selftest compares in node).
const SURF_DEF={"on":["Code","Cowork"],"rules":[]};
function surfMatch(c,s){if(!c||typeof c!=='object'||Array.isArray(c))return false;   // a malformed rule never matches (check.py reports it)
  const u=s.uses||[];return Object.keys(c).every(k=>{const v=c[k];
  if(k==='lock')return !!s.lock===!!v;
  if(k==='uses')return v==='prof'?(u.length===1&&u[0]==='prof'):u.includes(v);
  if(k==='type')return (Array.isArray(v)?v:[v]).includes(s.type);
  return true;});}
function trSurface(doc,s){
  const cfg=doc&&doc.surfaces&&typeof doc.surfaces==='object'&&!Array.isArray(doc.surfaces)?doc.surfaces:SURF_DEF;
  let rule=null,ri=null;(Array.isArray(cfg.rules)?cfg.rules:[]).some((r,i)=>{if(r&&typeof r==='object'&&surfMatch(r.if,s)){rule=r;ri=i;return true;}return false;});
  const allowed=(rule==null?[]:(Array.isArray(rule.on)?rule.on:[rule.on])).map(x=>x===undefined?null:x);
  const run=s.run&&typeof s.run==='object'&&!Array.isArray(s.run)?s.run:null;
  const on=run?(run.on===undefined?null:run.on):(allowed.length?allowed[0]:null);   // allowed[0] is never undefined (mapped to null, like Python's None)
  const why=run&&run.why?run.why:(rule?(rule.why===undefined?null:rule.why):'');
  return {on,allowed,why,rule:ri,fit:allowed.includes(on),override:!!(run&&run.override),set:run!==null};}

if(typeof module!=='undefined'&&module.exports)module.exports={trPlan,PLAN_DEF,planChats,planCal,trSurface};
