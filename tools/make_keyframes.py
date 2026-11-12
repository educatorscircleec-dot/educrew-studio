"""Step 1: photoreal still image (keyframe) for every shot. Free model: RealVisXL (SDXL).
Rear views and no faces keep characters consistent; fixed seeds make results repeatable."""
import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from common import args, fill, path, skip

a, ep, work, shots = args("Make keyframes", lambda ap: (
    ap.add_argument("--seed", type=int, default=1990),
    ap.add_argument("--model", default="SG161222/RealVisXL_V5.0"),
    ap.add_argument("--steps", type=int, default=30)))

pipe = StableDiffusionXLPipeline.from_pretrained(a.model, torch_dtype=torch.float16, variant="fp16")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
pipe.enable_model_cpu_offload()

for s in shots:
    out = path(work, "keyframes", f"shot{s['id']:02d}.png")
    if skip(out, a.force):
        continue
    prompt = fill(s["image"], ep) + ", " + ep["style"]
    print(f"shot {s['id']}: {prompt[:90]}...")
    img = pipe(prompt=prompt, negative_prompt=ep["negative"], width=768, height=1344,
               num_inference_steps=a.steps, guidance_scale=5.0,
               generator=torch.Generator("cpu").manual_seed(a.seed + s["id"])).images[0]
    img.save(out)
print("Keyframes done. Look at them; redo any with: --shots N --force --seed <another number>")
