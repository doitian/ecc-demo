from abc import ABC
from itertools import zip_longest


def term_to_str(coeff, degree, symbol="x"):
    if degree > 1:
        return f"{coeff} * x**{degree}"
    elif degree == 1:
        return f"{coeff} * x"
    else:
        return str(coeff)


def add_maybe_none(a, b):
    if a is not None and b is not None:
        return a + b
    return a if b is None else b


def sub_maybe_none(a, b):
    if a is not None and b is not None:
        return a - b
    return a if b is None else -b


# Represents polynomials using a tuple of coefficients starting from the lowest degree term.
class PolyABC(ABC):
    # Domain for coefficients
    domain = int

    def __init__(self, *coeffs):
        if all(isinstance(e, self.domain) for e in coeffs):
            self.n = tuple(coeffs)
        else:
            self.n = tuple(self.domain(e) for e in coeffs)

    def __eq__(self, other):
        return self.n == other.n

    def __ne__(self, other):
        return self.n != other.n

    def __add__(self, other):
        n = tuple(add_maybe_none(a, b) for a, b in zip_longest(self.n, other.n))
        return self.__class__(*n)

    def __neg__(self):
        n = tuple(-a for a in self.n)
        return self.__class__(*n)

    def __sub__(self, other):
        n = tuple(sub_maybe_none(a, b) for a, b in zip_longest(self.n, other.n))
        return self.__class__(*n)

    def __mul__(self, other):
        n = [self.domain(0)] * (len(self.n) + len(other.n) - 1)
        for i, a in enumerate(self.n):
            for j, b in enumerate(other.n):
                n[i + j] += a * b
        return self.__class__(*n)

    def __floordiv__(self, other):
        return divmod(self, other)[0]

    def __truediv__(self, other):
        q, r = divmod(self, other)
        if len(r.n) != 1 or r.n[0] != self.domain(0):
            raise ValueError("Division is not exact")
        return q

    def __mod__(self, other):
        return divmod(self, other)[1]

    # https://en.wikipedia.org/wiki/Polynomial_greatest_common_divisor#Euclidean_division
    def __divmod__(self, other):
        # if len(self.n) < len(other.n):
        #     return self.__class__(0), self

        zero = self.domain(0)
        b = other.n
        d = len(b)
        r = list(self.n)
        s_exp = len(r) - d
        q = [zero] * max(1, s_exp + 1)
        c = b[-1]
        while s_exp >= 0:
            s_coeff, s_rem = divmod(r[-1], c)
            if s_rem != zero:
                break

            q[s_exp] = s_coeff
            for i in range(d):
                # degree of b has been raised by s_exp
                r[i + s_exp] -= s_coeff * b[i]

            if len(r) > 1:
                r.pop()
            s_exp -= 1

        while len(q) > 1 and q[-1] == zero:
            q.pop()
        while len(r) > 1 and r[-1] == zero:
            r.pop()

        return self.__class__(*q), self.__class__(*r)

    def lcm(self):
        return self.n[-1]

    def degree(self):
        return len(self.n) - 1

    def __repr__(self):
        return f"{self.__class__.__name__}{repr(self.n)}"

    def __str__(self):
        expr = " + ".join(
            term_to_str(coeff, degree)
            for degree, coeff in enumerate(self.n)
            if coeff != self.domain(0)
        )
        return expr if len(expr) > 0 else "0"


class IntPoly(PolyABC):
    domain = int


def Poly(domain):
    if domain == int:
        return IntPoly
    return type(f"Poly({domain.__name__})", (PolyABC,), dict(domain=domain))
