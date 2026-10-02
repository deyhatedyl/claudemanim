# Worked solutions with indicative marks and traps

> All questions are original practice questions written for this series. They are not official VCAA examination questions, and the marks shown are indicative only, not an official marking scheme.

Each solution gives the working for every part, the indicative mark allocation shown in the video (each mark is attached to an observable step), the main trap, and where the question is worked in the series. Numerical values are recomputed independently in `checks/verify_anchors.py` (see `checks/numerical_check_record.md`).

**Data for all questions.** Unless a question says otherwise: SLC = 25 °C and 100 kPa; molar volume of a gas at SLC, V<sub>m</sub> = 24.8 L mol⁻¹; specific heat capacity of water, c = 4.18 J g⁻¹ °C⁻¹; relative atomic masses C = 12.0, H = 1.0, O = 16.0. Food energy factors: carbohydrate 16 kJ g⁻¹, protein 17 kJ g⁻¹, fat 37 kJ g⁻¹. Use molar masses supplied in a question.

## Episode 01: Mole calculations and units that unlock the topic

### Q01. Two different ways to obtain an amount of substance (4 marks)

**Question.** A 0.345 g sample of ethanol has M = 46.0 g mol⁻¹. A separate gas sample occupies 186 mL at SLC.

**a.** Calculate the amount, in mol, of ethanol in the sample. *[1]*

> n(ethanol) = 0.345 g ÷ 46.0 g mol⁻¹ = 0.00750 mol

**b.** Calculate the amount, in mol, of gas in the gas sample. *[2]*

> V = 186 mL = 0.186 L; n = 0.186 L ÷ 24.8 L mol⁻¹ = 0.00750 mol

**c.** Explain whether equal amounts in mol would imply equal masses. *[1]*

> Equal amounts mean equal numbers of particles, not equal masses: mass also depends on molar mass, which can differ. The gas's identity and molar mass are not given, so its mass cannot be found.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | a. amount of ethanol, 0.00750 mol |
| 2 | b. 186 mL → 0.186 L, then ÷ 24.8 L mol⁻¹ = 0.00750 mol |
| 1 | c. equal amounts ≠ equal masses: molar masses differ; gas unknown |
| **4** | **total** |

**Trap.** Using 186 (mL) as if it were litres, or treating mol and grams as interchangeable.

**Worked in:** E01S07 “Practice Q01: two routes to an amount” (≈9:39 in the draft)

### Q02. Conversions inside a realistic data sheet (5 marks)

**Question.** A data sheet lists 0.0850 m³ of dry air at SLC, 20.9% oxygen by volume, a heating duration of 0.150 h and an energy input of 7.20 × 10⁴ J.

**a.** Express the air volume in L, the heating time in s and the energy input in kJ. *[3]*

> 0.0850 m³ × 1000 L m⁻³ = 85.0 L; 0.150 h × 3600 s h⁻¹ = 540 s; 7.20 × 10⁴ J ÷ 1000 = 72.0 kJ

**b.** Calculate the amount, in mol, of oxygen in the air sample. *[2]*

> V(O₂) = 0.209 × 85.0 L = 17.765 L; n(O₂) = 17.765 L ÷ 24.8 L mol⁻¹ = 0.7163… ≈ 0.716 mol

**Indicative marks**

| Marks | Observable step |
|---|---|
| 3 | a. three conversions: 85.0 L, 540 s, 72.0 kJ |
| 1 | b. oxygen fraction: 17.765 L of O₂ |
| 1 | b. n(O₂) = 0.716 mol |
| **5** | **total** |

**Trap.** Treating the whole air volume as oxygen, or treating m³ as mL.

**Worked in:** E01S08 “Practice Q02: conversions inside a data sheet” (≈13:13 in the draft)

## Episode 02: Where reaction energy comes from

### Q03. A bond-energy ledger (4 marks)

**Question.** For H₂(g) + Cl₂(g) → 2HCl(g), use average bond enthalpies H–H 436, Cl–Cl 243 and H–Cl 431 kJ mol⁻¹.

**a.** Estimate the enthalpy change for the equation as written. *[3]*

> Energy absorbed breaking bonds = 436 + 243 = 679 kJ; energy released forming bonds = 2 × 431 = 862 kJ; ΔH ≈ 679 − 862 = −183 kJ (per mole of reaction as written; an estimate because average bond enthalpies are used).

**b.** Explain why the reaction is exothermic. *[1]*

> More energy is released when the 2 H–Cl bonds form than is absorbed when the H–H and Cl–Cl bonds break, so there is a net transfer of energy from the system to the surroundings.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | bonds broken total: 679 kJ |
| 1 | bonds formed total: 862 kJ |
| 1 | ΔH ≈ −183 kJ (subtraction, correct sign) |
| 1 | explanation compares energy released and absorbed |
| **4** | **total** |

**Trap.** Adding all bond energies together, or saying that breaking bonds releases energy.

**Worked in:** E02S05 “Practice Q03: a bond-energy ledger” (≈4:48 in the draft)

### Q04. Endothermic does not mean energy disappears (3 marks)

**Question.** An idealised dissolution absorbs 18.0 kJ per mole of solute. In an insulated calorimeter, 0.0250 mol of solute dissolves completely.

**a.** State the energy change of the reacting system. *[1]*

> q(system) = +18.0 kJ mol⁻¹ × 0.0250 mol = +0.450 kJ

**b.** State the energy change of the surrounding calorimeter. *[1]*

> q(calorimeter) = −0.450 kJ

**c.** State whether the measured temperature rises or falls. *[1]*

> The temperature falls (energy leaves the calorimeter contents and enters the dissolving system).

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | a. q(system) = +0.450 kJ |
| 1 | b. q(calorimeter) = −0.450 kJ |
| 1 | c. temperature falls |
| **3** | **total** |

**Trap.** Giving the system and the calorimeter the same sign.

**Worked in:** E02S07 “Practice Q04: an endothermic change” (≈10:01 in the draft)

## Episode 03: Energy profiles and thermochemical equations

### Q05. Equation coefficients and water's state (5 marks)

**Question.** 2H₂(g) + O₂(g) → 2H₂O(l)     ΔH = −572 kJ

**a.** Write the thermochemical equation for the decomposition of 1 mol of liquid water, with its ΔH. *[2]*

> H₂O(l) → H₂(g) + ½O₂(g)     ΔH = +286 kJ

**b.** Calculate the energy released by the complete reaction of 0.750 mol of H₂. *[2]*

> 572 kJ is released per 2 mol H₂, i.e. 286 kJ per mol H₂; 0.750 mol × 286 kJ mol⁻¹ = 214.5 kJ ≈ 215 kJ released

**c.** Explain whether −572 kJ can be used unchanged if the product in the original equation is H₂O(g). *[1]*

> No. Gaseous water has higher enthalpy than liquid water (vaporisation absorbs energy), so forming H₂O(g) releases less energy; a different ΔH is required.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | a. reversed, halved equation with ΔH = +286 kJ |
| 2 | b. 215 kJ released |
| 1 | c. state changes ΔH |
| **5** | **total** |

**Trap.** Treating −572 kJ as per mole of H₂, or ignoring physical states.

**Worked in:** E03S08 “Practice Q05: scaling, reversing and states” (≈9:33 in the draft)

### Q06. Read the vertical distances, not the absolute heights (5 marks)

**Question.** An energy profile uses a common arbitrary enthalpy reference, in kJ per mole of reaction. Reactants are at 80, products at 25 and the uncatalysed maximum at 150. A catalysed maximum is at 110.

**a.** Find the forward activation energy. *[1]*

> 150 − 80 = 70 kJ mol⁻¹

**b.** Find the reverse activation energy. *[1]*

> 150 − 25 = 125 kJ mol⁻¹

**c.** Find ΔH. *[1]*

> 25 − 80 = −55 kJ mol⁻¹

**d.** Find the catalysed forward activation energy. *[1]*

> 110 − 80 = 30 kJ mol⁻¹

**e.** Explain whether the catalyst changes the heat released by the same amount reacting. *[1]*

> No. The reactant and product enthalpies are unchanged, so ΔH and the heat released for the same amount reacting are unchanged; only the pathway's barrier is lower.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | a. 70 |
| 1 | b. 125 |
| 1 | c. −55 |
| 1 | d. 30 |
| 1 | e. ΔH unchanged |
| **5** | **total** |

**Trap.** Reading 150 as Ea, or saying a lower barrier changes ΔH.

**Worked in:** E03S05 “Practice Q06: read the vertical distances” (≈4:40 in the draft)

## Episode 04: Fuels, biofuels and the carbon cycle

### Q07. Fermentation yield and its coproduct (6 marks)

**Question.** A food-waste hydrolysate contains 270.0 g glucose (M = 180.0 g mol⁻¹). Assume fermentation produces only ethanol and carbon dioxide and achieves 78.0% of the theoretical conversion to these products.

**a.** Write the balanced equation for the fermentation, with states. *[1]*

> C₆H₁₂O₆(aq) → 2C₂H₅OH(aq) + 2CO₂(g)

**b.** Calculate the masses of ethanol and of carbon dioxide formed. *[4]*

> n(glucose) = 1.50 mol; theoretical ethanol = CO₂ = 3.00 mol; actual = 0.780 × 3.00 = 2.34 mol each; m(ethanol) = 2.34 × 46.0 = 107.64 ≈ 108 g; m(CO₂) = 2.34 × 44.0 = 102.96 ≈ 103 g

**c.** Give one role of the subsequent distillation. *[1]*

> Distillation separates and concentrates ethanol from the aqueous fermentation mixture, using the difference in volatility (boiling point) of ethanol and water.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | equation with states |
| 1 | 1 : 2 ratio → 3.00 mol |
| 1 | yield applied once → 2.34 mol |
| 2 | masses: 108 g ethanol, 103 g CO₂ |
| 1 | distillation separates/concentrates |
| **6** | **total** |

**Trap.** Using a 1 : 1 glucose : ethanol ratio, applying the 78.0% twice, or calling distillation fermentation.

**Worked in:** E04S07 “Practice Q07: fermentation yield” (≈6:09 in the draft)

### Q08. Same molecule, different source (4 marks)

**Question.** Two purified fuels each contain only CH₄. One is obtained from geological natural-gas reserves; the other from anaerobic digestion of recently grown plant waste.

**a.** Under the same conditions, compare the energy released and the CO₂ produced per mole burned. *[1]*

> Identical: the same molecule undergoing the same reaction releases the same energy and forms 1 mol CO₂ per mol CH₄.

**b.** Classify each source as renewable or non-renewable, with a reason. *[2]*

> Natural gas is non-renewable: it formed over millions of years and is used far faster than it is replaced. Biomethane is renewable: its plant feedstock regrows on a human timescale.

**c.** Explain why renewability alone does not prove overall sustainability. *[1]*

> Sustainability needs the whole lifecycle, e.g. methane leakage from digesters and pipelines (a potent greenhouse gas), energy used in processing, land and water use.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | a. same energy and CO₂ per mol |
| 2 | b. classification with timescale reasons |
| 1 | c. a lifecycle issue |
| **4** | **total** |

**Trap.** Claiming that biomethane produces no CO₂ when burned.

**Worked in:** E04S09 “Practice Q08: same molecule, different source” (≈10:07 in the draft)

## Episode 05: Food as a chemical energy source

### Q09. Food label with a serving and unit trap (4 marks)

**Question.** A 90 g packet contains three 30.0 g servings. Per 100 g, the product contains 48.0 g carbohydrate, 12.0 g protein and 18.0 g fat.

**a.** Calculate the energy per 100 g, in kJ, using the supplied food factors. *[2]*

> 48.0 × 16 + 12.0 × 17 + 18.0 × 37 = 768 + 204 + 666 = 1638 kJ per 100 g

**b.** Calculate the energy in one serving, in kJ. *[1]*

> 1638 kJ × (30.0 g ÷ 100 g) = 491.4 ≈ 491 kJ

**c.** Express the energy in one serving in J. *[1]*

> 491.4 kJ × 1000 J kJ⁻¹ = 4.91 × 10⁵ J

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | weighted sum: 1638 kJ per 100 g |
| 1 | serving factor: 491 kJ |
| 1 | conversion: 4.91 × 10⁵ J |
| **4** | **total** |

**Trap.** Using the whole packet, or reporting the kJ value as J.

**Worked in:** E05S06 “Practice Q09: a label with a serving trap” (≈5:03 in the draft)

### Q10. Which food has more energy depends on the comparison (5 marks)

**Question.** Idealised label values per 100 g: Food A contains 50 g carbohydrate, 10 g protein and 12 g fat; Food B contains 35 g carbohydrate, 20 g protein and 15 g fat. An A serving is 80 g and a B serving is 50 g.

**a.** Calculate the energy per 100 g of each food. *[2]*

> A: 800 + 170 + 444 = 1414 kJ per 100 g; B: 560 + 340 + 555 = 1455 kJ per 100 g

**b.** Calculate the energy in one serving of each food. *[2]*

> A: 1414 × 0.80 = 1131.2 ≈ 1131 kJ; B: 1455 × 0.50 = 727.5 ≈ 728 kJ

**c.** State which food has more energy per 100 g and which serving contains more energy. *[1]*

> B has more energy per 100 g; the A serving contains more energy. The ranking depends on the basis.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | a: energy per 100 g for each food |
| 2 | b: energy in one serving of each food |
| 1 | c: both comparisons stated, each on its basis |
| **5** | **total** |

**Trap.** Comparing unmatched portion sizes without stating the basis.

**Worked in:** E05S08 “Practice Q10: two bases, two answers” (≈8:06 in the draft)

## Episode 06: Combustion equations and gaseous products

### Q11. Incomplete combustion with enough information to balance it (5 marks)

**Question.** At high temperature, 1.00 mol of ethanol (supplied as a liquid) reacts with 2.50 mol O₂. All of the ethanol and oxygen react. The only products are CO₂(g), CO(g) and H₂O(g); no solid carbon forms.

**a.** Determine the amount of water formed. *[1]*

> H: 6 H atoms → 3.00 mol H₂O

**b.** Determine the amounts of CO₂ and CO formed. *[2]*

> C: x + y = 2; O: 1 + 5 = 2x + y + 3 → x = 1.00 mol CO₂, y = 1.00 mol CO

**c.** Write the balanced equation. *[1]*

> C₂H₅OH(l) + 2½O₂(g) → CO₂(g) + CO(g) + 3H₂O(g)  (or ×2: 2C₂H₅OH + 5O₂ → 2CO₂ + 2CO + 6H₂O)

**d.** Compare this oxygen requirement with that for complete combustion of 1 mol ethanol. *[1]*

> Complete combustion needs 3.00 mol O₂ per mol ethanol; this reaction uses only 2.50 mol.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | H balance: 3 H₂O |
| 2 | C and O balances: x = y = 1 |
| 1 | balanced equation |
| 1 | complete needs 3.00 mol O₂ |
| **5** | **total** |

**Trap.** Forgetting the O atom in ethanol, or assuming incomplete combustion always gives only CO.

**Worked in:** E06S05 “Practice Q11: incomplete combustion you can balance” (≈3:39 in the draft)

### Q12. Hot exhaust versus cooled dry gas (5 marks)

**Question.** Complete combustion of 0.250 mol CH₄ occurs in excess oxygen at 600 °C. The exhaust is then cooled, liquid water is removed, and the CO₂ is isolated and measured at SLC. Assume complete collection.

**a.** State the amounts of CO₂ and H₂O formed. *[1]*

> CH₄ + 2O₂ → CO₂ + 2H₂O: 0.250 mol CO₂ and 0.500 mol H₂O

**b.** Calculate the masses of CO₂ and of water vapour newly formed in the hot exhaust. *[2]*

> m(CO₂) = 0.250 × 44.0 = 11.0 g; m(H₂O) = 0.500 × 18.0 = 9.00 g

**c.** Calculate the total mass of these two greenhouse gases newly formed in the hot stream. *[1]*

> 20.0 g

**d.** Calculate the volume of the isolated dry CO₂ at SLC. *[1]*

> V = 0.250 mol × 24.8 L mol⁻¹ = 6.20 L

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | mole ratios |
| 2 | masses: 11.0 g and 9.00 g |
| 1 | total 20.0 g |
| 1 | 6.20 L at SLC |
| **5** | **total** |

**Trap.** Excluding hot water vapour, or applying the SLC molar volume to gas at 600 °C.

**Worked in:** E06S07 “Practice Q12: hot exhaust versus cooled dry gas” (≈7:19 in the draft)

## Episode 07: Limiting reactants, excess fuel and gas mixtures

### Q13. Excess means what is left after reaction (6 marks)

**Question.** An idealised calculation starts with 0.400 mol ethanol and 32.0 g O₂. Assume only complete combustion of the portion of ethanol that reacts, with unreacted excess left over. Use M(O₂) = 32.0 g mol⁻¹, M(ethanol) = 46.0 g mol⁻¹ and ΔH<sub>c</sub>(ethanol) = −1370 kJ mol⁻¹.

**a.** Identify the limiting reactant, with working. *[2]*

> n(O₂) = 1.00 mol. C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O. 0.400 mol ethanol would need 1.20 mol O₂ > 1.00 mol, so O₂ is limiting (n/coefficient: O₂ 0.333 < ethanol 0.400).

**b.** Calculate the mass of excess ethanol remaining. *[2]*

> Ethanol used = 1.00 ÷ 3 = 0.3333 mol; remaining = 0.0667 mol × 46.0 = 3.07 g

**c.** Calculate the mass of CO₂ produced. *[1]*

> CO₂ = 2 × 0.3333 = 0.6667 mol × 44.0 = 29.3 g

**d.** Calculate the energy released. *[1]*

> 0.3333 mol × 1370 kJ mol⁻¹ = 456.67 ≈ 457 kJ released

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | amounts and limiting justification |
| 2 | ethanol used; 3.07 g remaining |
| 1 | CO₂: 29.3 g |
| 1 | energy: 457 kJ |
| **6** | **total** |

**Trap.** Taking the smaller raw mole number as limiting, or reporting the starting amount as the amount remaining.

**Worked in:** E07S04 “Practice Q13: excess means what's left after reaction” (≈4:22 in the draft)

### Q14. A fuel stream already containing carbon dioxide (8 marks)

**Question.** At SLC, 12.4 L of an ideal gas mixture containing 80.0% CH₄ and 20.0% CO₂ by volume is supplied with 90.0 L of air containing 21.0% O₂ by volume. Treat the other air components as inert. Assume complete combustion of only the methane that can react, with excess methane left unreacted. Use M(CH₄) = 16.0 g mol⁻¹ and ΔH = −890 kJ mol⁻¹ for methane combustion to liquid water.

**a.** Calculate the initial amounts of CH₄ and O₂. *[2]*

> n(mixture) = 0.500 mol; n(CH₄) = 0.400 mol; V(O₂) = 18.9 L; n(O₂) = 0.76210 mol

**b.** Identify the limiting reactant. *[1]*

> CH₄ + 2O₂ → CO₂ + 2H₂O. 0.400 mol CH₄ needs 0.800 mol O₂ > 0.762 mol, so O₂ is limiting.

**c.** Calculate the mass of methane remaining. *[2]*

> CH₄ used = 0.38105 mol; remaining = 0.01895 mol × 16.0 = 0.303 g

**d.** Calculate the volume at SLC of newly formed CO₂. *[1]*

> 0.38105 mol × 24.8 = 9.45 L

**e.** Calculate the total CO₂ volume at SLC, including the CO₂ in the inlet stream. *[1]*

> Inlet CO₂ = 0.100 mol = 2.48 L; total = 11.93 ≈ 11.9 L

**f.** Calculate the energy released. *[1]*

> 0.38105 mol × 890 kJ mol⁻¹ = 339.1 ≈ 339 kJ

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | reactive fuel amount and O₂ amount |
| 1 | O₂ limiting |
| 2 | CH₄ remaining: 0.303 g |
| 1 | new CO₂: 9.45 L |
| 1 | total CO₂: 11.9 L |
| 1 | energy: 339 kJ |
| **8** | **total** |

**Trap.** Counting all of the fuel-stream gas as methane, or treating all measured CO₂ as newly formed.

**Worked in:** E07S07 “Practice Q14, part 1: budgets and the limiting reactant” (≈8:39 in the draft); E07S08 “Practice Q14, part 2: carbon dioxide and energy” (≈10:32 in the draft)

## Episode 08: Measuring combustion energy and efficiency

### Q15. A measured fuel mass loss (6 marks)

**Question.** An ethanol burner has a mass of 102.640 g before heating and 101.720 g afterwards. It heats 250.0 g of water from 19.8 °C to 37.0 °C. Assume the mass lost is ethanol combusted. Use M = 46.0 g mol⁻¹ and ΔH<sub>c</sub> = −1370 kJ mol⁻¹.

**a.** Calculate the mass and amount of ethanol burned. *[2]*

> 0.920 g; 0.920 ÷ 46.0 = 0.0200 mol

**b.** Calculate the energy released by the ethanol. *[1]*

> 0.0200 × 1370 = 27.4 kJ

**c.** Calculate the heat gained by the water. *[2]*

> ΔT = 17.2 °C; q = 250.0 × 4.18 × 17.2 = 17 974 J = 17.974 ≈ 18.0 kJ

**d.** Calculate the useful-energy efficiency for heating the water. *[1]*

> 17.974 ÷ 27.4 × 100% = 65.6%

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | mass and amount of ethanol |
| 1 | fuel energy: 27.4 kJ |
| 2 | water heat: 18.0 kJ |
| 1 | efficiency: 65.6% |
| **6** | **total** |

**Trap.** Using the full burner mass, using the fuel mass in q = mcΔT, or mixing J and kJ.

**Worked in:** E08S06 “Practice Q15: a measured fuel mass loss” (≈5:42 in the draft)

### Q16. Work backwards from useful heat (5 marks)

**Question.** A heater must warm 180.0 g of water from 18.0 °C to 78.0 °C. Its useful-energy efficiency is 45.0%, and the supplied fuel energy value is 29.8 kJ g⁻¹.

**a.** Calculate the useful heat required. *[2]*

> q = 180.0 × 4.18 × 60.0 = 45 144 J = 45.144 kJ

**b.** Calculate the chemical energy input required. *[1]*

> 45.144 ÷ 0.450 = 100.32 kJ

**c.** Calculate the minimum fuel mass required under this model. *[1]*

> 100.32 ÷ 29.8 = 3.366 ≈ 3.37 g

**d.** A student instead multiplies the water's required heat by 0.450 before dividing by 29.8. Explain the error. *[1]*

> Multiplying gives 0.682 g, less than the 1.515 g needed even at 100% efficiency, which is impossible: a less efficient heater needs more input, so divide by the efficiency.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | useful heat: 45.144 kJ |
| 1 | divide by efficiency: 100.32 kJ |
| 1 | fuel mass: 3.37 g |
| 1 | explanation with the 100% sanity check |
| **5** | **total** |

**Trap.** Using the efficiency in the wrong direction.

**Worked in:** E08S08 “Practice Q16: work backwards from useful heat” (≈9:28 in the draft)

## Episode 09: Why calorimeters need calibration

### Q17. Separate water heat capacity from apparatus heat capacity (6 marks)

**Question.** A calorimeter containing 120.0 g of water is electrically heated at 6.00 V and 1.50 A for 240 s. Its temperature rises by 4.00 °C. Assume negligible heat loss during calibration.

**a.** Determine the calibration factor. *[2]*

> E = 6.00 × 1.50 × 240 = 2160 J; CF = 2160 ÷ 4.00 = 540 J °C⁻¹

**b.** Determine the apparatus contribution to the heat capacity. *[1]*

> Water: 120.0 × 4.18 = 501.6 J °C⁻¹; apparatus = 540 − 501.6 = 38.4 J °C⁻¹

**c.** A later matched experiment produces a 5.60 °C rise. Calculate the heat gained by the calorimeter. *[1]*

> q = 540 × 5.60 = 3024 J ≈ 3.02 kJ

**d.** Estimate the calibration factor if the water mass is increased to 150.0 g with identical apparatus, assuming additive, constant heat capacities. *[2]*

> 150.0 × 4.18 + 38.4 = 627.0 + 38.4 = 665.4 ≈ 665 J °C⁻¹

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | E and CF |
| 1 | apparatus share |
| 1 | later heat |
| 2 | new CF |
| **6** | **total** |

**Trap.** Using mcΔT for the water as if it included the apparatus, or keeping CF unchanged after changing the contents.

**Worked in:** E09S05 “Practice Q17, part 1: calibrate, then use it” (≈3:58 in the draft)

### Q18. An impossible calibration factor and an appealing wrong explanation (4 marks)

**Question.** A setup contains 100.0 g of water and a cup/probe of positive heat capacity. A student reports CF = 360 J °C⁻¹ from electrical calibration and argues that heat loss explains the low value.

**a.** Assess the reported CF under the ordinary calibration model. *[2]*

> The water alone needs 100.0 × 4.18 = 418 J °C⁻¹; with positive apparatus heat capacity, CF must exceed 418, so 360 is inconsistent with the setup.

**b.** Assess the heat-loss explanation. *[1]*

> Heat loss reduces the observed ΔT, so CF = E/ΔT becomes larger, not smaller; it cannot explain a low CF.

**c.** Identify one measurement error that could make the reported CF too low. *[1]*

> An overestimated temperature rise, or an underestimated electrical energy (e.g. time, current or voltage recorded too low).

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | water-only lower bound: 418 J °C⁻¹ |
| 1 | 360 is inconsistent with the setup |
| 1 | heat loss would raise CF, not lower it |
| 1 | a valid error that lowers CF |
| **4** | **total** |

**Trap.** Giving 'heat loss' as a universal explanation without following the formula.

**Worked in:** E09S08 “Practice Q18: an impossible calibration factor” (≈8:36 in the draft)

## Episode 10: Reaction calorimetry and molar enthalpy

### Q19. A solution calorimetry denominator you must justify (8 marks)

**Question.** 75.0 mL of 0.800 mol L⁻¹ HCl is mixed with 50.0 mL of 0.900 mol L⁻¹ NaOH. The setup has been correctly calibrated for these conditions: CF = 590 J °C⁻¹. Both solutions begin at 20.00 °C and the final temperature is 24.30 °C. Assume complete neutralisation, with the measured rise attributable to it.

**a.** Calculate the amounts of HCl and NaOH. *[2]*

> n(HCl) = 0.0750 × 0.800 = 0.0600 mol; n(NaOH) = 0.0500 × 0.900 = 0.0450 mol

**b.** Identify the limiting reactant and the amount of acid left over. *[2]*

> HCl + NaOH → NaCl + H₂O (1 : 1): NaOH limiting; HCl left = 0.0150 mol

**c.** Calculate the heat gained by the calorimeter. *[2]*

> ΔT = 4.30 °C; q = 590 × 4.30 = 2537 J

**d.** Calculate the molar enthalpy change per mole of water formed. *[2]*

> n(H₂O) = 0.0450 mol; ΔH = −2.537 kJ ÷ 0.0450 mol = −56.4 kJ mol⁻¹

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | amounts |
| 2 | limiting reagent and excess |
| 2 | heat gained: 2537 J |
| 2 | denominator, sign and value: −56.4 kJ mol⁻¹ |
| **8** | **total** |

**Trap.** Dividing by the acid initially supplied, by total moles of solution, or by the total volume.

**Worked in:** E10S05 “Practice Q19: justify the denominator” (≈3:51 in the draft)

### Q20. One mole of reagent is not always one mole of reaction (6 marks)

**Question.** 2NaOH(aq) + H₂SO₄(aq) → Na₂SO₄(aq) + 2H₂O(l)     ΔH = −114 kJ for the equation as written. 0.0300 mol NaOH and 0.0200 mol H₂SO₄ are mixed in a correctly calibrated setup with CF = 480 J °C⁻¹. The initial temperature is 21.0 °C. Assume complete reaction and complete heat capture.

**a.** Identify the limiting reactant using the mole ratio. *[1]*

> n/coefficient: NaOH 0.0300 ÷ 2 = 0.0150; H₂SO₄ 0.0200 ÷ 1 = 0.0200 → NaOH limiting

**b.** Determine the reaction extent (moles of reaction as written). *[1]*

> 0.0150 mol of reaction

**c.** Calculate the heat released. *[1]*

> 0.0150 × 114 = 1.710 kJ

**d.** Calculate the temperature rise. *[1]*

> 1710 J ÷ 480 J °C⁻¹ = 3.5625 °C

**e.** Calculate the final temperature. *[1]*

> 21.0 + 3.5625 = 24.5625 ≈ 24.6 °C

**f.** Calculate the amount of H₂SO₄ remaining. *[1]*

> 0.0200 − 0.0150 = 0.00500 mol

**Indicative marks**

| Marks | Observable step |
|---|---|
| 1 | limiting by n/coefficient |
| 1 | extent 0.0150 mol |
| 1 | heat 1.710 kJ |
| 1 | rise 3.56 °C |
| 1 | final 24.6 °C |
| 1 | acid left 0.00500 mol |
| **6** | **total** |

**Trap.** Multiplying 0.0300 mol directly by 114 kJ, or reporting the rise as the final temperature.

**Worked in:** E10S07 “Practice Q20: predict the final temperature” (≈7:13 in the draft)

## Episode 11: Temperature graphs, correction and experimental reasoning

### Q21. Recover the appropriate temperature rise from a graph (5 marks)

**Question.** Mixing begins at t = 120 s. Pre-mixing temperatures at 0, 60 and 120 s are 21.0 °C. Subsequent measured temperatures: 135 s, 23.0 °C; 150 s, 25.0 °C; 165 s, 26.0 °C; 180 s, 26.1 °C; 240 s, 25.9 °C; 300 s, 25.7 °C; 360 s, 25.5 °C. CF = 650 J °C⁻¹.

**a.** Use the linear 180–360 s cooling trend to estimate the temperature at the mixing time. *[2]*

> Slope = (25.5 − 26.1) ÷ (360 − 180) = −0.00333 °C s⁻¹; T(120 s) = 26.1 + 0.00333 × 60 = 26.3 °C

**b.** Calculate the corrected temperature rise. *[1]*

> 26.3 − 21.0 = 5.3 °C

**c.** Calculate the corrected heat gained by the calorimeter. *[1]*

> 650 × 5.3 = 3445 J ≈ 3.4 kJ (two significant figures, graph estimate)

**d.** Compare this with the heat calculated from the highest observed temperature. *[1]*

> Highest observed 26.1 °C gives 5.1 °C and 3315 J ≈ 3.3 kJ, an underestimate because cooling had already begun before the peak was recorded.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | cooling region and extrapolation to 26.3 °C |
| 1 | corrected rise 5.3 °C |
| 1 | corrected heat ≈ 3.4 kJ |
| 1 | comparison: observed max underestimates |
| **5** | **total** |

**Trap.** Confusing the measured maximum with the corrected estimate, or reading the temperature itself as ΔT.

**Worked in:** E11S02 “Reading a temperature-time graph” (≈0:52 in the draft); E11S05 “Practice Q21: corrected heat” (≈3:58 in the draft)

### Q22. Good repeatability can coexist with the wrong answer (5 marks)

**Question.** A reaction of 0.0400 mol shows a 4.00 °C temperature rise. The valid CF is 500 J °C⁻¹, but a spreadsheet uses 450 J °C⁻¹. The reaction is exothermic.

**a.** Determine the reported and the corrected molar enthalpies. *[2]*

> Reported: −(450 × 4.00) ÷ 0.0400 = −45 000 J mol⁻¹ = −45.0 kJ mol⁻¹; corrected: −50.0 kJ mol⁻¹

**b.** Explain whether repeating the experiment fixes this error. *[1]*

> No. The same wrong CF is used every time, so repeats agree closely (good repeatability) but share the same systematic bias.

**c.** Would an additive thermometer offset of +1.5 °C on both initial and final readings change ΔT? Explain. *[2]*

> No. (T_f + 1.5) − (T_i + 1.5) = T_f − T_i, so an identical additive offset cancels in the difference. This does not apply to every kind of thermometer error (e.g. a scale error).

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | reported −45.0 and corrected −50.0 kJ mol⁻¹ |
| 1 | repeating keeps the same bias |
| 2 | offset cancels in the subtraction |
| **5** | **total** |

**Trap.** Equating repeatability with accuracy, or assuming every offset changes a difference.

**Worked in:** E11S08 “Practice Q22: a wrong CF and a thermometer offset” (≈7:41 in the draft)

## Episode 12: Fair fuel comparisons and sustainability

### Q23. Compare emissions per useful energy, not per fuel mass (7 marks)

**Question.** Hypothetical comparison data, supplied solely for this exercise. Fossil Fuel R: 43.0 MJ kg⁻¹, 35.0% useful-heat efficiency, lifecycle emissions 80.0 g CO₂-e per MJ of fuel energy. Waste-derived Biofuel S: 29.0 MJ kg⁻¹, 28.0% efficiency, lifecycle emissions 45.0 g CO₂-e per MJ of fuel energy.

**a.** For delivery of 1.00 MJ of useful heat, calculate the fuel energy input for each fuel. *[2]*

> R: 1.00 ÷ 0.350 = 2.857 MJ; S: 1.00 ÷ 0.280 = 3.571 MJ

**b.** Calculate the mass of each fuel required. *[2]*

> R: 2.857 ÷ 43.0 = 0.0664 kg; S: 3.571 ÷ 29.0 = 0.123 kg

**c.** Calculate the lifecycle emissions for each fuel. *[2]*

> R: 2.857 × 80.0 = 229 g CO₂-e; S: 3.571 × 45.0 = 161 g CO₂-e

**d.** Evaluate the claim that the lower fuel mass must mean lower emissions. *[1]*

> The claim is false here: R needs less mass but S has lower lifecycle emissions for the same useful output; mass and emissions measure different things.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | fuel energy input for each fuel |
| 2 | mass of each fuel |
| 2 | lifecycle emissions for each fuel |
| 1 | evaluation of the mass-based claim |
| **7** | **total** |

**Trap.** Comparing emissions per input MJ without correcting for efficiency.

**Worked in:** E12S04 “Practice Q23: emissions per useful energy” (≈2:43 in the draft)

### Q24. Evidence-based sustainability with an honest limit (6 marks)

**Question.** Per kilogram of ethanol produced: Process A uses edible crop feedstock, 8 MJ of natural-gas heat and 12 L of freshwater, and vents its fermentation CO₂. Process B uses food-processing waste, 10 MJ of electricity (60% renewable) and 20 L of freshwater, and its captured fermentation CO₂ is used in another manufacturing process. Both are technically viable.

**a.** Compare the processes using one relevant green chemistry or circular-economy consideration. *[2]*

> Feedstock: B uses waste rather than an edible crop, reducing competition with food and land use (renewable feedstock from waste; circular use).

**b.** Compare the processes using a second, different consideration. *[2]*

> Resources: A uses less listed energy (8 vs 10 MJ) and less freshwater (12 vs 20 L) per kg.

**c.** Identify one tradeoff, or one limit of the data. *[1]*

> Tradeoff: B's feedstock/CO₂ advantages versus A's lower energy and water use. CO₂ use need not mean permanent storage.

**d.** Recommend a process under explicitly stated priorities. Can the data establish which has lower total lifecycle greenhouse emissions? *[1]*

> Either recommendation is defensible if it follows from stated priorities (e.g. B if avoiding food competition is the priority). The data cannot establish total lifecycle emissions: emission factors for the natural gas and the 40% non-renewable electricity, and broader lifecycle data, are missing.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | a: first supported comparison (feedstock; circular use) |
| 2 | b: second supported comparison (listed energy and water) |
| 1 | c: a trade-off or data limit |
| 1 | d: recommendation consistent with stated priorities |
| **6** | **total** |

**Trap.** Assuming 'bio' or 'renewable electricity' makes a process superior on every criterion.

**Worked in:** E12S08 “Practice Q24: build an evidence-based answer” (≈7:41 in the draft)

## Episode 13: Exam workshop A: fuels and combustion

### Q25. Integrated workshop: a mixed-gas water heater (15 marks)

**Question.** A purified digester gas contains 90.0% CH₄ and 10.0% CO₂ by volume. An idealised heater receives 6.20 L of the fuel mixture and 60.0 L of air, both measured at SLC; air contains 21.0% O₂ by volume. Methane burns completely. Use M(CH₄) = 16.0 g mol⁻¹ and ΔH<sub>c</sub>(CH₄) = −890 kJ mol⁻¹ for formation of liquid water. The heater raises 800.0 g of water from 17.0 °C to 57.0 °C. Assume the fuel-stream CO₂ passes through unchanged and all methane burns.

**a.** Determine the total fuel-mixture amount, the methane amount and the available oxygen. *[3]*

> n(mixture) = 6.20 ÷ 24.8 = 0.250 mol; n(CH₄) = 0.900 × 0.250 = 0.225 mol; n(O₂) = 0.210 × 60.0 ÷ 24.8 = 0.50806 mol

**b.** Write the thermochemical equation for the combustion, with states. *[2]*

> CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)     ΔH = −890 kJ

**c.** Calculate the mass of excess O₂ remaining. *[2]*

> Required O₂ = 0.450 mol; remaining 0.05806 mol × 32.0 = 1.86 g

**d.** Calculate the energy released by the fuel and the heat gained by the water. *[2]*

> 0.225 × 890 = 200.25 kJ released; q(water) = 800.0 × 4.18 × 40.0 = 133 760 J = 133.76 kJ

**e.** Calculate the useful efficiency, and explain why an inverse-efficiency operation would be wrong here. *[3]*

> 133.76 ÷ 200.25 × 100% = 66.8%. Both input and useful output are known, so efficiency is output ÷ input; dividing by an efficiency is only for finding a required input from a target output.

**f.** Determine the total dry CO₂ volume at SLC after isolation. *[2]*

> CO₂ = 0.225 (new) + 0.0250 (inlet) = 0.250 mol × 24.8 = 6.20 L

**g.** Explain the source-based reason for calling this methane renewable. *[1]*

> It comes from recently grown biomass that is replenished on a short (human) timescale; the methane molecule itself is identical.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 3 | a: mixture amount, CH₄ amount, O₂ amount |
| 2 | b: equation with states; ΔH |
| 2 | c: O₂ required; excess mass |
| 2 | d: energy released; heat gained |
| 3 | e: ratio set up; value; direction explained |
| 2 | f: new + inlet CO₂; volume |
| 1 | g: source-based reason |
| **15** | **total** |

**Trap.** Mixture vs reactive component; air vs oxygen; new vs inlet CO₂; energy units; efficiency direction.

**Worked in:** E13S03 “Q25: attempt it first” (≈2:07 in the draft); E13S04 “Q25: read and annotate” (≈3:40 in the draft); E13S05 “Q25: plan the methods” (≈5:03 in the draft); E13S06 “Q25 parts a to c: amounts, equation and excess oxygen” (≈6:00 in the draft); E13S08 “Q25 parts d and e: energy and efficiency” (≈8:32 in the draft); E13S09 “Q25 parts f and g: carbon dioxide and the source” (≈10:07 in the draft)

### Q26. A fuel ranking that needs a specified basis (10 marks)

**Question.** Methanol: M = 32.0 g mol⁻¹, ΔH<sub>c</sub> = −726 kJ mol⁻¹. Ethanol: M = 46.0 g mol⁻¹, ΔH<sub>c</sub> = −1370 kJ mol⁻¹. Complete combustion produces 1 mol and 2 mol CO₂ per mole of fuel respectively. A methanol heater has 25.0% useful-energy efficiency and an ethanol heater 40.0%.

**a.** Calculate the energy released per gram for each fuel. *[2]*

> Methanol 726 ÷ 32.0 = 22.7 kJ g⁻¹; ethanol 1370 ÷ 46.0 = 29.8 kJ g⁻¹

**b.** Calculate the direct-combustion CO₂, in grams per useful kJ, for each heater. *[4]*

> Methanol: 44.0 g ÷ (726 × 0.250) kJ = 0.242 g kJ⁻¹; ethanol: 88.0 g ÷ (1370 × 0.400) kJ = 0.161 g kJ⁻¹

**c.** Explain why 'both contain an O–H bond, so they release equal energy per gram' is wrong. *[2]*

> Energy released depends on all the bonds broken and formed in the whole reaction, and per-gram values also depend on molar mass; one shared bond does not determine it.

**d.** Explain whether these results establish which fuel has lower lifecycle emissions. *[2]*

> No. Direct combustion CO₂ omits feedstock production, processing and transport; lifecycle data are needed.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | a: energy per gram for each fuel |
| 4 | b: useful energy and g CO₂ per useful kJ, each fuel |
| 2 | c: whole-reaction bonds; molar mass |
| 2 | d: no; lifecycle stages missing |
| **10** | **total** |

**Trap.** Per mole vs per gram; CO₂ per mole vs per useful energy; bond-breaking misconception; unsupported lifecycle claim.

**Worked in:** E13S12 “Q26: attempt it first” (≈13:45 in the draft); E13S13 “Q26 parts a and b: per gram and per useful kilojoule” (≈14:57 in the draft); E13S15 “Q26 parts c and d: explaining and limiting claims” (≈18:04 in the draft)

## Episode 14: Exam workshop B: calorimetry and data evaluation

### Q27. Integrated workshop: calibration, a graph and neutralisation (14 marks)

**Question.** A calorimeter is electrically calibrated with 125.0 g of water using 5.00 V and 1.20 A for 300 s, giving a 3.00 °C rise. Assume this CF also applies accurately to the reaction mixture below. 50.0 mL of 1.00 mol L⁻¹ HCl is mixed with 75.0 mL of 0.800 mol L⁻¹ NaOH. The initial baseline is 20.0 °C and mixing starts at t = 60 s. Post-reaction cooling measurements: 120 s, 24.7 °C; 180 s, 24.6 °C; 240 s, 24.5 °C; 300 s, 24.4 °C. Assume a linear cooling trend is suitable for the correction and neutralisation is complete.

**a.** Calculate the calibration energy and CF, and check CF against the water-only heat capacity. *[3]*

> E = 5.00 × 1.20 × 300 = 1800 J; CF = 1800 ÷ 3.00 = 600 J °C⁻¹; water-only = 125.0 × 4.18 = 522.5 J °C⁻¹ < 600, so CF is physically plausible.

**b.** Identify the available amounts and the limiting reactant. *[2]*

> n(HCl) = 0.0500 mol; n(NaOH) = 0.0600 mol; 1 : 1, so HCl is limiting.

**c.** Determine the corrected temperature rise. *[2]*

> Slope −0.1 °C per 60 s; extrapolated T(60 s) = 24.8 °C; corrected rise = 4.8 °C

**d.** Calculate the reaction heat and the experimental molar enthalpy per mole of water. *[3]*

> q = 600 × 4.8 = 2880 J; ΔH = −2.880 kJ ÷ 0.0500 mol = −57.6 ≈ −58 kJ mol⁻¹

**e.** Explain what repeatability would and would not establish about this result. *[2]*

> Close repeats show precision/repeatability, not accuracy; a shared systematic error (e.g. a wrong CF or unaccounted heat loss) would remain.

**f.** Predict whether doubling the NaOH concentration (same volume) would double the heat released, assuming CF and other conditions are unchanged. *[2]*

> No. HCl remains limiting at 0.0500 mol, so the same amount of water forms and the same heat is released.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 3 | a: energy, CF, plausibility check |
| 2 | b: amounts; limiting reactant |
| 2 | c: extrapolation; corrected rise |
| 3 | d: heat; ÷ limiting amount; sign and units |
| 2 | e: precise, not necessarily accurate |
| 2 | f: acid still limiting; same heat |
| **14** | **total** |

**Trap.** Seconds, solution volumes, wrong denominator, observed vs corrected peak, precision vs accuracy, excess vs reacted.

**Worked in:** E14S02 “Q27: attempt it first” (≈1:25 in the draft); E14S03 “Q27: read and annotate” (≈2:55 in the draft); E14S04 “Q27: plan the methods” (≈4:11 in the draft); E14S05 “Q27 part a: calibration” (≈4:58 in the draft); E14S06 “Q27 part b: the limiting reactant” (≈5:49 in the draft); E14S07 “Q27 part c: correcting the temperature rise” (≈6:36 in the draft); E14S08 “Q27 part d: molar enthalpy” (≈7:33 in the draft); E14S09 “Wrong solutions for Q27” (≈8:28 in the draft); E14S10 “Q27 parts e and f: evidence and prediction” (≈9:28 in the draft)

### Q28. A hand-warmer claim distorted by the wrong calibration (12 marks)

**Question.** An idealised hand-warmer powder contains a hypothetical active solid X (M = 80.0 g mol⁻¹) and inert filler. Dissolving X completely releases 24.0 kJ per mole of X; the filler has negligible thermal effect. A 4.00 g powder sample is tested in a setup correctly calibrated for this experiment (CF = 300 J °C⁻¹) and produces a 3.20 °C rise. Assume complete dissolution and accounted-for heat transfer. The manufacturer claims 95.0% X by mass.

**a.** Calculate the heat gained by the calorimeter. *[2]*

> q = 300 × 3.20 = 960 J

**b.** Determine the amount of X, the mass of X and the mass percentage of X. *[4]*

> n(X) = 0.960 kJ ÷ 24.0 kJ mol⁻¹ = 0.0400 mol; m(X) = 0.0400 × 80.0 = 3.20 g; 3.20 ÷ 4.00 × 100% = 80.0%

**c.** Assess the manufacturer's claim. *[1]*

> 80.0% < 95.0%: the claim is not supported by this modelled measurement.

**d.** Recalculate the percentage if a spreadsheet mistakenly uses CF = 360 J °C⁻¹ from a different setup, and explain the implication. *[2]*

> q = 360 × 3.20 = 1152 J → 0.0480 mol → 3.84 g → 96.0%: the wrong CF makes the claim appear supported.

**e.** State whether repeating with the wrong CF resolves the bias. *[1]*

> No. Repeating with the same wrong CF reproduces the same bias.

**f.** Explain how absorbed moisture could lower the active fraction in a subsequently weighed 4.00 g sample (assume negligible change to CF and no extra thermal effect from moisture). *[2]*

> Water absorbed by the powder takes up part of the fixed 4.00 g mass, so less X is present; less heat is released and the rise is smaller, lowering the calculated percentage of X.

**Indicative marks**

| Marks | Observable step |
|---|---|
| 2 | a: q = CF × ΔT = 960 J |
| 4 | b: kJ conversion; n(X); m(X); % X |
| 1 | c: 80.0% does not support 95.0% |
| 2 | d: 96.0% with CF = 360; bias direction |
| 1 | e: repeating keeps the bias |
| 2 | f: less active mass; lower result |
| **12** | **total** |

**Trap.** Claim vs evidence, calibration-error direction, precise but biased results, active mass vs total sample mass.

**Worked in:** E14S12 “Q28: attempt it first” (≈11:41 in the draft); E14S13 “Q28 parts a to c: testing the claim” (≈12:55 in the draft); E14S14 “Q28 parts d and e: a calibration error” (≈14:01 in the draft); E14S15 “Q28 part f: moisture” (≈15:02 in the draft)
