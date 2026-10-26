#include <stdio.h>

void itob(int n, char *s, int b) {
    int isNeg = n < 0;
    char *ss = s;
    if (isNeg) {
        ss++;
        *s++ = '-';
    }

    do {
        int m = n % b;

        if (isNeg) {
            m = -m;
        }

        if (m >= 10) {
            *s++ = 'a' + (m - 10); 
        } else {
            *s++ = '0' + m;
        }

        n /= b;
    } while (n != 0);
    *s = '\0';

    while (ss < s) {
        int intermediate = *ss;
        *ss++ = *--s;
        *s = intermediate;
    }


}