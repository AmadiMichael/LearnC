#include <stdio.h>

#define SIZE 100

void strcat(char *, char *);
void getLine(char *);

int main() {
    char s[SIZE];
    char t[SIZE];

    getLine(s);
    getLine(t);

    strcat(s, t);

    printf("%s\n", s);
}

void strcat(char *s, char *t) {
    // Get to the end of s.
    while(*s++ != '\0');

    // Go back to the terminator address;
    s--;

    // Copy t unto s until terminator.
    while ((*s++ = *t++));
}

void getLine(char *a) {
    char c;
    while((*a++ = c = getchar()) != EOF && (c != '\n'));
    *--a = '\0';
}