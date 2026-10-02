# Known issues and blockers

| Date | Item | Status |
|---|---|---|
| 2026-10-02 | **TTS blocked**: no `GEMINI_API_KEY` in the session environment. Gemini endpoint is reachable (HTTP 403 "unregistered caller" without a key). The env var must be added in the cloud environment settings and a new session started. Until then no narration clips exist, drafts are silent with estimated timing, and no episode can be called complete. | open |
| 2026-10-02 | Gemini TTS request shape for `gemini-3.8-flash-tts` not confirmed against live docs (ai.google.dev blocked by egress policy). `shared/tts.py` tries `voiceConfig.voice` and falls back to `voiceConfig.prebuiltVoiceConfig.voiceName`; `tools/tts_probe.py` records which one the API accepts. | open (verify with key) |
| 2026-10-02 | Source files (study design docx, 2024/2025/2026 exams and reports) were not supplied to this session; coverage follows the brief's self-contained objectives and has not been reconciled against them. | open (user offered to upload) |
| 2026-10-02 | Parallel renders raced on Manim's shared TeX cache ("latex failed but did not produce a log file"). Fixed: per-scene `tex_dir`. | fixed |
| 2026-10-02 | Draft layout defects in E01 (text past right edge in S01/S02/S03, overlaps in S04/S05/S06/S08). Fixed; an automatic per-beat layout check now flags off-frame/caption-strip objects. | fixed |
| 2026-10-02 | Storage plan for cached narration (~4 h of 24 kHz WAV ≈ 0.7 GB) and final MP4s in git is undecided (GitHub 100 MB file limit). Options: FLAC cache, Git LFS, or release assets. | open |
| 2026-10-02 | **Runtime**: the 14 silent drafts first totalled 191.9 min (3 h 12 min), below the brief's 3 h 15 min to 4 h 15 min. E09, E10, E11 and E12 were expanded with nine new teaching scenes; the drafts now total 203.5 min (3 h 24 min) at 145 words per minute including scripted pauses. E06 (11.5 min vs 12–16) and E08 (12.5 min vs 14–18) remain slightly under their own targets. Real narration pace will change every runtime. | in range (series) |
| 2026-10-02 | Coverage item **C26** carries no `coverage=` tag in any script (see `coverage_matrix.md`). It must be checked against the brief: either it is taught under another tag or it needs a scene. | open |
| 2026-10-02 | Reading `brief/production_brief.md` was refused by this session's permission classifier while E13/E14 were written, so the workshops follow the brief as recorded in the session notes and `coverage_matrix.md` lists item IDs without restating their wording. Re-check E13/E14 and C26 against the brief in a session that can read it. | open |
| 2026-10-02 | Question cards showed `ΔH_c` literally on screen (E07 Q13, E08 Q15). Fixed: text containing `ΔH_c` is drawn with a true subscript; affected scenes re-rendered. | fixed |
