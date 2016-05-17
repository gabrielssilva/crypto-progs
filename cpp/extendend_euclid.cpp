#include <iostream>

using namespace std;

int gcd(int a, int b, int *x, int *y) 
{ 
  if (b == 0)
  {
    *x = 1;
    *y = 0;
    return a;
  }
  
  int xn, yn;
  int r = a%b;
  int q = a / b;
  int d = gcd(b, r, &xn, &yn);

  *x = yn;
  *y = xn - q * yn;

  return d;
}

int main(int argc, char **argv)
{
  int d, x, y;

  d = gcd(17331, 3041, &x, &y);
  cout << "[a] " << d << " = " << x << "*17331 + " << y << "*3041" << endl;
  cout << "Multiplicative inverse of 3041 mod 17331 = " << y << endl << endl;

  d = gcd(21753, 213, &x, &y);
  cout << "[b] " << d << " = " << x << "*21753 + " << y << "*213" << endl;
  cout << "21753 and 213 are not relatively primes." << endl << endl;

  d = gcd(9571, 548, &x, &y);
  cout << "[c] " << d << " = " << x << "*9571 + " << y << "*548" << endl;
  cout << "Multiplicative inverse of 548 mod 9571 = " << y << endl << endl;

  d = gcd(68432, 24573, &x, &y);
  cout << "[d] " << d << " = " << x << "*68432 + " << y << "*24573" << endl;
  cout << "Multiplicative inverse of 24573 mod 68432 = " << y << endl << endl;

  return 0;
}
