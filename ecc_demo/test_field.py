from unittest import TestCase
import random
from py_ecc.fields import FQ
from .field import GF


class ReferenceGF53(FQ):
    degree = 1
    field_modulus = 53


MAX = 500

GF53 = GF(53)


class FieldTest(TestCase):
    def test_random_cases(self):
        pass
        test_data = [
            (random.randint(0, MAX), random.randint(0, MAX)) for _ in range(10)
        ]
        for a, b in test_data:
            a = GF53(a)
            b = GF53(b)
            self.assertEqual((a + b).n, (ReferenceGF53(a.n) + ReferenceGF53(b.n)).n)
            self.assertEqual((a - b).n, (ReferenceGF53(a.n) - ReferenceGF53(b.n)).n)
            self.assertEqual((-a).n, (-ReferenceGF53(a.n)).n)
            self.assertEqual((a * b).n, (ReferenceGF53(a.n) * ReferenceGF53(b.n)).n)
            if b.n != 0:
                self.assertEqual((a / b).n, (ReferenceGF53(a.n) / ReferenceGF53(b.n)).n)
            if a.n != 0:
                self.assertEqual((b / a).n, (ReferenceGF53(b.n) / ReferenceGF53(a.n)).n)
