"""ECDSA equations on a toy elliptic curve. NO IMPORTS.
NOT P-256 and NOT secure. Lab uses P-256/SHA-256 with cryptography library.
Here, small scalar mathematics helps you understand (r,s) signatures.
"""
FIELD = 17
CURVE_A = 2
CURVE_B = 2
G = (5, 1)
ORDER = 19  # 19G is the point at infinity
PRIVATE = 5  # fixed classroom scalar; real keys must be random and secret


def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1,y1 = P
    x2,y2 = Q
    if x1 == x2 and (y1+y2) % FIELD == 0:
        return None
    if P == Q:
        num,den = 3*x1*x1 + CURVE_A, 2*y1
    else:
        num,den = y2-y1, x2-x1
    slope = (num * pow(den, -1, FIELD)) % FIELD
    x3 = (slope*slope - x1-x2) % FIELD
    y3 = (slope*(x1-x3)-y1) % FIELD
    return x3,y3


def multiply(k, P):
    result = None
    while k > 0:
        if k & 1:
            result = point_add(result, P)
        P = point_add(P, P)
        k //= 2
    return result


def toy_message_hash(message):
    # NOT SHA-256: for learning only. Easily forged/colliding.
    return sum(message.encode('utf-8')) % ORDER


def sign(message, private=PRIVATE, nonce=3):
    if not (1 <= private < ORDER and 1 <= nonce < ORDER):
        raise ValueError('Invalid scalar')
    R = multiply(nonce, G)
    r = R[0] % ORDER
    if r == 0:
        raise ValueError('Choose another nonce')
    z = toy_message_hash(message)
    s = (pow(nonce, -1, ORDER) * (z + r*private)) % ORDER
    if s == 0:
        raise ValueError('Choose another nonce')
    return (r, s)


def verify(message, signature, public):
    r,s = signature
    if not (1 <= r < ORDER and 1 <= s < ORDER):
        return False
    w = pow(s, -1, ORDER)
    z = toy_message_hash(message)
    u1 = (z*w) % ORDER
    u2 = (r*w) % ORDER
    R = point_add(multiply(u1, G), multiply(u2, public))
    return R is not None and R[0] % ORDER == r


if __name__ == '__main__':
    message = input('Message [HELLO]: ') or 'HELLO'
    public = multiply(PRIVATE, G)
    sig = sign(message)
    print('Curve: y^2 = x^3 + 2x + 2 mod 17')
    print('Private (demo):', PRIVATE)
    print('Public point:', public)
    print('Signature (r,s):', sig)
    print('Original verified:', verify(message, sig, public))
    print('Tampered verified:', verify(message+'!', sig, public))
