"""Exercise 5-5: strncpy, strncat, and strncmp, at most n characters."""

import re

from pretty import mismatch


_COPY_NOTES = [
    "strncpy copies at most n characters of t into s and returns s.",
    "If t has fewer than n characters, the rest of those n are '\\0'.",
    "If t has at least n characters, those n are copied and no '\\0' is written after them.",
    "Characters in s past n stay as they were.",
    "A null byte in s is shown here as the two characters \\0.",
]

_CAT_NOTES = [
    "strncat appends at most n characters of t to s, writes a '\\0' at the end, and returns s.",
]

_CMP_NOTES = [
    "strncmp compares at most n characters. A '\\0' ends either string.",
    "0 means s and t are equal within those characters.",
    "A negative value means s is less than t. A positive value means s is greater.",
    "Any integer with that sign matches.",
    "n of 0 compares no characters, so the result is 0.",
]


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
                if src[i] == "\\" and i + 1 < n:
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


def _body(text, ret_re, name):
    pattern = ret_re + r"\s*" + name + r"\s*\("
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


def check_source(src, names=None):
    text = _strip(src)
    specs = (
        (
            "strncpy",
            r"char\s*\*",
            "define char *strncpy(s, t, n). It copies at most n characters and returns s.",
        ),
        (
            "strncat",
            r"char\s*\*",
            "define char *strncat(s, t, n). It appends at most n characters and returns s.",
        ),
        (
            "strncmp",
            r"int",
            "define int strncmp(s, t, n). It compares at most n characters.",
        ),
    )
    for name, ret, missing in specs:
        if names is not None and name not in names:
            continue
        body = _body(text, ret, name)
        if body is None:
            return False, missing
        if re.search(r"\b" + name + r"\s*\(", body):
            return False, "write " + name + " itself. Its body calls " + name + "."
    return True, ""


def _sign(text):
    if text.count("\n") != 1 or not text.endswith("\n"):
        return None
    body = text[:-1]
    if not re.fullmatch(r"-?(0|[1-9][0-9]*)", body):
        return None
    value = int(body)
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0


def check(got, wanted, inp):
    op = inp.split("\n", 1)[0]
    if op == "strncmp":
        got_sign = _sign(got)
        wanted_sign = _sign(wanted)
        if got_sign is not None and got_sign == wanted_sign:
            return True, ""
        return False, mismatch(
            "strncmp did not return the right sign.",
            got=got,
            wanted=wanted,
            tabstop=8,
            notes=_CMP_NOTES,
        )
    if got == wanted:
        return True, ""
    if op == "strncat":
        title = "strncat did not append at most n characters of t."
        notes = _CAT_NOTES
    else:
        title = "strncpy did not copy at most n characters of t."
        notes = _COPY_NOTES
    return False, mismatch(title, got=got, wanted=wanted, tabstop=8, notes=notes)
