#include <stdio.h>

#define SIZE 100

void clear(char s[SIZE]);
void itoa(int n, char s[SIZE], int w);

int main() {
    int n = 0;
    int w = 0;
    scanf("%d", &n);
    scanf("%d", &w);

    char s[SIZE];
    clear(s);

    itoa(n, s, w);

    printf("%s\n", s);
}

void itoa(int n, char s[SIZE], int w) {
    int i = 0;
    int isNeg = n < 0;
    int done = 0;

    do {
        if ((i < w) && (done == 1)) {
            s[i++] = ' ';
            continue;
        }

        int m = n % 10;
        if (isNeg) {
            m = -m;
        }

        s[i++] = '0' + m;
        n /= 10;

        if (n == 0) {
            done = 1;
            if (isNeg) {
                s[i++] = '-';
            }
        }
    } while ((n != 0) || (i < w));

    int j = 0;
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