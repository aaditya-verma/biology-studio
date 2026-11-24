/* Biology Studio — layout audit (RULES C8 + C13), run by tools/layout-check on every size and by ?debug=layout (button in the overlay).
   Ported from DrumPath v36 14-layout-check.js, plus tap size, text size and fixed-over-controls. Owner doc: build/design-plan.md §7.
   Checks the current screen: overlap · spill · page-wider · tap < --tap · text < --fs-min · fixed/sticky bars covering a control · a word split mid-word in a list title or h1 (L1F)
   · U2 part 2 (D-087): ctrl-overlap (boxes or tap areas of two controls) · ring-touch (boxes grown by box-shadow spread / outline) · pill-wrap · slider-label
   · stage-collide (3D labels vs labels, stamp, notes, gizmo, scale) · no-scroll-cue (a side panel hides content with no "More ↓"). Each has a --selftest case in tools/layout-check.
   EDIT: thresholds come from the CSS tokens; skip an element on purpose with data-layout-skip. */
'use strict';
function layoutAudit(root){
  root=root||document.body;const issues=[],W=document.documentElement.clientWidth,H=innerHeight,cs=getComputedStyle(document.documentElement);
  const px=v=>{const d=document.createElement('div');d.style.cssText='position:absolute;visibility:hidden;width:'+v;document.body.appendChild(d);const w=d.getBoundingClientRect().width;d.remove();return w;};
  const TAP=px(cs.getPropertyValue('--tap').trim()||'44px'),FSMIN=px(cs.getPropertyValue('--fs-min').trim()||'12px');
  const closedIn=el=>{for(let d=el.closest('details:not([open])');d;d=d.parentElement&&d.parentElement.closest('details:not([open])')){const sm=d.querySelector(':scope>summary');if(!(sm&&sm.contains(el)))return true;}return false;};
  const vis=el=>{if(closedIn(el))return false;const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden'||+s.opacity===0)return false;const r=el.getBoundingClientRect();return r.width>0&&r.height>0;};
  const scrollsX=el=>{for(let p=el.parentElement;p&&p!==document.body;p=p.parentElement){const o=getComputedStyle(p).overflowX;if(o==='auto'||o==='scroll')return p;}return null;};
  const name=el=>{let s=el.tagName.toLowerCase();if(el.id)s+='#'+el.id;const c=[...el.classList].slice(0,2).join('.');if(c)s+='.'+c;const t=(el.textContent||'').trim().replace(/\s+/g,' ').slice(0,28);return s+(t?' “'+t+'”':'');};
  const skip=el=>el.closest('svg,textarea,select,#dbg,[data-layout-skip],.sr');
  const clipTo=(el,r)=>{let L=r.left,T=r.top,R=r.right,B=r.bottom;for(let p=el;p&&p!==document.body;p=p.parentElement){const s=getComputedStyle(p);
    if(s.overflowX!=='visible'||s.overflowY!=='visible'){const q=p.getBoundingClientRect();L=Math.max(L,q.left);T=Math.max(T,q.top);R=Math.min(R,q.right);B=Math.min(B,q.bottom);}}
    return R-L>1&&B-T>1?{left:L,top:T,right:R,bottom:B}:null;};
  const boxes=[],tw=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.textContent.trim()?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_REJECT});let n;
  while((n=tw.nextNode())){const el=n.parentElement;if(!el||!vis(el)||skip(el))continue;const rg=document.createRange();rg.selectNodeContents(n);
    for(const r0 of rg.getClientRects()){if(r0.width<2||r0.height<2)continue;const r=clipTo(el,r0);if(r)boxes.push({el,r});}
    const fs=parseFloat(getComputedStyle(el).fontSize);if(fs+0.01<FSMIN&&!el.closest('.mono.slog'))issues.push({kind:'text-small',what:name(el)+' '+fs+'px < '+FSMIN+'px'});}
  // 1. text overlapping other text (not nested; fixed/sticky bars excluded — check 6 covers them)
  const seen=new Set();
  for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j];if(a.el===b.el||a.el.contains(b.el)||b.el.contains(a.el))continue;
    const x=Math.min(a.r.right,b.r.right)-Math.max(a.r.left,b.r.left),y=Math.min(a.r.bottom,b.r.bottom)-Math.max(a.r.top,b.r.top);
    if(x>2&&y>3){const fx=e=>{for(let p=e;p;p=p.parentElement){const s=getComputedStyle(p).position;if(s==='fixed'||s==='sticky')return true;}return false;};if(fx(a.el)||fx(b.el))continue;
      const k=name(a.el)+'|'+name(b.el);if(!seen.has(k)){seen.add(k);issues.push({kind:'overlap',what:name(a.el)+'  ⟷  '+name(b.el)});}}}
  // 2. text spilling out of its own box
  root.querySelectorAll('*').forEach(el=>{if(!vis(el)||skip(el)||el.closest('input'))return;const s=getComputedStyle(el);if(![...el.childNodes].some(c=>c.nodeType===3&&c.textContent.trim()))return;
    if(el.scrollWidth>el.clientWidth+2&&s.overflowX==='visible'&&s.textOverflow!=='ellipsis'&&el.clientWidth>0&&s.display!=='inline')issues.push({kind:'spill',what:name(el)+' needs '+el.scrollWidth+'px, has '+el.clientWidth+'px'});});
  // 3. page wider than the screen (sideways scroll only inside areas meant to scroll, §8a rule 6)
  if(document.documentElement.scrollWidth>W+1){const wide=[...root.querySelectorAll('*')].filter(el=>vis(el)&&!scrollsX(el)&&el.getBoundingClientRect().right>W+1&&getComputedStyle(el).position!=='fixed');
    issues.push({kind:'page-wider',what:'page '+document.documentElement.scrollWidth+'px on '+W+'px: '+wide.filter(el=>!wide.some(o=>o!==el&&o.contains(el))).slice(0,4).map(name).join(', ')});}
  // 4. tap targets smaller than --tap (touch 44, mouse 36), visible part only
  const ctrls=[...root.querySelectorAll('button,a[href],input:not([type=file]):not(.sr),select,summary,[role=button],label.btn')].filter(el=>vis(el)&&!el.closest('#dbg,[data-layout-skip],.sr'));
  ctrls.forEach(el=>{const r=el.getBoundingClientRect();if(el.closest('.sr'))return;
    if(el.matches('input[type=checkbox],input[type=radio]')){const l=el.closest('label');if(l){const q=l.getBoundingClientRect();if(q.height+0.5>=TAP&&q.width+0.5>=Math.min(TAP,W))return;}}   // H2: a box inside a tap-sized label — the label is the target (WCAG 2.5.8)
    if(r.width+0.5<Math.min(TAP,W)||r.height+0.5<TAP){const inline=getComputedStyle(el).display==='inline'&&el.tagName==='A';if(!inline)issues.push({kind:'tap-small',what:name(el)+' '+Math.round(r.width)+'×'+Math.round(r.height)+' < '+TAP});}});
  // 4b. a control pushed past the side of its own pane or card (hidden or needing a sideways scroll there); tables meant to scroll are fine
  ctrls.forEach(el=>{if(el.closest('.xt-wrap,.seg,.tr-mapw,.snap'))return;   // areas meant to scroll sideways (crosstab, progress map, snap rows — W1, U3 D-087)
    const r=el.getBoundingClientRect();for(let p=el.parentElement;p&&p!==document.body;p=p.parentElement){const s=getComputedStyle(p);
    if(s.overflowX!=='visible'||p.matches('.card,.pane')){const q=p.getBoundingClientRect(),pr=q.right-(parseFloat(s.borderRightWidth)||0);if(r.right>pr+1||r.left<q.left-1)issues.push({kind:'clipped',what:name(el)+' sticks out of '+name(p)+' by '+Math.round(Math.max(r.right-pr,q.left-r.left))+'px'});break;}}});
  // 5. cut off at the right edge inside a card that doesn't scroll
  root.querySelectorAll('.card,.pane').forEach(c=>{if(!vis(c))return;const r=c.getBoundingClientRect();if(r.right>W+1&&!scrollsX(c))issues.push({kind:'cut',what:name(c)+' runs past the screen edge'});});
  // 6. fixed/sticky bars covering a control in view (C8 "nothing fixed over controls")
  const bars=[...document.querySelectorAll('*')].filter(el=>{const p=getComputedStyle(el).position;return (p==='fixed'||p==='sticky')&&vis(el)&&!el.closest('#dbg,dialog,.toast')&&!el.matches('thead th,th.rh,.pane');});
  ctrls.forEach(el=>{if(bars.some(b=>b.contains(el)))return;const r=clipTo(el,el.getBoundingClientRect());if(!r||r.bottom<=0||r.top>=H)return;   // visible part only (scroll areas clip)
    const cx=Math.min(Math.max((r.left+r.right)/2,0),W-1),cy=Math.min(Math.max((r.top+r.bottom)/2,0),H-1),hit=document.elementFromPoint(cx,cy);
    if(!(hit&&!el.contains(hit)&&!hit.contains(el)))return;const bar=bars.find(b=>b.contains(hit));if(!bar)return;
    // a bar at a screen edge only counts if scrolling can't uncover the control (bottom bar at page end, top bar at page top)
    const br=bar.getBoundingClientRect(),sc=document.scrollingElement,atEnd=sc.scrollTop+H>=sc.scrollHeight-1,atTop=sc.scrollTop<=0;
    if(br.top>H/2&&!atEnd)return;if(br.bottom<H/2&&!atTop&&getComputedStyle(bar).position!=='sticky')return;if(br.bottom<H/2&&getComputedStyle(bar).position==='sticky'&&!atTop)return;
    issues.push({kind:'fixed-over',what:name(el)+' covered by '+name(bar)});});
  // 7. L1F (T7): a word split across two lines in a list-row title or an h1 ("Gast/rulati/on" on tablet portrait) — titles wrap on words; a break at a hyphen or dash is a word break, not mid-word
  root.querySelectorAll('.lrow .nm,h1').forEach(el=>{if(!vis(el)||skip(el))return;const w2=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let t;
    while((t=w2.nextNode())){for(const m of t.textContent.matchAll(/[\p{L}\p{N}]{4,}/gu)){const r=document.createRange();r.setStart(t,m.index);r.setEnd(t,m.index+m[0].length);
      const qs=[...r.getClientRects()].filter(q=>q.width>1),bx=el.matches('h1')?(el.closest('.card,section,.pane,main')||el):(()=>{let p=t.parentElement;while(p&&p!==el&&getComputedStyle(p).display==='inline')p=p.parentElement;return p||el;})(),   // h1: the column it lives in (G-Eng r2: never the squeezed box itself)
      cs2=getComputedStyle(bx),room=bx.clientWidth-(parseFloat(cs2.paddingLeft)||0)-(parseFloat(cs2.paddingRight)||0);   // the word's own box (a chip inside the title may be narrower)
      if(qs.reduce((a,q)=>a+q.width,0)>room+1)continue;   // D-087: a word wider than its whole line (200 % text) can only break — not a layout fault
      if(new Set(qs.map(q=>Math.round(q.top))).size>1){issues.push({kind:'midword',what:name(el)+' splits “'+m[0]+'”'});return;}}}});
  // 8–13: U2 part 2 (D-087) — the C8 fails the owner saw live on v18 (T13b) that 1–7 could not see
  issues.push(...layoutAudit2(root,ctrls,TAP,clipTo,vis,name));
  return issues;
}
function layoutAudit2(root,ctrls,TAP,clipTo,vis,name){
  const out=[],ov=(a,b,m)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>(m||1)&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>(m||1);
  const nested=(a,b)=>a.contains(b)||b.contains(a)||(a.closest('label')&&a.closest('label')===b.closest('label'));
  const inlineA=el=>el.tagName==='A'&&getComputedStyle(el).display==='inline';
  const layer=el=>{for(let p=el;p&&p!==document.body;p=p.parentElement){if(p.matches('dialog[open]'))return p;const ps=getComputedStyle(p).position;if(ps==='fixed')return 'fixed';if(ps==='sticky')return p;}return null;};   // an open dialog is its own layer; every other fixed control shares one (dock ⟷ fold handle)
  let modal=null;try{modal=document.querySelector('dialog[open]:modal');}catch(_){modal=document.querySelector('dialog[open]');}   // :modal is Chrome 105+ / Safari 15.6+   // every fixed control shares one layer (dock ⟷ fold handle are compared)   // fixed/sticky bars over the page are check 6's job (fixed-over), not a pair here
  const C=ctrls.filter(el=>!inlineA(el)&&!el.closest('.vw-lbls')&&(!modal||modal.contains(el))).map(el=>{const f=el.getBoundingClientRect(),r=clipTo(el,f);return r?{el,r,f,ly:layer(el)}:null;}).filter(Boolean);
  // 8. ctrl-overlap: two controls' boxes, or one's tap area and the other's box, overlap. Tap area = the box grown to --tap (centred);
  //    a range slider's thumb reaches (--tap − thumb) / 2 past each end of its track (so a ◀ flush with the slider's start is inside its tap area)
  const tapOf=({el,r,f})=>{let L=r.left,R=r.right,T=r.top,B=r.bottom;   // grown from the control's full size (a cell half-scrolled out of its frame is not "small")
    if(el.matches('input[type=range]')){const th=parseFloat(getComputedStyle(el).getPropertyValue('--thumb'))||16,g=Math.max(0,(TAP-th)/2);L-=g;R+=g;}
    else if(!(el.matches('input[type=checkbox],input[type=radio]')&&el.closest('label'))){const gw=Math.max(0,(TAP-f.width)/2);L-=gw;R+=gw;}
    const gh=Math.max(0,(TAP-f.height)/2);T-=gh;B+=gh;return {left:L,right:R,top:T,bottom:B};};
  const seenO=new Set(),seenR=new Set();
  C.sort((a,b)=>a.r.top-b.r.top);
  for(let i=0;i<C.length;i++){const a=C[i],ta=tapOf(a);for(let j=i+1;j<C.length;j++){const b=C[j];if(b.r.top-a.r.bottom>TAP)break;if(nested(a.el,b.el)||a.ly!==b.ly)continue;
    const tb=tapOf(b),hit=ov(a.r,b.r)?'boxes':(ov(ta,b.r)||ov(tb,a.r))?'tap areas':'';
    if(hit){const k=name(a.el)+'|'+name(b.el);if(!seenO.has(k)){seenO.add(k);out.push({kind:'ctrl-overlap',what:name(a.el)+'  ⟷  '+name(b.el)+' ('+hit+')'});}}}}
  // 9. ring-touch: boxes grown by their box-shadow spread (+ offset; blur ignored) and outline (width + offset) — e.g. the on-rings of two neighbouring chips
  const grow=({el,r})=>{const s=getComputedStyle(el);let L=0,R=0,T=0,B=0;
    if(s.boxShadow&&s.boxShadow!=='none')for(const sh of s.boxShadow.split(/,(?![^(]*\))/)){if(/inset/.test(sh))continue;const n=(sh.replace(/rgba?\([^)]*\)|#[0-9a-f]+|[a-z]+\([^)]*\)/gi,'').match(/-?[\d.]+px/g)||[]).map(parseFloat);
      const [x=0,y=0,,sp=0]=n;if(sp<=0&&!x&&!y)continue;L=Math.max(L,sp-x);R=Math.max(R,sp+x);T=Math.max(T,sp-y);B=Math.max(B,sp+y);}
    if(s.outlineStyle!=='none'&&el!==document.activeElement){const o=(parseFloat(s.outlineWidth)||0)+(parseFloat(s.outlineOffset)||0);if(o>0){L=Math.max(L,o);R=Math.max(R,o);T=Math.max(T,o);B=Math.max(B,o);}}
    return {left:r.left-L,right:r.right+R,top:r.top-T,bottom:r.bottom+B,g:L||R||T||B};};
  const G=C.map(c=>Object.assign({},c,{q:grow(c)}));
  for(let i=0;i<G.length;i++){const a=G[i];for(let j=i+1;j<G.length;j++){const b=G[j];if(b.r.top-a.r.bottom>40)break;if(!a.q.g&&!b.q.g)continue;if(nested(a.el,b.el)||a.ly!==b.ly||ov(a.r,b.r))continue;
    if(ov(a.q,b.q,0.5)){const k=name(a.el)+'|'+name(b.el);if(!seenR.has(k)){seenR.add(k);out.push({kind:'ring-touch',what:name(a.el)+'  ⟷  '+name(b.el)+' (rings/shadows meet)'});}}}}
  // 10. pill-wrap: a pill-shaped row of controls (.seg, [data-pill], or radius ≥ half its height) whose controls sit on more than one row, or a control in it whose words wrap
  const pillish=p=>p.matches('[data-pill]')||parseFloat(getComputedStyle(p).borderTopLeftRadius)>=p.getBoundingClientRect().height/2-1;   // pill-shaped: radius ≥ half its height (a .seg restyled as a grid with --r corners is a grid, and may wrap)
  const pills=[...root.querySelectorAll('.seg,[data-pill],.vw-tabs')].filter(p=>vis(p)&&!p.closest('#dbg,[data-layout-skip]')&&pillish(p));
  pills.forEach(p=>{    const kids=[...p.querySelectorAll('button,a[href],[role=button]')].filter(el=>vis(el)&&el.closest('.seg,[data-pill],.vw-tabs')===p);if(kids.length<2)return;
    const tops=kids.map(el=>el.getBoundingClientRect().top);if(Math.max(...tops)-Math.min(...tops)>4){out.push({kind:'pill-wrap',what:name(p)+' wraps onto '+new Set(tops.map(Math.round)).size+' rows'});return;}
    const lines=el=>{const rg=document.createRange();rg.selectNodeContents(el);const q=[...rg.getClientRects()].filter(x=>x.width>1).sort((a,b)=>a.top-b.top);let n=0,bot=-1e9;
      for(const x of q){if(x.top>=bot-2){n++;bot=x.bottom;}else bot=Math.max(bot,x.bottom);}return n;};   // a badge inside a tab is on the same line, not a wrap
    const w=kids.find(el=>lines(el)>1);
    if(w)out.push({kind:'pill-wrap',what:name(w)+' wraps its words inside '+name(p)});});
  // 11. slider-label: a slider's tick labels stay inside the slider's own box
  root.querySelectorAll('.vw-keys,[data-slider-ticks]').forEach(k=>{if(!vis(k))return;const rg=k.closest('.vw-range,[data-slider]')||k.parentElement;const inp=rg&&rg.querySelector('input[type=range]');if(!inp||!vis(inp))return;
    const q=inp.getBoundingClientRect();[...k.children].filter(vis).forEach(sp=>{const r=sp.getBoundingClientRect();if(r.left<q.left-1||r.right>q.right+1)out.push({kind:'slider-label',what:name(sp)+' sits '+Math.round(Math.max(q.left-r.left,r.right-q.right))+'px outside '+name(inp)});});});
  // 12. stage-collide: on a 3D stage, a shown label touches another label, the stamp, the notes line, the axis gizmo or the scale bar
  root.querySelectorAll('.vw-stage').forEach(st=>{if(!vis(st))return;const shown=el=>vis(el)&&!el.classList.contains('hidden');
    const L=[...st.querySelectorAll('.vw-lb,.vw-pin')].filter(shown).map(el=>({el,r:el.getBoundingClientRect()}));
    const O=[...st.querySelectorAll('.vw-stamp,.vw-disc,.vw-giz,.vw-scale')].filter(el=>shown(el)&&(el.textContent.trim()||el.tagName==='CANVAS')).map(el=>({el,r:el.getBoundingClientRect()}));
    for(let i=0;i<L.length;i++){for(let j=i+1;j<L.length;j++)if(ov(L[i].r,L[j].r))out.push({kind:'stage-collide',what:name(L[i].el)+'  ⟷  '+name(L[j].el)});
      for(const o of O)if(ov(L[i].r,o.r))out.push({kind:'stage-collide',what:name(L[i].el)+'  ⟷  '+name(o.el)});}});
  // 13. no-scroll-cue: a side panel that scrolls, with content hidden below and no visible "More ↓" cue
  root.querySelectorAll('.vw-panel,[data-cue]').forEach(p=>{if(!vis(p))return;const s=getComputedStyle(p);if(!/(auto|scroll)/.test(s.overflowY))return;
    if(p.scrollHeight-p.clientHeight>8&&p.scrollTop+p.clientHeight<p.scrollHeight-8){const c=p.querySelector(':scope>.cue');if(!(c&&vis(c)))out.push({kind:'no-scroll-cue',what:name(p)+' hides '+Math.round(p.scrollHeight-p.clientHeight-p.scrollTop)+'px below with no cue'});}});
  return out;
}
