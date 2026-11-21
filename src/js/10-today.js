/* Biology Studio — Today (§8a: 1 column phone · 2 columns phone landscape / tablet · 2–3 columns tablet landscape · 3 columns desktop).
   Owner doc: build/design-plan.md §4.1. L2 (IB01, D-070): the two plans first — On the go (≤ 5 min) and Study (15–30 min) (20-lessons.js lsTodayHtml) —
   then the Cards box (18-learn.js lnTodayHtml), continue, start here, map stats, what's coming. EDIT: words in STR; plan sizes in CONFIG.today. */
'use strict';
SCREENS.today=function(v){
  ROUTE.crumbs=[{label:STR.todayTitle}];
  const M=MAPD.M,C=MAPD.C;if(!M&&!MAPD.err)mapLoad().then(()=>{if(ROUTE.name==='today')render();});
  if(!LN.idx&&!LN.err)lnLoad().then(()=>{if(ROUTE.name==='today')render();},()=>{});
  if(CONFIG.learn.lessons.some(ch=>!LS.les[ch]&&!LS.err[ch]))lsLoadAll().then(()=>{if(ROUTE.name==='today')render();});
  const recent=Object.entries(state.visited).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([id])=>MAPD.byId[id]).filter(Boolean);
  const x1=C.filter(o=>o.x1).length,chs=M?M.chapters.length:0;
  const row=o=>`<button type="button" class="lrow" data-go="concept=${esc(o.id)}"><span class="sw L-${esc(o.layer)}" aria-hidden="true"></span><span class="nm">${esc(o.name)}</span><span class="id">${esc(o.id)}</span></button>`;
  v.innerHTML=`<h1>${esc(STR.todayTitle)}</h1><p class="mut" style="max-width:var(--measure)">${esc(STR.todayLead)}</p>
  <div class="today">${lsTodayHtml()}${lnTodayHtml()}
    <section class="card"><h2>${esc(STR.continueT)}</h2>${recent.length?recent.map(row).join(''):`<p class="mut sm">${esc(STR.continueNone)}</p>`}</section>
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
