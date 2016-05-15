import numpy as np
from debug_tools import * 
from aes_constants import BLOCK_SIZE, S_BOX, SHIFT_ROWS_INDEXES
from aes_constants import NUM_ROUNDS, MIX_COLUMNS_T, RC
from galois_operations import gf_ndarray_dot


def print_as_hex(block):
    print('[', end=' ')
    for cell in np.nditer(block):
        print(hex(cell), end=' ')
    print(']')



def input_to_blocks(str):
    for i in range(0, len(str), BLOCK_SIZE):
        block = str[i:i + BLOCK_SIZE]


def add_round_key(block, key):
    return np.bitwise_xor(block, key)


def sub_bytes(block, lookup_table):
    for cell in np.nditer(block, op_flags=['readwrite']):
        s_row = (cell >> 4) & 0xf
        s_col = cell & 0xf
        cell[...] = lookup_table[s_row][s_col]
    return block


def shift_rows(block, shift_indexes):
    rows, _ = block.shape
    for i in range(rows):
        block[i] = np.roll(block[i], shift_indexes[i])
    return block


def mix_columns(block, mix_columns_t):
    T = np.array(mix_columns_t, dtype=np.uint8)
    return gf_ndarray_dot(T, block)


class AESKey():
    def __init__(self, key):
        self.expand_key(key)

    def for_round(self, round):
        return self.round_keys[round]

    def expand_key(self, key):
        self.round_keys = []
        # Always transpose, words are columns and not rows
        self.round_keys.append(key.transpose())
        for i in range(1, NUM_ROUNDS+1):
            previous_key = self.round_keys[i-1].transpose()
            round_key = np.zeros(key.shape, dtype=np.uint8)
            round_key[0] = np.bitwise_xor(self.g(previous_key[3], i),
                                          previous_key[0])
            round_key[1] = np.bitwise_xor(round_key[0], previous_key[1])
            round_key[2] = np.bitwise_xor(round_key[1], previous_key[2])
            round_key[3] = np.bitwise_xor(round_key[2], previous_key[3])
            self.round_keys.append(round_key.transpose())

    def g(self, block, round):
        new_block = np.roll(block, -1)
        new_block = sub_bytes(new_block, S_BOX)
        round_constant = np.array([RC[round-1], 0, 0, 0], dtype=np.uint8)
        new_block = np.bitwise_xor(new_block, round_constant)
        return new_block


b = block_from_hex("87F24D976E4C90EC46E74AC3A68CD895")
key = block_from_hex("0f1571c947d9e8590cb7add6af7f6798")
aes_key = AESKey(key)

print_state_as_hex(key)
for i in range(11):
    print('round %s' % (i))
    print_state_as_hex(aes_key.for_round(i))

