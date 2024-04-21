
int findNth(String s, char c, int n) {
    if (n == 1) return s.indexOf(c);
    return s.indexOf(c, findNth(s, c, n - 1) + 1);
}

String selectiveReplace(String s, Set... ops) {
    char[] chars = s.toCharArray();
    for (Set set : ops)
        chars[findNth(s, set.old, set.n)] = set.rep;
    return new String(chars);
}

record Set(int n, char old, char rep) { }

selectiveReplace("abracadabra",
    new Set(1, 'a', 'A'),
    new Set(2, 'a', 'B'),
    new Set(4, 'a', 'C'),
    new Set(5, 'a', 'D'),
    new Set(1, 'b', 'E'),
    new Set(2, 'r', 'F'));
