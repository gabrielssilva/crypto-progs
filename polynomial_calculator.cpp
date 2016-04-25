#include <iostream>

using namespace std;

const int MAX_WORD_LENGTH = 8;
const int MASK_MAX_WORD = 255;
const int MASK_8TH_BIT = (1 << 7); // 10000000
const int MASK_R_POLYNOMIAL = 27; // for x^4 + x^3 + x + 1

int sum(int p1, int p2)
{
  return p1^p2; 
}

int sub(int p1, int p2)
{
  return sum(p1, p2);
}

int multiply_by_x(int p)
{
  int result = p << 1;
  result &= MASK_MAX_WORD; // keep only 8 bits

  // if 8th bit is active, get the modular congruent
  if (p & MASK_8TH_BIT)
  {
    result ^= MASK_R_POLYNOMIAL;
  }
  
  return result;
}

int multiply(int p1, int p2)
{
  int mask = 1; // beginning at 0000001
  int holder = p1;

  // check each bit
  int result = 0;
  for (int i=0; i<MAX_WORD_LENGTH; i++)
  {
    // xor if current bit is 1
    if (p2 & mask)
    {
      result ^= holder;
    }
    
    holder = multiply_by_x(holder);
    mask <<= 1; // go to next bit and check again
  }

  return result;
}

int inverse_multiplicative(int p)
{
    int result = p;

    // keep multiypling until word is completely shifted
    for (int i=0; i<(MAX_WORD_LENGTH - 2); i++)
    {
        result = multiply(multiply(result, result), p);
    }

    return multiply(result, result);
}

int divide(int p1, int p2)
{
  return multiply(p1, inverse_multiplicative(p2));
}

int main(int argc, char **argv)
{
  int p1, p2;
  cin >> p1 >> p2;

  cout << p1 << " + " << p2 << " = " << sum(p1, p2) << endl;
  cout << p1 << " * x = " << multiply_by_x(p1) << endl;
  cout << p1 << " * " << p2 << " = " << multiply(p1, p2) << endl;
  cout << p1 << " / " << p2 << " = " << divide(p1, p2) << endl;
 
  return 0;
}
