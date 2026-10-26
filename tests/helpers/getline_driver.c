#include <stdio.h>

int getLine(char *s, int lim);

static int read_lim(void)
{
    int c, n, any;

    n = 0;
    any = 0;
    while ((c = getchar()) != EOF && c != '\n') {
        if (c >= '0' && c <= '9') {
            n = 10 * n + (c - '0');
            any = 1;
        }
    }
    if (!any)
        return -1;
    return n;
}

int main(void)
{
    char s[1000];
    int lim, n, i;

    lim = read_lim();
    if (lim < 2 || lim > 1000)
        return 1;
    n = getLine(s, lim);
    printf("%d\n", n);
    for (i = 0; i < n; i++)
        putchar(s[i]);
    return 0;
}
