"""Check detab output: tabs gone, same displayed columns as the input."""

from expand import expand_tabs
from pretty import mismatch


def check(original, result, tabstop):
    expected = expand_tabs(original, tabstop)
    if result == expected:
        return True, ""
    notes = []
    if "\t" in result:
        notes.append("stdout still contains a tab character.")
    return False, mismatch(
        "stdout is not the detabbed text (tab stops every {} columns).".format(
            tabstop
        ),
        got=result,
        wanted=expected,
        tabstop=tabstop,
        notes=notes,
    )
