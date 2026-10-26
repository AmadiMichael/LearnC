#include <stdio.h>

void itoa(int n, char *s, int w);

int main(void)
{
    int n, w, i;
    char s[256];

    if (scanf("%d", &n) != 1 || scanf("%d", &w) != 1)
        return 1;
    for (i = 0; i < 256; i++)
        s[i] = 0;
    itoa(n, s, w);
    printf("%s\n", s);
    return 0;
}
