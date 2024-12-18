import numpy as np

inputfile = open("./day-15/input.txt", "r")

"""
We read the input map into a list of tuples, which we then convert to a numpy array. 0, 1, 2, and 9 mean empty spaces, walls, boxes, and the robot, respectively.
We find the robot's starting position, then replace the 9 with a 0 (we will not update the map with the robot's position, but use function parameters to pass the position instead; skipping unnecessary array reads and writes increases performance).
"""
warehouseCharMap = str.maketrans(".#O@", "0129")
warehouseMap = []
while line:=inputfile.readline().strip():
    warehouseMap.append(tuple(map(int, line.translate(warehouseCharMap))))
warehouseMap = np.array(warehouseMap, dtype=np.int8)
curPos = np.argwhere(warehouseMap==9)[0]
warehouseMap[*curPos] = 0

"""
We read the robot's moves into a tuple, where 1, 3, 2, and 4 mean up, down, left, and right, respectively (the reason for the seemingly arbitrary order is consistency, because in the second part it was advantageous to have the difference between the up and down values be 2).
"""
moveCharMap = str.maketrans("^v<>", "1324")
moveDirections = ""
for line in inputfile:
    moveDirections += line.strip().translate(moveCharMap)
moveDirections = tuple(map(int, moveDirections))

"""
The `move` function takes as inputs the current state of the map, the current position, and the direction of the next move, and it returns the resulting map and robot position.
First we define a `path` variable that contains everything ahead of the robot in the direction of the movement.
We also define a `moveDir` variable that contains the direction on the numpy array axes corresponding to the different directions (i.e. moving left means no movement on the 1st axis and decreasing the coordinate by 1 on the 2nd axis).
We save the location we want to move to in `nextPos`.
Then we check whether the first element in the path is 0, in which case we move forward (i.e. return the map unchanged, and update the robot's position according to the direction).
If it was not 0, we check whether it's a 1, in which case the robot ran into a wall, and it will not move forward (i.e. we return both the map and the robot's position unchanged).
If it was neither a 0 nor a 1, that means there is a box in front of the robot. In this case, we check if there are any empty spaces in the robot's path, and if there are none, it means the robot can't push the box, and remains at the same location.
If there are empty spaces, we save the location of the first one, and we also save the location of the first wall in the robot's path.
If the first wall occurs before the first empty space, that also means that the robot can't push the box(es), therefore it stays in the same place.
If the first wall occurs after the first empty space, that means the robot can push the box(es) forward, so we calculate the exact coordinates of the first empty space, and give it a value of 2. We update the robot's position, set the cell's value to 0, and return the new map and position.
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
    nextPos = curPos+moveDir
    if path[0] == 0:
        return (curMap, nextPos)
    if path[0] == 1:
        return (curMap, curPos)
    emptySpaces = np.where(path==0)[0]
    if emptySpaces.size:
        firstEmptySpace = emptySpaces[0]
        firstWall = np.where(path==1)[0][0]
        if firstEmptySpace < firstWall:
            newBox = curPos + moveDir * (np.argwhere(path[:firstEmptySpace]==2)[-1]+2)
            curMap[*newBox] = 2
            curMap[*nextPos] = 0
            return (curMap, nextPos)
    return (curMap, curPos)

"""
We iterate through all moves from the input, updating the map and the robot's position in each step.
"""
for moveDirection in moveDirections:
    warehouseMap, curPos = move(warehouseMap, curPos, moveDirection)

"""
We iterate through all boxes (i.e. all locations on the map with a value of 2), and add their GPS coordinates to our result counter.
"""
result = 0
for box in np.argwhere(warehouseMap==2):
    result += 100*box[0]+box[1]
print(result)


inputfile.close()