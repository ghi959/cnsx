"""Playfair digraph cipher with I/J combined. UID key UYECO. No imports.
Decrypt returns prepared plaintext; filler removal may be ambiguous.
"""

# Fixed 5x5 Playfair grid for UID keyword UYECO (I/J merged).
MATRIX = ["UYECO", "ABDFG", "HIKLM", "NPQRS", "TVWXZ"]


def clean(text):
    return ''.join('I' if c == 'J' else c for c in text.upper()
                   if 'A' <= c <= 'Z')


def make_pairs(text):
    text = clean(text)
    pairs = []
    i = 0
    while i < len(text):
        first = text[i]
        if i + 1 >= len(text) or text[i + 1] == first:
            second = 'X' if first != 'X' else 'Q'
            i += 1
        else:
            second = text[i + 1]
            i += 2
        pairs.append(first + second)
    return pairs


def playfair(text, matrix, decrypt=False):
    positions = {}
    for r in range(5):
        for c in range(5):
            positions[matrix[r][c]] = (r, c)
    if decrypt:
        data = clean(text)
        if len(data) % 2:
            raise ValueError("Ciphertext must have even length")
        pairs = [data[i:i+2] for i in range(0, len(data), 2)]
    else:
        pairs = make_pairs(text)
    shift = -1 if decrypt else 1
    out = ""
    for first, second in pairs:
        r1, c1 = positions[first]
        r2, c2 = positions[second]
        if r1 == r2:
            out += matrix[r1][(c1 + shift) % 5]
            out += matrix[r2][(c2 + shift) % 5]
        elif c1 == c2:
            out += matrix[(r1 + shift) % 5][c1]
            out += matrix[(r2 + shift) % 5][c2]
        else:
            out += matrix[r1][c2]
            out += matrix[r2][c1]
    return out


if __name__ == "__main__":
    # Precomputed UID keyword UYECO, with I/J merged.
    matrix = MATRIX
    print("Playfair matrix:")
    for row in matrix:
        print(' '.join(row))
    text = input("Plaintext [HELLO]: ") or "HELLO"
    cipher = playfair(text, matrix)
    print("Ciphertext:", cipher)
    print("Decrypted (with filler):", playfair(cipher, matrix, True))
