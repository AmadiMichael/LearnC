"""Exercise 5-14: the sort program gains a -r flag, including with -n.

No flag keeps increasing order. -r reverses it. -n compares numbers.
-n and -r are separate arguments. -n -r and -r -n are those two flags.
"""

from pretty import mismatch


def _lines(text):
    if text == "":
        return []
    if text.endswith("\n"):
        return text.split("\n")[:-1]
    return text.split("\n")


def _flags(argv):
    numeric = reverse = False
    for arg in argv:
        if arg == "-n":
            numeric = True
        elif arg == "-r":
            reverse = True
        else:
            raise ValueError("-n and -r are separate arguments, got {}".format(argv))
    return numeric, reverse


def expected(text, argv):
    numeric, reverse = _flags(argv)
    lines = _lines(text)
    if numeric:
        lines = sorted(lines, key=float, reverse=reverse)
    else:
        lines = sorted(lines, reverse=reverse)
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def check(original, result, argv):
    numeric, reverse = _flags(argv)
    wanted = expected(original, argv)
    if result == wanted:
        return True, ""
    if numeric and reverse:
        note = "-n with -r sorts the numbers into decreasing order."
    elif numeric:
        note = "-n sorts the numbers into increasing order."
    elif reverse:
        note = "-r sorts the lines into decreasing order."
    else:
        note = "with no flag, the lines stay in increasing order."
    return False, mismatch(
        "the lines are not in order.",
        got=result,
        wanted=wanted,
        notes=[
            note,
            "The newline that ends an input line is not part of the text.",
            "Write each sorted line, then a newline.",
        ],
    )
