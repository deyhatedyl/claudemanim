"""Summarise beat-level geometry and make inspection sheets from actual frames."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--tag", default="1080p30")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    ep = a.episode.upper()
    reports = sorted((ROOT / "checks/layout" / a.tag).glob(f"{ep}S*.json"))
    problems = [(b["key"], p) for path in reports for b in json.loads(path.read_text())["beats"] for p in b["layout"]]
    result = {"episode": ep, "scenes_checked": len(reports), "problems": problems}
    dest = ROOT / "checks/layout" / a.tag / f"{ep}_summary.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    frames = sorted((ROOT / "checks/beat_stills" / f"{ep}_{a.tag}").glob("*.png"))
    out = ROOT / "checks/contact_sheets" / f"{ep}_{a.tag}"
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    by_scene = {}
    for path in frames:
        by_scene.setdefault(path.stem.split(".")[0], []).append(path)
    for scene, paths in by_scene.items():
        for page, start in enumerate(range(0, len(paths), 6), 1):
            chunk = paths[start:start+6]
            sheet = Image.new("RGB", (1536, ((len(chunk)+1)//2)*456), "#1e1e1e")
            draw = ImageDraw.Draw(sheet)
            for i, path in enumerate(chunk):
                x, y = (i%2)*768, (i//2)*456
                draw.text((x+10,y+5), path.stem, fill="#ffce60", font=font)
                with Image.open(path) as im:
                    sheet.paste(im.convert("RGB").resize((768,432)), (x,y+24))
            sheet.save(out / f"{scene}_{page}.jpg", quality=92)
    if a.strict and (not reports or problems):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
