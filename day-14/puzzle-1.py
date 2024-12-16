import re
import math

inputfile = open("./day-14/input.txt", "r")

"""
We know the shape of the map from the description.
Based on this, we calculate the dividing lines between the quadrants of the map.
"""
mapSize = (101, 103)
quadrantDiv = ((mapSize[0]-1)//2, (mapSize[1]-1)//2)

"""
Using a simple regex, we gather all the robots into a list, each robot represented by a 4-element tuple (2 for position, 2 for velocity).
"""
robotPattern = re.compile(r"p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)")
robots = []
for line in inputfile:
    robots.append(tuple(map(int, re.search(robotPattern, line).groups())))

"""
We create a 4-element list that will contain the number of robots in each quadrant.
We iterate through the robots and for each one we calculate its final position by multiplying the velocities by the length of the simulation, adding these to the starting position, then taking the modulo with the sizes of the map.
Based on the final location of the robot, we increment the corresponding quadrant's count by one.
The final result is the product of these 4 counts.
"""
simSec = 100
quadrantRobots = [0, 0, 0, 0]
for robot in robots:
    robotX = (robot[0]+simSec*robot[2])%mapSize[0]
    robotY = (robot[1]+simSec*robot[3])%mapSize[1]
    if robotX < quadrantDiv[0] and robotY < quadrantDiv[1]:
        quadrantRobots[0] += 1
    elif robotX > quadrantDiv[0] and robotY < quadrantDiv[1]:
        quadrantRobots[1] += 1
    elif robotX < quadrantDiv[0] and robotY > quadrantDiv[1]:
        quadrantRobots[2] += 1
    elif robotX > quadrantDiv[0] and robotY > quadrantDiv[1]:
        quadrantRobots[3] += 1
print(math.prod(quadrantRobots))


inputfile.close()