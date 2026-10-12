"""Offline tests for the user's updated warm-Melburnian Gemini voice option."""

import argparse
import base64
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
import wave
from zipfile import ZipFile

from tools import narration_runner
from tools import gemini_audit_retakes as retakes
from tools.gemini_audit_retakes import prepare


class MelbourneVoiceTests(unittest.TestCase):
    def test_prebuilt_voice_needs_no_custom_voice_file(self):
        args = argparse.Namespace(studio_voice="Sulafat", voice_id=None, voice_file=None, lite=False)
        voice, source = narration_runner.voice_id(args)
        self.assertEqual(voice, "Sulafat")
        self.assertIn("studio", source)

    def test_studio_voice_cannot_be_mixed_with_old_custom_voice(self):
        args = argparse.Namespace(studio_voice="Sulafat", voice_id="voice_placeholder", voice_file=None, lite=False)
        with self.assertRaises(ValueError):
            narration_runner.voice_id(args)

    def test_melbourne_style_is_explicit(self):
        style = narration_runner.STYLE.lower()
        self.assertIn("melbourne", style)
        self.assertIn("australian accent", style)
        self.assertIn("chemistry teacher", style)

    def test_exactly_ten_reviewed_retakes(self):
        beats = prepare()
        self.assertEqual(len(beats), 10)
        self.assertEqual(len({b["key"] for b in beats}), 10)
        self.assertIn("E13S15.b01", {b["key"] for b in beats})

    def test_ten_retakes_package_offline_and_refuse_missing_audio(self):
        beats = prepare()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with self.assertRaisesRegex(ValueError, "E06S04"):
                retakes.package_verified(beats, output, narration_runner.FLASH_MODEL, "Sulafat")

            raw = io.BytesIO()
            with wave.open(raw, "wb") as w:
                w.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
                w.writeframes(bytes([0, 0]) * 2400)
            response = SimpleNamespace(output_audio=SimpleNamespace(
                data=base64.b64encode(raw.getvalue()).decode("ascii")))
            for beat in beats:
                dest = output / (beat["key"] + ".wav")
                narration_runner.save_response(
                    response, dest, beat["text"],
                    narration_runner.FLASH_MODEL, "Gemini studio voice: Sulafat", "Sulafat")
            archive = retakes.package_verified(
                beats, output, narration_runner.FLASH_MODEL, "Sulafat")
            self.assertTrue(archive.is_file())
            self.assertTrue((output / "segments.json").is_file())
            with ZipFile(archive) as bundle:
                files = bundle.namelist()
                self.assertEqual(len(files), 21)
                self.assertEqual(len([name for name in files if name.endswith(".wav")]), 10)
                portable = json.loads(bundle.read("segments.json"))
                self.assertEqual(len(portable), 10)
                self.assertIn("E13S15.b01", portable)
                self.assertEqual(portable["E13S15.b01"]["file"], "E13S15.b01.wav")
            # Switching delivery voice must NOT silently package old audio.
            with self.assertRaisesRegex(ValueError, "E06S04"):
                retakes.package_verified(
                    beats, output, narration_runner.FLASH_MODEL, "Kore")

    def test_native_retakes_dry_probe_does_not_use_api_or_create_audio(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(
                    retakes.main(["--probe", "--dry-run", "--studio-voice", "Sulafat"]), 0)
            self.assertIn("1 selected; 1 would be generated", stdout.getvalue())
            self.assertIn("probes", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
