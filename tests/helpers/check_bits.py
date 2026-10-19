"""Compare bit-exercise stdout to an unsigned decimal result."""

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
    elif got.strip().startswith("-"):
        notes.append(
            "the result is unsigned; use %u (not %d) so bits above 2^31-1 "
            "do not print as a negative number."
        )
    return False, mismatch(
        "stdout is not the unsigned result of the bit operation.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
