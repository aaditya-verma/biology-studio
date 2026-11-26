#!/usr/bin/env python3
"""Render table read + storyboard/shot list from s1e01_data.py and out/script.json (P1 ①)."""
import json, importlib.util, re
from pathlib import Path
H = Path(__file__).parent
spec = importlib.util.spec_from_file_location("d", H / "s1e01_data.py"); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
S = json.loads((H / "out/script.json").read_text(encoding="utf-8"))
def mmss(s): s = round(s); return f"{s//60}:{s%60:02d}"
UPD = "Updated: 27 Nov 2026 · Bio · Episode · S1E01 primer (P1F: primer + ideas, spec 2, D-107). Before: 22 Nov 2026 · Bio · Episode · S1E01 script (P1 ①)"

# ---- table read ----
t = ["# S1E01 Gastrulation — table read", "", f"*(Purpose: timings, hard-to-say lines and the pronunciation dictionary for the scratch voice (②) and the final voice. {UPD}.)*", "",
     f"Method: speech time = words ÷ {D.WPM} wpm (Kokoro `af_heart` 0.66, measured 143 wpm on the laptop, pipeline-reference §3) + the hold after each line. The real scratch-voice read happens in ② and replaces these estimates.", "",
     "## Timings", "", "| Profile | Words | Speech | With holds | Target | Speech wpm | Overall wpm |", "|---|---|---|---|---|---|---|"]
for p, lines in S["scripts"].items():
    w = sum(L["_words"] for L in lines); sp = sum(L["_dur"] for L in lines); tot = S["lengths_s"][p]; lo, hi = D.PROFILES[p]["length_target"]
    t.append(f"| {D.PROFILES[p]['name']} | {w} | {mmss(sp)} | **{mmss(tot)}** | {mmss(lo)}–{mmss(hi)} | {round(w/(sp/60))} | {round(w/(tot/60))} |")
t += ["", "Short chapters (grammar 8 s, visual-style §2):", ""]
for L in S["scripts"]["short"]:
    t.append(f"- {L['id']} {L['seg']}: {L['_words']} words · {L['_dur']} s speech + {L['hold']} s hold = {round(L['_dur']+L['hold'],1)} s")
t += ["", "Note: §2 suggests ≈ 17–20 words per chapter; at 143 wpm that is 7.1–8.4 s of speech with no room for the 1.5–2 s reveal hold, so chapters here run 15–17 words. G-Story to confirm.", "",
      "## Tongue-twisters (flag for the scratch read)", "",
      "- **L27** \"sacrococcygeal teratoma\" — said once; slow the scratch read on it.",
      "- **L24** \"nucleus pulposus\" — two stressed p's; check it isn't read 'pul-POH-zus'.",
      "- **L10** \"invagination\" — check the stress lands on NAY.",
      "- **G07** analogy line is the longest General line (~42 words) — breathe after 'underneath' and after 'floors'.", "",
      "## Pronunciation dictionary (EN)", "", "Kokoro (misaki) takes inline IPA as `[word](/IPA/)`; ② writes these into the scratch-voice text.", "",
      "| Term | Say | IPA |", "|---|---|---|"]
t += [f"| {a} | {b} | /{c}/ |" for a, b, c in D.PRONUN]
t += ["", "Hindi/Hinglish: not in this episode's profiles (English only, D-032 (3)); the dictionary gets a Devanagari column when a Hindi profile is asked for."]
(H / "out/table-read.md").write_text("\n".join(t) + "\n", encoding="utf-8")

# ---- storyboard + shot list ----
lines_by_shot = {}
for p, lines in S["scripts"].items():
    for L in lines: lines_by_shot.setdefault(L["shot"], []).append(f"{L['id']}")
b = ["# S1E01 Gastrulation — storyboard + shot list", "", f"*(Purpose: what each shot shows, its scene + day key, cameras, labels, honesty tag and caption band; V-step needs. Source of truth: `content/E/episodes/S1E01/shots.json`. {UPD}.)*", "",
     "## Frame rules used (all shots)", "",
     "- **Lesson + General (16:9):** captions 85–95 % from the top; bottom-left stack above the 84 % line: scale bar + honesty tag, axes, day/stage (visual-style §10). Labels ≤ 6, outside the subject's outline, leader lines (§12).",
     "- **Short (9:16):** M1b.q10 = **B** (D-059): captions **68–72 %, bottom-anchored at 72 %**, on host *and* anatomy shots; axes + scale bar move **top-left** (patch note `patches/visual-style-s1.md`). Labels ≤ 3. Cuts every 1–3 s; reveals hold ≥ 1 s.",
     "- **Host shots:** Nani (D-048, H-a in Blender, D-059). Any host shot with colour tokens on screen → neutral/cool key on her, or tokens on their own panel (D-059 (5)). Every host shot plans `cam_short` + `cam_lesson` on one scene (N1). Host never shows anatomy (playbook §5b).",
     "- **Always on 3D shots:** day/stage/size stamp, scale bar, axis gizmo (B2, H4). Stamps from the scene's day keys: day 15 · CS06 · ≈0.2 mm; day 17 · CS07 · ≈0.4 mm; day 18 · CS08 · ≈1.25 mm (dossier §1). Between keys the viewer eases (e.g. 'Day 16 · CS06–07 · ≈0.3 mm').",
     "- **Colour mode:** layer mode on every shot (no segment mode, no legend chip). Accent ring = 'look here' only; on tracer shots the ring is the marked cell's alone (scene spec §6).",
     "- **Reduced motion:** push-ins/orbits → cuts; no dust; label fades stay (§8).", "",
     "- **Primer (D-107, playbook §6b.3):** replaces the 5-s terms strip (S02, L02, G02 retired). After the cold open, ≤ 3 parts, each isolated (rest ctx-dimmed) on a still view or a ≤ 15° turntable, stamp + scale on; the label + token chip land on the spoken name; no process motion; ends with all parts in place and a 2 s hold.",
     "- **Ideas (D-107, playbook §6b.1):** Study pace pauses 0.3 s before the end of each idea's last hold (no speech ±0.3 s) on the held frame; panel words live in the app, never in the frame (D8). Watch plays through. Shorts never pause.", ""]
for p in ("lesson", "general"):
    P = S.get("primer", {}).get(p)
    if not P: continue
    b += [f"## Primer — {D.PROFILES[p]['name']} ({P['_dur']} s, end hold {P['hold']} s)", "", "| Part | Line | Card | Token (colour key) | View |", "|---|---|---|---|---|"]
    b += [f"| {q['term']} | {q['line']} | `{q['card']}` | {q['token']} | {q['view']} |" for q in P["parts"]]
    b.append("")
for p in ("lesson", "general"):
    I = S.get("ideas", {}).get(p)
    if not I: continue
    shots = {L["id"]: L["shot"] for L in S["scripts"][p]}; order = [L["id"] for L in S["scripts"][p]]
    b += [f"## Ideas — {D.PROFILES[p]['name']} ({len(I)}; the builder proposes, the story director signs)", "",
          "| Idea | Title | Lines | Shots | Length | Pause at | Objective | Check by |", "|---|---|---|---|---|---|---|---|"]
    for d in I:
        ls = order[order.index(d["from"]):order.index(d["to"]) + 1]; sh = list(dict.fromkeys(shots[x] for x in ls))
        b.append(f"| {d['id']} | {d['title']} | {d['from']}–{d['to']} | {sh[0]}–{sh[-1]} | {d['_dur']} s | {mmss(d['_break']) if '_break' in d else 'end'} | {d['objective']} | `{d['check_by']}` |")
    b.append("")
b += ["## Storyboard (Lesson order; General + Short reuse the same scene states)", ""]
for Sh in D.SHOTS:
    used = ", ".join(lines_by_shot.get(Sh["id"], [])) or "—"
    lab = ", ".join(Sh.get("labels", [])) or "none"
    lg = f" · General labels: {', '.join(Sh['labels_general']) or 'none'}" if "labels_general" in Sh else ""
    view = f" · view: {Sh['view']}" if Sh.get("view") else ""
    cam = Sh.get("cams") or ("cam_lesson + cam_short" if Sh["id"].startswith("S") and not Sh["id"].startswith("SS") else "cam_short")
    key = f" · key: {Sh['key']}" if Sh.get("key") else ""
    clin = " · **Clinical link slot**" if Sh.get("clinical") else ""
    need = f" · needs: {', '.join(Sh['needs'])}" if Sh["needs"] else ""
    b.append(f"- **{Sh['id']}** ({Sh['kind']}) `{Sh['scene']}` day {Sh['day'] or '—'}{view} — {Sh['what']}. Labels: {lab}{lg} · tag: {Sh['tag'] or 'none'} · cams: {cam}{key}{clin}{need} · lines: {used}")
b += ["", "## Shot list (table)", "", "| Shot | Scene | Day | Labels | Tag | Lines | Needs |", "|---|---|---|---|---|---|---|"]
for Sh in D.SHOTS:
    b.append(f"| {Sh['id']} | `{Sh['scene']}` | {Sh['day'] or '—'} | {', '.join(Sh.get('labels', [])) or '—'} | {Sh['tag'] or '—'} | {', '.join(lines_by_shot.get(Sh['id'], [])) or '—'} | {', '.join(Sh['needs']) or '—'} |")
b += ["", "## Simplifications and omissions (G-Sci item 9 — shown or in the description)", "",
      "- Amnion and yolk sac not drawn (scene disclaimers); the voice names the yolk sac only as the side the endoderm faces (L16).",
      "- Layer thickness not to scale; marked cell drawn larger (tracer disclaimer); time compressed on every moving shot (day 15 → 17 in ~2 min).",
      "- Oropharyngeal and cloacal membranes not shown (scene disclaimers) — not mentioned in the script.",
      "- 'Marked cell' label: used by sc-E00.01.04 (V3 trace drill) but not yet in GLOSSARY → commit task adds a GLOSSARY line (tracer convention, no book section).",
      "- Notochord: the book order only (head end first); the middle-first human data are not animated (D-029 (3)); one spoken pointer to the card (L22, MBBS only).",
      "- Neural tube not drawn or named (L23 says only 'help build the spine').",
      "- Fate map (E05.04.01) left out — not a core card for S1E01; the marked cell's mesoderm subtype is not named.", "",
      "## V-step needs (scenes or spec work that ② or R1 needs)", ""]
b += [f"- **{k}** — {v}" for k, v in D.NEEDS.items()]
b += ["", "## Per device (C13) — what ② must lay out", "",
      "- **Phone portrait:** the Lesson plays inline as a 16:9 preview with the transcript + Checks below; tap → full-screen landscape. The Short plays full-frame 9:16.",
      "- **Phone landscape / tablet:** Lesson full-width; tablet portrait shows the transcript beside or below (two panes).",
      "- **Desktop:** Lesson with transcript + shot list side panel (animatic review mode); labels must not look oversized at 1080 (playbook §6.10).",
      "- **Idea pause panel (Study pace):** drawn by the app per class (design-plan §2), never in the frame; the animatic marks each pause on the scrubber and in the transcript.",
      "- G-Art checks one 16:9 frame at 210 px high and at 1080, and the 9:16 frame at phone size, in ② (visual-style §10)."]
(H / "out/storyboard.md").write_text("\n".join(b) + "\n", encoding="utf-8")
print("ok")
