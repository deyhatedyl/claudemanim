# Resuming production (read this first in a new session)

1. **Read state**: `progress.json` (regenerate with `python tools/progress.py`), `checks/qa_status.json`,
   `logs/known_issues.md`, and the brief in `brief/production_brief.md`.
2. **Environment** (fresh container): `bash energy_fuels_calorimetry/tools/setup_env.sh` from the repo root.
   All commands below run from `energy_fuels_calorimetry/` with `../.venv/bin/python`.
3. **TTS check** (needs `GEMINI_API_KEY` in the environment):
   `python tools/tts_probe.py --voices Kore Charon Aoede` then listen to `audio/probe/*.wav`.
   Choose the voice (export `GEMINI_TTS_VOICE`), confirm pronunciation of joules, kilojoules, enthalpy,
   calorimetry, molar, methane and formulas. If the model name differs, set `GEMINI_TTS_MODEL`.
   Changing voice/model/style changes every clip hash, so decide before the full run.
4. **Per episode, in order** (resume at the first incomplete stage shown in progress.json):
   ```
   python tools/lint_scripts.py epNN          # spoken text TTS-ready (0 issues)
   python tools/gen_audio.py ENN              # narration clips (cached; safe to re-run)
   python tools/render.py ENN -q l            # narrated 480p draft with real timing + captions
   python tools/stills.py ENN -q l            # inspect checks/stills/ENN_480p15/sheet_*.png
   # watch the draft: renders/draft/ENN_*__480p15__narrated.mp4 (sync, pacing, pronunciation)
   python tools/render.py ENN -q h --jobs 2   # final 1080p30 -> renders/final/, captions/
   python tools/progress.py
   ```
   Record QA results in `checks/qa_status.json` (`final_qa: "pass"` only after watching the final).
5. **Scripts/visuals not yet written**: follow the pattern of `scripts/ep01.md` + `scenes/ep01.py`
   (one scene class per `## ENNSxx` heading; every `[bNN]` beat used once, in order — the render fails otherwise).
6. **Commit and push** after every completed stage. Rendered media under `renders/media/` is
   reproducible and git-ignored.
