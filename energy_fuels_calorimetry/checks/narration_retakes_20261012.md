# Narration retake manifest — 12 October 2026

This is an exact comparison of [bNN] spoken text on the chemistry branch before
the October 12 audit corrections (commit `ebad79350f5e70cf20f28cbdb0a8234b7ee0a3c0`)
and the corrected scripts. Preserve the learner's selected
**Gemini Melb Teacher F1 voice** for regenerated audio.

## Exactly nine changed narration beats

| Episode | Beat | Why narration must be refreshed |
|---|---|---|
| E06 | E06S04.b04 | Oxygen insufficiency alone does not determine the amount of fuel consumed or specific incomplete combustion products; add explicit premises |
| E07 | E07S12.b01 | Newly formed CO₂ is coefficient × extent; total outlet CO₂ can also contain inlet CO₂ |
| E08 | E08S06.b06 | Explain the 65,600% mixed-unit efficiency error correctly |
| E12 | E12S02.b01 | Octane: 5470 kJ/mol reference value |
| E12 | E12S02.b02 | Octane: 5470 ÷ 114 = 48.0 kJ/g |
| E12 | E12S04.b01 | Ethanol: 1367 kJ/mol, approximately 29.7 kJ/g in the current data-book comparison |
| E12 | E12S09.b03 | A lower-carbon claim needs lifecycle evidence |
| E14 | E14S17.b03 | Divide reaction heat by the requested molar basis, normally reaction extent for per-mole-of-reaction as written |
| E14 | E14S18.b02 | Same distinction when diagnosing an incorrect answer |

Every other `[bNN]` spoken line in those five episodes was unchanged by this
audit. Original question-specific values (e.g. Q13, Q15, Q26 ethanol
`-1370 kJ mol⁻¹`) remain valid because they were **given in those questions**.

## Rendering/synchronisation requirements

1. Export the nine **exact updated beat texts** from current `scripts/epNN.md`.
   Record only these segments with the same voice. Do not substitute the
   original recordings for beats whose words or numbers changed.
2. Recover original Archive 7–14 scene WAVs privately from ChatGPT Library.
   The full spoken asset archives and any Gemini credential must stay out of
   the public repository and CI. Existing recordings can be reused for
   unchanged text after checking audio quality and hashes.
3. Import all corrected beat clips into `audio/manual`, check alignment
   against the exact updated script and regenerate timing/word highlights.
4. Render affected scenes at 1080p30 after audio retakes; assemble and
   inspect the narrated full-episode outputs. Burned-in or embedded subtitles
   are not requested. Episode 3 remains unchanged.

The silent GitHub Actions episode previews are useful for visual QA, but
they cannot substitute for speech-matched narrated finals.
