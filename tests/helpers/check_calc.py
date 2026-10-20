"""Compare calculator stdout to a list of floating-point results."""

import math

from pretty import mismatch


def _floats(text):
    vals = []
    for tok in text.split():
        try:
            vals.append(float(tok))
        except ValueError:
            continue
    return vals


def _close(got, wanted):
    if wanted == 0:
        return math.isclose(got, wanted, abs_tol=1e-9)
    return math.isclose(got, wanted, rel_tol=1e-6, abs_tol=1e-9)


def check(got, wanted):
    got_n = _floats(got)
    want_n = _floats(wanted)
    if len(got_n) == len(want_n) and all(
        _close(g, w) for g, w in zip(got_n, want_n)
    ):
        return True, ""
    notes = []
    if len(got_n) != len(want_n):
        notes.append(
            "expected {} number(s) on stdout, got {}.".format(
                len(want_n), len(got_n)
            )
        )
    notes.append(
        "each newline pops and prints the top of the stack "
        "(optional leading tab). P also prints, without popping."
    )
    return False, mismatch(
        "stdout is not the calculator result(s).",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=notes,
    )
