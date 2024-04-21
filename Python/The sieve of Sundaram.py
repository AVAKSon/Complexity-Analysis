
from numpy import log

def sieve_of_Sundaram(nth, print_all=True):

    assert nth > 0, "nth must be a positive integer"
    k = int((2.4 * nth * log(nth)) // 2)  # nth prime is at about n * log(n)
    integers_list = [True] * k
    for i in range(1, k):
        j = i
        while i + j + 2 * i * j < k:
            integers_list[i + j + 2 * i * j] = False
            j += 1
    pcount = 0
    for i in range(1, k + 1):
        if integers_list[i]:
            pcount += 1
            if print_all:
                print(f"{2 * i + 1:4}", end=' ')
                if pcount % 10 == 0:
                    print()

            if pcount == nth:
                print(f"\nSundaram primes start with 3. The {nth}th Sundaram prime is {2 * i + 1}.\n")
                break



sieve_of_Sundaram(100, True)

sieve_of_Sundaram(1000000, False)
