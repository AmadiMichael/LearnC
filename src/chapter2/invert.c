#include <stdio.h>

#define UINT_SIZE 32u

int main() {
    // Flip n bits of x starting from position p from the right.
    unsigned int x, p, n;

    scanf("%u", &x);
    scanf("%u", &p);
    scanf("%u", &n);

    // Invert.
    unsigned int i = ~x;
    // Clean the upper bits.
    i = i << (UINT_SIZE - p - 1);
    // Clean the lower bits.
    i = i >> (UINT_SIZE - n);
    // Position back.
    i = i << ((p + 1) - n);

    // Clear the bits to be changed in x.
    unsigned int mask = (1u << n) - 1;
    mask = mask << ((p + 1) - n);
    mask = ~mask;

    x = x & mask;

    // Merge.
    x = x | i;

    printf("%u\n", x);
}