/* Biology Studio — device + input classes (§8a, RULES C13). Owner doc: build/design-plan.md §2.
   Sets one of dev-p / dev-pl / dev-tp / dev-tl / dev-d and in-touch / in-mouse on <html>, on load, rotate and resize.
   Changing class never re-renders or reloads: layouts switch in CSS, so place (scroll, open pane, route) is kept. */
'use strict';
const DEV={cls:'',input:'',listeners:[]};
function deviceClass(w,h,fine){  // pure, so the tests and tools/layout-check can call it
  const short=Math.min(w,h),land=w>h,C=CONFIG.device;
  if(short<C.phone)return land?'dev-pl':'dev-p';
  if(w>=C.tablet&&fine)return 'dev-d';            // ≥ 1024 wide with a mouse/trackpad
  if(short<C.tablet)return land?'dev-tl':'dev-tp';
  return land?(fine?'dev-d':'dev-tl'):'dev-tp';   // big touch screens stay tablet
}
function deviceApply(){
  const fine=matchMedia('(pointer: fine)').matches,hover=matchMedia('(hover: hover)').matches;
  const cls=deviceClass(innerWidth,innerHeight,fine),input=fine&&hover?'in-mouse':'in-touch',h=document.documentElement;
  if(cls===DEV.cls&&input===DEV.input)return;
  h.classList.remove('dev-p','dev-pl','dev-tp','dev-tl','dev-d','in-mouse','in-touch');h.classList.add(cls,input);
  const was=DEV.cls;DEV.cls=cls;DEV.input=input;dlog('device',was||'start','→',cls,input,innerWidth+'×'+innerHeight);
  DEV.listeners.forEach(f=>{try{f(cls,was);}catch(e){console.error(e);}});
}
const onDevice=f=>DEV.listeners.push(f);
let devT=0;addEventListener('resize',()=>{clearTimeout(devT);devT=setTimeout(deviceApply,80);});
try{matchMedia('(pointer: fine)').addEventListener('change',deviceApply);screen.orientation&&screen.orientation.addEventListener('change',deviceApply);}catch(_){}
