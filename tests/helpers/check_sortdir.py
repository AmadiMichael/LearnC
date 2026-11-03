"""Exercise 5-16: the sort program gains a -d flag.

-d compares only letters, numbers, and blanks. A letter is A-Z or a-z,
a number is 0-9, and a blank is a space. -d works with -f.
-n and -r stay as in 5-14. Flags are separate arguments.
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


def _dir(text):
    out = []
    for ch in text:
        if (
            ("A" <= ch <= "Z")
            or ("a" <= ch <= "z")
            or ("0" <= ch <= "9")
            or ch == " "
        ):
            out.append(ch)
    return "".join(out)


def _flags(argv):
    numeric = reverse = fold = directory = False
    for arg in argv:
        if arg == "-n":
            numeric = True
        elif arg == "-r":
            reverse = True
        elif arg == "-f":
            fold = True
        elif arg == "-d":
            directory = True
        else:
            raise ValueError(
                "-n, -r, -f, and -d are separate arguments, got {}".format(argv)
            )
    return numeric, reverse, fold, directory


def _key(line, numeric, fold, directory):
    if numeric:
        return (float(line),)
    text = _dir(line) if directory else line
    if fold:
        text = _fold(text)
    return (text,)


def _in_order(lines, numeric, reverse, fold, directory):
    keys = [_key(line, numeric, fold, directory) for line in lines]
    for i in range(len(keys) - 1):
        if reverse:
            if keys[i] < keys[i + 1]:
                return False
        elif keys[i] > keys[i + 1]:
            return False
    return True


def expected(text, argv):
    numeric, reverse, fold, directory = _flags(argv)
    lines = _lines(text)
    lines = sorted(
        lines,
        key=lambda line: _key(line, numeric, fold, directory),
        reverse=reverse,
    )
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def check(original, result, argv):
    numeric, reverse, fold, directory = _flags(argv)
    got = _lines(result)
    wanted_lines = _lines(original)
    same = sorted(got) == sorted(wanted_lines)
    ordered = _in_order(got, numeric, reverse, fold, directory)
    if same and ordered and result == ("" if not got else "\n".join(got) + "\n"):
        return True, ""
    wanted = expected(original, argv)
    if directory and fold:
        note = (
            "-d with -f compares letters, numbers, and blanks, "
            "and folds A-Z with a-z."
        )
    elif directory:
        note = "-d compares only letters, numbers, and blanks. A blank is a space."
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
    if directory or fold:
        extra.append(
            "Lines that compare equal under these flags may appear in either order."
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
