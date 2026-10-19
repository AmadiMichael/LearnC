"""Compare 2-4 stdout to s1 with every character that appears in s2 removed."""

from pretty import mismatch


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got + "\n" == wanted:
        notes.append(
            "the squeezed text looks right; print it, then one newline, "
            "like a normal line of output."
        )
    elif got.strip("\n") == wanted.strip("\n") and got != wanted:
        notes.append(
            "the remaining characters look right; match the line exactly "
            "(no extra spaces, one newline at the end)."
        )
    return False, mismatch(
        "stdout is not s1 after deleting every character that occurs in s2.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
