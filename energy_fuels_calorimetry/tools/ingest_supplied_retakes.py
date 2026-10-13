"""Import the ten user-supplied MP3 corrections with measured word timing.

This is a separate path from authenticated OpenRouter WAV imports. MP3s do
not contain provider, model or voice receipts, so none are invented. The
input bytes, lossless PCM decode, corrected text and local acoustic review
are recorded instead. Original scene recordings remain untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.tts import manual_text_hash, wav_duration
from tools.ingest_openrouter_retakes import (
    Rejected, align_measured, check_words, expected_beats, install_payloads, read_map,
)

SOURCE = "user_supplied_retake"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reviewed_alignment(approved: dict, directory: Path) -> dict:
    result = {}
    for key, item in approved.items():
        review = json.loads((directory / f"{key}.json").read_text())
        if (review.get("input_sha256") != item["input_sha256"]
                or review.get("audio_sha256") != sha(item["wav"].read_bytes())
                or review.get("text") != item["text"]
                or float(review["report"]["greedy_transcription_similarity"]) < 0.90):
            raise Rejected(f"{key}: saved measured review does not match source/text")
        result[key] = (review["words"][key], review["report"])
    return result


def ingest(directory: Path, review_directory: Path | None = None) -> dict:
    expected = expected_beats()
    files = {p.stem: p for p in directory.glob("*.mp3")}
    if set(files) != set(expected) or len(expected) != 10:
        raise Rejected(f"Exactly ten corrected MP3s required; missing={sorted(set(expected)-set(files))}; "
                       f"extra={sorted(set(files)-set(expected))}")
    audio = ROOT / "audio"
    audio.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mp3-retake-check-") as tmp:
        approved = {}
        for key, text in expected.items():
            original = files[key].read_bytes()
            decoded = Path(tmp) / f"{key}.wav"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(files[key]),
                            "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(decoded)], check=True)
            approved[key] = {"key": key, "text": text, "wav": decoded,
                             "duration": wav_duration(decoded), "input_bytes": original,
                             "input_sha256": sha(original)}
        result = (reviewed_alignment(approved, review_directory)
                  if review_directory else align_measured(approved))
        for key, item in approved.items():
            check_words(item, result[key][0])
            if sha(files[key].read_bytes()) != item["input_sha256"]:
                raise Rejected(f"{key}: input MP3 changed during alignment")
        manifest = read_map(audio / "manifest.json")
        changes = {}
        for key, item in approved.items():
            basename = f"{key}__supplied_{item['input_sha256'][:12]}"
            source = Path("audio/retakes/supplied_mp3") / f"{basename}.mp3"
            decoded = Path("audio/cache") / key[:3] / f"{basename}.wav"
            metadata = Path("audio/retakes/supplied_mp3") / f"{basename}.json"
            payload = item["wav"].read_bytes()
            words, report = result[key]
            receipt = {"source": SOURCE, "key": key, "input_path": str(source),
                       "input_sha256": item["input_sha256"], "audio_sha256": sha(payload),
                       "text_hash": manual_text_hash(item["text"]), "duration": item["duration"],
                       "decode": "FFmpeg PCM signed 16-bit, mono, 24000 Hz; no time stretching",
                       "alignment": report, "words": words,
                       "provider_verified": False, "voice_verified": False}
            changes[ROOT / source] = item["input_bytes"]
            changes[ROOT / decoded] = payload
            changes[ROOT / metadata] = (json.dumps(receipt, indent=2) + "\n").encode()
            manifest[key] = {"source": SOURCE, "path": str(decoded), "metadata_path": str(metadata),
                             "text_hash": receipt["text_hash"], "input_sha256": item["input_sha256"],
                             "audio_sha256": receipt["audio_sha256"], "duration": item["duration"]}
        for ep in sorted({key[:3] for key in approved}):
            folder = audio / "aligned" / ep
            words = read_map(folder / "words.json")
            segments = read_map(folder / "segments.json")
            reviews = read_map(folder / "retake-alignment-review.json")
            for key, item in approved.items():
                if not key.startswith(ep):
                    continue
                words[key] = result[key][0]
                segments[key] = {"file": str(ROOT / manifest[key]["path"]),
                                 "start": 0.0, "end": item["duration"]}
                reviews[key] = {**result[key][1], "source": SOURCE,
                                "input_sha256": item["input_sha256"]}
            for name, contents in (("words.json", words), ("segments.json", segments),
                                   ("retake-alignment-review.json", reviews)):
                changes[folder / name] = (json.dumps(contents, indent=2) + "\n").encode()
        changes[audio / "manifest.json"] = (json.dumps(manifest, indent=1, sort_keys=True) + "\n").encode()
        install_payloads(changes, audio)
    return {"imported": 10, "source": SOURCE, "keys": sorted(approved)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--review-directory", type=Path,
                        help="Reuse measured review only if input, decode and text hashes match")
    args = parser.parse_args()
    try:
        print(json.dumps(ingest(args.directory.resolve(), args.review_directory), indent=2))
    except (Rejected, ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"MP3 RETAKE IMPORT BLOCKED: {error}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
