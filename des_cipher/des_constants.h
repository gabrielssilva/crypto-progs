#ifndef DES_CONSTANTS_H
#define DES_CONSTANTS_H

class DESConstants
{
  public:
    static const int IP_INDEXES[64];
    static const int INV_IP_INDEXES[64];

    static const int E_INDEXES[48];
    static const int PC1_INDEXES[56];
    static const int PC2_INDEXES[48];
    static const int SHIFT_SCHEDULE[16];

    static const int P[32];
    static const int S[8][64];
};

#endif
