"""Exercise 5-3: pointer version of strcat."""

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
        if src[i] == '"':
            out.append(src[i])
            i += 1
            while i < n and src[i] != '"':
                if src[i] == '\\' and i + 1 < n:
                    out.append(src[i])
                    i += 1
                out.append(src[i])
                i += 1
            if i < n:
                out.append(src[i])
                i += 1
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


def _body(text):
    for m in re.finditer(r"\bstrcat\s*\(", text):
        close = _matching_paren(text, m.end() - 1)
        if close < 0:
            continue
        j = close + 1
        while j < len(text) and text[j] in " \t\r\n":
            j += 1
        if j >= len(text) or text[j] == ";":
            continue
        i = text.find("{", j)
        if i < 0:
            continue
        depth = 0
        for k in range(i, len(text)):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    return text[i + 1 : k]
    return None


def check_source(src):
    text = _strip(src)
    if not re.search(r"\bvoid\s+strcat\s*\(", text):
        return False, "define void strcat(char *s, char *t)."
    body = _body(text)
    if body is None:
        return False, "define void strcat(char *s, char *t)."
    if "[" in body:
        return False, "write the pointer version. Do not index with s[i] or t[j]."
    if re.search(r"\bstrcat\s*\(", body):
        return False, "copy t onto the end of s in strcat itself."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "s is not t copied onto its end.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=[
            "The first line of stdin is s. The second line is t.",
            "The newline that ends a line is not part of that string.",
            "stdout is s after the copy, then a newline.",
        ],
    )
