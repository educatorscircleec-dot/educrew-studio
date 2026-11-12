"""Step 4: realistic sound effects for every shot, matched to the clip's action.
Free model: MMAudio (github.com/hkchengrex/MMAudio). Music is pushed out with a negative prompt.
Run from the folder that contains the MMAudio checkout (set --mmaudio)."""
import glob, os, subprocess, sys
from common import args, path, skip

a, ep, work, shots = args("Make sound effects", lambda ap: (
    ap.add_argument("--mmaudio", default="MMAudio", help="path to the MMAudio repo"),
    ap.add_argument("--variant", default="large_44k_v2")))

for s in shots:
    n = f"shot{s['id']:02d}"
    out = path(work, "sfx", n + ".wav")
    if skip(out, a.force):
        continue
    tmp = path(work, "_sfx_tmp", n)
    os.makedirs(tmp, exist_ok=True)
    clip = os.path.join(work, "clips", n + ".mp4")
    cmd = [sys.executable, "demo.py", "--variant", a.variant, "--prompt", s["sfx"],
           "--negative_prompt", "music, melody, singing, speech, instruments",
           "--duration", str(s["duration"]), "--output", os.path.abspath(tmp)]
    if os.path.exists(clip):
        cmd += ["--video", os.path.abspath(clip), "--skip_video_composite"]
    print(f"shot {s['id']}: {s['sfx'][:70]}")
    subprocess.run(cmd, cwd=a.mmaudio, check=True)
    made = sorted(glob.glob(os.path.join(tmp, "**", "*.flac"), recursive=True), key=os.path.getmtime)
    if not made:
        sys.exit(f"MMAudio produced no audio for shot {s['id']}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", made[-1], out], check=True)
print("Sound effects done.")
