import numpy as np
from debug_tools import * 
from aes_constants import BLOCK_SIZE, NUM_ROUNDS, RC
from aes_constants import S_BOX, SHIFT_ROWS_INDEXES, MIX_COLUMNS_T
from aes_constants import S_BOX, SHIFT_ROWS_INDEXES, MIX_COLUMNS_T
from aes_constants import I_S_BOX, I_SHIFT_ROWS_INDEXES, I_MIX_COLUMNS_T
from galois_operations import gf_ndarray_dot
import copy


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

    def inverse(self):
        inverse_aes_key = copy.deepcopy(self)
        inverse_aes_key.round_keys = inverse_aes_key.round_keys[::-1]
        return inverse_aes_key

    def expand_key(self, key):
        self.round_keys = []
        self.round_keys.append(key)
        for i in range(1, NUM_ROUNDS+1):
            # Always transpose, words are columns and not rows
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


class AESBase():
    def __init__(self, aes_key):
        self.aes_key = aes_key
    
    def round(self, block, key):
        pass

    def last_round(self, block, key):
        pass

    def compute(self, block):
        block = add_round_key(block, self.aes_key.for_round(0))
        for i in range(1, NUM_ROUNDS):
            block = self.round(block, self.aes_key.for_round(i))
        return self.last_round(block, self.aes_key.for_round(NUM_ROUNDS))


class AESCipher(AESBase):
    def round(self, block, key):
        block = sub_bytes(block, S_BOX)
        block = shift_rows(block, SHIFT_ROWS_INDEXES)
        block = mix_columns(block, MIX_COLUMNS_T)
        return add_round_key(block, key)

    def last_round(self, block, key):
        block = sub_bytes(block, S_BOX)
        block = shift_rows(block, SHIFT_ROWS_INDEXES)
        return add_round_key(block, key)


class AESDecipher(AESBase):
    def round(self, block, key):
        block = shift_rows(block, I_SHIFT_ROWS_INDEXES)
        block = sub_bytes(block, I_S_BOX)
        block = add_round_key(block, key)
        return mix_columns(block, I_MIX_COLUMNS_T)

    def last_round(self, block, key):
        block = shift_rows(block, I_SHIFT_ROWS_INDEXES)
        block = sub_bytes(block, I_S_BOX)
        return add_round_key(block, key)


b = block_from_hex("0123456789abcdeffedcba9876543210")
key = block_from_hex("0f1571c947d9e8590cb7add6af7f6798")
aes_key = AESKey(key)
print_state_as_hex(b)
print('-'*20)
cipher = AESCipher(aes_key)
c = cipher.compute(b)
print_state_as_hex(c)
print('-'*20)
decipher = AESDecipher(aes_key.inverse())
d = decipher.compute(c)
print_state_as_hex(d)

