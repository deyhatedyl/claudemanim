"""Gate narrated Chemistry renders against *recorded* beat and word timing.

Run after private WAV import, force alignment, and full-HD scene rendering:
  python tools/audit_narration_alignment.py E04 --tag 1080p30

No audio or transcript content is uploaded. An ordinary visual preview using
estimated WPM cannot pass this final-audio gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import wave

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode
from shared.tts import cached_clip, load_manifest


def words_normalized(text: str) -> list[str]:
    """Use the same spoken-token boundaries as the local word aligner."""
    return [token for word in text.split()
            if (token := re.sub(r"[^\w]+", "", word.casefold()))]


def beat_errors(key: str, text: str, clip: dict | None, aligned: list | None,
                timeline: dict | None, *, rate_tolerance: float = 0.08) -> list[str]:
    errors = []
    if clip is None:
        return ["missing verified audio clip (or exact text hash mismatch)"]
    if timeline is None:
        return ["missing 1080p timeline for beat"]
    if timeline.get("estimated"):
        errors.append("uses estimated rather than recorded audio duration")
    if not timeline.get("audio"):
        errors.append("timeline has no recorded audio path")
    if timeline.get("text") != text:
        errors.append("timeline text differs from current script")
    duration = float(clip.get("duration", 0))
    if duration <= 0 or abs(float(timeline.get("speech", 0)) - duration) > rate_tolerance:
        errors.append("timeline speech duration differs from measured recorded beat")
    if float(timeline.get("overrun", 0)) > 0.15:
        errors.append("animation runs past narration beat by more than 150 ms")
    if not aligned:
        errors.append("missing measured word alignment")
        return errors
    got = [re.sub(r"[^\w]+", "", row.get("word", "").casefold()) for row in aligned]
    got = [w for w in got if w]
    if got != words_normalized(text):
        errors.append("aligned word transcript differs from current spoken beat")
    last = -0.001
    for row in aligned:
        start, end = float(row.get("start", -1)), float(row.get("end", -1))
        if start < -0.05 or end > duration + rate_tolerance or start >= end or start < last - 0.02:
            errors.append("word timestamps outside beat or out of order")
            break
        last = end
    return errors


def audit(episode: str, tag: str) -> dict:
    ep = load_episode(episode.upper())
    manifest = load_manifest()
    aligned_file = ROOT / "audio" / "aligned" / ep.id / "words.json"
    word_map = json.loads(aligned_file.read_text()) if aligned_file.is_file() else {}
    problems = []
    tested = 0
    for scene in ep.scenes:
        source = ROOT / "renders" / "timelines" / tag / f"{scene.id}.json"
        if not source.is_file():
            problems.append({"scene": scene.id, "error": "missing rendered scene timeline"})
            continue
        timeline = json.loads(source.read_text())
        observed = {b["key"]: b for b in timeline.get("beats", [])}
        expected = [b.key for b in scene.beats]
        if list(observed) != expected:
            problems.append({"scene": scene.id, "error": "rendered beat sequence differs from script"})
        for beat in scene.beats:
            clip = cached_clip(beat.key, beat.text, manifest)
            errors = beat_errors(beat.key, beat.text, clip, word_map.get(beat.key),
                                 observed.get(beat.key))
            tested += 1
            for error in errors:
                problems.append({"beat": beat.key, "error": error})
    return {"episode": ep.id, "render_tag": tag, "beats_tested": tested,
            "problems": problems, "passed": tested > 0 and not problems}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode", help="E04, E05, ..., E14")
    ap.add_argument("--tag", default="1080p30")
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    record = audit(args.episode, args.tag)
    value = json.dumps(record, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(value)
    print(value)
    if not record["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
