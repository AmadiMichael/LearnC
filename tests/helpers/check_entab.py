"""Check entab output against input. Does not prescribe the 1-space preference."""

from expand import expand_tabs
from pretty import mismatch


def _space_run_ok(output, tabstop):
    """Fail if output uses two or more spaces where a tab would reach a stop.

    A single space that already reaches the next stop is the book's preference
    question: both a space and a tab are accepted.
    """
    col = 0
    i = 0
    n = len(output)
    while i < n:
        ch = output[i]
        if ch == "\n":
            col = 0
            i += 1
            continue
        if ch == "\t":
            col = col + (tabstop - (col % tabstop))
            i += 1
            continue
        if ch != " ":
            col += 1
            i += 1
            continue
        start_col = col
        j = i
        while j < n and output[j] == " ":
            j += 1
            col += 1
        run = j - i
        dist = tabstop - (start_col % tabstop)
        if dist >= 2 and run >= dist:
            return (
                False,
                "output still has a run of spaces that a tab could replace "
                "(same appearance, fewer characters)",
            )
        i = j
    return True, ""


def check(original, result, tabstop):
    expanded_in = expand_tabs(original, tabstop)
    expanded_out = expand_tabs(result, tabstop)
    if expanded_in != expanded_out:
        return False, mismatch(
            "displayed text does not match (tabs expanded, tab stops every {} columns).".format(
                tabstop
            ),
            got=expanded_out,
            wanted=expanded_in,
            tabstop=tabstop,
        )
    ok, msg = _space_run_ok(result, tabstop)
    if not ok:
        return False, msg
    return True, ""
