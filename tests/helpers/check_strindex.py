"""Exercise 4-1: require strindex(); compare rightmost-match index."""

from pretty import mismatch


def rightmost(s, t):
    """Index of the rightmost occurrence of nonempty t in s, or -1."""
    if t == "":
        return -1
    pos = s.rfind(t)
    return pos


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
    if _has_ident(src, "strstr") or _has_ident(src, "strrstr"):
        return False, "write strindex yourself; do not call the library search."
    if not _has_ident(src, "strindex"):
        return False, "the exercise asks for a function named strindex."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got.strip() == wanted.strip():
        notes.append(
            "the number is right; print it as a single line of decimal digits "
            "(or -1) with one newline at the end, and no extra spaces."
        )
    try:
        g = int(got.strip())
        w = int(wanted.strip())
        if g >= 0 and w >= 0 and g < w:
            notes.append(
                "that looks like the leftmost match. this exercise wants the "
                "rightmost occurrence of t in s."
            )
    except ValueError:
        pass
    return False, mismatch(
        "stdout is not the 0-based index of the rightmost t in s (or -1).",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
