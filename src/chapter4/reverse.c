#include <stdio.h>
#include <string.h>

#define MAX 200

void reverse(char[MAX], int, int);

int main() {
    char s[MAX];

    char c;
    int i = 0;
    while (((c = getchar()) != EOF) && (c != '\n')) {
        s[i++] = c;
    }

    reverse(s, 0, i);
    s[i] = '\0';

    printf("%s\n", s);
}

void reverse(char s[MAX], int i, int end) {
    if (i < end) {
        int inter = s[i];
        s[i] = s[--end];
        s[end] = inter;

        reverse(s, i+1, end);
    }
}

