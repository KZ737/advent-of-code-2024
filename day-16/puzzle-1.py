import numpy as np

inputfile = open("./day-16/input.txt", "r")

"""
Helper function: its input is a number, and returns that number as a centered, 6-character string, except when the number is 0, when it returns 6 periods instead (readability).
I used it for printing the map in a readible manner during debugging.
"""
# def printNum(num):
#     if num == np.iinfo(int).max:
#         return "......"
#     else:
#         return str(num).center(6)

"""
We read the input file into a list of lists, which we then turn into a numpy array.
We use 0 for empty spaces, 1 for walls, and 8 and 9 for the starting and ending positions, respectively.
We save the starting and ending positions.
"""
mazeCharMap = str.maketrans(".#SE", "0189")
mazeMap = []
while line:=inputfile.readline().strip():
    mazeMap.append(tuple(map(int, line.translate(mazeCharMap))))
mazeMap = np.array(mazeMap, dtype=np.int8)
startPos = np.argwhere(mazeMap==8)[0].tolist()
endPos = np.argwhere(mazeMap==9)[0].tolist()

"""
The `moveDirs` dictionary contains the change in coordinate corresponding to each direction. -1 and +1 are north and south, while -2 and +2 are west and east, respectively. (respectively, respectively?)
"""
moveDirs = {-1: np.array([-1,  0]),
             1: np.array([+1,  0]),
            -2: np.array([ 0, -1]),
             2: np.array([ 0, +1])}

"""
We initialize an array with the shape of the map, full of biiig numbers (2^63 - 1, to be precise). Each element will contain the minimum score we can reach the corresponding location with.
"""
minScore = np.full_like(mazeMap, np.iinfo(int).max, dtype=int)

"""
The `getNeighbours` function takes the maze's map, the current position of the reindeer and direction they are facing, and their current score. It returns a set containing all the neighbours the reindeer can move to, and their direction and their score by the end of the move.
We initialize an empty set.
We look in all 4 directions, and check whether the space in that direction is a wall or empty. If it is empty, we compare the reindeer's current direction to the direction the empty space is in.
    If the empty space is in the same direction the reindeer are facing currently, we add the space to the list of neighbours with their score increased by 1 (the cost of moving 1 step).
    If the empty space is in the opposite direction, the reindeer would backtrack, which would make no sense if we are trying to minimize the score, so we discard this space.
    If the empty space is in an orthogonal direction compared to the current heading of the reindeer, we add the space to the list of neighbours with their score increased by 1001 (the cost of turning 90° + the cost of moving 1 step).
We initialize a set in which we will collect the neighbours that are spaces the reindeer can visit with lower scores, since we don't care about unoptimal routes.
We iterate through all the spaces we just collected, and check if their score is lower than the current minimum: if it is, we replace the current minimum with the neighbour's score, but if it isn't, we mark the neighbour for deletion.
We iterate through all the neighbours we marked as unuseful, and remove them from the `neighbours` set one by one (we can't discard them right away, since we would change the set whilst iterating through it).
We return the neighbours that remained.
"""
def getNeighbours(maze, curPos, curDir, curScore):
    neighbours = set()
    for moveDirNum, moveDir in moveDirs.items():
        nextPos = curPos+moveDir
        if maze[*nextPos] != 1:
            if moveDirNum == curDir:
                neighbours.add((tuple(nextPos.tolist()), moveDirNum, curScore+1))
            elif moveDirNum == -1*curDir:
                continue
            else:
                neighbours.add((tuple(nextPos.tolist()), moveDirNum, curScore+1001))
    toRemove = set()
    for neighbour in neighbours:
        if neighbour[2] >= minScore[neighbour[0]]:
            toRemove.add(neighbour)
        else:
            minScore[neighbour[0]] = neighbour[2]
    for neighbourToRemove in toRemove:
        neighbours.remove(neighbourToRemove)
    return neighbours

"""
We start the process by getting the neighbours of the starting space, with a starting heading of 2 (east) and a starting score of 0.
Then we go into a while loop that will run until the `neighbours` empties.
In this loop, we initialize a new set in which we will collect the currently investigated neighbours' neighbours.
We iterate through all current neighbours, and add all their neighbours to the set.
After we went through all neighbours, we replace the `neighbours` set with this newly collected set of neighbours, and start the loop again.
The loop will stop when we have discovered the whole map. (This kind of map traversal is called a breadth-first search, since in each loop we are looking at spaces at the same distance from the starting point.)
The solution is the value of the `minScore` array in the ending position.
"""
neighbours = getNeighbours(mazeMap, startPos, 2, 0)
while neighbours:
    newNeighbours = set()
    for neighbour in neighbours:
        newNeighbours = newNeighbours.union(getNeighbours(mazeMap, neighbour[0], neighbour[1], neighbour[2]))
    neighbours = newNeighbours
print(minScore[*endPos])


inputfile.close()