#!/usr/bin/env python3
"""Biology Studio — live progress page for any build job (D-089; RULES I9). Owner doc: tools/live/README.md.

Why: long checks (layout-check ~35 min, preview ~15 min, guards, renders) ran with no view of where they were. The owner
asked (22 Nov 2026, U2F) for the live screenshot page to apply to every build job: a hub listing every run, and a page per run
with state, elapsed time, the output tail and the newest screenshots, refreshing every 5 s while anything runs.

  python tools/live/live.py NAME [--shots DIR] -- <command> [args...]   run a command, tee its output, live page; exits with its code
  python tools/live/live.py NAME --attach LOG [--idle S] [--shots DIR]  watch a job already running: done when LOG has content and has
                                                                          not grown for S seconds (default 60); FAIL when a line starts
                                                                          with FAIL / FAILED / [sync] FAILED / Traceback
  python tools/live/live.py --serve [--port 8799]                       serve out/live (hub: http://localhost:8799/index.html)
  python tools/live/live.py --selftest

Pages: out/live/index.html (hub) and out/live/run-<slug>.html (gitignored, RULES I8). The same NAME again replaces that run.
Screenshots (--shots, any folder) are copied (newest 12) into out/live/shots/<slug>/. Relative --shots/--attach paths are
read from the folder you start the tool in; the command itself runs in the repo root.
Windows: a .bat runs directly (`-- sync.bat --check`); never `cmd /c` from Git Bash (it rewrites /c to C:/).
I5 flags (--debug, --dry-run, --only, --preview) don't apply: this tool only wraps other jobs.
EDIT: REFRESH (seconds), TAIL (lines), SHOTS (thumbnails), TICK, IDLE below.
"""
import collections, html, json, os, re, shutil, subprocess, sys, threading, time, traceback
from pathlib import Path
from urllib.parse import quote

for _s in (sys.stdout, sys.stderr):   # G-Eng: a cp1252 pipe must never kill the echo (the job would block on a full pipe)
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "out" / "live"
REFRESH, TAIL, SHOTS, TICK, IDLE = 5, 80, 12, 4, 60   # EDIT
FAIL_RE = re.compile(r"^\s*(FAIL\b|FAILED\b|\[sync\] FAILED|Traceback \(most recent call last\))", re.M)

CSS = """<style>:root{--bg:#f6f4f1;--fg:#222;--mut:#666;--card:#fff;--line:#8884}
@media(prefers-color-scheme:dark){:root{--bg:#1e2126;--fg:#eee;--mut:#aaa;--card:#2a2e35}}
body{background:var(--bg);color:var(--fg);font:15px system-ui,sans-serif;margin:16px;max-width:1200px}a{color:inherit}h1{font-size:20px}
.b{display:inline-block;padding:2px 10px;border-radius:10px;font-weight:700;font-size:13px;color:#fff}.run{background:#8a4b7a}.ok{background:#1d7a3a}.bad{background:#b3261e}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}figure{margin:0}img{width:100%;border:1px solid var(--line);border-radius:6px}
figcaption{font-size:11px;color:var(--mut);word-break:break-all}pre{white-space:pre-wrap;font-size:12px;background:var(--card);padding:10px;border-radius:8px;max-height:60vh;overflow:auto}
table{border-collapse:collapse;width:100%}td,th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left}</style>"""
BADGE = {"running": '<span class="b run">RUNNING</span>', "pass": '<span class="b ok">PASS</span>', "fail": '<span class="b bad">FAIL</span>'}


def slug(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-") or "run"


def fmt(t):
    t = int(t)
    return f"{t // 3600}h {t // 60 % 60:02d}m" if t >= 3600 else f"{t // 60}m {t % 60:02d}s"


def write_atomic(path, text):
    """G-Eng: unique temp name (parallel runs share the hub); retry while a reader (server, browser) holds the target on Windows."""
    path = Path(path)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    for i in range(20):
        try:
            os.replace(tmp, path); return True
        except PermissionError:
            time.sleep(0.05 * (i + 1))
    try:
        tmp.unlink()
    except OSError:
        pass
    return False


def tail_of(path, n=TAIL, chunk=65536):
    try:
        with open(path, "rb") as f:
            f.seek(0, 2); size = f.tell(); f.seek(max(0, size - chunk))
            data = f.read().decode("utf-8", errors="replace")
    except OSError:
        return ""
    lines = data.splitlines(True)
    if size > chunk:
        lines = lines[1:]
    return "".join(collections.deque(lines, n))


class Run:
    def __init__(self, name, log, shots=None, cmd=None, out=OUT, idle=IDLE):
        self.name, self.slug, self.log, self.cmd, self.out, self.idle = name, slug(name), Path(log), cmd, Path(out), idle
        self.shots = Path(shots).resolve() if shots else None
        self.t0, self.code, self.note = time.time(), None, ""
        self.out.mkdir(parents=True, exist_ok=True)
        self.sdir = self.out / "shots" / self.slug

    def _shots(self):
        if not (self.shots and self.shots.is_dir()):
            return 0, []
        fs = []
        for p in self.shots.iterdir():
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                try:
                    fs.append((p.stat().st_mtime, p))
                except OSError:
                    pass
        fs.sort(key=lambda x: x[0])
        new = [p for _, p in fs[-SHOTS:][::-1]]
        try:
            self.sdir.mkdir(parents=True, exist_ok=True)
            keep = {p.name for p in new}
            for old in self.sdir.iterdir():
                if old.name not in keep:
                    try:
                        old.unlink()
                    except OSError:
                        pass
            for p in new:
                d = self.sdir / p.name
                if not d.exists():
                    try:
                        shutil.copy2(p, d)
                    except OSError:
                        pass
        except OSError:
            pass
        return len(fs), [p.name for p in new]

    def write(self, state):
        """Never raises: a page that can't be written this tick is written on the next one."""
        try:
            self._write(state)
        except Exception as e:   # noqa: BLE001 — the job must keep running and its pipe keep draining
            sys.stderr.write(f"live: page not written this tick ({e})\n")

    def _write(self, state):
        tail = tail_of(self.log) + (("\n" + self.note) if self.note else "")
        n, new = self._shots()
        live, el = state == "running", time.time() - self.t0
        what = " ".join(self.cmd) if self.cmd else f"attached to {self.log}"
        cards = "".join(f'<figure><img src="shots/{quote(self.slug)}/{html.escape(quote(f))}" loading="lazy"><figcaption>{html.escape(f)}</figcaption></figure>' for f in new)
        bits = [f"elapsed {fmt(el)}"] + ([f"{n} screenshots"] if self.shots else []) + ([f"exit {self.code}"] if self.code is not None else []) + [f"updated {time.strftime('%H:%M:%S')}"] + ([f"refreshes every {REFRESH} s"] if live else [])
        page = (f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(self.name)}</title>'
                + (f'<meta http-equiv="refresh" content="{REFRESH}">' if live else "") + CSS
                + f'<p><a href="index.html">← all runs</a></p><h1>{html.escape(self.name)} {BADGE[state]}</h1><p><code>{html.escape(what)}</code><br>{" · ".join(bits)}</p>'
                + f'<h2>Output (last {TAIL} lines)</h2><pre>{html.escape(tail) or "(no output yet)"}</pre>'
                + (f'<h2>Newest screenshots</h2><div class="g">{cards}</div>' if new else ""))
        write_atomic(self.out / f"run-{self.slug}.html", page)
        meta = {"name": self.name, "slug": self.slug, "state": state, "start": time.strftime("%d %b %H:%M:%S", time.localtime(self.t0)),
                "t0": self.t0, "elapsed": fmt(el), "shots": n, "cmd": what}
        write_atomic(self.out / f"run-{self.slug}.json", json.dumps(meta))
        hub(self.out)

    def run(self):
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")   # the pipe is read as UTF-8
        state = "fail"
        try:
            with open(self.log, "w", encoding="utf-8") as lf:
                try:
                    p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, env=env,
                                         text=True, encoding="utf-8", errors="replace", cwd=str(ROOT))
                except OSError as e:
                    self.note = f"live: could not start the command: {e}"; self.code = 127
                    print(self.note); return 127

                def pump():
                    for line in p.stdout:   # always drain the pipe; echo failures must not stop it
                        try:
                            lf.write(line); lf.flush()
                        except Exception:  # noqa: BLE001
                            pass
                        try:
                            sys.stdout.write(line); sys.stdout.flush()
                        except Exception:  # noqa: BLE001
                            pass
                th = threading.Thread(target=pump, daemon=True)
                th.start()
                try:
                    while p.poll() is None:
                        self.write("running"); time.sleep(TICK)
                except KeyboardInterrupt:
                    p.terminate(); self.note = "live: stopped with Ctrl+C"; p.wait()
                th.join(timeout=10)
            self.code = p.returncode
            state = "pass" if self.code == 0 else "fail"
            return self.code
        except BaseException as e:
            self.note = self.note or "live: " + "".join(traceback.format_exception_only(type(e), e)).strip()
            raise
        finally:
            self.write(state)

    def attach(self):
        state, last, still = "fail", -1, time.time()
        try:
            while True:
                size = self.log.stat().st_size if self.log.exists() else 0
                if size != last:
                    last, still = size, time.time()
                if size > 0 and time.time() - still >= self.idle:
                    break
                self.write("running"); time.sleep(min(TICK, max(self.idle, 0.2)))
            bad = bool(FAIL_RE.search(self.log.read_text(encoding="utf-8", errors="replace")))
            state = "fail" if bad else "pass"
            return 1 if bad else 0
        except KeyboardInterrupt:
            self.note = "live: stopped watching with Ctrl+C"; return 130
        finally:
            self.write(state)


def hub(out=OUT):
    rows = []
    for f in Path(out).glob("run-*.json"):
        try:
            rows.append(json.loads(f.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            pass
    rows.sort(key=lambda m: m.get("t0", 0), reverse=True)
    live = any(m["state"] == "running" for m in rows)
    tr = "".join(f'<tr><td><a href="run-{html.escape(quote(m["slug"]))}.html">{html.escape(m["name"])}</a></td><td>{BADGE.get(m["state"], "")}</td><td>{m["start"]}</td><td>{m["elapsed"]}</td><td>{m["shots"] or ""}</td></tr>' for m in rows)
    page = (f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Live runs</title>'
            + (f'<meta http-equiv="refresh" content="{REFRESH}">' if live else "") + CSS
            + f'<h1>Live runs</h1><p>updated {time.strftime("%H:%M:%S")}{" · refreshes every %d s" % REFRESH if live else ""} · open a run for its output and screenshots</p>'
            + f'<table><tr><th>Run</th><th>State</th><th>Started</th><th>Elapsed</th><th>Shots</th></tr>{tr}</table>')
    write_atomic(Path(out) / "index.html", page)


def serve(port):
    import functools, http.server
    OUT.mkdir(parents=True, exist_ok=True); hub()

    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def end_headers(self):
            self.send_header("Cache-Control", "no-store"); super().end_headers()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(Q, directory=str(OUT)))
    print(f"live: http://localhost:{port}/index.html  (Ctrl+C stops)", flush=True)
    srv.serve_forever()


def selftest():
    import tempfile
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(("ok  " if cond else "BAD ") + label); ok &= bool(cond)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d); shots = d / "s"; shots.mkdir(); live = d / "live"
        (shots / "a #1.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        for name, code, want in (("self pass", 0, "pass"), ("self fail", 3, "fail")):
            r = Run(name, d / (slug(name) + ".log"), shots=shots, out=live,
                    cmd=[sys.executable, "-c", f"import sys;print('hello {name} → ✓');sys.exit({code})"])
            got = r.run()
            page = (live / f"run-{r.slug}.html").read_text(encoding="utf-8")
            meta = json.loads((live / f"run-{r.slug}.json").read_text(encoding="utf-8"))
            chk(f"{name}: exit code {code}", got == code); chk(f"{name}: state {want}", meta["state"] == want)
            chk(f"{name}: unicode output in page", f"hello {name} → ✓" in page); chk(f"{name}: no refresh when done", "http-equiv" not in page)
            chk(f"{name}: screenshot copied + url-encoded", (live / "shots" / r.slug / "a #1.png").exists() and "a%20%231.png" in page)
        # a cp1252 stdout must not deadlock the pump (G-Eng finding 1)
        env = dict(os.environ, PYTHONIOENCODING="cp1252"); env.pop("PYTHONUTF8", None)
        code = "import sys;[print('→ line %d ✓' % i) for i in range(5000)]"
        p = subprocess.run([sys.executable, str(Path(__file__)), "self cp1252", "--", sys.executable, "-c", code], env=env,
                           capture_output=True, timeout=120, cwd=str(ROOT))
        chk("cp1252 stdout: finishes with exit 0 (no deadlock)", p.returncode == 0)
        for f in OUT.glob("run-self-cp1252*"):
            f.unlink(missing_ok=True)
        shutil.rmtree(OUT / "shots" / "self-cp1252", ignore_errors=True)
        hub(OUT)
        if os.name == "nt":   # a .bat runs directly and passes its exit code (G-Eng finding 3)
            bat = d / "t5.bat"; bat.write_text("@echo off\r\necho bat ran %1\r\nexit /b 5\r\n", encoding="ascii")
            rc = main(["self bat", "--", str(bat), "x"])
            chk(".bat: exit code 5 + output", rc == 5 and "bat ran x" in (OUT / "run-self-bat.log").read_text(encoding="utf-8", errors="replace"))
            chk("cmd /c rewritten by Git Bash is refused", main(["self cmdc", "--", "cmd", "C:/", "x.bat"]) == 2)
            for f in OUT.glob("run-self-bat*"):
                f.unlink(missing_ok=True)
            hub(OUT)
        r = Run("self missing", d / "m.log", out=live, cmd=["no-such-command-xyz"])
        chk("missing command: exit 127 + FAIL page", r.run() == 127 and json.loads((live / "run-self-missing.json").read_text())["state"] == "fail")
        # attach waits for a streaming log to go quiet (finding 4)
        lg = d / "att.log"; lg.write_text("", encoding="utf-8")

        def writer():
            for i in range(4):
                time.sleep(0.4)
                with open(lg, "a", encoding="utf-8") as f:
                    f.write(f"step {i}\n")
            with open(lg, "a", encoding="utf-8") as f:
                f.write("Errors: 0 · FAILED: 0\nPASS: 0 issues\n")
        t = threading.Thread(target=writer); t0 = time.time(); t.start()
        a = Run("self attach", lg, out=live, idle=1.0)
        rc = a.attach(); t.join()
        chk("attach: waits for the log to go quiet", time.time() - t0 >= 2.0 and "PASS: 0 issues" in lg.read_text(encoding="utf-8"))
        chk("attach: 'FAILED: 0' mid-line is not a failure", rc == 0)
        lg2 = d / "att2.log"; lg2.write_text("x\nFAIL: 2 issues\n", encoding="utf-8")
        chk("attach: a FAIL line → fail", Run("self attach fail", lg2, out=live, idle=0.3).attach() == 1)
        chk("run named 'index' keeps its page", Run("index", d / "i.log", out=live, cmd=[sys.executable, "-c", "pass"]).run() == 0
            and (live / "run-index.html").exists() and "Live runs" in (live / "index.html").read_text(encoding="utf-8"))
        h = (live / "index.html").read_text(encoding="utf-8")
        chk("hub lists every run", all(s in h for s in ("self pass", "self fail", "self attach", "self missing")))
    print(("PASS" if ok else "FAIL") + ": live selftest")
    return 0 if ok else 1


def main(argv):
    if argv[:1] == ["--selftest"]:
        return selftest()
    if argv[:1] == ["--serve"]:
        rest = argv[1:]
        if rest and (rest[0] != "--port" or len(rest) != 2 or not rest[1].isdigit()):
            print("usage: live.py --serve [--port 8799]"); return 2
        return serve(int(rest[1]) if rest else 8799)
    if not argv or argv[0].startswith("-"):
        print(__doc__); return 2
    name, rest, cmd = argv[0], argv[1:], None
    if "--" in rest:
        i = rest.index("--"); cmd, rest = rest[i + 1:], rest[:i]
    if len(rest) % 2 or any(k not in ("--shots", "--attach", "--idle") for k in rest[::2]) or not re.fullmatch(r"\d+(\.\d+)?", dict(zip(rest[::2], rest[1::2])).get("--idle", "1")):
        print(f"unknown or incomplete options: {' '.join(rest)}\n\n{__doc__}"); return 2
    opt = dict(zip(rest[::2], rest[1::2]))
    attach = opt.get("--attach")
    if bool(cmd) == bool(attach):
        print("give either -- <command> or --attach LOG"); return 2
    if cmd and len(cmd) >= 2 and cmd[0].lower() in ("cmd", "cmd.exe") and re.match(r"^[A-Za-z]:[\\/]?$", cmd[1]):
        print("live: `cmd /c` became `cmd C:/` (Git Bash path rewrite) — run the .bat directly: -- sync.bat --check"); return 2
    if cmd and os.name == "nt" and cmd[0].lower().endswith((".bat", ".cmd")):   # a batch file runs through cmd, started from here (no shell rewrite)
        bat = next((p for p in (Path(cmd[0]), ROOT / cmd[0]) if p.is_file()), None)
        if bat:
            cmd = ["cmd.exe", "/d", "/c", str(bat.resolve())] + cmd[1:]
    r = Run(name, attach or OUT / f"run-{slug(name)}.log", shots=opt.get("--shots"), cmd=cmd, idle=float(opt.get("--idle", IDLE)))
    print(f"live: {name} -> out/live/run-{r.slug}.html", flush=True)
    return r.run() if cmd else r.attach()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
