"""Offline tests for the user's updated warm-Melburnian Gemini voice option."""

import argparse
import unittest

from tools import narration_runner
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


if __name__ == "__main__":
    unittest.main()
