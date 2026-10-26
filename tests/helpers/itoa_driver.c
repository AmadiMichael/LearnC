#include <stdio.h>

void itoa(int n, char *s);

int main(void)
{
    int n, i;
    char s[64];

    if (scanf("%d", &n) != 1)
        return 1;
    for (i = 0; i < 64; i++)
        s[i] = 0;
    itoa(n, s);
    printf("%s\n", s);
    return 0;
}
