#!/usr/bin/env python3
"""
EduCrew Studio: assemble an episode from generated parts into one finished video.

Expects (inside --work, default work/episodeNN):
  keyframes/shotNN.png     still image for each shot     (from step 1)
  clips/shotNN.mp4         AI video clip for each shot   (from step 2; optional)
  voice/shotNN_K.wav       spoken line K of shot NN      (from step 3)
  sfx/shotNN.wav           sound effects for the shot    (from step 4; optional)

If a shot has no clip, its keyframe is used with a slow cinematic push-in instead.

Usage:  python assemble.py episodes/<name>.json [--work DIR] [-o out.mp4]
Output: output/EduCrew_<name>.mp4
"""
import argparse, json, os, subprocess, sys


def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-2000:])


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def build_shot(shot, ep, work, out):
    W, H, fps, d = ep["width"], ep["height"], ep["fps"], shot["duration"]
    n = f"shot{shot['id']:02d}"
    clip = os.path.join(work, "clips", n + ".mp4")
    key = os.path.join(work, "keyframes", n + ".png")
    fill = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    if os.path.exists(clip):
        src = duration(clip)
        stretch = max(1.0, d / src) if src else 1.0  # gently slow a short clip to fill the shot
        if stretch > 1.6:
            print(f"  ! {n}: clip is {src:.1f}s for a {d}s shot (slowed {stretch:.2f}x)")
        vf = f"setpts={stretch:.4f}*PTS,{fill},fps={fps}"
        cmd = ["ffmpeg", "-y", "-i", clip]
        print(f"  {n}: AI clip ({src:.1f}s)")
    elif os.path.exists(key):
        frames = int(d * fps)
        vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
              f"zoompan=z='1+0.08*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d={frames}:s={W}x{H}:fps={fps},setsar=1")
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", key]
        print(f"  {n}: keyframe with slow push-in (no clip found)")
    else:
        sys.exit(f"Missing both {clip} and {key}")
    run(cmd + ["-vf", vf, "-t", f"{d}", "-an", "-c:v", "libx264", "-preset", "medium",
               "-crf", "18", "-pix_fmt", "yuv420p", out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--work")
    ap.add_argument("-o", "--output")
    ap.add_argument("--sfx-volume", type=float, default=0.45)
    a = ap.parse_args()

    ep = json.load(open(a.episode, encoding="utf-8"))
    name = os.path.splitext(os.path.basename(a.episode))[0]
    root = os.path.dirname(os.path.abspath(__file__))
    work = a.work or os.path.join(root, "work", name)
    out = a.output or os.path.join(root, "output", (name if name.startswith("EduCrew") else f"EduCrew_{name}") + ".mp4")
    os.makedirs(os.path.join(work, "_parts"), exist_ok=True)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    # 1. video: one normalised part per shot, then join
    print("Building video...")
    parts, starts, t = [], [], 0.0
    for s in ep["shots"]:
        p = os.path.join(work, "_parts", f"shot{s['id']:02d}.mp4")
        build_shot(s, ep, work, p)
        parts.append(p); starts.append(t); t += s["duration"]
    total = t
    lst = os.path.join(work, "_parts", "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    video = os.path.join(work, "_parts", "video.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])

    # 2. audio: place every voice line and sound effect on the timeline
    print("Mixing audio...")
    inputs, chains = [], []
    busy_until = 0.0  # spoken lines never overlap: a line waits for the previous one to finish
    for s, st in zip(ep["shots"], starts):
        n = f"shot{s['id']:02d}"
        fx = os.path.join(work, "sfx", n + ".wav")
        if os.path.exists(fx):
            inputs.append(fx)
            i = len(inputs)
            chains.append(f"[{i}:a]atrim=0:{s['duration']},afade=t=in:d=0.3,"
                          f"afade=t=out:st={max(0, s['duration'] - 0.4)}:d=0.4,"
                          f"volume={a.sfx_volume},adelay={int(st * 1000)}:all=1[a{i}]")
        for k, line in enumerate(s.get("lines", []), 1):
            v = os.path.join(work, "voice", f"{n}_{k}.wav")
            if not os.path.exists(v):
                print(f"  ! missing voice line: {v}")
                continue
            vd = duration(v)
            begin = max(st + line["at"], busy_until + 0.3)
            busy_until = begin + vd
            if busy_until > st + s["duration"] + 1.5:
                print(f"  ! {n} line {k} runs {busy_until - st - s['duration']:.1f}s past its shot "
                      f"(make the shot longer in the episode file)")
            inputs.append(v)
            i = len(inputs)
            chains.append(f"[{i}:a]adelay={int(begin * 1000)}:all=1[a{i}]")
    labels = "".join(f"[a{i}]" for i in range(1, len(inputs) + 1))
    graph = ";".join(chains)
    if inputs:
        graph += f";{labels}amix=inputs={len(inputs)}:normalize=0:duration=longest,"
    else:
        graph = "anullsrc=r=48000:cl=stereo,"
    graph += f"apad,atrim=0:{total},aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-16:TP=-1.5[aout]"

    if busy_until > total:
        print(f"  ! speech runs {busy_until - total:.1f}s past the end of the video")

    # 3. logo: fixed lower-right for the whole episode; optional large brand reveal at the end
    logo = os.path.join(root, ep.get("logo", ""))
    reveal = ep.get("brand_reveal")
    vchain = "[0:v]fade=t=in:d=0.6,fade=t=out:st={:.2f}:d=0.8[base]".format(total - 0.8)
    loop_inputs = set()
    if os.path.exists(logo):
        inputs.append(logo)
        li = len(inputs)
        loop_inputs.add(li)
        lw, m = int(ep["width"] * 0.14), int(ep["width"] * 0.04)
        if reveal:
            t0 = total - reveal.get("seconds", 5)
            big = int(ep["width"] * reveal.get("width", 0.6))
            vchain += (f";[{li}:v]split[l1][l2];[l1]scale={lw}:-1,format=rgba,colorchannelmixer=aa=0.9[logo];"
                       f"[l2]scale={big}:-1,format=rgba,fade=t=in:st={t0}:d=1.2:alpha=1[biglogo];"
                       f"[base]drawbox=x=0:y=0:w=iw:h=ih:color=black@0.35:t=fill:enable='gte(t,{t0})'[dim];"
                       f"[dim][logo]overlay=W-w-{m}:H-h-{m}:enable='lt(t,{t0})'[v1];"
                       f"[v1][biglogo]overlay=(W-w)/2:(H-h)/2:enable='gte(t,{t0})'[vout]")
        else:
            vchain += (f";[{li}:v]scale={lw}:-1,format=rgba,colorchannelmixer=aa=0.9[logo];"
                       f"[base][logo]overlay=W-w-{m}:H-h-{m}[vout]")
    else:
        print(f"  ! logo not found at {logo}: exporting without it")
        vchain += ";[base]null[vout]"

    cmd = ["ffmpeg", "-y", "-i", video]
    for i, p in enumerate(inputs, 1):
        cmd += (["-loop", "1", "-framerate", str(ep["fps"])] if i in loop_inputs else []) + ["-i", p]
    cmd += ["-filter_complex", vchain + ";" + graph, "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total}", out]
    print("Rendering final video...")
    run(cmd)
    print(f"Done -> {out}  ({duration(out):.1f}s)")


if __name__ == "__main__":
    main()
