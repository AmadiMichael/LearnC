"""Exercise 4-7: require ungets(); compare replayed leftover input."""

from pretty import mismatch


def _has_ident(src, name):
    i = 0
    n = len(src)
    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        if ch == "/" and nxt == "/":
            i = src.find("\n", i)
            if i < 0:
                break
            continue
        if ch == "/" and nxt == "*":
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if ch == '"':
            i += 1
            while i < n and src[i] != '"':
                i += 2 if src[i] == "\\" else 1
            i += 1
            continue
        if ch == "'":
            i += 1
            while i < n and src[i] != "'":
                i += 2 if src[i] == "\\" else 1
            i += 1
            continue
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            if src[i:j] == name:
                return True
            i = j
            continue
        i += 1
    return False


def check_source(src):
    if not _has_ident(src, "ungets"):
        return False, "the exercise asks for a function named ungets."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got.strip("\n") == wanted.strip("\n"):
        notes.append("the characters are right except for a newline at the edge.")
    notes.append(
        "stdout is s, then the leftover stdin after the one thrown-away getch."
    )
    return False, mismatch(
        "stdout is not the string ungets pushed back, followed by the leftover input.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
