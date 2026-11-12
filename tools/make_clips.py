"""Step 2: animate each keyframe into a short video clip. Free model: Wan 2.2 TI2V-5B (Apache 2.0).
Slow on free GPUs: run a few shots per session with --shots; finished clips are skipped."""
import torch
from PIL import Image
from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
from diffusers.utils import export_to_video
from common import args, fill, path, skip

a, ep, work, shots = args("Make video clips", lambda ap: (
    ap.add_argument("--model", default="Wan-AI/Wan2.2-TI2V-5B-Diffusers"),
    ap.add_argument("--width", type=int, default=704),
    ap.add_argument("--height", type=int, default=1280),
    ap.add_argument("--frames", type=int, default=121, help="4k+1; 121 = 5 s at 24 fps"),
    ap.add_argument("--steps", type=int, default=30),
    ap.add_argument("--seed", type=int, default=1990)))

dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
vae = AutoencoderKLWan.from_pretrained(a.model, subfolder="vae", torch_dtype=torch.float32)
pipe = WanImageToVideoPipeline.from_pretrained(a.model, vae=vae, torch_dtype=dtype)
pipe.enable_model_cpu_offload()
if hasattr(pipe.vae, "enable_tiling"):
    pipe.vae.enable_tiling()

for s in shots:
    out = path(work, "clips", f"shot{s['id']:02d}.mp4")
    if skip(out, a.force):
        continue
    key = path(work, "keyframes", f"shot{s['id']:02d}.png")
    image = Image.open(key).convert("RGB").resize((a.width, a.height))
    prompt = fill(s["image"], ep) + ". " + s["motion"] + ". " + ep["style"]
    print(f"shot {s['id']}: animating...")
    frames = pipe(image=image, prompt=prompt, negative_prompt=ep["negative"] + ", static, frozen",
                  width=a.width, height=a.height, num_frames=a.frames,
                  num_inference_steps=a.steps, guidance_scale=5.0,
                  generator=torch.Generator("cpu").manual_seed(a.seed + s["id"])).frames[0]
    export_to_video(frames, out, fps=24)
    torch.cuda.empty_cache()
print("Clips done.")
