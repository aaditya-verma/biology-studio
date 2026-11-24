/* Biology Studio — Today (§8a: 1 column phone · 2 columns phone landscape / tablet · 2–3 columns tablet landscape · 3 columns desktop).
   Owner doc: build/design-plan.md §4.1. U3 (D-087, P2/P4/P5): a progress hero (due · cards started · recall · one Start) first, then the
   plan card (On the go / Study as a switch, 20-lessons.js lsTodayHtml), then "Next up" (Continue + the Cards module, one snap row),
   then start here, map stats, what's coming. EDIT: words in STR; plan sizes in CONFIG.today. */
'use strict';
SCREENS.today=function(v){
  ROUTE.crumbs=[{label:STR.todayTitle}];
  const M=MAPD.M,C=MAPD.C;if(!M&&!MAPD.err)mapLoad().then(()=>{if(ROUTE.name==='today')render();});
  if(!LN.idx&&!LN.err)lnLoad().then(()=>{if(ROUTE.name==='today')render();},()=>{});
  if(CONFIG.learn.lessons.some(ch=>!LS.les[ch]&&!LS.err[ch]))lsLoadAll().then(()=>{if(ROUTE.name==='today')render();});
  const x1=C.filter(o=>o.x1).length,chs=M?M.chapters.length:0;
  const L=LN.idx?lnList():[],due=LN.idx?lnDeckDue().length:null,done=LN.idx?L.filter(c=>lnStatus(c.id)!=='none').length:null,R=LN.idx?lsRecall():null;

  const hero=`<section class="card td-hero"><div class="stats">
      <div class="stat"><b>${due===null?'…':due}</b><span class="sm mut">${esc(STR.ls.heroDue)}</span></div>
      <div class="stat"><b>${done===null?'…':done+'/'+L.length}</b><span class="sm mut">${esc(STR.ls.heroStarted)}</span></div>
      <div class="stat"><b>${R&&R.pct!==null?R.pct+'%':'—'}</b><span class="sm mut">${esc(STR.ls.heroRecall)}</span></div></div>
      <p style="margin-top:10px"><button type="button" class="btn pri" data-go="${esc(LN.idx?lsTodayPrimary():'deck=go')}">${esc(STR.ls.startBtn)}</button></p>
      <p class="xs mut" style="margin-top:6px">${esc(STR.ls.heroLead)}</p></section>`;

  /* "Next up": Continue (recently visited concepts) + the Cards module's own continue/next-new card, one horizontal snap row (U3, P5) */
  const recent=Object.entries(state.visited).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([id])=>MAPD.byId[id]).filter(Boolean);
  const cur=state.last.card&&L.find(c=>c.id===state.last.card),firstNew=L.find(c=>lnStatus(c.id)==='none');
  const cardUp=[];
  if(cur)cardUp.push({id:cur.id,name:STR.ln.today.cont+': '+cur.title,go:'card='+cur.id,layer:(MAPD.byId[cur.id]||{}).layer});
  if(firstNew&&(!cur||firstNew.id!==cur.id))cardUp.push({id:firstNew.id,name:(done?'':STR.ln.today.start+' · ')+firstNew.title,go:'card='+firstNew.id,layer:(MAPD.byId[firstNew.id]||{}).layer});
  const nextUp=cardUp.concat(recent.map(o=>({id:o.id,name:o.name,go:'concept='+o.id,layer:o.layer})));
  const nuCard=o=>`<button type="button" class="nu-card" data-go="${esc(o.go)}"><span class="sw L-${esc(o.layer||'none')}" aria-hidden="true"></span><span class="nm">${esc(o.name)}</span><span class="id">${esc(o.id)}</span></button>`;
  const nextUpHtml=`<section class="card td-nextup"><h2>${esc(STR.ls.nextUpT)}</h2>
      ${nextUp.length?`<div class="snap">${nextUp.map(nuCard).join('')}</div>`:`<p class="mut sm">${esc(STR.continueNone)}</p>`}
      <p class="row" style="margin-top:10px"><span class="sm mut">${esc(LN.idx?STR.ln.today.compact(done,L.length):STR.ln.loading)}</span><span class="sp"></span><button type="button" class="btn sm" data-go="lessons">${esc(STR.ls.pathT)}</button><button type="button" class="btn sm" data-go="cards">${esc(STR.ln.today.all)}</button></p></section>`;

  v.innerHTML=`<h1>${esc(STR.todayTitle)}</h1>
  <div class="today">${hero}${lsTodayHtml()}${nextUpHtml}
    <section class="card"><h2>${esc(STR.startT)}</h2>
      <button type="button" class="lrow" data-go="map=E00"><span class="sw L-none" aria-hidden="true"></span><span class="nm">${esc(STR.startPart0)}</span><span class="id">E00</span></button>
      <button type="button" class="lrow" data-go="map=E05"><span class="sw L-meso" aria-hidden="true"></span><span class="nm">${esc(STR.startGastr)}</span><span class="id">E05</span></button>
      <button type="button" class="lrow" data-go="scene=sc-E00.01.04"><span class="sw L-endo" aria-hidden="true"></span><span class="nm">${esc(STR.start3d)}</span><span class="id">3D</span></button></section>
    <section class="card"><h2>${esc(STR.mapStatsT)}</h2><div class="stats">
      <div class="stat"><b>${C.length||'…'}</b><span class="sm mut">${esc(STR.concepts)}</span></div>
      <div class="stat"><b>${chs||'…'}</b><span class="sm mut">${esc(STR.chapters)}</span></div>
      <div class="stat"><b>${M?x1:'…'}</b><span class="sm mut">${esc(STR.researched)}</span></div></div>
      <p style="margin-top:12px"><button type="button" class="btn pri" data-go="map">${esc(STR.nav.map)}</button></p></section>
    <section class="card wide"><h2>${esc(STR.comingT)}</h2><ul class="sm">${STR.coming.map(s=>`<li>${esc(s)}</li>`).join('')}</ul>${editBtn('screen','today','src/js/10-today.js + content/strings.js')}</section>
  </div>`;
};
