#include <stdio.h>

#ifndef LIM
#define LIM 8
#endif

void clear(char[LIM]);

int main() {
    int i;
    char s[LIM];
    clear(s);

    int c = getchar();
    for (i = 0; ((i < (LIM - 1)) + (c != '\n') + (c != EOF)) == 3; ++i) {
        s[i] = c;
        c = getchar();
    }

    printf("%s", s);
}

void clear(char s[LIM]) {
    int i = 0;
    while (i < LIM) {
        s[i++] = 0;
    }
}