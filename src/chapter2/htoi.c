#include <stdio.h>

#define SIZE 100

void clear(char hex[SIZE]);
int filter(char hex[SIZE]);
int htoi(char hex[SIZE], int len);
int val(char v);

int main() {
    // Get the hex.
    char hex[SIZE];
    clear(hex);

    fgets(hex, SIZE, stdin);

    int len = filter(hex);

    int val = htoi(hex, len);

    if (val == -1) return 1;

    printf("%d\n", val);
}

int htoi(char hex[SIZE], int len) {
    int lenCache = len;
    int res = 0;
    int base = 1;
    while(lenCache > 0) {
        int c = val(hex[--lenCache]);
        if (c == -1) return -1;

        res += (c * base);
        base *= 16;
    }
    return res;
}

void clear(char hex[SIZE]) {
    int i = 0;
    while (i < SIZE) {
        hex[i++] = 0;
    }
}

int filter(char hex[SIZE]) {
    int i = 0;
    int j = 0;

    if ((hex[0] == '0') && ((hex[1] == 'x') || (hex[1] == 'X'))) {
        j = 2;
    }

    while ((j < SIZE) && (hex[j] != '\n') && (hex[j] != '\0')) {
        hex[i++] = hex[j++];
    }

    // Get len.
    int len = i;
    // Clean upper side.
    while (i < SIZE) {
        hex[i++] = 0;
    }

    return len;
}

int val(char c) {
    if ((c >= '0') && (c <= '9')) {
        return c - '0';
    } else if ((c >= 'a') && (c <= 'f')) {
        return (10 + (c - 'a'));
    } else if ((c >= 'A') && (c <= 'F')) {
        return (10 + (c - 'A'));
    } else {
        printf("Invalid hex");
        return -1;
    }
}