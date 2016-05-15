import numpy as np


# The operations declared in this module are defined over GF(2^3)
WORD_LENGTH = 8


def gf_mult_step(a):
    result = (a << 1) & 0xff
    if a & (1 << 7):
        result ^= 27
    return result


def gf_mult(a, b):
    mask = 1
    result = 0
    holder = a
    for i in range(8):
        if b & mask:
            result ^= holder
        holder = gf_mult_step(holder) 
        mask <<= 1
    return result        


def gf_ndarray_dot(m1, m2):
    rows, cols = m2.shape
    new_m = np.copy(m2)
    for i in range(rows):
        for j in range(cols):
            new_m[i][j] = gf_mult(m1[i][0], m2[0][j]) ^\
                          gf_mult(m1[i][1], m2[1][j]) ^\
                          gf_mult(m1[i][2], m2[2][j]) ^\
                          gf_mult(m1[i][3], m2[3][j])
    return new_m
