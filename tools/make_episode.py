#!/usr/bin/env python3
"""Make a whole episode in one go, with every Kaggle fix built in.

    python tools/make_episode.py episodes/EduCrew_Biography_Episode_02.json --only pictures
    python tools/make_episode.py episodes/EduCrew_Biography_Episode_02.json          # everything else

Steps (each one skips what already exists, so re-running after a stop is always safe):
  pictures -> clips (both GPUs) -> voices -> sounds -> reel
Everything each step needs (extra packages, the voice environment, MMAudio) is set up
automatically the first time. Stops at the first failure and says which step failed.
"""
import argparse, glob, importlib.util, json, os, subprocess, sys, time

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
TTS_PY = "/kaggle/working/.tts_env/bin/python"
MMAUDIO = "/kaggle/working/MMAudio"
SFX_PACKAGES = ["av", "colorlog", "einops", "librosa", "omegaconf", "open_clip_torch", "timm", "torchdiffeq", "soundfile"]
STEPS = ["pictures", "clips", "voices", "sounds", "reel"]

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("episode")
ap.add_argument("--only", choices=STEPS, help="run just one step")
ap.add_argument("--skip", default="", help="comma-separated steps to skip, e.g. pictures")
ap.add_argument("--redo", default="", help="shot numbers to remake completely (picture, clip, sound), e.g. 1 or 1,4")
ap.add_argument("--seed", type=int, help="new seed for --redo, to get a different version")
a = ap.parse_args()

episode = os.path.abspath(a.episode)
ep = json.load(open(episode, encoding="utf-8"))
name = os.path.splitext(os.path.basename(episode))[0]
work = os.path.join(ROOT, "work", name)
skip = {s.strip() for s in a.skip.split(",") if s.strip()}
todo = [a.only] if a.only else [s for s in STEPS if s not in skip]


def run(cmd, cwd=TOOLS):
    print("  $", " ".join(os.path.basename(c) if c.startswith("/") and c.endswith(".py") else c for c in cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd).returncode == 0


def have(*mods):
    return all(importlib.util.find_spec(m) for m in mods)


def check_before(step):
    """Warn early about things that would otherwise fail or look wrong later."""
    if step == "pictures":
        for s in ep["shots"]:
            src = s.get("continue_from")
            if src and not os.path.exists(os.path.join(ROOT, src)):
                print(f"  ! shot {s['id']} should continue from {src}, which isn't made yet.\n"
                      f"    Make the episodes in order (the previous episode's pictures first).")
        missing_refs = {r for r, p in ep.get("refs", {}).items() if not os.path.exists(os.path.join(ROOT, p))}
        if missing_refs and ep.get("refs"):
            print(f"  ! character pictures missing for {sorted(missing_refs)}: run EduCrew_Characters.json first.")
    if step == "clips":
        missing = [s["id"] for s in ep["shots"]
                   if not os.path.exists(os.path.join(work, "keyframes", f"shot{s['id']:02d}.png"))]
        if missing:
            print(f"  ! pictures missing for shots {missing}: make the pictures first.")
            return False
    if step == "reel" and not os.path.exists(os.path.join(ROOT, ep.get("logo", ""))):
        print("  ! logo file not found: the Reel will have no logo.")
    return True


def step_pictures():
    return run([sys.executable, "make_keyframes.py", episode])


def step_clips():
    return run([sys.executable, "make_clips.py", episode])


def step_voices():
    if not any(s.get("lines") for s in ep["shots"]):
        print("  (no spoken lines in this file)")
        return True
    return run([sys.executable, "setup_tts_env.py"]) and run([TTS_PY, "make_voices.py", episode])


def step_sounds():
    return step_sounds_for([])


def step_sounds_for(extra):
    if not step_sounds_setup():
        return False
    return run([sys.executable, "make_sfx.py", episode, "--mmaudio", MMAUDIO, *extra])


def step_sounds_setup():
    if not have("av", "einops", "omegaconf", "open_clip", "timm", "torchdiffeq", "librosa", "colorlog", "soundfile"):
        if not run([sys.executable, "-m", "pip", "install", "-q", *SFX_PACKAGES]):
            return False
    return os.path.exists(MMAUDIO) or run(["git", "clone", "-q", "https://github.com/hkchengrex/MMAudio", MMAUDIO])


def step_reel():
    return run([sys.executable, os.path.join(ROOT, "assemble.py"), episode], cwd=ROOT)


if name == "EduCrew_Characters":
    todo = [s for s in todo if s == "pictures"]  # the character file only needs pictures
t_all = time.time()
if a.redo:  # remake the listed shots completely, then rebuild the Reel
    seed = ["--seed", str(a.seed)] if a.seed is not None else []
    shots = ["--shots", a.redo, "--force"]
    print(f"\n=== REDO shots {a.redo} ===", flush=True)
    ok = (run([sys.executable, "make_keyframes.py", episode, *shots, *seed])
          and run([sys.executable, "make_clips.py", episode, *shots, *seed])
          and step_sounds_for(shots) and step_reel())
    sys.exit(0 if ok else "Stopped: the redo failed. Send the red lines above to Claude.")
for step in todo:
    print(f"\n=== {step.upper()} ({name}) ===", flush=True)
    t0 = time.time()
    if not check_before(step) or not globals()[f"step_{step}"]():
        sys.exit(f"\nStopped: the '{step}' step failed. Send the red lines above to Claude, "
                 f"then run the same cell again (finished parts are kept).")
    print(f"=== {step} finished in {(time.time() - t0) / 60:.1f} min ===", flush=True)

print(f"\nAll done in {(time.time() - t_all) / 60:.1f} min.")
reel = glob.glob(os.path.join(ROOT, "output", f"*{name}.mp4"))
if "reel" in todo and reel:
    print("Your Reel:", reel[0])
