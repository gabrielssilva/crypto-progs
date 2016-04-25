#include <iostream>
#include <stdint.h>
#include "des_constants.h"

using namespace std;

uint64_t initial_permutation(uint64_t block, const int* indexes)
{
  uint64_t original = block;

  // permute each bit
  for (int i=0; i<64; i++)
  {
    int new_pos = indexes[i]-1;

    uint64_t diff = ((original >> i) & 1) ^ ((original >> new_pos) & 1);
    diff = (diff << new_pos);
    block = block ^ diff;
  }

  return block;
}

uint64_t round(uint64_t input) {
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
  uint64_t in = 1; 
  cin >> in;
  uint64_t out = initial_permutation(in, DESConstants::IP_INDEXES); 
  uint64_t inv_out = initial_permutation(out, DESConstants::INV_IP_INDEXES); 


  cout << "in: " << in << endl;
  cout << "out: " << out << endl;
  cout << "inv_out: " << inv_out << endl;
  return 0;
}
