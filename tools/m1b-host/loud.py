"""Two-pass loudness for the M1b kit (H6: about −14 LUFS integrated, true peak ≤ −1.5 dBTP after AAC).
Owner doc: studio-docs/claude/RULES.md H6 · used by m1b.py encode. Standalone test: python loud.py <in.wav> [--debug]

Why not plain gain: the Kokoro line is about −26.5 LUFS with peaks 16 dB above the average, so +12.5 dB of gain puts
the true peak above 0 dBTP. So: (1) measure, (2) gain + a 4×-oversampled limiter (true-peak aware) a little below the
ceiling, (3) loudnorm linear=true from the measured values (no dynamic pumping), (4) encode, (5) measure the encoded file;
if AAC pushed the true peak over the ceiling, lower the limiter by the overshoot and redo (max 3 rounds)."""
import json, os, subprocess, sys

FF = ["ffmpeg", "-hide_banner", "-nostats"]


def measure(path, I=-14.0, TP=-1.5):
    """loudnorm analysis pass → dict (input_i, input_tp, input_lra, input_thresh, target_offset …)."""
    e = subprocess.run(FF + ["-i", path, "-af", f"loudnorm=I={I}:TP={TP}:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return json.loads(e[e.rindex("{"):e.rindex("}") + 1])


def prep(wav, out_wav, I=-14.0, TP=-1.5, ceiling_margin=1.0, debug=False, run=subprocess.run):
    """wav → out_wav at I LUFS, TP ≤ ceiling. Returns a log dict (measurements, gain, limiter ceiling, linear y/n).
    Two-pass loudnorm: pass 1 measures, pass 2 applies linear=true with the measured values. Before it, gain + a 4×-oversampled
    limiter bring the peaks under (TP − margin) so pass 2 can stay linear; the gain is re-aimed until the limited file is within
    0.1 LU of I (the limiter costs ~1 dB)."""
    m1 = measure(wav, I, TP)
    gain = I - float(m1["input_i"])
    ceil_db = TP - ceiling_margin                    # EDIT: limiter ceiling below TP: leaves room for AAC overshoot (~0.7 dB)
    lim = out_wav.replace(".wav", "_lim.wav")
    for _ in range(4):
        run(FF + ["-y", "-loglevel", "error", "-i", wav, "-af",
                  f"volume={gain:.2f}dB,aresample=192000,alimiter=limit={10 ** (ceil_db / 20):.5f}:attack=2:release=60:level=false,"
                  f"aresample=48000", "-c:a", "pcm_f32le", lim], check=True)
        m2 = measure(lim, I, TP)
        miss = I - float(m2["input_i"])
        if abs(miss) < 0.1:
            break
        gain += miss
    af = (f"loudnorm=I={I}:TP={TP}:LRA=11:linear=true:measured_I={m2['input_i']}:measured_TP={m2['input_tp']}:"
          f"measured_LRA={m2['input_lra']}:measured_thresh={m2['input_thresh']}:offset={m2['target_offset']}:print_format=json,"
          "aresample=48000")
    e = run(FF + ["-y", "-i", lim, "-af", af, "-c:a", "pcm_f32le", out_wav], capture_output=True, text=True, check=True).stderr
    r = json.loads(e[e.rindex("{"):e.rindex("}") + 1])
    log = {"pass1": {k: m1[k] for k in ("input_i", "input_tp", "input_lra")}, "gain_db": round(gain, 2), "limiter_ceiling_dbtp": ceil_db,
           "pass2": {k: m2[k] for k in ("input_i", "input_tp", "input_lra")}, "normalization_type": r.get("normalization_type"),
           "out": {k: r[k] for k in ("output_i", "output_tp")}}
    if debug:
        print("[loud]", json.dumps(log), flush=True)
    os.remove(lim)
    return log


def verdict(m, I=-14.0, TP=-1.5, tol=0.5):
    i, tp = float(m["input_i"]), float(m["input_tp"])
    return {"I": i, "TP": tp, "I_ok": abs(i - I) <= tol, "TP_ok": tp <= TP, "ok": abs(i - I) <= tol and tp <= TP}


if __name__ == "__main__":
    src = sys.argv[1]; dst = os.path.splitext(src)[0] + "_norm.wav"
    lg = prep(src, dst, debug="--debug" in sys.argv)
    mp4 = os.path.splitext(src)[0] + "_test.m4a"
    subprocess.run(FF + ["-y", "-loglevel", "error", "-i", dst, "-c:a", "aac", "-b:a", "128k", mp4], check=True)
    print(json.dumps({"prep": lg, "after_aac": verdict(measure(mp4))}, indent=1))
