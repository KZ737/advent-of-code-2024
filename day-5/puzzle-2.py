import graphlib

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
To sort a given list of page numbers, we take the subset of the rules that has only the page numbers occuring in our list, then construct a directed acyclic graph from them using `graphlib.TopologicalSorter`, which conveniently has a `static_order` method that returns an iterable containing the ordering described by the graph, and therefore described by the rules themselves. Casting this iterable into a list, we get the page numbers in their correct order.
"""
def sortPages(pages):
    rulesSubset = {u: rules[u].intersection(set(pages)) for u in rules.keys() if u in pages}
    sortedSubset = list(graphlib.TopologicalSorter(rulesSubset).static_order())
    return sortedSubset


"""
We loop through all the lists of pages and if a list is not in order, we make it so, then take its middle element, which we add up for all the originally unordered lists.
"""
result = 0
for line in inputfile:
    pageList = list(map(int, line.strip().split(",")))
    inOrder = checkIfSorted(pageList)
    if not inOrder:
        sortedPages = sortPages(pageList)
        result += sortedPages[(len(sortedPages)-1)//2]


print(result)

inputfile.close()