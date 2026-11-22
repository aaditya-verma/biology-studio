/* Biology Studio — device + input classes (§8a, RULES C13). Owner doc: build/design-plan.md §2 (class rule, D-087).
   Sets one of dev-p / dev-pl / dev-tp / dev-tl / dev-d, in-touch / in-mouse and (split screen) in-split on <html>, on load, rotate and resize.
   U2 part 2 (D-087): on touch, phone vs tablet comes from the SCREEN's short side (system bars, page zoom and split screen shrink the window,
   not the device); orientation comes from the window. Changing class never re-renders or reloads: layouts switch in CSS, so place is kept. */
'use strict';
const DEV={cls:'',input:'',split:false,sw:0,sh:0,listeners:[]};
function deviceClass(w,h,fine,sw,sh){  // pure, so the tests and tools/layout-check can call it · w,h = window · sw,sh = screen (default: the window)
  const C=CONFIG.device,land=w>h,win=Math.min(w,h);
  if(fine){   // a mouse/trackpad: desktop windows resize freely, so the window decides (unchanged from A0)
    if(w>=C.tablet)return 'dev-d';
    if(win<C.phone)return land?'dev-pl':'dev-p';
    return land?'dev-tl':'dev-tp';}
  const scr=Math.min(sw||w,sh||h);   // EDIT: CONFIG.device.phone — the screen's short side below it = a phone
  if(scr<C.phone)return land?'dev-pl':'dev-p';
  return land?'dev-tl':'dev-tp';   // every touch screen ≥ phone is a tablet (big touch screens too)
}
function deviceSplit(w,h,fine,sw,sh){  // pure: a tablet window much smaller than its screen (split screen / pop-up window) — compact chrome, never a phone
  if(fine||!sw||!sh||Math.min(sw,sh)<CONFIG.device.phone)return false;
  if((w>h)!==(sw>sh))[sw,sh]=[sh,sw];   // G-Eng: iOS/iPadOS keep screen.* in portrait — compare with the screen turned to the window's orientation
  return w<CONFIG.device.splitW*sw||h<CONFIG.device.splitH*sh;}   // EDIT: CONFIG.device.splitW / splitH
function deviceApply(){
  const fine=matchMedia('(pointer: fine)').matches,hover=matchMedia('(hover: hover)').matches;const sw=screen.width||innerWidth,sh=screen.height||innerHeight;
  const cls=deviceClass(innerWidth,innerHeight,fine,sw,sh),input=fine&&hover?'in-mouse':'in-touch',split=deviceSplit(innerWidth,innerHeight,fine,sw,sh),h=document.documentElement;
  DEV.sw=sw;DEV.sh=sh;
  h.classList.toggle('big-text',parseFloat(getComputedStyle(h).fontSize)>=28&&innerHeight<700);   // G-Art (D-087): ≥ 175 % text on a short window — the full viewer stacks its panel (EDIT: 28 px, 700 px)
  if(cls===DEV.cls&&input===DEV.input&&split===DEV.split)return;
  h.classList.remove('dev-p','dev-pl','dev-tp','dev-tl','dev-d','in-mouse','in-touch');h.classList.add(cls,input);h.classList.toggle('in-split',split);
  const was=DEV.cls;DEV.cls=cls;DEV.input=input;DEV.split=split;dlog('device',was||'start','→',cls,input,devLine());
  DEV.listeners.forEach(f=>{try{f(cls,was);}catch(e){console.error(e);}});
}
const devLine=()=>DEV.cls+' · screen '+DEV.sw+'×'+DEV.sh+' · window '+innerWidth+'×'+innerHeight+(DEV.split?' · split':'');   // overlay + Settings › Version (D-087)
const onDevice=f=>DEV.listeners.push(f);
let devT=0;addEventListener('resize',()=>{clearTimeout(devT);devT=setTimeout(deviceApply,80);});
addEventListener('DOMContentLoaded',()=>deviceApply());addEventListener('load',()=>deviceApply());   // the text size is known only after styles load (big-text flag)
try{matchMedia('(pointer: fine)').addEventListener('change',deviceApply);screen.orientation&&screen.orientation.addEventListener('change',deviceApply);}catch(_){}
