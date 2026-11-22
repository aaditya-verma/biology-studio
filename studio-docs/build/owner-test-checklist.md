# Owner test checklist

*(Purpose: owner checks on real devices, T1…; no next build until the last is done. Updated: 22 Nov 2026 · Bio · Build · SR1 sources menu (scheduling) — T14 stub (planned, SR1). Before: 22 Nov 2026 · Bio · Build · U2 look tokens — T13b written (tokens, fonts, floating bar, Back history, v18; D-077, D-084, D-086). Before: 22 Nov 2026 · Bio · Design · U1 look canvas — T13 written (app look v2 canvas, D-077; T13b/T13c reserved for U2/U3). Before: 22 Nov 2026 · Bio · Build · V3 trace a cell — T8b written (trace drill, v15, D-075). Before: 22 Nov 2026 · Bio · Build · L2 lessons — T9 written (lessons, Today plans, Mixed review, D-070). Before: 21 Nov 2026 · Bio · Content · C2 round 3 — T3d part B written (all 23 Ch 6–8 cards Reviewed, D-065). Before: 21 Nov 2026 · Bio · Build · W2 scheduler — T11 written (W1 + W2; T6 folded in, D-063). Before: 21 Nov 2026 · Bio · Build · H2 reviewer mode — T10 written (part A you, part B the Professor; D-060, D-061). Before: 21 Nov 2026 · Bio · Content · C2 Ch 6–8 — T3d written (part A now, part B after round 3; D-058). Before: 21 Nov 2026 · Bio · Fix · L1 polish — T7b written (L1F re-checks, v10). Before: 21 Nov 2026 · Bio · Build · V2 3D drills — T8 written + result (pass, 3 notes → L1F). Before: 21 Nov 2026 · Bio · Review · T7 learning core — T7 result (pass except deck; deck step 22 Nov), step 4 button name, "open from the icon" note. Before: 21 Nov 2026 · Bio · Build · M1b v6 results — T1b result logged (pass, D-052). Before: 21 Nov 2026 · Bio · Build · M1b host results — T1b rewritten for the kit that actually runs (`m1b.py t1b`, v6, D-051). Before: 21 Nov 2026 · Bio · Build · L1 learning core — T7 written. Before: 21 Nov 2026 · Bio · Fix · M1b merge — T3c result logged (pass, from the L1 chat 03:43 IST). Before: 20 Nov 2026 · Bio · Build · M1b host shot (Step 2) — T1b written. Before: 21 Nov 2026 · Bio · Plan · App-first — T7, T8, T8b, T9, T3d stubs; T4 now the L3 player check (D-047). Before: 20 Nov 2026 · Bio · Build · M1 bake-off — T1 opened (3 clips, Method C pending). Before: 20 Nov 2026 · Bio · Content · C1 Part 0 + Ch 5 — T3c written. Before: 19 Nov 2026 · Bio · Build · W1 progress map — T6 written, T1b stub; open/pass state of each check now lives in `build/steps.json` (D-040). Before: V1 viewer — T3b written.)*

Run on real devices. Write each result on its **Result** line, then tick it in `claude/STATUS.md` › Owner reminders. Newest open items first. No next build starts until the last check is done (D-010).

**Devices (D-033, RULES C13):** every check with a screen runs on the **phone (portrait + landscape)**, a **tablet (portrait + landscape)** and the **laptop**. No tablet to hand → use the laptop browser's device mode (Chrome: F12 › device toolbar › iPad / Android tablet) and note "emulated". Report layout problems as *device + orientation + screen + what's wrong*.

**Apps:** A0 shell live at https://aaditya-verma.github.io/biology-studio/ (GitHub Pages, D-035).

**Status, 17 Nov 2026:** T1 written (opened 20 Nov, M1 run done). T2 open (K1 published the explorer). (Renumbered 17 Nov: old T2 → T3, old T3 → T4, after K1 was added, D-017.)

---

## T11. Progress map + Plan *(~12 min: phone, then tablet or laptop)* — OPEN (W1 + W2, 21 Nov 2026; D-063; includes T6)
Open https://aaditya-verma.github.io/biology-studio/#progress on the phone (pull to refresh once so **v13** loads), then a tablet (or the laptop's device mode, marked emulated), then the laptop. Steps 1–7 are T6.
1–7. **T6 steps 1–7** (map, C1, P1, board, your inputs, rotate, ✎). New on the map: on a **phone or tablet, the first tap on a box highlights its lines** (a short note says so); the second tap opens it. Back from a step → the box you came from has focus.
8. **Plan** tab (`#progress=plan`): *Estimated finish* + the critical path (◆ chain ending at GATE); one card per row — **Build lock · Laptop GPU · Research · You** — each with Now · Next · Later and ~dates. W2 shows on the lock row as Now; C2 is Next; GATE starts 7 days after L2 + V2.
9. **Your inputs, most useful first:** the top one unblocks the most steps; *All N in Your inputs* opens the full list. **Suggested for the professor (optional)** says nothing waits for it.
10. **Runs (plan vs actual):** newest first; a step with more runs than its estimate shows **slipped**.
11. Tap a step (e.g. **L2**): its facts now show **Plan** (~dates · row, ◆ if on the critical path) and its runs.
12. **Calendar line** at the bottom: your chat time per day. Answer **W2.q1** if the minutes are wrong (dates follow it).
13. Phone portrait: Plan cards stack (Now · Next · Later under each other); phone landscape / tablet: the three columns sit side by side; laptop: you + professor side by side under the rows.
- **Result:** ☐ pass ☐ problems · T6 steps 1–7 ☐ pass · plan dates believable: ☐ yes ☐ no (which?) · rows right: ☐ yes · ranked inputs make sense: ☐ yes · runs list right: ☐ yes · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · layout problems (device + screen):

---

## T10. Reviewer mode *(part A ~15 min you: phone, then laptop (+ tablet or device mode) · part B ~20 min the Professor: 2 real cards)* — OPEN (H2, 21 Nov 2026)
*(Numbered T10: T9 is L2's planned check — ids are permanent, A2.)*
**Before (2 min, laptop, once):** run `sync.bat "H2: Reviewer mode v12, D-060 D-061"` (this one sync also carries the C2 and M1b work waiting on the laptop) and press **Sync now**. On github.com/aaditya-verma/biology-studio: **Settings › General › Features › Issues** is ticked; **Issues › Labels › New label** `review` and `fixing` (chats can't change repo settings). **Issues › New issue** shows *Card review* and *General feedback*.
**Part A — you walk it (real mode: no `?test=1`).**
1. **Demo first (phone P):** `…/?test=1&fixture=review#review` — To review shows *Changed since your review* / *Fixed — please look again* chips; My feedback shows 7 items: *Sent — waiting for Aaditya*, *Being fixed*, *Fixed in app update 12*, *Done — thank you*, *No change needed — see the reply*, *Answered — see the reply*, each with its meaning printed under it. Add `&rvlimit=1`: the list stays, with *GitHub asks us to wait a little … can check again after HH:MM*.
2. **First visit (phone P, real mode, her link):** `…/#review` (pull to refresh until Settings shows **v12**). The **tour** opens by itself: 3 screens, Back/Next/Skip, buttons near the bottom. *Start reviewing* → Review home; a **Review** tab now sits after Cards. No ✎ pencils or *test* chip anywhere.
3. **Home (phone P → L):** *Hello, Komal* + three tabs (To review · What's new · My feedback) with counts; landscape puts the tabs in a side strip. What's new is empty today (the first visit is the starting point); *All updates* shows plain-English lines grouped by date.
4. **Card review (phone P, top card under To review):** the card reads in plain sections (numbered facts with book section + source names, mix-ups, questions with right answers). Tap **Send on GitHub** with nothing chosen → *Pick ✓ … first*. Pick **✎ Needs a fix** → it asks for a note. Write a test note, tick two boxes, pick *How sure*. Rotate to landscape → answers and place kept. **Send on GitHub** → GitHub opens with Card, Overall, Which part, How sure, Checklist and Note filled in, title `[review] <id> v1 ✎ …`. Press **Create** (a test — you'll close it).
5. **My feedback for your test:** it's under *your* name, so open `…/?debug=review#review=mine` → Debug → *Pretend to be* `aaditya-verma` → OK: *Sent — waiting for Aaditya*. On GitHub add label `fixing` → **Check for news** → *Being fixed*. Create milestone `v12`, set it, close the issue → *Fixed in app update 12*. Then close it as *not planned* (→ *No change needed*) or delete it.
6. **Laptop:** `#review` = three panes side by side; a card review = card │ your review, with **Send** in view at the bottom of the form. Tablet (or device mode iPad): portrait = tabs + one pane; landscape = To review │ My feedback over What's new.
7. **Settings › Reviewer mode:** *Turn off* hides the Review tab; *Turn on* brings it back.
8. **G-Owner on D-061** (addresses, 8-line checklist, ✓/✎/? + note rule, the issue words, 5-min check, updates from the build log): "D-061 confirmed" or what to change. Then send the welcome message (**H2.q3**) — WhatsApp or email, as is:
   > Hi Komal — Biology Studio is ready for your science review.
   > 1. Open https://aaditya-verma.github.io/biology-studio/#review on your phone or laptop — a 3-screen tour shows you around.
   > 2. Sign in to GitHub once (komalverma00500-byte). For each card: tick what's right, pick ✓ / ✎ / ?, press Send on GitHub, then Create.
   > 3. My feedback shows what happened to each note. Help, if you need it: https://github.com/aaditya-verma/biology-studio/blob/main/studio-docs/build/setup-guide.md#0-reviewer-start-here-no-setup-5-min
**Part B — the Professor (her phone or laptop, after the welcome message):**
9. She opens the link, takes the tour, signs in to GitHub and reviews **2 cards** from *To review* (one ✓; one ✎ or ? if she finds anything), pressing **Create** each time.
10. You: both issues are on GitHub with label `review`; decide the ✎ (label `fixing`, or close *not planned* with a reply); answer a ?. She sees the new words after **Check for news**. Her ✓ = the human science pass for that card version (D-060): the next content chat adds `G-Sci human ✓ · the Professor · issue #n` to the card's log.
- **Result T10:** ☐ pass / ☐ notes · A: demo states ☐ · tour + Review tab ☐ · home tabs P/L ☐ · send blocked + note rule ☐ · form pre-filled ☐ · rotate keeps answers ☐ · issue words after label/milestone ☐ · laptop 3 panes + Send in view ☐ · tablet ☐ · Settings toggle ☐ · D-061 ☐ · B: her 2 reviews arrived ☐ · her words ("easy / confusing at …") ☐ · devices: phone P/L ☐ tablet ☐ laptop ☐

## T6. Progress map *(~6 min: phone, then tablet or laptop)* — FOLDED into **T11** (D-063): run T11, which repeats these steps
Open https://aaditya-verma.github.io/biology-studio/#progress on the phone (pull to refresh once so v5 loads), then a tablet (or the laptop's device mode, marked emulated), then the laptop.
1. **Map:** lanes by chat type (Ideation · Build · Research · Content · Episode · Review · Ideas). Each box shows its id and status as colour **and** pattern **and** a word; the key under the map lists them. Phone portrait: the map runs top → bottom; landscape and larger: left → right.
2. Tap **C1**: the step page shows needs (S1, X1.05, X1.06 ✓), unblocks (P1, L1), gates, D-ids, last log line and your open D-037 question (C1.q1); a grey note says it waits only for the build lock if a build chat holds it. **Copy prompt** copies the ready prompt; the chat name shows above it.
3. Tap **P1**: a red "Can't start — needs C1 (ready), M1b (planned)" line shows.
4. **Board:** Now · Ready · Blocked · Done. Phone: one section under another; phone landscape and tablets: two columns (tablet landscape four if ≥ 1200 px wide); laptop: four.
5. **Your inputs:** oldest first; tap one → its step; **Copy reply** copies a line to paste into that step's chat.
6. **Rotate** phone and tablet on a step page: same step, same place.
7. Turn on testing mode (Settings): ✎ on a step opens an edit prompt pointing at `build/steps.json`.
- **Result:** ☐ pass ☐ problems · map readable on the phone: ☐ yes ☐ no (where?) · can't-start line right: ☐ yes · board columns right: ☐ yes · inputs list complete: ☐ yes ☐ missing (which?) · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · rotate keeps place: ☐ yes · layout problems (device + screen):

## T7. Learning core *(~20 min: phone, then tablet, then laptop; + 1 min tomorrow)* — PASS except deck (L1, 21 Nov 2026; deck step 22 Nov)
Open the app **without** `?test=1`: https://aaditya-verma.github.io/biology-studio/ — pull to refresh once so **v7** loads (Settings shows the version). This time your taps are saved on the device. Open it from the home-screen icon (or your browser), **not from a link inside the Claude app** — that opens Claude's own browser, which keeps a separate copy of your progress. Tap **Export backup** in Settings first (A3).
1. **Cards tab (phone, portrait):** 13 cards in two groups, each with a ring + word: ○ New, ◔ Read, ◑ Understood, ● Can explain.
2. **Open E05.01.01 Gastrulation in one picture.** Title, General/MBBS switch and "You will be able to" sit above the 3D. Wait 2 s: the chip turns **Read**. Turn the 3D and scrub the days; **Open full 3D** keeps the day. Tap a small number after a sentence: its facts open with source + mark.
3. **Check:** answer one question wrong on purpose. You should see ✗, the right answer and why. Finish → "Read the card again, then retry". Try again (options reshuffle) and get all right → **Understood**.
4. **Can explain:** say the objective out loud, tap **Show a model answer**, then **Mine matched** → **Can explain** (**Not yet** keeps it Understood).
5. **Rotate** to landscape mid-Check: same question, same day in 3D, same place on the page.
6. **E00.01.06 How to use the app** (the new guide card, marks ⓘ): does it describe the app as you just used it? Anything wrong or unclear → note the line.
7. **Tablet** (or laptop device mode, "emulated"): portrait = 3D on top, text below; landscape = 3D │ text. **Laptop:** 3D │ text │ card rail; the 3D stays in view while the text scrolls. Try the Check with the keyboard only (Tab, Enter/Space).
8. **Remember deck:** Today shows "Nothing due today" (prompts first come back tomorrow). **Tomorrow:** Today shows the due count → **Review now** → answer from memory, Show answer, Got it / Not yet. Note: anything confusing?
9. **G-Owner** on D-050 (guide cards + ⓘ, statuses, 1-3-7 deck, Reviewed cards shown to learners): say "D-050 confirmed" or what to change.
- **Result T7:** ☑ pass except deck (21 Nov 2026, 05:02–13:55 IST · owner with chat `Bio · Review · T7 learning core`) · statuses move as described: ☑ (tablet E05.01.01 + phone E00.01.01: Read → Understood → Can explain; kept after closing and reopening the app) · Check feedback clear: ☑ · Can explain makes sense: ☑ · rotate keeps place: ☑ (question + day kept; phone L: the 3D scrolls away with the text → L1F) · E00.01.06 matches the app: ☑ (tablet + phone) · devices: phone P ☑ L ☑ · tablet P ☑ L ☑ (real tablet) · laptop ☑ · deck next day: ☐ (22 Nov — **L1.q2**) · D-050: ☑ confirmed + change: the card text folds away while the Check runs (**D-053**) · notes: (1) tablet P · Cards + Today · titles break mid-word ("Gast/rulati/on…", "syncytiotrophobl/ast"); (2) phone L · card reader · 3D column scrolls away, left half empty; (3) phone P · Try it 3D · labels crowd (streak label on the cranial arrow, node/streak leaders cross); (4) all devices · every card · MORE + SOURCES headings empty; (5) card Remember · "next on tomorrow" wording; (6) Today intro says prompts come back after passing the Check — D-050 says they join on Read; (7) backup file name uses the UTC date; (8) G-Eng: saved state keeps `app` 5/6 and `savedAt` older than the last tap → all **L1F** (`Bio · Fix · L1 polish`). Not a bug: the 05:02 backup came from the Claude in-app browser (own storage, created 04:58), not the installed app — note added above.

## T7b. L1 polish re-check *(~12 min: phone, then tablet, then laptop)* — OPEN (L1F, 21 Nov 2026)
Open the app **without** `?test=1`, pull to refresh until Settings shows **v10**. Tap **Export backup** first (A3).
1. **Check hides the card (phone P, E05.01.01):** tap **Start the Check** — the body, Don't confuse, This becomes…, Remember, More and Sources fold away; one line says *Card text hidden during the Check* with **Read again**. The objective and Try it stay; **the 3D labels are off** during the run. Tap **Read again**: the text comes back, the run ends unscored (status unchanged), **Start the Check** starts fresh. Finish a run → text and labels come back.
2. **Notochord E05.02.01 (phone P):** Try it opens closer: strand → plate → rod and the *Prenotochordal cells* label show without zooming. Reset view / double-tap returns there.
3. **Label it (E05.02.01 q5, phone P):** the three pins sit clear of the stamp, notes and compass; after **Check the labels**, each pin shows its label right beside it, including *Epiblast → ectoderm*.
4. **Which day is this? (E05.05.01 q4, phone P + landscape):** the whole 1 mm ruler is on the stage, clear of the scale bar and notes.
5. **E00.01.01 Try it at phone P:** no label sits on an axis arrow.
6. **Phone landscape, any card:** the 3D stays on the left while you scroll the text (no empty left half). Watch it is left out here; Open full 3D is the small cube button.
7. **Tablet P:** Cards list and Today *Continue* titles wrap on whole words; chip + id drop below when narrow.
8. **Every card:** **Sources** lists the book sections and the outside sources by name (guide card E00.01.06: *App facts (ⓘ) — no book source*); **More** shows only when the card has extra facts and opens with ▸. Remember reads *Due tomorrow* (or a date). Today's intro says prompts join the deck when you read a card.
9. **Backup:** Settings › Export backup → the file is named with today's date where you are; in the file `app` is 10 and `savedAt` is close to now.
10. **Phone fps (carried from T8 step 7):** `…/?debug=viewer#scene=sc-E05.02.01` → Debug → **Measure fps** → Copy → paste in chat.
11. **G-Owner on D-056** (labels off during a run; leaving the card ends a run; phone framing; pinned labels): "D-056 confirmed" or what to change.
- **Result T7b:** ☐ pass / ☐ notes · fold + Read again: ☐ · labels off in a run: ☐ · notochord start view: ☐ · label drill labels: ☐ · day ruler: ☐ · arrows clear: ☐ · phone L 3D stays: ☐ · titles wrap: ☐ · Sources/More/Due: ☐ · backup name + fields: ☐ · fps: ☐ · D-056: ☐ · devices: phone P/L ☐ tablet P/L ☐ laptop ☐

## T8. 3D drills + new scenes *(~20 min: phone, then tablet, then laptop)* — PASS 21 Nov 2026 (V2)
Open the app **without** `?test=1` and pull to refresh until Settings shows **v8**. Tap **Export backup** first (A3). Two cards went back to draft for re-review and are Reviewed again in v8 (E05.02.01, E05.05.01).
1. **Notochord card E05.02.01 (phone, portrait).** Try it now shows its own scene: a cut down the midline on day 17. Can you see, from tail to head: the thin strand of cells, the flat plate in the bottom layer, then the round rod? Scrub days 16 → 18: the rod spreads from the head end (the book's order; the newer "middle first" finding is only in More). Labels sit on their structures; none points at something hidden.
2. **Check on the phone:** question 4 *Order the frames* — three cross-section pictures; move them with ↑/↓ into plate → lifting → rod. Question 5 *Label it* — the 3D moves into the Check with numbered pins; pick a label per pin; after checking, the real labels appear. Open *Describe the picture* once: does the text alone let you answer?
3. **Rotate to landscape mid-drill:** the 3D jumps beside the question and keeps your view; rotate back — it returns into the Check. Finish the Check → Try it gets its own view back.
4. **E05.05.01 The disc becomes a pear:** question 4 *Which day is this?* — the stamp reads **Day ? · stage ? · size ?** until you answer, the ruler and scale bar stay; then the real day shows.
5. **Demo of all five drills** (testing mode only, never for learners): open `…/biology-studio/?test=1&fixture=drills#card=E05.02.01` → Start the Check: *Rotate to match* (turn with drag or the ◀ ▶ ▲ ▼ buttons until it matches the target picture, then **Check my view**; also try **Answer in words instead**), *Which day is this?*, the two above, *Folded or not?* (rod or not yet, per picture).
6. **Tablet** (or laptop device mode, "emulated"): portrait = the drill 3D sits inside the Check; landscape = beside it. **Laptop:** the drill stays in the 3D column; try a whole drill with the keyboard only (Tab, Enter/Space, arrows in a select).
7. **fps on the new scene (phone):** open `…/?debug=viewer#scene=sc-E05.02.01` → Debug tab → **Measure fps (~30 s)** → Copy → paste into the next chat (pipeline reference §2). Also tap **Lose + restore context (test)** once: the 3D should come back within ~1 s.
8. **G-Owner on D-054** (drills as Check types, masked day only during *Which day is this?*, 3D in the Check on portrait / beside on landscape, rotate + folded waiting for Ch 6 cards): say "D-054 confirmed" or what to change.
- **Result T8:** ☑ pass (21 Nov 2026, 14:42–14:50 IST, owner: "all ok") · notochord scene reads (strand → plate → rod): ☑ after zooming (note 1) · frames + label drills fair: ☑ · rotate mid-drill keeps the view: ☑ · day mask clear: ☑ · demo rotate/folded: ☑ · keyboard only: ☑ · devices: phone P ☑ (v8, 360×720) · others reported ok · phone fps sc-E05.02.01: not sent (→ L1F to-do) · D-054: ☑ confirmed · notes: (1) Phone P · Notochord Try it opens too far out: strand → plate → rod and the Prenotochordal label show only after zooming — tighter phone start view for sc-E05.02.01 (2) Phone P · Notochord Q5 after answering: revealed labels crowd the pins and the top-layer label (Epiblast → ectoderm) is missing — pinned structures' labels first, beside their pin (3) Phone P · Pear Q4 (day drill): the 1 mm ruler was mostly off the stage in the owner's screenshot (owner may have zoomed) — check the drill start framing keeps the ruler in → L1F

## T13b. New look: tokens, fonts, floating bar, Back *(~15 min: phone first, then tablet, then laptop)* — OPEN (U2, app v18, 22 Nov 2026; D-077, D-084, D-086)
Hard-refresh first (pull down twice, or close and reopen the app from its icon) — Settings › version must say **v18**. Screens keep their old layout; U3 restyles them (T13c).
1. **Phone, portrait — the bar:** a floating bar at the bottom: **Today · Learn · Map · 3D · More**. Tap each. The current one has a plum line + its word. **More** opens a sheet with Settings (and Review if it's on). Scroll a long page down: the bar slides away; scroll up a little: it's back. Tap the search box on Map: the bar stays out of the keyboard's way.
2. **Back, everywhere (D-084):** Map › E05 › a concept › tap a *Needs first* link › another link. A round **Back** button floats bottom-left (above the bar). Tap it: you step back one concept at a time. Open two links again, then tap **✕** on the panel: you land back on the chapter, not on Today. Press the phone's own Back: same history, and it never leaves the app on the first press (at the very start it says *Press Back again to leave*).
3. **Search + trail:** the 🔍 at the top right opens the map's search box from any screen. The top line shows where you are (*E05 › Primitive streak*); tap the first part to go up.
4. **Look:** greys one shade darker per nested box, cards with soft shadows (no grey borders), titles in **Figtree**, reading text in **Atkinson Hyperlegible Next** (check *Il1 0O* in a card id). The plum fill is only on the main button (it has a small lift under it). Light **and** dark (Settings › Theme).
5. **3D (Learn › a card › Try it, or 3D):** the stage is still the dark island. Layer / Labels / Cut toggles: **on = dark fill + plum ring + ✓**, off = grey. A *look here* layer (streak) still shows its plum ring clearly against grey tissue — tell me if not (D-086 note for deuteranopes).
6. **Rotate:** turn the phone mid-scroll on a card: place kept; landscape shows a side strip of icons.
7. **Tablet (both ways) + laptop:** a rail with labels on the left (tablet portrait used to have the bottom bar). Back sits in the top bar.
- **Result:** ☐ pass ☐ changes · devices: · bar ☐ · Back/✕ ☐ · fonts ☐ · dark ☐ · 3D toggles ☐ · notes:

## T13. App look v2 — pick on the canvas *(~15 min: phone first, then tablet or laptop)* — PASS 22 Nov 2026 (U1; D-077 confirmed)
Open the canvas https://claude.ai/artifact/9ToGW4nXqsRve6KGp7znw9 (rows = Today, Card, Lesson, 3D viewer, Book map, Settings; each row light then dark; columns = phone portrait, phone landscape, tablet portrait, tablet landscape, desktop). Nothing in the app changes yet.
1. **Phone first:** open the Today, Card and 3D viewer phone boards full screen (tap a board, then its focus view). Does the tonal grey (each box one shade darker than the one it sits in) feel calmer and richer than today's white cards? Is the plum **Start** button the one thing your thumb goes to?
2. **Fonts:** open *Font comparison*. A (picked) uses Figtree for titles and numbers and Atkinson Hyperlegible Next for reading. Read the long terms and the *Il1 0O* line. Keep A, or switch to B or C?
3. **3D stage:** on Card and Viewer boards: day + stage + size stamp top left, disclaimers under or beside it, axes bottom left, 0.1 mm scale bottom right, floating control bar above them. Labels sit on dark pills. Anything you can't read on the phone board?
4. **Layouts:** phone landscape (side strip, 3D beside text), tablet (rail + two panes), desktop (rail + header tabs, three panes). Anything that should move?
5. **Dark:** same screens in dark. The 3D island stays the darkest thing in both themes.
6. **Ladder + contrast** board: light theme needs darker germ-layer outlines to stay readable on the darker greys (fills, patterns and labels do not change). OK to change the light outlines (D-077)?
7. **G-Owner on D-077:** say "D-077 confirmed" (U2 builds it) or list what to change; leave comments on the boards if easier.
- **T13b —** U2 tokens + fonts + shell on your phone (written by U2). **T13c —** U3 screen pass (written by U3).
- **Result:** ☑ pass ☐ changes · devices: not stated · fonts A ☑ B ☐ C ☐ · light outlines OK ☑ · D-077 ☑ confirmed (no changes) · notes: owner's answer, given in `Bio · Build · W3 run surface` and recorded by `Bio · Fix · W4 live desk row`, 22 Nov 2026 — route B for U2 was also named there

## T8b. Trace a cell *(~15 min: phone, then tablet, then laptop)* — OPEN (V3, app v15, D-075)
Open the app **without** `?test=1` and pull to refresh until Settings shows **v15**. Tap **Export backup** first (A3). Card E05.01.03 *Cells move in* went back to draft for re-review and is Reviewed again in v15 (a new question 4).
1. **Phone, portrait — E05.01.03 → Start the Check → answer q1–q3 → question 4 *Trace a cell*.** The 3D moves into the Check with a small cell ringed in pink and labelled *Marked cell*; the notes line starts *marked cell drawn larger*. The stamp shows the real day (Day 15 · CS06 · ≈0.20 mm) — it is not hidden.
2. **Follow it:** drag the **Day** slider, tap ▶ step by step (15 → 15.3 → 15.5 → 16 → 17), then press Play. Can you see the cell crawl along the top layer to the front of the groove, go under, and settle in the **bottom** layer (not the middle one)? Turn the 3D with the buttons or a drag if it helps. Then pick an answer — the right one is Endoderm; try a wrong one on a second run to read the feedback.
3. **Is it fair?** Could you answer without watching (from the question words or q1–q3)? Is the cell easy to see and tell apart from the layers on your phone? Open *Describe the picture*: does the text alone let you answer, without naming the layer?
4. **Rotate to landscape mid-drill:** the 3D jumps beside the question and keeps the day you were on; rotate back. Finish the Check → Try it shows **no** marked cell (it exists only in the question).
5. **Reduced motion** (phone setting, or Settings › Motion › Reduce): Play now jumps from step to step instead of gliding.
6. **Tablet** (or laptop device mode): portrait = the drill inside the Check; landscape = beside it. **Laptop:** do the whole question with the keyboard only — Tab to the Day row, ← → on the slider, `[` `]` steps and Space plays while the 3D has focus, Enter picks an answer.
7. **In a lesson:** Lessons → Ch 5 → the sitting with *Cells move in* → its Check step runs the same 4 questions (no new step). Mixed review never asks the trace (it asks words-only questions).
8. **G-Owner on D-075** (trace = a Check type; the path is scene data; the cell only during its question, ringed + labelled, drawn larger; first use = an early cell → endoderm, entering at the front of the streak): say "D-075 confirmed" or what to change.
- **Result:** ☐ pass ☐ problems · devices: phone P ☐ · tablet ☐ · laptop ☐ · D-075 ☐ · notes: ___

## T9. Lessons, Today, Mixed review *(~25 min: phone, then tablet, then laptop; + 2 min tomorrow)* — OPEN (L2, 22 Nov 2026; D-070)
Open the app **without** `?test=1` and pull to refresh until Settings shows **v14**. Tap **Export backup** first (A3). Built *at risk* (T7 deck step, T7b, T3d still open): if one of those fails, say so here too.
1. **Today (phone P):** two plans at the top — **On the go · up to 5 min** (Remember prompts due + one Check) and **Study · 15–30 min** (the next lesson sitting + prompts due + Mixed review once 2 cards are Understood). Do the words make sense without help? Is the minutes estimate believable?
2. **Lessons (phone P):** Today › Cards box › **Lessons**. Five chapters (Part 0, Ch 5–8), each with cards · sittings · minutes and a progress bar with words. **Continue where you stopped** is on top.
3. **One lesson (Part 0):** open it → *Needs first* (none for Part 0; Ch 5 shows Part 0 cards + *Bilaminar disc · Not in the app yet*) → sittings, each card with its step chips (○ Read · Check · Try the 3D · Remember). Tap **Start**.
4. **Lesson bar on a card:** the bar sits under the objective: *Lesson · Part 0 · sitting 1 · step 1 of 12*, this card's steps, **Now:** what to do. After a moment Read ticks ✓ and **Next step** appears → it scrolls to the Check (the address changes, nothing reloads). Do the Check (any score moves you on; all right = Understood). **Try the 3D** → turn it → **Done — next step** → **Remember**: say each answer, open it → **Done — next step** opens the next card.
5. **Skip + resume:** on a Check step tap **Skip for now** → next step. Go back to the lesson: the skipped step shows ↷; **Continue** goes to the first step not done; when only skipped steps are left it goes back to them. Close the app, open it again: the same place.
6. **A no-3D lesson (Ch 6):** cards have only Read · Check · Remember (no 3D step). **Ch 5 Notochord + The disc becomes a pear** show **3D drill** instead of Try the 3D: it ticks when the drill questions in the Check are right.
7. **Sitting end:** finish the last step of a sitting → back on the lesson with *Sitting 1 done* and *sitting done* under it. Is a sitting about 10–15 min for you? **Time one** and note the minutes.
8. **Mixed review:** once 2 cards are Understood, Today › Study › **Mixed review** → Start: 8 questions mixed across chapters, **no card text** shows; after each answer the right answer + why. At the end: *N of 8 right* and *Card statuses stay as they were*. Check a card in Cards: its status did not change.
9. **On the go › One Check:** a whole Check of one card you understood, card text hidden; Today then shows ✓ on it. **Remember** in On the go stops after 8 prompts (Study's goes to 20).
10. **Rotate + other devices:** phone landscape, tablet P/L, laptop: Lessons in 2–3 columns, a lesson as head │ sittings, the bar stays in the card head; rotating mid-lesson keeps the step and the Check. Keyboard on the laptop: Tab through the bar and Mixed review.
11. **How to use the app (E00.01.06, now v2):** the new lines on Today's plans, Lessons and Mixed review match what you just did.
12. **Tomorrow (~2 min):** Today shows the prompts from the cards you read as due; On the go works through them.
13. **G-Owner on D-070** (sittings of 10–15 min, the step rules incl. *any finished Check run ticks the step*, Skip for now, the drill step, Mixed review rules, Today plans, nav unchanged): "D-070 confirmed" or what to change.
- **Result T9:** ☐ pass / ☐ notes · Today plans: ☐ · path + lesson: ☐ · bar + steps: ☐ · skip + resume (after reopen): ☐ · no-3D + drill step: ☐ · sitting minutes: ___ · Mixed review (no text, status kept): ☐ · On the go: ☐ · rotate/devices: ☐ · guide card: ☐ · tomorrow: ☐ · D-070: ☐ · devices: phone P/L ☐ tablet P/L ☐ laptop ☐

## T3d. Ch 6–8 cards *(part A ~8 min + part B ~15 min, both now: phone, tablet, laptop)* — OPEN (C2, 21 Nov 2026; D-058, D-065)
**Part A — now (app v11).** First run `sync.bat`, then on each device pull to refresh until Settings shows **v11**.
1. Open https://aaditya-verma.github.io/biology-studio/#cards. You should see **Ch 6 · Weeks 3 to 8**, **Ch 7 · Gut tube and body cavities** and **Ch 8 · Fetus and placenta**, with 4 cards so far: *Foregut, midgut, hindgut*, *A tube on a tube*, *Linings and mesenteries* and *Counting to birth*. The other 19 are drafts, shown only in testing mode.
2. Open *A tube on a tube* on the phone (portrait, then landscape), the tablet (portrait, then landscape) and the laptop. There is no 3D yet: **Try it** and **Watch it** should both be small *Coming soon* strips above the text, in one reading column. On the laptop the chapter list stays on the right. Nothing should overlap or be cut off.
3. Run its Check once: the card text folds away, and you can pass or miss.
4. Open a Ch 5 card (e.g. *Notochord*). Its 3D still works as before.
5. On the laptop, run `python tools/layout-check/check.py` in the repo and send me the summary line. This chat couldn't run it here.
- **Result T3d part A:** ☐ pass ☐ fail · notes:

**Part B — now (after `Bio · Content · C2 round 3`, 21 Nov 2026; ~15 min; same app version, content only).** First run `sync.bat`, then pull to refresh on each device.
1. Open https://aaditya-verma.github.io/biology-studio/#cards (no testing mode needed now). Ch 6, Ch 7 and Ch 8 should list **all 23 cards** (Ch 6: 13 · Ch 7: 5 · Ch 8: 5), none marked draft.
2. On the **phone** (portrait, then landscape), read 3 cards at **General**: *Making the neural plate*, *Body wall and gut wall layers*, *How the umbilical cord forms*. Every name used in a Check or Remember should be explained on the card itself or in brackets where it's used (e.g. "ectoderm (the top germ layer)"). Note any word you'd stumble on.
3. Run the Check on *The neuropores close* and *Diaphragm and its parts* on the **tablet**: nothing in one answer should give away a later question, and you shouldn't be able to put the order steps in order from their wording alone.
4. On the **laptop**, open *Somites: blocks that keep time* › More: the ⚑ newer-evidence line (D-039 a) should read fairly next to the book's 42–44. Same for any ⚑ on *Counting to birth* (D-044 b).
5. Open the two fixed Ch 5 cards: *Gastrulation in one picture* (q1 no longer has "Trophoblast"; q3's steps have no "first/later") and *The disc becomes a pear* (the day drill comes first; General now gives the days with the sizes). Run the day drill once.
6. ~~**D-065:** do you accept the reading?~~ **Answered yes** in chat (21 Nov 2026, 23:52 IST) — D-065 decided. While reading, just note any gloss that feels clumsy.
7. Give **G-Owner** on one card of your choice (Studio › its G-Owner gate › name, role **Owner**, agent `T3d`, tick, **Pass**).
- **Result T3d part B:** ☐ pass ☐ fail · G-Owner: ☐ · D-065: ☑ yes (21 Nov, in chat) · notes:

## T1b. Host shot: Nani Koshika test *(~15–20 min laptop run + ~10 min phone, tablet/laptop)* — PASS 21 Nov 2026 on v6 (M1b, rewritten 21 Nov 2026 for v6, D-051; result D-052)
Host: **Nani Koshika** (D-048), voice Kokoro `af_heart`, route H-a = our 3D model in Blender (D-049). The v5 preview (360p) is not enough: T1b runs on the v6 720p render.
**Before:** Anaconda Prompt → `conda activate bio` → `cd D:\Projects\biology_studio\tools\m1b-host` → **`python m1b.py t1b`** (one run, ~10–20 min, plugged in). If a step fails, paste the last 30 lines into the chat.
1. Upload **the files inside** `tools\m1b-host\out\for_drive\` — not the folder — to Drive › renders › bakeoff › host. It holds v6 only: `M1b-hs01_v6_720p_cap-en.mp4`, `_cap-hi.mp4`, `_clean.mp4`, one `.manifest.json` per clip, `sheet_portrait.png`, `sheet_landscape.png`, the VTTs, `RESULTS.md`. (Optional tidy: move the old v1–v5 files on Drive into a folder `old`.)
2. **Sheet** (`sheet_portrait.png`) on the phone: clearly Nani from the reference (pearl egg body, wine shawl + fringe + pale vines, oval glasses on a chain, book)? Front and side the same character? All 6 faces readable at phone size — warm, curious, delighted, surprised (wide eyes from the lids), thinking, tsk?
3. **Shot** (`…_cap-en.mp4`), full screen, sound on, then sound off:
   - Same Nani in both angles (cut at 2.6 s)? Lips match the words? Blinks natural?
   - Light warm and cinematic; nothing flickers. In the second angle her head stands clear of the lamp (thin dark edge on the body is new — does it look natural or like a cartoon line?).
   - Captions: one phrase at a time, key word "whole body" highlighted, all clear of the app buttons (bottom + right).
   - Voice: pace OK (about 143 wpm), warm, no odd sounds; level about the same as other videos on your phone.
4. **Hindi** (`…_cap-hi.mp4`): "अगर एक चपटी डिस्क को / पूरा शरीर बनाना पड़े तो?" — letters joined right (no boxes, no broken matras), key "पूरा शरीर" highlighted. (Audio is still English — a Hindi voice is a later step.)
5. Against **QR01/QR02** (quality-references §1): would a student stop scrolling? Score 1–5 for look, face, lip-sync, captions.
6. Once on a tablet (both orientations) and once on the laptop: nothing blurry or oversized.
7. Reply in one message: pass / problems + the 4 scores + host OK y/n + notes, and paste `RESULTS.md`. If look or face ≤ 2 after one tune round, the chat brings the paid options (H-c, D-049/D-051 costs).
- **Result:** ☑ pass (owner, phone, 21 Nov 2026 12:44 IST, v6) · scores not given · host OK: not asked (D-049 still proposed, M1b.q4) · notes: shawl does not vanish into the background; caption band clear of the book + hands; voice speed right; keep the band. Kit QA failed host-vs-plate only → v7 rim glow (D-052); v7 needs only the RESULTS gate line + one look, not a new T1b.

## T1. Bake-off: pick the renderer + voice *(~10 min on the phone + ~3 min tablet/laptop)* — OPEN (M1, 20 Nov 2026)
Before: the laptop run is done (20 Nov). Upload `D:\Projects\biology_studio\tools\m1-bakeoff\out\for_drive\` (3 clips, 3 manifests, 2 voices) to Drive › renders › bakeoff. Keep `out\blind_key.json` closed.
1. Open Drive › renders › bakeoff on the phone. **3 clips** of the same 20 s shot: `clip-A … clip-C` (Blender Cycles, Blender Eevee, three.js — in random order). The AI clip (Method C) was not run (6 GB VRAM; D-045) — skip D.
   Known (reviewer, stills): the day-15 stamp says CS07 (should be CS06, fixed in the scene spec later); the colour key and disclaimer are too small to read on a phone — judge the shot, not the key size.
2. Watch each full screen, once with sound off.
2b. Watch your favourite clip once on a tablet (both orientations) and once on the laptop: labels legible, nothing looks oversized or blurry.
3. For each, judge:
   - **Biology:** streak in the caudal midline, node at its cranial tip, mesoderm spreading between the layers, endoderm replacing hypoblast, disc broader cranially, day 15 → 17.
   - **Readable:** day stamp, scale bar, axis gizmo (Cr/Ca/D/V) and the labels, on a phone.
   - **Steady:** the same embryo throughout; no flicker or jumps.
   - **Look:** clear and attractive enough for a medical student to keep watching.
4. Listen to `voice1_kokoro.wav` and `voice2_piper.wav` (20 terms in the order of `D_tts\terms.txt`, then one sentence). Note any term said wrong.
5. Then open `blind_key.json` and reply in the M1 chat with your picks (options in DECISIONS D-024).
- **Result:** ☐ pass ☐ problems — A: ☐ clear ☐ confusing · B: ☐ clear ☐ confusing · C: ☐ clear ☐ confusing · pick (D-024/D-045 O1–O3): ___ · encode E1/E2: ___ · favourite clip: ___ ☐ mix · voice: ☐ 1 ☐ 2 ☐ neither · mispronounced terms: ___ · tablet/laptop: ☐ fine ☐ labels too small/large ☐ blurry · notes:

## T5. Laptop 2 setup — the Professor *(~1 h 30 min on the laptop, once)* — OPEN: repo ready (H1 ✅ 17 Nov 2026); waits for the Professor's GitHub invite
Follow `build/setup-guide.md` §1–§5.
1. `nvidia-smi` shows the GPU; Studio Driver current.
2. `ffmpeg -hide_banner -encoders | findstr nvenc` lists `h264_nvenc`.
3. `python bakeoff.py hw` → no MISSING in `out\hw.json`.
4. `python bakeoff.py quick` finishes; Blender lists OptiX.
5. Claude Project shows today's STATUS (after Sync now).
6. First chat `Bio · Review · Laptop 2 setup` records Laptop 2 in `build/pipeline-reference.md` §1b.
- **Result:** ☐ pass ☐ problems · GPU/VRAM: ___ · missing tools: ___ · quick run minutes: ___ · stuck at step: ___ · notes:

## T2. Concept map explorer *(~10 min, phone + laptop)* — OPEN (K1) · **22 Nov 2026: step 1 problem** — no Back from a *Needs first* link (owner video) → **D-084**, built in U2. The K1 explorer artifact is **retired**: after U2, run steps 1, 3–5 and 6b on the app's **Book map** (`#map`); step 2 + 6 (crosstabs) wait for K3 *Tables* mode; steps 7–8 as written.
1. On the phone open https://claude.ai/artifact/Bg2DUqLgdqC3NgroWMEvin. Book tab: E05 › E05.01 › tap "Primitive streak". Read the page; tap a "Needs first" link, then go back.
2. Crosstabs: Rows = Germ layer, Columns = Day / week; tap Mesoderm × Wk 3; open one concept. Tap ⇄ Swap; try System × Tier.
3. Search "pouch" — the list narrows; clear it. Filters: Importance = exam-high, System = Heart & vessels.
4. Prerequisites tab: are the top 10 sensible "learn first" ideas?
5. Tap ✎ Test, then ✎ on any concept: an edit prompt appears; Copy works (or select by hand).
6. On the laptop: repeat step 2; the concept page opens beside the list.
6b. Rotate the phone mid-task, then open the explorer on a tablet (both orientations, or emulated). Note layout problems only — the explorer was built before the device rule (D-033); A0 brings it up to master plan §8a when it ports it as the Book map.
7. Open `curriculum/roadmap.md`: read Wave 1 (Season 1). Order sensible?
8. Skim one chapter you know well in `curriculum/concept-map.md` — anything missing or wrong?
- **Result:** ☐ pass ☐ problems · coverage: ☐ complete ☐ missing (which?) · crosstabs: ☐ useful ☐ confusing (which?) · navigation: ☐ easy ☐ lost (where?) · roadmap order: ☐ makes sense ☐ change (what?) · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · layout problems (device + screen):

## T3. App shell + 3D + Part 0 cards *(~15 min each: phone, tablet, laptop)* — **T3a ✅ 18 Nov 2026** (shell + Book map) · **T3b ✅ 19 Nov 2026** (3D viewer) · **T3c ✅ 21 Nov 2026** (C1, opened 20 Nov 2026): read the cards in the Studio review pane on each device and give your **G-Owner** on E05.01.01
**T3a — A0 shell (~10 min).** Open the app preview (link in STATUS › Owner reminders) on the phone, then a tablet (or the laptop browser's device mode, marked emulated), then the laptop.
1. **Today:** read it once. Tap **Book map** in the bar (phone) or rail (tablet landscape / laptop).
2. **Book map:** phone — tap Ch 5 → Notochord; tablet/laptop — the chapter list stays on the left, the concept opens beside it (laptop: three panes). Check the concept shows **Confidence ⚑**, **Stage CS07–12 · cited**, **NMC AN** codes.
3. **Back / Up:** use the top-bar ← and ↑, and the phone's Back gesture. At Today, Back once shows "Press Back again to leave"; the app should never close by surprise.
4. **Rotate** the phone and tablet on the Notochord page: same page, same place, layout changes (two columns in landscape).
5. **Crosstab:** Book map → Germ layer × Day/week → tap a cell → its concepts list. Each layer row shows its pattern swatch.
6. **Settings → Colour key:** every layer shows colour + pattern + label with ✓ marks; switch Theme to Dark and look again.
7. **Install** (phone): browser menu → Add to Home screen (works fully once the app is on GitHub Pages; the preview may not offer it).
8. **Testing mode:** Settings → Turn on testing mode → tap a ✎ → the edit prompt opens; Copy works. Turn it off again.
- **Result T3a (18 Nov 2026, on GitHub Pages):** ☑ pass · navigation: ☑ easy · Back/Up: ☑ right · Notochord ⚑ / CS07–12 cited / NMC AN: ☑ yes · crosstab + cell list: ☑ works · colours/patterns readable (light + dark): ☑ yes · install: ☑ worked · testing mode ✎ + Copy: ☑ worked · devices: phone P ☑ L ☑ · tablet P ☑ L ☑ (real/emulated + model not stated) · laptop ☑ · rotate keeps place: ☑ yes · layout problems: none · owner: "All are checked"; more feedback will come during later builds.

**T3b — 3D viewer (V1, ~10 min; cards part follows in C1).** Open https://aaditya-verma.github.io/biology-studio/ on the phone (pull to refresh once so v2 loads), then a tablet (or the laptop's device mode, marked emulated), then the laptop.
1. **Today → Start here → 3D · Two layers become three.** The stage shows `Day 15 · CS06 · ≈0.20 mm`, a scale bar, the Cr/Cd·D/V·L/R key and the disclaimer line.
2. **Day:** drag the slider 15 → 17, then tap ▶ Play. Mesoderm (orange, diagonal lines) spreads between the layers; endoderm (yellow, lines) appears under it; the stamp shows `CS06–07` between key days. On the laptop: `[` `]` step a day, Space plays.
3. **Turn + zoom:** drag to turn, pinch (phone) or scroll (laptop) to zoom, double-tap to reset. The scale bar changes length and label as you zoom.
4. **Layers:** turn Epiblast off, then on. Each toggle shows colour + pattern + name.
5. **Cut:** Cut tab → Cross-section → View → Face the cut: the layers show as stacked bands with labels on them.
6. **Rotate** phone and tablet mid-scene: same day, same view, same tab.
7. **3D list** (3D in the bar/rail) → Axes & planes → Layers → turn on the three planes; then **Days, stages & scale**: play 15 → 18 against the 1 mm ruler.
8. **Settings → Motion → Reduce**, then Play again: it jumps day to day, views snap. Set it back.
9. **fps (phone, once):** open https://aaditya-verma.github.io/biology-studio/?debug=viewer#scene=sc-E00.01.04 → Debug tab → **Measure fps** (~30 s, keep the screen on) → **Copy** → paste into a chat (fills pipeline reference §2).
- **Result T3b (19 Nov 2026, app v3 on GitHub Pages):** ☑ pass · 3D smooth: ☑ yes · labels readable / on the right structure: ☑ yes · cut face clear: ☑ yes · day/stage/size makes sense: ☑ yes · Reduce motion: ☑ works · devices: phone P ☑ L ☑ · tablet P ☑ L ☑ (real/emulated not stated) · laptop ☑ · rotate keeps place: ☑ yes · layout problems: none · fps (step 9): done earlier (phone 60, tablet P 60) · D-036 confirmed · owner: "All pass".

**T3c — cards in the Studio (C1, ~15 min: phone, tablet, laptop).** Open https://aaditya-verma.github.io/biology-studio/?test=1#studio (pull to refresh once so **v6** loads; Settings shows the version). The Studio saves nothing; you only read and judge.
1. **Card list:** 12 cards — 5 Part 0 (E00.01.01–05; E00.01.06 waits for L1, D-042) + 7 Ch 5 Tier A. Each shows its status (Reviewed once both gates pass) and ✓ when card-check is clean.
2. **Phone (portrait, then landscape):** open **E05.01.01 Gastrulation in one picture**. You get the review pane only. Read every line: General and MBBS sentences, facts with their [cites] and marks, misconceptions, Checks (✓ marks the right option), the new **Remember** prompts (r1–r3) and **Where it shows up**. Switch gates with the G-Sci / G-Learn / G-A11y / G-Owner buttons: G-Sci and G-Learn show the reviewers' passes.
3. **Tablet** (portrait: draft above review; landscape: draft │ review): open **E00.01.04 Colour key** and **E05.02.01 Notochord**. Check the colour key now names the three layers in plain words (your D-037 answer) and the notochord gives the book answer with the ⚑ "Newer evidence" line in More.
4. **Laptop** (draft │ review │ sources): skim the other cards. Rotate/resize once mid-card: same card, same pane.
5. **Read for sense, not rules:** would a non-medical reader follow the General text? Is anything wrong, unclear or dull? Note card id + line id (e.g. `E05.01.03 body.general.2`).
6. **G-Owner on E05.01.01:** if you're happy, open its G-Owner gate, put your name, role **Owner**, agent `T3c`, tick the box and tap **Pass** — then tell the next chat "G-Owner pass E05.01.01" (or tap Copy JSON and paste it). Shipping also needs G-A11y, which C1 passed on the text.
- **Result T3c:** ☑ pass (21 Nov 2026, 03:43 IST · by Aaditya, reported in the L1 chat) · G-Owner E05.01.01: ☑ pass · notes: tablet P · Studio · debug overlay covers text top-right; make it tap-to-hide (→ steps.json L1 to-do). ___
- **Result:** ☐ pass ☐ problems · 3D smooth: ☐ yes ☐ stutters (where?) · cards: ☐ clear ☐ too dense · navigation: ☐ easy ☐ lost (where?) · devices: phone P ☐ L ☐ · tablet P ☐ L ☐ (☐ emulated) · laptop ☐ · rotate keeps place: ☐ yes ☐ no · layout problems (device + screen):

## T14. Sources & Resources *(~15 min: phone first, then tablet, then laptop)* — PLANNED (SR1; the SR1 build writes the steps)
What it will cover: tap an Rxx chip on a card → source sheet → Open ↗ / PubMed ↗ open in a new tab and Back returns to the card; a book cite jumps to the Book map; **Resources** in the floating bar — search and filter Research, Back history, every screen size and orientation.

## T4. S1E01 Gastrulation *(~5 min on the phone + ~2 min next day + ~2 min at 7 days; one watch on tablet or laptop)* — PLANNED (R1, L3 player; D-047)
Steps written by the L1 build chat. Watch the MBBS cut; a non-medical friend watches the General cut if possible.
- **Result:** ☐ pass ☐ problems · ☐ biologically right ☐ off at (time) · ☐ watched to the end ☐ drifted at (time) · story ☐ gripping ☐ flat · voice pace ☐ right ☐ fast · 3D ☐ clear ☐ lost track at (time) · General cut understood by a non-medical viewer: ☐ yes ☐ no · Check: __ / __ · 24 h: __ / __ · 7 d: __ / __ · player on tablet/laptop: ☐ good ☐ problems (what?)
