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
The `getAntinodes` function takes the coordinates of two antennae and the size of the map as inputs, then starts going from the first one in the direction directly away from the second one, with steps exactly the distance between the two. It adds the antinode to a list, then calculates the position of the next antinode in this direction. It does this until the calculated coordinates are outside of the map. Then we do the same in the other direction. The function then returns the list of the coordinates of the computed antinodes.
"""
def getAntinodes(ant1, ant2, limit):
    locDiff = (ant2[0]-ant1[0], ant2[1]-ant1[1])
    ans = []
    backwards = ant1
    while 0 <= backwards[0] < limit and 0 <= backwards[1] < limit:
        ans.append(backwards)
        backwards = (backwards[0]-locDiff[0], backwards[1]-locDiff[1])
    forward = ant2
    while 0 <= forward[0] < limit and 0 <= forward[1] < limit:
        ans.append(forward)
        forward = (forward[0]+locDiff[0], forward[1]+locDiff[1])
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