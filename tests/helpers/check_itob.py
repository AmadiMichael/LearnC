"""Exercise 3-5: require itob(); compare base-b stdout."""

from pretty import mismatch

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def format_base(n, b):
    """Signed integer n in base b (2..36), lowercase letters, no prefix."""
    if n == 0:
        return "0"
    sign = n < 0
    if sign:
        n = -n
    chars = []
    while n:
        chars.append(DIGITS[n % b])
        n //= b
    if sign:
        chars.append("-")
    chars.reverse()
    return "".join(chars)


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
        return False, "write itob yourself; do not call sprintf."
    if not _has_ident(src, "itob"):
        return False, "the exercise asks for a function named itob."
    return True, ""


def check(got, wanted):
    if got == wanted:
        return True, ""
    notes = []
    if got.strip() == wanted.strip():
        notes.append(
            "the digits are right; print them as one line with a single newline "
            "at the end, and no extra spaces."
        )
    if got.strip().lower() == wanted.strip().lower() and got.strip() != wanted.strip():
        notes.append("digits above 9 are lowercase letters (a-f), not A-F.")
    gs = got.strip().lower()
    if gs.startswith("0x") or gs.startswith("-0x"):
        notes.append("print the digits only; no 0x prefix.")
    wanted_n = wanted.strip()
    if wanted_n.startswith("-") and not got.lstrip().startswith("-"):
        notes.append(
            "the sign is missing. treat itob like itoa: a leading - if n is "
            "negative, then the digits of the magnitude in base b."
        )
    return False, mismatch(
        "stdout is not n written in the requested base.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
