from unittest import TestCase
import random
from .ecc import Bn128G1Curve
import py_ecc.bn128 as bn128


# Generate random sG
def randpoint():
    s = random.randint(0, bn128.curve_order - 1)
    return bn128.multiply(bn128.G1, s)


class Secp256k1Test(TestCase):
    def test_random_cases(self):
        test_data = [(randpoint(), randpoint()) for _ in range(10)]
        for a, b in test_data:
            actual = Bn128G1Curve(a[0].n, a[1].n) + Bn128G1Curve(b[0].n, b[1].n)
            expected = bn128.add(a, b)
            self.assertEqual(actual.x.n, expected[0].n)
            self.assertEqual(actual.y.n, expected[1].n)

            actual = Bn128G1Curve(a[0].n, a[1].n) + Bn128G1Curve(a[0].n, a[1].n)
            expected = bn128.add(a, a)
            self.assertEqual(actual.x.n, expected[0].n)
            self.assertEqual(actual.y.n, expected[1].n)
