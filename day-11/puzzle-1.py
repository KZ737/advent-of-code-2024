inputfile = open("./day-11/input.txt", "r")

"""
We read the input file into a list of numbers, each corresponding to a stone.
"""
stones = list(map(int, inputfile.readline().strip().split(" ")))

"""
The `processStone` function takes the number of a stone as an input, and returns a list of stones that we get after blinking once.
As given:
    1. if the stone's number is 0, the result will be a stone with a number of 1,
    2. if the stone's number has an even number of digits, it will split into two, containing the two halves of the original number,
    3. and if neither of the two previous conditions were met, the stone's number will be multiplied by 2024.
Yes, this is the dumb way to solve the problem, but it worked for the first part... for something more sophisticated, check my solution for the second part.
"""
def processStone(stoneNum):
    if stoneNum == 0:
        return [1]
    stoneNumLength = len(str(stoneNum))
    if stoneNumLength%2 == 0:
        return [int(str(stoneNum)[:stoneNumLength//2]), int(str(stoneNum)[stoneNumLength//2:])]
    return [2024*stoneNum]

"""
For all timesteps, we take a new list of stones, we iterate through each current stone, and append the resulting stone(s) to the new list, which becomes our current list in the next timestep.
The result is the number of stones, i.e. the length of the `stones` list after 25 timesteps.
"""
for _ in range(25):
    newStoneList = []
    for stone in stones:
        newStoneList += processStone(stone)
    stones = newStoneList
print(len(stones))


inputfile.close()