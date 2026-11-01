"""Exercise 5-13: tail prints the last n lines of its input.

No argument means n is 10. One argument -n sets n. The lines are the
input split on newlines; a final line with no newline still counts.
n of 0 prints nothing. n larger than the input prints every line.
"""

import re

from pretty import mismatch


def lines_of(text):
    if text == "":
        return []
    if text.endswith("\n"):
        return [part + "\n" for part in text.split("\n")[:-1]]
    parts = text.split("\n")
    lines = [part + "\n" for part in parts[:-1]]
    lines.append(parts[-1])
    return lines


def n_of(argv):
    if not argv:
        return 10
    if len(argv) == 1 and re.fullmatch(r"-\d+", argv[0]):
        return int(argv[0][1:])
    raise ValueError("tail argument must be -n, got {}".format(argv))


def last_lines(text, n):
    if n <= 0:
        return ""
    return "".join(lines_of(text)[-n:])


def check(original, result, argv):
    n = n_of(argv)
    wanted = last_lines(original, n)
    if result == wanted:
        return True, ""
    if n == 0:
        note = "-0 prints nothing."
    elif n >= len(lines_of(original)):
        note = "n is {}, which covers the whole input, so every line is printed.".format(n)
    else:
        note = "n is {}. Print those last lines and nothing before them.".format(n)
    return False, mismatch(
        "tail did not print the last lines.",
        got=result,
        wanted=wanted,
        notes=[note],
    )


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


def check_storage(src):
    """Section 5.6 stores lines through an array of pointers.

    A declaration such as char lines[MAXLINES][MAXLEN] is the
    two-dimensional array the exercise rules out. char *lineptr[MAXLINES]
    has one pair of brackets, and argv[1][0] is a use, not that declaration.
    """
    text = re.sub(r"\s+", " ", _strip(src))
    pattern = re.compile(
        r"\bchar\b[^;{}]*\b[A-Za-z_]\w*\s*\[[^\[\]]*\]\s*\[[^\[\]]*\]"
    )
    for stmt in re.split(r"[;{}]", text):
        if pattern.search(stmt):
            return False, (
                "store the lines as in the sorting program of Section 5.6, "
                "through an array of pointers. "
                "A two-dimensional array of fixed size is not that storage."
            )
    return True, ""
