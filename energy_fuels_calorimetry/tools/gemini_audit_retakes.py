"""Regenerate only the ten reviewed chemistry narration corrections with Gemini.

Uses Gemini 3.8 Flash TTS with a warm prebuilt voice and Melbourne-accent
style instruction, as requested after the custom-F1-voice requirement was
relaxed. Existing unchanged recordings are left intact. Output is local,
private and excluded from version control.

Examples:
  python tools/gemini_audit_retakes.py --dry-run
  python tools/gemini_audit_retakes.py --probe
  python tools/gemini_audit_retakes.py
  python tools/gemini_audit_retakes.py --package-only
  python tools/gemini_audit_retakes.py --lite

The API key is NEVER requested or saved to a project file.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode
from tools.reconcile_authored_narration import AUDITED_RETAKES
from tools import narration_runner as gemini


def prepare() -> list[dict]:
    beats = {
        beat.key: beat
        for episode in ("E06", "E07", "E08", "E12", "E13", "E14")
        for beat in load_episode(episode).beats()
    }
    missing = AUDITED_RETAKES - beats.keys()
    if missing or len(AUDITED_RETAKES) != 10:
        raise ValueError(f"Missing reviewed audit beats: {sorted(missing)}")
    return [
        {"key": key, "scene": key.split(".")[0], "text": beats[key].text}
        for key in sorted(AUDITED_RETAKES)
    ]


def package_verified(beats: list[dict], output: Path, model: str, vid: str) -> Path:
    """Validate every expected clip before shipping a portable, exactly-ten-beat ZIP."""
    if len(beats) != 10 or len({beat["key"] for beat in beats}) != 10:
        raise ValueError("Retake manifest must contain exactly ten unique beats.")
    segments = {}
    clips = []
    for beat in beats:
        wav = output / f'{beat["key"]}.wav'
        if not gemini.ready(wav, beat["text"], model, vid, gemini.STYLE):
            raise ValueError(f'{beat["key"]}: WAV missing, corrupt, or mismatched in text/model/voice/style.')
        duration = gemini.wav_duration(wav.read_bytes())
        segments[beat["key"]] = {"file": str(wav.resolve()), "start": 0.0, "end": duration}
        clips.extend((wav, wav.with_suffix(".wav.json")))

    # Local segments can be imported immediately; ZIP uses relative paths on any machine.
    portable = {
        key: {"file": f"{key}.wav", "start": row["start"], "end": row["end"]}
        for key, row in segments.items()
    }
    result = output / "gemini-ten-retakes.zip"
    output.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".gemini-ten-", suffix=".zip", dir=output)
    os.close(fd)
    try:
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as archive:
            for clip in clips:
                archive.write(clip, clip.name)
            archive.writestr("segments.json", json.dumps(portable, indent=2) + "\n")
        os.replace(temp, result)
    finally:
        Path(temp).unlink(missing_ok=True)
    gemini.atomic_write(output / "segments.json",
                        (json.dumps(segments, indent=2) + "\n").encode("utf-8"))
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lite", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--probe", action="store_true",
                    help="synthesize one short sample into probes/; incurs one paid Gemini request")
    ap.add_argument("--package-only", action="store_true",
                    help="offline validate and ZIP all ten completed clips without using any key")
    ap.add_argument("--voice-file", type=Path)
    ap.add_argument("--studio-voice", default="Sulafat",
                    help="Gemini prebuilt warm voice; default Sulafat (use with an Australian-accent style)")
    ap.add_argument("--interval", type=float, default=21.0)
    args = ap.parse_args(argv)
    if args.package_only and (args.probe or args.dry_run):
        ap.error("--package-only cannot be combined with --probe or --dry-run")
    beats = prepare()
    gemini.BEATS = beats
    output = ROOT / "audio" / "gemini_retakes"
    params = ["all", "--beats", "--output", str(output),
              "--interval", str(args.interval)]
    if args.lite:
        params += ["--lite"]
    if args.voice_file:
        params += ["--voice-file", str(args.voice_file)]
    else:
        params += ["--studio-voice", args.studio_voice]
    try:
        parsed = gemini.parse_args(params)
        vid, _ = gemini.voice_id(parsed)
    except (OSError, ValueError) as exc:
        print(f"Voice selection failed: {type(exc).__name__}. Check the chosen preset or private voice file.",
              file=sys.stderr)
        return 2
    model = gemini.LITE_MODEL if args.lite else gemini.FLASH_MODEL
    if args.package_only:
        try:
            archive = package_verified(beats, output, model, vid)
        except (OSError, ValueError) as exc:
            print(f"Packaging blocked: {exc}", file=sys.stderr)
            return 3
        print(f"Validated and packaged 10 Gemini retakes: {archive}")
        return 0
    if args.probe:
        params += ["--probe"]
    if args.dry_run:
        params += ["--dry-run"]
    elif not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("Gemini API key unavailable. Set GEMINI_API_KEY in the "
              "Chat On Steroids terminal before running this script.", file=sys.stderr)
        return 2
    code = gemini.main(params)
    if code or args.dry_run or args.probe:
        return code
    try:
        archive = package_verified(beats, output, model, vid)
    except (OSError, ValueError) as exc:
        print(f"Packaging blocked: {exc}", file=sys.stderr)
        return 3
    print(f"Gemini clips verified (10): {output}")
    print(f"Portable ten-retake ZIP: {archive}")
    print(f"Import: python tools/import_manual_audio.py "
          f"--segments {output / 'segments.json'} --episodes E06 E07 E08 E12 E13 E14")
    return 0


if __name__ == "__main__":
    sys.exit(main())
