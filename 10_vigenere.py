"""Vigenere cipher. UID keyword is UYECO. No imports."""

def vigenere(text, key, decrypt=False):
    key = key.upper()
    if not key or any(not ('A' <= c <= 'Z') for c in key):
        raise ValueError("Key must contain only letters")
    output = ""
    j = 0
    for ch in text.upper():
        if 'A' <= ch <= 'Z':
            p = ord(ch) - 65
            k = ord(key[j % len(key)]) - 65
            value = (p - k if decrypt else p + k) % 26
            output += chr(65 + value)
            j += 1
        else:
            output += ch
    return output


if __name__ == "__main__":
    text = input("Plaintext [HELLO]: ") or "HELLO"
    keyword = "UYECO"  # UID-derived keyword
    cipher = vigenere(text, keyword)
    print("Ciphertext:", cipher)
    print("Decrypted:", vigenere(cipher, keyword, True))
