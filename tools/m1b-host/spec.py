"""M1b host shot — the one place for every changeable value (RULES I6).
Owner docs: studio-docs/build/studio-playbook.md §5b (host rules), build/visual-style.md §1 (frame, captions),
claude/DECISIONS.md D-048 (host = Nani Koshika, voice V-a) and D-049 (route H-a: 3D in Blender).
Edit points are marked `# EDIT:`. Nothing here is book text (F/G rules)."""

SHOT_ID = "M1b-host01"            # EDIT: bump (host02, …) for a new take; published files are never overwritten (H7)
HOST = "Nani Koshika"
REFERENCE = r"..\..\..\..\handoff\m1b-host\canva-refs\AaH5fRyruIHzmc8LDKQV2w-AaH5fRysNU1B-mJK6YtVbw.jpg"  # EDIT: identity reference (laptop only, never in the repo)
REFERENCE_CANVA_ID = "MAHbd5r-vTY"

# ---------- line + voice (D-024 V-a, D-048) ----------
LINE_EN = "What if a flat disc had to build a whole body?"   # EDIT: spoken line
LINE_HI = "चपटी डिस्क से पूरा शरीर?"                       # EDIT: Devanagari caption line ("a whole body from a flat disc?") — caption only, not spoken
KEY_EN = ["body"]                                           # EDIT: word(s) on the pearl highlight pill — one, so it stands out (G-Art R1)
KEY_HI = ["शरीर"]
PHRASE_BREAKS = ["had"]                                     # EDIT: a new caption phrase starts at these words
VOICE = {"engine": "kokoro", "voice": "af_heart", "speed": 0.9, "lang_code": "a"}  # EDIT: voice (V-a), speed 0.9 (owner)
LEAD_IN_S = 0.30                  # EDIT: silence before the line (hook lands by 1 s)

# ---------- frame (visual-style §1) ----------
FPS = 30                          # EDIT: 30 at 720p ship; 60 only once Measured
DURATION_S = 5.0
MASTER = (1080, 1920)             # EDIT: design/master size (9:16)
SHIP = (720, 1280)                # EDIT: shipped rendition until the 1080p rung is Measured (H8, D-033)
PREVIEW = (540, 960)              # --preview size
CUT_AT_S = 2.50                   # EDIT: cut from camera A to camera B (two angles, same identity)
SAFE = {"top": 0.14, "bottom": 0.25, "right": 0.14, "left": 0.04}   # fraction of frame (visual-style §1)
CAPTION_BAND = (0.55, 0.65)       # captions live between 55–65 % from the top
CAPTION_MAX_W = 0.70
CAPTION = {
    "cap_px_at_1080": 44,         # EDIT: cap height ≥ 40 px at 1080 wide
    "deva_scale": 1.15,           # Devanagari +15 %
    "weight_note": "bold (≥ 600)",
    "text": "#FFFFFF", "outline": "#1F1A24", "outline_px": 4,
    "scrim": (31, 26, 36, 190),   # EDIT: ink scrim, alpha 0–255 → contrast ≥ 4.5:1 (checked in the manifest)
    "pill_bg": "#F5EBFF", "pill_text": "#1F1A24",   # key word = ink on pearl pill; no gold (too close to the endoderm token)
    "pop_frames": 4, "pop_scale": 1.15,
    "max_chars_line": 28,
}
# Fonts: OFL first (registry § Tools); Windows system fallbacks are recorded in the manifest.
FONTS_LATIN = [r"..\..\..\..\apps\fonts\Inter-Bold.ttf", r"..\..\..\..\apps\fonts\JosefinSans-Bold.ttf",
               r"C:\Windows\Fonts\segoeuib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]   # EDIT
FONTS_DEVA = [r"..\..\..\..\apps\fonts\NotoSansDevanagari-Bold.ttf", r"..\..\..\..\apps\fonts\Mukta-Bold.ttf",
              r"C:\Windows\Fonts\NirmalaB.ttf", r"C:\Windows\Fonts\Nirmala.ttc"]                           # EDIT

# ---------- host look (playbook §5b, D-048) ----------
# Body stays a cool pearl: the reference's warm amber body is ΔE00 3.8 from the endoderm token (tritan) — not allowed as a main colour.
COL = {
    "body": "#F5EBFF",            # EDIT: pearl (ΔE00 17.7 from every token)
    "glow": "#FFE9D6",            # EDIT: pale inner glow — keep it small; body pixels are measured in the manifest
    "shawl": "#6A1A12",           # EDIT: crimson shifted toward red-orange, away from plum (ΔE00 17.1 vs accent, tritan; #7A1A2A is 14.5 → too close). G-Art R1: #4A0E16 crushed to black on phones
    "embroidery": "#C9A27A",
    "fringe": "#3E0B12",
    "ink": "#1F1A24", "iris": "#3A2414", "eye_white": "#FBF7F2",
    "blush": "#F0B8B0", "brow": "#7A6A64",
    "glasses": "#8A6A3A", "book": "#3B1A0A", "pages": "#EDE0C8", "ribbon": "#5A1018",
    "plate": "#4E4F51", "plate_low": "#666465",
}
SEED = 0                          # Eevee is deterministic; seed recorded for H7

# ---------- expressions (6 for the sheet; values drive the face rig in blender_host.py) ----------
# eye_open 0–1.3 · brow_l/brow_r raise (−1 frown … +1 up) · brow_tilt (inner up +) · smile (−1 frown … +1) · mouth_open 0–1 · mouth_round 0–1 · look (x, z) · asym (mouth corner skew)
EXPR = {                          # EDIT: tune faces here
    "neutral":   dict(eye_open=1.0, brow_l=0.0, brow_r=0.0, brow_tilt=0.0, smile=0.25, mouth_open=0.0, mouth_round=0.0, look=(0, 0), asym=0.0),
    "warm smile":dict(eye_open=0.8, brow_l=0.2, brow_r=0.2, brow_tilt=0.2, smile=1.0, mouth_open=0.1, mouth_round=0.0, look=(0, 0), asym=0.0),
    "surprise":  dict(eye_open=1.3, brow_l=1.0, brow_r=1.0, brow_tilt=0.3, smile=0.0, mouth_open=0.8, mouth_round=1.0, look=(0, 0), asym=0.0),  # open-eye surprise
    "doubt":     dict(eye_open=0.75, brow_l=0.9, brow_r=-0.4, brow_tilt=-0.2, smile=-0.2, mouth_open=0.0, mouth_round=0.0, look=(0.3, 0.1), asym=0.6),
    "laugh":     dict(eye_open=0.06, brow_l=0.5, brow_r=0.5, brow_tilt=0.4, smile=1.0, mouth_open=0.9, mouth_round=0.0, look=(0, 0), asym=0.0),
    "thinking":  dict(eye_open=0.9, brow_l=0.4, brow_r=0.1, brow_tilt=0.5, smile=0.0, mouth_open=0.0, mouth_round=0.4, look=(-0.4, 0.5), asym=0.2),
}

# ---------- performance on the line ----------
# (time_s, expression) — blended in blender_host.py; visemes from the TTS drive the mouth on top.
PERFORMANCE = [(0.0, "thinking"), (0.45, "neutral"), (1.2, "doubt"), (2.5, "neutral"), (3.4, "surprise"), (4.6, "warm smile")]  # EDIT
BLINKS_S = [1.05, 3.05]           # EDIT

# ---------- cameras (two angles, same identity) ----------
# Positions in metres; character is 2.5 m tall, faces −Y. A = front-left 3/4 push-in, B = right 3/4 (~45°) slow orbit. The pure side view is on the sheet.
CAM_A = dict(start=(-1.05, -4.6, 1.85), end=(-0.85, -3.9, 1.85), target=(0, 0, 1.55), lens_mm=60, fstop=2.8)   # EDIT
CAM_B = dict(start=(3.0, -3.3, 1.70), end=(2.6, -3.5, 1.72), target=(0, 0, 1.55), lens_mm=70, fstop=2.8)       # EDIT: ~45° 3/4 (a pure side profile hides the mouth while she speaks — G-Art R1)
SHEET_CAMS = {"front": dict(pos=(0, -7.0, 1.3), target=(0, 0, 1.25), lens_mm=55),
              "side": dict(pos=(7.0, 0, 1.3), target=(0, 0, 1.25), lens_mm=55),
              "face": dict(pos=(0, -3.4, 1.62), target=(0, 0, 1.55), lens_mm=85)}
ENGINE = "EEVEE"                  # EDIT: EEVEE (fast) or CYCLES (better glass; ~3× slower on the GTX 1060, D-045)
SAMPLES = {"EEVEE": 64, "CYCLES": 128, "preview": 16}
