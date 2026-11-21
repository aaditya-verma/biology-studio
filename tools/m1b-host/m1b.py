"""M1b host-shot runner (Laptop 1). Owner doc: studio-docs/build/pipeline-reference.md §7 · spec: host.json.
Run from this folder in an Anaconda Prompt (conda activate bio):
  python m1b.py check                 # tools, fonts, GPU — writes nothing else
  python m1b.py all                   # tts → tex → sheet → palette → shot → captions → encode → report → compare
  python m1b.py all --preview         # 360×640, 8 samples: whole pipeline in ~3–5 min
  python m1b.py t1b                   # D-051: only what owner check T1b needs, one run at 720×1280 → out\\for_drive\\
  python m1b.py <step> [--only A|B|<expression>] [--debug] [--dry-run] [--cycles] [--nvenc] [--safe]
Steps: check | tts | tex | sheet | shot | palette | captions | encode | report | compare (palette after shot: it reads the shot probes).  Output: out\\ (never committed) → out\\for_drive\\.
Quality pass (v2): tex = generated shawl/leather textures; palette = ΔE00 on RENDERED pixels (probe masks from the front tile);
compare = side-by-side with the Canva refs for G-Art (refs stay on the laptop: handoff\\m1b-host\\canva-refs)."""
import argparse, glob, hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime

KIT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KIT, "out")
SPEC = json.load(open(os.path.join(KIT, "host.json"), encoding="utf-8"))
TIMES = os.path.join(OUT, "timings.json")


def studio_home():
    """Studio home = the first parent folder holding apps\\ (works from Studio home tools\\m1b-host\\ or the repo clone's tools/m1b-host/).
    EDIT: or set STUDIO_HOME."""
    if os.environ.get("STUDIO_HOME"):
        return os.environ["STUDIO_HOME"]
    d = KIT
    for _ in range(6):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "apps")):
            return d
    return os.path.join(KIT, "..", "..")


def sh(cmd, dry=False, **kw):
    print(">", " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd), flush=True)
    if dry:
        return subprocess.CompletedProcess(cmd, 0, "", "")
    return subprocess.run(cmd, **kw)


def cap(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return f"n/a ({e.__class__.__name__})"


def jload(p, d=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except OSError:
        return d


def jsave(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def timed(name, fn, a):
    t0 = time.time(); fn(a); dt = round(time.time() - t0, 1)
    if not a.dry_run:
        t = jload(TIMES, {}); t[name + ("_preview" if a.preview else "")] = dt; jsave(TIMES, t)
    print(f"[m1b] {name} {dt} s", flush=True)


def find_blender():
    cands = [shutil.which("blender")] + glob.glob(r"C:\Program Files\Blender Foundation\*\blender.exe") + \
        glob.glob(os.path.join(studio_home(), "apps", "blender*", "blender.exe"))  # EDIT: Blender location
    cands = [c for c in cands if c and os.path.exists(c)]
    return sorted(cands)[-1] if cands else None


def fonts_dir():
    fd = os.path.abspath(os.path.join(KIT, SPEC["captions"]["fonts_dir"]))
    return fd if os.path.isdir(fd) else os.path.join(studio_home(), "apps", "fonts")


def res(a):
    return "preview" if a.preview else "ship"


# ---------------- steps ----------------
def s_check(a):
    fd = fonts_dir()
    have = [os.path.basename(f) for f in glob.glob(os.path.join(fd, "*.[ot]tf"))]
    r = {"blender": find_blender() or "MISSING", "ffmpeg": cap(["ffmpeg", "-version"]).splitlines()[0] if shutil.which("ffmpeg") else "MISSING",
         "libass": "yes" if "ass" in cap(["ffmpeg", "-hide_banner", "-filters"]) else "NO",
         "gpu": cap(["nvidia-smi", "--query-gpu=name,driver_version,memory.total,temperature.gpu", "--format=csv,noheader"]),
         "fonts_dir": fd, "fonts": have,
         "need_fonts": [f for f in ("Inter", "NotoSansDevanagari") if not any(f.lower() in h.lower() for h in have)]}
    try:
        import kokoro; r["kokoro"] = getattr(kokoro, "__version__", "installed")
    except ImportError:
        r["kokoro"] = "MISSING (pip install kokoro)"
    print(json.dumps(r, indent=2))
    if r["need_fonts"]:
        print("[m1b] Fonts missing → see README §Setup 2 (Inter + Noto Sans Devanagari, OFL) into", fd)
    if not a.dry_run:
        jsave(os.path.join(OUT, "check.json"), r)


def s_tts(a):
    sh([sys.executable, os.path.join(KIT, "lipsync.py")] + (["--debug"] if a.debug else []) + (["--dry-run"] if a.dry_run else []), check=True)


def s_tex(a):
    sh([sys.executable, os.path.join(KIT, "tex.py")] + [f for f, on in (("--preview", a.preview), ("--debug", a.debug), ("--dry-run", a.dry_run)) if on], check=True)


def blender(a, mode):
    b = find_blender()
    if not b and a.dry_run:
        b = "blender"
    if not b:
        sys.exit("[m1b] Blender not found — install 4.5 LTS or put it in apps\\blender*")
    cmd = [b, "-b", "--factory-startup", "-P", os.path.join(KIT, "blender_host.py"), "--", "--mode", mode, "--res", res(a),
           "--engine", "cycles" if a.cycles else "eevee"]
    for f, on in (("--preview", a.preview), ("--debug", a.debug), ("--dry-run", a.dry_run), ("--reduced-motion", a.reduced_motion),
                  ("--palette-pass", getattr(a, "palette_pass", False)), ("--no-sim", getattr(a, "no_sim", False)), ("--strict", getattr(a, "strict", False))):
        if on:
            cmd.append(f)
    if a.only:
        cmd += ["--only", a.only]
    sh(cmd, dry=a.dry_run, check=True)


def s_sheet(a):
    blender(a, "sheet")
    if not a.dry_run:
        compose_sheet(a)


def compose_sheet(a):
    """Tiles → sheet_portrait.png (phone) + sheet_landscape.png (tablet/desktop) — C13."""
    from PIL import Image, ImageDraw, ImageFont
    tdir = os.path.join(OUT, "sheet", "tiles")
    names = ["front", "side"] + SPEC["expressions"]
    tiles = {n: Image.open(os.path.join(tdir, n + ".png")).convert("RGB") for n in names if os.path.exists(os.path.join(tdir, n + ".png"))}
    if not tiles:
        print("[m1b] no tiles yet"); return
    fd = fonts_dir()
    fnt = lambda s, w="Bold": ImageFont.truetype(next(iter(glob.glob(os.path.join(fd, f"Inter*{w}*.[ot]tf"))), "arial.ttf"), s)
    pal = SPEC["host"]["palette"]
    for layout, cols, tw in (("portrait", 2, 540), ("landscape", 4, 480)):
        th = int(tw * 1.25); lab = 56; top = 150; chips = 90
        rows = -(-len(names) // cols)
        W, Hh = cols * tw, top + rows * (th + lab) + chips + 60
        S = Image.new("RGB", (W, Hh), pal["plate_bottom"]); d = ImageDraw.Draw(S)
        d.text((24, 22), f"{SPEC['host']['name']} — character sheet v{SPEC['version']}", fill="#FFFFFF", font=fnt(46))
        d.text((24, 84), "Front · side · 6 expressions · same model + seed (identity by construction)", fill="#D8CCE0", font=fnt(26, "Regular"))
        for i, n in enumerate(names):
            if n not in tiles:
                continue
            x, y = (i % cols) * tw, top + (i // cols) * (th + lab)
            S.paste(tiles[n].resize((tw, th)), (x, y))
            d.text((x + 16, y + th + 10), n, fill="#FFFFFF", font=fnt(30))
        cy = Hh - chips - 40
        for j, (k, v) in enumerate([(k, v) for k, v in pal.items() if k in ("body", "glow", "shawl", "embroidery", "glasses", "book_cover")]):
            d.rectangle([24 + j * 170, cy, 24 + j * 170 + 48, cy + 48], fill=v, outline="#FFFFFF")
            d.text((80 + j * 170, cy + 8), f"{k}\n{v}", fill="#FFFFFF", font=fnt(16, "Regular"))
        d.text((24, Hh - 40), SPEC["credit"], fill="#B9AEC2", font=fnt(18, "Regular"))
        S.save(os.path.join(OUT, "sheet", f"sheet_{layout}.png"))
    print("[m1b] sheet → out\\sheet\\sheet_portrait.png + sheet_landscape.png")


MAIN_REGIONS = ("body", "shawl")  # ΔE ≥ 15 vs on-screen tokens (D-046 main colours); props are logged, not gated
HOST_REGIONS = ("body",)          # figure/ground gate (G-A11y, D-051): the pearl body must stand off the real plate
SEP_RATIO, SEP_SHARE = 3.0, 0.90  # EDIT: WCAG 1.4.11 non-text contrast ≥ 3:1 on ≥ 90 % of the body's edge samples


def hexc(c):
    return "#%02X%02X%02X" % tuple(int(x) for x in c[:3])


def contrast(c1, c2):
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def probe_sets():
    """(tag, png, probe json) for the sheet front tile(s) and each shot camera's probe frame."""
    out = []
    for tag in ("front", "front_std"):
        png, pj = os.path.join(OUT, "sheet", "tiles", tag + ".png"), os.path.join(OUT, "sheet", f"probe_{tag}.json")
        if os.path.exists(png) and os.path.exists(pj):
            out.append((tag, png, pj))
    for pj in sorted(glob.glob(os.path.join(OUT, "shot", "probe_shot_*.json"))):
        pr = jload(pj); png = os.path.join(OUT, "frames", pr.get("res", "ship"), "f_%04d.png" % pr["frame"])
        if os.path.exists(png):
            out.append((os.path.basename(pj)[6:-5], png, pj))
    return out


def separation(im, pr, de, regions=HOST_REGIONS):
    """Host edge vs the real plate behind it: for every body sample with a plate neighbour, take the body pixel one step in,
    the edge pixel and the plate pixel one step out; score = best of (inner vs plate, edge vs plate) — so a dark outline
    counts on a light plate and a light body counts on a dark one. ΔE00 = worst of normal/deut/prot/trit."""
    st = pr["step"]; reg = {(x, y): r for r, pts in pr["pts"].items() for x, y in pts}
    W, Hh = im.size; rat, des = [], []
    for r in regions:
        for x, y in pr["pts"].get(r, []):
            for dx, dy in ((st, 0), (-st, 0), (0, st), (0, -st)):
                ox, oy = x + 2 * dx, y + 2 * dy  # plate 2 steps out: past the anti-aliased edge, inside any halo the viewer sees
                if reg.get((x + dx, y + dy)) == "plate" and reg.get((ox, oy)) == "plate" and reg.get((x - dx, y - dy)) == r \
                        and 0 <= ox < W and 0 <= oy < Hh:
                    e, i, p = im.getpixel((x, y)), im.getpixel((x - dx, y - dy)), im.getpixel((ox, oy))
                    rat.append(max(contrast(i, p), contrast(e, p)))
                    des.append(max(min(de.de00(de.sim(hexc(i), v), de.sim(hexc(p), v)) for v in ("norm", "deut", "prot", "trit")),
                                   min(de.de00(de.sim(hexc(e), v), de.sim(hexc(p), v)) for v in ("norm", "deut", "prot", "trit"))))
    if not rat:
        return None
    rat.sort(); des.sort(); k = len(rat) // 10
    share = sum(1 for x in rat if x >= SEP_RATIO) / len(rat)
    return {"n": len(rat), "p10_ratio": round(rat[k], 2), "min_ratio": round(rat[0], 2), "share_ok": round(share, 3),
            "p10_de": round(des[k], 1), "ok": share >= SEP_SHARE}


def embroidery(im, pr, de, onscreen):
    """Embroidery is a texture on the shawl, not an object: take shawl-mask pixels ≥ 25 L* brighter than the shawl median."""
    pts = pr["pts"].get("shawl", [])
    if len(pts) < 20:
        return None
    px = [im.getpixel((x, y))[:3] for x, y in pts]
    L = [de.lab(de.s2l(hexc(c)))[0] for c in px]; Lm = sorted(L)[len(L) // 2]
    th = [c for c, l in zip(px, L) if l >= Lm + 25]  # EDIT: thread = ≥ 25 L* over the wool
    if len(th) < 3:
        return {"n": len(th), "note": "too few thread pixels at this resolution"}
    import statistics
    med = hexc([statistics.median(c[i] for c in th) for i in range(3)])
    d, k, v = de.check(med, onscreen or None)
    d2, k2, v2 = de.check(med, ["endo"])
    return {"n": len(th), "median": med, "worst_de": round(d, 1), "vs": k, "vision": v, "vs_endo": round(d2, 1), "endo_vision": v2,
            "ok": d2 >= 15}


def s_palette(a):
    """Rendered-pixel colour checks (D-051): (1) host body vs the real plate behind it (gate, G-A11y); (2) host colours vs the
    germ-layer tokens — gated only for tokens on screen in the shot (owner, 21 Nov), else info; (3) embroidery thread vs endoderm;
    (4) swatches ≥ 15 (gate)."""
    import statistics
    from PIL import Image
    sys.path.insert(0, KIT); import de
    res_ = {"separation": {}}
    onscreen = SPEC.get("tokens_on_screen", [])  # EDIT: e.g. ["endo", "hypo"] when a shot shows germ layers; [] = host-only → info
    for tag, png, pj in probe_sets():
        im = Image.open(png).convert("RGB"); pr = jload(pj); step = pr["step"]
        reg_of = {(x, y): r for r, pts in pr["pts"].items() for x, y in pts}
        out = {}
        for r, pts in pr["pts"].items():
            if r == "plate":
                continue
            core = [(x, y) for x, y in pts if all(reg_of.get((x + dx, y + dy)) == r for dx, dy in ((step, 0), (-step, 0), (0, step), (0, -step)))]
            if len(core) < 5:
                continue
            px = [im.getpixel((x, y)) for x, y in core]
            med = hexc([statistics.median(c[i] for c in px) for i in range(3)])
            srt = sorted(px, key=lambda c: sum(c)); lo, hi = hexc(srt[len(px) // 10]), hexc(srt[len(px) * 9 // 10])
            w = min((de.check(h, onscreen or None) for h in (med, lo, hi)), key=lambda t: t[0])
            gate = bool(onscreen) and r in MAIN_REGIONS
            out[r] = {"median": med, "p10": lo, "p90": hi, "n": len(core), "worst_de": round(w[0], 1), "vs": w[1], "vision": w[2],
                      "gate": gate, "ok": (w[0] >= 15) if gate else None}
        emb = embroidery(im, pr, de, onscreen)
        if emb:
            out["embroidery"] = dict(emb, gate=False, worst_de=emb.get("worst_de"), vs=emb.get("vs"), vision=emb.get("vision"),
                                     median=emb.get("median"), ok=emb.get("ok"))
        res_[tag + f" ({pr['view']})"] = out
        sep = separation(im, pr, de)
        if sep:
            res_["separation"][tag] = sep
        sh_ = separation(im, pr, de, ("shawl",))  # G-A11y R5: shawl edge reported, not gated (costume, not the identity cue)
        if sh_:
            res_.setdefault("separation_shawl_info", {})[tag] = dict(sh_, ok=None)
    sw = {k: de.check(v) for k, v in SPEC["host"]["palette"].items() if k in ("body", "shawl", "shawl_dark", "embroidery", "book_cover")}
    res_["swatches"] = {k: [round(v[0], 1), v[1], v[2]] for k, v in sw.items()}
    sw_ok = all(sw[k][0] >= 15 for k in ("body", "shawl") if k in sw)
    px_ok = all(v["ok"] for t, rr in res_.items() if t.startswith(("front", "shot")) and isinstance(rr, dict)
                for v in rr.values() if isinstance(v, dict) and v.get("gate"))
    want = ["front"] + [f"shot_{s['id']}_{t}" for s in SPEC["video"]["shots"] for t in ("start", "mid", "end")]  # G-A11y R5: all, or no pass
    missing = [w for w in want if w not in res_["separation"]]
    res_["separation_missing"] = missing
    sep_ok = not missing and all(x["ok"] for x in res_["separation"].values())
    res_["tokens_on_screen"] = onscreen
    res_["pass"] = sw_ok and px_ok and sep_ok
    res_["parts"] = {"swatches": sw_ok, "tokens_px": px_ok, "host_vs_plate": sep_ok}
    if not a.dry_run:
        jsave(os.path.join(OUT, "palette_rendered.json"), res_)
    print("[m1b] palette:", json.dumps(res_, ensure_ascii=False))


def s_compare(a):
    """Side-by-side boards for G-Art: our front/side tiles vs the turnaround ref; shot frames vs the armchair hero ref.
    Writes out/review/compare_*.png (local only; refs are AI images and never leave the laptop/Drive)."""
    from PIL import Image, ImageDraw
    refd = os.path.join(studio_home(), "handoff", "m1b-host", "canva-refs")  # EDIT: where the refs live
    turn, arm = os.path.join(refd, "nani-ref-turnaround.png"), os.path.join(refd, "nani-ref-armchair.png")
    rv = os.path.join(OUT, "review"); os.makedirs(rv, exist_ok=True)
    tiles = os.path.join(OUT, "sheet", "tiles")

    def board(items, name, h=900):
        ims = [(lab, Image.open(p).convert("RGB")) for lab, p in items if p and os.path.exists(p)]
        if len(ims) < 2:
            print("[m1b] compare: missing images for", name); return
        ims = [(lab, im.resize((int(im.width * h / im.height), h))) for lab, im in ims]
        W = sum(im.width for _, im in ims) + 20 * (len(ims) + 1)
        B = Image.new("RGB", (W, h + 70), "#101010"); d = ImageDraw.Draw(B); x = 20
        for lab, im in ims:
            B.paste(im, (x, 50)); d.text((x, 15), lab, fill="#FFFFFF"); x += im.width + 20
        B.save(os.path.join(rv, name)); print("[m1b] compare →", os.path.relpath(os.path.join(rv, name), KIT))
    if os.path.exists(turn):
        T = Image.open(turn).convert("RGB"); w2 = T.width // 2
        T.crop((0, 0, w2, T.height)).save(os.path.join(rv, "_ref_front.png")); T.crop((w2, 0, T.width, T.height)).save(os.path.join(rv, "_ref_side.png"))
    board([("REF front", os.path.join(rv, "_ref_front.png")), ("ours front", os.path.join(tiles, "front.png")),
           ("REF side", os.path.join(rv, "_ref_side.png")), ("ours side", os.path.join(tiles, "side.png"))], "compare_sheet.png")
    fr = sorted(glob.glob(os.path.join(OUT, "frames", res(a), "f_*.png")))
    pick = [fr[int(len(fr) * k)] for k in (0.35, 0.8)] if fr else []
    board([("REF hero", arm)] + [(f"ours {os.path.basename(p)}", p) for p in pick], "compare_shot.png")
    board([("ours " + e, os.path.join(tiles, e + ".png")) for e in SPEC["expressions"]], "compare_expressions.png", h=600)
    if getattr(a, "onion", False):
        for v_ in ("front", "side"):
            onion(os.path.join(rv, f"_ref_{v_}.png"), os.path.join(tiles, v_ + ".png"), os.path.join(rv, f"onion_{v_}.png"))


def silhouette_box(im, bg_tol=28):
    """Bounding box of the figure: pixels that differ from the plate (sampled at the top corners) by more than bg_tol."""
    import numpy as np
    A = np.asarray(im.convert("RGB")).astype(int); h, w, _ = A.shape
    bg = np.median(np.concatenate([A[:h // 10, :w // 10].reshape(-1, 3), A[:h // 10, -w // 10:].reshape(-1, 3)]), axis=0)
    m = np.abs(A - bg).sum(axis=2) > bg_tol * 3
    m[int(h * 0.80):] = False  # EDIT: ignore the floor band (shadows, contact glow)
    ys, xs = np.nonzero(m)
    if len(xs) < 50:
        return (0, 0, w, h)
    return (int(np.percentile(xs, 1)), int(np.percentile(ys, 1)), int(np.percentile(xs, 99)), int(np.percentile(ys, 99)))


def onion(ref_p, ours_p, out_p):
    """G-Art R1 `--onion`: our tile scaled so its silhouette box matches the ref's, laid at 50 % over the ref, plus a
    red (ref) / cyan (ours) edge overlay. Shows proportion drift (egg height/width, shawl line, book height) at a glance."""
    from PIL import Image, ImageChops, ImageFilter, ImageDraw
    if not (os.path.exists(ref_p) and os.path.exists(ours_p)):
        print("[m1b] onion: missing", ref_p if not os.path.exists(ref_p) else ours_p); return
    R = Image.open(ref_p).convert("RGB"); O = Image.open(ours_p).convert("RGB")
    rb, ob = silhouette_box(R), silhouette_box(O)
    sx = (rb[2] - rb[0]) / max(1, ob[2] - ob[0]); sy = (rb[3] - rb[1]) / max(1, ob[3] - ob[1]); s = (sx + sy) / 2  # uniform: keep our proportions
    O2 = O.resize((int(O.width * s), int(O.height * s)))
    canvas = Image.new("RGB", R.size, (0, 0, 0))
    ox = int(rb[0] - ob[0] * s + ((rb[2] - rb[0]) - (ob[2] - ob[0]) * s) / 2); oy = int(rb[3] - ob[3] * s)  # align centres x, feet y
    canvas.paste(O2, (ox, oy))
    blend = Image.blend(R, canvas, 0.5)
    ed = lambda im: im.convert("L").filter(ImageFilter.GaussianBlur(3)).filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 12 else 0)
    er, eo = ed(R), ed(canvas)  # blurred first: silhouette + big shapes, not wool texture
    edges = Image.merge("RGB", (er, eo, eo))
    edges_on = Image.composite(edges, blend, ImageChops.lighter(er, eo))
    W = R.width
    B = Image.new("RGB", (W * 2 + 30, R.height + 60), "#101010"); d = ImageDraw.Draw(B)
    B.paste(blend, (10, 50)); B.paste(edges_on, (W + 20, 50))
    d.text((10, 15), f"onion 50 %: ref + ours (scale {s:.2f}; box ratio ref {(rb[3]-rb[1])/max(1,rb[2]-rb[0]):.2f} · ours {(ob[3]-ob[1])/max(1,ob[2]-ob[0]):.2f} h/w)", fill="#FFFFFF")
    d.text((W + 20, 15), "edges: red = ref · cyan = ours", fill="#FFFFFF")
    B.save(out_p); print("[m1b] onion →", os.path.relpath(out_p, KIT))


def s_shot(a):
    if not os.path.exists(os.path.join(OUT, "audio", "visemes.json")):
        sys.exit("[m1b] run `python m1b.py tts` first")
    blender(a, "shot")


def s_captions(a):
    sh([sys.executable, os.path.join(KIT, "captions.py"), "--res", res(a)] + (["--debug"] if a.debug else []) + (["--dry-run"] if a.dry_run else [])
       + (["--reduced-motion"] if a.reduced_motion else []), check=True)


def ff_path(p):  # libass filter paths on Windows: forward slashes, escaped drive colon
    return p.replace("\\", "/").replace(":", "\\:")


def s_encode(a):
    """Frames + loudness-prepped line → one mp4 per caption track + clean. Audio: loud.py two-pass loudnorm (H6, D-051):
    −14 LUFS ±0.5, true peak ≤ −1.5 dBTP measured on every encoded file; an AAC overshoot lowers the limiter and redoes (≤ 3 rounds)."""
    sys.path.insert(0, KIT); import loud
    r = res(a); E = SPEC["encode"]; A = SPEC["audio"]
    wav = os.path.join(OUT, "audio", "line.wav"); norm = os.path.join(OUT, "audio", "line_norm.wav")
    rm = "_rm" if a.reduced_motion else ""
    v = os.path.join(OUT, "video"); os.makedirs(v, exist_ok=True)
    tag = clip_tag(a)
    fr = os.path.join(OUT, "frames", r + rm, "f_%04d.png")
    W, Hh = SPEC["video"][r]; S = SPEC["safe"]
    safe = (f",drawbox=x=0:y=0:w={W}:h={int(Hh*S['top_pct']/100)}:color=red@0.25:t=fill"
            f",drawbox=x=0:y={int(Hh*(1-S['bottom_pct']/100))}:w={W}:h={int(Hh*S['bottom_pct']/100)}:color=red@0.25:t=fill"
            f",drawbox=x={int(W*(1-S['right_pct']/100))}:y=0:w={int(W*S['right_pct']/100)}:h={Hh}:color=red@0.25:t=fill") if a.safe else ""
    venc = ["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "23"] if a.nvenc else ["-c:v", E["codec"], "-preset", E["preset"], "-crf", str(E["crf"])]
    jobs = [(f"cap-{tr}", f"ass='{ff_path(os.path.join(OUT, 'captions', f'captions_{tr}_{r}{rm}.ass'))}':fontsdir='{ff_path(fonts_dir())}'" + safe)
            for tr in SPEC["captions"]["tracks"]] + [("clean", "null" + safe)]
    margin = A.get("limiter_margin_db", 1.0)  # EDIT: limiter ceiling = TP − margin (AAC overshoot room)
    for rnd in range(3):
        lg = {} if a.dry_run else loud.prep(wav, norm, A["lufs"], A["tp"], margin, a.debug)
        res_ = {}
        for kind, vf in jobs:
            outp = os.path.join(v, f"{tag}_{kind}{'_safe' if a.safe else ''}.mp4")
            sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-thread_queue_size", "64", "-framerate", str(SPEC["video"]["fps"]), "-i", fr, "-i", norm,
                "-ar", "48000", "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest",
                "-vf", vf] + venc + [outp], dry=a.dry_run, check=True)
            if not a.dry_run:
                res_[os.path.basename(outp)] = loud.verdict(loud.measure(outp, A["lufs"], A["tp"]), A["lufs"], A["tp"])
        if a.dry_run:
            return
        worst_tp = max(x["TP"] for x in res_.values())
        if all(x["ok"] for x in res_.values()) or rnd == 2:
            break
        margin += max(0.3, worst_tp - A["tp"] + 0.2)
        print(f"[m1b] loudness miss (worst TP {worst_tp}) → limiter margin {margin:.1f} dB, re-encode", flush=True)
    linear = (lg or {}).get("normalization_type") == "linear"  # G-A11y R5: dynamic mode = pumping → fail
    ok = all(x["ok"] for x in res_.values()) and linear
    jsave(os.path.join(OUT, "loudness.json"), {"tag": tag, "target": {"I": A["lufs"], "TP": A["tp"]}, "prep": lg, "linear": linear,
                                               "limiter_margin_db": margin, "rounds": rnd + 1, "files": res_, "pass": ok})
    if not ok:
        print(f"[m1b] LOUDNESS FAIL after {rnd + 1} round(s) (linear={linear}) — see out\\loudness.json", flush=True)
    print("[m1b] loudness:", json.dumps(res_), flush=True)


def clip_tag(a):
    return f"{SPEC['shot_id']}_v{SPEC['version']}_{SPEC['video'][res(a)][0]}p{'_rm' if a.reduced_motion else ''}"


def sha_files(paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(open(os.path.join(KIT, p), "rb").read())
    return h.hexdigest()[:16]


def lum(c):
    c = [x / 255 for x in c]; c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def qa(man, vids=None):
    """Ship gates the kit can check itself: grade ran; caption scrim contrast on RENDERED frames (G-A11y R2)."""
    from PIL import Image
    out = {"grade_ok": (man.get("render") or {}).get("grade", "on") == "on"}
    C = SPEC["captions"]; clean = [v for v in (vids or []) if v.endswith("_clean.mp4")]
    if clean:
        worst = 1.0
        for t in (0.5, 1.5, 2.5, 3.5, 4.5):  # brightest pixel in the caption band, under the scrim
            png = os.path.join(OUT, "qa_frame.png")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", clean[0], "-frames:v", "1", png])
            im = Image.open(png).convert("RGB"); W, Hh = im.size
            box = im.crop((int(W * 0.15), int(Hh * C["band_top_pct"] / 100), int(W * 0.85), int(Hh * C["band_bottom_pct"] / 100)))
            worst = max(worst, max(lum(p) for p in (box.get_flattened_data() if hasattr(box, "get_flattened_data") else box.getdata())))
        s = int(C["outline"][1:3], 16) / 255  # scrim colour ≈ dark; composite: alpha·scrim + (1−alpha)·bg
        bgL = C["scrim_alpha"] * lum(tuple(int(C["outline"][i:i + 2], 16) for i in (1, 3, 5))) + (1 - C["scrim_alpha"]) * worst
        cr = lambda fg: (lum(tuple(int(fg[i:i + 2], 16) for i in (1, 3, 5))) + 0.05) / (bgL + 0.05)
        out.update({"caption_bg_worst_L": round(bgL, 3), "contrast_text": round(cr(C["text"]), 1), "contrast_key": round(cr(C["key"]), 1)})
        out["contrast_ok"] = out["contrast_text"] >= 4.5 and out["contrast_key"] >= 4.5
    out["pass"] = out["grade_ok"] and out.get("contrast_ok", False)
    print("[m1b] QA:", out)
    return out


def s_report(a):
    """One manifest per clip (H7, D-051) + RESULTS.md. for_drive\\ is emptied and refilled with THIS version only:
    the clips, one <clip>.manifest.json each, the sheets, the VTTs and RESULTS.md. Upload the files inside for_drive\\, not the folder."""
    t = jload(TIMES, {}); w = jload(os.path.join(OUT, "audio", "words.json"), {}); L = jload(os.path.join(OUT, "loudness.json"), {})
    rs = {k: jload(os.path.join(OUT, f"render_stats_{k}.json")) for k in ("ship", "preview", "design")}
    tag = clip_tag(a)
    vids = sorted(v for v in glob.glob(os.path.join(OUT, "video", tag + "_*.mp4")) if "_safe" not in v)  # this version only
    pal = jload(os.path.join(OUT, "palette_rendered.json"))
    base = {"shot_id": SPEC["shot_id"], "version": SPEC["version"], "made": datetime.now().isoformat(timespec="minutes"),
            "scene_hash": sha_files(["host.json", "blender_host.py", "tex.py", "lipsync.py", "captions.py", "loud.py"]),
            "host": SPEC["host"]["id"], "seed": SPEC["host"]["seed"], "voice": w.get("info"), "line_s": w.get("line_s"), "wpm": w.get("wpm"),
            "render": rs.get(res(a)), "gpu": cap(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"]),
            "ffmpeg": cap(["ffmpeg", "-version"]).splitlines()[0] if shutil.which("ffmpeg") else "n/a",
            "encode": SPEC["encode"], "timings_s": t, "palette": pal,
            "credit": SPEC["credit"], "ai_in_shot": False, "ai_in_reference": "Canva AI concept images (look only)"}
    base["qa"] = qa(base, vids)
    base["qa"]["loudness_ok"] = bool(L.get("pass")) and L.get("tag") == tag
    base["qa"]["palette_ok"] = bool(pal and pal.get("pass"))
    base["qa"]["pass"] = base["qa"]["pass"] and base["qa"]["loudness_ok"] and base["qa"]["palette_ok"]
    fd = os.path.join(OUT, "for_drive")
    if os.path.isdir(fd):
        shutil.rmtree(fd)  # copies only — the originals stay in out\\video and are never overwritten (H7: bump the version)
    os.makedirs(fd)
    mans = {}
    for v in vids:
        b = os.path.basename(v); kind = b[len(tag) + 1:-4]
        h = hashlib.sha256(open(v, "rb").read()).hexdigest()[:16]
        m = dict(base, clip=b, kind=kind, captions={"clean": None}.get(kind, kind.replace("cap-", "")), sha256_16=h,
                 mb=round(os.path.getsize(v) / 1e6, 2), loudness=(L.get("files") or {}).get(b), loudness_prep=L.get("prep"))
        mp = os.path.join(fd, b[:-4] + ".manifest.json"); jsave(mp, m); mans[b] = m
        shutil.copy2(v, fd)
    for p in glob.glob(os.path.join(OUT, "sheet", "sheet_*.png")) + glob.glob(os.path.join(OUT, "captions", "captions_*.vtt")):
        shutil.copy2(p, fd)
    Ln = SPEC["line"]  # H5: plain transcript beside the captions
    open(os.path.join(fd, f"{tag}_transcript.txt"), "w", encoding="utf-8").write(
        f"{SPEC['shot_id']} v{SPEC['version']} — {SPEC['host']['name']} (host)\nEN (spoken): {Ln['en']}\nHI (caption only; audio is English): {Ln['hi']}\n")
    jsave(os.path.join(OUT, "manifest.json"), dict(base, clips=list(mans)))  # run summary, local only
    lines = ["# M1b results — paste into the chat", "", f"- Made {base['made']} · {tag} · scene {base['scene_hash']} · {base['gpu']}",
             f"- Line {base['line_s']} s · {base['wpm']} wpm · timings {(base['voice'] or {}).get('timings')}",
             f"- QA: {'PASS' if base['qa']['pass'] else 'FAIL'} · {base['qa']}"]
    for b, x in (L.get("files") or {}).items():
        lines.append(f"- Loudness {b}: I {x['I']} LUFS · TP {x['TP']} dBTP {'OK' if x['ok'] else 'FAIL'} (target −14 ±0.5 / ≤ −1.5)")
    if pal:
        for tg, rr in pal.items():
            if tg.startswith(("front", "shot")) and isinstance(rr, dict):
                lines.append(f"- ΔE tokens {tg}: " + " · ".join(f"{r} {x['median']} {x['worst_de']} ({x['vs']},{x['vision']}){' OK' if x['ok'] else (' LOW' if x['ok'] is False else '')}" for r, x in rr.items()))
        for tg, sep in (pal.get("separation") or {}).items():
            lines.append(f"- Host vs plate {tg}: edge contrast p10 {sep['p10_ratio']}:1 · ΔE p10 {sep['p10_de']} · {'OK' if sep['ok'] else 'FAIL'} (≥ 3:1 on 90 % of the edge)")
        if pal.get("separation_missing"):
            lines.append(f"- Host vs plate NOT MEASURED for {pal['separation_missing']} → gate FAIL (run sheet + shot first)")
        for tg, sep in (pal.get("separation_shawl_info") or {}).items():
            lines.append(f"- Shawl vs plate {tg} (info): p10 {sep['p10_ratio']}:1 · {round(100 * sep['share_ok'])} % ≥ 3:1")
        lines.append(f"- Palette gate (swatches ≥ 15 · host/plate edge ≥ 3:1 · tokens on screen {pal.get('tokens_on_screen') or 'none'}): {pal.get('pass')}")
    for m_ in ("sheet", "shot"):
        bl = jload(os.path.join(OUT, f"build_log_{m_}.json"))
        if bl:
            lines.append(f"- build {m_}: shawl {bl.get('shawl')} · failed parts {bl.get('failed') or 'none'} · {bl.get('seconds')} s")
            lines += [f"  - note: {n}" for n in bl.get("notes", [])]
    lines += [f"- {k}: {v} s" for k, v in t.items()]
    lines += [f"- {b}: {m['mb']} MB · sha {m['sha256_16']}" for b, m in mans.items()]
    open(os.path.join(OUT, "RESULTS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    shutil.copy2(os.path.join(OUT, "RESULTS.md"), fd)
    print("\n".join(lines)); print("[m1b] upload the FILES inside out\\for_drive\\ (not the folder) to Drive › renders › bakeoff › host")


STEPS = {"check": s_check, "tts": s_tts, "tex": s_tex, "sheet": s_sheet, "palette": s_palette, "shot": s_shot, "captions": s_captions,
         "encode": s_encode, "report": s_report, "compare": s_compare}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=list(STEPS) + ["all", "t1b"])
    ap.add_argument("--only", help="shot A|B, or one sheet tile (front, side, warm, curious, …)")
    ap.add_argument("--preview", action="store_true", help="360×640 / small tiles, 8 samples")
    ap.add_argument("--debug", action="store_true", help="verbose + save out\\debug\\host_*.blend")
    ap.add_argument("--dry-run", action="store_true", help="print commands; render and write nothing")
    ap.add_argument("--cycles", action="store_true", help="Cycles instead of Eevee (slow: ~5.6 s/frame at 720p)")
    ap.add_argument("--nvenc", action="store_true", help="h264_nvenc instead of x264")
    ap.add_argument("--safe", action="store_true", help="paint the 9:16 safe zones (review only, never publish)")
    ap.add_argument("--reduced-motion", action="store_true", help="H5 variant: no push-in, no caption pop, no book snap")
    ap.add_argument("--palette-pass", action="store_true", help="sheet only: Standard view transform for ΔE checks on rendered pixels")
    ap.add_argument("--no-sim", action="store_true", help="skip the cloth sim (procedural shawl) — fast look-dev")
    ap.add_argument("--strict", action="store_true", help="stop on the first failing build part (default: log it and go on)")
    ap.add_argument("--onion", action="store_true", help="compare: also write onion boards (ours at 50 %% over the ref, silhouettes aligned)")
    a = ap.parse_args()
    if a.step == "all":
        order = ["check", "tts", "tex", "sheet", "shot", "palette", "captions", "encode", "report", "compare"]
    elif a.step == "t1b":  # D-051: exactly what owner check T1b needs, one run, ship res; reuses line.wav if the voice is unchanged
        a.preview = False
        need_tts = not os.path.exists(os.path.join(OUT, "audio", "visemes.json"))
        order = ["check"] + (["tts"] if need_tts else []) + ["tex", "sheet", "shot", "palette", "captions", "encode", "report", "compare"]
    else:
        order = [a.step]
    for s in order:
        timed(s, STEPS[s], a)


if __name__ == "__main__":
    main()
