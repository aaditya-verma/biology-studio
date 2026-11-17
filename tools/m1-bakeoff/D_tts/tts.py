"""Two local TTS voices on 20 embryology terms + one narration sentence (pace check, RULES H6).
Voice 1: Kokoro-82M (T30, Apache 2.0, GPU or CPU).  Voice 2: Piper (T32, GPL, CPU) with a per-voice licence.
Usage: python D_tts/tts.py --out out/tts [--kokoro-voice af_heart] [--piper-voice en_US-ryan-high]"""
import argparse, json, os, subprocess, sys, time
import numpy as np
import soundfile as sf

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TERMS = [t.strip() for t in open(os.path.join(KIT, "D_tts", "terms.txt"), encoding="utf-8") if t.strip()]
SENTENCE = ("During the third week, cells of the epiblast move through the primitive streak and spread "
            "between the layers, turning a two-layered disc into three germ layers.")

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="out/tts")
ap.add_argument("--kokoro-voice", default="af_heart")
ap.add_argument("--piper-voice", default="en_US-ryan-high")
ap.add_argument("--models", default=os.path.join(KIT, "..", "..", "models"))
a = ap.parse_args()
out = os.path.abspath(os.path.join(KIT, a.out))
os.makedirs(out, exist_ok=True)


def join(clips, sr, gap=0.7):
    sil = np.zeros(int(sr * gap), dtype=np.float32)
    parts = []
    for c in clips:
        parts += [c.astype(np.float32), sil]
    return np.concatenate(parts)


results = {}

# ---- Voice 1: Kokoro ----
try:
    import torch
    from kokoro import KPipeline
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    pipe = KPipeline(lang_code="a", device=dev)
    load = time.time() - t0
    clips, rows = [], []
    for text in TERMS + [SENTENCE]:
        ts = time.time()
        audio, phon = [], []
        for _, ps, au in pipe(text, voice=a.kokoro_voice):
            audio.append(au.numpy() if hasattr(au, "numpy") else np.asarray(au))
            phon.append(ps)
        au = np.concatenate(audio)
        rows.append({"text": text, "phonemes": " ".join(phon), "synth_s": round(time.time() - ts, 3), "audio_s": round(len(au) / 24000, 2)})
        clips.append(au)
    sf.write(os.path.join(out, "voice1_kokoro.wav"), join(clips, 24000), 24000)
    sent = rows[-1]
    results["voice1"] = {"engine": "Kokoro-82M", "voice": a.kokoro_voice, "device": dev, "load_s": round(load, 1),
                         "total_synth_s": round(sum(r["synth_s"] for r in rows), 2),
                         "sentence_wpm": round(len(SENTENCE.split()) / (sent["audio_s"] / 60)), "items": rows}
    print("[TTS] Kokoro done")
except Exception as e:  # keep going so voice 2 still runs
    results["voice1"] = {"engine": "Kokoro-82M", "error": repr(e)}
    print("[TTS] Kokoro failed:", e)

# ---- Voice 2: Piper (runs in models/piper so voice files stay there) ----
try:
    pdir = os.path.abspath(os.path.join(a.models, "piper"))
    os.makedirs(pdir, exist_ok=True)
    if not os.path.exists(os.path.join(pdir, a.piper_voice + ".onnx")):
        subprocess.run([sys.executable, "-m", "piper.download_voices", a.piper_voice], cwd=pdir, check=True)
    clips, rows, sr = [], [], 22050
    for i, text in enumerate(TERMS + [SENTENCE]):
        wav = os.path.join(out, f"_piper_{i:02d}.wav")
        ts = time.time()
        subprocess.run([sys.executable, "-m", "piper", "-m", a.piper_voice, "-f", wav, "--", text], cwd=pdir, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        au, sr = sf.read(wav, dtype="float32")
        rows.append({"text": text, "synth_s": round(time.time() - ts, 3), "audio_s": round(len(au) / sr, 2)})
        clips.append(au)
        os.remove(wav)
    sf.write(os.path.join(out, "voice2_piper.wav"), join(clips, sr), sr)
    sent = rows[-1]
    results["voice2"] = {"engine": "Piper", "voice": a.piper_voice, "device": "cpu",
                         "note": "synth_s includes Python start-up per call; read the voice's MODEL_CARD for its licence",
                         "total_synth_s": round(sum(r["synth_s"] for r in rows), 2),
                         "sentence_wpm": round(len(SENTENCE.split()) / (sent["audio_s"] / 60)), "items": rows}
    print("[TTS] Piper done")
except Exception as e:
    results["voice2"] = {"engine": "Piper", "error": repr(e)}
    print("[TTS] Piper failed:", e)

results["listen_order"] = TERMS + ["(narration sentence)"]
with open(os.path.join(out, "tts_stats.json"), "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2, ensure_ascii=False)
print("[TTS] wrote", out)
