#include <stdio.h>

#define SIZE 100

void escape(char s[SIZE], char t[SIZE]);
void unescape(char s[SIZE], char t[SIZE]);
void clear(char v[SIZE]);

int main() {
    // Get the action.
    char action[SIZE];
    clear(action);
    scanf("%s", action);

    // Get rid of the breakline after the action.
    getchar();
    
    // Define the input string.
    char t[SIZE];
    clear(t);

    // Copy the rest of stdin into t.
    int c = 0;
    int i = 0;
    while (((c = getchar()) != EOF) && (i < SIZE)) {
        t[i++] = c;
    }

    // Define the output string.
    char s[SIZE];
    clear(s);
    
    // Call the expected function.
    if (action[0] == 'e') {
        escape(s, t);
    } else {
        unescape(s, t);
    }

    printf("%s", s);
}

void escape(char s[SIZE], char t[SIZE]) {
    // Counters for both strings.
    int sCounter = 0;
    int tCounter = 0;

    while (t[tCounter] != 0 && tCounter < SIZE && (sCounter + 2) < SIZE) {
        char v = t[tCounter++];
        switch (v) {
            case '\t': 
                {
                    s[sCounter++] = '\\';
                    s[sCounter++] = 't';
                    break;
                }
            case '\n':
                {
                    s[sCounter++] = '\\';
                    s[sCounter++] = 'n';
                    break;
                }
            default:
                {
                    s[sCounter++] = v;
                    break;
                }
        }
    }
}

void unescape(char s[SIZE], char t[SIZE]) {
    int sCounter = 0;
    int tCounter = 0;

    int seenSlash = 0;

    while(t[tCounter] != 0 && tCounter < SIZE) {
        int v = t[tCounter++];

        switch (v) {
            case '\\':
                {
                    if (seenSlash) {
                        s[sCounter++] = '\\';
                        seenSlash = 0;
                    } else {
                        seenSlash = 1;
                    }

                    break;
                }
            case 't':
                {
                    if (seenSlash) {
                        s[sCounter++] = '\t';
                        seenSlash = 0;
                    } else {
                        s[sCounter++] = 't';
                    }

                    break;
                }
            case 'n':
                {
                    if (seenSlash) {
                        s[sCounter++] = '\n';
                        seenSlash = 0;
                    } else {
                        s[sCounter++] = 'n';
                    }

                    break;
                }
            default:
                {
                    if (seenSlash) {
                        s[sCounter++] = '\\';
                        seenSlash = 0;
                    }
                    s[sCounter++] = v;

                    break;
                }
        }
    }

    // Any trailing slash should be added.
    if (seenSlash) s[sCounter++] = '\\';
}

void clear(char v[SIZE]) {
    int i = 0;
    while (i < SIZE) {
        v[i++] = 0;
    }
}