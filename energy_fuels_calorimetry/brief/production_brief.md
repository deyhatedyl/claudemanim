# Production brief (verbatim copy of the user's specification, 2026-10-02)

User note accompanying the brief: "For the narration; we'll be using gemini 3.8 tts flash.
If you want I can upload chemistry vce study design + exams unless you already have it."

---

Claude production brief for a VCE Chemistry Manim video series

## Your task

Create a complete, narrated Manim video series that teaches VCE Chemistry Units 3 and 4 energy, fuels and calorimetry from the foundations through demanding exam-style applications. The learner needs slow, explicit explanations of why each step works, not a formula slideshow. Deliver actual rendered videos, with synchronized narration and captions, alongside the editable project.

Use this brief as the production specification. Work through the series in order, saving progress after every scene and episode. Do not stop after proposing a plan or producing code. Continue through scripting, implementation, rendering and quality assurance for the full series where the available tools permit it. Report genuine blockers accurately and finish all unblocked work. Never claim an MP4, narration track or render was produced unless it exists and has been checked.

The requested deliverable is a series of individually watchable lessons. Target 12 teaching episodes and 2 exam workshops, approximately 3 hours 15 minutes to 4 hours 15 minutes altogether. These times are planning estimates, not limits: split a crowded episode or extend it rather than remove reasoning or rush speech. Do not compress the whole subject into a single 30-minute video. Individual MP4s are the primary deliverable; a compiled version is optional after the series is complete.

This brief contains 28 original anchor question sets with independently calculated answer targets. Use them as teaching and assessment anchors. They are newly written practice material, not official VCAA questions or marking schemes. You must independently verify them again before recording. Develop complete, step-by-step solutions and indicative marking guides from these targets.

## Audience and teaching contract

- Teach a Year 12 VCE Chemistry student whose algebra and mole calculations may be uneven. Explain symbols, units, ratios and reasoning before relying on them.
- Begin with intuition and a concrete picture, then connect it to precise chemistry and the equation used in an exam.
- For every calculation identify: what is given; what is being asked; which chemical model applies; which equation is appropriate; and why the chosen mole ratio is valid.
- Show one transformation at a time. Do not jump from a substituted expression to a final answer without showing the significant intermediate result.
- Explicitly separate amount in mol, mass in g, concentration in mol L^-1, volume in L and energy in J or kJ.
- Tell the learner what a plausible answer should look like before checking it numerically.
- Use recurring visual conventions, retrieval questions and worked examples. Revisit difficult distinctions in later contexts.
- Teach scientific wording alongside calculations. Show a concise full-credit-style answer and explain why a superficially similar answer misses a causal link.
- Use plain language first, but always supply the correct terms the learner will need in an exam.
- Never label the learner or an error as stupid or obvious. Explain why the tempting error is tempting, then resolve it.

## Scope and sources

The scope comes from the supplied Chemistry study design's Unit 3 carbon-based fuels and measuring changes in chemical reactions, with necessary links to organic biofuel manufacture, science skills and sustainability. Cover every item in the coverage matrix below.

The source examinations and reports used to identify recurring skills are:

- 2024 end-of-year: A1-A3; B3a, B3c.ii-iii; B5; fermentation and measurement elements of B8.
- 2025 end-of-year: A1-A6; B1; contextual science-skill lessons from the reports.
- 2025 NHT: A1, A3-A4; B2; B5; relevant biofuel context from B10.
- 2026 NHT: A1-A8; B1a-b,d-e; B2; relevant sustainability contexts.
- Study design supplied as 2023ChemistrySD (2).docx; Units 3 and 4 begin in 2024 in this version.

If the source files are also attached to your session, inspect relevant sections and reconcile coverage before production. If they are not accessible, this brief is self-contained: proceed from its objectives and fully specified practice data, identify that the original source files were not rechecked, and do not claim to have opened them.

Treat examiner reports as guidance about assessed reasoning, not error-free scientific textbooks. Resolve inconsistencies with balanced equations, units, independently computed arithmetic and the question's actual wording. Do not blindly copy apparent typographical errors in an answer report.

Do not turn this into an electrochemistry course, an organic-synthesis course or a full equilibrium course. Explain only the supporting concepts required here and signpost those separate topics. Specific heat capacity, calibration, heat-loss analysis and fuel/food comparisons must not be cut for time.

## Originality requirements

Preserve the assessed skill and misconception, not the exam's wording or surface story.

For every new question you create beyond the supplied anchors:

1. Specify the learning objective and exact trap first.
2. Change the context and at least two substantive features, such as the unknown quantity, data representation, required reasoning sequence, fuel composition or direction of calculation.
3. Do not merely replace a student's name and a few numbers in a past-paper question.
4. Provide all necessary data, phase information, assumptions and measurement conditions.
5. Solve it independently before turning it into a scene.
6. For multiple choice, ensure exactly one best answer and derive each distractor from a named error.
7. Never imply that an original practice question is an official VCAA question.

When adapting the anchor sets, retain their logical sufficiency and scientific assumptions. You may improve wording, but update the checked solution if you change any data. Do not show the source-exam reference in a way that gives away the answer during an attempt.

## Coverage matrix

| ID | Required content | Primary episodes | Later retrieval |
|---|---|---|---|
| C01 | Units, mole ratios, n=m/M, n=cV, n=V/Vm at SLC | 01 | 06-10, 13-14 |
| C02 | Fuel definition; fossil fuels versus biofuels; renewal timescales | 04 | 12-13 |
| C03 | Coal, natural gas, petrol; biogas, bioethanol, biodiesel | 04 | 06, 12 |
| C04 | Photosynthesis, respiration, fermentation; equations and energy conversion | 04-05 | 12 |
| C05 | Bioethanol manufacture and subsequent distillation | 04 | 12 |
| C06 | Basic triglyceride-to-biodiesel transesterification | 04 | 12 |
| C07 | Food energy from carbohydrates, protein and lipids | 05 | retrieval in 13 |
| C08 | System/surroundings, heat, temperature, exothermic/endothermic | 02 | 08-11 |
| C09 | Bond breaking and bond making; approximate bond-enthalpy calculations | 02 | 03, 13 |
| C10 | Enthalpy in kJ, molar enthalpy and energy per gram | 02-03 | 08-10, 13-14 |
| C11 | Energy profiles, activation energy, reverse reactions and catalysts | 03 | retrieval in 12 |
| C12 | Balanced complete/incomplete combustion and physical states | 06 | 07, 13 |
| C13 | Thermochemical equation scaling and reversing | 03, 06 | 10, 13 |
| C14 | Mass-mass, mass-volume and volume-volume stoichiometry | 06-07 | 13 |
| C15 | Limiting reactants and quantity of excess remaining | 07 | 10, 13-14 |
| C16 | Gas mixtures, air oxygen fraction, measured conditions | 07 | 13 |
| C17 | CO2, CH4 and H2O in fuel/environmental contexts | 04, 06, 12 | 13 |
| C18 | q=mc deltaT and combustion/food calorimetry | 08 | 13 |
| C19 | Efficiency, inverse efficiency and comparing fuels fairly | 08 | 12-13 |
| C20 | Electrical calibration; CF=VIt/deltaT | 09 | 14 |
| C21 | Apparatus heat capacity; physical bounds on CF | 09 | 11, 14 |
| C22 | Solution calorimetry; q=CF deltaT; molar reaction enthalpy | 10 | 14 |
| C23 | Limiting reactant versus reaction extent in calorimetry | 10 | 14 |
| C24 | Temperature-time graphs, cooling correction and extrapolation | 11 | 14 |
| C25 | Calibration mismatch, errors, accuracy, precision, repeatability and validity | 09, 11 | 14 |
| C26 | Purity/claim evaluation using energy data and assumptions | 14 | recap |
| C27 | Renewability versus sustainability, lifecycle boundaries, circular economy | 12 | 13 |
| C28 | Green chemistry principles, data-based comparisons and conclusions | 12 | 13 |

(Coverage IDs C01-C28 were added by Claude for tracking; the content is the brief's.)

## Episode plan and scene specifications

Each episode should contain: a short retrieval check; an intuitive model; precise chemistry; a guided original problem; a less scaffolded exam-style problem; a misconception correction; and a closing recall prompt. Use the question IDs in the bank below. Extra micro-checks can be brief verbal or on-screen predictions.

### Episode 01 Mole calculations and units that unlock the topic
Target: 10-14 minutes. Anchor sets: Q01-Q02.

Teach: amount versus mass; molar mass; concentration; SLC = 25 degrees C and 100 kPa; Vm = 24.8 L mol^-1 in this brief; balanced coefficients as mole ratios. Demonstrate g/mg, L/mL/m3, J/kJ/MJ and time conversions. Distinguish rounding during working from rounding the final result.

Manim scenes:
1. Label a container with its mass, amount and volume; change one label without implying the others are interchangeable.
2. Animate unit cancellation in n=m/M, n=cV and n=V/Vm.
3. Show a scale ladder for m3 to L to mL, with explicit multiplication factors.
4. Use a reaction as a recipe with a coefficient ratio. First show particle groups, then replace group counts with amounts in mol.
5. Work Q01 and Q02, keeping the requested unit visible throughout.

Checkpoint: explain why 250 mL cannot be substituted directly into a formula using concentration in mol L^-1.

### Episode 02 Where reaction energy comes from
Target: 12-16 minutes. Anchor sets: Q03-Q04.

Teach: system and surroundings; heat versus temperature; exothermic and endothermic reactions; q_system and q_surroundings with opposite signs in an ideal energy balance. Explain that bond breaking requires energy and bond formation releases energy. Net reaction energy depends on all bonds broken and formed, including oxygen in combustion. Introduce the qualitative idea that oxygenated fuels are already partly oxidised, without making it a universal numerical shortcut.

Manim scenes:
1. Draw a boundary around reacting chemicals, a separate surrounding calorimeter and an energy-transfer arrow.
2. Animate energy entering before a bond breaks; animate energy leaving as a bond forms. Never show bond breaking as the energy-release step.
3. Build an energy ledger for Q03, with separate totals for bonds broken and formed.
4. Introduce deltaH = H_products - H_reactants; show why a negative deltaH corresponds to heat transferred out of the reacting system.
5. Work the endothermic example Q04 to reverse the direction of the arrows.
6. Briefly place methane, methanol and CO2 on a qualitative carbon-oxidation ladder. Explain why partial oxidation can reduce the further energy available from combustion, while emphasizing that an exact fuel comparison requires the full reaction and a consistent per-mole or per-mass basis.

Checkpoint: distinguish 'deltaH = -50 kJ' from '50 kJ of energy is released'. Avoid describing a negative quantity of energy released.

### Episode 03 Energy profiles and thermochemical equations
Target: 12-16 minutes. Anchor sets: Q05-Q06.

Teach: reaction coordinate versus time; reactant/product enthalpy levels; forward and reverse activation energies; catalysts lowering the barrier without changing deltaH or the endpoint energy levels. Teach equation multiplication, reversal and the meaning of the amount specified by the equation. Separate deltaH for the equation as written from a molar quantity referring to a specified substance.

Manim scenes:
1. Draw the two endpoint levels before adding the curve.
2. Add separate labelled arrows for forward Ea, reverse Ea and deltaH.
3. Overlay a catalysed path with identical endpoints.
4. Double a thermochemical equation and its energy together; reverse both equation direction and enthalpy sign.
5. Reveal phase labels and show why changing liquid water to gaseous water requires different enthalpy data.

Checkpoint: a catalyst does not make an exothermic reaction release more energy for the same amount reacting.

### Episode 04 Fuels, biofuels and the carbon cycle
Target: 12-16 minutes. Anchor sets: Q07-Q08.

Teach: what a fuel is; coal, natural gas and petrol; biogas, bioethanol and biodiesel; replenishment timescale; identical fuel molecules can have different origins. Teach balanced photosynthesis, respiration and fermentation equations. Show anaerobic digestion conceptually, enzyme-catalysed fermentation and why very high temperature damages enzyme function. Explain distillation as concentrating/separating ethanol, without implying ordinary simple distillation necessarily produces pure ethanol. Include the basic triglyceride + 3 alcohol -> 3 fatty-acid alkyl esters + glycerol relationship.

Manim scenes:
1. Contrast a geological timescale with a renewable feedstock cycle.
2. Track labelled carbon atoms from atmospheric CO2 to plant material to fuel and back to CO2.
3. Show light supplying energy to photosynthesis; do not portray energy as appearing from nowhere or being released simply by breaking glucose bonds.
4. Animate glucose dividing into two ethanol and two CO2 molecules with atom counts preserved.
5. Show a simplified distillation setup and a triglyceride ester-exchange diagram. Label them schematic and keep organic detail proportionate to this series.

Checkpoint: renewable does not mean emission-free or automatically sustainable.

### Episode 05 Food as a chemical energy source
Target: 10-14 minutes. Anchor sets: Q09-Q10.

Teach: the supplied VCE-style energy factors: carbohydrate 16 kJ g^-1, protein 17 kJ g^-1, fat 37 kJ g^-1. Distinguish per gram, per 100 g, per serving and per packet. Connect glucose oxidation to respiration and conservation of energy. Identify oxygen as being reduced in the respiration equation using its change in oxidation number from 0 to -2; do not equate all released energy with useful biological work. State that these rounded nutritional factors are a different reporting basis from a specific measured molar heat of combustion; do not silently substitute one for the other.

Manim scenes:
1. Build an energy bar by summing three macronutrient contributions.
2. Animate scaling a 100 g label to a serving, keeping units attached.
3. Contrast a larger and smaller portion so the ranking can change with the basis of comparison.
4. Work Q09, then ask the learner to choose the comparison basis before Q10.

Checkpoint: doubling serving mass doubles its calculated energy; it does not change the energy per gram.

### Episode 06 Combustion equations and gaseous products
Target: 12-16 minutes. Anchor sets: Q11-Q12.

Teach: complete versus incomplete combustion; CO2, CO and carbon as possible carbon products according to available data; water production; balancing C then H then O. Include oxygen already present in an oxygenated fuel. Explain that the products of incomplete combustion are not uniquely determined solely by saying 'limited oxygen'. Teach physical states at SLC versus hot exhaust, greenhouse-gas mass, dry gas versus wet gas and the difference between carbon emissions and all greenhouse gases in a stated model.

Manim scenes:
1. Balance an oxygenated fuel with conserved colour-coded atom counters.
2. Show complete and specified incomplete product sets side by side.
3. Cool an exhaust stream: water condenses while dry CO2 remains to be measured.
4. Use two accounting columns: material formed in the reaction and material measured after cooling.

Checkpoint: a coefficient relates moles, not grams; 2 mol of product does not mean twice the mass unless molar masses also match.

### Episode 07 Limiting reactants, excess fuel and gas mixtures
Target: 16-20 minutes. Anchor sets: Q13-Q14.

Teach: convert both reactants to moles; compare n/coefficient; determine reaction extent; calculate amount used and amount remaining. Treat gas volume fractions as mole fractions only under the stated ideal-mixture/common-condition assumptions. Apply the oxygen fraction to air and the reactive fraction to a fuel mixture. Distinguish newly formed CO2 from CO2 already entering with the fuel.

Manim scenes:
1. Use reaction batches to show why comparing raw mole numbers is insufficient.
2. Separate 'initial', 'used' and 'remaining' trays.
3. Partition a gas stream into reactive and nonreactive components.
4. Keep an oxygen budget beside the fuel budget throughout Q14.
5. Animate the invariant: remaining amount = initial amount - amount used, and check that no result is negative.

Model note: the relevant questions explicitly assume complete combustion of the portion that reacts, with excess fuel left unreacted. Preserve that assumption. Do not simultaneously infer unspecified incomplete-combustion products. Use an abstract reaction box, not a depiction of an unsafe sealed combustion experiment.

### Episode 08 Measuring combustion energy and efficiency
Target: 14-18 minutes. Anchor sets: Q15-Q16.

Teach: derive q=mc deltaT as heat capacity per gram times mass times temperature rise. Identify whose mass and temperature are used. Compare theoretical fuel energy with measured useful heat. Define efficiency with an explicit numerator and denominator; solve both forward and inverse problems. Include measured fuel mass lost, unit matching and final-temperature versus temperature-rise distinctions.

Manim scenes:
1. Track energy from fuel into water, apparatus and surroundings with a labelled energy-flow diagram.
2. Vary water mass and energy separately to reveal their effects on deltaT.
3. Animate a before/after fuel-container mass reading. Include a short food-calorimetry transfer example: burning 1.50 g dry food raises 100.0 g water by 8.0 degrees C, so the water gains 3344 J and the measured water-heat yield is about 2.2 kJ per gram of food. Explain apparatus/environment losses and incomplete combustion, and distinguish this experimental water-heat yield from a nutritional label's metabolizable-energy basis.
4. Build efficiency = useful output / total input, then rearrange it visually.
5. Test the limiting cases: 100% efficiency and a lower efficiency for the same useful output.

Checkpoint: less efficient heating requires more fuel to deliver the same useful energy.

### Episode 09 Why calorimeters need calibration
Target: 14-18 minutes. Anchor sets: Q17-Q18.

Teach: the water is not the only component being heated; apparatus heat capacity; CF as energy per degree for the calibrated setup. Derive electrical calibration from E=VIt and CF=E/deltaT. Use seconds, joules and consistent temperature units. Explain dependence on contents, quantity and apparatus, and the approximate lower bound CF >= m_water c_water for an ideal correctly measured water calibration with positive apparatus heat capacity.

Manim scenes:
1. Split electrical input into water and cup/probe/stirrer energy changes.
2. Construct CF from the measured electrical energy and temperature rise.
3. Stack water heat capacity and apparatus heat capacity to get the total.
4. Add extra water and ask whether the earlier CF can be retained.
5. Put Q18's claimed CF next to the water-only lower bound and use arrows to reason about a calibration error's direction.

Checkpoint: heat loss during electrical calibration normally makes measured deltaT smaller and the apparent CF larger; do not memorise 'heat loss means the answer is smaller' for every stage.

### Episode 10 Reaction calorimetry and molar enthalpy
Target: 14-18 minutes. Anchor sets: Q19-Q20.

Teach: q_cal = CF deltaT; q_reaction = -q_cal under the stated model; divide by the appropriate amount. If expressing enthalpy per mole of reaction as written, divide by reaction extent, not blindly by the mole amount of whichever reagent is mentioned. Explain dilution volumes, limiting reagents, excess remaining and why the final temperature includes the initial temperature.

Manim scenes:
1. Animate the mixing of measured solution volumes and calculate the available mole amounts.
2. Highlight the limiting reagent and the corresponding amount of water produced/reaction extent.
3. Move measured heat into a positive calorimeter column and a negative reaction column.
4. Place equation coefficients directly beside the denominator used in the molar calculation.
5. Work Q20's factor-of-two trap without skipping the reaction-extent step.

Checkpoint: changing the equation coefficients changes the enthalpy associated with the equation, but cannot change the heat released by the same physical reaction.

### Episode 11 Temperature graphs, correction and experimental reasoning
Target: 16-20 minutes. Anchor sets: Q21-Q22.

Teach: pre-mixing baseline, mixing time, observed maximum, post-reaction cooling and back-extrapolated temperature. Describe extrapolation as a model-based estimate, not perfect recovery of the true temperature. Distinguish heat loss during calibration from heat loss during a later reaction. Cover systematic versus random errors, fixed thermometer offsets, accuracy, precision, repeatability, validity, reasonable assumptions and specific improvements.

Manim scenes:
1. Plot measured points on calibrated axes; do not invent a decorative curve unrelated to the data.
2. Fit/highlight the linear cooling region and extend it back to mixing time.
3. Mark observed and corrected rises with different line styles and labels.
4. Propagate a measurement error through the actual formula with up/down arrows.
5. Show repeated readings tightly grouped around a biased result; contrast repeatability with accuracy.

Required error table:

| Situation | Direction under the stated simple model |
|---|---|
| Heat loss in electrical calibration, E known correctly | Measured deltaT down; calculated CF up |
| Uncorrected heat loss during reaction, valid CF fixed | Measured deltaT down; inferred heat magnitude down |
| CF used is too small | Calculated heat and magnitude of molar enthalpy down |
| Same additive thermometer offset on both readings | Temperature difference unchanged |
| More repeat trials with the same systematic fault | Better estimate of a biased mean; fault remains |

Explain that if several biases occur together, the net result needs a full model and is not guaranteed by this table.

### Episode 12 Fair fuel comparisons and sustainability
Target: 12-16 minutes. Anchor sets: Q23-Q24.

Teach: comparisons per mole, per gram and per useful energy output; operational versus lifecycle emissions; renewable feedstocks versus sustainable processes; methane leakage; land/food/water tradeoffs; circular use of wastes; appropriate green chemistry principles and SDGs. Use supplied data to support a conclusion and explicitly identify where data is insufficient for a stronger claim.

Manim scenes:
1. Normalize competing fuels to the same useful-energy output before comparing their masses or emissions.
2. Draw a system boundary around direct combustion, then widen it to include feedstock, processing and transport.
3. Track waste becoming an input to another process.
4. Build a comparison answer one evidence-based sentence at a time.

Checkpoint: a lower emission per unit of input energy does not automatically guarantee a lower emission per unit of useful output; efficiency also matters.

### Episode 13 Exam workshop A on fuels and combustion
Target: 20-25 minutes, or split if needed. Anchor sets: Q25-Q26.

Start with an unworked question view. Give a quiet attempt period and a clear instruction to pause. Then model reading the question, annotating units/conditions, selecting the method, showing working and checking plausibility. Allocate indicative marks to observable steps. Include a wrong solution that uses all gas as methane, and another that compares emissions on different useful-energy bases.

Retrieve food-energy scaling and catalyst-versus-enthalpy distinctions in short opening checks. Finish with an error-log entry the learner can copy.

### Episode 14 Exam workshop B on calorimetry and data evaluation
Target: 20-25 minutes, or split if needed. Anchor sets: Q27-Q28.

Integrate electrical calibration, limiting-reactant analysis, a temperature graph, enthalpy and evaluation of a product claim. Use a new hand-warmer dissolution context for the purity question rather than reproducing the exam's sodium-hydroxide-pellet investigation. Show why a wrong calibration factor can make a claim appear supported. Finish with a method-selection recap and a short diagnostic covering every central trap in the series.

## Original anchor question bank

See `questions/anchor_bank.md` (verbatim data, checked targets, mark focus and traps for Q01-Q28)
and `checks/verify_anchors.py` (independent numerical verification).

### Shared data and marking convention

Unless overridden in a question, use SLC = 25 degrees C and 100 kPa; Vm = 24.8 L mol^-1; c_water = 4.18 J g^-1 degree C^-1; C = 12.0, H = 1.0, O = 16.0. Use the molecular masses explicitly supplied. Food factors are carbohydrate 16, protein 17 and fat 37 kJ g^-1. Give full precision in intermediate work and sensible final significant figures. These are supplied educational values; do not quietly swap constants midway through a solution.

Indicative marks below specify the intended assessment demand; they are not official marking schemes. Award independent method steps where appropriate. Do not punish a carried-forward arithmetic error repeatedly if the later chemistry and method are correct. Before final production, make sure each displayed subpart's mark value sums to the declared total.

For every solution show an exact/unrounded computational value where useful and a suitably rounded reported answer. Do not force three significant figures on graph estimates or data that support only two. Make requested rounding explicit where the original stem would otherwise be ambiguous.

## Required worked-solution format

For every anchor problem:

1. Show the complete prompt and mark value before revealing the solution. Identify supplied data without highlighting the answer.
2. Give a natural pause of approximately 8-15 seconds for short checks; for longer problems explicitly invite the learner to pause the player rather than embedding several minutes of dead air.
3. Read the question for the requested quantity and units.
4. Sketch the physical or chemical situation where it clarifies the method.
5. Write the relevant balanced equation before using its ratio.
6. Select and explain the relationship, then substitute with units.
7. Show unrounded intermediate values and appropriate final rounding.
8. Check signs, units, conservation and plausibility.
9. Display an indicative marking breakdown and a concise final response.
10. Show the trap as a clearly labelled incorrect approach, then diagnose its first incorrect step.
11. Finish with a brief changed-condition prediction. Avoid turning it into an unrelated new topic.

Question worksheets must separate prompts from solutions so a student can attempt them without spoilers. The question ID must match across video, worksheet, answers and captions.

## Formula selection guide to teach and include in the recap

| Question asks for | Start with | Essential qualification |
|---|---|---|
| Amount from mass | n=m/M | Match mass units to molar-mass units |
| Amount from solution | n=cV | V in L for c in mol L^-1 |
| Amount from gas at SLC | n=V/24.8 | V in L; check temperature, pressure and gas composition |
| Limiting reactant | Compare n/coefficient | Use the balanced equation and all relevant reactants |
| Heat released from a fuel amount | E_released=n times absolute molar combustion enthalpy | Positive magnitude; use compatible product phases |
| Heat gained by water | q=mc deltaT | Use water mass; this alone omits apparatus heat |
| Electrical energy supplied | E=VIt | Time in seconds gives J with V and A |
| Calibration factor | CF=E/deltaT | Applies to the setup and contents calibrated |
| Heat gained by calibrated calorimeter | q_cal=CF deltaT | Include sign if cooling; match energy units |
| Reaction enthalpy estimate | q_rxn=-q_cal, then divide by appropriate amount/extent | State exactly what one mole refers to |
| Efficiency | useful output / total input x 100% | Define useful output and match units |
| Input needed for a specified output | input=useful output / efficiency_fraction | A lower efficiency requires more input |
| Experimental percentage yield | actual amount / theoretical amount x 100% | Theoretical amount comes from limiting-reactant stoichiometry |
| Active fraction from heat | measured heat / theoretical heat for a fully active sample | Requires complete reaction, matched conditions and negligible other heat effects |

## Manim visual design requirements

- Use Manim for equations, plots, molecule schematics, counters and apparatus diagrams. Visuals should expose relationships and changes, not merely decorate a narration.
- Use 16:9, 1920x1080 at 30 fps for final output unless the working environment requires an explicitly documented change. Use inexpensive draft renders first.
- Keep high contrast and generous margins. Aim for main explanatory text around 38-44 px-equivalent and supporting labels around 28-32 or larger; inspect an actual 1080p frame rather than trusting nominal font sizes.
- Reserve a caption-safe bottom area. Do not put critical equations or axes beneath subtitles.
- Use a consistent palette for reacting system, calorimeter/surroundings, useful energy, losses and unknown quantities. Reinforce every colour with labels, arrows or line styles so colour is not the only cue.
- Use consistent equation layout: relationship, substituted values with units, result. Keep the current unknown visually distinct.
- Preserve atom counts in molecule animations and coefficients in reaction diagrams. Do not make atoms vanish during a transform.
- Label microscopic pictures as schematic where they could be mistaken for literal molecular behaviour. Heat is energy transfer; avoid depicting it as a chemical substance.
- Label axes with quantity and unit; use a reaction-coordinate axis rather than time for energy profiles. Temperature graphs must use the actual question data.
- Show both signed enthalpy and positive released-energy magnitude explicitly when a lesson compares them.
- Do not use tiny full-page tables, rapidly scrolling derivations, unnecessary camera moves or excessive simultaneous animations.
- Keep the chemistry readable in grayscale screenshots and on a laptop/tablet screen.

## Narration and audio requirements

- Use clear, conversational English, approximately 125-150 words per minute, with slower delivery for equations and unfamiliar steps. Let concept density and actual audio duration determine timing.
- Narration should explain causal reasoning rather than read every visible symbol. Say 'amount of ethanol in moles', not simply 'n'.
- Keep separate written-math and spoken-text versions. Convert symbols, subscripts and units into correct spoken phrases before sending them to TTS.
- Use a configured and accessible TTS provider/voice. Verify the actual available model and supported API rather than inventing a model name or SDK call. Keep provider and voice configurable; do not hard-code credentials into source files.
- Generate and cache audio by stable scene ID and narration-content hash. Reuse unchanged clips; avoid paying to regenerate an entire episode after a small edit.
- Measure generated audio duration and use it to schedule Manim reveals and pauses. Never trim the narration to fit a guessed scene duration.
- Provide matching SRT or VTT subtitles. Review pronunciations of joules, kilojoules, enthalpy, calorimetry, molar, methane and chemical formulas.
- Default to no background music. Maintain consistent comfortable loudness and avoid clipped audio.
- If TTS access is genuinely unavailable, finish scripts, timing estimates and visual previews, record the blocker, and mark episodes without narration as incomplete. Do not deliver silent placeholders as completed narrated lessons.

## Production workflow and resume behaviour

First inspect the existing project, installed Manim/LaTeX/FFmpeg environment, available rendering resources and configured audio tools. Reuse a working setup. Do not assume that a cloud workspace can access files or tools on the user's personal computer. Verify compatibility against the actual installed versions and their documentation when needed.

Use an isolated project folder without overwriting unrelated work (layout: brief/ scripts/ storyboards/ questions/ solutions/ scenes/ shared/ audio/ captions/ renders/draft/ renders/final/ checks/ logs/ progress.json README.md).

Use a small reusable component library for equation layouts, unit cancellation, calorimeter diagrams, energy profiles, mole-ratio trays and temperature plots. Keep episode classes small enough to render/debug independently. Do not make one enormous scene spanning the entire series.

For each episode, complete these stages:
1. Write the learning objectives and map coverage IDs and question IDs.
2. Solve and verify questions before recording narration.
3. Write a complete narration script and a scene table: scene ID; objective; spoken text; on-screen objects; transitions; expected duration; source/answer checks.
4. Produce a 30-60 second proof scene to verify equation rendering, layout, voice and synchronization. This is a technical checkpoint, not a requirement to stop and request approval for every episode.
5. Generate/cache narration and create captions.
6. Implement Manim scenes and render low-resolution drafts.
7. Inspect representative stills from every scene and watch each full draft for content, pacing, synchronization and visual defects. Inspect every calculation and graph, not only the title card.
8. Correct problems, render final episodes and inspect the final outputs.
9. Update the progress manifest, output inventory and known-issues log before moving on.

The progress manifest should contain episode/scene IDs, current stage, input hashes, narration/audio paths and durations, rendered outputs, validation status and blockers. After interruption, read it and resume from the first incomplete stage. Do not regenerate completed verified scenes unnecessarily.

Prioritise a complete verified pilot episode before implementing all remaining visual code, but keep the whole-series outline and answer bank ready from the start. Do not silently drop later episodes if a session ends; leave a clear resumable checkpoint.

## Scientific and production acceptance checks

### Chemistry and numerical checks
- All equations balance atoms and charge where relevant, with correct states.
- Every thermochemical value names its basis: equation as written, per mole of specified substance, or per gram.
- The same physical event has consistent energy signs across system and surroundings.
- Bond breaking always absorbs energy in the explanation; bond formation releases it.
- Catalysts alter activation pathways without changing reaction deltaH.
- Limiting-reactant logic compares n/coefficient; no excess remaining is negative.
- Gas volume calculations use common stated conditions; SLC Vm is never applied directly to hot exhaust volume.
- Air/fuel mixtures use only the relevant component for reaction stoichiometry.
- Direct heat and fuel input use compatible energy units; efficiencies are between 0 and 100% under the supplied idealized models.
- Electrical times are in seconds for E=VIt; CF units and quantities are consistent.
- A calibration for different contents is not silently reused without an explicit question assumption.
- Temperature plots match the data, and corrected estimates are clearly distinguished from measured points.
- Every error explanation follows the actual affected measurement through the formula to the result.
- No hypothetical practice data is presented as measured data about a real product or fuel.
- Numerical solutions are checked independently of the displayed Manim text, preferably with a small calculation script and conservation/unit checks. Graph fits should be recomputed from their data.
- Every MC item has a unique valid answer. Every marking guide sums to the marks displayed.

### Media checks
- Each episode is a playable MP4 with the expected duration, video and audio streams.
- No missing LaTeX glyphs, clipped equations, overlapping labels, unreadable tables or broken animations.
- Narration describes the currently visible step; there is time to read the result before moving on.
- Captions match the final narration and do not obscure essential content.
- Silence appears only where intentionally provided for reflection, not because an audio file was lost.
- Draft/example footage is not mislabelled as final.
- The final README lists real output paths, episode titles, runtimes, question IDs and any genuine unresolved issue.

## Deliverables
1. Fourteen individually named final narrated MP4 episodes, or a clearly documented split into more episodes when necessary for comprehension.
2. A matching subtitle file and transcript for each episode.
3. A questions-only worksheet containing all original anchor questions and any validated added practice.
4. A separate worked-solutions document with indicative marks and explanations of each trap.
5. A concise formula-and-method sheet covering the scope, units and assumptions for each equation.
6. Editable Manim source, shared assets, narration scripts, cached audio and environment/dependency information sufficient to reproduce the renders.
7. A completed coverage matrix, numerical-check record and progress manifest.
8. A series index with viewing order, durations and links/paths to the actual files.

Do not claim the series is finished until every required coverage row appears in a verified episode and every required final output is present. If a capability is blocked, distinguish the completed files from the remaining production work clearly.

## Start now
Read this brief, inventory the available environment and sources, and create the project outline, progress manifest and question-answer checks. Then fully script and produce Episode 01 as the pilot, validate it and continue through the remaining episodes. Make routine implementation decisions yourself, keep short progress updates, and leave a resumable project state after each completed stage.
