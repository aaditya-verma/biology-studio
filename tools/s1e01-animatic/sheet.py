"""Contact sheets of out/stills (review aid). sheet.py [prefix ...]"""
import sys, glob, os, math
from PIL import Image, ImageDraw
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
for cut in sys.argv[1:] or ["lesson", "short"]:
    fs = sorted(glob.glob(os.path.join(H, "stills", cut + "_*.jpg")), key=lambda f: (os.path.basename(f).split("_")[1], int(f.split("_")[-1][:-4])))
    tw, th, n = (213, 379, 8) if cut == "short" else (480, 270, 4)
    per = n * (4 if cut != "short" else 3)
    for p in range(math.ceil(len(fs) / per)):
        g = fs[p * per:(p + 1) * per]; im = Image.new("RGB", (n * tw, math.ceil(len(g) / n) * (th + 16)), "#333"); d = ImageDraw.Draw(im)
        for i, f in enumerate(g):
            x, y = i % n * tw, i // n * (th + 16); im.paste(Image.open(f).resize((tw, th)), (x, y + 16)); d.text((x + 3, y + 2), os.path.basename(f), fill="white")
        im.save(os.path.join(H, f"sheet_{cut}_{p}.jpg"), quality=85); print(f"sheet_{cut}_{p}.jpg", len(g))
