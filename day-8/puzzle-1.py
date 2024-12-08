import itertools

inputfile = open("./day-8/input.txt", "r")

"""
From the input file we construct a dictionary, with the keys being the frequencies and the corresponding values being the coordinates of the towers of those frequencies.
"""
antennae = {}
lineCount = 0
for line in inputfile:
    mapLine = list(line.strip())
    for i, ant in enumerate(mapLine):
        if ant != ".":
            if ant not in antennae.keys():
                antennae.update({ant: [(lineCount, i)]})
            else:
                antennae[ant].append((lineCount, i))
    lineCount += 1

"""
The `getAntinodes` function takes the coordinates of two antennae and the size of the map as inputs, then calculates the positions of the two antinodes, checks if they are within the map limits, and returns a list of all antinodes within limits.
"""
def getAntinodes(ant1, ant2, limit):
    locDiff = (ant2[0]-ant1[0], ant2[1]-ant1[1])
    ans = []
    for an in [(ant1[0]-locDiff[0], ant1[1]-locDiff[1]), (ant2[0]+locDiff[0], ant2[1]+locDiff[1])]:
        if 0 <= an[0] < limit and 0 <= an[1] < limit:
            ans.append(an)
    return ans

"""
We calculate the size of the map from the length of the last line from the input that we processed.
We define an `antinodes` set that will contain all the locations that have antinodes.
"""
mapSize = len(mapLine)
antinodes = set()

"""
We iterate through all the frequencies, and in each frequency we create an iterator for all pairs of antennae using that frequency, using `itertools.combinations`.
We iterate through all combinations of antennae, use the `getAntinodes` function to get their corresponding antinodes, which we add to the `antinodes` set.
"""
for places in antennae.values():
    for antPair in itertools.combinations(places, 2):
        for an in getAntinodes(*antPair, mapSize):
            antinodes.add(an)

"""
If 3 nested for loops look ugly for the reader (even though in this case they are pretty fast), you can "hide" them using list comprehension. Obviously they are there, but the missing indentation makes it look nicer lol
"""
# [[[antinodes.add(an) for an in getAntinodes(*antPair, mapSize)] for antPair in itertools.combinations(places, 2)] for places in antennae.values()]

"""
The result is the length of the set.
"""
print(len(antinodes))


inputfile.close()