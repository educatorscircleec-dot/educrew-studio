"""Shared helpers: load an episode file, fill in character descriptions, work folders."""
import argparse, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def args(desc, extra=None):
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument("episode", help="episodes/episodeNN.json")
    ap.add_argument("--work", help="work folder (default work/episodeNN)")
    ap.add_argument("--shots", help="only these shots, e.g. 1,4,9")
    ap.add_argument("--force", action="store_true", help="redo shots that already exist")
    if extra:
        extra(ap)
    a = ap.parse_args()
    ep = json.load(open(a.episode, encoding="utf-8"))
    name = os.path.splitext(os.path.basename(a.episode))[0]
    work = a.work or os.path.join(ROOT, "work", name)
    want = {int(x) for x in a.shots.split(",")} if a.shots else None
    shots = [s for s in ep["shots"] if want is None or s["id"] in want]
    return a, ep, work, shots


def fill(text, ep):
    """Replace {GIRL}, {MOTHER}, ... with the locked character descriptions."""
    return re.sub(r"\{(\w+)\}", lambda m: ep["characters"].get(m.group(1), m.group(0)), text)


def path(work, kind, name):
    d = os.path.join(work, kind)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def skip(p, force):
    if os.path.exists(p) and not force:
        print(f"  exists, skipping: {os.path.basename(p)}  (use --force to redo)")
        return True
    return False
