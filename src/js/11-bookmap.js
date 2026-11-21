/* Biology Studio — Book map: the K1 explorer ported into the app (master plan §5, §8a). Owner doc: build/design-plan.md §4.3.
   Data: content/E/map.json (tools/map/build_map.py). Three panes in the DOM — tree │ chapter or crosstab │ concept — and CSS shows
   one (phone), tree + detail (tablet) or all three (desktop) by device class; rotating keeps the route, so nothing is lost.
   Shows the X1 fields where present: `an` (NMC AN codes), `mark` (✔✔ ✔ ⚑ ✚ ≈), cited `cs` (else ≈ `cs_approx`).
   EDIT: crosstab dimensions in BM_DIMS; words in STR; concept rows live in tools/map/concepts.txt (✎ points there). */
'use strict';
const MAPD={M:null,C:[],byId:{},err:null,loading:null};
function mapLoad(){if(!MAPD.loading)MAPD.loading=fetch(CONFIG.mapUrl).then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json();})
  .then(d=>{MAPD.M=d;MAPD.C=d.concepts;d.concepts.forEach(o=>MAPD.byId[o.id]=o);dlog('map','loaded',d.concepts.length,'concepts');})
  .catch(e=>{MAPD.err=e.message;dlog('map','load failed',e.message);});return MAPD.loading;}
const BM={F:{},q:''};
const range=(a,b)=>{const r=[];for(let i=a;i<=b;i++)r.push(i);return r;};
const pad2=n=>String(n).padStart(2,'0');
const pages=p=>p?(p[0]===p[1]?'p '+p[0]:'pp '+p[0]+'–'+p[1]):'';
function dayBin(d){if(!d)return 'No day';const x=d[0];return x<=7?'Wk 1':x<=14?'Wk 2':x<=21?'Wk 3':x<=28?'Wk 4':x<=56?'Wk 5–8':'Fetal';}
/* EDIT: crosstab dimensions */
const BM_DIMS={
  chapter:{label:'Chapter',vals:o=>[o.ch]}, recurs:{label:'Chapter it recurs in',vals:o=>Object.keys(o.recurs).filter(k=>o.recurs[k]>0||k===o.ch)},
  day:{label:'Day / week',vals:o=>[dayBin(o.day)]},
  cs:{label:'Carnegie stage',vals:o=>{const c=o.cs||o.cs_approx;return c?range(c[0],c[1]).map(n=>'CS'+pad2(n)):['No stage'];}},
  layer:{label:'Germ layer',vals:o=>[o.layer]}, system:{label:'System',vals:o=>[o.system]},
  tier:{label:'Tier',vals:o=>[o.tier]}, importance:{label:'Importance',vals:o=>[o.importance]},
  thread:{label:'Thread',vals:o=>o.threads.length?o.threads:['—']}, mark:{label:'Confidence',vals:o=>[o.mark||'≈']}
};
function bmOrder(dim){const V=MAPD.M.vocab;switch(dim){case 'chapter':case 'recurs':return MAPD.M.chapters.map(c=>c.id);case 'day':return V.daybins;
  case 'cs':return range(1,23).map(n=>'CS'+pad2(n)).concat(['No stage']);case 'layer':return Object.keys(V.layer);case 'system':return Object.keys(V.system);
  case 'tier':return ['A','B','C','D'];case 'importance':return V.importance;case 'thread':return Object.keys(V.threads).concat(['—']);case 'mark':return ['✔✔','✔','⚑','✚','≈'];}return [];}
function bmLab(dim,v){const V=MAPD.M.vocab;if(dim==='layer')return V.layer[v]||v;if(dim==='system')return V.system[v]||v;if(dim==='tier')return v+' · '+(V.tier[v]||'');
  if(dim==='thread')return v+(V.threads[v]?' · '+V.threads[v]:'');if(dim==='mark')return v+' · '+(STR.marks[v]||'');
  if(dim==='chapter'||dim==='recurs'){const c=MAPD.M.chapters.find(c=>c.id===v);return c?v+' '+c.title:v;}return v;}
const bmShort=(dim,v)=>['layer','system'].includes(dim)?bmLab(dim,v):v;
const sw=l=>`<span class="sw L-${esc(l)}" aria-hidden="true"></span>`;
const badges=o=>`<span class="badge b-${esc(o.importance)}">${esc(o.importance)}</span><span class="badge" title="${esc(MAPD.M.vocab.tier[o.tier])}">${esc(STR.tierShort(o.tier))}</span><span class="badge mark" title="${esc(STR.marks[o.mark||'≈'])}">${esc(o.mark||'≈')} ${esc(STR.markShort[o.mark||'≈'])}</span>`;
const cEdit=o=>editBtn('concept',o.id,'tools/map/concepts.txt (row under @ '+o.sec+')'+(o.x1?' + tools/map/research.txt':''));
function crow(o,cur){return `<div class="row" style="flex-wrap:nowrap"><button type="button" class="lrow c" data-go="concept=${esc(o.id)}"${cur?' aria-current="true"':''}>${sw(o.layer)}<span class="nm">${esc(o.name)}<br><span class="xs mut">${esc(MAPD.M.vocab.layer[o.layer])} · ${esc(MAPD.M.vocab.system[o.system])}</span></span><span class="id">${esc(o.id)}</span></button>${cEdit(o)}</div>`;}
function bmPass(o){const F=BM.F;for(const k of ['tier','importance','layer','system','mark'])if(F[k]&&(o[k]||(k==='mark'?'≈':''))!==F[k])return false;
  if(F.thread&&!o.threads.includes(F.thread))return false;const q=BM.q.trim().toLowerCase();
  if(q){const t=(o.id+' '+o.name+' '+o.def_ours+' '+(o.misconception||'')+' '+(o.an||[]).join(' ')+' '+o.terms.map(t=>MAPD.M.terms[t]?.term).join(' ')).toLowerCase();if(!q.split(/\s+/).every(w=>t.includes(w)))return false;}
  return true;}
const bmFiltered=()=>Object.values(BM.F).some(Boolean)||!!BM.q.trim();

SCREENS.map=SCREENS.concept=SCREENS.x=function(v){
  if(!MAPD.M){v.innerHTML=MAPD.err?`<div class="card"><b>${esc(STR.loadFail)}</b><p class="mut">${esc(MAPD.err)}</p></div>`:`<p class="empty">…</p>`;
    ROUTE.crumbs=[{label:STR.mapTitle}];if(!MAPD.err)mapLoad().then(()=>{if(['map','concept','x'].includes(ROUTE.name))render();});return;}
  const r=ROUTE,M=MAPD.M,o=r.name==='concept'?MAPD.byId[r.id]:null,ch=r.ch&&M.chapters.find(c=>c.id===r.ch);
  const focus=r.name==='concept'?'concept':(r.name==='x'||ch)?'mid':'tree';
  r.crumbs=[{label:STR.mapTitle,hash:'map'}];if(ch)r.crumbs.push({label:ch.id+' '+ch.title,hash:'map='+ch.id});
  if(r.name==='x')r.crumbs.push({label:STR.crosstab,hash:hashOf(r)});if(o)r.crumbs.push({label:o.name,hash:hashOf(r)});
  if(o)stTouch(o.id);
  v.innerHTML=`<div class="bm" data-focus="${focus}"><section class="p-tree" aria-label="${esc(STR.tree)}"><div class="pane">${bmTree(ch)}</div></section>
    <section class="p-mid" aria-label="${esc(r.name==='x'?STR.crosstab:STR.chapterView)}"><div class="pane">${r.name==='x'?bmXt(r):ch?bmChapter(ch,o):bmOverview()}</div></section>
    <section class="p-con" aria-label="${esc(STR.conceptPane)}"><div class="pane">${o?bmConcept(o):r.id?`<p class="empty">${esc(STR.noConcept(r.id))}</p>`:`<p class="empty">${esc(STR.pickConcept)}</p>`}</div></section></div>`;
  bmWire(v);
  if(focus==='concept'&&DEV.cls!=='dev-d')scrollTo(0,0);
};
function bmTree(cur){const M=MAPD.M,V=M.vocab,L=MAPD.C.filter(bmPass);
  const opts={tier:['A','B','C','D'],importance:V.importance,layer:Object.keys(V.layer),system:Object.keys(V.system),thread:Object.keys(V.threads),mark:['✔✔','✔','⚑','✚','≈']};
  const nF=Object.values(BM.F).filter(Boolean).length;
  let h=`<label class="sr" for="bmq">${esc(STR.searchLabel)}</label><input id="bmq" class="bm-search" type="search" placeholder="${esc(STR.searchPh)}" value="${esc(BM.q)}" autocomplete="off">
   <details class="filt"${nF?' open':''}><summary class="row" style="min-height:var(--tap);cursor:pointer"><b>${esc(STR.filters)}</b>${nF?`<span class="badge">${nF}</span>`:''}</summary>
   <div class="filters">${Object.entries(opts).map(([k,vs])=>`<div><label for="f-${k}">${esc(BM_DIMS[k]?BM_DIMS[k].label:k)}</label><select id="f-${k}" data-f="${k}"><option value="">${esc(STR.all)}</option>${vs.map(x=>`<option value="${esc(x)}"${BM.F[k]===x?' selected':''}>${esc(bmLab(k,x))}</option>`).join('')}</select></div>`).join('')}</div>
   <button type="button" class="btn" data-act="clearf">${esc(STR.clearFilters)}</button></details>
   <p class="sm mut" aria-live="polite">${esc(STR.shown(L.length,MAPD.C.length))}</p>`;
  if(bmFiltered())return h+(L.length?L.slice(0,200).map(x=>crow(x,ROUTE.id===x.id)).join(''):`<p class="empty">—</p>`);
  let part=-1;h+='<div class="tree">';
  for(const c of M.chapters){const n=L.filter(x=>x.ch===c.id).length;if(c.part!==part){part=c.part;h+=`<div class="partlbl">${esc(STR.parts[part]||'')}</div>`;}
    h+=`<div class="row bm-ch"><button type="button" class="lrow" data-go="map=${esc(c.id)}"${cur&&cur.id===c.id?' aria-current="true"':''}><span class="nm">${esc(c.title)}<br><span class="xs mut">${esc(c.id)} · ${n} ${esc(STR.concepts)}</span></span></button>${editBtn('chapter',c.id,'tools/map/concepts.txt (sections of '+c.id+')')}</div>`;}
  return h+'</div>';}
function bmOverview(){const top=[...MAPD.C].sort((a,b)=>b.unlock_n-a.unlock_n).slice(0,12),pairs=[['layer','day'],['system','chapter'],['tier','chapter'],['mark','chapter'],['cs','layer']];
  return `<h1>${esc(STR.mapTitle)}</h1><p class="mut sm">${esc(STR.pickChapter)}</p>
   <h2>${esc(STR.crosstab)}</h2><div class="links">${pairs.map(([x,y])=>`<button type="button" class="lk" data-go="x=${x}&y=${y}">${esc(BM_DIMS[x].label)} × ${esc(BM_DIMS[y].label)}</button>`).join('')}</div>
   <h2 style="margin-top:16px">${esc(STR.unlocks)}</h2>${top.map(o=>`<div class="row" style="flex-wrap:nowrap"><span class="badge" title="concepts that build on it">${o.unlock_n}</span><div style="flex:1;min-width:0">${crow(o)}</div></div>`).join('')}`;}
function bmChapter(ch,cur){const M=MAPD.M,secs=M.sections.filter(s=>s.ch===ch.id),L=MAPD.C.filter(o=>o.ch===ch.id);
  let h=`<div class="row"><h1 style="flex:1;margin:0">${esc(ch.id)} ${esc(ch.title)}</h1>${editBtn('chapter',ch.id,'tools/map/concepts.txt (sections of '+ch.id+')')}</div>
    <p class="sm mut">${L.length} ${esc(STR.concepts)}${ch.pages?` · ${pages(ch.pages)} (${esc(STR.locator)})`:''}</p>`;
  for(const s of secs){const ss=L.filter(o=>o.sec===s.id);if(!ss.length)continue;
    h+=`<h3 style="margin-top:14px">${esc(s.id)} ${esc(s.title)} <span class="xs mut">${s.pages?'· '+pages(s.pages):''}${s.boxes&&s.boxes.length?' · '+s.boxes.map(b=>b==='clinical'?'CC':'MR').join(' '):''}</span></h3>${ss.map(o=>crow(o,cur&&cur.id===o.id)).join('')}`;}
  return h;}
function bmXt(r){const L=MAPD.C.filter(bmPass),xo=bmOrder(r.x),yo=bmOrder(r.y),m={};
  if(!BM_DIMS[r.x]||!BM_DIMS[r.y])return `<p class="empty">${esc(STR.badXt)}</p>`;
  for(const o of L)for(const a of BM_DIMS[r.x].vals(o))for(const b of BM_DIMS[r.y].vals(o))(m[a+'|'+b]??=[]).push(o.id);
  const xs=xo.filter(x=>yo.some(y=>m[x+'|'+y])),ys=yo.filter(y=>xs.some(x=>m[x+'|'+y])),mx=Math.max(1,...Object.values(m).map(a=>a.length));
  const sel=(id,c)=>`<select id="${id}" data-xt="${id}">${Object.keys(BM_DIMS).map(d=>`<option value="${d}"${d===c?' selected':''}>${esc(BM_DIMS[d].label)}</option>`).join('')}</select>`;
  let h=`<h1>${esc(STR.crosstab)}</h1><div class="row"><label class="sm">${esc(STR.rows)} ${sel('xtx',r.x)}</label><label class="sm">${esc(STR.cols)} ${sel('xty',r.y)}</label>
    <button type="button" class="btn" data-go="x=${esc(r.y)}&y=${esc(r.x)}">⇄ ${esc(STR.swap)}</button></div><p class="xs mut">${esc(STR.cellHint)}</p>
    <div class="xt-wrap"><table class="xt"><caption class="sr">${esc(BM_DIMS[r.x].label)} by ${esc(BM_DIMS[r.y].label)}</caption><thead><tr><th class="rh" scope="col">${esc(BM_DIMS[r.x].label)} ╲<br>${esc(BM_DIMS[r.y].label)}</th>${ys.map(y=>`<th scope="col" title="${esc(bmLab(r.y,y))}">${esc(bmShort(r.y,y))}</th>`).join('')}</tr></thead><tbody>`;
  for(const x of xs){h+=`<tr><th class="rh" scope="row" title="${esc(bmLab(r.x,x))}">${r.x==='layer'?sw(x)+' ':''}${esc(bmLab(r.x,x))}</th>`;
    for(const y of ys){const n=(m[x+'|'+y]||[]).length,lv=n?Math.min(4,1+Math.floor(3*n/mx)):0;
      h+=`<td><button type="button" class="h${lv}" data-go="x=${esc(r.x)}&y=${esc(r.y)}&cell=${encodeURIComponent(x+'|'+y)}" aria-label="${esc(bmLab(r.x,x))}, ${esc(bmLab(r.y,y))}: ${n}">${n||'·'}</button></td>`;}h+='</tr>';}
  h+='</tbody></table></div>';
  if(r.cell&&m[r.cell]){const[a,b]=r.cell.split('|');h+=`<div style="margin-top:12px"><b>${esc(bmLab(r.x,a))} × ${esc(bmLab(r.y,b))}</b> · ${m[r.cell].length}${m[r.cell].map(i=>crow(MAPD.byId[i])).join('')}</div>`;}
  return h;}
function bmConcept(o){const M=MAPD.M,V=M.vocab,sec=M.sections.find(s=>s.id===o.sec),ch=M.chapters.find(c=>c.id===o.ch);
  const lk=ids=>ids&&ids.length?`<div class="links">${ids.filter(i=>MAPD.byId[i]).map(i=>`<button type="button" class="lk" data-go="concept=${esc(i)}">${esc(i)} ${esc(MAPD.byId[i].name)}</button>`).join('')}</div>`:STR.none;
  const cs=o.cs?`CS${pad2(o.cs[0])}${o.cs[1]!==o.cs[0]?'–'+pad2(o.cs[1]):''} · ${STR.cited}`:o.cs_approx?`≈ CS${pad2(o.cs_approx[0])}${o.cs_approx[1]!==o.cs_approx[0]?'–'+pad2(o.cs_approx[1]):''} · ${STR.approx}`:STR.none;
  const mark=o.mark||'≈';
  return `<article class="cp" aria-labelledby="cpT"><div class="row"><span class="mono mut">${esc(o.id)}</span>${cEdit(o)}<span class="sp"></span></div>
   <h1 id="cpT" tabindex="-1">${esc(o.name)}</h1>
   <div class="meta">${badges(o)}<span class="badge">${sw(o.layer)} ${esc(V.layer[o.layer])}</span><span class="badge">${esc(V.system[o.system])}</span>${o.threads.map(t=>`<span class="badge" title="${esc(V.threads[t]||'')}">${esc(STR.threadShort(t,V.threads[t]))}</span>`).join('')}</div>
   <p class="def">${esc(o.def_ours)} ${mark==='≈'?`<span class="xs mut">(${esc(STR.approx)})</span>`:''}</p>
   ${o.misconception?`<div class="mis"><b>${esc(STR.mixup)}</b> “${esc(o.misconception)}” ${esc(STR.notRight)}</div>`:''}
   <dl><dt>${esc(STR.markT)}</dt><dd><b>${esc(mark)}</b> ${esc(STR.marks[mark]||'')}</dd>
   <dt>${esc(STR.where)}</dt><dd>${esc(o.ch)} ${esc(ch?.title)} › ${esc(o.sec)} ${esc(sec?.title)}${o.pages?` · ${pages(o.pages)} (${esc(STR.locator)})`:''}</dd>
   <dt>${esc(STR.day)}</dt><dd>${o.day?`day ${o.day[0]}${o.day[1]!==o.day[0]?'–'+o.day[1]:''}`:STR.none}</dd>
   <dt>${esc(STR.stage)}</dt><dd>${esc(cs)}</dd>
   <dt>${esc(STR.an)}</dt><dd>${o.an&&o.an.length?o.an.map(esc).join(' · '):STR.none}</dd>
   <dt>${esc(STR.needs)}</dt><dd>${lk(o.prereq)}</dd><dt>${esc(STR.unlocksT)}</dt><dd>${lk(o.unlocks)}${o.unlock_n?` <span class="xs mut">${esc(STR.inAll(o.unlock_n))}</span>`:''}</dd>
   <dt>${esc(STR.related)}</dt><dd>${lk(o.related)}</dd>
   <dt>${esc(STR.showsUp)}</dt><dd><div class="links">${Object.keys(o.recurs).filter(c=>o.recurs[c]>0).map(c=>`<button type="button" class="lk" data-go="map=${esc(c)}">${esc(c)}</button>`).join('')||STR.none}</div></dd>
   <dt>${esc(STR.terms)}</dt><dd>${o.terms.concat(o.terms_loose).map(t=>esc(M.terms[t]?.term)).filter(Boolean).join(' · ')||STR.none}</dd>
   <dt>${esc(STR.cardEp)}</dt><dd>${esc(STR.planned)}</dd>
   ${scenesFor(o.id).length?`<dt>${esc(STR.nav.scene)}</dt><dd><div class="links">${scenesFor(o.id).map(s=>`<button type="button" class="lk" data-go="scene=${esc(s.id)}">${esc(STR.vw.open)} · ${esc(s.title)}</button>`).join('')}</div></dd>`:''}</dl></article>`;}
function bmWire(v){   // only the search box needs its own listener (it is re-created with the tree)
  const q=$('#bmq',v);if(q)q.addEventListener('input',()=>{BM.q=q.value;const pos=q.selectionStart;bmRefreshTree();const n=$('#bmq');if(n){n.focus();try{n.setSelectionRange(pos,pos);}catch(_){}}});
}
/* one delegated listener each, added once (renders never stack listeners) */
document.addEventListener('change',e=>{if(!e.target.closest('.bm'))return;const f=e.target.dataset.f;if(f){BM.F[f]=e.target.value||undefined;render();return;}
  const x=e.target.dataset.xt;if(x){const r={...ROUTE,cell:null};if(x==='xtx')r.x=e.target.value;else r.y=e.target.value;go(r);}});
document.addEventListener('click',e=>{if(e.target.closest('.bm [data-act=clearf]')){BM.F={};BM.q='';render();}});
function bmRefreshTree(){const t=$('.p-tree .pane');if(t){const open=$('.filt',t)?.open;t.innerHTML=bmTree(ROUTE.ch&&MAPD.M.chapters.find(c=>c.id===ROUTE.ch));if(open)$('.filt',t).open=true;bmWire(t);}
  if(ROUTE.name==='x'){const m=$('.p-mid .pane');if(m)m.innerHTML=bmXt(ROUTE);}}
