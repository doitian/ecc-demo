from unittest import TestCase
import random
import sympy
from .field import GF


MAX = 500

GF53 = GF(53)
RGF53 = sympy.GF(53, symmetric=False)


class FieldTest(TestCase):
    def test_random_cases(self):
        test_data = [
            (random.randint(0, MAX), random.randint(0, MAX)) for _ in range(10)
        ]
        for a, b in test_data:
            a = GF53(a)
            b = GF53(b)
            self.assertEqual((a + b).n, (RGF53(a.n) + RGF53(b.n)).val)
            self.assertEqual((a - b).n, (RGF53(a.n) - RGF53(b.n)).val)
            self.assertEqual((-a).n, (-RGF53(a.n)).val)
            self.assertEqual((a * b).n, (RGF53(a.n) * RGF53(b.n)).val)
            if b.n != 0:
                self.assertEqual((a / b).n, (RGF53(a.n) / RGF53(b.n)).val)
            if a.n != 0:
                self.assertEqual((b / a).n, (RGF53(b.n) / RGF53(a.n)).val)
