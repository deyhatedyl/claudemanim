# VCE Chemistry: Energy, fuels and calorimetry — narrated Manim series

Production project for a 14-episode narrated video series (12 teaching episodes + 2 exam workshops)
following `brief/production_brief.md`. All practice questions (Q01–Q28) are original material written
for this series; they are not official VCAA questions or marking schemes.

**Current continuation: see `checks/ui_review_20261003.json` and `checks/qa_status.json`.**
`progress.json` records the earlier 480p draft run and does not include the new CI preview artifacts.

**Continuation, 3 October 2026:** the shared UI follows the supplied reference contact sheets:
Inter text and equation letters/numerals, dark navy, centered scene titles, compact section labels,
filled pills/checklist badges and lighter outlines. Question cards and graphs fit below the title;
long kickers leave room for the top-right pills. Internal label spacing was also reviewed.
E01–E03 have been rendered at 1080p30 and all 136 beat-end frames inspected. Automatic checks
report zero off-frame, caption-strip, header-crowding or kicker/pill flags across 27 scenes.
Captioned silent MP4s are available from the chemistry preview workflow; two-line captions fit
the reserved bottom strip. Narration remains pending; these are visual previews with estimated timing.
E04–E14 have **not** been rendered or reviewed with this new shared style; their older QA below
applies to the previously committed 480p drafts.

* All 14 episodes are scripted (TTS-ready, 0 lint issues), built as Manim scenes and rendered as
  **silent 480p drafts with estimated timing**; every beat-end still has been inspected and the
  automatic layout check reports no off-frame or caption-strip content. Draft series runtime is about
  3 h 34 min (`series_index.md`).
* Learner documents are complete: `questions/worksheet.md`, `solutions/worked_solutions.md`,
  `solutions/formula_and_method_sheet.md`; plus `coverage_matrix.md` and `series_index.md`.
* `checks/verify_anchors.py`: 337 independent numerical, atom-balance and marks checks, 0 failures.
* **Not yet produced:** narration audio, narrated drafts, final narrated 1080p30 lessons and audio-aligned captions.
  The learner will supply manually generated narration; no TTS API key is required for this route.
  Nothing in `renders/draft/` is a finished lesson: silent drafts carry `SILENT-estimated-timing`
  in their names, and draft MP4s are git-ignored (regenerate with `tools/render.py`).

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
normalises loudness (−16 LUFS, −1.5 dBTP), builds captions from the same timeline and muxes the MP4
with a soft subtitle track.

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
is kept clear for subtitles; every beat is checked automatically for off-frame or caption-strip content.

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
must match the exact current script; assembly rejects a mismatch. The narrated delivery has visible
captions, a separate SRT/VTT and a transcript. Keep recordings and generated alignment data private.

The prepared `.github/workflows/chemistry-previews.yml` renders only E01–E03 at 1080p30, exports
review frames and geometry reports, and packages silent MP4s with visible captions. The workflow
runs when changes are pushed to `codex/chemistry-layout-20261003`. The first three visual previews have been reviewed; they remain silent drafts with estimated
timing. Narrated final QA requires the learner's audio and re-rendering at measured beat durations.
