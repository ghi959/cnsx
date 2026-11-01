"""Elliptic Curve Diffie-Hellman over a SMALL toy curve. No imports.
Curve y^2 = x^3 + 2x + 2 modulo 17, base G=(5,1) of order 19.
This is mathematics practice only, NOT secure ECDH.
"""
p = 17
curve_a = 2
curve_b = 2
G = (5, 1)
ORDER = 19


def on_curve(P):
    if P is None:
        return True
    x, y = P
    return 0 <= x < p and 0 <= y < p and (y*y - x*x*x - curve_a*x - curve_b) % p == 0


def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    if not on_curve(P) or not on_curve(Q):
        raise ValueError("Point not on curve")
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None  # point at infinity
    if P == Q:
        numerator, denominator = 3*x1*x1 + curve_a, 2*y1
    else:
        numerator, denominator = y2 - y1, x2 - x1
    slope = (numerator * pow(denominator, -1, p)) % p
    x3 = (slope*slope - x1 - x2) % p
    y3 = (slope*(x1 - x3) - y1) % p
    return (x3, y3)


def multiply(k, P):
    if k < 0:
        raise ValueError("Use nonnegative scalar")
    result = None
    while k > 0:
        if k % 2:
            result = point_add(result, P)
        P = point_add(P, P)
        k //= 2
    return result


if __name__ == "__main__":
    # Toy curve G, FIELD and ORDER are already hardcoded above.
    alice = 5
    bob = 7
    A = multiply(alice, G)
    B = multiply(bob, G)
    s1 = multiply(alice, B)
    s2 = multiply(bob, A)
    print("Base G:", G)
    print("Alice public:", A)
    print("Bob public:", B)
    print("Alice shared:", s1)
    print("Bob shared:", s2)
    print("Match:", s1 == s2)
