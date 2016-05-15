import numpy as np

BLOCK_SIZE = 16
STATE_SIZE = 4

def block_from_hex(str):
    block = np.ndarray((BLOCK_SIZE), dtype=np.uint8)
    as_int = int(str, 16)

    for i in range(BLOCK_SIZE):
        block[BLOCK_SIZE - 1 - i] = (as_int >> (i*8)) & 0xff
    
    return block.reshape((STATE_SIZE, STATE_SIZE))


def print_state_as_hex(state):
    rows, cols = state.shape
    for i in range(rows):
        print('[', end=' ')
        for j in range(cols):
            print(hex(state[i][j]), end=' ')
        print(']')
