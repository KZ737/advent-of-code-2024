inputfile = open("./day-5/input.txt", "r")

"""
We processs the rules into a dict: to a page number corresponds a set containing all the page numbers that must not follow it.
"""
rules = {}
for line in inputfile:
    if len(line)==1:
        break
    v, u = map(int, line.strip().split("|"))
    if u not in rules.keys():
        rules.update({u: {v}})
    else:
        rules[u].add(v)
    if v not in rules.keys():
        rules.update({v: set()})


"""
Function to check if a list of pages is properly ordered. For each page number, we check if any of the page numbers following it is in the rules dict entry corresponding to the page number being checked. If the intersection of these sets is not empty (i.e. there is a common element in the following page numbers and the list of page numbers that must not follow the page number being checked), the list is not properly ordered, and we return false.
"""
def checkIfSorted(pages):
    for i in range(len(pages)-1):
        laterPages = pages[i+1:]
        if set(laterPages).intersection(set(rules[pages[i]])):
            return False
    return True


"""
We loop through all the lists of pages and add up the middle numbers from the properly ordered ones.
"""
result = 0
for line in inputfile:
    pageList = list(map(int, line.strip().split(",")))
    inOrder = checkIfSorted(pageList)
    if inOrder:
        result += pageList[(len(pageList)-1)//2]


print(result)

inputfile.close()