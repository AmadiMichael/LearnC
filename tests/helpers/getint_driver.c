#include <stdio.h>

int getint(int *);
int getch(void);

enum { SENTINEL = 1111111117 };

static void print_return(int r) {
    printf("return ");
    if (r == EOF)
        printf("EOF\n");
    else if (r == 0)
        printf("0\n");
    else if (r == '\n')
        printf("'\\n'\n");
    else if (r == '\t')
        printf("'\\t'\n");
    else if (r == '\r')
        printf("'\\r'\n");
    else if (r == '\'')
        printf("'\\''\n");
    else if (r == '\\')
        printf("'\\\\'\n");
    else if (r >= 32 && r <= 126)
        printf("'%c'\n", r);
    else
        printf("%d\n", r);
}

static void print_escaped(int c) {
    if (c == '\\' || c == '"') {
        putchar('\\');
        putchar(c);
    } else if (c == '\n')
        printf("\\n");
    else if (c == '\t')
        printf("\\t");
    else if (c == '\r')
        printf("\\r");
    else
        putchar(c);
}

int main(void) {
    int n = SENTINEL;
    int r = getint(&n);
    int c;

    print_return(r);
    if (n == SENTINEL)
        printf("pn unchanged\n");
    else
        printf("pn %d\n", n);
    printf("left \"");
    while ((c = getch()) != EOF)
        print_escaped(c);
    printf("\"\n");
    return 0;
}
