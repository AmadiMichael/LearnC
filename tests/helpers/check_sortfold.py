"""Exercise 5-15: the sort program gains a -f flag.

-f folds A-Z with a-z, so a and A compare equal. -n and -r stay as in 5-14.
"""

from pretty import mismatch


def _lines(text):
    if text == "":
        return []
    if text.endswith("\n"):
        return text.split("\n")[:-1]
    return text.split("\n")


def _fold(text):
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr(ord(ch) - ord("A") + ord("a")))
        else:
            out.append(ch)
    return "".join(out)


def _flags(argv):
    numeric = reverse = fold = False
    for arg in argv:
        if arg == "-n":
            numeric = True
        elif arg == "-r":
            reverse = True
        elif arg == "-f":
            fold = True
        else:
            raise ValueError("-n, -r, and -f are separate arguments, got {}".format(argv))
    return numeric, reverse, fold


def _key(line, numeric, fold):
    if numeric:
        return (float(line),)
    if fold:
        return (_fold(line),)
    return (line,)


def _in_order(lines, numeric, reverse, fold):
    keys = [_key(line, numeric, fold) for line in lines]
    for i in range(len(keys) - 1):
        if reverse:
            if keys[i] < keys[i + 1]:
                return False
        elif keys[i] > keys[i + 1]:
            return False
    return True


def expected(text, argv):
    numeric, reverse, fold = _flags(argv)
    lines = _lines(text)
    lines = sorted(lines, key=lambda line: _key(line, numeric, fold), reverse=reverse)
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def check(original, result, argv):
    numeric, reverse, fold = _flags(argv)
    got = _lines(result)
    wanted_lines = _lines(original)
    same = sorted(got) == sorted(wanted_lines)
    ordered = _in_order(got, numeric, reverse, fold)
    if same and ordered and result == ("" if not got else "\n".join(got) + "\n"):
        return True, ""
    wanted = expected(original, argv)
    if fold and reverse:
        note = "-f with -r sorts the folded lines into decreasing order."
    elif fold:
        note = "-f folds A-Z with a-z. a and A compare equal."
    elif numeric and reverse:
        note = "-n with -r sorts the numbers into decreasing order."
    elif numeric:
        note = "-n sorts the numbers into increasing order."
    elif reverse:
        note = "-r sorts the lines into decreasing order."
    else:
        note = "with no flag, the lines stay in increasing order."
    extra = []
    if fold:
        extra.append(
            "Lines that fold to the same text may appear in either order."
        )
    extra.extend(
        [
            "The newline that ends an input line is not part of the text.",
            "Write each sorted line, then a newline.",
        ]
    )
    return False, mismatch(
        "the lines are not in order.",
        got=result,
        wanted=wanted,
        notes=[note] + extra,
    )
