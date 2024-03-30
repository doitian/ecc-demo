from abc import ABC, abstractmethod
from .egcd import egcd

# https://kb.iany.me/para/lets/m/Math/Modular+Arithmetic


class GFABC(ABC):
    @classmethod
    @property
    @abstractmethod
    def order(cls):
        raise NotImplementedError

    def __init__(self, value):
        self.value = value % self.order

    def __ensure_other(self, other):
        if isinstance(other, self.__class__) and other.order == self.order:
            return other
        elif isinstance(other, int):
            return self.__class__(other)
        else:
            raise TypeError(
                f"Incompatible operand types: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        other = self.__ensure_other(other)
        return self.__class__(self.value + other.value)

    def __neg__(self):
        return self.__class__(-self.value)

    def __sub__(self, other):
        other = self.__ensure_other(other)
        return self + (-other)

    def __mul__(self, other):
        other = self.__ensure_other(other)
        return self.__class__(self.value * other.value)

    def __truediv__(self, other):
        other = self.__ensure_other(other)
        g, x, _y = egcd(other.value, self.order)
        if g != 1:
            raise TypeError(
                f"Multiplicative inverse does not exist for '{repr(other)}'"
            )
        return self.__class__(self.value * x)


# Integers modulus p
def GF(p):
    return type(f"GF({p})", (GFABC,), {"order": p})
