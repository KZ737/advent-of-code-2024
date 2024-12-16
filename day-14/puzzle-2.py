import re
import numpy as np
np.set_printoptions(threshold=np.inf)

inputfile = open("./day-14/input.txt", "r")
outputfile = open("./day-14/output.txt", "w")

"""
We know the shape of the map from the description.
"""
mapSize = (101, 103)

"""
Using a simple regex, we gather all the robots into a list, each robot represented by a 4-element tuple (2 for position, 2 for velocity).
"""
robotPattern = re.compile(r"p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)")
robots = []
for line in inputfile:
    robots.append(tuple(map(int, re.search(robotPattern, line).groups())))

"""
Helper function: its input is a number, and returns that number as a string, except when the number is 0, when it returns "." instead (readability).
"""
def printNum(num):
    if not num:
        return "."
    else:
        return str(num)

"""
`calcMap` takes the length of the simulation as an input, and returns the map after the given length.
We create an empty map of the same size as the original map. To each pair of coordinates will correspond the number of robots at that location.
We iterate through the robots and for each one we calculate its final position by multiplying the velocities by the length of the simulation, adding these to the starting position, then taking the modulo with the sizes of the map, and finally incrementing that location's counter by one.
"""
def calcMap(simSec):
    robotMap = np.zeros((mapSize[1], mapSize[0]), dtype=int)
    for robot in robots:
        robotX = (robot[1]+simSec*robot[3])%mapSize[1]
        robotY = (robot[0]+simSec*robot[2])%mapSize[0]
        robotMap[robotX, robotY] += 1
    return robotMap

"""
We write the first 1000 iterations into an output file.
"""
for simSec in range(1000):
    robotMap = calcMap(simSec)
    outputfile.write(str(simSec)+"\n")
    outputfile.write("\n".join(map(lambda x: "".join(map(printNum, x)), robotMap.tolist())))
    outputfile.write("\n\n")

"""
I noticed some patterns emerging at simulation lengths 19, 74, 122, 175, 225, 276.
I realized that 19, 122, and 225 are each 103 apart; likewise, 74, 175, and 276 are 101 apart.
So it seems like there is a pattern at simulation lengths `n*103 + 19`, where n is an integer, and the same can be said for simulation lengths `m*101 + 74`.
The natural instinct at this point is to find where these two sequences intersect:
n*103 + 19 = m*101 + 74
reorganized:
55 = 103*n - 101*m
This Diophantine equation has solutions of the form:
n = 101k + 78
m = 103k + 79
where k is an integer.
Using the smallest possible value for k, 0, we arrive at our possibly interesting location
78*103 + 19 = 79*101 + 74 = 8053
So I printed out the map after this timestamp and found the tree :)
"""
robotMap = calcMap(8053)
print("\n".join(map(lambda x: "".join(map(printNum, x)), robotMap.tolist())))


inputfile.close()
outputfile.close()