#include <ctype.h>
#include <stdio.h>
// #include "getint.c"

int getch(void);
void ungetch(int c);

// #define BUFSIZE 100

// int buf[BUFSIZE];
// int bufp = 0;

// int getch(void) /* get a (possibly pushed-back) character */
// {
//     return (bufp > 0) ? buf[--bufp] : getchar();
// }

// void ungetch(int c) /* push character back on input */
// {
//     if (bufp >= BUFSIZE)
//         printf("ungetch: too many characters\n");
//     else
//         buf[bufp++] = c;
// }

int getfloat(float *pn) {
    int c;

    while(isspace(c = getch()));

    if (!isdigit(c) && c != EOF && c != '+' && c != '-' && c != '.') {
        ungetch(c);
        return 0;
    }

    int sign = (c == '-') ? -1 : 1;

    if (c == '-' || c == '+') {
        int d = c;
        c = getch();

        if (!isdigit(c) && c != '.') {
            ungetch(c);
            ungetch(d);
            return 0;
        }
    }

    float i = 10;
    int seenDec = 0;
    for (*pn = 0; isdigit(c) || c == '.'; c = getch()) {
        if (isdigit(c)) {
            if (seenDec) {
                *pn += ((float)1 / i) * (c - '0');
                i *= 10;
            } else {
                *pn = (*pn * 10) + (c - '0');
            }
        } else {
            if (!seenDec) {
                seenDec = 1;
            } else {
                break;
            }
        }
    }
    *pn *= sign;

    if (c != EOF) {
        ungetch(c);
    }

    return c;
}