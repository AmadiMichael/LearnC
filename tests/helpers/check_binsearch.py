"""Compare 3-1 stdout to the index of x in a sorted array, or -1."""

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
        "stdout is not the 0-based index of x in the sorted array (or -1 if absent).",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
