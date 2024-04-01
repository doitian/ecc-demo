from sympy import symbols, pycode
from sympy.codegen.ast import Assignment

x1, y1, x2, y2 = symbols("self.x self.y other.x other.y")
lam = symbols("lam")
x3, y3 = symbols("x y")
a = symbols("a")

print("__add__")
print(pycode(Assignment(lam, (y2 - y1) / (x2 - x1))))
print(pycode(Assignment(x3, lam**2 - x1 - x2)))
print(pycode(Assignment(y3, lam * (x1 - x3) - y1)))

print()
print("double")
print(pycode(Assignment(lam, (3 * x1 * x1 + a) / (2 * y1))))
print(pycode(Assignment(x3, lam**2 - 2 * x1)))
print(pycode(Assignment(y3, lam * (x1 - x3) - y1)))
