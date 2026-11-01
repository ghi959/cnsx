"""Solovay-Strassen / Euler-Jacobi probable-prime test. No imports.
For odd n, compare a^((n-1)/2) mod n with Jacobi(a,n) mod n.
"""

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def jacobi(a, n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("Jacobi denominator must be positive and odd")
    a %= n
    answer = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                answer = -answer
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            answer = -answer
        a %= n
    return answer if n == 1 else 0


def euler_jacobi(n, k=5):
    if k <= 0:
        raise ValueError("k must be positive")
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    # Fixed sequential demonstration bases: no random module.
    for i in range(k):
        a = 2 + i % (n - 3)
        if gcd(a, n) != 1:
            return False
        j = jacobi(a, n)
        if j == 0 or pow(a, (n - 1) // 2, n) != j % n:
            return False
    return True  # Probable prime, not a proof


if __name__ == "__main__":
    n = int(input("Enter n [17]: ") or "17")
    k = 5  # fixed rounds for this example
    print("Probably prime" if euler_jacobi(n, k) else "Composite / not prime")
