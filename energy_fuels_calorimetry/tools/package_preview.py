"""Make a clean MP4 from an actually assembled silent preview; no subtitles."""
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
    ap.add_argument("--tag", default="1080p30", choices=["720p30", "1080p30", "480p15"])
    a = ap.parse_args()
    ep = a.episode.upper()
    report = json.loads((ROOT / "logs" / f"assemble_{ep}_{a.tag}.json").read_text())
    source = ROOT / report["output"]
    if report["narrated"]:
        raise ValueError("This command packages silent previews only")
    if report["problems"]:
        raise ValueError(f"Assembly timing failed: {report['problems']}")
    out = ROOT / "delivery" / ep
    out.mkdir(parents=True, exist_ok=True)
    output = out / f"{ep}-Chemistry-SILENT-preview-{a.tag}.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", str(source), "-an", "-sn",
                           "-map", "0:v:0", "-c:v", "copy",
                           "-movflags", "+faststart", str(output)], cwd=ROOT)
    for rel in report["captions"] + [report["transcript"]]:
        p = ROOT / rel
        shutil.copyfile(p, out / p.name)
    (out / "README.txt").write_text(f"Silent {a.tag} visual preview. Beat timing is estimated. No embedded subtitles.\n"
                                    "After manual narration is supplied, re-render with measured speech durations.\n")
    print(output)


if __name__ == "__main__":
    main()
