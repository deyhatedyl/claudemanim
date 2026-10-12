"""Verify a completed VCE Chemistry narrated MP4 and optionally sample frames.

Checks metadata, 1080p30 video, an AAC narration stream, absence of embedded
subtitles, assembly's full beat coverage, and full-stream decodability. This is
a structural check, not a replacement for listening and frame-by-frame QA.

Usage:
  python tools/verify_narrated_media.py delivery/E04/E04-Chemistry-Narrated-1080p.mp4 --assembly logs/assemble_E04_1080p30.json --sample-every 120
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess


def inspect_metadata(probe: dict, assembly: dict | None = None) -> dict:
    streams = probe.get("streams", [])
    video = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    subtitles = [s for s in streams if s.get("codec_type") == "subtitle"]
    if len(video) != 1 or len(audio) != 1 or subtitles:
        raise ValueError("Expected exactly one video, one audio and zero subtitle streams")
    v, a = video[0], audio[0]
    if v.get("codec_name") != "h264" or (v.get("width"), v.get("height")) != (1920, 1080):
        raise ValueError("Expected H.264 video at 1920x1080")
    if Fraction(v["r_frame_rate"]) != 30 or abs(float(Fraction(v["avg_frame_rate"])) - 30) > 0.01:
        raise ValueError("Expected constant approximately 30 fps, nominally 30/1")
    if a.get("codec_name") != "aac":
        raise ValueError("Expected AAC narration audio")
    duration = float(probe["format"]["duration"])
    if duration <= 1:
        raise ValueError("Video duration is implausibly short")
    audio_length = float(a.get("duration", duration))
    if abs(audio_length - duration) > 0.5:
        raise ValueError("Audio does not cover the full movie duration")
    if assembly is not None:
        if not assembly.get("narrated") or not assembly.get("final") or assembly.get("problems"):
            raise ValueError("Assembly did not certify a complete narrated final")
        count = assembly.get("beats")
        if not isinstance(count, int) or count < 1 or assembly.get("beats_with_audio") != count:
            raise ValueError("Missing recorded narration for one or more beats")
        if abs(float(assembly["duration"]) - duration) > 2 / 30:
            raise ValueError("Assembly timeline and movie duration diverge")
    return {"duration_seconds": duration, "video_codec": "h264", "audio_codec": "aac",
            "resolution": [1920, 1080], "fps": 30,
            "subtitle_streams": 0, "audio_streams": 1,
            "beat_coverage": assembly.get("beats_with_audio") if assembly else None}


def run(args: list[str]) -> None:
    subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def verify(movie: Path, assembly_file: Path | None, *, decode: bool, sample_every: int,
           sample_dir: Path | None) -> dict:
    if not movie.is_file():
        raise FileNotFoundError(movie)
    result = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams",
                             "-of", "json", str(movie)], check=True, capture_output=True, text=True)
    probe = json.loads(result.stdout)
    assembly = json.loads(assembly_file.read_text()) if assembly_file else None
    report = inspect_metadata(probe, assembly)
    if decode:
        run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
             "-threads", "2", "-i", str(movie), "-map", "0:v:0", "-map", "0:a:0",
             "-f", "null", "-"])
    report["full_stream_decode"] = "pass" if decode else "not_run"
    if sample_every > 0:
        if sample_dir is None:
            raise ValueError("sample_dir required when sampling frames")
        sample_dir.mkdir(parents=True, exist_ok=True)
        samples = []
        t = 5
        while t < report["duration_seconds"]:
            target = sample_dir / f"frame_{t:05d}s.jpg"
            run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", str(t),
                 "-i", str(movie), "-frames:v", "1", "-y", str(target)])
            samples.append(str(target))
            t += sample_every
        report["sampled_frames"] = samples
    digest = hashlib.sha256()
    with movie.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            digest.update(block)
    report["sha256"] = digest.hexdigest()
    report["movie"] = str(movie)
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("movie", type=Path)
    p.add_argument("--assembly", type=Path, help="matching logs/assemble_E##_1080p30.json")
    p.add_argument("--metadata-only", action="store_true", help="skip full decoding (not final QA)")
    p.add_argument("--sample-every", type=int, default=0, metavar="SECONDS")
    p.add_argument("--sample-dir", type=Path)
    p.add_argument("--report", type=Path)
    a = p.parse_args()
    if a.sample_every < 0:
        p.error("--sample-every must be nonnegative")
    output = verify(a.movie, a.assembly, decode=not a.metadata_only,
                    sample_every=a.sample_every,
                    sample_dir=a.sample_dir or (a.movie.parent / "frame_qa"))
    data = json.dumps(output, indent=2) + "\n"
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(data)
    print(data)


if __name__ == "__main__":
    main()
