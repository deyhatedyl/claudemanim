"""Hash and transcript guards for user-uploaded MP3 corrections, offline."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import wave

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C
from shared.tts import cached_clip, manual_text_hash
from tools.ingest_supplied_retakes import Rejected, ingest, reviewed_alignment


class SuppliedRetakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.key = "E06S04.b04"
        self.text = "The products need assumptions."
        data = io.BytesIO()
        with wave.open(data, "wb") as w:
            w.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
            w.writeframes(b"\0\0" * 24000)
        self.wav = self.root / "clip.wav"
        self.wav.write_bytes(data.getvalue())
        self.mp3 = self.root / "input.mp3"
        self.mp3.write_bytes(b"uploaded input fixture")
        self.meta = self.root / "receipt.json"
        self.receipt = {
            "source": "user_supplied_retake", "key": self.key, "input_path": "input.mp3",
            "input_sha256": hashlib.sha256(self.mp3.read_bytes()).hexdigest(),
            "audio_sha256": hashlib.sha256(self.wav.read_bytes()).hexdigest(),
            "text_hash": manual_text_hash(self.text), "duration": 1.0,
            "alignment": {"greedy_transcription_similarity": .99},
            "words": [{"word": x} for x in self.text.split()],
        }
        self.meta.write_text(json.dumps(self.receipt))
        self.entry = {**self.receipt, "path": "clip.wav", "metadata_path": "receipt.json"}

    def cached(self, text=None):
        with patch.object(C, "ROOT", self.root):
            return cached_clip(self.key, text or self.text, {self.key: self.entry})

    def test_reviewed_supplied_clip_is_admitted_without_fabricated_provider(self):
        self.assertIsNotNone(self.cached())
        self.assertNotIn("provider", self.receipt)

    def test_changed_input_and_changed_decode_are_rejected(self):
        self.mp3.write_bytes(b"different input")
        self.assertIsNone(self.cached())
        self.mp3.write_bytes(b"uploaded input fixture")
        self.wav.write_bytes(b"changed decode")
        self.assertIsNone(self.cached())

    def test_changed_script_or_missing_review_is_rejected(self):
        self.assertIsNone(self.cached(self.text + " Extra words."))
        self.meta.unlink()
        self.assertIsNone(self.cached())

    def test_incomplete_batch_is_rejected_before_any_audio_change(self):
        with patch("tools.ingest_supplied_retakes.ROOT", self.root):
            with self.assertRaises(Rejected):
                ingest(self.root)
        self.assertFalse((self.root / "audio").exists())


if __name__ == "__main__":
    unittest.main()
