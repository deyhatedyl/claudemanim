"""Offline checks for safe Gemini stored-voice project diagnostics."""
import io
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import check_gemini_voice_access as check


class Response:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class VoiceAccessTests(unittest.TestCase):
    def test_200_uses_google_api_key_not_openrouter(self):
        with mock.patch.object(check.urllib.request, "urlopen", return_value=Response()) as call:
            status, msg = check.check_access("voice_PRIVATE", "FAKE_GOOGLE_KEY")
        self.assertEqual(status, 200)
        self.assertIn("access", msg)
        request = call.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertTrue(request.full_url.startswith(check.BASE))
        self.assertEqual(request.get_header("X-goog-api-key"), "FAKE_GOOGLE_KEY")
        self.assertNotIn("PRIVATE", msg)
        self.assertNotIn("FAKE_GOOGLE_KEY", msg)

    def test_404_points_to_project_scope(self):
        error = urllib.error.HTTPError(check.BASE, 404, "Not Found", {},
                                      io.BytesIO(b'{"error":"voice_PRIVATE"}'))
        with mock.patch.object(check.urllib.request, "urlopen", side_effect=error):
            status, msg = check.check_access("voice_PRIVATE", "FAKE_GOOGLE_KEY")
        self.assertEqual(status, 404)
        self.assertIn("SAME Google AI Studio project", msg)
        self.assertNotIn("PRIVATE", msg)

    def test_stateless_keys_are_not_looked_up(self):
        with mock.patch.object(check.urllib.request, "urlopen") as call:
            status, msg = check.check_access("voicekey_PRIVATE", "FAKE_GOOGLE_KEY")
        call.assert_not_called()
        self.assertEqual(status, 0)
        self.assertIn("Stateless", msg)


if __name__ == "__main__":
    unittest.main()
