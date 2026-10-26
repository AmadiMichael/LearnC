#include <stdio.h>

void reverse(char *s) {
    // find end.
    char *ss = s;
    while (*s++ != '\0');
    --s;

    while (ss < s) {
        int inter = *ss;
        *ss++ = *--s;
        *s = inter;
    }
}