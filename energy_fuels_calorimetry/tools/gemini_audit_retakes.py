"""Regenerate only the ten reviewed chemistry narration corrections with Gemini.

Uses Gemini 3.8 Flash TTS with a warm prebuilt voice and Melbourne-accent
style instruction, as requested after the custom-F1-voice requirement was
relaxed. Existing unchanged recordings are left intact. Output is local,
private and excluded from version control.

Examples:
  python tools/gemini_audit_retakes.py --dry-run
  GEMINI_API_KEY=... python tools/gemini_audit_retakes.py
  python tools/gemini_audit_retakes.py --lite

The API key is NEVER requested or saved to a project file.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import wave

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
    if missing:
        raise ValueError(f"Missing reviewed audit beats: {sorted(missing)}")
    return [
        {"key": key, "scene": key.split(".")[0], "text": beats[key].text}
        for key in sorted(AUDITED_RETAKES)
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lite", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--voice-file", type=Path)
    ap.add_argument("--studio-voice", default="Sulafat",
                    help="Gemini prebuilt warm voice; default Sulafat (use with an Australian-accent style)")
    ap.add_argument("--interval", type=float, default=21.0)
    args = ap.parse_args()
    gemini.BEATS = prepare()
    output = ROOT / "audio" / "gemini_retakes"
    params = ["all", "--beats", "--output", str(output),
              "--interval", str(args.interval)]
    if args.lite:
        params += ["--lite"]
    if args.voice_file:
        params += ["--voice-file", str(args.voice_file)]
    else:
        params += ["--studio-voice", args.studio_voice]
    if args.dry_run:
        params += ["--dry-run"]
    elif not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("Gemini API key unavailable. Set GEMINI_API_KEY in the "
              "Chat On Steroids terminal before running this script.", file=sys.stderr)
        return 2
    code = gemini.main(params)
    if code or args.dry_run:
        return code
    segments = {}
    for beat in gemini.BEATS:
        wav = output / f"{beat['key']}.wav"
        with wave.open(str(wav), "rb") as audio:
            duration = audio.getnframes() / audio.getframerate()
        segments[beat["key"]] = {"file": str(wav.resolve()), "start": 0.0, "end": duration}
    (output / "segments.json").write_text(json.dumps(segments, indent=2))
    print(f"Gemini clips ready ({len(segments)}): {output}")
    print(f"Import: python tools/import_manual_audio.py "
          f"--segments {output / 'segments.json'} --episodes E06 E07 E08 E12 E13 E14")
    return 0


if __name__ == "__main__":
    sys.exit(main())
