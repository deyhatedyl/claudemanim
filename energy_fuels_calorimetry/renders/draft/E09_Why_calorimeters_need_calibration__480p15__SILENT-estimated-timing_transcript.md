# E09 Why calorimeters need calibration

Runtime 11:42. Narration transcript (matches the captions).

## [00:00] E09S01 Retrieval check

Welcome to episode nine. Last time we assumed that all the useful heat went into the water. In a real calorimeter, that isn't quite true, and today we'll fix it with a technique called calibration.
A quick check first. How much energy warms one hundred and twenty point zero grams of water by four point zero zero degrees? Pause and calculate.  *(pause)*
Using q equals m c delta T: one hundred and twenty point zero times four point one eight times four point zero zero, which is two thousand and six point four joules. Keep that number in mind; it's close to, but not the same as, what a real calorimeter needs.

## [00:57] E09S02 More than the water gets heated

Here's a solution calorimeter: an insulated cup with a lid, a measured volume of water, a stirrer, a temperature probe, and an electric heater.
When energy goes in, it doesn't only warm the water. It also warms the inside of the cup, the probe, the stirrer and the heater itself. Those parts are part of what heats up, so they absorb some of the energy too.
So instead of m c delta T for the water alone, we use a single number for the whole setup: the calibration factor, C F. It's the energy needed to raise the temperature of the calorimeter and its contents by one degree Celsius, in joules per degree.
The calibration factor belongs to this particular calorimeter with these particular contents. Change the cup, the probe, or the amount of liquid inside, and the calibration factor changes too.

## [02:00] E09S03 Electrical calibration: E = VIt, then CF = E / delta T

To find the calibration factor, we put in a known amount of energy and measure the temperature rise. An electric heater is ideal, because we can measure the energy very precisely.
The electrical energy equals voltage times current times time: E equals V times I times t. Voltage in volts, current in amps, and time in seconds. Volts times amps gives watts, which are joules per second, so multiplying by seconds leaves joules.
Time must be in seconds. A four-minute heating period is two hundred and forty seconds. Using four instead of two hundred and forty would make the energy sixty times too small.
Then the calibration factor is the energy supplied divided by the temperature rise it caused: C F equals E over delta T, in joules per degree Celsius.

## [02:58] E09S04 Stacking heat capacities and the lower bound

We can think of the calibration factor as two parts stacked together. The water's part is its mass times its specific heat capacity. The apparatus part is the energy per degree needed by the cup, probe, stirrer and heater.
Adding them gives the calibration factor. This simple model assumes the parts just add, and that their heat capacities don't change over the small temperature range we use.
Here's a powerful check. The apparatus always needs some energy to warm up, so its part is positive. That means a correctly measured calibration factor must be larger than the water's part alone: C F is at least m c for the water.
If a calculated calibration factor comes out smaller than the water alone could account for, something has gone wrong in the measurements or the calculation.

## [03:58] E09S05 Practice Q17, part 1: calibrate, then use it

Practice question Q seventeen is worth six marks. Pause the video and work through it.  *(pause)*
Part a. The electrical energy: six point zero zero volts times one point five zero amps times two hundred and forty seconds is two thousand one hundred and sixty joules. The temperature rose four point zero zero degrees, so the calibration factor is two thousand one hundred and sixty divided by four point zero zero: five hundred and forty joules per degree Celsius.
Plausibility check: the water alone needs one hundred and twenty point zero times four point one eight, which is five hundred and one point six joules per degree. Five hundred and forty is a bit larger, exactly as the model requires.
Part b. The apparatus contribution is the difference: five hundred and forty minus five hundred and one point six, which is thirty-eight point four joules per degree. It's small, but not zero.
Part c. In a later experiment with the same calorimeter and contents, the temperature rises five point six zero degrees. The heat gained by the calorimeter is the calibration factor times the rise: five hundred and forty times five point six zero, which is three thousand and twenty-four joules, about three point zero two kilojoules.

## [05:44] E09S06 Changing the contents changes CF

Part d. Now the water is increased to one hundred and fifty point zero grams, with the same cup, probe and stirrer. Can we still use five hundred and forty?
No. The water's part grows: one hundred and fifty point zero times four point one eight is six hundred and twenty-seven point zero joules per degree. The apparatus part stays at thirty-eight point four, assuming the heat capacities simply add and don't change. So the new calibration factor is six hundred and sixty-five point four, about six hundred and sixty-five joules per degree.
Marks for question seventeen: two for the energy and calibration factor, one for the apparatus contribution, one for the later heat, and two for the new calibration factor. The trap is keeping five hundred and forty after changing the contents, or using m c delta T for the water as if it included the apparatus.
So a calibration factor can only be reused if the calorimeter and its contents match the calibration. In an exam, a question will either say the setup is matched, or give you enough information to adjust it.

## [07:05] E09S07 Heat loss during calibration: follow the formula

Suppose some heat escapes during the electrical calibration. Which way does that push the calibration factor? Don't guess. Follow the formula.
The electrical energy is measured from the voltage, current and time, so it's correct: it doesn't change. But some of that energy leaks out instead of warming the calorimeter, so the measured temperature rise is smaller than it should be.
The calibration factor is E divided by delta T. The top stays the same, and the bottom gets smaller, so the calibration factor comes out larger than the true value.
This surprises many students, because they've memorised "heat loss makes the answer smaller". That's true for some quantities and false for others. The only reliable method is to trace the affected measurement through the actual formula.
Checkpoint. During a calibration, the student records the heating time as two hundred seconds when it was really two hundred and forty. Will the calibration factor be too big or too small? Pause and trace it through.  *(pause)*
Too small. A shorter recorded time gives a smaller calculated E. With the same measured delta T, E over delta T is smaller.

## [08:36] E09S08 Practice Q18: an impossible calibration factor

Practice question Q eighteen is worth four marks. Pause the video and decide what you'd write.  *(pause)*
Start with the lower bound. One hundred point zero grams of water alone needs one hundred point zero times four point one eight: four hundred and eighteen joules per degree. The cup and probe have a positive heat capacity, so the true calibration factor must be more than four hundred and eighteen. Three hundred and sixty is less, so it's inconsistent with this setup.
Now the student's explanation. Heat loss during calibration makes the measured temperature rise smaller, and that makes E over delta T larger. So heat loss would push the calibration factor up, not down. It can't explain a value that's too low.
What could make it too low? Anything that makes the calculated E too small, or the measured delta T too large. For example, an overestimated temperature rise, perhaps from a misread thermometer, or an underestimated electrical energy, such as a time, current or voltage recorded too low.
Marks: one for the lower bound, one for concluding that three hundred and sixty is inconsistent, one for the heat-loss direction, and one for a valid error. Notice the pattern: a full-credit answer always says which measurement is affected, which way it moves, and what that does to the calculated result.

## [10:25] E09S09 Recap and closing recall

To recap. A calorimeter's calibration factor is the energy needed per degree for the whole setup and its contents. Find it electrically, with E equals V times I times t, with t in seconds, then C F equals E over delta T. It must exceed the water's m c, and it only applies to matching contents. When something goes wrong, trace it through the formula.
Closing recall. A heater runs at twelve point zero volts and two point zero zero amps for five minutes, and the temperature rises six point zero degrees. What is the calibration factor?  *(pause)*
Five minutes is three hundred seconds. E equals twelve point zero times two point zero zero times three hundred: seven thousand two hundred joules. Divided by six point zero degrees, the calibration factor is one thousand two hundred joules per degree. Next episode: using a calibrated calorimeter to measure the enthalpy change of a reaction.
