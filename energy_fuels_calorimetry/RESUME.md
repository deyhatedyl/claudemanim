## Continuation 12 October 2026 — source and first render checks

The 12 October chemistry audit is available in the learner's ChatGPT file Library
as `Chemistry-Series-Audit-2026.md`, alongside the authoritative 2026 Chemistry
Data Book. Scene WAV ZIP archives `Archive 7.zip` through `Archive 14.zip`
and the original narrated 1080p MP4s are also in the learner's Library. They
are deliberately not checked into this public repository.

**Audited corrections committed on this branch:**
- E06: oxygen shortage does not force all methane to react incompletely;
  CO/CO₂ split requires complete-consumption and product assumptions.
  Cooling alone leaves residual water vapour, so a drying step is indicated.
- E07: distinguish newly produced CO₂ from the total CO₂ leaving the system.
- E08: mixing 17,974 J with 27.4 kJ and multiplying by 100 gives 65,600%,
  whereas the unit-consistent Q15 answer remains 65.6%.
- E12: octane -5470 kJ/mol and 48.0 kJ/g, ethanol -1367 kJ/mol and
  29.7 kJ/g for current-book GENERAL comparisons. Q13/Q15/Q26 explicitly
  supply -1370, which must be retained. Lower lifecycle emissions also
  require comparative evidence.
- E14: the molar-enthalpy denominator is the amount on the requested basis;
  for a reaction as written use reaction extent, not always raw limiting moles.
- Corresponding script wording was updated in scripts/ep06,07,08,12,14.md;
  altered speech must be rerecorded/checked before a narrated final export.

**Visual work committed:**
- `shared/worked_sidebar.py` holds a compact, persistent question/source
  panel with labels question (blue), 2026 data book (amber), earlier result
  (green) and focusable per-value rows.
- E07S05 (Q13), E08S06 (Q15) and E08S08 (Q16) preserve question givens
  beside calculation lines and Indicate() source quantities during related
  narration beats. The full question remains visible during the attempt.
- `shared/workshop.py:question_ribbon` supports full-width data-source
  reminders just below workshop scene titles.
- E13S06,S08,S09 (Q25) and E14S05,S06,S08,S13 (Q27/Q28) use this ribbon.

**Validation as of 12 Oct:**
- `.github/workflows/chemistry-worked-questions.yml` performs independent
  numeric/script checks, Python compilation, a 480p15 animated scene render,
  and a 1080p30 Manim still for each targeted scene.
- First run (GitHub Actions #38207504818) completed successfully for
  E07S05, E08S06 and E08S08; its artifacts contain silent 480p15
  animated previews and full-HD end frames.
- Follow-up run #38207998884 checks the additional E13/E14 workshop changes;
  inspect outcome and artifacts rather than assuming pass.
- The full corrected narrated MP4s have not yet been exported; the
  previous versions are still the original lessons.

**Next steps when the run finishes:**
1. Inspect its stills and mid-scene frames for visual overlap and layout.
   Correct any problems and rerun only failing scenes.
2. Continue the persistent question/source pattern for remaining worked
   examples, especially E07 Q14, E08 other practice, E13 Q26 and E14 Q28.
3. Restore WAVs from the learner's Archive ZIPs into private audio/manual.
   Compare their *actual revised spoken words* with the current scripts.
   Regenerate only narration affected by the audit, using the user's
   requested Gemini voice, then force-align and check all beat timestamps.
4. With matched speech, re-render affected scenes at 1080p30, assemble
   complete episodes, decode/listen through the MP4s and verify readability,
   chemistry, units, timing and absence of embedded subtitles.
5. Deliver revised narrated MP4s as private attachments rather than GitHub
   source commits. Do not modify delivered Episode 3.

---

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
## Gemini-only narration correction — 12 October 2026

The learner explicitly requires the existing **Gemini Melb Teacher F1**
voice for every final narrated video. No alternate voice is authorised for
delivery. The previous temporary macOS Karen retakes are EXCLUDED from the
active `audio/manifest.json` (all nine entries removed); never package them.
The original archived scene WAV files remain unmodified.

- The original voice ID exists in the user's private
  `Electrochemistry/voice_samples_melb/voice_ids.txt` and is resolved by
  `tools/narration_runner.py`.
- `tools/gemini_audit_retakes.py` prepares only the **ten** reviewed chemistry
  narration changes, preserving all other authored speech. Its dry run
  passed for `gemini-3.8-flash-tts` and the original Melb Teacher F1 voice.
- The connected workspace presently has no `GEMINI_API_KEY` or
  `GOOGLE_API_KEY`. Provide one as a private environment variable in the
  local Chat On Steroids session; never commit or paste it into source files.
- Then install the Google GenAI SDK in the project venv, run
  `python tools/gemini_audit_retakes.py`, and follow the import instruction
  printed by the script. Inspect the voice, exact numbers and pronunciation
  before full narration assembly.
- The known-good original Q13 recording was force-aligned with 0.9766
  recognition similarity; `audio/aligned/E07/words.json` contains measured
  speech timing for seven beats. The E08 Q15 recording was independently
  aligned at 0.9623 similarity.
- The exact-part question UI in `shared/active_question.py` now replaces the
  combined Q13/Q15/Q16 question sidebar. Additional source-backed question
  ribbons were added to Q14, Q25, Q26, Q27 and Q28 working.
- Python compilation, the 337 independent chemistry checks, the question
  stimulus audit and Q25/Q26 preview stills passed. Full revised 1080p
  narrated episodes have **not yet been produced**; more render and audio
  synchronization checks are required.

## Subsequent QA update — October 12 (after 1080p cloud review)

- Final-layout cloud run 38234850646 successfully rendered E07/E13/E14 at
  1080p30 and assembled silent previews, but strict validation flagged hidden
  replaced headers, footer tallies, and the E14 time-axis label. The layout
  detector now ignores transparent headers, recognises intentional footer
  tallies without exempting ordinary content, and still enforces off-frame
  bounds. E14 graph height was adjusted after inspecting the actual still.
- E13 Q25 part d now explicitly displays `57.0 - 17.0 = 40.0 °C` before
  substituting into `q = mcΔT`. Independent Q26 scientific review found the
  original oxygen-fraction wording too categorical. Q26 scene, answer and
  spoken script now use whole-molecule combustion enthalpies and molar masses.
  **This requires an additional Gemini retake `E13S15.b01`: ten in total.**
- Four layout regression tests pass; 337 chemistry anchor checks, question
  stimuli verification, Gemini cache tests and Python compilation pass.
- The original 161 WAV symlinks remain available locally. Initial E04S01
  original-speech alignment passed with 0.962 recognition similarity. Only
  E07 Q13 and E08 Q15 had been imported into the active beat manifest prior
  to the new E04 alignment test.
- The Mac checkout must not be hard-reset: remote branch has newer API-made
  commits, local HEAD differs, and private/QA files remain in the working tree.
- A final narrated 1080p export still requires complete checked audio imports,
  successful custom Melb Teacher F1 Gemini retakes, and rendered-frame QA.

## Updated user voice preference — October 12, later message

The learner has explicitly **relaxed** the earlier F1-only constraint:
"we dont need f1 melbourne tea cher voice, just a melbournian warm teacher voice."
Keep Gemini synthesis and a warm, natural Melbourne/Victorian Australian
Chemistry-teacher delivery. The retired exact Melb Teacher F1 voice ID is
**not** required for corrected audio. The corrected-beat tools now default
to Gemini's prebuilt warm **Sulafat** voice, with an explicit
Melbourne/Australian accent and Year 12 teaching style for native Google
speech_metadata. Choose/confirm a short audible sample before recording all
ten changed beats: a preset's warm timbre alone cannot prove its accent.
An existing private Google API key or OpenRouter key is still required to
actually generate the corrected WAVs; no key is present in this workspace.
Preserve existing good original WAVs, and never print credentials.

## First complete narrated full-HD output — Episode 4

The ten original E04 scene WAVs were force-aligned to the verified authored
transcript, with recognition similarity 0.962–0.995. All 42 beats were
imported and E04 rendered/assembled at 1080p30 with measured speech timing.

- Local MP4: `delivery/E04/E04-Chemistry-Narrated-1080p.mp4`.
- Assembly: 42/42 audio-backed beats, final and narrated, 770.83 seconds.
- Strict geometry: ten scenes, no reported layout problems.
- Full FFmpeg video/audio decoding succeeded; FFprobe found H.264
  1920×1080 at 30 fps, AAC audio, zero embedded subtitle tracks.
- Eight sampled frames across the completed movie showed no obvious overlaps.
  A continuous human watch-through is still recommended.

The existing original Gemini recording is retained; no new narration is
needed for E04. The studio-voice preference applies to future retakes.

---
