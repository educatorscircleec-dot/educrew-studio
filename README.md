# EduCrew Studio

Your own AI video pipeline built entirely from free, open-source models. It has no subscription and no per-video charges.

| Step | What it makes | Free model | Licence |
|---|---|---|---|
| 1 | Photoreal still for each shot | RealVisXL V5 (SDXL) | OpenRAIL++ |
| 2 | Moving video clip from each still | Wan 2.2 TI2V-5B | Apache 2.0 |
| 3 | Narrator and dialogue voices (Indian English) | Indic Parler-TTS (AI4Bharat) | Apache 2.0 |
| 4 | Realistic sound effects, no music | MMAudio | see its repo |
| 5 | Final edit: timing, audio mix, logo | `assemble.py` + ffmpeg | yours |

## Where to run it
- **Free:** on Kaggle (about 30 free GPU hours a week). Go to kaggle.com → **Create → New Notebook → File → Import Notebook**, choose the **GitHub** tab, and paste
  `https://github.com/educatorscircleec-dot/educrew-studio/blob/main/EduCrew_Studio_Kaggle.ipynb`.
  Then follow the steps at the top of the notebook.
- **Your own PC:** needs an NVIDIA GPU with 12 GB or more. Install Python, ffmpeg and the packages from the notebook, then run the same `tools/*.py` commands.

## Making a new video
See `NEW_VIDEO.md`. In short:
1. Copy `episodes/episode01.json` to `episode02.json`.
2. Change only the `shots`: the images, motion, sound effects and lines.
3. **Never change** `characters`, `voices`, `style` or `logo`. That keeps the family, narrator and logo the same across all 10 episodes.

The character designs are in `SERIES_BIBLE.md`. Put the logo at `logo/educrew_logo.png`.

## Honest expectations
- Free GPUs are slow. One 5-second clip can take many minutes. Make a few shots per session and save progress.
- A shot without a video clip still works: the assembler animates its still image with a slow push-in.
- Results vary. Regenerate any weak shot with `--shots N --force --seed <new number>`.

## Licence
The EduCrew Studio code is released under the MIT licence (see `LICENSE`).
Each AI model keeps its own licence. Check them before commercial use, especially the sound-effects model.
