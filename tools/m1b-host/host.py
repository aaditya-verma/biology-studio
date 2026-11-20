"""M1b host shot runner — Nani Koshika (D-048) via route H-a, 3D in Blender (D-049).
Owner docs: studio-docs/build/studio-playbook.md §5b · build/visual-style.md · build/pipeline-reference.md · README.md here.
Run from this folder in an Anaconda Prompt (`conda activate bio`):
  python host.py all                  check → tts → sheet → shot → captions → encode → report
  python host.py all --preview        540×960, 16 samples (all frames) — a ~5 min smoke test
  python host.py sheet --only doubt   one expression only (front, side, neutral, warm smile, surprise, doubt, laugh, thinking)
  python host.py shot --only A        camera A only (A | B)
  python host.py captions --safe      burn safe-zone guides onto the frames (debug)
  python host.py report | selftest | check
Flags on every step (RULES I5): --dry-run (print the plan, run nothing) --debug --only <id> --preview.
Edit values in spec.py (# EDIT:). Outputs: out\\<SHOT_ID>[ -preview]\\ (never committed; upload for_drive\\ to Drive › renders/bakeoff/host)."""
import argparse, glob, hashlib, json, os, platform, shutil, subprocess, sys, time
from datetime import datetime

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
import spec  # noqa: E402

STEPS = ["check", "tts", "sheet", "shot", "captions", "encode", "report"]
SHEET_VIEWS = ["front", "side"] + list(spec.EXPR.keys())
A = None  # parsed args
T = {}    # step timings (s)


def log(*a):
    print("[m1b]", *a, flush=True)


def dbg(*a):
    if A and A.debug:
        print("[m1b:debug]", *a, flush=True)


def out_dir():
    d = os.path.join(KIT, "out", spec.SHOT_ID + ("-preview" if A.preview else ""))
    os.makedirs(d, exist_ok=True)
    return d


def P(*parts):
    return os.path.join(out_dir(), *parts)


def PD(*parts):
    """Path in out_dir, parent folder created."""
    p = P(*parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


def jload(p, default=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def jsave(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)


def run(cmd, **kw):
    log(">", " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd))
    if A.dry_run:
        return subprocess.CompletedProcess(cmd, 0, "", "")
    r = subprocess.run(cmd, **kw)
    if r.returncode != 0:
        raise SystemExit(f"[m1b] command failed ({r.returncode}): {cmd[0]} — rerun with --debug; see the log above")
    return r


def cap(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return f"n/a ({e.__class__.__name__})"


def sha(path, n=16):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:n]


def find_blender():
    # EDIT: add your Blender path if it lives elsewhere
    for c in [os.environ.get("BLENDER", ""), shutil.which("blender") or "",
              *glob.glob(os.path.join(KIT, "..", "..", "..", "..", "apps", "blender*", "blender.exe")),
              *glob.glob(r"D:\Projects\biology_studio\apps\blender*\blender.exe"),
              *glob.glob(r"C:\Program Files\Blender Foundation\Blender*\blender.exe")]:
        if c and os.path.exists(c):
            return os.path.abspath(c)
    return None


def ref_path():
    p = os.path.normpath(os.path.join(KIT, spec.REFERENCE))
    return p if os.path.exists(p) else None


def n_frames():
    return int(round(spec.DURATION_S * spec.FPS))


def frame_size():
    return spec.PREVIEW if A.preview else spec.MASTER


# ---------------- steps ----------------
def step_check(_):
    from PIL import features
    rep = {
        "checked": datetime.now().isoformat(timespec="minutes"),
        "blender": find_blender() or "MISSING — set BLENDER=...\\blender.exe or put Blender 4.5 in apps\\",
        "ffmpeg": (cap(["ffmpeg", "-version"]).splitlines() or ["MISSING"])[0] if shutil.which("ffmpeg") else "MISSING",
        "gpu": cap(["nvidia-smi", "--query-gpu=name,driver_version,memory.total,pstate,power.draw,temperature.gpu", "--format=csv,noheader"]) if shutil.which("nvidia-smi") else "n/a",
        "python": sys.version.split()[0],
        "pillow_raqm": features.check("raqm"),
        "reference": ref_path() or f"MISSING ({spec.REFERENCE})",
    }
    try:
        import kokoro  # noqa: F401
        rep["kokoro"] = getattr(kokoro, "__version__", "installed")
    except Exception as e:
        rep["kokoro"] = f"MISSING ({e.__class__.__name__}) — pip install kokoro soundfile"
    import captions
    c = captions.Captioner(frame_size(), [{"w": "test", "t0": 0, "t1": 1}])
    rep["captions"] = c.report()
    jsave(P("check.json"), rep)
    for k, v in rep.items():
        log(f"{k:12} {v if not isinstance(v, dict) else json.dumps(v, ensure_ascii=False)}")
    bad = [k for k, v in rep.items() if isinstance(v, str) and v.startswith("MISSING")]
    if bad and "kokoro" not in bad and not A.dry_run:
        raise SystemExit(f"[m1b] fix first: {bad}")


# --- visemes ---
VIS = {  # phoneme char → viseme (Kokoro/misaki IPA)
    **{c: "open" for c in "aɑæʌɐAIW"},
    **{c: "wide" for c in "eiɪɛEᵻəɚ"},
    **{c: "round" for c in "ouʊɔOYwɜQ"},
    **{c: "closed" for c in "mbp"},
    **{c: "teeth" for c in "fv"},
}
VIS_POSE = {"open": (0.9, 0.0, 0.0), "wide": (0.45, 0.0, 0.4), "round": (0.5, 1.0, 0.0),
            "closed": (0.0, 0.0, 0.0), "teeth": (0.15, 0.0, 0.2), "cons": (0.25, 0.1, 0.1), "rest": (0.0, 0.0, 0.0)}


def visemes_from_words(words, nf, fps):
    """words: [{w, ph, t0, t1}] → per-frame {open, round, wide}, smoothed (attack 2 f, release 3 f)."""
    tgt = [VIS_POSE["rest"]] * nf
    for w in words:
        ph = [c for c in (w.get("ph") or "") if c not in "ˈˌː ."]
        if not ph:
            continue
        dur = (w["t1"] - w["t0"]) / len(ph)
        for i, c in enumerate(ph):
            a = int((w["t0"] + i * dur) * fps)
            b = max(a + 1, int((w["t0"] + (i + 1) * dur) * fps))
            for f in range(max(0, a), min(nf, b)):
                tgt[f] = VIS_POSE[VIS.get(c, "cons")]
    out, cur = [], (0.0, 0.0, 0.0)
    for f in range(nf):
        t = tgt[f]
        k = [0.55 if t[j] > cur[j] else 0.35 for j in range(3)]
        cur = tuple(cur[j] + (t[j] - cur[j]) * k[j] for j in range(3))
        out.append({"f": f, "open": round(cur[0], 3), "round": round(cur[1], 3), "wide": round(cur[2], 3)})
    return out


def step_tts(_):
    if A.dry_run:
        log(f"would synthesise {spec.LINE_EN!r} with Kokoro {spec.VOICE}"); return
    import numpy as np
    import soundfile as sf
    sr = 24000
    t0 = time.time()
    import torch
    from kokoro import KPipeline
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = KPipeline(lang_code=spec.VOICE["lang_code"], device=dev)
    load = time.time() - t0
    t1 = time.time()
    audio, words, off = [], [], spec.LEAD_IN_S
    for r in pipe(spec.LINE_EN, voice=spec.VOICE["voice"], speed=spec.VOICE["speed"]):
        au = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        toks = getattr(r, "tokens", None) or []
        for tk in toks:
            if getattr(tk, "start_ts", None) is None:
                continue
            words.append({"w": tk.text, "ph": tk.phonemes or "", "t0": round(off + tk.start_ts, 3), "t1": round(off + tk.end_ts, 3)})
        audio.append(au)
        off += len(au) / sr
    au = np.concatenate(audio).astype(np.float32)
    words = [w for w in words if w["w"].strip() and any(ch.isalnum() for ch in w["w"])]
    timing_src = "kokoro token timestamps"
    if not words:  # fallback: spread words by letter count
        ws = spec.LINE_EN.split()
        dur = len(au) / sr
        tot = sum(len(w) for w in ws)
        acc = spec.LEAD_IN_S
        for w in ws:
            d = dur * len(w) / tot
            words.append({"w": w, "ph": "", "t0": round(acc, 3), "t1": round(acc + d, 3)})
            acc += d
        timing_src = "fallback: letter-count spread (no timestamps from this Kokoro version)"
    lead = np.zeros(int(sr * spec.LEAD_IN_S), np.float32)
    total = np.zeros(int(sr * spec.DURATION_S), np.float32)
    full = np.concatenate([lead, au])[: len(total)]
    total[: len(full)] = full
    sf.write(PD("audio", "line.wav"), total, sr)
    nf, fps = n_frames(), spec.FPS
    vis = visemes_from_words(words, nf, fps)
    hop = sr // fps
    env = [float(np.sqrt(np.mean(total[i * hop:(i + 1) * hop] ** 2) + 1e-12)) for i in range(nf)]
    m = max(env) or 1
    env = [round(e / m, 3) for e in env]
    speech_s = len(au) / sr
    wpm = round(len(spec.LINE_EN.split()) / (speech_s / 60))
    data = {"line": spec.LINE_EN, "voice": spec.VOICE, "device": dev, "load_s": round(load, 1), "synth_s": round(time.time() - t1, 2),
            "speech_s": round(speech_s, 2), "wpm": wpm, "fits_5s": spec.LEAD_IN_S + speech_s <= spec.DURATION_S - 0.2,
            "timing_source": timing_src, "words": words, "visemes": vis, "envelope": env,
            "kokoro_version": __import__("kokoro").__dict__.get("__version__", "?")}
    jsave(P("audio", "anim.json"), data)
    log(f"TTS {speech_s:.2f} s speech, {wpm} wpm ({'OK' if 130 <= wpm <= 150 else 'outside 130–150 (H6)'}), timing: {timing_src}")
    if not data["fits_5s"]:
        log("WARNING: line + lead-in runs past 4.8 s — raise speed or shorten the line (spec.py)")


def blender(mode, extra=()):
    b = find_blender()
    if not b and not A.dry_run:
        raise SystemExit("[m1b] Blender not found — set BLENDER=<path to blender.exe>")
    cmd = [b or "blender", "--background", "--factory-startup", "--python", os.path.join(KIT, "blender_host.py"), "--",
           "--mode", mode, "--out", out_dir(), "--kit", KIT]
    if A.preview:
        cmd.append("--preview")
    if A.debug:
        cmd.append("--debug")
    if A.only:
        cmd += ["--only", A.only]
    cmd += list(extra)
    run(cmd)


def step_sheet(_):
    blender("sheet")
    if A.dry_run:
        return
    compose_sheet()


def compose_sheet():
    """character-sheet.png: front + side on top, 6 expressions below, palette + ΔE table (phone-readable)."""
    from PIL import Image, ImageDraw
    import captions
    import de
    measure_de()
    views = {v: P("sheet", f"{v.replace(' ', '_')}.png") for v in SHEET_VIEWS}
    have = {k: p for k, p in views.items() if os.path.exists(p)}
    if not have:
        log("no sheet renders found"); return
    W = 2160
    big = (W // 2, int(W // 2 * 16 / 9 * 0.75))
    small = (W // 3, W // 3)
    H = 140 + big[1] + 2 * (small[1] + 70) + 420
    sheet = Image.new("RGB", (W, H), (36, 32, 40))
    d = ImageDraw.Draw(sheet)
    f_big, _ = captions._font(spec.FONTS_LATIN, 64)
    f_lab, _ = captions._font(spec.FONTS_LATIN, 40)
    f_small, _ = captions._font(spec.FONTS_LATIN, 30)
    d.text((40, 30), f"{spec.HOST} — character sheet · {spec.SHOT_ID} · {datetime.now():%d %b %Y}", font=f_big, fill=(245, 235, 255))
    y = 140
    for i, v in enumerate(["front", "side"]):
        if v in have:
            im = Image.open(have[v]).convert("RGB")
            im.thumbnail(big)
            sheet.paste(im, (i * W // 2 + (W // 2 - im.width) // 2, y))
            d.text((i * W // 2 + 30, y + 10), v.upper(), font=f_lab, fill=(245, 235, 255))
    y += big[1] + 20
    ex = list(spec.EXPR.keys())
    for i, v in enumerate(ex):
        r, c = divmod(i, 3)
        if v in have:
            im = Image.open(have[v]).convert("RGB")
            im.thumbnail(small)
            sheet.paste(im, (c * small[0], y + r * (small[1] + 70)))
        d.text((c * small[0] + 20, y + r * (small[1] + 70) + small[1] + 10), v, font=f_lab, fill=(245, 235, 255))
    y += 2 * (small[1] + 70) + 10
    # palette + measured ΔE
    dE = jload(P("sheet", "deltaE.json"), {})
    x = 40
    for name in ["body", "shawl", "glow", "embroidery", "glasses", "ink"]:
        col = spec.COL[name]
        d.rounded_rectangle([x, y, x + 140, y + 100], 16, fill=col, outline=(245, 235, 255), width=2)
        d.text((x, y + 110), name, font=f_small, fill=(245, 235, 255))
        d.text((x, y + 145), col, font=f_small, fill=(200, 190, 210))
        x += 200
    lines = []
    for part, r in dE.items():
        if isinstance(r, dict) and "median_hex" in r:
            lines.append(f"{part}: rendered {r['median_hex']} · worst ΔE00 {r['worst_de']} vs {r['worst_token']} ({r['worst_vision']}) · {r['verdict']}")
    for j, l in enumerate(lines[:4]):
        d.text((40, y + 200 + j * 44), l, font=f_small, fill=(245, 235, 255))
    d.text((40, H - 50), "Own 3D model from the D-048 reference (Canva MAHbd5r-vTY, AI-made — credit per H9). Host never shows anatomy (D5).",
           font=f_small, fill=(170, 160, 180))
    sheet.save(PD("for_drive", f"{spec.SHOT_ID}_character-sheet.png"))
    log("wrote character sheet")


def measure_de():
    """ΔE00 of rendered body + shawl pixels vs tokens/accent, all vision types (playbook §5b) → sheet/deltaE.json."""
    import numpy as np
    from PIL import Image
    import de
    front = P("sheet", "front.png")
    if not os.path.exists(front):
        return
    img = np.asarray(Image.open(front).convert("RGB"))
    res = {}
    for part in ("body", "shawl"):
        mp = P("sheet", f"mask_{part}.png")
        if os.path.exists(mp):
            m = np.asarray(Image.open(mp).convert("RGBA"))[..., 3] / 255.0
            res[part] = de.check_pixels(img, m)
    res["design_minor_colours"] = {k: de.check_hex(spec.COL[k]) for k in ("glow", "blush", "embroidery", "glasses", "pages", "brow")}
    res["rule"] = "main colours (body, shawl) ≥ 15 in every vision type; minor accents are info only (host on its own plate)"
    jsave(P("sheet", "deltaE.json"), res)
    log("ΔE00:", {k: v.get("verdict") for k, v in res.items() if isinstance(v, dict) and "verdict" in v})


def step_shot(_):
    if not os.path.exists(P("audio", "anim.json")) and not A.dry_run:
        raise SystemExit("[m1b] run `python host.py tts` first (the shot needs anim.json)")
    blender("shot")


def step_captions(_):
    from PIL import Image
    import captions
    anim = jload(P("audio", "anim.json"))
    if not anim and not A.dry_run:
        raise SystemExit("[m1b] no anim.json — run tts first")
    raw = sorted(glob.glob(P("frames_raw", "*.png")))
    if A.dry_run:
        log(f"would caption {len(raw)} frames → frames_cap\\"); return
    if not raw:
        raise SystemExit("[m1b] no frames in frames_raw — run shot first")
    os.makedirs(P("frames_cap"), exist_ok=True)
    c = None
    for p in raw:
        im = Image.open(p).convert("RGB")
        if c is None:
            c = captions.Captioner(im.size, anim["words"], debug=A.safe or A.debug)
        f = int(os.path.basename(p).split("_")[-1].split(".")[0])   # Blender frames start at 1
        c.draw(im, (f - 1) / spec.FPS)
        im.save(P("frames_cap", os.path.basename(p)))
    jsave(P("captions.json"), c.report())
    # VTT for the app (captions toggleable there)
    def ts(s):
        return f"00:{int(s // 60):02d}:{s % 60:06.3f}"
    with open(PD("for_drive", f"{spec.SHOT_ID}.en.vtt"), "w", encoding="utf-8") as fh:
        fh.write("WEBVTT\n\n")
        for g in c.groups:
            fh.write(f"{ts(g[0]['t0'])} --> {ts(g[-1]['t1'] + 0.4)}\n{' '.join(w['w'] for w in g)}\n\n")
    log("captions:", json.dumps(c.report(), ensure_ascii=False))


def step_encode(_):
    fps = spec.FPS
    os.makedirs(P("for_drive"), exist_ok=True)
    wav = P("audio", "line.wav")
    af = "loudnorm=I=-14:TP=-1:LRA=7"   # H6 (single pass; R1 moves to two-pass)
    pat_cap = P("frames_cap", "f_%04d.png")
    pat_raw = P("frames_raw", "f_%04d.png")
    rf = fps
    outs = []
    W, H = spec.SHIP if not A.preview else spec.PREVIEW
    for tag, pat in [("captioned", pat_cap), ("clean", pat_raw)]:
        o = P("for_drive", f"{spec.SHOT_ID}_{W}x{H}_{tag}.mp4")
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(rf), "-start_number", "1", "-i", pat, "-i", wav,
             "-vf", f"scale={W}:{H}:flags=lanczos,format=yuv420p", "-r", str(fps),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", "-b:a", "128k", "-af", af,
             "-shortest", "-movflags", "+faststart", o])
        outs.append(o)
    if not A.preview:   # 1080×1920 master for the 1080p rung (kept on the laptop / Drive)
        o = P("for_drive", f"{spec.SHOT_ID}_1080x1920_captioned_master.mp4")
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(fps), "-start_number", "1", "-i", pat_cap, "-i", wav,
             "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
             "-af", af, "-shortest", "-movflags", "+faststart", o])
        outs.append(o)
    if not A.dry_run:
        jsave(P("encode.json"), {o: {"bytes": os.path.getsize(o), "mb": round(os.path.getsize(o) / 2**20, 2)} for o in outs if os.path.exists(o)})


def step_report(_):
    if A.dry_run:
        log("would write for_drive\\manifest.json + RESULTS.md"); return
    anim = jload(P("audio", "anim.json"), {})
    chk = jload(P("check.json"), {})
    man = {
        "shot": spec.SHOT_ID, "host": spec.HOST, "route": "H-a 3D Blender (D-049)", "made": datetime.now().isoformat(timespec="minutes"),
        "preview": A.preview,
        "scene_hash": hashlib.sha256(b"".join(open(os.path.join(KIT, f), "rb").read() for f in ["spec.py", "blender_host.py", "captions.py", "host.py"])).hexdigest()[:16],
        "reference": {"canva_id": spec.REFERENCE_CANVA_ID, "sha256_16": sha(ref_path()) if ref_path() else None,
                      "note": "AI-made reference (Canva); our 3D model is built from it — credit per H9; check Canva terms before publishing any Canva pixel"},
        "tools": {"blender": jload(P("blender.json"), {}).get("version"), "ffmpeg": chk.get("ffmpeg"), "kokoro": anim.get("kokoro_version"),
                  "python": sys.version.split()[0], "os": platform.platform()},
        "gpu": chk.get("gpu"), "seed": spec.SEED,
        "settings": {"engine": spec.ENGINE, "samples": spec.SAMPLES, "fps": spec.FPS, "master": spec.MASTER, "ship": spec.SHIP,
                     "cut_at_s": spec.CUT_AT_S, "cams": {"A": spec.CAM_A, "B": spec.CAM_B}},
        "voice": {**spec.VOICE, "wpm": anim.get("wpm"), "speech_s": anim.get("speech_s"), "timing": anim.get("timing_source")},
        "captions": jload(P("captions.json"), {}),
        "deltaE_rendered": jload(P("sheet", "deltaE.json"), {}),
        "timings_s": {**jload(P("timings.json"), {}), **T},
        "blender_stats": jload(P("blender.json"), {}),
        "files": jload(P("encode.json"), {}),
        "licences": {"Blender": "GPL (tool; output is ours)", "Kokoro-82M": "Apache 2.0 (T30)", "FFmpeg/x264": "GPL (tool)",
                     "Pillow": "MIT-CMU", "fonts": "Inter / Noto Sans Devanagari OFL; Segoe/Nirmala = Windows system fallback (see captions.font_*)"},
        "ai_disclosure": "Voice is synthetic (Kokoro). Character model is our own 3D build from an AI-made reference image (H9).",
    }
    jsave(PD("for_drive", f"{spec.SHOT_ID}_manifest.json"), man)
    tm = man["timings_s"]
    lines = [f"# {spec.SHOT_ID} — {spec.HOST} test shot ({'preview' if A.preview else 'full'})", "",
             f"- Voice: Kokoro {spec.VOICE['voice']} ×{spec.VOICE['speed']} → {anim.get('speech_s')} s, {anim.get('wpm')} wpm ({anim.get('timing_source')})",
             f"- GPU: {chk.get('gpu')}",
             f"- Timings (s): " + ", ".join(f"{k} {v}" for k, v in tm.items()),
             f"- Blender: {man['blender_stats']}",
             f"- Files: " + ", ".join(f"{os.path.basename(k)} {v['mb']} MB" for k, v in man["files"].items()),
             f"- ΔE00 (rendered): " + "; ".join(f"{k} {v.get('worst_de')} {v.get('verdict')}" for k, v in man["deltaE_rendered"].items() if isinstance(v, dict)),
             f"- Captions: {man['captions'].get('notes') or 'OK'}", "",
             "Paste this file into the next chat; upload for_drive\\ to Drive › renders/bakeoff/host."]
    with open(P("RESULTS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def step_selftest(_):
    """No Blender/GPU needed: viseme mapping, caption layout + safe area, contrast, ΔE helper."""
    from PIL import Image
    import captions, de
    ok = True
    words = [{"w": w, "ph": p, "t0": 0.3 + i * 0.38, "t1": 0.3 + (i + 1) * 0.38} for i, (w, p) in enumerate(
        zip(spec.LINE_EN.split(), ["wˈʌt", "ˈɪf", "ə", "flˈæt", "dˈɪsk", "hæd", "tu", "bˈɪld", "ə", "hˈOl", "bˈɑdi"]))]
    v = visemes_from_words(words, n_frames(), spec.FPS)
    ok &= len(v) == n_frames() and max(x["open"] for x in v) > 0.5 and v[0]["open"] == 0
    for size in [spec.PREVIEW, spec.MASTER]:
        c = captions.Captioner(size, words, debug=True)
        strip = Image.new("RGB", (size[0] * 4, size[1]))
        for i, t in enumerate([0.5, 1.6, 2.6, 4.4]):
            im = Image.new("RGB", size, (78, 79, 81))
            c.draw(im, t)
            strip.paste(im, (i * size[0], 0))
        os.makedirs(os.path.join(KIT, "out", "selftest"), exist_ok=True)
        strip.save(os.path.join(KIT, "out", "selftest", f"captions_{size[0]}x{size[1]}.png"))
        rep = c.report()
        ok &= rep["contrast_text_on_scrim_worst"] >= 4.5 and rep["contrast_key_pill"] >= 4.5
        ok &= all(len(p) <= spec.CAPTION["max_chars_line"] for p in rep["phrases"])
        log(f"captions {size}: {json.dumps(rep, ensure_ascii=False)}")
    r = de.check_hex(spec.COL["body"]); ok &= r["worst_de"] >= 15
    r2 = de.check_hex(spec.COL["shawl"]); ok &= r2["worst_de"] >= 15
    log("ΔE body", r, "shawl", r2)
    log("SELFTEST", "PASS" if ok else "FAIL")
    if not ok:
        sys.exit(1)


FUN = {"check": step_check, "tts": step_tts, "sheet": step_sheet, "shot": step_shot, "captions": step_captions,
       "encode": step_encode, "report": step_report, "selftest": step_selftest}


def main():
    global A
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["all"] + STEPS + ["selftest"])
    ap.add_argument("--dry-run", action="store_true", help="print the plan and commands; run nothing")
    ap.add_argument("--debug", action="store_true", help="verbose logs; safe-zone guides on caption frames; Blender keeps the .blend")
    ap.add_argument("--only", help="sheet: one view/expression · shot: camera A or B")
    ap.add_argument("--preview", action="store_true", help="540×960, 16 samples (all frames)")
    ap.add_argument("--safe", action="store_true", help="draw safe zones + caption band on caption frames")
    A = ap.parse_args()
    steps = STEPS if A.step == "all" else [A.step]
    log(f"{spec.SHOT_ID} · {spec.HOST} · steps {steps} · preview={A.preview} dry_run={A.dry_run} only={A.only}")
    for s in steps:
        t = time.time()
        FUN[s](A)
        T[s] = round(time.time() - t, 1)
        log(f"step {s} took {T[s]} s")
        if not A.dry_run and s != "report":
            jsave(P("timings.json"), {**jload(P("timings.json"), {}), s: T[s]})


if __name__ == "__main__":
    main()
