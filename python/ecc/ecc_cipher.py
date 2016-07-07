from random import randint

import ecc


def point_times_n(E, q, n):
    result = (0, 0)
    point = q
    for bit in range(n.bit_length()):
        if (n >> bit) & 1:
            result = ecc.sum_points(point, result, E)
        point = ecc.sum_points(point, point, E)
    return result 


def generate_keys(E, G, n):
    private_key = randint(1, n - 1) 
    public_key = point_times_n(E, G, private_key)
    return (private_key, public_key)


def cipher(E, P, G, k, keys):
    c_1 = point_times_n(E, G, k)
    c_2 = ecc.sum_points(P, point_times_n(E, keys[1], k), E)
    return (c_1, c_2)


def decipher(E, C, keys):
    secret = point_times_n(E, C[0], keys[0])
    inv_secret = (secret[0], -secret[1])
    return ecc.sum_points(C[1], inv_secret, E)


def input_for_global_params():
    print("Choose a value for a")
    a = int(input(">>> a = "))
    print("Choose a value for b")
    b = int(input(">>> b = "))
    print("Choose a value for p")
    p = int(input(">>> p = "))
    E = { 'a': a, 'b': b, 'p': p }

    print("\nChoose x for the base point G") 
    g_x = int(input(">>> Gx = "))
    print("Choose y for the base point G") 
    g_y = int(input(">>> Gy = "))
    G = (g_x, g_y) 

    return E, G


def run():
    E, G = input_for_global_params()

    print("\nChoose x for the input point P") 
    p_x = int(input(">>> Px = "))
    print("Choose y for the input point P") 
    p_y = int(input(">>> Py = "))
    P = (p_x, p_y)

    n = ecc.find_point_order(G, E)
    keys = generate_keys(E, G, n)
    print("\nThe following keys were generated for the receiver:")
    print("(private, public): %s" % (keys,))

    k = randint(1, n - 1)
    C = cipher(E, P, G, k, keys)
    print("\nThe value %d was chosen for k" % k)
    print("The following Cm was obtained:")
    print("(C_1, C_2): %s" % (C,))

    P_prime = decipher(E, C, keys)
    print("\nAfter deciphering, the following P' was obtained")
    print("(P'x, P'y): %s" % (P_prime,))


if __name__ == '__main__':
    run()
