#include <stdio.h>

int main() {
    unsigned int x;

    scanf("%u", &x);

    int b = 0;
    while (x != 0) {
        x &= (x - 1);
        b++;
    }

    printf("%d\n", b);
}