"""Step 3: speak every narration and dialogue line, word for word.
Free model: Indic Parler-TTS (Apache 2.0) by AI4Bharat, with natural Indian English voices.
Voices are set in the episode file ("voices"); keep the same text and seed in every episode."""
import torch, soundfile as sf
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
from common import args, path, skip

a, ep, work, shots = args("Make voices", lambda ap: ap.add_argument("--seed", type=int, default=7))
dev = "cuda" if torch.cuda.is_available() else "cpu"
name = "ai4bharat/indic-parler-tts"
model = ParlerTTSForConditionalGeneration.from_pretrained(name).to(dev)
tok = AutoTokenizer.from_pretrained(name)
dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

for s in shots:
    for k, line in enumerate(s.get("lines", []), 1):
        out = path(work, "voice", f"shot{s['id']:02d}_{k}.wav")
        if skip(out, a.force):
            continue
        desc = ep["voices"][line["speaker"]]
        spoken = line.get("tts_text", line["text"])  # tts_text = same words, spelt for pronunciation
        print(f"shot {s['id']} {line['speaker']}: {line['text']}")
        torch.manual_seed(a.seed)
        d = dtok(desc, return_tensors="pt").to(dev)
        p = tok(spoken, return_tensors="pt").to(dev)
        audio = model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask,
                               prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask)
        sf.write(out, audio.cpu().numpy().squeeze(), model.config.sampling_rate)
print("Voices done. Listen to them; redo any with --shots N --force --seed <another number>")
