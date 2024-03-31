import random
from unittest import TestCase

from sympy.polys.domains import ZZ
from sympy.polys.galoistools import (
    gf_add,
    gf_mul,
    gf_neg,
    gf_sub,
    gf_rem,
    gf_gcdex,
)

from .field import GF
from .poly import Poly

MAX = 500

P = [1, 0, 1, 7, 4, 45, 2]
GF53Poly = Poly(GF(53))
GF53P6 = GF(53, GF53Poly(*reversed(P)))


def random_coeffs():
    coeffs = list(random.randint(0, MAX) for _ in range(random.randint(0, 5)))
    if len(coeffs) == 0:
        return [random.randint(0, MAX)]
    else:
        coeffs.append(random.randint(1, MAX))
        return coeffs


def get_coeffs(p):
    return list(e.n for e in reversed(p.n.n))


def ref_add(a, b):
    return gf_add(get_coeffs(a), get_coeffs(b), 53, ZZ)


def ref_sub(a, b):
    return gf_sub(get_coeffs(a), get_coeffs(b), 53, ZZ)


def ref_neg(a):
    return gf_neg(get_coeffs(a), 53, ZZ)


def ref_mul(a, b):
    return gf_rem(gf_mul(get_coeffs(a), get_coeffs(b), 53, ZZ), P, 53, ZZ)


def ref_div(a, b):
    x, _y, g = gf_gcdex(get_coeffs(b), P, 53, ZZ)
    return gf_rem(gf_mul(get_coeffs(a), x, 53, ZZ), P, 53, ZZ)


class ExtensionFieldTest(TestCase):
    def test_mul(self):
        a = GF53P6(GF53Poly(30, 6, 17, 43, 5, 3))
        b = GF53P6(GF53Poly(26, 8, 52, 42, 43))
        self.assertEqual(get_coeffs(a * b), ref_mul(a, b))

    def test_div(self):
        a = GF53P6(GF53Poly(52))
        b = GF53P6(GF53Poly(22, 20, 4))
        self.assertEqual(get_coeffs(a / b), ref_div(a, b))

    def test_random_cases(self):
        zero = GF53Poly(0)
        test_data = [(random_coeffs(), random_coeffs()) for _ in range(10)]
        for a, b in test_data:
            a = GF53P6(GF53Poly(*a))
            b = GF53P6(GF53Poly(*b))
            self.assertEqual(get_coeffs(a + b), ref_add(a, b))
            self.assertEqual(get_coeffs(a - b), ref_sub(a, b))
            self.assertEqual(get_coeffs(-a), ref_neg(a))
            self.assertEqual(get_coeffs(a * b), ref_mul(a, b))
            if b.n != zero:
                self.assertEqual(get_coeffs(a / b), ref_div(a, b))
            if a.n != zero:
                self.assertEqual(get_coeffs(b / a), ref_div(b, a))
