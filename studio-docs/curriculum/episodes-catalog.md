# Episode catalog & how to add an episode — draft

Episodes are story-led 3D explainers. The app stores metadata, card tags, the cited script and Drive file ids — never book text or figures (RULES §G). Ids `S<season>E<nn>` are never reused or renumbered.

## How to add an episode
1. **In Studio (draft):** + New episode → pick a story format, the chapter, then tag cards none → **core** (×2) → **support** (×1).
2. **In this catalog (permanent):** add a row with the next free id; copy §5 to `content/episodes.js`.

**Tagging rules:** core = cards the episode can't be followed without; support = used in passing; tag what it actually needs, not every easier card; tags may point at unwritten cards ("Coming in Tier X"); tier = highest tier among core tags.
**Fact rule:** every script line cites a section; uncited lines are ≈ and block "final" (`factChecked` = false).
**Ready to watch:** weighted share of core/support cards Understood → Ready · In reach · Learning · Locked. Never blocks; offers a 30-second recap.

## 1. Catalog by season
### Season 1 — "How does a flat disc become a body?" (Part 1)
| Id | Title | Format | Length | Cards (★ core) | Fact-checked | Notes |
|---|---|---|---|---|---|---|
| S1E01 | Gastrulation | Journey (ride with an epiblast cell) | ~90–120 s | ★E05.01.02, ★E05.01.03, ★E05.01.04, E05.02.01, E00.01.04 | ≈ (not written) | Pilot (P1, R1) |

## 2. By system / thread · System × Tier counts
Filled as episodes are added.

## 3. By story format
| Format | Episodes |
|---|---|
| Journey | S1E01 |
| Mystery | — |
| Factory | — |
| Character | — |
| Countdown | — |

## 4. Card → episodes (unlock count)
Computed by I1 + this catalog. **Cards with no episode yet** and **top-10 cards by unlock count** go here.

## 5. Data for `content/episodes.js`
```js
// [id, title, format, seconds, coreCards, supportCards, factChecked]
const EPISODES = [
  ['S1E01','Gastrulation','journey',0,['E05.01.02','E05.01.03','E05.01.04'],['E05.02.01','E00.01.04'],false],
];
```
