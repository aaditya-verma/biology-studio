"""S1E01 animatic — timeline builder (P1 ②; P1F: idea pauses + out/<cut>.chapters.vtt): timings.json + script.json + shots.json → out/timeline.json, out/<cut>.vtt, out/<cut>.wav (two-pass −14 LUFS, H6).
Flags: --dry-run (no files) · --only <cut> · --debug · --preview (skip audio). EDIT: CAP (caption chars), FFMPEG."""
import argparse, difflib, json, os, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; REPO = Path(os.environ.get("BIO_REPO", HERE.parents[1] if (HERE.parents[1] / ".git").exists() else HERE.parents[1] / "repo" / "biology-studio"))
CAP = {"lesson": (42, 1), "general": (42, 1), "short": (22, 2)}   # EDIT: max characters per line, lines per caption (visual-style §1/§10)
ap = argparse.ArgumentParser()
for f in ("--dry-run", "--debug", "--preview"): ap.add_argument(f, action="store_true")
ap.add_argument("--only"); a = ap.parse_args()
J = lambda p: json.loads(p.read_text(encoding="utf8"))
sc, T = J(REPO / "content/E/episodes/S1E01/script.json"), J(HERE / "timings.json")["lines"]
out = HERE / "out"; out.mkdir(exist_ok=True)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
def align(text, toks, dur):
    """script words with the voice's times (dictionary tokens may hold several words; gaps are interpolated)"""
    W = text.split(); tk = []
    for w, s, e in toks:
        ps = w.split(); tot = sum(map(len, ps)) or 1; at = s
        for p in ps: d = (e - s) * len(p) / tot; tk.append((p, at, at + d)); at += d
    A = [norm(w) for w in W]; B = [norm(t[0]) for t in tk]; t = [None] * len(W)
    for i, j, n in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
        for k in range(n): t[i + k] = [tk[j + k][1], tk[j + k][2]]
    i = 0
    while i < len(W):
        if t[i] is None:
            j = i
            while j < len(W) and t[j] is None: j += 1
            s = t[i - 1][1] if i else 0.0; e = t[j][0] if j < len(W) else dur
            for k in range(i, j): t[k] = [s + (e - s) * (k - i) / (j - i), s + (e - s) * (k - i + 1) / (j - i)]
            i = j
        i += 1
    return [[w, round(x, 2), round(y, 2)] for w, (x, y) in zip(W, t)]
def chunks(words, cmax, nl):
    caps, cur = [], []
    def wrap(ws):
        L = [""]
        for w in ws:
            if L[-1] and len(L[-1]) + 1 + len(w) > cmax: L.append(w)
            else: L[-1] = (L[-1] + " " + w).strip()
        if len(L) == 2:   # even lines: no single word left on line two
            L = min(([" ".join(ws[:i]), " ".join(ws[i:])] for i in range(1, len(ws))), key=lambda q: (max(map(len, q)) > cmax, abs(len(q[0]) - len(q[1]))))
        return L
    sents = [[]]
    for w in words:
        sents[-1].append(w)
        if re.search(r"[.?!;:]$", w[0]): sents.append([])
    sents = [x for x in sents if x]
    for i in range(len(sents) - 2, -1, -1):   # "Next:" alone is under 1 s: join it to its neighbour
        if len(sents[i]) == 1: sents[i + 1] = sents[i] + sents[i + 1]; sents[i] = []
    ok = lambda ws: len(wrap([x[0] for x in ws])) <= nl
    for S in filter(None, sents):   # fewest captions per sentence, evenly filled (no one-word leftovers)
        n = len(S)
        for k in range(1, n + 1):
            memo = {}
            def go(i, left):
                if left == 0: return (0, []) if i == n else (1e9, [])
                if (i, left) not in memo:
                    r = (1e9, [])
                    for j in range(i + 1, n + 1):
                        if not ok(S[i:j]): break
                        c, rest = go(j, left - 1); c += len(" ".join(x[0] for x in S[i:j])) ** 2 - (150 if S[j - 1][0].endswith(",") else 0)
                        if c < r[0]: r = (c, [S[i:j]] + rest)
                    memo[(i, left)] = r
                return memo[(i, left)]
            best = go(0, k)
            if best[0] < 1e8: break
        caps += best[1]
    return [dict(s=c[0][1], e=c[-1][2], lines=wrap([x[0] for x in c])) for c in caps]
vt = lambda t: f"{int(t//3600):02}:{int(t//60)%60:02}:{t%60:06.3f}"
res = {}
for cut, lines in sc["scripts"].items():
    if a.only and cut != a.only: continue
    at, L, S = 0.0, [], []
    for l in lines:
        m = T[l["id"]]; ws = [[w, round(at + s, 2), round(at + e, 2)] for w, s, e in align(l["text"], m["w"], m["measured_s"])]
        end = at + m["measured_s"]; cps = chunks(ws, *CAP[cut])
        for i, c in enumerate(cps): c["e"] = cps[i + 1]["s"] if i + 1 < len(cps) else round(min(end + .4, end + l["hold"]), 2)
        L.append(dict(id=l["id"], seg=l["seg"], shot=l["shot"], s=round(at, 2), e=round(end, 2), hold=l["hold"], kind=l.get("kind"), title=l.get("title"), text=l["text"], words=ws, caps=cps, refs=[r["ref"] for r in l["refs"]], new=l.get("new", [])))
        if not S or S[-1]["id"] != l["shot"]: S.append(dict(id=l["shot"], s=round(at, 2)))
        at = end + l["hold"]; S[-1]["e"] = round(at, 2)
    wpm = sum(l["_words"] for l in lines) / sum(T[l["id"]]["measured_s"] for l in lines) * 60
    # P1F (spec 2, D-107): idea pauses from the measured voice, 0.3 s before the end of the last line's hold; checks hold >= 1.5 s, silence +-0.3 s, 20-60 s
    I, by = [], {x['id']: x for x in L}
    for k, d in enumerate(sc.get('ideas', {}).get(cut, [])):
        a_, b_ = by[d['from']], by[d['to']]; i_ = L.index(b_); e_ = L[i_ + 1]['s'] if i_ + 1 < len(L) else round(at, 2); last = k == len(sc['ideas'][cut]) - 1
        brk = None if last else round(e_ - 0.3, 2); I.append(dict(id=d['id'], title=d['title'], s=a_['s'], e=e_, dur=round(e_ - a_['s'], 2), brk=brk, **{'from': d['from'], 'to': d['to']}))
        bad = [] if 20 <= e_ - a_['s'] <= 60 else [f"{e_ - a_['s']:.1f} s"]
        if brk is not None:
            near = [w[0] for x in L for w in x['words'] if w[1] < brk + 0.3 and w[2] > brk - 0.3]
            if near: bad.append(f'speech within 0.3 s: {near}')
            if b_['hold'] < 1.5: bad.append(f"hold {b_['hold']} s")
        print(f"   {d['id']} {a_['s']:6.1f}-{e_:6.1f} ({e_ - a_['s']:4.1f} s) pause {brk if brk is not None else 'end':>6}  {'OK' if not bad else 'FAIL ' + '; '.join(bad)}")
    res[cut] = dict(dur=round(at, 2), wpm=round(wpm, 1), lines=L, shots=S, ideas=I)
    if I and not a.dry_run: (out / f'{cut}.chapters.vtt').write_text('WEBVTT\n\n' + '\n'.join(f"{vt(d['s'])} --> {vt(d['e'])}\n{d['title']}\n" for d in I), encoding='utf8', newline='\n')   # chapters = ideas (MM8)
    print(f"{cut}: {at:.1f} s, {wpm:.0f} wpm speech, {sum(len(l['caps']) for l in L)} captions")
    if a.dry_run: continue
    v = "WEBVTT\n\n" + "\n".join(f"{vt(c['s'])} --> {vt(c['e'])}\n" + "\n".join(c["lines"]) + "\n" for l in L for c in l["caps"])
    (out / f"{cut}.vtt").write_text(v, encoding="utf8", newline="\n")
    if a.preview: continue
    import wave, array
    buf = bytearray()
    for l, ln in zip(lines, L):
        with wave.open(str(HERE / "audio" / f"{l['id']}.wav")) as w: d = w.readframes(w.getnframes()); assert w.getframerate() == 24000 and w.getsampwidth() == 2
        want = int(round(ln["s"] * 24000)) * 2; buf += b"\0" * max(0, want - len(buf)); buf += d
    buf += b"\0" * max(0, int(at * 24000) * 2 - len(buf)); raw = out / f"{cut}_raw.wav"
    with wave.open(str(raw), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(bytes(buf))
    ff = lambda af, *o: subprocess.run(["ffmpeg", "-hide_banner", "-y", "-i", str(raw), "-af", af, *o], capture_output=True, text=True, encoding="utf8").stderr
    P = "loudnorm=I=-14:TP=-1.5:LRA=11"; j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", ff(P + ":print_format=json", "-f", "null", "-"))[0])
    def meas(): return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out / f"{cut}.wav"), "-af", P + ":print_format=json", "-f", "null", "-"], capture_output=True, text=True, encoding="utf8").stderr)[0])
    g = -14 - float(j["input_i"])
    for _ in range(3):   # limit at 192 kHz (inter-sample peaks), then give back the gain the limiter took
        ff(f"volume={g:.2f}dB,aresample=192000,alimiter=limit=0.74:level=false,aresample=48000", "-ar", "48000", str(out / f"{cut}.wav")); j2 = meas(); g += -14 - float(j2["input_i"])
        if abs(float(j2["input_i"]) + 14) < .1: break
    print("   loudness", j2["input_i"], "LUFS, true peak", j2["input_tp"]); raw.unlink()
if not a.dry_run: (out / "timeline.json").write_text(json.dumps(res, ensure_ascii=False), encoding="utf8", newline="\n")
