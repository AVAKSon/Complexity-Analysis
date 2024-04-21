
int op_arg(int a, int b)
{
	printf("%d %d %d\n", a, b, (&b)[1]);
	return a;
}  /* end of sensible code */
