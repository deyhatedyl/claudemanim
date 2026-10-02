"""
Anchor question bank Q01-Q28 (original practice material written for this series;
not official VCAA questions or marking schemes).

Single source of truth for:
  * questions/worksheet.md         (prompts only, no answers)              -> tools/build_docs.py
  * solutions/worked_solutions.md  (working per part, marks, traps)        -> tools/build_docs.py
  * on-screen question cards in the episodes (shared/components.question_card)

Wording has been lightly edited from the brief for clarity and to split each set into
lettered parts with indicative marks; no data value has been changed. Numerical targets are
verified independently in checks/verify_anchors.py.
"""

SHARED_DATA = (
    "Unless a question says otherwise: SLC = 25 °C and 100 kPa; molar volume of a gas at SLC, "
    "V_m = 24.8 L mol⁻¹; specific heat capacity of water, c = 4.18 J g⁻¹ °C⁻¹; "
    "relative atomic masses C = 12.0, H = 1.0, O = 16.0. Food energy factors: carbohydrate "
    "16 kJ g⁻¹, protein 17 kJ g⁻¹, fat 37 kJ g⁻¹. Use molar masses supplied in a question."
)

# Each question: id, episode, title, stem, parts [(label, text, marks)], answers [str], trap
BANK = [
    dict(
        id="Q01", episode=1, title="Two different ways to obtain an amount of substance",
        stem="A 0.345 g sample of ethanol has M = 46.0 g mol⁻¹. A separate gas sample occupies 186 mL at SLC.",
        parts=[
            ("a", "Calculate the amount, in mol, of ethanol in the sample.", 1),
            ("b", "Calculate the amount, in mol, of gas in the gas sample.", 2),
            ("c", "Explain whether equal amounts in mol would imply equal masses.", 1),
        ],
        answers=[
            "a. n(ethanol) = 0.345 g ÷ 46.0 g mol⁻¹ = 0.00750 mol",
            "b. V = 186 mL = 0.186 L; n = 0.186 L ÷ 24.8 L mol⁻¹ = 0.00750 mol",
            "c. Equal amounts mean equal numbers of particles, not equal masses: mass also depends on "
            "molar mass, which can differ. The gas's identity and molar mass are not given, so its mass "
            "cannot be found.",
        ],
        trap="Using 186 (mL) as if it were litres, or treating mol and grams as interchangeable.",
    ),
    dict(
        id="Q02", episode=1, title="Conversions inside a realistic data sheet",
        stem="A data sheet lists 0.0850 m³ of dry air at SLC, 20.9% oxygen by volume, a heating duration "
             "of 0.150 h and an energy input of 7.20 × 10⁴ J.",
        parts=[
            ("a", "Express the air volume in L, the heating time in s and the energy input in kJ.", 3),
            ("b", "Calculate the amount, in mol, of oxygen in the air sample.", 2),
        ],
        answers=[
            "a. 0.0850 m³ × 1000 L m⁻³ = 85.0 L; 0.150 h × 3600 s h⁻¹ = 540 s; 7.20 × 10⁴ J ÷ 1000 = 72.0 kJ",
            "b. V(O₂) = 0.209 × 85.0 L = 17.765 L; n(O₂) = 17.765 L ÷ 24.8 L mol⁻¹ = 0.7163… ≈ 0.716 mol",
        ],
        trap="Treating the whole air volume as oxygen, or treating m³ as mL.",
    ),
    dict(
        id="Q03", episode=2, title="A bond-energy ledger",
        stem="For H₂(g) + Cl₂(g) → 2HCl(g), use average bond enthalpies H–H 436, Cl–Cl 243 and "
             "H–Cl 431 kJ mol⁻¹.",
        parts=[
            ("a", "Estimate the enthalpy change for the equation as written.", 3),
            ("b", "Explain why the reaction is exothermic.", 1),
        ],
        answers=[
            "a. Energy absorbed breaking bonds = 436 + 243 = 679 kJ; energy released forming bonds = "
            "2 × 431 = 862 kJ; ΔH ≈ 679 − 862 = −183 kJ (per mole of reaction as written; an estimate "
            "because average bond enthalpies are used).",
            "b. More energy is released when the 2 H–Cl bonds form than is absorbed when the H–H and "
            "Cl–Cl bonds break, so there is a net transfer of energy from the system to the surroundings.",
        ],
        trap="Adding all bond energies together, or saying that breaking bonds releases energy.",
    ),
    dict(
        id="Q04", episode=2, title="Endothermic does not mean energy disappears",
        stem="An idealised dissolution absorbs 18.0 kJ per mole of solute. In an insulated calorimeter, "
             "0.0250 mol of solute dissolves completely.",
        parts=[
            ("a", "State the energy change of the reacting system.", 1),
            ("b", "State the energy change of the surrounding calorimeter.", 1),
            ("c", "State whether the measured temperature rises or falls.", 1),
        ],
        answers=[
            "a. q(system) = +18.0 kJ mol⁻¹ × 0.0250 mol = +0.450 kJ",
            "b. q(calorimeter) = −0.450 kJ",
            "c. The temperature falls (energy leaves the calorimeter contents and enters the dissolving system).",
        ],
        trap="Giving the system and the calorimeter the same sign.",
    ),
    dict(
        id="Q05", episode=3, title="Equation coefficients and water's state",
        stem="2H₂(g) + O₂(g) → 2H₂O(l)     ΔH = −572 kJ",
        parts=[
            ("a", "Write the thermochemical equation for the decomposition of 1 mol of liquid water, with its ΔH.", 2),
            ("b", "Calculate the energy released by the complete reaction of 0.750 mol of H₂.", 2),
            ("c", "Explain whether −572 kJ can be used unchanged if the product in the original equation is H₂O(g).", 1),
        ],
        answers=[
            "a. H₂O(l) → H₂(g) + ½O₂(g)     ΔH = +286 kJ",
            "b. 572 kJ is released per 2 mol H₂, i.e. 286 kJ per mol H₂; 0.750 mol × 286 kJ mol⁻¹ = 214.5 kJ ≈ 215 kJ released",
            "c. No. Gaseous water has higher enthalpy than liquid water (vaporisation absorbs energy), so "
            "forming H₂O(g) releases less energy; a different ΔH is required.",
        ],
        trap="Treating −572 kJ as per mole of H₂, or ignoring physical states.",
    ),
    dict(
        id="Q06", episode=3, title="Read the vertical distances, not the absolute heights",
        stem="An energy profile uses a common arbitrary enthalpy reference, in kJ per mole of reaction. "
             "Reactants are at 80, products at 25 and the uncatalysed maximum at 150. A catalysed maximum is at 110.",
        parts=[
            ("a", "Find the forward activation energy.", 1),
            ("b", "Find the reverse activation energy.", 1),
            ("c", "Find ΔH.", 1),
            ("d", "Find the catalysed forward activation energy.", 1),
            ("e", "Explain whether the catalyst changes the heat released by the same amount reacting.", 1),
        ],
        answers=[
            "a. 150 − 80 = 70 kJ mol⁻¹", "b. 150 − 25 = 125 kJ mol⁻¹", "c. 25 − 80 = −55 kJ mol⁻¹",
            "d. 110 − 80 = 30 kJ mol⁻¹",
            "e. No. The reactant and product enthalpies are unchanged, so ΔH and the heat released for the "
            "same amount reacting are unchanged; only the pathway's barrier is lower.",
        ],
        trap="Reading 150 as Ea, or saying a lower barrier changes ΔH.",
    ),
    dict(
        id="Q07", episode=4, title="Fermentation yield and its coproduct",
        stem="A food-waste hydrolysate contains 270.0 g glucose (M = 180.0 g mol⁻¹). Assume fermentation "
             "produces only ethanol and carbon dioxide and achieves 78.0% of the theoretical conversion to "
             "these products.",
        parts=[
            ("a", "Write the balanced equation for the fermentation, with states.", 1),
            ("b", "Calculate the masses of ethanol and of carbon dioxide formed.", 4),
            ("c", "Give one role of the subsequent distillation.", 1),
        ],
        answers=[
            "a. C₆H₁₂O₆(aq) → 2C₂H₅OH(aq) + 2CO₂(g)",
            "b. n(glucose) = 1.50 mol; theoretical ethanol = CO₂ = 3.00 mol; actual = 0.780 × 3.00 = 2.34 mol "
            "each; m(ethanol) = 2.34 × 46.0 = 107.64 ≈ 108 g; m(CO₂) = 2.34 × 44.0 = 102.96 ≈ 103 g",
            "c. Distillation separates and concentrates ethanol from the aqueous fermentation mixture, using "
            "the difference in volatility (boiling point) of ethanol and water.",
        ],
        trap="Using a 1 : 1 glucose : ethanol ratio, applying the 78.0% twice, or calling distillation fermentation.",
    ),
    dict(
        id="Q08", episode=4, title="Same molecule, different source",
        stem="Two purified fuels each contain only CH₄. One is obtained from geological natural-gas reserves; "
             "the other from anaerobic digestion of recently grown plant waste.",
        parts=[
            ("a", "Under the same conditions, compare the energy released and the CO₂ produced per mole burned.", 1),
            ("b", "Classify each source as renewable or non-renewable, with a reason.", 2),
            ("c", "Explain why renewability alone does not prove overall sustainability.", 1),
        ],
        answers=[
            "a. Identical: the same molecule undergoing the same reaction releases the same energy and forms "
            "1 mol CO₂ per mol CH₄.",
            "b. Natural gas is non-renewable: it formed over millions of years and is used far faster than it "
            "is replaced. Biomethane is renewable: its plant feedstock regrows on a human timescale.",
            "c. Sustainability needs the whole lifecycle, e.g. methane leakage from digesters and pipelines "
            "(a potent greenhouse gas), energy used in processing, land and water use.",
        ],
        trap="Claiming that biomethane produces no CO₂ when burned.",
    ),
    dict(
        id="Q09", episode=5, title="Food label with a serving and unit trap",
        stem="A 90 g packet contains three 30.0 g servings. Per 100 g, the product contains 48.0 g "
             "carbohydrate, 12.0 g protein and 18.0 g fat.",
        parts=[
            ("a", "Calculate the energy per 100 g, in kJ, using the supplied food factors.", 2),
            ("b", "Calculate the energy in one serving, in kJ.", 1),
            ("c", "Express the energy in one serving in J.", 1),
        ],
        answers=[
            "a. 48.0 × 16 + 12.0 × 17 + 18.0 × 37 = 768 + 204 + 666 = 1638 kJ per 100 g",
            "b. 1638 kJ × (30.0 g ÷ 100 g) = 491.4 ≈ 491 kJ",
            "c. 491.4 kJ × 1000 J kJ⁻¹ = 4.91 × 10⁵ J",
        ],
        trap="Using the whole packet, or reporting the kJ value as J.",
    ),
    dict(
        id="Q10", episode=5, title="Which food has more energy depends on the comparison",
        stem="Idealised label values per 100 g: Food A contains 50 g carbohydrate, 10 g protein and 12 g "
             "fat; Food B contains 35 g carbohydrate, 20 g protein and 15 g fat. An A serving is 80 g and "
             "a B serving is 50 g.",
        parts=[
            ("a", "Calculate the energy per 100 g of each food.", 2),
            ("b", "Calculate the energy in one serving of each food.", 2),
            ("c", "State which food has more energy per 100 g and which serving contains more energy.", 1),
        ],
        answers=[
            "a. A: 800 + 170 + 444 = 1414 kJ per 100 g; B: 560 + 340 + 555 = 1455 kJ per 100 g",
            "b. A: 1414 × 0.80 = 1131.2 ≈ 1131 kJ; B: 1455 × 0.50 = 727.5 ≈ 728 kJ",
            "c. B has more energy per 100 g; the A serving contains more energy. The ranking depends on the basis.",
        ],
        trap="Comparing unmatched portion sizes without stating the basis.",
    ),
    dict(
        id="Q11", episode=6, title="Incomplete combustion with enough information to balance it",
        stem="At high temperature, 1.00 mol of ethanol (supplied as a liquid) reacts with 2.50 mol O₂. All "
             "of the ethanol and oxygen react. The only products are CO₂(g), CO(g) and H₂O(g); no solid "
             "carbon forms.",
        parts=[
            ("a", "Determine the amount of water formed.", 1),
            ("b", "Determine the amounts of CO₂ and CO formed.", 2),
            ("c", "Write the balanced equation.", 1),
            ("d", "Compare this oxygen requirement with that for complete combustion of 1 mol ethanol.", 1),
        ],
        answers=[
            "a. H: 6 H atoms → 3.00 mol H₂O",
            "b. C: x + y = 2; O: 1 + 5 = 2x + y + 3 → x = 1.00 mol CO₂, y = 1.00 mol CO",
            "c. C₂H₅OH(l) + 2½O₂(g) → CO₂(g) + CO(g) + 3H₂O(g)  (or ×2: 2C₂H₅OH + 5O₂ → 2CO₂ + 2CO + 6H₂O)",
            "d. Complete combustion needs 3.00 mol O₂ per mol ethanol; this reaction uses only 2.50 mol.",
        ],
        trap="Forgetting the O atom in ethanol, or assuming incomplete combustion always gives only CO.",
    ),
    dict(
        id="Q12", episode=6, title="Hot exhaust versus cooled dry gas",
        stem="Complete combustion of 0.250 mol CH₄ occurs in excess oxygen at 600 °C. The exhaust is then "
             "cooled, liquid water is removed, and the CO₂ is isolated and measured at SLC. Assume complete collection.",
        parts=[
            ("a", "State the amounts of CO₂ and H₂O formed.", 1),
            ("b", "Calculate the masses of CO₂ and of water vapour newly formed in the hot exhaust.", 2),
            ("c", "Calculate the total mass of these two greenhouse gases newly formed in the hot stream.", 1),
            ("d", "Calculate the volume of the isolated dry CO₂ at SLC.", 1),
        ],
        answers=[
            "a. CH₄ + 2O₂ → CO₂ + 2H₂O: 0.250 mol CO₂ and 0.500 mol H₂O",
            "b. m(CO₂) = 0.250 × 44.0 = 11.0 g; m(H₂O) = 0.500 × 18.0 = 9.00 g",
            "c. 20.0 g",
            "d. V = 0.250 mol × 24.8 L mol⁻¹ = 6.20 L",
        ],
        trap="Excluding hot water vapour, or applying the SLC molar volume to gas at 600 °C.",
    ),
    dict(
        id="Q13", episode=7, title="Excess means what is left after reaction",
        stem="An idealised calculation starts with 0.400 mol ethanol and 32.0 g O₂. Assume only complete "
             "combustion of the portion of ethanol that reacts, with unreacted excess left over. Use "
             "M(O₂) = 32.0 g mol⁻¹, M(ethanol) = 46.0 g mol⁻¹ and ΔH_c(ethanol) = −1370 kJ mol⁻¹.",
        parts=[
            ("a", "Identify the limiting reactant, with working.", 2),
            ("b", "Calculate the mass of excess ethanol remaining.", 2),
            ("c", "Calculate the mass of CO₂ produced.", 1),
            ("d", "Calculate the energy released.", 1),
        ],
        answers=[
            "a. n(O₂) = 1.00 mol. C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O. 0.400 mol ethanol would need 1.20 mol O₂ > "
            "1.00 mol, so O₂ is limiting (n/coefficient: O₂ 0.333 < ethanol 0.400).",
            "b. Ethanol used = 1.00 ÷ 3 = 0.3333 mol; remaining = 0.0667 mol × 46.0 = 3.07 g",
            "c. CO₂ = 2 × 0.3333 = 0.6667 mol × 44.0 = 29.3 g",
            "d. 0.3333 mol × 1370 kJ mol⁻¹ = 456.67 ≈ 457 kJ released",
        ],
        trap="Taking the smaller raw mole number as limiting, or reporting the starting amount as the amount remaining.",
    ),
    dict(
        id="Q14", episode=7, title="A fuel stream already containing carbon dioxide",
        stem="At SLC, 12.4 L of an ideal gas mixture containing 80.0% CH₄ and 20.0% CO₂ by volume is "
             "supplied with 90.0 L of air containing 21.0% O₂ by volume. Treat the other air components "
             "as inert. Assume complete combustion of only the methane that can react, with excess methane "
             "left unreacted. Use M(CH₄) = 16.0 g mol⁻¹ and ΔH = −890 kJ mol⁻¹ for methane combustion to liquid water.",
        parts=[
            ("a", "Calculate the initial amounts of CH₄ and O₂.", 2),
            ("b", "Identify the limiting reactant.", 1),
            ("c", "Calculate the mass of methane remaining.", 2),
            ("d", "Calculate the volume at SLC of newly formed CO₂.", 1),
            ("e", "Calculate the total CO₂ volume at SLC, including the CO₂ in the inlet stream.", 1),
            ("f", "Calculate the energy released.", 1),
        ],
        answers=[
            "a. n(mixture) = 0.500 mol; n(CH₄) = 0.400 mol; V(O₂) = 18.9 L; n(O₂) = 0.76210 mol",
            "b. CH₄ + 2O₂ → CO₂ + 2H₂O. 0.400 mol CH₄ needs 0.800 mol O₂ > 0.762 mol, so O₂ is limiting.",
            "c. CH₄ used = 0.38105 mol; remaining = 0.01895 mol × 16.0 = 0.303 g",
            "d. 0.38105 mol × 24.8 = 9.45 L",
            "e. Inlet CO₂ = 0.100 mol = 2.48 L; total = 11.93 ≈ 11.9 L",
            "f. 0.38105 mol × 890 kJ mol⁻¹ = 339.1 ≈ 339 kJ",
        ],
        trap="Counting all of the fuel-stream gas as methane, or treating all measured CO₂ as newly formed.",
    ),
    dict(
        id="Q15", episode=8, title="A measured fuel mass loss",
        stem="An ethanol burner has a mass of 102.640 g before heating and 101.720 g afterwards. It heats "
             "250.0 g of water from 19.8 °C to 37.0 °C. Assume the mass lost is ethanol combusted. Use "
             "M = 46.0 g mol⁻¹ and ΔH_c = −1370 kJ mol⁻¹.",
        parts=[
            ("a", "Calculate the mass and amount of ethanol burned.", 2),
            ("b", "Calculate the energy released by the ethanol.", 1),
            ("c", "Calculate the heat gained by the water.", 2),
            ("d", "Calculate the useful-energy efficiency for heating the water.", 1),
        ],
        answers=[
            "a. 0.920 g; 0.920 ÷ 46.0 = 0.0200 mol",
            "b. 0.0200 × 1370 = 27.4 kJ",
            "c. ΔT = 17.2 °C; q = 250.0 × 4.18 × 17.2 = 17 974 J = 17.974 ≈ 18.0 kJ",
            "d. 17.974 ÷ 27.4 × 100% = 65.6%",
        ],
        trap="Using the full burner mass, using the fuel mass in q = mcΔT, or mixing J and kJ.",
    ),
    dict(
        id="Q16", episode=8, title="Work backwards from useful heat",
        stem="A heater must warm 180.0 g of water from 18.0 °C to 78.0 °C. Its useful-energy efficiency is "
             "45.0%, and the supplied fuel energy value is 29.8 kJ g⁻¹.",
        parts=[
            ("a", "Calculate the useful heat required.", 2),
            ("b", "Calculate the chemical energy input required.", 1),
            ("c", "Calculate the minimum fuel mass required under this model.", 1),
            ("d", "A student instead multiplies the water's required heat by 0.450 before dividing by 29.8. Explain the error.", 1),
        ],
        answers=[
            "a. q = 180.0 × 4.18 × 60.0 = 45 144 J = 45.144 kJ",
            "b. 45.144 ÷ 0.450 = 100.32 kJ",
            "c. 100.32 ÷ 29.8 = 3.366 ≈ 3.37 g",
            "d. Multiplying gives 0.682 g, less than the 1.515 g needed even at 100% efficiency, which is "
            "impossible: a less efficient heater needs more input, so divide by the efficiency.",
        ],
        trap="Using the efficiency in the wrong direction.",
    ),
    dict(
        id="Q17", episode=9, title="Separate water heat capacity from apparatus heat capacity",
        stem="A calorimeter containing 120.0 g of water is electrically heated at 6.00 V and 1.50 A for "
             "240 s. Its temperature rises by 4.00 °C. Assume negligible heat loss during calibration.",
        parts=[
            ("a", "Determine the calibration factor.", 2),
            ("b", "Determine the apparatus contribution to the heat capacity.", 1),
            ("c", "A later matched experiment produces a 5.60 °C rise. Calculate the heat gained by the calorimeter.", 1),
            ("d", "Estimate the calibration factor if the water mass is increased to 150.0 g with identical "
                  "apparatus, assuming additive, constant heat capacities.", 2),
        ],
        answers=[
            "a. E = 6.00 × 1.50 × 240 = 2160 J; CF = 2160 ÷ 4.00 = 540 J °C⁻¹",
            "b. Water: 120.0 × 4.18 = 501.6 J °C⁻¹; apparatus = 540 − 501.6 = 38.4 J °C⁻¹",
            "c. q = 540 × 5.60 = 3024 J ≈ 3.02 kJ",
            "d. 150.0 × 4.18 + 38.4 = 627.0 + 38.4 = 665.4 ≈ 665 J °C⁻¹",
        ],
        trap="Using mcΔT for the water as if it included the apparatus, or keeping CF unchanged after changing the contents.",
    ),
    dict(
        id="Q18", episode=9, title="An impossible calibration factor and an appealing wrong explanation",
        stem="A setup contains 100.0 g of water and a cup/probe of positive heat capacity. A student reports "
             "CF = 360 J °C⁻¹ from electrical calibration and argues that heat loss explains the low value.",
        parts=[
            ("a", "Assess the reported CF under the ordinary calibration model.", 2),
            ("b", "Assess the heat-loss explanation.", 1),
            ("c", "Identify one measurement error that could make the reported CF too low.", 1),
        ],
        answers=[
            "a. The water alone needs 100.0 × 4.18 = 418 J °C⁻¹; with positive apparatus heat capacity, "
            "CF must exceed 418, so 360 is inconsistent with the setup.",
            "b. Heat loss reduces the observed ΔT, so CF = E/ΔT becomes larger, not smaller; it cannot explain a low CF.",
            "c. An overestimated temperature rise, or an underestimated electrical energy (e.g. time, current "
            "or voltage recorded too low).",
        ],
        trap="Giving 'heat loss' as a universal explanation without following the formula.",
    ),
    dict(
        id="Q19", episode=10, title="A solution calorimetry denominator you must justify",
        stem="75.0 mL of 0.800 mol L⁻¹ HCl is mixed with 50.0 mL of 0.900 mol L⁻¹ NaOH. The setup has been "
             "correctly calibrated for these conditions: CF = 590 J °C⁻¹. Both solutions begin at 20.00 °C "
             "and the final temperature is 24.30 °C. Assume complete neutralisation, with the measured rise "
             "attributable to it.",
        parts=[
            ("a", "Calculate the amounts of HCl and NaOH.", 2),
            ("b", "Identify the limiting reactant and the amount of acid left over.", 2),
            ("c", "Calculate the heat gained by the calorimeter.", 2),
            ("d", "Calculate the molar enthalpy change per mole of water formed.", 2),
        ],
        answers=[
            "a. n(HCl) = 0.0750 × 0.800 = 0.0600 mol; n(NaOH) = 0.0500 × 0.900 = 0.0450 mol",
            "b. HCl + NaOH → NaCl + H₂O (1 : 1): NaOH limiting; HCl left = 0.0150 mol",
            "c. ΔT = 4.30 °C; q = 590 × 4.30 = 2537 J",
            "d. n(H₂O) = 0.0450 mol; ΔH = −2.537 kJ ÷ 0.0450 mol = −56.4 kJ mol⁻¹",
        ],
        trap="Dividing by the acid initially supplied, by total moles of solution, or by the total volume.",
    ),
    dict(
        id="Q20", episode=10, title="One mole of reagent is not always one mole of reaction",
        stem="2NaOH(aq) + H₂SO₄(aq) → Na₂SO₄(aq) + 2H₂O(l)     ΔH = −114 kJ for the equation as written. "
             "0.0300 mol NaOH and 0.0200 mol H₂SO₄ are mixed in a correctly calibrated setup with "
             "CF = 480 J °C⁻¹. The initial temperature is 21.0 °C. Assume complete reaction and complete heat capture.",
        parts=[
            ("a", "Identify the limiting reactant using the mole ratio.", 1),
            ("b", "Determine the reaction extent (moles of reaction as written).", 1),
            ("c", "Calculate the heat released.", 1),
            ("d", "Calculate the temperature rise.", 1),
            ("e", "Calculate the final temperature.", 1),
            ("f", "Calculate the amount of H₂SO₄ remaining.", 1),
        ],
        answers=[
            "a. n/coefficient: NaOH 0.0300 ÷ 2 = 0.0150; H₂SO₄ 0.0200 ÷ 1 = 0.0200 → NaOH limiting",
            "b. 0.0150 mol of reaction",
            "c. 0.0150 × 114 = 1.710 kJ",
            "d. 1710 J ÷ 480 J °C⁻¹ = 3.5625 °C",
            "e. 21.0 + 3.5625 = 24.5625 ≈ 24.6 °C",
            "f. 0.0200 − 0.0150 = 0.00500 mol",
        ],
        trap="Multiplying 0.0300 mol directly by 114 kJ, or reporting the rise as the final temperature.",
    ),
    dict(
        id="Q21", episode=11, title="Recover the appropriate temperature rise from a graph",
        stem="Mixing begins at t = 120 s. Pre-mixing temperatures at 0, 60 and 120 s are 21.0 °C. Subsequent "
             "measured temperatures: 135 s, 23.0 °C; 150 s, 25.0 °C; 165 s, 26.0 °C; 180 s, 26.1 °C; "
             "240 s, 25.9 °C; 300 s, 25.7 °C; 360 s, 25.5 °C. CF = 650 J °C⁻¹.",
        parts=[
            ("a", "Use the linear 180–360 s cooling trend to estimate the temperature at the mixing time.", 2),
            ("b", "Calculate the corrected temperature rise.", 1),
            ("c", "Calculate the corrected heat gained by the calorimeter.", 1),
            ("d", "Compare this with the heat calculated from the highest observed temperature.", 1),
        ],
        answers=[
            "a. Slope = (25.5 − 26.1) ÷ (360 − 180) = −0.00333 °C s⁻¹; T(120 s) = 26.1 + 0.00333 × 60 = 26.3 °C",
            "b. 26.3 − 21.0 = 5.3 °C",
            "c. 650 × 5.3 = 3445 J ≈ 3.4 kJ (two significant figures, graph estimate)",
            "d. Highest observed 26.1 °C gives 5.1 °C and 3315 J ≈ 3.3 kJ, an underestimate because cooling "
            "had already begun before the peak was recorded.",
        ],
        trap="Confusing the measured maximum with the corrected estimate, or reading the temperature itself as ΔT.",
    ),
    dict(
        id="Q22", episode=11, title="Good repeatability can coexist with the wrong answer",
        stem="A reaction of 0.0400 mol shows a 4.00 °C temperature rise. The valid CF is 500 J °C⁻¹, but a "
             "spreadsheet uses 450 J °C⁻¹. The reaction is exothermic.",
        parts=[
            ("a", "Determine the reported and the corrected molar enthalpies.", 2),
            ("b", "Explain whether repeating the experiment fixes this error.", 1),
            ("c", "Would an additive thermometer offset of +1.5 °C on both initial and final readings change ΔT? Explain.", 2),
        ],
        answers=[
            "a. Reported: −(450 × 4.00) ÷ 0.0400 = −45 000 J mol⁻¹ = −45.0 kJ mol⁻¹; corrected: −50.0 kJ mol⁻¹",
            "b. No. The same wrong CF is used every time, so repeats agree closely (good repeatability) but share "
            "the same systematic bias.",
            "c. No. (T_f + 1.5) − (T_i + 1.5) = T_f − T_i, so an identical additive offset cancels in the "
            "difference. This does not apply to every kind of thermometer error (e.g. a scale error).",
        ],
        trap="Equating repeatability with accuracy, or assuming every offset changes a difference.",
    ),
    dict(
        id="Q23", episode=12, title="Compare emissions per useful energy, not per fuel mass",
        stem="Hypothetical comparison data, supplied solely for this exercise. Fossil Fuel R: 43.0 MJ kg⁻¹, "
             "35.0% useful-heat efficiency, lifecycle emissions 80.0 g CO₂-e per MJ of fuel energy. "
             "Waste-derived Biofuel S: 29.0 MJ kg⁻¹, 28.0% efficiency, lifecycle emissions 45.0 g CO₂-e per MJ of fuel energy.",
        parts=[
            ("a", "For delivery of 1.00 MJ of useful heat, calculate the fuel energy input for each fuel.", 2),
            ("b", "Calculate the mass of each fuel required.", 2),
            ("c", "Calculate the lifecycle emissions for each fuel.", 2),
            ("d", "Evaluate the claim that the lower fuel mass must mean lower emissions.", 1),
        ],
        answers=[
            "a. R: 1.00 ÷ 0.350 = 2.857 MJ; S: 1.00 ÷ 0.280 = 3.571 MJ",
            "b. R: 2.857 ÷ 43.0 = 0.0664 kg; S: 3.571 ÷ 29.0 = 0.123 kg",
            "c. R: 2.857 × 80.0 = 229 g CO₂-e; S: 3.571 × 45.0 = 161 g CO₂-e",
            "d. The claim is false here: R needs less mass but S has lower lifecycle emissions for the same "
            "useful output; mass and emissions measure different things.",
        ],
        trap="Comparing emissions per input MJ without correcting for efficiency.",
    ),
    dict(
        id="Q24", episode=12, title="Evidence-based sustainability with an honest limit",
        stem="Per kilogram of ethanol produced: Process A uses edible crop feedstock, 8 MJ of natural-gas heat "
             "and 12 L of freshwater, and vents its fermentation CO₂. Process B uses food-processing waste, "
             "10 MJ of electricity (60% renewable) and 20 L of freshwater, and its captured fermentation CO₂ "
             "is used in another manufacturing process. Both are technically viable.",
        parts=[
            ("a", "Compare the processes using one relevant green chemistry or circular-economy consideration.", 2),
            ("b", "Compare the processes using a second, different consideration.", 2),
            ("c", "Identify one tradeoff, or one limit of the data.", 1),
            ("d", "Recommend a process under explicitly stated priorities. Can the data establish which has "
                  "lower total lifecycle greenhouse emissions?", 1),
        ],
        answers=[
            "a. Feedstock: B uses waste rather than an edible crop, reducing competition with food and land use "
            "(renewable feedstock from waste; circular use).",
            "b. Resources: A uses less listed energy (8 vs 10 MJ) and less freshwater (12 vs 20 L) per kg.",
            "c. Tradeoff: B's feedstock/CO₂ advantages versus A's lower energy and water use. CO₂ use need not "
            "mean permanent storage.",
            "d. Either recommendation is defensible if it follows from stated priorities (e.g. B if avoiding "
            "food competition is the priority). The data cannot establish total lifecycle emissions: emission "
            "factors for the natural gas and the 40% non-renewable electricity, and broader lifecycle data, are missing.",
        ],
        trap="Assuming 'bio' or 'renewable electricity' makes a process superior on every criterion.",
    ),
    dict(
        id="Q25", episode=13, title="Integrated workshop: a mixed-gas water heater",
        stem="A purified digester gas contains 90.0% CH₄ and 10.0% CO₂ by volume. An idealised heater "
             "receives 6.20 L of the fuel mixture and 60.0 L of air, both measured at SLC; air contains "
             "21.0% O₂ by volume. Methane burns completely. Use M(CH₄) = 16.0 g mol⁻¹ and ΔH_c(CH₄) = "
             "−890 kJ mol⁻¹ for formation of liquid water. The heater raises 800.0 g of water from 17.0 °C "
             "to 57.0 °C. Assume the fuel-stream CO₂ passes through unchanged and all methane burns.",
        parts=[
            ("a", "Determine the total fuel-mixture amount, the methane amount and the available oxygen.", 3),
            ("b", "Write the thermochemical equation for the combustion, with states.", 2),
            ("c", "Calculate the mass of excess O₂ remaining.", 2),
            ("d", "Calculate the energy released by the fuel and the heat gained by the water.", 2),
            ("e", "Calculate the useful efficiency, and explain why an inverse-efficiency operation would be wrong here.", 3),
            ("f", "Determine the total dry CO₂ volume at SLC after isolation.", 2),
            ("g", "Explain the source-based reason for calling this methane renewable.", 1),
        ],
        answers=[
            "a. n(mixture) = 6.20 ÷ 24.8 = 0.250 mol; n(CH₄) = 0.900 × 0.250 = 0.225 mol; "
            "n(O₂) = 0.210 × 60.0 ÷ 24.8 = 0.50806 mol",
            "b. CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)     ΔH = −890 kJ",
            "c. Required O₂ = 0.450 mol; remaining 0.05806 mol × 32.0 = 1.86 g",
            "d. 0.225 × 890 = 200.25 kJ released; q(water) = 800.0 × 4.18 × 40.0 = 133 760 J = 133.76 kJ",
            "e. 133.76 ÷ 200.25 × 100% = 66.8%. Both input and useful output are known, so efficiency is "
            "output ÷ input; dividing by an efficiency is only for finding a required input from a target output.",
            "f. CO₂ = 0.225 (new) + 0.0250 (inlet) = 0.250 mol × 24.8 = 6.20 L",
            "g. It comes from recently grown biomass that is replenished on a short (human) timescale; the methane molecule itself is identical.",
        ],
        trap="Mixture vs reactive component; air vs oxygen; new vs inlet CO₂; energy units; efficiency direction.",
    ),
    dict(
        id="Q26", episode=13, title="A fuel ranking that needs a specified basis",
        stem="Methanol: M = 32.0 g mol⁻¹, ΔH_c = −726 kJ mol⁻¹. Ethanol: M = 46.0 g mol⁻¹, ΔH_c = "
             "−1370 kJ mol⁻¹. Complete combustion produces 1 mol and 2 mol CO₂ per mole of fuel respectively. "
             "A methanol heater has 25.0% useful-energy efficiency and an ethanol heater 40.0%.",
        parts=[
            ("a", "Calculate the energy released per gram for each fuel.", 2),
            ("b", "Calculate the direct-combustion CO₂, in grams per useful kJ, for each heater.", 4),
            ("c", "Explain why 'both contain an O–H bond, so they release equal energy per gram' is wrong.", 2),
            ("d", "Explain whether these results establish which fuel has lower lifecycle emissions.", 2),
        ],
        answers=[
            "a. Methanol 726 ÷ 32.0 = 22.7 kJ g⁻¹; ethanol 1370 ÷ 46.0 = 29.8 kJ g⁻¹",
            "b. Methanol: 44.0 g ÷ (726 × 0.250) kJ = 0.242 g kJ⁻¹; ethanol: 88.0 g ÷ (1370 × 0.400) kJ = 0.161 g kJ⁻¹",
            "c. Energy released depends on all the bonds broken and formed in the whole reaction, and per-gram "
            "values also depend on molar mass; one shared bond does not determine it.",
            "d. No. Direct combustion CO₂ omits feedstock production, processing and transport; lifecycle "
            "data are needed.",
        ],
        trap="Per mole vs per gram; CO₂ per mole vs per useful energy; bond-breaking misconception; unsupported lifecycle claim.",
    ),
    dict(
        id="Q27", episode=14, title="Integrated workshop: calibration, a graph and neutralisation",
        stem="A calorimeter is electrically calibrated with 125.0 g of water using 5.00 V and 1.20 A for "
             "300 s, giving a 3.00 °C rise. Assume this CF also applies accurately to the reaction mixture "
             "below. 50.0 mL of 1.00 mol L⁻¹ HCl is mixed with 75.0 mL of 0.800 mol L⁻¹ NaOH. The initial "
             "baseline is 20.0 °C and mixing starts at t = 60 s. Post-reaction cooling measurements: 120 s, "
             "24.7 °C; 180 s, 24.6 °C; 240 s, 24.5 °C; 300 s, 24.4 °C. Assume a linear cooling trend is "
             "suitable for the correction and neutralisation is complete.",
        parts=[
            ("a", "Calculate the calibration energy and CF, and check CF against the water-only heat capacity.", 3),
            ("b", "Identify the available amounts and the limiting reactant.", 2),
            ("c", "Determine the corrected temperature rise.", 2),
            ("d", "Calculate the reaction heat and the experimental molar enthalpy per mole of water.", 3),
            ("e", "Explain what repeatability would and would not establish about this result.", 2),
            ("f", "Predict whether doubling the NaOH concentration (same volume) would double the heat "
                  "released, assuming CF and other conditions are unchanged.", 2),
        ],
        answers=[
            "a. E = 5.00 × 1.20 × 300 = 1800 J; CF = 1800 ÷ 3.00 = 600 J °C⁻¹; water-only = 125.0 × 4.18 = "
            "522.5 J °C⁻¹ < 600, so CF is physically plausible.",
            "b. n(HCl) = 0.0500 mol; n(NaOH) = 0.0600 mol; 1 : 1, so HCl is limiting.",
            "c. Slope −0.1 °C per 60 s; extrapolated T(60 s) = 24.8 °C; corrected rise = 4.8 °C",
            "d. q = 600 × 4.8 = 2880 J; ΔH = −2.880 kJ ÷ 0.0500 mol = −57.6 ≈ −58 kJ mol⁻¹",
            "e. Close repeats show precision/repeatability, not accuracy; a shared systematic error (e.g. a wrong "
            "CF or unaccounted heat loss) would remain.",
            "f. No. HCl remains limiting at 0.0500 mol, so the same amount of water forms and the same heat is released.",
        ],
        trap="Seconds, solution volumes, wrong denominator, observed vs corrected peak, precision vs accuracy, excess vs reacted.",
    ),
    dict(
        id="Q28", episode=14, title="A hand-warmer claim distorted by the wrong calibration",
        stem="An idealised hand-warmer powder contains a hypothetical active solid X (M = 80.0 g mol⁻¹) and "
             "inert filler. Dissolving X completely releases 24.0 kJ per mole of X; the filler has negligible "
             "thermal effect. A 4.00 g powder sample is tested in a setup correctly calibrated for this "
             "experiment (CF = 300 J °C⁻¹) and produces a 3.20 °C rise. Assume complete dissolution and "
             "accounted-for heat transfer. The manufacturer claims 95.0% X by mass.",
        parts=[
            ("a", "Calculate the heat gained by the calorimeter.", 2),
            ("b", "Determine the amount of X, the mass of X and the mass percentage of X.", 4),
            ("c", "Assess the manufacturer's claim.", 1),
            ("d", "Recalculate the percentage if a spreadsheet mistakenly uses CF = 360 J °C⁻¹ from a different "
                  "setup, and explain the implication.", 2),
            ("e", "State whether repeating with the wrong CF resolves the bias.", 1),
            ("f", "Explain how absorbed moisture could lower the active fraction in a subsequently weighed 4.00 g "
                  "sample (assume negligible change to CF and no extra thermal effect from moisture).", 2),
        ],
        answers=[
            "a. q = 300 × 3.20 = 960 J",
            "b. n(X) = 0.960 kJ ÷ 24.0 kJ mol⁻¹ = 0.0400 mol; m(X) = 0.0400 × 80.0 = 3.20 g; 3.20 ÷ 4.00 × 100% = 80.0%",
            "c. 80.0% < 95.0%: the claim is not supported by this modelled measurement.",
            "d. q = 360 × 3.20 = 1152 J → 0.0480 mol → 3.84 g → 96.0%: the wrong CF makes the claim appear supported.",
            "e. No. Repeating with the same wrong CF reproduces the same bias.",
            "f. Water absorbed by the powder takes up part of the fixed 4.00 g mass, so less X is present; less "
            "heat is released and the rise is smaller, lowering the calculated percentage of X.",
        ],
        trap="Claim vs evidence, calibration-error direction, precise but biased results, active mass vs total sample mass.",
    ),
]

BY_ID = {q["id"]: q for q in BANK}


def marks_total(qid: str) -> int:
    return sum(p[2] for p in BY_ID[qid]["parts"])
