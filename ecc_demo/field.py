from abc import ABC, abstractmethod
from .egcd import egcd

# https://kb.iany.me/para/lets/m/Math/Modular+Arithmetic


class Field(ABC):
    @classmethod
    def zero(cls):
        return cls(0)

    @classmethod
    def one(cls):
        return cls(1)

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __ne__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __neg__(self):
        raise NotImplementedError

    @abstractmethod
    def __sub__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __mul__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __truediv__(self, other):
        raise NotImplementedError


Field.register(int)


class FiniteField(Field):
    domain = int
    field_modulus = None
    order = None

    def __init_subclass__(cls):
        super().__init_subclass__()
        if hasattr(cls, "field_modulus"):
            cls.domain = type(cls.field_modulus)

    def __init__(self, n):
        if isinstance(n, self.domain):
            self.n = n % self.field_modulus
        elif isinstance(n, self.__class__):
            self.n = n.n
        else:
            raise TypeError(
                f"Incompatible types: '{type(self).__name__}' and '{type(n).__name__}'"
            )

    def __ensure_other(self, other):
        if isinstance(other, self.__class__):
            return other
        return self.__class__(other)

    def __eq__(self, other):
        other = self.__ensure_other(other)
        return self.n == other.n

    def __ne__(self, other):
        other = self.__ensure_other(other)
        return self.n != other.n

    def __add__(self, other):
        other = self.__ensure_other(other)
        return self.__class__(self.n + other.n)

    def __neg__(self):
        return self.__class__(-self.n)

    def __sub__(self, other):
        other = self.__ensure_other(other)
        return self + (-other)

    def __mul__(self, other):
        other = self.__ensure_other(other)
        return self.__class__(self.n * other.n)

    def __truediv__(self, other):
        other = self.__ensure_other(other)
        g, x, _y = egcd(other.n, self.field_modulus)
        if g != self.domain(1):
            raise TypeError(
                f"Multiplicative inverse does not exist for '{repr(other)}'"
            )

        return self.__class__(self.n * x)

    def __divmod__(self, other):
        return self / other, self.__class__(0)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.n})"

    def __str__(self):
        return str(self.n)


class GFABC(FiniteField):
    def __init_subclass__(cls):
        super().__init_subclass__()
        if not hasattr(cls, "order"):
            cls.order = cls.field_modulus


def GF(p, field_modulus=None):
    # Integers modulus GF(p)
    if field_modulus is None:
        return type(f"GF({p})", (GFABC,), dict(field_modulus=p))

    # Extension field GF(p^k).
    # field_modulus is the irreducible polynomial at degree k over GF(p)
    k = field_modulus.degree()
    return type(
        f"GF({p}**{k})", (GFABC,), dict(field_modulus=field_modulus, order=p**k)
    )
