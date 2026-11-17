"""Shared geometry for shot M1-ps01. Pure Python (no numpy) so Blender's Python can import it.
three.js mirrors this file in B_three/shot.js - keep the two in step (same names, same formulas)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SHOT_PATH = os.path.join(HERE, "..", "shot.json")


def load_shot(path=SHOT_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def lerp(a, b, t):
    return a + (b - a) * t


def clamp01(t):
    return max(0.0, min(1.0, t))


def smooth(t):
    t = clamp01(t)
    return t * t * (3 - 2 * t)


def progress(shot, frame):
    """0..1 morph progress for a frame (holds at both ends, eased in/out)."""
    tl = shot["timeline"]
    t = frame / shot["fps"]
    a, b = tl["hold_start_s"], shot["duration_s"] - tl["hold_end_s"]
    return smooth((t - a) / (b - a))


def state(shot, frame):
    u = progress(shot, frame)
    d, tl = shot["disc"], shot["timeline"]
    L = lerp(*d["length_units"], u)
    s = {
        "u": u,
        "L": L,
        "wr": lerp(*d["width_ratio"], u),
        "pear": lerp(*d["pear"], u),
        "tip": lerp(*shot["streak"]["tip_frac"], u),
        "meso": lerp(*shot["mesoderm"]["spread"], clamp01((u - shot["mesoderm"]["delay"]) / (1 - shot["mesoderm"]["delay"]))),
        "endo": lerp(*shot["endoderm"]["spread"], clamp01((u - shot["endoderm"]["delay"]) / (1 - shot["endoderm"]["delay"]))),
        "day_f": lerp(tl["day_start"], tl["day_end"], u),
    }
    s["day"] = int(math.floor(s["day_f"] + 0.5))
    s["size_mm"] = L * 0.1
    lay = shot["layers"]
    s["yc"] = lay["cut_y_frac"] * (s["wr"] * L / 2)  # cut plane (near side removed)
    return s


def outline(L, wr, pear, n):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x = (L / 2) * math.cos(a)
        y = (wr * L / 2) * math.sin(a) * (1 + 0.5 * pear * (x / (L / 2)))
        pts.append((x, y))
    return pts


def scale_from(pts, ax, k):
    return [(ax + k * (x - ax), k * y) for x, y in pts]


def clip_y_ge(pts, yc):
    """Sutherland-Hodgman clip of a closed polygon to y >= yc."""
    out = []
    n = len(pts)
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        pin, qin = p[1] >= yc, q[1] >= yc
        if pin:
            out.append(p)
        if pin != qin:
            t = (yc - p[1]) / (q[1] - p[1])
            out.append((p[0] + t * (q[0] - p[0]), yc))
    return out


def prism(poly, z0, z1):
    """Closed prism from a convex polygon. Returns (verts, tris) with separate cap/side verts
    so flat shading matches in Blender and three.js."""
    n = len(poly)
    verts, tris = [], []
    if n < 3:
        return verts, tris
    cx = sum(p[0] for p in poly) / n
    cy = sum(p[1] for p in poly) / n
    # top cap (fan around centroid), normal +z
    base = len(verts)
    verts.append((cx, cy, z1))
    verts += [(x, y, z1) for x, y in poly]
    for i in range(n):
        tris.append((base, base + 1 + i, base + 1 + (i + 1) % n))
    # bottom cap, normal -z
    base = len(verts)
    verts.append((cx, cy, z0))
    verts += [(x, y, z0) for x, y in poly]
    for i in range(n):
        tris.append((base, base + 1 + (i + 1) % n, base + 1 + i))
    # sides
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        b = len(verts)
        verts += [(x0, y0, z0), (x1, y1, z0), (x1, y1, z1), (x0, y0, z1)]
        tris += [(b, b + 1, b + 2), (b, b + 2, b + 3)]
    return verts, tris


def ccw(pts):
    a = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return pts if a > 0 else pts[::-1]


def build(shot, frame):
    """Returns (state, parts). Each part: name, poly(2D), z0, z1, color, opacity."""
    s = state(shot, frame)
    lay, n = shot["layers"], shot["disc"]["segments"]
    L, te, g, th, yc = s["L"], lay["epiblast_thick"], lay["gap"], lay["hypoblast_thick"], s["yc"]
    col, op = shot["colors"], shot["opacity"]
    disc = outline(L, s["wr"], s["pear"], n)
    parts = []

    def add(name, poly, z0, z1, opacity=1.0, colour=None):
        if len(poly) >= 3:
            parts.append(dict(name=name, poly=ccw(poly), z0=z0, z1=z1, color=colour or col[name], opacity=opacity))

    add("hypoblast", clip_y_ge(disc, yc), -g - th, -g)
    add("epiblast", clip_y_ge(disc, yc), 0.0, te, op["epiblast"])
    ax = -L / 2 + 0.03 * L
    if s["meso"] > 0.02:
        add("mesoderm", clip_y_ge(scale_from(disc, ax, s["meso"] * 0.97), yc), -g + 0.035, -0.02, op["mesoderm"])
    if s["endo"] > 0.02:
        add("endoderm", clip_y_ge(scale_from(disc, ax, s["endo"] * 0.97), yc - 0.004), -g - th - 0.005, -g + 0.005)
    st = shot["streak"]
    x0, x1, w = -L / 2 + st["start_frac"] * L, -L / 2 + s["tip"] * L, st["width"] / 2
    add("streak", [(x0, -w), (x1, -w), (x1, w), (x0, w)], te, te + st["height"])
    nd = shot["node"]
    circle = [(x1 + nd["radius"] * math.cos(2 * math.pi * i / 32), nd["radius"] * math.sin(2 * math.pi * i / 32)) for i in range(32)]
    add("node", circle, te, te + nd["height"], colour=col["streak"])
    return s, parts


def label_anchors(shot, s, parts):
    """3D anchor points for on-structure labels (RULES D8). Cut-face anchors only when the layer reaches the cut."""
    te, g, th = shot["layers"]["epiblast_thick"], shot["layers"]["gap"], shot["layers"]["hypoblast_thick"]
    by = {p["name"]: p for p in parts}
    out = {}

    def cut_x(p, yc, side="mid"):
        xs = [x for x, y in p["poly"] if abs(y - yc) < 1e-6]
        if len(xs) < 2:
            return None
        lo, hi = min(xs), max(xs)
        return {"mid": (lo + hi) / 2, "cranial": lo + 0.8 * (hi - lo)}[side]

    L = s["L"]
    out["epiblast"] = (0.30 * L, 0.20 * L * s["wr"], te)
    hx = cut_x(by["hypoblast"], s["yc"], "cranial")
    if hx is not None:
        out["hypoblast"] = (hx, s["yc"], -g - th / 2)
    xs = [x for x, _ in by["streak"]["poly"]]
    out["primitive streak"] = ((min(xs) + max(xs)) / 2, 0.0, te + 0.03)
    out["primitive node"] = (max(xs), 0.0, te + 0.06)
    if "mesoderm" in by:
        mx = cut_x(by["mesoderm"], s["yc"])
        if mx is not None:
            out["mesoderm"] = (mx, s["yc"], -g / 2)
    if "endoderm" in by:
        ex = cut_x(by["endoderm"], s["yc"] - 0.004)
        if ex is not None:
            out["endoderm"] = (ex, s["yc"] - 0.004, -g - th / 2)
    return out


def project(shot, p):
    """Ortho camera at (0, -D cos e, D sin e) looking at origin, up = +z. Returns pixel (x, y)."""
    W, H = shot["width"], shot["height"]
    ppu = W / shot["camera"]["ortho_width_units"]
    e = math.radians(shot["camera"]["elevation_deg"])
    x, y, z = p
    return (W / 2 + x * ppu, H / 2 - (y * math.sin(e) + z * math.cos(e)) * ppu)


def depth(shot, p):
    """Distance along view direction (bigger = farther) for painter's sort in the 2D preview."""
    e = math.radians(shot["camera"]["elevation_deg"])
    return p[1] * math.cos(e) - p[2] * math.sin(e)
