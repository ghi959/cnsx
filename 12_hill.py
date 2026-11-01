"""2x2 Hill cipher for UID 2024300214; no imports.
The assignment's initial [[20,24],[4,2]] always has even determinant
if only bottom-right changes, so it CANNOT be made invertible that way.
For this demonstration, use corrected invertible [[21,24],[4,3]].
"""
KEY = [[21, 24], [4, 3]]
INVERSE_KEY = [[7, 22], [8, 23]]  # precomputed inverse modulo 26


def hill(text, matrix, pad=True):
    clean = ''.join(ch for ch in text.upper() if 'A' <= ch <= 'Z')
    if len(clean) % 2:
        if pad:
            clean += 'X'
        else:
            raise ValueError("Ciphertext length must be even")
    output = ''
    for i in range(0, len(clean), 2):
        x, y = ord(clean[i]) - 65, ord(clean[i+1]) - 65
        c1 = (matrix[0][0]*x + matrix[0][1]*y) % 26
        c2 = (matrix[1][0]*x + matrix[1][1]*y) % 26
        output += chr(c1 + 65) + chr(c2 + 65)
    return output


if __name__ == "__main__":
    text = input("Plaintext [HI]: ") or "HI"
    cipher = hill(text, KEY)
    original = hill(cipher, INVERSE_KEY, pad=False)
    print("Key:", KEY)
    print("Inverse:", INVERSE_KEY)
    print("Ciphertext:", cipher)
    print("Decrypted (may include padding X):", original)
