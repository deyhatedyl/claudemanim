# E11 Temperature graphs, correction and experimental reasoning

Runtime 17:41. Narration transcript (matches the captions).

## [00:00] E11S01 Retrieval check

Welcome to episode eleven. Real calorimeters lose heat, and real thermometers aren't perfect. Today we'll learn to read temperature graphs, correct for heat lost while the reaction is happening, and reason carefully about errors.
Two quick checks. If heat escapes during an electrical calibration, is the calibration factor calculated too large or too small? And if a reaction raises the calorimeter's temperature, is delta H positive or negative? Pause and answer.  *(pause)*
Too large: the measured rise is smaller, and C F equals E over delta T. And delta H is negative, because the reaction transferred energy to the calorimeter.

## [00:52] E11S02 Reading a temperature-time graph

Here's real-looking data, from practice question Q twenty-one. Temperature is on the vertical axis, in degrees Celsius, and time is on the horizontal axis, in seconds. Each point is an actual measurement; we won't draw a decorative curve through them.
Before mixing, the temperature is steady at twenty-one point zero degrees. That's the baseline. Mixing happens at one hundred and twenty seconds.
After mixing, the temperature climbs quickly: twenty-three, twenty-five, twenty-six, and the highest reading, twenty-six point one degrees, at one hundred and eighty seconds.
After that, the readings fall slowly and steadily: twenty-five point nine, twenty-five point seven, twenty-five point five. The calorimeter is losing heat to the room. That steady fall is the cooling region.

## [01:45] E11S03 Why the highest reading is too low

Here's the problem. The calorimeter starts losing heat as soon as it's warmer than the room, which is while the reaction is still happening. So by the time the temperature peaks, some heat has already escaped.
That means the highest measured temperature is lower than the temperature the calorimeter would have reached if the reaction had been instantaneous and no heat had escaped. Using it would underestimate the temperature rise, and so underestimate the heat released.

## [02:19] E11S04 Extrapolating the cooling line

To estimate what the temperature would have been without that loss, we use the cooling region. Draw the best straight line through the cooling points. Here they lie exactly on a line.
The slope: the temperature falls from twenty-six point one to twenty-five point five degrees over one hundred and eighty seconds. That's negative zero point six over one hundred and eighty, or about negative zero point zero zero three three three degrees per second.
Now extend that line backwards, as a dashed line, to the moment of mixing at one hundred and twenty seconds. Going back sixty seconds adds sixty times zero point zero zero three three three, which is zero point two degrees. So the extrapolated temperature at mixing is twenty-six point three degrees.
Compare the two rises. Using the highest observed reading: twenty-six point one minus twenty-one point zero, which is five point one degrees. Using the extrapolated value: twenty-six point three minus twenty-one point zero, which is five point three degrees. The corrected rise is larger, because it adds back the heat lost while the reaction was happening.
Treat the extrapolated value as an estimate from a model. It assumes the cooling rate stays the same, and that the reaction happened at the moment of mixing. It's a better estimate than the raw maximum, not a perfect recovery of the true temperature.

## [03:58] E11S05 Practice Q21: corrected heat

Practice question Q twenty-one is worth five marks. You've seen the graph; pause the video and write the full solution.  *(pause)*
Part a: the cooling slope is negative zero point zero zero three three three degrees per second, and extrapolating back sixty seconds gives twenty-six point three degrees at mixing. Part b: the corrected rise is five point three degrees.
Part c: the corrected heat is six hundred and fifty times five point three: three thousand four hundred and forty-five joules. Since the temperature rise is a graph estimate to two significant figures, report it as about three point four kilojoules.
Part d: the highest observed temperature gives a rise of five point one degrees, and six hundred and fifty times five point one is three thousand three hundred and fifteen joules, about three point three kilojoules. That's an underestimate, because cooling had already started before the peak was recorded.
Marks: two for the correct region and extrapolation, one for the corrected rise, one for the corrected heat, and one for the comparison with its direction. The traps: using the observed maximum as if it were corrected, or reading twenty-six point three degrees itself as the temperature change.

## [05:37] E11S06 Drawing the extrapolation well

In an exam you'll often draw this line by hand, and real readings are rarely perfectly straight. Here's a hypothetical set of readings with a little scatter. Which points should your line follow?
Use only the steady cooling region. Leave out the points recorded while the temperature was still rising, because the reaction was still releasing heat then. A line dragged towards those points gets the wrong slope, and it extrapolates to the wrong value. And don't force the line through the highest point just because it's the highest.
Draw one straight line that balances the points, with roughly as many above it as below. Extend it with a ruler to a vertical line at the moment of mixing, read the temperature where they meet, and report it to a precision your graph can support.
If the cooling region curves, a straight-line extrapolation is less reliable. Use the part of the trend closest to the mixing time, and say that the corrected value is an estimate.

## [06:50] E11S07 When the temperature falls

The same idea works for an endothermic process, where the temperature falls. Here's a hypothetical example. The baseline is twenty-two point zero degrees, mixing happens at sixty seconds, the lowest reading is eighteen point nine degrees, and then the temperature creeps back up. Why does it rise again? Pause and think.  *(pause)*
Once the mixture is colder than the room, heat flows in from the surroundings, so it warms steadily. That warming began while the process was still absorbing heat, so the lowest reading isn't as low as it would have been without any heat gain.
So extrapolate the warming line back to the mixing time. It rises by zero point two degrees every sixty seconds, so going back sixty seconds from the lowest reading gives eighteen point seven degrees. The corrected change is eighteen point seven minus twenty-two point zero: negative three point three degrees, compared with negative three point one from the lowest reading.
The temperature change is negative, so q for the calorimeter is negative, and delta H for the process is positive. Uncorrected heat gain would make the size of that fall, and the size of delta H, too small.

## [08:22] E11S08 Heat loss during calibration versus during the reaction

Heat can escape at two different stages, and the effects go in different directions. That's why "heat loss makes the answer smaller" isn't a reliable rule.
During calibration, the electrical energy is known correctly. Heat loss makes the measured temperature rise smaller, so C F, which is E over delta T, comes out larger.
During the reaction, with a valid calibration factor fixed, uncorrected heat loss makes the measured rise smaller. Then q, which is C F times delta T, is smaller, so the calculated heat released, and the size of the molar enthalpy, are smaller too.
Same physical cause, opposite effects on the calculated quantity, because the temperature rise sits in the denominator in one formula and the numerator in the other. Always follow the measurement through the actual formula.

## [09:20] E11S09 Systematic and random errors; accuracy and precision

Some vocabulary, used precisely. A random error makes repeated measurements scatter unpredictably, sometimes high and sometimes low. A systematic error pushes every result in the same direction by a consistent amount or proportion.
Accuracy is how close a result is to the true value. Precision describes how closely repeated results agree with each other. Here's a set of results that are tightly grouped, so they're precise, but they're all too low, so they're not accurate. That's the fingerprint of a systematic error.
Repeatability means the same person, method and equipment get closely agreeing results when the experiment is repeated. Good repeatability shows precision, but it doesn't prove accuracy. Validity asks whether the experiment actually measures what it claims to, under suitable controlled conditions.
Averaging more repeats reduces the effect of random errors. It does nothing about a systematic error: you just get a better estimate of a biased value.

## [10:26] E11S10 Resolution, mistakes and outliers

One more measurement idea that exams test directly: resolution. Which has the higher resolution, a thermometer marked every one degree, or a digital probe that reads to zero point one of a degree? Pause and decide.  *(pause)*
Resolution is the smallest change an instrument can show, and it's always stated with a unit. For a scale, it's the smallest graduation: one degree for that thermometer. For a digital display, it's the last digit it can show: zero point one degree for the probe, or zero point zero one gram for a balance that reads to two decimal places. The probe has the higher resolution, because it records finer increments.
But higher resolution isn't the same as accuracy. A probe that reads to zero point one of a degree can still be badly calibrated. Resolution does limit how precisely you can quote a temperature change, which is why a rise read from a coarse thermometer supports fewer significant figures.
Two last terms. A mistake, such as misreading a scale or spilling some solution, isn't an error in the scientific sense: identify it, leave that result out, and repeat the measurement. And a single outlier in an otherwise precise set isn't evidence of a systematic error. Investigate it, and report how you treated it.

## [12:06] E11S11 Practice Q22: a wrong CF and a thermometer offset

Practice question Q twenty-two is worth five marks. Pause the video and work through it.  *(pause)*
Part a. The spreadsheet uses four hundred and fifty: four hundred and fifty times four point zero zero is one thousand eight hundred joules, divided by zero point zero four zero zero moles is forty-five thousand joules per mole. So the reported value is negative forty-five point zero kilojoules per mole. With the valid five hundred, the heat is two thousand joules, and the corrected value is negative fifty point zero kilojoules per mole.
Part b. Repeating the experiment doesn't fix this. Every repeat uses the same wrong calibration factor, so the results agree closely with each other: good repeatability. But they share the same systematic bias, so they stay inaccurate.
Part c. A thermometer that reads one point five degrees too high, on both readings, adds one point five to the initial and to the final temperature. The difference is final plus one point five, minus initial plus one point five, and the one point fives cancel. Delta T is unchanged.
But don't over-generalise. That cancellation only works for an identical additive offset. A thermometer whose scale is stretched, reading too many degrees per real degree, would change delta T.
Marks: two for the two enthalpies, one for the repetition explanation, and two for the offset conclusion with the subtraction reasoning. The traps: equating repeatability with accuracy, and assuming every thermometer error changes a temperature difference.

## [14:09] E11S12 The error-direction table

Here's a summary table. Each row follows one fault through the formula, under the simple model where only that fault is present.
Heat loss during electrical calibration, with E known correctly: the measured rise goes down, so the calculated calibration factor goes up. Uncorrected heat loss during the reaction, with a valid calibration factor: the measured rise goes down, so the inferred heat, and its magnitude, go down.
A calibration factor that's too small: the calculated heat and the magnitude of the molar enthalpy go down. The same additive thermometer offset on both readings: the temperature difference is unchanged. And more repeat trials with the same systematic fault: a better estimate of a biased mean, with the fault still there.
One caution. If several faults act together, the net effect needs a full model. They can partly cancel or add up, so the table alone can't tell you the overall direction.
And when an exam asks for an improvement, be specific: insulate the lid and sides, calibrate with the same volume of solution that will be used in the reaction, record temperatures more often and extrapolate, or repeat with fresh solutions and average the results.

## [15:35] E11S13 Checkpoint: which improvement fixes which error?

Checkpoint. Match each improvement to the problem it addresses. One: insulate the lid and sides. Two: calibrate using the same volume of solution as the reaction. Three: record temperatures more often and extrapolate. Four: repeat with fresh solutions and average. Pause and match them.  *(pause)*
Insulation reduces heat exchange with the surroundings, a systematic error. Calibrating with the same volume makes the calibration factor valid for the actual conditions, removing another systematic error. More frequent readings define the cooling line better, so the extrapolated temperature is more reliable. And repeating and averaging reduces the effect of random errors only. It can't remove a systematic error, which is why the first two improvements matter most when results are precise but biased.

## [16:40] E11S14 Recap and closing recall

To recap. Read the graph's baseline, mixing time and cooling region. Extend the cooling trend back to the mixing time to estimate the corrected temperature, and treat it as a model-based estimate. Trace every error through the actual formula, and remember: precise isn't the same as accurate.
Closing recall. A cooling line has a slope of negative zero point zero zero two degrees per second. Extrapolating back fifty seconds to the mixing time, how much does the temperature increase?  *(pause)*
Fifty seconds times zero point zero zero two degrees per second is zero point one degrees, added to the start of the cooling line. Next episode: comparing fuels fairly, and what sustainability really requires.
