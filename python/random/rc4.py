

MASK_8_BITS = 255       # decimal for '1111 1111'


def hex_str_to_key(str_key, n_bytes):
    """Turns a Hex string into a key vector K of size n_bytes
    """
    int_key = int(str_key, 16)
    k = []
    for i in range(0, n_bytes):
        k_item = (int_key >> (i * 8)) & MASK_8_BITS
        k.insert(0, k_item)
    return k


def initialization(k):
    # S and T initialization
    s = []
    t = []
    for i in range(0, 256):
        s.append(i)
        t.append(k[i % len(k)])

    # Initial permutation
    j = 0
    for i in range(0, 256):
        j = (j + s[i] + t[i]) % 256
        s[i], s[j] = s[j], s[i]
    return s


k = hex_str_to_key("F0CC", 2)
s = initialization(k)
