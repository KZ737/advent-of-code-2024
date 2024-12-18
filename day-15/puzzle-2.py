import numpy as np

inputfile = open("./day-15/input.txt", "r")

"""
0 - empty space
1 - wall
2 - box left
3 - box right
9 - robot
We read the input map into a list of tuples, which we then convert to a numpy array. 0, 1, 2, 3, and 9 mean empty spaces, walls, left and right sides of boxes, and the robot, respectively.
We find the robot's starting position, then replace the 9 with a 0 (we will not update the map with the robot's position, but use function parameters to pass the position instead; skipping unnecessary array reads and writes increases performance).
"""
warehouseCharMap = str.maketrans({".": "00", "#": "11", "O": "23", "@": "90"})
warehouseMap = []
while line:=inputfile.readline().strip():
    warehouseMap.append(tuple(map(int, line.translate(warehouseCharMap))))
warehouseMap = np.array(warehouseMap, dtype=np.int8)
curPos = np.argwhere(warehouseMap==9)[0]
warehouseMap[*curPos] = 0

"""
We read the robot's moves into a tuple, where 1, 3, 2, and 4 mean up, down, left, and right, respectively.
"""
moveCharMap = str.maketrans("^v<>", "1324")
moveDirections = ""
for line in inputfile:
    moveDirections += line.strip().translate(moveCharMap)
moveDirections = tuple(map(int, moveDirections))

boxExtDict = {2: 1, 3: -1}
"""
The `canTheBoxMove` function takes as inputs the current state of the map, the box's position, the box's "extent", and the direction of the movement, and returns a boolean telling us whether the box in question can be moved in the given direction or not.
Since boxes take up 2 spaces in this map, we not only have to know the coordinate we are trying to move to, but we have to deal with the other side of the box as well. The box's extent describes exactly this: it is -1 if the box extends to the left of the input coordinate, and 1 if to the right.
For easier calculation, direction here is not using the previous numbering, but instead -1 and +1 mean up and down, respectively (for the `maketrans` function we needed to have each direction's value to be the same length, and this way was the most simple, although not the most consistent).
We iterate through both halves of the box, and check the space above or below them (depending on the direction).
    If that space is a wall for any of the halves, the box can't be moved, and we return False.
    If that space is another box, we recursively call this same function on that box. We use the `boxExtDict` dictionary to tell the function the extent of the box (e.g. if the map's value there is 2, the box extends to the right, and the dictionary has a value of 1). If this recursive call returns False for any of the two halves, we return False, since there is at least one block in the way.
    If we haven't returned False for the previous checks, that means there are no obstacles blocking our way, therefore we can push the box forward and we return True.
"""
def canTheBoxMove(curMap, boxPos, boxExt, direction):
    for horCoord in [boxPos[1], boxPos[1]+boxExt]:
        spaceToMoveTo = curMap[boxPos[0]+direction, horCoord]
        if spaceToMoveTo == 1:
            return False
        if spaceToMoveTo in [2, 3]:
            if not canTheBoxMove(curMap, [boxPos[0]+direction, horCoord], boxExtDict[spaceToMoveTo], direction):
                return False
    return True

"""
The `moveTheBox` function takes the same parameters as the `canTheBoxMove` function, and starts similarly as well, by iterating through the two halves and check the space we want to move the box to: if that place contains a box, we call the `moveTheBox` function recursively on that box. In either case, the place we want to move the box to will be empty, so we move the block to the given direction, then empty the space previously occupied.
"""
def moveTheBox(curMap, boxPos, boxExt, direction):
    for horCoord in [boxPos[1], boxPos[1]+boxExt]:
        spaceToMoveTo = curMap[boxPos[0]+direction, horCoord]
        if spaceToMoveTo in [2, 3]:
            curMap = moveTheBox(curMap, [boxPos[0]+direction, horCoord], boxExtDict[spaceToMoveTo], direction)
        curMap[boxPos[0]+direction, horCoord] = curMap[boxPos[0], horCoord]
        curMap[boxPos[0], horCoord] = 0
    return curMap

"""
The `move` function takes as inputs the current state of the map, the current position, and the direction of the next move, and it returns the resulting map and robot position.
First we define a `path` variable that contains everything ahead of the robot in the direction of the movement.
We also define a `moveDir` variable that contains the direction on the numpy array axes corresponding to the different directions (i.e. moving left means no movement on the 1st axis and decreasing the coordinate by 1 on the 2nd axis).
Then we check whether the first element in the path is 0, in which case we move forward (i.e. return the map unchanged, and update the robot's position according to the direction).
If it was not 0, we check whether it's a 1, in which case the robot ran into a wall, and it will not move forward (i.e. we return both the map and the robot's position unchanged).
If it was neither a 0 nor a 1, that means there is a box in front of the robot. In this case, we check if there are any empty spaces in the robot's path, and if there are none, it means the robot can't push the box, and remains at the same location.
If there are empty spaces, we save the location of the first one, and we also save the location of the first wall in the robot's path.
If the first wall occurs before the first empty space, that also means that the robot can't push the box(es), therefore it stays in the same place.
If the first wall occurs after the first empty space, then we check which direction we are pushing the box in:
    If we are moving the box to the left, we copy the blocks between the robot and the empty space one unit to the left (we also copy the robot's block, to delete the rightmost box-half we just moved). We return the new state of the map and the robot's new position.
    If we are moving the box to the right, we do the same, but in the other direction. I wanted to handle both left and right in one case, but I couldn't find a (simple) way to index the map that works for both.
    If we are not moving the box to neither to the left nor to the right, that means we want to move it vertically. We calculate the box's extent, then check if the box can be moved, and if it can be, we move it, and return the updated map and the robot's new position.
If we haven't returned already, it means we had a box in front of us that we couldn't move, so we return the map and the position both unchanged.
"""
def move(curMap, curPos, direction):
    match direction:
        case 1:
            path = curMap[curPos[0]-1::-1, curPos[1]]
            moveDir = np.array([-1, 0])
        case 3:
            path = curMap[curPos[0]+1::1, curPos[1]]
            moveDir = np.array([1, 0])
        case 2:
            path = curMap[curPos[0], curPos[1]-1::-1]
            moveDir = np.array([0, -1])
        case 4:
            path = curMap[curPos[0], curPos[1]+1::1]
            moveDir = np.array([0, 1])
    nextPos = curPos + moveDir
    if path[0] == 0:
        return (curMap, nextPos)
    if path[0] == 1:
        return (curMap, curPos)
    emptySpaces = np.where(path==0)[0]
    if emptySpaces.size:
        firstEmptySpace = emptySpaces[0]
        firstWall = np.where(path==1)[0][0]
        if firstEmptySpace < firstWall:
            if direction == 2:
                curMap[curPos[0], curPos[1]-1-firstEmptySpace:curPos[1]] = curMap[curPos[0], curPos[1]-firstEmptySpace:curPos[1]+1]
                return (curMap, nextPos)
            elif direction == 4:
                curMap[curPos[0], curPos[1]+1:curPos[1]+2+firstEmptySpace] = curMap[curPos[0], curPos[1]:curPos[1]+1+firstEmptySpace]
                return (curMap, nextPos)
            else:
                boxExt = boxExtDict[curMap[*nextPos]]
                if canTheBoxMove(curMap, nextPos, boxExt, direction-2):
                    curMap = moveTheBox(curMap, nextPos, boxExt, direction-2)
                    return (curMap, nextPos)
    return (curMap, curPos)

"""
We iterate through all moves from the input, updating the map and the robot's position in each step.
"""
for moveDirection in moveDirections:
    warehouseMap, curPos = move(warehouseMap, curPos, moveDirection)

"""
Since it will always be the left side of a box that is closest to the map's left edge (duh), for calculating the result, we can just use the coordinates of the cells with a value of 2.
We iterate through all these cells and add their GPS coordinates to our result counter.
"""
result = 0
for box in np.argwhere(warehouseMap==2):
    result += 100*box[0]+box[1]
print(result)


inputfile.close()