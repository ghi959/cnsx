"""Miller-Rabin probable-prime test. No imports.
For numbers below 2^64, the seven fixed bases below give a deterministic test.
For larger n, use more suitably chosen bases; passing means probable prime.
"""

def miller_rabin(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
    for a in bases:
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


if __name__ == "__main__":
    n = int(input("Enter n [17]: ") or "17")
    print("Prime (for n < 2^64) / probable prime" if miller_rabin(n)
          else "Composite / not prime")
