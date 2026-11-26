# Templates

*(Purpose: copy-paste formats for handoffs, prompts, cards, episodes, reviews, bugs, decisions, dossiers, sources. Updated: 26 Nov 2026 · Bio · Fix · video craft (§4 Episode: primer + ideas, D-107). Before: 22 Nov 2026 · Bio · Fix · CI guard — §2 End line: route B relies on the sync.bat guard (D-083). Before: 22 Nov 2026 · Bio · Build · W3 run surface — §2 *Run in:* line (D-080). Before: 22 Nov 2026 · Bio · Build · V3 trace a cell — §2 End: re-run `--write-sources` after the last rebase. Before: 22 Nov 2026 · Bio · Fix · open-run first (§2 open-run line, RULES I8 (8)). Before: 17 Nov 2026 · Bio · Ideation · Setup guide (D-025).)*

Change the words in angle brackets.

## 1. Chat handoff (end of a chat)
```
Done: <what shipped / decided>. Owner check: <Tn, device, minutes>.
STATUS, log and DECISIONS updated (<D-ids>).
Next: <step> in a fresh chat named "Bio · <Type> · <Step>". Prompt: <ready prompt>.
Usage check: <1–3 suggestions, or "nothing to suggest">.
```

## 2. Build prompt (each plan holds one per step)
```
Chat: Bio · Build · <step> (Build).
Run in: <Code | Cowork> — <why: the step's `run` in steps.json; check.py --next shows it>.
First action: add an open run to <step> (start = now IST, outcome partial) and push it (route A), or tell me to run sync.bat (route B). Then read.
Read claude/STATUS.md, claude/RULES.md, claude/DECISIONS.md and <plan §n>.
Take the build lock in STATUS (RULES I8); check the latest commit. Scope: <…>. Out of scope: <…>. Don't break: <…>.
Test: <…>. End: STATUS, build log, DECISIONS (next free id), owner test steps, next prompt + chat name, usage check.
End (every chat that touched DECISIONS, cards, registry or terms — Build and Research): route B → give the `sync.bat "<step>: … · by <name>"` line; its guard rebuilds sources.json and runs card-check, scene-check and the tracker before the push (D-083). Route A → after the last `git pull --rebase`, `sync.bat --check` (laptop) or the same four commands (cloud), then push (parallel chats each write sources.json from their own DECISIONS — CI E-sources, 22 Nov 2026).
```

## 3. Card (in a book-index table and in content/cards)
```
Id: E<ch>.<sec>.<nn> · Title · Tier · Threads · AN <code>
Idea (1 line, our words) [E<ch>.<sec> · R<nn> <locator>] <✔✔/✔/⚑/✚>
3D scene: sc-<id> · day range · layers shown · checked against <R01 CSnn / R02>
Watch it: <clip, 10–20 s> · Try it: <rotate / scrub / label / make it>
Remember: <1–2 lines>
More: <why, common mistakes> · Newer evidence / beyond Langman: <if ⚑ or ✚>
Clinical link: <if any, cited>
Check: Q · right answer · distractors (from GLOSSARY "Don't confuse" + dossier misconceptions)
≈ lines: <none / list>
```

## 4. Episode
```
Id: S<n>E<nn> · Title · Format · target length
Cold open: <question or clinical mystery>
Primer (Lessons): <≤ 3 parts, ~20 s MBBS / 15 s General, incl. 2 s hold> (playbook §6b.3)
Ideas: <id · objective · check_by · from–to line · 20–60 s; cited + marked lines, scene ids, day range> (playbook §6b.1)
Ends on section view: <which plane, which day>
This becomes: <adult anchor>
Recap: <2 lines> · Check: <2 questions, ≥ 1 spatial>
Core cards ★ / support cards · New terms (≤ 3 per minute)
Checklist: research/teaching-methods.md ✔
```

## 5. Review entry (logs/review-log.md)
```
<date> · <device> · <what was watched/studied> · right? <y/n + timestamp> · drifted at <time> · story <format, gripping/flat> · recall <x/y, 24 h x/y, 7 d x/y> · next: <action>
```

## 6. Bug report
```
<date> · v<NN> · <device + size> · Steps: <…> · Expected: <…> · Got: <…> · Screenshot: <yes/no>
```

## 7. Decision entry
```
| D-<NNN> | <date> | <decision> | <why> | <rejected options> |
```

## 8. Research dossier (research/dossiers/ch<NN>-<topic>.md)
```
# Research dossier — Ch <NN> · <topic> (for <cards> + <episodes>)
1. Staging & scale — stage · days · size · events · cards (sources, day-count convention)
2. ⚑ Watch items — newer evidence vs book; action; scene rule until decided
3. Visual references — R-id + stage for each scene to check (look, don't copy)
4. Why learners struggle — evidence + Check distractors
5. Curriculum map — NMC AN topic + competency codes
6. To-do — open items for this chapter
```

## 9. Source entry (research/source-registry.md)
```
| R<nn> | <title, authors, year, where> | <best for> | <licence → reference only / may ship with credit> |
```

## 10. Handoff note (when a chat has no commit route — RULES I8 (6), setup guide §6a)
```
From: <name> · chat <Bio · Type · Step> · <date>
Did: <what was researched / reviewed / tried>
Propose for docs: <doc path> → <change, in one or two lines each>
Proposed decisions: <D-entry text, marked proposed>
Open questions for the owner: <…>
Next: <step + ready prompt>
```
