# Status — updated 28 Nov 2026

*(Purpose: now · next · lock — nothing else (D-040). Every step's status, blocks, pendencies and what you owe: `build/steps.json`, drawn at https://aaditya-verma.github.io/biology-studio/#progress. Finished work: `logs/build-log.md`. Updated: 28 Nov 2026 · Bio · Build · M1b v8 install (stopped at start checks, M1V8 parked, lock released). Before: 28 Nov 2026 · Bio · Fix · GPU first (D-110; STATUS cut to one screen — the old Now lines are in the build log). Before: 27 Nov 2026 · Bio · Build · W6 desk.)*

## Lock
- Build lock: free since 28 Nov 2026, 03:18 IST (released by `Bio · Build · M1b v8 install`, run stopped before install; laptop clone, route B).

## Now
- **⚠ Laptop drives not safe — M1V8 parked** (28 Nov, `Bio · Build · M1b v8 install`): during the start scans Windows found and repaired NTFS corruption on **D:** 61 times; the Seagate (D:) has 147 bad-block events and **F:** had lost writes on 25 Nov. Get-PhysicalDisk still says Healthy. No GPU step (M1V8, R1) until **M1V8.q1**: back up D:, `chkdsk D: /scan`, plan a new drive, check F:. No tracked repo file is damaged; cloud-clone steps (R1T) can go on.
- **GPU first — D-110** (28 Nov, `Bio · Fix · GPU first`, route A, docs + steps.json): lock lane after W6 = **M1V8 → R1T → V4 → SR2 → FA → L3**; new **R1T** builds R1's tools (render check, mix, chapters, renditions) in the cloud; **R1** renders on the GPU lane with no lock once T4 part A, T1 and R1T clear. D: drive cleared (wrong — see the line above) — GPU steps start with disk-health, D: ≥ 30 GB, git fsck and GPU-idle checks.
- **Waiting on you:** P1 + P1F → **T4 part A + P1.q2** (~6 min); M1 → **T1** (pick O/V/E, D-045); W6 → T13d; U3b → T13c; SR1 → T14; and the older checks on Plan › Your inputs.

## Next (in order)
<!-- next:auto -->
Schedule (auto · check.py --next · est. from 28 Nov; order fixed, dates move):
- Lock: R1T [Code] ~28 Nov next → V4 [Code] ~29 Nov → SR2 [Code] ~29 Nov → L3 [Code] ~29 Nov
- GPU: R1 [Code] ~29 Nov next
- You (no lock): M1·T1 [Cowork] ~28 Nov now → H1·T5 [Cowork] ~28 Nov now → H2·T10 [Cowork] ~28 Nov now → +14 more now → FD [Cowork] ~30 Nov next → GATE [Cowork] ~5 Dec
- Critical path: GATE (ends ~5 Dec)
- Your inputs first: T2 (unblocks 48) · H1.q4 (unblocks 47) · T5 (unblocks 47)
- Run in: R1T → Code (takes the build lock: changes app or tools, runs the checks, pushes) · R1 → Code (renders on the laptop GPU: desktop app with the laptop shell on)
- Lock: free
<!-- /next:auto -->
1. **R1T** — `Bio · Build · R1T render tools` [Code] (cloud clone, route A), then **V4**, **SR2** in the lock lane.
2. You: **M1V8.q1** (fix the laptop drives) — M1V8 (parked) and R1 wait on it; then **T4 part A + P1.q2** and **T1** for R1.
3. After M1V8.q1: unpark **M1V8** (`Bio · Build · M1b v8 install`, laptop clone, route B, prompt in master plan §13, sync line ends `--lock-ok`); **R1** on the GPU lane after T4 part A, T1 and R1T.
