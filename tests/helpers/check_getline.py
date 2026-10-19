"""Compare 2-2 stdout to the characters the book's for-loop would store."""

from pretty import mismatch


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got == wanted + "\n":
        notes.append(
            "stdout has one extra newline. The book's loop stops at '\\n' "
            "and does not store it; print only the characters stored in the array."
        )
    elif wanted == "" and got == "\n":
        notes.append(
            "stdout is a single newline, but the loop stored nothing "
            "(empty input, or it stopped on the first '\\n')."
        )
    return False, mismatch(
        "stdout is not what the book's for-loop stores.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
