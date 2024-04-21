
from time import time
st = time()
pn, an, dn = 0, 0, 0
tt = []
num = 20000
for n in range(1, num + 1):
	for x in range(1, 1 + n // 2):
		if n % x == 0: tt.append(x)
	if sum(tt) == n: pn += 1
	elif sum(tt) > n: an += 1
	elif sum(tt) < n: dn += 1
	tt = []
et1 = time() - st
print(str(pn) + " Perfect Numbers")
print(str(an) + " Abundant Numbers")
print(str(dn) + " Deficient Numbers")
print(et1, "sec\n")
