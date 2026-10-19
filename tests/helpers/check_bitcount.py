"""Compare 2-9 stdout to the number of 1-bits in unsigned x."""

from pretty import mismatch


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got.strip() == wanted.strip():
        notes.append(
            "the number is right; print it as a single line of decimal digits "
            "with one newline at the end, and no extra spaces."
        )
    return False, mismatch(
        "stdout is not the number of 1-bits in x.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
