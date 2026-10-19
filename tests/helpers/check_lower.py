"""Exercise 2-10: require ?: in code; compare stdout to ASCII A-Z folding."""

from pretty import mismatch


def _has_ternary(src):
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
        if ch == "?":
            return True
        i += 1
    return False


def check_source(src):
    if "tolower" in src or "ctype.h" in src:
        return False, "write lower yourself; do not call the library version."
    if not _has_ternary(src):
        return False, "the exercise asks for a conditional expression (? :), not if-else."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "stdout is not the input with A-Z folded to a-z (other characters unchanged).",
        got=got,
        wanted=wanted,
        tabstop=8,
    )
