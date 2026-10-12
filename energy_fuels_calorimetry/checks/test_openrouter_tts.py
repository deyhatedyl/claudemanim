"""Offline regression tests: never use or display a real API key."""
from __future__ import annotations

import io
import hashlib
import json
import os
import tempfile
import unittest
from unittest import mock
import urllib.error
from pathlib import Path
import sys
from contextlib import redirect_stdout, redirect_stderr
import wave

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

    def test_nested_provider_metadata_explains_generic_error(self):
        payload = {"error": {
            "message": "Provider returned an error",
            "metadata": {"raw": json.dumps({"error": {
                "message": "Unknown voice: voice_PRIVATENOTFOUND"}})}}}
        reason = tts.safe_provider_reason(json.dumps(payload).encode())
        self.assertIn("Unknown voice", reason)
        self.assertNotIn("PRIVATENOTFOUND", reason)

    def test_freeform_provider_response_never_leaks_unknown_secret(self):
        body = json.dumps({"error": {"message": "Account PRIVATE_RARE_VALUE has insufficient balance"}}).encode()
        reason = tts.safe_provider_reason(body)
        self.assertNotIn("PRIVATE_RARE_VALUE", reason)
        self.assertIn("omitted", reason)

    def test_offline_dry_run_selects_exact_ten_and_probe_without_key(self):
        for options, expected in (([], "E13S15.b01"),
                                  (["--probe"], "One short voice probe")):
            stdout = io.StringIO()
            with mock.patch.dict(os.environ, {}, clear=True), \
                 mock.patch.object(tts.urllib.request, "urlopen") as http, \
                 redirect_stdout(stdout):
                self.assertEqual(tts.main(["--dry-run", *options]), 0)
            http.assert_not_called()
            self.assertIn(expected, stdout.getvalue())

    def test_missing_openrouter_key_never_calls_provider(self):
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {}, clear=True), \
             mock.patch.object(tts.urllib.request, "urlopen") as http, \
             redirect_stderr(stderr):
            self.assertEqual(tts.main(["--probe"]), 2)
        http.assert_not_called()
        self.assertIn("OPENROUTER_API_KEY", stderr.getvalue())

    def test_mocked_probe_uses_selected_preset_and_unique_private_output(self):
        stdout = io.StringIO()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "NONREAL_KEY"}, clear=True), \
             mock.patch.object(tts, "check_authentication") as auth, \
             mock.patch.object(tts, "synthesize", return_value=0.6) as synth, \
             redirect_stdout(stdout):
            self.assertEqual(tts.main(["--probe", "--studio-voice", "Sulafat"]), 0)
        auth.assert_called_once_with("NONREAL_KEY")
        synth.assert_called_once()
        text, voice, api_key, destination = synth.call_args.args
        self.assertIn("calorimetry", text)
        self.assertEqual(voice, "Sulafat")
        self.assertEqual(api_key, "NONREAL_KEY")
        self.assertEqual(destination.parent.name, "probes")
        self.assertTrue(destination.name.startswith("openrouter_voice_probe_"))
        self.assertNotIn("NONREAL_KEY", stdout.getvalue())
        self.assertIn("does not expose", stdout.getvalue())

    def test_mocked_pcm_synthesis_atomic_and_cache_integrity(self):
        class FakeAudio:
            headers = {"Content-Type": "audio/pcm;rate=24000;channels=1"}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return bytes([0, 0]) * 2400

        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "retake.wav"
            with mock.patch.object(tts.urllib.request, "urlopen", return_value=FakeAudio()) as call:
                duration = tts.synthesize("Short test.", "Sulafat", "NONREAL_KEY", output)
            self.assertAlmostEqual(duration, 0.1)
            self.assertTrue(output.is_file())
            with wave.open(str(output), "rb") as wav:
                self.assertEqual(wav.getframerate(), 24000)
                self.assertEqual(wav.getnchannels(), 1)
            request = call.call_args.args[0]
            self.assertEqual(request.get_method(), "POST")
            self.assertEqual(request.full_url, tts.URL)
            payload = json.loads(request.data)
            self.assertEqual(payload, {
                "model": tts.MODEL, "voice": "Sulafat",
                "input": "Short test.", "response_format": "pcm",
            })
            meta = output.with_suffix(".wav.json")
            fields = {
                "text_sha256": hashlib.sha256(b"Short test.").hexdigest(),
                "model": tts.MODEL, "provider": "OpenRouter",
                "voice_fingerprint": hashlib.sha256(b"Sulafat").hexdigest(),
                "audio_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                "duration_seconds": duration,
            }
            meta.write_text(json.dumps(fields))
            self.assertEqual(tts.cached_duration(output, "Short test.", "Sulafat"), duration)
            self.assertIsNone(tts.cached_duration(output, "Another text", "Sulafat"))
            self.assertIsNone(tts.cached_duration(output, "Short test.", "Kore"))
            output.write_bytes(output.read_bytes()[:-4])
            self.assertIsNone(tts.cached_duration(output, "Short test.", "Sulafat"))

    def test_invalid_response_never_overwrites_existing_wav(self):
        class FakeBad:
            headers = {"Content-Type": "application/json"}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return b"PRIVATE" * 1000

        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / "original.wav"
            dest.write_bytes(b"ORIGINAL")
            with mock.patch.object(tts.urllib.request, "urlopen", return_value=FakeBad()):
                with self.assertRaises(ValueError):
                    tts.synthesize("text", "Sulafat", "KEY", dest)
            self.assertEqual(dest.read_bytes(), b"ORIGINAL")


if __name__ == "__main__":
    unittest.main()
