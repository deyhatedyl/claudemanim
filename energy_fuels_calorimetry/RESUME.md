# Resuming production (read this first in a new session)

1. **Read state**: `checks/ui_review_20261003.json`, `checks/qa_status.json`,
   `progress.json` (the older local draft snapshot; regenerate after new local renders),
   `logs/known_issues.md`, and the brief in `brief/production_brief.md`.
2. **Environment** (fresh container): `bash energy_fuels_calorimetry/tools/setup_env.sh` from the repo root.
   All commands below run from `energy_fuels_calorimetry/` with `../.venv/bin/python`.
3. **Narration route:** the learner will generate audio manually. No TTS key is required.
   `python tools/export_narration.py E01 E02 E03` produces the clean script pack and voice direction.
   Prefer one recording per scene (`E01S01.wav`, etc.) or per beat (`E01S01.b01.wav`, etc.).
   Keep the script's exact words and do not add long thinking pauses; the renderer adds those.
   Whole-scene/episode recordings need checked speech alignment before import. Do not use the
   silent preview's estimated timestamps as audio boundaries.
4. **Per episode, after audio arrives:**
   ```
   python tools/lint_scripts.py epNN
   python tools/import_manual_audio.py --directory audio/manual --episodes ENN
   # for scene/episode recordings instead: --segments checked-alignment.json --episodes ENN
   python tools/render.py ENN -q l --jobs 2
   python tools/stills.py ENN -q l
   # watch the narrated draft for sync, pacing and pronunciation
   EXPORT_BEAT_STILLS=1 python tools/render.py ENN -q h --jobs 2
   python tools/layout_report.py ENN --tag 1080p30 --strict
   python tools/progress.py
   ```
   Import only validated audio segments; the cache uses measured WAV durations and the current
   spoken text. Record narrated QA in `checks/qa_status.json` (`final_qa: "pass"` only after watching
   the final). E01–E03 silent 1080p previews have visual QA; narration and final QA are pending.
   E04–E14 still need rendering and inspection with the new shared UI.
5. **Scripts/visuals not yet written**: follow the pattern of `scripts/ep01.md` + `scenes/ep01.py`
   (one scene class per `## ENNSxx` heading; every `[bNN]` beat used once, in order — the render fails otherwise).
6. **Documents**: `python tools/build_docs.py` regenerates `questions/worksheet.md`,
   `solutions/worked_solutions.md` (mark tallies are read from the scenes, so they match the videos),
   `coverage_matrix.md` and `series_index.md`. Re-run after any change to `questions/bank.py`, a script,
   a practice scene or a render. `solutions/formula_and_method_sheet.md` is maintained by hand.
7. **Commit and push** after every completed stage. Rendered media under `renders/media/` is
   reproducible and git-ignored.
