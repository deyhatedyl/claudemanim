# Resuming the chemistry series

1. Read `checks/ui_review_20261005.json`, `checks/preview_validation_20261005.json`,
   `checks/qa_status.json`, `logs/known_issues.md` and `brief/production_brief.md`.
   The active branch is `codex/episode-01-narration`. E01–E03 were delivered earlier;
   the learner explicitly asked to keep Episode 3 as delivered.
2. E04–E14 have reference-style visual previews, richer diagrams/animation and original
   practice questions. Graph stimuli are shown during the attempt, before solution fits
   and annotations. Future MP4s have no burned-in captions or subtitle tracks.
   Preview timing is estimated; narrated final QA remains pending learner audio.
3. Build or reuse the narration pack:
   ```bash
   python tools/build_narration_pack.py E04 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14
   python checks/verify_narration_pack.py
   ```
   It contains `narration_e04.py` through `narration_e14.py`, exact scene text, voice direction,
   all Terminal commands and `zip_audio.py`. Preserve the learner's working Gemini request
   format and Melb Teacher F1 voice. The learner runs TTS locally and returns scene WAV ZIPs.
   Keep the exact spoken words; thinking pauses are added by the video renderer.
4. After each audio ZIP arrives, validate every scene WAV and transcript hash. Put recordings
   in `audio/manual`, align the exact speech locally, review the boundaries and recognition
   report, then import measured beat segments. Estimated preview timestamps are not speech
   boundaries. See the alignment commands in README.md. Keep audio and alignment private.
5. Re-render at measured durations, assemble and export:
   ```bash
   EXPORT_BEAT_STILLS=1 python tools/render.py E04 -q h --jobs 2 --no-assemble
   python tools/layout_report.py E04 --tag 1080p30 --strict
   python tools/assemble.py E04 -q h --word-timings audio/aligned/E04/words.json
   python tools/package_narrated.py E04
   ```
   Watch the narrated lesson for sync, pace and pronunciation; decode the complete MP4 and
   verify video/audio streams, duration and absence of subtitle tracks. Mark final QA pass
   only after the narrated final has been watched. Repeat for each episode as audio arrives.
6. For silent previews, run `tools/render_series.py E04 -q m --jobs 3`, `tools/assemble.py E04 -q m`,
   `tools/package_preview.py E04 --tag 720p30`, then `tools/verify_previews.py E04`.
   Do not render the same scene simultaneously at two qualities: its text/TeX cache is shared.
7. Run `checks/verify_anchors.py`, `checks/verify_question_visuals.py` and `tools/lint_scripts.py`
   after content changes. `tools/export_question_figures.py` and `tools/build_docs.py` regenerate
   learner resources. The formula/method sheet is maintained by hand. Commit public code,
   scripts, documents and review records; do not commit recordings, keys, alignment or MP4s.
