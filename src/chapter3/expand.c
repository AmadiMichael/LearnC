#include <stdio.h>

#define SIZE 100

void expand(char s1[SIZE], char s2[SIZE]);
void clear(char v[SIZE]);
int getType(char a);

enum RANGE_POSSIBILITIES {
    NONE,
    LETTER,
    HYPHEN
};

enum RANGE_TYPE {
    DEF,
    UPPER,
    LOWER,
    NUMBER
};

int main() {
    // Declare variables.
    char s1[SIZE];
    char s2[SIZE];

    // Clear the variables.
    clear(s1);
    clear(s2);

    // Copy stdin into s1.
    char c = 0;
    int i = 0;
    while (((c = getchar()) != EOF) && (c != '\n')) {
        s1[i++] = c;
    }

    // Call expand to expand it into s2.
    expand(s1, s2);

    // Print s2.
    printf("%s\n", s2);
}

void expand(char s1[SIZE], char s2[SIZE]) {
    // Declare required variables.

    int s1Counter = 0;
    int s2Counter = 0;
    char v = 0;

    enum RANGE_POSSIBILITIES rangePossibilities = NONE;
    char rangeStart = 0;

    while ((s1Counter < SIZE) && ((v = s1[s1Counter++]) != 0)) {
        switch (v) {
            case '-': {
                if (rangePossibilities == NONE) {
                    s2[s2Counter++] = v;
                } else if (rangePossibilities == LETTER) {
                    rangePossibilities = HYPHEN;
                } else {
                    s2[s2Counter++] = v;
                    s2[s2Counter++] = v;
                    rangePossibilities = NONE;
                    rangeStart = 0;
                }

                break;
            }
            case ' ': {
                if (rangePossibilities == NONE) {
                    s2[s2Counter++] = v;
                } else if (rangePossibilities == LETTER) {
                    s2[s2Counter++] = v;
                    rangePossibilities = NONE;
                    rangeStart = 0;
                } else {
                    s2[s2Counter++] = '-';
                    s2[s2Counter++] = v;
                    rangePossibilities = NONE;
                    rangeStart = 0;
                }

                break;
            }
            default: {
                if (rangePossibilities == NONE) {
                    s2[s2Counter++] = v;
                    rangePossibilities = LETTER;
                    rangeStart = v;
                } else if (rangePossibilities == LETTER) {
                    s2[s2Counter++] = v;
                    rangePossibilities = LETTER;
                    rangeStart = v;
                } else {
                    enum RANGE_TYPE t = DEF;
                    if (((t = getType(rangeStart)) == getType(v)) && (t != DEF) && (rangeStart <= v)) {
                        while (rangeStart < v) {
                            s2[s2Counter++] = ++rangeStart;
                        }
                    } else {
                        s2[s2Counter++] = '-';
                        s2[s2Counter++] = v;
                    }

                    rangePossibilities = LETTER;
                    rangeStart = v;
                }

                break;
            }
        }
    }

    if (rangePossibilities == HYPHEN) s2[s2Counter++] = '-';
}

int getType(char a) {
    if (a >= 'A' && a <= 'Z') {
        return UPPER;
    } else if (a >= 'a' && a <= 'z') {
        return LOWER;
    } else if (a >= '0' && a <= '9') {
        return NUMBER;
    } else {
        return DEF;
    }
}

void clear(char v[SIZE]) {
    int i = 0;
    while (i < SIZE) {
        v[i++] = 0;
    }
}