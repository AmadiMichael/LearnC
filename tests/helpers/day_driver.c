#include <stdio.h>
#include <string.h>

int day_of_year(int year, int month, int day);
void month_day(int year, int yearday, int *pmonth, int *pday);

int main(void)
{
    char op[16];
    int year, a, b;

    while (scanf("%15s", op) == 1) {
        if (strcmp(op, "day") == 0) {
            if (scanf("%d %d %d", &year, &a, &b) != 3)
                return 1;
            printf("%d\n", day_of_year(year, a, b));
        } else if (strcmp(op, "month") == 0) {
            if (scanf("%d %d", &year, &a) != 2)
                return 1;
            b = 0;
            month_day(year, a, &a, &b);
            printf("%d %d\n", a, b);
        } else {
            return 1;
        }
    }
    return 0;
}
