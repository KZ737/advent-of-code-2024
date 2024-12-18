import re
import itertools

inputfile = open("./day-17/input.txt", "r")

"""
We read all 3 registers' initial value into a dictionary.
"""
registerPattern = re.compile(r"Register ([A-C]):\s([0-9]+)")
registers = {}
while line:=inputfile.readline().strip():
    registerData = re.search(registerPattern, line).groups()
    registers.update({registerData[0]: int(registerData[1])})

"""
We read the program into a tuple.
After inspecting the program, I realized that it ends with an `out`, followed by an `adv`, then a `jnz`. I also realized that the values of registers B and C are calculated from A in each loop, and their values in one loop will not affect their values in another. I also realized that the only instruction that changes the value of register A is the `adv` instruction. The only `adv` instruction in the program is with an operand of 3, which means we divide by 8 every time.
All of this combined means that we start with some value in register A, we calculate and output a number that depends solely on the value in A, then we divide A by 8 (with no remainders) and start the loop again, until the value in A becomes smaller than 8, at which point the program executes its final loop, then exits.
Therefore, I extracted the part that calculates the output in each loop into a separate variable.
"""
programData = tuple(map(int, re.search(r"Program: ([0-9,]+)", inputfile.readline().strip()).groups()[0].split(",")))
loopedProgramData = programData[:-6]

"""
The `comboOperandValue` function returns its input if it's 0, 1, 2, or 3, and returns register A, B, and C if the inputs are 4, 5, and 6, respectively.
"""
def comboOperandValue(operand):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]

"""
The following functions do exactly what the puzzle described, so I refrain from further explanation of them.
I deleted the previously mentioned 3 instructions that do not appear in `loopedProgramData`.
"""
def bxl(operand):
    registers["B"] = registers["B"] ^ operand
    return

def bst(operand):
    registers["B"] = comboOperandValue(operand) % 8

def bxc(operand):
    registers["B"] = registers["B"] ^ registers["C"]
    return

def bdv(operand):
    registers["B"] = registers["A"] // (2 ** comboOperandValue(operand))
    return

def cdv(operand):
    registers["C"] = registers["A"] // (2 ** comboOperandValue(operand))
    return

"""
The `opcodes` dictionary maps the opcodes to the (used subset of) instructions.
"""
opcodes = {1: bxl, 2: bst, 4: bxc, 6: bdv, 7: cdv}

"""
The `progVal` function calculates the output value of a given loop, based on the value in register A at the start.
"""
def progVal(regA):
    registers["A"] = regA
    for i in range(0, len(loopedProgramData), 2):
        opcodes[loopedProgramData[i]](loopedProgramData[i+1])
    return registers["B"]&7

"""
Since we discovered that the output of each loop depends only on the value in register A at the start of the loop, we can calculate the value we need A to be in order to produce the program itself.
We know that the last number in our program was produced from an A value between 0 and 7. Therefore, we check all these numbers to see which of them produce the value we need. We collect these numbers into the `possibleNums` list. After we found which numbers produce the last program value, we multiply every one of them by 8, then we check if the sum of any of these numbers and any number between 0 and 7 produce the penultimate program value, and record them. We iterate through the whole program this way, and after the final iteration, we have a list of numbers that produce the program itself. The solution is the smallest of these numbers.
"""
possibleNums = [0]
for progNum in reversed(programData):
    possibleNums = [8*possibleNum for possibleNum in possibleNums]
    newPossibleNums = []
    for possibleNum, newDigit in itertools.product(possibleNums, range(0, 8)):
        if progVal(possibleNum+newDigit) == progNum:
            newPossibleNums.append(possibleNum+newDigit)
    possibleNums = newPossibleNums
print(min(possibleNums))
    

inputfile.close()