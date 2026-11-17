#!/usr/bin/env python3
"""Biology Studio — layout check (RULES C8 + C13, master plan §8a → build/design-plan.md §2).

Serves the repo, opens every screen at every size of the §8a matrix (phones + tablets in portrait AND landscape,
desktop sizes), at 100 % and 125 % text, light and dark, and runs the in-app audit (src/js/90-layout-audit.js):
overlap · spill · page wider than the screen · tap < --tap · text < --fs-min · fixed bars over controls.
Also checks: the device class each size gets, rotating keeps the place, the in-app tests (?test=1), and the D-031
colour re-check on the Colour key screen (fill or edge >= 3.5:1, label text >= 4.5:1, accent >= 3:1) in both themes.
Writes out/layout-check/report.json, report.md and contact sheets (one PNG per device class) for G-Art.

Run from the repo root:  python tools/layout-check/check.py [--preview] [--only concept] [--debug] [--dry-run] [--out DIR]
Needs: pip install playwright pillow  +  python -m playwright install chromium   (or CHROME=/path/to/chrome)
Exit code 1 if any issue. Owner doc: build/design-plan.md §7. EDIT: sizes in MATRIX, screens in SCREENS.
"""
import argparse, asyncio, functools, http.server, json, os, socketserver, sys, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# EDIT: §8a test matrix (CSS px, portrait for phones/tablets; landscape is added by swapping)
MATRIX = {
    "phone":   [(360, 640), (390, 844), (412, 915), (430, 932)],
    "tablet":  [(768, 1024), (800, 1280), (820, 1180), (1024, 1366)],
    "desktop": [(1280, 720), (1366, 768), (1440, 900), (1920, 1080), (2560, 1440)],
}
PREVIEW = [("phone", 390, 844), ("phone", 844, 390), ("tablet", 820, 1180), ("tablet", 1180, 820), ("desktop", 1440, 900)]
# EDIT: screens (hash routes)
SCREENS = {
    "today": "today", "map": "map", "chapter": "map=E05", "concept": "concept=E05.02.01",
    "crosstab": "x=layer&y=day", "cell": "x=layer&y=day&cell=meso%7CWk%203", "settings": "settings", "colours": "colours",
}


def expected_class(kind, w, h):
    short, land = min(w, h), w > h
    if kind == "desktop":
        return "dev-d"
    if short < 600:
        return "dev-pl" if land else "dev-p"
    if short < 1024:
        return "dev-tl" if land else "dev-tp"
    return "dev-tl" if land else "dev-tp"


def viewports(preview):
    if preview:
        return [(k, w, h) for k, w, h in PREVIEW]
    out = []
    for kind, sizes in MATRIX.items():
        for w, h in sizes:
            out.append((kind, w, h))
            if kind != "desktop":
                out.append((kind, h, w))
    return out


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/"


async def run(a):
    from playwright.async_api import async_playwright
    srv, base = serve()
    vps = viewports(a.preview)
    themes = ["light"] if a.preview else ["light", "dark"]
    texts = [100] if a.preview else [100, 125]
    screens = {k: v for k, v in SCREENS.items() if not a.only or k == a.only}
    out = Path(a.out); (out / "shots").mkdir(parents=True, exist_ok=True)
    report = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "base": base, "runs": [], "issues": [], "tests": None, "colours": [], "rotate": []}
    shots = {}  # class -> list of (label, path)
    async with async_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if os.environ.get("CHROME"):
            kw["executable_path"] = os.environ["CHROME"]
        try:
            browser = await p.chromium.launch(**kw)
        except Exception:
            browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for kind, w, h in vps:
            touch = kind != "desktop"
            for theme in themes:
                for text in texts:
                    ctx = await browser.new_context(viewport={"width": w, "height": h}, has_touch=touch, is_mobile=touch, device_scale_factor=1, color_scheme=theme)
                    await ctx.add_init_script(f"try{{localStorage.setItem('biostudio.theme','{theme}')}}catch(e){{}}")
                    if text != 100:
                        await ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='html{font-size:%d%%!important}';document.head.appendChild(s);});" % text)
                    if a.debug:
                        await ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>document.documentElement.classList.add('dbg-boxes'));")
                    page = await ctx.new_page()
                    errors = []
                    page.on("pageerror", lambda e: errors.append(str(e)))
                    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                    first = True
                    for sname, route in screens.items():
                        if first:
                            await page.goto(f"{base}?test=1&debug=0#{route}")
                            await page.wait_for_function("window.BOOTED && MAPD && (MAPD.M || MAPD.err)", timeout=20000)
                            first = False
                        else:
                            await page.evaluate(f"location.hash='#{route}'")
                        await page.wait_for_timeout(120)
                        cls = await page.evaluate("[...document.documentElement.classList].find(c=>c.startsWith('dev-'))")
                        got_theme = await page.evaluate("document.documentElement.dataset.theme")
                        want = expected_class(kind, w, h)
                        label = f"{w}x{h} {theme} {text}% {sname}"
                        iss = await page.evaluate("layoutAudit()")
                        await page.evaluate("scrollTo(0,document.scrollingElement.scrollHeight)")
                        await page.wait_for_timeout(60)
                        iss2 = [i for i in await page.evaluate("layoutAudit()") if i["kind"] == "fixed-over"]
                        await page.evaluate("scrollTo(0,0)")
                        found = [dict(i, at=label) for i in iss + iss2]
                        if cls != want:
                            found.append({"kind": "device-class", "what": f"got {cls}, want {want}", "at": label})
                        if got_theme != theme:
                            found.append({"kind": "theme", "what": f"page drew {got_theme}, asked for {theme}", "at": label})
                        for e in errors:
                            found.append({"kind": "js-error", "what": e, "at": label})
                        errors.clear()
                        if sname == "colours":
                            ck = await page.evaluate("window.CK_LAST")
                            ui = ck.get("ui", {})
                            if ui and not (ui["lineStrong"] >= 3 and ui["muted"] >= 4.5 and ui["heat3"] >= 4.5):
                                found.append({"kind": "colour", "what": "ui " + json.dumps({k: round(v, 2) for k, v in ui.items()}), "at": label})
                            for k, r in ck.items():
                                if not isinstance(r, dict) or k == "ui":
                                    continue
                                ok = True
                                if k == "accent":
                                    ok = r["cFill"] >= 3 and r["cText"] >= 4.5 and r.get("cAccentText", 9) >= 4.5
                                else:
                                    ok = (r["cFill"] >= 3.5 or r["cEdge"] >= 3.5) and r["cText"] >= 4.5
                                report["colours"].append({"at": label, "token": k, "fill": r["fill"], "cFill": round(r["cFill"], 2), "cEdge": round(r.get("cEdge", 0), 2), "cText": round(r["cText"], 2), "ok": ok})
                                if not ok:
                                    found.append({"kind": "colour", "what": f"{k} fill {r['cFill']:.2f} edge {r.get('cEdge', 0):.2f} text {r['cText']:.2f}", "at": label})
                        report["runs"].append({"at": label, "class": cls, "issues": len(found)})
                        report["issues"] += found
                        if text == 100 and theme == "light" or (a.preview and theme == "light"):
                            path = out / "shots" / f"{cls}_{w}x{h}_{theme}_{sname}.png"
                            await page.screenshot(path=str(path))
                            shots.setdefault(cls, []).append((f"{w}×{h} {sname}", path))
                        elif text == 125 and theme == "light" and sname in ("concept", "chapter", "settings"):
                            path = out / "shots" / f"{cls}_{w}x{h}_125_{sname}.png"
                            await page.screenshot(path=str(path))
                            shots.setdefault(cls + " 125", []).append((f"{w}×{h} {sname} 125%", path))
                        elif text == 100 and theme == "dark" and sname in ("concept", "colours", "today", "crosstab"):
                            path = out / "shots" / f"{cls}_{w}x{h}_{theme}_{sname}.png"
                            await page.screenshot(path=str(path))
                            shots.setdefault(cls + " dark", []).append((f"{w}×{h} {sname}", path))
                    if report["tests"] is None:
                        report["tests"] = await page.evaluate("appTests()")
                    await ctx.close()
        # rotate keeps place (§8a rule 2): phone portrait → landscape → portrait on a concept + scrolled chapter
        ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        page = await ctx.new_page()
        await page.goto(f"{base}?test=1&debug=0#map=E05")
        await page.wait_for_function("window.BOOTED && MAPD && MAPD.M", timeout=20000)
        await page.evaluate("scrollTo(0,400)"); y0 = await page.evaluate("scrollY")
        for vw, vh in [(844, 390), (390, 844)]:
            await page.set_viewport_size({"width": vw, "height": vh}); await page.wait_for_timeout(200)
            st = await page.evaluate("({h:location.hash,cls:DEV.cls,y:scrollY,len:history.length})")
            ok = st["h"] == "#map=E05" and st["cls"] == ("dev-pl" if vw > vh else "dev-p") and st["y"] > 0
            report["rotate"].append(dict(st, size=f"{vw}x{vh}", ok=ok, y0=y0))
            if not ok:
                report["issues"].append({"kind": "rotate", "what": json.dumps(st), "at": f"{vw}x{vh}"})
        await ctx.close()
        # real mode (no ?test): saving survives a reload; Back at home stays in the app (C8)
        report["flows"] = []
        ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        page = await ctx.new_page()
        await page.goto(f"{base}#concept=E05.02.01")
        await page.wait_for_function("window.BOOTED && MAPD && MAPD.M && STORE.mode==='idb'", timeout=20000)
        await page.wait_for_timeout(900)  # debounced save
        await page.reload(); await page.wait_for_function("window.BOOTED && STORE.mode==='idb'", timeout=20000)
        saved = await page.evaluate("!!state.visited['E05.02.01'] && STORE.rev>0")
        report["flows"].append({"flow": "save survives reload", "ok": saved})
        page2 = await ctx.new_page()   # fresh open at Today, then Back
        await page2.goto(f"{base}#today"); await page2.wait_for_function("window.BOOTED", timeout=20000); await page2.wait_for_timeout(150)
        await page2.go_back(); await page2.wait_for_timeout(250)
        page_guard = page2
        guard = await page_guard.evaluate("({h:location.hash, toast:(document.querySelector('#toast')||{}).textContent||''})")
        ok_guard = guard["h"] == "#today" and "Back again" in guard["toast"]
        report["flows"].append({"flow": "Back at home asks before leaving", "ok": ok_guard, "seen": guard})
        bad = await page.evaluate("location.hash='#concept=%E0%A4'; new Promise(r=>setTimeout(()=>r(ROUTE.name),150))")
        report["flows"].append({"flow": "malformed address falls back", "ok": bad in ("today", "concept"), "seen": bad})
        for f in report["flows"]:
            if not f["ok"]:
                report["issues"].append({"kind": "flow", "what": f["flow"] + " " + json.dumps(f.get("seen", "")), "at": "390x844 real mode"})
        await ctx.close()
        await browser.close()
    srv.shutdown()
    for t in report["tests"] or []:
        if not t["ok"]:
            report["issues"].append({"kind": "app-test", "what": t["name"] + " " + str(t["info"]), "at": "?test=1"})
    contact(shots, out)
    (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    write_md(report, out, len(vps), themes, texts, screens)
    return report


def contact(shots, out):
    from PIL import Image, ImageDraw
    for cls, items in shots.items():
        thumbs = []
        for label, path in items:
            im = Image.open(path).convert("RGB")
            tw = 300 if im.width <= 1000 else 420
            im = im.resize((tw, int(im.height * tw / im.width)))
            thumbs.append((label, im))
        cols = 6 if thumbs[0][1].width <= 300 else 4
        cw = max(t.width for _, t in thumbs) + 16
        rows = [thumbs[i:i + cols] for i in range(0, len(thumbs), cols)]
        H = sum(max(t.height for _, t in r) + 34 for r in rows) + 40
        sheet = Image.new("RGB", (cw * cols + 16, H), "#E9E8E3")
        d = ImageDraw.Draw(sheet)
        d.text((12, 10), f"Biology Studio · layout-check contact sheet · {cls}", fill="#111111")
        y = 36
        for r in rows:
            x = 12
            for label, t in r:
                d.text((x, y), label, fill="#111111")
                sheet.paste(t, (x, y + 16))
                x += cw
            y += max(t.height for _, t in r) + 34
        sheet.save(out / f"contact-{cls.replace(' ', '-')}.png", optimize=True)


def write_md(r, out, nvp, themes, texts, screens):
    kinds = {}
    for i in r["issues"]:
        kinds[i["kind"]] = kinds.get(i["kind"], 0) + 1
    ok_tests = sum(t["ok"] for t in r["tests"] or [])
    lines = [f"# Layout check — {r['started']}", "",
             f"{nvp} viewports × {len(themes)} themes × {len(texts)} text sizes × {len(screens)} screens = {len(r['runs'])} checks.",
             f"In-app tests: {ok_tests}/{len(r['tests'] or [])} · rotate: {sum(x['ok'] for x in r['rotate'])}/{len(r['rotate'])} · flows: {sum(x['ok'] for x in r.get('flows', []))}/{len(r.get('flows', []))} · colour re-checks: {sum(c['ok'] for c in r['colours'])}/{len(r['colours'])}",
             "", "**Issues:** " + (", ".join(f"{k} {v}" for k, v in sorted(kinds.items())) if kinds else "none ✅"), ""]
    for i in r["issues"][:200]:
        lines.append(f"- `{i['kind']}` {i['what']} — {i['at']}")
    (out / "report.md").write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preview", action="store_true", help="5 key sizes, light, 100 %% text")
    ap.add_argument("--only", choices=list(SCREENS), help="one screen")
    ap.add_argument("--debug", action="store_true", help="outline every box in the screenshots")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, open nothing")
    ap.add_argument("--out", default=str(ROOT / "out" / "layout-check"))
    a = ap.parse_args()
    vps = viewports(a.preview)
    if a.dry_run:
        print(f"{len(vps)} viewports:", ", ".join(f"{w}x{h}->{expected_class(k, w, h)}" for k, w, h in vps))
        print("screens:", ", ".join(SCREENS if not a.only else [a.only]))
        return 0
    r = asyncio.run(run(a))
    n = len(r["issues"])
    print((Path(a.out) / "report.md").read_text()[:3000])
    print(f"{'FAIL' if n else 'PASS'}: {n} issues · report {a.out}/report.md · contact sheets {a.out}/contact-*.png")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
