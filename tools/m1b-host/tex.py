"""M1b host textures — generated, ours (no photos, no AI): shawl wool + cream vine embroidery, leather book cover.
Owner doc: handoff/m1b-host/quality-target.md (plan step 2) · spec: host.json "quality.tex" (RULES I6).
Run through m1b.py (step `tex`), or:  python tex.py [--preview] [--debug] [--dry-run]
Writes out/tex/*.png (never committed). Needs numpy + pillow only. Same seed → same pixels."""
import json, math, os, random, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KIT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KIT, "out", "tex")
SPEC = json.load(open(os.path.join(KIT, "host.json"), encoding="utf-8"))
PAL = SPEC["host"]["palette"]
Q = SPEC.get("quality", {}).get("tex", {})
PREVIEW, DEBUG, DRY = "--preview" in sys.argv, "--debug" in sys.argv, "--dry-run" in sys.argv
SEED = SPEC["host"]["seed"]


def dbg(*a):
    if DEBUG:
        print("[tex]", *a, flush=True)


def rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


def vnoise(w, h, cell, rng, octaves=4):
    """Fractal value noise in 0..1 (bicubic-upsampled random grids)."""
    acc = np.zeros((h, w), np.float32); amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = max(2, int(cell / (2 ** o)))
        g = rng.random((h // c + 3, w // c + 3)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize(((w // c + 3) * c, (h // c + 3) * c), Image.BICUBIC)
        acc += amp * (np.asarray(im, np.float32)[:h, :w] / 255.0); tot += amp; amp *= 0.5
    acc /= tot
    return (acc - acc.min()) / max(1e-6, acc.max() - acc.min())


def save(arr, name, mode="RGB"):
    p = os.path.join(OUT, name)
    if DRY:
        print("[tex] would write", p, arr.shape); return
    a = np.clip(arr * 255 + 0.5, 0, 255).astype(np.uint8)
    Image.fromarray(a, mode if a.ndim == 3 else "L").save(p)
    print("[tex] wrote", os.path.relpath(p, KIT), a.shape[1], "x", a.shape[0], flush=True)


# ---------------- embroidery (vine with leaves + small five-petal flowers) ----------------
def leaf(d, cx, cy, ang, L, Wd, fill=255):
    pts = []
    for k in range(17):
        t = k / 16
        x = (t - 0.5) * L
        y = math.sin(math.pi * t) * Wd / 2
        pts.append((x, y))
    pts += [(x, -y) for x, y in reversed(pts)]
    ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts], fill=fill)
    # mid-vein left unstitched (reads as two satin halves)
    d.line([(cx - L * 0.45 * ca, cy - L * 0.45 * sa), (cx + L * 0.45 * ca, cy + L * 0.45 * sa)], fill=0, width=max(1, int(Wd * 0.12)))


def flower(d, cx, cy, r, rot):
    for k in range(5):
        a = rot + k * 2 * math.pi / 5
        px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
        d.ellipse([px - r * 0.48, py - r * 0.48, px + r * 0.48, py + r * 0.48], fill=255)
    d.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22], fill=0)
    d.ellipse([cx - r * 0.12, cy - r * 0.12, cx + r * 0.12, cy + r * 0.12], fill=255)


def vine(d, p0, p1, s, rng, amp=1.0):
    """Vine along the segment p0→p1 (pixels); s = pixel scale of one 'unit' (≈ 1 cm)."""
    (x0, y0), (x1, y1) = p0, p1
    Ltot = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / Ltot, (y1 - y0) / Ltot; nx, ny = -uy, ux
    lam = 11 * s; A = 1.6 * s * amp; w = max(2, int(0.32 * s))
    pts = []
    n = int(Ltot / (0.4 * s)) + 2
    for k in range(n):
        t = k / (n - 1) * Ltot
        o = A * math.sin(2 * math.pi * t / lam)
        pts.append((x0 + ux * t + nx * o, y0 + uy * t + ny * o))
    d.line(pts, fill=255, width=w, joint="curve")
    k = 0; t = lam * 0.25
    while t < Ltot - lam * 0.2:
        o = A * math.sin(2 * math.pi * t / lam); do = A * 2 * math.pi / lam * math.cos(2 * math.pi * t / lam)
        bx, by = x0 + ux * t + nx * o, y0 + uy * t + ny * o
        tang = math.atan2(uy + ny * do, ux + nx * do)
        side = 1 if k % 2 == 0 else -1
        a = tang + side * math.radians(rng.uniform(40, 60))
        Ll = s * rng.uniform(2.4, 3.0)
        leaf(d, bx + math.cos(a) * Ll * 0.5, by + math.sin(a) * Ll * 0.5, a, Ll, Ll * 0.42)
        if k % 4 == 1:  # flower on a short stalk
            a2 = tang - side * math.radians(70); st = s * 2.6
            fx, fy = bx + math.cos(a2) * st, by + math.sin(a2) * st
            d.line([(bx, by), (fx, fy)], fill=255, width=max(1, w - 1))
            flower(d, fx, fy, s * rng.uniform(1.5, 1.9), rng.uniform(0, 6.28))
        if k % 4 == 3:  # curl tendril
            r = s * 0.9; cx, cy = bx + math.cos(a + 3.14) * r * 1.6, by + math.sin(a + 3.14) * r * 1.6
            d.arc([cx - r, cy - r, cx + r, cy + r], start=math.degrees(a), end=math.degrees(a) + 250, fill=255, width=max(1, w - 1))
        k += 1; t += lam / 2


def sprig(d, cx, cy, s, rng):
    a = rng.uniform(0, 6.28); L = s * rng.uniform(4, 6)
    ex, ey = cx + math.cos(a) * L, cy + math.sin(a) * L
    d.line([(cx, cy), (ex, ey)], fill=255, width=max(1, int(0.28 * s)))
    for j in range(3):
        t = (j + 1) / 4; bx, by = cx + (ex - cx) * t, cy + (ey - cy) * t
        for side in (-1, 1):
            la = a + side * math.radians(50); Ll = s * 1.9
            leaf(d, bx + math.cos(la) * Ll * 0.5, by + math.sin(la) * Ll * 0.5, la, Ll, Ll * 0.45)
    flower(d, ex, ey, s * 1.5, rng.uniform(0, 6.28))


def shawl():
    W, H = Q.get("shawl_px", [4096, 1024])
    if PREVIEW:
        W, H = W // 2, H // 2
    rng = np.random.default_rng(SEED); prng = random.Random(SEED)
    SS = 2  # supersample the embroidery mask
    s = Q.get("stitch_unit_px", 7.0) * (W / 4096) * SS  # EDIT: motif scale (px per ≈1 cm at 4096 wide)
    m = Image.new("L", (W * SS, H * SS), 0); d = ImageDraw.Draw(m)
    bx = Q.get("border_u", 0.045); hy = Q.get("hem_v", 0.88); ty = Q.get("top_v", 0.07)  # EDIT: band centres (UV)
    vine(d, (bx * W * SS, 0.02 * H * SS), (bx * W * SS, (hy - 0.03) * H * SS), s, prng)                 # left front edge
    vine(d, ((1 - bx) * W * SS, 0.02 * H * SS), ((1 - bx) * W * SS, (hy - 0.03) * H * SS), s, prng)     # right front edge
    vine(d, (0.01 * W * SS, hy * H * SS), (0.99 * W * SS, hy * H * SS), s, prng)                         # hem band
    vine(d, (0.10 * W * SS, ty * H * SS), (0.90 * W * SS, ty * H * SS), s * 0.8, prng, amp=0.7)         # top fold band
    # thin straight guard lines either side of the hem vine
    for off in (-3.6, 3.6):
        y = hy * H * SS + off * s
        d.line([(0, y), (W * SS, y)], fill=255, width=max(1, int(0.22 * s)))
    # scattered sprigs (poisson-ish)
    placed = []
    for _ in range(int(Q.get("sprigs", 70))):
        for _try in range(30):
            x, y = prng.uniform(0.12, 0.88) * W * SS, prng.uniform(0.18, 0.78) * H * SS
            if all(math.hypot(x - a, y - b) > 14 * s for a, b in placed):
                placed.append((x, y)); sprig(d, x, y, s * 0.8, prng); break
    m = m.filter(ImageFilter.GaussianBlur(0.6 * SS)).resize((W, H), Image.LANCZOS)
    emb = np.asarray(m, np.float32) / 255.0
    # satin-stitch direction lines inside the motifs
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    stitch = 0.5 + 0.5 * np.sin((xx + yy) * (2 * math.pi / max(2.0, s / SS * 0.55)))
    thread = emb * (0.80 + 0.20 * stitch)
    # wool: knit rows + fuzzy fractal noise + two-tone mottling
    knit = 0.5 + 0.5 * np.sin(yy * 2 * math.pi / max(2.0, 2.2 * W / 4096)) * np.sin(xx * 2 * math.pi / max(2.0, 3.0 * W / 4096))
    fuzz = vnoise(W, H, max(4, W // 512), rng, 4)
    mott = vnoise(W, H, max(8, W // 24), rng, 3)
    base, dark = rgb(PAL["shawl"]), rgb(PAL["shawl_dark"])
    wool = base[None, None, :] * (1 - 0.35 * mott[..., None]) + dark[None, None, :] * (0.35 * mott[..., None])
    wool *= (0.90 + 0.08 * fuzz[..., None] + 0.04 * knit[..., None])
    th = rgb(PAL.get("embroidery", PAL["body"])) * Q.get("thread_dim", 0.9)  # EDIT: thread brightness (swatch stays the ΔE-checked body pearl)
    alb = wool * (1 - thread[..., None]) + th[None, None, :] * thread[..., None]
    height = 0.45 * fuzz + 0.10 * knit + 0.55 * emb
    save(alb, "shawl_albedo.png"); save(height, "shawl_height.png")
    dbg("shawl", W, H, "sprigs", len(placed))


def leather():
    S = Q.get("leather_px", 2048)
    if PREVIEW:
        S //= 2
    rng = np.random.default_rng(SEED + 7); prng = random.Random(SEED + 7)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) / S
    mott = vnoise(S, S, S // 10, rng, 4); grain = vnoise(S, S, max(3, S // 400), rng, 3)
    edge = np.minimum(np.minimum(xx, 1 - xx), np.minimum(yy, 1 - yy))
    wear = np.clip(1 - edge / 0.05, 0, 1) ** 1.5 * (0.6 + 0.4 * vnoise(S, S, S // 40, rng, 2))
    base = rgb(PAL["book_cover"])
    lum = 0.82 + 0.30 * mott + 0.08 * (grain - 0.5) + 0.35 * wear
    alb = np.clip(base[None, None, :] * lum[..., None], 0, 1)
    # scratches
    sc = Image.new("L", (S, S), 0); d = ImageDraw.Draw(sc)
    for _ in range(90):
        x, y = prng.uniform(0, S), prng.uniform(0, S); a = prng.uniform(0, 6.28); L = prng.uniform(0.01, 0.06) * S
        d.line([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], fill=prng.randint(60, 160), width=1)
    scr = np.asarray(sc.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255.0
    alb = np.clip(alb + scr[..., None] * 0.10, 0, 1)
    # blind-tooled double border + small centre lozenge (abstract, no text, no diagram)
    tl = Image.new("L", (S, S), 0); d = ImageDraw.Draw(tl); w = max(2, S // 300)
    for inset in (0.07, 0.095):
        a, b = inset * S, (1 - inset) * S
        d.rectangle([a, a, b, b], outline=255, width=w)
    c = S / 2; r = 0.06 * S
    d.polygon([(c, c - r * 1.5), (c + r, c), (c, c + r * 1.5), (c - r, c)], outline=255, width=w)
    tool = np.asarray(tl.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255.0
    alb *= (1 - 0.35 * tool[..., None])
    height = np.clip(0.5 + 0.25 * (grain - 0.5) + 0.15 * (mott - 0.5) - 0.40 * tool - 0.2 * scr, 0, 1)
    save(alb, "leather_albedo.png"); save(height, "leather_height.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    shawl(); leather()


if __name__ == "__main__":
    main()
