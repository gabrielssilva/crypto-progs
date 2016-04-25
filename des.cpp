#include <iostream>
#include <stdint.h>
#include "des_constants.h"

using namespace std;

uint64_t initial_permutation(uint64_t block, const int* indexes)
{
  uint64_t original = block;

  for (int i=0; i<64; i++)
  {
    int pos_a = i;
    int pos_b = indexes[i]-1;

    uint64_t diff = ((original >> pos_a) & 1) ^ ((original >> pos_b) & 1);
    diff = (diff << pos_b);
    block = block ^ diff;
  }

  return block;
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
