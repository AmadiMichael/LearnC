#include <stdio.h>

#define UINT_SIZE 32

int main() {
    unsigned int x, n;

    // Copy inputs into vars.
    scanf("%u", &x);
    scanf("%u", &n);

    if (n == 0) {
        printf("%u\n", x);
        return 0;
    } else if (x == 0) {
        printf("%u\n", 0u);
        return 0;
    }

    // Copy the rightmost n bits of x, write that into i.
    // Shift x to the right by n.
    // Shift i to the left by (UINT_SIZE - n).
    // Or i and x. 

    // Copy the rightmost n bits of x, write that into i.
    unsigned int i = (1u << n) - 1;
    i = x & i;

    // Shift x to the right by n.
    x = x >> n;

    // Shift i to the left by (UINT_SIZE - n).
    i = i << (UINT_SIZE - n);

    x = x | i;

    printf("%u\n", x);
}