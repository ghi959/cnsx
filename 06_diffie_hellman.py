"""Diffie-Hellman on fixed SMALL classroom numbers; NO imports.
Private values are visible in this file only for teaching.
"""
p, g = 23, 5
alice_private = 6
bob_private = 15

A = pow(g, alice_private, p)
B = pow(g, bob_private, p)

shared_alice = pow(B, alice_private, p)
shared_bob = pow(A, bob_private, p)

print("Alice public:", A)
print("Bob public:", B)
print("Alice shared:", shared_alice)
print("Bob shared:", shared_bob)
print("Keys match:", shared_alice == shared_bob)
