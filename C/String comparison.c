#include<string.h>

#define STREQ(A,B) (0==strcmp((A),(B)))
#define STRNE(A,B) (!STREQ(A,B))
#define STRLT(A,B) (strcmp((A),(B))<0)
#define STRLE(A,B) (strcmp((A),(B))<=0)
#define STRGT(A,B) STRLT(B,A)
#define STRGE(A,B) STRLE(B,A)

#define STRCEQ(A,B) (0==strcasecmp((A),(B)))
#define STRCNE(A,B) (!STRCEQ(A,B))
#define STRCLT(A,B) (strcasecmp((A),(B))<0)
#define STRCLE(A,B) (strcasecmp((A),(B))<=0)
#define STRCGT(A,B) STRCLT(B,A)
#define STRCGE(A,B) STRCLE(B,A)

#include<stdio.h>

void compare(const char*a, const char*b) {
  printf("%s%2d%2d%2d%2d%2d%2d %s\n",
	 a,
	 STREQ(a,b), STRNE(a,b), STRGT(a,b), STRLT(a,b), STRGE(a,b), STRLE(a,b),
	 b
	 );
}
void comparecase(const char*a, const char*b) {
  printf("%s%2d%2d%2d%2d%2d%2d %s ignoring case\n",
	 a,
	 STRCEQ(a,b), STRCNE(a,b), STRCGT(a,b), STRCLT(a,b), STRCGE(a,b), STRCLE(a,b),
	 b
	 );
}
int main(int ac, char*av[]) {
  char*a,*b;
  puts("\teq , ne , gt , lt , ge , le");
  while (0 < (ac -= 2)) {
    a = *++av, b = *++av;
    compare(a, b);
    comparecase(a, b);
  }
  return 0;
}
