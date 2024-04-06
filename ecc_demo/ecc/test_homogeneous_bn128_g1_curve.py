from unittest import TestCase
import random
from .homogeneous import Bn128G1Curve
import py_ecc.optimized_bn128 as bn128


# Generate random sG
def randpoint():
    s = random.randint(0, bn128.curve_order - 1)
    return bn128.multiply(bn128.G1, s)


class Secp256k1Test(TestCase):
    def test_additoin(self):
        g1 = Bn128G1Curve(bn128.G1[0].n, bn128.G1[1].n, bn128.G1[2].n)
        actual = g1 + g1
        expected = bn128.add(bn128.G1, bn128.G1)
        self.assertEqual(actual.x.n, expected[0].n)
        self.assertEqual(actual.y.n, expected[1].n)
        self.assertEqual(actual.z.n, expected[2].n)

    def test_random_cases(self):
        test_data = [(randpoint(), randpoint()) for _ in range(10)]
        for a, b in test_data:
            actual = Bn128G1Curve(a[0].n, a[1].n, a[2].n) + Bn128G1Curve(
                b[0].n, b[1].n, b[2].n
            )
            expected = bn128.add(a, b)
            self.assertEqual(actual.x.n, expected[0].n)
            self.assertEqual(actual.y.n, expected[1].n)
            self.assertEqual(actual.z.n, expected[2].n)

            actual = Bn128G1Curve(a[0].n, a[1].n, a[2].n) + Bn128G1Curve(
                a[0].n, a[1].n, a[2].n
            )
            expected = bn128.add(a, a)
            self.assertEqual(actual.x.n, expected[0].n)
            self.assertEqual(actual.y.n, expected[1].n)
            self.assertEqual(actual.z.n, expected[2].n)
