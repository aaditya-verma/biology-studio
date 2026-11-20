"""Nani Koshika — procedural 3D host for the M1b test shot (D-048 host, D-049 route H-a). Runs INSIDE Blender 4.5 LTS:
  blender --background --factory-startup --python blender_host.py -- --mode sheet|shot --out <dir> --kit <dir> [--preview] [--only X] [--debug]
Called by host.py; you rarely run it by hand. Our own model, built from the reference turnaround (never traced, never shipped).
Owner docs: build/studio-playbook.md §5b (host + D5 rules), build/visual-style.md §8 (light, camera). Values: spec.py (# EDIT:).
Shape edit points in this file are marked `# EDIT:`."""
import json, math, os, sys, time

import bmesh
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None, flag=False):
    if flag:
        return name in argv
    return argv[argv.index(name) + 1] if name in argv else default


MODE = arg("--mode", "sheet")
OUT = arg("--out", os.path.abspath("out"))
KIT = arg("--kit", os.path.dirname(os.path.abspath(__file__)))
PREVIEW = arg("--preview", flag=True)
DEBUG = arg("--debug", flag=True)
ONLY = arg("--only")
sys.path.insert(0, KIT)
import spec  # noqa: E402

STATS = {"version": bpy.app.version_string, "mode": MODE, "preview": PREVIEW, "renders": {}}


def dbg(*a):
    if DEBUG:
        print("[blender_host]", *a, flush=True)


# ---------------- body geometry (shared maths) ----------------
RX, RY, RZ, TAPER = 1.0, 0.92, 1.22, 0.07   # EDIT: egg radii (m) + bottom widening


def taper(z):            # z relative to the centre
    return 1 + TAPER * (-z / RZ)


def surf_y(x, zw):
    """Front surface y (negative) of the body at world x, z."""
    z = zw - RZ
    f = taper(z)
    X, Z = x / f / RX, z / RZ
    return -math.sqrt(max(0.0, 1 - X * X - Z * Z)) * RY * f


def section(zw):
    """Body cross-section semi-axes (a along x, b along y) at world height zw."""
    z = zw - RZ
    k = math.sqrt(max(0.0, 1 - (z / RZ) ** 2)) * taper(z)
    return RX * k, RY * k


# ---------------- helpers ----------------
def hexlin(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return (*c, a)


def setin(node, names, value):
    for n in names if isinstance(names, (list, tuple)) else [names]:
        if n in node.inputs:
            node.inputs[n].default_value = value
            return True
    dbg("no input", names, "on", node.name)
    return False


def mat(name, base, rough=0.5, sss=0.0, sss_radius=(0.6, 0.35, 0.25), coat=0.0, metal=0.0, emit=None, emit_strength=0.0, sheen=0.0, spec_ior=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    setin(b, "Base Color", hexlin(base))
    setin(b, "Roughness", rough)
    setin(b, "Metallic", metal)
    setin(b, ["Subsurface Weight", "Subsurface"], sss)
    setin(b, "Subsurface Radius", sss_radius)
    setin(b, ["Coat Weight", "Clearcoat"], coat)
    setin(b, ["Sheen Weight", "Sheen"], sheen)
    setin(b, ["Specular IOR Level", "Specular"], spec_ior)
    if emit:
        setin(b, ["Emission Color", "Emission"], hexlin(emit))
        setin(b, "Emission Strength", emit_strength)
    return m


def link(ob, parent=None, material=None):
    bpy.context.scene.collection.objects.link(ob)
    if parent:
        ob.parent = parent
    if material and ob.type in {"MESH", "CURVE"}:
        ob.data.materials.append(material)
    return ob


def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    e.empty_display_size = 0.1
    return link(e, parent)


def sphere(name, r, loc=(0, 0, 0), scale=(1, 1, 1), parent=None, material=None, seg=(32, 16), smooth=True):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg[0], v_segments=seg[1], radius=r)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.location, ob.scale = loc, scale
    return link(ob, parent, material)


def torus(name, R, r, loc, rot, parent=None, material=None, seg=(48, 10)):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = []
    for i in range(seg[0]):
        u = 2 * math.pi * i / seg[0]
        ring = []
        for j in range(seg[1]):
            v = 2 * math.pi * j / seg[1]
            ring.append(bm.verts.new(((R + r * math.cos(v)) * math.cos(u), (R + r * math.cos(v)) * math.sin(u), r * math.sin(v))))
        verts.append(ring)
    for i in range(seg[0]):
        for j in range(seg[1]):
            a, b = verts[i][j], verts[(i + 1) % seg[0]][j]
            c, d = verts[(i + 1) % seg[0]][(j + 1) % seg[1]], verts[i][(j + 1) % seg[1]]
            bm.faces.new((a, b, c, d))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.location, ob.rotation_euler = loc, rot
    return link(ob, parent, material)


def rod(name, p0, p1, r, parent=None, material=None):
    """Cylinder between two points."""
    p0, p1 = Vector(p0), Vector(p1)
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=r, radius2=r, depth=(p1 - p0).length)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = (p0 + p1) / 2
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference((p1 - p0).normalized())
    return link(ob, parent, material)


def curve(name, pts, bevel, parent=None, material=None):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = bevel
    cu.bevel_resolution = 4
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    ob = bpy.data.objects.new(name, cu)
    return link(ob, parent, material)


def box(name, size, loc, rot=(0, 0, 0), parent=None, material=None, bevel=0.01):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location, ob.rotation_euler, ob.scale = loc, rot, size
    link(ob, parent, material)
    if bevel:
        m = ob.modifiers.new("bevel", "BEVEL")
        m.width, m.segments = bevel, 2
    return ob


# ---------------- scene ----------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def build():
    C = spec.COL
    M = {
        # body: pearl, SSS, thin coat; warm glow low in the body (book light) — measured in the manifest
        "body": mat("body", C["body"], rough=0.18, sss=0.6, sss_radius=(0.9, 0.55, 0.4), coat=0.5, emit=C["glow"], emit_strength=0.0),   # EDIT: glassy SSS (G-Art R1: more depth)
        "shawl": mat("shawl", C["shawl"], rough=0.9, sheen=0.6),
        "fringe": mat("fringe", C["fringe"], rough=0.9, sheen=0.4),
        "ink": mat("ink", C["ink"], rough=0.3),
        "iris": mat("iris", C["iris"], rough=0.15, coat=1.0),
        "eye": mat("eye_white", C["eye_white"], rough=0.1, coat=1.0),
        "hi": mat("eye_highlight", "#FFFFFF", emit="#FFFFFF", emit_strength=4.0),
        "blush": mat("blush", C["blush"], rough=0.5, sss=0.2),
        "brow": mat("brow", C["brow"], rough=0.8),
        "metal": mat("glasses", C["glasses"], rough=0.25, metal=1.0),
        "book": mat("book", C["book"], rough=0.6),
        "pages": mat("pages", C["pages"], rough=0.8, emit=C["pages"], emit_strength=0.35),
        "ribbon": mat("ribbon", C["ribbon"], rough=0.6),
        "mouth": mat("mouth", "#2A1214", rough=0.6),
        "plate": mat("plate", C["plate"], rough=0.7),
    }
    glow_nodes(M["body"])
    hammered_bump(M["body"])
    embroidery_nodes(M["shawl"])
    root = empty("Nani")
    # body
    me = bpy.data.meshes.new("body")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=72, v_segments=40, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co.x * RX, v.co.y * RY, v.co.z * RZ
        f = taper(z)
        v.co = (x * f, y * f, z + RZ)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    body = link(bpy.data.objects.new("body", me), root, M["body"])
    s = body.modifiers.new("sub", "SUBSURF")
    s.levels, s.render_levels = 1, 2
    rig = {"root": root, "body": body, "M": M}
    build_face(rig)
    build_glasses(rig)
    build_shawl(rig)
    build_hands_book(rig)
    build_set(rig)
    return rig


def glow_nodes(m):
    """Emission strength rises toward the lower body (lit by the book), like the reference — kept pale (spec.COL.glow)."""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    mr.inputs["From Min"].default_value = 0.05
    mr.inputs["From Max"].default_value = 0.65
    mr.inputs["To Min"].default_value = 0.55   # EDIT: glow strength at the bottom
    mr.inputs["To Max"].default_value = 0.04   # EDIT: glow strength at the top
    nt.links.new(mr.outputs["Result"], b.inputs["Emission Strength"])


def hammered_bump(m, strength=0.05):
    """Subtle hammered-glass surface like the reference (EDIT strength). Diffuse glow only — no bright core (D5: must not read as a nucleus/yolk)."""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vo = nt.nodes.new("ShaderNodeTexVoronoi")
    vo.inputs["Scale"].default_value = 18.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    nt.links.new(tc.outputs["Object"], vo.inputs["Vector"])
    nt.links.new(vo.outputs["Distance"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])


def embroidery_nodes(m):
    """Sparse pale vine-like embroidery on the shawl (procedural; no copied pattern)."""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 7.0   # EDIT: motif size
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = hexlin(spec.COL["embroidery"])
    ramp.color_ramp.elements[1].position = 0.035  # EDIT: line thickness
    ramp.color_ramp.elements[1].color = hexlin(spec.COL["shawl"])
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    nt.links.new(vor.outputs["Distance"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])


EYE_Z, EYE_X = 1.72, 0.30       # EDIT: eye height + spacing
MOUTH_Z, MOUTH_W = 1.38, 0.15   # EDIT: mouth height + half width


def build_face(rig):
    M, root = rig["M"], rig["root"]
    for side, sx in (("L", -1), ("R", 1)):
        x = sx * EYE_X
        ey = surf_y(x, EYE_Z)
        eye = empty(f"eye_{side}", (x, ey + 0.05, EYE_Z), root)
        sphere(f"eyeball_{side}", 0.125, (0, 0, 0), parent=eye, material=M["eye"])
        look = empty(f"look_{side}", (0, 0, 0), eye)
        sphere(f"iris_{side}", 0.078, (0, -0.105, 0), (1, 0.35, 1), look, M["iris"])
        sphere(f"pupil_{side}", 0.04, (0, -0.128, 0), (1, 0.3, 1), look, M["ink"])
        sphere(f"hi_{side}", 0.017, (-0.03, -0.135, 0.035), parent=look, material=M["hi"], seg=(12, 6))
        rig[f"eye_{side}"], rig[f"look_{side}"] = eye, look
        bz = EYE_Z + 0.19
        brow = sphere(f"brow_{side}", 1.0, (x, surf_y(x, bz) - 0.01, bz), (0.10, 0.025, 0.02), root, M["brow"], seg=(16, 8))
        rig[f"brow_{side}"] = brow
        cz = 1.48
        sphere(f"blush_{side}", 0.11, (sx * 0.43, surf_y(sx * 0.43, cz) + 0.02, cz), (1, 0.25, 0.7), root, M["blush"], seg=(16, 8))
    sphere("nose", 0.06, (0, surf_y(0, 1.55) + 0.005, 1.55), (1, 0.8, 0.9), root, rig["M"]["body"], seg=(16, 8))
    pts = [(-MOUTH_W, surf_y(-MOUTH_W, MOUTH_Z) - 0.012, MOUTH_Z), (0, surf_y(0, MOUTH_Z) - 0.012, MOUTH_Z), (MOUTH_W, surf_y(MOUTH_W, MOUTH_Z) - 0.012, MOUTH_Z)]
    rig["lip"] = curve("lip", pts, 0.011, root, M["ink"])
    rig["lip_base"] = pts
    rig["mouth"] = sphere("mouth_open", 1.0, (0, surf_y(0, MOUTH_Z - 0.05) + 0.01, MOUTH_Z - 0.05), (0.1, 0.03, 0.005), root, M["mouth"], seg=(24, 12))


def build_glasses(rig):
    M, root = rig["M"], rig["root"]
    gy = {}
    for side, sx in (("L", -1), ("R", 1)):
        x = sx * EYE_X
        y = surf_y(x, EYE_Z) - 0.17
        gy[side] = y
        torus(f"lens_rim_{side}", 0.165, 0.009, (x, y, EYE_Z - 0.02), (math.radians(90), 0, 0), root, M["metal"])
        tx = sx * (EYE_X + 0.165)
        a, _ = section(EYE_Z)
        rod(f"temple_{side}", (tx, y, EYE_Z), (sx * a * 0.98, 0.0, EYE_Z + 0.02), 0.008, root, M["metal"])
        # chain: from the rim's outer edge, hanging to the shawl
        sa, sb = section(1.25)
        curve(f"chain_{side}", [(tx, y + 0.02, EYE_Z - 0.04), (sx * (EYE_X + 0.24), y - 0.03, 1.45), (sx * sa * 0.88, -sb * 0.72, 1.24)], 0.004, root, M["metal"])
    rod("bridge", (-EYE_X + 0.165, gy["L"], EYE_Z - 0.0), (EYE_X - 0.165, gy["R"], EYE_Z - 0.0), 0.008, root, M["metal"])


def build_shawl(rig):
    """A draped wool shell around the shoulders and sides, open at the front, with a fringe (EDIT values below)."""
    M, root = rig["M"], rig["root"]
    Z_TOP, Z_BOT = 1.46, 0.42           # EDIT: shawl top + hem heights
    OPEN_TOP, OPEN_BOT = 38, 24         # EDIT: front opening half-angle (deg) at top / hem
    NU, NV = 96, 28
    me = bpy.data.meshes.new("shawl")
    bm = bmesh.new()
    grid = []
    for j in range(NV + 1):
        t = j / NV
        z = Z_TOP + (Z_BOT - Z_TOP) * t
        a, b = section(z)
        o = math.radians(OPEN_TOP + (OPEN_BOT - OPEN_TOP) * t)
        drape = 0.05 + 0.12 * t ** 1.5      # EDIT: hangs away from the body toward the hem
        row = []
        for i in range(NU + 1):
            phi = o + (2 * math.pi - 2 * o) * i / NU
            fold = 0.025 * math.sin(phi * 9 + t * 4) * t
            k = 1.04
            x = (a * k + drape + fold) * math.sin(phi)
            y = -(b * k + drape + fold) * math.cos(phi)
            if t < 0.12:                     # rolled top edge hugs the body
                x, y = x * 0.985, y * 0.985
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for j in range(NV):
        for i in range(NU):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    sh = link(bpy.data.objects.new("shawl", me), root, M["shawl"])
    so = sh.modifiers.new("solid", "SOLIDIFY")
    so.thickness = 0.045
    su = sh.modifiers.new("sub", "SUBSURF")
    su.levels, su.render_levels = 1, 2
    # fringe
    fm = bpy.data.meshes.new("fringe")
    bm = bmesh.new()
    a, b = section(Z_BOT)
    o = math.radians(OPEN_BOT)
    n = 150                                   # EDIT: fringe strands
    for i in range(n + 1):
        phi = o + (2 * math.pi - 2 * o) * i / n
        drape = 0.05 + 0.12
        x = (a * 1.04 + drape) * math.sin(phi)
        y = -(b * 1.04 + drape) * math.cos(phi)
        L = 0.16 + 0.05 * ((i * 7919) % 13) / 13
        g = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.007, radius2=0.005, depth=L)
        bmesh.ops.translate(bm, verts=g["verts"], vec=(x, y, Z_BOT - L / 2 + 0.01))
    bm.to_mesh(fm)
    bm.free()
    link(bpy.data.objects.new("fringe", fm), root, M["fringe"])
    rig["shawl"] = sh


def build_hands_book(rig):
    M, root = rig["M"], rig["root"]
    hz = 1.02
    for side, sx in (("L", -1), ("R", 1)):
        x = sx * 0.36
        sphere(f"hand_{side}", 0.15, (x, surf_y(x, hz) - 0.13, hz), (1.25, 0.85, 0.8), root, M["body"])
    by = surf_y(0, 0.95) - 0.30
    tilt = (math.radians(-22), 0, 0)
    box("book", (0.82, 0.10, 0.46), (0, by, 0.86), tilt, root, M["book"], bevel=0.015)
    box("pages", (0.78, 0.08, 0.40), (0, by + 0.035, 1.05), (math.radians(68), 0, 0), root, M["pages"], bevel=0.02)
    box("ribbon", (0.025, 0.012, 0.42), (0, by - 0.058, 0.82), tilt, root, M["ribbon"], bevel=0)
    L = bpy.data.lights.new("book_glow", "AREA")      # warm light from the pages up to the face
    L.energy, L.size, L.color = 80, 0.5, hexlin(spec.COL["glow"])[:3]   # EDIT: book light (warmth comes from light, not the body hue — D-048)
    lo = bpy.data.objects.new("book_glow", L)
    lo.location, lo.rotation_euler = (0, by - 0.05, 1.12), (math.radians(180 - 25), 0, 0)
    link(lo, root)


def build_set(rig):
    sc = bpy.context.scene
    w = bpy.data.worlds.new("plate")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hexlin(spec.COL["plate"])
    bg.inputs["Strength"].default_value = 0.35
    sc.world = w
    me = bpy.data.meshes.new("ground")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=20)
    bm.to_mesh(me)
    bm.free()
    link(bpy.data.objects.new("ground", me), None, rig["M"]["plate"])
    box("backdrop", (40, 0.1, 20), (0, 9, 10), parent=None, material=rig["M"]["plate"], bevel=0)
    tgt = empty("light_target", (0, 0, 1.4))
    for name, loc, energy, size, col in [("key", (-3.6, -4.2, 4.6), 900, 2.5, "#FFF0E0"),     # EDIT: key (cranial-dorsal style: high, front-left)
                                         ("rim", (2.8, 3.8, 3.6), 700, 2.0, "#FFE2C8"),       # EDIT: warm backlight → rim glow
                                         ("fill", (4.2, -3.0, 1.5), 140, 3.0, "#E8E4F0")]:    # EDIT: soft fill
        L = bpy.data.lights.new(name, "AREA")
        L.energy, L.size, L.color = energy, size, hexlin(col)[:3]
        lo = link(bpy.data.objects.new(name, L))
        lo.location = loc
        c = lo.constraints.new("TRACK_TO")
        c.target, c.track_axis, c.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"


def camera(name, pos, target, lens, fstop=None):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_fit = "VERTICAL"
    cam = link(bpy.data.objects.new(name, cd))
    cam.location = pos
    t = empty(name + "_target", target)
    c = cam.constraints.new("TRACK_TO")
    c.target, c.track_axis, c.up_axis = t, "TRACK_NEGATIVE_Z", "UP_Y"
    if fstop:
        cd.dof.use_dof = True
        cd.dof.focus_object = t
        cd.dof.aperture_fstop = fstop
    return cam


# ---------------- face controls ----------------
def apply_face(rig, e, f=None, mouth=None):
    """e = expression dict (spec.EXPR); mouth = viseme {open, round, wide} or None; f = frame to key (None = no key)."""
    def key(ob, path):
        if f is not None:
            ob.keyframe_insert(path, frame=f)
    blink = e.get("blink", 1.0)
    for side, sx in (("L", -1), ("R", 1)):
        eye, look, brow = rig[f"eye_{side}"], rig[f"look_{side}"], rig[f"brow_{side}"]
        op = max(0.04, e["eye_open"] * blink)
        eye.scale = (1.0 + 0.04 * (e["eye_open"] > 1.1), 1.0, op)
        key(eye, "scale")
        look.location = (e["look"][0] * 0.03, 0, e["look"][1] * 0.025)
        key(look, "location")
        raise_ = e["brow_l"] if side == "L" else e["brow_r"]
        x = sx * EYE_X
        bz = EYE_Z + 0.19 + 0.06 * raise_ + (0.03 if e["eye_open"] > 1.1 else 0)
        brow.location = (x, surf_y(x, bz) - 0.01, bz)
        key(brow, "location")
        brow.rotation_euler = (0, (-1 if side == "L" else 1) * math.radians(14) * e["brow_tilt"], 0)
        key(brow, "rotation_euler")
    m = mouth or {"open": 0.0, "round": 0.0, "wide": 0.0}
    op = max(m["open"], e["mouth_open"] if mouth is None or m["open"] < 0.05 else 0.0)
    rd = max(m["round"], e["mouth_round"] if mouth is None else 0.0)
    smile = e["smile"] + 0.3 * m["wide"]
    lip = rig["lip"].data.splines[0].bezier_points
    base = rig["lip_base"]
    w = 1 - 0.35 * rd
    for i, (bp, b) in enumerate(zip(lip, base)):
        x = b[0] * w
        z = b[2] + (0.06 * smile if i != 1 else -0.02 * smile)
        if i == 2:
            z += 0.05 * e["asym"]
        if i == 0:
            z -= 0.015 * e["asym"]
        bp.co = (x, surf_y(x, z) - 0.012, z)
        if f is not None:
            bp.keyframe_insert("co", frame=f)
    mo = rig["mouth"]
    mo.scale = (0.09 * (1 + 0.3 * m["wide"]) * (1 - 0.4 * rd), 0.03, 0.004 + 0.085 * op)
    mz = MOUTH_Z - 0.01 - 0.08 * op
    mo.location = (0, surf_y(0, mz) + 0.012, mz)
    key(mo, "scale")
    key(mo, "location")


def blend_expr(a, b, t):
    out = {}
    for k in a:
        if isinstance(a[k], tuple):
            out[k] = tuple(x + (y - x) * t for x, y in zip(a[k], b[k]))
        else:
            out[k] = a[k] + (b[k] - a[k]) * t
    return out


def expr_at(ts):
    P = spec.PERFORMANCE
    cur = P[0]
    for i, (t0, name) in enumerate(P):
        if ts >= t0:
            cur = (i, name)
    i, name = cur
    e = dict(spec.EXPR[name])
    if i > 0:
        t0 = P[i][0]
        k = min(1.0, (ts - t0) / 0.25)                       # EDIT: 0.25 s expression transitions
        k = k * k * (3 - 2 * k)
        e = blend_expr(spec.EXPR[P[i - 1][1]], spec.EXPR[name], k)
    return e


def blink_at(ts):
    for b in spec.BLINKS_S:
        d = ts - b
        if 0 <= d < 2 / spec.FPS:
            return 0.05
        if 2 / spec.FPS <= d < 5 / spec.FPS:
            return 0.05 + 0.95 * (d - 2 / spec.FPS) / (3 / spec.FPS)
    return 1.0


# ---------------- render setup ----------------
def setup_render(size, samples, film_transparent=False):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = size
    sc.render.resolution_percentage = 100
    sc.render.fps = spec.FPS
    sc.render.film_transparent = film_transparent
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if film_transparent else "RGB"
    if spec.ENGINE == "CYCLES":
        sc.render.engine = "CYCLES"
        try:
            pr = bpy.context.preferences.addons["cycles"].preferences
            for dev_type in ("OPTIX", "CUDA"):
                try:
                    pr.compute_device_type = dev_type
                    pr.get_devices()
                    for d in pr.devices:
                        d.use = True
                    sc.cycles.device = "GPU"
                    break
                except TypeError:
                    continue
        except Exception as ex:
            dbg("GPU setup failed", ex)
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.seed = spec.SEED
    else:
        for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                sc.render.engine = e
                break
            except TypeError:
                continue
        sc.eevee.taa_render_samples = samples
        for attr, val in (("use_raytracing", True), ("use_shadows", True), ("use_gtao", True)):
            if hasattr(sc.eevee, attr):
                setattr(sc.eevee, attr, val)
    try:
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Medium High Contrast"   # EDIT: filmic grade (host skips the warm LUT, playbook §5b)
    except TypeError:
        dbg("AgX look not available; using default view transform")
    STATS["engine"] = sc.render.engine


def render_still(cam, path):
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.filepath = path
    t = time.time()
    bpy.ops.render.render(write_still=True)
    STATS["renders"][os.path.basename(path)] = round(time.time() - t, 2)
    print(f"[blender_host] {os.path.basename(path)} {STATS['renders'][os.path.basename(path)]} s", flush=True)


def render_mask(cam, path, targets):
    """Alpha = where `targets` are visible from cam (others become holdout) — for ΔE00 on rendered pixels."""
    hold = bpy.data.materials.new("holdout")
    hold.use_nodes = True
    nt = hold.node_tree
    nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    h = nt.nodes.new("ShaderNodeHoldout")
    nt.links.new(h.outputs[0], o.inputs["Surface"])
    white = mat("mask_white", "#FFFFFF", emit="#FFFFFF", emit_strength=1.0)
    saved = {}
    for ob in bpy.context.scene.objects:
        if ob.type in {"MESH", "CURVE"} and len(ob.material_slots):
            saved[ob.name] = [s.material for s in ob.material_slots]
            for s in ob.material_slots:
                s.material = white if ob.name in targets else hold
    sc = bpy.context.scene
    setup_render((sc.render.resolution_x, sc.render.resolution_y), 8, film_transparent=True)
    render_still(cam, path)
    for ob in bpy.context.scene.objects:
        if ob.name in saved:
            for s, m in zip(ob.material_slots, saved[ob.name]):
                s.material = m


# ---------------- modes ----------------
def mode_sheet(rig):
    size = (720, 1280) if PREVIEW else (1440, 2560)   # EDIT: sheet render size (portrait)
    face_size = (640, 640) if PREVIEW else (1400, 1400)
    samples = spec.SAMPLES["preview"] if PREVIEW else spec.SAMPLES[spec.ENGINE]
    cams = {k: camera(f"sheet_{k}", v["pos"], v["target"], v["lens_mm"]) for k, v in spec.SHEET_CAMS.items()}
    d = os.path.join(OUT, "sheet")
    os.makedirs(d, exist_ok=True)
    todo = ["front", "side"] + list(spec.EXPR.keys())
    if ONLY:
        todo = [t for t in todo if t == ONLY]
    for v in todo:
        if v in ("front", "side"):
            apply_face(rig, spec.EXPR["neutral"])
            setup_render(size, samples)
            render_still(cams[v], os.path.join(d, f"{v}.png"))
            if v == "front":
                render_mask(cams[v], os.path.join(d, "mask_body.png"), {"body", "nose", "hand_L", "hand_R"})
                render_mask(cams[v], os.path.join(d, "mask_shawl.png"), {"shawl"})
        else:
            apply_face(rig, spec.EXPR[v])
            setup_render(face_size, samples)
            render_still(cams["face"], os.path.join(d, f"{v.replace(' ', '_')}.png"))


def mode_shot(rig, anim):
    sc = bpy.context.scene
    nf = int(round(spec.DURATION_S * spec.FPS))
    cut = int(round(spec.CUT_AT_S * spec.FPS))
    sc.frame_start, sc.frame_end = 1, nf
    size = spec.PREVIEW if PREVIEW else spec.MASTER
    samples = spec.SAMPLES["preview"] if PREVIEW else spec.SAMPLES[spec.ENGINE]
    camA = camera("cam_A", spec.CAM_A["start"], spec.CAM_A["target"], spec.CAM_A["lens_mm"], spec.CAM_A["fstop"])
    camB = camera("cam_B", spec.CAM_B["start"], spec.CAM_B["target"], spec.CAM_B["lens_mm"], spec.CAM_B["fstop"])
    for cam, cs, f0, f1 in ((camA, spec.CAM_A, 1, cut), (camB, spec.CAM_B, cut + 1, nf)):
        cam.location = cs["start"]; cam.keyframe_insert("location", frame=f0)
        cam.location = cs["end"]; cam.keyframe_insert("location", frame=f1)
    sc.timeline_markers.new("A", frame=1).camera = camA
    sc.timeline_markers.new("B", frame=cut + 1).camera = camB
    vis = anim.get("visemes", [])
    env = anim.get("envelope", [0] * nf)
    root = rig["root"]
    for f in range(1, nf + 1):
        ts = (f - 1) / spec.FPS
        e = expr_at(ts)
        e["blink"] = blink_at(ts)
        m = vis[f - 1] if f - 1 < len(vis) else None
        speaking = m is not None and (m["open"] > 0.03 or m["round"] > 0.03)
        apply_face(rig, e, f, m if speaking else None)
        k = env[f - 1] if f - 1 < len(env) else 0
        root.scale = (1 - 0.008 * k, 1 - 0.008 * k, 1 + 0.015 * k)          # EDIT: speech squash
        root.rotation_euler = (0, 0, math.radians(2.0) * math.sin(ts * 1.3))  # EDIT: gentle sway
        root.keyframe_insert("scale", frame=f)
        root.keyframe_insert("rotation_euler", frame=f)
    setup_render(size, samples)
    d = os.path.join(OUT, "frames_raw")
    os.makedirs(d, exist_ok=True)
    rng = {"A": (1, cut), "B": (cut + 1, nf)}.get(ONLY, (1, nf))
    sc.frame_start, sc.frame_end = rng
    sc.render.filepath = os.path.join(d, "f_####")
    t = time.time()
    bpy.ops.render.render(animation=True)
    dt = time.time() - t
    n = rng[1] - rng[0] + 1
    STATS["shot"] = {"frames": n, "size": list(size), "samples": samples, "total_s": round(dt, 1), "s_per_frame": round(dt / n, 2)}
    print(f"[blender_host] shot {n} frames in {dt:.1f} s ({dt / n:.2f} s/frame)", flush=True)


def main():
    t0 = time.time()
    reset()
    rig = build()
    STATS["build_s"] = round(time.time() - t0, 2)
    if MODE == "sheet":
        mode_sheet(rig)
    elif MODE == "shot":
        with open(os.path.join(OUT, "audio", "anim.json"), encoding="utf-8") as fh:
            mode_shot(rig, json.load(fh))
    if DEBUG:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"host_{MODE}.blend"))
    p = os.path.join(OUT, "blender.json")
    old = {}
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            old = json.load(fh)
    old.update({"version": STATS["version"], MODE: STATS})
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(old, fh, indent=2)


main()
