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

    static const int S1[64];
    static const int S2[64];
    static const int S3[64];
    static const int S4[64];
    static const int S5[64];
    static const int S6[64];
    static const int S7[64];
    static const int S8[64];
};

#endif
