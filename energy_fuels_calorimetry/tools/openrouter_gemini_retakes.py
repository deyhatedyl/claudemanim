"""Re-record corrected chemistry beats through OpenRouter's Gemini 3.8 TTS.

Uses the existing Melb Teacher F1 custom voice ID from the user's private
Electrochemistry voice file; never substitutes a different voice silently.

    OPENROUTER_API_KEY=... python tools/openrouter_gemini_retakes.py --test
    OPENROUTER_API_KEY=... python tools/openrouter_gemini_retakes.py

The API key is read only from process environment, never recorded on disk.
Only the nine reviewed chemistry-audit beats are synthesized. Existing WAV
recordings and original voice configuration remain unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request
import wave

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode
from tools.reconcile_authored_narration import AUDITED_RETAKES
from tools.narration_runner import voice_id, VOICE_NAME

URL = "https://openrouter.ai/api/v1/audio/speech"
KEY_URL = "https://openrouter.ai/api/v1/key"
MODEL = "google/gemini-3.8-flash-tts"


def safe_provider_reason(body: bytes, *, voice: str = "", input_text: str = "") -> str:
    """Extract an actionable error reason without exposing user data.

    Do not echo raw HTTP responses: they may contain the request, voice ID,
    account details, or credentials. Redact before displaying any detail.
    """
    try:
        payload = json.loads(body[:10000].decode("utf-8", errors="replace"))
    except (ValueError, UnicodeError):
        return "The provider returned no readable JSON error explanation."
    if not isinstance(payload, dict):
        return "The provider returned an unexpected error response."
    err = payload.get("error", {})
    if not isinstance(err, dict):
        err = {}
    message = err.get("message", "")
    # Some upstream errors are embedded in the error's metadata.
    metadata = err.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
    raw = metadata.get("raw", "")
    if not isinstance(message, str):
        message = ""
    if not message and isinstance(raw, str):
        try:
            upstream = json.loads(raw)
            if isinstance(upstream, dict):
                nested = upstream.get("error", upstream)
                if isinstance(nested, dict):
                    message = nested.get("message", "") or ""
        except ValueError:
            message = raw
    if not isinstance(message, str) or not message.strip():
        return "No detailed error message was supplied."
    # Remove exact user-provided inputs and identifiable identifiers.
    if input_text:
        message = message.replace(input_text, "[narration text hidden]")
    if voice:
        message = message.replace(voice, "[custom voice ID hidden]")
    message = re.sub(r"(?i)bearer\s+[^\s,;}]+", "Bearer [hidden]", message)
    message = re.sub(r"sk-or-v1-[\w-]+|AIza[\w-]+", "[API key hidden]", message)
    message = re.sub(r"voice_[\w-]+|voicekey_[\w-]+", "[custom voice ID hidden]", message)
    message = re.sub(r"https?://\S+", "[URL hidden]", message)
    message = re.sub(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", "[email hidden]", message)
    return " ".join(message.split())[:280]


def diagnose_speech_error(status: int, body: bytes, *, voice: str, input_text: str) -> str:
    reason = safe_provider_reason(body, voice=voice, input_text=input_text)
    return explain_speech_error(status) + "\nProvider explanation (redacted): " + reason


def check_authentication(api_key: str) -> None:
    """Validate credentials before making a paid synthesis request.

    OpenRouter documents GET /api/v1/key for this purpose. Never display
    the key, request headers, account identity, or raw untrusted error body.
    """
    request = urllib.request.Request(
        KEY_URL, headers={"Authorization": "Bearer " + api_key})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError("Unexpected OpenRouter authentication response.")
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            raise RuntimeError(
                "OpenRouter authentication failed (HTTP 401). The key could be "
                "invalid, revoked, expired or attached to an inaccessible account. "
                "Generate a fresh API key in OpenRouter settings; do not retry "
                "the TTS request until /api/v1/key returns 200.") from None
        if exc.code == 403:
            raise RuntimeError(
                "OpenRouter authenticated request was refused (403). Check "
                "account or workspace restrictions.") from None
        raise RuntimeError(
            f"OpenRouter credential preflight returned HTTP {exc.code}.") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Could not contact OpenRouter's key-check endpoint; check internet "
            "connectivity or try later.") from None


def explain_speech_error(status: int) -> str:
    if status == 401:
        return ("HTTP 401: authentication was rejected by OpenRouter. "
                "This does not establish whether Gemini or the selected "
                "Melb Teacher F1 voice is supported.")
    if status == 400:
        return ("HTTP 400: TTS request validation failed. After successful "
                "authentication, verify model, voice identifier and format. "
                "Custom voice_ IDs may require provider-specific support.")
    if status == 402:
        return "HTTP 402: OpenRouter credits or budget may be insufficient."
    if status == 403:
        return "HTTP 403: the key/account may lack access to this model or voice."
    if status == 404:
        return "HTTP 404: check model availability and the speech endpoint."
    if status == 429:
        return "HTTP 429: rate limit reached; wait and retry."
    return f"HTTP {status}: TTS synthesis failed (no private request data logged)."


def synthesize(text: str, voice: str, api_key: str, dest: Path):
    req = urllib.request.Request(
        URL,
        data=json.dumps({
            "model": MODEL,
            "voice": voice,
            "input": text,
            "response_format": "pcm",
        }).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as resp:
            audio = resp.read()
            mime = resp.headers.get("Content-Type", "").lower()
    except urllib.error.HTTPError as exc:
        # Raw error bodies are untrusted and can contain private details.
        raise RuntimeError(diagnose_speech_error(
            exc.code, exc.read(10000), voice=voice, input_text=text)) from None
    if len(audio) < 4096:
        raise ValueError("Gemini returned implausibly little audio.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if mime.startswith("audio/wav") or audio[:4] == b"RIFF":
        dest.write_bytes(audio)
    elif "audio/pcm" in mime or "application/octet-stream" in mime:
        rate_match = re.search(r"rate=(\d+)", mime)
        channels_match = re.search(r"channels=(\d+)", mime)
        rate = int(rate_match.group(1)) if rate_match else 24000
        channels = int(channels_match.group(1)) if channels_match else 1
        if channels != 1:
            raise ValueError("Received multi-channel PCM; cannot import as mono.")
        if rate != 24000:
            raise ValueError(f"PCM sample rate {rate} Hz requires conversion to 24 kHz.")
        if len(audio) % 2:
            raise ValueError("PCM audio has odd byte count.")
        with wave.open(str(dest), "wb") as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(rate)
            out.writeframes(audio)
    else:
        raise ValueError(f"Unexpected Gemini TTS content-type {mime!r}")
    with wave.open(str(dest), "rb") as result:
        if (result.getframerate(), result.getnchannels(), result.getsampwidth()) != (24000, 1, 2):
            raise ValueError("Audio WAV format incompatible with existing narration pipeline.")
        duration = result.getnframes() / 24000.0
    return duration


def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("--test", action="store_true", help="Synthesize one 9-beat correction for voice compatibility")
    cli.add_argument("--interval", type=float, default=21.0)
    cli.add_argument("--voice-file", type=Path)
    cli.add_argument("--check-auth", action="store_true",
                     help="Validate the OpenRouter key; do not generate audio")
    cli.add_argument("--probe", action="store_true",
                     help="Generate 1 short sentence with the SAME custom Gemini voice to isolate voice access from input-length issues")
    args = cli.parse_args()
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY is not set in this process. Export a new key "
              "privately in Terminal; never paste it into chat or the repository.",
              file=sys.stderr)
        return 2
    try:
        check_authentication(key)
    except RuntimeError as exc:
        print(f"Authentication check: {exc}", file=sys.stderr)
        return 3
    if args.check_auth:
        print("OpenRouter authentication succeeded (HTTP 200). "
              "The Gemini model and custom voice have NOT been tested yet.")
        return 0
    voice, source = voice_id(argparse.Namespace(
        voice_id=None, voice_file=str(args.voice_file) if args.voice_file else None, lite=False))
    if args.probe:
        path = ROOT / "audio" / "gemini_retakes" / "voice_probe.wav"
        try:
            duration = synthesize(
                "Welcome to the VCE Chemistry lesson.", voice, key, path)
        except RuntimeError as exc:
            print(f"Same-voice short probe failed: {exc}", file=sys.stderr)
            return 4
        print(f"Same-voice probe succeeded ({duration:.1f}s): {path}")
        print("The voice works with a short input; the longer test segment or its text may be the issue.")
        return 0
    voice_fingerprint = hashlib.sha256(voice.encode("utf-8")).hexdigest()
    beats = {b.key: b for ep in ("E06", "E07", "E08", "E12", "E14")
             for b in load_episode(ep).beats()}
    all_keys = sorted(AUDITED_RETAKES)
    keys = ["E12S02.b01"] if args.test else all_keys
    target = ROOT / "audio" / "gemini_retakes"
    target.mkdir(parents=True, exist_ok=True)
    done = {}
    for index, beat_key in enumerate(keys):
        beat = beats[beat_key]
        dest = target / (beat_key + ".wav")
        digest = hashlib.sha256(beat.text.encode()).hexdigest()
        meta = dest.with_suffix(".wav.json")
        if dest.is_file() and meta.is_file():
            old = json.loads(meta.read_text())
            if (old.get("text_sha256") == digest
                    and old.get("model") == MODEL
                    and old.get("voice_fingerprint") == voice_fingerprint):
                done[beat_key] = {"file": str(dest.resolve()), "start": 0.0, "end": old["duration_seconds"]}
                print(f"REUSED {beat_key}")
                continue
        if index:
            time.sleep(max(0.0, args.interval))
        duration = synthesize(beat.text, voice, key, dest)
        meta.write_text(json.dumps({
            "text_sha256": digest, "model": MODEL, "voice_label": VOICE_NAME,
            "voice_fingerprint": voice_fingerprint,
            "voice_source": source, "provider": "OpenRouter", "duration_seconds": duration,
        }, indent=2))
        done[beat_key] = {"file": str(dest.resolve()), "start": 0.0, "end": duration}
        print(f"CREATED {beat_key}: {duration:.2f}s via Gemini")
    if not args.test and len(done) == len(all_keys):
        (target / "segments.json").write_text(json.dumps(done, indent=2))
        print(f"All nine Gemini TTS retakes ready in {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
