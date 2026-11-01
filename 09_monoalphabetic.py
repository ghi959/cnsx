"""Monoalphabetic substitution with UID-derived key. No imports.
The key was PRECOMPUTED using the assignment rule:
random.seed(2024300214); shuffle(A..Z), outside this standalone file.
To regenerate the precise Python shuffle without imports would require
reimplementing Python's seeded pseudorandom generator.
"""
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UID_KEY = "KZDXSRPVAGNJMUHWCFQIOTBEYL"


def mono(text, key, decrypt=False):
    key = key.upper()
    if len(key) != 26 or set(key) != set(ALPHABET):
        raise ValueError("Key must be a permutation of 26 uppercase letters")
    source = key if decrypt else ALPHABET
    target = ALPHABET if decrypt else key
    result = ""
    for ch in text.upper():
        if ch in source:
            result += target[source.index(ch)]
        else:
            result += ch
    return result


if __name__ == "__main__":
    message = input("Plaintext [HELLO]: ") or "HELLO"
    encrypted = mono(message, UID_KEY)
    print("Key:", UID_KEY)
    print("Ciphertext:", encrypted)
    print("Decrypted:", mono(encrypted, UID_KEY, decrypt=True))
