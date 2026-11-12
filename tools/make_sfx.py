"""Step 4: realistic sound effects for every shot, matched to what is on screen. No music.
Free model: MMAudio (github.com/hkchengrex/MMAudio), run straight from its folder (--mmaudio).

- The model is loaded once for all shots (much faster than once per shot).
- Each clip is first stretched to its shot length, exactly as the final edit shows it,
  so the sounds stay in sync.
- Audio is saved with soundfile, avoiding torchaudio.save (needs torchcodec on new torch).
"""
import os
import subprocess
import sys
import time
from pathlib import Path
from common import args, path

a, ep, work, shots = args("Make sound effects", lambda ap: (
    ap.add_argument("--mmaudio", default="/kaggle/working/MMAudio", help="path to the MMAudio repo"),
    ap.add_argument("--variant", default="large_44k_v2"),
    ap.add_argument("--steps", type=int, default=25),
    ap.add_argument("--seed", type=int, default=42)))

out_path = lambda s: os.path.join(work, "sfx", f"shot{s['id']:02d}.wav")
todo = [s for s in shots if a.force or not os.path.exists(out_path(s))]
if not todo:
    print("All sound effects already exist; nothing to make. (Use --shots N --force to redo one.)")
    raise SystemExit(0)

sys.path.insert(0, os.path.abspath(a.mmaudio))
import soundfile as sf
import torch
from mmaudio.eval_utils import all_model_cfg, generate, load_video, setup_eval_logging
from mmaudio.model.flow_matching import FlowMatching
from mmaudio.model.networks import get_my_mmaudio
from mmaudio.model.utils.features_utils import FeaturesUtils

setup_eval_logging()
os.makedirs(os.path.join(work, "sfx"), exist_ok=True)
dev = "cuda"
dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float32  # T4: no native bf16
cfg = all_model_cfg[a.variant]
cwd = os.getcwd()
os.chdir(a.mmaudio)  # MMAudio downloads its weights relative to its own folder
cfg.download_if_needed()
seq_cfg = cfg.seq_cfg
net = get_my_mmaudio(cfg.model_name).to(dev, dtype).eval()
net.load_weights(torch.load(cfg.model_path, map_location=dev, weights_only=True))
feats = FeaturesUtils(tod_vae_ckpt=cfg.vae_path, synchformer_ckpt=cfg.synchformer_ckpt, enable_conditions=True,
                      mode=cfg.mode, bigvgan_vocoder_ckpt=cfg.bigvgan_16k_path,
                      need_vae_encoder=False).to(dev, dtype).eval()
os.chdir(cwd)
NEG = "music, melody, singing, song, speech, talking, voice, instruments"

with torch.inference_mode():
    for s in todo:
        t0 = time.time()
        clip = os.path.join(work, "clips", f"shot{s['id']:02d}.mp4")
        clip_frames = sync_frames = None
        duration = float(s["duration"])
        if os.path.exists(clip):
            # stretch the clip to the shot length, the same way the final edit does
            src = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                        "csv=p=0", clip], capture_output=True, text=True).stdout.strip() or 0)
            stretched = path(work, "_sfx_tmp", f"shot{s['id']:02d}.mp4")
            factor = max(1.0, duration / src) if src else 1.0
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", f"setpts={factor:.4f}*PTS,fps=25",
                            "-an", "-t", str(duration), stretched], check=True)
            info = load_video(Path(stretched), duration)
            clip_frames, sync_frames = info.clip_frames.unsqueeze(0), info.sync_frames.unsqueeze(0)
            duration = info.duration_sec
            mode = "matched to the clip"
        else:
            mode = "from the description only (no clip yet)"
        seq_cfg.duration = duration
        net.update_seq_lengths(seq_cfg.latent_seq_len, seq_cfg.clip_seq_len, seq_cfg.sync_seq_len)
        rng = torch.Generator(device=dev).manual_seed(a.seed + s["id"])
        fm = FlowMatching(min_sigma=0, inference_mode="euler", num_steps=a.steps)
        audio = generate(clip_frames, sync_frames, [s["sfx"]], negative_text=[NEG], feature_utils=feats, net=net,
                         fm=fm, rng=rng, cfg_strength=4.5)
        wav = audio.float().cpu()[0].numpy()  # (channels, samples)
        sf.write(out_path(s), wav.T if wav.ndim == 2 else wav, seq_cfg.sampling_rate)
        print(f"shot {s['id']}: sound {mode}, {duration:.1f}s, in {time.time() - t0:.0f}s", flush=True)
print("[version: sfx-v2] Sound effects done.")
