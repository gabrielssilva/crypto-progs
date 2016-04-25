#include <iostream>

using namespace std;

int gcd_round(int a, int b, int *x, int *y) 
{ 
  if (b == 0)
  {
    *x = 1;
    *y = 0;
    cout << "Stage: a = " << a << ", b = " << b << endl;
    cout << "x = " << *x << ", y = " << *y << endl;
    cout << endl;
    return a;
  }
  
  int xn, yn;
  int r = a%b;
  int q = a / b;
  int d = gcd_round(b, r, &xn, &yn);

  *x = yn;
  *y = xn - q * yn;

  cout << "Stage: a = " << a << ", b = " << b << endl;
  cout << "x = " << *x << ", y = " << *y << endl;
  cout << "xn = " << xn << ", yn = " << yn << ", q = " << q << endl;
  cout << endl;

  return d;
}

int gcd(int a, int b, int *x, int *y)
{
  return gcd_round(a, b, x, y);
}

int main(int argc, char **argv)
{
  int a, b, x, y;

  cin >> a >> b;
  int d = gcd(a, b, &x, &y);

  cout << "GCD = " << d;
  cout << " = " << x << "*" << a << " + " << y << "*" << b << endl;

  return 0;
}
