# Formula and method sheet: energy, fuels and calorimetry

A one-page summary of the relationships, conventions and checks used in this series. It is a study aid,
not the official VCAA data book: in an exam, use the constants and data the paper gives you.

## Constants and conversions used in the series

| Quantity | Value |
|---|---|
| Standard laboratory conditions (SLC) | 25 °C and 100 kPa |
| Molar volume of a gas at SLC | V<sub>m</sub> = 24.8 L mol⁻¹ |
| Specific heat capacity of water | c = 4.18 J g⁻¹ °C⁻¹ (= 4.18 kJ kg⁻¹ °C⁻¹) |
| Relative atomic masses used | C = 12.0, H = 1.0, O = 16.0 (use any molar mass a question supplies) |
| Food energy factors used | carbohydrate 16 kJ g⁻¹, protein 17 kJ g⁻¹, fat 37 kJ g⁻¹ |
| Volume | 1 L = 1000 mL; 1 m³ = 1000 L |
| Energy | 1 kJ = 1000 J; 1 MJ = 1000 kJ |
| Time | 1 min = 60 s; 1 h = 3600 s |
| Temperature change | a change of 1 °C equals a change of 1 K |

## Amount of substance

| Situation | Relationship | Watch for |
|---|---|---|
| mass of a substance | n = m ÷ M | mass in g, M in g mol⁻¹ |
| gas at SLC | n = V ÷ 24.8 L mol⁻¹ | volume in L, not mL |
| solution | n = c × V | V in L |
| gas mixture | n(component) = fraction × n(total) | for gases at the same T and P, volume % = mole % |
| oxygen from air | n(O₂) = (O₂ fraction) × V(air) ÷ V<sub>m</sub> | air is not all oxygen (about 21%; use the value given) |
| from an equation | use the mole ratio of the balanced equation | balance first, with states |
| limiting reactant | compare n ÷ coefficient for each reactant: the smallest limits | the reactant in excess is what is **left over** |
| excess remaining | available − required | convert to a mass only at the end |

## Energy and enthalpy

* ΔH = H(products) − H(reactants). Exothermic: ΔH < 0 (energy released to the surroundings).
  Endothermic: ΔH > 0.
* A thermochemical equation's ΔH applies to the equation **as written**. Reverse the equation: change
  the sign. Multiply the coefficients: multiply ΔH by the same factor. States matter (H₂O(l) vs H₂O(g)).
* Bond enthalpies (estimate): ΔH ≈ Σ(bonds broken) − Σ(bonds formed).
* Energy profile: activation energy E<sub>a</sub> = H(transition state) − H(reactants); ΔH is the
  vertical distance from reactants to products.
* A catalyst provides a pathway with a lower activation energy. It does **not** change ΔH.
* Energy released by a fuel: E = n(fuel) × |ΔH<sub>c</sub>|. Energy per gram = |ΔH<sub>c</sub>| ÷ M.
* Food: energy = Σ(mass of each nutrient × its energy factor); scale to the portion actually eaten.

## Calorimetry

| Situation | Relationship |
|---|---|
| heating water | q = m c ΔT (m in g gives q in J) |
| electrical calibration | E = V × I × t (t in s); calibration factor CF = E ÷ ΔT (J °C⁻¹) |
| calibrated calorimeter | q = CF × ΔT |
| reaction in the calorimeter | q(reaction) = −q(calorimeter); ΔH = −q ÷ n(limiting), per mole of the stated substance |
| fuel or food burnt under a can | energy per gram = q ÷ mass burnt (heat losses make this an underestimate) |

**Corrected temperature rise.** When the mixture is already cooling, extrapolate the straight cooling line
back to the moment of mixing (or ignition). ΔT = extrapolated temperature − initial baseline. The highest
reading underestimates the rise.

**Plausibility.** A CF should be at least m(water) × c, because the cup, thermometer and stirrer also absorb
energy. A temperature rise means the reaction released heat, so ΔH is negative.

**Direction of errors.** Follow the change through the calculation chain (ΔT → q → n → m → %).
Heat lost during calibration makes the CF too large; heat lost during a reaction makes ΔT, q and the
calculated |ΔH| too small. A CF that is too large makes every quantity calculated from it too large.
Repeating with the same systematic error gives precise (repeatable) results that are still inaccurate.

## Efficiency and fair comparisons

* Efficiency = useful energy output ÷ energy input × 100%.
* Input needed for a target output = useful output ÷ efficiency (efficiency as a decimal).
  Use this inverse step only when the input is the unknown.
* Compare fuels on a stated basis: per mole, per gram, or per useful kilojoule (or megajoule).
  Emissions per useful output = emissions per unit of input energy ÷ efficiency.
* Direct (combustion) emissions are not lifecycle emissions: lifecycle data include producing,
  processing and transporting the fuel, and any methane leakage. State the system boundary.
* Renewable means replenished on a human timescale. Sustainable also weighs land, food, water,
  biodiversity and wastes. A renewable fuel is not automatically sustainable.

## Method selection

| Given or asked | Use |
|---|---|
| mass / gas volume at SLC / solution | n = m ÷ M / n = V ÷ 24.8 / n = c × V |
| energy released by a fuel | E = n × \|ΔH\| |
| heating water | q = m c ΔT |
| electrical calibration | E = V × I × t; CF = E ÷ ΔT |
| calibrated calorimeter | q = CF × ΔT |
| molar enthalpy | ΔH = −q ÷ n(limiting), negative if heat is released |
| efficiency | useful output ÷ input × 100% |
| input for a target output | useful output ÷ efficiency |
| comparing fuels | state the basis: per mol, per g or per useful kJ |

## Reporting answers

* Show each quantity with its unit; keep unrounded values until the final answer.
* Round the final answer to the number of significant figures justified by the data
  (a corrected temperature rise read from a graph often limits the answer to two).
* Give ΔH with its sign, its unit and the substance it is "per mole" of.
* Check plausibility: efficiencies between 0 and 100%, masses no larger than the sample, conservation of
  atoms (for example, moles of carbon in = moles of CO₂ out).

## Trap checklist

1. mL left unconverted in n = c × V or n = V ÷ V<sub>m</sub>; minutes left unconverted in E = V I t.
2. A gas mixture's total amount used as the amount of the reacting component.
3. The volume of air used as the volume of oxygen.
4. Dividing by the amount of the reactant in excess instead of the limiting reactant.
5. J and kJ mixed (for example, q in J divided by kJ mol⁻¹).
6. Wrong sign on ΔH; ΔH not matched to the equation as written.
7. The highest temperature reading used instead of the extrapolated value.
8. Repeatable results assumed to be accurate.
9. A catalyst assumed to change ΔH.
10. Efficiency applied in the wrong direction.
11. Fuels compared on different bases (per mole vs per useful kJ; per kJ released vs per useful kJ).
12. "Renewable" treated as "sustainable"; direct emissions treated as lifecycle emissions.
