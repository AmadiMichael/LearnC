"""Exercise 5-1: getint pushes back a sign that is not followed by a digit."""

import re

from pretty import mismatch


def _strip(src):
    out = []
    i = 0
    n = len(src)
    while i < n:
        if src.startswith("//", i):
            i = src.find("\n", i)
            i = n if i < 0 else i + 1
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        out.append(src[i])
        i += 1
    return "".join(out)


def check_source(src):
    text = _strip(src)
    if re.search(r"\bmain\s*\(", text):
        return False, "do not define main. The tests call getint and getch."
    if not re.search(r"\bgetint\s*\(", text):
        return False, "define getint(int *pn)."
    if not re.search(r"\bgetch\s*\(", text):
        return False, "define getch(). It reads the character getint pushes back."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "getint did not push a sign with no digit back on the input.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=[
            "One call to getint.",
            "return is what getint returned. pn is the integer it stored, or unchanged.",
            "left is the characters still waiting, including what getint pushed back.",
            "A + or - not followed by a digit is returned as 0, pn stays unchanged, and left still starts with that sign.",
        ],
    )
