
def jortsort(sequence):
return list(sequence) == sorted(sequence)
for data in [(1,2,4,3), (14,6,8), ['a', 'c'], ['s', 'u', 'x'], 'CVGH', 'PQRST']:
print(f'jortsort({repr(data)}) is {jortsort(data)}')