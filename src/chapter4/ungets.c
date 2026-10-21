#include <stdio.h>

#define MAX_BUF_SIZE 100

int getch(void);
void ungetch(int);
void ungets(char[MAX_BUF_SIZE], int);

int main() {
    char s[MAX_BUF_SIZE];

    int c;
    int i = 0;
    while (((c = getchar()) != EOF) && (c != '\n')) {
        s[i++] = c;
    }
    s[i++] = '\0';

    getch();

    ungets(s, i - 1);

    while ((c = getch()) != EOF) {
        putchar(c);
    }
}

void ungets(char s[MAX_BUF_SIZE], int i) {
    while (i > 0) {
        ungetch(s[--i]);
    }
}


char buf[MAX_BUF_SIZE];
int bufNextPointer = 0;

int getch() {
    if (bufNextPointer == 0) {
        int a = getchar();
        return a;
    } else {
        return buf[--bufNextPointer];
    }
}

void ungetch(int c) {
    if (bufNextPointer >= MAX_BUF_SIZE) {
        printf("Buffer full\n");
    } else {
        buf[bufNextPointer++] = c;
    }
}