"""Exercise 5-6: the rewritten routine uses pointers, not array indexing."""

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
        if src[i] == '"' or src[i] == "'":
            quote = src[i]
            out.append(quote)
            i += 1
            while i < n and src[i] != quote:
                if src[i] == "\\" and i + 1 < n:
                    i += 2
                else:
                    i += 1
            if i < n and src[i] == quote:
                out.append(quote)
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


def _body(text, ret_re, name):
    pattern = r"\b" + ret_re + r"\s+" + name + r"\s*\("
    for m in re.finditer(pattern, text):
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


def check_pointer(src, name, ret_re, missing):
    text = _strip(src)
    body = _body(text, ret_re, name)
    if body is None:
        return False, missing
    if "[" in body:
        return False, "use pointers in " + name + ". The function body has no array index."
    if re.search(r"\b" + name + r"\s*\(", body):
        return False, "write " + name + " itself."
    return True, ""


def check_text(got, wanted, title, notes):
    if got == wanted:
        return True, ""
    return False, mismatch(title, got=got, wanted=wanted, tabstop=8, notes=notes)
