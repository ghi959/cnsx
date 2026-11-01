"""Fermat probable-prime test. Standalone: no imports.
A probable-prime answer is NOT a proof (Carmichael numbers can fool it).
Uses successive FIXED demonstration bases, not secure random sampling.
"""

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def fermat(n, k=5):
    if k <= 0:
        raise ValueError("k must be positive")
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # No random library: cycle through 2,3,4,...,n-2 (toy test only).
    for i in range(k):
        a = 2 + i % (n - 3)
        if gcd(a, n) != 1:
            return False
        if pow(a, n - 1, n) != 1:
            return False
    return True  # Only 'probably prime'


if __name__ == "__main__":
    n = int(input("Enter number n [17]: ") or "17")
    k = 5  # fixed rounds for this example
    print("Probably prime" if fermat(n, k) else "Composite / not prime")
