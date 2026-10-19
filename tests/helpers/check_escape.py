"""Exercise 3-2: require switch; compare escape / unescape stdout."""

from pretty import mismatch


def _has_ident(src, name):
    i = 0
    n = len(src)
    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        if ch == "/" and nxt == "/":
            i = src.find("\n", i)
            if i < 0:
                break
            continue
        if ch == "/" and nxt == "*":
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if ch == '"':
            i += 1
            while i < n and src[i] != '"':
                i += 2 if src[i] == "\\" else 1
            i += 1
            continue
        if ch == "'":
            i += 1
            while i < n and src[i] != "'":
                i += 2 if src[i] == "\\" else 1
            i += 1
            continue
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            if src[i:j] == name:
                return True
            i = j
            continue
        i += 1
    return False


def check_source(src):
    if not _has_ident(src, "switch"):
        return False, "the exercise asks you to use a switch."
    return True, ""


def _notes(got, wanted):
    notes = []
    if got != wanted and got.strip("\n") == wanted.strip("\n"):
        notes.append(
            "the converted text is right except for a newline at the edge; "
            "print only s — no extra newline after it."
        )
    if got.startswith("\\n") and not wanted.startswith("\\n"):
        notes.append(
            "output starts with the two characters \\n. the newline after "
            "the direction word is not part of t — finish reading that line first."
        )
    elif got.startswith("\n") and not wanted.startswith("\n"):
        notes.append(
            "output starts with a real newline. the newline after "
            "the direction word is not part of t."
        )
    if "\t" in got and "\t" not in wanted:
        notes.append(
            "stdout still has a real tab. for escape, write the two "
            "characters \\ and t."
        )
    if "\n" in got and "\n" not in wanted:
        notes.append(
            "stdout still has a real newline. for escape, write the two "
            "characters \\ and n."
        )
    if "\\t" in got and "\t" in wanted and "\\t" not in wanted:
        notes.append(
            "stdout has the two characters \\t. for unescape, turn that "
            "sequence into a real tab."
        )
    if "\\n" in got and "\n" in wanted and "\\n" not in wanted:
        notes.append(
            "stdout has the two characters \\n. for unescape, turn that "
            "sequence into a real newline."
        )
    return notes


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "stdout is not the converted string s.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=_notes(got, wanted),
    )
