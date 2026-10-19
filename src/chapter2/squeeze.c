#include <stdio.h>

#define SIZE 100
#define TRUE 1
#define FALSE 0

void clear(char[SIZE]);

int main() {
    // Declare variables.
    char s1[SIZE];
    char s2[SIZE];

    // Initialize variables
    clear(s1);
    clear(s2);

    // Copy inputs from stdin.
    fgets(s1, SIZE, stdin);
    fgets(s2, SIZE, stdin);

    // For every char in s1 check if it is in s2, if not write it back to s1.
    int resIndex = 0;
    char c;
    for (int i = 0; (i < SIZE) && ((c = s1[i]) != '\n') && (c != '\0'); i++) {
        char d;
        int found = FALSE;

        for (int  j = 0; (j < SIZE) && ((d = s2[j]) != '\n') && (d != '\0'); j++) {
            if (c == d) {
                found = TRUE;
                break;
            }
        }

        if (found == FALSE) s1[resIndex++] = c;
    }

    // Add new line and null terminate to avoid further reading
    s1[resIndex++] = '\n';
    s1[resIndex] = '\0';

    // Print results.
    printf("%s", s1);
}

void clear(char a[SIZE]) {
    int i = 0;
    while (i < SIZE) {
        a[i++] = 0;
    }
}