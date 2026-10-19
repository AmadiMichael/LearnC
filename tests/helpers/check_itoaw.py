"""Exercise 3-6: require itoa(n,s,w); compare left-padded decimal stdout."""

from pretty import mismatch


def format_padded(n, w):
    """Signed decimal n, blanks on the left up to minimum width w."""
    body = str(n)
    if w > len(body):
        body = (" " * (w - len(body))) + body
    return body


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
    if _has_ident(src, "sprintf") or _has_ident(src, "snprintf"):
        return False, "write itoa yourself; do not call sprintf."
    if not _has_ident(src, "itoa"):
        return False, "the exercise asks for a function named itoa."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got.strip() == wanted.strip():
        notes.append(
            "the digits are right; pad with spaces on the left to the minimum "
            "width, then print s and one newline. do not pad on the right."
        )
    if "\t" in got:
        notes.append("pad with spaces, not tabs.")
    wanted_n = wanted.strip()
    if wanted_n.startswith("-") and "-" not in got:
        notes.append(
            "the sign is missing. the minus is part of the converted number; "
            "spaces go to the left of it."
        )
    return False, mismatch(
        "stdout is not n written in a field at least w characters wide.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
