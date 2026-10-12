"""Offline regression tests: never use or display a real API key."""
from __future__ import annotations

import io
import json
import unittest
from unittest import mock
import urllib.error
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools import openrouter_gemini_retakes as tts


class DummyResponse:
    status = 200
    def __enter__(self): return self
    def __exit__(self, *args): return False


class AuthTests(unittest.TestCase):
    def test_preflight_is_get_and_does_not_echo_key(self):
        with mock.patch.object(tts.urllib.request, "urlopen", return_value=DummyResponse()) as mocked:
            tts.check_authentication("NONREAL_PLACEHOLDER")
        request = mocked.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.full_url, "https://openrouter.ai/api/v1/key")

    def test_401_is_authentication_not_voice(self):
        err = urllib.error.HTTPError(tts.KEY_URL, 401, "Unauthorized", {}, io.BytesIO(
            b'{"error":{"message":"User not found."},"credential":"PRIVATE_SECRET"}'))
        with mock.patch.object(tts.urllib.request, "urlopen", side_effect=err):
            with self.assertRaisesRegex(RuntimeError, r"HTTP 401"):
                tts.check_authentication("PRIVATE_SECRET")
        self.assertNotIn("PRIVATE_SECRET", tts.explain_speech_error(401))
        self.assertIn("authentication", tts.explain_speech_error(401).lower())

    def test_400_is_validation_after_authentication(self):
        self.assertIn("voice", tts.explain_speech_error(400))
        self.assertIn("402", tts.explain_speech_error(402))
        self.assertIn("429", tts.explain_speech_error(429))

    def test_model_endpoint_and_format(self):
        self.assertEqual(tts.URL, "https://openrouter.ai/api/v1/audio/speech")
        self.assertEqual(tts.MODEL, "google/gemini-3.8-flash-tts")

    def test_provider_error_explanation_is_redacted(self):
        voice = "voice_PRIVATECUSTOMIDENTIFIER123"
        spoken = "secret narration words should not be copied back"
        body = json.dumps({"error": {
            "message": f"Voice {voice} not found; received {spoken}; "
                       "bearer sk-or-v1-PRIVATEKEY9876"}}).encode()
        result = tts.diagnose_speech_error(
            400, body, voice=voice, input_text=spoken)
        self.assertIn("HTTP 400", result)
        self.assertIn("not found", result)
        self.assertNotIn(voice, result)
        self.assertNotIn(spoken, result)
        self.assertNotIn("PRIVATEKEY", result)

    def test_unreadable_provider_error_does_not_echo_body(self):
        private = b"Not JSON: secret_account_number_123"
        result = tts.safe_provider_reason(private)
        self.assertNotIn("secret_account_number", result)

    def test_http_400_carries_sanitized_reason(self):
        voice = "voice_PRIVATEVOICE"
        err = urllib.error.HTTPError(tts.URL, 400, "Bad Request", {},
                                     io.BytesIO(json.dumps({
                                         "error": {"message": f"Voice {voice} is not available"}
                                     }).encode()))
        with mock.patch.object(tts.urllib.request, "urlopen", side_effect=err):
            with self.assertRaises(RuntimeError) as caught:
                tts.synthesize("test text", voice, "PLACEHOLDER_KEY", Path("/never-created.wav"))
        self.assertIn("not available", str(caught.exception))
        self.assertNotIn(voice, str(caught.exception))
        self.assertNotIn("PLACEHOLDER_KEY", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
