#include <stdio.h>

#define SIZE 100
#define DEF -1

void clear(char[SIZE]);

int main() {
    char s1[SIZE];
    char s2[SIZE];
    int ret = DEF;

    clear(s1);
    clear(s2);

    fgets(s1, SIZE, stdin);
    fgets(s2, SIZE, stdin);

    char c;
    for (int i = 0; (i < SIZE) && ((c = s1[i]) != '\n') && (c != '\0'); i++) {
        char d;
        for (int j = 0; (j < SIZE) && ((d = s2[j]) != '\n') && (d != '\0'); j++) {
            if (c == d) {
                ret = i;
                break;
            }
        }

        if (ret != DEF) break;
    }

    printf("%d\n", ret);
}

void clear(char a[SIZE]) {
    int i = 0;
    while (i < SIZE) {
        a[i++] = 0;
    }
}