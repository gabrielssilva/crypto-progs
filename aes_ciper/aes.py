import numpy as np
from debug_tools import * 
from aes_constants import BLOCK_SIZE, S_BOX, SHIFT_ROWS_INDEXES
from aes_constants import MIX_COLUMNS_T
from galois_operations import gf_ndarray_dot


def input_to_blocks(str):
    for i in range(0, len(str), BLOCK_SIZE):
        block = str[i:i + BLOCK_SIZE]


def add_round_key(block, key):
    return np.bitwise_xor(block, key)


def sub_bytes(block, lookup_table):
    rows, cols = block.shape
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


b = block_from_hex("87F24D976E4C90EC46E74AC3A68CD895")
key = block_from_hex("0f470caf15d9b77f71e8ad67c959d698")

print_state_as_hex(b)
print("----")
print_state_as_hex(mix_columns(b, MIX_COLUMNS_T))
