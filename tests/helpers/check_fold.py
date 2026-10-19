"""Check fold output. Word-boundary wraps have expected files; long words do not."""

from expand import display_length
from pretty import mismatch


def check_golden(got, expected):
    if got == expected:
        return True, ""
    return False, mismatch(
        "output does not match the expected wrapping.",
        got=got,
        wanted=expected,
        tabstop=8,
    )


def check_long_word(original, result, fold_col, tabstop):
    def sig(s):
        return "".join(ch for ch in s if not ch.isspace())

    if sig(original) != sig(result):
        return False, mismatch(
            "non-whitespace characters were lost or reordered.",
            got=sig(result),
            wanted=sig(original),
            tabstop=tabstop,
        )

    # Any wrap is fine; also fine to leave an over-long token on one line.
    for line in result.splitlines():
        if display_length(line, tabstop) > fold_col:
            # Allowed only when this line is a single run with no blank/tab.
            if (" " in line) or ("\t" in line):
                return False, (
                    "a line is longer than {} columns and still contains a blank "
                    "or tab, so it could have been folded at whitespace"
                ).format(fold_col)
    return True, ""
