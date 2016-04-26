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

uint64_t round(uint64_t input)
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
  uint32_t in = 1;
  cin >> in;
  uint64_t out = expansion(in);

  cout << "in: " << in << endl;
  cout << "out: " << out << endl;
  return 0;
}
