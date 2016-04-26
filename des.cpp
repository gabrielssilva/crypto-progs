#include <iostream>
#include <stdint.h>
#include <bitset>
#include <string>
#include "des_constants.h"

using namespace std;


uint64_t initial_permutation(uint64_t block, const int* indexes)
{
  uint64_t output = 0;

  // permute each bit
  for (int i=0; i<64; i++)
  {
    int new_bit_pos = indexes[i]-1;

    uint64_t new_bit = ((block >> i) & 1);
    output |= (new_bit << new_bit_pos);
  }

  return output;
}

bitset<48> expansion(bitset<32> input)
{
  bitset<48> output;

  for (int i=0; i<48; i++)
  {
    int new_bit_pos = DESConstants::E_INDEXES[i] - 1;
    output[47 - i] = input[31 - new_bit_pos];
  }

  return output;
}

void generate_keys(bitset<64> k, bitset<48> *keys)
{
  const bitset<28> MASK_28_BITS = 268435455;
  bitset<56> permuted_k; // actually, only 56 bits

  // Same permutation as expansion, only the indexes are different
  for (int i=0; i<56; i++)
  {
    int new_bit_pos = DESConstants::PC1_INDEXES[i] - 1;
    permuted_k[55 - i] = k[63 - new_bit_pos];
  }

  // left and right slices. Only 28 bits each
  bitset<28> c(permuted_k.to_string());
  bitset<28> d((permuted_k << 28).to_string());

  for (int i=0; i<16; i++)
  {
    int shift = DESConstants::SHIFT_SCHEDULE[i];
    // circular shift
    c = (c << shift) | (c >> (c.size() - shift)); 
    d = (d << shift) | (d >> (d.size() - shift)); 

    bitset<48> ki;
    bitset<56> c_d(c.to_string() + d.to_string());

    // Same permutation as expansion. Again
    for (int j=0; j<48; j++)
    {
      int new_bit_pos = DESConstants::PC2_INDEXES[j] - 1;
      ki[47 - j] = c_d[55 - new_bit_pos];
    }

    keys[i] = ki;
  }  
}

uint64_t round(uint64_t input, uint64_t key)
{
  uint32_t l_slice, r_slice;
  uint32_t *p = (uint32_t*) &input;

  memcpy(&l_slice, p, sizeof(uint32_t));
  memcpy(&r_slice, (p + 1), sizeof(uint32_t));

  // Substitution Step (f)

  //uint64_t expanded_r = expansion(r_slice);
  //expanded_r ^= key; 


  // Permutation step

  uint64_t output;
  p = (uint32_t*) &output;
  memcpy(p, &r_slice, sizeof(uint32_t));
  memcpy((p + 1), &l_slice, sizeof(uint32_t));
  return output;  
}


int main(int argc, char **argv)
{
  string s_k;
  cin >> s_k;

  bitset<48> keys[16];
  bitset<64> k (s_k);

  generate_keys(k, keys);

  return 0;
}
