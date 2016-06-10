

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


def generate_stream(s, n_bytes):
    stream = []
    i = j = 0
    while n_bytes > 0:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]

        t = (s[i] + s[j]) % 256
        stream.append(s[t])
        n_bytes -= 1
    return stream


def stream_to_int(stream):
    random_num = 0
    for i in range(0, len(stream)):
        random_num = (random_num << (i * 8)) | stream[i]
    return random_num


k = hex_str_to_key("F0CC", 2)
s = initialization(k)
random_stream = generate_stream(s, 2)
random_num = stream_to_int(random_stream)

print(random_stream)
print(random_num)
