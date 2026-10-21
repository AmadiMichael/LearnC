#include <stdio.h>

void ungetch(int);
int getch(void);

#define EMPTY -2

int buf = EMPTY;

int main() {
    int c;
    while((c = getch()) != EOF) {
        ungetch(c);
        ungetch('#');
        putchar(getch());
    }
}

int getch() {
    if (buf == EMPTY) {
        int a = getchar();
        return a;
    } else {
        int inter = buf;
        buf = EMPTY;
        return inter;
    }
}

void ungetch(int c) {
    if (buf == EMPTY) {
        buf = c;
    }
}