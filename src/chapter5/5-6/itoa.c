#include <stdio.h>

char *_itoa(int n, char *s);

void itoa(int n, char *s) {
    s = _itoa(n, s);
    *s = '\0';
}

char *_itoa(int n, char *s) {
    int isNeg = 0;

    if (n < 0) {
        isNeg = 1;
        *s++ = '-';
    }

    if (n / 10) {
        int m = isNeg ? -(n / 10) : n / 10;
        s = _itoa(m, s);
    }
        
    if (isNeg) {
        *s = '0' + (-(n % 10));
    } else {
        *s = '0' + (n % 10);
    }

    return ++s;
}