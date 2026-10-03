"""Import beat files or accurately aligned segments from manually generated narration.

python tools/import_manual_audio.py --directory audio/manual --episodes E01 E02 E03
python tools/import_manual_audio.py --segments checked-alignment.json --episodes E01

Segments map exact beat IDs to {file, start, end}; times are seconds in the source audio.
They must come from checked speech alignment, not estimated preview timestamps.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C
from shared.script_parser import load_episode
from shared.tts import load_manifest, manual_text_hash, save_manifest, wav_duration


def probe_duration(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "default=nw=1:nk=1", str(path)], text=True))


def main():
    ap = argparse.ArgumentParser()
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--directory", type=Path)
    source.add_argument("--segments", type=Path)
    ap.add_argument("--episodes", nargs="+", required=True)
    a = ap.parse_args()
    beats = {b.key: b for ep in a.episodes for b in load_episode(ep.upper()).beats()}
    entries = {}
    if a.segments:
        entries = json.loads(a.segments.read_text())
        if not isinstance(entries, dict):
            raise ValueError("Alignment must map beat IDs to checked audio segments")
    else:
        for p in sorted(a.directory.rglob("*")):
            if p.suffix.lower() not in (".wav", ".mp3", ".m4a", ".flac", ".ogg"):
                continue
            if p.stem in entries:
                raise ValueError(f"Duplicate beat file: {p.stem}")
            entries[p.stem] = {"file": str(p.resolve())}
    unknown = sorted(set(entries) - set(beats))
    if unknown:
        raise ValueError(f"Files/segments are not beat IDs from the selected episodes: {unknown}")
    if not entries:
        raise ValueError("No narration clips supplied")
    # Validate the entire request before creating files or replacing the manifest.
    checked = []
    for key, entry in entries.items():
        path = Path(entry["file"])
        if a.segments and not path.is_absolute():
            path = a.segments.parent / path
        duration = probe_duration(path)
        start, end = float(entry.get("start", 0)), float(entry.get("end", duration))
        if not 0 <= start < end <= duration + 0.03:
            raise ValueError(f"{key}: invalid segment [{start}, {end}] in {duration}s source")
        if end - start < 0.10:
            raise ValueError(f"{key}: narration segment is too short")
        checked.append((key, path, start, end))
    manifest = load_manifest()
    C.AUDIO_CACHE.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".manual-import-", dir=C.AUDIO_CACHE) as td:
        staged = []
        for key, path, start, end in checked:
            text_hash = manual_text_hash(beats[key].text)
            output = C.AUDIO_CACHE / key[:3] / f"{key}__manual_{text_hash[:12]}.wav"
            temp = Path(td) / output.name
            subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-ss", str(start),
                                   "-t", str(end-start), "-ac", "1", "-ar", str(C.AUDIO_RATE),
                                   "-c:a", "pcm_s16le", str(temp)])
            staged.append((key, temp, output, text_hash, wav_duration(temp)))
        for key, temp, output, text_hash, duration in staged:
            output.parent.mkdir(parents=True, exist_ok=True)
            temp.replace(output)
            manifest[key] = {"source": "manual", "text_hash": text_hash,
                             "path": str(output.relative_to(C.ROOT)), "duration": duration}
        save_manifest(manifest)
    missing = sorted(key for key in beats if key not in manifest or manifest[key].get("text_hash") != manual_text_hash(beats[key].text))
    print(json.dumps({"imported_beats": len(checked), "missing_manual_beats": missing}, indent=2))


if __name__ == "__main__":
    main()
