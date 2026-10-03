"""
Render the scenes of one episode (in parallel), then optionally assemble the episode.

    python tools/render.py E01                 # draft: 480p15, all scenes, then assemble
    python tools/render.py E01 -q h            # final: 1080p30 (see QUALITY below)
    python tools/render.py E01 --scenes E01S03 E01S07 --no-assemble
    python tools/render.py E01 --still E01S05   # one PNG of the last frame (layout check)

Always renders with --disable_caching: scene timelines rely on every frame being written.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C  # noqa: E402

MANIM = os.environ.get("MANIM_BIN", str(ROOT.parent / ".venv" / "bin" / "manim"))
# quality flag -> (manim args, folder tag)
QUALITY = {
    "l": (["-ql"], "480p15"),
    "m": (["-qm"], "720p30"),
    "h": (["-qh", "--frame_rate", "30"], "1080p30"),   # brief: 1920x1080 at 30 fps
}


def episode_scenes(ep: str) -> list[str]:
    path = ROOT / "scenes" / f"ep{ep[1:].lower()}.py"
    src = path.read_text()
    ns: dict = {}
    # cheap parse of EPISODE_SCENES without importing manim
    start = src.index("EPISODE_SCENES")
    exec(src[start:src.index("]", start) + 1], ns)
    return ns["EPISODE_SCENES"]


def render_scene(ep: str, cls: str, q: str, still: bool = False) -> tuple[str, bool, float, str]:
    args, tag = QUALITY[q]
    scene_file = ROOT / "scenes" / f"ep{ep[1:].lower()}.py"
    log = C.LOGS / f"render_{cls}_{tag}{'_still' if still else ''}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    cmd = [MANIM, *args, "--disable_caching", "--media_dir", str(C.RENDERS / "media"),
           "--progress_bar", "none", str(scene_file), cls]
    if still:
        cmd[1:1] = ["-s", "--format", "png"]
    t0 = time.time()
    with open(log, "w") as fh:
        rc = subprocess.call(cmd, cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT)
    return cls, rc == 0, time.time() - t0, str(log)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("-q", "--quality", default="l", choices=QUALITY)
    ap.add_argument("--scenes", nargs="*")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--no-assemble", action="store_true")
    ap.add_argument("--still", nargs="*")
    a = ap.parse_args()
    ep = a.episode.upper()
    classes = episode_scenes(ep)
    if a.still is not None:
        sel = [c for c in classes if not a.still or c.split("_")[0] in a.still]
        failures = []
        with cf.ThreadPoolExecutor(a.jobs) as ex:
            for cls, ok, dt, log in ex.map(lambda c: render_scene(ep, c, a.quality, True), sel):
                print(f"{'OK ' if ok else 'ERR'} still {cls} {dt:.0f}s  {log}")
                if not ok:
                    failures.append(cls)
        sys.exit(1 if failures else 0)
    if a.scenes:
        classes = [c for c in classes if c.split("_")[0] in a.scenes]
    failed = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for cls, ok, dt, log in ex.map(lambda c: render_scene(ep, c, a.quality), classes):
            print(f"{'OK ' if ok else 'ERR'} {cls:<28} {dt:6.0f}s  {log}", flush=True)
            if not ok:
                failed.append(cls)
    for p in layout_report(ep, QUALITY[a.quality][1]):
        print("LAYOUT/TIMING:", p)
    if failed:
        print("FAILED:", failed)
        sys.exit(1)
    if not a.no_assemble and not a.scenes:
        rc = subprocess.call([sys.executable, str(ROOT / "tools" / "assemble.py"), ep, "-q", a.quality])
        sys.exit(rc)


def layout_report(ep: str, tag: str) -> list[str]:
    probs = []
    for cls in episode_scenes(ep):
        sid = cls.split("_")[0]
        f = C.TIMELINES / tag / f"{sid}.json"
        if not f.exists():
            continue
        for b in json.loads(f.read_text())["beats"]:
            for p in b.get("layout", []):
                probs.append(f"{b['key']}: {p}")
            if b["overrun"] > 0.75:
                probs.append(f"{b['key']}: visuals overrun narration by {b['overrun']:.2f}s")
    return probs


if __name__ == "__main__":
    main()
