#include <iostream>
#include <stdint.h>
#include <bitset>
#include <string>
#include "des_constants.h"

using namespace std;


bitset<64> initial_permutation(bitset<64> block, const int* indexes)
{
  bitset<64> output;

  // permute each bit
  for (int i=0; i<64; i++)
  {
    int new_bit_pos = indexes[i]-1;
    output[63 - i] = block[63 - new_bit_pos];
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


bitset<32> apply_s_box(bitset<48> input)
{
  bitset<4> slices[8];
  bitset<32> output;

  for (int i=0; i<8; i++)
  {
    bitset<6> input_slice((input << (i * 6)).to_string());
    input_slice &= bitset<6>().set();

    bitset<2> row_bits(string(1, input_slice.to_string()[0]) + string(1, input_slice.to_string()[5]));
    bitset<4> col_bits(string((input_slice << 1).to_string()));

    int row = (row_bits & bitset<2>().set()).to_ulong();
    int col = (col_bits & bitset<4>().set()).to_ulong();
    slices[i] = bitset<4>(DESConstants::S[i][(row * 16) + col]) & bitset<4>().set();
  }

  return bitset<32>(slices[0].to_string() + slices[1].to_string() + slices[2].to_string() +
                    slices[3].to_string() + slices[4].to_string() + slices[5].to_string() +
                    slices[6].to_string() + slices[7].to_string()); 
}


bitset<64> round(bitset<64> input, bitset<48> key)
{
  bitset<32> l_slice, r_slice;
  uint32_t *p = (uint32_t*) &input;

  memcpy(&r_slice, p, sizeof(uint32_t));
  memcpy(&l_slice, (p + 1), sizeof(uint32_t));

  cout << l_slice << " " << r_slice << endl;

  // Substitution Step (f)

  bitset<48> expanded_r = expansion(r_slice);
  
  cout << "E(R) " << expanded_r << endl;

  bitset<32> s_result = apply_s_box(expanded_r ^ key);

  cout << "E(R) ^ K " << (expanded_r ^ key) << endl;
  cout << "S " << s_result << endl;

  bitset<32> new_r; 

  for (int i=0; i<32; i++)
  {
    int new_bit_pos = DESConstants::P[i] - 1;
    new_r[31 - i] = s_result[31 - new_bit_pos];
  }

  cout << new_r << endl;

  // Permutation step

  bitset<64> output(l_slice.to_string() + new_r.to_string());
  return output;  
}


int main(int argc, char **argv)
{
  string s_block, s_k;
  cin >> s_block >> s_k;
  
  bitset<48> keys[16];
  bitset<64> k (s_k);
  bitset<64> block (s_block);

  generate_keys(k, keys);
  cout << "K " << keys[0] << endl;
  cout << round(block, keys[0]) << endl;


//  cout << initial_permutation(k, DESConstants::IP_INDEXES) << endl;
//  cout << k.size() << endl;

  return 0;
}
