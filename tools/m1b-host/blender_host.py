"""M1b host v2 (quality pass) — builds Nani Koshika in Blender from host.json and renders the character sheet or the 5-s 9:16 shot.
Owner doc: studio-docs/build/studio-playbook.md §5b (host rules) · look: build/visual-style.md · target: handoff/m1b-host/quality-target.md
Spec: host.json (RULES I6; quality knobs under "quality"). Our own 3D model (no AI in the shot): same mesh + materials + seed + cloth sim
for every angle, so identity holds by construction.
Run through m1b.py, or:  blender -b -P blender_host.py -- --mode sheet|shot [--preview] [--only A|B|<tile>] [--debug] [--dry-run]
                          [--engine eevee|cycles] [--no-sim] [--strict] [--palette-pass] [--reduced-motion]
D5 guard rails built in: no organelles, no layers, no internal blobs, never divides; props are blank (no diagrams, pages blank);
hands are arms that leave the body (never separate pearl spheres — D5 R1). Every part is guarded: a failing part is logged to
out/build_log_<mode>.json and the render goes on (use --strict to stop on the first failure)."""
import hashlib, json, math, os, random, sys, time, traceback

import bpy
from mathutils import Vector, Quaternion

KIT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KIT, "out")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default


MODE = arg("--mode", "shot")
PREVIEW, DEBUG, DRY = "--preview" in argv, "--debug" in argv, "--dry-run" in argv
RM, PALPASS, NOSIM, STRICT = "--reduced-motion" in argv, "--palette-pass" in argv, "--no-sim" in argv, "--strict" in argv
ONLY = arg("--only")
ENGINE = arg("--engine", "eevee")
RES = arg("--res", "preview" if PREVIEW else "ship")  # design | ship | preview
SPEC = json.load(open(os.path.join(KIT, "host.json"), encoding="utf-8"))
H = SPEC["host"]
PAL = H["palette"]
V = SPEC["video"]
Q = SPEC.get("quality", {})
QS, QF, QA, QB, QP, QO = (Q.get(k, {}) for k in ("shawl", "face", "arms", "book", "plate", "outline"))
FPS = V["fps"]
NF = int(round(V["seconds"] * FPS))
random.seed(H["seed"])
LOG = {"parts": {}, "notes": []}


def dbg(*a):
    if DEBUG:
        print("[host]", *a, flush=True)


def guard(name, fn, *a, **k):
    """Run one build part; log and carry on if it fails (RULES §I debug hooks)."""
    t0 = time.time()
    try:
        r = fn(*a, **k)
        LOG["parts"][name] = f"ok {time.time() - t0:.1f} s"
        return r
    except Exception as e:
        print(f"[host] PART FAILED {name}: {e}\n{traceback.format_exc()}", flush=True)
        LOG["parts"][name] = f"FAILED: {type(e).__name__}: {e}"
        if STRICT:
            raise
        return None


def lin(hexs, a=1.0):
    """sRGB hex → linear RGBA for Blender colour sockets."""
    h = hexs.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c) + (a,)


def setin(node, names, val):
    for n in names if isinstance(names, (list, tuple)) else [names]:
        if n in node.inputs:
            node.inputs[n].default_value = val
            return True
    dbg("no input", names, "on", node.name)
    return False


def smooth(a, b, x):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


# ---------------- scene ----------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, NF
    w, h = {"design": V["design"], "ship": V["ship"], "preview": V["preview"]}[RES]
    if MODE == "sheet":
        w, h = (360, 450) if RES == "preview" else (1080, 1350)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard" if PALPASS else V.get("view_transform", "AgX")  # EDIT: AgX look; Standard for ΔE pass
    sc.view_settings.exposure = 0.0 if PALPASS else V.get("exposure", 0.0)  # EDIT: R2 −0.7 (body read blown)
    if not PALPASS and V.get("view_look"):  # EDIT: AgX desaturates brights; Punchy keeps the amber glow + wine (R3)
        try:
            sc.view_settings.look = V["view_look"]
        except TypeError as e:
            LOG["notes"].append(f"view look {V['view_look']} not available: {e}")
    if ENGINE == "cycles":
        sc.render.engine = "CYCLES"
        sc.cycles.samples = 16 if PREVIEW else V["cycles_samples"]
        sc.cycles.use_denoising = True
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for dev in ("OPTIX", "CUDA"):
                try:
                    prefs.compute_device_type = dev; prefs.get_devices()
                    for d in prefs.devices:
                        d.use = True
                    sc.cycles.device = "GPU"; break
                except TypeError:
                    continue
        except Exception as e:
            dbg("cycles GPU setup failed", e)
    else:
        for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                sc.render.engine = eng; break
            except TypeError:
                continue
        sc.eevee.taa_render_samples = 8 if PREVIEW else V["samples"]
        if QP.get("eevee_raytracing", True):  # EDIT: screen-space reflections/AO for the pearl and glasses
            try:
                sc.eevee.use_raytracing = True
            except Exception as e:
                dbg("raytracing off", e)
    return sc


# ---------------- materials ----------------
def mat(name, base, rough=0.5, sss=0.0, emit=None, emit_s=0.0, metal=0.0, coat=0.0, sheen=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes["Principled BSDF"]
    setin(bs, "Base Color", lin(base))
    setin(bs, "Roughness", rough)
    setin(bs, "Metallic", metal)
    if sss:
        setin(bs, ["Subsurface Weight", "Subsurface"], sss)
        setin(bs, "Subsurface Radius", (1.0, 0.85, 0.75))
        setin(bs, "Subsurface Scale", H["body"]["sss_radius"])
    if coat:
        setin(bs, ["Coat Weight", "Clearcoat"], coat)
    if sheen:
        setin(bs, ["Sheen Weight", "Sheen"], sheen)
    if emit:
        setin(bs, ["Emission Color", "Emission"], lin(emit))
        setin(bs, "Emission Strength", emit_s)
    return m


class NT:
    """Tiny node-graph helper."""

    def __init__(self, m):
        self.nt = m.node_tree; self.N = self.nt.nodes; self.bs = self.N["Principled BSDF"]

    def new(self, kind, **props):
        n = self.N.new(kind)
        for k, v in props.items():
            setattr(n, k, v)
        return n

    def link(self, a, b):
        self.nt.links.new(a, b)

    def math(self, op, a, b=None, clamp=False):
        n = self.new("ShaderNodeMath", operation=op, use_clamp=clamp)
        for i, x in enumerate((a, b)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = x
            else:
                self.link(x, n.inputs[i])
        return n.outputs[0]

    def maprange(self, val, fmin, fmax, tmin=0.0, tmax=1.0, smoothstep=True):
        n = self.new("ShaderNodeMapRange")
        if smoothstep:
            n.interpolation_type = "SMOOTHSTEP"
        n.inputs["From Min"].default_value, n.inputs["From Max"].default_value = fmin, fmax
        n.inputs["To Min"].default_value, n.inputs["To Max"].default_value = tmin, tmax
        self.link(val, n.inputs["Value"])
        return n.outputs["Result"]

    def mix(self, fac, a, b):
        n = self.new("ShaderNodeMix", data_type="RGBA")
        for sock, x in ((n.inputs[0], fac), (n.inputs[6], a), (n.inputs[7], b)):
            if isinstance(x, (tuple, float, int)):
                sock.default_value = x
            else:
                self.link(x, sock)
        return n.outputs[2]

    def coords(self, obj=None):
        tc = self.new("ShaderNodeTexCoord")
        if obj is not None:
            tc.object = obj
        return tc

    def sep(self, vec):
        s = self.new("ShaderNodeSeparateXYZ"); self.link(vec, s.inputs[0]); return s

    def bump(self, height, strength, distance=0.002):
        b = self.new("ShaderNodeBump"); b.inputs["Strength"].default_value = strength
        if "Distance" in b.inputs:
            b.inputs["Distance"].default_value = distance
        self.link(height, b.inputs["Height"]); self.link(b.outputs["Normal"], self.bs.inputs["Normal"])
        return b

    def noise(self, vec, scale, detail=4.0):
        n = self.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail
        self.link(vec, n.inputs["Vector"]); return n.outputs["Fac"]

    def image(self, path, vec, noncolor=False, box=False):
        if not os.path.exists(path):
            LOG["notes"].append(f"texture missing: {os.path.relpath(path, KIT)} (run `python m1b.py tex`)")
            return None
        im = bpy.data.images.load(path, check_existing=True)
        if noncolor:
            im.colorspace_settings.name = "Non-Color"
        n = self.new("ShaderNodeTexImage"); n.image = im
        if box:
            n.projection = "BOX"; n.projection_blend = 0.2
        self.link(vec, n.inputs["Vector"])
        return n


def body_mat(body):
    """Pearl: SSS + warm inner glow strongest low and where we look straight in, cheek blush, micro bump (target trait 1)."""
    m = mat("pearl", PAL["body"], QF.get("body_rough", 0.22), sss=0.65, emit=PAL["glow"], coat=0.55)
    g = NT(m); bs = g.bs
    setin(bs, "Subsurface Radius", (1.0, 0.62, 0.38)); setin(bs, "Coat Roughness", QF.get("coat_rough", 0.12))  # EDIT: warm jelly scatter
    tc = g.coords(body); s = g.sep(tc.outputs["Object"])
    low = g.maprange(s.outputs["Z"], -0.45, QF.get("glow_top", 0.18), 1.0, 0.0)  # EDIT: glow fades from the bottom to glow_top (R4: reach mid-body)
    lw = g.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
    facing = g.math("SUBTRACT", 1.0, lw.outputs["Facing"])
    gs = H["body"]["glow_strength"] * 1.2
    glow = g.math("MULTIPLY", g.math("MULTIPLY", low, facing), gs)
    QR = Q.get("rim", {})  # v7 (D-052): view-dependent rim glow. The inner glow above fades to 0 at the silhouette, so the
    if QR.get("on", True):  # body edge went dark against the dark plate (host-vs-plate gate, v6 p10 1.6–2.8:1). Works for every camera.
        rw = g.new("ShaderNodeLayerWeight"); rw.inputs["Blend"].default_value = QR.get("blend", 0.35)  # EDIT: rim width (higher = wider)
        rim = g.math("POWER", rw.outputs["Facing"], QR.get("power", 2.0))  # EDIT: falloff (higher = thinner line at the very edge)
        glow = g.math("ADD", glow, g.math("MULTIPLY", rim, QR.get("strength", 1.6)))  # EDIT: rim brightness (0 = v6 look)
    g.link(glow, bs.inputs["Emission Strength"])
    cx, cz, csig, _ = QF.get("cheeks", [0.15, -0.005, 0.07, 0.025])
    comb = g.new("ShaderNodeCombineXYZ")
    g.link(g.math("ABSOLUTE", s.outputs["X"]), comb.inputs["X"]); g.link(s.outputs["Z"], comb.inputs["Z"])
    sub = g.new("ShaderNodeVectorMath", operation="SUBTRACT"); sub.inputs[1].default_value = (cx + 0.01, 0.0, cz - 0.01)
    g.link(comb.outputs[0], sub.inputs[0])
    ln = g.new("ShaderNodeVectorMath", operation="LENGTH"); g.link(sub.outputs["Vector"], ln.inputs[0])
    bmask = g.math("MULTIPLY", g.maprange(ln.outputs["Value"], 0.0, 0.075, QF.get("blush", 0.8), 0.0), g.math("LESS_THAN", s.outputs["Y"], -0.15))
    mott = g.noise(tc.outputs["Object"], 9.0, 3.0)
    base = g.mix(g.maprange(mott, 0.3, 0.7, 0.0, 0.10), lin(PAL["body"]), lin(PAL["body_floor"]))  # very soft mottling
    g.link(g.mix(bmask, base, lin(PAL["blush"])), bs.inputs["Base Color"])
    g.bump(g.noise(tc.outputs["Object"], 220.0, 8.0), QF.get("micro_bump", 0.15), 0.002)  # EDIT: micro-texture
    return m


def lid_mat():
    m = mat("lid", PAL["body"], 0.32, sss=0.5, coat=0.25)
    g = NT(m); s = g.sep(g.coords().outputs["Object"])
    lash = g.maprange(s.outputs["Z"], 0.0, 0.17, 1.0, 0.0)
    g.link(g.mix(lash, lin(PAL["body"]), lin(PAL["ink"])), g.bs.inputs["Base Color"])
    return m


def eye_mat():
    """Sclera + warm-brown iris ring + pupil on one ball; rotating the ball = looking (target trait 2)."""
    m = mat("eye", PAL["sclera"], 0.12, coat=0.8)
    g = NT(m); s = g.sep(g.coords().outputs["Object"])
    xz = g.new("ShaderNodeCombineXYZ"); g.link(s.outputs["X"], xz.inputs["X"]); g.link(s.outputs["Z"], xz.inputs["Z"])
    ln = g.new("ShaderNodeVectorMath", operation="LENGTH"); g.link(xz.outputs[0], ln.inputs[0]); d = ln.outputs["Value"]
    front = g.math("LESS_THAN", s.outputs["Y"], -0.2)
    irn = QF.get("iris_r", 0.024) / QF.get("eye_r", 0.036); prn = irn * 0.45
    iris = g.math("MULTIPLY", g.maprange(d, irn - 0.03, irn + 0.03, 1.0, 0.0), front)
    pupil = g.math("MULTIPLY", g.maprange(d, prn - 0.025, prn + 0.025, 1.0, 0.0), front)
    ramp = g.new("ShaderNodeValToRGB"); el = ramp.color_ramp.elements
    el[0].position, el[0].color = 0.0, lin("#2A1508"); el[1].position, el[1].color = 1.0, lin(PAL["iris_rim"])
    for p_, c_ in ((0.45, "#7A4422"), (0.80, PAL["iris"])):
        e = el.new(p_); e.color = lin(c_)
    g.link(g.maprange(d, 0.0, irn, 0.0, 1.0, smoothstep=False), ramp.inputs["Fac"])
    c1 = g.mix(iris, lin(PAL["sclera"]), ramp.outputs["Color"])
    g.link(g.mix(pupil, c1, lin("#0C0705")), g.bs.inputs["Base Color"])
    return m


def shawl_mat():
    m = mat("shawl", PAL["shawl"], 0.92, sheen=QS.get("sheen", 0.3))
    g = NT(m); setin(g.bs, "Sheen Roughness", 0.6); setin(g.bs, ["Specular IOR Level", "Specular"], QS.get("spec", 0.1))  # EDIT: wool, not satin (R1 read salmon)
    tc = g.coords(); uv = tc.outputs["UV"]
    alb = g.image(os.path.join(OUT, "tex", "shawl_albedo.png"), uv)
    hgt = g.image(os.path.join(OUT, "tex", "shawl_height.png"), uv, noncolor=True)
    fuzz = g.noise(tc.outputs["Object"], 900.0, 2.0)
    if alb:
        g.link(alb.outputs["Color"], g.bs.inputs["Base Color"])
    else:
        g.link(g.mix(g.noise(tc.outputs["Object"], 60.0), lin(PAL["shawl"]), lin(PAL["shawl_dark"])), g.bs.inputs["Base Color"])
    h = g.math("ADD", hgt.outputs["Color"] if hgt else 0.5, g.math("MULTIPLY", fuzz, 0.35))
    g.bump(h, QS.get("bump", 0.35), 0.003)
    return m


def leather_mat():
    m = mat("book_cover", PAL["book_cover"], 0.55, coat=0.15)
    g = NT(m); tc = g.coords()
    alb = g.image(os.path.join(OUT, "tex", "leather_albedo.png"), tc.outputs["Generated"], box=True)
    hgt = g.image(os.path.join(OUT, "tex", "leather_height.png"), tc.outputs["Generated"], noncolor=True, box=True)
    if alb:
        g.link(alb.outputs["Color"], g.bs.inputs["Base Color"])
    g.bump(hgt.outputs["Color"] if hgt else g.noise(tc.outputs["Object"], 300.0), 0.4, 0.002)
    return m


def pages_mat():
    m = mat("book_pages", PAL["book_pages"], 0.85)  # blank pages, no lines (D5; G-Art R3 read the v2 bands as ruling)
    g = NT(m); tc = g.coords()
    g.link(g.mix(g.maprange(g.noise(tc.outputs["Object"], 25.0), 0.3, 0.7, 0.0, 0.10), lin(PAL["book_pages"]), lin("#C9B48E")), g.bs.inputs["Base Color"])
    return m


def lens_mat():
    m = mat("lens", "#FFFFFF", 0.04, coat=1.0)
    setin(m.node_tree.nodes["Principled BSDF"], "Alpha", 0.10)
    for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        try:
            setattr(m, attr, val)
        except Exception:
            pass
    return m


def attr_mat(name, rough=0.65):
    m = mat(name, "#808080", rough)
    g = NT(m); a = g.new("ShaderNodeAttribute"); a.attribute_name = "col"
    g.link(a.outputs["Color"], g.bs.inputs["Base Color"])
    return m


# ---------------- geometry helpers ----------------
HH = H["body"]["height"] / 2
RR = H["body"]["width"] / 2
TAPER = H["body"]["egg_taper"]
LOWB = H["body"].get("low_bias", 0.0)  # EDIT: >0 = plump egg, widest low (target trait 1)


def shape_k(zn):
    """Radius factor on top of the unit sphere: taper at the top, belly bulge low."""
    return (1 - TAPER * max(0.0, zn)) * (1 + LOWB * math.exp(-((zn + 0.35) / 0.38) ** 2))  # smooth belly bulge (R2: v2 had a kink)


def egg_r(zn):
    return RR * shape_k(zn) * math.sqrt(max(0.0, 1 - zn * zn))


def bumps(x, z):
    """Sculpt on the egg's front: nose bump + soft cheeks (radial fraction). EDIT via quality.face.nose/cheeks [x, z, sigma, amp]."""
    nx, nz, ns, na = QF.get("nose", [0.0, 0.045, 0.028, 0.030])
    cx, cz, cs, ca = QF.get("cheeks", [0.15, -0.005, 0.07, 0.025])
    s = na * math.exp(-((x - nx) ** 2 + (z - nz) ** 2) / ns ** 2)
    for sx in (-1, 1):
        s += ca * math.exp(-((x - sx * cx) ** 2 + (z - cz) ** 2) / cs ** 2)
    return s


def front_w(x, y):
    r = math.hypot(x, y)
    return smooth(0.2, 0.7, -y / r) if r > 1e-6 else 0.0


def surf_pt(x, z):
    """Point on the sculpted front surface at (x, z)."""
    xp, s, y0 = x, 1.0, 0.0
    for _ in range(4):
        r0 = egg_r(z / HH); y0 = -math.sqrt(max(r0 * r0 - xp * xp, 1e-9))
        s = 1 + front_w(xp, y0) * bumps(xp, z); xp = x / s
    return Vector((x, y0 * s, z))


def surf(x, z, off=0.0):
    """(point + off·normal, outward normal, quaternion turning −Y onto the normal)."""
    e = 0.002
    tx = surf_pt(x + e, z) - surf_pt(x - e, z); tz = surf_pt(x, z + e) - surf_pt(x, z - e)
    n = tx.cross(tz).normalized()
    if n.y > 0:
        n = -n
    return surf_pt(x, z) + n * off, n, Vector((0, -1, 0)).rotation_difference(n)


def link(o, parent=None):
    bpy.context.scene.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def mesh_obj(name, verts, faces, m=None, parent=None, smooth_=True, uv=None):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], faces); me.update()
    if uv is not None:
        ul = me.uv_layers.new(name="UV")
        for li, lp in enumerate(me.loops):
            ul.data[li].uv = uv[lp.vertex_index]
    if smooth_:
        try:
            me.shade_smooth()
        except AttributeError:
            for p in me.polygons:
                p.use_smooth = True
    o = link(bpy.data.objects.new(name, me), parent)
    if m:
        o.data.materials.append(m)
    return o


def sphere(name, loc, scale, m, parent, seg=32, quat=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=1.0, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    if quat is not None:
        o.rotation_mode = "QUATERNION"; o.rotation_quaternion = quat
    bpy.ops.object.shade_smooth(); o.data.materials.append(m)
    o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), parent=None):
    e = link(bpy.data.objects.new(name, None), parent); e.location = loc
    return e


def curve_obj(name, pts, bevel, m, parent=None, radii=None, cyclic=False, kind="BEZIER", extrude=0.0, caps=True):
    cd = bpy.data.curves.new(name, "CURVE"); cd.dimensions = "3D"; cd.bevel_depth = bevel; cd.bevel_resolution = 3
    cd.extrude = extrude
    try:
        cd.use_fill_caps = caps
    except AttributeError:
        pass
    if kind == "BEZIER":
        sp = cd.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
        for i, p in enumerate(pts):
            bp = sp.bezier_points[i]; bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
            if radii:
                bp.radius = radii[i]
    else:
        sp = cd.splines.new("POLY"); sp.points.add(len(pts) - 1)
        for i, p in enumerate(pts):
            sp.points[i].co = (*p, 1)
            if radii:
                sp.points[i].radius = radii[i]
    sp.use_cyclic_u = cyclic
    o = link(bpy.data.objects.new(name, cd), parent)
    if m:
        o.data.materials.append(m)
    return o


def box_geo(origin, ax, ay, az, verts, faces):
    """Append a parallelepiped (origin + edge vectors) to verts/faces."""
    b = len(verts); o = Vector(origin)
    for k in range(8):
        verts.append(o + (ax if k & 1 else Vector()) + (ay if k & 2 else Vector()) + (az if k & 4 else Vector()))
    for f in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)):
        faces.append(tuple(b + i for i in f))


def catmull(pts, n):
    P = [Vector(p) for p in pts]; P = [P[0] + (P[0] - P[1])] + P + [P[-1] + (P[-1] - P[-2])]
    out = []
    for i in range(1, len(P) - 2):
        for k in range(n):
            t = k / n; p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(Vector(pts[-1]))
    return out


def tube(name, path, radii, m, parent, seg=16):
    verts, faces = [], []
    up = Vector((0, 0, 1))
    for i, p in enumerate(path):
        t = (path[min(i + 1, len(path) - 1)] - path[max(i - 1, 0)]).normalized()
        a = t.cross(up)
        a = a.normalized() if a.length > 1e-4 else Vector((1, 0, 0))
        b = t.cross(a).normalized()
        for k in range(seg):
            th = 2 * math.pi * k / seg
            verts.append(p + (a * math.cos(th) + b * math.sin(th)) * radii[i])
    for i in range(len(path) - 1):
        for k in range(seg):
            k2 = (k + 1) % seg
            faces.append((i * seg + k, i * seg + k2, (i + 1) * seg + k2, (i + 1) * seg + k))
    for end, sgn in ((0, -1), (len(path) - 1, 1)):  # domed caps (watertight for the cloth collider)
        t = (path[min(end + 1, len(path) - 1)] - path[max(end - 1, 0)]).normalized()
        c = len(verts); verts.append(path[end] + t * sgn * radii[end] * 0.8)
        for k in range(seg):
            k2 = (k + 1) % seg
            faces.append((c, end * seg + k2, end * seg + k) if sgn > 0 else (c, end * seg + k, end * seg + k2))
    return mesh_obj(name, verts, faces, m, parent)


# ---------------- build ----------------
M = {}
P = {}


def build_materials(body):
    M["body"] = body_mat(body)
    M["lid"] = lid_mat(); M["eye"] = eye_mat()
    M["ink"] = mat("ink", PAL["ink"], 0.25, coat=0.6)
    M["brow"] = mat("brow", PAL["brow"], 0.7)
    M["crease"] = mat("crease", PAL["crease"], 0.5, sss=0.3)
    M["lip"] = mat("lip", PAL["lip"], 0.45)
    M["hi"] = mat("eye_hi", "#FFFFFF", 0.1, emit="#FFFFFF", emit_s=6.0)
    M["mouth"] = mat("mouth_in", "#2A0F14", 0.6)
    M["wire"] = mat("glasses", PAL["glasses"], 0.22, metal=1.0)
    M["gold"] = mat("gold", PAL["corner_gold"], 0.30, metal=1.0)
    M["lens"] = lens_mat()
    M["shawl"] = shawl_mat()
    M["fringe"] = mat("fringe", PAL["shawl"], 0.95, sheen=0.25)
    M["cover"] = leather_mat(); M["pages"] = pages_mat()
    M["ribbon"] = mat("ribbon", PAL["ribbon"], 0.45, sheen=0.4)
    M["bokeh"] = mat("bokeh", PAL["lamp"], 0.5, emit=PAL["lamp"], emit_s=QP.get("bokeh_emit", 5.0))  # EDIT: dimmer (owner, 21 Nov)
    M["bulb"] = mat("bulb", "#FFF2DC", 0.3, emit="#FFE2B0", emit_s=30.0)
    M["shade"] = mat("lamp_shade", PAL["lamp_shade"], 0.7, emit=PAL["lamp"], emit_s=QP.get("shade_emit", 3.5))  # EDIT: R4 shade clipped white
    M["brass"] = mat("brass", "#6B5230", 0.35, metal=1.0)
    M["lib"] = attr_mat("library")
    M["floor"] = mat("floor", PAL["wood"], 0.85)


def build_body(rig):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=1.0)
    b = bpy.context.object; b.name = "body"
    for v in b.data.vertices:
        zn = v.co.z
        s = RR * shape_k(zn)
        x, y, z = v.co.x * s, v.co.y * s, zn * HH
        k = 1 + front_w(x, y) * bumps(x, z)
        v.co = Vector((x * k, y * k, z))
    bpy.ops.object.shade_smooth(); b.parent = rig
    P["body"] = b
    return b


def outline_mat():
    """Ink line for the inverted-hull outline: shows only the hull's far side (the silhouette edge), transparent elsewhere.
    Works in Eevee and Cycles (Backfacing → transparent)."""
    m = bpy.data.materials.new("outline"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    geo = nt.nodes.new("ShaderNodeNewGeometry"); mx = nt.nodes.new("ShaderNodeMixShader")
    em.inputs["Color"].default_value = lin(QO.get("color", PAL["ink2"])); em.inputs["Strength"].default_value = QO.get("strength", 1.0)
    nt.links.new(geo.outputs["Backfacing"], mx.inputs["Fac"]); nt.links.new(em.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], o.inputs["Surface"])
    for k, v in (("use_backface_culling", True), ("surface_render_method", "DITHERED"), ("blend_method", "HASHED")):
        try:
            setattr(m, k, v)
        except (AttributeError, TypeError):
            pass
    return m


def add_outline(body):
    """G-A11y figure/ground (D-051): thin ink inverted hull on the pearl body so it stands off a light plate (lamp shade)
    as well as a dark one. Knobs: host.json → quality.outline {on, mm, color, strength}."""
    if not QO.get("on", False):
        return
    body.data.materials.append(outline_mat())
    so = body.modifiers.new("outline", "SOLIDIFY")
    so.thickness = -QO.get("mm", 4) / 1000.0; so.offset = 1.0; so.use_flip_normals = True; so.material_offset = 1
    so.use_rim = False


def build_face(rig):
    ex, ez, er = QF.get("eye_x", 0.105), QF.get("eye_z", 0.11), QF.get("eye_r", 0.036)
    for side, sx in (("L", -1), ("R", 1)):
        p, n, q = surf(sx * ex, ez, -0.010)  # EDIT: eye sunk 1 cm → ~1.7 cm proud of the face
        grp = empty("eye" + side, p, rig); grp.rotation_mode = "QUATERNION"; grp.rotation_quaternion = q
        ball = sphere("eyeball" + side, (0, 0, 0), (er, er * 0.75, er * 1.1), M["eye"], grp, 48)
        ball.rotation_mode = "XYZ"
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0)
        lid = bpy.context.object; lid.name = "lid" + side
        import bmesh
        bm = bmesh.new(); bm.from_mesh(lid.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.001], context="VERTS"); bm.to_mesh(lid.data); bm.free()
        lid.scale = (er * 1.10, er * 0.75 * 1.16, er * 1.1 * 1.10); bpy.ops.object.shade_smooth(); lid.data.materials.append(M["lid"])
        lid.parent = grp
        fy = -er * 0.75 - 0.0045
        h1 = sphere("hiA" + side, (-0.011, fy, 0.013), (0.0075,) * 3, M["hi"], grp, 12)
        h2 = sphere("hiB" + side, (0.009, fy + 0.002, -0.009), (0.0035,) * 3, M["hi"], grp, 10)
        P.update({"eye" + side: grp, "ball" + side: ball, "lid" + side: lid, "hiA" + side: h1, "hiB" + side: h2})
        # brow: thin tapered grey-brown arch on the surface
        bz = ez + 0.068; c, _, _ = surf(sx * ex, bz, 0.003)
        pts = [surf(sx * ex + dx, bz + dz, 0.003)[0] - c for dx, dz in ((-0.040, -0.004), (-0.013, 0.006), (0.013, 0.006), (0.040, -0.006))]
        if sx < 0:
            pts = pts[::-1]
        br = curve_obj("brow" + side, pts, QF.get("brow_w", 0.0068), M["brow"], rig, radii=[0.3, 1.0, 0.9, 0.3])
        br.location = c; P["brow" + side] = br; P["brow_z" + side] = c.z
        # smile creases at the outer eye corner + a soft under-eye line
        for k, (dx, dz) in enumerate(((0.050, 0.004), (0.052, -0.012))):
            a = [surf(sx * (ex + dx), ez + dz, 0.0012)[0], surf(sx * (ex + dx + 0.016), ez + dz - 0.006 * (1 + k), 0.0012)[0]]
            curve_obj(f"crease{side}{k}", a + [a[1] + (a[1] - a[0]) * 0.01], 0.0015, M["crease"], rig, radii=[0.4, 1.0, 0.3])
        ue = [surf(sx * (ex + dx), ez - 0.046 + 0.004 * math.cos(dx * 60), 0.0012)[0] for dx in (-0.018, 0.0, 0.018)]
        curve_obj("undereye" + side, ue, 0.0013, M["crease"], rig, radii=[0.3, 1.0, 0.3])
    # mouth: closed smile line with corners + dark interior for visemes
    mz = -0.03; c, n, q = surf(0, mz, 0.0015)
    xs = (-0.050, -0.025, 0.0, 0.025, 0.050)
    pts = [surf(x, mz, 0.0015)[0] - c for x in xs]
    lip = curve_obj("lip", pts, 0.0042, M["lip"], rig, radii=[0.45, 0.9, 1.0, 0.9, 0.45])
    lip.location = c; P["lip"] = lip; P["lip_base"] = [Vector(p) for p in pts]
    for sx in (-1, 1):
        a = [surf(sx * 0.056, mz + 0.004, 0.0012)[0], surf(sx * 0.064, mz + 0.010, 0.0012)[0], surf(sx * 0.062, mz + 0.016, 0.0012)[0]]
        curve_obj("dimple" + str(sx), a, 0.0014, M["crease"], rig, radii=[0.8, 0.6, 0.2])
    mp, mn, mq = surf(0, mz - 0.012, 0.002)
    P["mouth"] = sphere("mouth", mp, (0.042, 0.004, 0.002), M["mouth"], rig, 24, quat=mq)


def build_glasses(rig):
    ex, ez = QF.get("eye_x", 0.105), QF.get("eye_z", 0.11)
    gz, rx, rz, wr = QF.get("glasses_z", 0.068), QF.get("glasses_rx", 0.075), QF.get("glasses_rz", 0.05), QF.get("wire_r", 0.0032)
    ry = min(surf(ex, gz)[0].y, surf(ex, ez)[0].y) - 0.030   # EDIT: lens plane just in front of the eyes, low on the nose
    for side, sx in (("L", -1), ("R", 1)):
        g = empty("glass" + side, (sx * ex, ry, gz), rig); g.rotation_euler = (0, 0, sx * math.radians(10))  # slight wrap
        ring = [(rx * math.cos(t), 0.0, rz * math.sin(t)) for t in (2 * math.pi * k / 48 for k in range(48))]
        curve_obj("rim" + side, ring, wr, M["wire"], g, kind="POLY", cyclic=True)
        if QF.get("lens_glass", True):
            verts = [Vector((0, 0.001, 0))] + [Vector((rx * math.cos(t), 0.001, rz * math.sin(t))) for t in (2 * math.pi * k / 40 for k in range(40))]
            mesh_obj("lens" + side, verts, [(0, 1 + k, 1 + (k + 1) % 40) for k in range(40)], M["lens"], g)
        # temple: from the outer rim, back along the head (just off the surface) to behind the "ear"
        zt = gz + 0.018; r = egg_r(zt / HH) + QF.get("temple_gap", 0.007)  # EDIT: R4 hug the head (arms read as lines off the silhouette)
        start = Vector((sx * (ex + rx * math.cos(math.radians(10))), ry + rx * math.sin(math.radians(10)), gz + 0.008))  # outer rim point
        pa = math.degrees(math.asin(min(0.98, (ex + rx + 0.02) / r)))
        pts = [start, start + Vector((sx * 0.012, 0.012, 0.004))]
        for k in range(10):
            ph = math.radians(pa + (100 - pa) * k / 9)
            pts.append(Vector((sx * r * math.sin(ph), -r * math.cos(ph), zt)))
        curve_obj("temple" + side, pts, wr * 0.9, M["wire"], rig)
        if QF.get("chain", True):  # hanging chain: rim bottom-outer → behind the ear, sagging (catenary-ish), kept off the body
            A = Vector((sx * (ex + rx * 0.92), ry + rx * 0.18, gz - rz * 0.45))
            bz_ = QF.get("chain_end_z", -0.06); B = surf(sx * (ex + rx + 0.045), bz_, 0.02)[0]  # EDIT: chain ends on the shawl front
            sag = QF.get("chain_sag", 0.03); ch = []
            for k in range(24):
                t = k / 23; p_ = A.lerp(B, t) + Vector((0, 0, -sag * 4 * t * (1 - t)))
                rr = math.hypot(p_.x, p_.y); need = egg_r(max(-0.99, min(0.99, p_.z / HH))) * (1 + 0.04) + 0.01
                if rr < need and rr > 1e-6:
                    p_.x, p_.y = p_.x * need / rr, p_.y * need / rr
                ch.append(p_)
            curve_obj("chain" + side, ch, 0.0013, M["wire"], rig, kind="POLY")
    # bridge arching over the nose
    nb = surf(0, gz + 0.012)[0]
    yi = ry - rx * math.sin(math.radians(10))  # inner rim points sit forward (wrap)
    A = Vector((-ex + rx * 0.97, yi, gz + 0.010)); B = Vector((ex - rx * 0.97, yi, gz + 0.010))
    curve_obj("bridge", [A, Vector((0, min(nb.y - 0.004, ry + 0.012), gz + 0.022)), B], wr, M["wire"], rig)


def page_block(name, sx, hw, h, t, curl, m, parent):
    """Open page block on one half: thin at the gutter, rising, top curved (blank — D5)."""
    n = 24; verts, faces = [], []
    for i in range(n + 1):
        u = i / n; x = sx * (0.004 + u * (hw - 0.010))
        top = -(t * (0.35 + 0.65 * smooth(0.0, 0.35, u)) + curl * math.sin(math.pi * min(1.0, u * 1.1)) * (1 - 0.3 * u))
        for (y, z) in ((0.0, -h / 2), (0.0, h / 2), (top, h / 2), (top, -h / 2)):
            verts.append((x, y, z))
    for i in range(n):
        a, b = i * 4, (i + 1) * 4
        for k in range(4):
            k2 = (k + 1) % 4
            faces.append((a + k, a + k2, b + k2, b + k) if sx > 0 else (a + k, b + k, b + k2, a + k2))
    faces.append((0, 1, 2, 3)); faces.append((n * 4 + 3, n * 4 + 2, n * 4 + 1, n * 4))
    o = mesh_obj(name, verts, faces, m, parent, smooth_=False)
    return o


def build_book(rig):
    hw, h, t, curl = QB.get("half_w", 0.155), QB.get("h", 0.215), QB.get("pages_t", 0.02), QB.get("curl", 0.012)
    bz = QB.get("z", -0.22)  # EDIT: book height (centre of the spine)
    spine = empty("book_spine", (0, surf_pt(0, bz).y - QB.get("forward", 0.10), bz), rig)
    spine.rotation_euler = (math.radians(QB.get("tilt_deg", -35)), 0, math.pi if QB.get("flip") else 0.0)  # EDIT: flip + −30 = pages toward her, cover to camera (R3)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.014, depth=h, location=(0, 0.006, 0))
    sp = bpy.context.object; sp.name = "book_spine_leather"; sp.data.materials.append(M["cover"]); sp.parent = spine
    for side, sx in (("L", -1), ("R", 1)):
        hinge = empty("book_half" + side, (0, 0, 0), spine)
        verts, faces = [], []
        box_geo((min(0, sx * hw), 0.0, -h / 2), Vector((hw, 0, 0)), Vector((0, 0.007, 0)), Vector((0, 0, h)), verts, faces)
        cv = mesh_obj("book_cover" + side, verts, faces, M["cover"], hinge, smooth_=False)
        bv = cv.modifiers.new("bevel", "BEVEL"); bv.width = 0.0025; bv.segments = 2
        page_block("book_pages" + side, sx, hw - 0.010, h - QB.get("overhang", 0.026), t, curl, M["pages"], hinge)
        for zs in (-1, 1):  # gold corners wrapping the outer corners
            cx, cz, L = sx * (hw + 0.0015), zs * (h / 2 + 0.0015), 0.030
            tri = [(cx, cz), (cx - sx * L, cz), (cx, cz - zs * L)]
            vv = [(x, y, z) for y in (-0.0015, 0.0085) for (x, z) in tri]
            ff = [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
            mesh_obj(f"book_corner{side}{zs}", vv, ff, M["gold"], hinge, smooth_=False)
        P["book" + side] = hinge
        P["hand_tgt" + side] = empty("hand_tgt" + side, (sx * (hw - 0.030), -(t + 0.030), h / 2 - 0.050), hinge)  # EDIT: hands on the outer top corners
    rib = [(0.0, -0.010, h / 2 - 0.01), (0.0, -0.006, -h / 2 + 0.01), (0.002, 0.020, -h / 2 - 0.004), (0.004, 0.026, -h / 2 - QB.get("ribbon_tail", 0.10) * 0.5), (0.006, 0.030, -h / 2 - QB.get("ribbon_tail", 0.10))]  # EDIT: R4 tail length  # gutter → out under the spine, hanging on the cover side
    curve_obj("ribbon", rib, 0.0, M["ribbon"], spine, extrude=0.007, caps=False)
    for side, sx in (("L", -1), ("R", 1)):
        P["book" + side].rotation_euler = (0, 0, sx * math.radians(QB.get("open_deg", -20)))
    P["spine"] = spine
    bpy.context.view_layer.update()
    if P["hand_tgtL"].matrix_world.translation.x > 0:  # flipped book: the left hand takes the half that is now on the left
        P["hand_tgtL"], P["hand_tgtR"] = P["hand_tgtR"], P["hand_tgtL"]


ARM_OBST = []


def build_arms(rig):
    """Soft pearl arms from under the shawl edge to rounded hands resting on the book (D5 R1: arms, never loose spheres)."""
    bpy.context.view_layer.update()
    phi, rz = math.radians(QA.get("root_phi_deg", 52)), QA.get("root_z", -0.13)
    r0, r1 = QA.get("radius", [0.034, 0.03]); hs = QA.get("hand", [0.05, 0.042, 0.034])
    for side, sx in (("L", -1), ("R", 1)):
        tgt = P.get("hand_tgt" + side)
        Hp = tgt.matrix_world.translation.copy() if tgt else Vector((sx * 0.14, -0.50, -0.20))
        rb = egg_r(rz / HH); radial = Vector((sx * math.sin(phi), -math.cos(phi), 0))
        P0 = radial * (rb - 0.035) + Vector((0, 0, rz))
        P1 = radial * (rb + 0.03) + Vector((0, -0.02, rz - 0.035))
        P2 = P1.lerp(Hp, 0.5) + Vector((0, 0, -0.035)) + radial * 0.02
        d = (Hp - P2).normalized(); P3 = Hp - d * 0.028
        path = catmull([P0, P1, P2, P3], 8)
        radii = [r0 + (r1 - r0) * i / (len(path) - 1) for i in range(len(path))]
        arm = tube("arm" + side, path, radii, M["body"], rig)
        hand = sphere("hand" + side, Hp, tuple(hs), M["body"], rig, 32, quat=d.to_track_quat("X", "Z"))
        P["arm" + side], P["hand" + side] = arm, hand
        ARM_OBST.extend([(p, rr + 0.004) for p, rr in zip(path, radii)] + [(Hp, max(hs) + 0.004)])


def hook_arms():
    """After the cloth sim: hands follow the book halves (book snap), arm ends bend with them."""
    bpy.context.view_layer.update()
    for side in ("L", "R"):
        arm, hand, tgt = P.get("arm" + side), P.get("hand" + side), P.get("hand_tgt" + side)
        if not (arm and hand and tgt):
            continue
        mw = hand.matrix_world.copy(); hand.parent = tgt; hand.matrix_world = mw
        hk = arm.modifiers.new("follow_book", "HOOK"); hk.object = tgt
        hk.vertex_indices_set(list(range(len(arm.data.vertices))))
        hk.center = arm.matrix_world.inverted() @ tgt.matrix_world.translation
        hk.falloff_type = "SMOOTH"; hk.falloff_radius = 0.24  # EDIT: how much of the forearm bends with the hand
        hk.matrix_inverse = tgt.matrix_world.inverted() @ arm.matrix_world


def shawl_key():
    blob = json.dumps([QS, QA, QB, QF.get("nose"), QF.get("cheeks"), H["body"], "simv2"], sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:12]


def build_shawl(rig, body):
    """Cloth sim (headless): pinned along a shoulder line wrapped round the back, falls onto body + arms, frozen to mesh (trait 4)."""
    NU, NV = QS.get("nu", 128), QS.get("nv", 36)
    ph0 = QS.get("phi_open_deg", 30); zf, zb, zh = QS.get("z_front", -0.09), QS.get("z_back", 0.20), QS.get("z_hem", -0.36)
    gap, flare, folds, famp = QS.get("gap", 0.025), QS.get("flare", 0.04), QS.get("folds", 7), QS.get("fold_amp", 0.018)
    rng = random.Random(H["seed"] + 11); ph_off = rng.uniform(0, 6.28)
    verts, uv = [], []
    for j in range(NV + 1):
        t = j / NV
        for i in range(NU + 1):
            u = i / NU
            phs = math.radians(-ph0 - u * (360 - 2 * ph0)); c = math.cos(phs)
            ztop = zf + (zb - zf) * (1 - c) / 2
            z = ztop + (zh - ztop) * t
            if j == 0:
                r = egg_r(max(-0.99, min(0.99, z / HH))) + 0.018  # pinned shoulder line, just clear of the collider
            else:
                zs = [z + (ztop - z) * k / 8 for k in range(9)]
                r = max(egg_r(max(-0.99, min(0.99, zz / HH))) for zz in zs) + gap + flare * t + famp * t * math.sin(2 * math.pi * folds * u + ph_off)
            dirv = Vector((math.sin(phs), -math.cos(phs), 0))
            if j > 0:  # tent over the arms: start outside them (ray–sphere, analytic), then the sim lets it fall onto them
                for c_, cr in ARM_OBST:
                    a_ = dirv.x * c_.x + dirv.y * c_.y
                    d2 = c_.x * c_.x + c_.y * c_.y - a_ * a_ + (c_.z - z) ** 2; R2 = (cr + 0.02) ** 2
                    if a_ > 0 and d2 < R2:
                        r = max(r, a_ + math.sqrt(R2 - d2) + 0.014)
            p = dirv * r + Vector((0, 0, z))
            verts.append(p); uv.append((u, 1 - t))
    faces = [(j * (NU + 1) + i, j * (NU + 1) + i + 1, (j + 1) * (NU + 1) + i + 1, (j + 1) * (NU + 1) + i) for j in range(NV) for i in range(NU)]
    sh = mesh_obj("shawl", verts, faces, None, rig, uv=uv)
    vg = sh.vertex_groups.new(name="pin")
    vg.add(list(range(NU + 1)), 1.0, "REPLACE"); vg.add(list(range(NU + 1, 2 * (NU + 1))), 0.45, "REPLACE")
    n = len(sh.data.vertices); key = shawl_key(); cache = os.path.join(OUT, "cache", f"shawl_{key}.json")
    state = "procedural (no sim)"
    if QS.get("sim", True) and not NOSIM:
        if os.path.exists(cache):
            co = json.load(open(cache))
            if len(co) == n * 3:
                sh.data.vertices.foreach_set("co", co); sh.data.update(); state = f"cache {key}"
        if not state.startswith("cache"):
            state = simulate(sh, [body] + [P[k] for k in ("armL", "armR", "handL", "handR") if P.get(k)], n)
            if state.startswith("sim ok"):
                co = [0.0] * (n * 3); sh.data.vertices.foreach_get("co", co)
                os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump([round(x, 5) for x in co], open(cache, "w"))
    LOG["shawl"] = state; print("[host] shawl:", state, flush=True)
    sh.data.materials.append(M["shawl"])
    so = sh.modifiers.new("thick", "SOLIDIFY"); so.thickness = QS.get("thickness", 0.012); so.offset = 0.0
    sub = sh.modifiers.new("soft", "SUBSURF"); sub.levels = 1; sub.render_levels = 2
    P["shawl"] = sh
    guard("fringe", build_fringe, sh, NU, NV, rig)


def simulate(sh, colliders, n):
    sc = bpy.context.scene; frames = QS.get("sim_frames", 70)
    cols = []
    for o in colliders:
        md = o.modifiers.new("collision", "COLLISION"); cols.append((o, md))
        o.collision.thickness_outer = 0.006
        try:
            o.collision.cloth_friction = 5.0
        except AttributeError:
            pass
    cl = sh.modifiers.new("cloth", "CLOTH"); s = cl.settings
    s.quality = QS.get("quality", 6); s.mass = QS.get("mass", 0.3)
    s.tension_stiffness = s.compression_stiffness = QS.get("tension", 15); s.shear_stiffness = 5
    s.bending_stiffness = QS.get("bending", 0.4); s.air_damping = QS.get("air", 1.0)
    s.vertex_group_mass = "pin"; s.pin_stiffness = 1.0
    try:
        s.shrink_min = QS.get("shrink", 0.0)  # EDIT: >0 pulls the wool in so it hugs the body (R3: v3 hung like a cape)
    except AttributeError:
        pass
    cs = cl.collision_settings; cs.use_collision = True; cs.distance_min = 0.008; cs.use_self_collision = False
    try:
        cs.collision_quality = 3
    except AttributeError:
        pass
    cl.point_cache.frame_start, cl.point_cache.frame_end = 1, frames
    old_end = sc.frame_end; sc.frame_end = max(sc.frame_end, frames)
    t0 = time.time()
    for f in range(1, frames + 1):
        sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(sh.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    co = [0.0] * (n * 3); me.vertices.foreach_get("co", co)
    sh.modifiers.remove(cl)
    for o, md in cols:
        o.modifiers.remove(md)
    sc.frame_end = old_end; sc.frame_set(1)
    bad = any(not math.isfinite(x) or abs(x) > 2.5 for x in co)
    if bad or len(me.vertices) != n:
        bpy.data.meshes.remove(me)
        return "sim FAILED (exploded or topology changed) → procedural fallback"
    sh.data.vertices.foreach_set("co", co); sh.data.update(); bpy.data.meshes.remove(me)
    return f"sim ok {frames} frames {time.time() - t0:.1f} s"


def build_fringe(sh, NU, NV, rig):
    """Long twisted fringe from the hem vertices (two plied strands each)."""
    co = [v.co.copy() for v in sh.data.vertices]
    rng = random.Random(H["seed"] + 23); L0, L1 = QS.get("fringe_len", [0.07, 0.09]); rr = QS.get("fringe_r", 0.0016)
    cd = bpy.data.curves.new("fringe", "CURVE"); cd.dimensions = "3D"; cd.bevel_depth = rr; cd.bevel_resolution = 1
    every = max(1, QS.get("fringe_every", 1))
    for i in range(0, NU + 1, every):
        b = co[NV * (NU + 1) + i]; up = co[(NV - 1) * (NU + 1) + i]
        dc = (b - up).normalized(); d = (dc * 0.35 + Vector((0, 0, -1))).normalized()
        rad = Vector((b.x, b.y, 0)).normalized(); e1 = (rad - d * rad.dot(d)).normalized(); e2 = d.cross(e1)
        L = rng.uniform(L0, L1); sway = rng.uniform(-0.006, 0.006); turns = rng.uniform(2.0, 3.0)
        start = b - dc * 0.004
        for ply in (0.0, math.pi):
            sp = cd.splines.new("POLY"); sp.points.add(11)
            for k in range(12):
                t = k / 11; a = start + d * L * t
                w = 2 * math.pi * turns * t + ply
                p = a + (e1 * math.cos(w) + e2 * math.sin(w)) * rr * 1.1 * (1 - 0.25 * t) + e1 * sway * t * t
                sp.points[k].co = (p.x, p.y, p.z, 1)
    fr = link(bpy.data.objects.new("fringe", cd), rig); fr.data.materials.append(M["fringe"])
    P["fringe"] = fr


# ---------------- plate: studio (sheet) or library (shot) ----------------
SHEET_TILES = [("front", 0, 0, 3.4, 70, "warm"), ("side", 90, 0, 3.4, 70, "warm")] + \
    [(e, -15, 3, 2.6, 85, e) for e in SPEC["expressions"]]  # EDIT: tile list (name, yaw, pitch, dist, lens, expr)


def cam_pose(shot, d=None):
    """Camera location + frame axes for a shot dict (same maths as the camera itself)."""
    d = shot["dist"] if d is None else d
    lens = shot["lens_mm"]; ext = 2 * d * (18.0 / lens)
    off = (SPEC.get("face_at_pct", 38) / 100 - 0.5)
    yaw, pit = math.radians(shot["cam_yaw_deg"]), math.radians(shot["cam_pitch_deg"])
    tgt = Vector((0, -0.22, QF.get("eye_z", 0.11) + off * ext))
    loc = tgt + d * Vector((math.sin(yaw) * math.cos(pit), -math.cos(yaw) * math.cos(pit), math.sin(pit)))
    fwd = (tgt - loc).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd)
    sc = bpy.context.scene; asp = sc.render.resolution_x / sc.render.resolution_y
    th = 18.0 / lens if asp <= 1 else 18.0 / lens / asp
    return tgt, loc, fwd, right, up, th * asp, th


def at_screen(shot, fx, fy, depth):
    _, loc, fwd, right, up, tw, th = cam_pose(shot)
    return loc + fwd * depth + right * (fx * depth * tw) + up * (fy * depth * th), loc


def world_gradient(top, bottom, strength=1.0):
    w = bpy.data.worlds.new("plate"); bpy.context.scene.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = lin(bottom); ramp.color_ramp.elements[1].color = lin(top)
    nt.links.new(tc.outputs["Window"], sep.inputs[0]); nt.links.new(sep.outputs["Y"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = strength


def floor(m, size=14.0):
    s = size / 2
    mesh_obj("floor", [(-s, -s, -0.505), (s, -s, -0.505), (s, s, -0.505), (-s, s, -0.505)], [(0, 1, 2, 3)], m, None, smooth_=False)


def build_library():
    """Procedural shelves of book spines round the back (heavily defocused), one mesh, colour per book (trait 7)."""
    rng = random.Random(H["seed"] + 31)
    R = QP.get("shelf_radius", 3.6); a0, a1 = QP.get("shelf_deg", [-78, 78]); z0, z1 = QP.get("shelf_z", [-1.4, 2.0]); dz = QP.get("shelf_step", 0.4)
    spines = ["#3A1E1A", "#2E2A1C", "#1F2A24", "#2A2030", "#3A2A18", "#1E2430", "#40261E", "#2C1C14", "#4A2C20", "#233026"]  # EDIT: dark, muted
    wood = lin(PAL["wood"])
    verts, faces, cols = [], [], []

    def add(o, ax, ay, az, col):
        n0 = len(verts); box_geo(o, ax, ay, az, verts, faces); cols.extend([col] * (len(verts) - n0))
    step = 9.0; th = a0
    while th <= a1 + 1e-6:
        t = math.radians(th); C = Vector((R * math.sin(t), R * math.cos(t), 0)); nrm = -C.normalized(); tan = Vector((math.cos(t), -math.sin(t), 0))
        uw = 2 * R * math.tan(math.radians(step / 2))
        o0 = C - tan * (uw / 2)
        add(o0 + Vector((0, 0, z0 - 0.1)) - nrm * 0.05, tan * uw, nrm * 0.02, Vector((0, 0, z1 - z0 + 0.6)), wood)  # back board
        z = z0
        while z <= z1:
            add(o0 + Vector((0, 0, z - 0.03)), tan * uw, nrm * 0.30, Vector((0, 0, 0.03)), wood)
            s = 0.02
            while s < uw - 0.06:
                w = rng.uniform(0.028, 0.065); h = rng.uniform(0.22, dz - 0.06); dep = rng.uniform(0.18, 0.24)
                c = lin(rng.choice(spines)); k = rng.uniform(0.7, 1.15); col = (c[0] * k, c[1] * k, c[2] * k, 1.0)
                if rng.random() < 0.08:
                    s += w; continue  # gaps
                add(o0 + tan * s + nrm * rng.uniform(0.02, 0.06) + Vector((0, 0, z)), tan * w, nrm * dep, Vector((0, 0, h)), col)
                s += w + rng.uniform(0.0, 0.004)
            z += dz
        th += step
    o = mesh_obj("library", verts, faces, M["lib"], None, smooth_=False)
    ca = o.data.color_attributes.new("col", "FLOAT_COLOR", "POINT")
    flat = [x for c in cols for x in c]; ca.data.foreach_set("color", flat)
    dbg("library boxes", len(faces) // 6)


def build_lamp(name, pos):
    """Practical reading lamp: pleated shade (glowing), bulb (blooms), brass pole + trims (trait 7)."""
    seg, r_bot, r_top, hgt = 96, 0.30, 0.17, 0.28
    verts, faces = [], []
    for ring, (r0, z) in enumerate(((r_bot, -hgt / 2), (r_top, hgt / 2))):
        for k in range(seg):
            a = 2 * math.pi * k / seg; pl = 1 + 0.045 * abs(math.sin(14 * a))  # pleats
            verts.append(pos + Vector((r0 * pl * math.cos(a), r0 * pl * math.sin(a), z)))
    faces = [(k, (k + 1) % seg, seg + (k + 1) % seg, seg + k) for k in range(seg)]
    mesh_obj(name + "_shade", verts, faces, M["shade"], None)
    for r0, z in ((r_bot, -hgt / 2), (r_top, hgt / 2)):
        curve_obj(name + f"_trim{z:+.2f}", [pos + Vector((r0 * 1.04 * math.cos(a), r0 * 1.04 * math.sin(a), z)) for a in (2 * math.pi * k / 48 for k in range(48))],
                  0.006, M["brass"], None, kind="POLY", cyclic=True)
    sphere(name + "_bulb", pos + Vector((0, 0, -0.04)), (0.06,) * 3, M["bulb"], None, 16)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.012, depth=4.0, location=pos + Vector((0, 0, -2.0 - hgt / 2)))
    pole = bpy.context.object; pole.name = name + "_pole"; pole.data.materials.append(M["brass"])
    ld = bpy.data.lights.new(name + "_light", "POINT"); ld.energy = QP.get("lamp_energy", 60); ld.color = lin(PAL["lamp"])[:3]
    try:
        ld.shadow_soft_size = 0.08
    except AttributeError:
        pass
    lo = link(bpy.data.objects.new(name + "_light", ld)); lo.location = pos + Vector((0, 0, -0.03))


def build_plate(kind):
    if kind == "studio":
        world_gradient(PAL["studio_top"], PAL["studio_bottom"], 1.0)
        guard("floor", floor, mat("studio_floor", PAL["studio_floor"], 0.9))
    else:
        world_gradient(PAL["plate_top"], PAL["plate_bottom"], 1.0)
        guard("floor", floor, M["floor"])
        guard("library", build_library)
        rng = random.Random(H["seed"] + 41)
        for s in V["shots"]:
            for lp in QP.get("lamps", []):
                if lp["shot"] == s["id"]:
                    pos, _ = at_screen(s, *lp["at"])
                    guard("lamp_" + s["id"], build_lamp, "lamp_" + s["id"], pos)
            sides = QP.get("bokeh_sides", 8)  # 8-sided: near-round but clearly a lens shape, never round "cells" (owner, 21 Nov)
            for i in range(QP.get("bokeh_per_shot", 6)):  # top corners only, away from the host
                fx = rng.choice((-1, 1)) * rng.uniform(0.55, 0.95); fy = rng.uniform(0.45, 0.95)
                pos, cam = at_screen(s, fx, fy, rng.uniform(5.2, 6.4)); sz = rng.uniform(*QP.get("bokeh_size", [0.05, 0.10]))  # EDIT: R4 smaller
                bpy.ops.mesh.primitive_cylinder_add(vertices=sides, radius=sz, depth=0.004, location=pos)
                bo = bpy.context.object; bo.name = f"bokeh_{s['id']}{i:02d}"; bo.data.materials.append(M["bokeh"])
                bo.rotation_mode = "QUATERNION"; bo.rotation_quaternion = (cam - pos).to_track_quat("Z", "Y")
    Lg = dict(SPEC.get("lights", {}))
    if kind == "studio":
        Lg.update(SPEC.get("lights_studio", {}))

    def area(name, loc, energy, color, size):
        ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.color = lin(color)[:3]; ld.size = size
        lo = link(bpy.data.objects.new(name, ld)); lo.location = loc
        c = lo.constraints.new("TRACK_TO"); c.target = P["rig"]; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    for nm, dflt in (("key", [-2.3, -1.2, 1.3, 320, "#FFC890", 1.4]),     # EDIT: warm side key (≈2700 K, practical-motivated)
                     ("rim", [1.3, 1.9, 1.3, 340, PAL["lamp"], 1.0]),       # warm rim
                     ("fill", [2.0, -1.6, 0.1, 55, "#E8E0FF", 2.0])):      # soft cool fill
        x, y, z, e, c, s_ = Lg.get(nm, dflt)
        area(nm, (x, y, z), e, c, s_)


# ---------------- pose ----------------
# EDIT: six expressions (playbook §5b sheet). brow dz/tilt in m/deg, eye openness, smile −1…1, open 0…1, tilt deg, look x (m)
EXPR = {
    "warm":      dict(bdz=0.004, btilt=6,    eye=0.88, smile=0.65, open=0.00, tilt=-4, look=0.0),
    "curious":   dict(bdz=0.026, btilt=12,   eye=1.12, smile=0.15, open=0.00, tilt=10, look=0.008, asym=1),
    "delighted": dict(bdz=0.016, btilt=-4,   eye=0.45, smile=1.00, open=0.35, tilt=-5, look=0.0),
    "surprised": dict(bdz=0.036, btilt=0,    eye=1.28, smile=0.00, open=0.70, tilt=0,  look=0.0, oshape=1),
    "thinking":  dict(bdz=-0.006, btilt=-16, eye=0.70, smile=-0.10, open=0.00, tilt=-10, look=0.014, asym=1, gaze=18),
    "tsk":       dict(bdz=-0.012, btilt=-22, eye=0.58, smile=-0.40, open=0.00, tilt=7, look=-0.006),
}


def key(o, path, f):
    if f is not None and o is not None:
        o.keyframe_insert(path, frame=f)


def lid_deg(e):
    base = QF.get("lid_open_deg", -38)  # EDIT: resting upper lid (negative = more open)
    return base - (e - 1) * 96 if e >= 1 else base + (1 - e) * 134


def apply_expr(P, rig, e, f=None, blink=1.0):
    x = EXPR[e]; ev = x["eye"] * blink; ld = lid_deg(ev); er = QF.get("eye_r", 0.036)
    up = math.radians(-QF.get("gaze_up_deg", 8))  # looks up over the glasses
    for side, sx in (("L", -1), ("R", 1)):
        br = P.get("brow" + side)
        if br:
            dz = x["bdz"] + (0.012 if x.get("asym") and side == "R" else 0)
            br.location.z = P["brow_z" + side] + dz; br.rotation_euler = (0, math.radians(-sx * x["btilt"]), 0)
            key(br, "location", f); key(br, "rotation_euler", f)
        if not P.get("eye" + side):
            continue
        g = P["eye" + side]; s = 1 + max(0.0, ev - 1) * QF.get("surprise_eye_scale", 0.0)  # G-Art R1: wide eyes come from the
        g.scale = (s, s, s); key(g, "scale", f)  # upper-lid caps opening (lid_deg below), not from scaling the eyeball (default 0)
        lid = P["lid" + side]; lid.rotation_euler = (math.radians(ld), 0, 0); key(lid, "rotation_euler", f)
        ball = P["ball" + side]; ball.rotation_euler = (up - math.radians(x.get("gaze", 0)), 0, x["look"] / er); key(ball, "rotation_euler", f)
        hv = 1.0 if ld <= 0 else max(0.0, 1 - ld / 40)  # highlights go with the lid
        for hk, base in (("hiA", 0.0075), ("hiB", 0.0035)):
            h_ = P[hk + side]; h_.scale = (base, base, base * hv + 1e-5); key(h_, "scale", f)
    rig.rotation_euler = (0, math.radians(x["tilt"]), 0); key(rig, "rotation_euler", f)
    set_smile(P, x["smile"], f)


def set_smile(P, smile, f=None):
    if not P.get("lip"):
        return
    pts = P["lip"].data.splines[0].bezier_points
    dzs = (0.011, -0.003, -0.013, -0.003, 0.011)  # EDIT: corners up, middle down
    for i, bp in enumerate(pts):
        b = P["lip_base"][i]; bp.co = (b.x, b.y, b.z + dzs[i] * smile)
        if f is not None:
            bp.keyframe_insert("co", frame=f)


def set_mouth(P, shape, op, f=None):
    if not P.get("mouth"):
        return
    w = {"A": 1.0, "E": 1.2, "O": 0.62, "F": 0.95, "M": 1.0, "rest": 1.0}.get(shape, 1.0)
    P["mouth"].scale = (0.042 * w, 0.004, 0.002 + 0.038 * op)
    key(P["mouth"], "scale", f)


def camera(name, shot):
    cd = bpy.data.cameras.new(name); cd.lens = shot["lens_mm"]; cd.sensor_fit = "AUTO"
    cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2  # EDIT: macro DOF (visual-style §6)
    cam = link(bpy.data.objects.new(name, cd)); tgt = link(bpy.data.objects.new(name + "_aim", None))

    def place(d, f=None):
        t_, l_, *_ = cam_pose(shot, d)
        tgt.location = t_; cam.location = l_
        key(cam, "location", f); key(tgt, "location", f)
    c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    cd.dof.focus_object = P.get("eyeL") if shot["cam_yaw_deg"] <= 0 else P.get("eyeR")
    return cam, place


GRADE = {"state": "off"}


def grade():
    """Compositor: bloom on the practicals only, warm lift-gamma-gain, vignette (visual-style §5; trait 8)."""
    sc = bpy.context.scene; G = V.get("grade")
    if not G or PALPASS:
        return
    sc.use_nodes = True; nt = sc.node_tree
    for n in list(nt.nodes):
        if n.type not in ("R_LAYERS", "COMPOSITE"):
            nt.nodes.remove(n)
    rl = nt.nodes["Render Layers"]; comp = nt.nodes["Composite"]
    try:
        gl = nt.nodes.new("CompositorNodeGlare")
        for gt in ("BLOOM", "FOG_GLOW"):
            try:
                gl.glare_type = gt; break
            except TypeError:
                continue
        want = {"threshold": G.get("glare_threshold", 2.0), "size": 7, "mix": G["glare"] - 1.0, "strength": G["glare"]}
        done = []
        for attr, val in want.items():
            if hasattr(gl, attr):
                try:
                    setattr(gl, attr, val); done.append(attr)
                except Exception:
                    pass
        for sock in gl.inputs:  # Blender 4.4+: settings moved to sockets
            nm = sock.name.lower()
            for attr, val in want.items():
                if attr in nm and attr not in done and hasattr(sock, "default_value") and not isinstance(sock.default_value, (str,)):
                    try:
                        sock.default_value = val; done.append(attr)
                    except Exception:
                        pass
        dbg("glare set", done)
        cb = nt.nodes.new("CompositorNodeColorBalance"); cb.correction_method = "LIFT_GAMMA_GAIN"
        cb.lift, cb.gamma, cb.gain = G["lift"], G["gamma"], G["gain"]
        em = nt.nodes.new("CompositorNodeEllipseMask"); em.width, em.height = 0.95, 0.75
        bl = nt.nodes.new("CompositorNodeBlur"); bl.size_x = bl.size_y = 200; bl.use_relative = False
        vm = nt.nodes.new("CompositorNodeMixRGB"); vm.blend_type = "MULTIPLY"; vm.inputs[0].default_value = G["vignette"]
        nt.links.new(rl.outputs["Image"], gl.inputs[0]); nt.links.new(gl.outputs[0], cb.inputs[1])
        nt.links.new(em.outputs[0], bl.inputs[0]); nt.links.new(cb.outputs[0], vm.inputs[1]); nt.links.new(bl.outputs[0], vm.inputs[2])
        nt.links.new(vm.outputs[0], comp.inputs[0])
        GRADE["state"] = "on"; dbg("grade on")
    except Exception as e:  # never block a render on the grade; log it
        print("[host] grade skipped:", e); GRADE["state"] = f"skipped: {e}"
        nt.links.new(rl.outputs["Image"], comp.inputs[0])


def frame_of(t):
    return 1 + int(round(t * FPS))


def anim_shot(rig):
    sc = bpy.context.scene
    vis = json.load(open(os.path.join(OUT, "audio", "visemes.json")))["frames"]
    track = V["expression_track"]
    cur = lambda t: [e["expr"] for e in track if e["t"] <= t + 1e-6][-1]
    for e in track:                                   # expressions, eased (Bezier)
        apply_expr(P, rig, e["expr"], frame_of(e["t"]))
        apply_expr(P, rig, e["expr"], max(1, frame_of(e["t"]) - 1 + 6))
    t, blinks = random.uniform(*V["blink_every_s"]) * 0.5, []
    while t < V["seconds"] - 0.3:                     # blinks (never on a cut frame)
        blinks.append(t); t += random.uniform(*V["blink_every_s"])
    for bt in blinks:
        f = frame_of(bt); e = cur(bt)
        apply_expr(P, rig, e, f - 2); apply_expr(P, rig, e, f, blink=0.08); apply_expr(P, rig, e, f + 2)
    o0, o1 = V.get("book_open_s", [0, 0])
    for side, sx in (("L", -1), ("R", 1)):  # book: closed (pages together) → open (blank pages); reduced motion: open from the start
        h = P.get("book" + side)
        if not h:
            continue
        if not RM and o1 > 0:
            h.rotation_euler = (0, 0, sx * math.radians(QB.get("closed_deg", -84))); key(h, "rotation_euler", frame_of(o0))
        h.rotation_euler = (0, 0, sx * math.radians(QB.get("open_deg", -20))); key(h, "rotation_euler", frame_of(o1) if not RM else 1)
    rim = bpy.data.objects.get("rim")
    if rim and V.get("rim_flicker_hz"):  # slow warm flicker, far below 3/s (H5)
        e0 = rim.data.energy
        for f in range(1, NF + 1, 3):
            rim.data.energy = e0 * (1 + 0.06 * math.sin(2 * math.pi * V["rim_flicker_hz"] * f / FPS)); rim.data.keyframe_insert("energy", frame=f)
    for v in vis:                                     # mouth from visemes (beat-scaled)
        f = v["f"] + 1
        speaking = v["shape"] != "rest"
        set_mouth(P, v["shape"] if speaking else ("O" if EXPR[cur(v["f"] / FPS)].get("oshape") else "rest"),
                  v["open"] if speaking else EXPR[cur(v["f"] / FPS)]["open"], f)
        rig.scale = (1, 1, 1 + 0.012 * v["env"]); key(rig, "scale", f)  # tiny bob on stresses
    for s in V["shots"]:                              # two cameras + timeline markers = the cut
        cam, place = camera("cam_" + s["id"], s)
        f0, f1 = frame_of(s["start_s"]), frame_of(s["end_s"])
        push = 0.0 if RM else s["push_in"]
        place(s["dist"], f0); place(s["dist"] * (1 - push), f1)
        m = sc.timeline_markers.new("shot_" + s["id"], frame=f0); m.camera = cam
        if f0 == 1:
            sc.camera = cam
    dbg("blinks", [round(b, 2) for b in blinks], "frames", NF)


REGION = (("body", "body"), ("arm", "body"), ("hand", "body"), ("lid", "body"), ("shawl", "shawl"), ("fringe", "shawl"),
          ("book_cover", "book_cover"), ("book_pages", "pages"))
HOST_PARTS = ("eye", "hi", "brow", "crease", "undereye", "lip", "dimple", "mouth", "rim", "temple", "chain", "bridge", "lens",
              "glass", "book", "ribbon", "corner", "nose", "cheek")  # small host features: neither host region nor plate


def probe(cam, name, sub="sheet", frame=None):
    """Object mask by ray casting through the pixel grid → out/<sub>/probe_<name>.json (m1b.py palette: rendered-pixel ΔE and
    host-vs-plate separation). Anything that is not host (floor, shelves, lamps, bokeh, sky) counts as the plate."""
    sc = bpy.context.scene; bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    W, Hh = sc.render.resolution_x, sc.render.resolution_y; step = 3 if W <= 400 else 6
    mw = cam.matrix_world; o = mw.translation
    tr, br, bl, tl = [mw @ v for v in cam.data.view_frame(scene=sc)]
    pts = {}
    for py in range(step // 2, Hh, step):
        for px in range(step // 2, W, step):
            u, v = (px + 0.5) / W, (py + 0.5) / Hh
            p = tl.lerp(tr, u).lerp(bl.lerp(br, u), v)
            hit, _, _, _, ob, _ = sc.ray_cast(dg, o, (p - o).normalized())
            reg = "plate"
            if hit:
                reg = next((r for pre, r in REGION if ob.name.startswith(pre)), "plate" if not ob.name.startswith(HOST_PARTS) else None)
            if reg:
                pts.setdefault(reg, []).append([px, py])
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    json.dump({"w": W, "h": Hh, "step": step, "view": sc.view_settings.view_transform, "frame": frame, "res": RES + ("_rm" if RM else ""),
               "camera": cam.name, "pts": pts}, open(os.path.join(OUT, sub, f"probe_{name}.json"), "w"))


def probe_shots():
    """Probes per camera at the start, middle and end of its shot (G-A11y R5: shot B's lamp is the case to catch);
    m1b.py palette reads each frame back from out/frames/<res>/."""
    sc = bpy.context.scene
    for s_ in V["shots"]:
        if ONLY in ("A", "B") and ONLY != s_["id"]:
            continue
        f0, f1 = frame_of(s_["start_s"]), min(NF, frame_of(s_["end_s"]) - 1)
        cam = bpy.data.objects.get("cam_" + s_["id"])
        for tag, f in (("start", f0 + 2), ("mid", (f0 + f1) // 2), ("end", f1 - 2)):  # EDIT: ±2 frames off the cut
            sc.frame_set(f)
            if cam:
                sc.camera = cam; probe(cam, f"shot_{s_['id']}_{tag}", "shot", f)
    sc.frame_set(sc.frame_start)


def sheet(rig):
    os.makedirs(os.path.join(OUT, "sheet", "tiles"), exist_ok=True)
    sc = bpy.context.scene
    for name, yaw, pit, d, lens, e in SHEET_TILES:
        if ONLY and ONLY != name:
            continue
        for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
            bpy.data.objects.remove(o)
        apply_expr(P, rig, e); set_mouth(P, "O" if EXPR[e].get("oshape") else "A", EXPR[e]["open"])
        cam, place = camera("cam_" + name, {"lens_mm": lens, "cam_yaw_deg": yaw, "cam_pitch_deg": pit, "dist": d})
        place(d); sc.camera = cam
        tag = name + ("_std" if PALPASS else "")
        sc.render.filepath = os.path.join(OUT, "sheet", "tiles", tag + ".png")
        t0 = time.time()
        if not DRY:
            bpy.ops.render.render(write_still=True)
            if name == "front":
                guard("probe_" + tag, probe, cam, tag)
        print(f"[host] tile {tag} {time.time() - t0:.1f} s", flush=True)


def main():
    t_all = time.time()
    sc = reset()
    rig = empty("rig"); P["rig"] = rig
    body = build_body(rig)
    build_materials(body); body.data.materials.append(M["body"])
    guard("face", build_face, rig)
    guard("glasses", build_glasses, rig)
    guard("book", build_book, rig)
    guard("arms", build_arms, rig)
    guard("shawl", build_shawl, rig, body)
    guard("hooks", hook_arms)
    sub = body.modifiers.new("soft", "SUBSURF"); sub.levels = 0; sub.render_levels = 1
    guard("outline", add_outline, body)  # after subsurf, so the hull follows the smoothed silhouette
    plate = QP.get("sheet", "studio") if MODE == "sheet" else QP.get("shot", "library")
    guard("plate_" + plate, build_plate, plate)
    dbg("objects", len(bpy.data.objects), "engine", sc.render.engine, "res", RES)
    if MODE == "sheet":
        grade()
        sheet(rig)
    else:
        guard("anim", anim_shot, rig)
        grade()
        d = os.path.join(OUT, "frames", RES + ("_rm" if RM else "")); os.makedirs(d, exist_ok=True)
        sc.render.filepath = os.path.join(d, "f_")
        if ONLY in ("A", "B"):
            s = [x for x in V["shots"] if x["id"] == ONLY][0]
            sc.frame_start, sc.frame_end = frame_of(s["start_s"]), min(NF, frame_of(s["end_s"]) - (0 if s["end_s"] >= V["seconds"] else 1))
        print(f"[host] shot frames {sc.frame_start}-{sc.frame_end} @ {sc.render.resolution_x}x{sc.render.resolution_y} → {d}", flush=True)
        if not DRY:
            guard("probe_shots", probe_shots)
            t0 = time.time(); bpy.ops.render.render(animation=True)
            json.dump({"render_s": round(time.time() - t0, 1), "frames": sc.frame_end - sc.frame_start + 1,
                       "engine": sc.render.engine, "res": [sc.render.resolution_x, sc.render.resolution_y],
                       "blender": bpy.app.version_string, "shawl": LOG.get("shawl"),
                       "grade": GRADE["state"], "view_transform": sc.view_settings.view_transform, "reduced_motion": RM},
                      open(os.path.join(OUT, f"render_stats_{RES}.json"), "w"), indent=1)
    LOG.update({"mode": MODE, "res": RES, "seconds": round(time.time() - t_all, 1), "blender": bpy.app.version_string,
                "failed": [k for k, v in LOG["parts"].items() if v.startswith("FAILED")]})
    json.dump(LOG, open(os.path.join(OUT, f"build_log_{MODE}.json"), "w"), indent=1)
    if LOG["failed"]:
        print("[host] PARTS FAILED:", LOG["failed"], "→ see out/build_log_%s.json" % MODE, flush=True)
    if DEBUG or DRY:
        os.makedirs(os.path.join(OUT, "debug"), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "debug", f"host_{MODE}.blend"))
        print("[host] saved debug .blend (open it to inspect or nudge # EDIT: values)")


main()
