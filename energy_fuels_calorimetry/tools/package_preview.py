"""Make a captioned MP4 from an actually assembled silent preview."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    a = ap.parse_args()
    ep = a.episode.upper()
    report = json.loads((ROOT / "logs" / f"assemble_{ep}_1080p30.json").read_text())
    source = ROOT / report["output"]
    if report["narrated"]:
        raise ValueError("This command packages silent previews only")
    if report["problems"]:
        raise ValueError(f"Assembly timing failed: {report['problems']}")
    out = ROOT / "delivery" / ep
    out.mkdir(parents=True, exist_ok=True)
    caption = ROOT / report["captions"][0]
    output = out / f"{ep}-Chemistry-SILENT-preview-1080p.mp4"
    # Captions occupy the reserved lower strip and remain readable in players
    # that do not expose the MP4's optional soft-subtitle track.
    relative_caption = str(caption.relative_to(ROOT))
    style = "FontName=Inter,FontSize=22,PrimaryColour=&H00F8F1EE,OutlineColour=&H001E110C,BorderStyle=1,Outline=1,Shadow=0,MarginV=18"
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", str(source), "-vf",
                           f"subtitles={relative_caption}:force_style='{style}'", "-an", "-sn",
                           "-c:v", "libx264", "-preset", "fast", "-crf", "19",
                           "-movflags", "+faststart", str(output)], cwd=ROOT)
    for rel in report["captions"] + [report["transcript"]]:
        p = ROOT / rel
        shutil.copyfile(p, out / p.name)
    (out / "README.txt").write_text("Silent 1080p30 visual preview. Captions and beat timing are estimated.\n"
                                    "After manual narration is supplied, re-render with measured speech durations.\n")
    print(output)


if __name__ == "__main__":
    main()
