/* Calls strncpy, strncat, and strncmp. The exercise does not ask for this main. */

#include <stdio.h>
#include <stdlib.h>

#define MAX 400

char *strncpy(char *s, char *t, int n);
char *strncat(char *s, char *t, int n);
int strncmp(char *s, char *t, int n);

static int read_line(char *s, int lim)
{
    int c, i;

    i = 0;
    while (i < lim - 1 && (c = getchar()) != EOF && c != '\n')
        s[i++] = c;
    s[i] = '\0';
    return i;
}

static int same(char *a, char *b)
{
    while (*a != '\0' && *a == *b) {
        a++;
        b++;
    }
    return *a == *b;
}

static void print_window(char *s, int len)
{
    int i;

    for (i = 0; i < len; i++) {
        if (s[i] == '\0')
            printf("\\0");
        else
            putchar(s[i]);
    }
    putchar('\n');
}

int main(void)
{
    char op[32], s[MAX], t[MAX], nbuf[32], buf[MAX];
    int n, len, i;
    char *r;

    read_line(op, 32);
    len = read_line(s, MAX);
    read_line(t, MAX);
    read_line(nbuf, 32);
    n = atoi(nbuf);

    if (same(op, "strncpy")) {
        for (i = 0; i <= len; i++)
            buf[i] = s[i];
        r = strncpy(buf, t, n);
        print_window(buf, len);
        if (r != buf)
            printf("return\n");
    } else if (same(op, "strncat")) {
        for (i = 0; i < MAX - 1; i++)
            buf[i] = 'A';
        buf[MAX - 1] = '\0';
        for (i = 0; i <= len; i++)
            buf[i] = s[i];
        r = strncat(buf, t, n);
        printf("%s\n", buf);
        if (r != buf)
            printf("return\n");
    } else if (same(op, "strncmp")) {
        printf("%d\n", strncmp(s, t, n));
    }
    return 0;
}
