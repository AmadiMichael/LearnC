#include <stdio.h>

int strindex(char *s, char *t);

static void read_line(char *s, int lim)
{
    int c, i;

    i = 0;
    while (i < lim - 1 && (c = getchar()) != EOF && c != '\n')
        s[i++] = c;
    s[i] = '\0';
}

int main(void)
{
    char s[1000], t[1000];

    read_line(s, 1000);
    read_line(t, 1000);
    printf("%d\n", strindex(s, t));
    return 0;
}
