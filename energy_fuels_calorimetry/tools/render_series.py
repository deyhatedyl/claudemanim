"""Render several episodes with one bounded worker pool and isolated movie files.

python tools/render_series.py E04 E05 --still -q h
python tools/render_series.py E04 E05 -q m --jobs 3

Finished clips are copied into the usual Manim media directory. Keeping ffmpeg's
active files in a temporary directory avoids interference from workspace sync.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.render import MANIM, QUALITY, episode_scenes


def render(ep, cls, quality, still=False):
    args, tag = QUALITY[quality]
    log = ROOT / "logs" / f"render_{cls}_{tag}{'_still' if still else ''}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f"chemistry-{cls}-") as tmp:
        cmd = [MANIM, *args, "--disable_caching", "--media_dir", tmp,
               "--progress_bar", "none", str(ROOT / "scenes" / f"ep{ep[1:]}.py"), cls]
        if still:
            cmd[1:1] = ["-s", "--format", "png"]
        with log.open("w") as fh:
            rc = subprocess.call(cmd, cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT)
        if rc == 0:
            if still:
                images = list((Path(tmp) / "images").rglob("*.png"))
                if images:
                    target = ROOT / "checks" / "scene_stills" / tag
                    target.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(images[-1], target / f"{cls}.png")
            else:
                source = Path(tmp) / "videos" / f"ep{ep[1:]}" / tag / f"{cls}.mp4"
                if not source.exists():
                    rc = 1
                else:
                    target = ROOT / "renders" / "media" / "videos" / f"ep{ep[1:]}" / tag
                    target.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target / source.name)
    return {"scene": cls, "episode": ep, "ok": rc == 0,
            "seconds": round(time.monotonic() - started, 1), "log": str(log)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("-q", "--quality", choices=QUALITY, default="m")
    ap.add_argument("--still", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--scenes", nargs="*")
    a = ap.parse_args()
    jobs = [(ep.upper(), cls) for ep in a.episodes for cls in episode_scenes(ep.upper())
            if not a.scenes or cls.split("_")[0] in a.scenes]
    if not jobs:
        ap.error("No scenes selected")
    report = ROOT / "checks" / f"series_render_{QUALITY[a.quality][1]}{'_still' if a.still else ''}.json"
    results = []
    with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        futures = [ex.submit(render, ep, cls, a.quality, a.still) for ep, cls in jobs]
        for f in cf.as_completed(futures):
            r = f.result()
            results.append(r)
            print(f"{'OK' if r['ok'] else 'ERROR'} {r['scene']} {r['seconds']:.0f}s "
                  f"({len(results)}/{len(jobs)})", flush=True)
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps(results, indent=2) + "\n")
    raise SystemExit(0 if all(r["ok"] for r in results) else 1)


if __name__ == "__main__":
    main()
