import itertools

inputfile = open("./day-7/input.txt", "r")


"""
We define an `ops` tuple containing the integer addition and the multiplication functions.
"""
ops = (int.__add__, int.__mul__)


"""
From the test value, a starting value (the first number after the test value), a list of numbers (of length N-1), and a list of operators (of length N-1), the `isPossible` function calculates if the test value can be constructed from the list of numbers.
First, we check if the starting value is larger than the test value: since none of our operations (addition, multiplication) can result in an output less than its inputs, if the starting value is larger than the test value, the test value cannot be constructed, therefore we return false.
Then, we check whether we have numbers to use from the list or not: if we don't, and the starting value is equal to the test value, then we have constructed the test value, therefore we return true. If we don't have any more numbers, but the starting value is different from the test value, we failed to construct the test value, therefore we return false.
If the previous conditions were not met, i.e. we have not overshot the test value, and we still have numbers in the list, then we loop through all the possible operations for the next step, calculate the result (`nextOp(leftVal, numList[0])`), then recursively call this same function with this newly calculated number as the starting value, and with the numbers and operations lists shortened by one (via slicing from their second elements).
If the recursive function call returns true for any operation in the loop, then we return true. If it returns false from all of them, we return false.
"""
def isPossible(testVal, leftVal, numList, operators):
    if leftVal > testVal:
        return False
    if len(numList) == 0:
        return testVal == leftVal
    for nextOp in operators[0]:
        if isPossible(testVal, nextOp(leftVal, numList[0]), numList[1:], operators[1:]):
            return True
    return False


"""
The `testLine` function takes a test value and a list of numbers.
We optimize by restricting the last operation: if the test value is not divisible by the last number in the list, we exclude multiplication from the operations in the last place.
We construct our list of possible operations by repeating all the operations N-2 times, adding onto this the possibilities for the last operation, obtained by the previous two tests.
Then we return the value of the `isPossible` function for the given test value, numbers list, and operations list.
"""
def testLine(testValue, numList):
    lastOp = (ops[0],)
    lastNum = numList[-1]
    if not testValue%lastNum:
        lastOp += (ops[1],)
    return isPossible(testValue, numList[0], numList[1:], (*itertools.repeat(ops, len(numList)-2), lastOp))


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