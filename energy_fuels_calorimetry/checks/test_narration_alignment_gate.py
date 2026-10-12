"""Offline narration alignment gate regression tests."""
import unittest

from tools.audit_narration_alignment import beat_errors, words_normalized


class AlignmentGateTests(unittest.TestCase):
    def setUp(self):
        self.text = "Methanol gives twenty two point seven."
        self.clip = {"path": "audio/cache/E13/a.wav", "duration": 3.0}
        self.timeline = {"key": "E13S15.b01", "estimated": False,
                         "audio": "audio/cache/E13/a.wav", "text": self.text,
                         "speech": 3.0, "overrun": 0}
        self.words = [
            {"word": word, "start": i*0.3, "end": i*0.3+0.2}
            for i, word in enumerate(self.text.split())
        ]

    def test_normalized_words(self):
        self.assertEqual(words_normalized("CO₂ is 1,370."), ["co₂", "is", "1370"])

    def test_matching_recording_and_words_pass(self):
        self.assertEqual(beat_errors("E13S15.b01", self.text, self.clip,
                                     self.words, self.timeline), [])

    def test_estimated_duration_never_passes(self):
        self.timeline["estimated"] = True
        self.assertIn("uses estimated", " ".join(beat_errors(
            "E13S15.b01", self.text, self.clip, self.words, self.timeline)))

    def test_changed_narration_requires_new_alignment(self):
        self.assertIn("differs", " ".join(beat_errors(
            "E13S15.b01", self.text+" Updated.", self.clip, self.words, self.timeline)))

    def test_missing_audio_is_rejected(self):
        self.assertIn("missing verified audio", " ".join(beat_errors(
            "E13S15.b01", self.text, None, self.words, self.timeline)))

    def test_out_of_bounds_word_time_rejected(self):
        self.words[-1]["end"] = 4.0
        self.assertIn("timestamps", " ".join(beat_errors(
            "E13S15.b01", self.text, self.clip, self.words, self.timeline)))

    def test_animation_overrun_rejected(self):
        self.timeline["overrun"] = 0.24
        self.assertIn("animation runs past", " ".join(beat_errors(
            "E13S15.b01", self.text, self.clip, self.words, self.timeline)))


if __name__ == "__main__":
    unittest.main()
