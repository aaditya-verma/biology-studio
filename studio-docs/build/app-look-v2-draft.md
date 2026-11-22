# App look v2 — fonts, surfaces, depth, layouts (plan draft) — **built → design-plan**

> **Built in U2 (22 Nov 2026, `Bio · Build · U2 look tokens`, D-086):** §4.1–§4.3a now live in `build/design-plan.md` §1 (tokens — the owner doc), §4.4 in design-plan §2 (shell row + *As built in U2*) and §3 (D-084 history). Edit there, not here; this file stays as the record of the U1 proposal and its measurements. §4.4's screen rows and §4.5 motion are U3's.

*(Purpose: the plan for the app's v2 look (U1 canvas → U2 tokens → U3 screens) until U2 moves the final values into `build/design-plan.md` §1–§2. Updated: 22 Nov 2026 · Bio · Design · U1 look canvas — committed from the Project ideation draft; owner answers U0.q1–q4 recorded; U1 contrast results (§4.3a); owner check renumbered **T13** (T12 is K3's). Before: 22 Nov 2026 · Bio · Ideation · App look v2 (Project draft only). Owner doc when built: `build/design-plan.md` §1–§2 (+ RULES C8, C13, B3, H5).)*

Decision: **D-077** (numbered D-066 in the ideation draft — taken by X1 Ch 11; then D-070 in the U1 prompt — taken by L2; then D-076 — taken by X1 Ch 16 while U1 ran. `tools/tracker/check.py` now fails a draft whose id clashes.)

**Owner answers (22 Nov 2026, U1 chat):** q1 = **A** (Figtree + Atkinson Hyperlegible Next) · q2 = **DrumPath tonal greys** · q3 = **plain** background · q4 = **S1** (U2 + U3 before GATE; U3 added to GATE's needs).

**U1 canvas:** https://claude.ai/artifact/9ToGW4nXqsRve6KGp7znw9 — 6 screens × 5 device classes × light/dark (60 boards) + font comparison + ladder/contrast board.

## 1. Where we are
- Tokens (design-plan §1): system font stack, flat white cards, 12 px radius, plum accent. Works and passes every check, but reads plain next to DrumPath.
- The depth-look canvas approved on 19 Nov (gradients, shadows, depth on cards + menus) **was never put into tokens**. v2 is that port, plus fonts and layout.
- Hard limits that stay: germ-layer colours only mean layers (B3, D-031), pattern + label always (H5), accent = ring/label never a fill (D-036), 3D stage stays a dark island, 12 px text floor and 44 px taps (C8), offline PWA, optimal layout per device class (C13).

## 2. What to take from DrumPath (reference artifact A4goxQDpCkAaK7wLE81eFx)
| DrumPath pattern | Take it? | How for Biology Studio |
|---|---|---|
| Tonal ladder L0–L4: each nested window one tone darker | **Yes** (q2) | Replaces white cards. Needs a D-031/D-034 colour re-check on every level — done in U1, §4.3a. |
| Edge = 1 px light hairline + soft shadow, no grey borders | **Yes** | `--edge`, `--edge-2` → our elevation tokens e1–e3. |
| One family, heavy uppercase display, tabular numbers | **Yes, adapted** | Heavy display for screen titles only; card and lesson titles stay sentence case (long medical terms). |
| Pill buttons, segmented control, chips | **Yes** | Segments for day / tier / view switches. |
| Frosted sticky header; tab row on wide | **Yes, with fallback** | Blur only over plain page, never over 3D or text; opaque under `prefers-reduced-transparency`. |
| Floating bottom bar with pill indicator (phone) | **Yes** | 5 items: Today · Learn · Map · 3D · More. |
| Floating dock (Back), bottom-sheet menu grid | **Yes** | Thumb reach on phones, only on screens that have a Back (not on the 5 root tabs); rail on tablets/desktop. |
| Big stat numerals (stat tiles) | **Yes** | Today: cards understood, streak, recall %. |
| Snap-scroll deck of cards | **Yes** | Lesson path + "next up" row. |
| Faint line-pattern background | **No** (q3 = plain) | — |
| Green brand accent, pad colours | **No** | Our accent stays plum; colour belongs to germ layers. |

## 3. What the best apps teach (benchmarks, Nov 2026)
- **Material 3 Expressive (Google, 2025):** expressive variants won on preference and found the key button faster → the one main action per screen bigger and differently shaped (not more colour). Floating toolbar for the viewer.
- **Apple Liquid Glass (iOS 26):** criticised for low contrast from transparency → glass only on chrome, never under text; opaque fallback.
- **Duolingo:** display font where you *feel*, legible body where you *read*; chunky "lift" buttons; 16–20 px card radii, pill chips → lift on the primary button only; radii 16/20.
- **Brilliant:** animation reserved for state changes that motivate → motion on Check right/wrong, card status up, streak — nowhere else.
- **Complete Anatomy:** the 3D model owns the screen; menus in a hub; UI can hide on small screens → viewer canvas first, floating bar + sheet, "hide UI" on phones.
- **Atkinson Hyperlegible Next (Braille Institute, 2025):** free (OFL), variable, built for letter distinction (I l 1, 0 O) → body/label font for terms and ids.

## 4. Proposal
### 4.1 Fonts (self-hosted woff2 in `assets/fonts/`, cached by `sw.js`; OFL; registry + THIRD_PARTY before use, F4/H10) — **A picked**
| Option | Display (titles, numbers) | Body + labels | Why / cost |
|---|---|---|---|
| **A (picked)** | Figtree 700–800 | Atkinson Hyperlegible Next (variable) | DrumPath feel on top, best legibility where students read terms. 2 families. |
| B | Figtree | Figtree | Exact DrumPath; less letter distinction. |
| C | Inter Display | Inter | Matches video chapter titles; most neutral. |
Replaces D-034 (5) "system fonts" once U2 ships. Devanagari (later): Mukta or Noto Sans Devanagari. Budget: ≤ 120 KB woff2 total, Latin subset; measured in U2. `font-display: swap`; system stack stays as fallback.

### 4.2 Type scale (rem, scales with OS text size; 125 % stays in the matrix)
- Body: phone 1.0625 rem (17 px) on reading screens (card, lesson), 1 rem UI; tablet/desktop 1.0625.
- Steps ×1.2 (phone) / ×1.25 (tablet+): sm .875 · base · lg 1.25 · xl 1.5 · 2xl 1.875 · display clamp(1.75, 4vw, 2.5) rem.
- Line height 1.5 body, 1.15 display; measure 60–68ch; tabular numbers on stats, days, ids.
- Long terms: `hyphens: manual` + soft hyphens from a term list; mid-word audit stays (L1F).

### 4.3 Surfaces + depth (both themes)
- Ladder L0 page → L1 card → L2 inner → L3 control → L4 pressed; each nested level one tone darker in **both** themes (as DrumPath).
- Elevation e0–e3: e1 card (hairline + 6 px ambient), e2 sheet/menu, e3 floating bar/dock. Pressed = one level darker + scale .97.
- Radii: 20 card · 14 inner · 999 pill · 12 inputs. Primary button: plum, label always, 3 px "lift" shade.
- One soft gradient: Today hero (L1 → L3), never on content cards or layers.
- 3D stage: dark island `#14161A` kept (D-036); floating control bar with opaque fallback. Toggles "on" = ink fill + plum ring (no plum fill).

### 4.3a U1 measured values (proposal for U2; WCAG 2.x ratios, every level)
| | L0 | L1 | L2 | L3 | L4 |
|---|---|---|---|---|---|
| Light | `#F3F1EC` | `#EBE9E3` | `#E3E1DA` | `#DBD8D0` | `#D2CFC6` |
| Dark | `#252930` | `#1F2228` | `#1A1D22` | `#16181C` | `#121417` |
- **Dark:** every D-031/D-034 value passes on every level as is (worst: ecto edge `#0082CA` 3.51 on L0; accent-text `#C77BA2` 4.72 on L0; control border 3.34 on L0).
- **Light: the D-034 edges fail from L1 down** (e.g. 3.06 on L2, 2.57 on L4), so do plum text (4.20 on L3) and the control border (2.94 on L2). Proposed (fills, patterns, labels unchanged): edges epi `#146DA0` · hypo `#45723D` · ecto `#006CA9` (ecto now needs an edge on light) · meso `#AB4B00` · endo `#75680F` · crest `#007656` · ctx `#606875` — all 3.60–5.00; new light `--accent-text #873E66` (4.63–6.39); `--line-strong #747169` (3.13–4.32). Ink 10.8+, muted 4.57+ (L4 worst). White on accent 6.0 unchanged. Accent as ring/fill ≥ 3.84.
- Heat scale re-based on the ladder: light `#E3E1DA #C9C6BD #A9A59B #66625A #3D3F45` (ink on 0–2, `#F3F1EC` on 3–4); dark `#2A2E35 #3E434C #596069 #9AA0AA #DCDDE0` (light ink on 0–2, `#14161A` on 3–4); all ≥ 5.0:1.
- These are a D-031/D-034 change: recorded as proposed in D-077; U2 re-runs the CIEDE2000 + colour-vision check on the new edges before they ship.

### 4.4 Layout per device class (C13)
| Screen | Phone portrait | Phone landscape | Tablet | Desktop |
|---|---|---|---|---|
| Shell | Floating bottom bar; Back dock on non-root screens | Side strip (icons), bar hidden | Rail (icons + labels) | Rail + header tabs |
| Today | Hero (due + Start) → stat tiles → continue → next-up deck | Hero left, tiles + deck right | Hero + tiles + continue + deck (tp); 2 cols (tl) | 3 cols: hero + tiles · deck · continue + progress |
| Card | Title → 3D → text → Check (floating CTA) | 3D left fits height · text right | 3D │ text (study mode) | 3D │ text │ sources/related |
| Lesson path (L2) | Vertical path of sittings | Horizontal path + due row | Path │ selected sitting | Path │ sitting │ due |
| 3D viewer | Canvas, floating bar, sheet; Back dock above sheet | Strip + canvas + layer strip | Canvas │ panel | Canvas │ panel, hover + keys |
| Map | Drill-down list | List │ detail | Two panes (+ heatmap on tl) | Three panes |
| Settings | Look · Your data · Study | 2 columns | One column (tp), 2 (tl) | 3 columns |

### 4.5 Motion
150–250 ms, ease-out; spring only on Check result, status up, streak. Off with Motion = reduce. No flashing (H5).

## 5. Steps, dependencies, schedule
| Id | Step (chat) | Needs | Lock | Est | Gates · check |
|---|---|---|---|---|---|
| U0 | Ideation (`Bio · Ideation · App look v2`) | — | no | done | owner answers q1–q4 (22 Nov) |
| U1 | Look canvas (`Bio · Design · U1 look canvas`) | U0 answers | **no** (artifact only) | 1 chat | G-Art, G-A11y · **T13** owner pick |
| U2 | Tokens + fonts + shell (`Bio · Build · U2 look tokens`) | U1 + T13, L2 | **yes** | 1–2 chats | G-Eng, G-Art, G-A11y; D-031/D-034 re-check; layout-check all sizes × 100/125 % × themes · **T13b** |
| U3 | Screen pass — Today, Card, Lesson path, Viewer bar, Map, Settings (`Bio · Build · U3 look screens`) | U2 | **yes** | 1 chat | same + stills re-baseline after review · **T13c** |

**S1 (picked):** U2 + U3 take the lock right after V3 (the lock holder now), before W3 and GATE, so the 7 use days are on the new look. GATE slips ~1–2 days; U3 is in GATE's `needs`.

**Scheduling checks before each step:** (1) prior step pushed and visible in the laptop clone (`git log -1` = Pages version); (2) build lock free in STATUS (U1 needs none); (3) blocking inputs closed: U2 ← T13 and L2 owner check; (4) `python tools/tracker/check.py --next` shows the step as *now*.

## 6. Owner inputs — answered 22 Nov 2026 (see top). Left: **T13** (pick or tweak the canvas).

## Sources
- Material 3 Expressive research — https://design.google/library/expressive-material-design-google-research
- Liquid Glass legibility — https://infinum.com/blog/apples-ios-26-liquid-glass-sleek-shiny-and-questionably-accessible/
- Duolingo type — https://www.designyourway.net/blog/duolingo-font/
- Brilliant motion — https://rive.app/blog/how-brilliant-org-motivates-learners-with-rive-animations
- Complete Anatomy — https://pmc.ncbi.nlm.nih.gov/articles/PMC6920010
- Atkinson Hyperlegible Next — https://fonts.google.com/specimen/Atkinson+Hyperlegible+Next
