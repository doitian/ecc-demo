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
        test_data = [
            (random.randint(0, MAX), random.randint(0, MAX)) for _ in range(10)
        ]
        for a, b in test_data:
            a = GF53(a)
            b = GF53(b)
            self.assertEqual(
                (a + b).value, (ReferenceGF53(a.value) + ReferenceGF53(b.value)).n
            )
            self.assertEqual(
                (a - b).value, (ReferenceGF53(a.value) - ReferenceGF53(b.value)).n
            )
            self.assertEqual((-a).value, (-ReferenceGF53(a.value)).n)
            self.assertEqual(
                (a * b).value, (ReferenceGF53(a.value) * ReferenceGF53(b.value)).n
            )
            if b.value != 0:
                self.assertEqual(
                    (a / b).value, (ReferenceGF53(a.value) / ReferenceGF53(b.value)).n
                )
            if a.value != 0:
                self.assertEqual(
                    (b / a).value, (ReferenceGF53(b.value) / ReferenceGF53(a.value)).n
                )
