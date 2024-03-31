from unittest import TestCase
import random
import sympy
from sympy.abc import x
from .poly import IntPoly


MAX = 500


def random_coeffs():
    coeffs = list(random.randint(0, MAX) for _ in range(random.randint(0, 11)))
    if len(coeffs) == 0:
        return [random.randint(0, MAX)]
    else:
        coeffs.append(random.randint(1, MAX))
        return coeffs


def ref_add(a, b):
    a = sympy.Poly(reversed(a.n), x)
    b = sympy.Poly(reversed(b.n), x)
    c = a + b
    return tuple(reversed(c.all_coeffs()))


def ref_sub(a, b):
    a = sympy.Poly(reversed(a.n), x)
    b = sympy.Poly(reversed(b.n), x)
    c = a - b
    return tuple(reversed(c.all_coeffs()))


def ref_neg(a):
    a = sympy.Poly(reversed(a.n), x)
    c = -a
    return tuple(reversed(c.all_coeffs()))


def ref_mul(a, b):
    a = sympy.Poly(reversed(a.n), x)
    b = sympy.Poly(reversed(b.n), x)
    c = a * b
    return tuple(reversed(c.all_coeffs()))


def ref_divmod(a, b):
    a = sympy.Poly(reversed(a.n), x)
    b = sympy.Poly(reversed(b.n), x)
    q = sympy.quo(a, b, domain="ZZ")
    r = sympy.rem(a, b, domain="ZZ")
    return (
        tuple(reversed(q.all_coeffs())),
        tuple(reversed(r.all_coeffs())),
    )


class FieldTest(TestCase):
    def test_add(self):
        a = IntPoly(1, 0, 2)
        b = IntPoly(1, 2, 3, 4)
        self.assertEqual(a + b, IntPoly(2, 2, 5, 4))

    def test_sub(self):
        a = IntPoly(1, 0, 2)
        b = IntPoly(1, 2, 3, 4)
        self.assertEqual(a - b, IntPoly(0, -2, -1, -4))

    def test_neg(self):
        a = IntPoly(1, 0, 2)
        self.assertEqual(-a, IntPoly(-1, 0, -2))

    def test_mul(self):
        a = IntPoly(1, 0, 1)
        b = IntPoly(1, 0, 0, 1)
        self.assertEqual(a * b, IntPoly(1, 0, 1, 1, 0, 1))

    def test_divmod_q0(self):
        a = IntPoly(0, 0, 0, 2)
        b = IntPoly(0, 0, 3)
        q, r = divmod(a, b)
        self.assertEqual(q, IntPoly(0))
        self.assertEqual(r, a)

    def test_divmod_r0(self):
        a = IntPoly(1, 2, 1)
        b = IntPoly(1, 1)
        q, r = divmod(a, b)
        self.assertEqual(q, b)
        self.assertEqual(r, IntPoly(0))

    def test_random_cases(self):
        test_data = [(random_coeffs(), random_coeffs()) for _ in range(10)]
        for a, b in test_data:
            a = IntPoly(*a)
            b = IntPoly(*b)
            self.assertEqual((a + b).n, ref_add(a, b))
            self.assertEqual((a - b).n, ref_sub(a, b))
            self.assertEqual((-a).n, ref_neg(a))
            self.assertEqual((a * b).n, ref_mul(a, b))
            if b.n != (0,):
                q, r = divmod(a, b)
                self.assertEqual((q.n, r.n), ref_divmod(a, b))
            if a.n != (0,):
                q, r = divmod(b, a)
                self.assertEqual((q.n, r.n), ref_divmod(b, a))
