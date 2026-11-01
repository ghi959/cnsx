"""Euler's theorem — no imports, no third-party libraries."""

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


def phi(n):
    if n < 1:
        raise ValueError('n must be positive')
    count = 0
    for i in range(1, n + 1):
        if gcd(i, n) == 1:
            count += 1
    return count


def euler(a, n):
    if n <= 1:
        raise ValueError('n must be greater than 1')
    if gcd(a, n) != 1:
        print('Euler theorem does not apply: a and n are not coprime')
        return False
    result = pow(a, phi(n), n)
    print('phi(n) =', phi(n))
    print('a^phi(n) mod n =', result)
    return result == 1


if __name__ == '__main__':
    a = 11  # Hardcoded example from notes
    n = 26
    print('Euler theorem holds:', euler(a, n))
