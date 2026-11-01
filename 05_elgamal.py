"""ElGamal encryption/decryption with hardcoded SMALL toy keys; NO imports.
Fixed k is INSECURE in real ElGamal. For real encryption use fresh secret k.
"""
p, g = 23, 5
x = 6  # fixed toy private key
k = 7  # fixed toy ephemeral exponent: NOT secure
message = int(input("Message M (0..22) [10]: ") or "10")
if not (0 <= message < p):
    raise ValueError("Message must be 0..22")

y = pow(g, x, p)
c1 = pow(g, k, p)
c2 = (message * pow(y, k, p)) % p

s = pow(c1, x, p)
plain = (c2 * pow(s, -1, p)) % p

print("Public key (p,g,y):", (p, g, y))
print("Ciphertext:", (c1, c2))
print("Decrypted:", plain)
