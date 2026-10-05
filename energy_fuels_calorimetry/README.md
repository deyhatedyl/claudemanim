# VCE Chemistry: Energy, fuels and calorimetry — narrated Manim series

Production project for a 14-episode narrated video series (12 teaching episodes + 2 exam workshops)
following `brief/production_brief.md`. All practice questions (Q01–Q28) are original material written
for this series; they are not official VCAA questions or marking schemes.

**Current continuation (5 October 2026): Episodes 4–14.** Episodes 1–3 were delivered earlier;
Episode 3 is kept as delivered. The continuation keeps the supplied reference UI: Inter text and
equation letters/numerals, navy background, compact section labels, centered titles and colored badges.

The remaining episodes add curved carbon and molecule movement, animated useful/lost energy,
thermometer changes, matching equation transformations, traced cooling extrapolation and moving
calibration-bias markers. Graph questions Q21 and Q27 show actual plotted givens during the attempt,
with fine divisions and exact cooling readings. Fits and corrected temperatures appear in the solution.
Q09, Q10, Q23, Q24 and Q26 display comparison data as tables. All questions remain original practice
with indicative marks. The numerical givens and spoken scripts are unchanged.

`checks/ui_review_20261005.json` and `checks/preview_validation_20261005.json` record the new review.
The continuation exports **silent 720p30 visual previews with estimated timing**. They are not narrated
final lessons. The narration pack supplies 11 standalone Python files using the learner's working
Gemini request format and existing Melb Teacher F1 voice. Narrated 1080p30 renders require the learner's
WAVs, checked speech alignment and measured beat durations.

**Future MP4s contain neither burned-in captions nor embedded subtitle tracks.** SRT/VTT and
transcripts remain separate optional files. Nothing from the earlier delivered Episode 3 is replaced.
Recorded narration, keys and derived alignment files stay private and outside GitHub.

All 14 episodes are scripted; the 337 independent numerical, atom-balance and mark checks pass.
The full worksheet, worked solutions, formula/method sheet, coverage matrix and viewing order are
included. C26 is taught in Episode 14's Q28 calibration/active-fraction example and is now tagged.

## Layout

| Path | Contents |
|---|---|
| `brief/` | the production brief (verbatim) |
| `questions/bank.py` | Q01–Q28 prompts, parts, marks, final answers, traps (single source) |
| `questions/worksheet.md` | learner worksheet: questions only (generated) |
| `solutions/worked_solutions.md` | working per part, indicative marks per observable step, traps, where each is worked (generated) |
| `solutions/formula_and_method_sheet.md` | formula and method sheet (hand-written) |
| `exam_reconciliation.md` | 2024, 2025, 2025 NHT and 2026 NHT exams and reports mapped to episodes; changes made |
| `coverage_matrix.md`, `series_index.md` | coverage C01–C28 → episodes/questions; viewing order, runtimes, files (generated) |
| `checks/verify_anchors.py` | independent numerical/atom-balance/marks verification → `checks/numerical_check_record.md` |
| `scripts/epNN.md` | narration scripts + scene table (objective, on-screen, transitions, checks per scene) |
| `scenes/epNN.py` | Manim scenes, one class per script scene; timing driven by narration beats |
| `shared/` | style (palette, fonts, safe areas), components, script parser, TTS client, NarratedScene |
| `tools/` | lint, audio generation, rendering, assembly (captions/transcripts/mux), stills, progress, docs, scene renumbering |
| `audio/` | narration clip cache + manifest (content-hash keyed) |
| `captions/` | final SRT/VTT/transcripts (drafts keep theirs beside the draft MP4) |
| `renders/draft`, `renders/final` | assembled episodes |

## How timing works

Each scene's narration is split into beats (`[bNN]` in the script). `NarratedScene.beat()` reads the
measured duration of that beat's clip (or a words-per-minute estimate when no clip exists), runs the
visuals inside it, then waits for the narration to finish. Frame-accurate start times are written to
`renders/timelines/<quality>/<scene>.json`; `tools/assemble.py` places each clip at its start time,
normalises loudness (−16 LUFS, −1.5 dBTP), writes separate captions from the same timeline and
exports the MP4 without subtitles.

## Commands

See `RESUME.md`. Quick reference (from this folder, using the repo's `.venv`):

```
python checks/verify_anchors.py        # 337 checks must pass
python tools/lint_scripts.py           # spoken text TTS-ready + timing estimates
python tools/render.py E01 -q l        # draft
python tools/stills.py E01 -q l        # beat-end stills for review
python tools/progress.py               # refresh progress.json
python tools/build_docs.py             # worksheet, worked solutions, coverage matrix, series index
```

## Visual conventions

Dark navy background, Inter text and equation letters/numerals (XeLaTeX + mathastext; mathematical
symbols use the available TeX symbol fonts). Colour roles (always paired with a label,
arrow or line style): system = orange, calorimeter/surroundings = blue, useful energy = green solid,
losses = red dashed, unknown = yellow box with "?"/"Asked" tag. Quantity chips: amount (mol) lavender,
mass (g) teal, volume (L) light blue, concentration pink, energy amber. The bottom ~15% of the frame
remains clear for thinking timers and visual breathing room; every beat is checked automatically for off-frame or caption-strip content.

## Manual narration and preview workflow

```
python tools/export_narration.py E01 E02 E03
python tools/import_manual_audio.py --directory audio/manual --episodes E01 E02 E03
MANIM_BIN=$(command -v manim) EXPORT_BEAT_STILLS=1 python tools/render.py E01 -q h
python tools/layout_report.py E01 --tag 1080p30
```

The narration pack includes clean full-episode and per-scene text, optional per-beat text and one
voice-direction file. Beat files import directly. Whole-scene/episode recordings require checked
speech alignment first; `import_manual_audio.py --segments checked-alignment.json --episodes E01`
imports those measured segments. An edit to the spoken script invalidates that beat's audio cache.
Re-render with measured durations before assembling narrated lessons. Estimated preview timestamps
must never be used as an audio alignment.

For scene recordings named `E01S01.wav` through `E01S09.wav`, a local alignment route is available:

```
python -m pip install torch==2.8.0 torchaudio==2.8.0
python tools/align_manual_audio.py E01 --directory audio/manual --output audio/aligned/E01
# Review audio/aligned/E01/alignment-review.json and the scene boundaries before import.
python tools/import_manual_audio.py --segments audio/aligned/E01/segments.json --episodes E01
EXPORT_BEAT_STILLS=1 python tools/render.py E01 -q h --no-assemble
python tools/layout_report.py E01 --tag 1080p30 --strict
python tools/assemble.py E01 -q h --word-timings audio/aligned/E01/words.json
python tools/package_narrated.py E01
```

The alignment tool downloads an English acoustic model on first use, then processes recordings
locally. It produces measured beat boundaries, word timings and a recognition report. TorchAudio
2.8 is pinned because later versions remove the CTC alignment functions used here. Word timings
must match the exact current script; assembly rejects a mismatch. The narrated delivery has no subtitles in the MP4, plus a separate SRT/VTT and a transcript. Keep recordings and generated alignment data private.

The older chemistry preview workflow covers Episodes 1–3 and is a historical preview route. For the
continuation, use `tools/render_series.py E04 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 -q m --jobs 3`,
then `tools/assemble.py E04 -q m` and `tools/package_preview.py E04 --tag 720p30` (repeat by episode).
`tools/verify_previews.py E04` checks the complete video stream, timing, layout and absence of audio/subtitles.
Do not render the same scene concurrently at different qualities: its per-scene text/TeX cache is shared.

Generate the reusable narration pack with:

```bash
python tools/build_narration_pack.py E04 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14
python checks/verify_narration_pack.py
python checks/verify_question_visuals.py
python tools/export_question_figures.py
```

The pack's START-HERE.md includes all Terminal commands and the per-episode WAV ZIP helper.
Question graph/table conventions follow the VCAA Chemistry [planning guidance](https://www.vcaa.vic.edu.au/curriculum/vce-curriculum/vce-study-designs/chemistry/planning)
for labelled quantities, units, scales and data presentation; these are original practice questions.
