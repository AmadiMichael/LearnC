"""Compare 2-5 stdout to the first index in s1 of any character from s2."""

from pretty import mismatch


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got.strip() == wanted.strip():
        notes.append(
            "the number is right; print it as a single line of decimal digits "
            "(or -1) with one newline at the end, and no extra spaces."
        )
    return False, mismatch(
        "stdout is not the first location in s1 of a character from s2 "
        "(0-based, or -1 if none).",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
