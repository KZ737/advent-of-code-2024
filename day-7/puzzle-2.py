import itertools

inputfile = open("./day-7/input.txt", "r")


"""
The `concatNums` function concatenates two integers by casting them into strings, concenating those, then casting the result into an int.
"""
def concatNums(num1, num2):
    return int(str(num1)+str(num2))

"""
We define an `ops` enum containing the integer addition and the multiplication functions, as well as our newly defined integer concatenation function.
"""
ops = {0: int.__add__, 1: int.__mul__, 2: concatNums}


"""
From a list of numbers (of length N) and a list of operators (of length N-1), the `calcVal` function calculates the value of the line left-to-right: it takes the first number from the line, `leftVal`. This will become our running total. The function enters a loop where we take the next values and operators from their corresponding lists, then calculate the result of the next operator on `leftVal` and the next value, and assign this value to `leftVal`.
After we have depleted the list of numbers, the loop exits, and returns `leftVal`, which is by this point equal to the result of the whole list using the given operators.
"""
def calcVal(numList, operators):
    numListCopy = numList[:]
    leftVal = numListCopy.pop(0)
    while numListCopy:
        rightVal = numListCopy.pop(0)
        curOp = operators.pop(0)
        leftVal = ops[curOp](leftVal, rightVal)
    return leftVal


"""
The `testLine` function takes a test value and a list of numbers, gets all possible combinations of operators given the length of the list of numbers, then loops through all combinations and checks if the value obtained by a given combination on the list is equal to the test value. If it is, we return true, as the test value can be produced by the list of numbers. If we exhausted all the possible combinations and we haven't found any that would result in the test value, we return false.
"""
def testLine(testValue, numList):
    numOfOps = len(numList)-1
    combinations = list(map(list, itertools.product(ops.keys(), repeat=numOfOps)))
    for combination in combinations:
        if testValue == calcVal(numList, combination):
            return True
    return False


"""
We loop through all lines of the input, parse a line by taking the first number as the test value, and the remaining ones as the list of numbers, then, using the `testLine` function, we check if we can produce the test value from the list of numbers. If we can, we add the test value to our running sum, if we cannot, we continue with the next line.
"""
result = 0
for line in inputfile:
    (testVal, *numList) = map(int, line.strip().replace(":", "").split(" "))
    if testLine(testVal, numList):
        result += testVal

print(result)


inputfile.close()