import numpy as np

inputfile = open("./day-11/input.txt", "r")

"""
We read the input file into a list of numbers, each corresponding to a stone.
"""
stones = list(map(int, inputfile.readline().strip().split(" ")))

"""
The `processStone` function takes the number of the stone and the number of remaining blinks as inputs, and returns the number of stones you get from the original stone after the given number of blinks, calculated iteratively.
If there are no blinks remaining, the stone will not change, therefore the number of stones we get from it is 1.
If there are blinks remaining, we first check whether the stone's number is a single digit or not: if it is, we process it using a special function, creatively named `processSingleDigit`.
If the number has more than one digits, and an even number of them, the result will be the sum of the values of `processStone` for the two halves with 1 less blink remaining.
If the number has more than one digits, and an odd number of them, the result will the the value of `processStone` for the number multiplied by 2024 with 1 less blink remaining.
"""
def processStone(stoneNum, blinksRemaining):
    if blinksRemaining == 0:
        return 1
    stoneNumLength = len(str(stoneNum))
    if stoneNumLength == 1:
        return processSingleDigit(stoneNum, blinksRemaining)
    if stoneNumLength%2 == 0:
        return processStone(int(str(stoneNum)[:stoneNumLength//2]), blinksRemaining-1) + processStone(int(str(stoneNum)[stoneNumLength//2:]), blinksRemaining-1)
    return processStone(2024*stoneNum, blinksRemaining-1)

"""
`spawnDict` contains some hand-calculated data to speed up the process.
For each digit corresponds a list of tuples about the results of a stone having that digit. Each tuple consists of 3 numbers: N1 stones of N2 are produced from the original number after N3 blinks.
For example: 3 --> 6072 --> 60, 72 --> 6, 0, 7, 2, therefore we get 1 of 0, 1 of 2, 1 of 6, and 1 of 7, all after 3 blinks, leading to the list `[(1, 0, 3), (1, 2, 3), (1, 6, 3), (1, 7, 3)]`.
We must note that the digit 8 is trickier than the others, as the numbers it spawns are not all created at the same time:
8 --> 16192 --> 32772608 --> 3277, 2608 --> 32, 77, 26, 8 --> 3, 2, 7, 7, 2, 6
                                                          --> 16192...
Therefore the number 8 results in 2 of 2, 1 of 3, 1 of 6, and 2 of 7 after 5 blinks each, but 1 of 8 after just 4 blinks.
"""
spawnDict = {0: [(1, 1, 1)],
             1: [(1, 0, 3), (2, 2, 3), (1, 4, 3)],
             2: [(1, 0, 3), (2, 4, 3), (1, 8, 3)],
             3: [(1, 0, 3), (1, 2, 3), (1, 6, 3), (1, 7, 3)],
             4: [(1, 0, 3), (1, 6, 3), (1, 8, 3), (1, 9, 3)],
             5: [(2, 0, 5), (2, 2, 5), (1, 4, 5), (3, 8, 5)],
             6: [(1, 2, 5), (2, 4, 5), (2, 5, 5), (1, 6, 5), (1, 7, 5), (1, 9, 5)],
             7: [(1, 0, 5), (2, 2, 5), (1, 3, 5), (2, 6, 5), (1, 7, 5), (1, 8, 5)],
             8: [(1, 8, 4), (2, 2, 5), (1, 3, 5), (1, 6, 5), (2, 7, 5)],
             9: [(1, 1, 5), (1, 3, 5), (1, 4, 5), (2, 6, 5), (2, 8, 5), (1, 9, 5)]}

"""
For some speed, we will utilise a 2D array that will contain the number of stones resulting from a given digit after a given number of blinks.
We initialize the array with -1s, and we fill up some basic values obtained during the making of that monster above.
"""
dp = np.full((10, 76), -1, dtype=int)
dp[:, 0:2] = 1
dp[1:5, 2] = 2
dp[5:, 2] = 1
dp[5:, 3] = 2
dp[5:, 4] = 4

"""
The `processSingleDigit` takes a single-digit number and the number of blinks remaining as inputs, and returns the number of stones resulting from a stone of the input number after the input amount of blinks.
First we check if the number we're interested in can be found in the array, in which case we return that number.
Otherwise, we go through all the numbers that we get from this one, calculate the number of stones they produce (after a reduced number of blinks, of course), multiply them by how many of them were made, and sum these up to get the result for the input number, which we then save in our array.
"""
def processSingleDigit(stoneNum, blinksRemaining):
    if dp[stoneNum, blinksRemaining] != -1:
        return dp[stoneNum, blinksRemaining]
    res = 0
    for spawnedNum in spawnDict[stoneNum]:
        res += spawnedNum[0]*processSingleDigit(spawnedNum[1], blinksRemaining-spawnedNum[2])
    dp[stoneNum, blinksRemaining] = res
    return res

"""
We go through all the original stones, calculate the number of stones they produce after 75 timesteps, and sum these to get the final result.
"""
print(sum(map(lambda x: processStone(x, 75), stones)))


inputfile.close()