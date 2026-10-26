"""Exercise 5-7: the line sorter stores lines in an array from main."""

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
            i += 1
            while i < n and src[i] != quote:
                if src[i] == "\\" and i + 1 < n:
                    i += 2
                else:
                    i += 1
            if i < n:
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


def _body(text, name):
    pattern = r"\b" + name + r"\s*\("
    for m in re.finditer(pattern, text):
        close = _matching_paren(text, m.end() - 1)
        if close < 0:
            continue
        j = close + 1
        while j < len(text) and text[j] in " \t\r\n":
            j += 1
        if j >= len(text) or text[j] != "{":
            continue
        i = j
        depth = 0
        for k in range(i, len(text)):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    return text[i + 1 : k]
    return None


def _char_arrays(text):
    return re.findall(r"\bchar\s+([A-Za-z_][A-Za-z0-9_]*)\s*\[", text)


def _call_args(text, name):
    found = []
    for m in re.finditer(r"\b" + name + r"\s*\(", text):
        close = _matching_paren(text, m.end() - 1)
        if close < 0:
            continue
        found.append(text[m.end() : close])
    return found


def check_source(src):
    text = _strip(src)
    body = _body(text, "readlines")
    if body is None:
        return False, "rewrite readlines."
    if re.search(r"\b(alloc|malloc|calloc|realloc)\s*\(", body):
        return False, (
            "readlines still calls alloc. "
            "Store the lines in an array supplied by main."
        )
    main = _body(text, "main")
    if main is None:
        return False, "main passes readlines the array that holds the lines."
    arrays = set(_char_arrays(text))
    passed = False
    for args in _call_args(main, "readlines"):
        for name in arrays:
            if re.search(r"\b" + name + r"\b", args):
                passed = True
    if not passed:
        return False, (
            "main passes readlines a char array, "
            "and readlines stores the lines there."
        )
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "the lines are not in order.",
        got=got,
        wanted=wanted,
        notes=[
            "The newline that ends an input line is not part of the text.",
            "Write each sorted line, then a newline.",
        ],
    )
