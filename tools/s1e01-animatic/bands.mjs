/* S1E01 animatic — every on-screen position in one place (RULES I6). Owner doc: visual-style §1 (Short, with patches/visual-style-s1.md = M1b.q10 B), §10 (Lesson).
   Numbers are % of the frame. EDIT here only. */
export const BANDS = {
  short: { title: [15, 21], stamp: [22, 24], axes: [28, 34], tag: [34.5, 37.5], subject: [38, 64], caption: [68, 72], capMaxW: 70, capTop: 64, left: 4, right: 14, blockW: 30, ui: 75 },
  lesson: { stackBottom: 84, caption: [85, 95], capMaxW: 90, safe: 5, subject: [14, 80] },
};
export const MIN_PX = { caption: 12, label: 11, tag: 10.5 };   // smallest text on small frames
