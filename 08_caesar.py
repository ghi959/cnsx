"""Caesar cipher; UID 2024300214 implies shift 19. No imports."""

def caesar(text, key, decrypt=False):
    if decrypt:
        key = -key
    result = ""
    for ch in text.upper():
        if 'A' <= ch <= 'Z':
            number = ord(ch) - ord('A')
            result += chr((number + key) % 26 + ord('A'))
        else:
            result += ch
    return result


if __name__ == "__main__":
    message = input("Plaintext [HELLO]: ") or "HELLO"
    key = 19  # UID-derived shift
    encrypted = caesar(message, key)
    print("Ciphertext:", encrypted)
    print("Decrypted:", caesar(encrypted, key, decrypt=True))
