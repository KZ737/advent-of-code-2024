inputfile = open("./day-1/input.txt", "r")
"""
Collect the numbers
"""
leftList = []
rightList = []
for line in inputfile:
    leftList.append(int(line.strip().split()[0]))
    rightList.append(int(line.strip().split()[1]))
"""
Sort them
"""
leftList.sort()
rightList.sort()
"""
Calculate the absolute differences and sum them
"""
diffSum = sum([abs(leftList[i]-rightList[i]) for i in range(len(leftList))])
print(diffSum)
inputfile.close()