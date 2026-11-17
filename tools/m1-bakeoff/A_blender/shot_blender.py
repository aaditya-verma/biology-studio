"""Method A: Blender, scripted from Python. Renders shot M1-ps01 clean (no text) frame by frame.
Run (from the kit folder):
  blender -b --factory-startup -P A_blender/shot_blender.py -- --engine CYCLES --out out/A_cycles
  blender -b --factory-startup -P A_blender/shot_blender.py -- --engine EEVEE  --out out/A_eevee
Options: --every N (render every Nth frame, for a quick s/frame estimate), --samples 64."""
import argparse, json, math, os, sys, time
import bpy

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(KIT, "common"))
import scene_math as sm

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--engine", choices=["CYCLES", "EEVEE"], required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--every", type=int, default=1)
ap.add_argument("--samples", type=int, default=64)
a = ap.parse_args(argv)

shot = sm.load_shot()
out = os.path.abspath(os.path.join(KIT, a.out)) if not os.path.isabs(a.out) else a.out
os.makedirs(os.path.join(out, "frames"), exist_ok=True)


def srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgba(h, alpha=1.0):
    h = h.lstrip("#")
    return tuple(srgb_to_lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)) + (alpha,)


# ---------- scene ----------
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene
r = sc.render
r.resolution_x, r.resolution_y, r.resolution_percentage = shot["width"], shot["height"], 100
r.fps = shot["fps"]
r.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "Standard"  # keep token colours true (no Filmic/AgX desaturation)
sc.view_settings.look = "None"

engine_note = ""
if a.engine == "CYCLES":
    r.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    device_type = None
    for dt in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = dt
            prefs.get_devices()
            devs = [d for d in prefs.devices if d.type == dt]
            if devs:
                for d in prefs.devices:
                    d.use = d.type == dt
                device_type = dt
                break
        except TypeError:
            continue
    sc.cycles.device = "GPU" if device_type else "CPU"
    sc.cycles.samples = a.samples
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = "OPTIX" if device_type == "OPTIX" else "OPENIMAGEDENOISE"
    except TypeError:
        pass
    sc.cycles.seed = shot["seed"]
    engine_note = f"Cycles {sc.cycles.device}/{device_type or 'none'} {a.samples} spp, denoise {sc.cycles.denoiser}"
else:
    ids = [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    r.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in ids else "BLENDER_EEVEE"
    engine_note = r.engine

world = bpy.data.worlds.new("bg")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = rgba(shot["colors"]["background"])
sc.world = world

cam_d = bpy.data.cameras.new("cam")
cam_d.type = "ORTHO"
cam_d.ortho_scale = shot["camera"]["ortho_width_units"]
cam_d.sensor_fit = "HORIZONTAL"
cam_d.clip_end = 200
cam = bpy.data.objects.new("cam", cam_d)
sc.collection.objects.link(cam)
e, D = math.radians(shot["camera"]["elevation_deg"]), shot["camera"]["distance"]
cam.location = (0, -D * math.cos(e), D * math.sin(e))
cam.rotation_euler = (math.pi / 2 - e, 0, 0)
sc.camera = cam

for name, energy, rot in [("key", 3.0, (math.radians(35), math.radians(15), math.radians(-30))),
                          ("fill", 1.0, (math.radians(-40), math.radians(-20), math.radians(160)))]:
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy = energy
    lo = bpy.data.objects.new(name, ld)
    lo.rotation_euler = rot
    sc.collection.objects.link(lo)

mats = {}


def material(key, hexcol, opacity):
    if key in mats:
        return mats[key]
    m = bpy.data.materials.new(key)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba(hexcol)
    b.inputs["Roughness"].default_value = 0.55
    b.inputs["Alpha"].default_value = opacity
    if opacity < 1:
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
        elif hasattr(m, "blend_method"):
            m.blend_method = "BLEND"
    mats[key] = m
    return m


objs = {}


def update(frame):
    s, parts = sm.build(shot, frame)
    seen = set()
    for p in parts:
        verts, tris = sm.prism(p["poly"], p["z0"], p["z1"])
        me = bpy.data.meshes.new(p["name"])
        me.from_pydata(verts, [], tris)
        me.materials.append(material(p["name"], p["color"], p["opacity"]))
        if p["name"] in objs:
            old = objs[p["name"]].data
            objs[p["name"]].data = me
            bpy.data.meshes.remove(old)
        else:
            o = bpy.data.objects.new(p["name"], me)
            sc.collection.objects.link(o)
            objs[p["name"]] = o
        objs[p["name"]].hide_render = False
        seen.add(p["name"])
    for n, o in objs.items():
        if n not in seen:
            o.hide_render = True
    return s


n_frames = int(shot["fps"] * shot["duration_s"])
todo = list(range(0, n_frames, a.every))
t0 = time.time()
per = []
for f in todo:
    tf = time.time()
    update(f)
    r.filepath = os.path.join(out, "frames", f"{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    per.append(time.time() - tf)
    print(f"[A] frame {f} {per[-1]:.2f}s", flush=True)
total = time.time() - t0

stats = {
    "method": f"A_blender_{a.engine.lower()}",
    "tool": f"Blender {bpy.app.version_string}",
    "engine": engine_note,
    "frames_rendered": len(todo),
    "frames_total": n_frames,
    "every": a.every,
    "sec_total": round(total, 1),
    "sec_per_frame_mean": round(sum(per) / len(per), 3),
    "sec_first_frame": round(per[0], 2),
    "est_sec_full_shot": round(sum(per) / len(per) * n_frames, 1),
    "settings": {"res": [shot["width"], shot["height"]], "samples": a.samples if a.engine == "CYCLES" else None,
                 "view_transform": "Standard"},
}
with open(os.path.join(out, "render_stats.json"), "w") as fh:
    json.dump(stats, fh, indent=2)
print("[A] done", json.dumps(stats))
