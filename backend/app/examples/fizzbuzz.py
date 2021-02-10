"""
Write a program that prints the numbers from 1 to 100.
But for multiples of three print "Fizz" instead of the number
and for the multiples of five print "Buzz".
For numbers which are multiples of both three and five print "FizzBuzz".

see: http://blog.codinghorror.com/why-cant-programmers-program/
"""

for x in range(1, 101):
    line = ''
    if x % 3 == 0:
        line += 'Fizz'
    if x % 5 == 0:
        line += 'Buzz'
    if not line:
        line = x
    print(line)
