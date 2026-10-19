#include <stdio.h>

#define SIZE 20

void clear(char s[SIZE]);
void itoa(int n, char s[SIZE]);

int main() {
    int n;
    scanf("%d", &n);

    char s[SIZE];
    clear(s);

    itoa(n, s);

    printf("%s\n", s);
}

void itoa(int n, char s[SIZE]) {
    int isNeg = n < 0;
    int i = 0;
    if (isNeg) {
        s[i++] = '-';
    }

    do {
        int m = n % 10;
        if (isNeg) {
            m = -m;
        }
        s[i++] = '0' + m;
        n /= 10;
    } while (n != 0);

    // Reverse it back.
    int j = 0;
    if (isNeg) {
        j = 1;
    }
    while (j < i) {
        int intermediate = s[j];
        s[j++] = s[--i];
        s[i] = intermediate;
    }
}

void clear(char s[SIZE]) {
    int i = 0;
    while (i < SIZE) {
        s[i++] = 0;
    }
}