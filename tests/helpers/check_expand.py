"""Exercise 3-3: require expand(); compare shorthand expansion on stdout."""

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
    if not _has_ident(src, "expand"):
        return False, "the exercise asks for a function named expand."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got.strip("\n") == wanted.strip("\n"):
        notes.append(
            "the expansion is right; print s2 as one line with a single newline at the end."
        )
    return False, mismatch(
        "stdout is not s1 with ranges like a-z, A-Z, and 0-9 written out.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
