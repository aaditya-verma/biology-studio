/* Biology Studio — settings that code reads (RULES I6). Owner doc: build/design-plan.md §6. EDIT: values here, not in code. */
'use strict';
const CONFIG={
  book:'E',                                   // EDIT: book code (README) — every content path is under it
  mapUrl:'content/E/map.json',                // EDIT: K1 map data
  idb:{name:'biostudio',ver:1,stores:['state','answers','files']},   // D-019; add stores only (A1)
  saveDelayMs:400,                            // debounce between a change and the write
  saveLogMax:20,
  keys:{theme:'biostudio.theme',slog:'biostudio.savelog',flags:'biostudio.flags',stash:'biostudio.stash'},
  nav:['today','cards','map','scene','settings'],             // EDIT: order of the main nav
  navTest:['studio','progress'],                      // EDIT: nav items shown only in testing mode (S1 Studio, W1 progress map — #progress still opens without it)
  routes:['today','lessons','lesson','mix','cards','card','deck','map','concept','x','scene','day','settings','colours','studio','calib','progress','step','review','rcard','rtour','updates'],   // first key of the hash; see src/js/05-router.js
  home:'today',
  leaveWindowMs:2000,                         // Android Back at home: a second press within this leaves
  // device classes (§8a): short side < phone ⇒ phone; < tablet ⇒ tablet; desktop needs ≥ 1024 wide + fine pointer
  device:{phone:600,tablet:1024},
  xt:{x:'layer',y:'day'},                     // default crosstab
  debugAreas:['map','viewer','layout','store','router','device','test','studio','tracker','learn','review','lessons'],
  navReview:'review',                         // EDIT (H2): nav item added after Cards once Reviewer mode is on (not in testing mode — its nav is full)
  // EDIT: 3D viewer (V1; design plan §2 3D row, RULES H8). Budgets stay "Expected" until pipeline reference §2 is Measured (C4).
  viewer:{
    scenesUrl:'content/E/scenes/',            // EDIT: scene files (docs/scene-spec.md)
    engine:'src/js/14-scene3d.mjs',           // loaded on first open (three.js r170 in lib/three-r170/)
    dprCap:2,                                 // §2 rule 7
    turn:{az:15,el:12}, lostMs:1500, drillShift:0.1, pinOffset:12, frame:{padTop:30,pad:8,pin:34,maxIn:2.5,traceMaxIn:4,trace:26,cellGap:11},   // frame (L1F): room kept around the embryo + ruler when a drill frames itself (px; padTop fits the ruler's '1 mm' label; pin = room around each pinned structure in a label drill)
      // EDIT (V2): drill turn buttons (°), wait before 'The 3D stopped', drill framing (share of the stage height), pin offset (px)
    still:{w:360,h:240}, tolDefault:25,       // EDIT (V2): drill stills (px), rotate tolerance when a card sets none (card-spec §2a)
    budget:{phoneTris:150000,phoneFps:30},    // H8 until Measured
    scaleSteps:[0.01,0.02,0.05,0.1,0.2,0.5,1,2,5],   // mm — scale bar picks the largest that fits 130 px
    secPerDay:2.5,                            // Play speed (full motion)
    stepMs:1600,                              // Play with reduced motion: jump key to key
    tweenMs:450,                              // view preset camera move (0 with reduced motion)
    measure:{phaseMs:4000,warmFrames:10,orbitDegPerS:20,stress:[50000,150000,300000]}   // ?debug=viewer › Measure fps
  },
  // EDIT: progress map (W1, D-040) — read live from the deployed repo (GitHub Pages serves the repo root; .nojekyll keeps .md raw)
  tracker:{
    steps:'studio-docs/build/steps.json', status:'studio-docs/claude/STATUS.md', plan:'studio-docs/build/master-plan.md', backlog:'studio-docs/build/ideas-backlog.md',
    repo:'https://github.com/aaditya-verma/biology-studio/blob/main/'   // EDIT: links to D-ids, checklist (open in GitHub)
  },
  // EDIT: cards + Studio (S1; docs/card-spec.md). Studio is testing mode only (?test=1) — nothing it does is saved; export the JSON and commit it.
  cards:{
    dir:'content/E/cards/',                   // card files + index.json + calibration.json
    sources:'content/E/sources.json',
    fixtures:{'E05.02.01':'tools/layout-check/fixtures/E05.02.01-drills.json'},   // EDIT: testing-only demo cards (?test=1&fixture=drills) — all five drill types; never shown to learners         // derived by tools/card-check --write-sources (registry, decisions, sections, terms)
    checkDelayMs:250,                         // live card-check after typing
    roles:['Lead scientist','Research librarian','Learning designer','Story director / writer','Art director','QA & accessibility','Owner']   // playbook §1
  },
  // EDIT: learning core (L1; docs/card-spec.md §7, design plan §4.8). Statuses Read → Understood → Can explain (B4).
  learn:{
    show:['reviewed','shipped'],              // card statuses a learner sees (testing mode also shows drafts)
    levels:['general','mbbs'],                // level toggle order; a card's optional levels (school, neet, pg) join when it has them
    level:'general',                          // default level for a new save
    deckDays:[1,3,7],                         // Remember deck spacing in days: step 0 → +1 d, 1 → +3 d, 2+ → +7 d (master plan §9 lists 21/60 later)
    deckSession:20,                           // most prompts in one deck session
    readMs:1500,                              // a card counts as Read after it has been open this long
    groups:['E00','E05','E06','E07','E08'],   // EDIT: card list order (chapters with cards)
    // EDIT (L2, D-070; docs/lesson-spec.md): the chapter path — one lesson per chapter in content/<book>/lessons/<ch>.json, in this order
    lessons:['E00','E05','E06','E07','E08'],
    lessonDir:'content/E/lessons/',
    mix:{n:8,minCards:4,minChapters:2,perCard:2,restDays:1,keep:60,recallDays:30,types:['mcq','order']}   // Mixed review (IB03): questions per run · Understood cards + chapters needed · most questions per card · prefer cards Understood ≥ restDays ago · runs kept · recall window · Check types asked (drills stay on their card)
  },
  // EDIT (L2): Today plans (IB01; design plan §4.1) — On the go ≤ 5 min · Study 15–30 min
  today:{goPrompts:8,promptS:15,checkS:120,goMax:5,studyMin:15,studyMax:30},   // checkS = the estimate for one Check
  // EDIT: Reviewer mode (H2, D-060/D-061; design plan §4.10). The human science reviewer reads cards, ticks a plain checklist and sends
  // ✓ / ✎ / ? as a pre-filled GitHub Issue Form; My feedback reads her issues back from the public API (no token; 60 calls an hour per network).
  review:{
    name:'Komal',                             // EDIT: how the home greets the reviewer
    login:'komalverma00500-byte',             // EDIT: the reviewer's GitHub username (public) — My feedback lists issues she opened
    owner:'Aaditya',                          // who decides on a fix (D-060)
    repo:'aaditya-verma/biology-studio',
    api:'https://api.github.com/repos/aaditya-verma/biology-studio/issues',
    newIssue:'https://github.com/aaditya-verma/biology-studio/issues/new',
    form:'card-review.yml', formOther:'other-feedback.yml',   // .github/ISSUE_TEMPLATE/ — field ids must match REVIEW_FIELDS in 19-review.js
    label:'review', fixingLabel:'fixing',     // the forms add `review`; the owner adds `fixing` when he agrees to a fix; a closed issue with milestone vN = fixed in vN
    refreshMs:300000, maxUrl:7000,           // maxUrl: the form link stays under ~7 KB (the note is shortened past it)
                            // check GitHub at most every 5 min on its own (Check for news always asks)
    show:['reviewed','shipped'],              // cards under To review; drafts are listed below, folded
    updatesUrl:'studio-docs/logs/build-log.md',   // #updates reads the plain line <!--plain: …--> of each log entry (else its title)
    updatesShow:6, updatesPage:20,            // updates on What's new; per page on #updates
    fixture:'tools/layout-check/fixtures/review-issues.json'   // ?test=1&fixture=review: demo issues (every state + a rate-limit case) instead of GitHub
  }
};
