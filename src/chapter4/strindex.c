#include <stdio.h>

#define SIZE 1000

void getLine(char l[SIZE]);
int strindex(char s[SIZE], char t[SIZE]);


int main() {
    char s[SIZE];
    char t[SIZE];

    getLine(s);
    getLine(t);

    int i = strindex(s, t);

    printf("%d\n", i);
}

int strindex(char s[SIZE], char t[SIZE]) {
    int ans = -1;
    int i;
    for (i = 0; (s[i] != '\0') && (i < SIZE); i++) {
        int j, k;
        for(j = i, k = 0; (t[k] != '\0') && (k < SIZE); j++, k++) {
            if (s[j] != t[k]) break;
        }
        if ((k > 0) && (t[k] == '\0')) {
            ans = i;
        }
    }

    return ans;
}


void getLine(char l[SIZE]) {
    int i = 0;
    int c;
    while(((c = getchar()) != EOF) && (c != '\n')) {
        l[i++] = c;
    }

    l[i++] = '\0';
}