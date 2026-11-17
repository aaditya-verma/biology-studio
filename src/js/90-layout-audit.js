/* Biology Studio — layout audit (RULES C8 + C13), run by tools/layout-check on every size and by ?debug=layout (button in the overlay).
   Ported from DrumPath v36 14-layout-check.js, plus tap size, text size and fixed-over-controls. Owner doc: build/design-plan.md §7.
   Checks the current screen: overlap · spill · page-wider · tap < --tap · text < --fs-min · fixed/sticky bars covering a control.
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
  ctrls.forEach(el=>{const r=el.getBoundingClientRect();if(el.closest('.sr'))return;if(r.width+0.5<Math.min(TAP,W)||r.height+0.5<TAP){const inline=getComputedStyle(el).display==='inline'&&el.tagName==='A';if(!inline)issues.push({kind:'tap-small',what:name(el)+' '+Math.round(r.width)+'×'+Math.round(r.height)+' < '+TAP});}});
  // 4b. a control pushed past the side of its own pane or card (hidden or needing a sideways scroll there); tables meant to scroll are fine
  ctrls.forEach(el=>{if(el.closest('.xt-wrap,.seg'))return;const r=el.getBoundingClientRect();for(let p=el.parentElement;p&&p!==document.body;p=p.parentElement){const s=getComputedStyle(p);
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
  return issues;
}
