from unittest import TestCase
import random
from .homogeneous import Bn128G2Curve, Bn128G2CurvePoly
import py_ecc.optimized_bn128 as bn128


# Generate random sG
def randpoint():
    s = random.randint(0, bn128.curve_order - 1)
    return bn128.multiply(bn128.G2, s)


def from_py_ecc_poly(poly):
    return Bn128G2Curve.base_field(Bn128G2CurvePoly(poly.coeffs[0], poly.coeffs[1]))


class Secp256k1Test(TestCase):
    def test_addition(self):
        g2 = Bn128G2Curve(
            from_py_ecc_poly(bn128.G2[0]),
            from_py_ecc_poly(bn128.G2[1]),
            from_py_ecc_poly(bn128.G2[2]),
        )

        actual = g2 + g2
        expected = bn128.add(bn128.G2, bn128.G2)
        self.assertEqual(actual.x.n.n[0], expected[0].coeffs[0])
        self.assertEqual(actual.x.n.n[1], expected[0].coeffs[1])
        self.assertEqual(actual.y.n.n[0], expected[1].coeffs[0])
        self.assertEqual(actual.y.n.n[1], expected[1].coeffs[1])
        self.assertEqual(actual.z.n.n[0], expected[2].coeffs[0])
        self.assertEqual(actual.z.n.n[1], expected[2].coeffs[1])

    def test_random_cases(self):
        test_data = [(randpoint(), randpoint()) for _ in range(10)]
        for a, b in test_data:
            actual = Bn128G2Curve(
                from_py_ecc_poly(a[0]), from_py_ecc_poly(a[1]), from_py_ecc_poly(a[2])
            ) + Bn128G2Curve(
                from_py_ecc_poly(b[0]), from_py_ecc_poly(b[1]), from_py_ecc_poly(b[2])
            )
            expected = bn128.add(a, b)
            self.assertEqual(actual.x.n.n[0], expected[0].coeffs[0])
            self.assertEqual(actual.x.n.n[1], expected[0].coeffs[1])
            self.assertEqual(actual.y.n.n[0], expected[1].coeffs[0])
            self.assertEqual(actual.y.n.n[1], expected[1].coeffs[1])
            self.assertEqual(actual.z.n.n[0], expected[2].coeffs[0])
            self.assertEqual(actual.z.n.n[1], expected[2].coeffs[1])

            actual = Bn128G2Curve(
                from_py_ecc_poly(a[0]), from_py_ecc_poly(a[1]), from_py_ecc_poly(a[2])
            ) + Bn128G2Curve(
                from_py_ecc_poly(a[0]), from_py_ecc_poly(a[1]), from_py_ecc_poly(a[2])
            )
            expected = bn128.add(a, a)
            self.assertEqual(actual.x.n.n[0], expected[0].coeffs[0])
            self.assertEqual(actual.x.n.n[1], expected[0].coeffs[1])
            self.assertEqual(actual.y.n.n[0], expected[1].coeffs[0])
            self.assertEqual(actual.y.n.n[1], expected[1].coeffs[1])
            self.assertEqual(actual.z.n.n[0], expected[2].coeffs[0])
            self.assertEqual(actual.z.n.n[1], expected[2].coeffs[1])
