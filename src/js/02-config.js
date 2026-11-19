/* Biology Studio — settings that code reads (RULES I6). Owner doc: build/design-plan.md §6. EDIT: values here, not in code. */
'use strict';
const CONFIG={
  book:'E',                                   // EDIT: book code (README) — every content path is under it
  mapUrl:'content/E/map.json',                // EDIT: K1 map data
  idb:{name:'biostudio',ver:1,stores:['state','answers','files']},   // D-019; add stores only (A1)
  saveDelayMs:400,                            // debounce between a change and the write
  saveLogMax:20,
  keys:{theme:'biostudio.theme',slog:'biostudio.savelog',flags:'biostudio.flags',stash:'biostudio.stash'},
  nav:['today','map','scene','settings'],             // EDIT: order of the main nav
  navTest:['studio'],                                 // EDIT: nav items shown only in testing mode (S1 Studio)
  routes:['today','map','concept','x','scene','day','settings','colours','studio','calib'],   // first key of the hash; see src/js/05-router.js
  home:'today',
  leaveWindowMs:2000,                         // Android Back at home: a second press within this leaves
  // device classes (§8a): short side < phone ⇒ phone; < tablet ⇒ tablet; desktop needs ≥ 1024 wide + fine pointer
  device:{phone:600,tablet:1024},
  xt:{x:'layer',y:'day'},                     // default crosstab
  debugAreas:['map','viewer','layout','store','router','device','test'],
  // EDIT: 3D viewer (V1; design plan §2 3D row, RULES H8). Budgets stay "Expected" until pipeline reference §2 is Measured (C4).
  viewer:{
    scenesUrl:'content/E/scenes/',            // EDIT: scene files (docs/scene-spec.md)
    engine:'src/js/14-scene3d.mjs',           // loaded on first open (three.js r170 in lib/three-r170/)
    dprCap:2,                                 // §2 rule 7
    budget:{phoneTris:150000,phoneFps:30},    // H8 until Measured
    scaleSteps:[0.01,0.02,0.05,0.1,0.2,0.5,1,2,5],   // mm — scale bar picks the largest that fits 130 px
    secPerDay:2.5,                            // Play speed (full motion)
    stepMs:1600,                              // Play with reduced motion: jump key to key
    tweenMs:450,                              // view preset camera move (0 with reduced motion)
    measure:{phaseMs:4000,warmFrames:10,orbitDegPerS:20,stress:[50000,150000,300000]}   // ?debug=viewer › Measure fps
  },
  // EDIT: cards + Studio (S1; docs/card-spec.md). Studio is testing mode only (?test=1) — nothing it does is saved; export the JSON and commit it.
  cards:{
    dir:'content/E/cards/',                   // card files + index.json + calibration.json
    sources:'content/E/sources.json',         // derived by tools/card-check --write-sources (registry, decisions, sections, terms)
    checkDelayMs:250,                         // live card-check after typing
    roles:['Lead scientist','Research librarian','Learning designer','Story director / writer','Art director','QA & accessibility','Owner']   // playbook §1
  }
};
