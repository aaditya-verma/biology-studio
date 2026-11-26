# S1E01 Gastrulation — the one source of the brief, scripts and shot list (P1, Bio · Episode · S1E01 script).
# EDIT: lines live here; build.py renders the docs + JSON and runs the pipeline checks.
# Each line: id, shot, text (spoken, numbers as words), facts (card#fact or card#m<n>), new (terms first named here),
#            hold (s of silence after the line; reveals hold 1.5 s in Lessons, D-032).

WPM = 143  # Kokoro af_heart speed 0.66 (M1b.q6)

PROFILES = {
  "lesson": {"name": "MBBS Lesson", "frame": "16:9 (1920×1080 master, 1280×720 ship)", "level": "MBBS", "depth": "Tier A (+ ⚑ pointer)",
             "type": "Journey explainer", "length_target": [180, 330], "language": "English", "host": "Nani (H-a)"},
  "general": {"name": "General Lesson cut", "frame": "16:9 (same scenes, same cameras)", "level": "General", "depth": "Tier A core only",
              "type": "Journey explainer", "length_target": [100, 190], "language": "English", "host": "Nani (H-a)"},
  "short": {"name": "9:16 Short", "frame": "9:16 (1080×1920 master, 720×1280 ship)", "level": "General / pre-med", "depth": "one idea",
            "type": "Short (6 × 8 s)", "length_target": [44, 60], "language": "English", "host": "Nani (H-a)"},
}

# ---------------- MBBS Lesson ----------------
LESSON = [
  # Opener (no previous Part → no recap beats; visual-style §15 opener = the question)
  dict(id="L01", seg="Open", shot="S01", text="Two flat sheets of cells. One week later, three. How does that happen, and where does each new layer come from?", facts=[], hold=2.0, kind="question"),
  # "Meet the parts" primer (spec 2, D-107; P1F) — replaces the 5-s terms strip L02 (retired). Opens on the cold-open question; names + looks only.
  dict(id="L02b", seg="Open", shot="S02b", text="To answer that, meet three parts first.", facts=[], hold=0.3, kind="primer"),
  dict(id="L02c", seg="Open", shot="S02b", text="Germ layers: the three sheets of cells that every tissue is built from.", facts=["E00.01.04#f5"], new=["germ layers"], hold=0.4, kind="primer"),
  dict(id="L02d", seg="Open", shot="S02c", text="Primitive node: a low mound at the head end of the primitive streak.", facts=["E05.01.02#f2", "E00.01.01#f2"], new=["primitive node"], hold=0.4, kind="primer"),
  dict(id="L02e", seg="Open", shot="S02d", text="Notochord: a solid rod of cells along the midline.", facts=["E05.02.01#f3", "E05.02.01#f1", "E05.02.01#f4"], new=["notochord"], hold=2.0, kind="primer"),
  # Segment 1 — The groove
  dict(id="L03", seg="1 The groove", shot="S03", text="This is the disc at the very start of week three. Its upper layer, from week two, is the epiblast.", facts=["E05.01.04#f1"], hold=1.0),
  dict(id="L04", seg="1 The groove", shot="S03", text="In week three the disc makes three germ layers: ectoderm, mesoderm and endoderm. That process is gastrulation.", facts=["E05.01.01#f1"], hold=1.5),
  dict(id="L05", seg="1 The groove", shot="S04", text="Gastrulation starts when the primitive streak appears on the epiblast, around days fourteen to fifteen.", facts=["E05.01.01#f2"], hold=1.0),
  dict(id="L06", seg="1 The groove", shot="S04", text="The streak first shows as a faint line in the caudal midline. By days fifteen to sixteen it is a narrow groove with raised edges.", facts=["E05.01.02#f1"], hold=1.5),
  dict(id="L07", seg="1 The groove", shot="S05", text="Its cranial end is a low mound, with a small pit at its centre. Keep an eye on it.", facts=["E05.01.02#f2"], hold=1.5),
  dict(id="L08", seg="1 The groove", shot="S06", text="The streak also marks the body's long axis. It lies at the tail end; the head end is the opposite end.", facts=["E05.01.02#f3"], hold=1.5),
  # Segment 2 — The dive (Journey: one marked epiblast cell)
  dict(id="L09", seg="2 The dive", shot="S07", text="Back to day fifteen. Let's follow one epiblast cell. We have marked it.", facts=[], hold=1.0, kind="frame"),
  dict(id="L10", seg="2 The dive", shot="S08", text="Epiblast cells move toward the streak, change shape, let go of their neighbours and slip underneath. This inward move is called invagination.", facts=["E05.01.03#f1"], new=["invagination"], hold=1.5),
  dict(id="L11", seg="2 The dive", shot="S09", text="The first cells in push into the hypoblast and replace it, forming the embryo's endoderm.", facts=["E05.01.03#f2"], hold=1.0),
  dict(id="L12", seg="2 The dive", shot="S09", text="So the hypoblast does not turn into endoderm. Epiblast cells take its place.", facts=["E05.01.01#m1"], hold=1.5),
  dict(id="L13", seg="2 The dive", shot="S10", text="Our cell goes in later. It settles between the epiblast and the new endoderm, as mesoderm.", facts=["E05.01.03#f3"], hold=1.5),
  dict(id="L14", seg="2 The dive", shot="S11", text="Mesoderm spreads sideways and toward the head.", facts=["E05.01.03#f4"], hold=1.5),
  dict(id="L15", seg="2 The dive", shot="S12", text="Cells that stay in the epiblast become ectoderm.", facts=["E05.01.03#f5"], hold=1.5),
  dict(id="L16", seg="2 The dive", shot="S13", text="Cut across the disc. Ectoderm is the top layer. Mesoderm is the middle layer. Endoderm is the bottom layer, facing the yolk sac.", facts=["E00.01.04#f2", "E00.01.04#f3", "E00.01.04#f4"], new=["yolk sac"], hold=2.0),
  dict(id="L17", seg="2 The dive", shot="S13", text="So all three germ layers come from the epiblast. The epiblast is not the ectoderm; ectoderm is only the part it leaves behind.", facts=["E05.01.04#f4", "E05.01.01#m3"], hold=2.0),
  # Segment 3 — The rod, and what is left
  dict(id="L18", seg="3 The rod", shot="S14", text="Our cell is out in the mesoderm now. Back to day sixteen, at that mound: the primitive node.", facts=["E05.01.02#f2"], hold=1.5),
  dict(id="L18b", seg="3 The rod", shot="S14", text="One stream of cells does something different there. Cells entering at the node move straight forward in the midline, toward the head end.", facts=["E05.02.01#f1"], hold=1.5),
  dict(id="L19", seg="3 The rod", shot="S15", text="For a short time they sit within the endoderm, as a flat plate.", facts=["E05.02.01#f2"], hold=1.0),
  dict(id="L20", seg="3 The rod", shot="S15", text="Then the plate lifts off the endoderm and rolls into a solid rod: the notochord.", facts=["E05.02.01#f3"], hold=1.5),
  dict(id="L21", seg="3 The rod", shot="S16", text="In the book, its head end forms first, by about day seventeen, and tail parts are added as the streak moves back.", facts=["E05.02.01#f4"], hold=1.0),
  dict(id="L22", seg="3 The rod", shot="S16", text="Newer human data tell a different story. You'll find it on the notochord card.", facts=["E05.02.01#f6"], hold=1.5, kind="flag-pointer"),
  dict(id="L23", seg="3 The rod", shot="S17", text="The notochord lies in the midline and sends signals that help build the spine around it.", facts=["E05.02.01#f5"], hold=1.5),
  dict(id="L24", seg="3 The rod", shot="S18", text="In adults only bits of it remain, in the nucleus pulposus, at the core of each spinal disc, the cushion between the vertebrae. It does not become the vertebrae.", facts=["E05.02.01#f7", "E05.02.01#m1"], new=["nucleus pulposus"], hold=2.0),
  dict(id="L25", seg="3 The rod", shot="S19", text="And the mesoderm our cell joined goes on to build muscle, bone, connective tissue, the heart, vessels and blood.", facts=["E05.01.03#f6"], hold=2.0),
  # Clinical link slot (visual-style §14, 15–30 s, Lesson only)
  dict(id="L26", seg="Clinical link", shot="S20", text="Clinical link. Here, at day seventeen, the groove our cell went through is still adding cells. It keeps going until the end of week four, then shrinks fast and disappears.", facts=["E05.01.02#f4"], hold=1.0),
  dict(id="L27", seg="Clinical link", shot="S21", text="Leftover streak cells near the base of the spine can form a sacrococcygeal teratoma, the most common tumour in newborns.", facts=["E05.01.02#f5", "E05.01.02#f6"], new=["sacrococcygeal teratoma"], hold=1.0),
  dict(id="L28", seg="Clinical link", shot="S21", text="It holds tissue from all three germ layers, and it is often found on scans before birth.", facts=["E05.01.02#f7"], hold=1.5),
  # Close — payoff on the section view (D9), 2 Checks, teaser
  dict(id="L29", seg="Close", shot="S22", text="So, back to our question. Cells went in through the streak. The first replaced the hypoblast as endoderm, the next became mesoderm, and those left on top became ectoderm.", facts=["E05.01.03#f2", "E05.01.03#f3", "E05.01.03#f5"], hold=1.0),
  dict(id="L30", seg="Close", shot="S22", text="Three layers, all from the epiblast.", facts=["E05.01.04#f4"], hold=2.0),
  dict(id="L31", seg="Close", shot="S23", text="Two quick checks. On this section, tap the layer our cell joined.", facts=[], hold=4.0, kind="check", check="spatial: tap Mesoderm on the day-17 cross-section (answer from E05.01.03#f3)"),
  dict(id="L31a", seg="Close", shot="S23", text="The middle layer: mesoderm.", facts=["E05.01.03#f3"], hold=2.0, kind="reveal"),
  dict(id="L32", seg="Close", shot="S23", text="And the hypoblast: does it become endoderm, or is it replaced?", facts=[], hold=4.0, kind="check", check="E05.01.01 q2 (refutes m1), spoken choices; chips 'Becomes endoderm' / 'Is replaced'"),
  dict(id="L32a", seg="Close", shot="S23", text="It is replaced. Epiblast cells take its place; it does not become endoderm.", facts=["E05.01.01#m1"], hold=2.0, kind="reveal"),
  dict(id="L33", seg="Close", shot="S24", text="Next: how does this flat disc fold into a body?", facts=[], hold=1.0, kind="teaser"),
]

# ---------------- General Lesson cut ----------------
GENERAL = [
  dict(id="G01", seg="Open", shot="S01", text="Every tissue in your body traces back to one thin sheet of cells. So how does one sheet make three different layers?", facts=["E05.01.04#f4"], hold=2.0, kind="question"),
  # "Meet the parts" primer, everyday words (spec 2, D-107; P1F) — replaces the terms strip G02 (retired).
  dict(id="G02b", seg="Open", shot="S02e", text="To answer that, meet three parts first.", facts=[], hold=0.3, kind="primer"),
  dict(id="G02c", seg="Open", shot="S02e", text="The epiblast: the top layer, where we start.", facts=["E05.01.04#f1"], new=["epiblast"], hold=0.3, kind="primer"),
  dict(id="G02d", seg="Open", shot="S02e", text="The hypoblast: the bottom layer, under it.", facts=["E00.01.01#f4"], new=["hypoblast"], hold=0.3, kind="primer"),
  dict(id="G02e", seg="Open", shot="S02f", text="The primitive streak: a groove at the tail end.", facts=["E05.01.02#f1", "E05.01.02#f3"], new=["primitive streak"], hold=2.0, kind="primer"),
  dict(id="G03", seg="1 The groove", shot="S03", text="This tiny disc is an embryo, about two weeks old. It has two layers. The upper one is the epiblast, our starting layer.", facts=["E05.01.04#f1"], hold=1.0),
  dict(id="G04", seg="1 The groove", shot="S04", text="In week three a groove appears on that starting layer, at the tail end. This is the primitive streak.", facts=["E05.01.01#f1", "E05.01.01#f2", "E05.01.02#f1", "E05.01.02#f3"], hold=1.5),
  dict(id="G05", seg="1 The groove", shot="S06", text="The head will form at the other end, so the streak marks which way is head and which way is tail.", facts=["E05.01.02#f3"], hold=1.5),
  dict(id="G06", seg="2 The dive", shot="S07", text="Let's go back a day and follow one cell from the starting layer. We have marked it.", facts=[], hold=1.0, kind="frame"),
  dict(id="G07", seg="2 The dive", shot="S08", text="Cells move toward the groove, let go of their neighbours and slip underneath. Think of a crowd filing down a narrow ramp, then spreading out in the thin gap between two floors. Unlike a ramp, the groove is made of the cells themselves.", facts=["E05.01.03#f1"], hold=1.5, kind="analogy"),
  dict(id="G08", seg="2 The dive", shot="S09", text="The first cells in push the old bottom layer, the hypoblast, aside and take its place. They become the new bottom layer.", facts=["E05.01.03#f2"], hold=1.5),
  dict(id="G09", seg="2 The dive", shot="S10", text="Our cell goes in later. It settles in between, in a new middle layer.", facts=["E05.01.03#f3"], hold=1.5),
  dict(id="G10", seg="2 The dive", shot="S11", text="The middle layer spreads out to the sides and toward the head.", facts=["E05.01.03#f4"], hold=1.0),
  dict(id="G11", seg="2 The dive", shot="S12", text="Cells that stay behind on top become the new top layer. This new top layer is only part of the starting layer.", facts=["E05.01.03#f5", "E05.01.01#m3"], hold=1.5),
  dict(id="G12", seg="2 The dive", shot="S13", text="Cut across the disc, and there they are: ectoderm on top, mesoderm in the middle, endoderm at the bottom. These are the three layers, and making them is gastrulation.", facts=["E00.01.04#f2", "E00.01.04#f3", "E00.01.04#f4", "E05.01.01#f1"], new=["ectoderm", "mesoderm", "endoderm"], hold=2.0),
  dict(id="G13", seg="This becomes", shot="S19", text="The middle layer our cell joined goes on to build muscle, bone, the heart, vessels and blood.", facts=["E05.01.03#f6"], hold=2.0),
  dict(id="G14", seg="Close", shot="S22", text="So, one sheet became three, because cells dived in through the streak. All three layers come from that one starting layer.", facts=["E05.01.03#f1", "E05.01.04#f4"], hold=2.0),
  dict(id="G15", seg="Close", shot="S23", text="Quick check. On this section, tap the layer our cell joined.", facts=[], hold=4.0, kind="check", check="spatial: tap Mesoderm"),
  dict(id="G15a", seg="Close", shot="S23", text="The middle layer, the mesoderm.", facts=["E05.01.03#f3"], hold=2.0, kind="reveal"),
  dict(id="G16", seg="Close", shot="S23", text="And which layer did all three come from: the epiblast, the old bottom layer, or a different one for each?", facts=[], hold=4.0, kind="check", check="own options (refutes E05.01.01 m2); chips 'Epiblast' / 'Old bottom layer' / 'One each'"),
  dict(id="G16a", seg="Close", shot="S23", text="The epiblast. All three came from it.", facts=["E05.01.04#f4"], hold=2.0, kind="reveal"),
  dict(id="G17", seg="Close", shot="S24", text="Next: how does this flat disc fold into a body?", facts=[], hold=1.0, kind="teaser"),
]

# ---------------- 9:16 Short (6 × 8 s, visual-style §2) ----------------
SHORT = [
  dict(id="R01", seg="Ch1 hook", shot="SS1", text="How does this one sheet of cells become three? Every tissue in your body comes from it.", facts=["E05.01.04#f4"], hold=0.8, kind="question", title=None),
  dict(id="R02", seg="Ch2", shot="SS2", text="Watch this cell. In week three a groove appears at the tail end: the primitive streak.", facts=["E05.01.01#f1", "E05.01.01#f2", "E05.01.02#f1", "E05.01.02#f3"], new=["primitive streak"], hold=1.5, title="THE GROOVE"),
  dict(id="R03", seg="Ch3", shot="SS3", text="Cells move to the groove, let go of their neighbours and slip underneath. Ours too.", facts=["E05.01.03#f1"], hold=1.5, title="THE DIVE"),
  dict(id="R04", seg="Ch4", shot="SS4", text="The first cells in replace the old layer underneath. Later ones, like ours, settle in between: mesoderm.", facts=["E05.01.03#f2", "E05.01.03#f3"], new=["mesoderm"], hold=1.5, title="A NEW MIDDLE"),
  dict(id="R05", seg="Ch5", shot="SS5", text="Cells left on top form the new top layer. Three layers from one sheet: gastrulation.", facts=["E05.01.03#f5", "E05.01.04#f4", "E05.01.01#f1"], new=["gastrulation"], hold=1.5, title="LEFT ON TOP"),
  dict(id="R06", seg="Ch6 payoff", shot="SS6", text="Three layers. Ours is in the middle one. Mesoderm builds muscle, bone, heart and blood.", facts=["E00.01.04#f1", "E00.01.04#f3", "E05.01.03#f6"], hold=2.0, title="THIS BECOMES"),
  dict(id="R07", seg="End card", shot="SS7", text="Full episode in the app.", facts=[], hold=1.0, kind="endcard", title=None),
]

SCRIPTS = {"lesson": LESSON, "general": GENERAL, "short": SHORT}

# ---------------- Shot list ----------------
# cam: lesson / short framings on the same scene state (scene spec §10). caption: band per M1b.q10 = B (D-059) for Shorts;
# Lessons keep 85–95 % (visual-style §10). tag = one §15 honesty tag. needs = V-step needs (new scene / spec work).
SHOTS = [
  dict(id="S01", kind="host", scene="host (tools/m1b-host)", day=None, what="Nani asks the question to camera; book closed on her lap", cams="cam_short + cam_lesson", key="warm key (no tokens on screen)", labels=[], tag=None, needs=["N1"]),
  # Primer shots (D-107, playbook §6b.3; S02 terms strip retired): each part isolated (rest ctx-dimmed), still view or ≤ 15° turntable, stamp + scale; label lands on the spoken name; no process motion.
  dict(id="S02b", kind="3D", scene="sc-E00.01.04", day="17", view="front (From the head), transverse cut + slab, ≤ 15° turntable", what="Primer part 1 (MBBS): the three germ layers stacked on the day-17 section, nothing else lit; one label 'Germ layers' with a three-token chip", labels=["Germ layers"], tag="Not to scale", needs=["N2", "N7"]),
  dict(id="S02c", kind="3D", scene="sc-E05.02.01", day="16", view="top, close, still", what="Primer part 2 (MBBS): the node isolated at the head end of the streak, rest ctx; accent ring on the node only", labels=["Primitive node"], tag="Colours illustrative", needs=["N2", "N12"]),
  dict(id="S02d", kind="3D", scene="sc-E05.02.01", day="18", view="end (transverse cut cranial of the node), then top at day 18 with all three parts in place", what="Primer part 3 (MBBS): the rod in the midline, isolated; then all three parts in place (layers, node, rod) for the 2 s end hold", labels=["Notochord", "Primitive node", "Germ layers"], tag="Simplified", needs=["N2", "N7"]),
  dict(id="S02e", kind="3D", scene="sc-E00.01.04", day="15", view="side (From the right), lengthwise cut, ≤ 15° turntable", what="Primer parts 1–2 (General): the top layer lit (epiblast), then the bottom layer lit (hypoblast), the other dimmed", labels=["Epiblast", "Hypoblast"], tag="Colours illustrative", needs=["N2"]),
  dict(id="S02f", kind="3D", scene="sc-E00.01.04", day="15", view="top, still; then the 2 s end hold with all three labels", what="Primer part 3 (General): the groove at the tail end (label + glow, no accent ring — the ring stays free for the marked cell); then all three parts in place", labels=["Primitive streak", "Epiblast", "Hypoblast"], tag="Colours illustrative", needs=["N2"]),
  dict(id="S03", labels_general=[], kind="3D", scene="sc-E00.01.04", day="15", view="top (From the back)", what="Establish: two-layer disc, slow push-in; Lesson only: from 'three germ layers' (L04) the day-17 three-layer stack as in S02b, so the i01 pause shows the three layers (P1F gates)", labels=["Epiblast", "Hypoblast", "Germ layers"], tag="Not to scale", needs=[]),
  dict(id="S04", kind="3D", scene="sc-E00.01.04", day="15", view="top", what="Push in to the caudal midline; streak ring (accent); stamp Day 15 · CS06", labels=["Primitive streak"], tag="Colours illustrative", needs=[]),
  dict(id="S05", kind="3D", scene="sc-E00.01.04", day="15→16", view="top, close", what="Ring moves to the cranial end; the mound is shown, not named yet (named at L18/S14)", labels=[], tag="Time compressed", needs=[]),
  dict(id="S06", kind="3D", scene="sc-E00.01.04", day="16", view="top, pull back", what="Pull back to whole disc; axis gizmo arrows Cranial/Caudal highlighted", labels=["Primitive streak"], tag="Colours illustrative", needs=["N12"]),
  dict(id="S07", labels_general=['Marked cell'], kind="3D", scene="sc-E00.01.04", day="15", view="side (From the right), lengthwise cut", what="Rewind to day 15; marked cell appears in the epiblast (accent ring is the cell's alone)", labels=["Marked cell", "Epiblast"], tag="Exaggerated for clarity", exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N4"]),
  dict(id="S08", kind="3D", scene="sc-E00.01.04", day="15→15.5", view="side, lengthwise cut", what="Cell moves to the streak, briefly changes shape and slips under (invagination; no sheet stretch). General G07: camera stays on the marked cell through the whole analogy (no cut ahead to S10, keeps time order)", labels=["Marked cell", "Primitive streak"], tag="Exaggerated for clarity", tag_also='Time compressed', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N4"]),
  dict(id="S09", labels_general=[], kind="3D", scene="sc-E00.01.04", day="15.5→16", view="side, lengthwise cut", what="Earlier cells (ghost tracer t-endo) replace the hypoblast; endoderm label as the sheet forms", labels=["Endoderm", "Hypoblast"], tag="Exaggerated for clarity", tag_also='Time compressed', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3"]),
  dict(id="S10", labels_general=['Marked cell'], kind="3D", scene="sc-E00.01.04", day="16", view="side, lengthwise cut", what="Our cell settles between the layers; mesoderm label", labels=["Marked cell", "Mesoderm"], tag="Exaggerated for clarity", tag_also='Time compressed', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N4", "N12"]),
  dict(id="S11", labels_general=[], kind="3D", scene="sc-E00.01.04", day="16→17", view="top, semi-transparent epiblast", what="Mesoderm sheet spreads sideways + cranially; marked cell ringed, riding the sheet", labels=["Mesoderm", "Marked cell"], tag="Exaggerated for clarity", tag_also='Time compressed', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3"]),
  dict(id="S12", labels_general=[], kind="3D", scene="sc-E00.01.04", day="17", view="side, lengthwise cut", what="Cells left on top lit; marked cell ringed below them; label Epiblast → Ectoderm swap", labels=["Ectoderm"], tag="Exaggerated for clarity", tag_also='Colours illustrative', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N6"]),
  dict(id="S13", kind="3D", scene="sc-E00.01.04", day="17", view="front (From the head), transverse cut through the streak + slab", what="D9 section: ectoderm / mesoderm / endoderm, yolk-sac side ventral; marked cell ringed in the mesoderm; hold", labels=["Ectoderm", "Mesoderm", "Endoderm"], tag="Not to scale", exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N7"]),
  dict(id="S14", kind="3D", scene="sc-E05.02.01", day="16", view="top", what="Opens on the day-17 frame, our marked cell dimmed out in the lateral mesoderm (end of its t-meso path); stamp counts back to day 16 (N11); pan to the node; prenotochordal cells run forward toward the head end", labels=["Primitive node"], tag="Exaggerated for clarity", tag_also='Time compressed', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N4", "N11", "N12"]),
  dict(id="S15", kind="3D", scene="sc-E05.02.01", day="16→17", view="end (transverse cut, cranial of node)", what="Notochordal plate in the endoderm, then folds into a rod; 'Notochord' label appears only on L20 (no label on the plate stage — the voice does not name it)", labels=["Endoderm", "Notochord"], tag="Time compressed", needs=[]),
  dict(id="S16", kind="3D", scene="sc-E05.02.01", day="17→18", view="side", what="Book order: head end of the rod first, tail parts added as the streak moves back (D-029: book version only)", labels=["Notochord"], tag="Time compressed", needs=[]),
  dict(id="S17", kind="3D", scene="sc-E05.02.01", day="18", view="end", what="Rod in the midline under the ectoderm; no neural tube drawn or named", labels=["Notochord"], tag="Simplified", needs=[]),
  dict(id="S18", kind="3D-adult", scene="new: sc-S1E01-18 (adult disc, Z-Anatomy, D-021)", day="adult", view="spine segment, one disc cut; cm scale bar + 'Adult' stamp replace the day stamp; Z-Anatomy credit + licence row (D-021)", what="This becomes: nucleus pulposus at the core of an intervertebral disc; vertebrae dim (ctx)", labels=["Nucleus pulposus"], tag="Not to scale", needs=["N8"]),
  dict(id="S19", kind="3D", scene="sc-E00.01.04", day="17", view="top, mesoderm only", what="This becomes: mesoderm sheet lit, rest ctx; marked cell ringed in it; no icons on anatomy — the voice carries the list", labels=["Mesoderm"], tag="Exaggerated for clarity", tag_also='Colours illustrative', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3"]),
  dict(id="S20", kind="3D", scene="sc-E00.01.04", day="17", view="top", what="Clinical link slot: replay starts on the marked cell's entry point in the streak (2 s), then ring the caudal streak; 'Clinical link' tag top-left", labels=["Primitive streak"], tag="Exaggerated for clarity", tag_also='Colours illustrative', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], clinical=True, needs=["N9"]),
  dict(id="S21", kind="diagram", scene="new: sc-S1E01-21 (caudal remnant diagram)", day="—", view="sagittal sketch", what="Diagram of a remnant at the sacrococcygeal region (no patient imaging, D6)", labels=["Sacrococcygeal teratoma"], tag="Simplified", clinical=True, needs=["N9"]),
  dict(id="S22", kind="3D", scene="sc-E00.01.04", day="17", view="front, transverse cut + slab", what="Payoff: back to the S13 section; marked cell shown in mesoderm", labels=["Ectoderm", "Mesoderm", "Endoderm"], tag="Not to scale", exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N7"]),
  dict(id="S23", kind="check", scene="sc-E00.01.04", day="17", view="front, transverse cut", what="2 Checks: tap-the-layer (spatial) + spoken-choice MCQ with ≤ 3-word chips; labels off for the tap; on the reveal (L31a/G15a) the Mesoderm label and the marked cell's ring come back", labels=[], tag="Not to scale", exaggerations=[{"what": "marked cell (reveal)", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N10"]),
  dict(id="S24", kind="host", scene="host", day=None, what="Teaser ≤ 5 s; Nani opens the book — pages blank/abstract, no diagram (host props carry no diagrams, §5b)", cams="cam_short + cam_lesson", key="warm key", labels=[], tag=None, needs=["N1"]),
  # Short shots (9:16 framings; most reuse Lesson scene states with cam_short)
  dict(id="SS1", kind="host+3D", scene="host / sc-E00.01.04 d15", day="15", what="Frame 1: day-15 disc, epiblast lit, hypoblast dimmed ('this one sheet'), question starts at 0 s; Nani cut-in at ~1.5 s; marked cell visible from ch2", cams="cam_short", key="neutral/cool key on Nani (tokens on screen)", labels=[], tag="Colours illustrative", needs=["N1"]),
  dict(id="SS2", kind="3D", scene="sc-E00.01.04", day="15", what="S04 push-in → S05 close → S06 pull-back (3 cuts); the streak gets label + glow, no ring — the accent ring is the marked cell's alone", labels=["Primitive streak", "Marked cell"], tag="Exaggerated for clarity", tag_also='Colours illustrative', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=[]),
  dict(id="SS3", kind="3D", scene="sc-E00.01.04", day="15→15.5", what="S07 → S08 shape change → S08 slip-under (3 shots, ~2.6 s each)", labels=["Marked cell"], tag="Exaggerated for clarity", tag_also='Time compressed', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N4"]),
  dict(id="SS4", kind="3D", scene="sc-E00.01.04", day="15.5→16", what="S09 → S09 endoderm close → S10 → close on the marked cell's ring (4 shots ~2.4 s + 1.5 s hold)", labels=["Mesoderm"], tag="Exaggerated for clarity", tag_also='Time compressed', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3"]),
  dict(id="SS5", kind="3D", scene="sc-E00.01.04", day="17", what="S12 ring → S11 top → S12 cells-on-top close → 1.5 s close on the marked cell's ring (4 shots ~2.1 s + 1.5 s hold)", labels=[], tag="Exaggerated for clarity", tag_also='Colours illustrative', exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N6"]),
  dict(id="SS6", kind="3D", scene="sc-E00.01.04", day="17", what="Section cut-in → ring on the marked cell in mesoderm → 2 s hold (3 beats)", labels=["Mesoderm", "Marked cell"], tag="Not to scale", exaggerations=[{"what": "marked cell", "how_much": "~4× size", "why": "so one cell reads at phone size", "exam_fact": False}], needs=["N3", "N7"]),
  dict(id="SS7", kind="endcard", scene="end card", day=None, what="'Full episode in the app' + chip 'Gastrulation · Part 1'; key structure + title inside the centre 4:5 crop (§15)", labels=[], tag=None, needs=[]),
]

# V-step needs (scene ids exist today unless listed here)
NEEDS = {
  "N1": "Host scene: add `cam_lesson` (16:9) beside the 9:16 camera — one scene, two cameras (M1b to-do; visual-style §10). Lines S01/S24/SS1. Step: M1V8 or R1.",
  "N2": "Primer (D-107, playbook §6b.3; replaces the terms-strip graphic, S02 retired): each part's label + token chip lands on its spoken name; the part's token colour + pattern becomes the episode's colour key (germ layers = ecto · meso · endo tokens; node = ctx + accent ring; notochord = meso; epiblast = epi; hypoblast = hypo; streak = ctx glow). The app shows the parts as chips linking to their cards + 'Know these? Skip ▸' (L3). Step: R1 (render) + L3 (player).",
  "N3": "Video use of a tracer: scene spec §5/§6 make `tracer` drill-only ('never in Try it, stills or video'). S1E01 needs the marked cell on screen. Spec change + engine flag, e.g. shot `show.trace` (scene-spec §10). Step: V-step (V4?) before ② can show it; ② may fake it as an animatic placeholder.",
  "N4": "New tracer `t-meso` (with the scene disclaimer 'marked cell drawn larger' kept on every shot it appears in) in sc-E00.01.04 (and the same cell in sc-E05.02.01 at its day-16 lateral mesoderm position, for S14): an epiblast cell that ingresses after the endoderm cell and ends in mesoderm, then spreads laterally (path keyed days 15 → 17). The existing `t-endo` stays as the 'first cells' ghost. Step: V-step (scene edit + scene-check path rules).",
  "N6": "Label swap 'Epiblast → ectoderm' becomes a spoken text item (C1 G-A11y to-do: '→' needs spoken text) and a clean 'Ectoderm' label at day 17. Step: V-step / scene owner.",
  "N7": "Shot-sheet `show` state: §10 has no `view/cut/slab_mm/layers/trace` per shot — add `show` (same shape as card drills §8a) so S13/S22 can ask for the transverse cut + slab at day 17. Step: R1 shot-sheet code (spec first).",
  "N8": "Adult anchor scene `sc-S1E01-18`: adult lumbar segment, one intervertebral disc cut to show the nucleus pulposus (Z-Anatomy adult mesh, rendered video only, D-021); vertebrae ctx. Step: V-step or R1.",
  "N9": "Clinical slot: caudal streak remnant + sacrococcygeal teratoma diagram `sc-S1E01-21` (our own diagram, no imaging, D6/§14); streak shrink after day 18 is not in any scene (keys end at day 17/18) → either a day-28 key or a diagram only. Step: V-step.",
  "N11": "Day stamp rewinds on screen (counts back) on the S06→S07 and S13→S14 time jumps, so a jump back in day reads as intended (G-Story r1). Step: ② animatic overlay, then R1.",
  "N12": "Day-16 stamp agrees across scenes: sc-E00.01.04 eases day 16 to 'CS06–07 · ≈0.3 mm' while sc-E05.02.01 keys day 16 as 'CS07 · 0.4 mm'. Add a day-16 key to sc-E00.01.04 = CS07 · 0.4 mm (dossier §1 book 16–18 d, R06/R08), or re-key sc-E05.02.01. Step: V-step (scene edit + scene-check).",
  "N10": "Spatial Check in video: tap-the-layer on a section is an app drill (V2 label drill); the video shows the question + a 4 s pause and the answer reveal; the app version links to the E05.01.03 drill. Step: R1 (player Checks).",
}

PRONUN = [
  ("gastrulation", "gas-troo-LAY-shun", "ˌɡæstɹʊˈleɪʃən"),
  ("epiblast", "EP-ee-blast", "ˈɛpiˌblæst"),
  ("hypoblast", "HY-poh-blast", "ˈhaɪpoʊˌblæst"),
  ("ectoderm", "EK-toh-derm", "ˈɛktoʊˌdɜɹm"),
  ("mesoderm", "MEZ-oh-derm", "ˈmɛzoʊˌdɜɹm"),
  ("endoderm", "EN-doh-derm", "ˈɛndoʊˌdɜɹm"),
  ("extraembryonic", "EK-struh-em-bree-ON-ik", "ˌɛkstɹəˌɛmbɹiˈɑnɪk"),
  ("invagination", "in-vaj-ih-NAY-shun", "ɪnˌvædʒɪˈneɪʃən"),
  ("caudal", "KAW-dul", "ˈkɔdəl"),
  ("cranial", "KRAY-nee-ul", "ˈkɹeɪniəl"),
  ("Carnegie", "kar-NAY-gee", "kɑɹˈneɪɡi"),
  ("prechordal", "pree-KOR-dul", "pɹiˈkɔɹdəl"),
  ("notochord", "NOH-toh-kord", "ˈnoʊtəˌkɔɹd"),
  ("nucleus pulposus", "NOO-klee-us pul-POH-sus", "ˈnukliəs pʌlˈpoʊsəs"),
  ("intervertebral", "in-ter-VER-teh-brul", "ˌɪntɚˈvɜɹtəbɹəl"),
  ("vertebrae", "VER-teh-bray", "ˈvɜɹtəbɹeɪ"),
  ("sacrococcygeal", "say-kroh-kok-SIJ-ee-ul", "ˌseɪkɹoʊkɑkˈsɪdʒiəl"),
  ("teratoma", "ter-uh-TOH-muh", "ˌtɛɹəˈtoʊmə"),
  ("primitive node", "PRIM-ih-tiv NOHD", "ˈpɹɪmɪtɪv noʊd"),
]

# Technical-term lexicon for the term check (G-Learn r1): any of these spoken must be known for the profile or declared `new` on that line or earlier.
LEXICON = ["gastrulation", "germ layers", "primitive streak", "primitive node", "primitive pit", "epiblast", "hypoblast", "ectoderm", "mesoderm", "endoderm",
  "invagination", "ingression", "extraembryonic", "notochord", "notochordal plate", "prechordal plate", "nucleus pulposus", "intervertebral", "vertebrae",
  "neural tube", "axial skeleton", "connective tissue", "spine", "vertebra", "prenotochordal", "sacrococcygeal", "teratoma", "yolk sac", "caudal", "cranial", "midline", "carnegie"]
KNOWN = {
  "lesson": ["epiblast", "hypoblast", "ectoderm", "mesoderm", "endoderm", "caudal", "cranial", "midline", "carnegie", "primitive streak", "gastrulation", "vertebrae", "connective tissue", "spine"],  # Part 0 E00.01.01–05 + E04
  "general": ["spine"],
  "short": [],
}

# ---------------- Spec 2 (D-107, docs/episode-spec.md §3; P1F) ----------------
SPEC = 2
CORE = ["E05.01.01", "E05.01.02", "E05.01.03", "E05.01.04"]   # brief: ★ core cards (B5)
# Review, not new (spec §3): a term introduced in Part 0 or on a core card, decided here at build time — term → the card whose terms.new has it.
REVIEW = {"lesson": {"primitive streak": "E00.01.01"}, "general": {"gastrulation": "E00.01.02"}, "short": {}}
# "Meet the parts" primer (playbook §6b.3): ≤ 3 parts; token = colour key; view = still or ≤ 15° turntable; hold = end hold (s).
PRIMER = {
  "lesson": {"parts": [
    {"term": "germ layers", "line": "L02c", "card": "E05.01.01", "token": "ecto · meso · endo", "view": "day-17 section, ≤ 15° turntable"},
    {"term": "primitive node", "line": "L02d", "card": "E05.01.02", "token": "ctx + accent ring", "view": "top, close, still"},
    {"term": "notochord", "line": "L02e", "card": "E05.02.01", "token": "meso, outlined", "view": "end cut, still; then all parts in place"}], "hold": 2.0, "target_s": 20},
  "general": {"parts": [
    {"term": "epiblast", "line": "G02c", "card": "E05.01.04", "token": "epi", "view": "side cut, ≤ 15° turntable"},
    {"term": "hypoblast", "line": "G02d", "card": "E05.01.01", "token": "hypo", "view": "side cut, ≤ 15° turntable"},
    {"term": "primitive streak", "line": "G02e", "card": "E05.01.01", "token": "ctx glow", "view": "top, still; then all parts in place"}], "hold": 2.0, "target_s": 15},
}
# Ideas (playbook §6b.1): proposal from the video-craft draft §5, re-cut by the builder to the 20–60 s + break rules (P1F); the story director signs (G-Story).
IDEAS = {
  "lesson": [
    dict(id="S1E01.L.i01", frm="L01", to="L04", objective="Name the three germ layers and the process that makes them in week three.", check_by="E05.01.01", title="Three layers, week three", next_q="So where does it start?"),
    dict(id="S1E01.L.i02", frm="L05", to="L08", objective="Say where and when the primitive streak forms and how it marks the head–tail axis.", check_by="E05.01.02", title="The groove"),
    dict(id="S1E01.L.i03", frm="L09", to="L12", objective="Explain that the first cells through the streak replace the hypoblast as endoderm.", check_by="L32", title="The first cells in", next_q="Where does our cell go?"),
    dict(id="S1E01.L.i04", frm="L13", to="L17", objective="Place ectoderm, mesoderm and endoderm on a section, all from the epiblast.", check_by="L31", title="All from the epiblast"),
    dict(id="S1E01.L.i05", frm="L18", to="L22", objective="Describe how cells from the primitive node form the notochordal plate, then the rod.", check_by="E05.02.01", title="From node to rod"),
    dict(id="S1E01.L.i06", frm="L23", to="L25", objective="State what the notochord does and what is left of it in adults.", check_by="E05.02.01", title="This becomes"),
    dict(id="S1E01.L.i07", frm="L26", to="L28", objective="Link leftover streak cells to sacrococcygeal teratoma.", check_by="E05.01.02", title="Clinical link"),
    dict(id="S1E01.L.i08", frm="L29", to="L33", objective="Answer the opening question: all three layers come from the epiblast.", check_by="L31", title="Back to our question"),
  ],
  "general": [
    dict(id="S1E01.G.i01", frm="G01", to="G05", objective="Point to the primitive streak and say it marks head and tail.", check_by="E05.01.02", title="The groove", next_q="How does one sheet make three?"),
    dict(id="S1E01.G.i02", frm="G06", to="G08", objective="Say that the first cells in replace the old bottom layer.", check_by="E05.01.03", title="The first cells in", next_q="Where does our cell go?"),
    dict(id="S1E01.G.i03", frm="G09", to="G12", objective="Say which of the three layers our cell ended up in.", check_by="G15", title="Three layers"),
    dict(id="S1E01.G.i04", frm="G13", to="G17", objective="Say that all three layers come from the one starting layer.", check_by="G16", title="Back to our question"),
  ],
}
RETIRED = ["L02", "G02"]         # terms-strip lines, replaced by the primer (A2: never reused)
SHOTS_RETIRED = ["S02"]          # terms-strip shot
