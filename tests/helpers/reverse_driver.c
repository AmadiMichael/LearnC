#include <stdio.h>

void reverse(char *s);

int main(void)
{
    char s[10000];
    int c, n;

    n = 0;
    while (n < 9998 && (c = getchar()) != EOF)
        s[n++] = c;
    if (n > 0 && s[n - 1] == '\n')
        n--;
    s[n] = '\0';
    reverse(s);
    printf("%s\n", s);
    return 0;
}
