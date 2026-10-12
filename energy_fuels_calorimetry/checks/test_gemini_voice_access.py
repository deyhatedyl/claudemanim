"""Offline checks of Google's documented GetVoice and native TTS contracts."""
import io
import os
import sys
import unittest
import urllib.error
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import check_gemini_voice_access as check
from tools import narration_runner


class Response:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class VoiceAccessTests(unittest.TestCase):
    def test_get_voice_uses_official_path_and_google_header(self):
        with mock.patch.object(check.urllib.request, "urlopen", return_value=Response()) as call:
            status, msg = check.check_access("voice_PRIVATE", "FAKE_GOOGLE_KEY")
        self.assertEqual(status, 200)
        self.assertIn("retrieved", msg)
        self.assertIn("does not test Gemini TTS synthesis", msg)
        request = call.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.full_url,
                         "https://generativelanguage.googleapis.com/v1beta/voices/voice_PRIVATE")
        self.assertEqual(request.get_header("X-goog-api-key"), "FAKE_GOOGLE_KEY")
        self.assertNotIn("OPENROUTER", str(request.headers).upper())
        self.assertNotIn("PRIVATE", msg)
        self.assertNotIn("FAKE_GOOGLE_KEY", msg)

    def test_404_is_not_treated_as_proof_of_wrong_project(self):
        error = urllib.error.HTTPError(check.BASE, 404, "Not Found", {},
                                      io.BytesIO(b'{"error":"voice_PRIVATE"}'))
        with mock.patch.object(check.urllib.request, "urlopen", side_effect=error):
            status, msg = check.check_access("voice_PRIVATE", "FAKE_GOOGLE_KEY")
        self.assertEqual(status, 404)
        self.assertIn("original Google AI Studio", msg)
        self.assertIn("does not establish", msg)
        self.assertNotIn("PRIVATE", msg)
        self.assertNotIn("FAKE_GOOGLE_KEY", msg)

    def test_http_errors_are_safely_classified(self):
        cases = {400: "voice ID format", 401: "authentication failed",
                 403: "denied access", 429: "rate-limited", 503: "HTTP 503"}
        for code, phrase in cases.items():
            with self.subTest(code=code):
                error = urllib.error.HTTPError(
                    check.BASE, code, "secret voice_PRIVATE FAKE_GOOGLE_KEY",
                    {}, io.BytesIO(b'voice_PRIVATE FAKE_GOOGLE_KEY'))
                with mock.patch.object(check.urllib.request, "urlopen", side_effect=error):
                    status, msg = check.check_access("voice_PRIVATE", "FAKE_GOOGLE_KEY")
                self.assertEqual(status, code)
                self.assertIn(phrase, msg)
                self.assertNotIn("PRIVATE", msg)
                self.assertNotIn("FAKE_GOOGLE_KEY", msg)

    def test_stateless_keys_are_not_looked_up(self):
        with mock.patch.object(check.urllib.request, "urlopen") as call:
            status, msg = check.check_access("voicekey_PRIVATE", "FAKE_GOOGLE_KEY")
        call.assert_not_called()
        self.assertEqual(status, 0)
        self.assertIn("Stateless", msg)

    def test_other_voice_names_do_not_trigger_stored_voice_lookup(self):
        with mock.patch.object(check.urllib.request, "urlopen") as call:
            status, msg = check.check_access("Kore", "FAKE_GOOGLE_KEY")
        self.assertEqual(status, 0)
        call.assert_not_called()
        self.assertNotIn("FAKE_GOOGLE_KEY", msg)

    def test_network_errors_are_safe(self):
        for error in (urllib.error.URLError("voice_PRIVATE FAKE_GOOGLE_KEY"),
                      TimeoutError("voice_PRIVATE FAKE_GOOGLE_KEY")):
            with self.subTest(type=type(error).__name__):
                with mock.patch.object(check.urllib.request, "urlopen", side_effect=error):
                    status, msg = check.check_access("voice_PRIVATE", "FAKE_GOOGLE_KEY")
                self.assertEqual(status, 0)
                self.assertNotIn("PRIVATE", msg)
                self.assertNotIn("FAKE_GOOGLE_KEY", msg)

    def test_missing_credentials_fail_before_any_lookup(self):
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            mock.patch.object(check.urllib.request, "urlopen") as request,
            mock.patch.object(check, "voice_id") as lookup,
        ):
            with mock.patch.object(sys, "argv", ["check_gemini_voice_access.py"]):
                self.assertEqual(check.main(), 2)
        request.assert_not_called()
        lookup.assert_not_called()

    def test_native_tts_runner_matches_gemini_38_documentation(self):
        client = SimpleNamespace(interactions=SimpleNamespace(create=mock.Mock()))
        narration_runner.request_audio(
            client, narration_runner.FLASH_MODEL, "Verbatim transcript", "voice_FAKE")
        kwargs = client.interactions.create.call_args.kwargs
        self.assertEqual(kwargs["model"], "gemini-3.8-flash-tts")
        self.assertEqual(kwargs["input"], [{
            "type": "user_input", "content": [{
                "type": "text", "text": "Verbatim transcript",
                "annotations": [{"type": "speech_metadata",
                                 "style": narration_runner.STYLE}],
            }],
        }])
        self.assertEqual(kwargs["response_format"], {"type": "audio"})
        self.assertEqual(kwargs["generation_config"],
                         {"speech_config": [{"voice": "voice_FAKE"}]})
        self.assertEqual(narration_runner.LITE_MODEL, "gemini-3.8-flash-lite-tts")


if __name__ == "__main__":
    unittest.main()
