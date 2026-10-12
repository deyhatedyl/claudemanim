"""Offline regression tests for Gemini narration cache identity and validation.

Run: python -m unittest discover -s checks -p test_narration_cache.py -v
No API credentials, model calls, or real audio recordings are required.
"""
from __future__ import annotations

import base64
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from types import ModuleType
import unittest
from unittest.mock import Mock, patch
import wave


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools import narration_runner as tts


TRANSCRIPT = "The reaction releases energy."
MODEL = tts.FLASH_MODEL
VOICE_ID = "synthetic-melb-teacher-voice-01"


def synthetic_wav() -> bytes:
    output = io.BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
        audio.writeframes(b"\x00\x00" * 240)
    return output.getvalue()


class NarrationCacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dest = Path(self.tmp.name) / "E01S01.wav"
        self.dest.write_bytes(synthetic_wav())
        self.meta = self.dest.with_suffix(".wav.json")

    def store_metadata(self, **overrides):
        data = {
            "text_sha256": hashlib.sha256(TRANSCRIPT.encode("utf-8")).hexdigest(),
            "model": MODEL,
            "voice_label": tts.VOICE_NAME,
            "voice_fingerprint": tts.voice_fingerprint(VOICE_ID),
            "style_sha256": tts.style_fingerprint(),
        }
        data.update(overrides)
        self.meta.write_text(json.dumps(data), encoding="utf-8")

    def test_missing_metadata_never_matches(self):
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID))

    def test_matching_recording_is_reusable(self):
        self.store_metadata()
        self.assertTrue(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID))

    def test_text_change_invalidates_recording(self):
        self.store_metadata()
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT + " Updated.", MODEL, VOICE_ID))

    def test_model_change_invalidates_recording(self):
        self.store_metadata()
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, tts.LITE_MODEL, VOICE_ID))

    def test_custom_voice_change_invalidates_same_label(self):
        self.store_metadata()
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, MODEL, "another-custom-voice-id"))

    def test_accent_instruction_change_invalidates_cache(self):
        self.store_metadata()
        self.assertTrue(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID, tts.STYLE))
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID, "Different accent"))

    def test_missing_style_fingerprint_is_stale(self):
        self.store_metadata(style_sha256=None)
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID))

    def test_legacy_metadata_without_fingerprint_is_stale(self):
        self.store_metadata()
        data = json.loads(self.meta.read_text(encoding="utf-8"))
        del data["voice_fingerprint"]
        self.meta.write_text(json.dumps(data), encoding="utf-8")
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID))

    def test_malformed_metadata_and_corrupted_wav_are_stale(self):
        self.meta.write_text("{", encoding="utf-8")
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID))
        self.store_metadata()
        self.dest.write_bytes(synthetic_wav()[:-2])
        self.assertFalse(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID))

    def test_saved_metadata_contains_hash_without_voice_id(self):
        self.dest.unlink()
        response = SimpleNamespace(output_audio=SimpleNamespace(
            data=base64.b64encode(synthetic_wav()).decode("ascii")))
        duration = tts.save_response(response, self.dest, TRANSCRIPT, MODEL, tts.VOICE_NAME, VOICE_ID)
        self.assertAlmostEqual(duration, 0.01)
        metadata = json.loads(self.meta.read_text(encoding="utf-8"))
        self.assertEqual(metadata["voice_fingerprint"], tts.voice_fingerprint(VOICE_ID))
        self.assertEqual(metadata["style_sha256"], tts.style_fingerprint())
        self.assertNotIn(VOICE_ID, self.meta.read_text(encoding="utf-8"))
        self.assertTrue(tts.ready(self.dest, TRANSCRIPT, MODEL, VOICE_ID))

    def test_dry_run_detects_model_and_voice_changes_without_api(self):
        self.store_metadata()
        beats = [{"scene": "E01S01", "key": "E01S01.b01", "text": TRANSCRIPT}]

        def run(*options, voice=VOICE_ID):
            stdout = io.StringIO()
            with patch.object(tts, "BEATS", beats), redirect_stdout(stdout):
                code = tts.main(["ep1", "--dry-run", "--output", self.tmp.name,
                                 "--voice-id", voice, *options])
            self.assertEqual(code, 0)
            return stdout.getvalue()

        self.assertIn("1 selected; 0 would be generated", run())
        self.assertIn("1 selected; 1 would be generated", run("--lite"))
        self.assertIn("1 selected; 1 would be generated", run(voice="another-custom-voice-id"))
        self.assertIn("1 selected; 1 would be generated", run("--force"))

    def test_dry_run_with_unavailable_voice_marks_existing_audio_pending(self):
        self.store_metadata()
        beats = [{"scene": "E01S01", "key": "E01S01.b01", "text": TRANSCRIPT}]
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(tts, "BEATS", beats), patch.object(tts, "voice_id", side_effect=ValueError("missing")):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = tts.main(["ep1", "--dry-run", "--output", self.tmp.name])
        self.assertEqual(code, 0)
        self.assertIn("1 selected; 1 would be generated", stdout.getvalue())
        self.assertIn("Custom voice unavailable", stderr.getvalue())

    def test_probe_dry_run_requires_no_beats_or_credentials(self):
        with patch.object(tts, "BEATS", []), patch.dict("os.environ", {}, clear=True):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = tts.main(["--probe", "--dry-run", "--studio-voice", "Sulafat",
                                 "--output", self.tmp.name])
        self.assertEqual(code, 0)
        self.assertIn("1 selected; 1 would be generated", stdout.getvalue())
        self.assertIn("probes", stdout.getvalue())
        self.assertFalse((Path(self.tmp.name) / "probes").exists())

    def test_sdk_error_never_prints_private_provider_text(self):
        secret = "PRIVATE_TRANSCRIPT APIKEY_RANDOM_123"
        error = RuntimeError("upstream failed: " + secret)
        self.assertNotIn(secret, tts.safe_gemini_error(error))
        error.status_code = 401
        self.assertIn("HTTP 401", tts.safe_gemini_error(error))

    def test_native_probe_mocked_end_to_end_creates_one_unique_wav(self):
        response = SimpleNamespace(output_audio=SimpleNamespace(
            data=base64.b64encode(synthetic_wav()).decode("ascii")))
        mock_create = Mock(return_value=response)
        client = SimpleNamespace(interactions=SimpleNamespace(create=mock_create), close=Mock())
        google_module = ModuleType("google")
        google_module.genai = SimpleNamespace(Client=Mock(return_value=client))
        stdout = io.StringIO()
        with patch.dict(sys.modules, {"google": google_module}), \
             patch.dict("os.environ", {"GEMINI_API_KEY": "NONREAL_PLACEHOLDER"}, clear=True), \
             patch.object(tts, "BEATS", []), redirect_stdout(stdout):
            status = tts.main(["--probe", "--studio-voice", "Sulafat",
                               "--output", self.tmp.name, "--interval", "0"])
        self.assertEqual(status, 0)
        mock_create.assert_called_once()
        request = mock_create.call_args.kwargs
        self.assertEqual(request["model"], tts.FLASH_MODEL)
        self.assertEqual(request["generation_config"], {"speech_config": [{"voice": "Sulafat"}]})
        self.assertEqual(request["input"][0]["content"][0]["annotations"][0]["style"], tts.STYLE)
        files = list((Path(self.tmp.name) / "probes").glob("voice_probe_*.wav"))
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].with_suffix(".wav.json").is_file())
        self.assertNotIn("NONREAL_PLACEHOLDER", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
