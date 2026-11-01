"""Educational Lamport one-time, hash-style signature analogue (NO IMPORTS).

NOT SLH-DSA, NOT FIPS 205, NOT SECURE. Actual SLH-DSA uses cryptographic
hash functions, FORS, WOTS+ and Merkle hypertrees with careful indexing.
This toy uses FNV-1a as a WEAK checksum, deterministic private values and
ONE-TIME secret pairs. It teaches selective secret reveal only.
"""


def toy_hash(data):
    # FNV-1a is NOT a cryptographic hash and cannot secure signatures.
    h = 2166136261
    for value in data:
        h = ((h ^ value) * 16777619) % (2 ** 32)
    return h


def keygen():
    secret = []
    public = []
    for bit_index in range(32):
        pair = []
        pub_pair = []
        for bit_value in (0,1):
            s = toy_hash(f'UID2024300214:{bit_index}:{bit_value}:secret'.encode())
            pair.append(s)
            pub_pair.append(toy_hash(s.to_bytes(4,'big')))
        secret.append(pair)
        public.append(pub_pair)
    return secret, public


def sign(message, secret):
    digest = toy_hash(message.encode())
    revealed = []
    for i in range(32):
        bit = (digest >> (31 - i)) & 1
        revealed.append(secret[i][bit])
    return revealed


def verify(message, signature, public):
    if len(signature) != 32:
        return False
    digest = toy_hash(message.encode())
    for i in range(32):
        bit = (digest >> (31 - i)) & 1
        if toy_hash(signature[i].to_bytes(4,'big')) != public[i][bit]:
            return False
    return True


if __name__ == '__main__':
    message = input('Message [HELLO]: ') or 'HELLO'
    sk, pk = keygen()
    signature = sign(message, sk)
    print('Educational Lamport-like ONE-TIME signing demo ONLY')
    print('Revealed secret values:', len(signature))
    print('Original verifies:', verify(message, signature, pk))
    print('Tampered verifies:', verify(message+'!', signature, pk))
    print('Do not reuse this toy key; not SLH-DSA or production security.')
