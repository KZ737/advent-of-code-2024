import numpy as np
from tqdm import tqdm

inputfile = open("./day-6/input.txt", "r")

"""
We read the map into a numpy array where empty spaces are denoted by 0s, obstacles by 1s, and the guard is by a 2.
"""
firstline = inputfile.readline().strip()
mapSize = len(firstline)
inputMap = np.empty((mapSize, mapSize), dtype=np.int8)
firstline = list(map(int, firstline.replace(".", "0").replace("#", "1").replace("^", "2")))
lineCount = 0
inputMap[lineCount] = firstline
for line in inputfile:
    lineCount += 1
    inputMap[lineCount] = list(map(int, line.strip().replace(".", "0").replace("#", "1").replace("^", "2")))
startPos = [np.where(inputMap==2)[0][0], np.where(inputMap==2)[1][0]]


"""
The `moveMod` function takes the current state of the map, the direction the guard is going, and the guard's history as an input.
Directions: 0 -- up, 1 -- down, 2 -- left, 3 -- right
We calculate the current position of the guard by finding the 2 in the map.
We calculate the path ahead of the guard by slicing the array in the proper dimensions depending on the direction. We also save the next direction.
We look for obstacles in the guard's path by searching for 1s in her path.
If we found any number of 1s, we take the first, and calculate the coordinate based on its location in the guard's path and the guard's location.
    Then we move the guard to just before the obstacle, and mark every space on the map between the guard's previous and new location with 9 (including the previous but not the new location), denoting visited spaces.
    We also add the current direction to all the newly visited spaces in the history array.
    Then we return the current state of the map and the next direction.
If we did not found any 1s, we set all the spaces ahead of the guard, as well as her current position, to 9, then return the (final) map with a "direction" of 0: this denotes that we are finished.

The `move` function works very similarly to `moveMod`, but it doesn't modify the map in the process, increasing performance: it uses an extra argument and an extra entry in its return value to communicate the position of the guard.
It also uses a history argument which is a set of tuples containing each coordinate the guard's been to and the directions she was going in.
When the function is called, we check if the guard has been in this space going in the same direction before, if yes, we return 5: this denotes that we found a loop.
"""
def moveMod(curMap, direction):
    curPos = [np.where(curMap==2)[0][0], np.where(curMap==2)[1][0]]
    match direction:
        case 1:
            path = curMap[curPos[0]-1::-1, curPos[1]]
            obstacleDir = np.array([-1, 0])
            nextDir = 4
        case 2:
            path = curMap[curPos[0]+1::1, curPos[1]]
            obstacleDir = np.array([1, 0])
            nextDir = 3
        case 3:
            path = curMap[curPos[0], curPos[1]-1::-1]
            obstacleDir = np.array([0, -1])
            nextDir = 1
        case 4:
            path = curMap[curPos[0], curPos[1]+1::1]
            obstacleDir = np.array([0, 1])
            nextDir = 2
    obstacles = np.where(path==1)[0]
    if len(obstacles):
        obstacleCoords = curPos + obstacles[0]*obstacleDir
        if obstacleDir[0]:
            curMap[curPos[0]:obstacleCoords[0]:obstacleDir[0], curPos[1]] = 9
        else:
            curMap[curPos[0], curPos[1]:obstacleCoords[1]:obstacleDir[1]] = 9
        curMap[obstacleCoords[0], obstacleCoords[1]] = 2
    else:
        if obstacleDir[0]:
            curMap[curPos[0]::obstacleDir[0], curPos[1]] = 9
        else:
            curMap[curPos[0], curPos[1]::obstacleDir[1]] = 9
        nextDir = 0
    return (curMap, nextDir)


def move(curMap, curPos, direction, history):
    if (tuple(curPos), direction) in history:
        return (curMap, curPos, 5, history)
    history.add((tuple(curPos), direction))
    match direction:
        case 1:
            path = curMap[curPos[0]-1::-1, curPos[1]]
            obstacleDir = np.array([-1, 0])
            nextDir = 4
        case 2:
            path = curMap[curPos[0]+1::1, curPos[1]]
            obstacleDir = np.array([1, 0])
            nextDir = 3
        case 3:
            path = curMap[curPos[0], curPos[1]-1::-1]
            obstacleDir = np.array([0, -1])
            nextDir = 1
        case 4:
            path = curMap[curPos[0], curPos[1]+1::1]
            obstacleDir = np.array([0, 1])
            nextDir = 2
    obstacles = np.where(path==1)[0]
    if len(obstacles):
        obstacleCoords = curPos + obstacles[0]*obstacleDir
        curPos = obstacleCoords
    else:
        nextDir = 0
    return (curMap, curPos, nextDir, history)



"""
We create a set for the guard's history, as described above for the `move` function. It will contain tuples of the form ((xCoord, yCoord), direction).
Then, given a map, we move the guard through it until we either find that she went off the map (direction == 0) or that she is in a loop (direction == 5). If we found a loop, we return 1, otherwise we return 0.
"""
def checkForLoop(curMap):
    guardMapHistory = set()
    direction = 1
    curPos = startPos
    while direction in [1, 2, 3, 4]:
        curMap, curPos, direction, guardMapHistory = move(curMap, curPos, direction, guardMapHistory)
    if direction == 5:
        return 1
    else:
        return 0

"""
We take a copy of the original map, and walk the guard through it: all the places she visited (except her starting position) are marked as potentially loop-inducing if an obstacle is placed on them. (Places outside of her path on the original map are irrelevant in terms of the problem, since placing an obstacle on them has no effect on the guard's route.)
"""
guardMap = np.copy(inputMap)
direction = 1
while direction in [1, 2, 3, 4]:
    guardMap, direction = moveMod(guardMap, direction)
potentialPlaces = np.argwhere((guardMap==9) & (inputMap!=2))


"""
We loop through all the potentially loop-inducing places, construct a new map from the original, adding an obstacle to the candidate position, and then checking if it actually results in a loop. We increment our result counter based on the loop check.
"""
result = 0
for potentialPlace in tqdm(potentialPlaces):
    guardMap = np.copy(inputMap)
    guardMap[potentialPlace[0], potentialPlace[1]] = 1
    result += checkForLoop(guardMap)


print(result)


inputfile.close()