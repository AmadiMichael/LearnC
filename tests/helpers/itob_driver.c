#include <stdio.h>

void itob(int n, char *s, int b);

int main(void)
{
    int n, b, i;
    char s[256];

    if (scanf("%d", &n) != 1 || scanf("%d", &b) != 1)
        return 1;
    for (i = 0; i < 256; i++)
        s[i] = 0;
    itob(n, s, b);
    printf("%s\n", s);
    return 0;
}
