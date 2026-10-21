"""Checks for the book's calculator and for exercise 4-11.

The exercise changes getop: the character read past a number is kept in a
static variable inside getop. getop must not call ungetch, directly or
through another function.
"""

from pretty import mismatch


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "stdout is not the calculator result.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=[
            "a newline prints a tab, then the top of the stack, with %.8g.",
            "operators are + - * /.",
            "the character read past a number is the next token.",
        ],
    )


def _line_start(src, i):
    j = i
    while j > 0 and src[j - 1] != "\n":
        if not src[j - 1].isspace():
            return False
        j -= 1
    return True


def _skip_quote(src, i):
    quote = src[i]
    i += 1
    n = len(src)
    while i < n and src[i] != quote:
        i += 2 if src[i] == "\\" else 1
    return min(i + 1, n)


def tokenize(src):
    tokens = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c.isspace():
            i += 1
            continue
        if c == "#" and _line_start(src, i):
            while i < n and src[i] != "\n":
                if src[i] == "\\" and i + 1 < n and src[i + 1] == "\n":
                    i += 2
                    continue
                i += 1
            continue
        if src.startswith("//", i):
            i = src.find("\n", i)
            i = n if i < 0 else i + 1
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c == '"' or c == "'":
            i = _skip_quote(src, i)
            continue
        if c.isalpha() or c == "_":
            j = i + 1
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            tokens.append(("ident", src[i:j]))
            i = j
            continue
        if c.isdigit():
            j = i + 1
            while j < n and (src[j].isalnum() or src[j] == "."):
                j += 1
            i = j
            continue
        tokens.append(("punct", c))
        i += 1
    return tokens


def _match(tokens, open_i, open_ch, close_ch):
    depth = 0
    for i in range(open_i, len(tokens)):
        kind, val = tokens[i]
        if kind != "punct":
            continue
        if val == open_ch:
            depth += 1
        elif val == close_ch:
            depth -= 1
            if depth == 0:
                return i
    return None


def function_bodies(src):
    tokens = tokenize(src)
    bodies = {}
    duplicate_getop = False
    i = 0
    while i < len(tokens):
        kind, val = tokens[i]
        if kind == "ident" and i + 1 < len(tokens) and tokens[i + 1] == ("punct", "("):
            end_paren = _match(tokens, i + 1, "(", ")")
            nxt = None if end_paren is None else end_paren + 1
            if nxt is not None and nxt < len(tokens) and tokens[nxt] == ("punct", "{"):
                end_body = _match(tokens, nxt, "{", "}")
                if end_body is not None:
                    if val == "getop" and val in bodies:
                        duplicate_getop = True
                    bodies[val] = tokens[nxt + 1 : end_body]
                    i = end_body + 1
                    continue
        i += 1
    return bodies, duplicate_getop


def _calls(tokens, name):
    n = 0
    for i, (kind, val) in enumerate(tokens):
        if kind == "ident" and val == name:
            if i + 1 < len(tokens) and tokens[i + 1] == ("punct", "("):
                n += 1
    return n


def _callees(tokens):
    names = []
    for i, (kind, val) in enumerate(tokens):
        if kind == "ident" and i + 1 < len(tokens) and tokens[i + 1] == ("punct", "("):
            names.append(val)
    return names


def _has(tokens, name):
    return any(kind == "ident" and val == name for kind, val in tokens)


def _static_array(tokens):
    for i, (kind, val) in enumerate(tokens):
        if kind == "ident" and val == "static":
            for kind2, val2 in tokens[i + 1 :]:
                if kind2 == "punct" and val2 == ";":
                    break
                if kind2 == "punct" and val2 == "[":
                    return True
    return False


def _ungetch_from(name, bodies, seen):
    if name in seen or name not in bodies:
        return None
    seen.add(name)
    body = bodies[name]
    if name != "getop" and _calls(body, "ungetch"):
        return (
            "{} calls ungetch. The extra character belongs in the static "
            "variable inside getop."
        ).format(name)
    for callee in _callees(body):
        if callee == "ungetch":
            continue
        msg = _ungetch_from(callee, bodies, seen)
        if msg:
            return msg
    return None


def check_source(src):
    bodies, duplicate = function_bodies(src)
    if "getop" not in bodies:
        return False, "define getop."
    if duplicate:
        return False, "define getop once."
    body = bodies["getop"]
    problems = []
    if not _has(body, "static"):
        problems.append("keep the extra character in a static variable inside getop.")
    elif _static_array(body):
        problems.append("use one static variable inside getop, not an array.")
    if _calls(body, "ungetch"):
        problems.append("getop must not call ungetch.")
    else:
        msg = _ungetch_from("getop", bodies, set())
        if msg:
            problems.append(msg)
    if problems:
        return False, " ".join(problems)
    return True, ""
