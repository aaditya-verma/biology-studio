"""M1 bake-off runner. Run from this folder in an Anaconda Prompt:
  python bakeoff.py all              # hw → overlays → Blender Cycles + Eevee → three.js → encode → TTS → report
  python bakeoff.py quick            # every 12th frame only: fast s/frame estimates, no clips
  python bakeoff.py ai PATH_TO_CLIP --gen-seconds S --model NAME --vram-peak-gb G
  python bakeoff.py report
Steps can also run alone: hw | overlay | blender | three | encode | tts."""
import argparse, glob, hashlib, json, os, platform, random, shutil, subprocess, sys, time
from datetime import datetime, timezone

KIT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KIT, "out")
sys.path.insert(0, os.path.join(KIT, "common"))
import scene_math as sm

METHODS = {"A_cycles": "Blender Cycles", "A_eevee": "Blender Eevee", "B_three": "three.js headless", "C_ai": "AI video model"}


def sh(cmd, **kw):
    print(">", " ".join(cmd) if isinstance(cmd, list) else cmd, flush=True)
    return subprocess.run(cmd, **kw)


def cap(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return f"n/a ({e.__class__.__name__})"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def scene_hash(extra):
    h = hashlib.sha256()
    for p in ["shot.json", "common/scene_math.py", "common/overlay.py"] + extra:
        with open(os.path.join(KIT, p), "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:16]


def jload(p, default=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        return default


def jsave(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)


# ---------------- steps ----------------
def step_hw(_):
    ps = lambda q: cap(["powershell", "-NoProfile", "-Command", q])
    du = shutil.disk_usage(KIT)
    hw = {
        "checked": datetime.now().isoformat(timespec="minutes"),
        "gpu": cap(["nvidia-smi", "--query-gpu=name,driver_version,memory.total,power.limit", "--format=csv,noheader"]),
        "cuda_version": cap(["nvidia-smi"]).split("CUDA Version:")[-1].split("|")[0].strip() if shutil.which("nvidia-smi") else "n/a",
        "cpu": ps("(Get-CimInstance Win32_Processor).Name"),
        "cores_threads": ps("$p=Get-CimInstance Win32_Processor; \"$($p.NumberOfCores)C/$($p.NumberOfLogicalProcessors)T\""),
        "ram_gb": ps("[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1)"),
        "os": ps("(Get-CimInstance Win32_OperatingSystem).Caption + ' ' + (Get-CimInstance Win32_OperatingSystem).Version"),
        "free_disk_gb_kit_drive": round(du.free / 2**30, 1),
        "python": sys.version.split()[0],
        "ffmpeg": cap(["ffmpeg", "-version"]).splitlines()[0] if shutil.which("ffmpeg") else "MISSING",
        "nvenc_encoders": [l.split()[1] for l in cap(["ffmpeg", "-hide_banner", "-encoders"]).splitlines() if "nvenc" in l] if shutil.which("ffmpeg") else [],
        "blender": find_blender() or "MISSING",
        "node": cap(["node", "--version"]) if shutil.which("node") else "MISSING",
    }
    jsave(os.path.join(OUT, "hw.json"), hw)
    print(json.dumps(hw, indent=2))


def find_blender():
    if shutil.which("blender"):
        return shutil.which("blender")
    c = sorted(glob.glob(r"C:\Program Files\Blender Foundation\Blender*\blender.exe")
               + glob.glob(os.path.join(KIT, "..", "..", "apps", "blender*", "blender.exe")))
    return c[-1] if c else None


def step_overlay(a):
    from overlay import draw, frames
    shot = sm.load_shot()
    for sub, lab in [("overlay", True), ("overlay_nolabels", False)]:
        d = os.path.join(OUT, sub)
        os.makedirs(d, exist_ok=True)
        for f in range(frames(shot)):
            draw(shot, f, lab).save(os.path.join(d, f"{f:04d}.png"))
    print("overlays ready")


def step_blender(a):
    exe = find_blender()
    if not exe:
        sys.exit("Blender not found: install Blender 4.2+ or put a portable copy in D:\\Projects\\biology_studio\\apps\\")
    for eng, m in [("CYCLES", "A_cycles"), ("EEVEE", "A_eevee")]:
        t0 = time.time()
        sh([exe, "-b", "--factory-startup", "-P", os.path.join(KIT, "A_blender", "shot_blender.py"), "--",
            "--engine", eng, "--out", os.path.join(OUT, m), "--every", str(a.every)], check=True)
        st = jload(os.path.join(OUT, m, "render_stats.json"))
        st["sec_wall_incl_startup"] = round(time.time() - t0, 1)
        jsave(os.path.join(OUT, m, "render_stats.json"), st)


def step_three(a):
    bdir = os.path.join(KIT, "B_three")
    npm = "npm.cmd" if os.name == "nt" else "npm"
    if not os.path.exists(os.path.join(bdir, "node_modules", "three")):
        sh([npm, "install"], cwd=bdir, check=True)
        sh(["npx.cmd" if os.name == "nt" else "npx", "playwright", "install", "chromium"], cwd=bdir, check=True)
    t0 = time.time()
    sh(["node", os.path.join(bdir, "record.mjs"), "--out", os.path.join(OUT, "B_three"), "--every", str(a.every)], cwd=KIT, check=True)
    st = jload(os.path.join(OUT, "B_three", "render_stats.json"))
    st["sec_wall_incl_startup"] = round(time.time() - t0, 1)
    jsave(os.path.join(OUT, "B_three", "render_stats.json"), st)


def encode(src_pattern, overlay_dir, dst, encoder, start_number=0):
    ff = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", "24", "-start_number", str(start_number), "-i", src_pattern,
          "-framerate", "24", "-i", os.path.join(overlay_dir, "%04d.png"),
          "-filter_complex", "[0:v]scale=1280:720,setsar=1[b];[b][1:v]overlay=0:0:shortest=1,format=yuv420p",
          "-r", "24", "-movflags", "+faststart"]
    if encoder == "nvenc":
        ff += ["-c:v", "h264_nvenc", "-preset", "p5", "-tune", "hq", "-rc", "vbr", "-cq", "23", "-b:v", "0"]
    else:
        ff += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23"]
    t0 = time.time()
    r = sh(ff + [dst])
    return {"ok": r.returncode == 0, "sec": round(time.time() - t0, 2),
            "mb": round(os.path.getsize(dst) / 1e6, 2) if r.returncode == 0 else None, "args": " ".join(ff[ff.index("-c:v"):])}


def manifest(m, clip, extra_files, enc, stats, extra=None):
    hw = jload(os.path.join(OUT, "hw.json"), {})
    shot = sm.load_shot()
    man = {
        "manifest_version": 1, "shot_id": shot["id"], "shot_version": shot["version"], "method": m,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scene_hash": scene_hash(extra_files), "seed": shot["seed"],
        "tool": stats.get("tool"), "engine": stats.get("engine"), "settings": stats.get("settings"),
        "gpu": hw.get("gpu"), "driver_cuda": hw.get("cuda_version"), "os": hw.get("os"),
        "render": {k: stats.get(k) for k in ["frames_rendered", "frames_total", "sec_total", "sec_per_frame_mean", "est_sec_full_shot", "sec_wall_incl_startup"]},
        "encode": enc, "output": {"file": os.path.basename(clip), "sha256": sha(clip) if os.path.exists(clip) else None},
        "voice_version": None, "licence_notes": "renders ours; tools per registry T01/T03/T20/T35",
    }
    if extra:
        man.update(extra)
    jsave(os.path.join(OUT, m, "manifest.json"), man)
    return man


EXTRA = {"A_cycles": ["A_blender/shot_blender.py"], "A_eevee": ["A_blender/shot_blender.py"],
         "B_three": ["B_three/shot.js", "B_three/shot.html", "B_three/record.mjs"], "C_ai": ["C_ai/README.md"]}


def step_encode(a):
    for m in ["A_cycles", "A_eevee", "B_three"]:
        fdir = os.path.join(OUT, m, "frames")
        st = jload(os.path.join(OUT, m, "render_stats.json"))
        if not st or st.get("every", 1) != 1:
            print(f"skip encode {m}: needs a full render (every=1)")
            continue
        enc = {"nvenc": encode(os.path.join(fdir, "%04d.png"), os.path.join(OUT, "overlay"), os.path.join(OUT, m, f"{m}_720p_nvenc.mp4"), "nvenc"),
               "x264": encode(os.path.join(fdir, "%04d.png"), os.path.join(OUT, "overlay"), os.path.join(OUT, m, f"{m}_720p_x264.mp4"), "x264")}
        manifest(m, os.path.join(OUT, m, f"{m}_720p_nvenc.mp4"), EXTRA[m], enc, st)


def step_ai(a):
    m, d = "C_ai", os.path.join(OUT, "C_ai")
    os.makedirs(os.path.join(d, "frames"), exist_ok=True)
    # normalise any clip to 1280x720@24 frames, looping/trimming to 20 s, then add the no-label overlay
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stream_loop", "-1", "-i", a.clip, "-t", "20",
        "-vf", "fps=24,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x14171c",
        os.path.join(d, "frames", "%04d.png")], check=True)
    stats = {"tool": a.model, "engine": "ComfyUI (local)" if not a.online else "online free tier", "settings": {"source_clip": os.path.basename(a.clip)},
             "sec_total": a.gen_seconds, "frames_total": 480}
    enc = {"nvenc": encode(os.path.join(d, "frames", "%04d.png"), os.path.join(OUT, "overlay_nolabels"), os.path.join(d, "C_ai_720p_nvenc.mp4"), "nvenc", 1)}
    jsave(os.path.join(d, "render_stats.json"), stats)
    manifest(m, os.path.join(d, "C_ai_720p_nvenc.mp4"), EXTRA[m], enc, stats,
             {"vram_peak_gb": a.vram_peak_gb, "ai_disclosure": "AI-generated (H9); no on-structure labels; anatomy not trusted until G-Sci"})


def step_tts(a):
    sh([sys.executable, os.path.join(KIT, "D_tts", "tts.py"), "--out", os.path.join(OUT, "tts")], check=False)


def step_report(a):
    hw = jload(os.path.join(OUT, "hw.json"), {})
    rows, blind = [], {}
    clips = [m for m in METHODS if os.path.exists(os.path.join(OUT, m, f"{m}_720p_nvenc.mp4"))]
    rnd = random.Random(1517)
    letters = list("ABCD")[:len(clips)]
    rnd.shuffle(letters)
    os.makedirs(os.path.join(OUT, "for_drive"), exist_ok=True)
    for m, letter in zip(clips, letters):
        blind[letter] = m
        shutil.copy(os.path.join(OUT, m, f"{m}_720p_nvenc.mp4"), os.path.join(OUT, "for_drive", f"clip-{letter}.mp4"))
        shutil.copy(os.path.join(OUT, m, "manifest.json"), os.path.join(OUT, "for_drive", f"manifest-{letter}.json"))
    for m in METHODS:
        st = jload(os.path.join(OUT, m, "render_stats.json"))
        man = jload(os.path.join(OUT, m, "manifest.json"), {})
        if not st:
            continue
        enc = (man.get("encode") or {})
        rows.append({"method": METHODS[m], "engine": st.get("engine"), "frames": f"{st.get('frames_rendered')}/{st.get('frames_total')}",
                     "s_per_frame": st.get("sec_per_frame_mean"), "est_full_shot_s": st.get("est_sec_full_shot") or st.get("sec_total"),
                     "wall_s": st.get("sec_wall_incl_startup"), "nvenc_s": (enc.get("nvenc") or {}).get("sec"),
                     "nvenc_MB": (enc.get("nvenc") or {}).get("mb"), "x264_MB": (enc.get("x264") or {}).get("mb")})
    tts = jload(os.path.join(OUT, "tts", "tts_stats.json"), {})
    for k in ("voice1", "voice2"):
        if k in tts:
            shutil.copy(os.path.join(OUT, "tts", f"{k}_{'kokoro' if k == 'voice1' else 'piper'}.wav"), os.path.join(OUT, "for_drive")) if "error" not in tts[k] else None
    res = {"hw": hw, "renders": rows, "tts": {k: {kk: v for kk, v in tts.get(k, {}).items() if kk != "items"} for k in ("voice1", "voice2")}}
    jsave(os.path.join(OUT, "results.json"), res)
    jsave(os.path.join(OUT, "blind_key.json"), blind)  # do NOT upload this to Drive until T1 is rated
    lines = ["# M1 results (paste this file back into the chat)", "", "## Laptop", "```", json.dumps(hw, indent=1), "```", "", "## Renders",
             "| Method | Engine | Frames | s/frame | Full shot s | Wall s | NVENC s | NVENC MB | x264 MB |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| " + " | ".join(str(r[k]) for k in ["method", "engine", "frames", "s_per_frame", "est_full_shot_s", "wall_s", "nvenc_s", "nvenc_MB", "x264_MB"]) + " |")
    lines += ["", "## TTS", "```", json.dumps(res["tts"], indent=1), "```", "", f"Blind key saved in out/blind_key.json ({len(blind)} clips) — keep it closed until you rate T1."]
    with open(os.path.join(OUT, "RESULTS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    print(f"\nUpload everything in {os.path.join(OUT, 'for_drive')} to Drive › renders/bakeoff")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["all", "quick", "hw", "overlay", "blender", "three", "encode", "ai", "tts", "report"])
    ap.add_argument("clip", nargs="?")
    ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--gen-seconds", type=float)
    ap.add_argument("--model", default="Wan2.2-TI2V-5B")
    ap.add_argument("--vram-peak-gb", type=float)
    ap.add_argument("--online", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.step == "quick":
        a.every = 12
        for f in (step_hw, step_blender, step_three, step_report):
            f(a)
    elif a.step == "all":
        for f in (step_hw, step_overlay, step_blender, step_three, step_encode, step_tts, step_report):
            f(a)
    else:
        globals()["step_" + a.step](a)
