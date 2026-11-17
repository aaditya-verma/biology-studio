"""Cloud-side check only (not a bake-off method): flat 2D painter's render of the shared geometry +
the real overlay, to verify projection maths, label anchors and the encode/manifest path.
Usage: python preview2d.py OUT_DIR"""
import os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_math as sm
from overlay import draw, frames, hexc


def shade(c, k):
    return tuple(int(min(255, v * k)) for v in c[:3]) + (c[3],)


def render(shot, f):
    W, H = shot["width"], shot["height"]
    img = Image.new("RGBA", (W, H), hexc(shot["colors"]["background"]))
    _, parts = sm.build(shot, f)
    faces = []
    for p in parts:
        v, t = sm.prism(p["poly"], p["z0"], p["z1"])
        base = hexc(p["color"], int(255 * p["opacity"]))
        for a, b, c in t:
            pa, pb, pc = v[a], v[b], v[c]
            nz = ((pb[0] - pa[0]) * (pc[1] - pa[1]) - (pb[1] - pa[1]) * (pc[0] - pa[0]))
            k = 1.0 if abs(pa[2] - pb[2]) < 1e-9 and abs(pa[2] - pc[2]) < 1e-9 else 0.72
            if k == 1.0 and nz < 0:
                k = 0.5
            dep = sum(sm.depth(shot, q) for q in (pa, pb, pc)) / 3
            faces.append((dep, [sm.project(shot, q) for q in (pa, pb, pc)], shade(base, k)))
    faces.sort(key=lambda x: -x[0])
    dr = ImageDraw.Draw(img, "RGBA")
    for _, pts, col in faces:
        dr.polygon(pts, fill=col)
    img.alpha_composite(draw(shot, f))
    return img.convert("RGB")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    shot = sm.load_shot()
    for f in range(frames(shot)):
        render(shot, f).save(os.path.join(out, f"{f:04d}.png"))
