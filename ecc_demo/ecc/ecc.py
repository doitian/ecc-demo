from abc import ABC
from ..field import GF


# An Elllptic Curve y^2 = x^3 + ax + b where a, b, x, y is in the `base_field`.
# https://kb.iany.me/para/lets/c/Cryptography/Elliptic+Curve+Addition
class EccABC(ABC):
    base_field = None
    a = None
    b = None

    def __init__(self, x=None, y=None):
        if x is not None:
            self.x = x if isinstance(x, self.base_field) else self.base_field(x)
        if y is not None:
            self.y = y if isinstance(y, self.base_field) else self.base_field(y)

    def is_infinity(self):
        return self.x is None or self.y is None

    def __add__(self, other):
        if self.is_infinity():
            return other
        if other.is_infinity():
            return self
        if self == other:
            return self.double()
        if self.x == other.x:
            return self.__class__()

        lam = (other.y - self.y) / (other.x - self.x)
        x = lam * lam - other.x - self.x
        y = lam * (self.x - x) - self.y
        return self.__class__(x, y)

    def double(self):
        if self.is_infinity():
            return self
        if self.y == self.base_field(0):
            return self.__class__()

        lam = (self.a + self.base_field(3) * self.x * self.x) / (
            self.base_field(2) * self.y
        )
        x = lam * lam - self.x - self.x
        y = lam * (self.x - x) - self.y
        return self.__class__(x, y)

    def __eq__(self, other):
        if not self.is_infinity() and not other.is_infinity():
            return self.x == other.x and self.y == other.y
        return self.is_infinity() == other.is_infinity()

    def __repr__(self):
        return f"{self.__class__}{self}"

    def __str__(self):
        return f"({self.x}, {self.y})"


def Ecc(a, b):
    base_field = type(a)
    return type(f"Ecc({base_field})", (EccABC,), dict(base_field=base_field, a=a, b=b))


Secp256k1BaseField = GF(2**256 - 2**32 - 977)
Secp256k1 = Ecc(Secp256k1BaseField(0), Secp256k1BaseField(7))
Secp256k1.G = Secp256k1(
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    32670510020758816978083085130507043184471273380659243275938904335757337482424,
)

Bn128G1CurveBaseField = GF(
    21888242871839275222246405745257275088696311157297823662689037894645226208583
)
Bn128G1Curve = Ecc(Bn128G1CurveBaseField(0), Bn128G1CurveBaseField(3))
Bn128G1Curve.G = Bn128G1Curve(1, 2)
