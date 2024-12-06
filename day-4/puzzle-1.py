import regex

inputfile = open("./day-4/input.txt", "r")
"""
We read the table, flatten it by joining them with "Z" letters, then look for any of the 8 possible directions XMAS can be in and count all the matches.
It is important to note that I used the `regex` library here and _not_ the `re` library, since `regex.findall()` can look for overlapping patterns without having to mess around with lookaheads.
The regexes:
  1. XMAS: trivial.
  2. X[XMASZ]{tableSize}M[XMASZ]{tableSize}A[XMASZ]{tableSize}S[XMAS]{0,tableSize-4}Z
      We look for an X, then `tableSize` amount of any of the letters XMASZ, then we look for an M, etc. This finds XMAS patterns in the topleft->bottomright direction. After we found an S in the last position, we check the number of letters between that S and the next Z: if we have more than `tableSize-4` letters, that means this isn't a true match, since we wrapped around the right side of the table at some point.
  3. X[XMASZ]{tableSize-1}M[XMASZ]{tableSize-1}A[XMASZ]{tableSize-1}S
      We look for an X, then `tableSize-1` amount of any of the letters XMASZ, then we look for an M, etc. This finds XMAS patterns in the top->bottom direction.
  4. X[XMASZ]{tableSize-2}M[XMASZ]{tableSize-2}A[XMASZ]{tableSize-2}S[XMAS]{3,}Z
      We look for an X, then `tableSize-2` amount of any of the letters XMASZ, then we look for an M, etc. This finds XMAS patterns in the topright->bottomleft direction. After we found an S in the last position, we check the number of letters between that S and the next Z: if we have less than 3 letters, that means this isn't a true match, since we wrapped around the left side of the table at some point.
  5-8. equivalent to 1-4.

The wrapping-arounds described in 2. and 4., respectively:
....X.        .X....
.....M        M.....
A.....        .....A
.S....        ....S.

"""
tableToSearch = inputfile.read().splitlines()
tableSize = len(tableToSearch[0])+1
patterns = ["XMAS",
            "X[XMASZ]{tableSize-2}M[XMASZ]{{{0}}}A[XMASZ]{{{0}}}S[XMAS]{{0,{1}}}Z".format(tableSize, tableSize-4),
            "X[XMASZ]{{{0}}}M[XMASZ]{{{0}}}A[XMASZ]{{{0}}}S".format(tableSize-1),
            "X[XMASZ]{{{0}}}M[XMASZ]{{{0}}}A[XMASZ]{{{0}}}S[XMAS]{{3,}}Z".format(tableSize-2),
            "SAMX",
            "S[XMASZ]{{{0}}}A[XMASZ]{{{0}}}M[XMASZ]{{{0}}}X[XMAS]{{0,{1}}}Z".format(tableSize, tableSize-4),
            "S[XMASZ]{{{0}}}A[XMASZ]{{{0}}}M[XMASZ]{{{0}}}X".format(tableSize-1),
            "S[XMASZ]{{{0}}}A[XMASZ]{{{0}}}M[XMASZ]{{{0}}}X[XMAS]{{3,}}Z".format(tableSize-2)]
tableToSearch = "Z" + "Z".join(tableToSearch) + "Z"
result = 0
for pattern in patterns:
    m=regex.findall(pattern, tableToSearch, overlapped=True)
    if m:
        result += len(m)


print(result)

inputfile.close()