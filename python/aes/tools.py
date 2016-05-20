import numpy as np

BLOCK_SIZE = 16
STATE_SIZE = 4

def block_from_hex(str):
    block = np.ndarray((BLOCK_SIZE), dtype=np.uint8)
    as_int = int(str, 16)

    for i in range(BLOCK_SIZE):
        block[BLOCK_SIZE - 1 - i] = (as_int >> (i*8)) & 0xff
    
    return block.reshape((STATE_SIZE, STATE_SIZE)).transpose()

def hex_from_block(block):
    block_str = ''
    for cell in np.nditer(block):
        block_str += '%02x' % cell
    return block_str

def hex_to_str(hex_text):
    text = ''
    for i in range(0, len(hex_text), 2):
        text += (str(chr(int(hex_text[i:i+2], 16))))
    return text


def state_to_long(state):
    state_as_long = 0
    for cell in np.nditer(state):
        state_as_long <<= 8
        state_as_long |= int(cell)
    return state_as_long


def print_state_as_hex(state):
    rows, cols = state.shape
    for i in range(rows):
        print('[', end=' ')
        for j in range(cols):
            print(hex(state[i][j]), end=' ')
        print(']')
