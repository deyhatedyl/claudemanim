"""Offline, fail-closed import of ALL ten OpenRouter/Gemini corrected narration beats.

  python tools/ingest_openrouter_retakes.py --check  # safe default; requires all ten
  python tools/ingest_openrouter_retakes.py --apply  # local CTC forced word alignment

No keys, network API calls, resynthesis, time stretching, or edits to original WAVs.
Run --apply only when other workers are NOT writing the same active alignment files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import wave

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode
from shared.tts import manual_text_hash
from tools.reconcile_authored_narration import AUDITED_RETAKES

EPS = ("E06", "E07", "E08", "E12", "E13", "E14")
SOURCE = "openrouter_gemini_retake"
MODEL = "google/gemini-3.8-flash-tts"
MIN_FREE = 750 * 1024 * 1024


class Rejected(ValueError):
    """Retakes are missing, stale, inconsistent, or cannot be safely installed."""


def read_map(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(result, dict):
            raise ValueError("not an object")
        return result
    except (OSError, UnicodeError, ValueError):
        raise Rejected(f"{path.name}: invalid JSON object") from None


def expected_beats() -> dict[str, str]:
    beats = {b.key: b.text for ep in EPS for b in load_episode(ep).beats()}
    if len(AUDITED_RETAKES) != 10 or "E13S15.b01" not in AUDITED_RETAKES:
        raise Rejected("Audited correction manifest must have exactly ten keys including E13S15.b01")
    if not AUDITED_RETAKES <= beats.keys():
        raise Rejected(f"Missing corrected script keys: {sorted(AUDITED_RETAKES - beats.keys())}")
    return {key: beats[key] for key in sorted(AUDITED_RETAKES)}


def measured_wav_duration(wav: Path) -> float:
    try:
        with wave.open(str(wav), "rb") as stream:
            if (stream.getnchannels(), stream.getsampwidth(), stream.getframerate(),
                    stream.getcomptype()) != (1, 2, 24000, "NONE"):
                raise Rejected(f"{wav.name}: expected mono 24kHz 16-bit PCM WAV")
            duration = stream.getnframes() / stream.getframerate()
    except (OSError, EOFError, wave.Error):
        raise Rejected(f"{wav.name}: unreadable/corrupt WAV") from None
    if not 0.5 < duration <= 180:
        raise Rejected(f"{wav.name}: implausible measured beat duration")
    return duration


def inspect_one(key: str, text: str, directory: Path, voice: str) -> dict:
    wav = directory / (key + ".wav")
    meta_path = directory / (key + ".wav.json")
    if not wav.is_file() or not meta_path.is_file():
        missing = [p.name for p in (wav, meta_path) if not p.is_file()]
        raise Rejected(f"{key}: missing {', '.join(missing)}")
    if wav.is_symlink() or meta_path.is_symlink():
        raise Rejected(f"{key}: retake symlinks are prohibited")
    meta = read_map(meta_path)
    voice_label = "Gemini studio voice: " + voice
    fields = {
        "provider": "OpenRouter", "model": MODEL,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "voice_fingerprint": hashlib.sha256(voice.encode("utf-8")).hexdigest(),
        "voice_label": voice_label, "voice_source": voice_label,
    }
    for field, value in fields.items():
        if meta.get(field) != value:
            raise Rejected(f"{key}: invalid {field} (not consistent with corrected script/settings)")
    with wav.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if meta.get("audio_sha256") != digest or wav.stat().st_size < 4096:
        raise Rejected(f"{key}: audio bytes/hash inconsistent with metadata")
    duration = measured_wav_duration(wav)
    try:
        recorded = float(meta["duration_seconds"])
    except (TypeError, ValueError, KeyError):
        raise Rejected(f"{key}: missing measured duration") from None
    if not 0 < recorded <= 180 or abs(recorded - duration) > 0.02:
        raise Rejected(f"{key}: WAV duration differs from metadata")
    return {"key": key, "text": text, "wav": wav, "meta": meta_path,
            "duration": duration, "audio_sha256": digest,
            "voice_fingerprint": fields["voice_fingerprint"]}


def validate_existing(root: Path, expected: dict, manifest: dict) -> None:
    # A stale manually sliced ORIGINAL, even with a matching manifest text
    # hash (the old E08S06.b06 bug), cannot qualify as a Gemini retake.
    errors = []
    for key in expected:
        entry = manifest.get(key)
        if entry is not None and (
            not isinstance(entry, dict) or entry.get("source") != SOURCE
        ):
            errors.append(f"{key}: stale/non-Gemini manifest entry; quarantine it first")
    for ep in EPS:
        for name in ("words.json", "segments.json"):
            old = read_map(root / "audio" / "aligned" / ep / name)
            for key in old.keys() & expected.keys():
                if manifest.get(key, {}).get("source") != SOURCE:
                    errors.append(f"{key}: stale original active {ep}/{name}; quarantine first")
    if errors:
        raise Rejected("\n  ".join(errors))


def preflight(root: Path, directory: Path, voice: str,
              expected: dict[str, str] | None = None) -> tuple[dict, dict]:
    expected = expected if expected is not None else expected_beats()
    if len(expected) != 10 or not voice or voice != voice.strip():
        raise Rejected("Exactly ten audited beats and one pinned studio voice required")
    try:
        directory.resolve().relative_to(root.resolve())
    except ValueError:
        raise Rejected("Private retake directory must be inside this project's audio tree") from None
    manifest = read_map(root / "audio" / "manifest.json")
    failures = []
    try:
        validate_existing(root, expected, manifest)
    except Rejected as error:
        failures.append(str(error))
    extra = sorted(p.name for p in directory.glob("*.wav") if p.stem not in expected)
    if extra:
        failures.append(f"Unexpected WAVs in retake directory: {', '.join(extra)}")
    approved = {}
    for key, text in expected.items():
        try:
            approved[key] = inspect_one(key, text, directory, voice)
        except Rejected as error:
            failures.append(str(error))
    if failures:
        raise Rejected(
            f"Preflight rejected ({len(approved)}/10 verified); no changes made:\n  "
            + "\n  ".join(failures))
    return approved, manifest


def align_measured(approved: dict) -> dict:
    """Per-beat local CTC measured words, never a guessed WPM timeline."""
    import torch
    import torchaudio
    from types import SimpleNamespace
    from tools.align_manual_audio import align_scene
    torch.set_num_threads(2)
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model, labels = bundle.get_model().eval(), bundle.get_labels()
    results = {}
    for key, item in approved.items():
        beat = SimpleNamespace(key=key, text=item["text"])
        scene = SimpleNamespace(id=key.split(".")[0], beats=[beat])
        _, words, report = align_scene(scene, item["wav"], model, labels)
        if float(report["greedy_transcription_similarity"]) < 0.90:
            raise Rejected(f"{key}: CTC acoustic similarity below 0.90; check recording")
        results[key] = (words[key], report)
        print(f"ALIGNED {key} ({len(words[key])} measured words)", flush=True)
    return results


def check_words(item: dict, aligned: list) -> None:
    if not aligned or " ".join(row["word"] for row in aligned) != item["text"]:
        raise Rejected(f'{item["key"]}: measured word transcript differs from corrected script')
    last = -0.001
    for word in aligned:
        start, end = float(word["start"]), float(word["end"])
        if start < -0.05 or start < last - 0.02 or start >= end or end > item["duration"] + 0.08:
            raise Rejected(f'{item["key"]}: out-of-order or out-of-range measured word alignment')
        last = end


def install_payloads(changes: dict[Path, bytes], private_audio: Path) -> None:
    """Prepare everything, publish manifest last, rollback on any write failure."""
    private_audio.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="retake-import-txn-", dir=private_audio) as folder:
        td = Path(folder)
        old, staged = {}, {}
        for i, (target, payload) in enumerate(changes.items()):
            staged_file = td / f"new-{i}"
            staged_file.write_bytes(payload)
            staged[target] = staged_file
            old[target] = target.read_bytes() if target.exists() else None
        updated = []
        try:
            for target, file in staged.items():
                # Detect an independent worker's intervening update rather than
                # overwriting their E13/E14 words or shared audio manifest.
                live = target.read_bytes() if target.exists() else None
                if live != old[target]:
                    raise Rejected(f"{target.name}: changed concurrently; no retakes committed")
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(file, target)
                updated.append(target)
        except BaseException:
            for target in reversed(updated):
                previous = old[target]
                if previous is None:
                    target.unlink(missing_ok=True)
                else:
                    restore = td / "rollback"
                    restore.write_bytes(previous)
                    os.replace(restore, target)
            raise


def apply_verified(root: Path, approved: dict, *, voice: str,
                   aligner=align_measured) -> dict:
    """All-or-nothing retake-only update; never touch unchanged beat clips."""
    if len(approved) != 10 or set(approved) != set(expected_beats()):
        raise Rejected("Refusing to import fewer than all ten audited corrected keys")
    if shutil.disk_usage(root).free < MIN_FREE:
        raise Rejected("Insufficient free disk: 750 MiB minimum for local alignment")
    result = aligner(approved)
    if set(result) != set(approved):
        raise Rejected("Alignment returned an incomplete/extra set of retake keys")
    for key, item in approved.items():
        check_words(item, result[key][0])
        # Source bytes and sidecars may have changed during slow CTC alignment.
        refreshed = inspect_one(key, item["text"], item["wav"].parent, voice)
        if refreshed != item:
            raise Rejected(f"{key}: source changed during alignment")
    manifest_path = root / "audio" / "manifest.json"
    current = read_map(manifest_path)
    validate_existing(root, approved, current)
    next_manifest = dict(current)
    changes: dict[Path, bytes] = {}
    for key, item in approved.items():
        rel = Path("audio") / "cache" / key[:3] / (
            key + "__retake_" + manual_text_hash(item["text"])[:12] + ".wav")
        target = root / rel
        wav_bytes = item["wav"].read_bytes()   # direct byte-copy, NO resampling/stretch
        if hashlib.sha256(wav_bytes).hexdigest() != item["audio_sha256"]:
            raise Rejected(f"{key}: source WAV changed")
        if target.exists() and target.read_bytes() != wav_bytes:
            raise Rejected(f"{key}: conflicting existing retake cache WAV")
        if not target.exists():
            changes[target] = wav_bytes
        next_manifest[key] = {
            "source": SOURCE, "text_hash": manual_text_hash(item["text"]),
            "path": str(rel), "metadata_path": str(item["meta"].relative_to(root)),
            "duration": item["duration"], "audio_sha256": item["audio_sha256"],
            "model": MODEL, "voice_fingerprint": item["voice_fingerprint"],
        }
    # Latest disk state is read only after alignment, so original-audio edits
    # by another worker aren't replaced by an earlier snapshot.
    for ep in EPS:
        keys = [k for k in approved if k.startswith(ep)]
        if not keys:
            continue
        folder = root / "audio" / "aligned" / ep
        aligned_words = read_map(folder / "words.json")
        segments = read_map(folder / "segments.json")
        reviews = read_map(folder / "retake-alignment-review.json")
        for key in keys:
            item = approved[key]
            aligned_words[key] = result[key][0]
            segments[key] = {
                "file": str(item["wav"].resolve()), "start": 0.0,
                "end": item["duration"],
            }
            reviews[key] = {**result[key][1], "source": SOURCE}
        for name, contents in (
            ("words.json", aligned_words), ("segments.json", segments),
            ("retake-alignment-review.json", reviews)
        ):
            changes[folder / name] = (json.dumps(contents, indent=2) + "\n").encode("utf-8")
    # Manifest is installed LAST, when every audio clip and word timestamp is ready.
    changes[manifest_path] = (json.dumps(next_manifest, indent=1, sort_keys=True) + "\n").encode("utf-8")
    install_payloads(changes, root / "audio")
    return {"imported": 10, "keys": sorted(approved), "source": SOURCE,
            "word_alignment": "measured local Wav2Vec2 CTC"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="Read-only, default")
    action.add_argument("--apply", action="store_true", help="Require all ten; align words; import")
    parser.add_argument("--directory", type=Path, default=ROOT / "audio" / "gemini_retakes")
    parser.add_argument("--studio-voice", default="Sulafat")
    args = parser.parse_args(argv)
    try:
        approved, _ = preflight(ROOT, args.directory.resolve(), args.studio_voice)
        print("PREFLIGHT PASS: all ten corrected WAVs and OpenRouter/Gemini sidecars verified")
        if args.apply:
            print(json.dumps(apply_verified(ROOT, approved, voice=args.studio_voice), indent=2))
        else:
            print("CHECK ONLY: no import, no final episode claim")
        return 0
    except (OSError, Rejected, ValueError, KeyError) as exc:
        print(f"RETAKE INGESTION BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
