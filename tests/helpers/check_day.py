"""Exercise 5-8: day_of_year and month_day reject impossible dates."""

from pretty import mismatch


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "the date was not converted.",
        got=got,
        wanted=wanted,
        notes=[
            "day_of_year returns the day of the year, from 1.",
            "A month outside 1..12, or a day outside that month, returns -1.",
            "month_day stores the month and the day.",
            "A yearday outside 1..365, or 1..366 in a leap year, stores -1 and -1.",
        ],
    )
