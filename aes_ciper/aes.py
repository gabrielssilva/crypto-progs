import numpy as np
from debug_tools import * 




def input_to_blocks(str):
    for i in range(0, len(str), BLOCK_SIZE):
        block = str[i:i + BLOCK_SIZE]


def add_round_key(block, key):
    return np.bitwise_xor(block, key)


