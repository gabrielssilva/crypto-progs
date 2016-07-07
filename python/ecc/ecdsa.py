from random import randint
import hashlib

import ecc
import ecc_cipher


def sign(E, G, keys, n, message):
    r, s = 0, 0
    while (r == 0) or (s == 0):
        k = randint(1, n - 1)
        P = ecc_cipher.point_times_n(E, G, k)
        r = P[0] % n
        if r == 0:
            continue

        inv_k, _ = ecc.extended_euclid(k, n)
        t = inv_k % n

        H = hashlib.sha1(message.encode('utf-8')).hexdigest()
        e = int(H, 16)
        s = (t * (e + (keys[0] * r))) % n
    return (r, s)


def verify(E, G, keys, n, message, signature):
    r, s = signature
    valid_range = range(1, n)
    if (r not in valid_range) or (s not in valid_range):
        return False

    H = hashlib.sha1(message.encode('utf-8')).hexdigest()
    e = int(H, 16)
    inv_s, _ = ecc.extended_euclid(s, n)
    w = inv_s % n

    u_1, u_2 = (e * w), (r * w)
    X = ecc.sum_points(ecc_cipher.point_times_n(E, G, u_1),
                       ecc_cipher.point_times_n(E, keys[1], u_2), E)

    if X == (0, 0):
        return False

    v = X[0] % n
    print(X)
    return r == v


def run():
    # NIST-192 params
    E = { 'a': -3,
          'b': int('64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1', 16),
          'p': 6277101735386680763835789423207666416083908700390324961279 }
    G = (int('188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012', 16),
         int('07192B95FFC8DA78631011ED6B24CDD573F977A11E794811', 16))
    n = 6277101735386680763835789423176059013767194773182842284081
    keys = ecc_cipher.generate_keys(E, G, n)

    print('\nEnter the input file path')
    in_path = input('>>> ')
    print('Enter the output file path')
    out_path = input('>>> ')


if __name__ == '__main__':

    keys = ecc_cipher.generate_keys(E, G, n)
    run()
