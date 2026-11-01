"""Import-free RSA-PSS classroom demo: SHA-256 + MGF1 + PSS + RSA-3072.

WARNING: Contains a fixed public/private RSA key and a deterministic salt, both
INSECURE for actual signatures. This is for studying PSS encoding ONLY. Real
RSA-PSS needs secure prime generation, secure randomness, protected keys and a
vetted library. SHA-256 below is implemented directly to avoid imports.
"""

# SHA-256 initial state and round constants (FIPS 180-4).
INITIAL = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]
K = [
  0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
  0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
  0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
  0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
  0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
  0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
  0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
  0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
]
MASK32 = (1 << 32) - 1


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK32


def sha256(data):
    data = bytearray(data)
    bit_length = len(data) * 8
    data.append(0x80)
    while len(data) % 64 != 56:
        data.append(0)
    data.extend(bit_length.to_bytes(8, 'big'))
    h = INITIAL[:]
    for offset in range(0, len(data), 64):
        block = data[offset:offset+64]
        w = [int.from_bytes(block[i:i+4], 'big') for i in range(0, 64, 4)]
        for i in range(16, 64):
            s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = rotr(w[i-2], 17) ^ rotr(w[i-2], 19) ^ (w[i-2] >> 10)
            w.append((w[i-16] + s0 + w[i-7] + s1) & MASK32)
        a,b,c,d,e,f,g,hh = h
        for i in range(64):
            s1 = rotr(e,6) ^ rotr(e,11) ^ rotr(e,25)
            ch = (e & f) ^ (~e & g)
            t1 = (hh + s1 + ch + K[i] + w[i]) & MASK32
            s0 = rotr(a,2) ^ rotr(a,13) ^ rotr(a,22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = (s0 + maj) & MASK32
            hh,g,f,e,d,c,b,a = g,f,e,(d+t1)&MASK32,c,b,a,(t1+t2)&MASK32
        h = [(u + v) & MASK32 for u,v in zip(h,[a,b,c,d,e,f,g,hh])]
    return b''.join(number.to_bytes(4, 'big') for number in h)


def mgf1(seed, length):
    output = b''
    counter = 0
    while len(output) < length:
        output += sha256(seed + counter.to_bytes(4, 'big'))
        counter += 1
    return output[:length]


def xor_bytes(a, b):
    return bytes(x ^ y for x,y in zip(a,b))


def pss_encode(message, em_bits, salt):
    em_len = (em_bits + 7) // 8
    if em_len < 32 + len(salt) + 2:
        raise ValueError('RSA modulus too short for PSS SHA-256 + salt')
    m_hash = sha256(message)
    h = sha256(b'\x00'*8 + m_hash + salt)
    db = b'\x00'*(em_len - 32 - len(salt) - 2) + b'\x01' + salt
    masked = bytearray(xor_bytes(db, mgf1(h, len(db))))
    extra_bits = 8*em_len - em_bits
    masked[0] &= 0xff >> extra_bits
    return bytes(masked) + h + b'\xbc'


def pss_check(message, encoded, em_bits, salt_length=32):
    em_len = (em_bits + 7) // 8
    if len(encoded) != em_len or em_len < 32 + salt_length + 2:
        return False
    if encoded[-1] != 0xbc:
        return False
    mask_db = encoded[:em_len-33]
    h = encoded[em_len-33:-1]
    extra_bits = 8*em_len-em_bits
    if extra_bits and (mask_db[0] >> (8 - extra_bits)) != 0:
        return False
    db = bytearray(xor_bytes(mask_db, mgf1(h, len(mask_db))))
    db[0] &= 0xff >> extra_bits
    prefix_length = em_len-32-salt_length-2
    if db[:prefix_length] != b'\x00'*prefix_length or db[prefix_length] != 1:
        return False
    salt = bytes(db[-salt_length:]) if salt_length else b''
    return h == sha256(b'\x00'*8 + sha256(message) + salt)


# Fixed 1536-bit primes used to construct a 3072-bit RSA demonstration key.
# Insecure: anyone reading this file knows the private key.
P = int("""cce403d465648f16df8d2ff1e7cb8531aed2ce4d379a88e4797d5404ce8238cef46c930d129e387453eec773ec9c0ea3a9ec5642050c8798c94e5ea3e229c53d22395ba4fa27cd5c399e9a8fb5bcd89d87b6ae24cc8d55150ab2a54622ad30a01521dace721a34c101668907d136300d56330acb3cf341f4a9867078ac95bfe64706abc2aa26cc2496dd20c4086973321cbcb14758491b4d30bd7047391e6d56a29a325d4becee2d0692512c9c7551b8c156b60b16e00fddae6e5d00562352bb""", 16)
Q = int("""beee0a6c2e972d7741f6874c937c4039f27f908ff12ba4d6108a32c55d3ab6e3f64b171e408964154e86b9f0431ba482863180b494329dcf7fd5ca951c2d1d48272076da239fb475699a8fecd9f7fe645ce2f4d8ba59876eec61cd5708332875ff7fd16a25478cdb63c90c2f52faeed2103116d95193b640de36aa1ea86117cadcb0145835eee741c7dffdc40bae13e222bcf1091543119240af3096bf75bc1cfe152810e02840acf6908d49c7c68ec062e4639562c3ca1481a3a03854fd792f""", 16)
E = 65537
N = P*Q
PHI = (P-1)*(Q-1)
D = pow(E, -1, PHI)


def sign(message):
    # Deterministic DEMO salt; real PSS requires secure random salt generation.
    salt = sha256(b'classroom salt:' + message)
    em = pss_encode(message, N.bit_length()-1, salt)
    signature_integer = pow(int.from_bytes(em, 'big'), D, N)
    return signature_integer.to_bytes((N.bit_length()+7)//8, 'big')


def verify(message, signature):
    if len(signature) != (N.bit_length()+7)//8:
        return False
    s = int.from_bytes(signature, 'big')
    if s >= N:
        return False
    recovered = pow(s, E, N)
    em_len = ((N.bit_length()-1)+7)//8
    return pss_check(message, recovered.to_bytes(em_len, 'big'), N.bit_length()-1)


if __name__ == '__main__':
    message = input('Message [HELLO]: ') or 'HELLO'
    data = message.encode('utf-8')
    sig = sign(data)
    print('Public exponent:', E)
    print('Modulus bits:', N.bit_length())
    print('Signature size (bytes):', len(sig))
    print('Original verified:', verify(data, sig))
    print('Tampered verified:', verify(data+b'!', sig))
