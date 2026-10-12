"""Check whether a private Google Gemini API project owns Melb Teacher F1.

The stateful voice_... ID is stored in the project that created it. An
OpenRouter API key is NOT a Google API key and cannot access Google Voices API.
No audio is generated and no credentials or voice identifiers are printed.

  read -rs "GEMINI_API_KEY?Google Gemini API key: "; echo
  export GEMINI_API_KEY
  ../.venv/bin/python tools/check_gemini_voice_access.py
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.narration_runner import voice_id

BASE = "https://generativelanguage.googleapis.com/v1beta/voices/"


def check_access(voice: str, google_api_key: str) -> tuple[int, str]:
    """Return HTTP status and safe diagnostic; never return secret input."""
    if not voice.startswith("voice_"):
        if voice.startswith("voicekey_"):
            return 0, ("Stateless voice keys cannot be looked up with the "
                       "stored-voice endpoint; test synthesis directly.")
        return 0, "The configured Melb Teacher F1 ID is not a Google voice_ ID."
    request = urllib.request.Request(
        BASE + urllib.parse.quote(voice, safe=""),
        headers={"x-goog-api-key": google_api_key},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status == 200:
                return 200, ("This Google API key can access the stored Melb "
                             "Teacher F1 voice. You can use direct Gemini TTS.")
            return response.status, "Unexpected Google Voices API response."
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return 404, ("Voice not found for this Google project. Use an API "
                         "key from the SAME Google AI Studio project that "
                         "created Melb Teacher F1, or check voice expiry.")
        if exc.code == 403:
            return 403, ("Google denied access to this stored voice; check "
                         "project ownership, API permissions and TTS access.")
        if exc.code == 401:
            return 401, "Google API key authentication failed."
        if exc.code == 400:
            return 400, ("Google rejected the lookup request. The stored "
                         "voice may not be recognised by this project.")
        return exc.code, f"Google Voices API returned HTTP {exc.code}."
    except urllib.error.URLError:
        return 0, "Unable to reach Google's Voices API; check the connection."


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--voice-file", type=Path, help="Path to original voice_ids.txt")
    args = cli.parse_args()
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        print("GEMINI_API_KEY is unset. Use the Google AI Studio project's "
              "API key, not an OpenRouter key.", file=sys.stderr)
        return 2
    try:
        identifier, _ = voice_id(argparse.Namespace(
            voice_id=None,
            voice_file=str(args.voice_file) if args.voice_file else None,
            lite=False,
        ))
    except (ValueError, OSError):
        print("Couldn't locate the original Melb Teacher F1 voice file.",
              file=sys.stderr)
        return 3
    status, detail = check_access(identifier, key)
    print(f"Google Melb Teacher F1 voice check: {detail}")
    return 0 if status == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
