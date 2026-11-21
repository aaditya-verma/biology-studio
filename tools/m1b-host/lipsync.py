"""M1b host line: TTS (Kokoro af_heart) + viseme/beat track for the Blender host.
Owner doc: studio-docs/build/studio-playbook.md §5b · spec: host.json (RULES I6).
Outputs (out/audio/): line.wav (24 kHz) · words.json (word timings, Kokoro tokens) · visemes.json (per frame: shape + open 0–1).
Sync method: phoneme-driven visemes inside Kokoro's word timings, mouth opening scaled by the audio envelope
(beat sync). If Kokoro gives no timings, words are spread by syllable count over voiced audio.
Usage: python lipsync.py [--dry-run] [--debug] [--wav existing.wav]"""
import argparse, json, math, os, re, sys, time, wave

import numpy as np

KIT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KIT, "out", "audio")
SR = 24000

# EDIT: phoneme → mouth shape (misaki/espeak IPA). Shapes match the Blender shape keys in blender_host.py.
SHAPES = [
    ("M", "mbp"),
    ("F", "fv"),
    ("O", "oɔuʊwɒ"),
    ("A", "aɑæʌɐ"),
    ("E", "eɛiɪjəɚɜ"),
]
SHAPE_OPEN = {"A": 1.0, "E": 0.65, "O": 0.75, "F": 0.25, "M": 0.0, "rest": 0.0}  # EDIT: max jaw per shape


def log(debug, *a):
    if debug:
        print("[lipsync]", *a, flush=True)


def shape_of(ph):
    for s, chars in SHAPES:
        if ph and ph[0] in chars:
            return s
    return None  # consonants without a strong shape keep the neighbour's shape


def read_wav(p):
    try:
        import soundfile as sf
        a, sr = sf.read(p, dtype="float32")
    except ImportError:
        with wave.open(p) as w:
            sr = w.getframerate()
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
            if w.getnchannels() > 1:
                a = a.reshape(-1, w.getnchannels())
    if a.ndim > 1:
        a = a.mean(axis=1)
    return a, sr


def write_wav(p, a, sr):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def tts(spec, debug):
    """Kokoro on the laptop GPU (falls back to CPU). Returns audio, words[{w, ph, t0, t1}], info."""
    import torch
    from kokoro import KPipeline
    v = spec["line"]["voice"]
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    pipe = KPipeline(lang_code=v["lang_code"], device=dev)
    load = time.time() - t0
    t1 = time.time()
    audio, words, offset = [], [], 0.0
    for res in pipe(spec["line"]["en"], voice=v["voice"], speed=v.get("speed", 1.0)):
        au = res.audio.numpy() if hasattr(res.audio, "numpy") else np.asarray(res.audio)
        for tk in (getattr(res, "tokens", None) or []):
            st, en = getattr(tk, "start_ts", None), getattr(tk, "end_ts", None)
            if st is not None and en is not None and tk.text.strip(".,?!"):
                words.append({"w": tk.text, "ph": tk.phonemes or "", "t0": offset + st, "t1": offset + en})
        audio.append(au)
        offset += len(au) / SR
    info = {"engine": "Kokoro-82M", "voice": v["voice"], "speed": v.get("speed", 1.0), "device": dev,
            "load_s": round(load, 1), "synth_s": round(time.time() - t1, 2), "timings": "kokoro" if words else "estimated"}
    log(debug, info)
    return np.concatenate(audio), words, info


def estimate_words(text, env, fps):
    """No timings: spread words by vowel-group count over the voiced span."""
    ws = [w for w in re.findall(r"[A-Za-z']+", text)]
    syl = [max(1, len(re.findall(r"[aeiouy]+", w.lower()))) for w in ws]
    voiced = np.where(env > 0.08)[0]
    a, b = (voiced[0], voiced[-1]) if len(voiced) else (0, len(env) - 1)
    total, t, out = sum(syl), a / fps, []
    span = (b - a) / fps
    for w, s in zip(ws, syl):
        d = span * s / total
        out.append({"w": w, "ph": "", "t0": t, "t1": t + d}); t += d
    return out


def guess_ph(word):
    """Letters → rough shapes when there are no phonemes (estimate path only)."""
    m = {"a": "a", "e": "e", "i": "i", "o": "o", "u": "u", "y": "i", "w": "w", "m": "m", "b": "b", "p": "p", "f": "f", "v": "v"}
    return "".join(m.get(c, "") for c in word.lower())


def envelope(a, sr, fps, n):
    hop = sr / fps
    seg = lambda i: a[int(i * hop):int((i + 1) * hop)]
    env = np.array([np.sqrt(np.mean(seg(i) ** 2) + 1e-12) if len(seg(i)) else 0.0 for i in range(n)])
    env = env / (env.max() + 1e-9)
    k = np.array([0.25, 0.5, 0.25])  # light smoothing (no jitter, H5 no flashing)
    return np.convolve(env, k, mode="same")


def visemes(a, sr, words, spec, lead):
    fps = spec["video"]["fps"]
    n = int(round(spec["video"]["seconds"] * fps))
    env = np.zeros(n)
    e = envelope(a, sr, fps, n - int(lead * fps))
    env[int(lead * fps):int(lead * fps) + len(e)] = e[: n - int(lead * fps)]
    shapes = ["rest"] * n
    for w in words:
        phs = [p for p in (w["ph"] or guess_ph(w["w"])) if not p.isspace() and p not in "ˈˌː"]
        f0, f1 = int((w["t0"] + lead) * fps), max(int((w["t0"] + lead) * fps) + 1, int((w["t1"] + lead) * fps))
        cur = None
        for i, f in enumerate(range(f0, min(f1, n))):
            ph = phs[min(len(phs) - 1, int(i * len(phs) / max(1, f1 - f0)))] if phs else ""
            cur = shape_of(ph) or cur or "E"
            shapes[f] = cur
    frames = []
    for f in range(n):
        s = shapes[f]
        op = 0.0 if s in ("M", "rest") else min(1.0, SHAPE_OPEN[s] * (0.35 + 0.9 * env[f]))
        frames.append({"f": f, "shape": s, "open": round(float(op), 3), "env": round(float(env[f]), 3)})
    return frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the plan; write nothing")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--wav", help="use an existing wav (skip TTS); timings are estimated")
    ap.add_argument("--only", help="unused here; accepted for kit symmetry")
    ap.add_argument("--preview", action="store_true", help="accepted for kit symmetry (audio is always full quality)")
    a = ap.parse_args()
    spec = json.load(open(os.path.join(KIT, "host.json"), encoding="utf-8"))
    lead = spec["video"]["lead_in_s"]
    if a.dry_run:
        print(f"[lipsync] would synthesise {spec['line']['en']!r} with {spec['line']['voice']} → {OUT}\\line.wav, words.json, visemes.json")
        return
    if a.wav:
        au, sr = read_wav(a.wav); info = {"engine": "file", "path": a.wav, "timings": "estimated"}; words = []
    else:
        au, words, info = tts(spec, a.debug); sr = SR
    dur = len(au) / sr
    if dur + lead > spec["video"]["seconds"]:
        print(f"[lipsync] WARNING line is {dur:.2f} s + lead {lead} s > {spec['video']['seconds']} s — raise voice.speed in host.json")
    if not words:
        fps = spec["video"]["fps"]
        words = estimate_words(spec["line"]["en"], envelope(au, sr, fps, int(dur * fps) + 1), fps)
    pad = np.zeros(int(lead * sr), dtype=np.float32)
    tail = np.zeros(max(0, int(spec["video"]["seconds"] * sr) - len(pad) - len(au)), dtype=np.float32)
    full = np.concatenate([pad, au.astype(np.float32), tail])[: int(spec["video"]["seconds"] * sr)]
    write_wav(os.path.join(OUT, "line.wav"), full, sr)
    fr = visemes(au, sr, words, spec, lead)
    wpm = round(len(spec["line"]["en"].split()) / (dur / 60))
    json.dump({"info": info, "line_s": round(dur, 2), "wpm": wpm, "lead_in_s": lead, "words": words},
              open(os.path.join(OUT, "words.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump({"fps": spec["video"]["fps"], "frames": fr}, open(os.path.join(OUT, "visemes.json"), "w"), indent=0)
    print(f"[lipsync] line {dur:.2f} s · {wpm} wpm · timings {info['timings']} · {len(fr)} frames → {OUT}")
    if a.debug:
        print(" ".join(f"{x['shape'][0]}{int(x['open']*9)}" for x in fr[::2]))


if __name__ == "__main__":
    main()
