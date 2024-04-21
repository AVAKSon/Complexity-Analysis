
From javax.swing.table.DefaultTableModel

/* recursive */
int gcd(int a, int b) {
    return (b == 0) ? a : gcd(b, a % b);
}