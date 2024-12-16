import numpy as np

inputfile = open("./day-10/input.txt", "r")

"""
We read the map from the input file into a numpy array. We also save the map's width/height N for later use (the map is an NxN matrix).
"""
topoMap = []
for line in inputfile:
    topoMap.append(list(map(int, list(line.strip()))))
topoMap = np.array(topoMap)
mapSize = topoMap.shape[0]

"""
We create an array of the same size as the map, `reachablePeaks`, filled with empty sets.
Each set will contain the peaks that can be reached from the corresponding location on the map.
For each peak (location where the value of the map is 9) we add its location to the same place in `reachablePeaks`.
"""
reachablePeaks = np.array([set() for i in range(topoMap.size)]).reshape((mapSize, mapSize))
for peakLoc in np.argwhere(topoMap==9):
    reachablePeaks[*peakLoc].add(tuple(peakLoc))

"""
The `processNeighbours` takes the topographical map, a pair of coordinates, and the height corresponding to the coordinates as inputs.
We iterate through all 4 directions, and if the resulting location is:
    1. within the bounds of the map (the first 2 checks), and
    2. has a height exactly 1 less than the coordinate we gave as the input,
then we add all the peaks reachable from the input coordinates to the set of reachable peaks of the location.
Note: we could calculate the height at the input coordinates in this function, but it is very easy to pass it as a parameter, which means we can skip a ton of lookups, saving some time.
"""
def processNeighbours(topoMap, curPos, curHeight):
    neighbours = []
    for i, j in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if (0 <= curPos[0]+i < mapSize) and (0 <= curPos[1]+j < mapSize) and (topoMap[curPos[0]+i, curPos[1]+j] == curHeight-1):
            [reachablePeaks[curPos[0]+i, curPos[1]+j].add(reachablePeak) for reachablePeak in reachablePeaks[*curPos]]
            neighbours.append((curPos[0]+i, curPos[1]+j))
    return

"""
From 9 to 1 we iterate through all the locations of the map of given height, and process their neighbours. In the end we will have a complete map of all peaks reachable from any given position.
"""
for i in range(9, 0, -1):
    for location in np.argwhere(topoMap==i):
        processNeighbours(topoMap, location, i)

"""
We iterate through the low points of the map (where the value is 0), and sum the number of peaks reachable from each location, which is our result.
"""
result = 0
for lowLoc in np.argwhere(topoMap==0):
    result += len(reachablePeaks[*lowLoc])

print(result)


inputfile.close()