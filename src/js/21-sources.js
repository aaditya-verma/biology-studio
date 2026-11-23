/* Biology Studio — sources + Resources (SR1, D-098). Owner docs: docs/card-spec.md §1a (sources.json fields), build/design-plan.md §4.12.
   (1) citeHtml(cite, mark): a cite as links — book sections open that section in the Book map (#map=E05&sec=E05.02); every Rxx is a small
       inline chip that opens the source sheet (title, our one-line note, tier · species · mark, Open ↗, PubMed ↗, Also used in).
   (2) #res = Resources (a nav item; in the More sheet on phone portrait): Book · Research · Curriculum · Tools & assets · How we mark facts.
   Links + our own one-line note only — no abstracts or quotes (RULES §G). Data: content/E/sources.json (tools/card-check --write-sources),
   map.json (NMC codes). Nothing here is saved (filters live in memory). EDIT: tab order in RES_TABS, words in STR.src, look in app.css (SR1 block). */
'use strict';
const RES_TABS=['book','research','curriculum','tools','marks'];   // EDIT: Resources tabs, in order (#res=<tab>)
const RES={F:{ch:'',tier:'',sp:'',mark:'',q:''},err:null,seen:null};
const srcReg=()=>{const s=CD.src;if(!s)return {};if(!s._by)s._by=Object.fromEntries((s.registry||[]).map(r=>[r.id,r]));return s._by;};
const srcUrlSec=(ch,sec)=>'map='+ch+(sec?'&sec='+sec:'');

/* (1) a cite string as links + chips (falls back to plain text when it does not parse — card-check keeps cards clean) */
function citeHtml(cite,mark){let p;try{p=parseCite(cite);}catch(_){return esc(cite);}
  const reg=srcReg(),secN=(CD.src&&CD.src.sections)||{},chN=(CD.src&&CD.src.chapters)||{};
  const sec=x=>{const k=x.sec||x.ch,nm=secN[k]||chN[x.ch]||'';return `<a class="cite-b" href="#${esc(srcUrlSec(x.ch,x.sec))}" title="${esc(STR.src.bookAt(k,nm))}">${esc(k)}${x.loc?' '+esc(x.loc):''}</a>`;};
  const src=x=>{const r=reg[x.id];return `<a class="src-chip" href="#res=research&amp;id=${esc(x.id)}" role="button" aria-haspopup="dialog" data-src="${esc(x.id)}"${mark?` data-mark="${esc(mark)}"`:''} aria-label="${esc(STR.src.chipL(x.id+(x.loc?' '+x.loc:''),r?r.name:''))}">${esc(x.id)}${x.loc?' '+esc(x.loc):''}</a>`;};
  const L=p.sections.map(sec).join(', '),R=p.sources.map(src).concat(p.xrefs.map(sec)).join(', ');
  return L&&R?L+' · '+R:L||(' · '+R);}

/* the source sheet (one dialog, made on first use; a bottom sheet on phone portrait like every dialog — D-087) */
function srcDlg(){let d=$('#srcdlg');if(d)return d;d=document.createElement('dialog');d.id='srcdlg';d.className='src-dlg';d.setAttribute('aria-labelledby','srcdT');
  d.innerHTML=`<div class="grip" aria-hidden="true"><span></span></div><div id="srcdB"></div><div class="row src-dx"><span class="sp"></span><button type="button" class="btn" id="srcdX">${esc(STR.close)}</button></div>`;
  document.body.appendChild(d);
  d.addEventListener('click',e=>{if(e.target.closest('#srcdX')){d.close();return;}
    if(e.target.closest('[data-go],a[href^="#"]'))d.close();   // a link inside the sheet: close it first, then the shell / the browser goes there (D-084 history)
    else if(e.target===d){const b=d.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)d.close();}});
  d.addEventListener('close',()=>{const o=SRCD.opener;SRCD.opener=null;if(o&&o.isConnected&&!$('dialog[open]'))o.focus({preventScroll:true});});   // focus goes back to the chip (G-A11y)
  return d;}
const SRCD={opener:null};
function srcSheetHtml(r,mark){const u=r.usedBy||{cards:[],lessons:[],dossiers:[]},S=STR.src,idx=(LN.idx&&LN.idx.cards)||[],ttl=Object.fromEntries(idx.map(c=>[c.id,c.title]));
  const meta=[S.tier(r.tier),r.species&&r.species.length?r.species.join(', '):S.spNone].concat(mark?[S.lineMark(mark,STR.marks[mark]||'')]:[]);
  const links=(r.doi?`<a class="btn pri" href="${esc(r.url)}" target="_blank" rel="noopener">${esc(S.open)} ↗${S.nt(r.id)}</a>`:r.url&&r.url!==r.pubmed?`<a class="btn pri" href="${esc(r.url)}" target="_blank" rel="noopener">${esc(S.openWeb)} ↗${S.nt(r.id)}</a>`:'')
    +(r.pubmed?`<a class="btn" href="${esc(r.pubmed)}" target="_blank" rel="noopener">${esc(S.pubmed)} ↗${S.nt(r.id)}</a>`:'');
  const also=u.cards.map(c=>`<li><a href="#card=${esc(c)}">${esc(c)} ${esc(ttl[c]||'')}</a></li>`)
    .concat(u.lessons.map(l=>`<li><a href="#lesson=${esc(l)}">${esc(S.lessonL(l))}</a></li>`));
  const dos=u.dossiers.length?`<details class="src-dos sm"><summary>${esc(S.dosT(u.dossiers.length))}</summary><ul class="src-also">${u.dossiers.map(d=>`<li><a href="${esc(CONFIG.src.repo+CONFIG.src.dossiers+d+'.md')}" target="_blank" rel="noopener">${esc(S.dossierL(d))} ↗</a></li>`).join('')}</ul></details>`:'';   // G-Learn r1: cards + lessons first, the research notes folded
  return `<p class="xs mut mono">${esc(r.id)}</p><h2 id="srcdT" class="src-t">${esc(r.title||r.name)}</h2>`
    +(r.note?`<p class="sm"><span class="sr">${esc(S.noteL)}</span>${esc(r.note)}</p>`:'')
    +`<p class="xs mut">${meta.map(esc).join(' · ')}</p>`+(r.licence?`<p class="xs mut">${esc(S.licL)} ${esc(r.licence)}</p>`:'')
    +(links?`<div class="row src-links">${links}</div>`:`<p class="sm mut">${esc(S.noLink)}</p>`)
    +(also.length||dos?`<h3 class="sm">${esc(S.alsoT)}</h3>${also.length?`<ul class="src-also sm">${also.join('')}</ul>`:''}${dos}`:'')
    +`<p class="sm"><a href="#res=research&amp;id=${esc(r.id)}">${esc(S.allSrc)}</a></p>`;}
function srcOpen(id,mark,opener){cdSources().then(()=>{const r=srcReg()[id];if(!r){toast(STR.src.unknown(id));return;}
  const d=srcDlg();$('#srcdB',d).innerHTML=srcSheetHtml(r,mark);SRCD.opener=opener||null;if(!d.open)d.showModal();const t=$('#srcdT',d);t.setAttribute('tabindex','-1');t.focus();},()=>toast(STR.src.loadFail));}
document.addEventListener('click',e=>{const c=e.target.closest('[data-src]');if(!c||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();srcOpen(c.dataset.src,c.dataset.mark||'',c);});
document.addEventListener('keydown',e=>{if(e.key===' '&&e.target.matches&&e.target.matches('a[data-src]')){e.preventDefault();e.target.click();}});   // a role=button link opens on Space too

/* Copy sources (card Sources box): one line per source — id, title, link */
function srcLines(ids){const reg=srcReg();return ids.map(i=>{const r=reg[i];return r?`${i} — ${r.title||r.name}${r.url?' — '+r.url:''}`:i;}).join('\n');}
async function srcCopy(ids){const t=srcLines(ids);try{await navigator.clipboard.writeText(t);toast(STR.src.copied(ids.length));}catch(_){toast(STR.copyFail);}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-src-copy]');if(!b)return;srcCopy(b.dataset.srcCopy.split(',').filter(Boolean));});

/* (2) #res — Resources */
const RES_F0=()=>({ch:'',tier:'',sp:'',mark:'',q:''});
SCREENS.res=function(v,prev){const S=STR.src,tab=ROUTE.view||'book',arrived=RES.seen!==ROUTE.raw;ROUTE.crumbs=[{label:S.title,hash:'res'},{label:S.tabs[tab]}];
  if(!CD.src){v.innerHTML=`<h1>${esc(S.title)}</h1><p class="mut" role="status">${esc(RES.err?S.loadFail+' ('+RES.err+')':S.loading)}</p>`;
    cdSources().then(()=>{RES.err=null;if(ROUTE.name!=='res')return;render();const el=ROUTE.id&&document.getElementById('src-'+ROUTE.id);if(el&&el.hasAttribute('data-focus-first')){el.setAttribute('tabindex','-1');el.focus({preventScroll:true});}},e=>{RES.err=(e&&e.message)||'error';if(ROUTE.name==='res')render();});return;}   // G-Eng r1: its own error, retried on every visit
  if(arrived&&ROUTE.id&&tab==='research'&&!resRows().some(r=>r.id===ROUTE.id))RES.F=RES_F0();   // a deep link shows its source: filters that hide it are cleared on arrival only (G-Eng r1)
  if(tab==='curriculum'&&!MAPD.M&&!MAPD.err){mapLoad().then(()=>{if(ROUTE.name==='res')render();});}
  const body={book:resBook,research:resResearch,curriculum:resCurriculum,tools:resTools,marks:resMarks}[tab]();
  v.innerHTML=`<div class="res" data-tab="${esc(tab)}"><h1>${esc(S.title)}</h1><p class="sm mut">${esc(S.lead)}</p>
    ${Object.keys(LN.ck||{}).some(lnRun)?`<p class="banner" role="note">${esc(S.ckOpen)}</p>`:''}<nav class="seg res-tabs" aria-label="${esc(S.tabsL)}">${RES_TABS.map(t=>`<button type="button" data-go="res=${t}" data-fk="res-${t}"${t===tab?' aria-current="page"':''}>${esc(S.tabs[t])}</button>`).join('')}</nav>
    <h2 class="res-h2 sr">${esc(S.tabs[tab])}</h2>${body}</div>`;
  {const ct=v.querySelector('.res-tabs [aria-current]');if(ct){const n=ct.parentElement;n.scrollLeft=Math.max(0,ct.offsetLeft-(n.clientWidth-ct.offsetWidth)/2);}}   // G-Art r1: the current tab is always in view (the pill scrolls; its fade cues the rest)
  RES.seen=ROUTE.raw;   // G-Eng r2: a theme / motion redraw is not an arrival (set only once the data is drawn)
  if(tab==='research')resWire(v);
  if(ROUTE.id){const el=document.getElementById('src-'+ROUTE.id);if(el){el.classList.add('hit');if(arrived){el.setAttribute('data-focus-first','');requestAnimationFrame(()=>el.scrollIntoView({block:'center'}));}}}
};
function resBook(){const S=STR.src,s=CD.src,r0=srcReg().R00||{},secs=Object.entries(s.sections||{});
  return `<section class="card"><h2>${esc(r0.title||r0.name||STR.ln.bookDefault)}</h2><p class="sm">${esc(S.bookLead)}</p><p class="xs mut">${esc(S.licL)} ${esc(r0.licence||'')}</p></section>
    <ul class="res-list">${Object.entries(s.chapters||{}).map(([ch,t])=>{const L=secs.filter(([k])=>k.startsWith(ch+'.'));
      return `<li><details class="res-ch"><summary><span class="mono">${esc(ch)}</span><span class="res-t">${esc(t)} <span class="xs mut">· ${esc(S.nSec(L.length))}</span></span></summary>
        <ul class="res-secs sm"><li><a href="#${esc(srcUrlSec(ch))}">${esc(S.chOpen(ch))}</a></li>${L.map(([k,n])=>`<li><a href="#${esc(srcUrlSec(ch,k))}"><span class="mono">${esc(k)}</span> ${esc(n)}</a></li>`).join('')}</ul></details></li>`;}).join('')}</ul>`;}
function resRows(){const F=RES.F,q=F.q.trim().toLowerCase();
  return (CD.src.registry||[]).filter(r=>r.id!=='R00'&&(!F.ch||(r.chapters||[]).includes(F.ch))&&(!F.tier||String(r.tier)===F.tier)
    &&(!F.sp||(F.sp==='-'?!(r.species||[]).length:(r.species||[]).includes(F.sp)))&&(!F.mark||((r.usedBy||{}).marks||[]).includes(F.mark))
    &&(!q||(r.id+' '+(r.title||'')+' '+(r.note||'')).toLowerCase().includes(q)))
    .map((r,i)=>[r,i]).sort((a,b)=>(((b[0].usedBy||{}).cards||[]).length>0)-(((a[0].usedBy||{}).cards||[]).length>0)||a[1]-b[1]).map(x=>x[0]);}   // G-Learn r1: sources cited on a card come first, then registry order
function resRowHtml(r){const S=STR.src,u=r.usedBy||{};
  return `<li class="src-row" id="src-${esc(r.id)}"><h3 class="src-h"><a class="src-rt" href="#res=research&amp;id=${esc(r.id)}" role="button" aria-haspopup="dialog" data-src="${esc(r.id)}"><span class="mono">${esc(r.id)}</span><span class="res-t">${esc(r.title||r.name)}</span></a></h3>
    ${r.note?`<p class="sm">${esc(r.note)}</p>`:''}<p class="xs mut">${esc([S.tier(r.tier)].concat(r.species&&r.species.length?[r.species.join(', ')]:[],(r.chapters||[]).length?[S.chs(r.chapters)]:[],u.cards&&u.cards.length?[S.nCards(u.cards.length)]:[]).join(' · '))}</p>
    ${r.url||r.pubmed?`<p class="sm src-rl">${r.url&&r.url!==r.pubmed?`<a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.doi?S.open:S.openWeb)} ↗${S.nt(r.id)}</a>`:''}${r.pubmed?` <a href="${esc(r.pubmed)}" target="_blank" rel="noopener">${esc(S.pubmed)} ↗${S.nt(r.id)}</a>`:''}</p>`:''}</li>`;}
function resResearch(){const S=STR.src,F=RES.F,reg=CD.src.registry||[],chs=Object.keys(CD.src.chapters||{}),rows=resRows();
  const tiers=[...new Set(reg.map(r=>String(r.tier)))].filter(t=>t!=='0'),sps=[...new Set(reg.flatMap(r=>r.species||[]))];
  const sel=(id,lab,k,opts)=>`<label class="res-f" for="${id}"><span class="xs">${esc(lab)}</span><select id="${id}" data-rf="${k}"><option value="">${esc(S.any)}</option>${opts.map(([v,l])=>`<option value="${esc(v)}"${F[k]===v?' selected':''}>${esc(l)}</option>`).join('')}</select></label>`;
  const filt=`<div class="res-fs">${sel('rfCh',S.fCh,'ch',chs.map(c=>[c,c+' '+CD.src.chapters[c]]))}${sel('rfTier',S.fTier,'tier',tiers.map(t=>[t,S.tier(t)]))}
    ${sel('rfSp',S.fSp,'sp',sps.map(s=>[s,s]).concat([['-',S.spNone]]))}${sel('rfMark',S.fMark,'mark',['✔✔','✔','⚑','✚','≈'].map(m=>[m,m+' '+(STR.marks[m]||'')]))}
    <label class="res-f res-q" for="rfQ"><span class="xs">${esc(S.fQ)}</span><input id="rfQ" type="search" data-rf="q" value="${esc(F.q)}" autocomplete="off"></label>
    <button type="button" class="btn" data-rf-clear${Object.values(F).some(Boolean)?'':' disabled'}>${esc(S.clear)}</button></div>`;   // G-A11y r1: always there (disabled when nothing is set), so focus never falls to the page
  return `<div class="res-rs"><aside class="res-side" aria-label="${esc(S.filtersL)}">${['dev-p','dev-pl','dev-tp'].includes(DEV.cls)?`<details class="res-fd"${Object.values(F).some(Boolean)?' open':''}><summary>${esc(S.filtersL)}</summary>${filt}</details>`:filt}<p class="xs mut">${esc(S.spHint)}</p></aside>
    <section class="res-main" aria-label="${esc(S.tabs.research)}"><p class="sm" role="status" id="rfN">${esc(S.nShown(rows.length,reg.length-1))}</p><ul class="res-list src-rows" id="rfL">${rows.length?rows.map(resRowHtml).join(''):`<li class="sm mut">${esc(S.none)}</li>`}</ul></section></div>`;}
/* filters update in place (G-A11y r1): the list + the one status line change, the controls stay — focus, caret and the live region are kept;
   the count is announced after typing pauses (300 ms) */
function resWire(v){let tq=0;
  const upd=slow=>{const L=$('#rfL',v),rows=resRows();if(L)L.innerHTML=rows.length?rows.map(resRowHtml).join(''):`<li class="sm mut">${esc(STR.src.none)}</li>`;
    const c=$('[data-rf-clear]',v);if(c)c.disabled=!Object.values(RES.F).some(Boolean);
    const say=()=>{const n=$('#rfN',v);if(n)n.textContent=STR.src.nShown(rows.length,CD.src.registry.length-1);};clearTimeout(tq);if(slow)tq=setTimeout(say,300);else say();};
  $$('[data-rf]',v).forEach(el=>{el.addEventListener(el.tagName==='INPUT'?'input':'change',()=>{RES.F[el.dataset.rf]=el.value;upd(el.tagName==='INPUT');});});
  const c=$('[data-rf-clear]',v);if(c)c.onclick=()=>{RES.F=RES_F0();$$('[data-rf]',v).forEach(el=>{el.value='';});upd(false);const f=$('#rfCh',v);if(f)f.focus();};}
function resCurriculum(){const S=STR.src,r30=srcReg().R30;
  const head=`<section class="card"><h2>${esc(S.nmcT)}</h2><p class="sm">${esc(r30?r30.title:S.nmcT)}</p><p class="xs mut">${esc(S.nmcLead)}</p></section>`;
  if(!MAPD.M)return head+`<p class="mut" role="status">${esc(MAPD.err?STR.loadFail:S.loading)}</p>`;
  const by={};for(const o of MAPD.C)for(const a of (o.an||[]))(by[a]=by[a]||[]).push(o);
  const codes=Object.keys(by).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
  return head+`<p class="sm" role="status">${esc(S.nCodes(codes.length))}</p><ul class="res-list">${codes.map(a=>`<li><details class="res-ch"><summary><span class="mono">${esc(a)}</span><span class="res-t xs mut">${esc(S.nCon(by[a].length))}</span></summary><ul class="res-secs sm">${by[a].map(o=>`<li><a href="#concept=${esc(o.id)}"><span class="mono">${esc(o.id)}</span> ${esc(o.name)}</a></li>`).join('')}</ul></details></li>`).join('')}</ul>`;}
function resTools(){const S=STR.src,T=CD.src.third_party||[],app=T.filter(t=>/^app\b/i.test(t.use)),mk=T.filter(t=>!/^app\b/i.test(t.use));   // G-Art r1: what is in the app (with what it does) · what we use to make it (name + licence)
  const li=(t,full)=>`<li class="res-tool"><b>${esc(t.name)}</b>${full?`<p class="sm">${esc(t.use.replace(/^app\s*/i,''))}</p>`:''}<p class="xs mut">${esc(S.licL)} ${esc(t.licence)}</p></li>`;
  return `<p class="sm">${esc(S.toolsLead)}</p><h3 class="res-sub">${esc(S.toolsApp)}</h3><ul class="res-list">${app.map(t=>li(t,true)).join('')}</ul>
    <h3 class="res-sub">${esc(S.toolsMake)}</h3><ul class="res-list res-tools-mk">${mk.map(t=>li(t,false)).join('')}</ul>
    <p class="sm"><a href="${esc(CONFIG.src.repo+'THIRD_PARTY.md')}" target="_blank" rel="noopener">${esc(S.toolsAll)} ↗${S.nt('THIRD_PARTY.md')}</a></p>`;}
function resMarks(){const S=STR.src;
  return `<p class="sm">${esc(S.marksLead)}</p><ul class="res-list res-marks">${Object.keys(S.markLong).map(m=>`<li class="card"><b class="mark res-mk" aria-hidden="true">${esc(m)}</b><div><b>${esc(STR.marks[m]||'')}</b><span class="sr"> (${esc(m)})</span><p class="sm">${esc(S.markLong[m])}</p></div></li>`).join('')}</ul>
    <p class="xs mut">${esc(S.citeHow)}</p>`;}

/* in-app tests (?test=1 — 91-tests.js calls this) */
function srcTests(t){
  const a=parseHash('#res=research&id=R05f'),b=parseHash('#map=E06&sec=E06.06'),c=parseHash('#map=E06&sec=E07.01'),d=parseHash('#res'),e=parseHash('#res=nope');
  t('SR1 address: #res=research&id=R05f',a.name==='res'&&a.view==='research'&&a.id==='R05f'&&hashOf(a)==='res=research&id=R05f');
  t('SR1 address: #map=E06&sec=E06.06 round trip; a section of another chapter is dropped',b.sec==='E06.06'&&hashOf(b)==='map=E06&sec=E06.06'&&!c.sec);
  t('SR1 address: #res and an unknown tab → Book',d.view==='book'&&e.view==='book');
  if(CD.src){const h=citeHtml('E05.01 · R06 CS6','✔✔');
    t('SR1 cite: book section → Book map link, source → chip with its mark',/href="#map=E05&amp;sec=E05.01"/.test(h)&&/data-src="R06"/.test(h)&&/data-mark="✔✔"/.test(h)&&/R06 CS6/.test(h),h);
    t('SR1 cite: a bad cite stays plain text',citeHtml('nonsense')==='nonsense');
    const r=srcReg();t('SR1 data: every source a card cites opens (url), the book has none',(CD.src.registry||[]).filter(x=>x.usedBy&&x.usedBy.cards.length&&x.id!=='R00').every(x=>x.url)&&!(r.R00||{}).url);}
}
