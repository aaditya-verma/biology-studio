/* Biology Studio — every UI word in one place (RULES I6). Owner doc: build/design-plan.md §5.
   EDIT: change words here only; code reads STR.<key>. Keep labels short (phone first). */
'use strict';
const STR={
  app:'Biology Studio',
  nav:{today:'Today',map:'Book map',scene:'3D',settings:'Settings'},
  navHint:{today:'Where to start and what is next',map:'Every concept in the book, mapped',scene:'3D scenes: turn, scrub the days, slice',settings:'Theme, motion, storage, backup, colour key'},
  back:'Back', up:'Up', close:'Close', search:'Search', clear:'Clear', all:'All', none:'—',
  leaveHint:'Press Back again to leave Biology Studio',
  testFlag:'Testing mode — nothing is saved', testShort:'✎ test',
  // Today
  todayTitle:'Today',
  todayLead:'The app grows step by step. Right now you can explore the whole book map and the first 3D scenes; cards and episodes arrive in the next builds.',
  continueT:'Continue', continueNone:'Nothing opened yet. Start with Part 0, then gastrulation.',
  startT:'Start here', startPart0:'Part 0 · Reading an embryo', startGastr:'Ch 5 · Gastrulation (researched ✔)', start3d:'3D · Two layers become three',
  mapStatsT:'The book, mapped', concepts:'concepts', chapters:'chapters', researched:'researched (X1)',
  comingT:'Coming next', coming:['Concept cards with Checks (C1)','Episode S1E01 · Gastrulation (P1)','Remember deck + On the go / Study (L1)'],
  // Book map
  mapTitle:'Book map', tree:'Chapters', chapterView:'Chapter', crosstab:'Crosstab', unlocks:'Unlocks most',
  searchPh:'Search…', searchLabel:'Search concepts, terms, ids', filters:'Filters', clearFilters:'Clear filters',
  rows:'Rows', cols:'Columns', swap:'Swap', cellHint:'Each number counts concepts; tap a cell to list them.',
  shown:(n,t)=>`${n} of ${t} concepts`,
  pickConcept:'Pick a concept to see its page.', pickChapter:'Pick a chapter, or open a crosstab.',
  where:'Where', day:'Day', stage:'Stage', needs:'Needs first', unlocksT:'Unlocks', related:'Related', showsUp:'Shows up in', terms:'Glossary terms',
  an:'NMC AN', markT:'Confidence', cardEp:'Card · episode', planned:'planned', mixup:'Common mix-up:', notRight:'— not right.',
  approx:'≈ not yet cited', cited:'cited (X1)', locator:'locator',
  parts:['Part 0 · Orientation','Part 1 · General embryology','Part 2 · Systems-based embryology'],
  marks:{'✔✔':'book + Tier 1 source agree','✔':'book only','⚑':'book vs newer evidence — see More','✚':'beyond the book','≈':'not yet cited'},
  markShort:{'✔✔':'agreed','✔':'book','⚑':'check','✚':'beyond','≈':'uncited'},
  tierShort:t=>'Tier '+t, threadShort:(t,l)=>l?l.split(/[ ,(]/)[0]:'Thread '+t,
  conceptPane:'Concept', noConcept:id=>'No concept '+id+'.', badXt:'Unknown crosstab.', inAll:n=>n+' build on it in all',
  // 3D viewer (V1)
  vw:{title:'3D scene', listTitle:'3D scenes', listLead:'Turn the embryo, scrub through the days and slice it. Each scene says its day, stage and size, and where every fact comes from.',
    open:'Open in 3D', all:'All 3D scenes', loading:'Loading…', loading3d:'Starting 3D…', loadFail:'Could not load the 3D scenes',
    noScene:id=>'No scene '+id+'.', noGL:'3D needs WebGL, which this browser has turned off. The facts are still under About.',
    stageLabel:t=>'3D view: '+t+'. Drag to turn, pinch or scroll to zoom.', controls:'3D controls', sections:'Control sections',
    dayGroup:'Day', day:'Day', dayPrev:'One day back', dayNext:'One day on', play:'Play the days', pause:'Pause',
    dayShort:d=>'d'+d, dayLong:d=>'Day '+d, daysRange:d=>'Days '+d[0]+'–'+d[1],
    tabs:{layers:'Layers',cut:'Cut',view:'View',about:'About',debug:'Debug'},
    heads:{layers:'Layers',cut:'Labels & cut',view:'View',about:'About this scene',debug:'Debug'},
    labels:'Labels', cut:'Cut', cutAxis:'Cut direction', cutAxes:{x:'Cross-section',y:'Lengthwise'}, cutAt:'Cut position',
    views:{three:'3/4 view',top:'From the back',side:'From the side',cut:'Face the cut',reset:'Reset'},
    zoom:'Zoom', zoomIn:'Zoom in', zoomOut:'Zoom out',
    hintMouse:'Drag to turn · scroll to zoom · hover to name a structure · keys: [ ] day, Space play, arrows turn, + − zoom, 0 reset, L labels, C cut.',
    hintTouch:'Drag to turn · pinch to zoom · double-tap to reset.',
    gizmo:'Axis key: Cr cranial (head), Cd caudal (tail), D dorsal (back), V ventral (belly), L left, R right of the embryo.',
    axes:{cranial:'Cranial',caudal:'Caudal',dorsal:'Dorsal',ventral:'Ventral',left:'Left',right:'Right'},
    mm:m=>(m<0.1?(m*1000)+' µm':m+' mm'), cardsT:'Cards:', marksKey:'Marks: ✔✔ book + Tier 1 source agree · ✔ book only · ⚑ disagree (logged) · ✚ beyond the book · ≈ not yet cited.',
    tech:(r,g)=>'three.js r'+r+' · '+g, labelsShown:a=>a.length?'Labels on screen: '+a.join(', ')+'.':'',
    measure:'Measure fps (~30 s)', boxes:'Bounding boxes', measOut:'Measurement results', measHint:'Plays every scene, then adds 50k, 150k and 300k test triangles. Keep the screen on; then Copy and paste the result into the chat.',
    measuring:n=>'Measuring '+n+'…', measDone:'Done — tap Copy and paste this into the chat.',
    discLine:d=>d.slice(0,2).join(' · ')+(d.length>2?' · +'+(d.length-2)+' more':''), discT:'Simplified on purpose', termsT:'Terms (conventions, not book facts)',
    cutText:(axis,at)=>'Cut at '+Math.round((at+1)*50)+' % from the '+(axis==='x'?'caudal end':'right side'),
    viewText:(az,el,cut)=>{const a=((az%360)+540)%360-180,side=Math.abs(a+90)<45?'the right side':Math.abs(a-90)<45?'the left side':Math.abs(a)<45?'the head end':'the tail end';
      return 'Viewed from '+(el>70?'the back (dorsal)':el<-70?'the belly (ventral)':side+(el>20?', from above':el<-20?', from below':''))+(cut&&cut.on?'; cut '+(cut.axis==='x'?'across':'lengthwise'):'')+'.';}},
  // Settings
  settingsTitle:'Settings', themeT:'Theme', themes:{system:'Device',light:'Light',dark:'Dark'},
  motionT:'Motion', motions:{system:'Device',reduce:'Reduce',full:'Full'}, motionHint:'Reduce = no smooth camera moves; Play jumps from key day to key day.',
  storageT:'Storage', saved:'Saved on this device', savedTest:'Testing mode: nothing is written', rev:'revision', saveLog:'Save log (this device, last 20)',
  backupT:'Backup', exportB:'Export backup', importB:'Import backup', importOk:'Backup merged.', importBad:'That file is not a Biology Studio backup.', importNewer:'That backup is from a newer app version — update the app first.',
  exportHint:'Tap Export backup before any update that touches saved data (RULES A3).',
  testT:'Testing mode', testOn:'Turn on testing mode', testOff:'Turn off testing mode', testHint:'Shows ✎ edit hooks and the debug overlay. Nothing is saved while it is on.',
  colourKeyT:'Colour key', colourKeyHint:'The germ-layer colours, each with its pattern and label, checked on this screen.',
  versionT:'Version',
  // Colour key
  ckTitle:'Colour key', ckLead:'Every layer has a colour, a pattern and a label — colour is never the only cue. Numbers are measured on this screen now.',
  ckLayers:{epi:'Epiblast',hypo:'Hypoblast',ecto:'Ectoderm',meso:'Mesoderm',endo:'Endoderm',crest:'Neural crest',ctx:'Context (non-layer tissue)'},
  ckPattern:{epi:'open rings',hypo:'vertical lines',ecto:'dots',meso:'diagonal lines',endo:'horizontal lines',crest:'cross-hatch',ctx:'speckle'},
  ckAccent:'Accent — "look here": a ring + label, never a layer colour', ckEdge:'edge', ckFill:'fill', ckText:'label text', ckRing:'ring', ckBtnText:'button text',
  // edit hook dialog
  editT:'Edit this', editChat:'Paste into a new chat named', copy:'Copy prompt', copied:'Copied.', copyFail:'Select the text and copy it by hand.',
  // errors
  loadFail:'Could not load the book map', drawFail:'Something went wrong drawing this page.'
};
