
s = 'abcdefgh'
n, m, char, chars = 2, 3, 'd', 'cd'
# starting from n=2 characters in and m=3 in length;
s[n-1:n+m-1]
# starting from n characters in, up to the end of the string;
s[n-1:]
# whole string minus last character;
s[:-1]
# starting from a known character char="d" within the string and of m length;
indx = s.index(char)
s[indx:indx+m]
# starting from a known substring chars="cd" within the string and of m length. 
indx = s.index(chars)
s[indx:indx+m]
