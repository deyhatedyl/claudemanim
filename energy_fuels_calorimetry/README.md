# VCE Chemistry: Energy, fuels and calorimetry — narrated Manim series

Production project for a 14-episode narrated video series (12 teaching episodes + 2 exam workshops)
following `brief/production_brief.md`. All practice questions (Q01–Q28) are original material written
for this series; they are not official VCAA questions or marking schemes.

**Current state: see `progress.json` (generated) and `logs/known_issues.md`.**

* All 14 episodes are scripted (TTS-ready, 0 lint issues), built as Manim scenes and rendered as
  **silent 480p drafts with estimated timing**; every beat-end still has been inspected and the
  automatic layout check reports no off-frame or caption-strip content. Draft series runtime is about
  3 h 28 min (`series_index.md`).
* Learner documents are complete: `questions/worksheet.md`, `solutions/worked_solutions.md`,
  `solutions/formula_and_method_sheet.md`; plus `coverage_matrix.md` and `series_index.md`.
* `checks/verify_anchors.py`: 326 independent numerical, atom-balance and marks checks, 0 failures.
* **Not yet produced:** narration audio, narrated drafts, final 1080p30 renders and final captions.
  Narration is blocked until a `GEMINI_API_KEY` is available in the environment (see `RESUME.md`).
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
python checks/verify_anchors.py        # 326 checks must pass
python tools/lint_scripts.py           # spoken text TTS-ready + timing estimates
python tools/render.py E01 -q l        # draft
python tools/stills.py E01 -q l        # beat-end stills for review
python tools/progress.py               # refresh progress.json
python tools/build_docs.py             # worksheet, worked solutions, coverage matrix, series index
```

## Visual conventions

Dark background, Noto Sans text, Computer Modern maths. Colour roles (always paired with a label,
arrow or line style): system = orange, calorimeter/surroundings = blue, useful energy = green solid,
losses = red dashed, unknown = yellow box with "?"/"Asked" tag. Quantity chips: amount (mol) lavender,
mass (g) teal, volume (L) light blue, concentration pink, energy amber. The bottom ~15% of the frame
is kept clear for subtitles; every beat is checked automatically for off-frame or caption-strip content.
