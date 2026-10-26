#include <ctype.h>
#include <stdio.h>

int atoi(char *s) {
    int v = 0;
    int c;

    while(isspace(c = *s++));

    int sign = c == '-' ? -1 : 1; 
    if ((c == '-' || c == '+') && isdigit(*s)) {
        for(c = *s; isdigit(c); c = *++s) {
        v = (v * 10) + (c - '0');
        }

        return v *= sign;
    }

    for(; isdigit(c); c = *s++) {
        v = (v * 10) + (c - '0');
    }
    return v *= sign;
}