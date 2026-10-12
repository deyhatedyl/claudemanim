"""Re-record corrected chemistry beats through OpenRouter's Gemini 3.8 TTS.

Defaults to the warm Sulafat Gemini studio voice; an explicitly supplied
private voice file remains supported. Voice selection is recorded.

    OPENROUTER_API_KEY=... python tools/openrouter_gemini_retakes.py --test
    OPENROUTER_API_KEY=... python tools/openrouter_gemini_retakes.py

The API key is read only from process environment, never recorded on disk.
Only the ten reviewed chemistry-correction beats are synthesized. Existing WAV
recordings and original voice configuration remain unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request
import wave
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode
from tools.reconcile_authored_narration import AUDITED_RETAKES
from tools.narration_runner import atomic_write, voice_id, wav_duration

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
    upstream_message = ""
    if isinstance(raw, str):
        try:
            upstream = json.loads(raw)
            if isinstance(upstream, dict):
                nested = upstream.get("error", upstream)
                if isinstance(nested, dict):
                    upstream_message = nested.get("message", "") or ""
        except ValueError:
            upstream_message = raw
    elif isinstance(raw, dict):
        nested = raw.get("error", raw)
        if isinstance(nested, dict):
            upstream_message = nested.get("message", "") or ""
    if isinstance(upstream_message, str) and upstream_message:
        # Upstream details can be more useful than generic OpenRouter wording.
        if not message or any(x in message.casefold() for x in (
                "provider returned", "provider error", "bad request", "validation failed")):
            message = upstream_message
    # Never echo free-form provider text: it can contain arbitrary account fields,
    # partial transcript fragments, and secrets that regex redaction cannot know.
    lowered = message.casefold() if isinstance(message, str) else ""
    if "unknown voice" in lowered:
        return "Unknown voice identifier."
    if "voice" in lowered and "not available" in lowered:
        return "Selected voice is not available."
    if "voice" in lowered and "not found" in lowered:
        return "Selected voice not found by provider."
    if "model" in lowered and ("not found" in lowered or "not available" in lowered):
        return "Selected speech model not available."
    if "unsupported" in lowered:
        return "A requested speech option is unsupported."
    if "invalid" in lowered:
        return "Provider reports invalid speech request parameters."
    return "Provider rejected the request; private response details omitted."


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
                "voice is supported.")
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
    except urllib.error.URLError:
        raise RuntimeError("Could not reach OpenRouter speech endpoint.") from None
    if len(audio) < 4096:
        raise ValueError("Gemini returned implausibly little audio.")
    if mime.startswith("audio/wav") or audio[:4] == b"RIFF":
        prepared = audio
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
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(rate)
            out.writeframes(audio)
        prepared = buffer.getvalue()
    else:
        raise ValueError("Unexpected speech audio content type.")
    duration = wav_duration(prepared)
    atomic_write(dest, prepared)
    return duration


def cached_duration(dest: Path, text: str, voice: str) -> float | None:
    """Reject stale/malformed cache, including WAV bytes that changed on disk."""
    meta = dest.with_suffix(".wav.json")
    if not dest.is_file() or not meta.is_file():
        return None
    try:
        record = json.loads(meta.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or record.get("provider") != "OpenRouter":
            return None
        if record.get("model") != MODEL:
            return None
        if record.get("text_sha256") != hashlib.sha256(text.encode("utf-8")).hexdigest():
            return None
        if record.get("voice_fingerprint") != hashlib.sha256(voice.encode("utf-8")).hexdigest():
            return None
        wav = dest.read_bytes()
        if record.get("audio_sha256") != hashlib.sha256(wav).hexdigest():
            return None
        duration = wav_duration(wav)
        if abs(float(record.get("duration_seconds", -1)) - duration) > 0.02:
            return None
        return duration
    except (OSError, ValueError, TypeError, UnicodeError, EOFError, wave.Error):
        return None


def main(argv=None) -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("--test", action="store_true", help="Synthesize one corrected beat for voice compatibility")
    cli.add_argument("--dry-run", action="store_true", help="Show exactly ten selected beats without credentials or API calls")
    cli.add_argument("--interval", type=float, default=21.0)
    cli.add_argument("--voice-file", type=Path)
    cli.add_argument("--studio-voice", default="Sulafat",
                     help="Gemini prebuilt warm voice (no custom voice ID); default Sulafat")
    cli.add_argument("--check-auth", action="store_true",
                     help="Validate the OpenRouter key; do not generate audio")
    cli.add_argument("--probe", action="store_true",
                     help="One paid short preset/custom-voice sample; stored with a unique name under probes/")
    args = cli.parse_args(argv)
    if args.interval < 0:
        cli.error("--interval must be nonnegative")
    if args.probe and args.test:
        cli.error("--test and --probe are mutually exclusive")
    all_keys = sorted(AUDITED_RETAKES)
    if len(all_keys) != 10 or "E13S15.b01" not in all_keys:
        print("Ten-retake manifest is inconsistent.", file=sys.stderr)
        return 2
    if args.dry_run:
        if args.probe:
            print("One short voice probe would be generated in probes/ (billable without --dry-run).")
        else:
            for beat_key in (["E12S02.b01"] if args.test else all_keys):
                print(f"  {beat_key}: would generate/validate")
        print("Offline dry run; no credentials or API requests used.")
        return 0
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
              "The Gemini model and selected voice have NOT been tested yet.")
        return 0
    try:
        voice, source = voice_id(argparse.Namespace(
            voice_id=None, voice_file=str(args.voice_file) if args.voice_file else None,
            studio_voice=None if args.voice_file else args.studio_voice, lite=False))
    except (ValueError, OSError):
        print("Voice selection failed. Verify the private file or studio voice name.",
              file=sys.stderr)
        return 2
    if args.probe:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        path = ROOT / "audio" / "gemini_retakes" / "probes" / f"openrouter_voice_probe_{stamp}.wav"
        try:
            duration = synthesize(
                "Good morning, Year Twelve. Let's check the units in this calorimetry question.", voice, key, path)
        except (RuntimeError, ValueError, OSError) as exc:
            print(f"Selected-voice short probe failed: {exc}", file=sys.stderr)
            return 4
        print(f"Selected-voice probe succeeded ({duration:.1f}s): {path}")
        print("Listen for accent and tone; OpenRouter's speech endpoint does not expose Google's native speech_metadata style field.")
        return 0
    voice_fingerprint = hashlib.sha256(voice.encode("utf-8")).hexdigest()
    beats = {b.key: b for ep in ("E06", "E07", "E08", "E12", "E13", "E14")
             for b in load_episode(ep).beats()}
    if any(key not in beats for key in all_keys):
        print("Retake manifest references missing script beats.", file=sys.stderr)
        return 2
    keys = ["E12S02.b01"] if args.test else all_keys
    target = ROOT / "audio" / "gemini_retakes"
    target.mkdir(parents=True, exist_ok=True)
    done = {}
    for index, beat_key in enumerate(keys):
        beat = beats[beat_key]
        dest = target / (beat_key + ".wav")
        digest = hashlib.sha256(beat.text.encode()).hexdigest()
        meta = dest.with_suffix(".wav.json")
        cached = cached_duration(dest, beat.text, voice)
        if cached is not None:
            done[beat_key] = {"file": str(dest.resolve()), "start": 0.0, "end": cached}
            print(f"REUSED {beat_key}")
            continue
        if index:
            time.sleep(max(0.0, args.interval))
        try:
            duration = synthesize(beat.text, voice, key, dest)
        except (RuntimeError, ValueError, OSError) as exc:
            print(f"{beat_key}: synthesis stopped: {exc}", file=sys.stderr)
            return 4
        metadata = {
            "text_sha256": digest, "model": MODEL, "voice_label": source,
            "voice_fingerprint": voice_fingerprint,
            "voice_source": source, "provider": "OpenRouter", "duration_seconds": duration,
            "audio_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
        }
        atomic_write(meta, (json.dumps(metadata, indent=2) + "\n").encode("utf-8"))
        done[beat_key] = {"file": str(dest.resolve()), "start": 0.0, "end": duration}
        print(f"CREATED {beat_key}: {duration:.2f}s via Gemini")
    if not args.test and len(done) == len(all_keys):
        atomic_write(target / "segments.json", (json.dumps(done, indent=2) + "\n").encode("utf-8"))
        print(f"All {len(all_keys)} Gemini TTS retakes ready in {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
