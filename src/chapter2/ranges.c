#include <stdio.h>
#include <limits.h>
#include <float.h>

long poww(long, long);

int main() {
    printf("header signed_char %d %d\n", SCHAR_MIN, SCHAR_MAX);
    printf("header unsigned_char %u %u\n", 0, UCHAR_MAX);
    printf("header short %d %d\n", SHRT_MIN, SHRT_MAX);
    printf("header unsigned_short %u %u\n", 0, USHRT_MAX);
    printf("header int %d %d\n", INT_MIN, INT_MAX);
    printf("header unsigned_int %u %u\n", 0, UINT_MAX);
    printf("header long %ld %ld\n", LONG_MIN, LONG_MAX);
    printf("header unsigned_long %lu %lu\n", 0lu, ULONG_MAX);
    printf("header float %e %e\n", FLT_MIN, FLT_MAX);
    printf("header double %e %e\n", DBL_MIN, DBL_MAX);
    printf("header long_double %Le %Le\n", LDBL_MIN, LDBL_MAX);

    printf("computed signed_char %d %d\n", (int)(-poww(2, 7)), (int)(poww(2, 7) - 1));
    printf("computed unsigned_char %u %u\n", 0, (int)(poww(2, 8) - 1));
    printf("computed short %d %d\n", (int)(-poww(2, 15)), (int)(poww(2, 15) - 1));
    printf("computed unsigned_short %u %u\n", 0, (int)(poww(2, 16) - 1));
    printf("computed int %d %d\n", (int)(-poww(2, 31)), (int)(poww(2, 31) - 1));
    printf("computed unsigned_int %u %u\n", 0, (int)(poww(2, 32) - 1));
    printf("computed long %ld %ld\n", -poww(2, 63), poww(2, 63) - 1);
    printf("computed unsigned_long %lu %lu\n", 0lu, poww(2, 64) - 1);
    printf("computed float %e %e\n", FLT_MIN, FLT_MAX);
    printf("computed double %e %e\n", DBL_MIN, DBL_MAX);
    printf("computed long_double %Le %Le\n", LDBL_MIN, LDBL_MAX);
}

long poww(long x, long y) {
    long res = 1;
    while (y > 0) {
        res *= x;
        --y;
    }
    return res;
}