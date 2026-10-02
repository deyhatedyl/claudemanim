# Reconciliation against VCAA examinations and examiners' reports

This document maps the series against the VCAA Chemistry examinations and examiners' reports that were supplied,
records what the reports say examiners expect, and lists every change made as a result. Exam questions are
referred to by number and paraphrased; no exam text is reproduced in the videos or learner documents, and the
series' practice questions (Q01–Q28) remain original material.

## Sources received

Uploaded to the repository on branch `deyhatedyl-patch-1` (not copied into this branch).

| File | Contents | Text | SHA-256 (first 16) |
|---|---|---|---|
| `2024chemistry-w.pdf` | 2024 examination | scanned; read via the report | `66da06fcc2d86c9c` |
| `2024chemistry-report.docx` | 2024 examiners' report | text | `3ee77c4529a042c9` |
| `2025-Chemistry.pdf` | 2025 examination | text | `f3e9c41333724c12` |
| `2025-Chemistry-report.docx` | 2025 examiners' report | text | `4c781d41533296f7` |
| `2025-NHT-chemistry.pdf` | 2025 NHT examination | scanned; Section A read page by page | `88ef2c54cbae4c09` |
| `2025-NHT-chemistry-report_0.docx` | 2025 NHT examiners' report | text | `e2a2f84b59f6e9c5` |
| `2026-NHT-Chemistry.pdf` | 2026 NHT examination | text | `21573912fc72f09e` |
| `2026-Chemistry-NHT-report.docx` | 2026 NHT examiners' report | text | `0050f316496f3a07` |

**Not received:** the VCE Chemistry Study Design. Scope statements below come from what the examiners' reports
say about the study design, not from the study design itself.

## Method

All 318 report items were parsed and the energy, fuels and calorimetry items identified by reading each one.
For questions whose report comment was blank (NHT Section A), the question itself was read. Each relevant item
was matched to the episode and scene that teaches the same skill. Gaps and examiner-reported errors were then
handled by adding or revising scenes, revising the worked solution for Q26 c, and updating the formula sheet.

## What the examiners' reports emphasise, and how the series responds

| Report emphasis | Source | Series response |
|---|---|---|
| "Energy released" is a positive quantity with a unit; a negative energy released is not a valid concept | 2024 report (general and Q5), 2025 B1b, 2026 NHT B2d.i | already taught (E02 checkpoint on ΔH sign vs energy released); added to the formula-sheet trap list |
| Explain the lower energy content of ethanol by partial oxidation (the hydroxy group); bond-enthalpy explanations need full calculations for both combustion equations, which is beyond the study design | 2025 B1e | **added** E12S04 "Why oxygen-containing fuels release less energy"; **revised** Q26 c answer, narration, on-screen reasons and mark tally (oxygen mass fraction, not one shared bond) |
| Bond enthalpies (Data Book) are used to explain and predict for simple structures: breaking is endothermic, forming exothermic | 2024 report (general and B3c.iii), 2025 A3, 2025 NHT A11 and B2b | covered: E02 bond ledger and exo/endo reasoning |
| Resolution is a property of an instrument stated with a unit: the smallest graduation of a scale, or the last digit of a digital display | 2024 report (general and B8b.iv), 2025 A19 | **added** E11S10 "Resolution, mistakes and outliers" |
| Identified mistakes are excluded and repeated; an outlier is not evidence of a systematic error | 2025 NHT A30 | **added** in E11S10 |
| Averaging reduces the *effect* of random errors (not "reduces random error") | 2025 NHT B9a.i | already worded this way in E11S09; on-screen tag in E11S13 tightened to match |
| Scatter about a line of best fit indicates random error; systematic error needs a reference value | 2025 A20 | covered: E11S06 and E11S09 |
| Record temperatures more often to define the maximum or the extrapolation better | 2025 NHT A29 | covered: E11S06, E11S13 |
| A calibration factor below the water-only heat capacity is impossible (for example a 100 mL calorimeter needs at least 418–420 J °C⁻¹) | 2025 NHT B5a.ii, 2026 NHT B2e | covered: E09S05 lower bound, Q18 (E09S10), Q27 a (E14S05) |
| Without calibration (water only) the calculated enthalpy is always smaller in size | 2024 B5b.i | covered: E09S02, E10S07 (CF model vs solution-only model) |
| A purity claim from calorimetry: kJ mol⁻¹ → kJ g⁻¹, % purity, compare with the claim, reasons it is low (CF too small; hygroscopic sample takes up water) | 2026 NHT B2b–e | covered closely by Q28 (E14S12–S16) and E14S16 error directions |
| Gas volumes: final − initial reading, mL → L, ÷ 24.8 at SLC; assumptions (25 °C and 100 kPa, ideal, only that gas, none dissolves); limitations; % yield | 2024 B8b, B8d; 2026 NHT B7c–g | **added** E07S08 "Measuring a gas volume" |
| An O₂ : fuel ratio below the complete-combustion ratio means combustion must be incomplete; products then follow from extra information (for example, no soot) | 2025 NHT B2c.ii | **added** beat E06S04 b04 |
| Water vapour from hot combustion counts as a greenhouse gas | 2026 NHT B1b | covered: E06S06–S08 (hot exhaust; greenhouse gases include water vapour) |
| Biodiesel/biofuel climate arguments must not claim less CO₂ on combustion | 2025 NHT B10b | covered: E04 (Q08 same molecule, different source), E12S09 carbon-neutral claim |
| Renewable needs a reference to time (replenished within a short period vs millions of years) | 2026 NHT B1d | covered: E04S03 |
| Atom economy is a green chemistry principle (percentage yield is not) | 2024 B9a.ii, 2025 NHT A19, 2026 NHT A26 and B4c.ii | **added** to the principles in E12S10 |
| Quote answers with units and justified significant figures (for example efficiency to 3 s.f.) | 2024 report, B5a.iii; 2025 NHT B6c.i; 2026 NHT B1c.ii | covered throughout; formula sheet "Reporting answers" |
| Do not use the old Data Book density of water (0.997 g mL⁻¹) | 2024 B5a.ii | consistent: the series uses 1.00 g mL⁻¹ only where a question says to treat a solution as water (E10S07) |

## Item-by-item map (energy, fuels and calorimetry items only)

Status: **covered** (taught and practised), **added** (new or revised content after this reconciliation),
**partial** (idea taught but not in this exam's form), **outside** (outside this series' scope).

| Exam | Item | Skill (paraphrased) | Where in the series | Status |
|---|---|---|---|---|
| 2024 | A1 | photosynthesis is endothermic, the reverse of combustion | E03 (reversing ΔH), E04S05 | covered |
| 2024 | A2 | energy per gram from Data Book values (glucose, hydrogen) | E05, E12S03 | covered |
| 2024 | A3 | reactant in excess from a mass of O₂ | E07S03–S05 | covered |
| 2024 | A11 | linear vs circular economy; SDGs | E12S10 | covered |
| 2024 | A13 | removing a catalyst raises Ea, not reactant or product energies | E03S04 | covered |
| 2024 | B3a | food energy from composition | E05 | covered |
| 2024 | B3c.ii | balancing a fatty-acid combustion (fractional O₂) | E06S02–S03 | covered |
| 2024 | B3c.iii | predicting the larger enthalpy change from bond types | E02 | partial |
| 2024 | B5a | fuel energy released, q = m c ΔT, % efficiency (3 s.f.) | E08 | covered |
| 2024 | B5b.i–iii | why calibrate; predicted maximum temperature; reasons for a high rise | E09, E10S09 (Q20), E11S12 | covered |
| 2024 | B8a | fermentation equation; enzyme denaturation | E04S06 (equation) | partial (enzymes outside) |
| 2024 | B8b, B8d | gas volume readings, assumptions, resolution, limitations | E07S08, E11S10 | added |
| 2024 | B9a.ii | atom economy as a green chemistry principle | E12S10 | added |
| 2025 | A1, A21 | renewable feedstocks (biomethane vs natural gas) | E04 | covered |
| 2025 | A2 | food energy from composition, scaled; J vs kJ | E05 | covered |
| 2025 | A3 | bond breaking endothermic, forming exothermic | E02 | covered |
| 2025 | A4 | circular economy | E12S10 | covered |
| 2025 | A5 | CF = VIt ÷ ΔT | E09 | covered |
| 2025 | A6 | reversing and dividing a thermochemical equation | E03 | covered |
| 2025 | A19 | resolution of glassware | E11S10 | added |
| 2025 | A20 | random error from scatter about a line of best fit | E11S06, E11S09 | covered |
| 2025 | B1a–c | thermochemical equation with states; energy released; q; efficiency | E03, E06S09, E08 | covered |
| 2025 | B1d | m³ → L; O₂ from air; excess O₂ mass | E01 (Q02), E07, E13 (Q25) | covered |
| 2025 | B1e | ethanol vs propane energy content: partial oxidation | E12S04, E13S15 (Q26 c) | added |
| 2025 | B7b | two green chemistry principles with evidence, an ethical factor, a conclusion | E12S10–S11 | partial (ethical factor not explicit) |
| 2025 NHT | A1 | food energy from composition (Data Book factors) | E05 | covered |
| 2025 NHT | A3 | activation energy read from a profile and scaled to an amount | E03 | partial (ΔH scaling taught; Ea scaling not shown) |
| 2025 NHT | A4 | fuel mass needed for a useful energy at a given efficiency | E08S07, E12S05 | covered |
| 2025 NHT | A11 | comparing bond strengths with Data Book bond enthalpies | E02 | covered |
| 2025 NHT | A19, A21 | green chemistry principles (atom economy) | E12S10 | added |
| 2025 NHT | A29 | improving a temperature–time measurement | E11S06, E11S13 | covered |
| 2025 NHT | A30 | mistakes and outliers | E11S10 | added |
| 2025 NHT | B2a–b | CO₂ mass from octane; exothermic via bonds | E06, E02 | covered |
| 2025 NHT | B2c | incomplete combustion from the O₂ : fuel ratio | E06S04 b04 | added |
| 2025 NHT | B5a | CF use; time from E = VIt; CF below the water-only value | E09 | covered (time rearrangement on the formula sheet) |
| 2025 NHT | B5b | excess reagent with a 1 : 2 ratio | E10S08 | covered |
| 2025 NHT | B9a.i | averaging and random error | E11S09, E11S13 | covered (wording tightened) |
| 2025 NHT | B10b | biodiesel and climate | E04, E12S09 | covered |
| 2026 NHT | A1, A2, A4 | respiration vs combustion; photosynthesis stores energy; fermentation products | E05S02, E04S05, E04S06 | covered |
| 2026 NHT | A5 | comparing energy profiles | E03 | covered |
| 2026 NHT | A6 | excess reagent and product mass | E07 | covered |
| 2026 NHT | A7, A8 | food label serve energy; maximum water temperature from SLC | E05, E10S09 | covered |
| 2026 NHT | A26, A27 | green chemistry principles; evidence for a "greener" claim | E12S10–S11 | covered / partial |
| 2026 NHT | B1a–b | thermochemical equation; greenhouse gas mass including water vapour | E03, E06S06–S08 | covered |
| 2026 NHT | B1d–e | renewable with a time reference; transesterification | E04S03, E04S08 | covered |
| 2026 NHT | B2a–e | circular economy; calibration; kJ g⁻¹; % purity vs claim; reasons | E09, E12S10, Q28 (E14) | covered |
| 2026 NHT | B4c.ii | sustainability of a methane-based process | E12 | covered |
| 2026 NHT | B7a–d, g | gas volume from a graph; % yield; assumptions; method accuracy | E07S08 | added (fuel-cell parts outside) |

## Outside this series

These exams also assess galvanic and electrolytic cells, fuel cells and Faraday calculations, rates and
equilibrium, organic reaction pathways, instrumental analysis (IR, NMR, mass spectrometry, HPLC), proteins and
enzymes, and titrations. None of these is taught here. Galvanic and fuel cells appear in the exams as energy
options; if the series should cover them, that is a scope decision for you.

## Remaining open points

* The VCE Chemistry Study Design was not supplied, so scope is inferred from the examiners' reports.
* Q03 (E02) calculates ΔH for H₂ + Cl₂ from bond enthalpies. The 2024 report expects bond-enthalpy reasoning
  for simple structures, so this is kept; the 2025 report's "beyond scope" comment concerns full calculations for
  fuels, which the series no longer uses as an explanation.
* Coverage item C26 still carries no episode tag, and E13/E14 have not been re-checked against the brief (see
  `logs/known_issues.md`).
