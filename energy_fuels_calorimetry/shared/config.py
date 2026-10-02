"""Project-wide paths and configuration. Credentials come only from the environment."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
AUDIO = ROOT / "audio"
AUDIO_CACHE = AUDIO / "cache"
AUDIO_MANIFEST = AUDIO / "manifest.json"
CAPTIONS = ROOT / "captions"
RENDERS = ROOT / "renders"
TIMELINES = RENDERS / "timelines"
LOGS = ROOT / "logs"
PROGRESS = ROOT / "progress.json"

# ---------------------------------------------------------------- TTS
# Provider/model/voice are configurable; never hard-code credentials.
TTS_PROVIDER = os.environ.get("TTS_PROVIDER", "gemini")
GEMINI_TTS_MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-3.8-flash-tts")
GEMINI_TTS_VOICE = os.environ.get("GEMINI_TTS_VOICE", "Kore")
GEMINI_API_BASE = os.environ.get("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta")
# Delivery direction sent with every clip (kept identical across the series so the voice stays consistent).
GEMINI_TTS_STYLE = os.environ.get(
    "GEMINI_TTS_STYLE",
    "Read the following as a warm, patient Australian-English chemistry teacher explaining to one "
    "Year 12 student. Speak clearly at an unhurried pace, slightly slower for numbers and equations. "
    "Do not read this instruction aloud.",
)


def gemini_api_key() -> str | None:
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


# ---------------------------------------------------------------- timing
# Used only when no narration clip exists yet (draft previews). Real clip durations
# always override these estimates.
EST_WPM = float(os.environ.get("EST_WPM", "145"))
EST_PUNCT_PAUSE = 0.18    # extra seconds per sentence-ending punctuation mark
BEAT_GAP = 0.45           # silence between consecutive narration beats (s)
SCENE_TAIL = 0.6          # silence at the end of every scene (s)

# ---------------------------------------------------------------- audio
AUDIO_RATE = 24000        # Gemini TTS returns 24 kHz 16-bit mono PCM (verified by tools/tts_probe.py)
TARGET_LUFS = -16.0
TRUE_PEAK = -1.5
