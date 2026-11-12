"""Step 2: animate each keyframe into a short video clip. Free model: Wan 2.2 TI2V-5B (Apache 2.0).

Built for free Kaggle (2 x T4 16 GB, ~29 GB RAM):
- Phase 1 reads every shot's text with the big text model, saves the result, and unloads it.
  (Text model ~11 GB + video model ~10 GB together would exceed the RAM and get killed.)
- Phase 2 uses BOTH GPUs at once: shots are split between them, roughly halving the time.
Finished clips are skipped, so it is safe to re-run after a session ends.
"""
import os
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")  # less memory fragmentation
import gc
import subprocess
import sys
import time
import torch
from PIL import Image
from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
from diffusers.utils import export_to_video
from common import args, fill, path

a, ep, work, shots = args("Make video clips", lambda ap: (
    # defaults sized for a free 16 GB T4; on a 24 GB+ GPU try --width 704 --height 1280 --frames 121 --fps 24
    ap.add_argument("--model", default="Wan-AI/Wan2.2-TI2V-5B-Diffusers"),
    ap.add_argument("--width", type=int, default=480),
    ap.add_argument("--height", type=int, default=832),
    ap.add_argument("--frames", type=int, default=81, help="4k+1; 81 frames at 16 fps = 5 s"),
    ap.add_argument("--fps", type=int, default=16),
    ap.add_argument("--steps", type=int, default=30, help="fewer = faster but rougher (try 20)"),
    ap.add_argument("--gpus", type=int, default=0, help="how many GPUs to use (0 = all)"),
    ap.add_argument("--offload", choices=["none", "model", "sequential"], default="none",
                    help="none = fastest; model / sequential use less GPU memory but are slower"),
    ap.add_argument("--seed", type=int, default=1990),
    ap.add_argument("--worker", type=int, default=-1, help="(internal)"),
    ap.add_argument("--of", type=int, default=1, help="(internal)")))

clip_path = lambda s: os.path.join(work, "clips", f"shot{s['id']:02d}.mp4")
emb_path = lambda s: path(work, "_embeds", f"shot{s['id']:02d}.pt")
todo = [s for s in shots if a.force or not os.path.exists(clip_path(s))]
dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16  # T4: no native bf16


def ram():
    try:
        import psutil
        return f"(RAM used {psutil.virtual_memory().used / 1e9:.1f} GB)"
    except Exception:
        return ""


def animate(my_shots, tag):
    """Load the video model (without the text model) and animate the given shots."""
    print(f"{tag} loading the video model for shots {[s['id'] for s in my_shots]} {ram()}", flush=True)
    vae = AutoencoderKLWan.from_pretrained(a.model, subfolder="vae", torch_dtype=torch.float32)
    pipe = WanImageToVideoPipeline.from_pretrained(a.model, vae=vae, text_encoder=None, tokenizer=None,
                                                   torch_dtype=dtype)
    if a.offload == "sequential":
        pipe.enable_sequential_cpu_offload()
    elif a.offload == "model":
        pipe.enable_model_cpu_offload()
    else:
        pipe.to("cuda")
        gc.collect()  # release the CPU copy so two workers fit in RAM
    pipe.vae.enable_tiling()
    for s in my_shots:
        image = Image.open(path(work, "keyframes", f"shot{s['id']:02d}.png")).convert("RGB").resize((a.width, a.height))
        pe, ne = torch.load(emb_path(s))
        print(f"{tag} shot {s['id']}: animating at {a.width}x{a.height}, {a.frames} frames... {ram()}", flush=True)
        t0 = time.time()
        frames = pipe(image=image, prompt_embeds=pe.to("cuda"), negative_prompt_embeds=ne.to("cuda"),
                      width=a.width, height=a.height, num_frames=a.frames,
                      num_inference_steps=a.steps, guidance_scale=5.0,
                      generator=torch.Generator("cpu").manual_seed(a.seed + s["id"])).frames[0]
        export_to_video(frames, clip_path(s), fps=a.fps)
        print(f"{tag} shot {s['id']} done in {(time.time() - t0) / 60:.1f} min", flush=True)
        del frames
        torch.cuda.empty_cache()


# ---- worker process (one per GPU, started by the main process) ----
if a.worker >= 0:
    time.sleep(a.worker * 120)  # stagger loading so both workers don't peak in RAM together
    animate(todo[a.worker::a.of], f"[GPU {a.worker}]")
    raise SystemExit(0)

# ---- main process ----
if not todo:
    print("All clips already exist; nothing to make. (Use --shots N --force to redo one.)")
    raise SystemExit(0)
os.makedirs(os.path.join(work, "clips"), exist_ok=True)

print(f"Phase 1/2: reading the prompts for shots {[s['id'] for s in todo]}... {ram()}", flush=True)
NEG = ep["negative"] + ", static, frozen"
tp = WanImageToVideoPipeline.from_pretrained(a.model, transformer=None, torch_dtype=dtype)
tp.text_encoder.to("cuda")
with torch.no_grad():
    for s in todo:
        prompt = fill(s["image"], ep) + ". " + s["motion"] + ". " + ep["style"]
        pe, ne = tp.encode_prompt(prompt=prompt, negative_prompt=NEG, do_classifier_free_guidance=True,
                                  max_sequence_length=512, device="cuda", dtype=dtype)
        torch.save((pe.cpu(), ne.cpu()), emb_path(s))
del tp
gc.collect()
torch.cuda.empty_cache()

n = min(a.gpus or torch.cuda.device_count(), len(todo))
print(f"Phase 2/2: animating {len(todo)} shot(s) on {n} GPU(s)... {ram()}", flush=True)
t_all = time.time()
if n <= 1:
    animate(todo, "[GPU 0]")
else:
    passthrough = ["--work", work, "--shots", ",".join(str(s["id"]) for s in todo), "--model", a.model,
                   "--width", str(a.width), "--height", str(a.height), "--frames", str(a.frames),
                   "--fps", str(a.fps), "--steps", str(a.steps), "--offload", a.offload, "--seed", str(a.seed)]
    if a.force:
        passthrough.append("--force")
    procs = []
    for k in range(n):
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(k))
        procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), a.episode, *passthrough,
                                       "--worker", str(k), "--of", str(n)], env=env))
    codes = [p.wait() for p in procs]
    if any(codes):
        missing = [s["id"] for s in todo if not os.path.exists(clip_path(s))]
        sys.exit(f"A GPU worker failed (exit codes {codes}). Missing clips: {missing}. "
                 f"Re-run to retry them, or add --gpus 1 --offload model if memory ran out.")
print(f"[version: 2gpu] Clips done in {(time.time() - t_all) / 60:.1f} min.")
