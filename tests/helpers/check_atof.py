"""Exercise 4-2: require atof(); compare printed value as a float."""

import math
import re

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
    if re.search(r"#\s*include\s*<stdlib\.h>", src):
        return False, "write atof yourself; do not pull in the library version."
    if _has_ident(src, "strtod") or _has_ident(src, "strtof"):
        return False, "write atof yourself; do not call strtod."
    if not _has_ident(src, "atof"):
        return False, "the exercise asks for a function named atof."
    return True, ""


def _parse(text):
    token = text.strip().split()[0] if text.strip() else ""
    try:
        return float(token)
    except ValueError:
        return None


def _close(got, wanted):
    if wanted == 0:
        return math.isclose(got, wanted, abs_tol=1e-12)
    return math.isclose(got, wanted, rel_tol=1e-8, abs_tol=1e-12)


def check(got, wanted):
    want_n = _parse(wanted)
    got_n = _parse(got)
    if want_n is not None and got_n is not None and _close(got_n, want_n):
        return True, ""
    notes = []
    if got_n is None:
        notes.append(
            "print the number as a floating-point value, then a newline "
            "(the book's %.8g from this section is enough)."
        )
    elif want_n is not None and abs(got_n) > 0 and abs(got_n - want_n) / max(abs(want_n), 1e-300) > 0.5:
        notes.append(
            "this looks like the exponent was ignored. after the fraction, "
            "e or E and an optionally signed integer scale the value by powers of 10."
        )
    return False, mismatch(
        "stdout is not the floating-point value of the input string.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
