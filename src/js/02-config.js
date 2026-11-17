/* Biology Studio — settings that code reads (RULES I6). Owner doc: build/design-plan.md §6. EDIT: values here, not in code. */
'use strict';
const CONFIG={
  book:'E',                                   // EDIT: book code (README) — every content path is under it
  mapUrl:'content/E/map.json',                // EDIT: K1 map data
  idb:{name:'biostudio',ver:1,stores:['state','answers','files']},   // D-019; add stores only (A1)
  saveDelayMs:400,                            // debounce between a change and the write
  saveLogMax:20,
  keys:{theme:'biostudio.theme',slog:'biostudio.savelog',flags:'biostudio.flags',stash:'biostudio.stash'},
  nav:['today','map','settings'],             // EDIT: order of the main nav
  routes:['today','map','concept','x','settings','colours'],   // first key of the hash; see src/js/05-router.js
  home:'today',
  leaveWindowMs:2000,                         // Android Back at home: a second press within this leaves
  // device classes (§8a): short side < phone ⇒ phone; < tablet ⇒ tablet; desktop needs ≥ 1024 wide + fine pointer
  device:{phone:600,tablet:1024},
  xt:{x:'layer',y:'day'},                     // default crosstab
  debugAreas:['map','layout','store','router','device','test']
};
