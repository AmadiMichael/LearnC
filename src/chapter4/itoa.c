#include <stdio.h>

#define MAX 100

int itoa(int, char[MAX], int, int);

int main() {
    int n;
    scanf("%d", &n);

    char s[MAX];
    int i = itoa(n, s, 0, n < 0);
    s[i] = '\0';

    printf("%s\n", s);
}

int itoa(int n, char s[MAX], int i, int isNeg) {
    if ((n < 0) && (i == 0)) {
        s[i++] = '-';
    }

    if (n / 10) {
        i = itoa(n / 10, s, i, isNeg);
    }
        
    if (isNeg) {
        s[i++] = '0' + (-(n % 10));
    } else {
        s[i++] = '0' + (n % 10);
    }
    
    return i;
}