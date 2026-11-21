# Setup guide — run Biology Studio on a second laptop

*(Purpose: §0 = the reviewer's zero-setup start; §0a–§8 = full setup for a collaborator's Windows + NVIDIA laptop, and how two people share the project. Updated: 21 Nov 2026 · Bio · Build · H2 reviewer mode — §0 Reviewer: start here (D-060, D-061). Before: 17 Nov 2026 · Bio · Build · H1 shared repo — repo live, §6a commit route (D-027).)*

**Reviewing only?** Read **§0** and stop there — nothing to install.

**Who §0a–§8 are for:** a collaborator (first: the Professor, at Level 3) who joins the owner (Aaditya) on one **shared** project (D-025). Same kind of machine: Windows laptop with an NVIDIA GPU.
**Time:** about 1 h 30 min (mostly downloads) + 40 min if you also set up AI video. **Disk:** ≥ 40 GB free (≥ 20 GB without AI video).
**Cost:** free tools only, except your own Claude plan (§1). Nothing paid without the owner's OK (RULES §F).
**Shareable copy:** the owner sends you a Doc made from this page; this markdown is the source of truth — if they differ, this page wins.

---

## 0. Reviewer: start here (no setup, ~5 min)
*For the Professor (Komal Verma) as the human science reviewer (D-060). You need a browser and a free GitHub account — nothing else: no install, no repo, no Claude Project, no book PDF.*

1. **Open the app:** https://aaditya-verma.github.io/biology-studio/#review — on your phone or laptop (Chrome or Edge). On a phone you can keep it: browser menu ⋮ → **Add to Home screen** (or **Install app**).
2. **Take the tour** — three short screens open by themselves the first time. You can see them again from the Review page (**Show me around again**).
3. **Sign in to GitHub once** in the same browser: github.com → **Sign in** (your username `komalverma00500-byte`). The app never asks for your password; GitHub does, on its own page.
4. **Review a card:** Review → **To review** → open the top card → read it → tick what looks right → pick **✓ Looks right**, **✎ Needs a fix** or **? Question** → for ✎ or ? write a short note (a page number or source helps) → **Send on GitHub**. A GitHub page opens with everything filled in → check it → press **Create**. That's it — it isn't sent until you press Create.
5. **Follow it:** **My feedback** shows each thing you sent: *Sent — waiting for Aaditya* → *Being fixed* → *Fixed in app update N* (or *Done*, *Answered*, *No change needed*; tap one to read the reply on GitHub). A fixed card comes back under To review for a last look. On a phone, stay in the browser if GitHub offers its app. **What's new** lists new or changed cards and the team's updates; **All updates** shows the full list in plain words.

**Good to know**
- Your ✓ is the **human science check** for that version of the card. Aaditya decides on each ✎ before anything changes (D-060).
- Feedback on GitHub is **public**. Write as you would on a public page: no patient details, and **don't paste book text or figures** — a chapter and page number is enough (RULES §G).
- Your email address is not in the app or the repo.
- Something general (the app, a screen, an idea)? Review → My feedback → **Send general feedback**.

**If something looks wrong**
| You see | Do this |
|---|---|
| A blank or old page | Pull down to refresh (phone) or press Ctrl + Shift + R (laptop). |
| "GitHub asks us to wait a little" | Normal — GitHub limits how often the app may ask. Your list is still shown; it checks again later by itself. |
| You sent something but it's not in My feedback | Did you press **Create** on GitHub? Then tap **Check for news**. |
| GitHub says "Sign in" | Sign in, then press **Send on GitHub** in the app again — your answers are still there. |

*Later (Level 3), if you want to build too: the rest of this guide, from §0a.*

---

## 0a. How the sharing works (read once)
| Thing | Shared how | Notes |
|---|---|---|
| **Project docs** (plans, rules, status…) | One copy in the private GitHub repo `aaditya-verma/biology-studio`, folder `studio-docs/`; each person's Claude Project reads it via **GitHub → Sync now** | Chats change docs only by a git commit (§6a). |
| **Claude Project** | Each person has their **own** Project "Biology Studio" with the same custom instructions | Sharing one Project needs a Claude Team plan (paid option in D-025). |
| **Code + tool kits** | GitHub repo `biology-studio` (`tools/`, later the app) | Owner adds you as a collaborator. |
| **Media** (renders, audio, research files, index data) | Owner's Google Drive folders shared with you as **Editor** | Folder name today: *Embryo Studio* (may be renamed *Biology Studio*). |
| **The book (Langman 14e PDF)** | **Not shared.** Use your own licensed copy, kept private in your own Drive | Copyright (D-005). Only derived data (index, maps) is shared. |
| **Heavy apps + model weights** | Installed on each laptop; never in the repo | Blender, ComfyUI, TTS voices (RULES F4). |
| **Who decides** | The owner logs decisions (DECISIONS) and passes G-Owner | You propose; your chats end with a handoff the owner can act on. |
| **Building** | **One build chat at a time across both people** — take the build lock in STATUS first (RULES I8) | Ideation, Research and Review chats don't need the lock. |

---

## 1. Accounts (10 min)
1. **Google account** — you have one. Tell the owner the address to share Drive folders with.
2. **GitHub** (free): github.com → Sign up. Send the owner your username.
3. **Claude:** claude.ai → sign up. The free plan works for short chats but hits limits quickly on this project's long reads. *Paid suggestion (RULES F2):* Claude Pro, about $20/month (less if paid yearly) — more usage per session; the free alternative is the free plan with shorter, fewer chats.
4. **Hugging Face** (free, optional): only if your GPU can't run the AI video model and you need the online fallback (§5 step 7).

## 2. Accept the invites (5 min, after the owner sends them)
- Drive: the shared folders appear under **Shared with me** → right-click each → **Organize › Add shortcut** → My Drive, so they show in one place.
- GitHub: accept the `biology-studio` collaborator email (github.com/aaditya-verma/biology-studio/invitations).
- GitHub → Settings → Applications → **Claude** → make sure Claude may use `biology-studio` (needed for Project sync and route A in §6a). If your account has no Claude app yet, it is added when you connect GitHub in claude.ai (§4).
- Google Cloud test user: only later, when the app's Drive sync is built (D1). Nothing to do now.

## 3. Your copy of the book (5 min)
Put your own Langman's Medical Embryology 14e PDF in **your** Drive in a private folder `Biology Studio – private/book/`. Never upload it to the shared folders, the repo, or a shared chat. Chats that need it (I1 index, C1 cards) will ask you to attach it.

## 4. Claude Project (15 min)
1. Install the **Claude desktop app** for Windows (claude.ai/download) and sign in — chats can then read and write files in your laptop's Studio folder.
2. claude.ai → **Projects → + New Project** → name **Biology Studio**.
3. **Set project instructions:** paste the quoted block from `claude/INSTRUCTIONS.md` §6 (the owner sends it, or copy it from the repo). Don't edit it — both people use the same text.
4. **Add the docs:**
   - claude.ai Settings → Connectors → **GitHub → Connect**. In the Project's knowledge: **+ → GitHub** → repo `aaditya-verma/biology-studio` → tick folder `studio-docs/` only → Add. **Press Sync now before every new chat** (it does not update by itself).
   - Don't upload docs by hand — an uploaded copy goes stale and confuses chats.
5. In the desktop app, connect your Studio folder (§5 step 2) when a chat asks for it.

## 5. Laptop setup (≈ 1 h; Windows, NVIDIA)
Use **Anaconda Prompt** (or Miniconda Prompt) for every command. After installing anything with `winget`, close and reopen the prompt.

1. **Check the GPU.** Run `nvidia-smi`. Note the GPU name, driver version and memory (VRAM). Update the driver if it is old: NVIDIA app → Drivers → **Studio Driver** (more stable for Blender than Game Ready).
2. **Make your Studio home.** Any drive works. Owner uses `D:\Projects\biology_studio`; if you have no D: drive use `C:\Projects\biology_studio`. Inside it:
   ```
   tools\     kits and scripts (from the repo)
   apps\      Blender portable (optional), ComfyUI — never in the repo
   models\    voices, AI weights — laptop only
   repo\      the biology-studio repo clone
   ```
   Wherever a doc says `D:\Projects\biology_studio`, use your own Studio home.
3. **Install the tools** (one line each):
   - Python: `winget install Anaconda.Miniconda3` (skip if Anaconda is installed)
   - Git: `winget install Git.Git`
   - ffmpeg: `winget install Gyan.FFmpeg`
   - Node.js: `winget install OpenJS.NodeJS.LTS`
   - eSpeak NG (voice helper): `winget install eSpeak-NG.eSpeak-NG`
   - Blender 4.2 LTS or newer: `winget install BlenderFoundation.Blender` (or blender.org → portable zip into `apps\`)
4. **Python environment** (≈ 10 min, ~3 GB):
   ```
   conda create -n bio python=3.11 -y
   conda activate bio
   pip install torch --index-url https://download.pytorch.org/whl/cu124
   pip install pillow numpy soundfile kokoro piper-tts
   ```
5. **Get the repo.** `cd <Studio home>\repo` → `git clone https://github.com/aaditya-verma/biology-studio.git` (a browser window asks you to sign in to GitHub once). Kits are then in `repo\biology-studio\tools\` — e.g. `tools\m1-bakeoff`. Run `sync.bat` in that folder to pull the latest.
6. **Check everything works** (`conda activate bio`, then `cd` into the kit folder):
   - `ffmpeg -hide_banner -encoders | findstr nvenc` → must list `h264_nvenc`.
   - `python bakeoff.py hw` → writes `out\hw.json` (GPU, VRAM, CPU, RAM, Blender, ffmpeg). Any "MISSING" → see §8.
   - `python bakeoff.py quick` → ~5 min test render of every method (every 12th frame).
   - Blender → Edit › Preferences › System › Cycles Render Devices → **OptiX** lists your GPU.
7. **Optional — AI video (≈ 40 min, ~16 GB):** follow the kit's `C_ai\README.md`; put ComfyUI in `<Studio home>\apps\ComfyUI`. Needs about 8 GB VRAM; if it runs out of memory, use the free Hugging Face fallback described there.
8. **Report back:** send `out\hw.json` to the owner (or open a chat, step 9). It goes into `build/pipeline-reference.md` as **Laptop 2**; owner check **T5** is then done.
9. **First chat:** in your Project, start `Bio · Review · Laptop 2 setup` and say: *"Read claude/STATUS.md and build/setup-guide.md. My laptop setup is done — read out\hw.json from my Studio folder, record it as Laptop 2 in build/pipeline-reference.md, tick T5, and tell me what I can work on."*

## 6. Working together (every day)
- **Before a chat:** double-click `sync.bat` in your clone (pulls code) · **Sync now** in the Project (docs) · read STATUS (what's next, who holds the build lock).
- **Chat names:** `Bio · <Type> · <Step>` as usual. One step per chat.
- **Build chats:** take the lock first (RULES I8): the chat writes `Build lock: <your name> · <chat name> · <date, time IST>` in STATUS; it releases it at the end. Lock held by the other person → don't build; do Ideation/Research/Review instead.
- **Code and docs:** pull before, commit + push after — by route A or B below. Never commit `out\`, `apps\`, `models\` or anything from the book (`.gitignore` blocks the usual ones).
- **End of chat:** the usual end-of-chat duties (INSTRUCTIONS §4); log lines say who (`· by Prof` / `· by Aaditya`).
- **Decisions:** your chat may propose a D-entry marked *proposed*; the owner confirms it.

### 6a. How a chat commits doc changes (RULES I8, D-027)
Docs exist **only** in `studio-docs/` of the repo. Project knowledge is a read-only mirror. A chat never changes a doc by uploading it or writing it into Project knowledge.

**Route A — chat pushes itself (default).** Works in any chat whose Claude account can use the repo (Claude GitHub app has `biology-studio` ticked).
1. Chat attaches the repo (`aaditya-verma/biology-studio`, push access) and makes a shallow clone in its own workspace.
2. It edits `studio-docs/<path>` in the clone (the same paths as in Project knowledge).
3. `git pull --rebase`, then one commit to `main`: `<step>: <what changed> · by <name>` (e.g. `K1: concept map rows Ch 5 · by Aaditya`), then push. Never force-push. On a conflict, keep both people's lines and say so.
4. Tells you: **press Sync now**. The next chat then sees the change.

**Route B — via your laptop clone (if A can't attach the repo).** Needs the desktop app with your Studio home connected.
1. You double-click `sync.bat` in `<Studio home>\repo\biology-studio` (pull).
2. Chat writes the changed files into `repo\biology-studio\studio-docs\…` on your laptop.
3. You run `sync.bat "K1: concept map rows · by Aaditya"` (commit + push) — the chat gives the exact line — then **Sync now**.

**No route (e.g. phone only).** End with a **handoff note** (templates §10); the next chat with a route applies it.

`sync.bat` also takes `--dry-run` (shows what would be committed, changes nothing).

## 7. What never to do
- Share the book PDF, book sentences, figures or page photos anywhere shared (RULES §G).
- Put NC/ND sources or Z-Anatomy meshes in the repo or app (RULES G4–G5).
- Renumber or reuse an id (RULES A2).
- Build while the other person holds the build lock.

## 8. Troubleshooting
| Problem | Fix |
|---|---|
| `'xyz' is not recognized` after a winget install | Close and reopen the prompt. Still missing → reinstall and tick "Add to PATH". |
| `bakeoff.py hw` says Blender MISSING | Install to `C:\Program Files\Blender Foundation\…`, or put the portable folder in `<Studio home>\apps\blender-…\`. |
| No `h264_nvenc` | Update the NVIDIA driver; check `nvidia-smi` works. The kit falls back to x264 (slower, same quality). |
| OptiX not listed in Blender | Update to the Studio Driver; older (GTX) cards use CUDA — the kit falls back automatically. |
| `torch` says CUDA not available | `pip uninstall torch -y` then the `cu124` install line again (in the `bio` env). |
| three.js step fails on first run | It installs three.js + Playwright itself; run `npx playwright install chromium` in `B_three\` if asked. |
| Out of GPU memory (AI video) | Close games/Chrome; use the online fallback in `C_ai\README.md`. |
| Claude can't see my files | Open the chat in the desktop app on this laptop and connect the Studio folder. |
| Project docs look old | Press **Sync now** in Project knowledge. Still old → the change wasn't pushed: check the repo's commits on github.com. |
| `sync.bat` says pull failed | You have local edits that clash. Don't delete anything; open a chat with route B and ask it to merge. |
| Chat can't attach the repo (route A) | GitHub → Settings → Applications → Claude → Configure → tick `biology-studio`. Meanwhile use route B. |
