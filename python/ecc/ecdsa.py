from random import randint
import hashlib
import pickle

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
    return r == v


def sign_file(E, G, keys, n):
    print('\nEnter the input file path')
    in_path = input('>>> ')
    print('Enter the signature output file path')
    out_path = input('>>> ')
    print('Enter the public key output file path')
    key_path = input('>>> ')

    in_file = open(in_path, 'r')
    message = in_file.read()
    signature = sign(E, G, keys, n, message)
    in_file.close()

    out_file = open(out_path, 'wb')
    pickle.dump(signature, out_file)
    out_file.close()

    key_file = open(key_path, 'wb')
    pickle.dump(keys[1], key_file)
    key_file.close()


def verify_file(E, G, n):
    print('\nEnter the message file path')
    message_path = input('>>> ')
    print('Enter the signature file path')
    signature_path = input('>>> ')
    print('Enter the public key file path')
    key_path = input('>>> ')

    message_file = open(message_path, 'r')
    message = message_file.read()
    message_file.close()

    signature_file = open(signature_path, 'rb')
    signature = pickle.load(signature_file)
    signature_file.close()

    key_file = open(key_path, 'rb')
    p_key = pickle.load(key_file)
    key_file.close()

    if verify(E, G, (0, p_key), n, message, signature):
        print("The signature is valid.")
    else:
        print("The signature is NOT valid")


def run():
    # NIST-192 params
    E = { 'a': -3,
          'b': int('64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1', 16),
          'p': 6277101735386680763835789423207666416083908700390324961279 }
    G = (int('188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012', 16),
         int('07192B95FFC8DA78631011ED6B24CDD573F977A11E794811', 16))
    n = 6277101735386680763835789423176059013767194773182842284081
    keys = ecc_cipher.generate_keys(E, G, n)

    print('Which operation do yout want to perform?')
    print('[1] Sign a file')
    print('[2] Verify a file')
    while True:
        op = input('>>> ')
        if op is '1':
            sign_file(E, G, keys, n)
            break
        if op is '2':
            verify_file(E, G, n)
            break
        else:
            print('Invalid operation. Try again')


if __name__ == '__main__':
    run()
