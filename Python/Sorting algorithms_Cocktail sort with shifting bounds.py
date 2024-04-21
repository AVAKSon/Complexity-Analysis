   
def cocktailshiftingbounds(A):
    beginIdx = 0
    endIdx = len(A) - 1
    
    while beginIdx <= endIdx:
        newBeginIdx = endIdx
        newEndIdx = beginIdx
        for ii in range(beginIdx,endIdx):
            if A[ii] > A[ii + 1]:
                A[ii+1], A[ii] = A[ii], A[ii+1]
                newEndIdx = ii
                
        endIdx = newEndIdx
    
        for ii in range(endIdx,beginIdx-1,-1):
            if A[ii] > A[ii + 1]:
                A[ii+1], A[ii] = A[ii], A[ii+1]
                newBeginIdx = ii
        
        beginIdx = newBeginIdx + 1
            
test1 = [7, 6, 5, 9, 8, 4, 3, 1, 2, 0]
cocktailshiftingbounds(test1)
print(test1)
 
test2=list('big fjords vex quick waltz nymph')
cocktailshiftingbounds(test2)
print(''.join(test2))


Output:
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
     abcdefghiijklmnopqrstuvwxyz
