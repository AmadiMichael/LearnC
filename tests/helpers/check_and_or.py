"""Fail if a C file uses &&, ||, or iso646 and/or (Exercise 2-2)."""

import re


def _banned_in_code(src):
    """Return (line, token) for the first &&, ||, or iso646 and/or in code."""
    i = 0
    n = len(src)
    line = 1
    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        if ch == "\n":
            line += 1
            i += 1
            continue

        if ch == "/" and nxt == "/":
            i = src.find("\n", i)
            if i < 0:
                break
            continue

        if ch == "/" and nxt == "*":
            j = src.find("*/", i + 2)
            if j < 0:
                break
            line += src.count("\n", i, j)
            i = j + 2
            continue

        if ch == '"':
            i += 1
            while i < n and src[i] != '"':
                if src[i] == "\n":
                    line += 1
                if src[i] == "\\":
                    i += 2
                else:
                    i += 1
            i += 1
            continue

        if ch == "'":
            i += 1
            while i < n and src[i] != "'":
                if src[i] == "\\":
                    i += 2
                else:
                    i += 1
            i += 1
            continue

        if ch == "&" and nxt == "&":
            return line, "&&"
        if ch == "|" and nxt == "|":
            return line, "||"
        i += 1

    return None


def check(src):
    if re.search(r"#\s*include\s*<iso646\.h>", src):
        return False, "do not pull in iso646.h (that is still && / ||)."
    hit = _banned_in_code(src)
    if hit is None:
        return True, ""
    line, token = hit
    return False, "found {} on line {} — the exercise asks for a loop without && or ||.".format(
        token, line
    )
