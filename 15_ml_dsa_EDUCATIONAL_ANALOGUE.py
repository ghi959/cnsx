"""Educational analogue of a lattice-style signature, not ML-DSA.

NO IMPORTS. NOT FIPS 204, NOT ML-DSA-44, NOT SECURE. Does not implement
Module-LWE, Module-SIS, SHAKE, rejection sampling or ML-DSA encodings.
It only illustrates a public matrix relation and a sign/verify equation.
You CANNOT use this to verify actual ML-DSA signatures.
"""
MODULUS = 97
A = [[5, 7], [11, 13]]  # public matrix
SECRET = [2, 3]  # toy private vector; not a real ML-DSA secret


def matvec(matrix, vector):
    return [sum(matrix[row][col]*vector[col] for col in range(2)) % MODULUS
            for row in range(2)]


def addvec(a, b):
    return [(a[i]+b[i]) % MODULUS for i in range(2)]


def challenge(message, commitment):
    # Toy checksum, NOT a cryptographic hash. Actual ML-DSA differs radically.
    return (sum(message.encode('utf-8')) + sum(commitment)) % 5


def public_key():
    return matvec(A, SECRET)


def sign(message):
    y = [4, 6]  # deterministic demo masking vector; INSECURE
    w = matvec(A, y)
    c = challenge(message, w)
    z = [y[i] + c*SECRET[i] for i in range(2)]
    return (w, z)


def verify(message, signature, t):
    w,z = signature
    c = challenge(message, w)
    lhs = matvec(A, z)
    rhs = addvec(w, [(c*v) % MODULUS for v in t])
    return lhs == rhs


if __name__ == '__main__':
    message = input('Message [HELLO]: ') or 'HELLO'
    pk = public_key()
    signature = sign(message)
    print('Educational lattice-relation analogue ONLY')
    print('Public matrix:', A)
    print('Public vector:', pk)
    print('Toy signature:', signature)
    print('Original relation verifies:', verify(message, signature, pk))
    print('Modified relation verifies:', verify(message+'!', signature, pk))
    print('This is NOT an ML-DSA implementation.')
