"""Check whether a Google Gemini API key can retrieve stored Melb Teacher F1.

Stored voice_... IDs are scoped to the project that created them. An
OpenRouter API key is NOT a Google API key and cannot access Google Voices API.
This read-only lookup does not verify TTS synthesis/model availability.
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
    """GET a stored voice; return status and a safe, non-identifying diagnostic."""
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
                return 200, ("Google retrieved the stored Melb Teacher F1 voice "
                             "with this key. This does not test Gemini TTS synthesis "
                             "or access to a particular speech model.")
            return response.status, "Unexpected Google Voices API response."
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return 404, ("Google could not retrieve this stored voice with the "
                         "supplied key. Check the original Google AI Studio "
                         "project, voice ID and expiry; a 404 does not establish "
                         "which of those is responsible.")
        if exc.code == 403:
            return 403, ("Google denied access to this stored voice; check "
                         "project ownership, API permissions and TTS access.")
        if exc.code == 401:
            return 401, "Google API key authentication failed."
        if exc.code == 400:
            return 400, ("Google rejected the lookup request. Check the voice "
                         "ID format and Google API key configuration; this "
                         "response does not establish voice ownership.")
        if exc.code == 429:
            return 429, "Google rate-limited the voice lookup; try again later."
        return exc.code, f"Google Voices API returned HTTP {exc.code}."
    except urllib.error.URLError:
        return 0, "Unable to reach Google's Voices API; check the connection."
    except (TimeoutError, OSError):
        return 0, "The Google Voices API lookup failed locally; check the connection."


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
