import re
from math import prod

inputfile = open("./day-3/input.txt", "r")
"""
We read the whole file (I know, it's not a great way to do it, but the lines are already massive themselves, so might as well read the entire thing) and remove all its substrings that start with "don't()" and end with "do()". We do this lazily, i.e. we look for the first "do()" after a "don't()". If we were to do this greedily (the default way of matching), the match would contain the substring from the first "don't()" to the last "do()", which would lead to erroneus results. We use the re.DOTALL flag to denote that the "." should match newline characters as well (by default it matches all characters _except_ newlines).
After this removal, we calculate the result exactly like in the first puzzle, but this time using the shortened string.

                     force the preceding
                        thing to match
           match any  as few characters   
           character     as possible
               |              |        
               v              v         
    don't\(\)  .      *       ?    do\(\)
        ^             ^              ^    
        |             |              |    
    "don't()"       match          "do()"
     literal    the preceding     literal 
               thing 0 or more 
                    times      

I will definitely never do this kind of a visual explanation for any more of these puzzles, it took at least 10x as long as solving the puzzle...
"""
m = re.sub("don't\(\).*?do\(\)", "", inputfile.read(), flags=re.DOTALL)
m = re.findall("mul\(([0-9]+),([0-9]+)\)", m)
result = sum(map(lambda x: prod(map(int, x)), m))

print(result)

inputfile.close()