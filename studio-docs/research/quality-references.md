# Quality references — the bar we aim for

*(Purpose: owner-supplied reference videos, what they do well (measured), and what that means for our pipeline. Updated: 20 Nov 2026 · Bio · Fix · Visual style port (QR03, D-041). Before: 18 Nov 2026 · Bio · Fix · doc reconcile — ported from the uploaded Project copy (written 17 Nov 2026 · Bio · Ideation (quality refs)); owner answers logged as D-032. Reference only — third-party, AI-generated Instagram reels: never reuse frames, audio, characters or captions (RULES §G). Keep the files in Drive › research/quality-refs/, not in the repo.)*

## 1. The references
| Id | What it is | Measured |
|---|---|---|
| **QR01** | Reel (svertoc.live, labelled "AI content"): two anthropomorphic tigers in kurtas in a Rajasthani bazaar at blue hour; comedy about saying "uncle" in Hindi (चाचा / चम्मच / चाँदी mix-ups) | 9:16 · 720×1608 · 60 fps · 10.4 s · ~8 Mbps · ~12 cuts (avg ~0.8 s per shot, shot–reverse-shot dialogue) · audio mean ≈ −19 dB, peak ≈ −2.7 dBFS |
| **QR02** | Reel (ai.video.creator.ai, "AI content"): "Sheru bhai" — a tiger in a black suit, then a white lion in a white suit and sunglasses in a gold palace hall, then a gold helicopter reveal at an airport | 9:16 · 720×1608 · 60 fps · 10.7 s · ~8 Mbps · 3 shots (~3.2 s, ~4.5 s, ~2.7 s), each an escalation · speech with short pauses · audio mean ≈ −18 dB, peak ≈ −1 dBFS |
| **QR03** | YouTube Short (@MedNurseAcademy97, https://youtube.com/shorts/DI7oat-HzhY; owner-supplied 19 Nov 2026): embryology-style macro tissue piece — glassy translucent tissue, warm pink grade, macro depth of field, floating dust, colour-coded layers, 6 chapters of ~8 s with top-centre thin-caps titles | File: Drive › research/quality-refs/ "QR03 - reference reel (screen recording 19 Nov 2026).mp4" (id 1ODMlQx1XElrP4DBhL25dWybdOOIDKLhi, 47.6 MB, owner's phone screen recording). Not measured yet — a laptop chat runs ffprobe/ffmpeg for size, fps, length, cuts, loudness (screen recording: fps and bitrate reflect the recorder, not the original) |

## 2. What makes them work (the bar)
1. **Photoreal, cinematic look:** dense fur and fabric detail, warm practical lights (lanterns, chandeliers), blue-hour or golden light, shallow depth of field with soft bokeh, a filmic colour grade.
2. **Characters you remember:** one strong character per shot, the same identity across cuts, expressive faces, lip-synced speech, a name ("Sheru bhai") and a look (suit, sunglasses).
3. **Local and relatable:** Indian settings, Hindi/Hinglish dialogue, everyday humour (language mix-ups, flexing).
4. **Hook in the first second, payoff by 10 s:** QR01 = a question then rapid back-and-forth; QR02 = escalation ending on a big visual reveal.
5. **Short-form editing:** 9:16, subject centred in the safe zone, cuts every ~0.8–4 s, no dead air.
6. **Kinetic captions (QR01):** one phrase at a time, bold serif with dark outline, key word in gold, centre-low; Devanagari and Latin mixed.
7. **Loud, clean mix:** voice forward, peaks near 0 dBFS (louder than our −14 LUFS/−1 dBTP target, which stays).

## 3. What we adopt (D-032, decided 17 Nov 2026)
1. **All four qualities** are the bar: cinematic look, character + humour, local language, short-form pacing.
2. **Science shots:** cinematic microscopy look (subsurface tissue, translucent membranes, volumetric light, depth of field, graded palette) — but **exact, our 3D only** (RULES H9). Render quality target for M1/V1.
3. **Host character, chosen per episode** (audience profile `host`): **cell/embryo character (default)** · animal · stylised human · none. The host asks the question, reacts, jokes; it never shows anatomy; designs are our own originals; AI-made host shots are credited.
4. **Language per episode** (profile `language`): **English (default)** · Hinglish · Hindi. Script-first: a new language = new voice + captions, no re-render.
5. **Short profile** (9:16, ≤ 60 s): hook ≤ 1 s, cuts every 1–3 s, kinetic captions (styled subtitles, toggleable, key word highlighted, Latin + Devanagari), humour only if the science stays exact (D5), ends with "full episode in the app". Explainer/MBBS cuts keep learning pace (hold 1–2 s after each reveal).
6. **M1b Host shot** (after M1 numbers): one 5-s 9:16 shot of the default cell/embryo host, consistent across 2 angles, synced to one spoken line, cinematic light — made locally (character sheet → image-to-video → lip/beat sync → our TTS), judged against QR01/QR02 in owner check T1b. Candidates and licences from the registry § Tools / Hugging Face; paid tools (e.g. Kling, Veo, Runway) only suggested, with checked cost, if local can't reach the bar (RULES F2).
7. **QR03 look (D-041, 20 Nov 2026):** adopted as `build/visual-style.md` — glassy SSS tissue, warm grade (background + ctx only), macro DOF, background dust, chapter titles, 6 × 8 s Short grammar. Science checks: playbook §2 G-Sci video checklist.

## 4. Open
- Host design: the M1b chat proposes 2–3 cell/embryo host concepts (name, look, voice, personality) for the owner to pick.
