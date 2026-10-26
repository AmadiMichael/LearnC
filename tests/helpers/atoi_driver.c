#include <stdio.h>

int atoi(char *s);

int main(void)
{
    char s[1000];
    int c, i;

    i = 0;
    while (i < 999 && (c = getchar()) != EOF && c != '\n')
        s[i++] = c;
    s[i] = '\0';
    printf("%d\n", atoi(s));
    return 0;
}
