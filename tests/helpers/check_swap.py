"""Exercise 4-14: macro swap(t, x, y)."""

from pretty import mismatch


def _macro_body(src):
    """Return the body of #define swap(...), or None."""
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
        if src[i] == "#" and (i == 0 or src[i - 1] == "\n"):
            j = i
            lines = []
            while j < n:
                end = src.find("\n", j)
                if end < 0:
                    end = n
                line = src[j:end]
                lines.append(line[:-1] if line.endswith("\\") else line)
                j = end + 1
                if not line.endswith("\\"):
                    break
            text = " ".join(lines).lstrip()
            if text.startswith("#"):
                rest = text[1:].lstrip()
                if rest.startswith("define"):
                    rest = rest[len("define") :].lstrip()
                    if rest.startswith("swap") and (
                        len(rest) == 4 or not (rest[4].isalnum() or rest[4] == "_")
                    ):
                        return rest[4:].lstrip()
            i = j
            continue
        i += 1
    return None


def check_source(src):
    body = _macro_body(src)
    if body is None or not body.startswith("("):
        return False, "define a macro swap(t, x, y)."
    if "{" not in body:
        return False, "use a block so the temporary has type t."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "stdout is not the swapped values.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=["swap(t, x, y) exchanges the two arguments. The temporary has type t."],
    )
