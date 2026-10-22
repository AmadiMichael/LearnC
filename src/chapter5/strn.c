#include <stdio.h>

#define MAX 100

char *strncpy(char *, char *, int);
char *strncat(char *, char *, int);
int strncmp(char *, char *, int);
void getLine(char *);

char *strncpy(char *s, char *t, int n) {
    char *ss = s;
    while(n > 0) {
        if (*t != '\0') {
            *s++ = *t++;
        } else {
            *s++ = *t;
        }

        --n;
    }
    return ss;
}

char *strncat(char *s, char *t, int n) {
    char *ss = s;

    while (*s++ != '\0');
    --s;

    while(n > 0) {
        if (*t == '\0') {
            *s = '\0';
            break;
        } else {
            *s++ = *t++;
        }

        --n;
    }
    *s = '\0';

    return ss;
}

int strncmp(char *s, char *t, int n) {
    for(; n > 0; ++s, ++t, --n) {
        if (*s == '\0' && *t != '\0') {
            return -1;
        }

        if (*s != '\0' && *t == '\0') {
            return 1;
        }

        if (*s == '\0' && *t == '\0') {
            return 0;
        }

        if (*s != *t) {
            return *s - *t;
        }
    }

    return 0;
}

void getLine(char *a) {
    char c;
    while((c = getchar()) != EOF && c != '\n') {
        *a++ = c;
    }

    *a = '\0';
}
