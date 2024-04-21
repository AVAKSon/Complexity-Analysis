
import sys

for line in sys.stdin:
    print(sum(map(int, line.split())))
Console, Python 3 only
a = int(input("First number: "))
b = int(input("Second number: "))
print("Result:", a+b)