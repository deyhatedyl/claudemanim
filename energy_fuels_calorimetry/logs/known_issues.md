# Known issues and blockers

| Date | Item | Status |
|---|---|---|
| 2026-10-02 | **TTS blocked**: no `GEMINI_API_KEY` in the session environment. Gemini endpoint is reachable (HTTP 403 "unregistered caller" without a key). The env var must be added in the cloud environment settings and a new session started. Until then no narration clips exist, drafts are silent with estimated timing, and no episode can be called complete. | open |
| 2026-10-02 | Gemini TTS request shape for `gemini-3.8-flash-tts` not confirmed against live docs (ai.google.dev blocked by egress policy). `shared/tts.py` tries `voiceConfig.voice` and falls back to `voiceConfig.prebuiltVoiceConfig.voiceName`; `tools/tts_probe.py` records which one the API accepts. | open (verify with key) |
| 2026-10-02 | Source files (study design docx, 2024/2025/2026 exams and reports) were not supplied to this session; coverage follows the brief's self-contained objectives and has not been reconciled against them. | open (user offered to upload) |
| 2026-10-02 | Parallel renders raced on Manim's shared TeX cache ("latex failed but did not produce a log file"). Fixed: per-scene `tex_dir`. | fixed |
| 2026-10-02 | Draft layout defects in E01 (text past right edge in S01/S02/S03, overlaps in S04/S05/S06/S08). Fixed; an automatic per-beat layout check now flags off-frame/caption-strip objects. | fixed |
| 2026-10-02 | Storage plan for cached narration (~4 h of 24 kHz WAV ≈ 0.7 GB) and final MP4s in git is undecided (GitHub 100 MB file limit). Options: FLAC cache, Git LFS, or release assets. | open |
