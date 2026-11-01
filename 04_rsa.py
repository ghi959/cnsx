"""Textbook RSA with hardcoded classroom primes and exponent; NO imports.
NOT real-world secure RSA. If exam asks for input primes or key generation,
replace the constants with the required input or generation procedure.
"""
p = 11
q = 17
e = 7

n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)  # inverse mod PHI, not mod n

message = int(input("Message integer M (0..186) [8]: ") or "8")
if not (0 <= message < n):
    raise ValueError("Message must be in 0..n-1")

cipher = pow(message, e, n)
plain = pow(cipher, d, n)

print("Public key:", (e, n))
print("Private key:", (d, n))
print("Encrypted:", cipher)
print("Decrypted:", plain)
