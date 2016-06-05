from random import randint


def decompose(n):
    """Decomposes an even number into 2^k * q form
    """    
    k = 1
    q = n // 2 
    while (q % 2) == 0:
        k += 1
        q = n // 2**k
    return k, q 

def test(n):
    """Returns False if n is composite, and True if the result is inconclusive
    n must be odd, and greather than 3
    """
    k, q = decompose(n - 1)       # finds k and q programatically
    a = randint(2, n - 2)         # do not include 1 or (n - 1)
    
    if (a**q % n) == 1: return True

    for j in range(0, k):
        if (a**(2**j * q) % n) == n - 1: return True
    return False                  # The number is definitely composite

def is_prime(n, m):
    for _ in range(0, m):
        if test(n) is False: return "%s is composite" % n
    p = 1 - (1 / 4)**m
    return "%s is probably prime, p = %s" % (n, p)
