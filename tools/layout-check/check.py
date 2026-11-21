#!/usr/bin/env python3
"""Biology Studio — layout check (RULES C8 + C13, master plan §8a → build/design-plan.md §2). V1: + 3D list, viewer (2 scenes), viewer rotate.
S1: + Studio (list, card on G-Sci and G-Learn, calibration), Studio rotate, Studio review round trip + reviewer = maker blocked + edit reopens.
W1: + progress map (Map, Board, Your inputs, 3 step pages), step page rotate, map with done shown, progress outside testing mode.
L1: + cards list, card reader (concept, guide, clinical), Remember deck; card mid-Check survives rotate (question, 3D day, scroll).
L1F: + D-053 fold (Check hides the card text; Read again ends the run unscored), saved app/savedAt, pins clear of overlays + pinned labels after a
    label drill, the day drill keeps the ruler clear of overlays (2 phone sizes), mid-word titles (in-app audit). V2: + notochord card; every drill type (the demo fixture ?fixture=drills) on 5 classes × 100/125 % with audit + contact sheet; label pins drawn;
    rotate mid-drill moves the stage (in the Check ↔ beside it) and keeps the view; Try it gets its view back; WebGL context loss redraws.

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
    "scenes": "scene", "viewer": "scene=sc-E00.01.04&day=16", "viewer-axes": "scene=sc-E00.01.01&day=17",
    "studio": "studio", "studio-card": "studio=E05.01.01", "studio-learn": "studio=E05.01.01&gate=G-Learn", "calib": "calib",
    "progress": "progress", "progress-board": "progress=board", "progress-inputs": "progress=inputs",
    "step": "step=C1", "step-blocked": "step=P1", "step-idea": "step=IB01",
    "cards": "cards", "card": "card=E05.01.01", "card-noto": "card=E05.02.01", "card-guide": "card=E00.01.06", "card-clin": "card=E05.05.01", "deck": "deck",
    # H2 Reviewer mode — opened with the demo issues (?fixture=review, never GitHub); keep these last (the page reloads once with the fixture)
    "review": "review", "review-news": "review=news", "review-mine": "review=mine", "rcard": "rcard=E05.01.02", "rcard-draft": "rcard=E06.02.01",
    "rtour": "rtour", "rtour-3": "rtour=3", "updates": "updates",
}
REVIEW_SCREENS = ("review", "review-news", "review-mine", "rcard", "rcard-draft", "rtour", "rtour-3", "updates")


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
    FONT[0] = a.font
    vps = viewports(a.preview)
    themes = ["light"] if a.preview else ["light", "dark"]
    texts = [100] if a.preview else [100, 125]
    screens = {k: v for k, v in SCREENS.items() if not a.only or k == a.only}
    out = Path(a.out); (out / "shots").mkdir(parents=True, exist_ok=True)
    report = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "base": base, "runs": [], "issues": [], "tests": None, "colours": [], "rotate": [], "_out": str(out)}
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
                    if a.font:
                        await ctx.add_init_script(FONT_JS % a.font)
                    if a.debug:
                        await ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>document.documentElement.classList.add('dbg-boxes'));")
                    page = await ctx.new_page()
                    errors = []
                    page.on("pageerror", lambda e: errors.append(str(e)))
                    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                    first = True
                    in_fx = False
                    for sname, route in screens.items():
                        if sname in REVIEW_SCREENS and not in_fx:   # H2: one reload into the demo issues; the next screens change the hash only
                            await page.goto(f"{base}?test=1&debug=0&fixture=review#{route}")
                            await page.wait_for_function("window.BOOTED", timeout=20000)
                            in_fx, first = True, False
                        elif first:
                            await page.goto(f"{base}?test=1&debug=0#{route}")
                            await page.wait_for_function("window.BOOTED && MAPD && (MAPD.M || MAPD.err)", timeout=20000)
                            first = False
                        else:
                            await page.evaluate(f"location.hash='#{route}'")
                        await page.wait_for_timeout(120)
                        if route.startswith("scene="):   # 3D viewer: wait for the engine + first frame (V1)
                            sid = route.split("=")[1].split("&")[0]
                            await page.wait_for_function(f"window.VW_READY===true && ROUTE.id==='{sid}'", timeout=30000)
                            await page.wait_for_timeout(80)
                        if route.startswith(("studio", "calib")):   # Studio: wait for cards + sources (S1)
                            await page.wait_for_function(f"window.ST_READY==={json.dumps(route)}", timeout=20000)
                        if route.startswith(("cards", "card=", "deck")):   # L1: cards loaded + drawn; a card also waits for its inline 3D
                            await page.wait_for_function(f"window.LN_READY==={json.dumps(route)}", timeout=20000)
                            if route.startswith("card="):
                                await page.wait_for_function("window.VW_READY===true", timeout=30000)
                                await page.wait_for_timeout(80)
                        if sname in REVIEW_SCREENS:   # H2: cards, demo issues and the build log loaded + drawn
                            await page.wait_for_function(f"window.RV_READY==={json.dumps(route)} && (!['review','review=news','review=mine'].includes(window.RV_READY) || (RV.idx && RV.upd && !RV.busy))", timeout=20000)
                            if route.startswith("review"):
                                await page.evaluate("render()")
                            await page.wait_for_timeout(80)
                        if route.startswith(("progress", "step")):   # progress map: wait for steps.json + draw (W1)
                            await page.wait_for_function(f"window.TR_READY==={json.dumps(route)}", timeout=20000)
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
                        elif text == 125 and theme == "light" and sname in ("concept", "chapter", "settings", "viewer", "viewer-axes", "scenes", "studio-card", "calib", "progress", "step", "review", "rcard", "rtour"):
                            path = out / "shots" / f"{cls}_{w}x{h}_125_{sname}.png"
                            await page.screenshot(path=str(path))
                            shots.setdefault(cls + " 125", []).append((f"{w}×{h} {sname} 125%", path))
                        elif text == 100 and theme == "dark" and sname in ("concept", "colours", "today", "crosstab", "viewer", "studio-card", "progress", "progress-board", "step", "review-mine", "rcard"):
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
        # rotate keeps place in the 3D viewer (§2 rule 2, V1): day, camera, cut and open tab survive portrait → landscape → portrait
        ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        page = await ctx.new_page()
        await page.goto(f"{base}?test=1&debug=0#scene=sc-E00.01.04&day=16")
        await page.wait_for_function("window.VW_READY===true", timeout=30000)
        await page.evaluate("SC.eng.orbitBy(30,-10); scSave(); document.querySelector('[data-vw=tab][data-t=view]').click()")
        s0 = await page.evaluate("({h:location.hash, cam:SC.eng.state(), tab:SC.tab})")
        for vw, vh in [(844, 390), (390, 844)]:
            await page.set_viewport_size({"width": vw, "height": vh}); await page.wait_for_timeout(250)
            st = await page.evaluate("({h:location.hash, cam:SC.eng.state(), tab:SC.tab, cls:DEV.cls, w:SC.canvas.clientWidth})")
            ok = st["h"] == s0["h"] and abs(st["cam"]["az"] - s0["cam"]["az"]) < 1e-6 and st["cam"]["day"] == s0["cam"]["day"] and st["tab"] == "view" and st["w"] > 100
            report["rotate"].append({"size": f"{vw}x{vh} viewer", "ok": ok, "h": st["h"], "cls": st["cls"]})
            if not ok:
                report["issues"].append({"kind": "rotate", "what": "viewer " + json.dumps(st), "at": f"{vw}x{vh}"})
        await ctx.close()
        # Studio (S1): rotate keeps the card, gate and draft edits; a review round trip in the UI (draft → reviewed); reviewer = maker is blocked; an edit reopens
        if not a.only or a.only.startswith(("studio", "calib")):
            await studio_flows(browser, base, report)
        # progress map (W1): rotate keeps the step page and scroll; the map with Done shown fits every class
        if not a.only or a.only.startswith(("progress", "step")):
            await tracker_flows(browser, base, report, vps if not a.preview else PREVIEW)
        # L1 learning core: mid-Check rotate keeps the question, 3D day and scroll; real mode: statuses + deck survive a reload
        if not a.only or a.only.startswith(("card", "deck")):
            await learn_flows(browser, base, report)
        if not a.only or a.only.startswith(("card", "drill")):
            await drill_flows(browser, base, report, a.preview)
        if not a.only or a.only.startswith(("review", "rcard", "rtour", "updates")):
            await review_flows(browser, base, report)
        # real mode (no ?test): saving survives a reload; Back at home stays in the app (C8)
        report.setdefault("flows", [])
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
        st = await page.evaluate("location.hash='#studio'; new Promise(r=>setTimeout(()=>r({nav:!!document.querySelector('[data-nav=studio]'), msg:document.querySelector('#view').textContent.includes('testing mode only')}),200))")
        report["flows"].append({"flow": "Studio hidden outside testing mode", "ok": (not st["nav"]) and st["msg"], "seen": st})
        st = await page.evaluate("location.hash='#progress'; new Promise(r=>{const t0=Date.now();(function w(){if(window.TR_READY==='progress'||Date.now()-t0>8000)r({nav:!!document.querySelector('[data-nav=progress]'), nodes:document.querySelectorAll('.tr-node').length});else setTimeout(w,100);})();})")
        report["flows"].append({"flow": "progress opens outside testing mode, not in the nav", "ok": (not st["nav"]) and st["nodes"] > 5, "seen": st})
        for f in report["flows"]:
            if not f["ok"]:
                report["issues"].append({"kind": "flow", "what": f["flow"] + " " + json.dumps(f.get("seen", "")), "at": "390x844 real mode"})
        await ctx.close()
        await browser.close()
    srv.shutdown()
    for t in report["tests"] or []:
        if not t["ok"]:
            report["issues"].append({"kind": "app-test", "what": t["name"] + " " + str(t["info"]), "at": "?test=1"})
    for cls, label, path in report.pop("_extra", []):
        shots.setdefault(cls, []).append((label, Path(path)))
    contact(shots, out)
    report.pop("_out", None)
    (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    write_md(report, out, len(vps), themes, texts, screens)
    return report


async def studio_flows(browser, base, report):
    report.setdefault("flows", [])
    ok = lambda name, cond, seen="": report["flows"].append({"flow": name, "ok": bool(cond), "seen": seen})
    # 1. rotate keeps place: card, gate, an unsaved edit and the scroll position (phone → landscape → portrait; tablet portrait → landscape)
    for (w, h) in [(390, 844), (820, 1180)]:
        ctx = await browser.new_context(viewport={"width": w, "height": h}, has_touch=True, is_mobile=True)
        page = await ctx.new_page()
        await page.goto(f"{base}?test=1&debug=0#studio=E05.01.01&gate=G-Learn")
        await page.wait_for_function("window.ST_READY==='studio=E05.01.01&gate=G-Learn'", timeout=20000)
        await page.evaluate("ST.draft['E05.01.01'].title='Rotate test'; scrollTo(0,300)")
        for vw, vh in [(h, w), (w, h)]:
            await page.set_viewport_size({"width": vw, "height": vh}); await page.wait_for_timeout(250)
            st = await page.evaluate("({h:location.hash, t:ST.draft['E05.01.01'].title, y:scrollY, cls:DEV.cls, gate:document.querySelector('.st').dataset.gate})")
            good = st["h"] == "#studio=E05.01.01&gate=G-Learn" and st["t"] == "Rotate test" and st["gate"] == "G-Learn" and st["y"] > 0
            report["rotate"].append({"size": f"{vw}x{vh} studio", "ok": good, "h": st["h"], "cls": st["cls"]})
            if not good:
                report["issues"].append({"kind": "rotate", "what": "studio " + json.dumps(st), "at": f"{vw}x{vh}"})
        await ctx.close()
    # 2. review round trip in the UI on a desktop (in memory; nothing is saved in testing mode)
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
    page = await ctx.new_page()
    await page.goto(f"{base}?test=1&debug=0#studio=E05.01.01")
    await page.wait_for_function("window.ST_READY==='studio=E05.01.01'", timeout=20000)
    await page.evaluate("ST.draft['E05.01.01'].status='draft'; ST.draft['E05.01.01'].review={}; ST.rv={}; render()")

    async def who(by, role, agent):
        await page.fill("#sdBy", by); await page.select_option("#sdRole", role); await page.fill("#sdAgent", agent)

    async def sign(gate):
        if gate != "G-Sci":
            await page.click(f"[data-st-gate='{gate}']"); await page.wait_for_timeout(80)
        for k in await page.evaluate("[...document.querySelectorAll('[data-st-ck]')].filter(i=>!i.checked).map(i=>i.dataset.stCk)"):
            await page.click(f"[data-st-ck='{k}']")   # each click redraws the review pane: query by name, never hold handles
        for ln in await page.evaluate("[...document.querySelectorAll('[data-st-v=ok]')].map(b=>b.dataset.ln)"):
            await page.click(f"[data-st-v='ok'][data-ln='{ln}']")
    # maker reviewing own card is blocked
    await who("Aaditya", "Lead scientist", "Bio · Build · S1 studio")
    await sign("G-Sci")
    blocked = await page.evaluate("document.querySelector('[data-st-act=pass]').disabled && document.querySelector('#sdWhoNote').textContent.length>0")
    ok("Studio: maker can't pass their own card (H2)", blocked)
    await who("Layout-check", "Research librarian", "layout-check flow")
    passable = await page.evaluate("!document.querySelector('[data-st-act=pass]').disabled")
    await page.fill("#sdAgent", ""); await page.type("#sdAgent", "chatX"); typed = await page.evaluate("document.querySelector('#sdAgent').value")
    ok("Studio: typing in the reviewer fields keeps the caret", typed == "chatX", typed)
    await page.fill("#sdAgent", "layout-check flow")
    await page.focus("#sdCk-cited"); await page.keyboard.press("Space"); await page.keyboard.press("Space")
    fid = await page.evaluate("document.activeElement.id")
    ok("Studio: keyboard on a checklist box keeps focus", fid == "sdCk-cited", fid)
    await page.click("[data-st-act=pass]"); await page.wait_for_timeout(80)
    await who("Layout-check", "Learning designer", "layout-check flow")
    await sign("G-Learn")
    await page.click("[data-st-act=pass]"); await page.wait_for_timeout(80)
    r = await page.evaluate("(()=>{const c=ST.draft['E05.01.01'];return {st:c.status, sci:c.review['G-Sci'].result, learn:c.review['G-Learn'].result, f:cardCheck(c,c.id,ST.ctx).filter(i=>i.lvl==='E').map(i=>i.code+' '+i.line)}})()")
    ok("Studio: G-Sci + G-Learn by other roles → reviewed, card-check clean", passable and r["st"] == "reviewed" and not r["f"], r)
    fo = await page.evaluate("({a:document.activeElement.id, dis:document.querySelector('[data-st-act=pass]').disabled})")
    ok("Studio: after Pass, focus is on the result and Pass is off", fo["a"] == "sdGateDone" and fo["dis"], fo)
    # an edit after review sends the card back to draft
    await page.focus("#stp-title"); await page.keyboard.press("End"); await page.keyboard.type("XYZ"); await page.wait_for_timeout(350)
    tv = await page.evaluate("document.querySelector('#stp-title').value")
    ok("Studio: typing that clears passes keeps the caret", tv == "Gastrulation in one pictureXYZ", tv)
    r2 = await page.evaluate("({st:ST.draft['E05.01.01'].status, rv:Object.keys(ST.draft['E05.01.01'].review).length})")
    ok("Studio: editing a reviewed card reopens it as draft", r2["st"] == "draft" and r2["rv"] == 0, r2)
    stale = await page.evaluate("Object.entries(ST.rv).filter(([k,r])=>k.startsWith('E05.01.01|')&&(Object.values(r.checklist).some(Boolean)||Object.values(r.lines).some(Boolean))).length")
    ok("Studio: an edit drops the review ticks", stale == 0, stale)
    # a failed line gives a fix prompt
    await page.evaluate("ST.draft['E05.01.01'].title='Gastrulation in one picture'; ST.rv={}; render()")
    await page.click("[data-st-gate='G-Sci']"); await page.wait_for_timeout(80)
    await who("Layout-check", "Research librarian", "layout-check flow")
    await page.click("[data-st-v='fix'][data-ln='f3']"); await page.fill("[data-st-note='f3']", "test note")
    await page.click("[data-st-act=fail]"); await page.wait_for_timeout(80)
    fp = await page.evaluate("ST.draft['E05.01.01'].review['G-Sci'].lines.f3")
    has = await page.evaluate("!!document.querySelector('[data-st-act=fixprompt]')")
    ok("Studio: a Fix line fails the gate and offers a fix prompt", fp == "fix: test note" and has, fp)
    # import links → a cited line
    await page.fill("#sdImp", "https://pubmed.ncbi.nlm.nih.gov/30346967/"); await page.fill("#sdImpLoc", "CS8"); await page.wait_for_timeout(60)
    line = await page.evaluate("document.querySelector('.st-cline').textContent")
    ok("Studio: a PubMed link becomes a cited line", "[E05.01 · R05a CS8] ✔✔" in line, line)
    # calibration
    await page.evaluate("location.hash='#calib'"); await page.wait_for_function("window.ST_READY==='calib'", timeout=20000)
    sc = await page.evaluate("document.querySelector('.st-score').textContent")
    ok("Studio: calibration — suggester 5/5", "suggester 5/5" in sc, sc)
    await ctx.close()


async def learn_flows(browser, base, report):
    """L1: rotate mid-Check keeps place; a passed Check, Can explain and the deck survive a reload (real mode, IndexedDB); an old save opens."""
    report.setdefault("flows", [])
    def ok(name, cond, info=""):   # failed flows become issues at the end of run() (one place)
        report["flows"].append({"flow": "L1 " + name, "ok": bool(cond), "seen": str(info)[:300]})
    card = json.loads((ROOT / "content" / "E" / "cards" / "E00.01.04.json").read_text())
    # 1. rotate mid-Check (testing mode): question index, 3D day and scroll survive phone portrait → landscape → portrait
    ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    page = await ctx.new_page()
    await page.goto(f"{base}?test=1&debug=0#card=E00.01.04")
    await page.wait_for_function("window.LN_READY==='card=E00.01.04' && window.VW_READY===true", timeout=30000)
    await page.click("[data-ln=start]")
    fold = await page.evaluate("({on:document.querySelector('#lnCard').classList.contains('ck-on'),body:getComputedStyle(document.querySelector('#lnBody')).display,hid:getComputedStyle(document.querySelector('#lnHid')).display,src:getComputedStyle(document.querySelector('#lnSrc')).display})")
    ok("D-053: a Check run folds the card text away", fold["on"] and fold["body"] == "none" and fold["src"] == "none" and fold["hid"] != "none", fold)
    await page.click("[data-ln=reread]"); await page.wait_for_timeout(200)
    back = await page.evaluate("({run:!!LN.ck['E00.01.04'],on:document.querySelector('#lnCard').classList.contains('ck-on'),body:getComputedStyle(document.querySelector('#lnBody')).display,start:!!document.querySelector('[data-ln=start]'),checks:(state.cards['E00.01.04']||{}).checks||0})")
    ok("D-053: Read again ends the run unscored", (not back["run"]) and (not back["on"]) and back["body"] != "none" and back["start"] and back["checks"] == 0, back)
    await page.click("[data-ln=start]")
    q = card["checks"][0]
    if q["type"] == "mcq":
        await page.click(f'[data-ln=pick][data-o="{q["answer"]}"]')
    else:
        await page.click("[data-ln=order]")
    await page.click("[data-ln=next]")
    await page.evaluate("document.querySelector('#lnCheck').scrollIntoView()")
    s0 = await page.evaluate("({h:location.hash,i:LN.ck['E00.01.04'].i,day:SC.st['sc-E00.01.04'].day,y:scrollY})")
    for vw, vh in [(844, 390), (390, 844)]:
        await page.set_viewport_size({"width": vw, "height": vh}); await page.wait_for_timeout(250)
        st = await page.evaluate("({h:location.hash,i:LN.ck['E00.01.04'].i,day:SC.st['sc-E00.01.04'].day,y:scrollY,cls:DEV.cls,q:!!document.querySelector('#lnQ'),w:SC.canvas.clientWidth})")
        good = st["h"] == s0["h"] and st["i"] == 1 and st["day"] == s0["day"] and st["q"] and st["y"] > 0 and st["w"] > 100
        report["rotate"].append({"size": f"{vw}x{vh} card", "ok": good, "h": st["h"], "cls": st["cls"]})
        if not good:
            report["issues"].append({"kind": "rotate", "what": "card " + json.dumps(st), "at": f"{vw}x{vh}"})
    await ctx.close()
    # 2. real mode: pass the Check, explain, reload → statuses + deck kept; the deck schedules Got it at +3 days
    ctx = await browser.new_context(viewport={"width": 1366, "height": 768})
    page = await ctx.new_page()
    await page.goto(f"{base}#card=E00.01.04")
    await page.wait_for_function("window.LN_READY==='card=E00.01.04' && STORE.mode==='idb'", timeout=30000)
    await page.click("[data-ln=start]")
    for q in card["checks"]:
        if q["type"] == "mcq":
            await page.click(f'[data-ln=pick][data-o="{q["answer"]}"]')
        else:
            await page.evaluate("(()=>{const c=LN.ck['E00.01.04'];c.ord=c.ord.slice().sort((a,b)=>a-b);})()")   # the right order = the options as listed (card-spec)
            await page.click("[data-ln=order]")
        await page.click("[data-ln=next]")
    res = await page.inner_text("#lnRes")
    ok("Card: a clean Check run marks Understood", "Understood" in res, res)
    await page.click("[data-ln=exshow]"); await page.click("[data-ln=exyes]")
    await page.wait_for_timeout(900)
    await page.reload(); await page.wait_for_function("window.LN_READY==='card=E00.01.04'", timeout=30000)
    st = await page.evaluate("({s:lnStatus('E00.01.04'),d:Object.keys(state.deck).length,rev:STORE.rev})")
    ok("Card: Can explain + deck survive a reload (IndexedDB)", st["s"] == "exp" and st["d"] == len(card["remember"]), st)
    await page.evaluate("stTouch('E05.01.01')"); await page.wait_for_timeout(900)
    sv = await page.evaluate("(async()=>{const s=await idbGet(STORE.db);return {mem:state.savedAt,db:s.savedAt,app:state.app,dbApp:s.app,v:APP.v,name:stLocalDate()};})()")
    ok("L1F: memory carries savedAt + app of the last write (backup tells the truth)", sv["mem"] == sv["db"] and sv["app"] == sv["v"] == sv["dbApp"], sv)
    await page.evaluate("for(const k in state.deck)state.deck[k].due=Date.now()-1000;stSave()"); await page.wait_for_timeout(700)
    await page.evaluate("location.hash='#deck'"); await page.wait_for_function("window.LN_READY==='deck'", timeout=20000)
    await page.click("[data-ln=dstart]"); await page.click("[data-ln=dshow]"); await page.click("[data-ln=dgot]")
    d = await page.evaluate("(()=>{const x=Object.values(state.deck).find(v=>v.n===1);return x?Math.round((x.due-lnDay0(Date.now()))/864e5):null;})()")
    ok("Deck: Got it brings a prompt back in 3 days", d == 3, d)
    # 3. an old (v6) save opens and is back-filled (A1, A4)
    await page.evaluate("""(async()=>{const tx=STORE.db.transaction('state','readwrite');tx.objectStore('state').put({schema:1,rev:STORE.rev,app:6,visited:{'E05.01.01':5},answers:{},settings:{theme:'light',motion:'system',t:1},last:{route:'today'}},'main');await new Promise(r=>tx.oncomplete=r);})()""")
    await page.goto(f"{base}#card=E05.01.01"); await page.reload(); await page.wait_for_function("window.LN_READY==='card=E05.01.01'", timeout=30000)
    st = await page.evaluate("({c:typeof state.cards,d:typeof state.deck,l:state.settings.level,v:state.visited['E05.01.01']})")
    ok("Old save (v6) opens with cards + deck back-filled", st == {"c": "object", "d": "object", "l": "general", "v": 5}, st)
    av = await page.evaluate("({app:state.app,v:APP.v})")
    ok("L1F: an old save's app is bumped to the running version on load", av["app"] == av["v"], av)
    await ctx.close()


FONT = [None]   # set from --font (drill flows use it too)
FONT_JS = "document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent=':root{--font:\"%s\",sans-serif!important}';document.head.appendChild(s);});"


async def drill_flows(browser, base, report, preview):
    """V2 (card-spec §2a): each drill type of the demo fixture (?test=1&fixture=drills, E05.02.01) at 5 sizes × 100/125 % — audit, pins, contact sheet;
    rotate mid-drill; Try it's view comes back; WebGL context loss redraws (V1 note)."""
    report.setdefault("flows", []); report.setdefault("_extra", [])
    out = Path(report["_out"]) / "shots"
    def ok(name, cond, info=""):
        report["flows"].append({"flow": "V2 " + name, "ok": bool(cond), "seen": str(info)[:300]})
    fx = json.loads((ROOT / "tools" / "layout-check" / "fixtures" / "E05.02.01-drills.json").read_text())
    for kind, w, h in PREVIEW:
        for text in ([100] if preview else [100, 125]):
            ctx = await browser.new_context(viewport={"width": w, "height": h}, has_touch=kind != "desktop", is_mobile=kind != "desktop", device_scale_factor=1)
            if FONT[0]:
                await ctx.add_init_script(FONT_JS % FONT[0])
            if text != 100:
                await ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='html{font-size:%d%%!important}';document.head.appendChild(s);});" % text)
            page = await ctx.new_page(); errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            await page.goto(f"{base}?test=1&debug=0&fixture=drills#card=E05.02.01")
            await page.wait_for_function("window.LN_READY==='card=E05.02.01' && window.VW_READY===true", timeout=30000)
            await page.click("[data-ln=start]")
            for i, q in enumerate(fx["checks"]):
                if i:
                    await page.evaluate(f"(()=>{{const c=LN.ck['E05.02.01'];c.i={i};c.pick=null;c.ord=null;c.sel=[];c.fold={{}};c.words=false;lnPaint('check');}})()")
                await page.wait_for_timeout(300)
                if q["type"] in ("rotate", "day", "label"):
                    await page.wait_for_function("window.VW_READY===true && !!SC.drill", timeout=30000)
                else:
                    await page.wait_for_function("[...document.querySelectorAll('#lnCheck img[data-snap]')].every(i=>i.complete&&i.naturalWidth>0)", timeout=30000)
                await page.wait_for_timeout(250)
                cls = await page.evaluate("DEV.cls")
                label = f"{w}x{h} {text}% drill {q['type']}"
                if q["type"] == "label":
                    pins = await page.evaluate("[...document.querySelectorAll('.vw-pin')].map(p=>!p.classList.contains('hidden'))")
                    ok(f"label pins drawn at {w}x{h} {text}%", len(pins) == len(q["pins"]) and all(pins), pins)
                    PINJS = """(()=>{const R=e=>e&&e.offsetParent!==null?e.getBoundingClientRect():null,ov=['#vwStamp','#vwDisc','#vwGiz','#vwScale'].map(s=>R(document.querySelector(s))).filter(Boolean),
                      hit=(a,b)=>a.left<b.right-1&&a.right>b.left+1&&a.top<b.bottom-1&&a.bottom>b.top+1,pins=[...document.querySelectorAll('.vw-pin:not(.hidden)')].map(R);
                      const labs=SC.lbl.filter(it=>SC.drill&&it.done===SC.drill.key).map(it=>R(it.el));
                      return {pins:pins.length,under:pins.filter(p=>ov.some(o=>hit(p,o))).length,labs:labs.length,labUnder:labs.filter(p=>ov.some(o=>hit(p,o))||pins.some(o=>hit(p,o))).length};})()"""
                    pv = await page.evaluate(PINJS)
                    ok(f"L1F: label pins clear of the stamp, notes, gizmo + scale at {w}x{h} {text}%", pv["under"] == 0, pv)
                    await page.evaluate(f"(()=>{{const c=LN.ck['E05.02.01'],k=LN.open['E05.02.01'];c.sel=k.checks[{i}].pins.map(p=>p.answer);lnCheckAct(k,'lcheck',{{}});}})()"); await page.wait_for_timeout(700)
                    pv = await page.evaluate(PINJS)
                    need = len(q["pins"]) if text == 100 else len(q["pins"]) - 1   # scene-spec §8a: on the tightest stages (125 % text) one pinned label may fall back to the Check feedback (Pin n: …)
                    ok(f"L1F: answered label drill — each pin carries its label, clear of overlays at {w}x{h} {text}%", pv["pins"] == len(q["pins"]) and pv["labs"] >= need and pv["under"] == 0 and pv["labUnder"] == 0, pv)
                if q["type"] == "day":
                    stamp = await page.inner_text("#vwStamp")
                    ok(f"day stamp masked at {w}x{h} {text}%", "?" in stamp and str(q["show"]["day"]) not in stamp, stamp)
                await page.evaluate("document.querySelector('#lnQ').scrollIntoView({block:'start'})"); await page.wait_for_timeout(100)
                iss = await page.evaluate("layoutAudit()")
                report["runs"].append({"at": label, "class": cls, "issues": len(iss)})
                report["issues"] += [dict(x, at=label) for x in iss] + [{"kind": "js-error", "what": e, "at": label} for e in errs]
                errs.clear()
                if text == 100 or q["type"] in ("label", "frames"):
                    path = out / f"{cls}_{w}x{h}_{text}_drill_{q['type']}.png"
                    await page.screenshot(path=str(path))
                    report["_extra"].append((cls + (" 125" if text != 100 else "") + " drills", f"{w}×{h} {q['type']}{' 125%' if text != 100 else ''}", str(path)))
            # leaving the drills gives Try it its own view back
            await page.evaluate("(()=>{const c=LN.ck['E05.02.01'];c.i=0;c.pick=null;c.done=true;lnPaint('check');})()"); await page.wait_for_timeout(500)
            back = await page.evaluate("({drill:!!SC.drill,inVw:!!document.querySelector('#lnVw canvas'),day:SC.eng.state().day})")
            ok(f"Try it gets its view back at {w}x{h} {text}%", not back["drill"] and back["inVw"] and back["day"] == 17, back)
            await ctx.close()
    # rotate mid-drill: phone portrait (stage in the Check) → landscape (beside it) → portrait; the turned view is kept
    ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    page = await ctx.new_page()
    await page.goto(f"{base}?test=1&debug=0&fixture=drills#card=E05.02.01")
    await page.wait_for_function("window.LN_READY==='card=E05.02.01' && window.VW_READY===true", timeout=30000)
    await page.click("[data-ln=start]"); await page.wait_for_function("window.VW_READY===true && !!SC.drill", timeout=30000)
    await page.evaluate("document.querySelector('[data-vw=turn][data-d=r]').click()"); await page.wait_for_timeout(200)
    az0 = await page.evaluate("SC.eng.state().az")
    for vw, vh, where in [(844, 390, "#lnVw"), (390, 844, "#lnDVw")]:   # phone landscape: the drill sits in the (then sticky) 3D column
        await page.set_viewport_size({"width": vw, "height": vh}); await page.wait_for_timeout(600)
        await page.evaluate("document.querySelector('#lnQ').scrollIntoView({block:'start'})"); await page.wait_for_timeout(150)
        st = await page.evaluate(f"(()=>{{const c=document.querySelector('{where} canvas'),r=c&&c.getBoundingClientRect();return {{in:!!c,vis:!!r&&r.bottom>0&&r.top<innerHeight&&r.height>100,az:SC.eng.state().az,q:LN.ck['E05.02.01'].i,cls:DEV.cls}};}})()")
        good = st["in"] and st["vis"] and abs(st["az"] - az0) < 1e-6 and st["q"] == 0   # the stage is on screen beside/with the question
        report["rotate"].append({"size": f"{vw}x{vh} drill", "ok": good, "cls": st["cls"]})
        if not good:
            report["issues"].append({"kind": "rotate", "what": "drill " + json.dumps(st), "at": f"{vw}x{vh}"})
    # the rotate drill scores the live view: matching the target passes
    await page.evaluate("(()=>{const t=SC.loaded['sc-E05.02.01'].views.find(v=>v.id==='top');SC.eng.view(t.azimuth_deg+10,t.elevation_deg-5,null);scSave();})()")
    await page.click("[data-ln=rcheck]"); await page.wait_for_timeout(200)
    ok("rotate drill: a view 10° off the target counts", await page.evaluate("LN.ck['E05.02.01'].res[0]===true"))
    await ctx.close()
    # L1F (T8): the day drill on E05.05.01 (sc-E00.01.02, with a 1 mm ruler) opens with the embryo + whole ruler clear of the overlays
    day_i = next(i for i, q in enumerate(json.loads((ROOT / "content" / "E" / "cards" / "E05.05.01.json").read_text())["checks"]) if q["type"] == "day")
    for vw, vh in [(360, 804), (640, 360), (390, 844)]:
        ctx = await browser.new_context(viewport={"width": vw, "height": vh}, has_touch=True, is_mobile=True)
        page = await ctx.new_page()
        await page.goto(f"{base}?test=1&debug=0#card=E05.05.01")
        await page.wait_for_function("window.LN_READY==='card=E05.05.01' && window.VW_READY===true", timeout=30000)
        await page.evaluate(f"(()=>{{const c=LN.open['E05.05.01'];const k=LN.ck[c.id]=lnCkNew(c);k.i={day_i};lnPaint('check');}})()")
        await page.wait_for_function("window.VW_READY===true && !!SC.drill && SC.drill.type==='day'", timeout=30000); await page.wait_for_timeout(500)
        fr = await page.evaluate("""(()=>{const st=document.querySelector('#vwStage').getBoundingClientRect(),b=SC.eng.screenBox(),R=e=>e&&e.offsetParent!==null?e.getBoundingClientRect():null;
          const box={left:st.left+b.l,right:st.left+b.r,top:st.top+b.t,bottom:st.top+b.b},ov=['#vwStamp','#vwDisc','#vwGiz','#vwScale'].map(s=>R(document.querySelector(s))).filter(Boolean);
          const hit=o=>box.left<o.right-1&&box.right>o.left+1&&box.top<o.bottom-1&&box.bottom>o.top+1;
          return {inside:box.left>=st.left-1&&box.right<=st.right+1&&box.top>=st.top-1&&box.bottom<=st.bottom+1,under:ov.filter(hit).length,zoom:+SC.eng.state().zoom.toFixed(2),h:Math.round(st.height)};})()""")
        ok(f"L1F: day drill keeps the embryo + ruler in view, clear of overlays at {vw}x{vh}", fr["inside"] and fr["under"] == 0, fr)
        await ctx.close()
    # WebGL context loss (V1 note): lose + restore → the scene draws again, no error message left up
    ctx = await browser.new_context(viewport={"width": 1366, "height": 768})
    page = await ctx.new_page(); errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    await page.goto(f"{base}?test=1&debug=0#scene=sc-E05.02.01&day=17")
    await page.wait_for_function("window.VW_READY===true", timeout=30000)
    lit = "(()=>{const r=SC.eng.snapshot(SC.eng.state(),160,100);return r?r.url.length:0;})()"
    n0 = await page.evaluate(lit)
    lost = await page.evaluate("SC.eng.loseContext(400)")
    await page.wait_for_timeout(300); mid = await page.evaluate("SC.eng.lost()")
    await page.wait_for_timeout(2500)
    st = await page.evaluate("({lost:SC.eng.lost(),msg:!document.querySelector('#vwLost').classList.contains('hidden')})")
    n1 = await page.evaluate(lit)
    # mouse hover names a structure outside drills, with no page error (G-Eng R1: a broken hover went unseen)
    await page.mouse.move(683, 330); await page.mouse.move(700, 345); await page.wait_for_timeout(200)
    hov = await page.evaluate("(()=>{const r=SC.canvas.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2};})()")
    await page.mouse.move(hov["x"], hov["y"]); await page.mouse.move(hov["x"] + 3, hov["y"] + 2); await page.wait_for_timeout(250)
    hshown = await page.evaluate("!!SC.hoverEl && !SC.hoverEl.classList.contains('hidden')")
    ok("mouse hover names a structure (desktop), no page error", hshown and not errs, {"shown": hshown, "errs": errs})
    ok("WebGL context loss: redraws after restore", lost and mid and not st["lost"] and not st["msg"] and n1 > 0.8 * n0 and not errs, {"n0": n0, "n1": n1, **st, "errs": errs})
    await ctx.close()


async def review_flows(browser, base, report):
    """H2 Reviewer mode (design plan §4.10, D-061): the form link carries every answer; Send is blocked until the answers are enough;
    rotate on a card review keeps the draft and the scroll; the rate-limit case shows the saved list + message; real mode: the first visit
    opens the tour, finishing it lands on Review and survives a reload, the Review tab appears, and a draft survives a reload."""
    report.setdefault("flows", [])
    def ok(name, cond, info=""):
        report["flows"].append({"flow": "H2 " + name, "ok": bool(cond), "seen": str(info)[:300]})
    from urllib.parse import urlparse, parse_qs
    # 1. demo: fill the form on a card, Send → the GitHub link (testing mode keeps the app on the page)
    ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    page = await ctx.new_page()
    await page.goto(f"{base}?test=1&debug=0&fixture=review#rcard=E05.01.03")
    await page.wait_for_function("window.RV_READY==='rcard=E05.01.03'", timeout=20000)
    await page.click("#rvSend", force=True); await page.wait_for_timeout(100)   # aria-disabled: a tap still reaches it and explains what is missing
    blocked = await page.evaluate("({url:window.RV_LAST_URL||null, help:document.querySelector('#rvSendHelp').textContent})")
    ok("send blocked with no verdict", blocked["url"] is None and "first" in blocked["help"], blocked)
    await page.click("label.rv-tick:has(input[value=facts])")
    await page.click("button.rv-vb[value=fix]")
    await page.click("#rvSend", force=True); await page.wait_for_timeout(100)   # aria-disabled: a tap still reaches it and explains what is missing
    b2 = await page.evaluate("({url:window.RV_LAST_URL||null, help:document.querySelector('#rvSendHelp').textContent})")
    ok("send blocked: a fix needs a note", b2["url"] is None and "note" in b2["help"], b2)
    await page.select_option("#rvWhere", "body")
    await page.fill("#rvNote", "Day 15 should be day 16 (E05.01).")
    await page.click(".rv-form .seg button[value=mid]")
    await page.click("#rvSend"); await page.wait_for_timeout(150)
    url = await page.evaluate("window.RV_LAST_URL||''")
    q = {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}
    want = q.get("template") == "card-review.yml" and q.get("labels") == "review" and q.get("title", "").startswith("[review] E05.01.03 v1 ✎") \
        and q.get("card", "").startswith("E05.01.03 v1") and q.get("verdict", "").startswith("✎") and q.get("where") == "The card text" \
        and q.get("sure") == "Fairly sure" and "- [x] The facts are right" in q.get("checklist", "") and q.get("note") == "Day 15 should be day 16 (E05.01)."
    ok("form link carries every answer", want, q)
    # 2. rotate keeps the draft and the place
    await page.evaluate("scrollTo(0,700)")
    for vw, vh in [(844, 390), (390, 844)]:
        await page.set_viewport_size({"width": vw, "height": vh}); await page.wait_for_timeout(250)
        st = await page.evaluate("({h:location.hash, cls:DEV.cls, y:scrollY, note:(document.querySelector('#rvNote')||{}).value, v:(document.querySelector('button.rv-vb[aria-pressed=true]')||{}).value})")
        good = st["h"] == "#rcard=E05.01.03" and st["note"].startswith("Day 15") and st["v"] == "fix" and st["y"] > 0
        report["rotate"].append({"size": f"{vw}x{vh} rcard", "ok": good, "h": st["h"], "cls": st["cls"]})
        if not good:
            report["issues"].append({"kind": "rotate", "what": "rcard " + json.dumps(st), "at": f"{vw}x{vh}"})
    # 3. demo states → words; rate-limit message over the saved list
    await page.goto(f"{base}?test=1&debug=0&fixture=review#review=mine")
    await page.wait_for_function("window.RV_READY==='review=mine' && RV.issues && !RV.busy", timeout=20000)
    await page.evaluate("render()")
    words = await page.evaluate("[...document.querySelectorAll('#rv-mine .rv-st')].map(e=>e.textContent.trim())")
    ok("demo: 7 of hers (not another person's, not a PR), every state shown", len(words) == 7 and any("Fixed in app update 12" in w for w in words) and any("Being fixed" in w for w in words)
       and any("No change" in w for w in words) and any("Done" in w for w in words) and any("Sent" in w for w in words), words)
    await page.goto(f"{base}?test=1&debug=0&fixture=review&rvlimit=1#review=mine")
    await page.wait_for_function("window.RV_READY==='review=mine' && RV.issues && !RV.busy", timeout=20000)
    await page.evaluate("render()")
    lim = await page.evaluate("({warn:(document.querySelector('#rv-mine .rv-warn')||{}).textContent||'', n:document.querySelectorAll('#rv-mine .rv-mine').length})")
    ok("rate limit: saved list + when to retry", "wait" in lim["warn"] and "Last checked" in lim["warn"] and lim["n"] == 7, lim)
    await ctx.close()
    # 4. real mode (no ?test, no GitHub: the API is answered by a stub): first visit → tour → Review; tab appears; tour + draft survive a reload
    ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    fx = json.loads((ROOT / "tools" / "layout-check" / "fixtures" / "review-issues.json").read_text())["items"]
    hits = []
    async def stub(route):
        hits.append(route.request.url)
        await route.fulfill(status=200, content_type="application/json", body=json.dumps(fx), headers={"etag": "W/\"h2\"", "x-ratelimit-remaining": "59", "access-control-allow-origin": "*", "access-control-expose-headers": "etag, x-ratelimit-remaining"})
    await ctx.route("https://api.github.com/**", stub)
    page = await ctx.new_page()
    await page.goto(f"{base}#review")
    await page.wait_for_function("window.BOOTED && STORE.mode==='idb' && window.RV_READY==='rtour'", timeout=20000)
    ok("first visit opens the tour", await page.evaluate("location.hash") == "#rtour")
    for _ in range(3):
        await page.click("[data-rvt]:not([data-rvt='done']).pri, [data-rvt='done'].pri"); await page.wait_for_timeout(120)
    await page.wait_for_function("window.RV_READY==='review' && RV.src==='live'", timeout=20000)
    nav = await page.evaluate("[...document.querySelectorAll('#nav [data-nav]')].map(b=>b.dataset.nav)")
    ok("tour done → Review, Review tab after Cards, GitHub asked once with her name", nav[:3] == ["today", "cards", "review"] and len(hits) == 1 and "creator=komalverma00500-byte" in hits[0], [nav, hits])
    await page.evaluate("location.hash='#rcard=E05.01.03'")
    await page.wait_for_function("window.RV_READY==='rcard=E05.01.03'", timeout=20000)
    await page.click("button.rv-vb[value=ask]"); await page.fill("#rvNote", "Is this day 15 or 16?")
    await page.wait_for_timeout(900)   # saves after CONFIG.saveDelayMs
    await page.reload()
    await page.wait_for_function("window.BOOTED && STORE.mode==='idb' && window.RV_READY==='rcard=E05.01.03'", timeout=20000)
    st = await page.evaluate("({tour:state.review.tour>0, on:state.review.on, note:(document.querySelector('#rvNote')||{}).value, v:(document.querySelector('button.rv-vb[aria-pressed=true]')||{}).value, cache:!!(state.review.cache&&state.review.cache.items.length)})")
    ok("reload keeps tour, Review tab, draft and the saved list", st["tour"] and st["on"] and st["note"] == "Is this day 15 or 16?" and st["v"] == "ask" and st["cache"], st)
    await page.evaluate("location.hash='#review'"); await page.wait_for_timeout(400)
    ok("cached list within 5 min: no second GitHub call", len(hits) == 1, hits)
    await ctx.close()
    # 5. errors never loop or crash (G-Eng round 1): a 500, a rate limit and offline → at most one call, no page error, the right words
    for case in ("500", "403", "offline"):
        ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        await ctx.add_init_script("indexedDB.deleteDatabase('biostudio')")
        calls, errs = [], []
        def mk(case):
          async def bad(route, *_):   # Playwright may pass the request as a 2nd argument
              calls.append(route.request.url)
              if case == "500":
                  await route.fulfill(status=500, body="oops", headers={"access-control-allow-origin": "*"})
              else:
                  await route.fulfill(status=403, body="{}", content_type="application/json", headers={"access-control-allow-origin": "*", "access-control-expose-headers": "x-ratelimit-remaining, x-ratelimit-reset",
                      "x-ratelimit-remaining": "0", "x-ratelimit-reset": str(int(time.time()) + 1200)})
          return bad
        await ctx.route("https://api.github.com/**", mk(case))
        page = await ctx.new_page()
        page.on("pageerror", lambda e: errs.append(str(e)))
        await page.goto(f"{base}#rtour")
        await page.wait_for_function("window.BOOTED && STORE.mode==='idb'", timeout=20000)
        await page.evaluate("state.review.tour=Date.now()")
        if case == "offline":
            await ctx.set_offline(True)
        await page.evaluate("location.hash='#review=mine'")
        await page.wait_for_timeout(2500)
        txt = await page.evaluate("(document.querySelector('#rv-mine')||{}).textContent||''")
        words = {"500": "Could not reach GitHub", "403": "GitHub asks us to wait", "offline": "offline"}[case]
        ok(f"error {case}: ≤ 1 call, no page error, says so", len(calls) <= 1 and not errs and words in txt, [len(calls), errs[:2], txt[:160]])
        await ctx.close()


async def tracker_flows(browser, base, report, vps):
    """W1: the step page keeps its place on rotate; the Map with Done + Ideas shown has no layout issue on any class."""
    report.setdefault("flows", [])
    ctx = await browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    page = await ctx.new_page()
    await page.goto(f"{base}?test=1&debug=0#step=C1")
    await page.wait_for_function("window.TR_READY==='step=C1'", timeout=20000)
    await page.evaluate("scrollTo(0,500)")
    for vw, vh in [(844, 390), (390, 844)]:
        await page.set_viewport_size({"width": vw, "height": vh}); await page.wait_for_timeout(250)
        st = await page.evaluate("({h:location.hash, cls:DEV.cls, y:scrollY, t:document.querySelector('#cpT')&&document.querySelector('#cpT').textContent})")
        ok = st["h"] == "#step=C1" and st["cls"] == ("dev-pl" if vw > vh else "dev-p") and st["y"] > 0
        report["rotate"].append({"size": f"{vw}x{vh} step", "ok": ok, "h": st["h"], "cls": st["cls"]})
        if not ok:
            report["issues"].append({"kind": "rotate", "what": "step " + json.dumps(st), "at": f"{vw}x{vh}"})
    await ctx.close()
    seen = set()
    for kind, w, h in vps:
        touch = kind != "desktop"
        ctx = await browser.new_context(viewport={"width": w, "height": h}, has_touch=touch, is_mobile=touch)
        await ctx.add_init_script("sessionStorage.setItem('biostudio.tracker',JSON.stringify({done:true,ideas:true}))")
        page = await ctx.new_page()
        await page.goto(f"{base}?test=1&debug=0#progress")
        await page.wait_for_function("window.TR_READY==='progress' && document.querySelectorAll('.tr-node').length>20", timeout=20000)
        iss = await page.evaluate("layoutAudit()")
        cls = await page.evaluate("DEV.cls")
        for i in iss:
            report["issues"].append(dict(i, at=f"{w}x{h} progress (done shown)"))
        report["flows"].append({"flow": f"map with done shown {w}x{h}", "ok": not iss, "seen": len(iss)})
        if cls not in seen:
            seen.add(cls)
            path = Path(report.get("_out", "out/layout-check")) / "shots" / f"{cls}_{w}x{h}_progress-all.png"
            await page.screenshot(path=str(path), full_page=True)
            report.setdefault("_extra", []).append((cls, f"{w}×{h} progress (done shown)", str(path)))
        await ctx.close()


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
    ap.add_argument("--font", help="stress test: render with this font family (e.g. \"DejaVu Sans Mono\") — CI fonts can be wider than yours (V2)")
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
