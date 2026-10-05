"""Offline regression checks: exact transcripts, selection, resumability and audio ZIPs."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import wave
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode


def pcm_wav():
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
        w.writeframes(b"\0\0" * 240)
    return out.getvalue()


def verify(pack):
    counts = dict(scenes=0, beats=0)
    for num in range(4, 15):
        ep = f"E{num:02d}"
        path = pack / f"narration_{ep.lower()}.py"
        spec = importlib.util.spec_from_file_location(ep, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        script = load_episode(ep)
        expected = [(s.id, "\n\n".join(b.text for b in s.beats)) for s in script.scenes]
        assert module.selected_jobs(ep, False) == expected, f"{ep}: transcript drift"
        assert module.DEFAULT_PREFIX == ep
        assert module.selected_jobs(f"ep{num}", False) == expected
        assert module.selected_jobs(str(num), False) == expected
        assert len(module.selected_jobs(script.scenes[0].id + ".b01", True)) == 1
        assert module.selected_jobs("E01", False) == []
        assert module.normalized_prefix("ep10") == "E10"
        assert module.normalized_prefix("14") == "E14"
        assert module.normalized_prefix("1") == "E01"
        dry = subprocess.run([sys.executable, str(path), "--dry-run", "--lite"],
                             capture_output=True, text=True)
        assert dry.returncode == 0, dry.stderr
        assert f"{len(expected)} selected" in dry.stdout
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            sid, text = expected[0]
            wav = out / f"{sid}.wav"
            wav.write_bytes(pcm_wav())
            assert module.ready(wav, text), "Valid existing WAV must resume"
            meta = wav.with_suffix(".wav.json")
            meta.write_text(json.dumps({"text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                                       "model": "other-model"}))
            assert module.ready(wav, text), "Switching models must retain completed speech"
            assert not module.ready(wav, text + " changed"), "Changed transcript must regenerate"
            wav.write_bytes(pcm_wav()[:-2])
            assert not module.ready(wav, text), "Truncated audio must not count as complete"
            # No API: synthetic clips only exercise packaging, never become deliverables.
            for sid, text in expected:
                wav = out / f"{sid}.wav"
                wav.write_bytes(pcm_wav())
                wav.with_suffix(".wav.json").write_text(json.dumps({
                    "text_sha256": hashlib.sha256(text.encode()).hexdigest()}))
            stage = out / "pack"
            stage.mkdir()
            for name in (f"narration_{ep.lower()}.py", "zip_audio.py", "scene-manifest.json"):
                (stage / name).write_bytes((pack / name).read_bytes())
            zipped = subprocess.run([sys.executable, str(stage / "zip_audio.py"), ep,
                                     "--input", str(out)], capture_output=True, text=True)
            assert zipped.returncode == 0, zipped.stderr
            with zipfile.ZipFile(stage / "audio" / f"{ep}-audio.zip") as z:
                assert sum(n.endswith(".wav") for n in z.namelist()) == len(expected)
                assert all(n.startswith(ep + "S") for n in z.namelist())
            (out / f"{expected[-1][0]}.wav").unlink()
            missing = subprocess.run([sys.executable, str(stage / "zip_audio.py"), ep,
                                      "--input", str(out)], capture_output=True, text=True)
            assert missing.returncode != 0, "Incomplete episodes must not be packaged"
        counts["scenes"] += len(expected)
        counts["beats"] += len(module.BEATS)
        print(f"{ep}: {len(expected)} scenes, {len(module.BEATS)} beats; offline checks passed")
    print(json.dumps(counts))


if __name__ == "__main__":
    verify(ROOT / "delivery/Narration-E04-E14")
