"""
Extract a still at the end of every narration beat and build labelled contact sheets for review.

    python tools/stills.py E01 -q l [--scenes E01S03] [--per-sheet 4]

Writes checks/stills/<EP>_<tag>/<beat>.png and sheet_<scene>_<k>.png.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C  # noqa: E402
from tools.render import QUALITY, episode_scenes  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("-q", "--quality", default="l")
    ap.add_argument("--scenes", nargs="*")
    ap.add_argument("--per-sheet", type=int, default=4)
    ap.add_argument("--width", type=int, default=760)
    a = ap.parse_args()
    ep = a.episode.upper()
    tag = QUALITY[a.quality][1]
    out = ROOT / "checks" / "stills" / f"{ep}_{tag}"
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    for cls in episode_scenes(ep):
        sid = cls.split("_")[0]
        if a.scenes and sid not in a.scenes:
            continue
        tl = json.loads((C.TIMELINES / tag / f"{sid}.json").read_text())
        video = C.RENDERS / "media" / "videos" / f"ep{ep[1:].lower()}" / tag / f"{cls}.mp4"
        frames = []
        for b in tl["beats"]:
            t = b["start"] + max(b["speech"], 0.2) - 0.15 + b["overrun"]
            png = out / f"{b['key'].replace('.', '_')}.png"
            subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
                                   "-frames:v", "1", str(png)])
            frames.append((b["key"], png))
        for k in range(0, len(frames), a.per_sheet):
            chunk = frames[k:k + a.per_sheet]
            ims = [Image.open(p).convert("RGB") for _, p in chunk]
            w = a.width
            h = int(ims[0].height * w / ims[0].width)
            cols = 2
            rows = (len(ims) + 1) // 2
            sheet = Image.new("RGB", (cols * w + 10, rows * (h + 26) + 4), (40, 40, 40))
            d = ImageDraw.Draw(sheet)
            for i, ((key, _), im) in enumerate(zip(chunk, ims)):
                x, y = (i % cols) * (w + 10), (i // cols) * (h + 26)
                sheet.paste(im.resize((w, h)), (x, y + 22))
                d.text((x + 4, y + 2), key, fill=(255, 220, 120), font=font)
            sheet.save(out / f"sheet_{sid}_{k // a.per_sheet + 1}.png")
        print(sid, len(frames), "frames")


if __name__ == "__main__":
    main()
