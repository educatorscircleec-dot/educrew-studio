# Making a new video

Every video is one file in the `episodes/` folder. To make a new one:

## Option A: ask Claude (easiest)
Send Claude your story, narration and dialogue, like you did for Episode 1.
Claude writes the new episode file (e.g. `episodes/episode02.json`) and adds it to GitHub.

## Option B: write it yourself on GitHub
1. Open `episodes/_TEMPLATE.json` on GitHub, copy all of it.
2. Go to the `episodes` folder, then **Add file → Create new file**. Name it, e.g. `episode02.json`, paste, and fill in the shots.
3. Click **Commit changes**.

## Then make it on Kaggle
1. Open your EduCrew Studio notebook.
2. In the first code cell, change one line:
   ```
   EPISODE = "episodes/episode02.json"
   ```
3. Run all cells. The finished video appears as `output/EduCrew_episode02.mp4`.

## Rules that keep the series consistent
- Keep `style`, `negative`, `characters`, `voices` and `logo` exactly the same in every EduCrew episode.
- Write shot pictures with `{GIRL}`, `{MOTHER}`, `{FATHER}`, `{BROTHER}`, `{GRANDMOTHER}`, `{HOME}`.
  They are replaced with the locked character descriptions automatically.
- Describe people seen from behind, hands, or silhouettes: no faces.
- All shot durations added together = the video length (60 for a Reel).
- For a completely different video (not the series), you can change `characters` and `voices` freely.
