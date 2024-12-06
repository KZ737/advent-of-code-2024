import regex

inputfile = open("./day-4/input.txt", "r")
"""
We read the table, flatten it by joining them with "Z" letters, then look for any of the 4 possible configurations X-MAS can be in.
It is important to note that I used the `regex` library here and _not_ the `re` library, since `regex.findall()` can look for overlapping patterns without having to mess around with lookaheads.
M[XMAS]S[XMASZ]{tableSize-2}A[XMASZ]{tableSize-2}M[XMAS]S
This regex looks for an M followed by 1 of any of the letters XMAS, then an S, then `tableSize-2` amount of the letters XMASZ, then a letter A, then `tableSize-2` of XMASZ again, then an M followed by 1 of any of the letters XMAS, then an S.
This looks for the following pattern:
  M.S
  .A.
  M.S

The other 4 regexes vary in the corner letters, but otherwise completely analogous to the one described above.  
"""
tableToSearch = inputfile.read().splitlines()
tableSize = len(tableToSearch[0])+1
patterns = ["M[XMAS]S[XMASZ]{{{0}}}A[XMASZ]{{{0}}}M[XMAS]S".format(tableSize-2),
            "M[XMAS]M[XMASZ]{{{0}}}A[XMASZ]{{{0}}}S[XMAS]S".format(tableSize-2),
            "S[XMAS]S[XMASZ]{{{0}}}A[XMASZ]{{{0}}}M[XMAS]M".format(tableSize-2),
            "S[XMAS]M[XMASZ]{{{0}}}A[XMASZ]{{{0}}}S[XMAS]M".format(tableSize-2)]
tableToSearch = "Z" + "Z".join(tableToSearch) + "Z"
result = 0
for pattern in patterns:
    m=regex.findall(pattern, tableToSearch, overlapped=True)
    if m:
        result += len(m)

print(result)

inputfile.close()