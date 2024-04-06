from abc import ABC
from ..field import GF


# An Elllptic Curve over homogeneous coordinates:
#
# (y/z)^2 = (x/z)^3 + a(x/z) + b where a, b, x, y, z is in the `base_field`.
# https://kb.iany.me/para/lets/c/Cryptography/Elliptic+Curve+in+the+Homogeneous+Coordinate
class EccABC(ABC):
    base_field = None
    a = None
    b = None

    def __init__(self, x, y, z=None):
        self.x = x if isinstance(x, self.base_field) else self.base_field(x)
        self.y = y if isinstance(y, self.base_field) else self.base_field(y)
        if z is not None:
            self.z = z if isinstance(z, self.base_field) else self.base_field(z)
        else:
            self.z = self.base_field(1)

    def is_infinity(self):
        return self.z == self.base_field(0)

    @classmethod
    def infinity(cls):
        return cls(cls.base_field(1), cls.base_field(1), cls.base_field(0))

    def __add__(self, other):
        if self.is_infinity():
            return other
        if other.is_infinity():
            return self
        if self == other:
            return self.double()
        if (
            self.x / self.z == other.x / other.z
            and self.y / self.z == other.y / other.z
        ):
            return self.double()
        if self.x == other.x:
            return self.infinity()

        # distinct points
        u = other.y * self.z - other.z * self.y
        v = other.x * self.z - other.z * self.x
        v_square = v * v
        v_cube = v_square * v
        u_square = u * u

        x = (
            -other.x * self.z * v_cube
            - other.z * self.x * v_cube
            + other.z * self.z * u_square * v
        )
        y = -other.z * self.y * v_cube + u * (
            other.x * self.z * v_square
            + self.base_field(2) * other.z * self.x * v_square
            - other.z * self.z * u_square
        )
        z = other.z * self.z * v_cube
        return self.__class__(x, y, z)

    def double(self):
        if self.is_infinity():
            return self
        if self.y == self.base_field(0):
            return self.infinity()

        self_y_cube = self.y * self.y * self.y
        self_z_square = self.z * self.z
        w = self.a * self_z_square + self.base_field(3) * self.x * self.x
        w_square = w * w

        x = (
            -self.base_field(16) * self.x * self_y_cube * self_z_square
            + self.base_field(2) * self.y * self.z * w_square
        )
        y = -self.base_field(8) * self.y * self_y_cube * self_z_square + w * (
            self.base_field(12) * self.x * self.y * self.y * self.z - w_square
        )
        z = self.base_field(8) * self_y_cube * self_z_square * self.z
        return self.__class__(x, y, z)

    def __eq__(self, other):
        if not self.is_infinity() and not other.is_infinity():
            return self.x == other.x and self.y == other.y
        return self.is_infinity() == other.is_infinity()

    def __repr__(self):
        return f"{self.__class__}{self}"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


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
