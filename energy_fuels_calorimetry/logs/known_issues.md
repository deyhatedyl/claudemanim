# Known issues and blockers

| Date | Item | Status |
|---|---|---|
| 2026-10-03 | **E04–E14 narration pending:** E01–E03 were delivered earlier. The learner generates the remaining speech locally using the standalone episode files and Melb Teacher F1 voice. Import measured beat clips or checked speech-aligned scene/episode segments, then re-render. No Gemini API key is required for this route. Silent previews are not finished narrated lessons. | awaiting learner audio |
| 2026-10-02 | Gemini TTS request shape for `gemini-3.8-flash-tts` not confirmed against live docs (ai.google.dev blocked by egress policy). `shared/tts.py` tries `voiceConfig.voice` and falls back to `voiceConfig.prebuiltVoiceConfig.voiceName`; `tools/tts_probe.py` records which one the API accepts. | optional Gemini route only; unused for manual narration |
| 2026-10-02 | Source files: the 2024 and 2025 examinations, the 2025 and 2026 NHT examinations and their four examiners' reports were supplied (branch `deyhatedyl-patch-1`) and reconciled; see `exam_reconciliation.md` (seven content additions or revisions). The VCE Chemistry Study Design was not among the files, so scope is inferred from the reports. | partly resolved |
| 2026-10-02 | Parallel renders raced on Manim's shared TeX cache ("latex failed but did not produce a log file"). Fixed: per-scene `tex_dir`. | fixed |
| 2026-10-02 | Draft layout defects in E01 (text past right edge in S01/S02/S03, overlaps in S04/S05/S06/S08). Fixed; an automatic per-beat layout check now flags off-frame/caption-strip objects. | fixed |
| 2026-10-02 | Recordings, generated alignment and MP4s are git-ignored. Public code/documents are committed; downloadable deliverables are kept outside the public repository. | resolved |
| 2026-10-02 | **Runtime**: the 14 silent drafts first totalled 191.9 min (3 h 12 min), below the brief's 3 h 15 min to 4 h 15 min. Twelve teaching scenes were added (E06, E07, E08, E09, E10, E11, E12); the drafts now total about 3 h 34 min at 145 words per minute including scripted pauses, and every episode except E01 sits inside its own target range. E01 (pilot) runs about 16.9 min against 10–14 min; it was left intact rather than cutting validated teaching. Real narration pace will change every runtime. | in range (series) |
| 2026-10-02 | Coverage item **C26** was checked against the accessible production brief. Q28 in E14S13–E14S16 teaches active fraction and the effect of calibration bias; the E14 script now carries the C26 tag. | resolved 2026-10-05 |
| 2026-10-02 | The production brief was read during the 5 October continuation; E13/E14 and C26 were checked. The earlier file-access blocker no longer applies. | resolved 2026-10-05 |
| 2026-10-02 | Question cards showed `ΔH_c` literally on screen (E07 Q13, E08 Q15). Fixed: text containing `ΔH_c` is drawn with a true subscript; affected scenes re-rendered. | fixed |
| 2026-10-03 | Reference-style continuation: header/card crowding, long kicker/pill collisions, graph/title clearance, Inter numerals and internal E01/E02 label spacing fixed. E01–E03: all 136 beat-end frames inspected at 1080p; 0 geometry flags. E04–E14 need a new-style render and review. | first three visually reviewed |


| 2026-10-05 | E04–E14 reference UI rendered and reviewed. New question stimuli, explanatory animation and internal label fixes are recorded in `checks/ui_review_20261005.json`. All new exported MP4s omit burned-in captions and subtitle tracks. E03 is kept as delivered. | visual continuation complete; narrated finals await WAVs |
