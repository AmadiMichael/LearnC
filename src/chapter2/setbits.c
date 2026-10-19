#include <stdio.h>

int main() {
    // Return `x` with `n` bits starting from index `p` replaced with 
    // the rightmost `n` bits of `y`.
    unsigned int x, p, n, y;

    scanf("%u", &x);
    scanf("%u", &p);
    scanf("%u", &n);
    scanf("%u", &y);

    // Set `n` bits in `x` from index `p` to 0 using &.

    // Create a mask for this.
    unsigned int mask = (1 << n) - 1;

    mask = mask << ((p + 1) - n);

    mask = ~mask;

    // Set `n` bits in `x` from index `p` to 0 using &.
    x = x & mask;

    // Get the mask to isolate the last `n` bits of `y`.
    mask = (1 << n) - 1;
    mask = y & mask;

    // Shift y to the right position.
    mask = mask << ((p + 1) - n);

    // Get result and set it to x.
    x = x | mask;

    printf("%u\n", x);
}