"""S1E01 animatic — scratch voice (P1 ②). Owner doc: studio-docs/episodes/S1E01/table-read.md.
One WAV per spoken line (Kokoro af_heart, speed 0.66 + the table-read pronunciation dictionary) → audio/ (never committed) + timings.json.
Flags (RULES I5): --dry-run (print the marked-up text, synthesise nothing) · --only L01[,L02b,…] · --debug · --preview (first 3 lines per cut).
EDIT: VOICE, SPEED, TRIM_DB, PAD below. Pronunciations live in table-read.md only (RULES I6)."""
import argparse, json, os, re, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("BIO_REPO", HERE.parents[1] if (HERE.parents[1] / ".git").exists() else HERE.parents[1] / "repo" / "biology-studio"))
VOICE, SR, TRIM_DB, PAD = "af_heart", 24000, -45, 0.05   # EDIT
SPEED = {"lesson": 0.80, "general": 0.75, "short": 0.80}   # EDIT: owner pick 24 Nov 2026 (per cut, keeps H6 130–150 wpm; replaces 0.66)
KOKORO = [("oʊ", "O"), ("eɪ", "A"), ("aɪ", "I"), ("aʊ", "W"), ("ɔɪ", "Y"), ("dʒ", "ʤ"), ("tʃ", "ʧ")]   # IPA → Kokoro letters
ap = argparse.ArgumentParser()
for f in ("--dry-run", "--debug", "--preview"): ap.add_argument(f, action="store_true")
ap.add_argument("--only"); a = ap.parse_args()
sc = json.loads((REPO / "content/E/episodes/S1E01/script.json").read_text(encoding="utf8"))
rows = re.findall(r"^\| ([^|]+?) \| [^|]+? \| /(.+?)/ \|", (REPO / "studio-docs/episodes/S1E01/table-read.md").read_text(encoding="utf8"), re.M)
DICT = sorted(rows, key=lambda r: -len(r[0]))
print(f"[voice] {len(DICT)} dictionary terms, {SPEED} {VOICE}")
def kk(x):
    for a_, b in KOKORO: x = x.replace(a_, b)
    return x
def mark(t):
    for w, ipa in DICT:   # whole words only, longest first; never inside an existing [..](/../)
        t = re.sub(r"(?<![\w\[(/])(%s)\b(?![^\[]*\]\()" % re.escape(w), lambda m: f"[{m.group(1)}](/{kk(ipa)}/)", t, flags=re.I)
    return t
jobs = [(p, l) for p in sc["scripts"] for i, l in enumerate(sc["scripts"][p]) if (not a.only or l["id"] in a.only.split(",")) and not (a.preview and i > 2)]
if a.dry_run:
    for p, l in jobs: print(l["id"], mark(l["text"]))
    sys.exit()
import numpy as np, soundfile as sf
from kokoro import KPipeline
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M", device="cuda")
out = HERE / "audio"; out.mkdir(exist_ok=True); tf = HERE / "timings.json"
T = json.loads(tf.read_text(encoding="utf8")) if tf.exists() and (a.only or a.preview) else {"voice": VOICE, "speed": SPEED, "lines": {}}
for p, l in jobs:
    t0 = time.time(); ph = []; au = []
    words = []; off = 0.0
    for r in pipe(mark(l["text"]), voice=VOICE, speed=SPEED[p]):
        y = r.audio.cpu().numpy(); ph.append(r.phonemes); au.append(y)
        for k in r.tokens or []:
            if k.start_ts is not None and re.search(r"\w", k.text): words.append([k.text, off + k.start_ts, off + (k.end_ts or k.start_ts)])
        off += len(y) / SR
    x = np.concatenate(au); raw = len(x) / SR
    env = np.abs(x) > 10 ** (TRIM_DB / 20) * np.abs(x).max(); i = np.flatnonzero(env)
    t_cut = max(0, i[0] - int(PAD * SR)) / SR
    x = x[max(0, i[0] - int(PAD * SR)):i[-1] + int(PAD * SR)]
    sf.write(out / f"{l['id']}.wav", x, SR)
    m = len(x) / SR
    words = [[w, round(max(0, b - t_cut), 2), round(min(m, e - t_cut), 2)] for w, b, e in words]
    T["lines"][l["id"]] = dict(cut=p, shot=l["shot"], words=l["_words"], planned_s=l["_dur"], hold_s=l["hold"], measured_s=round(m, 2), raw_s=round(raw, 2), speed=SPEED[p], w=words, phonemes=" ".join(ph))
    print(f"{l['id']:5} plan {l['_dur']:5.1f} meas {m:5.2f} ({(m/l['_dur']-1)*100:+.0f}%) raw {raw:.2f} wpm {l['_words']/m*60:.0f}", flush=True)
    if a.debug: print("   ", " ".join(ph))
tf.write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf8", newline="\n")
for cut in sc["scripts"]:
    L = [v for v in T["lines"].values() if v["cut"] == cut]
    shots = {}
    for v in L: s = shots.setdefault(v["shot"], [0, 0]); s[0] += v["planned_s"] + v["hold_s"]; s[1] += v["measured_s"] + v["hold_s"]
    print(cut, "planned", round(sum(s[0] for s in shots.values()), 1), "measured", round(sum(s[1] for s in shots.values()), 1))
    for k, (pl, me) in shots.items(): print(f"  {k:4} {pl:5.1f} {me:6.2f} {(me/pl-1)*100:+5.1f}% {'' if abs(me/pl-1)<=.05 else 'OUT'}")
