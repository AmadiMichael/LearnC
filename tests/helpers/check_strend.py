"""Exercise 5-4: strend(s, t) is 1 when t occurs at the end of s."""

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


def _matching_paren(text, open_at):
    depth = 0
    for i in range(open_at, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _defined(text, name):
    for m in re.finditer(r"\b" + name + r"\s*\(", text):
        close = _matching_paren(text, m.end() - 1)
        if close < 0:
            continue
        j = close + 1
        while j < len(text) and text[j] in " \t\r\n":
            j += 1
        if j < len(text) and text[j] != ";":
            return True
    return False


def check_source(src):
    text = _strip(src)
    if not _defined(text, "strend"):
        return False, "define strend(s, t). It returns 1 or 0."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "strend did not say whether t occurs at the end of s.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=[
            "The first line of stdin is s. The second line is t.",
            "The newline that ends a line is not part of that string.",
            "Print 1 if t occurs at the end of s, and 0 otherwise, then a newline.",
            "An empty t occurs at the end of every s, including an empty s.",
        ],
    )
