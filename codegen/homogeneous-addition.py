from sympy import symbols, simplify, lcm, pycode
from sympy.codegen.ast import Assignment


def add_distinct_points():
    x1, y1, z1, x2, y2, z2, u, v = symbols(
        "self.x self.y self.z other.x other.y other.z u v"
    )
    x3, y3, z3 = symbols("x y z")

    lam = (y2 / z2 - y1 / z1) / (x2 / z2 - x1 / z1)
    v_expr = x2 * z1 - x1 * z2
    u_expr = y2 * z1 - y1 * z2
    x3_expr = simplify((lam**2 - x1 / z1 - x2 / z2) * z3).subs(
        [(v_expr, v), (u_expr, u)]
    )
    y3_expr = simplify((lam * (x1 / z1 - x3_expr / z3) - y1 / z1) * z3).subs(
        [(v_expr, v), (u_expr, u)]
    )
    x3_denom = x3_expr.as_numer_denom()[1]
    y3_denom = y3_expr.as_numer_denom()[1]
    z3_expr = lcm(x3_denom, y3_denom)

    print("# distinct points")
    print(pycode(Assignment(u, u_expr)))
    print(pycode(Assignment(v, v_expr)))
    print(pycode(Assignment(x3, x3_expr.subs(z3, z3_expr))))
    print(pycode(Assignment(y3, y3_expr.subs(z3, z3_expr))))
    print(pycode(Assignment(z3, z3_expr)))


def double():
    x1, y1, z1, a, w = symbols("self.x self.y self.z a w")
    x3, y3, z3 = symbols("x y z")

    lam = (3 * (x1 / z1) * (x1 / z1) + a) / (2 * y1 / z1)
    w_expr = 3 * x1 * x1 + a * z1 * z1
    x3_expr = simplify((lam**2 - 2 * x1 / z1) * z3).subs(w_expr, w)
    y3_expr = simplify((lam * (x1 / z1 - x3_expr / z3) - y1 / z1) * z3).subs(w_expr, w)

    x3_denom = x3_expr.as_numer_denom()[1]
    y3_denom = y3_expr.as_numer_denom()[1]

    z3_expr = lcm(x3_denom, y3_denom)
    print("# double")
    print(pycode(Assignment(w, w_expr)))
    print(pycode(Assignment(x3, x3_expr.subs(z3, z3_expr))))
    print(pycode(Assignment(y3, y3_expr.subs(z3, z3_expr))))
    print(pycode(Assignment(z3, z3_expr)))


add_distinct_points()
double()
