import numpy as np
from debug_tools import * 
from aes_constants import BLOCK_SIZE, S_BOX


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


b = block_from_hex("EA04658583455D965C3398B0F02DADC5")
key = block_from_hex("0f470caf15d9b77f71e8ad67c959d698")

print_state_as_hex(b)
print("----")
print_state_as_hex(sub_bytes(b, S_BOX))
