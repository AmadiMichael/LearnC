"""Exercise 5-17: sort by fields, each with its own options.

The book does not name the argument form. These tests use a field number,
then the options for that field. Fields are separated by spaces. Field 1
is the first field. With no field number, the whole line is sorted as in
5-14 through 5-16. Flags stay separate arguments.
"""

from functools import cmp_to_key

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


def _parse(argv):
    specs = []
    field = None
    flags = {"n": False, "r": False, "f": False, "d": False}

    def flush():
        specs.append((field, dict(flags)))

    for arg in argv:
        if arg.isdigit() and int(arg) >= 1:
            if field is not None or any(flags.values()):
                flush()
            field = int(arg)
            flags = {"n": False, "r": False, "f": False, "d": False}
        elif arg == "-n":
            flags["n"] = True
        elif arg == "-r":
            flags["r"] = True
        elif arg == "-f":
            flags["f"] = True
        elif arg == "-d":
            flags["d"] = True
        else:
            raise ValueError(
                "arguments are field numbers and separate -n -r -f -d, got {}".format(
                    argv
                )
            )
    flush()
    return specs


def _field(line, number):
    if number is None:
        return line
    parts = line.split()
    if number > len(parts):
        return ""
    return parts[number - 1]


def _plain_key(text, flags):
    if flags["n"]:
        return (float(text),) if text else (float("-inf"),)
    value = _dir(text) if flags["d"] else text
    if flags["f"]:
        value = _fold(value)
    return (value,)


def _cmp_keys(a, b, reverse):
    if a < b:
        r = -1
    elif a > b:
        r = 1
    else:
        r = 0
    if reverse:
        r = -r
    return r


def _cmp_lines(left, right, specs):
    for number, flags in specs:
        r = _cmp_keys(
            _plain_key(_field(left, number), flags),
            _plain_key(_field(right, number), flags),
            flags["r"],
        )
        if r != 0:
            return r
    return 0


def _in_order(lines, specs):
    for i in range(len(lines) - 1):
        if _cmp_lines(lines[i], lines[i + 1], specs) > 0:
            return False
    return True


def expected(text, argv):
    specs = _parse(argv)
    lines = sorted(_lines(text), key=cmp_to_key(lambda a, b: _cmp_lines(a, b, specs)))
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def check(original, result, argv):
    specs = _parse(argv)
    got = _lines(result)
    wanted_lines = _lines(original)
    same = sorted(got) == sorted(wanted_lines)
    ordered = _in_order(got, specs)
    if same and ordered and result == ("" if not got else "\n".join(got) + "\n"):
        return True, ""
    wanted = expected(original, argv)
    fields = [number for number, _ in specs if number is not None]
    if fields:
        note = "sort by field {}, then later fields, each with its own options.".format(
            ", ".join(str(n) for n in fields)
        )
    else:
        note = "with no field number, the whole line is sorted as in 5-14 through 5-16."
    return False, mismatch(
        "the lines are not in order.",
        got=result,
        wanted=wanted,
        notes=[
            note,
            "Fields are separated by spaces. Field 1 is the first field.",
            "Lines that compare equal on the given fields may appear in either order.",
            "The newline that ends an input line is not part of the text.",
            "Write each sorted line, then a newline.",
        ],
    )
