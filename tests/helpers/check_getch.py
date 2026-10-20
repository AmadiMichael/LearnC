"""Identity stdin→stdout for getch / ungetch programs."""

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


def check_source_getline(src):
    if not (_has_ident(src, "getline") or _has_ident(src, "getLine")):
        return False, "the exercise asks you to read lines with getline (getch/ungetch should go)."
    return True, ""


def check_source_getch(src):
    if not _has_ident(src, "getch") or not _has_ident(src, "ungetch"):
        return False, "write getch and ungetch."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "stdout should be a copy of stdin.",
        got=got,
        wanted=wanted,
        tabstop=8,
    )
