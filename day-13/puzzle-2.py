import re
from fractions import Fraction

inputfile = open("./day-13/input.txt", "r")

"""
We read the file into a list. Every machine is described by 3 lines and are separated from each other by 1 empty line, therefore the number of lines in the input file is 3*N+(N-1). So by counting the number of lines, adding 1, and dividing this by 4, we get the number of machines.
"""
inputList = inputfile.readlines()
numOfMachines = (len(inputList) + 1)//4

"""
The `minTokens` function calculates the number of tokens needed to win on a machine. The inputs are tuples for each button, containing the X and Y displacements; and the location of the prize.
We denote the number of times we have to press button A and B with N and M, respectively. We have to solve the following system of equations:
N*A(x) + M*B(x) = P(x)
N*A(y) + M*B(y) = P(y)
Fortunately this has a very simple analytic solution:

     A(y)*P(x) - A(x)*P(y)
M = -----------------------
     A(y)*B(x) - A(x)*B(y)

     
     P(x) - M*B(x)
N = ---------------
         A(x)

We calculate M with the formula above, check if it's an integer: if it is, we calculate N with the formula above and check it if it's an integer: if it is, we return the number of tokens needed: 3*N+M.
If either of the two are non-integers, we can't win with the machine, so we return 0.
"""
def minTokens(buttonA, buttonB, prize):
    M = Fraction(buttonA[1]*prize[0]-buttonA[0]*prize[1], buttonA[1]*buttonB[0]-buttonA[0]*buttonB[1])
    if M.is_integer():
        N = Fraction(prize[0]-M*buttonB[0], buttonA[0])
        if N.is_integer():
            return 3*N+M
    return 0

"""
We use 2 simple regex patterns to parse the input.
"""
buttonPattern = re.compile(r"X\+([0-9]+), Y\+([0-9]+)")
prizePattern = re.compile(r"X=([0-9]+), Y=([0-9]+)")

"""
We iterate through the machines, reading and parsing their data from the input. We translate the prize's coordinates according to the description, then add the value of `minTokens` to our final result counter.
"""
result = 0
for i in range(numOfMachines):
    buttonA = tuple(map(int, re.search(buttonPattern, inputList[4*i]).groups()))
    buttonB = tuple(map(int, re.search(buttonPattern, inputList[4*i+1]).groups()))
    prize = tuple(map(int, re.search(prizePattern, inputList[4*i+2]).groups()))
    prize = (prize[0]+10000000000000, prize[1]+10000000000000)
    result += minTokens(buttonA, buttonB, prize)
print(result)

inputfile.close()