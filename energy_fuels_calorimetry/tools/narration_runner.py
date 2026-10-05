#!/usr/bin/env python3
"""Gemini narration for VCE Chemistry - Energy, Fuels and Calorimetry, Episodes 1-14.

The narration is embedded in this file. No separate text files are required.
Install once: python3.12 -m pip install --upgrade google-genai
Run: python3.12 narration_tts.py ep1 --lite
Use --force to regenerate matching files; --beats makes smaller beat clips.
Use --dry-run to list the selection without calling Google or asking for a key.
"""
from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import wave
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
FLASH_MODEL = "gemini-3.8-flash-tts"
LITE_MODEL = "gemini-3.8-flash-lite-tts"
VOICE_NAME = "Melb Teacher F1"
DEFAULT_PREFIX = None
STYLE = (
    "Clear, warm Australian high-school chemistry teacher explaining to one Year 12 student; "
    "calm, steady pace; friendly but precise. Aim for about 145 words per minute, slightly "
    "slower for numbers and equations. Articulate decimal numbers, chemical names and units "
    "clearly. Read the supplied transcript exactly without adding an introduction, commentary "
    "or music. Do not add long thinking pauses; these are inserted separately in the video."
)

# Each entry is an unchanged narration beat from the reviewed video scripts.
BEATS = []


def normalized_prefix(value: str) -> str:
    value = value.strip()
    if value.lower() in {"all", "*"}:
        return ""
    alias = re.fullmatch(r"(?:ep|e)?0?(\d{1,2})", value, flags=re.IGNORECASE)
    if alias and 1 <= int(alias.group(1)) <= 14:
        return f"E{int(alias.group(1)):02d}"
    return value.upper()


def selected_jobs(prefix: str, use_beats: bool) -> list[tuple[str, str]]:
    prefix = normalized_prefix(prefix)
    if use_beats:
        rows = [(b["key"], b["text"]) for b in BEATS]
    else:
        grouped: dict[str, list[str]] = {}
        for b in BEATS:
            grouped.setdefault(b["scene"], []).append(b["text"])
        rows = [(sid, "\n\n".join(texts)) for sid, texts in grouped.items()]
    return [(sid, text) for sid, text in rows if sid.upper().startswith(prefix)]


def voice_id(args) -> tuple[str, str]:
    if args.voice_id:
        return args.voice_id.strip(), "explicit voice ID"
    if os.environ.get("GEMINI_TTS_VOICE_ID", "").strip():
        return os.environ["GEMINI_TTS_VOICE_ID"].strip(), "GEMINI_TTS_VOICE_ID"
    candidates = [Path(args.voice_file).expanduser()] if args.voice_file else [
        ROOT / "voice_samples_melb" / "voice_ids.txt",
        ROOT.parent / "Electrochemistry" / "voice_samples_melb" / "voice_ids.txt",
        ROOT.parent / "voice_samples_melb" / "voice_ids.txt",
        Path.home() / "Downloads" / "VCE-Chemistry-Videos" / "Electrochemistry"
        / "voice_samples_melb" / "voice_ids.txt",
    ]
    labels = [f"{VOICE_NAME} Lite", VOICE_NAME] if args.lite else [VOICE_NAME]
    for f in dict.fromkeys(candidates):
        if not f.is_file():
            continue
        ids = {}
        for line in f.read_text(encoding="utf-8-sig").splitlines():
            if line.strip().startswith("#") or ":" not in line:
                continue
            k, v = line.split(":", 1)
            if v.strip():
                ids[k.strip()] = v.strip()
        for label in labels:
            if label in ids:
                return ids[label], label
    raise ValueError(
        f"Couldn't find '{VOICE_NAME}' in voice_samples_melb/voice_ids.txt.\n"
        "Your existing Electrochemistry voice file is checked automatically. You can also use\n"
        "  --voice-file ~/Downloads/VCE-Chemistry-Videos/Electrochemistry/voice_samples_melb/voice_ids.txt\n"
        "or --voice-id YOUR_EXISTING_VOICE_ID. No new voice is created."
    )


def wav_duration(data: bytes) -> float:
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError("Google returned audio without a WAV header; no WAV was saved.")
    with wave.open(io.BytesIO(data), "rb") as w:
        frames, channels, width, rate = (
            w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        )
        if not frames or channels != 1 or width != 2 or rate != 24000:
            raise ValueError("Expected a nonempty 24 kHz, mono, 16-bit WAV.")
        if len(w.readframes(frames)) != frames * channels * width:
            raise ValueError("Audio was truncated; no WAV was saved.")
        return frames / rate


def ready(dest: Path, text: str) -> bool:
    if not dest.is_file():
        return False
    try:
        wav_duration(dest.read_bytes())
        meta = dest.with_suffix(".wav.json")
        if meta.is_file():
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            metadata = json.loads(meta.read_text(encoding="utf-8"))
            if not isinstance(metadata, dict) or metadata.get("text_sha256") != digest:
                return False
        return True
    except (OSError, ValueError, EOFError, wave.Error):
        return False


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".narration-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def save_response(response, dest: Path, text: str, model: str, label: str) -> float:
    audio = getattr(response, "output_audio", None)
    if audio is None or not getattr(audio, "data", None):
        raise ValueError("Google returned no audio. No output file was created.")
    # Unary Gemini 3.8 TTS returns a complete WAV, not headerless streaming PCM.
    data = base64.b64decode(audio.data, validate=True)
    duration = wav_duration(data)
    atomic_write(dest, data)
    meta = {
        "section": dest.stem,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "model": model,
        "voice_label": label,
        "duration_seconds": round(duration, 6),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    atomic_write(dest.with_suffix(".wav.json"), (json.dumps(meta, indent=2) + "\n").encode())
    return duration


def request_audio(client, model: str, text: str, vid: str):
    return client.interactions.create(
        model=model,
        input=[{"type": "user_input", "content": [{
            "type": "text", "text": text,
            "annotations": [{"type": "speech_metadata", "style": STYLE}],
        }]}],
        response_format={"type": "audio"},
        generation_config={"speech_config": [{"voice": vid}]},
    )


def daily_limit(message: str) -> bool:
    compact = re.sub(r"[\s_-]+", "", message.lower())
    return "perday" in compact or "daily" in compact


def parse_args(argv=None):
    p = argparse.ArgumentParser(description='VCE Chemistry - Energy, Fuels and Calorimetry, Episodes 1-14')
    p.add_argument("prefix", nargs="?", default=DEFAULT_PREFIX,
                   help="ep4, ep10, E04S03, or all; this file only contains its listed episodes")
    p.add_argument("--lite", action="store_true", help="use Gemini 3.8 Flash-Lite TTS")
    p.add_argument("--force", action="store_true", help="regenerate selected files")
    p.add_argument("--beats", action="store_true", help="one WAV per narration beat instead of per scene")
    p.add_argument("--dry-run", action="store_true", help="list files; no key, SDK or API calls needed")
    p.add_argument("--voice-file", help="path to your existing voice_ids.txt")
    p.add_argument("--voice-id", help="use your existing voice ID directly")
    p.add_argument("--output", type=Path, default=ROOT / "audio" / "raw")
    p.add_argument("--interval", type=float, default=21.0,
                   help="minimum seconds between request starts (default: 21)")
    args = p.parse_args(argv)
    if args.prefix is None:
        p.error("choose an episode prefix or all")
    if args.interval < 0:
        p.error("--interval must be nonnegative")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    model = LITE_MODEL if args.lite else FLASH_MODEL
    jobs = selected_jobs(args.prefix, args.beats or "." in args.prefix)
    if not jobs:
        print(f"No narration matches '{args.prefix}' in this Python file.", file=sys.stderr)
        return 1
    out = args.output.expanduser().resolve()
    print(f"Model: {model}\nOutput: {out}")
    pending = []
    for sid, text in jobs:
        dest = out / f"{sid}.wav"
        done = not args.force and ready(dest, text)
        if done:
            print(f"{sid}: already done (use --force to redo)")
        else:
            pending.append((sid, text, dest))
        if args.dry_run:
            print(f"  {sid}.wav: {len(text)} characters; {'skip' if done else 'generate'}")
    if args.dry_run:
        print(f"Dry run: {len(jobs)} selected; {len(pending)} would be generated. No API calls made.")
        return 0
    if not pending:
        print(f"\n{len(jobs)}/{len(jobs)} sections ready. No API call needed.")
        return 0
    try:
        vid, label = voice_id(args)
        from google import genai
    except ImportError:
        print("Install/update the SDK first: python3.12 -m pip install --upgrade google-genai",
              file=sys.stderr)
        return 1
    except (OSError, ValueError) as e:
        print(e, file=sys.stderr)
        return 1
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        key = getpass.getpass("Paste your Gemini API key (hidden): ").strip()
    if not key.strip():
        print("No API key supplied.", file=sys.stderr)
        return 1
    key = key.strip()
    try:
        client = genai.Client(api_key=key)
    except Exception as e:
        print(f"Couldn't initialise Gemini: {str(e).replace(key, '[hidden API key]')}",
              file=sys.stderr)
        return 1
    ok = len(jobs) - len(pending)
    last_start = None
    waits = [65, 120, 180, 240]
    print(f"Voice: {label}\nGenerating {len(pending)} sections. Existing WAVs are kept when switching models.")
    try:
        for sid, text, dest in pending:
            print(f"{sid}: {len(text)} characters...", flush=True)
            limited_attempts = transient_attempts = 0
            while True:
                if last_start is not None:
                    time.sleep(max(0.0, args.interval - (time.monotonic() - last_start)))
                last_start = time.monotonic()
                try:
                    response = request_audio(client, model, text, vid)
                except Exception as e:
                    msg = str(e).replace(key, "[hidden API key]")
                    lower = msg.lower()
                    limited = "429" in msg or "resource_exhausted" in lower or "quota" in lower
                    if limited:
                        if limited_attempts == 0:
                            print("  Google says:", msg[:700].replace("\n", " "), flush=True)
                        if daily_limit(msg):
                            other = "remove --lite" if args.lite else "add --lite"
                            print(f"Daily limit reached. {ok}/{len(jobs)} sections ready; {other} to try the other model.")
                            return 2
                        if limited_attempts < len(waits):
                            delay = waits[limited_attempts]
                            limited_attempts += 1
                            print(f"  Waiting {delay} seconds, then retrying...", flush=True)
                            time.sleep(delay)
                            continue
                        print(f"Still limited. {ok}/{len(jobs)} sections ready. Rerun later to resume.")
                        return 2
                    transient = any(s in lower for s in (
                        "500", "502", "503", "504", "unavailable", "timeout", "timed out", "connection"
                    ))
                    if transient and transient_attempts < 2:
                        transient_attempts += 1
                        print("  Temporary error; waiting 25 seconds, then retrying...", flush=True)
                        time.sleep(25)
                        continue
                    print(f"FAILED: {msg[:1000]}\n{ok}/{len(jobs)} sections ready. Fix the error and rerun.",
                          file=sys.stderr)
                    return 1
                # Local validation/write failures must not trigger another billable API request.
                try:
                    duration = save_response(response, dest, text, model, label)
                except (OSError, ValueError, EOFError, wave.Error) as e:
                    print(f"Couldn't save {sid}: {e}. Fix the problem before retrying.", file=sys.stderr)
                    return 1
                print(f"  Saved {dest.name} ({duration:.1f} seconds)", flush=True)
                ok += 1
                break
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()
    print(f"\n{ok}/{len(jobs)} sections ready. ZIP {out} and send it back for syncing.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped. Completed WAVs are kept; rerun the same command to resume.")
        raise SystemExit(130)
