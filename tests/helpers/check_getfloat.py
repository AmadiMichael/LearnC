"""Exercise 5-2: getfloat, the floating-point analog of getint."""

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
        return False, "do not define main. The tests call getfloat and getch."
    if re.search(r"\b(float|double)\s+getfloat\s*\(", text):
        return False, "getfloat returns int. The floating value is stored through the pointer."
    if not re.search(r"\bint\s+getfloat\s*\(", text):
        return False, "define int getfloat(float *pn)."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "getfloat did not store the floating value.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=[
            "One call to getfloat.",
            "return is what getfloat returned. pn is the float it stored, or unchanged.",
            "left is the characters still waiting, including what getfloat pushed back.",
        ],
    )
