inputfile = open("./day-9/input.txt", "r")

"""
We read the numbers from the inputfile, then create two lists: `files` containing numbers that correspond to files, and `emptySpaces` with the numbers that correspond to the empty spaces between the files.
We calculate and save the total space occupied by the empty spaces in `emptiesToFill`.
"""
filesystemList = list(map(int, inputfile.readline()))
files = filesystemList[0::2]
emptySpaces = filesystemList[1::2]
emptiesToFill = sum(emptySpaces)

"""
We create a list of numbers (fileIDs) to move into the empty spaces: `numsToInsert`.
We fill this list up the following way:
    1. We start a loop.
    2. We check the list has fewer elements than the number of (to-be-filled) empty spaces left. If this is the case, we go to step 3, otherwise we exit the loop.
    3. We take the last element of our `files` list: this number (`lastNum`) will tell us the amount of space the last file occupies.
    4. We measure the length of the `files` list: this number (`fileID`) tells us the ID of the file the length of which we just obtained (since the files are 0-indexed, for a given `files` list, `len(files)-1` is the last fileID, or, conversely, if we pop the size of the file with fileID `N`, the remaining list will have a length of `N`).
    5. We extend our `numsToInsert` list with `lastNum` amount of `fileID` values.
    6. From the empty space to be filled, we subtract the space requirement of the last empty space, since we do not need to fill that anymore (see "map equivalent" in the following example).
    7. Go to step 2.

Using the sample input as an example:
    Values before the loop:
        numsToInsert == [] (len 0)
        files == [2, 3, 1, 3, 2, 4, 4, 3, 4, 2]
        emptySpaces == [3, 3, 3, 1, 1, 1, 1, 1, 0]
        emptiesToFill == 14
        map equivalent: 00...111...2...333.44.5555.6666.777.888899
    After loop #1:
        lastNum == 2
        fileID == 9
        numsToInsert == [9, 9] (len 2)
        files == [2, 3, 1, 3, 2, 4, 4, 3, 4]
        emptySpaces == [3, 3, 3, 1, 1, 1, 1, 1]
        emptiesToFill == 14
        map equivalent: 00...111...2...333.44.5555.6666.777.8888
    After loop #2:
        lastNum == 4
        fileID == 8
        numsToInsert == [9, 9, 8, 8, 8, 8] (len 6)
        files == [2, 3, 1, 3, 2, 4, 4, 3]
        emptySpaces == [3, 3, 3, 1, 1, 1, 1]
        emptiesToFill == 13
        map equivalent: 00...111...2...333.44.5555.6666.777
    After loop #3:
        lastNum == 3
        fileID == 7
        numsToInsert == [9, 9, 8, 8, 8, 8, 7, 7, 7] (len 9)
        files == [2, 3, 1, 3, 2, 4, 4]
        emptySpaces == [3, 3, 3, 1, 1, 1]
        emptiesToFill == 12
        map equivalent: 00...111...2...333.44.5555.6666
    After loop #4:
        lastNum == 3
        fileID == 7
        numsToInsert == [9, 9, 8, 8, 8, 8, 7, 7, 7, 6, 6, 6, 6] (len 13)
        files == [2, 3, 1, 3, 2, 4]
        emptySpaces == [3, 3, 3, 1, 1]
        emptiesToFill == 11
        map equivalent: 00...111...2...333.44.5555
    Since `len(numsToInsert) >= emptiesToFill`, we exit the loop.
"""
numsToInsert = []
while len(numsToInsert) < emptiesToFill:
    lastNum = files.pop()
    fileID = len(files)
    numsToInsert.extend([fileID for _ in range(lastNum)])
    emptiesToFill -= emptySpaces.pop()

"""
Variable `result` will contain the required sum, while `numsCounted` will contain the number of blocks counted so far.
Since the first file has an ID of 0, all its blocks' value (ID*position) will be 0 irrespectively of their position, so without going through them, we just start `numsCounted` from whatever length the 0th file has (e.g. for the sample input we have a 0th file of length 2, which means the 0th file occupies blocks [0, 1], therefore we start counting blocks from position 2).
Note: originally the `files` list had 1 more element than the `emptySpaces` list, and our previous loop did not change this difference (since every loop removed 1 element from each), but now since we popped the 0th file, they have the same length, which is just convenient.
We loop through the number of files to count (remember, `files` only contains the files that remained in the position they started out on), equal to the number of empty spaces to fill in (see previous line). In each loop:
    1. We check how many empty spaces are between the previous and the next files (`emptySpaces[i]`), and then we remove one-by-one this many elements from `numsToInsert` (always removing the first element), calculating their value and adding them to `result`, while incrementing `numsCounted` in every step.
    2. We now take the next file (that remained in its original position), and add its value to `result`. We use a little trick here to speed up the process: since we know that every number we add to the result is equal (unlike when filling up the empty spaces), we can calculate the whole file's value in one step instead of doing it block-by-block. We add the file's value and length to `result` and `numsConsidered`, respectively.
        Derivation of the formula for the value of a file with fileID `ID` that starts at position `N` and is `k` blocks long:
            value = sum(ID*(N+i)) for i=0,..,k-1
                  = ID*sum(N+i) for i=0,..,k-1
                  = ID*(k*N + sum(i)) for i=0,..,k-1
                  = ID*(k*N + (k-1)*k/2)
                  = ID*k*(N+(k-1)/2)
        In our case `ID == i+1` (since we skipped the file with the ID of 0), `N == numsCounted`, and `k == files[i]`.
        Note: even though the calculated value is an integer, the division by 2 always returns a float which propagates through the calculation, therefore we cast the value into an int before adding it to `result`.
"""
result = 0
numsCounted = files.pop(0)
for i in range(len(files)):
    for _ in range(emptySpaces[i]):
        result += numsCounted*numsToInsert.pop(0)
        numsCounted += 1
    result += int((i+1)*files[i]*(numsCounted+(files[i]-1)/2))
    numsCounted += files[i]

"""
After looping through all files that stayed in their original places and through all the empty spaces between them, we might still have some numbers in `numsToInsert`: this happens if and only if there is a file that has some of its blocks moved but also has some of its blocks stay in their original locations. This happens in the sample input as well: the first block of file #6 remains at its starting location, while the remaining 3 blocks have been moved forward (see below).
    00...111...2...333.44.5555. 6 666.777.888899
    009981118882777333644655556 6 ..............
This happens because in our while loop earlier, we add numbers to `numToInsert` file-by-file. We potentially could add exactly as many numbers to `numToInsert` as needed, but that would require extra checks, use of min/max, and modification of a value in `files`, and I found it simpler to just deal with this afterwards.
We loop through the remaining numbers in `numsToInsert` and add their value to `result`, incrementing `numsCounted` by 1 in every loop.
"""
for i in range(len(numsToInsert)):
    result += numsCounted*numsToInsert.pop(0)
    numsCounted += 1

print(result)


inputfile.close()