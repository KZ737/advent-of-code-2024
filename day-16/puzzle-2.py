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
We initialize an array with the shape of the map + another dimension with a length of 4, full of biiig numbers (2^63 - 1, to be precise). Each element will contain the minimum score we can reach the corresponding location with, from a given direction.
"""
minScore = np.full((*mazeMap.shape, 4), np.iinfo(int).max, dtype=int)

"""
This time we initialize another array which will contain all the locations that are on an optimal route to a given coordinate (including the coordinate itself).
"""
startDir = 2
startHist = (tuple(startPos),)
locsEnRoute = np.array([set() for _ in range(minScore.size)]).reshape(minScore.shape)
locsEnRoute[*startPos, startDir].add(tuple([*startPos, startDir]))

"""
The `getNeighbours` function takes the maze's map, the current position of the reindeer and direction they are facing, their current score, and their history (a tuple containing the locations they were previously in, and the direction they were facing towards). It returns a set containing all the neighbours the reindeer can move to, and their direction and their score by the end of the move.
We initialize an empty set.
We look in all 4 directions, and check whether the space in that direction is a wall or empty. If it is empty, we compare the reindeer's current direction to the direction the empty space is in.
    If the empty space is in the same direction the reindeer are facing currently, we add the space to the list of neighbours with their score increased by 1 (the cost of moving 1 step), and with the space added to the history.
    If the empty space is in the opposite direction, the reindeer would backtrack, which would make no sense if we are trying to minimize the score, so we discard this space.
    If the empty space is in an orthogonal direction compared to the current heading of the reindeer, we add the space to the list of neighbours with their score increased by 1001 (the cost of turning 90° + the cost of moving 1 step), and with the space added to the history.
We initialize a set in which we will collect the neighbours that are spaces the reindeer can visit with lower scores, since we don't care about unoptimal routes.
We iterate through all the spaces we just collected, and compare their score to the current minimum for the same location in the same direction:
    1. If their score is higher than the current minimum, we mark the neighbour for deletion.
    2. If the scores are equal, we add the history to the current set of locations on an optimal route.
    3. If the score is lower than the current minimum, we replace the current minimum with this score, and replace the set of locations on an optimal route with the set of locations in the current history.
We iterate through all the neighbours we marked as unuseful, and remove them from the `neighbours` set one by one (we can't discard them right away, since we would change the set whilst iterating through it).
We return the neighbours that remained.
"""
def getNeighbours(maze, curPos, curDir, curScore, curHist):
    neighbours = set()
    for moveDirNum, moveDir in moveDirs.items():
        nextPos = curPos+moveDir
        if maze[*nextPos] != 1:
            if moveDirNum == curDir:
                neighbours.add((tuple(nextPos.tolist()), moveDirNum, curScore+1, curHist+(tuple(nextPos.tolist()),)))
            elif moveDirNum == -1*curDir:
                continue
            else:
                neighbours.add((tuple(nextPos.tolist()), moveDirNum, curScore+1001, curHist+(tuple(nextPos.tolist()),)))
    toRemove = set()
    for neighbour in neighbours:
        if neighbour[2] > minScore[*neighbour[0], neighbour[1]]:
            toRemove.add(neighbour)
        elif neighbour[2] == minScore[*neighbour[0], neighbour[1]]:
            locsEnRoute[*neighbour[0], neighbour[1]] = locsEnRoute[*neighbour[0], neighbour[1]].union(neighbour[3])
        else:
            minScore[*neighbour[0], neighbour[1]] = neighbour[2]
            locsEnRoute[*neighbour[0], neighbour[1]] = set(neighbour[3])
    for neighbourToRemove in toRemove:
        neighbours.remove(neighbourToRemove)
    return neighbours

"""
We start the process by getting the neighbours of the starting space, with a starting heading of 2 (east), a starting score of 0, and a starting history consisting solely of the starting position.
Then we go into a while loop that will run until the `neighbours` empties.
In this loop, we initialize a new set in which we will collect the currently investigated neighbours' neighbours.
We iterate through all current neighbours, and add all their neighbours to the set.
After we went through all neighbours, we replace the `neighbours` set with this newly collected set of neighbours, and start the loop again.
The loop will stop when we have discovered the whole map. (This kind of map traversal is called a breadth-first search, since in each loop we are looking at spaces at the same distance from the starting point.)
"""
neighbours = getNeighbours(mazeMap, startPos, startDir, 0, startHist)
while neighbours:
    newNeighbours = set()
    for neighbour in neighbours:
        newNeighbours = newNeighbours.union(getNeighbours(mazeMap, neighbour[0], neighbour[1], neighbour[2], neighbour[3]))
    neighbours = newNeighbours

"""
We create a set that will contain all the locations on the optimal route to the end position.
We record the directions from which there were optimal routes to the ending position, then iterate through all these directions and adding the set of locations on an optimal route from that direction to our final result set.
The solution is the size of the set.
"""
resultSet = set()
minScoreDirs = np.argwhere(minScore[*endPos] == np.min(minScore[*endPos]))
for i in range(minScoreDirs.size):
    resultSet = resultSet.union(locsEnRoute[*endPos, minScoreDirs[i][0]])
print(len(resultSet))


inputfile.close()