static char daytab[2][13] = {
    {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31},
    {0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
};

char *daysptr = &daytab[0][0];

/* day_of_year: set day of year from month & day */
int day_of_year(int year, int month, int day)
{
    int i, leap;

    if (month < 1 || month > 12) return -1;

    leap = (year%4 == 0 && year%100 != 0) || year%400 == 0;
    if (day < 1 || day > *(daysptr + (leap * 13) + month)) return -1;

    for (i = 1; i < month; i++)
        day += *(daysptr + (leap * 13) + i);
    return day;
}

/* month_day: set month, day from day of year */
void month_day(int year, int yearday, int *pmonth, int *pday)
{
    int i, leap;

    leap = (year%4 == 0 && year%100 != 0) || year%400 == 0;
    if (yearday < 1 || yearday > (365 + leap)) {
        *pmonth = *pday = -1;
        return;
    }

    for (i = 1; yearday > *(daysptr + (leap * 13) + i); i++)
        yearday -= *(daysptr + (leap * 13) + i);
    *pmonth = i;
    *pday = yearday;
}
