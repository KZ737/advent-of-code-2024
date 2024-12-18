import re

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
"""
programData = tuple(map(int, re.search(r"Program: ([0-9,]+)", inputfile.readline().strip()).groups()[0].split(",")))
progLength = len(programData)

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
"""
def adv(operand):
    registers["A"] = registers["A"] // (2 ** comboOperandValue(operand))
    return

def bxl(operand):
    registers["B"] = registers["B"] ^ operand
    return

def bst(operand):
    registers["B"] = comboOperandValue(operand) % 8

def jnz(operand):
    if registers["A"] == 0:
        return
    global ip 
    ip = operand - 2
    return

def bxc(operand):
    registers["B"] = registers["B"] ^ registers["C"]
    return

def out(operand):
    outputList.append(comboOperandValue(operand) % 8)
    return

def bdv(operand):
    registers["B"] = registers["A"] // (2 ** comboOperandValue(operand))
    return

def cdv(operand):
    registers["C"] = registers["A"] // (2 ** comboOperandValue(operand))
    return

"""
The `opcodes` dictionary maps the opcodes to the instructions.
"""
opcodes = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}

"""
We will collect the outputs in `outputList`.
Starting from an instruction pointer (`ip`) value of 0, we go into a loop in which we complete the instructions until we run out of them, incrementing `ip` by 2 in every step (in case of a jump, the function already set `ip` to be the location we jump to, minus 2).
The solution is a comma-separated list of the outputs.
"""
outputList = []
ip = 0
while ip < progLength-1:
    opcodes[programData[ip]](programData[ip+1])
    ip += 2
print(",".join(map(str, outputList)))


inputfile.close()