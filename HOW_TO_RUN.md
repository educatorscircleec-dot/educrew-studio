# How to make the EduCrew videos (full process)

Everything is free. You need a computer with a web browser (a phone is too small for this).
In total: about 15 minutes of setup once, then roughly 2–3 Kaggle sessions per episode.

---

## Part A: one-time setup

### A1. Kaggle account (gives you a free GPU)
1. Go to https://www.kaggle.com and **Register** (signing up with Google is easiest).
2. Click your profile picture (top right), then **Settings**.
3. Find **Phone verification** and verify your mobile number.
   Without this, Kaggle won't give you a GPU or internet.

### A2. Hugging Face account (needed for the free Indian voice)
1. Go to https://huggingface.co/join and create an account. Confirm your email.
2. Open https://huggingface.co/ai4bharat/indic-parler-tts and click **Agree and access repository**.
3. Open https://huggingface.co/settings/tokens, then **Create new token**. Choose **Read**, name it `kaggle`, click **Create**.
4. **Copy the token** (it starts with `hf_`). Keep it private.

### A3. Create your EduCrew notebook on Kaggle
1. On Kaggle, click **+ Create**, then **New Notebook**.
2. In the notebook menu, choose **File**, then **Import Notebook**. Open the **GitHub** tab and paste:
   `https://github.com/educatorscircleec-dot/educrew-studio/blob/main/EduCrew_Studio_Kaggle.ipynb`
   Click **Import**.
3. Rename the notebook (click the title at the top left) to **EduCrew Studio**.

### A4. Notebook settings (right-hand panel; click **>** to open it if hidden)
1. **Session options**, then **Accelerator**: choose **GPU T4 x2**.
2. **Internet**: turn it **on**.
3. **Persistence** (if shown): choose **Files only**. This keeps your progress between sessions.
4. **Add-ons**, then **Secrets**, then **Add Secret**:
   - Label: `HF_TOKEN`
   - Value: paste your Hugging Face token. Save it, and make sure its checkbox is **ticked**.

The setup is now done. The EduCrew logo is already in the project, so you don't need to upload it.

---

## Part B: make the character pictures (once, about 20 minutes)

These pictures keep the girl, her mother, father and children looking the same in every episode.

1. Click **Start session** (or the power button) at the top. Wait until it shows the GPU is on.
2. In the **first code cell**, set this line:
   ```
   EPISODE = "episodes/EduCrew_Characters.json"
   ```
3. Run **only these two cells**, one at a time (click inside, then Shift + Enter):
   - **Setup** (first code cell; the first time it installs everything, 3–5 minutes)
   - **Step 1: pictures**
4. The 16 character pictures appear under Step 1. Check them:
   - Same girl, getting older? Teal clothes and mustard dupatta?
   - Modest clothing, an Indian Muslim family, a nice 3D storybook look?
5. **Don't like one?** Use the **Redo one thing** cell at the bottom, for example (picture 3, new attempt):
   ```
   !cd tools && python make_keyframes.py ../$EPISODE --shots 3 --force --seed 77
   ```
   Change the seed number until you like it.
6. Do **not** run Steps 2–5 for the character file.

---

## Part C: make an episode (3 cells)

1. **Setup:** set the episode and run the cell (Shift + Enter):
   ```
   EPISODE = "episodes/EduCrew_Biography_Episode_01.json"
   ```
   It always downloads the latest fixes, installs what's needed, and logs in. It ends with `Ready: …`.
2. **Pictures** (about 10 min): run the cell, then **look at the 10 pictures**.
   To remake a weak one, use the **Redo one shot** cell at the bottom (`--redo 3 --seed 7`).
3. **Everything else** (about 1.5 hours): run the cell. It makes, in order:
   clips (on both GPUs) → voices → sound effects → the final 60-second Reel, and shows it.
   You can switch tabs while it runs; keep the Mac awake (`caffeinate -d` in Terminal).

If it stops, it says which step failed. Send the red lines to Claude, then run the same cell again;
finished parts are kept.

**Download the Reel:** right panel → **Output** → `educrew-studio/output/EduCrew_Biography_Episode_01.mp4` → ⋮ → **Download**.

## Part D: when a session ends (time limits)

Kaggle gives about **30 GPU hours a week**, and a session stops after a while if you're idle.

- **With Persistence set to "Files only"**: just open the notebook again, set the same `EPISODE`, and run
  **Setup**, **Login + install**, then continue with the step you were on. Finished parts are skipped.
- **Without Persistence**: before stopping, run the last cell **Save progress**, then download `work.zip`
  from **Output**. Next time, click **Add Input**, upload `work.zip`, and run **Setup**. It restores everything.

Always click **Stop session** when you're done, to save your weekly GPU hours.

---

## Part E: episodes 2 to 10

Make them **in order**. Each episode starts from the last picture of the episode before it.

1. In **Setup**, change only the number:
   ```
   EPISODE = "episodes/EduCrew_Biography_Episode_02.json"
   ```
2. Run **Setup**, **Pictures** and **Everything else**, as in Part C.
3. Download each finished video, named `EduCrew_Biography_Episode_02.mp4` and so on.

---

## If something goes wrong

| Problem | What to do |
|---|---|
| Red error text in a cell | Copy the **last 10–20 lines** and send them to Claude |
| "CUDA out of memory" in Step 2 | Add `--offload sequential` to the Step 2 command (slower, uses less memory) |
| "401" or "gated repo" error in Step 3 | Check A2 step 2 (Agree and access) and that the `HF_TOKEN` secret is ticked |
| No GPU option | Phone verification isn't done (A1) |
| A shot looks wrong | Redo it with `--shots N --force --seed <new number>` in that step |
| A voice is mispronounced | Tell Claude which line; it can change the pronunciation spelling |

## Posting on Instagram
Upload the `.mp4` as a **Reel**. It's already 9:16, 60 seconds, with sound and logo.
Instagram's buttons and caption cover the bottom-right area while people scroll, so check your logo in the preview.
