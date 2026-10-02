"""
Narration synthesis with a content-hash cache.

* One clip per script beat; cache key = sha256(provider, model, voice, style, spoken text).
* Clips live in audio/cache/<EPISODE>/<beat-key>__<hash12>.wav; audio/manifest.json maps each
  beat key to its current clip and measured duration.
* Unchanged beats are never re-synthesised; editing one beat regenerates one clip.
* Credentials are read from the environment only (GEMINI_API_KEY or GOOGLE_API_KEY).

The Gemini REST request shape is probed at runtime (tools/tts_probe.py) instead of being assumed:
two voice-config shapes are supported and the one the API accepts is remembered in
audio/tts_runtime.json.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

from . import config as C

RUNTIME = C.AUDIO / "tts_runtime.json"


class TTSUnavailable(RuntimeError):
    pass


# ---------------------------------------------------------------- cache/manifest
def clip_hash(text: str, model: str | None = None, voice: str | None = None, style: str | None = None) -> str:
    payload = json.dumps(dict(provider=C.TTS_PROVIDER, model=model or C.GEMINI_TTS_MODEL,
                              voice=voice or C.GEMINI_TTS_VOICE, style=style or C.GEMINI_TTS_STYLE,
                              text=text), sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def load_manifest() -> dict:
    if C.AUDIO_MANIFEST.exists():
        return json.loads(C.AUDIO_MANIFEST.read_text())
    return {}


def save_manifest(m: dict) -> None:
    C.AUDIO_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    tmp = C.AUDIO_MANIFEST.with_suffix(".tmp")
    tmp.write_text(json.dumps(m, indent=1, sort_keys=True))
    tmp.replace(C.AUDIO_MANIFEST)


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def cached_clip(beat_key: str, text: str, manifest: dict | None = None) -> dict | None:
    """Return the manifest entry if a clip for exactly this text/voice exists on disk."""
    manifest = manifest if manifest is not None else load_manifest()
    e = manifest.get(beat_key)
    if not e or e.get("hash") != clip_hash(text):
        return None
    p = C.ROOT / e["path"]
    return e if p.exists() else None


# ---------------------------------------------------------------- Gemini REST
def _runtime() -> dict:
    return json.loads(RUNTIME.read_text()) if RUNTIME.exists() else {}


def _speech_config(shape: str, voice: str) -> dict:
    if shape == "prebuilt":
        return {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
    return {"voiceConfig": {"voice": voice}}


def _post(url: str, body: dict, key: str, timeout: float = 180) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def list_models() -> list[dict]:
    key = C.gemini_api_key()
    if not key:
        raise TTSUnavailable("GEMINI_API_KEY is not set in this environment")
    out, token = [], None
    while True:
        url = f"{C.GEMINI_API_BASE}/models?pageSize=200" + (f"&pageToken={token}" if token else "")
        req = urllib.request.Request(url, headers={"x-goog-api-key": key})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        out += d.get("models", [])
        token = d.get("nextPageToken")
        if not token:
            return out


def synthesize_gemini(text: str, out_path: Path, model: str | None = None, voice: str | None = None,
                      style: str | None = None, max_retries: int = 6) -> float:
    key = C.gemini_api_key()
    if not key:
        raise TTSUnavailable("GEMINI_API_KEY is not set in this environment")
    model = model or C.GEMINI_TTS_MODEL
    voice = voice or C.GEMINI_TTS_VOICE
    style = style or C.GEMINI_TTS_STYLE
    url = f"{C.GEMINI_API_BASE}/models/{model}:generateContent"
    rt = _runtime()
    shapes = [rt.get("voice_shape", "voice"), "prebuilt", "voice"]
    shapes = list(dict.fromkeys(shapes))
    prompt = f"{style}\n\n{text}"
    last_err = None
    for shape in shapes:
        body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["AUDIO"],
                                     "speechConfig": _speech_config(shape, voice)}}
        for attempt in range(max_retries):
            try:
                d = _post(url, body, key)
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:600]
                last_err = f"HTTP {e.code}: {msg}"
                if e.code in (429, 500, 502, 503, 504):
                    time.sleep(min(60, 2 ** attempt * 2))
                    continue
                d = None
                break
            except (urllib.error.URLError, TimeoutError) as e:
                last_err = repr(e)
                time.sleep(min(60, 2 ** attempt * 2))
        else:
            d = None
        if d is None:
            if last_err and last_err.startswith("HTTP 400"):
                continue          # try the other request shape
            raise TTSUnavailable(last_err or "TTS request failed")
        try:
            part = next(p for p in d["candidates"][0]["content"]["parts"] if "inlineData" in p)
        except (KeyError, IndexError, StopIteration):
            raise TTSUnavailable(f"no audio in response: {json.dumps(d)[:600]}")
        mime = part["inlineData"].get("mimeType", "")
        pcm = base64.b64decode(part["inlineData"]["data"])
        rate = int(re.search(r"rate=(\d+)", mime).group(1)) if "rate=" in mime else C.AUDIO_RATE
        if "wav" in mime:
            out_path.write_bytes(pcm)
        else:  # raw little-endian 16-bit mono PCM (audio/L16)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with wave.open(str(out_path), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(rate)
                w.writeframes(pcm)
        if rt.get("voice_shape") != shape or rt.get("mime") != mime:
            RUNTIME.parent.mkdir(parents=True, exist_ok=True)
            RUNTIME.write_text(json.dumps(dict(voice_shape=shape, mime=mime, model=model, voice=voice), indent=1))
        return wav_duration(out_path)
    raise TTSUnavailable(last_err or "TTS request failed for every request shape")


def ensure_clip(beat_key: str, text: str, manifest: dict) -> dict:
    """Synthesise (or reuse) the clip for one beat and update the manifest in memory."""
    hit = cached_clip(beat_key, text, manifest)
    if hit:
        return hit
    h = clip_hash(text)
    ep = beat_key.split("S")[0]
    rel = Path("audio/cache") / ep / f"{beat_key}__{h[:12]}.wav"
    out = C.ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = synthesize_gemini(text, out)
    words = len(text.split())
    entry = dict(hash=h, path=str(rel), duration=round(dur, 3), words=words,
                 wpm=round(words / dur * 60, 1) if dur else None,
                 model=C.GEMINI_TTS_MODEL, voice=C.GEMINI_TTS_VOICE,
                 created=time.strftime("%Y-%m-%dT%H:%M:%S"))
    manifest[beat_key] = entry
    return entry


def estimate_duration(text: str) -> float:
    words = len(text.split())
    stops = len(re.findall(r"[.?!;:]", text))
    return words / C.EST_WPM * 60 + stops * C.EST_PUNCT_PAUSE
