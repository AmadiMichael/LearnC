#include <ctype.h>
#include <stdio.h>
#include "calc.h"

int getop(char s[]) {
    static int lastch = '\0';

    int i, c;

    int x = 1;
    if (lastch != '\0') {
        s[0] = c = lastch;
        lastch = '\0';
        if (c != ' ' && c != '\t') {
            x = 0;
        }
    }
    if (x) { 
        while ((s[0] = c = getch()) == ' ' || c == '\t');
    }

    s[1] = '\0';
    if (!isdigit(c) && c != '.') {
        return c; /* not a number */
    }

    i = 0;
    if (isdigit(c)) {
        /* collect integer part */
        while (isdigit(s[++i] = c = getch()));
    }

    if (c == '.') {
        /* collect fraction part */
        while (isdigit(s[++i] = c = getch()));
    }

    s[i] = '\0';
    if (c != EOF) {
        lastch = c;
    }

    return NUMBER;
}

