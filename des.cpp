#include <iostream>
#include <stdint.h>
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

uint64_t expansion(uint32_t input)
{
  uint64_t output = 0; // actually, has only 48 bits

  for (int i=0; i<48; i++)
  {
    int new_bit_pos = DESConstants::E_INDEXES[i] - 1;

    uint64_t new_bit = (input >> new_bit_pos) & 1;
    output |= (new_bit << i);
  }

  return output;
}

void generate_keys(uint64_t k, uint64_t *keys)
{
  const uint32_t MASK_28_BITS = 268435455;
  uint64_t permuted_k = 0; // actually, only 56 bits

  cout << k << endl;
  
  // Same permutation as expansion, only the indexes are different
  for (int i=0; i<56; i++)
  {
    int new_bit_pos = DESConstants::PC1_INDEXES[i] - 1;
    uint64_t new_bit = (k >> new_bit_pos) & 1;
    permuted_k |= (new_bit << i);
  }

  cout << "k after PC1: " << permuted_k << endl;

  // left and right slices. Only 28 bits each
  uint32_t c, d;
  c = (permuted_k >> 28) & MASK_28_BITS;
  d = permuted_k & MASK_28_BITS;

  cout << c << " << " << d << endl;

  for (int i=0; i<16; i++)
  {
    int shift = DESConstants::SHIFT_SCHEDULE[i];
    // circular shift
    c = ((c << shift) | (c >> (28 - shift))) & MASK_28_BITS; 
    d = ((d << shift) | (d >> (28 - shift))) & MASK_28_BITS; 
    cout << c << " <<" << shift << "<< " << d << endl;

    uint64_t ki = 0; // actually, only 48 bits
    uint64_t c_d = c;
    c_d = (c_d << 28) | d; // only 56 bits

    // Same permutation as expansion. Again
    for (int j=0; j<48; j++)
    {
      int new_bit_pos = DESConstants::PC2_INDEXES[j] - 1;
      uint64_t new_bit = (c_d >> new_bit_pos) & 1;
      ki |= (new_bit << j);
    }

    keys[i] = ki;
    cout << "k" << i+1 << ": " << keys[i] << endl;
  }  
}

uint64_t round(uint64_t input, uint64_t key)
{
  uint32_t l_slice, r_slice;
  uint32_t *p = (uint32_t*) &input;

  memcpy(&l_slice, p, sizeof(uint32_t));
  memcpy(&r_slice, (p + 1), sizeof(uint32_t));

  // Substitution Step

  // Function...
  // r_slice = ...

  // Permutation step

  uint64_t output;
  p = (uint32_t*) &output;
  memcpy(p, &r_slice, sizeof(uint32_t));
  memcpy((p + 1), &l_slice, sizeof(uint32_t));
  return output;  
}


int main(int argc, char **argv)
{
  uint64_t keys[64], k;
  cin >> k;
  
  generate_keys(k, keys);

  return 0;
}
