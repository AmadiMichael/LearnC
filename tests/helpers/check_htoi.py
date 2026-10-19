"""Compare 2-3 stdout to the decimal value of a hex string."""

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
    elif got.strip().lower().startswith("0x"):
        notes.append("print a decimal integer, not a hex string.")
    return False, mismatch(
        "stdout is not the decimal value of the hex input.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
