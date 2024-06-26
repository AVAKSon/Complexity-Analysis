#define _CRT_SECURE_NO_WARNINGS /* MSVS compilers need this */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Put no more than m characters from string to standard output.
 *
 * It is worth noting that printf("%*s",width,string) does not limit the number
 * of characters to be printed.
 *
 * @param string null terminated string
 * @param m      number of characters to display
 */
void putm(char* string, size_t m)
{
    while(*string && m--)
        putchar(*string++);
}

int main(void)
{

    char string[] = 
        "Programs for other encodings (such as 8-bit ASCII, or EUC-JP)."

    int n = 3;
    int m = 4;
    char knownCharacter = '(';
    char knownSubstring[] = "encodings";

    putm(string+n-1, m );                       putchar('\n');
    puts(string+n+1);                           putchar('\n');
    putm(string, strlen(string)-1);             putchar('\n');
    putm(strchr(string, knownCharacter), m );   putchar('\n');
    putm(strstr(string, knownSubstring), m );   putchar('\n');

    return EXIT_SUCCESS;
}