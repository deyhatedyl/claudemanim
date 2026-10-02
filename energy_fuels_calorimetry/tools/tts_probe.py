"""
Verify the configured TTS provider before generating narration (run this first in a new session).

    python tools/tts_probe.py            # list TTS-capable models, synthesise the pronunciation test
    python tools/tts_probe.py --voices Kore Charon Puck   # compare voices on the same test line

Checks performed
  1. GEMINI_API_KEY (or GOOGLE_API_KEY) is present.
  2. The configured model (GEMINI_TTS_MODEL, default gemini-3.8-flash-tts) is listed by the API.
  3. A short pronunciation test is synthesised; sample rate, duration and words-per-minute are reported.
     A rate far outside ~110-180 wpm suggests the style instruction was read aloud or the clip is truncated.
Writes audio/probe/<voice>.wav and audio/probe/report.json. Listen to the clips before a full run.
"""
from __future__ import annotations

import argparse
import json
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C  # noqa: E402
from shared.tts import TTSUnavailable, list_models, synthesize_gemini  # noqa: E402

TEST = ("In this lesson we measure energy in joules and kilojoules. The enthalpy change for the combustion "
        "of methane is negative eight hundred and ninety kilojoules per mole. In calorimetry, the calibration "
        "factor is measured in joules per degree Celsius, and the molar volume at standard laboratory "
        "conditions is twenty-four point eight litres per mole. Ethanol, C two H five O H, burns to form "
        "carbon dioxide and water.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voices", nargs="*", default=[C.GEMINI_TTS_VOICE])
    a = ap.parse_args()
    out = C.AUDIO / "probe"
    out.mkdir(parents=True, exist_ok=True)
    report = dict(model=C.GEMINI_TTS_MODEL, style=C.GEMINI_TTS_STYLE, clips=[])
    try:
        models = list_models()
    except TTSUnavailable as e:
        print("BLOCKED:", e)
        sys.exit(2)
    names = [m["name"].split("/")[-1] for m in models]
    tts = [n for n in names if "tts" in n]
    report["tts_models_listed"] = tts
    print("TTS-capable models listed by the API:", ", ".join(tts) or "(none)")
    if C.GEMINI_TTS_MODEL not in names:
        print(f"WARNING: configured model {C.GEMINI_TTS_MODEL!r} is not listed; set GEMINI_TTS_MODEL")
        report["model_listed"] = False
    else:
        report["model_listed"] = True
    for v in a.voices:
        p = out / f"{v}.wav"
        try:
            dur = synthesize_gemini(TEST, p, voice=v)
        except TTSUnavailable as e:
            print(f"{v}: FAILED {e}")
            report["clips"].append(dict(voice=v, error=str(e)))
            continue
        with wave.open(str(p)) as w:
            rate = w.getframerate()
        wpm = len(TEST.split()) / dur * 60
        flag = "" if 110 <= wpm <= 180 else "  <-- check: unusual rate"
        print(f"{v}: {dur:.1f}s, {rate} Hz, {wpm:.0f} wpm{flag}  -> {p.relative_to(ROOT)}")
        report["clips"].append(dict(voice=v, path=str(p.relative_to(ROOT)), duration=dur, rate=rate, wpm=wpm))
    (out / "report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
