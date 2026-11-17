"""Draws the shared overlay (day stamp, colour key, scale bar, axis gizmo, labels) as RGBA PNGs,
one per frame, so every method carries identical on-screen text (RULES B2, H4, D8).
Usage: python overlay.py OUT_DIR [--no-labels] [--every N]"""
import argparse, math, os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_math as sm

FONT_CANDIDATES = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"]
BOLD_CANDIDATES = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf"]
LABEL_OFFSETS = {"epiblast": (-60, -150), "primitive node": (10, -150), "primitive streak": (-190, -120),
                 "hypoblast": (60, 130), "mesoderm": (120, 110), "endoderm": (-170, 150)}


def font(size, bold=False):
    for p in (BOLD_CANDIDATES if bold else FONT_CANDIDATES):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def text(d, xy, s, f, fill, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=3, stroke_fill=(10, 12, 15, 230))


def hexc(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def pattern(d, box, kind, ink):
    """Fixed pattern per token (D-031): rings, vlines, diag, hlines, dots, xhatch, speckle, ring. EDIT: spacing here."""
    x0, y0, x1, y1 = box
    if kind == "hlines":
        for yy in range(y0 + 3, y1, 5): d.line([x0 + 1, yy, x1 - 1, yy], fill=ink, width=1)
    elif kind == "vlines":
        for xx in range(x0 + 3, x1, 5): d.line([xx, y0 + 1, xx, y1 - 1], fill=ink, width=1)
    elif kind == "diag":
        for k in range(-(y1 - y0), x1 - x0, 5): d.line([x0 + k, y1 - 1, x0 + k + (y1 - y0), y0 + 1], fill=ink, width=1)
        d.rectangle(box, outline=None)
    elif kind in ("rings", "dots"):
        for yy in range(y0 + 4, y1 - 2, 6):
            for xx in range(x0 + 4, x1 - 2, 6):
                if kind == "rings": d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], outline=ink)
                else: d.ellipse([xx - 1, yy - 1, xx + 1, yy + 1], fill=ink)
    elif kind == "ring":
        d.ellipse([x0 + 3, y0 + 3, x1 - 3, y1 - 3], outline=(255, 255, 255, 230), width=2)


def draw(shot, frame, labels=True):
    W, H = shot["width"], shot["height"]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s, parts = sm.build(shot, frame)
    fg = hexc(shot["colors"]["text"])
    f_big, f_mid, f_small = font(30, True), font(22), font(17)
    ov = shot["overlay"]
    # day / stage / size stamp
    text(d, (36, 30), ov["stamp"].format(day=s["day"], stage=shot["timeline"]["stage"], size=f"{s['size_mm']:.2f}"), f_big, fg)
    # colour key (label + swatch; names also sit on the structures, so colour is never the only cue)
    keys = [("epiblast", "epiblast"), ("hypoblast", "hypoblast"), ("mesoderm", "mesoderm"),
            ("endoderm", "endoderm"), ("streak", "primitive streak / node")]
    y = 30
    pats = shot.get("patterns", {})  # D-031: every key swatch carries its layer pattern, not colour alone (RULES B3)
    for k, name in keys:
        box = [W - 300, y + 4, W - 280, y + 24]
        d.rectangle(box, fill=hexc(shot["colors"][k]), outline=fg)
        pattern(d, box, pats.get(k), (17, 17, 17, 150))
        text(d, (W - 268, y), name, f_mid, fg)
        y += 32
    # scale bar (ortho camera: exact pixels per unit along screen x)
    ppu = W / shot["camera"]["ortho_width_units"]
    bar = ov["scale_bar_mm"] / 0.1 * ppu
    x0, yb = 40, H - 70
    d.rectangle([x0, yb, x0 + bar, yb + 6], fill=fg)
    d.line([x0, yb - 6, x0, yb + 12], fill=fg, width=3)
    d.line([x0 + bar, yb - 6, x0 + bar, yb + 12], fill=fg, width=3)
    text(d, (x0 + bar / 2, yb - 10), f"{ov['scale_bar_mm']} mm", f_mid, fg, "md")
    # axis gizmo: cranial = screen right, caudal = left, dorsal = up, ventral = down
    cx, cy, r = W - 120, H - 110, 46
    for (dx, dy, lab, anc) in [(1, 0, "Cr", "lm"), (-1, 0, "Ca", "rm"), (0, -1, "D", "md"), (0, 1, "V", "ma")]:
        ex, ey = cx + dx * r, cy + dy * r
        d.line([cx, cy, ex, ey], fill=fg, width=3)
        hx, hy = -dy * 7, dx * 7
        d.polygon([(ex + dx * 10, ey + dy * 10), (ex + hx, ey + hy), (ex - hx, ey - hy)], fill=fg)
        text(d, (ex + dx * 16, ey + dy * 16), lab, f_mid, fg, anc)
    # disclaimer
    text(d, (W / 2, H - 22), ov["disclaimer"], f_small, fg, "md")
    # on-structure labels with leader lines
    if labels:
        for name, p in sm.label_anchors(shot, s, parts).items():
            ax, ay = sm.project(shot, p)
            ox, oy = LABEL_OFFSETS[name]
            tx, ty = ax + ox, ay + oy
            d.line([ax, ay, tx, ty], fill=fg, width=2)
            d.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=fg)
            text(d, (tx, ty), name, f_mid, fg, "lm" if ox >= 0 else "rm")
    return img


def frames(shot):
    return int(shot["fps"] * shot["duration_s"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--no-labels", action="store_true")
    ap.add_argument("--every", type=int, default=1)
    a = ap.parse_args()
    shot = sm.load_shot()
    os.makedirs(a.out, exist_ok=True)
    for f in range(0, frames(shot), a.every):
        draw(shot, f, not a.no_labels).save(os.path.join(a.out, f"{f:04d}.png"))
    print("overlay frames:", a.out)
