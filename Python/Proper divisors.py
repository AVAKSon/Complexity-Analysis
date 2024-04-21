
for m[0] in range(M(0) + 1):
    for m[1] in range(M[1] + 1):
        ...
                for m[i - 1] in range(M[i - 1] + 1):
                    mult = 1
                    for j in range(i):
                        mult *= P[j] ** m[j]
                    yield mult
