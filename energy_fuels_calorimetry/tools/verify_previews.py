"""Validate silent preview streams, measured container durations and full video decoding."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def verify(ep, tag):
    path = ROOT / "delivery" / ep / f"{ep}-Chemistry-SILENT-preview-{tag}.mp4"
    assembly = json.loads((ROOT / "logs" / f"assemble_{ep}_{tag}.json").read_text())
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]))
    streams = probe["streams"]
    assert len(streams) == 1 and streams[0]["codec_type"] == "video", f"{ep}: unexpected streams"
    video = streams[0]
    width, height, fps = {"720p30": (1280, 720, 30), "1080p30": (1920, 1080, 30),
                          "480p15": (854, 480, 15)}[tag]
    assert (video["width"], video["height"]) == (width, height), f"{ep}: wrong resolution"
    assert Fraction(video["r_frame_rate"]) == fps, f"{ep}: wrong nominal frame rate"
    # MP4 end-packet duration may round by a fraction of a millisecond at concat.
    # Check the average as well, allowing only that container rounding.
    average_fps = float(Fraction(video["avg_frame_rate"]))
    assert abs(average_fps - fps) < 0.001, f"{ep}: wrong average frame rate"
    assert not assembly["narrated"] and not assembly["problems"], f"{ep}: assembly failed"
    duration = float(probe["format"]["duration"])
    assert abs(duration - assembly["duration"]) <= 2 / fps, f"{ep}: timeline drift"
    layout = []
    for row in assembly["scenes"]:
        record = json.loads((ROOT / f"checks/layout/{tag}/{row['scene']}.json").read_text())
        layout.extend((b["key"], problem) for b in record["beats"] for problem in b["layout"])
    assert not layout, f"{ep}: unresolved layout warnings: {layout}"
    decoded = subprocess.run(["ffmpeg", "-v", "error", "-threads", "2", "-i", str(path),
                              "-map", "0:v:0", "-f", "null", "-"], capture_output=True, text=True)
    assert decoded.returncode == 0 and not decoded.stderr.strip(), f"{ep}: decode error: {decoded.stderr}"
    return dict(file=str(path.relative_to(ROOT)), resolution=[width, height], fps=fps,
                average_fps=average_fps,
                duration_seconds=duration, scenes=len(assembly["scenes"]), beats=assembly["beats"],
                audio_streams=0, subtitle_streams=0, assembly_timing_problems=0,
                geometry_flags=0, full_video_decode="pass", sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("--tag", default="720p30")
    args = ap.parse_args()
    dest = ROOT / "checks/preview_validation_20261005.json"
    record = json.loads(dest.read_text()) if dest.exists() else {}
    for ep in args.episodes:
        ep = ep.upper()
        result = verify(ep, args.tag)
        record[ep] = result
        dest.write_text(json.dumps(dict(sorted(record.items())), indent=2) + "\n")
        print(f"{ep}: full decode, geometry, timing and no-subtitle stream checks passed", flush=True)


if __name__ == "__main__":
    main()
