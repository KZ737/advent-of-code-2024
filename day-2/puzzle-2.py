import numpy as np

inputfile = open("./day-2/input.txt", "r")
safeCount = 0
"""
Parse each line into a list of ints which we then convert into a numpy array and calculate the differences between subsequent elements.
Then we check if the series is monotonic by taking the sign of each difference, then getting all unique elements of this array: if there are more than 1 elements in this array, there must have been more than 1 signs to the differences, meaning it cannot be strictly monotonic.
We also check if there is any difference smaller than 1 or larger than 3 (in absolute value) by creating an array from all the differences outside of this interval and if the resulting array has any elements, the sequence does not meet the criteria.
We increment our counter if either of the following criteria are met:
    1. both our checks returned true
    2. removing one element from the numpy array results in an array that passes both checks
"""
for line in inputfile:
    sequence = np.array(list(map(int, line.strip().split())))
    diffs = np.diff(sequence)
    monotonic = np.unique(np.sign(diffs)).size == 1
    diffSpacingGood = diffs[(np.abs(diffs) < 1) | (np.abs(diffs) > 3)].size == 0
    if not (monotonic and diffSpacingGood):
        for i in range(sequence.size):
            newDiffs = np.diff(np.delete(sequence, i))
            monotonic = np.unique(np.sign(newDiffs)).size == 1
            diffSpacingGood = newDiffs[(np.abs(newDiffs) < 1) | (np.abs(newDiffs) > 3)].size == 0
            if (monotonic and diffSpacingGood):
                safeCount += 1
                break
    else:
        safeCount += 1

print(safeCount)

inputfile.close()