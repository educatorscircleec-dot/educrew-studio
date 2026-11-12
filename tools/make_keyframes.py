"""Step 1: one still image (keyframe) for every shot.

Consistency features:
- {NAME} placeholders are replaced with the locked character descriptions.
- "ref": a shot can name a character reference image (from the character bible).
  It is fed to the model through IP-Adapter, so the character keeps the same look.
- "continue_from": the first shot of an episode can start from the previous episode's
  last keyframe, so each episode picks up from the previous final moment.
- Fixed seeds make results repeatable; redo a weak shot with --shots N --force --seed X.
"""
import os
import torch
from PIL import Image
from diffusers import AutoPipelineForImage2Image, DPMSolverMultistepScheduler, StableDiffusionXLPipeline
from compel import Compel, ReturnedEmbeddingsType
from common import ROOT, args, fill, path, skip

a, ep, work, shots = args("Make keyframes", lambda ap: (
    ap.add_argument("--seed", type=int, default=1990),
    ap.add_argument("--steps", type=int, default=32),
    ap.add_argument("--ref-strength", type=float, default=0.55, help="how strongly to copy the character reference")))

model = ep.get("image_model", "stabilityai/stable-diffusion-xl-base-1.0")
W, H = ep.get("key_width", 768), ep.get("key_height", 1344)
pipe = StableDiffusionXLPipeline.from_pretrained(model, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)


def ref_path(name):
    p = ep.get("refs", {}).get(name)
    return os.path.join(ROOT, p) if p else None


use_refs = any(s.get("ref") and ref_path(s["ref"]) and os.path.exists(ref_path(s["ref"])) for s in shots)
if use_refs:
    pipe.load_ip_adapter("h94/IP-Adapter", subfolder="sdxl_models", weight_name="ip-adapter_sdxl.bin")
pipe.to("cuda")  # SDXL fits on a 16 GB T4
img2img = AutoPipelineForImage2Image.from_pipe(pipe)
blank = Image.new("RGB", (224, 224), (128, 128, 128))
# Compel lets prompts run past SDXL's 77-token limit, so character descriptions are never cut off
compel = Compel(tokenizer=[pipe.tokenizer, pipe.tokenizer_2], text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
                returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
                requires_pooled=[False, True], truncate_long_prompts=False)

for s in shots:
    out = path(work, "keyframes", f"shot{s['id']:02d}.png")
    if skip(out, a.force):
        continue
    prompt = fill(s["image"], ep) + ", " + ep["style"]
    cond, pooled = compel(prompt)
    ncond, npooled = compel(ep["negative"])
    cond, ncond = compel.pad_conditioning_tensors_to_same_length([cond, ncond])
    kw = dict(prompt_embeds=cond, pooled_prompt_embeds=pooled, negative_prompt_embeds=ncond,
              negative_pooled_prompt_embeds=npooled, num_inference_steps=a.steps,
              guidance_scale=6.0, generator=torch.Generator("cpu").manual_seed(a.seed + s["id"]))

    if use_refs:
        rp = ref_path(s.get("ref", ""))
        if rp and os.path.exists(rp):
            pipe.set_ip_adapter_scale(a.ref_strength)
            kw["ip_adapter_image"] = Image.open(rp).convert("RGB")
            print(f"  using character reference {s['ref']}")
        else:
            pipe.set_ip_adapter_scale(0.0)
            kw["ip_adapter_image"] = blank

    start = s.get("continue_from")
    start_img = os.path.join(ROOT, start) if start else None
    if start_img and os.path.exists(start_img):
        print(f"shot {s['id']}: continuing from {start}")
        init = Image.open(start_img).convert("RGB").resize((W, H))
        img = img2img(image=init, strength=s.get("continue_strength", 0.6), **kw).images[0]
    else:
        if start:
            print(f"  ! {start} not made yet: shot {s['id']} starts fresh")
        print(f"shot {s['id']}: {s['image'][:80]}...")
        img = pipe(width=W, height=H, **kw).images[0]
    img.save(out)
print("Keyframes done. Look at them; redo any with: --shots N --force --seed <another number>")
