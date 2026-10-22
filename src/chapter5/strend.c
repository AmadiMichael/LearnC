#include <stdio.h>

#define MAX 100

void getLine(char *);
int strend(char *, char *);

int main() {
    char s[MAX];
    char t[MAX];

    getLine(s);
    getLine(t);

    int i = strend(s, t);

    printf("%d\n", i);
}

void getLine(char *a) {
    char c;

    while((*a++ = c = getchar()) != EOF && c != '\n');

    *--a = '\0';
}

int strend(char *s, char *t) {
    // Cache start address.
    char *ss = s;
    char *tt = t;

    // Get to the end of both strings.
    while (*s++ != '\0');
    while (*t++ != '\0');

    // Compare backwards.
    while ((ss < s && tt < t) && (*--s == *--t));

    // If we are at the start of t and the last s and t matched, return true.
    return (tt == t && *s == *t);
}