"""Make the separate environment the voice model needs (it pins an older transformers).

Kaggle-safe: the environment is created WITHOUT its own pip (ensurepip fails on Kaggle),
is linked to the machine's existing packages (so torch is not downloaded again), and the
voice model is installed into it with the machine's own pip. Only the pinned packages
live in the environment; the main environment is not changed.
Run with the main python:  python tools/setup_tts_env.py
"""
import os, shutil, subprocess, sys

ENV = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working/.tts_env"
PY = os.path.join(ENV, "bin", "python")
CHECK = "import torch, soundfile, parler_tts; print('voice environment ready, torch', torch.__version__)"


def works():
    return os.path.exists(PY) and subprocess.run([PY, "-c", CHECK]).returncode == 0


if works():
    raise SystemExit(0)
print("Setting up the voice environment (first time only, a few minutes)...", flush=True)
shutil.rmtree(ENV, ignore_errors=True)
subprocess.run([sys.executable, "-m", "venv", "--without-pip", ENV], check=True)
site = subprocess.run([PY, "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"],
                      capture_output=True, text=True).stdout.strip().splitlines()[-1]
system_dirs = [p for p in sys.path if p.endswith(("site-packages", "dist-packages")) and os.path.isdir(p)]
with open(os.path.join(site, "_system_packages.pth"), "w") as f:
    f.write("\n".join(system_dirs) + "\n")   # after the env's own folder, so its pinned versions win
subprocess.run([sys.executable, "-m", "pip", "--python", PY, "install", "-q", "soundfile",
                "git+https://github.com/huggingface/parler-tts.git"], check=True)
if not works():
    sys.exit("The voice environment could not be set up; send the error above to Claude.")
