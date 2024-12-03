import re
from math import prod

inputfile = open("./day-3/input.txt", "r")
"""
We read the whole file (I know, it's not a great way to do it, but the lines are already massive themselves, so might as well read the entire thing) and find all matches of the regex corresponding to the problem.
We describe a lambda function that converts a tuple of strings of numbers to int and then multiplies them, then we apply this function to all the regex matches using map(), then we sum the products to get the result.

         "("           ","           ")"  
       literal       literal       literal
          |             |             |   
          v             v             v   
    mul  \(  ([0-9]+)   ,   ([0-9]+) \)
    ^           ^              ^      
    |           |              |      
  "mul"     match and      match and  
 literal    capture a      capture a  
            string of      string of  
            1 or more      1 or more  
           consecutive    consecutive 
            numerals       numerals   
             
"""
m = re.findall("mul\(([0-9]+),([0-9]+)\)", inputfile.read())
result = sum(map(lambda x: prod(map(int, x)), m))

print(result)

inputfile.close()