#!/usr/bin/env python3
"""Biology Studio — still regression (RULES C11): a viewer or scene change re-renders every scene still and compares.

For every scene in content/<book>/scenes/index.json and each of its `stills` days (docs/scene-spec.md §3), opens the app in
still mode (`?still=1` → the stage alone, 960×540, device pixel ratio 1) in headless Chromium (WebGL via SwiftShader),
saves the WebGL canvas and compares it with tools/stills/baseline/<id>_d<day>.png. Differences must be intended: review the
diff images, then accept with --update. Also records triangles + draw calls per still against the phone budget (H8) and
writes a "look" contact sheet (stage with labels, stamp, scale bar, gizmo) for G-Art.

Run from the repo root:  python tools/stills/stills.py [--update] [--only sc-E00.01.04] [--preview] [--debug] [--dry-run]
  --update  write new baselines (after review)   --preview  first still day per scene only   --debug  keep diff images + print metrics
Needs: pip install playwright pillow numpy + python -m playwright install chromium. Exit 1 on any difference, missing baseline or
budget overrun. Writes out/stills/ (report.md, canvas PNGs, look/, diff/, contact-look.png). Owner doc: docs/scene-spec.md §9.
EDIT: tolerances below (SwiftShader output is stable for one Chromium version — CI pins Playwright to the same version).
"""
import argparse, asyncio, base64, functools, http.server, json, os, socketserver, sys, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent / "baseline"
# EDIT: a still passes if the mean absolute difference < MEAN_MAX (0–255) and < SHARE_MAX of pixels differ by > PIX_DELTA
MEAN_MAX, SHARE_MAX, PIX_DELTA = 0.5, 0.0005, 24
W, H = 1280, 720   # viewport (desktop class); the still stage itself is 960×540


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/"


def plan(a):
    idx = json.loads((ROOT / "content" / a.book / "scenes" / "index.json").read_text(encoding="utf-8"))
    out = []
    for s in idx["scenes"]:
        if a.only and s["id"] != a.only:
            continue
        S = json.loads((ROOT / "content" / a.book / "scenes" / f"{s['id']}.json").read_text(encoding="utf-8"))
        days = S.get("stills") or [k["day"] for k in S["days"]]
        out += [(s["id"], d) for d in (days[:1] if a.preview else days)]
    return out


def fmt(d):
    return str(int(d)) if float(d).is_integer() else f"{d:.1f}"


def compare(new, base, diff_path, keep):
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(new).convert("RGB"), dtype=np.int16)
    b = np.asarray(Image.open(base).convert("RGB"), dtype=np.int16)
    if a.shape != b.shape:
        return {"ok": False, "why": f"size {a.shape[1]}×{a.shape[0]} vs baseline {b.shape[1]}×{b.shape[0]}"}
    d = np.abs(a - b)
    mean, share = float(d.mean()), float((d.max(axis=2) > PIX_DELTA).mean())
    ok = mean < MEAN_MAX and share < SHARE_MAX
    if not ok or keep:
        m = (d.max(axis=2) > PIX_DELTA)
        vis = (np.asarray(Image.open(new).convert("RGB")) * 0.35).astype("uint8")
        vis[m] = [255, 0, 170]
        Image.fromarray(vis).save(diff_path)
    return {"ok": ok, "mean": round(mean, 3), "share": round(share * 100, 3)}


async def run(a, items):
    from playwright.async_api import async_playwright
    srv, base = serve()
    out = ROOT / "out" / "stills"
    for sub in ("", "look", "diff"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    BASE.mkdir(parents=True, exist_ok=True)
    budget = 150000
    rep = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "items": [], "errors": []}
    async with async_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if os.environ.get("CHROME"):
            kw["executable_path"] = os.environ["CHROME"]
        br = await p.chromium.launch(**kw)
        rep["chromium"] = br.version
        ctx = await br.new_context(viewport={"width": W, "height": H}, device_scale_factor=1, color_scheme="dark")
        page = await ctx.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        first = True
        for sid, day in items:
            url = f"{base}?still=1&test=1&debug=0#scene={sid}&day={fmt(day)}"
            if first:
                await page.goto(url)
                first = False
            else:
                await page.evaluate(f"location.hash='#scene={sid}&day={fmt(day)}'")
            await page.wait_for_function(f"window.VW_READY===true && ROUTE.id==='{sid}'", timeout=30000)
            await page.evaluate(f"SC.eng.setDay({day}); scDay({day},true); SC.eng.render()")
            await page.wait_for_timeout(250)
            budget = await page.evaluate("CONFIG.viewer.budget.phoneTris")
            info = await page.evaluate("SC.eng.info()")
            name = f"{sid}_d{fmt(day)}.png"
            data = await page.evaluate("SC.canvas.toDataURL('image/png')")   # the WebGL pixels only (overlay is DOM; preserveDrawingBuffer in still mode)
            (out / name).write_bytes(base64.b64decode(data.split(",", 1)[1]))
            await page.locator("#vwStage").screenshot(path=str(out / "look" / name))
            it = {"still": name, "triangles": info["triangles"], "calls": info["calls"], "px": info["px"]}
            bfile = BASE / name
            if a.update:
                bfile.write_bytes((out / name).read_bytes())
                it.update(ok=True, note="baseline written")
            elif not bfile.exists():
                it.update(ok=False, note="no baseline — review out/stills/look, then run with --update")
            else:
                it.update(compare(out / name, bfile, out / "diff" / name, a.debug))
            if info["triangles"] > budget:
                it["ok"] = False
                it["note"] = f"{info['triangles']} triangles > phone budget {budget} (H8)"
            for e in errs:
                rep["errors"].append(f"{name}: {e}")
            errs.clear()
            rep["items"].append(it)
            if a.debug:
                print(json.dumps(it, ensure_ascii=False))
        await br.close()
    srv.shutdown()
    contact(rep["items"], out)
    return rep


def contact(items, out):
    from PIL import Image, ImageDraw
    ims = [(i["still"], Image.open(out / "look" / i["still"]).convert("RGB")) for i in items if (out / "look" / i["still"]).exists()]
    if not ims:
        return
    tw, cols = 480, 3
    th = int(ims[0][1].height * tw / ims[0][1].width)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 16) + 16, rows * (th + 30) + 40), "#E9E8E3")
    d = ImageDraw.Draw(sheet)
    d.text((12, 10), "Biology Studio · stills · look sheet (G-Art)", fill="#111111")
    for n, (label, im) in enumerate(ims):
        x, y = 12 + (n % cols) * (tw + 16), 34 + (n // cols) * (th + 30)
        d.text((x, y), label, fill="#111111")
        sheet.paste(im.resize((tw, th)), (x, y + 14))
    sheet.save(out / "contact-look.png", optimize=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", default="E")
    ap.add_argument("--only")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    items = plan(a)
    if a.dry_run:
        print(f"{len(items)} still(s): " + ", ".join(f"{s} d{fmt(d)}" for s, d in items))
        return 0
    rep = asyncio.run(run(a, items))
    bad = [i for i in rep["items"] if not i.get("ok")] + rep["errors"]
    lines = [f"# Stills — {rep['started']} · Chromium {rep.get('chromium')}", "",
             f"{len(rep['items'])} stills · {len(bad)} problem(s) · tolerance mean < {MEAN_MAX}, < {SHARE_MAX*100:.1f} % pixels off by > {PIX_DELTA}", "",
             "| Still | Result | Mean diff | % pixels | Triangles | Calls |", "|---|---|---|---|---|---|"]
    for i in rep["items"]:
        lines.append(f"| {i['still']} | {'✅' if i.get('ok') else '❌'} {i.get('note', i.get('why', ''))} | {i.get('mean', '—')} | {i.get('share', '—')} | {i['triangles']} | {i['calls']} |")
    lines += [f"- ❌ {e}" for e in rep["errors"]]
    out = ROOT / "out" / "stills"
    (out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n".join(lines))
    print(("FAIL" if bad else "PASS") + f": {len(bad)} problem(s) · out/stills/report.md · look sheet out/stills/contact-look.png")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
