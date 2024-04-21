
Y = lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))
fib = lambda f: lambda n: None if n < 0 else (0 if n == 0 else (1 if n == 1 else f(n-1) + f(n-2)))
[ Y(fib)(i) for i in range(-2, 10) ]
