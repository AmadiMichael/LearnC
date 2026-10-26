#include <stdio.h>

int strindex(char *s, char *t) {
    for (int i = 0; (*s != '\0'); i++) {
        char *ss = s;
        char *tt = t;

        for(; *tt != '\0'; tt++, ss++) {
            if (*tt != *ss) break;
        }
        if ((*tt == '\0') && (tt - t > 0)) {
            return i;
        }

        ++s;
    }

    return -1;
}