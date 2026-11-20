"""Kinetic captions for the M1b host shot (playbook §5b Short profile; visual-style §1 caption spec).
Burns one English phrase at a time (words pop in on their spoken time, key words on a pearl pill) plus one
Devanagari line, inside the 9:16 safe area. Pillow + raqm shapes Devanagari; without raqm the Devanagari line is
skipped and the manifest says so (never ship broken conjuncts). Owner doc: build/visual-style.md §1. Edit values: spec.py."""
import os
from PIL import Image, ImageDraw, ImageFont, features

import spec

HERE = os.path.dirname(os.path.abspath(__file__))


def _font(cands, size):
    for c in cands:
        p = c if os.path.isabs(c) else os.path.normpath(os.path.join(HERE, c))
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, layout_engine=ImageFont.Layout.RAQM if features.check("raqm") else ImageFont.Layout.BASIC), p
            except OSError:
                continue
    return None, None


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    c = [v / 255 for v in rgb]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def phrases(words):
    """Split timed words into phrases of ≤ max_chars_line characters (≤ 2 lines incl. the Devanagari line)."""
    out, cur = [], []
    for w in words:
        trial = " ".join(x["w"] for x in cur + [w])
        if cur and (len(trial) > spec.CAPTION["max_chars_line"] or w["w"].lower() in getattr(spec, "PHRASE_BREAKS", [])):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


class Captioner:
    def __init__(self, size, words, debug=False):
        """size = (w, h) of the frame; words = [{"w": str, "t0": s, "t1": s}] from the TTS step."""
        self.W, self.H = size
        self.debug = debug
        k = self.W / 1080
        cap_px = spec.CAPTION["cap_px_at_1080"] * k
        self.size_en = int(round(cap_px / 0.70))          # cap height ≈ 0.70 em for Inter/Segoe
        self.size_hi = int(round(self.size_en * spec.CAPTION["deva_scale"]))
        self.f_en, self.f_en_path = _font(spec.FONTS_LATIN, self.size_en)
        self.f_hi, self.f_hi_path = _font(spec.FONTS_DEVA, self.size_hi)
        self.raqm = features.check("raqm")
        self.deva_ok = bool(self.f_hi) and self.raqm
        self.words = words
        self.groups = self._fit(phrases(words)) if self.f_en else phrases(words)
        self.t_end = words[-1]["t1"] if words else 0
        self.notes = []
        if not self.f_en:
            raise SystemExit("[captions] no Latin font found — put Inter-Bold.ttf in Studio home apps\\fonts (spec.FONTS_LATIN)")
        if not self.f_hi:
            self.notes.append("Devanagari font missing → Devanagari line skipped (spec.FONTS_DEVA)")
        elif not self.raqm:
            self.notes.append("Pillow without raqm → Devanagari would render unshaped; line skipped. Fix: pip install --upgrade pillow (wheels bundle raqm)")
        ink = hex2rgb(spec.CAPTION["outline"])
        scrim = spec.CAPTION["scrim"]
        # worst case: scrim over a white pixel
        a = scrim[3] / 255
        bg = tuple(int(scrim[i] * a + 255 * (1 - a)) for i in range(3))
        self.contrast_text_on_scrim = round(contrast(hex2rgb(spec.CAPTION["text"]), bg), 2)
        self.contrast_pill = round(contrast(hex2rgb(spec.CAPTION["pill_text"]), hex2rgb(spec.CAPTION["pill_bg"])), 2)
        self.ink = ink

    # ---- layout ----
    def _fit(self, groups):
        """Split any phrase wider than the caption box (70 % of the frame, inside the safe area) at a word boundary."""
        maxw = min(spec.CAPTION_MAX_W * self.W, (1 - spec.SAFE["left"] - spec.SAFE["right"]) * self.W) * 0.88
        out = []
        fits = lambda ws: self.f_en.getlength(" ".join(x["w"] for x in ws)) * spec.CAPTION["pop_scale"] <= maxw
        for g in groups:
            for k in range(1, len(g) + 1):      # fewest balanced chunks that all fit
                tot = sum(len(x["w"]) + 1 for x in g)
                chunks, cur, acc, j = [], [], 0, 1
                for x in g:
                    cur.append(x)
                    acc += len(x["w"]) + 1
                    if acc >= tot * j / k - 0.5 and j < k:
                        chunks.append(cur); cur = []; j += 1
                if cur:
                    chunks.append(cur)
                if all(fits(ch) for ch in chunks):
                    out += chunks
                    break
            else:
                out += [[x] for x in g]
        return out

    def _key(self, w, keys):
        return w.strip("?,.!").lower() in [k.lower() for k in keys]

    def _ease(self, t, t0):
        f = (t - t0) * spec.FPS
        n = spec.CAPTION["pop_frames"]
        if f < 0:
            return None
        if f >= n:
            return 1.0
        x = f / n
        return spec.CAPTION["pop_scale"] - (spec.CAPTION["pop_scale"] - 1) * (1 - (1 - x) ** 3)

    def draw(self, img, t):
        """Draw captions for time t (s) onto RGBA/RGB image in place. Returns img."""
        W, H = self.W, self.H
        d = ImageDraw.Draw(img, "RGBA")
        band_top = int(spec.CAPTION_BAND[0] * H)
        band_bot = int(spec.CAPTION_BAND[1] * H)
        left = int(spec.SAFE["left"] * W)
        right = int(W - spec.SAFE["right"] * W)
        cx = (left + right) // 2
        maxw = int(spec.CAPTION_MAX_W * W)
        # active English phrase: from its first word until the next phrase starts (last one holds to the end)
        grp = None
        for i, g in enumerate(self.groups):
            start = g[0]["t0"]
            nxt = self.groups[i + 1][0]["t0"] if i + 1 < len(self.groups) else 1e9
            if start - 0.05 <= t < nxt:
                grp = g
        lines = []
        if grp:
            lines.append(("en", grp))
        show_hi = self.deva_ok and t >= spec.CUT_AT_S
        if show_hi:
            lines.append(("hi", spec.LINE_HI))
        if not lines:
            return img
        # measure
        gap = int(self.size_en * 0.28)
        rows = []
        for kind, content in lines:
            if kind == "en":
                f = self.f_en
                items = [(w["w"], self._key(w["w"], spec.KEY_EN), self._ease(t, w["t0"] - 0.03)) for w in content]
            else:
                f = self.f_hi
                items = [(w, self._key(w, spec.KEY_HI), 1.0) for w in content.split(" ")]
            sp = f.getlength(" ")
            widths = [f.getlength(w) for w, _, _ in items]
            total = sum(widths) + sp * (len(items) - 1)
            asc, desc = f.getmetrics()
            rows.append((kind, f, items, widths, sp, total, asc + desc))
        block_h = sum(r[6] for r in rows) + gap * (len(rows) - 1)
        y = band_top + max(0, (band_bot - band_top - block_h) // 2)
        if y + block_h > band_bot:   # stay inside the 55–65 % band (G-Art R1); may start above it, never below
            y = band_bot - block_h
        pad = int(self.size_en * 0.45)
        # scrim grows with the words already spoken (no empty box ahead of the voice — G-Art R1)
        shown = []
        for kind, f, items, widths, sp, total, lh in rows:
            vis = [ww for (w, key, s), ww in zip(items, widths) if s is not None]
            shown.append(sum(vis) + sp * max(0, len(vis) - 1))
        cur_w = max(shown) if shown else 0
        if cur_w <= 0:
            return img
        bw = int(min(maxw, cur_w)) + 2 * pad
        d.rounded_rectangle([cx - bw // 2, y - pad, cx + bw // 2, y + block_h + pad], radius=pad, fill=spec.CAPTION["scrim"])
        for (kind, f, items, widths, sp, total, lh), sw in zip(rows, shown):
            x = cx - sw / 2
            for (w, key, s), ww in zip(items, widths):
                if s is None:          # not spoken yet → nothing drawn; line re-centres as words arrive
                    continue
                fs = f
                if s != 1.0:
                    fs = f.font_variant(size=max(8, int(f.size * s)))
                wpx = fs.getlength(w)
                ox = x + (ww - wpx) / 2
                oy = y + (lh - lh * s) / 2
                if key:
                    pp = int(self.size_en * 0.12)
                    ox += 0  # pill padding kept inside the scrim: scrim pad ≥ 3× pill pad
                    d.rounded_rectangle([ox - pp, oy, ox + wpx + pp, oy + lh * s], radius=pp * 2, fill=spec.CAPTION["pill_bg"])
                    d.text((ox, oy), w, font=fs, fill=spec.CAPTION["pill_text"])
                else:
                    d.text((ox, oy), w, font=fs, fill=spec.CAPTION["text"],
                           stroke_width=max(1, int(spec.CAPTION["outline_px"] * W / 1080)), stroke_fill=spec.CAPTION["outline"])
                x += ww + sp
            y += lh + gap
        if self.debug:
            self.draw_safe(img)
        return img

    def draw_safe(self, img):
        """--safe / --debug overlay: safe zones + caption band (visual-style §1)."""
        W, H = self.W, self.H
        d = ImageDraw.Draw(img, "RGBA")
        s = spec.SAFE
        red = (255, 60, 60, 70)
        d.rectangle([0, 0, W, int(s["top"] * H)], fill=red)
        d.rectangle([0, H - int(s["bottom"] * H), W, H], fill=red)
        d.rectangle([W - int(s["right"] * W), 0, W, H], fill=red)
        d.rectangle([0, 0, int(s["left"] * W), H], fill=red)
        d.rectangle([0, int(spec.CAPTION_BAND[0] * H), W, int(spec.CAPTION_BAND[1] * H)], outline=(80, 200, 255, 200), width=2)
        return img

    def report(self):
        return {"font_latin": self.f_en_path, "font_devanagari": self.f_hi_path, "raqm": self.raqm,
                "devanagari_drawn": self.deva_ok, "size_px_en": self.size_en, "size_px_hi": self.size_hi,
                "contrast_text_on_scrim_worst": self.contrast_text_on_scrim, "contrast_key_pill": self.contrast_pill,
                "phrases": [" ".join(w["w"] for w in g) for g in self.groups], "notes": self.notes}
