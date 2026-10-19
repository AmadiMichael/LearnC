#include <stdio.h>

#define SIZE 100

void clear(char s[SIZE]);
void itob(int n, char s[SIZE], int b);

int main() {
    int n = 0;
    int b = 0;
    scanf("%d", &n);
    scanf("%d", &b);

    char s[SIZE];
    clear(s);

    itob(n, s, b);

    printf("%s\n", s);
}

void itob(int n, char s[SIZE], int b) {
    int isNeg = n < 0;
    int i = 0;
    if (isNeg) {
        s[i++] = '-';
    }

    do {
        int m = n % b;

        if (isNeg) {
            m = -m;
        }

        if (m >= 10) {
            s[i++] = 'a' + (m - 10); 
        } else {
            s[i++] = '0' + m;
        }

        n /= b;
    } while (n != 0);

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