#include <stdio.h>

int getLine(char *s, int lim) {
    int c, i;
    int max = lim - 1;

    for(i = 0; i < max; i++) {
        c = getchar();

        if (c == EOF) {
            break;
        }

        *s++ = c;

        if (c == '\n') {
            i++;
            break;
        }
    }

    *s = '\0';

    return i;
}