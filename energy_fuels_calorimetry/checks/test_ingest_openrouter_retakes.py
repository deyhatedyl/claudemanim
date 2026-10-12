"""Offline fail-closed retake ingestion tests; all audio and sidecars are synthetic."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import wave

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C
from shared.tts import cached_clip, manual_text_hash
from tools import ingest_openrouter_retakes as imp


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.directory = self.root / "audio" / "gemini_retakes"
        self.directory.mkdir(parents=True)
        self.beats = imp.expected_beats()
        self.assertEqual(len(self.beats), 10)
        self.assertIn("E13S15.b01", self.beats)
        for key, text in self.beats.items():
            wav = self.directory / f"{key}.wav"
            with wave.open(str(wav), "wb") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(24000)
                f.writeframes(b"\x01\x00" * 24000)
            meta = {
                "provider": "OpenRouter",
                "model": imp.MODEL,
                "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "voice_label": "Gemini studio voice: Sulafat",
                "voice_source": "Gemini studio voice: Sulafat",
                "voice_fingerprint": hashlib.sha256(b"Sulafat").hexdigest(),
                "audio_sha256": hashlib.sha256(wav.read_bytes()).hexdigest(),
                "duration_seconds": 1.0,
            }
            wav.with_suffix(".wav.json").write_text(json.dumps(meta))
        self.manifest_path = self.root / "audio" / "manifest.json"
        self.manifest_path.write_text(json.dumps({
            "E07S01.b01": {"source": "manual", "text_hash": "original-retained",
                            "path": "audio/cache/E07/unchanged.wav", "duration": 2.0}
        }))
        ep7 = self.root / "audio" / "aligned" / "E07"
        ep7.mkdir(parents=True)
        (ep7 / "words.json").write_text(json.dumps({"E07S01.b01": [{"word": "Unchanged"}]}))
        (ep7 / "segments.json").write_text(json.dumps({"E07S01.b01": {"file": "original.wav"}}))

    def metadata(self, key):
        return self.directory / f"{key}.wav.json"

    def change_meta(self, key, **change):
        path = self.metadata(key)
        obj = json.loads(path.read_text())
        obj.update(change)
        path.write_text(json.dumps(obj))

    def fake_aligner(self, approved):
        out = {}
        for key, item in approved.items():
            tokens = item["text"].split()
            step = .9 / len(tokens)
            words = [{"word": word, "start": i * step, "end": (i + 1) * step,
                      "score": .99} for i, word in enumerate(tokens)]
            out[key] = (words, {"scene": key.split(".")[0],
                                "greedy_transcription_similarity": .99,
                                "method": "mocked CTC in unit test"})
        return out

    def test_all_ten_preflight_and_atomic_import_preserve_original(self):
        approved, before = imp.preflight(self.root, self.directory, "Sulafat")
        self.assertEqual(len(approved), 10)
        status = imp.apply_verified(self.root, approved, voice="Sulafat",
                                    aligner=self.fake_aligner)
        self.assertEqual(status["imported"], 10)
        after = json.loads(self.manifest_path.read_text())
        self.assertEqual(after["E07S01.b01"], before["E07S01.b01"])
        for key, text in self.beats.items():
            self.assertEqual(after[key]["source"], imp.SOURCE)
            self.assertEqual(after[key]["text_hash"], manual_text_hash(text))
            self.assertEqual(
                (self.root / after[key]["path"]).read_bytes(),
                (self.directory / (key + ".wav")).read_bytes())
            with mock.patch.object(C, "ROOT", self.root):
                self.assertIsNotNone(cached_clip(key, text, after))
                self.assertIsNone(cached_clip(key, text + " changed", after))
            ep = key[:3]
            words = json.loads((self.root / "audio" / "aligned" / ep / "words.json").read_text())
            self.assertEqual(" ".join(row["word"] for row in words[key]), text)
        # A post-import cache-file modification must invalidate playback.
        key = "E13S15.b01"
        dest = self.root / after[key]["path"]
        contents = dest.read_bytes()
        dest.write_bytes(contents[:-4] + b"XXXX")
        with mock.patch.object(C, "ROOT", self.root):
            self.assertIsNone(cached_clip(key, self.beats[key], after))
        dest.write_bytes(contents)
        original_words = json.loads(
            (self.root / "audio" / "aligned" / "E07" / "words.json").read_text())
        self.assertEqual(original_words["E07S01.b01"], [{"word": "Unchanged"}])
        # Re-importing an identical, reviewed set is safe/idempotent.
        checked, _ = imp.preflight(self.root, self.directory, "Sulafat")
        self.assertEqual(imp.apply_verified(self.root, checked, voice="Sulafat",
                                             aligner=self.fake_aligner)["imported"], 10)

    def test_missing_one_and_missing_all_fail_without_mutation(self):
        key = "E13S15.b01"
        self.metadata(key).unlink()
        before = self.manifest_path.read_bytes()
        with self.assertRaisesRegex(imp.Rejected, "E13S15.b01: missing"):
            imp.preflight(self.root, self.directory, "Sulafat")
        self.assertEqual(self.manifest_path.read_bytes(), before)
        for wav in self.directory.glob("*.wav"):
            wav.unlink()
        with self.assertRaisesRegex(imp.Rejected, "0/10 verified"):
            imp.preflight(self.root, self.directory, "Sulafat")

    def test_wrong_provenance_voice_model_script_hash_and_audio_hash(self):
        key = "E13S15.b01"
        for changed in (
            {"provider": "Google"},
            {"model": "unknown-model"},
            {"voice_fingerprint": hashlib.sha256(b"wrong").hexdigest()},
            {"voice_label": "uncertified"},
            {"voice_source": "uncertified"},
            {"text_sha256": hashlib.sha256(b"stale narration").hexdigest()},
            {"audio_sha256": hashlib.sha256(b"other audio").hexdigest()},
            {"duration_seconds": 9.0},
        ):
            original = self.metadata(key).read_bytes()
            try:
                self.change_meta(key, **changed)
                with self.assertRaises(imp.Rejected):
                    imp.preflight(self.root, self.directory, "Sulafat")
            finally:
                self.metadata(key).write_bytes(original)

    def test_stale_manual_cache_and_original_aligned_words_fail(self):
        key = "E08S06.b06"
        text = self.beats[key]
        legacy = json.loads(self.manifest_path.read_text())
        legacy[key] = {"source": "manual", "text_hash": manual_text_hash(text),
                       "path": "audio/cache/E08/original.wav", "duration": 1.0}
        self.manifest_path.write_text(json.dumps(legacy))
        with self.assertRaisesRegex(imp.Rejected, "stale/non-Gemini manifest"):
            imp.preflight(self.root, self.directory, "Sulafat")
        (self.root / "audio" / "cache" / "E08").mkdir(parents=True)
        (self.root / "audio" / "cache" / "E08" / "original.wav").write_bytes(
            (self.directory / (key + ".wav")).read_bytes())
        with mock.patch.object(C, "ROOT", self.root):
            self.assertIsNone(cached_clip(key, text, legacy))
            # This ban covers all ten audited keys, not just E08.
            for audited_key, authored in self.beats.items():
                stale = {audited_key: {
                    "source": "manual", "text_hash": manual_text_hash(authored),
                    "path": "audio/cache/E08/original.wav", "duration": 1.0,
                }}
                self.assertIsNone(cached_clip(audited_key, authored, stale))
        legacy.pop(key)
        self.manifest_path.write_text(json.dumps(legacy))
        folder = self.root / "audio" / "aligned" / "E08"
        folder.mkdir(parents=True)
        (folder / "words.json").write_text(json.dumps({key: [{"word": "old"}]}))
        with self.assertRaisesRegex(imp.Rejected, "stale original active"):
            imp.preflight(self.root, self.directory, "Sulafat")

    def test_refuse_incomplete_or_failed_word_alignment_without_changes(self):
        approved, _ = imp.preflight(self.root, self.directory, "Sulafat")
        before = self.manifest_path.read_bytes()
        with self.assertRaisesRegex(imp.Rejected, "incomplete/extra"):
            imp.apply_verified(self.root, approved, voice="Sulafat",
                               aligner=lambda _: {})
        def broken(approved):
            result = self.fake_aligner(approved)
            key = "E13S15.b01"
            result[key][0][0]["word"] = "wrong"
            return result
        with self.assertRaisesRegex(imp.Rejected, "transcript differs"):
            imp.apply_verified(self.root, approved, voice="Sulafat", aligner=broken)
        self.assertEqual(self.manifest_path.read_bytes(), before)
        self.assertFalse((self.root / "audio" / "cache").exists())

    def test_rollback_on_failed_install(self):
        original = self.root / "audio" / "existing.json"
        additional = self.root / "audio" / "new.json"
        original.write_bytes(b"ORIGINAL")
        real_replace = imp.os.replace
        count = 0

        def fail_second(src, dest):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("simulated disk failure")
            return real_replace(src, dest)

        with mock.patch.object(imp.os, "replace", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "simulated disk failure"):
                imp.install_payloads(
                    {original: b"CHANGED", additional: b"NEW"}, self.root / "audio")
        self.assertEqual(original.read_bytes(), b"ORIGINAL")
        self.assertFalse(additional.exists())

    def test_unexpected_wav_rejected(self):
        (self.directory / "UNEXPECTED.wav").write_bytes(b"junk")
        with self.assertRaisesRegex(imp.Rejected, "Unexpected WAV"):
            imp.preflight(self.root, self.directory, "Sulafat")


if __name__ == "__main__":
    unittest.main()
