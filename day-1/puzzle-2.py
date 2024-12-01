inputfile = open("./day-1/input.txt", "r")
"""
Collect the numbers into two dicts, each of them containing the number of times the given number appears in the list
"""
leftList = {}
rightList = {}
for line in inputfile:
    if int(line.strip().split()[0]) in leftList.keys():
        leftList[int(line.strip().split()[0])] += 1
    else:
        leftList.update({int(line.strip().split()[0]): 1})
    if int(line.strip().split()[1]) in rightList.keys():
        rightList[int(line.strip().split()[1])] += 1
    else:
        rightList.update({int(line.strip().split()[1]): 1})
"""
For all the numbers that appear in both lists, multiply the number by the appearances from each of the two lists, and sum this to get the result
"""
sumCount = 0
for i in set(leftList.keys()).intersection(set(rightList.keys())):
    sumCount += i*leftList[i]*rightList[i]
print(sumCount)
inputfile.close()