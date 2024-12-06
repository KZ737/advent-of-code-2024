import numpy as np

inputfile = open("./day-6/input.txt", "r")

"""
We read the map into a numpy array where empty spaces are denoted by 0s, obstacles by 1s, and the guard is by a 2.
"""
firstline = inputfile.readline().strip()
mapSize = len(firstline)
guardMap = np.empty((mapSize, mapSize), dtype=np.int8)
firstline = list(map(int, firstline.replace(".", "0").replace("#", "1").replace("^", "2")))
lineCount = 0
guardMap[lineCount] = firstline
for line in inputfile:
    lineCount += 1
    guardMap[lineCount] = list(map(int, line.strip().replace(".", "0").replace("#", "1").replace("^", "2")))


"""
The move function takes the current state of the map and the direction the guard is going as an input.
Directions: 0 -- up, 1 -- down, 2 -- left, 3 -- right
We calculate the current position of the guard by finding the 2 in the map.
We calculate the path ahead of the guard by slicing the array in the proper dimensions depending on the direction. We also save the next direction.
We look for obstacles in the guard's path by searching for 1s in her path.
If we found any number of 1s, we take the first, and calculate the coordinate based on its location in the guard's path and the guard's location.
    Then we move the guard to just before the obstacle, and mark every space on the map between the guard's previous and new location with 9 (including the previous but not the new location), denoting visited spaces.
    Then we return the current state of the map and the next direction.
If we did not found any 1s, we set all the spaces ahead of the guard, as well as her current position, to 9, then return the (final) map with a "direction" of 0: this denotes that we are finished.
"""
def move(curMap, direction):
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


"""
With a starting direction of 1 (up), we move through the map until we get a direction of 0 from the move function.
Following this, we count the number of 9s in the final map.
"""
direction = 1
while direction:
    guardMap, direction = move(guardMap, direction)
print(np.count_nonzero(guardMap==9))

inputfile.close()