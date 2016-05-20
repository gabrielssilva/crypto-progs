from aes.aes import AESCipher, AESDecipher, AESKey
from aes.tools import *

S_BITS = 16                   # eg.: 16
S_BYTES = int(S_BITS / 8)     # eg.: 2
S_MASK = (2 ** S_BITS) - 1    # eg.: 0xffff


def blocks_from_hex(input):
    blocks = []
    as_int = int(input, 16)

    for i in range(0, len(input), 2 * S_BYTES):
        blocks.insert(0, as_int & S_MASK)
        as_int >>= S_BITS
    return blocks


class CFBBase():
    def __init__(self, cipher, iv):
        self.cipher = cipher
        self.iv = iv

    def round(self, block, register):
        out = self.cipher.compute_as_long(register)
        # get only s bits from the ciphertext
        s_out = (out >> (self.cipher.size - S_BITS)) & S_MASK
        return block ^ s_out

    def compute(self, blocks):
        register = self.iv
        output = []

        for block in blocks:
            c = self.round(block, register)
            output.append(c)
            register = (register << S_BITS) | self.remainder(block, c)
        return output

    def compute_str(self, text):
        hex_text = ''.join([('%02x' % ord(c)) for c in text])
        blocks = blocks_from_hex(hex_text)
        r_blocks = self.compute(blocks)

        r_text = ''
        for block in r_blocks:
            r_text += hex_to_str(hex(block)[2:])
        return r_text
    
    def remainder(self, plaintext, ciphertext):
        if self.type is "cipher":
            return ciphertext
        elif self.type is "decipher":
            return plaintext


class CFBCipher(CFBBase):
    def __init__(self, block, register):
        self.type = "cipher"
        super().__init__(block, register)

class CFBDecipher(CFBBase):
    def __init__(self, block, register):
        self.type = "decipher"
        super().__init__(block, register)

    

iv = int("0123456789abcdeffedcba9876543210", 16)
key = block_from_hex("0f1571c947d9e8590cb7add6af7f6798")
aes_key = AESKey(key)
cipher = AESCipher(aes_key)

cfb_cipher = CFBCipher(cipher, iv)
blocks = blocks_from_hex("ffaa02a20335c4d8")
print(blocks)
c = cfb_cipher.compute(blocks)
print(c)

print('-'*40)

cfb_decipher = CFBDecipher(cipher, iv)
blocks = c
print(blocks)
c = cfb_decipher.compute(blocks)
print(c)
