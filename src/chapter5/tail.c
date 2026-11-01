#include <stdio.h>
#include <stdlib.h>

#define DEFN 10
#define MAXLINES 5000
#define LINESIZE 1000

int readn(int argc, char *argv[]);
int readlines(char *[]);
int getLine(char *);
void tail(char *[], int, int);

int main(int argc, char *argv[]) {
    char *lineptrs[MAXLINES];

    // Read input lines.
    int l = readlines(lineptrs);

    // Get n.
    int n = readn(argc, argv);

    tail(lineptrs, l, n);
}

void tail(char *lineptrs[], int l, int n) {
    int start = n >= l ? 0 : l - n;
    
    while(start < l) {
        printf("%s", *(lineptrs + start));
        start++;
    }
}

int readlines(char *lineptrs[]) {
    char *line;
    int i = 0;

    while (i < MAXLINES && getLine(line = malloc(LINESIZE)) != EOF) {
        *lineptrs = line;
        lineptrs++;
        i++;
    }

    return i;
}

int getLine(char *line) {
    int c, i = 0;
    while (i < LINESIZE - 1) {
        if ((c = getchar()) == EOF) break;

        *line = c;
        line++; i++;
        if (c == '\n') break;
    }

    if (c == EOF && i == 0) return EOF;

    *line = '\0';
    return i;
}

int readn(int argc, char *argv[]) {
    if (argc > 1 && (**(argv + 1) == '-')) {
        return atoi(*(argv + 1) + 1);
    } else {
        return DEFN;
    }
}