"""Step 2: animate each keyframe into a short video clip. Free model: Wan 2.2 TI2V-5B (Apache 2.0).
Slow on free GPUs: run a few shots per session with --shots; finished clips are skipped."""
import os
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")  # less memory fragmentation
import gc
import time
import torch
from PIL import Image
from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
from diffusers.utils import export_to_video
from common import args, fill, path, skip

a, ep, work, shots = args("Make video clips", lambda ap: (
    ap.add_argument("--model", default="Wan-AI/Wan2.2-TI2V-5B-Diffusers"),
    # defaults sized for a free 16 GB T4; on a 24 GB+ GPU try --width 704 --height 1280 --frames 121 --fps 24
    ap.add_argument("--width", type=int, default=480),
    ap.add_argument("--height", type=int, default=832),
    ap.add_argument("--frames", type=int, default=81, help="4k+1; 81 frames at 16 fps = 5 s"),
    ap.add_argument("--fps", type=int, default=16),
    ap.add_argument("--steps", type=int, default=30),
    ap.add_argument("--offload", choices=["model", "sequential"], default="model",
                    help="sequential = much less GPU memory, but slower"),
    ap.add_argument("--seed", type=int, default=1990)))

todo = [s for s in shots if a.force or not os.path.exists(os.path.join(work, "clips", f"shot{s['id']:02d}.mp4"))]
if not todo:
    print("All clips already exist; nothing to make. (Use --shots N --force to redo one.)")
    raise SystemExit(0)

# T4 (compute 7.5) has no native bfloat16; emulating it is very slow, so use float16 there
dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16
NEG = ep["negative"] + ", static, frozen"


def ram():
    try:
        import psutil
        return f"RAM used {psutil.virtual_memory().used / 1e9:.1f} GB"
    except Exception:
        return ""


# Phase 1: read every shot's text with the big text model, then unload it.
# Holding the text model (~11 GB) and the video model (~10 GB) in memory together
# is more than a free Kaggle machine has, and the process gets silently killed.
print(f"Phase 1/2: reading the prompts for {len(todo)} shot(s)... {ram()}")
tp = WanImageToVideoPipeline.from_pretrained(a.model, transformer=None, torch_dtype=dtype)
tp.text_encoder.to("cuda")
embeds = {}
with torch.no_grad():
    for s in todo:
        prompt = fill(s["image"], ep) + ". " + s["motion"] + ". " + ep["style"]
        pe, ne = tp.encode_prompt(prompt=prompt, negative_prompt=NEG, do_classifier_free_guidance=True,
                                  max_sequence_length=512, device="cuda", dtype=dtype)
        embeds[s["id"]] = (pe.cpu(), ne.cpu())
del tp
gc.collect()
torch.cuda.empty_cache()

# Phase 2: load the video model without the text model and animate.
print(f"Phase 2/2: loading the video model... {ram()}")
vae = AutoencoderKLWan.from_pretrained(a.model, subfolder="vae", torch_dtype=torch.float32)
pipe = WanImageToVideoPipeline.from_pretrained(a.model, vae=vae, text_encoder=None, tokenizer=None,
                                               torch_dtype=dtype)
if a.offload == "sequential":
    pipe.enable_sequential_cpu_offload()
else:
    pipe.enable_model_cpu_offload()
if hasattr(pipe.vae, "enable_tiling"):
    pipe.vae.enable_tiling()

for s in todo:
    out = path(work, "clips", f"shot{s['id']:02d}.mp4")
    key = path(work, "keyframes", f"shot{s['id']:02d}.png")
    image = Image.open(key).convert("RGB").resize((a.width, a.height))
    pe, ne = embeds[s["id"]]
    print(f"shot {s['id']}: animating at {a.width}x{a.height}, {a.frames} frames... {ram()}")
    t0 = time.time()
    frames = pipe(image=image, prompt_embeds=pe.to("cuda"), negative_prompt_embeds=ne.to("cuda"),
                  width=a.width, height=a.height, num_frames=a.frames,
                  num_inference_steps=a.steps, guidance_scale=5.0,
                  generator=torch.Generator("cpu").manual_seed(a.seed + s["id"])).frames[0]
    export_to_video(frames, out, fps=a.fps)
    print(f"  shot {s['id']} done in {(time.time() - t0) / 60:.1f} min")
    del frames
    torch.cuda.empty_cache()
print("[version: free-T4-2phase] Clips done.")
