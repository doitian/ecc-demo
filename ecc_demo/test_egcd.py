from unittest import TestCase
from .egcd import egcd
from .field import GF
from .poly import Poly

GF53Poly = Poly(GF(53))


class EgcdTest(TestCase):
    def test_poly_egcd(self):
        a = GF53Poly(36, 25)
        b = GF53Poly(14)
        g, x, y = egcd(a, b)
        self.assertEqual(g, GF53Poly(1))
        self.assertEqual(x, GF53Poly(0))
        self.assertEqual(y, GF53Poly(19))
