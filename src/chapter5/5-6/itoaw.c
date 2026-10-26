#include <stdio.h>

void itoa(int n, char *s, int w) {
    char *ss = s;
    int isNeg = n < 0;
    int done = 0;

    do {
        if (((s - ss) < w) && (done == 1)) {
            *s++ = ' ';
            continue;
        }

        int m = n % 10;
        if (isNeg) {
            m = -m;
        }

        *s++ = '0' + m;
        n /= 10;

        if (n == 0) {
            done = 1;
            if (isNeg) {
                *s++ = '-';
            }
        }
    } while ((n != 0) || ((s - ss) < w));

    *s = '\0';

    while (ss < s) {
        int intermediate = *ss;
        *ss++ = *--s;
        *s = intermediate;
    }
}