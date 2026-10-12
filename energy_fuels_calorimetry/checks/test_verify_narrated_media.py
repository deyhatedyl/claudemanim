"""Offline structural checks for narrated Chemistry MP4 acceptance."""
import unittest

from tools.verify_narrated_media import inspect_metadata


def base_probe():
    return {"format": {"duration": "770.833333"},
            "streams": [
                {"codec_type": "video", "codec_name": "h264", "width": 1920,
                 "height": 1080, "r_frame_rate": "30/1", "avg_frame_rate": "30/1"},
                {"codec_type": "audio", "codec_name": "aac", "duration": "770.8"},
            ]}


def base_report():
    return {"final": True, "narrated": True, "beats": 42, "beats_with_audio": 42,
            "duration": 770.83, "problems": []}


class MediaAcceptanceTests(unittest.TestCase):
    def test_valid_full_length_narrated_episode(self):
        record = inspect_metadata(base_probe(), base_report())
        self.assertEqual(record["beat_coverage"], 42)
        self.assertEqual(record["subtitle_streams"], 0)

    def test_rejects_silent_preview(self):
        p = base_probe()
        p["streams"] = p["streams"][:1]
        with self.assertRaisesRegex(ValueError, "exactly one"):
            inspect_metadata(p)

    def test_rejects_embedded_subtitles(self):
        p = base_probe()
        p["streams"].append({"codec_type": "subtitle", "codec_name": "mov_text"})
        with self.assertRaisesRegex(ValueError, "zero subtitle"):
            inspect_metadata(p)

    def test_rejects_partial_narration(self):
        r = base_report()
        r["beats_with_audio"] = 41
        with self.assertRaisesRegex(ValueError, "Missing recorded"):
            inspect_metadata(base_probe(), r)

    def test_rejects_audio_duration_gap(self):
        p = base_probe()
        p["streams"][1]["duration"] = "760.0"
        with self.assertRaisesRegex(ValueError, "cover"):
            inspect_metadata(p, base_report())

    def test_rejects_video_duration_drift(self):
        r = base_report()
        r["duration"] = 772.0
        with self.assertRaisesRegex(ValueError, "diverge"):
            inspect_metadata(base_probe(), r)


if __name__ == "__main__":
    unittest.main()
