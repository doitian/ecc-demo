from .poly import PolyABC


# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
def egcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    zero = a.__class__(0)
    one = a.__class__(1)

    x0, x1, y0, y1 = zero, one, one, zero
    while a != zero:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1

    if not isinstance(b, PolyABC):
        return b, x0, y0

    # Tweak for poly, normalize the constant polynomial to 1
    if b.degree() == 0 and b != one and b != zero:
        x0 = x0.__class__(*(e / b.n[0] for e in x0.n))
        y0 = y0.__class__(*(e / b.n[0] for e in y0.n))
        return one, x0, y0
    return b, x0, y0
