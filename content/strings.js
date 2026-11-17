/* Biology Studio — every UI word in one place (RULES I6). Owner doc: build/design-plan.md §5.
   EDIT: change words here only; code reads STR.<key>. Keep labels short (phone first). */
'use strict';
const STR={
  app:'Biology Studio',
  nav:{today:'Today',map:'Book map',settings:'Settings'},
  navHint:{today:'Where to start and what is next',map:'Every concept in the book, mapped',settings:'Theme, storage, backup, colour key'},
  back:'Back', up:'Up', close:'Close', search:'Search', clear:'Clear', all:'All', none:'—',
  leaveHint:'Press Back again to leave Biology Studio',
  testFlag:'Testing mode — nothing is saved', testShort:'✎ test',
  // Today
  todayTitle:'Today',
  todayLead:'The app grows step by step. Right now you can explore the whole book map; cards, 3D and episodes arrive in the next builds.',
  continueT:'Continue', continueNone:'Nothing opened yet. Start with Part 0, then gastrulation.',
  startT:'Start here', startPart0:'Part 0 · Reading an embryo', startGastr:'Ch 5 · Gastrulation (researched ✔)',
  mapStatsT:'The book, mapped', concepts:'concepts', chapters:'chapters', researched:'researched (X1)',
  comingT:'Coming next', coming:['3D viewer with a day scrubber (V1)','Concept cards with Checks (C1)','Episode S1E01 · Gastrulation (P1)','Remember deck + On the go / Study (L1)'],
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
  // Settings
  settingsTitle:'Settings', themeT:'Theme', themes:{system:'Device',light:'Light',dark:'Dark'},
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
