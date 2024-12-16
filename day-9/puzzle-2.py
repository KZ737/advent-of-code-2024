inputfile = open("./day-9/input.txt", "r")

"""
We read the numbers from the inputfile, then create two tuples: `files` containing numbers that correspond to files, and `emptySpaces` with the numbers that correspond to the empty spaces between the files.
"""
filesystemTuple = tuple(map(int, inputfile.readline()))
files = filesystemTuple[0::2]
emptySpaces = filesystemTuple[1::2]

"""
We create a dict for the files, where file IDs are the keys, and the file's starting positions and lengths are the values (being contained in another dict, one layer deeper).
A file's starting position is calculated by summing the values in `files` from the first, up to the previous file, summing the values in `emptySpaces` from 0 up to the empty space just before the file, and adding these sums together.
A file's length is just its value in `files`.
"""
filesDict = dict()
for idx, file in enumerate(files):
    filesDict.update({idx: {"start": sum(files[:idx])+sum(emptySpaces[:idx]), "length": file}})

"""
Similarly, we create a dict for the empty spaces. There are 2 differences to note:
    1. If the length of the empty space is 0, we don't register it, since not being able to move anything to it renders it useless for us.
    2. While the file with the ID `idx` is preceded by files `0,..,idx-1` and empty spaces `0,..,idx-1`, the empty space of index `idx` is preceded by files `0,..,idx` and empty spaces `0,..,idx-1`, which is why we have `sum(files[:idx+1])` here instead of `sum(files[:idx])` like previously.
After filling up the dict, we create a list of its keys to trade in some memory in exchange for speed, as we later use this list frequently.
"""
emptySpacesDict = dict()
for idx, emptySpace in enumerate(emptySpaces):
    if emptySpace:
        emptySpacesDict.update({idx: {"start": sum(files[:idx+1])+sum(emptySpaces[:idx]), "length": emptySpace}})
emptySpaceIDs = list(emptySpacesDict.keys())

"""
We loop through each file starting from the end in order to move them to available empty spaces.
We check if the file's starting position is before the starting position of the first empty space.
    a) If it is, that means neither this file, nor any of the preceding files, can be moved to a preceding empty space (since there is none), therefore we break out of the loop.
    b) If it isn't, that means there might be a chance that we can move this file, therefore we loop through all the available empty spaces (from the beginning):
        1. We check whether the empty space considered is starting after the start of the file:
            i) If it is, that means we found no empty space big enough for the file (and before the file), therefore we break out of the inner loop and start considering the next file (i.e. the file that _precedes_ this file, since we are checking them starting from the end).
            ii) If it isn't, i.e. the empty space starts before the file, we go to the next step.
        2. We check if the empty space is large enough for the file by comparing their lengths.
            i) If it is large enough, we move the file's starting point to the empty space's starting point, we subtract the file's length from the empty space's length, and we move the start of the empty place forward by the file's length. We also check whether the empty space left after this operation is larger than 0: if it is not, that means we completely filled it up with no space remaining for another file, therefore we remove the ID of this space from our list of empty space IDs. Then we break from the inner loop, since we already moved the file to the best position it can be in.
            ii) If it isn't large enough, we continue with checking the next empty space.
After the outer loop finishes, `filesDict` will have the files in their final positions, thus we can go on to count their values.
"""
for fileID, fileData in reversed(filesDict.items()):
    if fileData["start"] < emptySpacesDict[emptySpaceIDs[0]]["start"]:
        break
    for emptySpaceID in emptySpaceIDs:
        if emptySpacesDict[emptySpaceID]["start"] > fileData["start"]:
            break
        if emptySpacesDict[emptySpaceID]["length"] >= fileData["length"]:
            fileData["start"] = emptySpacesDict[emptySpaceID]["start"]
            emptySpacesDict[emptySpaceID]["length"] -= fileData["length"]
            emptySpacesDict[emptySpaceID]["start"] += fileData["length"]
            if emptySpacesDict[emptySpaceID]["length"] == 0:
                emptySpaceIDs.remove(emptySpaceID)
            break

"""
For each file, we calculate its value using the formula mentioned in the solution for the first puzzle of the day (below), and sum these values to get our final result.
    ID*length*(startingPosition+(length-1)/2)
"""
result = 0
for fileID, fileData in filesDict.items():
    result += int(fileID*fileData["length"]*(fileData["start"]+(fileData["length"]-1)/2))

print(result)


inputfile.close()