from unittest import TestCase
import random
from .ecc import Secp256k1
from py_ecc.secp256k1 import secp256k1


# Generate random sG
def randpoint():
    s = random.randint(0, secp256k1.N - 1)
    return secp256k1.multiply(secp256k1.G, s)


class Secp256k1Test(TestCase):
    def test_random_cases(self):
        test_data = [(randpoint(), randpoint()) for _ in range(10)]
        for a, b in test_data:
            actual = Secp256k1(*a) + Secp256k1(*b)
            expected = secp256k1.add(a, b)
            self.assertEqual(actual.x, expected[0])
            self.assertEqual(actual.y, expected[1])
